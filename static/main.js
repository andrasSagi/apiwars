function init() {

    $('#residentModal').on('show.bs.modal', function (event) {

        let modal = $(this);
        let button = $(event.relatedTarget);
        let planetName = button.data('planetname');
        let planetURL = button.data('whatever');

        $( ".residents" ).empty();

        $.getJSON(planetURL, function(response){

            let residents = response['residents'];
            modal.find('.modal-title').text('Residents of ' + planetName);

            for (let resident of residents) {
                $.getJSON(resident, function( data ) {
                    let items = [];
                    $.each( data, function( key, val ) {
                        items.push( "<td id='" + key + "'>" + val + "</td>" );
                    });
                    let properties = items.slice(0, 8);
                    $( "<tr/>", {
                        "class": "resident-row",
                        html: properties.join( "" )
                    }).appendTo($( ".residents" ));
                });
            }
        });
    });

    $('.vote-button').each(function () {
        let $this = $(this);
        $this.on("click", function () {
            let planetName = $(this).data('planet_name');
            let userName = $(this).data('username');
            alert('Your vote has been saved!');
            $.post("/vote", {'planetname': planetName, 'username': userName
            });
        });
    });

    $('#voteModal').on('show.bs.modal', function () {

        $( ".planetVoteTable" ).empty();

        $.getJSON('/vote-statistics', function(response){

            for (let voteData of response) {

                let statisticTable = [];
                statisticTable.push("<td>" + voteData['planet_name'] + "</td>");
                statisticTable.push("<td>" + voteData['count'] + "</td>");

            $("<tr/>", {
                "class": "votes-row",
                html: statisticTable.join("")
            }).appendTo($(".planetVoteTable"));
            }
        });
    });

}

init();