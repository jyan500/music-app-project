import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit"
import { api } from "../config/api" 

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
	error: string | null
}

export const login = createAsyncThunk("login", async (data: User) => {
	const response = await api.post("/api/user/token/", data)	
	const resData = response.data
	localStorage.setItem("userInfo", JSON.stringify(resData))
	return resData
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
	error: null,
}


const authSlice = createSlice({
	name: "auth",
	initialState,
	reducers: {},
	extraReducers: (builder) => {
		builder.addCase(login.pending, (state) => {
			state.status = "loading"	
			state.error = null
		}).addCase(
			login.fulfilled,
			(state, action: PayloadAction<UserBasicInfo>) => {
				state.status = "idle"
				state.basicUserInfo = action.payload
			}
		).addCase(login.rejected, (state, action) => {
			state.status = "failed"	
			state.error = action.error.message || "Login Failed"
		}).addCase(getUser.pending, (state) => {
	        state.status = "loading"
	        state.error = null;
	    }).addCase(getUser.fulfilled, (state, action) => {
	        state.status = "idle"
	        state.userProfileData = action.payload;
	    }).addCase(getUser.rejected, (state, action) => {
	        state.status = "failed"
	        state.error = action.error.message || "Get user profile data failed";
        })
	}
})

export const authReducer = authSlice.reducer
