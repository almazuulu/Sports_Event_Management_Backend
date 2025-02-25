import LoginForm from "../components/LoginForm";

import classes from './LoginPage.module.css'

function LoginPage() {
  return (
    <div className={classes.container}>
      <h1>Welcome to Sport Event Management</h1>
      <p>Organizing tournaments, handling team, games and more with ease.</p>
      <LoginForm />
    </div>
  );
}

export default LoginPage;
