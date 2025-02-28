import { useEffect, useState } from "react";
import classes from "../components/Table.module.css";
import { fetchWithAuth } from "../utils/FetchClient";

import StatusChip from "./StatusChip"; // Import StatusChip
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
     <div className={classes.tableWrapper}>
         <table className={classes.modernTable}>
           <thead>
             <tr>
             <th>No</th>
<th>Name</th>
<th>Description</th>
<th>Location</th>
<th>Start Date</th>
<th>End Date</th>
<th>Status</th>
             </tr>
           </thead>
           <tbody>
             {events.map((event, index) => (
               <tr key={index}>
                <td>{index + 1}</td>
                 <td>
                   <span>{event.name}</span>
                 </td>
                 <td>{event.description}</td>
                 <td>{event.location}</td>
                 <td>{event.start_date}</td>
                 <td>{event.end_date}</td>
                 <td style={{ textAlign: "center", width: "120px" }}> {/* Fixed width */}
                <StatusChip status={event.status} />
              </td>
               </tr>
             ))}
           </tbody>
         </table>
       </div>
  );
}

export default EventTable;


