let usernameEle = document.querySelector('#username')
let passwordEle = document.querySelector('#password')
const loginForm = document.querySelector('#login-form')

hostname = getCookie('hostname')
loginEndpoint = 'api/api-token-auth/'

function loginHelper(result) {
    setCookie('token', result.token)
    console.log(result)
    redirectUrl('files/')
}

loginForm.onsubmit = function () {
    let username = usernameEle.value
    let password = passwordEle.value

    console.log(username, password)

    var myHeaders = new Headers();

    var formdata = new FormData();
    formdata.append("username", username)
    formdata.append("password", password)


    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: formdata,
        redirect: 'follow'
    };

    const url = hostname + loginEndpoint
    console.log(url)

    fetch(hostname + loginEndpoint, requestOptions)
        .then(response => response.json())
        .then(result => loginHelper(result))
        .catch(error => console.log('error', error));
    return false
}