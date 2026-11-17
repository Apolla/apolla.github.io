## 一、Apple Configurator 2

### 1.1 什么是Apple Configurator

[关于 Mac 上的 Apple Configurator 介绍](https://links.jianshu.com/go?to=https%3A%2F%2Fsupport.apple.com%2Fzh-cn%2Fguide%2Fapple-configurator-2%2Fcadf1802aed%2Fmac)

Apple Configurator 有很多功能，如：

- Domains 域名
- Global HTTP Proxy 全局 HTTP 代理
- DNS Proxy DNS 代理
- Content Filter 内容过滤
- Certificates 证书管理
....
- `Web Clips 网页快捷方式`，今天的重点

### 1.2、下载地址

前往 Mac App Store 下载该工具
[https://itunes.apple.com/cn/app/apple-configurator-2/id1037126344?mt=12](https://links.jianshu.com/go?to=https%3A%2F%2Fitunes.apple.com%2Fcn%2Fapp%2Fapple-configurator-2%2Fid1037126344%3Fmt%3D12)

### 1.3、界面布局

![](83fe72d43f460af2802cd0a6f21dcb9f.png)

### 1.4 创建描述文件

![](a0bd5df44b1e4fed050d96ca84972ff5.png)

image.png

### 1.5 填写描述文件

请参考如下内容填写您需要的内容，然后保存。

![](506fd11b0d417051290afc549c31522e.png)

分别解释一下每个选项的作用，如下：

- Label：显示在手机界面上的 APP 名称
- Identifier：描述文件的唯一标识， 用相同的 Identifier 安装会覆盖上一次
- Organization：公司和组织机构名称
- Description 和 Consent Message：都是安装时的一些介绍
- Security: 里有 3 个选项，分别是： 
   - Always 表示可以随便删除该描述文件
   - With Authorization 表示需要验证才能删除该描述文件
   - Never 表示流氓方式，用户不能删除描述文件（慎用！！！）
- Automatically Remove Profile：里也有 3 个选项：分别是： 
   - Never 永不删除
   - On date: 默认是 3 个月后自动删除
   - After Interval：默认 90 天后自动删除（除了设置天数外，还可设置小时）

## 二、Web Clips

### 2.1 什么是 Web Clips

用一句话来说就是：在 iPhone 桌面生成网页快捷方式图标，如果你的网页是`SPA（Single Page Web Application）`或是 `PWA（Progressive Web App）`用这技术，那真是爽的一批了，你的网站 PV 将会大幅提升。

![](6c1ffe3c2d15a6c9ff220a843ca6fbf8.png)

### 2.2 如何配置 Web Clips

可以参考如下图中所示来填写你的 Web Clips 配置项，最后记得保存，我的配置文件名为`Kenny锅.mobileconfig`。

![](4f8a7b8dcd77216f072c19867adb47f6.png)

分别解释一下每个选项的作用，如下：

- Label：显示在手机界面上的 APP 名称
- URL：打开 APP 后显示的网页地址
- Removable：APP 是否可以删除（强烈抵制 APP 不能删除的做法）
- Icon：APP 图标
- Precomposed Icon：如果你的APP 图标想根着网站 Icon 变化，`才需要`勾选
- Full Screen：是否全屏显示你的网页内容

### 2.3 调试

iPhone 连上 Mac 电脑后，手机上会弹出「信任」的弹框，选择「信任」。如果你的 iPhone 数据线没有问题的话（[需苹果 MFi 认证的数据线](https://links.jianshu.com/go?to=https%3A%2F%2Fbaike.baidu.com%2Fitem%2F%25E8%258B%25B9%25E6%259E%259CMFi%25E8%25AE%25A4%25E8%25AF%2581%2F751582%3Ffr%3Daladdin)），此时就会在 Apple Configurator 2 界面上看到你的手机，如图所示：

![](f5064ef451cf0fffa521f0d3cbdc3b91.png)

将`Kenny锅.mobileconfig`文件拖拽到Apple Configurator 2 界面上，会弹出如下界面：

![](9d0e37cd42da4d9510b5e7873edea7e0.png)

`先别点`「Stop」或 「Skip Profile」按钮，看看手机发生了什么？这时手机弹出让我们安装的界面，如下图所示（注意看签名者：`未签名`，后面我会告诉大家如何签名）：

![](b6ea96c8e7bfc91f3b87b4eef5f953c9.png)

在手机上点击`安装`，`下一步` 之类的操作，直到安装完成，就是出来如下图所示的描述文件。

![](b94a5ca7e2b6f4eeb694eab64887508c.png)

此时，回到 iPhone Home 界面，你会看到两个像 APP 一样的图标。

![](1a40f7cf01ce9ed30571e4e8e96079fc.png)

我们点一下 `Kenny锅盖`这个「APP」，打开了锅盖的百度百科，按手机 Home 键，这个图标怎么变了？

![](b3a2a931188ce0ef9c0230ca3b132c06.png)

对，我们在Web Clips 的配置里勾选了 `Precomposed Icon`。

### 2.4 配置文件（Kenny.mobileconfig）签名

执行如下命令：

> openssl req -x509 -newkey rsa:2048 -keyout my.pem -out signer.pem -days 3650 -nodes


会提示让我们填写签名的公司信息，可参考如下：

- Country Name (2 letter code) []:`CN`
- State or Province Name (full name) []:`Hubei`
- Locality Name (eg, city) []:`Wuhan`
- Organization Name (eg, company) []:`Kenny Group`
- Organizational Unit Name (eg, section) []:`Mobile Department`
- Common Name (eg, fully qualified host name) []:`192.168.1.5`
- Email Address []:`保密@gmail.com`

接下来，我们还需要执行一个命令（我已将`Kenny锅.mobileconfig`改为`Kenny.mobileconfig`）：

> openssl smime -sign -in Kenny.mobileconfig -out Kenny_signed.mobileconfig -signer signer.pem -inkey my.pem -outform der -nodetach


### 2.5 描述文件签名

打开 Apple Developer 后台，进入 [https://developer.apple.com/account/ios/certificate/distribution](https://links.jianshu.com/go?to=https%3A%2F%2Fdeveloper.apple.com%2Faccount%2Fios%2Fcertificate%2Fdistribution)

下载对应的 distribution.cer 文件，然后双击安装。

用 Apple Configurator 2 打开 Kenny.mobileconfig 描述配置文件，然后按如下配置：

![](9b71e968a79c85ab3ab92bfb812384e8.png)

选择刚刚下载的 distribution 证书，然后「Sign」完成描述文件签名，如下图所示：

![](7d6932af388085c6df73b1c549aaf6f5.png)

### 2.6 描述文件分发

描述文件分发就得部署到服务器上了，那我们就用 Node.js 来做吧。

创建一个 `web-clips-server.ts` 文件，将如下代码复制并保存，然后将 `Kenny_signed.mobileconfig` 文件放在同目录下。

```
const http = require('http');
const fs = require('fs');
const path = require('path');

const host = 'http://192.168.1.5';
const port = 3000;
const fileName = 'Kenny_signed.mobileconfig';

http.createServer((req, res) => {
  if(req.url === '/') {
    res.writeHead(200, {'Content-Type':'text/html; charset=utf-8'});
    const htmlChunk = `<html><body><h1><a href="/download">Kenny锅描述文件</a></h1></body></html>`;
    res.write(htmlChunk);
    res.end();
  } else if(req.url === '/download') {
    res.setHeader('Content-Disposition', 'attachment;filename=' + fileName);
    const filePath = path.resolve(__dirname, fileName);
    const fileStream = fs.createReadStream(filePath);
    fileStream.pipe(res);
  } else {
     res.end('Invalid Request!');
  }
}).listen(port);

console.log(`Server running at ${host}:${port}`);
```

在安装有 Node.js 的服务器上部署该文件， `注意：host 和 port 记得改成你需要的`，然后在 Terminal 里执行如下命令：

`node web-clips-server.ts`

让其它要下载的描述文件的用户访问地址，如：[http://192.168.1.5:3000/download](https://links.jianshu.com/go?to=http%3A%2F%2F192.168.1.5%3A3000%2Fdownload)

## 三、安装：

### 3.1 允许安装

![](531478d2959a60efde8b085d83943e56.png)

### 3.2 进行安装

![](641ac481f8e0d49a3c150bbd73ab0a2e.png)

### 3.3 完成安装

![](af9e8b78406bae76769f2c6275adbe3e.png)

## 四、总结

到此为止，我们完成了Web Clips 的配置基本信息、配置 Web Clips 信息、签名配置文件、配置描述文件、部署分发描述（自建Node.js 下载服务）等完整实战流程。

希望对大家有帮忙，让大家少走弯路！

参考文档：

- [https://www.jianshu.com/p/2ab0945823d8](https://www.jianshu.com/p/2ab0945823d8)


