import React from "react";
import TeamStatusChip from "./TeamStatusChip";
import ViewButton from "../Button/ViewButton";
import { useNavigate } from "react-router-dom";

function TeamTable({ teams = [], onRefetchData }) {
  const navigate = useNavigate();

  const handleView = (teamId) => {
    navigate(`${teamId}`);
  };

  return (
    <>
      <div>
        <table>
          <thead>
            <tr>
              <th>No</th>
              <th>Team Name</th>
              <th>Team Logo</th>
              <th>Team Captain</th>
              <th>Contact Info</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {teams.map((team, index) => (
              <tr key={team.id}>
                <td>{index + 1}</td>
                <td>{team.name}</td>
                <td>
                  {" "}
                  <img
                    src={team.logo ? team.logo : "https://placehold.co/400"}
                    alt="Team Logo"
                    width="50"
                    height="50"
                  />
                </td>
                <td>
                  {team.captain.first_name} {team.captain.last_name}
                </td>
                <td style={{ textAlign: "left" }}>
                  <p>Email: {team.contact_email}</p>
                  <p>Phone: {team.contact_phone}</p>
                </td>
                <td>
                  <TeamStatusChip status={team.status} />
                </td>
                <td>
                  <ViewButton onClick={() => handleView(team.id)}>
                    View Details
                  </ViewButton>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}

export default TeamTable;
