import classes from "./Dashboard.module.css";
import Card from "../../components/Card";
import Table from "../../components/Table";
import EventCard from "../../components/EventCard";

const DUMMY_DATA = [
  { title: "Total Sport Events", count: "12" },
  { title: "Ongoing Events", count: "4" },
  { title: "Completed Events", count: "8" },
  { title: "Upcoming Matches", count: "6" },
];
const DashboardPage = () => {
  return (
    <div className={classes.dashboard}>
      <div className={classes.cardsContainer}>
        {DUMMY_DATA.map((card) => (
          <Card key={card.title} {...card} />
        ))}
      </div>

      <div className={classes.dashboardContent}>
        <div className={classes.tableContainer}>
          <p className={classes.tableTitle}>Teams</p>
          <Table />
        </div>

        <div className={classes.tableContainer}>
          <p className={classes.tableTitle}>Events</p>
          <EventCard />
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
