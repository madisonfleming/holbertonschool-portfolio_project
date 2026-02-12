import axios from 'axios';

// create an instance of axios with the base url
const api = axios.create({
    baseURL: "http://127.0.0.1:8000"
});

//export the axios instance
export default api;
