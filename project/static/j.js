document.getElementById("translateForm").addEventListener("submit", function(event) {
    event.preventDefault();

    // Get the selected input and output languages
    var inputLang = document.getElementById("input_lang").value;
    var outputLang = document.getElementById("output_lang").value;

    // Send a POST request to the /translate endpoint
    fetch("/translate", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            input_lang: inputLang,
            output_lang: outputLang
        })
    })
    .then(response => response.text())
    .then(data => {
        // Display the translated text
        document.getElementById("result").textContent = data;
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("result").textContent = "An error occurred. Please try again.";
    });
});// JavaScript source code
// JavaScript source code
// JavaScript source code
// JavaScript source code
