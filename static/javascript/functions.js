function checkRegisterForm(nameInputFieldId, nameInputErrorFieldId, passwordInputFieldId, passwordInputErrorFieldId,
                           reTypedPasswordInputFieldId, reTypedPasswordInputErrorFieldId, submitButtonId,
                           nameMinLength, nameMaxLength, passwordMinLength, passwordMaxLength){

    generateInputFieldErrors(nameInputFieldId, nameInputErrorFieldId, nameMinLength, nameMaxLength)
    generateInputFieldErrors(passwordInputFieldId, passwordInputErrorFieldId, passwordMinLength, passwordMaxLength)
    generateReTypedPasswordErrors(passwordInputFieldId, reTypedPasswordInputFieldId, reTypedPasswordInputErrorFieldId)

    allContainText = noFieldEmpty([nameInputFieldId, passwordInputFieldId, reTypedPasswordInputFieldId])
    noErrors = noErrorMessages([nameInputErrorFieldId, passwordInputErrorFieldId, reTypedPasswordInputErrorFieldId])

    disableSubmitButtonConditionsNotMet([allContainText, noErrors], submitButtonId)
}

function generateInputFieldErrors(inputFieldId, errorFieldId, minLength, maxLength){
    input = document.getElementById(inputFieldId).value
        
    if (input.length > 0 && input.length < minLength){
        document.getElementById(errorFieldId).innerText = "Needs to be at least " + minLength.toString() + " characters long!"
    } else if (input.length >= maxLength){
        document.getElementById(errorFieldId).innerText = "Can be " + maxLength.toString() + " characters long at the maximum!"
    } else {
        document.getElementById(errorFieldId).innerText = ""
    }
}

function generateReTypedPasswordErrors(passwordInputFieldId, reTypedPasswordInputFieldId, reTypedPasswordInputErrorFieldId){
    var password = document.getElementById(passwordInputFieldId).value
    var reTypedPassword = document.getElementById(reTypedPasswordInputFieldId).value    

    if (reTypedPassword.length > 0 && password != reTypedPassword){
        document.getElementById(reTypedPasswordInputErrorFieldId).innerText = "Passwords do not match!"
    } else {
        document.getElementById(reTypedPasswordInputErrorFieldId).innerText = ""
    }
}

function arrayElementsMeetCondition(array, conditionFunction){
    if (array.length <= 0){
        return true
    } else if (conditionFunction(array.shift())){
        return false
    } else {
        return arrayElementsMeetCondition(array, conditionFunction)
    }
}

function checkProjectCreationForm(nameInputFieldId, nameInputErrorFieldId, submitButtonId, nameMinLength, nameMaxLength){
    generateInputFieldErrors(nameInputFieldId, nameInputErrorFieldId, nameMinLength, nameMaxLength)

    allContainText = noFieldEmpty([nameInputFieldId])
    noErrors = noErrorMessages([nameInputErrorFieldId])

    disableSubmitButtonConditionsNotMet([allContainText, noErrors], submitButtonId)
}

function checkLoginForm(nameInputFieldId, passwordInputFieldId, submitButtonId){
    allContainText = noFieldEmpty([nameInputFieldId, passwordInputFieldId])

    disableSubmitButtonConditionsNotMet([allContainText], submitButtonId)
}

function noErrorMessages(textInputFieldIds){
    const fieldNotEmpty = (fieldId) => {return document.getElementById(fieldId).innerHTML.length > 0}

    return arrayElementsMeetCondition(textInputFieldIds, fieldNotEmpty)
}

function noFieldEmpty(textInputFieldIds){   
    const fieldEmpty = (fieldId) => {return document.getElementById(fieldId).value.length === 0}

    return arrayElementsMeetCondition(textInputFieldIds, fieldEmpty)
}

function disableSubmitButtonConditionsNotMet(conditions, submitButtonId){   
    if (conditions.length <= 0){
        document.getElementById(submitButtonId).disabled = false
    } else if (conditions.shift() === true){
        return disableSubmitButtonConditionsNotMet(conditions, submitButtonId)
    } else {
        document.getElementById(submitButtonId).disabled = true
    }
}

function removeTextIfJavascriptEnabled(fieldId){
    document.getElementById(fieldId).innerText = ""
}
