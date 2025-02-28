// src/components/Dashboard.js
import Card from "../components/Cardnew";
import Table from "../components/Table";
import classes from "../styles/Dashboard.module.css";
import Navbar from "../components/Navbar";
import  EventCard from "../components/EventCard";
import SportsCard from "../components/Matches";

const Dashboard = () => {
  return (
   <div>
     <Navbar/>
  
    <div className={classes.dashboard}>
      
      <h2></h2>

      <div className={classes.dashboardCards}>
       <Card/>

      </div>

      <div className={classes.dashboardContent}>
        <div className={classes.tableContainer}>
          <h3>My Teams</h3>
          <Table />
        </div>
        
        <div className={classes.events}>
        <h3>Public Events</h3>
        <EventCard/>
        </div>
      </div>

      <div className={classes.sportsInfo}>
        <div className={classes.infoBox}>
          <h3></h3>
          <SportsCard/>
        </div>
       
      </div>
    </div>
    </div>
  );
};

export default Dashboard;
