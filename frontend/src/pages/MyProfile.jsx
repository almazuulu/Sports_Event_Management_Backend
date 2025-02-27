import { useEffect, useState } from "react";
import { toast } from "react-toastify";

import Header from "../components/Header";
import classes from "./MyProfile.module.css";
import { fetchWithAuth } from "../utils/FetchClient";
import UserForm from "../components/UserForm";

function MyProfilePage() {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isEdit, setIsEdit] = useState(false);

  const handleEdit = () => {
    setIsEdit((prevData) => !prevData);
  };

  const handleUpdateUser = async (formData) => {
    setLoading(true);

    try {
      const response = await fetchWithAuth("/api/users/profile/", {
        method: "PUT",
        body: JSON.stringify(formData),
      });

      if (!response.ok) toast.error("Failed to update user");

      handleEdit();
      toast.success("User updated successfully!");
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
        const response = await fetchWithAuth(`/api/users/profile`);
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
  }, []);

  return (
    <div className={classes.container}>
      <Header title={"My Profile"} />
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

export default MyProfilePage;
