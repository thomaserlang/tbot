import axios from 'axios';

axios.interceptors.response.use(function(response) {
    return response;
}, function (error) {
    if (error.response.status == 401) {
        let next = encodeURIComponent(
            location.pathname + location.search
        )
        location.href = '/twitch/login?next='+next;
        throw 'Not authenticated!';
    }
    return Promise.reject(error);
});

export default axios;