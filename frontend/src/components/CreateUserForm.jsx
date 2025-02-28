import { useState } from "react";

import classes from "./CreateUserForm.module.css";
import RolesDropdown from "./RolesDropdown";

function CreateUserForm({ onSubmit, loading }) {
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

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className={classes.formContainer}>
      <form onSubmit={handleSubmit}>
        <div className={classes.formGroup}>
          <label className={classes.label}>
            First Name <span>*</span>
          </label>
          <input
            type="text"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            className={classes.input}
          />
        </div>

        <div className={classes.formGroup}>
          <label className={classes.label}>
            Last Name <span>*</span>
          </label>
          <input
            type="text"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            className={classes.input}
          />
        </div>

        <div className={classes.formGroup}>
          <label className={classes.label}>
            Username <span>*</span>
          </label>
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            className={classes.input}
          />
        </div>

        <div className={classes.formGroup}>
          <label className={classes.label}>
            Email <span>*</span>
          </label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            className={classes.input}
          />
        </div>

        <div className={classes.formGroup}>
          <label className={classes.label}>
            Password <span>*</span>
          </label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            className={classes.input}
          />
        </div>

        <div className={classes.formGroup}>
          <label className={classes.label}>
            Confirm Password <span>*</span>
          </label>
          <input
            type="password"
            name="password_confirm"
            value={formData.password_confirm}
            onChange={handleChange}
            className={classes.input}
          />
        </div>

        <RolesDropdown value={formData.role} onChange={handleChange} />

        <button type="submit" className={classes.button} disabled={loading}>
          {loading ? "Submitting..." : "Create User"}
        </button>
      </form>
    </div>
  );
}

export default CreateUserForm;
