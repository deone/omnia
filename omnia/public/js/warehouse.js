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

function displayItems(list)  {//{{{
    for (i=0; i<list.length; i++)   {

        if (list[i]['itemtype'] == "Computer Hardware")  {

            $("#cat0 .item-list").append(
                    "<li>" + 
                        "<a href='#'>" + list[i]['name'] + " (" + list[i]['quantity'] + ")</a>" + 
                    "</li>" + 
                    "<li>" + 
                        "<ul class='item-spec'>" + 
                            "<li><b>Specs</b>:" + list[i]['specification'] + "</li>" + 
                            "<li><b>Vendor</b>:" + list[i]['vendor'] + "</li>" + 
                        "</ul>" + 
                    "</li>"
                    );

        }


        if (list[i]['itemtype'] == "Engineering Tool")  {

            $("#cat1 .item-list").append(
                    "<li>" + 
                        "<a href='#'>" + list[i]['name'] + " (" + list[i]['quantity'] + ")</a>" + 
                    "</li>" + 
                    "<li>" + 
                        "<ul class='item-spec'>" + 
                            "<li><b>Specs</b>:" + list[i]['specification'] + "</li>" + 
                            "<li><b>Vendor</b>:" + list[i]['vendor'] + "</li>" + 
                        "</ul>" + 
                    "</li>"
                    ); 

        }

        if (list[i]['itemtype'] == "Computer Software")  {

            $("#cat2 .item-list").append(
                    "<li>" + 
                        "<a href='#'>" + list[i]['name'] + " (" + list[i]['quantity'] + ")</a>" + 
                    "</li>" + 
                    "<li>" + 
                        "<ul class='item-spec'>" + 
                            "<li><b>Specs</b>:" + list[i]['specification'] + "</li>" + 
                            "<li><b>Vendor</b>:" + list[i]['vendor'] + "</li>" + 
                        "</ul>" + 
                    "</li>"
                    );

        }

    }
}//}}}
