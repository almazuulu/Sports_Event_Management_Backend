import { useEffect, useState } from "react";
import { toast } from "react-toastify";

import classes from "./Users.module.css";
import EventTable from "../components/EventTable";
import Header from "../components/Header";
import { fetchWithAuth } from "../utils/FetchClient";
import LoadingScreen from "../components/UI/LoadingScreen";

function EventsPage() {
  const [eventList, setEventList] = useState([]);
  const [isFetching, setIsFetching] = useState(false);

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
    <div className={classes.container}>
      <Header title={"All Events"} />
      <div className={classes.card}>
        <EventTable eventList={eventList} onRefetchData={fetchEventsData} />
      </div>
    </div>
  );
}

export default EventsPage;
