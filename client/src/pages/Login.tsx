import React, { useEffect, useState } from "react"
import { styles, buttonTheme, colorVariants } from "../assets/styles"
import { useAppDispatch, useAppSelector } from "../hooks/redux-hooks" 
import { setCredentials } from "../reducers/auth" 
import { useLoginMutation } from "../services/auth" 
import { api } from "../config/api"
import {v4 as uuidv4} from "uuid"
import axios from "axios"
import { useLocation, useNavigate } from "react-router-dom" 
import { useForm, Resolver } from "react-hook-form"
import { parseErrorResponse } from "../helpers/functions"

type FormValues = {
	email: string
	password: string
}

export const Login = () => {
	const dispatch = useAppDispatch()
	const location = useLocation()
	const navigate = useNavigate()
	const [login, { isLoading, error }] = useLoginMutation()
	const { token, errors: responseErrors } = useAppSelector((state) => state.auth)
	const defaultButton = `${styles.button} ${buttonTheme("blue")}`
	const { register, handleSubmit, formState: {errors} } = useForm<FormValues>()
	const registerOptions = {
	    email: { required: "Email is required" },
	    password: { required: "Password is required"},
    }
    useEffect(() => {
    	// 
    	if (token && !responseErrors.length){
    		navigate("/")
    	}	
    }, [navigate, token, responseErrors])

    useEffect(() => {
    	window.history.replaceState(null, location.pathname)
    }, [])

	const onSubmit = async (values: FormValues) => {
		try {
			console.log("within the new onsubmit")
			const data = await login(values).unwrap()
			dispatch(setCredentials(data))
		}
		catch (err) {
			console.log(err)
		}
	}
	return (
		<div className = "flex h-screen justify-center items-center">
			<div className = "w-96 border p-4 mb-32">
				<div><h1 className = "text-2xl">Login</h1></div>
				{/* checking if "status" in error narrows down the type to the CustomError defined in services/auth.ts,
				 rather than SerializedError Type */}
				{error && "status" in error ? (parseErrorResponse(error.data).map((errorMessage) => <p key = {uuidv4()} className = {colorVariants.red}>{errorMessage}</p>)) : null}
				{location.state?.message ? <p>{location.state.message}</p> : null}
				<form onSubmit={handleSubmit(onSubmit)}>
					<div className="md:flex flex-col mt-2 mb-2">
					    <label className={`${styles.label}`}>
					    	Email: 
					    </label>
						<input 
						className={styles.textInput}
						{...register("email", registerOptions.email)}
						/>
				        {errors?.email && <small className = {colorVariants.red}>{errors.email.message}</small>}
				    </div>
				    <div className="md:flex flex-col mt-2 mb-2">
					    <label className={`${styles.label}`}>
					    	Password:
					    </label>
						<input 
						type="password"
						className={styles.textInput}
						{...register("password", registerOptions.password)}
						/>
				        {errors?.password && <small className = {colorVariants.red}>{errors.password.message}</small>}
				    </div>
				    <div className = "mt-4 mb-4">
						<button type = "submit" className = {defaultButton}>Submit</button>
					</div>
					<div className = "mt-2 mb-2">
						<small>Don't have an account? Click <button onClick={() => navigate("/register")}>Here</button> to Register</small>
					</div>
				</form>
			</div>
		</div>
	)	
}