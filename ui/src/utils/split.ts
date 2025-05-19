export function splitGroup(text: string): string[] {
    const re = /[^\s"]+|"([^"]*)"/gi
    const arr: string[] = []
    do {
        var match = re.exec(text || '')
        if (match !== null) {
            arr.push(match[1] ? match[1] : match[0])
        }
    } while (match !== null)
    return arr
}
