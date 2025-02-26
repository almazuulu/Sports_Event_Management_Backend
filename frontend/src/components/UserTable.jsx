import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import classes from "./UserTable.module.css";
import { fetchWithAuth } from "../utils/FetchClient";

function UserTable() {
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleDeleteUser = async (userId) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this user?"
    );
    if (!confirmDelete) return;

    try {
      const response = await fetchWithAuth(`/api/users/${userId}/`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error(`Failed to delete user: ${response.statusText}`);
      }

      const data = await response.json();
      // console.log("User deleted successfully:", data);

      // Optionally, update UI after deletion
      alert("User deleted successfully!");
    } catch (error) {
      console.error("Error deleting user:", error);
      alert("Failed to delete user!");
    }
  };

  useEffect(() => {
    const fetchUsersData = async () => {
      try {
        setIsLoading(true);
        const response = await fetchWithAuth("/api/users/");

        if (!response.ok) {
          alert("Failed to fetch users data");
        }

        const data = await response.json();
        setUsers(data.results);
      } catch (error) {
        console.error("Error fetching user data:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchUsersData();
  }, []);

  if (isLoading) {
    <p>Loading...</p>;
  }

  return (
    <div>
      <table className={classes.table}>
        <thead>
          <tr>
            <th className={classes.th}>No</th>
            <th className={classes.th}>First Name</th>
            <th className={classes.th}>Last Name</th>
            <th className={classes.th}>Email</th>
            <th className={classes.th}>Full Name</th>
            <th className={classes.th}>Role</th>
            <th className={classes.th}>Action</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user, index) => (
            <tr key={user.id}>
              <td className={classes.td}>{index + 1}</td>
              <td className={classes.td}>{user.first_name}</td>
              <td className={classes.td}>{user.last_name}</td>
              <td className={classes.td}>{user.email}</td>
              <td
                className={classes.td}
              >{`${user.first_name} ${user.last_name}`}</td>
              <td className={classes.td}>{user.role}</td>
              <td className={classes.td}>
                <section className={classes.actionsButton}>
                  <button
                    className={classes.editButton}
                    onClick={() => navigate(`${user.id}`)}
                  >
                    View
                  </button>
                  {/* <button
                    className={classes.deleteButton}
                    onClick={() => handleDeleteUser(user.id)}
                  >
                    Delete
                  </button> */}
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
