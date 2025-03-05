import { formatToShortDate } from "../../utils/helpers";
import StatusChip from "../StatusChip";

function JoinedSportEventTable({ sportEventList = [] }) {
  return (
    <table>
      <thead>
        <tr>
          <th>No</th>
          <th>Sport Event Name</th>
          <th>Registration Date</th>
          <th>Notes</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {sportEventList.map((data, index) => (
          <tr key={data.id}>
            <td>{index + 1}</td>
            <td>{data.sport_event_name}</td>
            <td>{formatToShortDate(data.registration_date)}</td>
            <td>{data.notes}</td>
            <td style={{ width: "200px" }}>
              <StatusChip status={data.status} />
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default JoinedSportEventTable;
