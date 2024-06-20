import { useState } from "react";
import { Box, Collapse, Flex } from "@chakra-ui/react";
import Header from "./Header";
import LoginForm from "./LoginForm";
import NavBar from "./NavBar";
import PretzelList from "./PretzelList";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import RegisterForm from "./RegisterForm";

export default function Widget() {
  const [show, setShow] = useState(false);

  return (
    <Box
      position="absolute"
      left="30px"
      top="15px"
      w={show ? "350px" : "350px"}
      h={show ? "500px" : ""}
      zIndex={1000}
      bg="white"
      p="5"
      borderWidth="2px"
      borderColor="gray.300"
      borderRadius="md"
      boxShadow="sm"
    >
      <Header
        handleToggle={() => {
          setShow((prevShow) => !prevShow);
        }}
        show={show}
      />

      <Collapse in={show}>
        <Box w="350px">
          <Router>
            <NavBar />
            <Flex flexDirection="column" width="300px" marginTop="10px">
              <Routes>
                <Route path="/" element={<PretzelList />} />
                <Route path="/login" element={<LoginForm />} />
                <Route path="/register" element={<RegisterForm />} />
              </Routes>
            </Flex>
          </Router>
        </Box>
      </Collapse>
    </Box>
  );
}
