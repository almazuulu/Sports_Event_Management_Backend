import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

function LogoutPage() {
  const navigate = useNavigate();

  useEffect(() => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("userRole");

    navigate("/", { replace: true });
  });
}

export default LogoutPage;
