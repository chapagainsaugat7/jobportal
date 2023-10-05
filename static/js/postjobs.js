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
      const deadline = $('#deadline')
      const loc_type = $('#loc_type').val()
     
    })
  })