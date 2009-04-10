var vendor = "";

// AjaxPost
function createPO() {//{{{

    var vendorId = $("#vendor").val();
    var data = "vendor=" + vendorId;

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
                alert("Sucess: Item added");
            }
        }

    });
}//}}}
// Ajax Post functions end here


function populatePO(data)   {//{{{
    $("#po #id").html(data['id']);
    $("#po #date").html(data['date_created']);
    $("#po a").attr("href", "/purchase_order/" + data['id'] + "/add_line_item");

    $("#line-items #amount").html(data['total_amount']);

    // Get vendor object and populate vendor-details div
    obj = new AjaxGet();
    obj.get("/vendor/" + data['vendorid'] + "/get_by_id");
}//}}}

function fillItemForm(data)    {//{{{
    vendor = data;
    populateItemField(data.lineitems);
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
