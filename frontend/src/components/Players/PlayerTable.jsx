import { useState } from "react";

import classes from "./PlayerTable.module.css";
import ViewButton from "../Button/ViewButton";
import Modal from "../UI/Modal";
import PlayerForm from "./PlayerForm";
import { fetchWithAuth } from "../../utils/FetchClient";
import { toast } from "react-toastify";
import { getUserRole } from "../../utils/Authentication";
import DeleteButton from "../Button/DeleteButton";
import CancelButton from "../Button/CancelButton";

function PlayerTable({ players = [], onRefetchData }) {
  const role = getUserRole();
  const [isModalViewOpen, setIsModalViewOpen] = useState(false);
  const [isModalEditOpen, setIsModalEditOpen] = useState(false);
  const [isModalDeleteOpen, setIsModalDeleteOpen] = useState(false);
  const [isFetchingPlayerData, setIsFetchingPlayerData] = useState(false);
  const [playerData, setPlayerData] = useState(null);
  const [isSubmittingEdit, setIsSubmittingEdit] = useState(false);
  const [isDeletingPlayer, setIsDeletingPlayer] = useState(false);
  const [playerId, setPlayerId] = useState("null");

  const handleViewPlayer = (playerId) => {
    setIsModalViewOpen(true);
    fetchPlayerData(playerId);
  };

  const handleEditPlayer = (playerId) => {
    setIsModalEditOpen(true);
    fetchPlayerData(playerId);
  };

  const handleDeletePlayer = (playerId) => {
    setIsModalDeleteOpen(true);
    setPlayerId(playerId);
  };

  const handleSubmitEdit = async (formData) => {
    const formDataToSend = {
      ...formData,
      is_active: formData.is_active === "active" ? true : false,
    };

    try {
      setIsSubmittingEdit(true);
      const response = await fetchWithAuth(
        `/api/teams/players/${formDataToSend.id}/`,
        {
          method: "PUT",
          body: JSON.stringify(formDataToSend),
        }
      );
      if (!response.ok) {
        toast.error("Failed to edit player!");
      }

      if (response.ok) {
        toast.success("Player edited successfully!");
        onRefetchData();
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsSubmittingEdit(false);
    }
  };

  const confirmDeletePlayer = async () => {
    try {
      setIsDeletingPlayer(true);
      const response = await fetchWithAuth(`/api/teams/players/${playerId}/`, {
        method: "DELETE",
      });

      if (!response.ok) {
        toast.error(`Failed to delete player: ${response.statusText}`);
      }

      if (response.ok) {
        toast.success("Player deleted successfully!");
        onRefetchData();
      }
    } catch (error) {
      console.error("Error deleting player:", error);
    } finally {
      setIsDeletingPlayer(false);
    }
  };

  const fetchPlayerData = async (playerId) => {
    try {
      setIsFetchingPlayerData(true);
      const res = await fetchWithAuth(`/api/teams/players/${playerId}`);
      const data = await res.json();
      if (!res.ok) toast.error("Failed to fetch player data!");

      if (res.ok) {
        setPlayerData(data);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsFetchingPlayerData(false);
    }
  };

  return (
    <>
      {players.length === 0 && (
        <p style={{ color: "#000", textAlign: "center" }}>
          No players available.
        </p>
      )}
      {players.length > 0 && (
        <table>
          <thead>
            <tr>
              <th>No</th>
              <th>Player Name</th>
              <th>Team Name</th>
              <th>Jersey Number</th>
              <th>Position</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {players.map((player, index) => (
              <tr key={player.id}>
                <td>{index + 1}</td>
                <td>
                  {player.first_name} {player.last_name}
                </td>
                <td>{player.team_name}</td>
                <td>{player.jersey_number}</td>
                <td>{player.position}</td>
                <td>{player.is_active === true ? "Active" : "Inactive"}</td>
                <td>
                  {(role === "admin" || role === "team_captain") &&
                  window.location.pathname.includes("/my-teams/") ? (
                    <>
                      <ViewButton
                        style={{ marginRight: "10px" }}
                        onClick={() => handleEditPlayer(player.id)}
                      >
                        Edit
                      </ViewButton>
                      <DeleteButton
                        onClick={() => handleDeletePlayer(player.id)}
                      >
                        Delete
                      </DeleteButton>
                    </>
                  ) : (
                    <>
                      <ViewButton onClick={() => handleViewPlayer(player.id)}>
                        View
                      </ViewButton>
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* VIEW PLAYER MODAL */}
      <Modal
        open={isModalViewOpen}
        onClose={() => setIsModalViewOpen(false)}
        className={classes.modalContainer}
      >
        <PlayerForm
          initialData={playerData}
          onClose={() => setIsModalViewOpen(false)}
          loading={isFetchingPlayerData}
        />
      </Modal>

      {/* EDIT PLAYER MODAL */}
      <Modal
        open={isModalEditOpen}
        onClose={() => setIsModalEditOpen(false)}
        className={classes.modalContainer}
      >
        <PlayerForm
          initialData={playerData}
          onClose={() => setIsModalEditOpen(false)}
          onSubmit={handleSubmitEdit}
          allowedEdit
          loading={isSubmittingEdit}
        />
      </Modal>

      {/* Delete Modal */}
      <Modal
        className={classes.modalContainer}
        open={isModalDeleteOpen}
        onClose={() => setIsModalDeleteOpen(false)}
      >
        <p>Are you sure you want to delete this player?</p>
        <DeleteButton
          style={{ marginRight: "10px" }}
          onClick={confirmDeletePlayer}
        >
          Yes, Delete
        </DeleteButton>
        <CancelButton onClick={() => setIsModalDeleteOpen(false)}>
          Cancel
        </CancelButton>
      </Modal>
    </>
  );
}

export default PlayerTable;
