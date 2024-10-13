function runPythonScript(){
    // var data = {}; data to send to script
    $.ajax({
        url: "/run_function",
        type: "POST",
        success: function(response){
            console.log(response.result);
            alert("everythinghelp");
        },
        error: function(error){
            console.error("AJAX request failed:", error);
        }


    });
}