import axios from "axios"
import { BACKEND_BASE_URL } from "./constants"

export const api = axios.create({
	baseURL: BACKEND_BASE_URL,
	// send cookies
	// withCredentials: true
})

