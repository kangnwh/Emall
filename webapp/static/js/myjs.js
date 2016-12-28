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


String.format = function() {
    if (arguments.length == 0)
        return null;
    var str = arguments[0];
    for ( var i = 1; i < arguments.length; i++) {
        var re = new RegExp('\\{' + (i - 1) + '\\}', 'gm');
        str = str.replace(re, arguments[i]);
    }
    return str;
};