import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import classes from "./UserTable.module.css";
import { fetchWithAuth } from "../utils/FetchClient";
import Modal from "./UI/Modal";
import { toast } from "react-toastify";
import DeleteButton from "./Button/DeleteButton";
import CancelButton from "./Button/CancelButton";

const ROLE_LABELS = {
  admin: "Administrator",
  team_captain: "Team Captain",
  scorekeeper: "Scorekeeper",
  public: "Public User",
};

const getRoleLabel = (role) => ROLE_LABELS[role];

function UserTable() {
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedUserId, setSelectedUserId] = useState("");

  const handleDeleteUser = (userId) => {
    setSelectedUserId(userId);
    setIsModalOpen(true);
  };

  const confirmDelete = async () => {
    try {
      const response = await fetchWithAuth(`/api/users/${selectedUserId}/`, {
        method: "DELETE",
      });

      if (!response.ok) {
        toast.error(`Failed to delete user: ${response.statusText}`);
      }

      if (response.ok) {
        toast.success("User deleted successfully!");
        fetchUsersData();
      }
    } catch (error) {
      console.error("Error deleting user:", error);
    } finally {
      setIsModalOpen(false);
    }
  };

  const fetchUsersData = async () => {
    try {
      setIsLoading(true);
      const response = await fetchWithAuth("/api/users/?page=1");

      if (!response.ok) {
        toast.error("Failed to fetch users data");
      }

      const data = await response.json();
      setUsers(data.results);
    } catch (error) {
      console.error("Error fetching user data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchUsersData();
  }, []);

  return (
    <div>
      <table className={classes.table}>
        <thead>
          <tr>
            <th className={classes.th}>No</th>
            <th className={classes.th}>Full Name</th>
            <th className={classes.th}>Username</th>
            <th className={classes.th}>Email</th>
            <th className={classes.th}>Role</th>
            <th className={classes.th}>Action</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user, index) => (
            <tr key={user.id}>
              <td className={classes.td}>{index + 1}</td>
              <td
                className={classes.td}
              >{`${user.first_name} ${user.last_name}`}</td>
              <td className={classes.td}>{user.username}</td>
              <td className={classes.td}>{user.email}</td>
              <td className={classes.td}>{getRoleLabel(user.role)}</td>
              <td className={classes.td}>
                <section className={classes.actionsButton}>
                  <button
                    className={classes.editButton}
                    onClick={() => navigate(`${user.id}`)}
                  >
                    View
                  </button>
                  <button
                    className={classes.deleteButton}
                    onClick={() => handleDeleteUser(user.id)}
                  >
                    Delete
                  </button>

                  <Modal
                    open={isModalOpen}
                    onClose={() => setIsModalOpen(false)}
                  >
                    <p>Are you sure you want to delete this user?</p>
                    <DeleteButton onClick={confirmDelete}>
                      Yes, Delete
                    </DeleteButton>
                    <CancelButton onClick={() => setIsModalOpen(false)}>
                      Cancel
                    </CancelButton>
                  </Modal>
                </section>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default UserTable;
