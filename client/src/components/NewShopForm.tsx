import {
  AlertDialog,
  AlertDialogBody,
  AlertDialogContent,
  AlertDialogHeader,
  AlertDialogOverlay,
  Checkbox,
  CheckboxGroup,
  FormLabel,
  VStack,
  NumberInputStepper,
  NumberInput,
  Stack,
  NumberIncrementStepper,
  NumberDecrementStepper,
  NumberInputField,
  FormControl,
  Button,
} from "@chakra-ui/react";
import { useRef, useState } from "react";
import { SingleDatepicker } from "chakra-dayzed-datepicker";
import { type LatLngLiteral } from "leaflet";
import { Time, prettyTime } from "../utils/time";
import { useAddShopMutation } from "../hooks/useShopsQuery";

export type NewShop = {
  lat: number;
  lng: number;
  name: string;
  flavors: string[];
  card_payment: boolean;
  is_open_today: boolean;
  price: number;
  opening_time: string;
  closing_time: string;
};
type Flavour = {
  name: string;
  isChecked: boolean;
};

const flavours = ["Ser", "Mak", "Mieszany", "Sezam", "Sól"];
const users = [
  "Pan Piotrek",
  "Pan Kamil",
  "Pan Wiktor",
  "Pan Bartek",
  "Pan Wojtek",
  "Pani Basia",
];

function NewShopForm({
  position,
  isOpen,
  onClose,
}: {
  position: LatLngLiteral;
  isOpen: boolean;
  onClose: () => void;
}) {
  const { mutateAsync: addShop } = useAddShopMutation();

  const [flavourChecked, setFlavourChecked] = useState<Flavour[]>(
    flavours.map((f) => ({
      name: f,
      isChecked: false,
    }))
  );
  const [date, setDate] = useState(new Date());
  const [openTime, setStartTime] = useState<Time>({
    hour: 8,
    minute: 0,
  });
  const [closeTime, setEndTime] = useState<Time>({
    hour: 16,
    minute: 0,
  });
  const [isCardChecked, setIsCardChecked] = useState(false);

  const cancelRef = useRef(null);

  const handleSubmit = async () => {
    const newShop: NewShop = {
      ...position,
      name: users[Math.floor(Math.random() * users.length)],
      flavors: flavourChecked.filter((f) => f.isChecked).map((f) => f.name),
      card_payment: isCardChecked,
      is_open_today: true,
      opening_time: prettyTime(openTime),
      closing_time: prettyTime(closeTime),
      price: 3.0,
    };
    const { error } = await addShop(newShop);
    if (error) {
      console.error(error.message);
    }
    onClose();
  };

  const handleFlavoursToggled = (idx: number) => {
    const nextFlavourChecked = flavourChecked.map((f, index) =>
      index === idx ? { ...f, isChecked: !f.isChecked } : f
    );
    setFlavourChecked(nextFlavourChecked);
  };

  return (
    <AlertDialog
      isOpen={isOpen}
      onClose={onClose}
      leastDestructiveRef={cancelRef}
    >
      <AlertDialogOverlay>
        <AlertDialogContent mt={10}>
          <AlertDialogHeader>Nowe stoisko</AlertDialogHeader>
          <AlertDialogBody>
            <FormLabel>Data:</FormLabel>
            <SingleDatepicker
              name="date-input"
              date={date}
              onDateChange={setDate}
            />

            <FormControl>
              <FormLabel mt={4}>Godzina rozpoczęcia:</FormLabel>
              <Stack shouldWrapChildren direction="row" align="left">
                <NumberInput
                  size="sm"
                  maxW={16}
                  value={openTime.hour}
                  min={0}
                  max={23}
                  onChange={(value) =>
                    setStartTime({ ...openTime, hour: parseInt(value) })
                  }
                >
                  <NumberInputField />
                  <NumberInputStepper>
                    <NumberIncrementStepper />
                    <NumberDecrementStepper />
                  </NumberInputStepper>
                </NumberInput>
                <NumberInput
                  size="sm"
                  maxW={16}
                  value={openTime.minute}
                  min={0}
                  max={59}
                  step={5}
                  onChange={(value) =>
                    setStartTime({ ...openTime, minute: parseInt(value) })
                  }
                >
                  <NumberInputField />
                  <NumberInputStepper>
                    <NumberIncrementStepper />
                    <NumberDecrementStepper />
                  </NumberInputStepper>
                </NumberInput>
              </Stack>
              <FormLabel mt={2}>Godzina zakończenia:</FormLabel>
              <Stack shouldWrapChildren direction="row" align="left">
                <NumberInput
                  size="sm"
                  maxW={16}
                  value={closeTime.hour}
                  min={0}
                  max={23}
                  onChange={(value) =>
                    setEndTime({ ...closeTime, hour: parseInt(value) })
                  }
                >
                  <NumberInputField />
                  <NumberInputStepper>
                    <NumberIncrementStepper />
                    <NumberDecrementStepper />
                  </NumberInputStepper>
                </NumberInput>
                <NumberInput
                  size="sm"
                  maxW={16}
                  value={closeTime.minute}
                  min={0}
                  max={59}
                  step={5}
                  onChange={(value) =>
                    setEndTime({ ...closeTime, minute: parseInt(value) })
                  }
                >
                  <NumberInputField />
                  <NumberInputStepper>
                    <NumberIncrementStepper />
                    <NumberDecrementStepper />
                  </NumberInputStepper>
                </NumberInput>
              </Stack>
            </FormControl>

            <FormLabel mt={2}>Dostępne smaki obwarzanków</FormLabel>
            <CheckboxGroup colorScheme="teal">
              <VStack align="start">
                {flavourChecked.map((f, i) => (
                  <Checkbox
                    key={i}
                    isChecked={f.isChecked}
                    onChange={() => handleFlavoursToggled(i)}
                  >
                    {f.name}
                  </Checkbox>
                ))}
              </VStack>
            </CheckboxGroup>
            <FormLabel mt={2}>Płatności</FormLabel>
            <Checkbox
              isChecked={isCardChecked}
              colorScheme="teal"
              onChange={() =>
                setIsCardChecked((prevIsCardChecked) => !prevIsCardChecked)
              }
            >
              Płatność kartą
            </Checkbox>
            <VStack>
              <Button mt={2} colorScheme="teal" onClick={handleSubmit}>
                Potwierdź
              </Button>
            </VStack>
          </AlertDialogBody>
        </AlertDialogContent>
      </AlertDialogOverlay>
    </AlertDialog>
  );
}

export default NewShopForm;
