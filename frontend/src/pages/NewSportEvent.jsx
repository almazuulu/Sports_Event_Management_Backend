import React, { useState } from "react";

import classes from "./NewSportEvent.module.css";
import Header from "../components/Header";
import SportEventForm from "../components/SportEventForm";
import { fetchWithAuth } from "../utils/FetchClient";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";

function NewSportEventPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

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

  return (
    <div className={classes.container}>
      <Header title={"Create New Sport Event"} enableBack />
      <SportEventForm onSubmit={handleCreateSportEvent} loading={loading} />
    </div>
  );
}

export default NewSportEventPage;
