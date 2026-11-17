---
title: "5：推流发布和播放【RTMP】介绍"
date: 2024-03-10T09:47:41+08:00
lastmod: 2024-03-10T09:47:41+08:00
draft: false
categories: ["直播"]
aliases:
  - "/posts/5推流发布和播放rtmp介绍/"
---

准备工作（~表示安装目录）：
1、在~/applications下创建一个live文件夹`

2、在~/conf下创建一个live文件夹，并把conf目录下的Application.xml复制进去

3、编辑Application.xml：
（1）设置Streams/StreamType属性（live：仅直播；record：仅记录；live-record：既直播又记录）
<StreamType>live</StreamType>
注意：记录的视频保存在~/content目录下。
（2）设置HTTPStreamers属性：
<HTTPStreamers>cupertinostreaming,smoothstreaming,sanjosestreaming</HTTPStreamers>
（3）设置Streams/LiveStreamPacketizers属性：
<LiveStreamPacketizers>cupertinostreamingpacketizer, smoothstreamingpacketizer,                     sanjosestreamingpacketizer</LiveStreamPacketizers>
（4）设置RTP/Authentication/PlayMethod属性：
<PlayMethod>none</PlayMethod>

4、这一步只有采用RTSP/RTP编码时才需要做：编辑~/conf下的publish.password文件，添加一个用户名和密码来控制RTSP/RTP访问：
# Publish password file (format [username][space][password])
# username password
myuser mypassword

5、保存文件，重启服务器
推流：
1、基于rtmp，打开encoder，输入以下参数：
Server URL: rtmp://[wowza-address]/live
Stream Name: myStream.sdp
2、基于rtsp，参数如下：
Host Address: [wowza-address]:1935
Stream Name: live/myStream.sdp

播放流：
1、rtmp（用flash player播放），参数如下：
Server: rtmp://[wowza-address]/live
Stream: myStream.sdp
2、rtsp（用vlc或者QuickTime播放）
视频源：rtsp://[wowza-address]:1935/live/myStream.sdp

用rtmp协议推的流，也可以用rtsp协议播放。
介绍与架构图详细参见 [http://www.cuplayer.com/rtsp/](http://www.cuplayer.com/rtsp/)

RTSP视频监控WEB截图效果
![image.png](/images/4bcf18bf90beebb3ad033f7060a85eaf.png)

RTSP视频监控WEB截图效果
![image.png](/images/26eaf6ce67825f73444b4c07836ba8de.png)

基于极酷阳光播放器的调用：
<script type="text/javascript" src="/player/images/swfobject.js"></script>
<div class="video" id="CuPlayer"> <b> <img src="/player/images/loading.gif" /> 网页视频播放器加载中，请稍后...</b> </div>
<script type="text/javascript">
var so = new SWFObject("/player/player.swf","ply","980","460","9","#000000");
so.addParam("allowfullscreen","true");
so.addParam("allowscriptaccess","always");
so.addParam("wmode","opaque");
so.addParam("quality","high");
so.addParam("salign","lt");

<!-- HTML代码参数/Begin -->
so.addVariable("JcScpServer","rtmp://www.cuplauyer.com/vod"); //注意：wowza流媒体服务器地址
so.addVariable("JcScpVideoPath","mp4:test.mp4"); //wowza视频文件地址
so.addVariable("JcScpImg","/player/Images/start.jpg");
so.addVariable("JcScpFile","/player/CuSunV2Set.xml");
<!-- HTML代码参数/End -->
so.write("CuPlayer");
</script>

