function fetchOptions(url, element, match) {

    $.ajax({
            url: url,
            type: "GET",
            dataType: "json",

            success: function(response) {
                displayOptions(response.data.body, element, match);
            }

    });

}


function displayOptions(data, element, match)   {

    var options = "<option value=''>--Select--</option>";

    for (i=0; i<data.length; i++)   {

        if (data[i]["name"] == match)   {
            options += "<option value='" + data[i]["id"] + "' selected='selected'>" + data[i]["name"] + "</option>";
        } else  {
            options += "<option value='" + data[i]["id"] + "'>" + data[i]["name"] + "</option>";
        }

    }

    $(element).append(options);

}
