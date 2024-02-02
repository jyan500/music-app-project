import React, { useEffect, useState } from "react"
import { styles, buttonTheme, colorVariants } from "../assets/styles"
import { useAppDispatch, useAppSelector } from "../hooks/redux-hooks" 
import { login } from "../reducers/auth" 
import { api } from "../config/api"
import axios from "axios"
import { useNavigate } from "react-router-dom" 
import { useForm, Resolver } from "react-hook-form"
import { FaEye } from "react-icons/fa"

type FormValues = {
	firstName: string
	lastName: string
	email: string
	password: string
	confirmPassword: string
}

export const Register = () => {
	const dispatch = useAppDispatch()
	const navigate = useNavigate()
	const { basicUserInfo, errors: responseErrors } = useAppSelector((state) => state.auth)
	const defaultButton = `${styles.button} ${buttonTheme("blue")}`
	const { register, handleSubmit, formState: {errors} } = useForm<FormValues>()
	const [showPassword, setShowPassword] = useState(false)
	const registerOptions = {
		firstName: { required: "First Name is required"},
		lastName: { required: "Last Name is required"},
	    email: { required: "Email is required" },
	    password: { required: "Password is required"},
	    confirmPassword: { required: "Confirm Password is required"}
    }
    useEffect(() => {
    	// 
    }, [navigate, basicUserInfo, responseErrors])

	const onSubmit = (values: FormValues) => {
		// dispatch(login(values))
	}
	return (
		<div className = "flex h-screen justify-center items-center">
			<div className = "w-96 border p-4 mb-32">
				<div><h1 className = "text-2xl">Register</h1></div>
				{responseErrors.length ? (responseErrors.map((errorMessage) => <p className = {colorVariants.red}>{errorMessage}</p>)) : null}
				<form onSubmit={handleSubmit(onSubmit)}>
					<div className="md:flex flex-col mt-2 mb-2">
					    <label className={`${styles.label}`}>
					    	First Name: 
					    </label>
						<input 
						className={styles.textInput}
						{...register("email", registerOptions.email)}
						/>
				        {errors?.firstName && <small className = {colorVariants.red}>{errors.firstName.message}</small>}
				    </div>
				    <div className="md:flex flex-col mt-2 mb-2">
					    <label className={`${styles.label}`}>
					    	Last Name:
					    </label>
						<input 
						type="password"
						className={styles.textInput}
						{...register("password", registerOptions.password)}
						/>
				        {errors?.lastName && <small className = {colorVariants.red}>{errors.lastName.message}</small>}
				    </div>
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
				    <div className="md:flex flex-col mt-2 mb-2">
					    <label className={`${styles.label}`}>
					    	Confirm Password:
					    </label>
					    <div className = "relative">
							<input 
							type={!showPassword ? "password" : "text"}
							className={styles.textInput}
							{...register("password", registerOptions.password)}
							/>
							<FaEye onClick={() => setShowPassword(!showPassword)} className="absolute top-0 right-0 w-6 h-6 mt-2 mr-2 hover:opacity-60"/>
						</div>
				        {errors?.confirmPassword && <small className = {colorVariants.red}>{errors.confirmPassword.message}</small>}
				    </div>
				    <div className = "mt-4 mb-4">
						<button type = "submit" className = {defaultButton}>Submit</button>
					</div>
					<div className = "mt-2 mb-2">
						<small>Already have an account? Click <button onClick = {() => navigate("/login")}>here</button> to login</small>
					</div>
				</form>
			</div>
		</div>
	)	
}