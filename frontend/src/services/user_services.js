import http from "../httpService";
import Config from "../config/config";

class UserServices {

    /**
     * login function
     * @param username username
     * @param password password
     * @returns {Promise<AxiosResponse<any>>} A Http Request promise, need to use await or then to parse.
     */
    login(username, password) {

        let req_body = {
            "email": username,
            "password": password
        }
        return http.post(Config.userLoginUrl, JSON.stringify(req_body));
    }

    /**
     * logout function, delete token on the browser
     */
    logout() {
        localStorage.removeItem("token");
    }


}


export default new UserServices();