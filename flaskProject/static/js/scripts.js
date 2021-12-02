$(document).ready(function() {
    $(".owl-carousel").owlCarousel({
        autoplay: true,
        autoplayhoverpause: true,
        autoplaytimeout: 100,
        //items: 4,
        nav: true,
        loop: true,
        margin: 50,
        padding: 5,
        stagePdding: 5,
    });

    // Add new user and roles when creating events (create_editEvents.html)
    $("#add_row").on("click", function() {
        // Get max row id and set new id
        var newid = 0;
        $.each($("#tab_logic tr"), function() {
            if (parseInt($(this).data("id")) > newid) {
                newid = parseInt($(this).data("id"));
            }
        });
        newid++;
        
        var tr = $("<tr></tr>", {
            id: "addr"+newid,
            "data-id": newid
        });
        
        // loop through each td and create new elements with name of newid
        $.each($("#tab_logic tbody tr:nth(0) td"), function() {
            var td;
            var cur_td = $(this);
            
            var children = cur_td.children();
            
            // add new td and element if it has a name
            if ($(this).data("name") !== undefined) {
                td = $("<td></td>", {
                    "data-name": $(cur_td).data("name")
                });
                
                var c = $(cur_td).find($(children[0]).prop('tagName')).clone().val("");
                c.attr("name", $(cur_td).data("name") + newid);
                c.appendTo($(td));
                td.appendTo($(tr));
            } else {
                td = $("<td></td>", {
                    'text': $('#tab_logic tr').length
                }).appendTo($(tr));
            }
        });
        
        // add the new row
        $(tr).appendTo($('#tab_logic'));
        
        // delete row
        $(tr).find("td a.row-remove").on("click", function() {
            $(this).closest("tr").remove();
        });
    });

    var fixHelperModified = function(e, tr) {
        var $originals = tr.children();
        var $helper = tr.clone();
    
        $helper.children().each(function(index) {
            $(this).width($originals.eq(index).width())
        });
        
        return $helper;
    };
    $(".table-sortable tbody").sortable({
        helper: fixHelperModified      
    }).disableSelection();
    $(".table-sortable thead").disableSelection();
    $("#add_row").trigger("click");
});
