import React from "react";
import useIsAuthenticated from "react-auth-kit/hooks/useIsAuthenticated";
import { useNavigate } from "react-router-dom";

// This component should be used to protect routes that require authentication.
function SecuredRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useIsAuthenticated();
  const navigate = useNavigate();
  if (!isAuthenticated) {
    navigate("/login");
  }
  return <>{children}</>;
}

export default SecuredRoute;
