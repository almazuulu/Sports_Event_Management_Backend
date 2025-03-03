import { createBrowserRouter, RouterProvider } from "react-router-dom";

import RootLayout from "./pages/RootLayout";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import ProtectedRoute from "./ProtectedRoute";
import PublicRoute from "./PublicRoute";
import UsersPage from "./pages/Users";
import EventsPage from "./pages/Events";
import MyProfilePage from "./pages/MyProfile";
import ChangePasswordPage from "./pages/ChangePassword";
import SportEventsPage from "./pages/SportEvents";
import PageRootLayout from "./pages/PageRoot";
import LogoutPage from "./pages/Logout";

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
          {
            path: "events",
            element: <PageRootLayout />,
            children: [
              {
                index: true,
                element: <EventsPage />,
              },
            ],
          },
          {
            path: "sport-events",
            element: <PageRootLayout />,
            children: [
              {
                index: true,
                element: <SportEventsPage />,
              },
            ],
          },
          {
            path: "admin-panel",
            element: <ProtectedRoute allowedRoles={["admin"]} />,
            children: [
              {
                index: true,
                element: <UsersPage />,
              },
            ],
          },
          {
            path: "settings",
            element: <PageRootLayout />,
            children: [
              {
                path: "my-profile",
                element: <MyProfilePage />,
              },
              {
                path: "change-password",
                element: <ChangePasswordPage />,
              },
              {
                path: "logout",
                element: <LogoutPage />,
              },
            ],
          },
        ],
      },
    ],
  },
]);
function App() {
  return <RouterProvider router={router} />;
}

export default App;
