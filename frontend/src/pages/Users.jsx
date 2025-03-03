import { useEffect, useState } from "react";
import { toast } from "react-toastify";

import classes from "./Users.module.css";
import CreateButton from "../components/Button/CreateButton";
import Header from "../components/Header";
import UserTable from "../components/UserTable";
import { fetchWithAuth } from "../utils/FetchClient";
import Modal from "../components/UI/Modal";
import CreateUserForm from "../components/CreateUserForm";
import LoadingScreen from "../components/UI/LoadingScreen";

function UsersPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isFetching, setIsFetching] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);

  const handleCreateNew = () => {
    setIsModalOpen(true);
  };

  const handleSubmitNewUser = async (formData) => {
    setIsSubmitting(true);
    try {
      const response = await fetchWithAuth("/api/users/", {
        method: "POST",
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        toast.error(
          <div>
            <strong>Failed to submit form:</strong>
            <ul>
              {Object.entries(data).map(([field, messages]) => (
                <li key={field}>
                  <strong>{field}:</strong> {messages.join(", ")}
                </li>
              ))}
            </ul>
          </div>
        );
      }

      if (response.ok) {
        toast.success("New user created successfully!");
        fetchUsersData();
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const fetchUsersData = async () => {
    try {
      setIsFetching(true);
      const response = await fetchWithAuth("/api/users/?page=1");
      const data = await response.json();

      if (!response.ok) {
        toast.error("Failed to fetch users data");
      }

      if (response.ok) {
        setUsers(data.results);
      }
    } catch (error) {
      console.error("Error fetching user data:", error);
    } finally {
      setIsFetching(false);
    }
  };

  const fetchUserRoles = async () => {
    try {
      const response = await fetchWithAuth("/api/users/roles");
      const data = await response.json();

      if (!response.ok) toast.error("Failed to fetch roles!");

      if (response.ok) {
        setRoles(data);
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchUsersData();
    fetchUserRoles();
  }, []);

  if (isFetching) return <LoadingScreen />;

  return (
    <>
      <div className={classes.container}>
        <Header title={"All Users"} />
        <div className={classes.card}>
          <section className={classes.sectionButton}>
            <CreateButton onClick={handleCreateNew}>
              Create New User
            </CreateButton>
          </section>
          <UserTable
            userList={users}
            onRefetchData={fetchUsersData}
            roles={roles}
          />
        </div>
      </div>

      <Modal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        className={classes.modalContainer}
      >
        <CreateUserForm
          onSubmit={handleSubmitNewUser}
          loading={isSubmitting}
          onClose={() => setIsModalOpen(false)}
          roles={roles}
        />
      </Modal>
    </>
  );
}

export default UsersPage;
