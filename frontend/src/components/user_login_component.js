import React, {useState, useEffect} from "react";
import UserServices from "../services/user_services";
import {InputGroup, Form, FormControl} from "react-bootstrap";
import {errorMonitor} from "form-data";
import { useNavigate } from "react-router-dom";


function UserLoginComponent(props) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [errMsg, setErrMsg] = useState("");
    const [successMsg, setSuccessMsg] = useState("");
    let navigate = useNavigate();

    const routeChange = (url) => {
        navigate(url);
    }

    const sleep = (milliseconds) => {
        return new Promise(resolve => setTimeout(resolve, milliseconds));
    }

    function onClickTest() {
        routeChange("/");
    }

    function submitLoginRequest(e) {
        e.preventDefault();
        UserServices.login(email, password).then(res => {
            console.log("login success");
            localStorage.setItem("token", res.data['access-token']);
            setErrMsg("");
            setSuccessMsg("Login successfully, redirecting in 2s...");
            console.log(localStorage.getItem("token"));
            sleep(2000).then(() => {
                navigate("/");
            });
        }).catch(error => {
            setSuccessMsg("");
            const errResMsg =
                (error.response && error.response.data && error.response.data.message)
                || (error.message || error.toString());
            setErrMsg(errResMsg);
            console.log(error);
        })

    }

    return (
        <div>
            {/*<button onClick={(e) => {*/}
            {/*    onClickTest();*/}
            {/*}}>test</button>*/}
            <form>
                <h5>Log in</h5>
                <InputGroup className="mb-lg-3">
                    <InputGroup.Text>
                        Email
                    </InputGroup.Text>
                    <FormControl
                        placeholder="email@example.com"
                        onChange={(e) => {
                            setEmail(e.target.value);
                        }}
                        value={email}
                    />
                </InputGroup>
                <InputGroup className="mb-lg-3">
                    <InputGroup.Text>
                        Password
                    </InputGroup.Text>
                    <FormControl
                        type="password"
                        placeholder="password"
                        onChange={(e) => {
                            setPassword(e.target.value);
                        }}
                        value={password}
                    />
                </InputGroup>
                <button
                    className="btn btn-outline-primary btn-block"
                    disabled={!email || !password}
                    onClick={(e) => {
                        submitLoginRequest(e);
                    }}
                >
                    <span>Log in</span>
                </button>
            </form>
            {successMsg && (
                <div className="form-group">
                    <div className="alert alert-success" role="alert">
                        {successMsg}
                    </div>
                </div>
            )}
            {errMsg && (
                <div className="form-group">
                    <div className="alert alert-danger" role="alert">
                        {errMsg}
                    </div>
                </div>
            )}
        </div>
    )
}

export default UserLoginComponent;