// AjaxPost
function createInvoice()    {//{{{

    var invoiceNo = $("#invoice-no").val();
    var poId = $("#purchase-order-id").val();
    var vendorId = $("#vendor-id").val();
    var userId = $("#user-id").val();

    var data =  "invoice_no=" + invoiceNo + 
                "&po_id=" + poId + 
                "&vendor_id=" + vendorId + 
                "&user_id=" + userId;

    var url = "/invoice/new";

    $.ajax({
        url: url,
        type: "POST",
        data: data,
        dataType: "json",

        success: function(response) {
            if (response.code != 0) {
                $("#create-invoice-form .feedback")
                    .addClass("err")
                    .html("Error Creating Invoice");

            } else  {
                $("#invoice-detail a").attr("href", "/invoice/" + response.data.body['invoice_no'] + "/add_item");
                showInvoice(response.data.body);
            }

        }

    });

}//}}}

function showInvoice(data)  {//{{{
    $("#create-invoice").hide();

    $("#invoice-detail span").html(data['invoice_no']);
    $("#line-items #amount").html(data['total_amount']);

    $(".grid_12").removeClass("main");
    $("#invoice").show();
}//}}}

function addItemToInvoice() {//{{{
    var itemId = $("#item-name").val();
    var specification = $("#specification").val();
    var quantity = $("#quantity").val();
    var unitPrice = $("#unit-price").val();
    var invoiceNo = $("#invoice-no").val();

    var data =  "item_id=" + 
                "&specification=" + specification + 
                "&quantity=" + quantity + 
                "&unit_price=" + unitPrice + 
                "&invoice_no=" + invoiceNo;
    
    var url = "/lineitem/" + itemId + "/invoice";

    $.ajax({
        url: url,
        type: "POST",
        data: data,
        dataType: "json",

        success: function(response) {
            if (response.code != 0) {
                $("#add-inv-item-form .feedback")
                    .addClass("err")
                    .html("Error Adding Item To Invoice");
            } else  {
                document.location = "/invoice/" + invoiceNo + "/edit";
            }

        }

    });

}//}}}


function editInvoiceItems(list, container)  {

    var rows = "";

    for (i=0; i<list.length; i++)   {
        
        rows += "<tr>" + 
                    "<td>" + list[i]['id'] + "</td>" + 
                    "<td>" + list[i]['name'] + "<br/>" + list[i]['specification'] + "</td>" + 
                    "<td>" + list[i]['quantity'] + "</td>" + 
                    "<td>" + list[i]['unitprice'] + "</td>" + 
                    "<td>" + list[i]['totalprice'] + "</td>" + 
                    "<td><a href=''>Delete</a></td>" + 
                "</tr>";

    }

    $(container).html(rows);

}

function showInvoiceItems(list, container)  {

    var rows = "";

    for (i=0; i<list.length; i++)   {
        
        rows += "<tr>" + 
                    "<td>" + list[i]['id'] + "</td>" + 
                    "<td>" + list[i]['name'] + "<br/>" + list[i]['specification'] + "</td>" + 
                    "<td>" + list[i]['quantity'] + "</td>" + 
                    "<td>" + list[i]['unitprice'] + "</td>" + 
                    "<td>" + list[i]['totalprice'] + "</td>" + 
                "</tr>";

    }

    $(container).html(rows);

}
