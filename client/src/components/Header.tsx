import { Flex, Heading, IconButton } from "@chakra-ui/react";
import { IoIosArrowDown, IoIosArrowUp } from "react-icons/io";

type HeaderProps = {
  handleToggle: () => void;
  show: boolean;
};

const Header = ({ handleToggle, show }: HeaderProps) => {
  return (
    <Flex justify="space-between" align="center">
      <Heading as="h2" size="md">
        Krakoskie Obwarzanki
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
