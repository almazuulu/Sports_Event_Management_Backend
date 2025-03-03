import { useEffect, useState } from "react";

import classes from "./UserForm.module.css";
import { getUserRole } from "../utils/Authentication";
import { ROLE_LABELS } from "../constant";

const getRoleLabel = (role) => ROLE_LABELS[role];

function UserForm({
  initialData = null,
  onSubmit,
  loading,
  allowEdit,
  roles = [],
}) {
  const role = getUserRole();

  const [formData, setFormData] = useState({
    username: "",
    first_name: "",
    last_name: "",
    email: "",
    role: "",
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
        <div>
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

        <div>
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

        <div>
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

        <div>
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

        <div>
          <label className={classes.label}>
            Role <span>*</span>
          </label>
          {role === "admin" ? (
            <select
              name="role"
              value={formData.role}
              onChange={handleChange}
              className={classes.select}
              required
              disabled={!allowEdit}
            >
              {roles.map((role) => (
                <option key={role.id} value={role.id}>
                  {role.name}
                </option>
              ))}
            </select>
          ) : (
            <input
              type="text"
              value={getRoleLabel(formData.role)}
              disabled
              className={classes.input}
            />
          )}
        </div>

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
