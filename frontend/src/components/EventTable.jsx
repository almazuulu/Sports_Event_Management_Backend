import { useEffect, useState } from "react";
import classes from "./UserTable.module.css";
import { fetchWithAuth } from "../utils/FetchClient";


function EventTable() {
 
  const [events, setEvents] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
 
  const fetchEventsData = async () => {
    try {
      setIsLoading(true);
      const response = await fetchWithAuth("/api/events/events/");

      if (!response.ok) {
        toast.error("Failed to fetch events data");
      }

      const data = await response.json();
      setEvents(data.results);
    } catch (error) {
      console.error("Error fetching events data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchEventsData();
  }, []);

  return (
    <div>
      <table className={classes.table}>
        <thead>
          <tr>
            <th className={classes.th}>No</th>
            <th className={classes.th}>Name</th>
            <th className={classes.th}>Description</th>
            <th className={classes.th}>Location</th>
            <th className={classes.th}>Start Date</th>
            <th className={classes.th}>End Date</th>
            <th className={classes.th}>Status</th>
           
           
           
          </tr>
        </thead>
        <tbody>
          {events.map((event, index) => (
            <tr key={event.id}>
              <td className={classes.td}>{index + 1}</td>
              <td className={classes.td}>{event.name}</td>
              <td className={classes.td}>{event.description}</td>
              <td className={classes.td}>{event.location}</td>
              <td className={classes.td}>{event.start_date}</td>
              <td className={classes.td}>{event.end_date}</td>
              <td className={classes.td}>{event.status}</td>
             
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default EventTable;
