// Ajax POST
function createReq()    {//{{{

    var dateRequired = parseDate($("#day").val(), $("#month").val(), $("#year").val());
    var reqDesc = $("#req-description").val();
    var organization = $("#organization").val();
    var fullName = $("#firstname").val() + " " + $("#surname").val();
    var phoneNumber = $("#phone-number").val();

    var data = "datereq=" + dateRequired +
                "&reqdesc=" + reqDesc + 
                "&organization=" + organization +
                "&fullname=" + fullName + 
                "&phone=" + phoneNumber;

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
                document.location = "/requisition/" + response.data.body['id'] + "/add_line_item";
            }
        }

    });

}//}}}

function addLineItem(reqId)  {//{{{

    var name = $("#item-name").val();
    var type = $("#item-type").val();
    var specification = $("#specification").val();
    var qty = $("#quantity").val();
    var unitprice = $("#unitprice").val();
    var vendor = $("#vendor").val();

    var data =  "name=" + name +
                "&type=" + type +
                "&spec=" + specification +
                "&qty=" + qty + 
                "&unitprice=" + unitprice + 
                "&vendor=" + vendor;

    var url = "/lineitem/" + reqId + "/new";

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

function approveReq(id, user_id) {//{{{

    $.ajax({

        url: "/requisition/" + id + "/approve_req",
        type: "POST",
        data: "user_id=" + user_id,
        dataType: "json",

        success: function(response) {
            if (response.code != 0)  {
                alert("Error Approving requisition");
            } else  {
                document.location = "/requisition/approve";
            }
        }

    });

}//}}}



function showReqDetails(req)   {//{{{

    rf = document.referrer.split("/");

    var reqDetail = "<p>" + 
                        "Requisition <b>#" + req['id'] + "</b><br/>" + 
                        "Required <b>" + req['date_required'].split(" ")[0] + "</b><br/>" + 
                        "Requestor <b>" + req['full_name'] + "</b><br/>" + 
                        "Organization <b>" + req['organization'] + "</b><br/>" + 
                        "Requestor&rsquo;s Phone Number <b>" + req['phone_number'] + "</b><br/>" + 
                        "Description <b>" + req['description'] + "</b><br/>" + 
                        "<a href='/requisition/" + req['id'] + "/add_line_item'>Add Item</a>" + 
                    "</p>";

    $("#req-detail").html(reqDetail);

}//}}}

function displayReqAndItems(req)   {//{{{

    showReqDetails(req); 

    if (req['lineitems'] != "") {

        var lineItems = req['lineitems'];
        createItemRows("#req-items", lineItems);
        showExtraActions();

    }
        
}//}}}

function displayReqs(reqList, container)  {//{{{

    var rows = "";

    for (i=0; i<reqList.length; i++)   {

        rows += "<tr>" + 
                    "<td>" + reqList[i]['id'] + "</td>" + 
                    "<td>" + reqList[i]['description'] + "</td>" + 
                    "<td>" + reqList[i]['organization'] + "</td>" + 
                    "<td>" + reqList[i]['lineitems'].length + "</td>" + 
                    "<td>" + reqList[i]['status'] + "</td>" + 
                    "<td><a href='/requisition/" + reqList[i]['id'] + "/req_and_items'>Details</a></td>" + 
                "</tr>";

    }

    $(container).html(rows);

}//}}}

function displayApprovedReqs(reqList, container)  {//{{{

    var rows = "";

    for (i=0; i<reqList.length; i++)   {

        rows += "<tr>" + 
                    "<td>" + reqList[i]['requisition_id'] + "</td>" + 
                    "<td>" + reqList[i]['requisition']['description'] + "</td>" + 
                    "<td>" + reqList[i]['user']['firstname'] + " " + reqList[i]['user']['lastname'] + "</td>" + 
                "</tr>";

    }

    $(container).html(rows);

}//}}}

function createItemRows(container, list)   {//{{{

    var rows = "";
    var totalQty = 0;
    var totalAmount = 0;

    for (i=0; i<list.length; i++)   {

        totalAmount += parseInt(list[i]['unitprice'] * parseInt(list[i]['quantity']));

        rows += "<tr>" + 
                    "<td>" + list[i]['id'] + "</td>" + 
                    "<td>" + list[i]['name'] + "</td>" + 
                    "<td>" + list[i]['itemtype'] + "</td>" + 
                    "<td>" + list[i]['vendorid'] + "</td>" + 
                    "<td>" + list[i]['specification'] + "</td>" + 
                    "<td>" + list[i]['quantity'] + "</td>" + 
                    "<td>" + list[i]['unitprice'] + "</td>" + 
                    "<td>" + list[i]['totalprice'] + "</td>" + 
                "</tr>";

    }

    $(container).html(rows + "<tr>" + 
                                "<td>&nbsp;</td>" + 
                                "<td>&nbsp;</td>" + 
                                "<td>&nbsp;</td>" + 
                                "<td>&nbsp;</td>" + 
                                "<td><b>TOTAL</b></td>" + 
                                "<td>&nbsp;</td>" + 
                                "<td>&nbsp;</td>" + 
                                "<td>" + totalAmount + "</td>" + 
                            "</tr>"
            );

}//}}}

function showExtraActions() {//{{{

    var referrer = document.referrer;

    // Add 'back' links to page (to ease viewing) except when adding line item
    var rf = referrer.split("/");
    if (rf[rf.length - 1] != "add_line_item") {
        $("#other").show();
        $("#other input").before("<a class='link-back' href='" + referrer + "'>Back</a>");
    }

    // If page was redirected from http://foobar/requisition/approve, add 'Approve' button
    if (rf[rf.length - 1] == "approve") {
        $(".inner input").show();
    }

}//}}}

function populateItemnameVendor(type) {//{{{
    var obj = new AjaxGet();
    obj.get("/item/get_by_type/" + type);
    obj.get("/vendor/get_names");
}//}}}
