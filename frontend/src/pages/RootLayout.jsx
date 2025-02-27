import { Outlet, useLocation } from "react-router-dom";
import { ToastContainer } from "react-toastify";

import MainNavigation from "../components/MainNavigation";

function RootLayout() {
  const location = useLocation();
  const isLoginPage = location.pathname === "/";

  return (
    <div style={{ display: "flex" }}>
      <ToastContainer />
      {!isLoginPage && <MainNavigation />}
      <main style={{ width: "100%", backgroundColor: "#f3f3f3" }}>
        <Outlet />
      </main>
    </div>
  );
}

export default RootLayout;
