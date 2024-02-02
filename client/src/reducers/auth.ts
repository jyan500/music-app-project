import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit"
import { api } from "../config/api" 
import { AxiosError } from "axios" 
import { parseErrorResponse } from "../helpers/functions" 

type User = {
	email: string
	password: string
}

type NewUser = User & {
	name: string
}

type UserBasicInfo = {
	id: string
	email: string
	token: string
}

type UserProfileData = {
	name: string
	email: string
}

type AuthApiState = {
	basicUserInfo?: UserBasicInfo | null
	userProfileData?: UserProfileData | null
	status: "idle" | "loading" | "failed"
	errors: Array<string> 
}

export const login = createAsyncThunk("login", async (data: User, { rejectWithValue }) => {
	try {
		const response = await api.post("/api/user/token/", data)	
		const resData = response.data
		localStorage.setItem("userInfo", JSON.stringify(resData))
		return resData
	}	
	catch (e) {
		console.log("e: ", e)
		const err = e as AxiosError
		console.log("err: ", err.response?.data)
		return rejectWithValue(err.response?.data)
	}
})

export const logout = createAsyncThunk("logout", async () => {
	// create logout endpoint first...
	localStorage.removeItem("userInfo")
})

export const getUser = createAsyncThunk("users/profile", async (userId: string) => {
	const response = await api.get(`/api/user/${userId}`)
	return response.data
})

const initialState: AuthApiState = {
	basicUserInfo: localStorage.getItem("userInfo") ? JSON.parse(localStorage.getItem("userInfo") as string) : null,
	userProfileData: null,
	status: "idle",
	errors: [],
}


const authSlice = createSlice({
	name: "auth",
	initialState,
	reducers: {},
	extraReducers: (builder) => {
		builder.addCase(login.pending, (state) => {
			state.status = "loading"	
			state.errors = []
		}).addCase(
			login.fulfilled,
			(state, action: PayloadAction<UserBasicInfo>) => {
				state.status = "idle"
				state.basicUserInfo = action.payload
			}
		).addCase(login.rejected, (state, action) => {
			console.log("payload: ", action.payload)
			state.status = "failed"	
			state.errors = parseErrorResponse(action.payload as Record<string, any>) || ["Login Failed"]
		}).addCase(getUser.pending, (state) => {
	        state.status = "loading"
	        state.errors = [];
	    }).addCase(getUser.fulfilled, (state, action) => {
	        state.status = "idle"
	        state.userProfileData = action.payload;
	    }).addCase(getUser.rejected, (state, action) => {
	        state.status = "failed"
	        state.errors =  parseErrorResponse(action.payload as Record<string, any>) || ["Get user profile data failed"];
        })
	}
})

export const authReducer = authSlice.reducer
