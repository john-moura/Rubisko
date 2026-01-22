export const formatLocalDate = (utcString: string | undefined): string => {
    if (!utcString) return '-'

    try {
        const date = new Date(utcString)
        if (isNaN(date.getTime())) return utcString

        const year = date.getFullYear()
        const month = String(date.getMonth() + 1).padStart(2, '0')
        const day = String(date.getDate()).padStart(2, '0')
        const hours = String(date.getHours()).padStart(2, '0')
        const minutes = String(date.getMinutes()).padStart(2, '0')

        return `${year}-${month}-${day} ${hours}:${minutes}`
    } catch (e) {
        return utcString
    }
}
