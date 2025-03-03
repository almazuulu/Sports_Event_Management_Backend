import { useState } from "react";
import { toast } from "react-toastify";

import classes from "./ChangePassword.module.css";
import Header from "../components/Header";
import { fetchWithAuth } from "../utils/FetchClient";
import NormalButton from "../components/Button/NormalButton";
import CreateButton from "../components/Button/CreateButton";

function ChangePasswordPage() {
  const [formData, setFormData] = useState({
    old_password: "",
    new_password: "",
    new_password_confirm: "",
  });
  const [loading, setLoading] = useState(false);
  const [isEdit, setIsEdit] = useState(false);

  const handleEdit = () => {
    setIsEdit((prevData) => !prevData);
  };

  const handleChange = (e) => {
    setFormData((prevData) => ({
      ...prevData,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);
      const response = await fetchWithAuth("/api/users/change-password/", {
        method: "POST",
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        console.log(data);
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
        handleEdit();
        toast.success("Pasword changed successfully!");
        setFormData({
          old_password: "",
          new_password: "",
          new_password_confirm: "",
        });
      }
    } catch (error) {
      console.error("Error changing password!", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={classes.container}>
      <Header title={"Change Password"} />
      <div className={classes.card}>
        <section className={classes.sectionButton}>
          {isEdit ? (
            <NormalButton onClick={handleEdit}>Cancel</NormalButton>
          ) : (
            <CreateButton onClick={handleEdit}>Edit</CreateButton>
          )}
        </section>

        <div className={classes.formContainer}>
          <form onSubmit={handleSubmit}>
            <div>
              <label className={classes.label}>
                Old Password <span>*</span>
              </label>
              <input
                type="password"
                name="old_password"
                value={formData.old_password}
                onChange={handleChange}
                className={classes.input}
                disabled={!isEdit}
              />
            </div>

            <div>
              <label className={classes.label}>
                New Password <span>*</span>
              </label>
              <input
                type="password"
                name="new_password"
                value={formData.new_password}
                onChange={handleChange}
                className={classes.input}
                disabled={!isEdit}
              />
            </div>

            <div>
              <label className={classes.label}>
                New Password Confirm <span>*</span>
              </label>
              <input
                type="password"
                name="new_password_confirm"
                value={formData.new_password_confirm}
                onChange={handleChange}
                className={classes.input}
                disabled={!isEdit}
              />
            </div>

            {isEdit && (
              <button
                type="submit"
                className={classes.button}
                disabled={loading}
              >
                {loading ? "Saving..." : "Change Password"}
              </button>
            )}
          </form>
        </div>
      </div>
    </div>
  );
}

export default ChangePasswordPage;
