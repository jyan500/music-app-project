import React from 'react';
import './App.css';
import { Login } from "./pages/Login"
import { Register } from "./pages/Register" 
import { Home } from  "./pages/Home"
import { Routes, Route } from "react-router-dom";
import DefaultLayout from "./layouts/DefaultLayout" 
import ProtectedLayout from "./layouts/ProtectedLayout"

function App() {
  return (
    <div className="">
	    <Routes>
	    	<Route element={<DefaultLayout/>}>
			    <Route path="/login" element={<Login/>} />
			    <Route path="/register" element={<Register/>}/>
		   {/* <Route path="/login" element={<LoginPage />} />*/}
		   </Route>
		   <Route element = {<ProtectedLayout/>}>
			   	<Route path = "/" element = {<Home/>}/>
		   </Route>
	    </Routes>
    </div>
  );
}

export default App;
