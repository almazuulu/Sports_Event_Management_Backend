import { useState } from "react";
import { useNavigate } from "react-router-dom";

import classes from "./LoginForm.module.css";
import { saveTokens } from "../utils/FetchClient";
import { toast } from "react-toastify";

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

  const formHandler = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:8000/api/token/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          login: userEmail,
          email: userEmail,
          password: userPassword,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        saveTokens(data.access, data.refresh);

        const profileResponse = await fetch(
          "http://127.0.0.1:8000/api/users/profile/",
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${data.access}`,
            },
          }
        );

        const profileData = await profileResponse.json();

        if (profileResponse.ok) {
          localStorage.setItem("userRole", profileData.role);
          navigate("dashboard");
        }
      } else {
        toast.error("Invalid credentials! Please, try again.");
      }
    } catch (error) {
      console.error("Login error:", error);
      toast.error("Something went wrong. Please try again later.");
    }
  };
  return (
    <div className={classes.container}>
      <div className={classes.card}>
        <h2 className={classes.title}>Sign In</h2>
        <form onSubmit={formHandler}>
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
