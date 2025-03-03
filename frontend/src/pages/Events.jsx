import { useEffect, useState } from "react";
import { toast } from "react-toastify";

import EventTable from "../components/EventTable";
import CreateButton from "../components/Button/CreateButton";
import Header from "../components/Header";
import Modal from "../components/UI/Modal";
import CreateEventForm from "../components/CreateEventForm";
import { fetchWithAuth } from "../utils/FetchClient";
import { getUserRole } from "../utils/Authentication";
import LoadingScreen from "../components/UI/LoadingScreen";
import classes from "./Users.module.css";

function EventsPage() {
  const role = getUserRole();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [eventList, setEventList] = useState([]);
  const [isFetching, setIsFetching] = useState(false);

  const handleCreateNew = () => {
    setIsModalOpen(true);
  };

  const handleSubmitNewEvent = async (formData) => {
    setIsSubmitting(true);
    try {
      const response = await fetchWithAuth("/api/events/events/", {
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
        fetchEventsData();
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const fetchEventsData = async () => {
    try {
      setIsFetching(true);
      const response = await fetchWithAuth("/api/events/events/");

      const data = await response.json();

      if (!response.ok) {
        toast.error("Failed to fetch events data");
      }

      if (response.ok) {
        setEventList(data.results);
      }
    } catch (error) {
      console.error("Error fetching events data:", error);
    } finally {
      setIsFetching(false);
    }
  };

  useEffect(() => {
    fetchEventsData();
  }, []);

  if (isFetching) return <LoadingScreen />;

  return (
    <>
      <div className={classes.container}>
        <Header title={"All Events"} />
        <div className={classes.card}>
          {role === "admin" && (
            <section className={classes.sectionButton}>
              <CreateButton
                title={"Create New Event"}
                onClick={handleCreateNew}
              />
            </section>
          )}
          <EventTable eventList={eventList} onRefetchData={fetchEventsData}/>
        </div>
      </div>

      <Modal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        className={classes.modalContainer}
      >
        <CreateEventForm
          onSubmit={handleSubmitNewEvent}
          loading={isSubmitting}
          onClose={() => setIsModalOpen(false)}
        />
      </Modal>
    </>
  );
}

export default EventsPage;
