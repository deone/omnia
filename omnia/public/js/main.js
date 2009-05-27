function parseDate(day, month, year)   {//{{{

    var _date = year + "-" + month + "-" + day;
    return _date;

}//}}}

function displayOptions(data, element, match)   {//{{{

    var options = "<option value=''>--Select--</option>";

    for (i=0; i<data.length; i++)   {

        if (data[i]["name"] == match)   {
            options +=  "<option value='" + data[i]["id"] + 
                        "' selected='selected'>" + 
                        data[i]["name"] + "</option>";
        } else  {
            options +=  "<option value='" + data[i]["id"] + 
                        "'>" + data[i]["name"] + "</option>";
        }

    }

    $(element).html(options);

}//}}}

function $$(id) {
    return document.getElementById(id);
}

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
                "</tr>";

    }

    $(container).html(rows);

}//}}}

function displayVendorDetails(data) {//{{{
    $("#name").html(data['name']);
    $("#address").html(data['address']);
    $("#phone").html(data['phone']);
}//}}}

var role = {//{{{
    "Administrator": "<li><a href='/dashboard'>Dashboard</a></li><br/>" + 
            "<li><span>Requisition</span></li>" + 
            "<li><a href='/requisition/create'>Create Requisition</a></li>" + 
            "<li><a href='/requisition'>View Requisitions</a></li>" + 
            "<li><a href='/requisition/approve'>Approve Requisitions</a></li><br/>" + 
            "<li><span>Purchase Order<span></li>" + 
            "<li><a href='/purchase_order/create'>Create Purchase Order</a></li>" + 
            "<li><a href='/purchase_order'>View Purchase Orders</a></li><br/>" + 
            "<li><span>Warehouse</span></li>" + 
            "<li><a href='/receiving'>Receive Items</a></li>" + 
            "<li><a href='/warehouse'>View Warehouse</a></li><br/>" + 
            "<li><a href='/logout'>Logout</a></li>",

    "Buyer": "<li><a href='/dashboard'>Dashboard</a></li><br/>" + 
            "<li><span>Requisition</span></li>" + 
            "<li><a href='/requisition/create'>Create Requisition</a></li>" + 
            "<li><a href='/requisition'>View Requisitions</a></li></br/>" + 
            "<li><span>Purchase Order<span></li>" + 
            "<li><a href='/purchase_order/create'>Create Purchase Order</a></li>" + 
            "<li><a href='/purchase_order'>View Purchase Orders</a></li><br/>" +
            "<li><a href='/logout'>Logout</a></li>",

    "Procurement Manager": "<li><a href='/dashboard'>Dashboard</a></li><br/>" +
            "<li><span>Requisition</span></li>" + 
            "<li><a href='/requisition/approve'>Approve Requisitions</a></li><br/>" + 
            "<li><a href='/logout'>Logout</a></li>",

    "Warehouse Manager": "<li><a href='/dashboard'>Dashboard</a></li><br/>" +
            "<li><span>Warehouse</span></li>" + 
            "<li><a href='/receiving'>Receive Items</a></li>" + 
            "<li><a href='/warehouse'>View Warehouse</a></li><br/>" + 
            "<li><a href='/logout'>Logout</a></li>",
}//}}}
