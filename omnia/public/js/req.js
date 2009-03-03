function showCreateReqForm()    {

    $("#req-links").remove();
    $("#requisition-form").show();

}

function submitReq()    {
            
    var data = "description=" + $("#req-description").val();

    var url = "/requisition/new";

    $.ajax({

        url: url,
        type: "POST",
        data: data,
        dataType: "json",

        success: function(response) {
            if (response.code != 0) {
                $("#requisition .feedback")
                    .addClass("err")
                    .html("Error Creating Requisition");

            } else  {
                document.location = "/requisition/" + response.data.body['id'] + "/add_item";
            }
        }

    });

}
