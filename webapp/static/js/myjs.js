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

function checkNum(obj) {
     //检查是否是非数字值
     if (isNaN(obj.value)) {
         obj.value = "";
     }
     if (obj != null) {
         //检查小数点后是否对于两位
         if (obj.value.toString().split(".").length > 1 && obj.value.toString().split(".")[1].length > 2) {
             alert("小数点后多于两位！");
             obj.value = "";
         }
     }
 };