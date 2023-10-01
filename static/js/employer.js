import { regexValidation, setBorderRed,showErrorMessage,setBorderIfValid,removeErrorMessage} from "./utility.js"
$(function(){
    // $('#register_employer').prop('disabled',true)
    
    var name = ''
    $('#employer_name').val(name)
    var validName = false
    $('#employer_name').on('input',function(){
        const regex = /^[A-Za-z\s]+$/
        name = $(this).val()
        if(name === ''){
            setBorderRed('employer_name');
            showErrorMessage('nameError',"Name is required.")
        }else if(name.length <3){
              setBorderRed('employer_name')
              showErrorMessage('nameError',"Too short name.")
        }else if(!regexValidation(regex,name)){
                validName = false
                setBorderRed('employer_name')
                showErrorMessage('nameError',"Invalid name")
        }else{
            validName = true
            removeErrorMessage('nameError')
            setBorderIfValid('employer_name')
            validateState();
          }
    })

    var number = ''
    $('#employer_number').val(number)
    var validNumber = false
    $('#employer_number').on('input',function(){
        var numberRegex = /^\d{10}$/
        number = $(this).val()
        if(number == ''){
            setBorderRed('employer_number')
            showErrorMessage('phoneError',"Number is required.")
            validNumber = false
        }else if(number.length < 10){
            setBorderRed('employer_number')
            showErrorMessage('phoneError',"Number must be of 10 digits.")
            validNumber = false
        }else if(!regexValidation(numberRegex, number)){
            setBorderRed('employer_number')
            showErrorMessage('phoneError',"Invalid Number")
        }else{
            validNumber = true
            setBorderIfValid('employer_number')
            removeErrorMessage('phoneError')
            validateState();
        }
    })

    var email = ''
    var validEmail = false
    $('#employer_email').val(email)
    $('#employer_email').on('input',function(){
        const emailRegex = /^[a-zA-Z0-9._%+-]+@gmail\.com$/
        email = $(this).val()
        if(email == ''){
            setBorderRed('employer_email')
            showErrorMessage('emailError',"Email is required.")
        }else if(!regexValidation(emailRegex,email)){
            validEmail = false
            setBorderRed('employer_email')
            showErrorMessage('emailError',"Invalid email. (Provide gmail only)")
        }else{
            validEmail = true
            setBorderIfValid('employer_email')
            removeErrorMessage('emailError')
            validateState();
        }
    })

    var password = ''
    var validPassword= false
    $('#employer_password').val(password)
    $('#employer_password').on('input',function(){
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()-_=+[\]{}|;:'",.<>?`~]).{5,}$/
        password = $(this).val()
        if(password == '' || !regexValidation(passwordRegex,password)){
            setBorderRed('employer_password')
            showErrorMessage('passwordError',"Please choose a strong password")
            validPassword = false;
        }else{
            validPassword = true
            setBorderIfValid('employer_password')
            removeErrorMessage('passwordError')
            validateState();
        }
    })

    
    function validateState(){
       
        if(validName && validNumber && validEmail && validPassword){
            // alert("Invoked.")
            $('#register_employer').prop('disabled',false)
        }else{
             // alert("Disabled.")
            $('#register_employer').prop('disabled',true)
        }
    }


})
