import { useState } from "react";
import { toast } from "react-toastify";

import classes from "./UserTable.module.css";
import { fetchWithAuth } from "../utils/FetchClient";
import Modal from "./UI/Modal";
import DeleteButton from "./Button/DeleteButton";
import CancelButton from "./Button/CancelButton";
import { ROLE_LABELS } from "../constant";
import ViewButton from "./Button/ViewButton";
import CreateUserForm from "./CreateUserForm";

const getRoleLabel = (role) => ROLE_LABELS[role];

function UserTable({ userList = [], onRefetchData, roles = [] }) {
  const [selectedUserId, setSelectedUserId] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [isFetching, setIsFetching] = useState(false);
  const [userData, setUserData] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const handleEdit = (userId) => {
    setIsEditing(true);
    fetchUserData(userId);
    setSelectedUserId(userId);
  };

  const handleDelete = (userId) => {
    setIsDeleting(true);
    setSelectedUserId(userId);
  };

  const confirmDelete = async () => {
    try {
      setIsDeleting(true);
      const response = await fetchWithAuth(`/api/users/${selectedUserId}/`, {
        method: "DELETE",
      });

      if (!response.ok) {
        toast.error(`Failed to delete user: ${response.statusText}`);
      }

      if (response.ok) {
        toast.success("User deleted successfully!");
        onRefetchData();
      }
    } catch (error) {
      console.error("Error deleting user:", error);
    } finally {
      setIsDeleting(false);
    }
  };

  const fetchUserData = async (userId) => {
    try {
      setIsFetching(true);
      const response = await fetchWithAuth(`/api/users/${userId}/`);
      const data = await response.json();
      if (!response.ok) toast.error("Failed to sport event");

      if (response.ok) {
        setUserData(data);
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
      const response = await fetchWithAuth(`/api/users/${selectedUserId}/`, {
        method: "PUT",
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        toast.error("Failed to update user!");
      }

      if (response.ok) {
        toast.success("User updated successfully!");
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
      <div>
        <table>
          <thead>
            <tr>
              <th>No</th>
              <th>Full Name</th>
              <th>Username</th>
              <th>Email</th>
              <th>Role</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {userList.map((user, index) => (
              <tr key={user.id}>
                <td>{index + 1}</td>
                <td>{`${user.first_name} ${user.last_name}`}</td>
                <td>{user.username}</td>
                <td>{user.email}</td>
                <td>{getRoleLabel(user.role)}</td>
                <td style={{ width: "200px" }}>
                  <ViewButton
                    style={{ marginRight: "10px" }}
                    onClick={() => handleEdit(`${user.id}`)}
                  >
                    Edit
                  </ViewButton>
                  <DeleteButton onClick={() => handleDelete(user.id)}>
                    Delete
                  </DeleteButton>
                </td>
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
        <CreateUserForm
          initialData={userData}
          onClose={() => setIsEditing(false)}
          loading={isFetching}
          roles={roles}
          isEdit={true}
          onSubmit={handleSubmitEdit}
        />
      </Modal>

      {/* Delete Modal */}
      <Modal
        className={classes.modalContainer}
        open={isDeleting}
        onClose={() => setIsDeleting(false)}
      >
        <p>Are you sure you want to delete this user?</p>
        <DeleteButton style={{ marginRight: "10px" }} onClick={confirmDelete}>
          Yes, Delete
        </DeleteButton>
        <CancelButton onClick={() => setIsDeleting(false)}>Cancel</CancelButton>
      </Modal>
    </>
  );
}

export default UserTable;
