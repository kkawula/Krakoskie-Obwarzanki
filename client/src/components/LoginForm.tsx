import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  Text,
} from "@chakra-ui/react";
import { useRef } from "react";
import { Link } from "react-router-dom";

// TODO: Add Formik library
export default function LoginForm() {
  const emailRef = useRef<HTMLInputElement | null>(null);
  const passwordRef = useRef<HTMLInputElement | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // const emailValue = emailRef.current?.value;
    // const passwordValue = passwordRef.current?.value;

    // TODO: Implement form submission logic
  };

  const handleSubmit = () => {}; // TODO implement

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
