import { configureStore } from "@reduxjs/toolkit" 
import { authReducer } from "./reducers/auth" 
import { userReducer } from "./reducers/user" 
import { api } from "./services/auth" 

export const store = configureStore({
	reducer: {
		[api.reducerPath]: api.reducer,
		auth: authReducer,
		user: userReducer,
	},
	middleware: (getDefaultMiddleware) => {
		return getDefaultMiddleware().concat(api.middleware)
	}
})

// rely on type inference for RootState and AppDispatch
export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch

export default store