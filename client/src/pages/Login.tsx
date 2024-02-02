import React, { useEffect, useState } from "react"
import { styles, buttonTheme, colorVariants } from "../assets/styles"
import { useAppDispatch, useAppSelector } from "../hooks/redux-hooks" 
import { login } from "../reducers/auth" 
import { api } from "../config/api"
import axios from "axios"
import { useLocation, useNavigate } from "react-router-dom" 
import { useForm, Resolver } from "react-hook-form"

type FormValues = {
	email: string
	password: string
}

export const Login = () => {
	const dispatch = useAppDispatch()
	const location = useLocation()
	const navigate = useNavigate()
	const { basicUserInfo, errors: responseErrors } = useAppSelector((state) => state.auth)
	const defaultButton = `${styles.button} ${buttonTheme("blue")}`
	const { register, handleSubmit, formState: {errors} } = useForm<FormValues>()
	const registerOptions = {
	    email: { required: "Email is required" },
	    password: { required: "Password is required"},
    }
    useEffect(() => {
    	// 
    	if (basicUserInfo && !responseErrors.length){
    		navigate("/")
    	}	
    }, [navigate, basicUserInfo, responseErrors])

	const onSubmit = (values: FormValues) => {
		dispatch(login(values))
	}
	return (
		<div className = "flex h-screen justify-center items-center">
			<div className = "w-96 border p-4 mb-32">
				<div><h1 className = "text-2xl">Login</h1></div>
				{responseErrors.length ? (responseErrors.map((errorMessage) => <p className = {colorVariants.red}>{errorMessage}</p>)) : null}
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