export interface ITime {
  hour: number;
  minute: number;
}
export const prettyTime = (time: ITime) =>
  `${addLeadingZero(time.hour)}:${addLeadingZero(time.minute)}`;

const addLeadingZero = (value: number) => String(value).padStart(2, "0");
