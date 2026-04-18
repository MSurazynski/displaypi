import React from "react";

/**
 * WeatherTemperatureChart
 *
 * E-ink friendly stepped weather chart with temperature + optional rain line.
 */
export default function WeatherTemperatureChart({ data }) {
  const hours = data?.hours ?? [];

  if (!hours.length) {
    return (
      <div className="w-full rounded-xl border border-neutral-300 bg-white p-4 text-sm text-neutral-600">
        No weather data available.
      </div>
    );
  }

  const width = 400;
  const height = 120;

  const paddingNoRain = {
    top: 16,
    right: 30,
    bottom: 30,
    left: 35,
  };

  const paddingWithRain = {
    top: 16,
    right: 55,
    bottom: 28,
    left: 35,
  };

  const rainValues = hours.map((item) => item.rain_mm ?? 0);
  const hasRain = rainValues.some((value) => value > 0);

  const padding = hasRain ? paddingWithRain : paddingNoRain;

  const innerWidth = width - padding.left - padding.right;
  const innerHeight = height - padding.top - padding.bottom;

  const temps = hours.map((item) => item.temp ?? 0);
  const minTemp = Math.min(...temps);
  const maxTemp = Math.max(...temps);

  const minRain = hasRain ? Math.min(...rainValues) : 0;
  const maxRain = hasRain ? Math.max(...rainValues) : 0;

  const tempChartMin = minTemp - 1;
  const tempChartMax = maxTemp + 1;
  const tempChartRange = Math.max(1, tempChartMax - tempChartMin);

  const rainChartMax = hasRain ? Math.max(maxRain, 1) : 1;

  const getX = (index) => {
    if (hours.length === 1) return padding.left + innerWidth / 2;
    return padding.left + (index / (hours.length - 1)) * innerWidth;
  };

  const getTempY = (temp) => {
    const normalized = (temp - tempChartMin) / tempChartRange;
    return padding.top + innerHeight - normalized * innerHeight;
  };

  const getRainY = (rain) => {
    // Rain uses only half of the vertical range
    const normalized = rain / rainChartMax;
    const scaled = normalized * 0.5; // <-- key change
    return padding.top + innerHeight - scaled * innerHeight;
  };

  const tempPoints = hours.map((item, index) => ({
    x: getX(index),
    y: getTempY(item.temp ?? 0),
    value: item.temp ?? 0,
    hour: item.hour,
  }));

  const rainPoints = hours.map((item, index) => ({
    x: getX(index),
    y: getRainY(item.rain_mm ?? 0),
    value: item.rain_mm ?? 0,
    hour: item.hour,
  }));

  const midpoints = [];
  for (let i = 0; i < tempPoints.length - 1; i++) {
    midpoints.push((tempPoints[i].x + tempPoints[i + 1].x) / 2);
  }

  const buildStepPath = (points) => {
    if (!points.length) return "";

    let path = `M ${points[0].x} ${points[0].y}`;

    for (let i = 0; i < points.length - 1; i++) {
      const midX = (points[i].x + points[i + 1].x) / 2;
      path += ` L ${midX} ${points[i].y}`;
      path += ` L ${midX} ${points[i + 1].y}`;
      path += ` L ${points[i + 1].x} ${points[i + 1].y}`;
    }

    return path;
  };

  const buildAreaPath = (points) => {
    if (!points.length) return "";

    let path = `M ${points[0].x} ${padding.top + innerHeight}`;
    path += ` L ${points[0].x} ${points[0].y}`;

    for (let i = 0; i < points.length - 1; i++) {
      const midX = (points[i].x + points[i + 1].x) / 2;
      path += ` L ${midX} ${points[i].y}`;
      path += ` L ${midX} ${points[i + 1].y}`;
      path += ` L ${points[i + 1].x} ${points[i + 1].y}`;
    }

    path += ` L ${points[points.length - 1].x} ${padding.top + innerHeight} Z`;
    return path;
  };

  const tempLinePath = buildStepPath(tempPoints);
  const tempAreaPath = buildAreaPath(tempPoints);
  const rainLinePath = hasRain ? buildStepPath(rainPoints) : "";

  return (
    <div className="max-w">
      <svg
        viewBox={`0 0 ${width} ${height}`}
        className="h-auto w-full"
        role="img"
      >
        {/* Bottom axis */}
        <line
          x1={padding.left}
          y1={padding.top + innerHeight}
          x2={padding.left + innerWidth}
          y2={padding.top + innerHeight}
          stroke="#000000"
          strokeWidth="1"
        />

        {/* Temperature max label */}
        <text
          x={padding.left - 6}
          y={padding.top + 4}
          textAnchor="end"
          className="fill-neutral-800 text-xs font-medium"
        >
          {maxTemp}°
        </text>

        {/* Temperature min label */}
        <text
          x={padding.left - 6}
          y={padding.top + innerHeight}
          textAnchor="end"
          dominantBaseline="ideographic"
          className="fill-neutral-800 text-xs font-medium"
        >
          {minTemp}°
        </text>

        {/* Rain max label */}
        {hasRain && (
          <text
            x={width - padding.right + 6}
            y={padding.top + 4}
            textAnchor="start"
            className="fill-neutral-800 text-xs font-medium"
          >
            {maxRain * 2} mm
          </text>
        )}

        {/* Rain min label */}
        {hasRain && (
          <text
            x={width - padding.right + 6}
            y={padding.top + innerHeight}
            textAnchor="start"
            dominantBaseline="ideographic"
            className="fill-neutral-800 text-xs font-medium"
          >
            {minRain} mm
          </text>
        )}

        {/* Temperature area fill */}
        <path d={tempAreaPath} fill="#fa7000" fillOpacity="0.25" />

        {/* Temperature step line */}
        <path
          d={tempLinePath}
          fill="none"
          stroke="#fa7000"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="miter"
        />

        {/* Rain step line */}
        {hasRain && (
          <path
            d={rainLinePath}
            fill="none"
            stroke="#0000FF"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="miter"
          />
        )}

        {/* Temperature points */}
        {tempPoints.map((point) => (
          <circle
            key={`temp-${point.hour}`}
            cx={point.x}
            cy={point.y}
            r="2.5"
            fill="#fa7000"
          />
        ))}

        {/* Rain points, only where rain > 0 */}
        {hasRain &&
          rainPoints
            .filter((point) => point.value > 0)
            .map((point) => (
              <circle
                key={`rain-${point.hour}`}
                cx={point.x}
                cy={point.y}
                r="2"
                fill="#0000FF"
              />
            ))}

        {/* Hour labels */}
        {tempPoints.map((point) => (
          <text
            key={`hour-${point.hour}`}
            x={point.x}
            y={height - 8}
            textAnchor="middle"
            className="fill-neutral-700 text-sm font-medium"
          >
            {point.hour}
          </text>
        ))}
      </svg>
    </div>
  );
}
