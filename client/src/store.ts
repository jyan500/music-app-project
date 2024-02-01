import { configureStore } from "@reduxjs/toolkit" 
import { authReducer } from "./reducers/auth" 
import { userReducer } from "./reducers/user" 

export const store = configureStore({
	reducer: {
		auth: authReducer,
		user: userReducer
	}
})

// rely on type inference for RootState and AppDispatch
export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch

export default store