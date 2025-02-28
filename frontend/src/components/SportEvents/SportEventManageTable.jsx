import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

import { fetchWithAuth } from "../../utils/FetchClient";
import ViewButton from "../Button/ViewButton";
import Modal from "../UI/Modal";
import CreateButton from "../Button/CreateButton";
import CancelButton from "../Button/CancelButton";
import DeleteButton from "../Button/DeleteButton";

function SportEventManageTable({ data, onRefresh }) {
  const navigate = useNavigate();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedSportEventId, setSelectedSportEventId] = useState("");

  const handleDelete = (userId) => {
    setSelectedSportEventId(userId);
    setIsModalOpen(true);
  };

  const confirmDelete = async () => {
    try {
      const response = await fetchWithAuth(
        `/api/events/sport-events/${selectedSportEventId}/`,
        {
          method: "DELETE",
        }
      );

      if (!response.ok) {
        toast.error(`Failed to delete sport event: ${response.statusText}`);
      }

      if (response.ok) {
        toast.success("Sport event deleted successfully!");
        onRefresh();
      }
    } catch (error) {
      console.error("Error deleting sport event:", error);
    } finally {
      setIsModalOpen(false);
    }
  };

  return (
    <div>
      <table>
        <thead>
          <tr>
            <th>No</th>
            <th>Sport Event Name</th>
            <th>Sport Type</th>
            <th>Event Name</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {data.map((sport, index) => (
            <tr key={sport.id}>
              <td>{index + 1}</td>
              <td>{sport.name}</td>
              <td>{sport.sport_type_display}</td>
              <td>{sport.event_name}</td>
              <td>{sport.start_date}</td>
              <td>{sport.end_date}</td>
              <td>{sport.status_display}</td>
              <td>
                <ViewButton
                  style={{ marginRight: "10px" }}
                  onClick={() => navigate(`${sport.id}`)}
                />
                <DeleteButton onClick={() => handleDelete(sport.id)} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <Modal open={isModalOpen} onClose={() => setIsModalOpen(false)}>
        <p>Are you sure you want to delete?</p>
        <CreateButton style={{ marginRight: "10px" }} onClick={confirmDelete}>
          Yes
        </CreateButton>
        <CancelButton onClick={() => setIsModalOpen(false)} />
      </Modal>
    </div>
  );
}

export default SportEventManageTable;
