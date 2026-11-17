- 解读：[X264和H264 是什么？](http://blog.sina.com.cn/s/blog_4ad042e50100ijcq.html)
- 解读：[rtmp和http方式在播放flv方面的各自优势和劣势](http://bbs.9ria.com/thread-110484-1-1.html)
- 解读：[I,P，B帧和PTS，DTS的关系](http://www.cnblogs.com/qingquan/archive/2011/07/27/2118967.html)
- 解读：[移动直播技术秒开优化经验(超级重要，必读！)](http://weibo.com/ttarticle/p/show?id=2309403969318634263193)
- 解读：[iOS8系统H264视频硬件编解码说明](http://www.jianshu.com/p/b78db64acd77)
- [download x264](http://www.videolan.org/developers/x264.html)
- 解读：[FFmpeg发送流媒体的命令（UDP，RTP，RTMP）](http://blog.csdn.net/leixiaohua1020/article/details/38283297)
- 解读：[FFmpeg官网](http://blog.csdn.net/leixiaohua1020/article/details/38283297)
- 解读：[FFMPEG视音频编解码零基础学习方法（最权威推荐阅读）](http://blog.csdn.net/leixiaohua1020/article/details/15811977/)
- [download x264](http://www.videolan.org/developers/x264.html)
- GitHub -> [jgh-](https://github.com/jgh-)/[VideoCore](https://github.com/jgh-/VideoCore)**GitHub -> [runner365](https://github.com/runner365)/[LiveVideoCoreSDK](https://github.com/runner365/LiveVideoCoreSDK)
- 解读：[HTTP Live       Streaming直播(iOS直播)技术分析与实现](http://www.cnblogs.com/haibindev/archive/2013/01/30/2880764.html)
GitHub -> [LaiFengiOS](https://github.com/LaiFengiOS)/[LFLiveKit](https://github.com/LaiFengiOS/LFLiveKit)**GitHub -> [BradLarson](https://github.com/BradLarson)/[GPUImage](https://github.com/BradLarson/GPUImage)**GitHub -> [BeautifyFaceDemo](https://github.com/Guikunzhi/BeautifyFaceDemo)
- 解读：[iOS实时美颜滤镜是怎样炼成的](http://www.open-open.com/lib/view/open1463108934371.html)
GitHub -> [Bilibili](https://github.com/Bilibili)/[ijkplayer](https://github.com/Bilibili/ijkplayer)

一般做rtmp编程的时候，需要用到rtmp视频源地址，通常可以自己搭建Red5等服务器到自己的机器配置好后，编写客户端，但是这样有点麻烦；

为了方便，可以直接用电视台的rtmp直播地址：
:::info
rtmp://live.hkstv.hk.lxdns.com/live/hks    测试可用；
rtmp://www.planeta-online.tv:1936/live/channel_4

香港卫视 rtmp://live.hkstv.hk.lxdns.com/live/hks
香港卫视 [http://live.hkstv.hk.lxdns.com/live/hks/playlist.m3u8](http://live.hkstv.hk.lxdns.com/live/hks/playlist.m3u8)
香港卫视 [http://124.160.184.137:80/live/5](http://124.160.184.137:80/live/5) ... a46720.m3u8?type=tv

香港卫视精品台 [http://221.120.177.59/hls/i3d7ragr.m3u8](http://221.120.177.59/hls/i3d7ragr.m3u8)
香港卫视精品台 rtmp://221.120.177.59/livestream/ucagm8kk  

香港9DTV  mmsh://media.9dtv.com.hk:8088/9DTVBroadCast           
酷六V音乐 [http://main.gslb.ku6.com/broadcast/sub?channel=910](http://main.gslb.ku6.com/broadcast/sub?channel=910)
东森新闻   rtsp://adelivery_s.emome.net:554 ... ;at=1&mc=d2d58c
东森新闻亚洲 rtsp://adelivery_s.emome.net:554 ... ;at=1&mc=d2d58c

东森幼儿  [http://119.147.242.8:14207](http://119.147.242.8:14207)            
华娱卫视  rtsp://116.199.127.68/huayu

阳光卫视  [http://wzfree.10043.doftp.com/tvtest/182tv.php/live/id/suntv.m3u8](http://wzfree.10043.doftp.com/tvtest/182tv.php/live/id/suntv.m3u8)
[http://proxy.myvst.net/live/7167](http://proxy.myvst.net/live/7167) ... 53565151E76D4F.m3u8


本港卫视   rtsp://116.199.127.68/bengang
本港卫视   [http://119.147.242.7:14075](http://119.147.242.7:14075)
本港卫视   rtsp://3ptv.cietv.com/bengang
本港台     [http://v.hrtv8.com/vip.hrtv8.com/stream/2506.m3u8](http://v.hrtv8.com/vip.hrtv8.com/stream/2506.m3u8)

本港亚洲台 [http://119.147.242.7:14083](http://119.147.242.7:14083)

本港国际台 [http://119.147.242.7:14082](http://119.147.242.7:14082)

健康生活台 [http://wzfree.10043.doftp.com/tvtest/182tv.php/live/id/hlc.m3u8](http://wzfree.10043.doftp.com/tvtest/182tv.php/live/id/hlc.m3u8)

TVB  [http://rtsp.vdowowza.tvb.com:193](http://rtsp.vdowowza.tvb.com:193) ... ream/chunklist.m3u8
TVB8 [http://202.102.79.114:554/live/tvb8.stream/playlist.m3u8](http://202.102.79.114:554/live/tvb8.stream/playlist.m3u8)
TVB8 [http://122.192.35.76:554/live/tvb8.stream/playlist.m3u8](http://122.192.35.76:554/live/tvb8.stream/playlist.m3u8)
TVB 互动新闻台  [http://119.147.242.7:14078](http://119.147.242.7:14078)
TVB 互动新闻台  [http://rtsp.vdowowza.tvb.com/tvb](http://rtsp.vdowowza.tvb.com/tvb) ... ream/chunklist.m3u8
TVB 互动新闻台  [http://rtsp.vdowowza.tvb.com:193](http://rtsp.vdowowza.tvb.com:193) ... ream/chunklist.m3u8
TVB 互动新闻台  [http://rtsp.vdowowza.tvb.com:554](http://rtsp.vdowowza.tvb.com:554) ... ream/chunklist.m3u8
TVB 互动新闻台  [http://rtsp.vdowowza.tvb.com:554](http://rtsp.vdowowza.tvb.com:554) ... ream/chunklist.m3u8
TVB 互动新闻台  [http://rtsp.vdowowza.tvb.com:554](http://rtsp.vdowowza.tvb.com:554) ... ream/chunklist.m3u8
TVB 互动新闻台  rtsp://rtsp.vdowowza.tvb.com/tvblive/mobile_inews_200.stream
TVB 翡翠台  [http://119.147.242.7:14076](http://119.147.242.7:14076)
TVB 翡翠台  mmsh://222.84.226.99:88/333


高清翡翠台  [http://119.147.242.7:14119](http://119.147.242.7:14119)
高清翡翠台  [http://119.147.242.7:14120](http://119.147.242.7:14120)
高清翡翠台  [http://119.147.242.7:14164](http://119.147.242.7:14164)
高清翡翠台  [http://119.147.242.7:14076](http://119.147.242.7:14076)
翡翠台2     [http://119.147.242.7:14076](http://119.147.242.7:14076)
翡翠台-珍藏  mmsh://222.84.226.99:88/333
翡翠台-珍藏  [http://119.147.242.7:14076](http://119.147.242.7:14076)

互动新闻台1  rtsp://rtsp.vdowowza.tvb.com/tvblive/mobile_inews_200.stream
互动新闻台1  [http://rtsp.vdowowza.tvb.com:554](http://rtsp.vdowowza.tvb.com:554) ... ream/chunklist.m3u8
互动新闻台1  [http://rtsp.vdowowza.tvb.com:554](http://rtsp.vdowowza.tvb.com:554) ... ream/chunklist.m3u8
互动新闻台2  [http://rtsp.vdowowza.tvb.com:193](http://rtsp.vdowowza.tvb.com:193) ... ream/chunklist.m3u8
互动新闻台2  [http://rtsp.vdowowza.tvb.com/tvb](http://rtsp.vdowowza.tvb.com/tvb) ... ream/chunklist.m3u8
互动新闻台2  [http://rtsp.vdowowza.tvb.com:554](http://rtsp.vdowowza.tvb.com:554) ... ream/chunklist.m3u8
互动新闻台2  [http://rtsp.vdowowza.tvb.com:554](http://rtsp.vdowowza.tvb.com:554) ... ream/chunklist.m3u8
互动新闻台2  [http://rtsp.vdowowza.tvb.com:554](http://rtsp.vdowowza.tvb.com:554) ... ream/chunklist.m3u8


TVB明珠台    [http://119.147.242.7:14080](http://119.147.242.7:14080)

无线J2       [http://119.147.242.7:14079](http://119.147.242.7:14079)

新娱乐       [http://live-cdn.kksmg.com/channels/tvie/ylpd/flv:sd/live](http://live-cdn.kksmg.com/channels/tvie/ylpd/flv:sd/live)

龙翔时代     mms://mtv.smallsun.biz/m64
龙翔时代     rtsp://mtv.smallsun.biz/m3

卡通卫视    rtsp://adelivery_s.emome.net:554 ... ;at=1&mc=d2d58c

天映频道    rtmp://victorynet.tv:1935/live/mvcelesx01

台湾


TVBS    rtsp://211.79.36.213/tvbs_gphone.sdp
TVBS新闻台  rtsp://211.79.36.213/tvbsn_gphone.sdp
TVBS新闻台  rtsp://211.79.36.213:554/tvbsn_gphone.sdp
台视  rtsp://210.61.68.145/m50
台视  rtsp://adelivery_s.emome.net:554 ... ;at=1&mc=d2d58c
台视  [http://202.76.72.141:30080/Entry/8132?m3u8](http://202.76.72.141:30080/Entry/8132?m3u8)
台视  rtsp://211.79.36.213:554/ttv_gphone.sdp
星空卫视  [http://proxy.myvst.net/live/5335](http://proxy.myvst.net/live/5335) ... 942336E6A1763C7.flv
星空卫视  rtsp://stream13.gzcbn.tv:554/app_2/ls_7.stream


星空制作  [http://starry.mop.com/live/star.m3u8](http://starry.mop.com/live/star.m3u8)


凤凰卫视中文  rtsp://116.199.127.68/fenghuang
凤凰卫视中文  [http://ifenglive.soooner.com/?uu](http://ifenglive.soooner.com/?uu) ... E5DVSDNSOOONERCOM00
凤凰视频      [http://live.3gv.ifeng.com/live/zhongwen.m3u8](http://live.3gv.ifeng.com/live/zhongwen.m3u8)
凤凰视频      [http://live.3gv.ifeng.com/live/zhongwen.m3u8?fmt=x264_0k_mpegt](http://live.3gv.ifeng.com/live/zhongwen.m3u8?fmt=x264_0k_mpegt)
凤凰视频      [http://live.3gv.ifeng.com/live/z](http://live.3gv.ifeng.com/live/z) ... ts&size=320x240          
凤凰视频      rtsp://live.3gv.ifeng.com/live/2256
凤凰视频      [http://live.3gv.ifeng.com/live/hls/2500.m3u8](http://live.3gv.ifeng.com/live/hls/2500.m3u8)
凤凰视频      [http://live.3gv.ifeng.com/live/FHZXHD.m3u8](http://live.3gv.ifeng.com/live/FHZXHD.m3u8)             
凤凰资讯台    [http://live.3gv.ifeng.com/live/z](http://live.3gv.ifeng.com/live/z) ... ts&size=320x240
凤凰资讯台    [http://live.3gv.ifeng.com/live/hls/1500.m3u8](http://live.3gv.ifeng.com/live/hls/1500.m3u8)
凤凰资讯台    [http://lmyy.7drt.com/s/aa15.phps](http://lmyy.7drt.com/s/aa15.phps) ... .php?flvid=42100024
凤凰资讯台    [http://http://live.3gv.ifeng.com/live/zixun.m3u8?fmt=x264_0k_mpegts&size=320x240/s/aa15.php?s=234](http://http:/live.3gv.ifeng.com/live/zixun.m3u8?fmt=x264_0k_mpegts&size=320x240/s/aa15.php?s=234)
凤凰资讯台    [http://ims.veryhd.net/ty/fh_flv.php?flvid=42100024](http://ims.veryhd.net/ty/fh_flv.php?flvid=42100024) 
凤凰资讯高清  rtsp://live.3gv.ifeng.com/live/71
凤凰卫视香港台  [http://live.3gv.ifeng.com/live/hongkong.m3u8](http://live.3gv.ifeng.com/live/hongkong.m3u8)
凤凰卫视香港台  [http://119.147.242.7:14137](http://119.147.242.7:14137)
凤凰卫视香港台  [http://v.znds.com/a8c513fb0aff806867a4613ae509101ef](http://v.znds.com/a8c513fb0aff806867a4613ae509101ef)
凤凰卫视香港台  [http://proxy.myvst.net/live/5335](http://proxy.myvst.net/live/5335) ... 176333651BB5507.flv
凤凰卫视香港台  [http://live.3gv.ifeng.com/live/3128](http://live.3gv.ifeng.com/live/3128)
凤凰卫视宽屏   [http://itv.hdpfans.com/ty/fh_flv.php?flvid=42100011](http://itv.hdpfans.com/ty/fh_flv.php?flvid=42100011)

资讯卫视       [http://58.221.254.33:1935/live/zhongwen.sdp/playlist.m3u](http://58.221.254.33:1935/live/zhongwen.sdp/playlist.m3u)

SCN TV       [http://zb.v.qq.com:1863/?progid=2674956498&ostype=ios](http://zb.v.qq.com:1863/?progid=2674956498&ostype=ios)


@TV选美频道  [http://live121.cnlive.com:1935/live/shijiexiaojie/playlist.m3u8](http://live121.cnlive.com:1935/live/shijiexiaojie/playlist.m3u8)
@TV综艺频道  [http://live121.cnlive.com:1935/live/izongyi/playlist.m3u8](http://live121.cnlive.com:1935/live/izongyi/playlist.m3u8)
@tv写真频道  [http://live121.cnlive.com:1935/live/meixingxiezhen/playlist.m3u8](http://live121.cnlive.com:1935/live/meixingxiezhen/playlist.m3u8)
@TV娱乐频道  [http://live121.cnlive.com:1935/live/xuanhanyu/playlist.m3u8](http://live121.cnlive.com:1935/live/xuanhanyu/playlist.m3u8)
@TV卡通频道  [http://live121.cnlive.com:1935/live/eyule/playlist.m3u8](http://live121.cnlive.com:1935/live/eyule/playlist.m3u8)
@TV体育频道  [http://live121.cnlive.com:1935/live/chaotiyu/playlist.m3u8](http://live121.cnlive.com:1935/live/chaotiyu/playlist.m3u8)
@tv火星视频  [http://live121.cnlive.com:1935/live/huoxingshipin/playlist.m3u8](http://live121.cnlive.com:1935/live/huoxingshipin/playlist.m3u8)
@TV新闻频道  [http://live121.cnlive.com:1935/live/news/playlist.m3u8](http://live121.cnlive.com:1935/live/news/playlist.m3u8)
@TV美尚生活  [http://live121.cnlive.com:1935/l](http://live121.cnlive.com:1935/l) ... nghuo/playlist.m3u8
@TV动漫频道  [http://live121.cnlive.com:1935/live/dongman/playlist.m3u8](http://live121.cnlive.com:1935/live/dongman/playlist.m3u8)
@tv健康频道  [http://live121.cnlive.com:1935/live/meilizhongguo/playlist.m3u8](http://live121.cnlive.com:1935/live/meilizhongguo/playlist.m3u8)
@TV影视频道  [http://live121.cnlive.com:1935/live/xinyingshi/playlist.m3u8](http://live121.cnlive.com:1935/live/xinyingshi/playlist.m3u8)
@TV幸福频道  [http://live121.cnlive.com:1935/live/jidongpindao/playlist.m3u8](http://live121.cnlive.com:1935/live/jidongpindao/playlist.m3u8)


亚太卫视 rtmp://58.61.150.198/live/Livestream


东方电影 [http://112.117.210.8:80/live/5/4](http://112.117.210.8:80/live/5/4) ... bb534ec7d253cc0ed14


亚太第一卫视 rtmp://v1.one-tv.com/live/mpegts.stream


希望电视台 rtmp://203.69.85.37/livepkgr/hopestream1?adbe-live-event=hopetv


台湾TVBS新闻 rtsp://adelivery_s.emome.net:554 ... ;at=1&mc=d2d58c


GOOD TV 1  rtmp://l.jdjys.net/livefy/livestream
GOOD TV 1  rtsp://live.jdjys.net/tv1
GOOD TV 1  [http://210.59.248.53/hls-live/li](http://210.59.248.53/hls-live/li) ... ent/live-ch1-1.m3u8
GOOD TV 1  mms://122.226.102.202:1755/tv1


GOOD TV 2  rtmp://l.jdjys.net/livefy2/livestream
GOOD TV 2  rtsp://live.jdjys.net/tv2
GOOD TV 2  [http://210.59.248.53/hls-live/li](http://210.59.248.53/hls-live/li) ... ent/live-ch2-1.m3u8
GOOD TV 2  mms://122.226.102.202:1755/tv2


台湾民视   rtmp://202.39.43.80:80/live_hich/BC000121_1
台湾民视   [http://202.76.72.141:30080/Entry/8131?m3u8](http://202.76.72.141:30080/Entry/8131?m3u8)   
台湾民视   rtsp://adelivery_s.emome.net:554/ftv_gphone.sdp
:::


如果有测试可用的，可以添加到评论中；

| TVB8 ,[http://proxy.myvst.net/live/5335    ... 9424D42336E6A806E82](http://proxy.myvst.net/live/53357A52616B5A4D6279424D42336E6A806E82)
星空卫视 ,
华娱卫视, 
凤凰卫视中文台, [http://proxy.myvst.net/live/5335 ...    9426A42336E6A18AA44](http://proxy.myvst.net/live/53357A52616B5A4D6279426A42336E6A18AA44)
凤凰卫视咨询台, 
channel v ,
本港台, [rtsp://116.199.127.68/bengang/](http://bbs.wobo.tv/rtsp:/116.199.127.68/bengang/)
香港卫视, rtmp://live.hkstv.hk.lxdns.com/live/hks
卫视国际电影台 ,rtmp://202.117.80.19:1935/live/live2
卫视国际电影台 ,
卫视合家欢, 
卫视合家欢 ,
澳门莲花 ,[http://61.14.175.39/zerox/LOTUS/0-39.m3u8](http://61.14.175.39/zerox/LOTUS/0-39.m3u8)
澳亚卫视, rtmp://live.mastv.cc:1935/live/live1
澳视体育, 
澳视澳门 ,[http://live4.tdm.com.mo:1935/tv/ch1_H.live/playlist.m3u8](http://live4.tdm.com.mo:1935/tv/ch1_H.live/playlist.m3u8)
澳视生活, [http://live4.tdm.com.mo:1935/tv/ch5.live/playlist.m3u8](http://live4.tdm.com.mo:1935/tv/ch5.live/playlist.m3u8) |
| --- |


