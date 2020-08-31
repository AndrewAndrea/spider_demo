const express = require('express')
const app = express()

function Base64() {

    _keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";

    this.encode = function (input) {
        var output = "";
        var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
        var i = 0;
        input = _utf8_encode(input);
        while (i < input.length) {
            chr1 = input.charCodeAt(i++);
            chr2 = input.charCodeAt(i++);
            chr3 = input.charCodeAt(i++);
            enc1 = chr1 >> 2;
            enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
            enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
            enc4 = chr3 & 63;
            if (isNaN(chr2)) {
                enc3 = enc4 = 64;
            } else if (isNaN(chr3)) {
                enc4 = 64;
            }
            output = output +
                _keyStr.charAt(enc1) + _keyStr.charAt(enc2) +
                _keyStr.charAt(enc3) + _keyStr.charAt(enc4);
        }
        return output;
    }

    this.decode = function (input) {
        var output = "";
        var chr1, chr2, chr3;
        var enc1, enc2, enc3, enc4;
        var i = 0;
        input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");
        while (i < input.length) {
            enc1 = _keyStr.indexOf(input.charAt(i++));
            enc2 = _keyStr.indexOf(input.charAt(i++));
            enc3 = _keyStr.indexOf(input.charAt(i++));
            enc4 = _keyStr.indexOf(input.charAt(i++));
            chr1 = (enc1 << 2) | (enc2 >> 4);
            chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
            chr3 = ((enc3 & 3) << 6) | enc4;
            output = output + String.fromCharCode(chr1);
            if (enc3 != 64) {
                output = output + String.fromCharCode(chr2);
            }
            if (enc4 != 64) {
                output = output + String.fromCharCode(chr3);
            }
        }
        //output = _utf8_decode(output);
        return output;
    }

    _utf8_encode = function (string) {
        string = string.replace(/\r\n/g,"\n");
        var utftext = "";
        for (var n = 0; n < string.length; n++) {
            var c = string.charCodeAt(n);
            if (c < 128) {
                utftext += String.fromCharCode(c);
            } else if((c > 127) && (c < 2048)) {
                utftext += String.fromCharCode((c >> 6) | 192);
                utftext += String.fromCharCode((c & 63) | 128);
            } else {
                utftext += String.fromCharCode((c >> 12) | 224);
                utftext += String.fromCharCode(((c >> 6) & 63) | 128);
                utftext += String.fromCharCode((c & 63) | 128);
            }

        }
        return utftext;
    }

    _utf8_decode = function (utftext) {
        var string = "";
        var i = 0;
        var c = c1 = c2 = 0;
        while ( i < utftext.length ) {
            c = utftext.charCodeAt(i);
            if (c < 128) {
                string += String.fromCharCode(c);
                i++;
            } else if((c > 191) && (c < 224)) {
                c2 = utftext.charCodeAt(i+1);
                string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
                i += 2;
            } else {
                c2 = utftext.charCodeAt(i+1);
                c3 = utftext.charCodeAt(i+2);
                string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
                i += 3;
            }
        }
        return string;
    }
}


var base64 = new Base64();
let atob = base64.decode;

var _0x4818 = ["csKHwqMI", "ZsKJwr8VeAsy", "UcKiN8O/wplwMA==", "JR8CTg==", "YsOnbSEQw7ozwqZKesKUw7kwX8ORIQ==", "w7oVS8OSwoPCl3jChMKhw6HDlsKXw4s/YsOG", "fwVmI1AtwplaY8Otw5cNfSgpw6M=", "OcONwrjCqsKxTGTChsOjEWE8PcOcJ8K6", "U8K5LcOtwpV0EMOkw47DrMOX", "HMO2woHCiMK9SlXClcOoC1k=", "asKIwqMDdgMuPsOKBMKcwrrCtkLDrMKBw64d", "wqImMT0tw6RNw5k=", "DMKcU0JmUwUv", "VjHDlMOHVcONX3fDicKJHQ==", "wqhBH8Knw4TDhSDDgMOdwrjCncOWwphhN8KCGcKqw6dHAU5+wrg2JcKaw4IEJcOcwrRJwoZ0wqF9YgAV", "dzd2w5bDm3jDpsK3wpY=", "w4PDgcKXwo3CkcKLwr5qwrY=", "wrJOTcOQWMOg", "wqTDvcOjw447wr4=", "w5XDqsKhMF1/", "wrAyHsOfwppc", "J3dVPcOxLg==", "wrdHw7p9Zw==", "w4rDo8KmNEw=", "IMKAUkBt", "w6bDrcKQwpVHwpNQwqU=", "d8OsWhAUw7YzwrU=", "wqnCksOeezrDhw==", "UsKnIMKWV8K/", "w4zDocK8NUZv", "c8OxZhAJw6skwqJj", "PcKIw4nCkkVb", "KHgodMO2VQ==", "wpsmwqvDnGFq", "wqLDt8Okw4c=", "w7w1w4PCpsO4wqA=", "wq9FRsOqWMOq", "byBhw7rDm34=", "LHg+S8OtTw==", "wqhOw715dsOH", "U8O7VsO0wqvDvcKuKsOqX8Kr", "Yittw5DDnWnDrA==", "YMKIwqUUfgIk", "aB7DlMODTQ==", "wpfDh8Orw6kk", "w7vCqMOrY8KAVk5OwpnCu8OaXsKZP3DClcKyw6HDrQ==", "wow+w6vDmHpsw7Rtwo98LC7CiG7CksORT8KlW8O5wr3Di8OTHsODeHjDmcKlJsKqVA==", "NwV+", "w7HDrcKtwpJawpZb", "wpQswqvDiHpuw6I=", "YMKUwqMJZQ==", "KH1VKcOqKsK1", "fQ5sFUkkwpI=", "wrvCrcOBR8Kk", "M3w0fQ==", "w6xXwqPDvMOFwo5d"];

(function (_0x4c97f0, _0x1742fd) {
    var _0x4db1c = function (_0x48181e) {
        while (--_0x48181e) {
            _0x4c97f0["push"](_0x4c97f0["shift"]());
        }
    };
    _0x4db1c(++_0x1742fd);
})(_0x4818, 347);

var _0x55f3 = function (_0x4c97f0, _0x1742fd) {
    var _0x4c97f0 = parseInt(_0x4c97f0, 16);

    var _0x48181e = _0x4818[_0x4c97f0];

    if (!_0x55f3["rc4"]) {
        var _0x232678 = function (_0x401af1, _0x532ac0) {
            var _0x45079a = [],
                _0x52d57c = 0,
                _0x105f59,
                _0x3fd789 = "",
                _0x4a2aed = "";

            _0x401af1 = atob(_0x401af1);

            for (var _0x124d17 = 0, _0x1b9115 = _0x401af1["length"]; _0x124d17 < _0x1b9115; _0x124d17++) {
                _0x4a2aed += "%" + ("00" + _0x401af1["charCodeAt"](_0x124d17)["toString"](16))["slice"](-2);
            }

            _0x401af1 = decodeURIComponent(_0x4a2aed);

            for (var _0x2d67ec = 0; _0x2d67ec < 256; _0x2d67ec++) {
                _0x45079a[_0x2d67ec] = _0x2d67ec;
            }

            for (_0x2d67ec = 0; _0x2d67ec < 256; _0x2d67ec++) {
                _0x52d57c = (_0x52d57c + _0x45079a[_0x2d67ec] + _0x532ac0["charCodeAt"](_0x2d67ec % _0x532ac0["length"])) % 256;
                _0x105f59 = _0x45079a[_0x2d67ec];
                _0x45079a[_0x2d67ec] = _0x45079a[_0x52d57c];
                _0x45079a[_0x52d57c] = _0x105f59;
            }

            _0x2d67ec = 0;
            _0x52d57c = 0;

            for (var _0x4e5ce2 = 0; _0x4e5ce2 < _0x401af1["length"]; _0x4e5ce2++) {
                _0x2d67ec = (_0x2d67ec + 1) % 256;
                _0x52d57c = (_0x52d57c + _0x45079a[_0x2d67ec]) % 256;
                _0x105f59 = _0x45079a[_0x2d67ec];
                _0x45079a[_0x2d67ec] = _0x45079a[_0x52d57c];
                _0x45079a[_0x52d57c] = _0x105f59;
                _0x3fd789 += String["fromCharCode"](_0x401af1["charCodeAt"](_0x4e5ce2) ^ _0x45079a[(_0x45079a[_0x2d67ec] + _0x45079a[_0x52d57c]) % 256]);
            }

            return _0x3fd789;
        };

        _0x55f3["rc4"] = _0x232678;
    }

    _0x48181e = _0x55f3["rc4"](_0x48181e, _0x1742fd);



    return _0x48181e;
};

var arg3 = null;
var arg4 = null;
var arg5 = null;
var arg6 = null;
var arg7 = null;
var arg8 = null;
var arg9 = null;
var arg10 = null;

String["prototype"]["hexXor"] = function (_0x4e08d8) {
    var _0x5a5d3b = "";

    for (var _0xe89588 = 0x0; _0xe89588 < this["length"] && _0xe89588 < _0x4e08d8["length"]; _0xe89588 += 0x2) {
        var _0x401af1 = parseInt(this["slice"](_0xe89588, _0xe89588 + 0x2), 0x10);

        var _0x105f59 = parseInt(_0x4e08d8["slice"](_0xe89588, _0xe89588 + 0x2), 0x10);

        var _0x189e2c = (_0x401af1 ^ _0x105f59)["toString"](0x10);

        if (_0x189e2c["length"] == 0x1) {
            _0x189e2c = "0" + _0x189e2c;
        }

        _0x5a5d3b += _0x189e2c;
    }

    return _0x5a5d3b;
};

String["prototype"]["unsbox"] = function () {
    var _0x4b082b = [0xf, 0x23, 0x1d, 0x18, 0x21, 0x10, 0x1, 0x26, 0xa, 0x9, 0x13, 0x1f, 0x28, 0x1b, 0x16, 0x17, 0x19, 0xd, 0x6, 0xb, 0x27, 0x12, 0x14, 0x8, 0xe, 0x15, 0x20, 0x1a, 0x2, 0x1e, 0x7, 0x4, 0x11, 0x5, 0x3, 0x1c, 0x22, 0x25, 0xc, 0x24];
    var _0x4da0dc = [];
    var _0x12605e = "";

    for (var _0x20a7bf = 0x0; _0x20a7bf < this["length"]; _0x20a7bf++) {
        var _0x385ee3 = this[_0x20a7bf];
        for (var _0x217721 = 0x0; _0x217721 < _0x4b082b["length"]; _0x217721++) {
            if (_0x4b082b[_0x217721] == _0x20a7bf + 0x1) {
                _0x4da0dc[_0x217721] = _0x385ee3;
            }
        }
    }

    _0x12605e = _0x4da0dc["join"]("");
    return _0x12605e;
};

function arg2_get(arg1) {
    var _0x5e8b26 = _0x55f3("0x3", "jS1Y");
    var _0x23a392 = arg1[_0x55f3("0x19", "Pg54")]();
    arg2 = _0x23a392[_0x55f3("0x1b", "z5O&")](_0x5e8b26);
    return arg2;
}


app.get('/', function (req, res) {
    let arg1 = req.query.arg1;
    let value = arg2_get(arg1);
    console.log("arg2: " + value)
    res.send(value);
})

app.listen(3000)
