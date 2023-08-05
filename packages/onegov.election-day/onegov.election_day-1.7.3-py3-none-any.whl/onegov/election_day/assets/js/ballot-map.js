(function($) {
    $(document).ready(function() {
        $('.ballot-map').each(function(ix, el) {
            var mapurl =  $(el).data('mapurl');
            var dataurl =  $(el).data('dataurl');
            $.ajax({ url: mapurl }).done(function(mapdata) {
                $.ajax({ url: dataurl }).done(function(data) {
                    var canton =  $(el).data('canton');
                    var yay = $(el).data('left-hand');
                    var nay = $(el).data('right-hand');
                    var map = ballotMap({
                        mapdata: mapdata,
                        data: data,
                        canton: canton,
                        interactive: true,
                        yay: yay,
                        nay: nay
                    })(el);

                    var embed_link = $(el).data('embed-link');
                    var embed_source = $(el).data('embed-source');
                    if (embed_link && embed_source) {
                        appendEmbedCode(el, 500, map.height(), embed_source, embed_link);
                    }
                });
            });
        });
    });
})(jQuery);
