import { Outlet, useLocation } from "react-router-dom";

import MainNavigation from "../components/MainNavigation";

function RootLayout() {
  const location = useLocation();
  const isLoginPage = location.pathname === "/";

  return (
    <div style={{ display: "flex" }}>
      {!isLoginPage && <MainNavigation />}
      <main style={{ width: "100%" }}>
        <Outlet />
      </main>
    </div>
  );
}

export default RootLayout;
