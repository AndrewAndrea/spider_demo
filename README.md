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

qcc 请求频繁会直接返回一个 混淆 js, 这个 js 会生成一个新的 cookie的值，更新到cookie中。

`qcc_ob_js/qcc_cookie_parse_16.js` 已经做了处理，使用 AST做的处理，参考蔡老板的文章，该文件可以直接在 node环境下运行，使用 express 做服务。需要安装相关的库。

访问方式 ：http://127.0.0.1:3000/?arg1={arg1}

登陆就是个阿里的滑动，晚点放个 demo。特别简单，百度就有。

## 八、tb_slide 滑动demo

这些百度一下都能搜到，改个 $cdc , 加个 webdriver, 再加上处理轨迹就 OK 了，目前没有发现大的问题。轨迹必须加。在一个 selenium 打开的浏览器中，打开第二个标签页，可能会导致滑动失败。每次打开页面不关闭浏览器进行第二次登陆，可能也会导致失败。

demo可以直接运行。

--------------------------------------------------------------------------------------------------------------------------------------

如果对你有用，欢迎 star
