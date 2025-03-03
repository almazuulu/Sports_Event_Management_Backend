import React, { useState } from "react";

import classes from "./NewTeamForm.module.css";

// icons
import { CgCloseO } from "react-icons/cg";

function NewTeamForm({ onSubmit, loading, onClose }) {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    contact_email: "",
    contact_phone: "",
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
    onClose();
  };

  return (
    <section className={classes.formContainer}>
      <CgCloseO className={classes.closeIcon} onClick={onClose} />
      <h1 className={classes.formHeader}>Create New Team</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label className={classes.label}>
            Name <span>*</span>
          </label>
          <input
            className={classes.input}
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            autoComplete="off"
          />
        </div>

        <div>
          <label className={classes.label}>
            Description <span>*</span>
          </label>
          <input
            className={classes.input}
            type="text"
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
            autoComplete="off"
          />
        </div>

        <div>
          <label className={classes.label}>
            Contact Email <span>*</span>
          </label>
          <input
            className={classes.input}
            type="email"
            name="contact_email"
            value={formData.contact_email}
            onChange={handleChange}
            required
            autoComplete="off"
          />
        </div>

        <div>
          <label className={classes.label}>
            Contact Phone <span>*</span>
          </label>
          <input
            className={classes.input}
            type="text"
            name="contact_phone"
            value={formData.contact_phone}
            onChange={handleChange}
            required
            autoComplete="off"
          />
        </div>

        <button type="submit" className={classes.button} disabled={loading}>
          {loading ? "Submitting..." : "Submit"}
        </button>
      </form>
    </section>
  );
}

export default NewTeamForm;
