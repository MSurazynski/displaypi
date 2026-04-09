export default function StyledText({ children, size = "medium", align = "center", font = "semiBold" }) {
    const textSize = {
        small: "text-sm",
        medium: "text-md",
        large: "text-xl"
    }[size]

    let textAlign = "text-center";
    switch (align) {
        case "left":
            textAlign = "text-left";
            break;
        case "right":
            textAlign = "text-right";
            break;
        default:
            textAlign = "text-center";
    }

    const fontWeight = {
        light: "font-light",
        bold: "font-bold",
        italic: "font-italic",
        normal: "font-normal",
        semiBold: "font-semibold",
    }[font]

    return (
        <h2 className={`text-text font-lora ${textSize} ${textAlign} ${fontWeight}`}>
            {children}
        </h2>
    )
}
