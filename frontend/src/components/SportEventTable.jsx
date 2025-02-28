import { useNavigate } from "react-router-dom";

import ViewButton from "./Button/ViewButton";

function SportEventTable({ sportEventList = [] }) {
  const navigate = useNavigate();

  return (
    <div>
      <table>
        <thead>
          <tr>
            <th>No</th>
            <th>Name</th>
            <th>Event</th>
            <th>Sport Type</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {sportEventList.map((data, index) => (
            <tr key={data.id}>
              <td>{index + 1}</td>
              <td>{data.name}</td>
              <td>{data.event_name}</td>
              <td>{data.sport_type_display}</td>
              <td>{data.status_display}</td>
              <td>
                <ViewButton onClick={() => navigate(`${data.id}`)}>
                  View
                </ViewButton>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default SportEventTable;
