/**
 * @param string designating color such as "purple" or "blue"
 * @return string designating tailwind className for that color
 **/
export const buttonTheme = (color: string) => {
	const themes: Record<string, string> = {
		"red": "bg-red-500 hover:opacity-70",	
		"blue": "bg-blue-500 hover:opacity-70",
	}
	return `${themes[color]} text-white`
}
/**
 * @param string designating color such as "purple" or "blue"
 * @return string designating tailwind className for that color focus
 **/
export const textFocus = (color: string) => {
	const themes: Record<string, string> = {
		"blue": "focus:border-blue-500",
		"red": "focus:border-red-500"
	}
	return themes[color]
}

export const colorVariants: Record<string, string> = {
	"red": "text-red-500",	
	"lime": "text-lime-500",	
	"sky": "text-sky-500",	
}

export const borderVariants: Record<string, string> = {
	"red": "border-red-500",
	"lime": "border-lime-500",
	"sky": "border-sky-500"
}

export const styles: Record<string, string> = {
	"button" : "mr-2 shadow focus:shadow-outline focus:outline-none font-bold py-2 px-4 rounded",
	"textInput": `bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 leading-tight focus:outline-none focus:bg-white ${textFocus("blue")}`,
	"textInputDark": `appearance-none border-2 border-gray-200 text-gray-800 rounded w-full py-2 px-4 focus:outline-none leading-tight ${textFocus("blue")}`,
	"label": "block font-bold mb-2",
	"verticalLabel": "block font-bold",
	"checkbox": "w-4 h-4 bg-gray-100 border-gray-300 rounded dark:bg-gray-700 dark:border-gray-600",
	"icon": "w-8 h-8 hover:opacity-60"
}

export const zIndices: Record<string, string> = {
	"SIDEBAR": "z-40",
	"HEADER": "z-30",
}
