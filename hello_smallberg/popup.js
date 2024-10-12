$(function(){
    $('#name').keyup(function(){
        $('#greet').text($('#name').val()+" loves Smallberg!");
    })
})