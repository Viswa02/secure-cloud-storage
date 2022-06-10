const uploadForm = document.querySelector('#upload-form')
const fileInput = document.querySelector('input[name="uploadfile"]')

const filesDiv = document.querySelector('#files')

const hostname = getCookie('hostname')
const uploadEndpoint = 'api/files/'
const detailLink = 'files/'

let token = getCookie('token')

if (token === null)
    redirectUrl('login/')

function createFileElement(file) {
    console.log('createFileElement is called')
    let fileEle = document.createElement('div')
    fileEle.classList.add(['card'])
    // let fileLink = document.createElement('a')
    // fileLink.setAttribute('href', `${hostname}${detailLink}${file.blob_name}`)
    // fileLink.innerText = file.blob_name
    // <p class="card-text">Integrity : ${file.integrity_score.toFixed(2)}%</p>
    fileEle.innerHTML = `
        <div class="card-body">
            <h5 class="card-title">${file.name} - ${moment(file.created_at).format('MMMM Do YYYY, h:mm:ss a')}</h5>
            <p class="card-text">Blob Name : ${file.blob_name}</p>
            <a href="${hostname}${detailLink}${file.blob_name}" class="btn btn-primary">Details</a>
        </div>
    `
    return fileEle
}

// console.log(moment().format('MMMM Do YYYY, h:mm:ss a'))

function renderFiles(files) {
    console.log(files)
    filesDiv.innerHTML = ""
    for (let file of files) {
        filesDiv.append(createFileElement(file))
    }
}

function getFilesDetails() {
    let token = getCookie('token')

    console.log('token ', token)
    if (token === null)
        redirectUrl('login/')

    var myHeaders = new Headers();
    myHeaders.append("Authorization", `Token ${token}`);
    // myHeaders.append("Cookie", "csrftoken=MWwmpqrXX4mdrEvgcEke6v7esJlkqKRZbiDxcTvZAPB8HY01obzfG1Pj4mXp3vjI");

    var requestOptions = {
        method: 'GET',
        headers: myHeaders,
        // body: formdata,
        redirect: 'follow'
    };

    fetch(hostname + uploadEndpoint, requestOptions)
        .then(response => response.json())
        .then(result => renderFiles(result))
        .catch(error => console.log('error', error));
}

console.log('getFilesDetails about to be called')
getFilesDetails()

uploadForm.onsubmit = function () {
    let token = getCookie('token')

    if (token === null)
        redirectUrl('login/')
    console.log(token)

    var myHeaders = new Headers();
    myHeaders.append("Authorization", `Token ${token}`);
    // myHeaders.append("Cookie", "csrftoken=MWwmpqrXX4mdrEvgcEke6v7esJlkqKRZbiDxcTvZAPB8HY01obzfG1Pj4mXp3vjI");

    var formdata = new FormData();
    console.log(fileInput.files[0])
    const file = fileInput.files[0]
    formdata.append("uploadfile", file, file.name);

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: formdata,
        redirect: 'follow'
    };

    fetch(hostname + uploadEndpoint, requestOptions)
        .then(response => response.json())
        .then(result => getFilesDetails())
        .catch(error => console.log('error', error));

    return false;
}