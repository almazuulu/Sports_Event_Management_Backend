import classes from  "../components/Matches.module.css";

const SportsCards = () => {
  return (
    <div className={classes.sportsContainer}>
      {/* My Single-Player Sports Card */}
      <div className={classes.sportsCard}>
        <div className={classes.cardHeader}>
          <h3>Upcoming Matches</h3>
          <span className={classes.menuIcon}>⋮</span>
        </div>
        <table>
          <thead>
            <tr>
              <th>Sport Name</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Chess</td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* My Team-Player Sports Card */}
      <div className={classes.sportsCard}>
        <div className={classes.cardHeader}>
          <h3>Ongoing Matches</h3>
          <span className={classes.menuIcon}>⋮</span>
        </div>
        <table>
          <thead>
            <tr>
              <th>Sport</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Football</td>
            </tr>
            <tr>
              <td>Basketball</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default SportsCards;
