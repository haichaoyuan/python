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

// 1. 长轮训 本地先请求
function requestInventory() {
    jQuery.getJSON('//localhost:8000/cart/status', {session: document.session},
        function(data, status, xhr) {
            // 5. 长轮训 客户端接受到响应，更新页面，重新建立连接
            $('#count').html(data['inventoryCount']);
            setTimeout(requestInventory, 100);
        }
    );
}