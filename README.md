# spider_demo
个人爬虫练习代码，一点点总结上传。

## wenshu的 js hook

可以找到加密参数发送请求前的位置，从而根据debugger位置，打断点找到加密入口。具体的加密在一点点进行中。

也可以根据这个不破解加密的具体方法。

1、通过 `js hook` 到 `XMLHttpRequest` 的请求，

![](http://img.andrewblog.cn/blog/20200422/jedajV4esIoj.png)

2、判断请求中是否有加密参数

3、取消请求

4、将获取到的加密参数以及 `cookie` 返回到爬虫程序

5、就可以实现抓取了

![](http://img.andrewblog.cn/blog/20200422/842rJD0eQNmt.png)

![](http://img.andrewblog.cn/blog/20200422/2mLI9OOeLucH.png)

还有一种思路是自己执行 `XMLHttpRequest` 发送请求，并执行拦截和取消。这种思路的话生成加密参数的速度应该是最快的。不过我不太清楚这种自己制造自己拦截具体是怎么操作的。如果有知道的，可以指点一下。谢谢！

加密的参数具体破解还在一步步解析中
