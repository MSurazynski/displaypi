import StyledText from "@comp/StyledText";

export default function AniversayView() {
  const dayNumber = new Date().getDate();

  return dayNumber == 27 ? (
    <div className="flex flex-col gap-2 px-4">
      <StyledText align="left" size="large" font="semiBold">
        Dzisiaj 27t!
      </StyledText>

      <StyledText align="left">Napisz Mai, że ją kochasz!</StyledText>
    </div>
  ) : (
    <></>
  );
}
