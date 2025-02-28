import { useState } from "react";
import { toast } from "react-toastify";

import Header from "../components/Header";
import { fetchWithAuth } from "../utils/FetchClient";
import classes from "./NewUser.module.css";
import CreateUserForm from "../components/CreateUserForm";
import { useNavigate } from "react-router-dom";

function NewUserPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleCreateUser = async (formData) => {
    setLoading(true);
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
        navigate("..");
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={classes.container}>
      <Header title={"Create New User"} enableBack />
      <CreateUserForm onSubmit={handleCreateUser} loading={loading} />
    </div>
  );
}

export default NewUserPage;
