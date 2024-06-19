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
import { useContext, useRef, useState } from "react";
import { SingleDatepicker } from "chakra-dayzed-datepicker";
import { usePost } from "../hooks/usePost";
import { MarkerSetter } from "./Map";
import { type LatLngLiteral } from "leaflet";

type Flavour = {
  name: string;
  isChecked: boolean;
};

const flavours = ["Ser", "Mak", "Mieszany", "Sezam", "Sól"];

type AddShopProps = {
  position: LatLngLiteral;
  isOpen: boolean;
  onClose: () => void;
  // onAddShop: () => void;
  // shopData: { name: string; location: string; description: string; image: string };
};

function AddShop({ position, isOpen, onClose }: AddShopProps) {
  const [date, setDate] = useState(new Date());
  const setNewMarker = useContext(MarkerSetter);
  const [flavourChecked, setFlavourChecked] = useState<Flavour[]>(
    flavours.map((f) => {
      return {
        name: f,
        isChecked: false,
      };
    })
  );

  const prettyTime = (val: string) => {
    if (val.length === 1) {
      return "0" + val;
    }
    return val;
  };

  const post = usePost();

  const users = [
    "Pan Piotrek",
    "Pan Kamil",
    "Pan Wiktor",
    "Pan Bartek",
    "Pan Wojtek",
    "Pan Basia",
  ];

  const [startTimeHour, setStartTimeHour] = useState("8");
  const [startTimeMinute, setStartTimeMinute] = useState("0");

  const [endTimeHour, setEndTimeHour] = useState("16");
  const [endTimeMinute, setEndTimeMinute] = useState("0");

  // const [endTimeHour, setEndTimeHour] = useState(16);
  // const [endTimeMinute, setEndTimeMinute] = useState(0);

  const handleSubmit = () => {
    // console.log("Start Time:", startTimeHour, ":", startTimeMinute);
    // console.log("End Time:", endTimeHour, ":", endTimeMinute);
    console.log(position);
    const body = {
      ...position,
      name: users[Math.floor(Math.random() * users.length)],
      flavors: flavourChecked.filter((f) => f.isChecked).map((f) => f.name),
      card_payment: isCheckedCard,
      // time: [date.getUTCDate() + 1, date.getUTCMonth() + 1, date.getUTCFullYear()],
      is_open_today: true,
      start_time: prettyTime(startTimeHour) + ":" + prettyTime(startTimeMinute),
      end_time: prettyTime(endTimeHour) + ":" + prettyTime(endTimeMinute),
    };
    // console.log(body);
    post("/shops", body).catch(console.log);
    setNewMarker({
      ...body,
      id: "1",
      name: "temp",
    });
    onClose();
  };

  const [isCheckedCard, setIsCheckedCard] = useState(false);

  const handleTogglev2 = () => {
    setIsCheckedCard(!isCheckedCard);
  };

  const handleToggle = (i: number) => {
    flavourChecked[i].isChecked = !flavourChecked[i].isChecked;
    setFlavourChecked([...flavourChecked]);
  };

  const cancelRef = useRef(null);
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
                  value={startTimeHour}
                  min={0}
                  max={23}
                  onChange={setStartTimeHour}
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
                  value={startTimeMinute}
                  min={0}
                  max={59}
                  step={5}
                  onChange={setStartTimeMinute}
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
                  value={endTimeHour}
                  min={0}
                  max={23}
                  onChange={setEndTimeHour}
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
                  value={endTimeMinute}
                  min={0}
                  max={59}
                  step={5}
                  onChange={setEndTimeMinute}
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
                {flavourChecked.map((f, i) => {
                  return (
                    <Checkbox
                      key={i}
                      isChecked={f.isChecked}
                      onChange={() => {
                        handleToggle(i);
                      }}
                    >
                      {f.name}
                    </Checkbox>
                  );
                })}
              </VStack>
            </CheckboxGroup>
            <FormLabel mt={2}>Płatności</FormLabel>
            <Checkbox
              isChecked={isCheckedCard}
              colorScheme="teal"
              onChange={handleTogglev2}
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

export default AddShop;
