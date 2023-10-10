import { regexValidation, setBorderRed,showErrorMessage,setBorderIfValid,removeErrorMessage} from "./utility.js"
$(function(){
    var name = ''
    $('#jname').val(name)
    var validName = false
    $('#jname').on('input',function(){
        var nameRegex = /^[A-Za-z\s]+$/
        name = $(this).val()
        // console.log(name)

        if(name === ''){
            setBorderRed('jname');
            showErrorMessage('nameError',"Name is required.")
        }else if(name.length <3){
              setBorderRed('jname')
              showErrorMessage('nameError',"Too short name.")
        }else if(!regexValidation(nameRegex,name)){
                validName = false
                setBorderRed('jname')
                showErrorMessage('nameError',"Invalid name")
        }else{
            validName = true
            removeErrorMessage('nameError')
            setBorderIfValid('jname')
            validateState();
          }
    })
// jname jphone jemail jpassword

    var number = ''
    $('#jphone').val(number)
    var validNumber = false
    $('#jphone').on('input',function(){
        var numberRegex =  /^\d{10}$/
        number = $(this).val()
        console.log(number);
        if(number == ''){
            setBorderRed('jphone')
            showErrorMessage('phoneError',"Number is required.")
            validNumber = false
        }else if(number.length < 10){
            setBorderRed('jphone')
            showErrorMessage('phoneError',"Number must be of 10 digits.")
            validNumber = false
        }else if(!regexValidation(numberRegex, number)){
            setBorderRed('jphone')
            showErrorMessage('phoneError',"Invalid Number")
        }else{
            validNumber = true
            setBorderIfValid('jphone')
            removeErrorMessage('phoneError')
            validateState();
        }
    })


    var email = ''
    $('#jemail').val(email)
    var validEmail = false
    $('#jemail').on('input',function(){
        var emailRegex = /^[a-zA-Z0-9._%+-]+@gmail\.com$/;
        email = $(this).val()
        console.log(email);
        if(email == ''){
            setBorderRed('jemail')
            showErrorMessage('emailError',"Email is required.")
        }else if(!regexValidation(emailRegex,email)){
            validEmail = false
            setBorderRed('jemail')
            showErrorMessage('emailError',"Invalid email. (Provide gmail only)")
        }else{
            validEmail = true
            setBorderIfValid('jemail')
            removeErrorMessage('emailError')
            validateState();
        }
    })


    var password = ''
    $('#jpassword').val(password)
    var validPassword = false
    $('#jpassword').on('input',function () {
        var passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()-_=+[\]{}|;:'",.<>?`~]).{5,}$/
        password = $(this).val()
        console.log(password);
        if(password == '' || !regexValidation(passwordRegex,password)){
            setBorderRed('jpassword')
            showErrorMessage('passwordError',"Please choose a strong password")
            validPassword = false;
        }else{
            validPassword = true
            setBorderIfValid('jpassword')
            removeErrorMessage('passwordError')
            validateState();
        }
    })

    function validateState(){
       
        if(validName && validNumber && validEmail && validPassword){
            // alert("Invoked.")
            $('#register_jobseeker').prop('disabled',false)
        }else{
             // alert("Disabled.")
            $('#register_jobseeker').prop('disabled',true)
        }
    }
})