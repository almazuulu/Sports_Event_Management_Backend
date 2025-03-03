import { useState } from "react";
import { useNavigate } from "react-router-dom";

import CreateEventForm from "../components/CreateEventForm";
import Header from "../components/Header";
import { toast } from "react-toastify";
import { fetchWithAuth } from "../utils/FetchClient";
import classes from "./NewEvent.module.css";

function NewEventPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleCreateEvent = async (formData) => {
    setLoading(true);
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
        toast.success("New user created successfully!");
        navigate("..");
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={classes.container}>
      <Header title="Create New Event" />
      <CreateEventForm onSubmit={handleCreateEvent} loading={loading} />
    </div>
  );
}

export default NewEventPage;
