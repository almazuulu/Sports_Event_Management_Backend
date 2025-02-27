import { createBrowserRouter, RouterProvider } from "react-router-dom";

import RootLayout from "./pages/RootLayout";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import ProtectedRoute from "./ProtectedRoute";
import PublicRoute from "./PublicRoute";
import UserDetailPage from "./pages/UserDetail";
import UsersPage from "./pages/Users";
import NewUserPage from "./pages/NewUser";
import MyProfilePage from "./pages/MyProfile";
import ChangePasswordPage from "./pages/ChangePassword";
import SettingsRootLayout from "./pages/SettingsRoot";
import ManageUsersLayout from "./pages/ManageUsersLayout";
import EventsRootLayout from "./pages/EventsRoot";
import NewEventPage from "./pages/NewEvent";

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
            element: <EventsRootLayout />,
            children: [
              {
                path: "view-events",
                // element:  view events page,
              },
              {
                path: "create-new",
                element: <NewEventPage />,
              },
            ],
          },
          {
            path: "settings",
            element: <SettingsRootLayout />,
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
                element: <ProtectedRoute allowedRoles={["admin"]} />,
                children: [
                  {
                    path: "manage-users",
                    element: <ManageUsersLayout />,
                    children: [
                      { index: true, element: <UsersPage /> },
                      { path: "create-new", element: <NewUserPage /> },
                      { path: ":userId", element: <UserDetailPage /> },
                    ],
                  },
                ],
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
