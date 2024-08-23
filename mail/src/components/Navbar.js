import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from './Home';
import Dashboard from './Dashboard';
import SendMail from './SendMail';
import 'material-icons/iconfont/material-icons.css';
import Login from "./Login";

function Navbar() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userEmail, setUserEmail] = useState('');

    useEffect(() => {
        // Check if there is a user email in localStorage
        const storedEmail = localStorage.getItem('userEmail');
        if (storedEmail) {
            setIsLoggedIn(true);
            setUserEmail(storedEmail);
        } else {
            setIsLoggedIn(false);
        }
    }, []);

    // Handle login
    const handleLogin = (email) => {
        localStorage.setItem('userEmail', email);
        setUserEmail(email);
        setIsLoggedIn(true);
    };

    // Handle logout
    const handleLogout = () => {
        localStorage.removeItem('userEmail');
        setUserEmail('');
        setIsLoggedIn(false);
    };

    return (
        <div className="Navibar">
            <ul>
                <li id="logo">
                    <a href="#home">
                        <img style={{ height: "1.5em" }} src="https://i.ibb.co/vDYXr2S/path1079.png" alt="logo" />
                        Mail Track
                    </a>
                </li>

                <li style={{ float: "right" }}>
                    <a href="/dashboard">
                        <div id="howtouse">Dashboard<i className="material-icons-outlined">arrow_forward_ios</i></div>
                    </a>
                </li>

                <li style={{ float: "right" }}>
                    <a href="/">
                        <div id="login">Home</div>
                    </a>
                </li>

                {isLoggedIn ? (
                    <>
                        <li style={{ float: "right" }}>
                            <a onClick={handleLogout} style={{ cursor: 'pointer' }}>
                                <div id="logout">Logout</div>
                            </a>
                        </li>
                        <li style={{ float: "right" }}>
                            <a>
                                <div>Welcome "{userEmail}" </div>
                            </a>
                        </li>
                    </>
                ) : null /* Do not render Login button if logged in */}
            </ul>

            <BrowserRouter>
                <Routes>
                    <Route exact path="/" element={<Home />} />
                    <Route exact path="/dashboard" element={<Dashboard />} />
                    <Route exact path="/login" element={<Login onLogin={handleLogin} />} />
                    <Route exact path="/send" element={<SendMail />} />
                </Routes>
            </BrowserRouter>
        </div>
    );
}

export default Navbar;
