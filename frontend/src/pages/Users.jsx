import { useNavigate } from "react-router-dom";

import ActionButton from "../components/ActionButton";
import UserTable from "../components/UserTable";
import classes from "./Users.module.css";

function UsersPage() {
  const navigate = useNavigate();
  const handleClick = () => {
    navigate("create-user");
  };

  return (
    <div className={classes.container}>
      <h1>List of Users</h1>
      <div className={classes.card}>
        <section className={classes.sectionButton}>
          <ActionButton title={"Create New User"} onClick={handleClick} />
        </section>
        <UserTable />
      </div>
    </div>
  );
}

export default UsersPage;
