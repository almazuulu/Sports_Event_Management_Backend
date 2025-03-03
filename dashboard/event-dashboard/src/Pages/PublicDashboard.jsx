// src/components/Dashboard.js
import Card from "../components/Cardnew";

import classes from "../Pages/Dashboard.module.css";
import Navbar from "../components/Navbar";
import  EventCard from "../components/EventCard";


const PublicDashboard = () => {
  return (
   <div>
     <Navbar/>
  
    <div className={classes.dashboard}>
      
      <h2></h2>

      <div className={classes.dashboardCards}>
       <Card/>

      </div>

      <div className={classes.dashboardContent}>
       
        
        <div className={classes.events}>
        <h3>Public Events</h3>
        <EventCard/>
        </div>
      </div>

     
    </div>
    </div>
  );
};

export default PublicDashboard;
