import React, { useState } from "react"
import { styles, buttonTheme, colorVariants } from "../assets/styles"
import { useForm, Resolver } from "react-hook-form"
import { useAppDispatch } from "../hooks/redux-hooks" 
import { login } from "../reducers/auth" 
import axios from "axios"
import { api } from "../config/api"

type FormValues = {
	email: string
	password: string
}

export const Login = () => {
	const dispatch = useAppDispatch()
	const defaultButton = `${styles.button} ${buttonTheme("blue")}`
	const { register, handleSubmit, formState: {errors} } = useForm<FormValues>()
	const registerOptions = {
    email: { required: "Email is required" },
    password: { required: "Password is required"},
  };
	// const handleLogin = () => {
	// 	api.post("/api/user/token/", form).then((res) => {
	// 		console.log(res)
	// 	})
	// }
	const onSubmit = (values: FormValues) => {
		dispatch(login(values))
		// api.post("/api/user/token/", values).then((res) => {
		// 	console.log(res)
		// }).catch((e) => {
		// 	console.log(e)
		// })
	}
	return (
		<div className = "flex h-screen justify-center items-center">
			<div className = "w-96 border p-4 mb-32">
				<div><h1 className = "text-2xl">Login</h1></div>
				<form onSubmit={handleSubmit(onSubmit)}>
					<div className="md:flex flex-col mt-2 mb-2">
					    <label className={`${styles.label}`}>
					    	Email: 
					    </label>
						<input 
						className={styles.textInput}
						{...register("email", registerOptions.email)}
						/>
				        {errors?.email && <small className = {`${colorVariants.red}`}>{errors.email.message}</small>}
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
				        {errors?.password && <small className = {`${colorVariants.red}`}>{errors.password.message}</small>}
				    </div>
					<button type = "submit" className = {defaultButton}>Submit</button>
				</form>
			</div>
		</div>
	)	
}