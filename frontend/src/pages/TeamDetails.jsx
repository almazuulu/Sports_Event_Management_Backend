import { useCallback, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { toast } from "react-toastify";

import classes from "./TeamDetails.module.css";
import { fetchWithAuth } from "../utils/FetchClient";
import LoadingScreen from "../components/UI/LoadingScreen";
import Header from "../components/Header";
import ViewTeamForm from "../components/Teams/ViewTeamForm";
import { getUserRole } from "../utils/Authentication";
import CreateButton from "../components/Button/CreateButton";
import Modal from "../components/UI/Modal";
import NewTeamForm from "../components/Teams/NewTeamForm";
import DeleteButton from "../components/Button/DeleteButton";
import CancelButton from "../components/Button/CancelButton";
import PlayerTable from "../components/Players/PlayerTable";
import SportEventTable from "../components/SportEvents/SportEventTable";
import PlayerForm from "../components/Players/PlayerForm";
import RegisterSportEventForm from "../components/SportEvents/RegisterSportEventForm";
import JoinedSportEventTable from "../components/Teams/JoinedSportEventTable";

function TeamDetailsPage() {
  const role = getUserRole();
  const navigate = useNavigate();
  const { teamId } = useParams();
  const [isFetchingTeam, setIsFetchingTeam] = useState(false);
  const [isFetchingPlayers, setIsFetchingPlayers] = useState(false);
  const [isFetchingJoinedSportEvents, setIsFetchingJoinedSportEvents] =
    useState(false);
  const [team, setTeam] = useState([]);
  const [players, setPlayers] = useState([]);
  const [sportEvents, setSportEvents] = useState([]);
  const [sportEventsJoined, setSportEventsJoined] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmittingNewPlayer, setIsSubmittingNewPlayer] = useState(false);
  const [isSubmittingJoinSportEvent, setIsSubmittingJoinSportEvent] =
    useState(false);
  const [isModalDeleteOpen, setIsModalDeleteOpen] = useState(false);
  const [isModalAddPlayerOpen, setIsModalAddPlayerOpen] = useState(false);
  const [isModalJoinSportEventsOpen, setIsModalJoinSportEventsOpen] =
    useState(false);
  const [activeTab, setActiveTab] = useState("info");
  const [isFetchingSportEvents, setIsFetchingSportEvents] = useState(false);

  const handleEdit = () => {
    setIsModalOpen((prevData) => !prevData);
  };

  const handleDelete = () => {
    setIsModalDeleteOpen(true);
  };

  const handleAddPlayer = () => {
    setIsModalAddPlayerOpen(true);
  };

  const handleJoinSportEvents = () => {
    setIsModalJoinSportEventsOpen(true);
  };

  const confirmDelete = async () => {
    try {
      const response = await fetchWithAuth(`/api/teams/teams/${teamId}/`, {
        method: "DELETE",
      });

      if (!response.ok) {
        toast.error(`Failed to delete team ${teamId}`);
      }

      if (response.ok) {
        toast.success("Team deleted successfully!");
        navigate("..");
      }
    } catch (error) {
      console.error("Error deleting team:", error);
    } finally {
      setIsModalDeleteOpen(false);
    }
  };

  const handleSubmit = async (formData) => {
    try {
      setIsSubmitting(true);
      const response = await fetchWithAuth(`/api/teams/teams/${teamId}/`, {
        method: "PUT",
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        toast.error("Failed to update new team!");
      }

      if (response.ok) {
        toast.success("Team updated successfully!");
        fetchTeam();
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSubmitAddPlayer = async (formData) => {
    const formDataToSend = {
      ...formData,
      team: teamId,
      is_active: formData.is_active === "active" ? true : false,
    };

    try {
      setIsSubmittingNewPlayer(true);
      const response = await fetchWithAuth("/api/teams/players/", {
        method: "POST",
        body: JSON.stringify(formDataToSend),
      });

      if (!response.ok) {
        toast.error("Failed to add new player!");
      }

      if (response.ok) {
        toast.success("New player added successfully!");
        fetchPlayers();
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsSubmittingNewPlayer(false);
    }
  };

  const handleSubmitJoinSportEvent = async (formData) => {
    const formDataToSend = {
      ...formData,
      team: teamId,
    };
    try {
      setIsSubmittingJoinSportEvent(true);
      const response = await fetchWithAuth(
        `/api/teams/teams/${formDataToSend.team}/registrations/`,
        {
          method: "POST",
          body: JSON.stringify(formDataToSend),
        }
      );

      if (!response.ok) {
        toast.error("Failed to register sport events!");
      }

      if (response.ok) {
        toast.success("Sport events registered successfully!");
        fetchSportEventsJoined();
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsSubmittingJoinSportEvent(false);
    }
  };

  const fetchTeam = useCallback(async () => {
    try {
      setIsFetchingTeam(true);
      const response = await fetchWithAuth(`/api/teams/teams/${teamId}/`);
      const data = await response.json();

      if (!response.ok) {
        return toast.error("Failed to fetch team data");
      }

      setTeam(data);
    } catch (error) {
      console.error(error);
    } finally {
      setIsFetchingTeam(false);
    }
  }, [teamId]);

  const fetchPlayers = useCallback(async () => {
    try {
      setIsFetchingPlayers(true);
      const response = await fetchWithAuth(
        `/api/teams/teams/${teamId}/players/`
      );
      const data = await response.json();

      if (!response.ok) {
        return toast.error("Failed to fetch team data");
      }

      if (response.ok) {
        setPlayers(data.results);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsFetchingPlayers(false);
    }
  }, [teamId]);

  const fetchSportEventsJoined = useCallback(async () => {
    try {
      setIsFetchingJoinedSportEvents(true);
      const response = await fetchWithAuth(
        `/api/teams/teams/${teamId}/registrations/`
      );
      const data = await response.json();

      if (!response.ok) {
        return toast.error("Failed to fetch joined sport events data");
      }

      if (response.ok) {
        setSportEventsJoined(data.results);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsFetchingJoinedSportEvents(false);
    }
  }, [teamId]);

  useEffect(() => {
    const fetchSportEvents = async () => {
      try {
        setIsFetchingSportEvents(true);
        const response = await fetchWithAuth("/api/events/sport-events/");

        if (!response.ok) {
          toast.error("Failed to fetch sport events data");
        }

        const data = await response.json();
        setSportEvents(data.results);
      } catch (error) {
        console.error("Error fetching sport events data:", error);
      } finally {
        setIsFetchingSportEvents(false);
      }
    };

    fetchSportEvents();
  }, []);

  useEffect(() => {
    fetchTeam();
    fetchPlayers();
    fetchSportEventsJoined();
  }, [fetchTeam, fetchPlayers, fetchSportEventsJoined]);

  if (isFetchingTeam && isFetchingJoinedSportEvents && isFetchingPlayers)
    return <LoadingScreen />;

  return (
    <>
      <div className={classes.container}>
        <Header title={team.name} enableBack />

        <div className={classes.tabsContainer}>
          <button
            type="button"
            className={
              activeTab === "info"
                ? `${classes.tabsButton} ${classes.active}`
                : classes.tabsButton
            }
            onClick={() => setActiveTab("info")}
          >
            Team Info
          </button>
          <button
            type="button"
            className={
              activeTab === "players"
                ? `${classes.tabsButton} ${classes.active}`
                : classes.tabsButton
            }
            onClick={() => setActiveTab("players")}
          >
            Team Players
          </button>
          <button
            type="button"
            className={
              activeTab === "sport-events"
                ? `${classes.tabsButton} ${classes.active}`
                : classes.tabsButton
            }
            onClick={() => setActiveTab("sport-events")}
          >
            Sport Events
          </button>
        </div>

        <div className={classes.card}>
          {activeTab === "info" && (
            <>
              {(role === "admin" || role === "team_captain") &&
                window.location.pathname.includes("/my-teams/") && (
                  <section className={classes.sectionButton}>
                    <CreateButton
                      style={{ marginRight: "10px" }}
                      onClick={handleEdit}
                    >
                      Edit
                    </CreateButton>
                    <DeleteButton onClick={handleDelete}>Delete</DeleteButton>
                  </section>
                )}
              <ViewTeamForm initialData={team} />
            </>
          )}

          {activeTab === "players" && (
            <>
              {(role === "admin" || role === "team_captain") &&
                window.location.pathname.includes("/my-teams/") && (
                  <section className={classes.sectionButton}>
                    <CreateButton
                      style={{ marginRight: "10px" }}
                      onClick={handleAddPlayer}
                    >
                      Add Player
                    </CreateButton>
                  </section>
                )}
              {players.length === 0 && <p>No players available.</p>}
              {players.length > 0 && (
                <PlayerTable players={players} onRefetchData={fetchPlayers} />
              )}
            </>
          )}

          {/* ONLY TEAM CAPTAIN AND ADMIN CAN VIEW */}
          {activeTab === "sport-events" && (
            <>
              {role === "team_captain" &&
                window.location.pathname.includes("/my-teams/") && (
                  <section className={classes.sectionButton}>
                    <CreateButton
                      style={{ marginRight: "10px" }}
                      onClick={handleJoinSportEvents}
                    >
                      Join Sport Events
                    </CreateButton>
                  </section>
                )}
              {sportEventsJoined.length === 0 && <p>No sport events joined.</p>}
              {sportEventsJoined.length > 0 && (
                <JoinedSportEventTable sportEventList={sportEventsJoined} />
              )}
            </>
          )}
        </div>
      </div>

      {/* EDIT MODAL */}
      <Modal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        className={classes.modalContainer}
      >
        <NewTeamForm
          onSubmit={handleSubmit}
          loading={isSubmitting}
          onClose={() => setIsModalOpen(false)}
          initialData={{
            // logo: data.logo,
            name: team.name,
            description: team.description,
            contact_email: team.contact_email,
            contact_phone: team.contact_phone,
          }}
        />
      </Modal>

      {/* DELETE MODAL */}
      <Modal
        open={isModalDeleteOpen}
        onClose={() => setIsModalDeleteOpen(false)}
        className={classes.modalContainer}
      >
        <p>Are you sure you want to delete this team?</p>
        <CreateButton style={{ marginRight: "10px" }} onClick={confirmDelete}>
          Yes
        </CreateButton>
        <CancelButton onClick={() => setIsModalOpen(false)} />
      </Modal>

      {/* ADD PLAYER MODAL */}
      <Modal
        open={isModalAddPlayerOpen}
        onClose={() => setIsModalAddPlayerOpen(false)}
        className={classes.modalContainer}
      >
        <PlayerForm
          onSubmit={handleSubmitAddPlayer}
          teamId={teamId}
          onClose={() => setIsModalAddPlayerOpen(false)}
          allowedEdit
          loading={isSubmittingNewPlayer}
        />
      </Modal>

      {/* JOIN SPORT EVENTS MODAL */}
      <Modal
        open={isModalJoinSportEventsOpen}
        onClose={() => setIsModalJoinSportEventsOpen(false)}
        className={classes.modalContainer}
      >
        <RegisterSportEventForm
          onSubmit={handleSubmitJoinSportEvent}
          loading={isSubmittingJoinSportEvent}
          onClose={() => setIsModalJoinSportEventsOpen(false)}
          sportEvents={sportEvents}
        />
      </Modal>
    </>
  );
}

export default TeamDetailsPage;
