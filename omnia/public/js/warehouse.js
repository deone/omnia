function showItemBoxes(list)    {//{{{

    for (i=0; i<list.length; i++)   {
        $(".inner").append(
                "<div id='" + i + "' class='grid_4 omega itembox'>" + 
                    "<h6>" + list[i] + "</h6>" + 
                    "<ul></ul>" + 
                "</div>"
                );
    }

    $(".inner").append("<div class='clear-float'></div>");

}//}}}

function displayItems(list)  {//{{{
    for (i=0; i<list.length; i++)   {

        if (list[i][1] == "Computer Hardware")  {

            if (list[i][2] != 1)    {
                $("#0 ul").append(
                        "<li>" + 
                        "<a href='/lineitem/get_spec?name=" + list[i][0] + "'>" + 
                        list[i][0] + " (" + list[i][2] + ")</a>" + 
                        "<div id='spec" + i + "' class='spec'>dfhdfh</div>" + 
                        "</li>"
                        );
            } else  {
                $("#0 ul").append(
                        "<a href='/lineitem/get_spec?name='>" + 
                        "<li>" + list[i][0] + "</li>" + 
                        "</a>"
                        );
            }
        }

        if (list[i][1] == "Engineering Tool")  {
            if (list[i][2] != 1)    {
                $("#1 ul").append(
                        "<a href='/lineitem/get_spec?name=" + list[i][0] + "'>" + 
                        "<li>" + list[i][0] + " (" + list[i][2] + ")</li>" + 
                        "</a>"
                        );
            } else  {
                $("#1 ul").append(
                        "<a href='/lineitem/get_spec?name=" + list[i][0] + "'>" + 
                        "<li>" + list[i][0] + "</li>" + 
                        "</a>"
                        );
            }
        }

        if (list[i][1] == "Computer Software")  {
            if (list[i][2] != 1)    {
                $("#2 ul").append(
                        "<a href='/lineitem/get_spec?name=" + list[i][0] + "'>" + 
                        "<li>" + list[i][0] + " (" + list[i][2] + ")</li>" + 
                        "</a>"
                        );
            } else  {
                $("#2 ul").append(
                        "<a href='/lineitem/get_spec?name=" + list[i][0] + "'>" + 
                        "<li>" + list[i][0] + "</li>" + 
                        "</a>"
                        );
            }
        }

    }
}//}}}

function showSpec(list) {
}
