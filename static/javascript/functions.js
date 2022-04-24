function checkRegisterForm(){
    generateNameErrors()
    generatePasswordErrors()
    generateReTypedPasswordErrors()
    ifNoErrorsActivateSubmitButton()
}

function generateNameErrors(){
    var name = document.getElementById("nameInput").value
    if (name.length < 3){
        document.getElementById("nameInputError").innerText = "Name needs to be at least 3 characters long!"
    } else if (name.length >= 20){
        document.getElementById("nameInputError").innerText = "Name can be 20 characters long at the maximum!"
    } else {
        document.getElementById("nameInputError").innerText = ""
    }
}

function generatePasswordErrors(){
    var password = document.getElementById("passwordInput").value
    if (password.length < 8){
        document.getElementById("passwordInputError").innerText = "Password needs to be at least 8 characters long!"
    } else if (password.length >= 30){
        document.getElementById("passwordInputError").innerText = "Password can be 30 characters long at the maximum!"
    } else {
        document.getElementById("passwordInputError").innerText = ""
    }
}

function generateReTypedPasswordErrors(){
    var password = document.getElementById("passwordInput").value
    var reTypedPassword = document.getElementById("reTypedPasswordInput").value
    if (password != reTypedPassword){
        document.getElementById("reTypedPasswordInputError").innerText = "Passwords do not match!"
    } else {
        document.getElementById("reTypedPasswordInputError").innerText = ""
    }
}

function ifNoErrorsActivateSubmitButton(){
    var nameInputError = document.getElementById("nameInputError").innerText
    var passwordInputError = document.getElementById("passwordInputError").innerText
    var reTypedPasswordInputError = document.getElementById("reTypedPasswordInputError").innerText
    if (nameInputError.length > 0 || passwordInputError.length > 0 || reTypedPasswordInputError.length > 0) {
        document.getElementById("registerSubmitButton").disabled = true
    } else {
        document.getElementById("registerSubmitButton").disabled = false
    }
}