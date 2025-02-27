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
import NewEventPage from "./pages/NewEvent";
import SportEventsPage from "./pages/SportEvents";
import PageRootLayout from "./pages/PageRoot";
import NewSportEventPage from "./pages/NewSportEvent";

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
                path: "view-events",
                // element:  view events page,
              },
              {
                path: "create-new",
                element: <NewEventPage />,
              },
              {
                element: <ProtectedRoute allowedRoles={["admin"]} />,
                children: [
                  {
                    path: "manage-sport-events",
                    element: <PageRootLayout />,
                    children: [
                      { index: true, element: <SportEventsPage /> },
                      { path: "create-new", element: <NewSportEventPage /> },
                      // { path: ":sportEventId", element: <UserDetailPage /> },
                    ],
                  },
                ],
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
                element: <ProtectedRoute allowedRoles={["admin"]} />,
                children: [
                  {
                    path: "manage-users",
                    element: <PageRootLayout />,
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
