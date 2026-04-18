import StyledText from "@comp/StyledText";
import WeatherTemperatureChart from "@comp/WeatherTemperatureChart";

export default function WeatherView({ weatherData }) {
  return (
    <div className="flex flex-col">
      <div className="flex flex-col gap-2 px-4">
        <StyledText align="left" size="large">
          Pogoda
        </StyledText>
      </div>

      <WeatherTemperatureChart data={weatherData} className="w-30 h-30" />
    </div>
  );
}
