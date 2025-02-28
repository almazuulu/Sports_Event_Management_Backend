import { useEffect, useState } from "react";

import classes from "./NewSportEvent.module.css";
import Header from "../components/Header";
import { fetchWithAuth } from "../utils/FetchClient";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import SportEventForm from "../components/SportEvents/SportEventForm";

function NewSportEventPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [eventList, setEventList] = useState([]);

  const handleCreateSportEvent = async (formData) => {
    setLoading(true);
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
        toast.success("New sport event created successfully!");
        navigate("..");
      }
    } catch (error) {
      console.error(error);
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

  useEffect(() => {
    fetchEventsList();
  }, []);

  return (
    <div className={classes.container}>
      <Header title={"Create New Sport Event"} />
      <SportEventForm
        onSubmit={handleCreateSportEvent}
        loading={loading}
        allowEdit
        eventList={eventList}
      />
    </div>
  );
}

export default NewSportEventPage;
