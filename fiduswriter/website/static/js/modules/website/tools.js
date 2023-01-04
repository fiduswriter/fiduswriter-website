export function getTextContent(node) {
    let text = ""
    if (node.attrs && node.attrs.hidden) {
        return text
    }
    if (node.type === "text") {
        text += node.text
    }
    if (node.content) {
        text += node.content.map(subNode => getTextContent(subNode)).join("")
    }
    if (["paragraph", "heading1", "heading2", "heading3", "heading4", "heading5", "heading6"].includes(node.type)) {
        text += "\n"
    }
    return text
}
