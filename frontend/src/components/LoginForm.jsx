import { useState } from "react";
import { useNavigate } from "react-router-dom";

import classes from "./LoginForm.module.css";

const USERS = {
  "admin@example.com": { role: "admin", password: "admin123" },
  "user@example.com": { role: "user", password: "user123" },
};

function LoginForm() {
  const navigate = useNavigate();
  const [userEmail, setUserEmail] = useState("");
  const [userPassword, setUserPassword] = useState("");

  const emailChange = (event) => {
    setUserEmail(event.target.value);
  };

  const passwordChange = (event) => {
    setUserPassword(event.target.value);
  };

  const formHandler = (event) => {
    event.preventDefault();

    if (USERS[userEmail] && USERS[userEmail].password === userPassword) {
      localStorage.setItem("authToken", "token"); // Store auth token
      localStorage.setItem("userRole", USERS[userEmail].role); // Store role

      // Redirect based on role
      if (USERS[userEmail].role === "admin") {
        navigate("/admin");
      } else if (USERS[userEmail].role === "user") {
        navigate("/user/dashboard");
      }
    } else {
      alert("Invalid credentials. Try again!");
    }
  };
  return (
    <div className={classes.container}>
      <div className={classes.card}>
        <h2 className={classes.title}>Sign In</h2>
        <form method="post" onSubmit={formHandler}>
          <div className={classes.inputGroup}>
            <label htmlFor="email" className={classes.label}>
              Email:
            </label>
            <input
              id="email"
              type="email"
              name="email"
              onChange={emailChange}
              value={userEmail}
              className={classes.input}
              required
            />
          </div>
          <div className={classes.inputGroup}>
            <label htmlFor="password" className={classes.label}>
              Password:
            </label>
            <input
              id="password"
              type="password"
              name="password"
              onChange={passwordChange}
              value={userPassword}
              className={classes.input}
              required
            />
          </div>
          <button className={classes.button}>Sign In</button>
        </form>
      </div>
    </div>
  );
}

export default LoginForm;
