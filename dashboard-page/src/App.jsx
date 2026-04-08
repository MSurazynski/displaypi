import weatherData from "../../data/weather.json";
const icons = import.meta.glob("./assets/icons/*.svg", { eager: true });

function getIcon(code) {
  const name = WMO_TO_ICON[code];
  const key = `./assets/icons/${name}.svg`;
  return icons[key]?.default;
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

function App() {

  return (
    <div className="absolute w-full h-full bg-background-sky">
      <div className="my-12 mx-8">
        <div className="flex justify-center gap-8 bg-primary p-4 rounded-xl">
          {weatherData.map((entry) => (
            <div key={entry.hour} className="flex flex-col items-center">
              <h2 className="text-text text-xl font-semibold">
                {entry.hour}:00
              </h2>
              <img src={getIcon(entry.weather_code)} className="w-22 h-22" />
              <h2 className="text-text text-2xl font-bold">
                {entry.temp}°C
              </h2>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default App
