function isValidJwt (jwt) {
    if (!jwt || jwt.split('.').length < 3) {
      return false
    }

    const data = JSON.parse(atob(jwt.split('.')[1]))
    const exp = new Date(data.exp * 1000)
    const now = new Date()
    return now < exp
  }
  function bindAjaxToProccessButtons(jquery_object){
    jquery_object("button[id^='file_']").click(function(e){
        e.preventDefault();
        file_name = jquery_object(this)[0].id.substring(5) + '.csv';
        jquery_object.ajax({
              url: window.location.origin+'/user/files/'+file_name,
              type: 'POST',
              contentType: false,
              processData: false,
              success: function(response){
                console.log(response);
                alert("Proccessed")
              },
              headers: {"Authorization": "Bearer: " + localStorage.getItem("jwt_token")}
            
    })
      });
  }
  $(document).ready(function() {
    if(localStorage.getItem("jwt_token") == null){
      window.location.replace("/login");
    } else {
      if(isValidJwt(localStorage.getItem("jwt_token")) == false)
      {
        alert("Token Expired");
        window.location.replace("/login");
      }
    }
    $.ajax({
              url: window.location.origin+'/user/files/api',
              type: 'GET',
              contentType: false,
              processData: false,
              success: function(response){
                for(i=0;i<response["files"].length;i++){
                  $('#table_body').append("<tr>"+
                          "<td>"+response["files"][i]+"</td>"+
                          "<td><button id='file_"+response["files"][i].split(".")[0]+"'>Process</button></td>"
                      +"</tr>");
                }
                console.log(response);
              },
              headers: {"Authorization": "Bearer: " + localStorage.getItem("jwt_token")}
            
    }).then(function(){
      $("button[id^='file_']").click(function(){
        
        bindAjaxToProccessButtons($)
      });
    });
    $("#but_upload").click(function() {
        var fd = new FormData();
        var files = $('#file')[0].files[0];
        fd.append('file', files);

        $.ajax({
            url: window.location.origin+'/upload_file',
            type: 'post',
            data: fd,
            contentType: false,
            processData: false,
            headers: {"Authorization": "Bearer: " + localStorage.getItem("jwt_token")},
            success: function(response){
                console.log(response);
                if(response != 0){
                    alert('file uploaded');
                    $('#table_body').append("<tr>"+
                        "<td>"+response.new_file_name+"</td>"+
                        "<td><button id='file_"+response['new_file_name'].split(".")[0]+"'>Process</button></td>"
                    +"</tr>");
                }
                else{
                    console.log(response)
                    alert('file not uploaded');
                }
            },
        }).then(function(){
            $("button[id^='file_']").click(function(){
              bindAjaxToProccessButtons($)
            });
          });
    });
  });