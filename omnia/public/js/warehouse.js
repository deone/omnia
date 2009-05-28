function showItemBoxes(list)    {//{{{

    for (i=0; i<list.length; i++)   {
        $(".inner").append(
                "<div id='cat" + i + "' class='grid_4 omega itembox'>" + 
                    "<h6>" + list[i] + "</h6>" + 
                    "<ul class='item-list'></ul>" + 
                "</div>"
                );
    }

    $(".inner").append("<div class='clear-float'></div>");

}//}}}

function showItemDetails(elem, name, qty, spec, vendor) {//{{{
    if (qty > 1)    {
        $(elem).append(
                "<li>" + 
                    "<a href='#'>" + name + " (" + qty + ")</a>" + 
                "</li>"
                );
    } else  {
        $(elem).append(
                "<li>" + 
                    "<a href='#'>" + name  + "</a>" + 
                "</li>"
                );
    }

    $(elem).append(
                "<li>" + 
                    "<ul class='item-spec'>" + 
                        "<li><b>Specs</b>:" + spec + "</li>" + 
                        "<li><b>Vendor</b>:" + vendor + "</li>" + 
                    "</ul>" + 
                "</li>"
                );
}//}}}

function displayItems(list)  {//{{{
    for (i=0; i<list.length; i++)   {

        if (list[i]['itemtype'] == "Computer Hardware")  {

            showItemDetails("#cat0 .item-list", list[i]['name'], list[i]['quantity'], list[i]['specification'], list[i]['vendor']);

        }


        if (list[i]['itemtype'] == "Engineering Tool")  {

            showItemDetails("#cat1 .item-list", list[i]['name'], list[i]['quantity'], list[i]['specification'], list[i]['vendor']);

        }

        if (list[i]['itemtype'] == "Computer Software")  {

            showItemDetails("#cat2 .item-list", list[i]['name'], list[i]['quantity'], list[i]['specification'], list[i]['vendor']);

        }

    }
}//}}}
