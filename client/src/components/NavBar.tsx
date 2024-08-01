import { Box, Tabs, TabList, Tab } from "@chakra-ui/react";
import { Link, useLocation } from "react-router-dom";
import { FaUser } from "react-icons/fa";
import { CiLogin } from "react-icons/ci";
import { GiPretzel } from "react-icons/gi";
import useIsAuthenticated from "react-auth-kit/hooks/useIsAuthenticated";
import { useEffect, useState } from "react";

export default function NavBar() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const { pathname } = useLocation();

  const isAuthenticatedVal = useIsAuthenticated();
  useEffect(() => {
    setIsAuthenticated(isAuthenticatedVal);
  }, [isAuthenticatedVal]);
  return (
    <Box>
      <Tabs variant="enclosed" index={getCurrentIndex(pathname)}>
        <TabList>
          <Tab as={Link} to="/">
            <GiPretzel />
          </Tab>
          {isAuthenticated ? (
            <Tab as={Link} to="/profile">
              <FaUser />
            </Tab>
          ) : (
            <>
              <Tab as={Link} to="/login">
                <CiLogin />
              </Tab>
              <Tab as={Link} to="/register">
                <FaUser />
              </Tab>
            </>
          )}
        </TabList>
      </Tabs>
    </Box>
  );
}

const getCurrentIndex = (pathname: string) => {
  if (pathname === "/") return 0;
  if (pathname === "/login" || pathname === "profile") return 1;
  if (pathname === "/register") return 2;
  return 0;
};
