import { useEffect, useState } from "react";

import classes from "./CreateUserForm.module.css";

// icons
import { CgCloseO } from "react-icons/cg";
import { getUserRole } from "../utils/Authentication";

function CreateUserForm({
  initialData = null,
  onSubmit,
  loading,
  onClose,
  roles = [],
  isEdit = false,
}) {
  const role = getUserRole();
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await onSubmit(formData);

      if (res.success) {
        setFormData({
          username: "",
          first_name: "",
          last_name: "",
          email: "",
          password: "",
          password_confirm: "",
          role: "public",
        });
      }
    } catch (error) {
      console.error("Error Response:", error);
    }
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
      <CgCloseO className={classes.closeIcon} onClick={onClose} />
      <h1 className={classes.formHeader}>
        {initialData ? "Update User" : "Create New User"}
      </h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label className={classes.label}>
            First Name <span>*</span>
          </label>
          <input
            type="text"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            className={classes.input}
            required
            autoComplete="off"
          />
        </div>

        <div>
          <label className={classes.label}>
            Last Name <span>*</span>
          </label>
          <input
            type="text"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            className={classes.input}
            required
            autoComplete="off"
          />
        </div>

        <div>
          <label className={classes.label}>
            Username <span>*</span>
          </label>
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            className={classes.input}
            required
            autoComplete="off"
          />
        </div>

        <div>
          <label className={classes.label}>
            Email <span>*</span>
          </label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            className={classes.input}
            required
            autoComplete="off"
          />
        </div>

        {!isEdit && (
          <div>
            <label className={classes.label}>
              Password <span>*</span>
            </label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className={classes.input}
              required
            />
          </div>
        )}

        {!isEdit && (
          <div>
            <label className={classes.label}>
              Confirm Password <span>*</span>
            </label>
            <input
              type="password"
              name="password_confirm"
              value={formData.password_confirm}
              onChange={handleChange}
              className={classes.input}
              required
            />
          </div>
        )}

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
              value={formData.role}
              disabled
              className={classes.input}
            />
          )}
        </div>

        <button type="submit" className={classes.button} disabled={loading}>
          {loading ? "Submitting..." : "Submit"}
        </button>
      </form>
    </div>
  );
}

export default CreateUserForm;
