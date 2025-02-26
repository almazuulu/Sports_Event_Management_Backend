import { useState } from "react";

import Header from "../components/Header";
import UserForm from "../components/UserForm";
import { fetchWithAuth } from "../utils/FetchClient";
import classes from "./NewUser.module.css";

function NewUserPage() {
  const [loading, setLoading] = useState(false);

  const handleCreateUser = async (formData) => {
    setLoading(true);
    try {
      const response = await fetchWithAuth("/api/users/", {
        method: "POST",
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error("Failed to create user");
      alert("User created successfully!");
    } catch (error) {
      console.error(error);
      alert("Failed to create user. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={classes.container}>
      <Header title={"Create New User"} />
      <UserForm onSubmit={handleCreateUser} loading={loading}/>
    </div>
  );
}

export default NewUserPage;
