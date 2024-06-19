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
import { LatLngLiteral } from "leaflet";
import { Time } from "../utils/time";

interface Flavour {
  name: string;
  isChecked: boolean;
}
interface AddShopProps {
  position: LatLngLiteral;
  isOpen: boolean;
  onClose: () => void;
  // onAddShop: () => void;
  // shopData: { name: string; location: string; description: string; image: string };
}
const flavours = ["Ser", "Mak", "Mieszany", "Sezam", "Sól"];
const users = ["Pan Piotrek", "Pan Kamil", "Pan Wiktor", "Pan Bartek", "Pan Wojtek", "Pan Basia"];

function AddShop({ position, isOpen, onClose }: AddShopProps) {
  const setNewMarker = useContext(MarkerSetter);

  const [flavourChecked, setFlavourChecked] = useState(
    flavours.map((f) => {
      return {
        name: f,
        isChecked: false,
      } as Flavour;
    })
  );
  const [date, setDate] = useState(new Date());
  const [startTime, setStartTime] = useState(new Time(8, 0));
  const [endTime, setEndTime] = useState(new Time(16, 0));
  const [isCardChecked, setIsCheckedCard] = useState(false);

  const cancelRef = useRef(null);

  const post = usePost();

  const handleSubmit = () => {
    const body = {
      ...position,
      name: users[Math.floor(Math.random() * users.length)], // ! temporary
      flavors: flavourChecked.filter((f) => f.isChecked).map((f) => f.name),
      card_payment: isCardChecked,
      is_open_today: true,
      start_time: startTime.toString(),
      end_time: endTime.toString(),
    };
    post("/shops", body).catch(console.log);
    setNewMarker({
      ...body,
      id: "1",
      name: "temp",
    });
    onClose();
  };

  const handleFlavoursToggled = (idx: number) => {
    const nextFlavourChecked = flavourChecked.map((f, index) =>
      index === idx ? { ...f, isChecked: !f.isChecked } : f
    );
    setFlavourChecked(nextFlavourChecked);
  };
  return (
    <AlertDialog isOpen={isOpen} onClose={onClose} leastDestructiveRef={cancelRef}>
      <AlertDialogOverlay>
        <AlertDialogContent mt={10}>
          <AlertDialogHeader>Nowe stoisko</AlertDialogHeader>
          <AlertDialogBody>
            <FormLabel>Data:</FormLabel>
            <SingleDatepicker name="date-input" date={date} onDateChange={setDate} />

            <FormControl>
              <FormLabel mt={4}>Godzina rozpoczęcia:</FormLabel>
              <Stack shouldWrapChildren direction="row" align={"left"}>
                <NumberInput
                  size="sm"
                  maxW={16}
                  value={startTime.hour}
                  min={0}
                  max={23}
                  onChange={(value) => setStartTime(startTime.setHour(value))}
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
                  value={startTime.minute}
                  min={0}
                  max={59}
                  step={5}
                  onChange={(value) => setStartTime(startTime.setMinute(value))}
                >
                  <NumberInputField />
                  <NumberInputStepper>
                    <NumberIncrementStepper />
                    <NumberDecrementStepper />
                  </NumberInputStepper>
                </NumberInput>
              </Stack>
              <FormLabel mt={2}>Godzina zakończenia:</FormLabel>
              <Stack shouldWrapChildren direction="row" align={"left"}>
                <NumberInput
                  size="sm"
                  maxW={16}
                  value={endTime.hour}
                  min={0}
                  max={23}
                  onChange={(value) => setEndTime(endTime.setHour(value))}
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
                  value={endTime.minute}
                  min={0}
                  max={59}
                  step={5}
                  onChange={(value) => setEndTime(endTime.setMinute(value))}
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
              <VStack align={"start"}>
                {flavourChecked.map((f, i) => {
                  return (
                    <Checkbox
                      key={i}
                      isChecked={f.isChecked}
                      onChange={() => handleFlavoursToggled(i)}
                    >
                      {f.name}
                    </Checkbox>
                  );
                })}
              </VStack>
            </CheckboxGroup>
            <FormLabel mt={2}>Płatności</FormLabel>
            <Checkbox
              isChecked={isCardChecked}
              colorScheme="teal"
              onChange={() => setIsCheckedCard(!isCardChecked)}
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
