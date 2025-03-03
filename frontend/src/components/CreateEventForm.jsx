import { useEffect, useState } from "react";

import StatusEventDropdown from "./StatusEventDropdown";
import classes from "./CreateEventForm.module.css";

// icons
import { CgCloseO } from "react-icons/cg";

function CreateEventForm({ initialData = null, onSubmit, loading, onClose }) {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    start_date: "",
    end_date: "",
    location: "",
    status: "",
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

  useEffect(() => {
    if (initialData) {
      setFormData((prevData) => ({
        ...prevData,
        ...initialData,
      }));
    }
  }, [initialData]);

  return (
    <section className={classes.formContainer}>
      <CgCloseO className={classes.closeIcon} onClick={onClose} />
      <h1 className={classes.formHeader}>Create New Event</h1>
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

        <div className={classes.dateInputWrapper}>
          <section>
            <label className={classes.label}>
              Start date <span>*</span>
            </label>
            <input
              type="date"
              name="start_date"
              value={formData.start_date}
              onChange={handleChange}
              className={classes.input}
              required
            />
          </section>
          <section>
            <label className={classes.label}>
              End date <span>*</span>
            </label>
            <input
              type="date"
              name="end_date"
              value={formData.end_date}
              onChange={handleChange}
              className={classes.input}
              required
            />
          </section>
        </div>

        <div>
          <label className={classes.label}>
            Location <span>*</span>
          </label>
          <input
            type="text"
            name="location"
            value={formData.location}
            onChange={handleChange}
            className={classes.input}
            required
            autoComplete="off"
          />
        </div>

        <StatusEventDropdown value={formData.status} onChange={handleChange} />

        <button type="submit" className={classes.button} disabled={loading}>
          {loading ? "Submitting..." : "Submit"}
        </button>
      </form>
    </section>
  );
}

export default CreateEventForm;
