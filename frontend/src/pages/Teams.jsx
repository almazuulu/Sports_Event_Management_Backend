import { useEffect, useState } from "react";

import classes from "./Teams.module.css";
import Header from "../components/Header";
import TeamTable from "../components/Teams/TeamTable";
import { fetchWithAuth } from "../utils/FetchClient";
import { toast } from "react-toastify";
import LoadingScreen from "../components/UI/LoadingScreen";

function TeamsPage() {
  const [teams, setTeams] = useState([]);
  const [isFetchingTeams, setIsFetchingTeams] = useState(false);

  const fetchAllTeams = async () => {
    try {
      setIsFetchingTeams(true);
      const response = await fetchWithAuth("/api/teams/public/teams/");
      const data = await response.json();
      if (!response.ok) return toast.error("Failed to fetch teams");
      if (response.ok) {
        console.log(data)
        setTeams(data);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsFetchingTeams(false);
    }
  };

  useEffect(() => {
    fetchAllTeams();
  }, []);

  if (isFetchingTeams) return <LoadingScreen />;

  return (
    <>
      <div className={classes.container}>
        <Header title={"All Teams"} />
        <div className={classes.card}>
          <TeamTable teams={teams} />
        </div>
      </div>
    </>
  );
}

export default TeamsPage;
