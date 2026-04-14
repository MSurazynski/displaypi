/**
 * Component with styled text.
 * @param {string} size small | medium | large | veryLarge
 */
export default function StyledText({ children, size = "medium", align = "center", font = "semiBold" }) {
    const textSize = {
        small: "text-sm",
        medium: "text-md",
        large: "text-xl",
        veryLarge: "text-3xl"
    }[size]

    const textAlign = {
        left: "text-left",
        center: "text-center",
        right: "text-right"
    }[align]

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
