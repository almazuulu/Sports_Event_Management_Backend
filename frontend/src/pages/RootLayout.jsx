import { Outlet, useLocation } from "react-router-dom";
import { ToastContainer } from "react-toastify";

import MainNavigation from "../components/MainNavigation";
import HeaderNavBar from "../components/HeaderNavBar";

function RootLayout() {
  const location = useLocation();
  const isLoginPage = location.pathname === "/";

  return (
    <div style={{ display: "flex" }}>
      <ToastContainer />
      {!isLoginPage && <MainNavigation />}
      <main style={{ width: "100%" }}>
        <HeaderNavBar />

        <Outlet />
      </main>
    </div>
  );
}

export default RootLayout;
