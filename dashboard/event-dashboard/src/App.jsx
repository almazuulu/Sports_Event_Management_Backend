import { createBrowserRouter, RouterProvider, Navigate } from "react-router-dom";
import PublicDashboard from "../src/Pages/PublicDashboard";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Navigate to="/public-dashboard" replace />, // Redirect root to /public-dashboard
  },
  {
    path: "/public-dashboard",
    element: <PublicDashboard />,
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
