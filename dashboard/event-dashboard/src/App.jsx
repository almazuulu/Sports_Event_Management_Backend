import { createBrowserRouter, RouterProvider } from "react-router-dom";

import RootLayout from "./pages/RootLayout";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import ProtectedRoute from "./ProtectedRoute";
import PublicRoute from "./PublicRoute";
import UserDetailPage from "./pages/UserDetail";
import UsersPage from "./pages/Users";
import EventsPage from "./pages/Events";
import NewUserPage from "./pages/NewUser";
import MyProfilePage from "./pages/MyProfile";
import ChangePasswordPage from "./pages/ChangePassword";
import NewEventPage from "./pages/NewEvent";
import SportEventsPage from "./pages/SportEvents";
import PageRootLayout from "./pages/PageRoot";
import NewSportEventPage from "./pages/NewSportEvent";
import SportEventDetailPage from "./pages/SportEventDetail";
import LogoutPage from "./pages/Logout";

const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
   
     
       
       
           path: "dashboard-view", element: <DashboardPage /> 
         
         
         
        
      
    
  },
]);
function App() {
  return <RouterProvider router={router} />;
}

export default App;
