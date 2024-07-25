import { Flex, Heading, IconButton } from "@chakra-ui/react";
import useIsAuthenticated from "react-auth-kit/hooks/useIsAuthenticated";
import { IoIosArrowDown, IoIosArrowUp } from "react-icons/io";

type HeaderProps = {
  handleToggle: () => void;
  show: boolean;
};

const Header = ({ handleToggle, show }: HeaderProps) => {
  const isAuthenticated = useIsAuthenticated();
  return (
    <Flex justify="space-between" align="center">
      <Heading as="h2" size="md">
        Krakoskie Obwarzanki {isAuthenticated ? "Admin" : "User"}
      </Heading>
      <Flex>
        <IconButton
          onClick={handleToggle}
          aria-label="More options"
          icon={show ? <IoIosArrowUp /> : <IoIosArrowDown />}
        />
      </Flex>
    </Flex>
  );
};

export default Header;
