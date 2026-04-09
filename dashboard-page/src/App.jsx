import weatherData from "../../data/weather.json";
import taskData from "../../data/tasks.json";
const icons = import.meta.glob("./assets/icons/*.svg", { eager: true });
import { CircleCheck, Recycle, Ellipsis } from 'lucide-react'
import StyledText from "./StyledText";


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
      <div className="my-16 mx-8 flex flex-col  space-y-4">

        <div className="flex justify-center mb-8!">
          <StyledText size="large" font="bold">
            Poniedziałek, 9 kwietnia
          </StyledText>
        </div>

        <div className="flex justify-center gap-4 bg-primary p-4 rounded-3xl">
          {weatherData.map((entry, index) => (
            <div key={index} className="flex flex-col items-center">
              <StyledText>
                {entry.hour}:00
              </StyledText>
              <img src={getIcon(entry.weather_code)} className="w-20 h-20" />
              <StyledText size="large">
                {entry.temp}°C
              </StyledText>
            </div>
          ))}
        </div>

        <div className="flex flex-col justify-center gap-8 bg-primary p-4 rounded-3xl">
          {taskData.tasks.map((entry, index) => (
            <div key={index} className="flex items-center space-x-4">
              <CircleCheck />
              <StyledText>
                {entry.title}
              </StyledText>
            </div>
          ))}
          {taskData["more-than-three"] ?
            (<div className="w-full flex justify-center">
              <Ellipsis size={30} />
            </div>) :
            (<></>)}
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="flex flex-col justify-center items-center gap-4 p-4 rounded-3xl bg-primary">
            <StyledText>
              Papier
            </StyledText>
            <Recycle size={30} />
            <StyledText>
              10 kwietnia
            </StyledText>
          </div>

          <div className="flex flex-col justify-center gap-8 p-6 rounded-3xl bg-primary">
          </div>
        </div>
      </div>

    </div>
  )
}

export default App
