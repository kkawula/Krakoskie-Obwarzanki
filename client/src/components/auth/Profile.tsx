import { Button, HStack } from "@chakra-ui/react";
import useSignOut from "react-auth-kit/hooks/useSignOut";
import { useNavigate } from "react-router-dom";

function Profile() {
  const navigate = useNavigate();
  const signOut = useSignOut();
  return (
    <HStack>
      <Button
        onClick={() => {
          signOut();
          navigate("/");
        }}
      >
        Sign out
      </Button>
    </HStack>
  );
}

export default Profile;
