$(function(){
    $('#addQuestion').on('click',function(){
        const job_id = $('#job_id').val()
        let question = $('#question').val()
        let correctAnswer = $('#correctAnswer').val()
        let opt1 = $('#opt_1').val()
        let opt2 = $('#opt_2').val()
        let opt3 = $('#opt_3').val()
        let opt4 = $('#opt_4').val()
        const csrf = $('input[name=csrfmiddlewaretoken]').val()

        if(question === '' || correctAnswer === '' || opt1 === '' ||opt2===''||opt3===''||opt4==='' ){
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Please fill all the fields!',
              })
        }else{
            let data = {
                'job_id':job_id,
                'question':question,
                'correctAnswer':correctAnswer,
                'opt1':opt1,
                'opt2':opt2,
                'opt3':opt3,
                'opt4':opt4
            }
            $.ajax({
                url:'/employer/viewquestions/'+job_id,
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
                    Swal.fire({
                        icon:'success',
                        title:'Success',
                        text:"Questions added successfully.",
                    }).then((result)=>{
                        if (result.isConfirmed) {
                            location.reload()
                        }
                    })
                },
                error:function(res){
                    Swal.fire({
                        icon: 'error',
                        title: 'Oopss...',
                        text: 'Something went wrong! ',
                      })
                }
            })


        }

    })
})