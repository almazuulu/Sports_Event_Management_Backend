import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { toast } from "react-toastify";

import classes from "./TeamDetails.module.css";
import { fetchWithAuth } from "../utils/FetchClient";
import LoadingScreen from "../components/UI/LoadingScreen";
import Header from "../components/Header";
import ViewTeamForm from "../components/Teams/ViewTeamForm";

function TeamDetailsPage() {
  const { teamId } = useParams();
  const [isFetching, setIsFetching] = useState(false);
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchTeam = async () => {
      try {
        setIsFetching(true);
        const response = await fetchWithAuth(`/api/teams/teams/${teamId}/`);
        const data = await response.json();
        if (!response.ok) return toast.error("Failed to fetch team data");
        if (response.ok) {
          setData(data);
        }
      } catch (error) {
        console.error(error);
      } finally {
        setIsFetching(false);
      }
    };

    fetchTeam();
  }, [teamId]);

  if (isFetching) return <LoadingScreen />;
  return (
    <div className={classes.container}>
      <Header title={data.name} />
      <div className={classes.card}>
        <ViewTeamForm initialData={data} />
      </div>
    </div>
  );
}

export default TeamDetailsPage;
