let urlResult = document.getElementById('result')
let urlInput = document.getElementById('url')
let urlSubmit = document.getElementById('url-submit')

function validateUrl(e) {
    console.log(e.target.value)
    console.log(urlResult.innerText)
    urlSubmit.disabled = !e.target.value || !parseInt(urlResult.innerText)
}

urlInput.addEventListener('change', validateUrl);