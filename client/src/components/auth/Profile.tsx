import { Button, HStack } from "@chakra-ui/react";
import useSignOut from "react-auth-kit/hooks/useSignOut";

function Profile() {
  // const auth = useAuthUser();
  // const navigate = useNavigate();
  // useEffect(() => {
  //     if (!auth) {
  //         return navigate("/");
  //     }
  // }, [auth]);
  const signOut = useSignOut();
  return (
    <HStack>
      {/* <h1>{auth}</h1> */}
      <Button onClick={signOut}>Sign out</Button>
    </HStack>
  );
}

export default Profile;
