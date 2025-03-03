import { useEffect, useState } from "react";

import { SPORT_EVENTS_STATUS, SPORTS_TYPE_OPTIONS } from "../../constant";
import { getUserRole } from "../../utils/Authentication";
import CreateButton from "../Button/CreateButton";
import classes from "./SportEventForm.module.css";

// icons
import { CgCloseO } from "react-icons/cg";

function SportEventForm({
  initialData = null,
  eventList = [],
  onSubmit,
  loading,
  onClose,
}) {
  const [formData, setFormData] = useState({
    event: "",
    sport_type: "",
    name: "",
    description: "",
    start_date: "",
    end_date: "",
    max_teams: "",
    registration_deadline: "",
    rules: "",
    scoring_system: "",
    status: "",
  });

  const formattedDate = (dateString) => {
    if (dateString === "") return;
    const date = new Date(dateString);
    date.setDate(date.getDate());
    return date.toISOString().split("T")[0];
  };

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
    <div className={classes.formContainer}>
      <CgCloseO className={classes.closeIcon} onClick={onClose} />
      <h1 className={classes.formHeader}>Create New Sport Event</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label className={classes.label}>
            Event <span>*</span>
          </label>
          <Dropdown
            name={"event"}
            placeholder={"Please select an event"}
            data={eventList}
            value={formData.event_name}
            onChange={handleChange}
          />
        </div>

        <div>
          <label className={classes.label}>
            Sport type <span>*</span>
          </label>
          <Dropdown
            name={"sport_type"}
            placeholder={"Please select a sport type"}
            data={SPORTS_TYPE_OPTIONS}
            value={formData.sport_type}
            onChange={handleChange}
          />
        </div>

        <div>
          <label className={classes.label}>
            Name <span>*</span>
          </label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className={classes.input}
            required
            autoComplete="off"
          />
        </div>

        <div>
          <label className={classes.label}>
            Description <span>*</span>
          </label>
          <input
            type="text"
            name="description"
            value={formData.description}
            onChange={handleChange}
            className={classes.input}
            required
            autoComplete="off"
          />
        </div>

        <div className={classes.dateInputWrapper}>
          <section>
            <label className={classes.label}>
              Start Date <span>*</span>
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
              End Date <span>*</span>
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
            Max team <span>*</span>
          </label>
          <input
            type="number"
            name="max_teams"
            value={formData.max_teams}
            onChange={handleChange}
            className={classes.input}
            required
          />
        </div>

        <div>
          <label className={classes.label}>
            Registration deadline <span>*</span>
          </label>
          <input
            type="date"
            name="registration_deadline"
            value={formattedDate(formData.registration_deadline)}
            onChange={handleChange}
            className={classes.input}
            required
          />
        </div>

        <div>
          <label className={classes.label}>
            Rules <span>*</span>
          </label>
          <textarea
            name="rules"
            value={formData.rules}
            onChange={handleChange}
            className={classes.textarea}
            required
            autoComplete="off"
          />
        </div>

        <div>
          <label className={classes.label}>
            Scoring system <span>*</span>
          </label>
          <textarea
            name="scoring_system"
            value={formData.scoring_system}
            onChange={handleChange}
            className={classes.textarea}
            required
            autoComplete="off"
          />
        </div>

        <div>
          <label className={classes.label}>
            Status <span>*</span>
          </label>
          <Dropdown
            name={"status"}
            placeholder={"Please select a status"}
            data={SPORT_EVENTS_STATUS}
            value={formData.status}
            onChange={handleChange}
          />
        </div>

        <button type="submit" className={classes.button} disabled={loading}>
          {loading ? "Submitting..." : "Submit"}
        </button>
      </form>
    </div>
  );
}

export default SportEventForm;

const Dropdown = ({
  data = [],
  name,
  value,
  onChange,
  allowedEdit = false,
  placeholder,
}) => {
  const role = getUserRole();

  return (
    <section>
      {role === "admin" ? (
        <select
          name={name}
          value={value}
          onChange={onChange}
          className={classes.select}
          disabled={allowedEdit}
          required
        >
          <option value={""} disabled>
            {placeholder}
          </option>
          {data.map((dataa) => (
            <option key={dataa.id} value={dataa.id}>
              {dataa.name}
            </option>
          ))}
        </select>
      ) : (
        <input type="text" value={value} disabled className={classes.input} />
      )}
    </section>
  );
};
