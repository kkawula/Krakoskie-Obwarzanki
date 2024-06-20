export interface ITime {
  hour: number;
  minute: number;
}
export const prettyTime = (time: ITime) =>
  `${addLeadingZero(time.hour)}:${addLeadingZero(time.minute)}`;

// class Time {
//   constructor(public hour: number, public minute: number) {
//     this.hour = hour;
//     this.minute = minute;
//   }

//   setHour(hour: number | string) {
//     if (typeof hour === "string") {
//       hour = parseInt(hour);
//     }
//     if (hour < 0 || hour > 23) {
//       throw new Error("Hour must be between 0 and 23");
//     }
//     this.hour = hour;
//     return new Time(this.hour, this.minute);
//   }
//   setMinute(minute: number | string) {
//     if (typeof minute === "string") {
//       minute = parseInt(minute);
//     }
//     if (minute < 0 || minute > 59) {
//       throw new Error("Minute must be between 0 and 59");
//     }
//     this.minute = minute;

//     return new Time(this.hour, this.minute);
//   }

//   toString() {
//     return `${addLeadingZero(this.hour)}:${addLeadingZero(this.minute)}`;
//   }
// }
const addLeadingZero = (value: number) => String(value).padStart(2, "0");
