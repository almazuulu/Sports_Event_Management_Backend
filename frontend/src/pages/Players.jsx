import React, { useEffect, useState } from "react";

import classes from "./Players.module.css";
import Header from "../components/Header";
import PlayerTable from "../components/Players/PlayerTable";
import { fetchWithAuth } from "../utils/FetchClient";
import { toast } from "react-toastify";
import LoadingScreen from "../components/UI/LoadingScreen";

function PlayersPage() {
  const [players, setPlayers] = useState([]);
  const [isFetching, setIsFetching] = useState(false);

  const fetchAllPlayers = async () => {
    try {
      setIsFetching(true);
      const response = await fetchWithAuth("/api/teams/players/");
      const data = await response.json();
      if (!response.ok) toast.error("Failed to fetch players!");
      if (response.ok) {
        setPlayers(data.results);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsFetching(false);
    }
  };

  useEffect(() => {
    fetchAllPlayers();
  }, []);

  if (isFetching) return <LoadingScreen />;

  return (
    <div className={classes.container}>
      <Header title={"All Players"} />
      <div className={classes.card}>
        <PlayerTable players={players} />
      </div>
    </div>
  );
}

export default PlayersPage;
