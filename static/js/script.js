$('document').ready(function(){
   if ( window.history.replaceState ) {
      window.history.replaceState( null, null, window.location.href );
    }

    // Handeling employer dashboard sidebar
        $('[data-toggle=offcanvas]').click(function() {
          $('.row-offcanvas').toggleClass('active');
        });
        
        $('textarea').each(function(){
                $(this).val($(this).val().trim());
            }
        );
})