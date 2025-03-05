import { useEffect, useState } from "react";
import { toast } from "react-toastify";

import classes from "./ManageSportEvents.module.css";
import Header from "../../components/Header";
import { getUserRole } from "../../utils/Authentication";
import CreateButton from "../../components/Button/CreateButton";
import SportEventTable from "../../components/SportEvents/SportEventTable";
import Modal from "../../components/UI/Modal";
import SportEventForm from "../../components/SportEvents/SportEventForm";
import LoadingScreen from "../../components/UI/LoadingScreen";
import { fetchWithAuth } from "../../utils/FetchClient";

function ManageSportEventsPage() {
  const role = getUserRole();
  const [sportEventList, setSportEventList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [eventList, setEventList] = useState([]);

  const handleCreateNew = () => {
    setIsModalOpen(true);
  };

  const handleSubmitNewSportEvent = async (formData) => {
    setIsSubmitting(true);
    try {
      const response = await fetchWithAuth("/api/events/sport-events/", {
        method: "POST",
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        toast.error(
          <div>
            <strong>Failed to submit form:</strong>
            <ul>
              {Object.entries(data).map(([field, messages]) => (
                <li key={field}>
                  <strong>{field}:</strong> {messages.join(", ")}
                </li>
              ))}
            </ul>
          </div>
        );
      }

      if (response.ok) {
        toast.success("New event created successfully!");
        fetchSportEvents();
        setIsModalOpen(false);

        return { success: true, data };
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const fetchSportEvents = async () => {
    try {
      setLoading(true);
      const response = await fetchWithAuth("/api/events/sport-events/");

      const data = await response.json();

      if (!response.ok) {
        toast.error("Failed to fetch data");
      }

      if (response.ok) {
        setSportEventList(data.results);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchEventsList = async () => {
    try {
      const response = await fetchWithAuth("/api/events/events/");

      const data = await response.json();

      if (!response.ok) toast.error("Failed to fetch events!");

      if (response.ok) {
        setEventList(data.results);
      }
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {}, []);

  useEffect(() => {
    fetchEventsList();
    fetchSportEvents();
  }, []);

  return (
    <>
      <div className={classes.container}>
        <Header title={"Manage Sport Events"} />
        {loading ? (
          <LoadingScreen />
        ) : (
          <div className={classes.card}>
            {role === "admin" && (
              <section className={classes.sectionButton}>
                <CreateButton
                  title={"Create New Sport Event"}
                  onClick={handleCreateNew}
                />
              </section>
            )}
            <SportEventTable
              sportEventList={sportEventList}
              onRefetchData={fetchSportEvents}
            />
          </div>
        )}
      </div>

      <Modal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        className={classes.modalContainer}
      >
        <SportEventForm
          onSubmit={handleSubmitNewSportEvent}
          loading={isSubmitting}
          onClose={() => setIsModalOpen(false)}
          eventList={eventList}
        />
      </Modal>
    </>
  );
}

export default ManageSportEventsPage;
