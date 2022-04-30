import React, {useState} from "react";
import httpService from "./httpService";
import Config from "./config/config";
import axios from "axios";

// const FormData = require("form-data");

function TestComponent (props) {
    const [count, setCount] = useState(props.name);
    const [file, setFile] = useState("");

    function testFunc(e) {
        e.preventDefault();
        let body = {
            "email": "cl2228@cornell.edu",
            "password": "cl2228.0284"
        };
        console.log("fuck");
        const formData = new FormData();
        // formData.getHeaders();
        formData.append("age", "323");
        formData.append("name", "cl2228")
        // formData.append("img", file)
        console.log(formData);

        axios.post("http://127.0.0.1:5000/", formData).then(res => {
            console.log("success")
            console.log(res);
        }).catch(err => {
            console.log("err occurred");
            console.log(err);
            console.log(err.response);
        })
    }
    // console.log(setCount)
    return (
        <div>
            <h1>Hello, {props.name}</h1>
            <input type="text" onChange={(event) => {
                setCount(event.target.value);
            }}/>
            <input type="file" onChange={(event) => {
                console.log(event)
                console.log(event.target.files[0]);
                setFile(event.target.files[0]);
            }}/>
            <button onClick={(event) => {
                console.log(count);
                testFunc(event);
            }}>
                btn
            </button>
        </div>
    );
}

export default TestComponent