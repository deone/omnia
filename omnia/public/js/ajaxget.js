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
                    var url = document.URL.split("/");

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
                        // This is used for both items and lineitems. See controllers for details.
                        displayOptions(data, "#item-name", "");

                    } else if (dataType == "item_list") {
                        if (url[url.length - 1] == "view")    {
                            showInvoiceItems(data, "#inv-items");
                        }

                        if (url[url.length - 1] == "edit")  {
                            editInvoiceItems(data, "#inv-items");
                        }

                        if (url[url.length - 1] == "warehouse") {
                            displayItems(data);
                        }

                    } else if (dataType == "item_type_list")    {
                        showItemBoxes(data);

                    } else if (dataType == "item_spec_list")    {
                        showSpec(data);

                    } else if (dataType == "vendorname_list")   {
                        displayOptions(data, "#vendor", "");

                    } else if (dataType == "poid_list") {
                        displayOptions(data, "#PO-no", "");

                    } else if (dataType == "po_object") {

                        if (url[url.length - 1] == "add_line_item")    {
                            $("#vendor-name").html(data['vendor']['name']);
                            fillItemForm(data['vendor']);
                        }

                        if (url[url.length - 1] == "edit")  {
                            populatePO(data);
                            editPOItems(data['line_items'], "#po-items");
                        }

                        if (url[url.length - 1] == "view" || url[url.length - 1] == "doc_print")  {
                            populatePO(data);
                            if (data['status'] == "Closed") {
                                $("#po ul").append("<li>Status&nbsp;<b>" + data['status'] + "</b></li>" +
                                "<li>Closed By&nbsp;<b>" + data['closed_by'] + "</b></li>" + 
                                "<li>Date Closed&nbsp;<b>" + data['date_closed'] + "</b></li>"
                                );
                            }
                            showPOItems(data['line_items'], "#po-items");
                        }

                        if (url[url.length - 1].split("=")[0] == "create?po_id") {
                            $("#vendor-name").html(data['vendor']['name']);
                            $("#po-id").html(data['id']);
                            $("#purchase-order-id").attr("value", data["id"]);
                            $("#vendor-id").attr("value", data["vendor"]["id"]);

                            $("#vendor #name").html(data['vendor']['name']);
                            $("#vendor #address").html(data['vendor']['address']);
                            $("#vendor #phone").html(data['vendor']['phone']);
                        }

                    } else if (dataType == "po_list")   {
                        displayPOs(data, "#pos-container");

                    } else if (dataType == "invoice_object")    {
                        if (url[url.length - 1] == "receiving")  {
                            $("#invoice-detail #number").html(data['invoice_no']);
                            $("#invoice-detail #date").html(data['date_created']);
                        }

                        if (url[url.length - 1] == "add_item")  {
                            $("#vendor-name").html(data['vendor']['name']);

                            var obj = new AjaxGet();
                            obj.get("/lineitem/" + data['vendor']['id'] + "/get_for_invoice?po_id=" + data['po_id']);

                        }

                        if (url[url.length - 1] != "add_item")  {

                            if (url[url.length - 1] != "receiving")  {
                                $("#name").html(data['vendor']['name']);
                                $("#address").html(data['vendor']['address']);
                                $("#phone").html(data['vendor']['phone']);
                                $("#invoice-detail span").html(data['invoice_no']);
                                $("#amount").html(data['total_amount']);

                                var obj = new AjaxGet();
                                obj.get("/lineitem/" + data['invoice_no'] + "/get_by_invoice_no");
                            }

                        }

                    } else if (dataType == "error")   {

                        if (data == "Invoice not received") {
                            $("#invoice-button").show();
                        }

                    } else if (dataType == "ok")    {

                            $("#edit-PO").hide();
                            $("#add-line-item").hide();
                            $("#view-PO").hide();
                            $("#line-items a").hide();

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
