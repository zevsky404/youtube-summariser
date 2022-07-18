summariseButton = document.getElementById('summarise-button');
summariseButton.addEventListener('click', function (message){
    function outputSummary() {
        this.message = '';
    }
    chrome.runtime.sendMessage(message, outputSummary);
})