function cipher() {
	var date = new Date();
	var timestamp = date.getTime().toString();
	// var salt = $.WebSite.random(24);
	var year = date.getFullYear().toString();
	var month = (date.getMonth() + 1 < 10 ? "0" + (date.getMonth() + 1) : date
			.getMonth()).toString();
	var day = (date.getDate() < 10 ? "0" + date.getDate() : date.getDate())
			.toString();
	var iv = year + month + day;
	return iv
	// var enc = DES3.encrypt(timestamp, salt, iv).toString();
	// var str = salt + iv + enc;
	// var ciphertext = strTobinary(str);
	// return ciphertext;
}
function return_result(str_en){
    // var str = salt + iv + enc;
	var ciphertext = strTobinary(str_en);
	return ciphertext;
}

function strTobinary(str) {
	var result = [];
	var list = str.split("");
	for (var i = 0; i < list.length; i++) {
		if (i != 0) {
			result.push(" ");
		}
		var item = list[i];
		var binaryStr = item.charCodeAt().toString(2);
		result.push(binaryStr);
	};
	return result.join("");
}
