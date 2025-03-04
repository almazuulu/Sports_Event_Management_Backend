import { useEffect, useState } from "react";
import {
  FaTrophy,
  FaCalendarAlt,
  FaFutbol,
  FaUsers,
  FaChartBar,
  FaClock,
  FaList
} from "react-icons/fa";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";
import styles from "../Pages/Dashboard.module.css";
import StatusChip from "../components/StatusChip"; 

function PublicDashboard () {
    const [events, setEvents] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
  
    async function fetchData() {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/events/events/public/", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });
  
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
  
        const data = await response.json();
        console.log(data);
        setEvents(data.results);
      } catch (error) {
        console.error("Error:", error);
      } finally {
        setIsLoading(false);
      }
    }
  
    useEffect(() => {
      fetchData();
    }, []);
  
  const upcomingMatches = [
    { date: "Mar 10", time: "18:00", teams: "Team A vs Team B", location: "Berlin Stadium" },
    { date: "Mar 12", time: "20:30", teams: "Team C vs Team D", location: "Munich Arena" },
    { date: "Mar 15", time: "17:00", teams: "Team E vs Team F", location: "Hamburg Dome" }
  ];
  return (
    <div className={styles.dashboard}>
      <div className={styles.gridContainer}>

        {/* Large Header Card */}
       

        {/* Upcoming Matches */}
        <div className={`${styles.card} ${styles.tallCard}`}>
        <FaCalendarAlt className={styles.icon} />
          <h3>Public Events</h3>
          <table className={styles.table}>
            <thead>
              <tr>
              {/* <th>No</th> */}
            <th>Name</th>
            <th>Location</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>No.of sport events</th>
            <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {events.map((match, index) => (
                <tr key={index}>
                  {/* <td>{index + 1}</td> */}
                  <td>{match.name}</td>
                  <td>{match.location}</td>
                  <td>{match.start_date}</td>
                  <td>{match.end_date}</td>
                  <td>{match.sport_events_count}</td>
                  <td style={{ textAlign: "center", width: "120px" }}> {/* Fixed width */}
                <StatusChip status={match.status_display} />
              </td>
                  
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Live Scores with Circular Progress */}
        <div className={`${styles.card} ${styles.wideCard}`}>
          <FaClock className={styles.icon} />
          <h3>Real time scores and updates</h3>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Date</th>
                <th>Time</th>
                <th>Match</th>
                <th>Location</th>
              </tr>
            </thead>
            <tbody>
              {upcomingMatches.map((match, index) => (
                <tr key={index}>
                  <td>{match.date}</td>
                  <td>{match.time}</td>
                  <td>{match.teams}</td>
                  <td>{match.location}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Leaderboard with Mini Bar Chart */}
        <div className={`${styles.card} ${styles.tallCard}`}>
          <FaList className={styles.icon} />
          <h3>Leaderboard</h3>
          <div className={styles.leaderboardChart}>
           
           
           
          </div>
        </div>

        {/* Event Winners */}
        <div className={`${styles.card} ${styles.smallCard}`}>
          <FaTrophy className={styles.icon} />
          <h3>Event Winner</h3>
          <p>Team X</p>
        </div>

        {/* Sport Events */}
        <div className={`${styles.card} ${styles.smallCard}`}>
          <FaFutbol className={styles.icon} />
          <h3>Live Score</h3>
          <p>Basketball | March 12 - 18</p>
        </div>

        {/* Team Information */}
        <div className={`${styles.card} ${styles.wideCard}`}>
          <FaUsers className={styles.icon} />
          <h2>Standings and final rankings</h2>
          <p>Warriors | Captain: John Doe</p>
        </div>
        <div className={`${styles.card} ${styles.wideCard}`}>
          <FaCalendarAlt className={styles.icon} />
          <h2>Upcoming Matches</h2>
        
        </div>
      </div>
    </div>
  );
};

export default PublicDashboard;
