function AjaxGet(url)   {

    this.get = function (url)  {

        $.ajax({

            url: url,
            type: "GET",
            dataType: "json",

            success: function(response) {
                if (response.code != 0) {
                    alert(response.code + ": " + response.data.body);

                } else  {
                    var data = response.data.body;
                    var dataType = response.data.type;

                    var typeObj = {
                        day_optionlist: "#day",
                        month_optionlist: "#month",
                        year_optionlist: "#year",
                    }

                    if (dataType.split("_")[1] == "optionlist")   {
                        displayOptions(data, typeObj[dataType], "");

                    } else if (dataType == "itemtype_list") {
                        displayOptions(data, "#item-type", "");

                    } else if (dataType == "itemname_list") {
                        displayOptions(data, "#item-name", "");

                    } else if (dataType == "vendorname_list")   {
                        displayOptions(data, "#vendor", "");

                    } else if (dataType == "vendor_object") {
                        var url = document.URL.split("/");

                        if (url[url.length - 1] == "create")    {
                            displayVendorDetails(data);
                        }

                        if (url[url.length - 1] == "add_line_item")    {
                            $("#vendor-name").html(data['name']);
                            fillItemForm(data);
                        }

                    } else if (dataType == "po_object") {
                        obj = new AjaxGet();
                        obj.get("/vendor/" + data['vendorid'] + "/get_by_id");

                    } else if (dataType == "req_list")    {
                        displayReqs(data, "#reqs-container");

                    } else if (dataType == "openreqs_list") {
                        displayReqs(data, "#open-reqs-container");

                    } else if (dataType == "approvedreqs_list") {
                        displayApprovedReqs(data, "#approved-reqs-container");

                    } else if (dataType == "req_object")    {
                        displayReqAndItems(data);

                    } else  {
                        alert("Unrecognized data format: " + dataType);
                    }

                }
            }

        });

    }
    
}
