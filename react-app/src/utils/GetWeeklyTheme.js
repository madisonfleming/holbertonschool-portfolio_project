import { themes } from "./themes";

export function getWeeklyTheme() {
  const now = new Date();

  // get the week of the year doesnt change once refresh page
  const first_of_jan = new Date(now.getFullYear(), 0, 1);
  // num of days between 1st of Jan and today
  const numberOfDays = Math.floor((now - first_of_jan) / (24 * 60 * 60 * 1000));
  const weekNumber = Math.ceil((now.getDay() + 1 + numberOfDays) / 7);

  // Selecs a theme based on the week number
  const index = weekNumber % themes.length;

  return themes[index];
}
