import React, { useState } from "react"
import { styles, buttonTheme } from "../assets/styles"
import api from "../config/api" 
import axios from "axios"

export const Login = () => {
	const [form, setForm] = useState({email: "", password: ""})
	const defaultButton = `${styles.button} ${buttonTheme("blue")}`
	const onSubmit = () => {
		api.post("/api/user/token/", form).then((res) => {
			console.log(res)
		})
	}
	return (
		<div className = "flex h-screen justify-center items-center">
			<div className = "w-96 border p-4 mb-32">
				<div><h1 className = "text-2xl">Login</h1></div>
				<div className="md:flex flex-col mt-2 mb-2">
				    <label className={`${styles.label}`}>
				    	Email: 
				    </label>
					<input 
					className={styles.textInput}
				    onChange={(e) => setForm({...form, email: e.target.value})}
					value={form.email}
					/>
			    </div>
			    <div className="md:flex flex-col mt-2 mb-2">
				    <label className={`${styles.label}`}>
				    	Password:
				    </label>
					<input 
					className={styles.textInput}
				    onChange={(e) => setForm({...form, password: e.target.value})}
					value={form.password}
					/>
			    </div>
				<button onClick = {onSubmit} className = {defaultButton}>Submit</button>
			</div>
		</div>
	)	
}