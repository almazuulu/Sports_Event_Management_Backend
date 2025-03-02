import { useNavigate } from "react-router-dom";

import ActionButton from "../components/ActionButton";
import EventTable from "../components/EventTable";
import classes from "./Users.module.css";
import CreateButton from "../components/Button/CreateButton";

function EventsPage() {
  const navigate = useNavigate();
  const handleClick = () => {
    navigate("create-new");
  };

  return (
    <div className={classes.container}>
      <h1>List of Events</h1>
      <div className={classes.card}>
        <section className={classes.sectionButton}>
          <CreateButton title={"Create New Event"} onClick={handleClick} />
        </section>
        <EventTable />
      </div>
    </div>
  );
}

export default EventsPage;
