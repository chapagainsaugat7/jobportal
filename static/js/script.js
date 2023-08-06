$('document').ready(function(){

  if ( window.history.replaceState ) {
      window.history.replaceState( null, null, window.location.href );
    }
  
      $('#register_jobseeker').on('click', function(event){
        const name = $('#jobseeker_name').val();
        const phone_number = $('#phone_number').val();
        const preference = $('#company_type').val();
        const email = $('#email').val();
        const password = $('#password').val();
        const confirm_password = $('#confirm_password').val();
        const csrf = $('input[name=csrfmiddlewaretoken]').val();
        
        event.preventDefault();
        if(validateJobSeekerForm(name,phone_number,email,password,confirm_password)){
          data = {name:name,
            phone:phone_number,
            job_preference:preference,
            email:email,
            password:password,
            csrfmiddlewaretoken:csrf
          };
      
          $.ajax({
            url:"/jobseeker/register-job-seeker/",
            method:"POST",
            data:data,
            success:function(data){
              console.log("data");
            }
          })
        }else{
          // console.log("Check validator once please.")
        }

      })

    $('#register_employer').on('click',function(event){
      event.preventDefault();
      const name = $('#employer_name').val();
      const phone_number = $('#employer_number').val();
      const type_of_hiring = $('#type_of_hiring').val();
      const email = $('#employer_email').val();
      const password = $('#employer_password').val();
      const confirm_password = $('#confirm_password').val();
      const csrf_token = $('input[name=csrfmiddlewaretoken]').val();
     
      if(validateEmployerForm(name,phone_number,email,password,confirm_password)){
        data = {
          name:name,
          number:phone_number,
          email:email,
          type_of_hiring:type_of_hiring,
          password:password,
          csrfmiddlewaretoken:csrf_token
        };

        
        $.ajax({
          url:'/employer/register_employer/',
          method:"POST",
          data:data,
          success:function(data){
            
          },
          error:function(){
            console.log("Error occured.");
          }
        })
      }else{
        // ............
      }

    })
    let nameValid = false;
    let numberValid = false;
    let emailValid = false;
    let passwordValid = false;
    const regexName =  /^[A-Za-z\s]+$/
    const numberRegex = /^\d{10}$/;
    const emailRegex = /^[a-zA-Z0-9._%+-]+@gmail\.com$/;
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()-_=+[\]{}|;:'",.<>?`~]).{5,}$/;
          
    // Set border red if field is invalid while validation.
    const setBorderRedIfInvalid = (id)=>{
      const element = document.getElementById(id);
      element.classList.add('invalid');
      element.classList.remove('valid');
    }

    //set border green if field is valid.
    const setBorderIfValid = (id)=>{
      const element = document.getElementById(id);
      element.classList.remove('invalid');
      element.classList.add('valid');
    }

    //Show error message.
    const showErrorMessage = (id,message)=>{
      const element = document.getElementById(id);
      element.innerText = message;
      element.classList.add('d-block');
      element.classList.remove('d-none');
    }
    // remove error message
    const removeErrorMessage = (id)=>{
      const element = document.getElementById(id);
      element.innerText = '';
      element.classList.add('d-none');
      element.classList.remove('d-block');
    }

    //check if password and confirm password values are matched or not.
    const checkPassword = (password,confirm_password) =>{
      if(password == confirm_password){
        return true;
      }else{
        return false;
      }
    }
    
    
    //Form validation.
    const validateJobSeekerForm = (name,number,email,password,confirm_password)=>{
      /*-----------Validate Name---------------------*/
      if(name == ''){
        setBorderRedIfInvalid('jobseeker_name');
        showErrorMessage('nameError',"Please enter name.")
      }
      else if(name.length<4 || !matchRegex(regexName,name)){
        setBorderRedIfInvalid('jobseeker_name');
        showErrorMessage('nameError',"Please enter a valid name.")
      }else{
        setBorderIfValid('jobseeker_name');
        removeErrorMessage('nameError');
         nameValid = true;
      }
      /*-----------Validate Number---------------------*/
      if(number == ''){
        setBorderRedIfInvalid('phone_number');
        showErrorMessage('phoneError',"Please enter your number.")
      }
      else if(!matchRegex(numberRegex,number)){
        setBorderRedIfInvalid('phone_number');
        showErrorMessage('phoneError',"Please enter a valid contact number.")
      }else{
        setBorderIfValid('phone_number');
        removeErrorMessage('phoneError');
        numberValid = true;
      }
      /*----------------Validate Email -----------------*/
      if(email == ''){
        setBorderRedIfInvalid('email');
        showErrorMessage('emailError',"Please enter email address.")
      }else if(!matchRegex(emailRegex,email)){
        setBorderRedIfInvalid('email');
        showErrorMessage('emailError',"Please enter valid email address.(gmail only)")
      }else{
        setBorderIfValid('email');
        removeErrorMessage('emailError');
        emailValid = true;
      }
      /*---------------Validate Password ---------------------*/
      if(password == '' || !matchRegex(passwordRegex,password)){
        setBorderRedIfInvalid('password');
        showErrorMessage('passwordError',"Please enter a strong password.");
      }else{

        setBorderIfValid('password');
        removeErrorMessage('passwordError');
      }
      /*------------------Check if password match or not ------------*/
      if(checkPassword(password,confirm_password)){
        setBorderIfValid('confirm_password');
        removeErrorMessage('cpasswordError');
        passwordValid = true;
      }else{
        setBorderRedIfInvalid('confirm_password');
        showErrorMessage('cpasswordError',"Password not matched.");
      }
        // console.log(nameValid,emailValid,numberValid,passwordValid)
      if(nameValid && emailValid && numberValid && passwordValid){
        return true;
      }else{
        return false;
      }
    }

    const validateEmployerForm = (name,number,email,password,confirm_password)=>{
      if(name == ''){
        setBorderRedIfInvalid('employer_name');
        showErrorMessage('nameError',"Name is required.")
      }
      else if(name.length < 4 || !matchRegex(regexName,name)){
        setBorderRedIfInvalid('employer_name');
        showErrorMessage('nameError',"Enter a valid name ( at least 4 characters)")
      }else{
        setBorderIfValid('employer_name')
        removeErrorMessage('nameError')
        nameValid = true
      }
      // Validate number.
      if(number == ''){
        setBorderRedIfInvalid('employer_number')
        showErrorMessage('phoneError',"Phone number is required.")
      }
      else if(!matchRegex(numberRegex,number)){
        setBorderRedIfInvalid('employer_number')
        showErrorMessage('phoneError',"Please enter valid phone number.")
      }
      else{
        setBorderIfValid('employer_number')
        removeErrorMessage('phoneError')
        numberValid = true
      }
     
      if(email == ''){
        setBorderRedIfInvalid('employer_email')
        showErrorMessage("emailError","Email is required.")
      }
      else if(!matchRegex(emailRegex,email)){
        setBorderRedIfInvalid('employer_email')
        showErrorMessage("emailError","Please enter valid email (Gmail only).")
      }else{
        setBorderIfValid("employer_email")
        removeErrorMessage("emailError")
        emailValid = true;
      }
      
      // Password validation
      if(password == '' || !matchRegex(passwordRegex,password)){
        setBorderRedIfInvalid('employer_password')
        showErrorMessage("passwordError","Password choose a strong password.")
        
      }else{
        setBorderIfValid("employer_password")
        removeErrorMessage("passwordError")
      }

      if(checkPassword(password,confirm_password)){
        setBorderIfValid('confirm_password')
        removeErrorMessage('cpasswordError')
        passwordValid = true;
      }else{

        showErrorMessage('cpasswordError',"Password doesn't matched.")
        setBorderRedIfInvalid('confirm_password')

      }
      if(nameValid && emailValid && numberValid && passwordValid){
        return true
      }else{
        return false
      }
    }

    // Match regex with string.
    const matchRegex = (regExp,value)=>{
      return regExp.test(value);    
    }
})