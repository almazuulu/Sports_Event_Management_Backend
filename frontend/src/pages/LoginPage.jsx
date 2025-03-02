import LoginForm from "../components/LoginForm";

import logo from "../assets/images/ust-black-logo.svg";
import classes from "./LoginPage.module.css";

function LoginPage() {
  return (
    <div className={classes.container}>
      <img src={logo} alt="UST Logo" />
      <LoginForm />
      <p>Developed by UST Development Team</p>
    </div>
  );
}

export default LoginPage;
