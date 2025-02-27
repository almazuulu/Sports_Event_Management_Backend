// src/components/Dashboard.js
import React from "react";
import Card from "../components/Cardnew";
import Table from "./Table";
import "../styles/Dashboard.css";
import Navbar from "../pages/Navbar";
import  EventCard from "../pages/Eventcard"
import SportsCard from "./Matches";

const Dashboard = () => {
  return (
   <div>
     <Navbar/>
  
    <div className="dashboard">
      
      <h2></h2>

      <div className="dashboard-cards">
       <Card/>

      </div>

      <div className="dashboard-content">
        <div className="table-container">
          <h3>My Teams</h3>
          <Table />
        </div>
        
        <div className="events">
        <EventCard/>
        </div>
      </div>

      <div className="sports-info">
        <div className="info-box">
          <h3></h3>
          <SportsCard/>
        </div>
       
      </div>
    </div>
    </div>
  );
};

export default Dashboard;
