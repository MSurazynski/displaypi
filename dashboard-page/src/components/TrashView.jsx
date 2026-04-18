import StyledText from "@comp/StyledText";

// Maps labels like "mixed" to text to render like "Zmieszane".
function mapTrashLabel(label) {
  const newLabel = {
    garden: "Śmieci ogrodowe",
    mixed: "Zmieszanie",
    paper: "Papiery",
  }[label];

  return newLabel;
}

// Takes a list of dates and returns the closest upcominf date.
function getNearestUpcomingDay(data) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const nearestDate = data
    .map((d) => new Date(d))
    .filter((d) => d >= today)
    .sort((a, b) => a - b)[0];

  return nearestDate;
}

// Returns nearest ucpoming day for 3 categories of trash.
function getNearestTrashDays(trashData) {
  return {
    paper: getNearestUpcomingDay(trashData.paper),
    mixed: getNearestUpcomingDay(trashData.mixed),
    garden: getNearestUpcomingDay(trashData.garden),
  };
}

// Output string representation of the date or string "jutro" or string "dzisiaj".
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

export default function TrashView({ trashData }) {
  return (
    <div className="flex flex-col justify-start items-start px-4 gap-2">
      <StyledText align="left" size="large">
        Śmieci
      </StyledText>

      <div className="flex flex-col gap-1">
        {Object.entries(getNearestTrashDays(trashData))
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
  );
}
