$(document).ready(function(){
    const today = new Date()
    const oneMontFromToday = new Date()
    oneMontFromToday.setMonth(today.getMonth()+1)
    const todayFormatted = today.toISOString().split("T")[0]
    const oneMontFromTodayFormatted = oneMontFromToday.toISOString().split("T")[0]
    const datePicker = document.getElementById('deadline')
    datePicker.setAttribute('min',todayFormatted)
    datePicker.setAttribute('max',oneMontFromTodayFormatted)

    $('#addjob').on('click',function(ev){
      ev.preventDefault()
      const jobType = $('#job_type').val()
      const position = $('#position').val()
      const requirement = $('#requirement').val()
      const description = $('#description').val()
      const salary = $('#salary').val()
      const deadline = $('#deadline').val()
      const loc_type = $('#loc_type').val()
      const csrf = $('input[name=csrfmiddlewaretoken]').val()
      if (jobType === ''|| jobType==='Job Type' ||position === ''||requirement===''||description===''||salary===''||deadline===''||loc_type==='' || loc_type === 'Location Type'){
        
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Please Fill all fields.'
        })
    }else{
        let data = {
            type : jobType,
            job_position : position,
            job_requirement : requirement,
            job_description : description,
            job_salary : salary,
            job_deadline:deadline,
            location_type : loc_type,
        }
        $.ajax({
            url:'',
            method:"POST",
            headers:{
                "X-Requested-With": "XMLHttpRequest",
                'Accept':'application/json',
                'Content-Type':'application/json',
                'X-CSRFToken':csrf
            },
            dataType:'json',
            data:JSON.stringify(data),
            success:function(res){
                let message = res.message
                if(res.status == 200){
                    Swal.fire({
                        icon:'success',
                        title:'Success.',
                        text: 'Please Fill all fields.'
                        })
                    }
                },
                error:function(res){
                    console.log(`Error:{res}`);
                }
            })
        }
    })
  })