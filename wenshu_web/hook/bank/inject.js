
var code = function () {
//  function code() {
    window.request_url = "";
   var open = window.XMLHttpRequest.prototype.open;
    // __dyn  文书网HifJzoc9
    window.XMLHttpRequest.prototype.open = function open(method, url, async) {
        
        if (url.indexOf("HifJzoc9") > -1) {
            debugger;
            // 取消请求
            // window.XMLHttpRequest.abort();
            
           	
        }
    };
};
var script = document.createElement('script');
script.textContent = '(' + code + ')()';
(document.head || document.documentElement).appendChild(script);
script.parentNode.removeChild(script);
