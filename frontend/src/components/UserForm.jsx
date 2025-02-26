import { useEffect, useState } from "react";

import classes from "./UserForm.module.css";
import { useNavigate } from "react-router-dom";

function UserForm({ initialData = null, onSubmit, loading }) {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    password_confirm: "",
    role: "public",
  });

  const handleChange = (e) => {
    setFormData((prevData) => ({
      ...prevData,
      [e.target.name]: e.target.value,
    }));
  };

  const validateForm = () => {
    if (!initialData) {
      if (formData.password !== formData.password_confirm) {
        alert("Passwords do not match");
        return false;
      }
    }

    return true;
  };

  useEffect(() => {
    if (initialData) {
      setFormData({ ...initialData, password: "", password_confirm: "" }); // Clear passwords for security
    }
  }, [initialData]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit(formData);
      navigate("..");
    }

  };

  useEffect(() => {
    if (initialData) {
      setFormData({ ...initialData, password: "", password_confirm: "" }); // Clear passwords for security
    }
  }, [initialData]);

  return (
    <div className={classes.formContainer}>
      <h2>{initialData ? "Edit User" : "Create New User"}</h2>

      <form onSubmit={handleSubmit}>
        <div className={classes.formGroup}>
          <label className={classes.label}>First Name</label>
          <input
            type="text"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            className={classes.input}
            required
          />
        </div>

        <div className={classes.formGroup}>
          <label className={classes.label}>Last Name</label>
          <input
            type="text"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            className={classes.input}
            required
          />
        </div>

        <div className={classes.formGroup}>
          <label className={classes.label}>Username</label>
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            className={classes.input}
            required
          />
        </div>

        <div className={classes.formGroup}>
          <label className={classes.label}>Email</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            className={classes.input}
            required
          />
        </div>

        <div className={classes.formGroup}>
          <label className={classes.label}>Password</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            className={classes.input}
            required
          />
        </div>

        <div className={classes.formGroup}>
          <label className={classes.label}>Confirm Password</label>
          <input
            type="password"
            name="password_confirm"
            value={formData.password_confirm}
            onChange={handleChange}
            className={classes.input}
            required
          />
        </div>

        <div className={classes.formGroup}>
          <label className={classes.label}>Role</label>
          <select
            name="role"
            value={formData.role}
            onChange={handleChange}
            className={classes.select}
          >
            <option value="public">Public User</option>
            <option value="admin">Administrator</option>
            <option value="team_captain">Team Captain</option>
            <option value="scorekeeper">Scorekeeper</option>
          </select>
        </div>

        <button type="submit" className={classes.button} disabled={loading}>
          {loading ? "Saving..." : initialData ? "Update User" : "Create User"}
        </button>
      </form>
    </div>
  );
}

export default UserForm;
