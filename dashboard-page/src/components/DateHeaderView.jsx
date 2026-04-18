import StyledText from "@comp/StyledText";
const icons = import.meta.glob("../assets/icons/*.svg", { eager: true });

function getIcon(code) {
  const name = WMO_TO_ICON[code];
  const key = `../assets/icons/${name}.svg`;
  return icons[key]?.default;
}

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

export default function ({ weatherData }) {
  const date = new Date();
  const dayNumber = date.getDate();
  const weekDayName = capitalize(
    date.toLocaleDateString("pl-PL", { weekday: "long" }),
  );
  const monthName = capitalize(
    date.toLocaleDateString("pl-PL", { month: "long" }),
  );

  return (
    <div className="flex items-center justify-between px-4 mb-0!">
      <StyledText size="veryLarge" align="left" font="bold">
        {`${weekDayName}, ${dayNumber} ${monthName}`}
      </StyledText>
      <img src={getIcon(weatherData.day.weather_code)} className="w-20 h-20" />
    </div>
  );
}
