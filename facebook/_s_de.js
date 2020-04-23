var g, h = 36, i = 6, j = Math.pow(h, i);

function o() {
        var a = Math.floor(Math.random() * j);   // 随机数random.random()
        a = a.toString(h);
        return "0".repeat(i - a.length) + a
    }
    var p = null;
    function q() {
        p == null && (p = o());
        return p
    }

function getId() {
            var a, b, c = q();
            a = (a = s()) != null ? a : "";
            b = (b = t()) != null ? b : "";
            return a + ":" + b + ":" + c
        }

function r(a) {
        a === void 0 && (a = Date.now());
        var c = (g || (g = b("WebStorage"))).getLocalStorageForRead();
        if (c == null)
            return null;
        c = n(c.getItem("Session"));
        return c && a < c.expiryTime ? c : null
    }
    function s() {
        var a;
        return (a = r()) == null ? void 0 : a.id
    }


    function t() {
        __p && __p();
        var a = (g || (g = b("WebStorage"))).getSessionStorageForRead();
        if (a == null)
            return null;
        a = m(a.getItem("TabId"));
        if (a == null) {
            var c = (g || (g = b("WebStorage"))).getSessionStorage();
            if (c == null)
                return null;
            var d = o();
            c.setItem("TabId", d);
            return d
        }
        return a
    }


    function j(a, c, d) {
        if (d === "localStorage") {
            a = !1;
            try {
                a = test("946894")
            } catch (a) {}
            a && b("repairLocalStorage")()
        }
        Object.prototype.hasOwnProperty.call(h, d) || (h[d] = c(d));
        return h[d]
    }
    function test(a) {   // a=946894
        var h = {}
      , i = {};
        // var c = "AT4BjNm2xGxt1BO-";  //AT4BjNm2xGxt1BO-
        var c = {result: false, hash: "AT4BjNm2xGxt1BO-"};
        i[a] || (i[a] = !0,
        b("requireWeak")("Banzai", function(b) {
            return b.post("gk2_exposure", {
                identifier: a,
                hash: c.hash
            })
        }));
        return c.result
    }