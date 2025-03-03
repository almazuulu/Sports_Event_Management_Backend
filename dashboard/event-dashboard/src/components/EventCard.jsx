// src/components/EventCard.jsx
import { useEffect, useState } from "react";
import StatusChip from "./StatusChip"; // Import StatusChip
import classes from "../components/EventCard.module.css";

function EventCard() {
  const [events, setEvents] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  async function fetchData() {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/events/events/public/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log(data);
      setEvents(data.results);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className={classes.tableWrapper}>
      <table className={classes.modernTable}>
        <thead>
          <tr>
            <th>No</th>
            <th>Name</th>
            <th>Location</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th style={{ width: "120px" }}>Status</th> {/* Fixed width for Status column */}
          </tr>
        </thead>
        <tbody>
          {events.map((event, index) => (
            <tr key={event.id}>
              <td>{index + 1}</td>
              <td>
                <div className={classes.teamInfo}>
                  <span>{event.name}</span>
                </div>
              </td>
              <td>
                <span>{event.location}</span>
              </td>
              <td>{event.start_date}</td>
              <td>{event.end_date}</td>
              <td style={{ textAlign: "center", width: "120px" }}> {/* Fixed width */}
                <StatusChip status={event.status_display} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default EventCard;
