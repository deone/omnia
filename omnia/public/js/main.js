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
