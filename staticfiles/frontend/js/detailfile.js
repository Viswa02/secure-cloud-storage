const fileDetailDiv = document.querySelector('#file-detail')

const hostname = getCookie('hostname')
const detailEndpoint = 'api/files/'
const verifyEndpoint = 'api/verify/'

let token = getCookie('token')

if (token === null)
    redirectUrl('login/')

function renderFile(file) {
    let createdAtFormated = moment(file.created_at).format('MM/DD/YYYY HH:MM')
    let successBadge = `<span class="badge text-bg-success">${file.integrity_score}</span>`
    let dangerBadge = `<span class="badge text-bg-danger">${file.integrity_score}</span>`
    let statusBadge
    if (file.integrity)
        statusBadge = successBadge
    else
        statusBadge = dangerBadge

    console.log(file.sas_url)
    fileDetailDiv.innerHTML = `
        <div class="card">
            <div class="card-header">
                ${file.name}
            </div>
            <div class="card-body">
                <h5 class="card-title">${file.blob_name} - <span  style="color: #888888;">${createdAtFormated}</span></h5>
                <p class="card-text">Verified at : ${moment(file.verified_at).fromNow()}</p>
                <p class="card-text">Integrity score : ${statusBadge}</p>
                <button id="verify-btn" class="btn btn-primary">Verify</button>
                <a target="_blank" href="${file.sas_url}"><button id="download-btn" class="btn btn-primary">Download</button></a>
            </div>
        </div>
    `

    let verifyButton = document.querySelector('#verify-btn')
    verifyButton.addEventListener('click', function () {
        verifyFile(file.blob_name)
    })
}

function verifyFile(blobName) {
    let token = getCookie('token')
    if (token === null)
        redirectUrl('login/')

    var myHeaders = new Headers();
    myHeaders.append("Authorization", `Token ${token}`);

    let formdata = new FormData()

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: formdata,
        redirect: 'follow'
    };

    const requestUrl = `${hostname}${verifyEndpoint}${blobName}/`
    fetch(requestUrl, requestOptions)
        .then(response => response.json())
        .then(file => renderFile(file))
        .catch(error => console.log('error', error));
}

function getFile(blobName) {
    let token = getCookie('token')

    if (token === null)
        redirectUrl('login/')

    var myHeaders = new Headers();
    myHeaders.append("Authorization", `Token ${token}`);

    var requestOptions = {
        method: 'GET',
        headers: myHeaders,
        redirect: 'follow'
    };

    const requestUrl = `${hostname}${detailEndpoint}${blobName}`
    fetch(requestUrl, requestOptions)
        .then(response => response.json())
        .then(file => renderFile(file))
        .catch(error => console.log('error', error));
}

const blobName = fileDetailDiv.dataset.blobName
getFile(blobName)