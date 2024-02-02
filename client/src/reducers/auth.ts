import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit"
import { api } from "../config/api" 
import { AxiosError } from "axios" 
import { parseErrorResponse } from "../helpers/functions" 
import { LOGIN_URL, REGISTER_URL } from "../config/constants" 

type User = {
	email: string
	password: string
}

type NewUser = User & {
	firstName: string
	lastName: string
}

type UserBasicInfo = {
	id: string
	email: string
	token: string
}

type UserProfileData = {
	firstName: string
	lastName: string
	email: string
}

type AuthApiState = {
	basicUserInfo?: UserBasicInfo | null
	userProfileData?: UserProfileData | null
	regSuccess: boolean
	errors: Array<string> 
}

export const login = createAsyncThunk("login", async (data: User, { rejectWithValue }) => {
	try {
		const response = await api.post(LOGIN_URL, data)	
		const resData = response.data
		localStorage.setItem("userInfo", JSON.stringify(resData))
		return resData
	}	
	catch (e) {
		const err = e as AxiosError
		return rejectWithValue(err.response?.data)
	}
})

export const register = createAsyncThunk("register", async (data: NewUser, { rejectWithValue }) => {
	try {
		const response = await api.post(REGISTER_URL, {
			"first_name": data.firstName,	
			"last_name": data.lastName,
			"email": data.email,
			"password": data.password,
		})
		return response.data
	}	
	catch (e) {
		const err = e as AxiosError
		return rejectWithValue(err.response?.data)
	}
})

export const getUser = createAsyncThunk("users/profile", async (userId: string) => {
	const response = await api.get(`/api/user/${userId}`)
	return response.data
})

const initialState: AuthApiState = {
	basicUserInfo: localStorage.getItem("userInfo") ? JSON.parse(localStorage.getItem("userInfo") as string) : null,
	userProfileData: null,
	regSuccess: false,
	errors: [],
}


const authSlice = createSlice({
	name: "auth",
	initialState,
	reducers: {
		logout: (state) => {
			localStorage.removeItem("userInfo")
			state.basicUserInfo = null
		}	
	},
	extraReducers: (builder) => {
		builder.addCase(login.pending, (state) => {
			state.errors = []
		}).addCase(
			login.fulfilled,
			(state, action: PayloadAction<UserBasicInfo>) => {
				state.basicUserInfo = action.payload
			}
		).addCase(login.rejected, (state, action) => {
			state.errors = parseErrorResponse(action.payload as Record<string, any>) || ["Login Failed"]
		}).addCase(register.pending, (state) => {
			state.errors = []
		}).addCase(register.fulfilled, (state) => {
			state.regSuccess = true 
		}).addCase(register.rejected, (state, action) => {
			state.errors = parseErrorResponse(action.payload as Record<string, any>) || ["User Registration Failed"]
		}).addCase(getUser.pending, (state) => {
	        state.errors = [];
	    }).addCase(getUser.fulfilled, (state, action) => {
	        state.userProfileData = action.payload;
	    }).addCase(getUser.rejected, (state, action) => {
	        state.errors =  parseErrorResponse(action.payload as Record<string, any>) || ["Get user profile data failed"];
        })
	}
})

export const { logout } = authSlice.actions 
export const authReducer = authSlice.reducer
