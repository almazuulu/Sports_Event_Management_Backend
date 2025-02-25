import { Navigate, Outlet } from "react-router-dom";
import { isAuthenticated } from "./utils/Authentication";

function ProtectedRoute() {
  return isAuthenticated() ? <Outlet /> : <Navigate to="/" replace />;
}

export default ProtectedRoute;
