function initSwitch(s, stat, func) {
    var el = $(s).bootstrapSwitch();
    el.bootstrapSwitch('state', stat);
    if (func) {
        el.on('switchChange.bootstrapSwitch', func);
    }
    //el.on('switchChange.bootstrapSwitch', function (event, state) {
    //    if (state) {
    //        $('#remember_me').attr('checked', true);
    //    } else {
    //        $('#remember_me').removeAttr('checked');
    //    }
    //});
}