export function setBorderRed(id){
    const element = document.getElementById(id);
    element.classList.add('invalid');
    element.classList.remove('valid');
}

export function showErrorMessage(id,message){
    const element = document.getElementById(id);
    element.innerText = message;
    element.classList.add('d-block');
    element.classList.remove('d-none');
}

export function setBorderIfValid(id){
    const element = document.getElementById(id);
    element.classList.remove('invalid');
    element.classList.add('valid');
}

export function removeErrorMessage(id){
    const element = document.getElementById(id);
    element.innerText = '';
    element.classList.add('d-none');
    element.classList.remove('d-block');
}
export function regexValidation(regex,value){
    return regex.test(value)
}