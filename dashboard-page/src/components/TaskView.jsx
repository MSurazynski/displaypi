import StyledText from "@comp/StyledText";

export default function TaskView({ taskData }) {
  return taskData.tasks.length > 0 ? (
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
        <StyledText align="left"> {"Brak zadań :)"} </StyledText>
      </div>
    </div>
  );
}
