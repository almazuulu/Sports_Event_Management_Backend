import Header from "../components/Header";
import UserTable from "../components/UserTable";
import classes from "./Users.module.css";

function UsersPage() {
  return (
    <div className={classes.container}>
      <Header title={'All Users'}/>
      <div className={classes.card}>
        <UserTable />
      </div>
    </div>
  );
}

export default UsersPage;
