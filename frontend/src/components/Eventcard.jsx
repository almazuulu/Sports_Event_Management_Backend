// src/components/EventCard.js
import { useEffect, useState } from "react";
import classes from "../components/Table.module.css";


function EventCard() {

  const [events, setEvents] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  async function fetchData() {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/events/events/public/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log(data);
      setEvents(data.results);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  }
  useEffect(() => {
    fetchData();
  }, []);
  // Call the function
  return (

    <div className={classes.tableWrapper}>
      <table className={classes.modernTable}>
        <thead>
          <tr>
            <th>No</th>
            <th>Name</th>
            <th>location</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Status</th>

          </tr>
        </thead>
        <tbody>
          {events.map((events, index) => (
            <tr key={events.id}>
              <td>{index + 1}</td>
              <td>
                <div className={classes.teamInfo}>

                  <span>{events.name}</span>
                </div>
              </td>
              <td>
                <span>{events.location}</span>
              </td>
              <td>{events.start_date}</td>
              <td>{events.end_date}</td>
              <td>{events.status_display}</td>

            </tr>
          ))}
        </tbody>
      </table>
    </div>

  );

}
export default EventCard;
