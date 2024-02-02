import React, {useEffect} from "react"
import { useAppDispatch, useAppSelector } from "../hooks/redux-hooks" 
import { logout } from "../reducers/auth" 

export const Home = () => {
	const dispatch = useAppDispatch()
	const { basicUserInfo } = useAppSelector((state) => state.auth)
	const onLogout = () => {
		dispatch(logout())
	}
	return (
		<div>
			<h1>Home</h1>
			<button onClick={onLogout}>Logout</button>
		</div>
	)
}