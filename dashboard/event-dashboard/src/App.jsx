import { createBrowserRouter, RouterProvider } from "react-router-dom";
import PublicDashboard from "../src/Pages/PublicDashboard";

const router = createBrowserRouter([
  {
    path: "/public-dashboard",
    element: <PublicDashboard />, // Directly set element
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
