import { useEffect, useState } from "react";

import classes from "./UserForm.module.css";
import RolesDropdown from "./RolesDropdown";

function UserForm({ initialData = null, onSubmit, loading, allowEdit }) {
  const [formData, setFormData] = useState({
    username: "",
    first_name: "",
    last_name: "",
    email: "",
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

  useEffect(() => {
    if (initialData) {
      setFormData((prevData) => ({
        ...prevData,
        ...initialData,
      }));
    }
  }, [initialData]);

  return (
    <div className={classes.formContainer}>
      <form onSubmit={handleSubmit}>
        <div className={classes.formGroup}>
          <label className={classes.label}>First Name</label>
          <input
            type="text"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            className={classes.input}
            disabled={!allowEdit}
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
            disabled={!allowEdit}
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
            disabled={!allowEdit}
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
            disabled={!allowEdit}
          />
        </div>

        <RolesDropdown value={formData.role} onChange={handleChange} allowedEdit={!allowEdit}/>

        {allowEdit && (
          <button type="submit" className={classes.button} disabled={loading}>
            {loading ? "Saving..." : "Update"}
          </button>
        )}
      </form>
    </div>
  );
}

export default UserForm;
