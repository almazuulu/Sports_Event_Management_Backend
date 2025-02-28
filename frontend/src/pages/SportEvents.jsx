import { useEffect, useState } from "react";
import { toast } from "react-toastify";

import SportEventTable from "../components/SportEventTable";
import Header from "../components/Header";
import LoadingScreen from "../components/UI/LoadingScreen";
import { fetchWithAuth } from "../utils/FetchClient";
import classes from "./SportEvents.module.css";

function SportEventsPage() {
  const [sportEventList, setSportEventList] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchSportEvents = async () => {
    try {
      setLoading(true);
      const response = await fetchWithAuth("/api/events/sport-events/");

      const data = await response.json();

      if (!response.ok) {
        toast.error("Failed to fetch data");
      }

      if (response.ok) {
        setSportEventList(data.results);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSportEvents();
  }, []);

  if (loading) return <LoadingScreen />;

  return (
    <div className={classes.container}>
      <Header title={"All Sport Events"} />
      <div className={classes.card}>
        <SportEventTable sportEventList={sportEventList}/>
      </div>
    </div>
  );
}

export default SportEventsPage;
