$(document).ready(function() {
    $("form").submit(function(e) {
        e.preventDefault();
        console.log("entro aqui")
        $.ajax({
            url: window.location.origin+'/login/',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({
                "user_email": $("#user_email").val(),
                "user_password": $("#user_password").val()
            }),
            contentType: "application/json;charset=utf-8",
            Accept: 'application/json',
            success: function(response){
                console.log(response)
                if(response != 0){
                    localStorage.setItem("jwt_token", response.token);
                    window.location.replace("/user/files");
                    
                }
                else{
                    alert("login incorrecto");
                }
            },
        });
    });
});