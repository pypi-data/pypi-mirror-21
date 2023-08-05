
var Harambe = {
    init: function() {

        // Lazy load images
        $("img.lazy").lazy({
            effect: "fadeIn",
            effectTime: 1000
        })

        // Oembed
        $("a.oembed").oembed(null, {
            includeHandle: false,
            maxWidth: "100%",
            maxHeight: "480",
        });

        $('.datetimepicker').datetimepicker({
                debug: true,
                icons: {
                    time: 'fa fa-clock-o',
                    date: 'fa fa-calendar',
                    up: 'fa fa-chevron-up',
                    down: 'fa fa-chevron-down',
                    previous: 'fa fa-chevron-left',
                    next: 'fa fa-chevron-right',
                    today: 'fa fa-screenshot',
                    clear: 'fa fa-trash',
                    close: 'fa fa-remove'                    
                }
        });

        // Share buttons
        $(".widget-share-buttons").each(function(){
            var el = $(this)
            el.jsSocials({
                url: el.data("url"),
                text: el.data("text"),
                showCount: el.data("show-count"),
                showLabel: el.data("show-label"),
                shares:el.data("buttons"),
                _getShareUrl: function() {
                    var url = jsSocials.Socials.prototype._getShareUrl.apply(this, arguments);
                    var width = 550;
                    var height = 420;
                    var winHeight = screen.height, winWidth = screen.width;
                    var left = Math.round((winWidth / 2) - (width / 2));
                    var top = (winHeight > height) ? Math.round((winHeight / 2) - (height / 2)) : 0;
                    var options = "scrollbars=yes,resizable=yes,toolbar=no,location=yes" + ",width=" + width + ",height=" + height + ",left=" + left + ",top=" + top;
                    return "javascript:window.open('" + url + "', 'Sharing', '"+ options +"')";
                }
            });

        })

        // form validator
        $.validate({
            modules : 'security'
        });

        this.Widget.parseWidgetModalContent();
        //this.Widget.parseWidgetPanelContent();

    }
}


$(function(){
    Harambe.init()
})