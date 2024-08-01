import { Avatar, AvatarBadge } from "@chakra-ui/react";
import useIsAuthenticated from "react-auth-kit/hooks/useIsAuthenticated";

function UserAvatar() {
  const isAuthenticated = useIsAuthenticated();

  return (
    <Avatar position="absolute" top="1rem" right="4rem" zIndex="9999">
      <AvatarBadge boxSize="1em" bg={isAuthenticated ? "green.500" : "red"} />
    </Avatar>
  );
}

export default UserAvatar;
