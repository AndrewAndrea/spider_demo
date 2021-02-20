# spider_demo
个人爬虫练习代码，一点点总结上传。

* [spider\_demo](#spider_demo)
  * [一、wenshu的 js hook](#%E4%B8%80wenshu%E7%9A%84-js-hook)
  * [二、wenshu app 的逆向](#%E4%BA%8Cwenshu-app-%E7%9A%84%E9%80%86%E5%90%91)
  * [三、 FaceBook js破解](#%E4%B8%89-facebook-js%E7%A0%B4%E8%A7%A3)
  * [四、KuGouTop500](#%E5%9B%9Bkugoutop500)
  * [五、duapp\_unidbg 调用 so](#%E4%BA%94duapp_unidbg-%E8%B0%83%E7%94%A8-so)
  * [六、中华人民共和国行政区划（五级）：省级、地级、县级、乡级和村级。](#%E5%85%AD%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92%E4%BA%94%E7%BA%A7%E7%9C%81%E7%BA%A7%E5%9C%B0%E7%BA%A7%E5%8E%BF%E7%BA%A7%E4%B9%A1%E7%BA%A7%E5%92%8C%E6%9D%91%E7%BA%A7)
  * [七、qcc 请求频繁类似 ob 的 js 。以及登陆](#%E4%B8%83qcc-%E8%AF%B7%E6%B1%82%E9%A2%91%E7%B9%81%E7%B1%BB%E4%BC%BC-ob-%E7%9A%84-js-%E4%BB%A5%E5%8F%8A%E7%99%BB%E9%99%86)
  * [八、tb\_slide 滑动demo](#%E5%85%ABtb_slide-%E6%BB%91%E5%8A%A8demo)
  * [九、头条 \_signature、\_signature、 \_\_ac\_nonce、 \_\_ac\_signature参数](#%E4%B9%9D%E5%A4%B4%E6%9D%A1-_signature_signature-__ac_nonce-__ac_signature%E5%8F%82%E6%95%B0)
    * [cookie 中的 \_\_ac\_nonce \_\_ac\_signature](#cookie-%E4%B8%AD%E7%9A%84-__ac_nonce-__ac_signature)
  * [十、signature 更新 (2021-02-20)]

## 一、wenshu的 js hook

可以找到加密参数发送请求前的位置，从而根据debugger位置，打断点找到加密入口。具体的加密在一点点进行中。

也可以根据这个不破解加密的具体方法。

1、通过 `js hook` 到 `XMLHttpRequest` 的请求，

![](http://img.andrewblog.cn/blog/20200422/jedajV4esIoj.png)

2、判断请求中是否有加密参数

3、取消请求

4、将获取到的加密参数以及 `cookie` 返回到爬虫程序。返回通过谷歌插件的形式。

5、就可以实现抓取了

![](http://img.andrewblog.cn/blog/20200422/842rJD0eQNmt.png)

![](http://img.andrewblog.cn/blog/20200422/2mLI9OOeLucH.png)

还有一种思路是自己执行 `XMLHttpRequest` 发送请求，并执行拦截和取消。这种思路的话生成加密参数的速度应该是最快的。不过我不太清楚这种自己制造自己拦截具体是怎么操作的。如果有知道的，可以指点一下。谢谢！

增加抓取数据的处理逻辑，并将抓取的数据保存到 `mongodb` 数据库中。增加验证码手动处理。

需要修改优化的部分：

- 将详情处理与列表的处理分开，详情做多线程或者异步协程抓取。
- 增加 `redis` 处理，实现分布式增加去重抓取
- 增加代理 `ip` 池

加密的参数具体破解还在一步步解析中

## 二、wenshu app 的逆向

这个真的简单。而且网上到处都有。

## 三、 FaceBook js破解

## 四、KuGouTop500

## 五、duapp_unidbg 调用 so
 在大佬 [@zhaoboy9692](https://github.com/zhaoboy9692/dailyanalysis/tree/master/%E6%AF%92unidbg) 代码上做了简单的修改

## 六、中华人民共和国行政区划（五级）：省级、地级、县级、乡级和村级。
[关于更新全国统计用区划代码和城乡划分代码的公告](http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/index.html)

![](http://img.andrewblog.cn/blog/20200604/ucRNtuUyWRE6.png-shuiyin)

使用 `python` 重新实现了一下，代码比较简单，由于没有代理ip，没有进行多线程也没有异步还是挺慢的，而且会有频率限制。所以建议可以上代理ip，这样会非常快。也没有保存相关的 `code` ,我只需要名字，所以就只保存了名字。使用 `MySQL` 保存。

-----------------------------------------------------------------------------

这个数据太多了，又用 `scrapy-redis`重新实现了一遍。我只是单机跑，速度其实还不是很快。可以多部署几台去抓就快多了。五级的数据是在是多，四级的话会少很多。

AreaSpider 文件夹下的 area 文件夹。执行 `main.py` 就可以了。然后再 `redis`中 `push` 一条起始数据就 OK 了。

需要注意的问题就是一个电脑抓的太频繁就会出现一个频率太快，会禁止你的请求，可以等几秒后。还有一个就是会出现 `sojson.v5` 的 js,其实这个还原之后你会发现就是生成了 `cookie` 中的一个参数。可以选择破解 `sojson.v5` 也可以直接复制 `cookie` 控制一下请求的频率就可以。

保存的数据预览

|  id  | pid  |       name       | level |
| :--: | :--: | :--------------: | :---: |
|  1   |  0   |       中国       |   0   |
|  2   |  1   |      北京市      |   1   |
|  3   |  1   |      天津市      |   1   |
|  4   |  1   |      河北省      |   1   |
|  5   |  1   |      山西省      |   1   |
| ...  | ...  |       ...        |  ...  |
|  33  |  2   |      市辖区      |   2   |
|  34  |  33  |      东城区      |   3   |
|  35  |  34  |    东华门街道    |   4   |
|  36  |  35  | 多福巷社区居委会 |   5   |
| ...  | ...  |       ...        |  ...  |

大家可以直接下载 `sql` 文件。也可以直接修改代码重新自己抓取一份。sql 文件在 AreaSpider 目录下。总共数据有将近70万的数据。我对第五级的数据进行了处理，原本都是居委会等等，把居委会。。删除后保存的。

`area_spider.sql` 文件大小 `56.9MB` 

![](http://img.andrewblog.cn/blog/20200606/i8p5xxWRRy35.png-shuiyin)

![](http://img.andrewblog.cn/blog/20200606/wxfM9xOUk1f5.png-shuiyin)

## 七、qcc 请求频繁类似 ob 的 js 。以及登陆

如果账号够多，可以通过并发提高抓取速度，同时10个账号并发，账号触发请求频繁的风控时，更换账号。
qcc 请求频繁会直接返回一个 混淆 js, 这个 js 会生成一个新的 cookie的值，更新到cookie中。

`qcc_ob_js/qcc_cookie_parse_16.js` 已经做了处理，使用 AST做的处理，参考蔡老板的文章，该文件可以直接在 node环境下运行，使用 express 做服务。需要安装相关的库。

访问方式 ：http://127.0.0.1:3000/?arg1={arg1}

登陆就是个阿里的滑动，晚点放个 demo。特别简单，百度就有。

## 八、tb_slide 滑动demo

这些百度一下都能搜到，改个 $cdc , 加个 webdriver, 再加上处理轨迹就 OK 了，目前没有发现大的问题。轨迹必须加。在一个 selenium 打开的浏览器中，打开第二个标签页，可能会导致滑动失败。每次打开页面不关闭浏览器进行第二次登陆，可能也会导致失败。

demo可以直接运行。

## 九、头条 _signature、_signature、 __ac_nonce、 __ac_signature参数

接口中有参数 `_signature` 参数

![](http://img.andrewblog.cn/qiniu_PicGoimage-20201022115056889.png-shuiyin)



直接全局搜索这个参数，会在一个 `index-*.js` 中搜索到, 虽然 `captcha.js` 中也有，不过没用 

![](http://img.andrewblog.cn/qiniu_PicGoimage-20201022115344290.png-gg)

在文件中找到该字符串位置，打断点，调试。

![](http://img.andrewblog.cn/qiniu_PicGoimage-20201022115939303.png-gg)

继续下一步，调试会跳转到 `acrawler.js` 文件中. 

![](http://img.andrewblog.cn/qiniu_PicGoimage-20201022120219522.png-gg)

`acrawler.js` 文件

![](http://img.andrewblog.cn/qiniu_PicGoimage-20201022120847497.png-gg)



下一步直接将 js 文件拿出来， 执行。

![](http://img.andrewblog.cn/workqiniu/image-20201203165354610.png-gg)

1、简化 `js`, 删除一些没有用的东西

![](http://img.andrewblog.cn/workqiniu/image-20201203164718585.png-gg)

参数后改为空列表即可

2、`node` 中 `window` 为 `global`

![](http://img.andrewblog.cn/workqiniu/image-20201203165044166.png-gg)

定义

```js
var window = global;
```

继续执行，缺啥补啥（调试打印 `Z[S]`，就可以知道缺啥了 ）

![](http://img.andrewblog.cn/workqiniu/image-20201203165436808.png-gg)

<img src="http://img.andrewblog.cn/workqiniu/carbon (1).png-gg" style="zoom:50%;" />

```js
window.location = params.location;
window.navigator = params.navigator;
```

然后就可以出来短的了

![](http://img.andrewblog.cn/workqiniu/image-20201203171616949.png-gg)

- 有个问题加了下面的代码就会报错 

```js
window.byted_acrawler && window.byted_acrawler.init({
                aid: 24,
                dfp: !0
            });
```

![](http://img.andrewblog.cn/workqiniu/image-20201203171543843.png-gg)

注释掉就可以，不知道啥原因。

长的 `_signature` 需要加 `cookie`,把 `cookie` 放进去就 ok 了。放在主要加密函数的后面，放在前面没用。不生效

![](http://img.andrewblog.cn/workqiniu/image-20201203172028896.png-gg)

结果：

![](http://img.andrewblog.cn/workqiniu/image-20201203172133438.png-gg)

测试一下

![](http://img.andrewblog.cn/workqiniu/image-20201203173600786.png-gg)

请求 `api/pc/feed` 接口时，需要在前面加上 `toutiao` 进行加密。

### cookie 中的 __ac_nonce __ac_signature

直接请求详情，不携带 `cookie`, 会响应 cookie  ` __ac_nonce`

![image-20201203175421719](http://img.andrewblog.cn/workqiniu/image-20201203175421719.png-gg)

![](http://img.andrewblog.cn/workqiniu/image-20201203175755230.png-gg)

通过 ` __ac_nonce` 生成 `__ac_signature`

直接调用上面的方法即可

```js
function f2(__ac_nonce){
    ac_signature = window.byted_acrawler.sign("", __ac_nonce);
    return ac_signature
}
```

![](http://img.andrewblog.cn/workqiniu/image-20201203185022708.png-gg)

## 十、signature 更新 (2021-02-20)

现在加 `cookie` 生成出来的变短了，不是原来那个长长的了

![image-20210201150223602](http://img.andrewblog.cn/workqiniu/image-20210201150223602.png-gg)

按照原来的跑会出来这么个错误

![image-20210201150510043](http://img.andrewblog.cn/workqiniu/image-20210201150510043.png-gg)

原来整个代码还是可以用的，并且是可以抓取到数据到，就是需要频繁的更换 ip

关注我的公众号获取更新后的源码 Python爬虫scrapy

![python爬虫scrapy](https://img.andrewblog.cn/qrcode_for_gh_77d4a09b9801_258.jpg)
--------------------------------------------------------------------------------------------------------------------------------------

如果对你有用，欢迎 star
