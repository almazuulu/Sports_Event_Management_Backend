import React from "react";
import { useNavigate } from "react-router-dom";

import ActionButton from "../components/ActionButton";
import classes from "./SportEvents.module.css";
import SportEventTable from "../components/SportEventTable";

function SportEventsPage() {
  const navigate = useNavigate();
  const handleClick = () => {
    navigate("create-new");
  };

  return (
    <div className={classes.container}>
      <h1>List of Sport Events</h1>
      <div className={classes.card}>
        <section className={classes.sectionButton}>
          <ActionButton
            title={"Create New Sport Event"}
            onClick={handleClick}
          />
        </section>
        <SportEventTable />
      </div>
    </div>
  );
}

export default SportEventsPage;
