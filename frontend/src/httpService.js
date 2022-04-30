import axios from "axios";
import config from "./config/config";


export default axios.create({
    baseURL: config.azureBaseUrl,
    headers: {
        'Content-Type': 'application/json'
    }
});

