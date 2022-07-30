$(document).ready(function() {
    $("form").submit(function(e) {
        e.preventDefault();
        if($('#confirm_password').val() == $("#user_password").val()){
            $.ajax({
                url: window.location.origin+'/users',
                type: 'POST',
                dataType: 'json',
                data: JSON.stringify({
                    "user_name": $("#user_name").val(),
                    "user_email": $("#user_email").val(),
                    "user_password": $("#user_password").val()
                }),
                contentType: "application/json;charset=utf-8",
                Accept: 'application/json',
                success: function(response){
                    console.log(response)
                    if(response != 0){
                        window.location.replace("/login");
                        
                    }
                },
                error: function(){
                    alert("something went wrong")
                }
            });
        } else {
            alert("Password must match")
        }

    });
});