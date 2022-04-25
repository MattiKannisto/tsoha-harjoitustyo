function checkRegisterForm(){
    var nameInputValue = document.getElementById("nameInput").value
    var passwordInputValue = document.getElementById("passwordInput").value
    var reTypedPasswordInputValue = document.getElementById("reTypedPasswordInput").value
    var inputValues = [nameInputValue, passwordInputValue, reTypedPasswordInputValue]

    generateNameErrors(nameInputValue, "nameInputError")
    generatePasswordErrors(passwordInputValue)
    generateReTypedPasswordErrors(reTypedPasswordInput)

    var nameInputError = document.getElementById("nameInputError").innerText
    var passwordInputError = document.getElementById("passwordInputError").innerText
    var reTypedPasswordInputError = document.getElementById("reTypedPasswordInputError").innerText
    var inputErrors = [nameInputError, passwordInputError, reTypedPasswordInputError]
 
    const lengthEqualsToZero = (parameter) => {return parameter.length === 0}
    const lengthCreaterThanZero = (parameter) => {return parameter.length > 0}

    if (arrayElementsMeetCondition(inputValues, lengthEqualsToZero) && arrayElementsMeetCondition(inputErrors, lengthCreaterThanZero)){
        document.getElementById("registerSubmitButton").disabled = false
    } else {
        document.getElementById("registerSubmitButton").disabled = true
    }
}

function generateNameErrors(name, errorFieldId){
    if (name.length > 0 && name.length < 3){
        document.getElementById(errorFieldId).innerText = "Name needs to be at least 3 characters long!"
    } else if (name.length >= 20){
        document.getElementById(errorFieldId).innerText = "Name can be 20 characters long at the maximum!"
    } else {
        document.getElementById(errorFieldId).innerText = ""
    }
}

function generatePasswordErrors(password){
    if (password.length > 0 && password.length < 8){
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
    if (reTypedPassword.length > 0 && password != reTypedPassword){
        document.getElementById("reTypedPasswordInputError").innerText = "Passwords do not match!"
    } else {
        document.getElementById("reTypedPasswordInputError").innerText = ""
    }
}

function arrayElementsMeetCondition(array, conditionFunction){
    if (array.length === 0){
        return true
    } else if (conditionFunction(array.shift())){
        return false
    } else {
        return arrayElementsMeetCondition(array, conditionFunction)
    }
}

function checkProjectCreationForm(){
    var projectNameInputValue = document.getElementById("projectCreationNameInput").value
    
    const lengthEqualsToZero = (parameter) => {return parameter.length === 0}
    const lengthCreaterThanZero = (parameter) => {return parameter.length > 0}

    generateNameErrors(projectNameInputValue, "projectNameInputError")

    var projectNameInputError = document.getElementById("projectNameInputError").innerText

    if (arrayElementsMeetCondition([projectNameInputValue], lengthEqualsToZero) && arrayElementsMeetCondition([projectNameInputError], lengthCreaterThanZero)){
        document.getElementById("projectCreationSubmitButton").disabled = false
    } else {
        document.getElementById("projectCreationSubmitButton").disabled = true
    }
}

function checkLoginForm(){
    var nameInputValue = document.getElementById("loginNameInput").value
    var passwordInputValue = document.getElementById("loginPasswordInput").value
    inputValues = [nameInputValue, passwordInputValue]

    const lengthEqualsToZero = (parameter) => {return parameter.length === 0}

    if (arrayElementsMeetCondition(inputValues, lengthEqualsToZero)){
        document.getElementById("loginSubmitButton").disabled = false
    } else {
        document.getElementById("loginSubmitButton").disabled = true
    }
}