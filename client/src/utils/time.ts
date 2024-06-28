export type Time = {
  hour: number;
  minute: number;
};
export const prettyTime = (time: Time) =>
  `${addLeadingZero(time.hour)}:${addLeadingZero(time.minute)}`;
// time.minute * 60 + time.hour * 60 * 60;

const addLeadingZero = (value: number) => String(value).padStart(2, "0");
