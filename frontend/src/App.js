// import logo from './logo.svg';
import './App.css';
import TestComponent from "./test-component";
import "bootstrap/dist/css/bootstrap.min.css";
import {Link, Routes, Route } from "react-router-dom";
import {useState, useEffect} from "react";
import UserLoginComponent from "./components/user_login_component";
import MainPageComponent from "./components/main_page_component";
import User_register_component from "./components/user_register_component";


function App() {
    const [vari, setVari] = useState(false);
    const [token, setToken] = useState(localStorage.getItem("token"));

useEffect(() => {
    console.log("Main page loaded");
    console.log(localStorage.getItem("token"));
})
  return (
    <div className="App">
      <div>
          <h1>CL2228 GOD</h1>
      </div>
        {token? (
            <div>{token}</div>
        ): (
            <div>No token</div>
        )}
        <nav className="navbar navbar-expand navbar-light bg-light justify-content-center">
            <div className="navbar-nav mr-auto">
                <ul className="navbar-nav">
                    <a className="navbar-brand" href="/">
                        Home
                    </a>

                    {!vari && (
                        <li className="nav-item">
                            <Link to="/login" className="nav-link">Login</Link>
                        </li>
                    )}

                    <li className="nav-item">
                        <Link to="/c1" className="nav-link">C1</Link>
                    </li>

                    <li className="c2">
                        <Link to="/c2" className="nav-link">C2</Link>
                    </li>

                    <li className="c2">
                        <Link to="/test" className="nav-link">Test</Link>
                    </li>
                </ul>
            </div>
        </nav>

        <div className="main">
            <Routes>
                <Route exact path="/" element={<MainPageComponent/>}/>
                <Route path="/c1" element={<TestComponent/>}/>
                <Route path="/c2" element={<TestComponent/>}/>
                <Route path={"/register"} element={<User_register_component/>}/>
                <Route path="/login" element={<UserLoginComponent/>}/>
                <Route path={"/test"} element={<TestComponent/>}/>
            </Routes>
        </div>
    </div>
  );
}

export default App;
