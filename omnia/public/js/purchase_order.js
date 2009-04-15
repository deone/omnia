var vendor = "";

// AjaxPost
function createPO(id) {//{{{

    var vendorId = $("#vendor").val();
    var userId = id;
    var data = "vendor=" + vendorId + 
                "&user=" + userId;

    var url = "/purchase_order/new";

    $.ajax({

        url: url,
        type: "POST",
        data: data,
        dataType: "json",

        success: function(response) {
            if (response.code != 0) {
                $("#createPO-form .feedback")
                    .addClass("err")
                    .html("Error Creating Purchase Order");

            } else  {
                $("#po a").attr("href", "/purchase_order/" + response.data.body['id'] + "/add_line_item");
                showPO(response.data.body);
            }
        }

    });

}//}}}

function orderItem(POId)    {//{{{
    var item = $("#item").val();
    var unitprice = $("#unit-price").val();

    var data = "unitprice=" + unitprice + "&poid=" + POId;

    var url = "/lineitem/" + item + "/order";

    $.ajax({

        url: url,
        type: "POST",
        data: data,
        dataType: "json",

        success: function(response) {
            if (response.code != 0) {
                $("#add-PO-item-form .feedback")
                    .addClass("err")
                    .html("Error Adding Item");

            } else  {
                document.location = "/purchase_order/" + POId + "/edit";
            }
        }

    });
}//}}}
// Ajax Post functions end here


function populatePO(data)   {//{{{
    $("#po #id").html(data['id']);
    $("#po #date").html(data['date_created']);

    $("#line-items #amount").html(data['total_amount']);

    // Populate vendor-details div
    displayVendorDetails(data['vendor']);

}//}}}

function fillItemForm(data)    {//{{{
    vendor = data;
    populateItemField(data['lineitems']);
}//}}}

function showPO(po)   {//{{{
    // Hide form
    $("#create-PO").hide();

    // Populate Purchase Order
    populatePO(po);

    // Show Purchase Order
    $(".grid_12").removeClass("main");
    $("#purchase-order").show();
}//}}}

function displayVendorDetails(data) {//{{{
    $("#name").html(data['name']);
    $("#address").html(data['address']);
    $("#phone").html(data['phone']);
}//}}}

function populateItemField(data)    {//{{{

    var itemList = [];

    for (i = 0; i < data.length; i++)   {
        var itemObj = {};
        itemObj['id'] = data[i]['id'];
        itemObj['name'] = data[i]['name'];

        itemList[i] = itemObj;
    }

    displayOptions(itemList, "#item", "");

}//}}}

function showItemDetail() {//{{{
    $("#item-id")
        .attr("value",
            vendor['lineitems'][$$("item").selectedIndex - 1]['id']
        );
    
    $("#specification")
        .attr("value", 
            vendor['lineitems'][$$("item").selectedIndex - 1]['specification']
        );

    $("#quantity")
        .attr("value",
            vendor['lineitems'][$$("item").selectedIndex - 1]['quantity']
        );

    $("#unit-price")
        .attr("value",
            vendor['lineitems'][$$("item").selectedIndex - 1]['unitprice']
        );
}//}}}

function showPOItems(list, container)  {//{{{

    var rows = "";

    for (i=0; i<list.length; i++)   {
        
        rows += "<tr>" + 
                    "<td>" + list[i]['id'] + "</td>" + 
                    "<td>" + list[i]['name'] + "</td>" + 
                    "<td>" + list[i]['specification'] + "</td>" + 
                    "<td>" + list[i]['quantity'] + "</td>" + 
                    "<td>" + list[i]['unitprice'] + "</td>" + 
                    "<td>" + list[i]['totalprice'] + "</td>" + 
                    "<td><a href='/purchase_order/'>Delete</td>" + 
                "</tr>";

    }

    $(container).html(rows);

}//}}}

function displayPOs(POList, container)    {//{{{

    var rows = "";

    for (i=0; i<POList.length; i++) {
        
        rows += "<tr>" + 
                    "<td>" + POList[i]['id'] + "</td>" + 
                    "<td>" + POList[i]['vendor']['name'] + "</td>" + 
                    "<td>" + POList[i]['line_items'].length + "</td>" + 
                    "<td>" + POList[i]['total_amount'] + "</td>" + 
                    "<td>" + POList[i]['date_created'] + "</td>" + 
                    "<td>" + POList[i]['created_by']['firstname'] + " " + POList[i]['created_by']['lastname'] + "</td>" + 
                    "<td>" + POList[i]['status'] + "</td>" + 
                    "<td><a href='/purchase_order/" + POList[i]['id'] + "/view'>View</a></td>" + 
                "</tr>";

    }

    $(container).html(rows);

}//}}}
