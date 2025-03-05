import { useEffect, useState } from "react";
import { toast } from "react-toastify";

import classes from "./SportEventTable.module.css";
import ViewButton from "../Button/ViewButton";
import StatusChip from "../StatusChip";
import { getUserRole } from "../../utils/Authentication";
import DeleteButton from "../Button/DeleteButton";
import { fetchWithAuth } from "../../utils/FetchClient";
import Modal from "../UI/Modal";
import SportEventForm from "./SportEventForm";
import CancelButton from "../Button/CancelButton";
import { formatToShortDate } from "../../utils/helpers";

function SportEventTable({ sportEventList = [], onRefetchData }) {
  const role = getUserRole();
  const [isEditing, setIsEditing] = useState(false);
  const [sportEventId, setSportEventId] = useState("");
  const [isDeleting, setIsDeleting] = useState(false);
  const [isFetching, setIsFetching] = useState(false);
  const [sportEventData, setSportEventData] = useState(null);
  const [eventList, setEventList] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleEdit = (sportEventId) => {
    setIsEditing(true);
    fetchEventSport(sportEventId);
    setSportEventId(sportEventId);
  };

  const handleDelete = (sportEventId) => {
    setIsDeleting(true);
    setSportEventId(sportEventId);
  };

  const confirmDelete = async () => {
    try {
      setIsDeleting(true);
      const response = await fetchWithAuth(
        `/api/events/sport-events/${sportEventId}/`,
        {
          method: "DELETE",
        }
      );

      if (!response.ok) toast.error("Failed to delete sport event!");

      if (response.ok) {
        toast.success("Sport event deleted successfully!");
        onRefetchData();
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsDeleting(false);
    }
  };

  const fetchEventSport = async (sportEventId) => {
    try {
      setIsFetching(true);
      const response = await fetchWithAuth(
        `/api/events/sport-events/${sportEventId}`
      );
      const data = await response.json();
      if (!response.ok) toast.error("Failed to sport event");

      if (response.ok) {
        setSportEventData(data);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsFetching(false);
    }
  };

  const fetchEventsList = async () => {
    try {
      const response = await fetchWithAuth("/api/events/events/");

      const data = await response.json();

      if (!response.ok) toast.error("Failed to fetch events!");

      if (response.ok) {
        setEventList(data.results);
      }
    } catch (error) {
      console.error(error);
    }
  };

  const handleSubmitEdit = async (formData) => {
    try {
      setIsSubmitting(true);
      const response = await fetchWithAuth(
        `/api/events/sport-events/${sportEventId}/`,
        {
          method: "PUT",
          body: JSON.stringify(formData),
        }
      );
      const data = await response.json();

      if (!response.ok) {
        toast.error("Failed to update sport event!");
      }

      if (response.ok) {
        toast.success("Sport event updated successfully!");
        setIsEditing(false);
        onRefetchData();

        return { success: true, data };
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  useEffect(() => {
    fetchEventsList();
  }, []);

  return (
    <>
      <div>
        <table>
          <thead>
            <tr>
              <th>No</th>
              <th>Name</th>
              <th>Event</th>
              <th>Sport Type</th>
              <th>Start Date</th>
              <th>End Date</th>
              <th>Status</th>
              {role === "admin" &&
                window.location.pathname.includes("/admin-panel/") && (
                  <th>Action</th>
                )}
            </tr>
          </thead>
          <tbody>
            {sportEventList.map((data, index) => (
              <tr key={data.id}>
                <td>{index + 1}</td>
                <td>{data.name}</td>
                <td>{data.event_name}</td>
                <td>{data.sport_type_display}</td>
                <td>{formatToShortDate(data.start_date)}</td>
                <td>{formatToShortDate(data.end_date)}</td>
                <td style={{ width: "200px" }}>
                  <StatusChip status={data.status} />
                </td>
                {role === "admin" &&
                  window.location.pathname.includes("/admin-panel/") && (
                    <td style={{ width: "200px" }}>
                      <ViewButton
                        style={{ marginRight: "10px" }}
                        onClick={() => handleEdit(`${data.id}`)}
                      >
                        Edit
                      </ViewButton>
                      <DeleteButton onClick={() => handleDelete(data.id)} />
                    </td>
                  )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* EDIT MODAL */}
      <Modal
        className={classes.modalContainer}
        open={isEditing}
        onClose={() => setIsEditing(false)}
      >
        <SportEventForm
          initialData={sportEventData}
          onClose={() => setIsEditing(false)}
          loading={isFetching}
          eventList={eventList}
          onSubmit={handleSubmitEdit}
        />
      </Modal>

      {/* Delete Modal */}
      <Modal
        className={classes.modalContainer}
        open={isDeleting}
        onClose={() => setIsDeleting(false)}
      >
        <p>Are you sure you want to delete this sport event?</p>
        <DeleteButton style={{ marginRight: "10px" }} onClick={confirmDelete}>
          Yes, Delete
        </DeleteButton>
        <CancelButton onClick={() => setIsDeleting(false)}>Cancel</CancelButton>
      </Modal>
    </>
  );
}

export default SportEventTable;
