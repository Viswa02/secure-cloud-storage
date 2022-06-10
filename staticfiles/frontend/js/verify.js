const verifyBtn = document.querySelector('#verify-btn')

const hostname = getCookie('hostname')
const verifyEndpoint = 'api/verify/'

let token = getCookie('token')

if (token === null)
    redirectUrl('login/')

verifyBtn.addEventListener('click', function () {
    let token = getCookie('token')
    if (token === null)
        redirectUrl('login/')

    let headers = new Headers()
    headers.set('Authorization', `Token ${token}`)

    let formdata = new FormData()

    let requestOptions = {
        method: 'POST',
        headers: headers,
        body: formdata,
        redirect: 'follow'
    };

    fetch(hostname + verifyEndpoint, requestOptions)
        .then(response => response.json())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));
})