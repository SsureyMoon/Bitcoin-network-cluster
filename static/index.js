(function() {
$('#input-btn').val("17z35xHz19KcdnxDGH9awSsqxSYSLeu35T");
    console.log('welcome to bitcoin network')
    $('#cluster-btn').hide()
    $.getScript("/static/plot.js", function(){
        $('#mySpinner').removeClass('spinner');
        console.log("get plot.js done.")
        $('#get-btn').submit(function(event){
            var btn_addr = $('#input-btn').val();
            $('#d3_selectable_force_directed_graph').html('<div align="center" id="d3_selectable_force_directed_graph"></div>');
            $('#mySpinner').addClass('spinner');
            $.ajax({
                type: "POST",
                url: "/get_btn",
                data: "btn_address="+btn_addr,
                success: function(data){
                        $('#mySpinner').removeClass('spinner');
                        selectableForceDirectedGraph(btn_addr, data)
                        $('#cluster-btn').show()
                    },
                error: function(XMLHttpRequest) {
                    console.log(XMLHttpRequest);
                    if(XMLHttpRequest.status !== 0){
                        alert("unexpected error");
                    } else {
                        alert("request time out: 20 sec.(the network is too big)\nplease try another address.");
                    }
                    $('#mySpinner').removeClass('spinner');
                }
            });
            return false;
        });

        $('#cluster-btn').on('click', function(){
            origin_addr = $('#origin').attr('address')
            console.log('origin_addr')
            console.log(origin_addr)
            $('#d3_selectable_force_directed_graph').html('<div align="center" id="d3_selectable_force_directed_graph"></div>');
            $('#mySpinner').addClass('spinner');
            $.ajax({
                type: "POST",
                url: "/get_cluster",
                data: "origin_addr="+origin_addr,
                success: function(data){
                        $('#mySpinner').removeClass('spinner');
                        selectableForceDirectedGraph(origin_addr, data)
                        $('#cluster-btn').show()
                    },
                error: function(XMLHttpRequest) {
                    $('#cluster-btn').hide()
                    console.log(XMLHttpRequest);
                    if(XMLHttpRequest.status !== 0){
                        alert("unexpected error");
                    } else {
                        alert("request time out: 20 sec.(the network is too big)\nplease try another address.");
                    }
                    $('#mySpinner').removeClass('spinner');
                }
            });
            return false;
        })
    });

})();