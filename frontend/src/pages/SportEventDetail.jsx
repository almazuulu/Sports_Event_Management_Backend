import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { toast } from "react-toastify";

import { fetchWithAuth } from "../utils/FetchClient";
import Header from "../components/Header";
import SportEventForm from "../components/SportEvents/SportEventForm";
import LoadingScreen from "../components/UI/LoadingScreen";
import { getUserRole } from "../utils/Authentication";
import CancelButton from "../components/Button/CancelButton";
import ViewButton from "../components/Button/ViewButton";
import DeleteButton from "../components/Button/DeleteButton";
import Modal from "../components/UI/Modal";
import classes from "./SportEventDetail.module.css";

function SportEventDetailPage() {
  const role = getUserRole();
  const navigate = useNavigate();
  const { sportEventId } = useParams();
  const [data, setData] = useState({});
  const [eventList, setEventList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingUpdate, setLoadingUpdate] = useState(false);
  const [isEdit, setIsEdit] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleEdit = () => {
    setIsEdit((prevData) => !prevData);
  };

  const handleDelete = () => {
    setIsModalOpen(true);
  };

  const handleUpdate = async (formData) => {
    setLoadingUpdate(true);

    try {
      const response = await fetchWithAuth(
        `/api/events/sport-events/${sportEventId}/`,
        {
          method: "PUT",
          body: JSON.stringify(formData),
        }
      );

      if (!response.ok) toast.error("Failed to update sport event!");

      if (response.ok) {
        handleEdit();
        toast.success("Sport event updated successfully!");
      }
    } catch (error) {
      console.error("Error updating sport event", error);
    } finally {
      setLoadingUpdate(false);
    }
  };

  const confirmDelete = async () => {
    try {
      const response = await fetchWithAuth(
        `/api/events/sport-events/${sportEventId}/`,
        {
          method: "DELETE",
        }
      );

      if (!response.ok) {
        toast.error(`Failed to delete sport event: ${response.statusText}`);
      }

      if (response.ok) {
        toast.success("Sport event deleted successfully!");
        navigate("..");
      }
    } catch (error) {
      console.error("Error deleting sport event:", error);
    } finally {
      setIsModalOpen(false);
    }
  };

  useEffect(() => {
    const fetchSportEvent = async () => {
      setLoading(true);
      try {
        const response = await fetchWithAuth(
          `/api/events/sport-events/${sportEventId}`
        );
        const data = await response.json();

        if (!response.ok) toast.error("Failed to sport event");

        if (response.ok) {
          setData(data);
        }
      } catch (error) {
        console.error("Error fetching user:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchSportEvent();
  }, [sportEventId]);

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

  useEffect(() => {
    fetchEventsList();
  }, []);

  if (loading) return <LoadingScreen />;

  return (
    <div className={classes.container}>
      <Header title={data.name} enableBack />
      {role === "admin" && (
        <section className={classes.section}>
          {isEdit ? (
            <CancelButton onClick={handleEdit} />
          ) : (
            <ViewButton onClick={handleEdit}>Edit</ViewButton>
          )}
          <DeleteButton
            onClick={handleDelete}
            style={{ marginLeft: "10px" }}
            disabled={isEdit}
          />
        </section>
      )}
      <SportEventForm
        initialData={data}
        allowEdit={isEdit}
        loading={loadingUpdate}
        onSubmit={handleUpdate}
        eventList={eventList}
      />

      <Modal open={isModalOpen} onClose={() => setIsModalOpen(false)}>
        <p>Are you sure you want to delete this sport event?</p>
        <DeleteButton onClick={confirmDelete}>Yes, Delete</DeleteButton>
        <CancelButton onClick={() => setIsModalOpen(false)}>
          Cancel
        </CancelButton>
      </Modal>
    </div>
  );
}

export default SportEventDetailPage;
