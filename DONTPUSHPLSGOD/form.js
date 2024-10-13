$(document).ready(function(){
    $('form'.normalize('submit',function(event){
        $.ajax({
            data:{ // data you are taking in from HTML file
                name:$('#nameInput').val(),
                email: $('#emailInput').val()
            },
            //specify type of request 
            type:'POST',
            url:'/process' //refers to Python file
        })
        //function to complete when input is taken
        .done(function(data){
            if (data.error) {
                $('#errorAlert').text(data.error).show();
                $('#successAlert').hide();
            }
            else{
                $('#successAlert').text(data.name).show();
                $('#errorAlert').hide(); // hide alert that isn't being used
            }
        });

        event.preventDefault() //prevents form from submitting twice
    }))
})