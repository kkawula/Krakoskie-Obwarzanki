import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  Text,
} from "@chakra-ui/react";
import { useRef } from "react";
import useIsAuthenticated from "react-auth-kit/hooks/useIsAuthenticated";
import useSignIn from "react-auth-kit/hooks/useSignIn";
import toast from "react-hot-toast";
import { Link } from "react-router-dom";
import { sendLoginData } from "../utils/login";

// TODO: Add Formik library
export default function LoginForm() {
  const usernameRef = useRef<HTMLInputElement | null>(null);
  const passwordRef = useRef<HTMLInputElement | null>(null);

  const signIn = useSignIn();
  const isAuthenticated = useIsAuthenticated();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const emailValue = usernameRef.current?.value;
    if (!emailValue) {
      console.error("Email is required");
      return;
    }
    const passwordValue = passwordRef.current?.value;
    if (!passwordValue) {
      toast.error("Password is required");
      return;
    }

    try {
      const username = usernameRef.current!.value;
      const password = passwordRef.current!.value;
      const tokens = await sendLoginData({
        login: username,
        password: password,
      });
      if (
        signIn({
          auth: {
            token: tokens.access_token,
          },
        })
      ) {
        toast.success("Logged in successfully");
      }
    } catch (error) {
      console.error("Error:", error);
      toast.error("Something went wrong");
    }
    console.log(isAuthenticated);
    // const emailValue = emailRef.current?.value;
    // const passwordValue = passwordRef.current?.value;

    // TODO: Implement form submission logic
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
        <FormLabel>Username</FormLabel>
        <Input type="text" ref={usernameRef} />
      </FormControl>
      <FormControl id="password" isRequired mt="4">
        <FormLabel>Hasło</FormLabel>
        <Input type="password" ref={passwordRef} />
      </FormControl>
      <Button type="submit" colorScheme="blue" mt="4">
        Zaloguj się
      </Button>
      <Text mt="4" fontSize="sm" color="gray.500">
        Nie masz konta? <Link to="/register">Zarejestruj się</Link>
      </Text>
    </Box>
  );
}
