import { Box, Button, FormControl, FormLabel, Input } from "@chakra-ui/react";
import { useEffect, useRef } from "react";
import useSignIn from "react-auth-kit/hooks/useSignIn";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";
import useIsAuthenticated from "react-auth-kit/hooks/useIsAuthenticated";
import { sendLoginData } from "src/utils/login";
import { sendPostRequest } from "src/utils/sendPostRequest";

// TODO: Add Formik library
export default function RegisterForm() {
  const usernameRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);
  const emailRef = useRef<HTMLInputElement>(null);

  const signIn = useSignIn();
  const navigate = useNavigate();
  const isAuthenticated = useIsAuthenticated();
  useEffect(() => {
    if (isAuthenticated) {
      return navigate("/");
    }
  }, [isAuthenticated]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const username = usernameRef.current!.value;
    const password = passwordRef.current!.value;
    const email = emailRef.current!.value;
    const name = usernameRef.current!.value;
    console.log(username, password, email, name);
    await sendPostRequest({
      url: "/user/register",
      data: {
        name: usernameRef.current!.value,
        username: usernameRef.current!.value,
        password: passwordRef.current!.value,
        email: emailRef.current!.value,
      },
    });
    const tokens = await sendLoginData({ login: username, password: password });
    if (
      signIn({
        auth: {
          token: tokens.access_token,
        },
      })
    ) {
      toast.success("Registered in successfully");
    }
  };

  return (
    <Box
      as="form"
      onSubmit={handleSubmit}
      p="4"
      borderWidth="2px"
      borderRadius="md"
      width="300px"
    >
      <FormControl id="username" isRequired>
        <FormLabel>Imię i Nazwisko</FormLabel>
        <Input type="text" ref={usernameRef} />
      </FormControl>
      <FormControl id="email" isRequired mt={4}>
        <FormLabel>Email</FormLabel>
        <Input type="email" ref={emailRef} />
      </FormControl>
      <FormControl id="password" isRequired mt={4}>
        <FormLabel>Hasło</FormLabel>
        <Input type="password" ref={passwordRef} />
      </FormControl>
      <Button mt={4} type="submit">
        Zarejestruj się
      </Button>
    </Box>
  );
}
