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

function PublicDashboard() {
  const [events, setEvents] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  async function fetchData() {
    try {
      setIsLoading(true);
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

      // Format the dates in the event list
      const formattedEvents = data.results.map(event => ({
        ...event,
        start_date: formatDate(event.start_date),
        end_date: formatDate(event.end_date),
      }));

      setEvents(formattedEvents);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    fetchData();
  }, []);

  // Function to format the date from "YYYY-MM-DD" to "MMM DD"
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
  };

  const upcomingMatches = [
    { date: "Mar 10", time: "18:00", teams: "Team A vs Team B", location: "Berlin Stadium" },
    { date: "Mar 12", time: "20:30", teams: "Team C vs Team D", location: "Munich Arena" },
    { date: "Mar 15", time: "17:00", teams: "Team E vs Team F", location: "Hamburg Dome" }
  ];

  return (
    <div className={styles.dashboard}>
      <div className={styles.gridContainer}>
        {/* Public Events */}
        <div className={`${styles.card} ${styles.tallCard}`}>
          <FaCalendarAlt className={styles.icon} />
          <h3>Public Events</h3>
          {isLoading ? (
            <p>Loading events...</p>
          ) : (
            <table className={styles.table}>
              <thead>
                <tr>
                  <th style={{ textAlign: "center" }}>Name</th>
                  <th style={{ textAlign: "center" }}>Location</th>
                  <th style={{ textAlign: "center" }}>Start Date</th>
                  <th style={{ textAlign: "center" }}>End Date</th>
                  <th>Year</th>
                  <th style={{ textAlign: "center" }}>No. of sport events</th>
                  <th style={{ textAlign: "center" }}>Status</th>
                </tr>
              </thead>
              <tbody>
                {events.map((event, index) => (
                  <tr key={index}>
                    <td style={{ textAlign: "center" }}>{event.name}</td>
                    <td style={{ textAlign: "center" }}>{event.location}</td>
                    <td style={{ textAlign: "center" }}>{event.start_date}</td>
                    <td style={{ textAlign: "center" }}>{event.end_date}</td>
                    <td>2025</td>
                    <td style={{ textAlign: "center" }}>{event.sport_events_count}</td>
                    <td style={{ textAlign: "center" }}>
                      <StatusChip status={event.status_display} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* Live Scores with Circular Progress */}
        <div className={`${styles.card} ${styles.wideCard}`}>
          <FaClock className={styles.icon} />
          <h3>Real-time scores and updates</h3>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Date</th>
                <th>Time</th>
                <th>Match</th>
                <th>Year</th>
                <th>Location</th>
              </tr>
            </thead>
            <tbody>
              {upcomingMatches.map((match, index) => (
                <tr key={index}>
                  <td>{match.date}</td>
                  <td>{match.time}</td>
                  <td>{match.teams}</td>
                  <td>2025</td>
                  <td>{match.location}</td>
              
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Leaderboard */}
        <div className={`${styles.card} ${styles.tallCard}`}>
          <FaList className={styles.icon} />
          <h3>Leaderboard</h3>
          <div className={styles.leaderboardChart}></div>
        </div>

        {/* Event Winner */}
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

        {/* Standings and Rankings */}
        <div className={`${styles.card} ${styles.wideCard}`}>
          <FaUsers className={styles.icon} />
          <h2>Standings and final rankings</h2>
          <p>Warriors | Captain: John Doe</p>
        </div>

        {/* Upcoming Matches Section */}
        <div className={`${styles.card} ${styles.wideCard}`}>
          <FaCalendarAlt className={styles.icon} />
          <h2>Upcoming Matches</h2>
        </div>
      </div>
    </div>
  );
}

export default PublicDashboard;
