import { createBrowserRouter, RouterProvider } from "react-router-dom";

import RootLayout from "./pages/RootLayout";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import DummyPage from "./pages/DummyPage";
import ProtectedRoute from "./ProtectedRoute";
import PublicRoute from "./PublicRoute";

const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    children: [
      {
        element: <PublicRoute />, 
        children: [{ index: true, element: <LoginPage /> }],
      },
      {
        element: <ProtectedRoute />, 
        children: [
          { path: "dashboard", element: <DashboardPage /> },
          { path: "dummy-1", element: <DummyPage /> },
        ],
      },
    ],
  },
]);
function App() {
  return <RouterProvider router={router} />;
}

export default App;
