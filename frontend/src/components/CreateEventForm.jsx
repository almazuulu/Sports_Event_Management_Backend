import { useState } from "react";

import classes from "./CreateEventForm.module.css";
import StatusEventDropdown from "./StatusEventDropdown";

function CreateEventForm({ onSubmit, loading }) {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    start_date: "",
    end_date: "",
    location: "",
    status: "draft",
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
            Name <span>*</span>
          </label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className={classes.input}
          />
        </div>

        <div className={classes.formGroup}>
          <label className={classes.label}>
            Description <span>*</span>
          </label>
          <input
            type="text"
            name="description"
            value={formData.description}
            onChange={handleChange}
            className={classes.input}
          />
        </div>

        <div className={classes.formGroup}>
          <label className={classes.label}>
            Start Date <span>*</span>
          </label>
          <input
            type="date"
            name="start_date"
            value={formData.start_date}
            onChange={handleChange}
            className={classes.input}
          />
        </div>

        <div className={classes.formGroup}>
          <label className={classes.label}>
            End Date <span>*</span>
          </label>
          <input
            type="date"
            name="end_date"
            value={formData.end_date}
            onChange={handleChange}
            className={classes.input}
          />
        </div>

        <div className={classes.formGroup}>
          <label className={classes.label}>
            Location <span>*</span>
          </label>
          <input
            type="text"
            name="location"
            value={formData.location}
            onChange={handleChange}
            className={classes.input}
          />
        </div>

        <StatusEventDropdown value={formData.status} onChange={handleChange}/>

        <button type="submit" className={classes.button} disabled={loading}>
          {loading ? "Submitting..." : "Create Event"}
        </button>
      </form>
    </div>
  );
}

export default CreateEventForm;
