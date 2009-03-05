// Requisitions
function showCreateReqForm()    {//{{{

    $("#req-links").remove();
    $("#requisition-form").show();

}//}}}

function createReq()    {//{{{
            
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

}//}}}

function addItem(reqId)  {//{{{

    var qty = $("#quantity").val();
    var name = $("#item-name").val();
    var desc = $("#item-description").val();
    var unitprice = $("#unitprice").val();

    var data =  "qty=" + qty +
                "&name=" + name +
                "&desc=" + desc +
                "&unitprice=" + unitprice;

    var url = "/requisition/" + reqId + "/new_item";

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
                document.location = "/requisition/" + reqId + "/req_and_items";
            }
        }

    });

}//}}}

function getReq(url)  {//{{{

    $.ajax({

        url: url,
        type: "GET",
        dataType: "json",

        success: function(response)  {

            var req = response.data.body;

            if (response.data.type == "list")   {
                displayReqs(req);

            } else if(response.data.type == "object") {
                displayReqAndItems(req);

            }

        }

    });

}//}}}

function displayReqAndItems(req)   {//{{{

    var reqDetail = "<p>" + 
                        "Requisition #" + req['id'] + "<br/>" + 
                        req['description'] + "&nbsp;&nbsp;" + 
                        "<a href='/requisition/" + req['id'] + "/add_item'>Add Item</a>" + 
                    "</p>";

    $("#req-detail").html(reqDetail);

    if (req['items'] != "") {

        var items = req['items'];
        var itemList = "";

        for (i=0; i<items.length; i++)  {
            itemList += "<tr>" + 
                            "<td>" + items[i]['id'] + "</td>" + 
                            "<td>" + items[i]['name'] + "</td>" + 
                            "<td>" + items[i]['description'] + "</td>" + 
                            "<td>" + items[i]['quantity'] + "</td>" + 
                            "<td>" + items[i]['unitprice'] + "</td>" + 
                            "<td><a href='#'>Edit</a></td>" + 
                            "<td><a href='#'>Delete</a></td>" +
                        "</tr>";
        }

        $("#req-items").html(itemList);

    }
        
}//}}}

function displayReqs(req)  {//{{{
    var rows = "";

    for (i=0; i<req.length; i++)   {

        rows += "<tr>" + 
                    "<td>" + req[i]['id'] + "</td>" + 
                    "<td>" + req[i]['description'] + "</td>" + 
                    "<td>" + req[i]['status'] + "</td>" + 
                    "<td><a href='/requisition/" + req[i]['id'] + "/items'>View Items</a></td>" + 
                "</tr>";

    }

    $("#reqs-container").html(rows);

}//}}}

// Items//{{{
function createItemRows(list)   {

    var rows = "";

    for (i=0; i<list.length; i++)   {

        rows += "<tr>" + 
                    "<td>" + list[i]['id'] + "</td>" + 
                    "<td>" + list[i]['name'] + "</td>" + 
                    "<td>" + list[i]['description'] + "</td>" + 
                    "<td>" + list[i]['quantity'] + "</td>" + 
                    "<td>" + list[i]['unitprice'] + "</td>" + 
                "</tr>";
    }

    $("#item-container").html(rows);
    $("#item-container").append("<a href='/requisition/all'>Back</a>");
}

function showItems(url)    {
    
    $.ajax({

        url: url,
        type: "GET",
        dataType: "json",

        success: function(itemList)  {
            if (itemList.code != 0)  {
                alert(itemList.code + ": " + itemList.data.body);
            } else  {
                if (itemList.data.type != "list")    {
                    alert("Unrecognized data format: " + itemList.data.type);
                } else  {
                    createItemRows(itemList.data.body);
                }
            }
        }

    });

}//}}}
