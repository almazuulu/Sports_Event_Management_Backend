import { useNavigate } from "react-router-dom";

import ViewButton from "../Button/ViewButton";
import { getUserRole } from "../../utils/Authentication";

function SportEventTable({ data }) {
  const role = getUserRole();
  const navigate = useNavigate();

  return (
    <div>
      <table>
        <thead>
          <tr>
            <th>No</th>
            <th>Sport Event Name</th>
            <th>Sport Type</th>
            <th>Event Name</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Status</th>
            {role === "admin" && <th>Action</th>}
          </tr>
        </thead>
        <tbody>
          {data.map((sport, index) => (
            <tr key={sport.id}>
              <td>{index + 1}</td>
              <td>{sport.name}</td>
              <td>{sport.sport_type_display}</td>
              <td>{sport.event_name}</td>
              <td>{sport.start_date}</td>
              <td>{sport.end_date}</td>
              <td>{sport.status_display}</td>
              <td>
                <ViewButton
                  style={{ marginRight: "10px" }}
                  onClick={() => navigate(`${sport.id}`)}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default SportEventTable;
