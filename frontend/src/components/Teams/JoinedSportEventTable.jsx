import StatusChip from "../StatusChip";

function JoinedSportEventTable({ sportEventList = [] }) {
  const formattedDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };
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
            <td>{formattedDate(data.registration_date)}</td>
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
