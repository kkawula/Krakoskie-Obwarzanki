import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  Text,
} from "@chakra-ui/react";
import { useEffect, useRef } from "react";
import useIsAuthenticated from "react-auth-kit/hooks/useIsAuthenticated";
import useSignIn from "react-auth-kit/hooks/useSignIn";
import toast from "react-hot-toast";
import { Link, useNavigate } from "react-router-dom";
import { sendLoginData } from "../../utils/login";

// TODO: Add Formik library
export default function LoginForm() {
  const emailRef = useRef<HTMLInputElement | null>(null);
  const passwordRef = useRef<HTMLInputElement | null>(null);

  const signIn = useSignIn();
  const isAuthenticated = useIsAuthenticated();
  const navigate = useNavigate();
  useEffect(() => {
    if (isAuthenticated) {
      return navigate("/");
    }
  }, [isAuthenticated]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const emailValue = emailRef.current?.value;
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
      const email = emailRef.current!.value;
      const password = passwordRef.current!.value;
      const tokens = await sendLoginData({
        login: email,
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
      <FormControl id="email" isRequired>
        <FormLabel>Email</FormLabel>
        <Input type="text" ref={emailRef} />
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
