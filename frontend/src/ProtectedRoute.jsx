import { Navigate, Outlet, useLocation } from "react-router-dom";
import { getUserRole, isAuthenticated } from "./utils/Authentication";

function ProtectedRoute({ allowedRoles }) {
  const location = useLocation();
  const token = isAuthenticated();
  const userRole = getUserRole();

  // Redirect to login if not authenticated
  if (!token) {
    return <Navigate to="/" replace state={{ from: location }} />;
  }

  // If allowedRoles is set and userRole is not in the list, deny access
  if (allowedRoles && !allowedRoles.includes(userRole)) {
    return <Navigate to="/dashboard" replace />;
  }

  return <Outlet />;
}

export default ProtectedRoute;
