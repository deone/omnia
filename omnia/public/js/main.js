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
