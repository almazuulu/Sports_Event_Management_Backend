import { useState } from "react";
import { toast } from "react-toastify";

import { getUserRole } from "../utils/Authentication";
import DeleteButton from "./Button/DeleteButton";
import ViewButton from "./Button/ViewButton";
import StatusChip from "./StatusChip";
import Modal from "./UI/Modal";
import CreateEventForm from "./CreateEventForm";
import { fetchWithAuth } from "../utils/FetchClient";
import CancelButton from "./Button/CancelButton";
import classes from "../components/Table.module.css";

function EventTable({ eventList = [], onRefetchData }) {
  const role = getUserRole();
  const [isEditing, setIsEditing] = useState(false);
  const [isFetching, setIsFetching] = useState(false);
  const [eventData, setEventData] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [eventId, setEventId] = useState("");
  const [isDeleting, setIsDeleting] = useState(false);

  const handleEdit = (eventId) => {
    setIsEditing(true);
    fetchEvent(eventId);
    setEventId(eventId);
  };

  const handleDelete = (eventId) => {
    setIsDeleting(true);
    setEventId(eventId);
  };

  const confirmDelete = async () => {
    try {
      setIsDeleting(true);
      const response = await fetchWithAuth(`/api/events/events/${eventId}/`, {
        method: "DELETE",
      });

      if (!response.ok) toast.error("Failed to delete event");

      if (response.ok) {
        toast.success("Event deleted successfully!");
        onRefetchData();
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsDeleting(false);
    }
  };

  const fetchEvent = async (eventId) => {
    try {
      setIsFetching(true);
      const response = await fetchWithAuth(`/api/events/events/${eventId}`);
      const data = await response.json();
      if (!response.ok) toast.error("Failed to sport event");

      if (response.ok) {
        setEventData(data);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsFetching(false);
    }
  };

  const handleSubmitEdit = async (formData) => {
    try {
      setIsSubmitting(true);
      const response = await fetchWithAuth(`/api/events/events/${eventId}/`, {
        method: "PUT",
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        toast.error("Failed to update event!");
      }

      if (response.ok) {
        toast.success("Event updated successfully!");
        setIsEditing(false);
        onRefetchData();
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <div className={classes.tableWrapper}>
        <table className={classes.modernTable}>
          <thead>
            <tr>
              <th>No</th>
              <th>Name</th>
              {/* <th>Description</th> */}
              <th>Location</th>
              <th>Start Date</th>
              <th>End Date</th>
              <th>Status</th>
              {role === "admin" && <th>Action</th>}
            </tr>
          </thead>
          <tbody>
            {eventList.map((event, index) => (
              <tr key={index}>
                <td>{index + 1}</td>
                <td>
                  <span>{event.name}</span>
                </td>
                {/* <td>{event.description}</td> */}
                <td>{event.location}</td>
                <td>{event.start_date}</td>
                <td>{event.end_date}</td>
                <td style={{ textAlign: "center", width: "120px" }}>
                  {" "}
                  <StatusChip status={event.status} />
                </td>
                {role === "admin" && (
                  <td style={{ width: "200px" }}>
                    <ViewButton
                      style={{ marginRight: "10px" }}
                      onClick={() => handleEdit(event.id)}
                    >
                      Edit
                    </ViewButton>
                    <DeleteButton onClick={() => handleDelete(event.id)} />
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* View Modal */}
      <Modal
        className={classes.modalContainer}
        open={isEditing}
        onClose={() => setIsEditing(false)}
      >
        <CreateEventForm
          initialData={eventData}
          onClose={() => setIsEditing(false)}
          loading={isFetching}
          onSubmit={handleSubmitEdit}
        />
      </Modal>

      {/* Delete Modal */}
      <Modal
        className={classes.modalContainer}
        open={isDeleting}
        onClose={() => setIsDeleting(false)}
      >
        <p>Are you sure you want to delete this event?</p>
        <DeleteButton style={{ marginRight: "10px" }} onClick={confirmDelete}>
          Yes, Delete
        </DeleteButton>
        <CancelButton onClick={() => setIsDeleting(false)}>Cancel</CancelButton>
      </Modal>
    </>
  );
}

export default EventTable;
