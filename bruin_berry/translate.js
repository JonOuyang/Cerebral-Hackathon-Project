// const spawner = require('child_process').spawn;

// const python_process = spawner('python', ['../backend.py']);

// python_process.stdout.on('data', (data) => {
//     console.log(JSON.parse(data));
// });

$(function(){
    $('#name').keyup(function(){
        $('#greet').text($('#name').val()+" loves Smallberg!");
    })
})

// $.ajax({
//     type: "POST",
//     url: "~/pythoncode.py",
//     data: { param: text}
//   }).done(function( o ) {
//      // do something
//   });

//const { spawn } = require('child_process');


// const sensor = spawn('python', ['backend.py']);
// sensor.stdout.on('data', function(data) {

//     // convert Buffer object to Float
//     console.log(data);
// });