import { createBrowserRouter, RouterProvider } from "react-router-dom";

import RootLayout from "./pages/RootLayout";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import ProtectedRoute from "./ProtectedRoute";
import PublicRoute from "./PublicRoute";
import UserDetailPage from "./pages/UserDetail";
import EditUserPage from "./pages/EditUser";
import UserRootLayout from "./pages/UsersRoot";
import UsersPage from "./pages/Users";
import NewUserPage from "./pages/NewUser";

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
            path: "manage-users",
            element: <UserRootLayout />,
            children: [
              { index: true, element: <UsersPage /> },
              { path: "create-user", element: <NewUserPage /> },
              {
                path: ":userId",
                children: [
                  { index: true, element: <UserDetailPage /> },
                  { path: "edit", element: <EditUserPage /> },
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
