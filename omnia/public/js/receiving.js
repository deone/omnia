var POObject = "";

function showDelivery(data) {//{{{
    $(".grid_12").removeClass("main");
    $("#create-delivery").hide();
    $("#receiving").show();

    $("#po #id").html(data['id']);
    $("#po #date").html(data['date_created']);

    showPOItems(data['line_items'], "#po-items");

    $("#line-items #amount").html(data['total_amount']);

    displayVendorDetails(data['vendor']);

    /*if (data['status'] != "Closed") {
        $("#po-id").attr("value", data['id']);
        $("#storage-location").show();
    } else  {
        $("#receiving").append("<div class='ok'><b>This Purchase Order Is Closed.</b></div>");
    }*/
}//}}}

function deliverItems() {//{{{
    var storageLocation = $("#location").val();
    var POId = $("#po-id").val();
    var poClosedBy = $("#user-id").val();

    for (i=0; i<POObject.line_items.length; i++)    {
        var item = POObject.line_items[i]['id'];
        var reqId = POObject.line_items[i]['requisitionid'];
        deliverItem(item, 2);
        closeReq(reqId);
    }
    closePO(storageLocation, poClosedBy, POId);
}//}}}

// AjaxPost
function deliverItem(itemId, _status)    {//{{{

    var url = "/lineitem/" + itemId + "/deliver";
    var data = "status=" + _status;

    $.ajax({

        url: url,
        type: "POST",
        data: data,
        dataType: "json",

        success: function(response) {
            if (response.code != 0) {
                $("#storage-location .feedback")
                    .addClass("err")
                    .html("Error. " + response.data.body);
            } else  {
                if (response.data.type == "error")    {
                    $("#storage-location .feedback")
                        .addClass("err")
                        .html("Error. " + response.data.body);
                }
            }
        }

    });
}//}}}

function fetchPO() {//{{{
    var poId = $("#PO-no").val();

    var url = "/purchase_order/" + poId + "/get_by_id";
    var data = "";

    $.ajax({

        url: url,
        type: "POST",
        data: data,
        dataType: "json",

        success: function(response) {
            if (response.code != 0) {
                $("#receive-form .feedback")
                    .addClass("err")
                    .html("Error. " + response.data.body);
            } else  {
                if (response.data.type == "error")  {
                    $("#receive-form .feedback")
                        .addClass("err")
                        .html("Error. " + response.data.body);
                } else  {
                    POObject = response.data.body;

                    var obj = new AjaxGet();
                    obj.get("/invoice/" + response.data.body['id'] + "/get_by_poid");

                    showDelivery(response.data.body);
                }
            }
        }
        
    });

}//}}}

function closePO(storageLocation, poClosedBy, POId)  {//{{{
    var url = "/purchase_order/" + POId + "/close";
    var data =  "location=" + storageLocation + 
                "&closed_by=" + poClosedBy;

    $.ajax({

        url: url,
        type: "POST",
        data: data,
        dataType: "json",

        success: function(response) {
            if (response.code != 0) {
                alert("Error");
            } else  {
                $("#storage-location .feedback")
                    .addClass("ok")
                    .html("Items Received. Purchase Order Closed.");
            }
        }

    });
}//}}}

function closeReq(reqId)    {//{{{
    var url = "/requisition/close";
    var data = "req_id=" + reqId;

    $.ajax({
        url: url,
        type: "POST",
        data: data,
        dataType: "json",

        success: function(response) {
            if (response.code != 0) {
                alert("Error: " + response.data.body);
            } else  {
                if (response.data.type != "ok") {
                    alert("Error: " + response.data.body);
                }
            }
        }
    });
}//}}}
