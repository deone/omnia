var req;

function setReq(obj)   {
    req = obj;
}

function addItem()  {

    var qty = $("#quantity").val();
    var name = $("#item-name").val();
    var desc = $("#item-description").val();
    var unitprice = $("#unitprice").val();

    var data =  "qty=" + qty +
                "&name=" + name +
                "&desc=" + desc +
                "&unitprice=" + unitprice;

    var url = "/requisition/" + req['id'] + "/add_item";

    $.ajax({

        url: url,
        type: "POST",
        data: data,
        dataType: "json",

        success: function(response) {
            if (response.code != 0) {
                $("#add-item-form .feedback")
                    .addClass("err")
                    .html("Error Adding Item");
            } else  {
                showReq(req);
            }
        }

    });

}

function showReq(req)  {
    alert(req['description']);
    $("#add-item-form").remove();
    // Why is the action below not performed? I need to investigate this later.
    // For now, checkout to another branch to continue
    $("#req-info").show();
}

function showCreatereqForm()    {
    $("#req-links").remove();
    $("#requisition-form").show();
}

function showAdditemForm()  {
    $(".info").remove();
    $("#add-item-form").show();
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
                $("#requisition-form").remove();
                $(".activity-board").append(
                                        "<div class='info'>" + 
                                            "<h6 class='ok'>Requisition Created Successfully.</h6>" + 
                                            "<a id='add-item' href='#' onclick=\"showAdditemForm()\">Add item</a>" + 
                                        "</div>"
                                    );

                setReq(response.data.body);
            }
        }

    });

}
