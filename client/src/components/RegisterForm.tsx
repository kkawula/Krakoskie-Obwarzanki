import { Box, Button, FormControl, FormLabel, Input } from "@chakra-ui/react";
import { useRef } from "react";
import { sendPostRequest } from "../utils/sendPostRequest";

// TODO: Add Formik library
export default function RegisterForm() {
  const usernameRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);
  const emailRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    sendPostRequest({
      url: "/user/register",
      data: {
        username: usernameRef.current!.value,
        password: passwordRef.current!.value,
        email: emailRef.current!.value,
      },
    });

    // const username = usernameRef.current?.value;
    // const password = passwordRef.current?.value;
    // const email = emailRef.current?.value;
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
