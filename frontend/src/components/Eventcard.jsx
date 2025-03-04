import { useEffect, useState } from "react";

import StatusChip from "./StatusChip";
import classes from "../components/Table.module.css";
import { formatToShortDate } from "../utils/helpers";

function EventCard() {
  const [events, setEvents] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  async function fetchData() {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/events/events/public/"
      );

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
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
      <table>
        <thead>
          <tr>
            <th>No</th>
            <th>Name</th>
            <th>Location</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {events.map((event, index) => (
            <tr key={event.id}>
              <td>{index + 1}</td>
              <td>{event.name}</td>
              <td>{event.location}</td>
              <td>{formatToShortDate(event.start_date)}</td>
              <td>{formatToShortDate(event.end_date)}</td>
              <td style={{ textAlign: "center", width: "120px" }}>
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
