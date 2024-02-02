import React from "react"
import { Link, Outlet, Navigate } from "react-router-dom"
import { useAppDispatch, useAppSelector } from "../hooks/redux-hooks" 

const DefaultLayout = () => {
	const basicUserInfo = useAppSelector((state) => state.auth.basicUserInfo)

	if (basicUserInfo){
		return <Navigate replace to = {"/"} />
	}

	return (
		<>
			<Outlet/>
		</>
	)
}

export default DefaultLayout
