import classes from "../components/Table.module.css";

// icons
import { FaUsers } from "react-icons/fa";

const teams = [
  {
    name: "Gilgit",
    sport: "Football",
    members: 2,
    wins: 1,
    losses: 1,
    rating: 8,
  },
  {
    name: "Naryn",
    sport: "Football",
    members: 2,
    wins: 0,
    losses: 1,
    rating: 2,
  },
  {
    name: "Hawks",
    sport: "Basketball",
    members: 1,
    wins: 0,
    losses: 0,
    rating: 0,
  },
  {
    name: "Khorog",
    sport: "Football",
    members: 2,
    wins: 1,
    losses: 0,
    rating: 6,
  },
  {
    name: "Pamir",
    sport: "Football",
    members: 1,
    wins: 0,
    losses: 0,
    rating: 0,
  },
];

const Table = () => {
  return (
    <div className={classes.tableWrapper}>
      <table>
        <thead>
          <tr>
            <th>Team Name</th>
            <th>Sport</th>
            <th>Members</th>
            <th>Wins</th>
            <th>Losses</th>
            <th>Rating points</th>
          </tr>
        </thead>
        <tbody>
          {teams.map((team, index) => (
            <tr key={index}>
              <td>
                <div className={classes.teamInfo}>
                  <div className={classes.teamIconWrapper}>
                    <FaUsers className={classes.teamIcon} />{" "}
                  </div>
                  <span>{team.name}</span>
                </div>
              </td>
              <td>
                <span>{team.sport}</span>
              </td>
              <td>{team.members}</td>
              <td>{team.wins}</td>
              <td>{team.losses}</td>
              <td className={classes.rating}>{team.rating}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Table;
