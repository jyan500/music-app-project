import React from 'react';
import './App.css';
import { Login } from "./pages/Login"
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <div className="">
	    <Routes>
		    <Route path="/" element={<Login/>} />
		   {/* <Route path="/login" element={<LoginPage />} />*/}
	    </Routes>
    </div>
  );
}

export default App;
