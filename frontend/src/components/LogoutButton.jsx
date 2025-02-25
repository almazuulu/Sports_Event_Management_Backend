import { useNavigate } from "react-router-dom";
import classes from "./LogoutButton.module.css";
function LogoutButton() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");

    navigate("/", { replace: true });
  };
  return (
    <button className={classes.button} onClick={handleLogout}>
      Logout
    </button>
  );
}

export default LogoutButton;
