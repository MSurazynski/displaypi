import weatherData from "../../data/weather.json";
import taskData from "../../data/tasks.json";
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
      <div className="my-16 mx-8 flex flex-col space-y-12">

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

        <div className="flex flex-col justify-center gap-8 bg-primary p-8 rounded-xl">
          {taskData.tasks.map((entry) => (
            <div className="flex items-center space-x-6">
              <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-circle-check-big-icon lucide-circle-check-big"><path d="M21.801 10A10 10 0 1 1 17 3.335" /><path d="m9 11 3 3L22 4" /></svg>
              <h2 className="text-text text-xl font-semibold">
                {entry.title}
              </h2>
            </div>
          ))}
          {taskData["more-than-three"] ?
            (<div className="w-full flex justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-ellipsis-icon lucide-ellipsis"><circle cx="12" cy="12" r="1" /><circle cx="19" cy="12" r="1" /><circle cx="5" cy="12" r="1" /></svg>
            </div>) :
            (<></>)}
        </div>
      </div>

    </div>
  )
}

export default App
