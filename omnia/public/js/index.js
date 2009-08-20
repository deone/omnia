$(function()    {

    document.forms.login.username.focus();

    validateLogin();

});

function validateLogin()    {

    $("#login").validate({

        rules:  {
            username: "required",
            password: "required"
        },

        messages:   {
            username: "Your username is required",
            password: "Your password is required"
        },

        submitHandler: function()   {

            var username = $("#username").val();
            var password = $("#password").val();
            var url = "/auth/login";

            var data =  "username=" + username + 
                        "&password=" + password;

            login(data, url);

        }

    });

}

function login(data, url)   {

    $(".feedback").html("<img src='/img/ajax-loader.gif'/>");

    $.ajax({

        url: url,
        type: "POST",
        data: data,
        dataType: "json",

        success: function(response) {
            type = response.data.type;
            data = response.data.body;

            if (type == "error")    {
                $(".feedback")
                    .addClass("err")
                    .html("Invalid username and/or password");
            } else {
                document.location = "/dashboard";
            }
        }

    });

}
