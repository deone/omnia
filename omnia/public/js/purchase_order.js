$(function()    {//{{{


    var obj = new AjaxGet();
    obj.get("/vendor/get_names");

    $("#item-name")
        .change(function()  {
            showItemSpec();
        });

    /*$("#quantity")
        .focus(alert($$("item-name").selectedIndex));*/
        
});//}}}

var vendor = "";

function showPOForm()   {//{{{
    var vendorId = ($("#vendor").val());

    obj = new AjaxGet();
    obj.get("/vendor/" + vendorId + "/get_by_id");

    $("#select-vendor-form").hide();

    $("#specification").attr("value", "");
    $("#purchase-order-form").show();
}//}}}

function displayVendorName(data, container) {//{{{
    vendor = data;
    $(container).html(data.name);
    populateItemField(data);
}//}}}

function populateItemField(data)    {//{{{

    var itemList = [];

    for (i = 0; i < data['lineitems'].length; i++)   {
        var itemObj = {};
        itemObj['id'] = data['lineitems'][i]['name'];
        itemObj['name'] = data['lineitems'][i]['name'];

        itemList[i] = itemObj;
    }

    displayOptions(itemList, "#item-name", "");

}//}}}

function showItemSpec() {
    $("#specification")
        .attr("value", 
            vendor['lineitems'][$$("item-name").selectedIndex - 1]['specification']
        );
}

function checkQuantity()    {
    var qty = vendor['lineitems'][$$("item-name").selectedIndex - 1]['quantity'];
    if (parseInt($("#quantity").val()) > parseInt(qty))   {
        $("#msg").html("You cannot order more than was requested");
        $("#quantity").attr("value", qty);
    }
}
