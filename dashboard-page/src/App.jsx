import weatherData from "../../assets/json/weather.json";
import taskData from "../../assets/json/tasks.json";
import dateData from "../../assets/json/date.json";
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
    <div className="absolute w-full h-full bg-backrgound-paper">
      <div className="my-16 mx-8 flex flex-col space-y-4">

        <div className="flex justify-center mb-8!">
          <StyledText size="veryLarge" font="bold">
            {dateData[0]}
          </StyledText>
        </div>

        <div className="flex justify-center p-4 rounded-3xl">
          {weatherData.map((entry, index) => (
            <div key={index} className="flex flex-col items-center">
              <StyledText>
                {entry.hour}:00
              </StyledText>
              <img src={getIcon(entry.weather_code)} className="w-30 h-30" />
              <StyledText size="large">
                {entry.temp}°C
              </StyledText>
            </div>
          ))}
        </div>

        <div className="flex flex-col justify-center p-4 rounded-3xl">
          <div className="flex flex-col gap-2">
            <StyledText size="large" align="left">
                Zadania
            </StyledText>
            <hr className="border-t border-text"/>
            {taskData.tasks.slice(0, 3).map((entry, index) => (
              <div key={index} className="flex-col items-start justify-items-start space-x-4">
                <StyledText>
                  {(index+1) + ". " + entry.title}
                </StyledText>
                
                <hr className="w-full border-t text-text mt-2"/>
              </div>
            ))}
          </div>
          {taskData["more-than-three"] ?
            (<div className="w-full flex justify-start mt-2">
                <StyledText>
                    {"Pozostałych zadań: " + (taskData.tasks.length - 3)}
                </StyledText>
            </div>) :
            (<></>)}
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div className="flex flex-col justify-center items-center gap-4 p-4 rounded-3x">
            <StyledText>
              Papier
            </StyledText>
            <Recycle size={30} />
            <StyledText>
              10 kwietnia
            </StyledText>
          </div>

          {/* <div className="flex flex-col justify-center gap-8 p-6 rounded-3xl bg-primary">
          </div> */}
        </div>
      </div>

    </div>
  )
}

export default App
