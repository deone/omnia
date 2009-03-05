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

            if (response.data.type == "object")   {
                displayReqAndItems(req);

            } else if (response.data.type == "all_reqs_list") {
                displayReqs("#reqs-container", req);

            } else if (response.data.type == "open_reqs_list")  {
                displayOpenReqs("#open-reqs-container", req);
            }

        }

    });

}//}}}

function showReqDetails(req)   {//{{{

    rf = document.referrer.split("/");

    if (rf[rf.length - 1] == "add_item")  {
        var reqDetail = "<p>" + 
                            "Requisition #" + req['id'] + "<br/>" + 
                            req['description'] + "&nbsp;&nbsp;" + 
                            "<a href='/requisition/" + req['id'] + "/add_item'>Add Item</a>" + 
                        "</p>";
    } else  {
        var reqDetail = "<p>" + 
                            "Requisition #" + req['id'] + "<br/>" + 
                            req['description'] + 
                        "</p>";
    }

    $("#req-detail").html(reqDetail);

}//}}}

function displayReqAndItems(req)   {//{{{

    showReqDetails(req); 

    if (req['items'] != "") {

        var items = req['items'];
        createItemRows("#req-items", items);
        showExtraActions();

    }
        
}//}}}

function approveReq(id) {//{{{
    alert("Requisition " + id + " approved");
}//}}}

// Req. status is the only difference btw displayReqs() and displayOpenReqs(), refactor!
function displayReqs(container, req)  {//{{{
    var rows = "";

    for (i=0; i<req.length; i++)   {

        rows += "<tr>" + 
                    "<td>" + req[i]['id'] + "</td>" + 
                    "<td>" + req[i]['description'] + "</td>" + 
                    "<td>" + req[i]['status'] + "</td>" + 
                    "<td><a href='/requisition/" + req[i]['id'] + "/req_and_items'>Details</a></td>" + 
                "</tr>";

    }

    $(container).html(rows);

}//}}}

function displayOpenReqs(container, req)  {//{{{
    var rows = "";

    for (i=0; i<req.length; i++)   {

        rows += "<tr>" + 
                    "<td>" + req[i]['id'] + "</td>" + 
                    "<td>" + req[i]['description'] + "</td>" + 
                    "<td><a href='/requisition/" + req[i]['id'] + "/req_and_items'>Details</a></td>" + 
                "</tr>";

    }

    $(container).html(rows);

}//}}}


// Items
function createItemRows(container, list)   {//{{{

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

    $(container).html(rows);

}//}}}

function showExtraActions() {//{{{

    var referrer = document.referrer;

    // Add 'back' links to page (to ease viewing) except during requisition creation
    var rf = referrer.split("/");
    if (rf[rf.length - 1] != "add_item") {
        $("#other").show();
        $("#other input").before("<a class='link-back' href='" + referrer + "'>Back</a>");
    }

    // If page was redirected from http://foobar/requistion/approve, add 'Approve' button
    if (rf[rf.length - 1] == "approve") {
        $(".inner input").show();
    }

}//}}}

function showItems(url)    {//{{{

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
                    createItemRows("#item-container", itemList.data.body);
                }
            }
        }

    });

}//}}}
