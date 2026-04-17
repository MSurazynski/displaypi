import weatherData from "../../assets/json/weather.json";
import taskData from "../../assets/json/tasks.json";
import dateData from "../../assets/json/date.json";
import trashData from "../../assets/json/trash.json";
const icons = import.meta.glob("./assets/icons/*.svg", { eager: true });
import StyledText from "./StyledText";
import WeatherTemperatureChart from "./WeatherTemperatureChart";

function getIcon(code) {
  const name = WMO_TO_ICON[code];
  const key = `./assets/icons/${name}.svg`;
  return icons[key]?.default;
}

function mapTrashLabel(label) {
  const newLabel = {
    garden: "Śmieci ogrodowe",
    mixed: "Zmieszanie",
    paper: "Papiery",
  }[label];

  return newLabel;
}

function getNearestUpcomingDay(data) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const nearestDate = data
    .map((d) => new Date(d))
    .filter((d) => d >= today)
    .sort((a, b) => a - b)[0];

  return nearestDate;
}

function getNearestTrashDays() {
  return {
    paper: getNearestUpcomingDay(trashData.paper),
    mixed: getNearestUpcomingDay(trashData.mixed),
    garden: getNearestUpcomingDay(trashData.garden),
  };
}

// TODO REMAP
const WMO_TO_ICON = {
  0: "clear-day",
  1: "partly-cloudy-day",
  2: "partly-cloudy-day",
  3: "overcast",
  45: "mist",
  48: "mist",
  51: "partly-cloudy-day-drizzle",
  53: "partly-cloudy-day-drizzle",
  55: "rain",
  61: "rain",
  63: "rain",
  65: "rain",
  71: "snow",
  73: "snow",
  75: "snow",
  80: "partly-cloudy-day-rain",
  81: "rain",
  82: "rain",
  85: "partly-cloudy-day-snow",
  95: "thunderstorms",
  96: "thunderstorms-rain",
  99: "thunderstorms-rain",
};

const monthTranslated = {
  January: "Styczeń",
  February: "Luty",
  March: "Marzec",
  April: "Kwiecień",
  May: "Maj",
  June: "Czerwiec",
  July: "Lipiec",
  August: "Styczeń",
  September: "Wrzesień",
  October: "Październik",
  November: "Listopad",
  December: "Grudzień",
};

const dayTranslated = {
  Monday: "Poniedziałek",
  Tuesday: "Wtorek",
  Wednesday: "Środa",
  Thursday: "Czwartek",
  Friday: "Piątek",
  Saturday: "Sobota",
  Sunday: "Niedziela",
};

function App() {
  const weekDayName = dayTranslated[dateData[0].split(",")[0]];
  const dayNumber = dateData[0].split(",")[1].split(" ")[1];
  const monthName = monthTranslated[dateData[0].split(",")[1].split(" ").pop()];

  return (
    <div className="absolute w-full h-full bg-backrgound-paper">
      <div className="my-16 mx-8 flex flex-col space-y-6">
        <div className="flex items-center justify-between px-4">
          <StyledText size="veryLarge" align="left" font="bold">
            {`${weekDayName}, ${dayNumber} ${monthName}`}
          </StyledText>
          <img
            src={getIcon(weatherData.day.weather_code)}
            className="w-20 h-20"
          />
        </div>

        <div className="flex flex-col gap-2 px-4">
          <StyledText align="left" size="large">
            Pogoda
          </StyledText>
          <WeatherTemperatureChart data={weatherData} className="w-30 h-30" />
        </div>

        <div className="flex flex-col justify-center px-4">
          <div className="flex flex-col gap-2">
            <StyledText size="large" align="left">
              Zadania
            </StyledText>
            <hr className="border-t border-text" />
            {taskData.tasks.slice(0, 3).map((entry, index) => (
              <div
                key={index}
                className="flex-col items-start justify-items-start space-x-4"
              >
                <StyledText>{index + 1 + ". " + entry.title}</StyledText>
                <hr className="w-full border-t text-text mt-2" />
              </div>
            ))}
          </div>
          {taskData.tasks.length > 3 ? (
            <div className="w-full flex justify-start mt-2">
              <StyledText>
                {"Pozostałych zadań: " + (taskData.tasks.length - 3)}
              </StyledText>
            </div>
          ) : (
            <></>
          )}
        </div>

        <div className="flex, justify-start items-start px-4">
          <StyledText align="left" size="large">
            Śmieci
          </StyledText>
          {Object.entries(getNearestTrashDays()).map(([type, date]) => (
            <div key={type}>
              <StyledText align="left">
                {mapTrashLabel(type) + ": " + date.toLocaleDateString()}
              </StyledText>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
