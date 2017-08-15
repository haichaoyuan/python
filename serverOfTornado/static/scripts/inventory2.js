$(document).ready(function() {
    document.session = $('#session').val();

    setTimeout(requestInventory, 100);

    $('#add-button').click(function(event) {
        jQuery.ajax({
            url: '//localhost:8000/cart',
            type: 'POST',
            data: {
                session: document.session,
                action: 'add'
            },
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                $(event.target).attr('disabled', 'disabled');
            },
            success: function(data, status) {
            },
            complete:function(XHR, TS){

            },
            error: function(data, status) {
                if(data.status == 200){
                    $('#remove-from-cart').show();
                }

            },
        });
    });

    $('#remove-button').click(function(event) {
        jQuery.ajax({
            url: '//localhost:8000/cart',
            type: 'POST',
            data: {
                session: document.session,
                action: 'remove'
            },
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                $(event.target).attr('disabled', 'disabled');
            },
            success: function(data, status, xhr) {
                $('#remove-from-cart').hide();
                    $(event.target).removeAttr('disabled');
            },
            error: function(data, status) {
                if(data.status == 200){
                    $('#remove-button').removeAttr('disabled');
                    $('#remove-from-cart').hide();
                    $('#add-button').removeAttr('disabled');
                }
            },
        });
    });
});

// 使用HTML5 WebSocket API取代长轮询资源的AJAX请求
//就像前面的例子一样，在购物者添加书籍到购物车时库存量会实时更新。
//不同之处在于一个持久的WebSocket连接取代了每次长轮询更新中重新打开的HTTP请求。
function requestInventory() {
    var host = 'ws://localhost:8000/cart/status';
    var websocket = new WebSocket(host);

    websocket.onopen = function(evt){};
    websocket.onmessage = function(evt){
        $('#count').html($.parseJSON(evt.data)['inventoryCount']);
    };
    websocket.onerror = function(evt){};
}