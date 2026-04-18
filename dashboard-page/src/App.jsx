import weatherData from "../../assets/json/weather.json";
import taskData from "../../assets/json/tasks.json";
import dateData from "../../assets/json/date.json";
import trashData from "../../assets/json/trash.json";
const icons = import.meta.glob("./assets/icons/*.svg", { eager: true });
import StyledText from "@comp/StyledText";
import WeatherTemperatureChart from "@comp/WeatherTemperatureChart";

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

// capitalizes first letter of a string
const capitalize = (text) => text.charAt(0).toUpperCase() + text.slice(1);

/**
 * Output string representation of the date or string "jutro" or string "dzisiaj".
 */
function formatTrashDate(date) {
  const input = new Date(date);

  const d = new Date(input.getFullYear(), input.getMonth(), input.getDate());

  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const tomorrow = new Date(
    now.getFullYear(),
    now.getMonth(),
    now.getDate() + 1,
  );

  if (d.getTime() === today.getTime()) return "Dzisiaj";
  if (d.getTime() === tomorrow.getTime()) return "Jutro";

  return d.toLocaleDateString("pl-PL");
}

function App() {
  const date = new Date();
  const dayNumber = date.getDate();
  const weekDayName = capitalize(
    date.toLocaleDateString("pl-PL", { weekday: "long" }),
  );
  const monthName = capitalize(
    date.toLocaleDateString("pl-PL", { month: "long" }),
  );

  return (
    <div className="absolute w-full h-full bg-backrgound-paper">
      <div className="my-16 mx-8 flex flex-col space-y-6">
        {/* Dzień i miesiąc */}
        <div className="flex items-center justify-between px-4 mb-0!">
          <StyledText size="veryLarge" align="left" font="bold">
            {`${weekDayName}, ${dayNumber} ${monthName}`}
          </StyledText>
          <img
            src={getIcon(weatherData.day.weather_code)}
            className="w-20 h-20"
          />
        </div>

        {/* 27ty miesiąca */}
        {dayNumber == 27 && (
          <div className="flex flex-col gap-2 px-4">
            <StyledText align="left" size="large" font="semiBold">
              Dzisiaj 27ty!
            </StyledText>
          </div>
        )}

        {/* pogoda */}
        <div className="flex flex-col">
          <div className="flex flex-col gap-2 px-4">
            <StyledText align="left" size="large">
              Pogoda
            </StyledText>
          </div>

          <WeatherTemperatureChart data={weatherData} className="w-30 h-30" />
        </div>

        {taskData.tasks.length > 0 ? (
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
                  <StyledText align="left">
                    {index + 1 + ". " + entry.title}
                  </StyledText>
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
        ) : (
          <div className="flex flex-col justify-center px-4">
            <div className="flex flex-col gap-2">
              <StyledText size="large" align="left">
                Zadania
              </StyledText>
              <StyledText align="left"> Brak zadań :) </StyledText>
            </div>
          </div>
        )}

        {/* Component ze śmieciami */}
        <div className="flex flex-col justify-start items-start px-4 gap-2">
          <StyledText align="left" size="large">
            Śmieci
          </StyledText>

          <div className="flex flex-col gap-1">
            {Object.entries(getNearestTrashDays())
              .sort(([, dateA], [, dateB]) => new Date(dateA) - new Date(dateB))
              .map(([type, date]) => (
                <div key={type}>
                  <StyledText align="left">
                    {mapTrashLabel(type) + ": " + formatTrashDate(date)}
                  </StyledText>
                </div>
              ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
