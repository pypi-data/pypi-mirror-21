/* JS */
$(document).on("click", ".kotti-alert-closer", function(){
    var $this = $(this);
    var alert_id = $this.attr("data-alert");
    var target = $this.attr("data-href");
    var cookies = Cookies.get('kotti-alerts');
    if(cookies == undefined || cookies == ''){
        Cookies.set("kotti-alerts", ""+alert_id);
    }else{
        Cookies.set("kotti-alerts", cookies+","+alert_id);
    }
    $.post(target);
});