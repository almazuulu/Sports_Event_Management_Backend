import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import Header from "../components/Header";
import UserForm from "../components/UserForm";
import classes from "./UserDetail.module.css";
import { fetchWithAuth } from "../utils/FetchClient";

function UserDetailPage() {
  const { userId } = useParams();
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpdateUser = () => {};

  useEffect(() => {
    const fetchUser = async () => {
      setLoading(true);
      try {
        const response = await fetchWithAuth(`/api/users/${userId}`);
        if (!response.ok) alert("Failed to fetch user");
        const data = await response.json();
        console.log(data);
        // setUserData(data);
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
      <Header title={"View User"} />
      <UserForm
        initialData={userData}
        onSubmit={handleUpdateUser}
        loading={loading}
      />
    </div>
  );
}

export default UserDetailPage;
