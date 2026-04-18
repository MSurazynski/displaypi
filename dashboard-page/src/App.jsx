import weatherData from "../../assets/json/weather.json";
import taskData from "../../assets/json/tasks.json";
import trashData from "../../assets/json/trash.json";
import TaskView from "@comp/TaskView";
import TrashView from "@comp/TrashView";
import WeatherView from "@comp/WeatherView";
import DateHeaderView from "@comp/DateHeaderView";
import AniversaryView from "@comp/AniversaryView";

function App() {
  return (
    <div className="absolute w-full h-full bg-backrgound-paper">
      <div className="my-16 mx-8 flex flex-col space-y-6">
        {/* header */}
        <DateHeaderView weatherData={weatherData} />

        {/* anniversary */}
        <AniversaryView />

        {/* weather */}
        <WeatherView weatherData={weatherData} />

        {/* tasks */}
        <TaskView taskData={taskData} />

        {/* Trash */}
        <TrashView trashData={trashData} />
      </div>
    </div>
  );
}

export default App;
