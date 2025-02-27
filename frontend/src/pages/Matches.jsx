import React from "react";
import "../pages/Matches.css";

const SportsCards = () => {
  return (
    <div className="sports-container">
      {/* My Single-Player Sports Card */}
      <div className="sports-card">
        <div className="card-header">
          <h3>My Single-Player Sports</h3>
          <span className="menu-icon">⋮</span>
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
      <div className="sports-card">
        <div className="card-header">
          <h3>My Team-Player Sports</h3>
          <span className="menu-icon">⋮</span>
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
