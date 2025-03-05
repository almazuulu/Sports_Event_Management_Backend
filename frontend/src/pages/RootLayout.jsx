import { Outlet, useLocation } from "react-router-dom";
import { ToastContainer } from "react-toastify";

import MainNavigation from "../components/MainNavigation";
import HeaderNavBar from "../components/HeaderNavBar";

function RootLayout() {
  const location = useLocation();

  return (
    <div>
      <HeaderNavBar />
      <main>
        <Outlet />
      </main>
    </div>
  );
}

export default RootLayout;
