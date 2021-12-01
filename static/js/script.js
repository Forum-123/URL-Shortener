urlResult = document.getElementById('result')
urlInput = document.getElementById('url')
urlSubmit = document.getElementById('url-submit')


urlInput.addEventListener('change', (e) => {
    validateUrl(e)
});


function validateUrl(e) {
    console.log(e.target.value)
    console.log(urlInput.innerText)
    urlSubmit.disabled = !e.target.value || !parseInt(urlInput.innerText)
}