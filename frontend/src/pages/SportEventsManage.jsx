import { useEffect, useState } from "react";
import { toast } from "react-toastify";

import Header from "../components/Header";
import SportEventManageTable from "../components/SportEvents/SportEventManageTable";
import { fetchWithAuth } from "../utils/FetchClient";
import LoadingScreen from "../components/UI/LoadingScreen";
import classes from "./SportEventsManage.module.css";

function SportEventsManagePage() {
  const [sportEventList, setSportEventList] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchSportEvents = async () => {
    try {
      setLoading(true);
      const response = await fetchWithAuth("/api/events/sport-events/");

      if (!response.ok) {
        toast.error("Failed to fetch sport events data");
      }

      const data = await response.json();
      setSportEventList(data.results);
    } catch (error) {
      console.error("Error fetching sport events data:", error);
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
      <Header title={"Manage Sport Events"} />
      <div className={classes.card}>
        <SportEventManageTable
          data={sportEventList}
          onRefresh={fetchSportEvents}
        />
      </div>
    </div>
  );
}

export default SportEventsManagePage;
