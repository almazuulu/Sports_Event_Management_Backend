import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

import classes from "./LoginForm.module.css";
import { saveTokens } from "../utils/FetchClient";

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
    <section className={classes.container}>
      <h1 className={classes.loginHeader}>Sport Event Management System</h1>

      <form onSubmit={formHandler}>
        <div>
          <input
            type="email"
            className={classes.input}
            placeholder="Email"
            onChange={emailChange}
            value={userEmail}
            required
            autoComplete="off"
          />
        </div>
        <div>
          <input
            type="password"
            className={classes.input}
            placeholder="Password"
            onChange={passwordChange}
            value={userPassword}
            required
            autoComplete="off"
          />
        </div>
        <div className={classes.inputSubmit}>
          <button className={classes.button}></button>
          <label>Sign In</label>
        </div>
      </form>
    </section>
  );
}

export default LoginForm;
