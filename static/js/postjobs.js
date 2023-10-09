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
                Swal.fire({
                    icon:'success',
                    text:message,
                    text:"Job Added Successfully."

                }).then(()=>{
                    $('#jobform')[0].reset()
                    fetchDataAndUpdateTable()
                })
                },
                error:function(res){
                    var message = res.error
                    if(res.status === 500){
                        Swal.fire({
                            icon:'error',
                            title:message,
                            text:"Please Try again."
                        })
                    }
                }
            })
        }

    })
   
       // Function to fetch and update data
  function fetchDataAndUpdateTable() {
    $.ajax({
      url: '/employer/getdata/',
      dataType: 'json',
      success: function (response) {
        if (response.data) {
          console.log(response.data)
          $.each(response.data, function (index, data) {
            var editIcon =" <div class='flex flex-md-col flex-sm-row'><a href='#' id='"+data.job_id+"' class='mx-2'><i class='fas fa-pen text-blue'></i></a>"
            var deleteIcon = "<a href='#' data-bs-toggle='modal' id='"+data.job_id+"' data-bs-target='#deletejob'><i class='fas fa-trash text-danger'></i></a></div>"

            var newRow = '<tr><td>'+(index+1)+'</td><td>'+data.job_type+'</td><td>'+data.job_position+'</td><td>'+data.job_requirement+'</td><td>'+data.job_description.substring(0,15)+'...'+'</td><td>'+data.salary+'</td><td>'+data.location_type+'</td><td>'+editIcon+deleteIcon+'</td></tr>'
            $('#jobTable tbody').append(newRow)
          });
        }else{
          var row = "<tr><td class='bg-danger text-white'>No Jobs are posted.</td></tr>"
          $('#jobTable tbody').append(row)
        }
      },
      error: function () {
        console.log('Error fetching data');
      },
    });

  }

  // Fetch and update data when the page loads
  fetchDataAndUpdateTable();
  })