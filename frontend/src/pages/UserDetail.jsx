import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { toast } from "react-toastify";

import Header from "../components/Header";
import { fetchWithAuth } from "../utils/FetchClient";
import UserForm from "../components/UserForm";
import classes from "./UserDetail.module.css";

function UserDetailPage() {
  const { userId } = useParams();
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isEdit, setIsEdit] = useState(false);

  const handleEdit = () => {
    setIsEdit((prevData) => !prevData);
  };

  const handleUpdateUser = async (formData) => {
    setLoading(true);

    try {
      const response = await fetchWithAuth(`/api/users/${userId}/`, {
        method: "PUT",
        body: JSON.stringify(formData),
      });

      // const data = await response.json();

      if (!response.ok) toast.error("Failed to update user");

      if (response.ok) {
        handleEdit();
        toast.success("User updated successfully!");
      }
    } catch (error) {
      console.error("Error updating user", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const fetchUser = async () => {
      setLoading(true);
      try {
        const response = await fetchWithAuth(`/api/users/${userId}`);
        if (!response.ok) toast.error("Failed to fetch user");
        const data = await response.json();
        setUserData(data);
      } catch (error) {
        console.error("Error fetching user:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, [userId]);

  return (
    <div className={classes.container}>
      <Header title={"View User"} enableBack />
      <section className={classes.section}>
        <button className={classes.button} onClick={handleEdit}>
          {isEdit ? "Cancel" : "Edit"}
        </button>
      </section>
      <UserForm
        initialData={userData}
        onSubmit={handleUpdateUser}
        loading={loading}
        allowEdit={isEdit}
      />
    </div>
  );
}

export default UserDetailPage;
