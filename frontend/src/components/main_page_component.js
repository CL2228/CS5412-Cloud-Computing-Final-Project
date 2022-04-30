import React, {useState, useEffect} from "react";
import UserServices from "../services/user_services";
import {InputGroup, Form, FormControl} from "react-bootstrap";


function MainPageComponent(props) {
    const [token, setToken] = useState(localStorage.getItem("token"));


    return (
        <div>
            {token? (
                <div>{token}</div>
            ) : (
                <div>{"Not logged in."}</div>
            )}
            <h1>Main Page</h1>
        </div>
    )
}

export default MainPageComponent;