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
  const [sportevents, setSportevents] = useState([]);
  const [team, setTeam] = useState([]);
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


      // Format the dates in the event list
      const formattedEvents = data.results.map(event => ({
        ...event,
        start_date: formatDate(event.start_date),
        end_date: formatDate(event.end_date),
        year: getYear(event.start_date),
      }));

      setEvents(formattedEvents);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  }


  async function fetchsportData() {
    try {
      setIsLoading(true);
      const response = await fetch("http://127.0.0.1:8000/api/events/sport-events/public/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();


      // Format the dates in the event list
      const formattedsportEvents = data.results.map(event => ({
        ...event,
        start_date: formatDate(event.start_date),
        end_date: formatDate(event.end_date),
        year: getYear(event.start_date),
      }));

      setSportevents(formattedsportEvents);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  }

  async function TeamData() {
    try {
      setIsLoading(true);
      const response = await fetch("http://127.0.0.1:8000/api/teams/public/teams/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();



      setTeam(data);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    fetchData();
    fetchsportData();
    TeamData();
  }, []);

  // Function to format the date from "YYYY-MM-DD" to "MMM DD"
  const formatDate = (dateString) => {
    if (!dateString) return "";

    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", { month: "short", day: "numeric" }); // Example: Mar 10
  };

  const getYear = (dateString) => {
    if (!dateString) return "";

    return new Date(dateString).getFullYear(); // Example: 2025
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
                  <th>Name</th>
                  <th>Location</th>
                  <th >Start Date</th>
                  <th >End Date</th>
                  <th>Year</th>
                  <th >No. of sport events</th>
                  <th >Status</th>
                </tr>
              </thead>
              <tbody>
                {events.map((event, index) => (
                  <tr key={index}>
                    <td>{event.name}</td>
                    <td >{event.location}</td>
                    <td >{event.start_date}</td>
                    <td >{event.end_date}</td>
                    <td>{event.year}</td>
                    <td>{event.sport_events_count}</td>
                    <td>
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
          <h3>Sport Events</h3>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Sport Name</th>
                <th>Type</th>
                <th>Event Name</th>
                <th>Start Date</th>
                <th>End Date</th>
                <th>Year</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {sportevents.map((match, index) => (
                <tr key={index}>
                  <td>{match.name}</td>
                  <td>{match.sport_type}</td>
                  <td>{match.event_name}</td>
                  <td>{match.start_date}</td>
                  <td>{match.end_date}</td>
                  <td>{match.year}</td>
                  <td> <StatusChip status={match.status} /></td>

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
        <div className={`${styles.card} ${styles.tallCard}`}>
          <FaUsers className={styles.icon} />
          <h2>Team</h2>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Team</th>
                <th>Caption</th>
                <th >Logo</th>

              </tr>
            </thead>
            <tbody>
              {team.map((t, index) => (
                <tr key={index}>
                  <td>{t.name}</td>
                  <td >{t.captain_name}</td>
                  <td>
                    {/* <div className={styles.teamLogoContainer}> */}
                    <FaUsers className={styles.teamIcon} />
                    {t.logo}
                    {/* </div> */}
                  </td>


                </tr>
              ))}
            </tbody>
          </table>
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
