SegmentFault 兄弟 + 基友单位弹幕视频网 Bilibili（B 站）近日在 GitHub 网站上建立了开源工作组（BOSTF）（此处 1024 赞），用以分享与维护自己的开源项目，其中包括 DanmakuFlameMaster（燃烧吧！烈焰弹幕使）与 ijkplayer。前者是免费提供 Android 平台下应用弹幕集成的解决方案，而后者则提供 Android 和 iOS 双平台视频播放器的解决方案。

| ![image.png](4d8946751f0f4a23590399c9713e58c7.png)  | ![image.png](392f0b22ca3fa912f8574e9d1d0aea86.png) |
| --- | --- |


开始项目介绍之前，悄悄地放张照片，从左到右以次是 B 站站长 bishi、IDG 资本女神 Linda、SF.GG CEO Sunny


DanmakuFlameMaster
项目地址：[https://github.com/Bilibili/DanmakuFlameMaster](https://github.com/Bilibili/DanmakuFlameMaster)
![image.png](a5bc64ff84fecc877810212c0016dc3e.png)


DanmakuFlameMaster，android 上开源弹幕解析绘制引擎项目，实现的特性有：

   - 使用多种方式 ( View / SurfaceView / TextureView ) 实现高效绘制
   - B 站 xml 弹幕格式解析
   - 基础弹幕精确还原绘制
   - 支持 mode7 特殊弹幕
   - 多核机型优化，高效的预缓存机制
   - 支持多种显示效果选项实时切换
   - 实时弹幕显示支持
   - 换行弹幕支持/运动弹幕支持
   - 支持自定义字体
   - 支持多种弹幕参数设置
   - 支持多种方式的弹幕屏蔽

ijkplayer
项目地址：[https://github.com/Bilibili/ijkplayer](https://github.com/Bilibili/ijkplayer)
![image.png](984a7b85c1702f66bdc2f1f5d7e3aec9.png)


ijkplayer，基于 ffplay 的跨平台播放器，实现的特性有：

   - 移除 FFmpeg 中不常用的特性以减小体积。
   - 对一些在线视频播放的 BUG 修复
   - 支持安卓 API 9-22 和 iOS 5.1.1-8.3.X
   - 使用各种平台原生的渲染方式进行优化

作为国内首屈一指的弹幕视频网站，B 站的两个开源项目已经被多个 App 使用。其中美拍和斗鱼使用了 ijkplayer 项目，DanmakuFlameMaster 项目则被包括优酷土豆、开迅视频、MissEvan、echo 回声、斗鱼 TV、天天动听、被窝声次元、ACFUN 等 App 使用。
技术上，ijkplayer 实现了跨平台功能，支持 Android 和 iOS 双平台；API 易于集成；编译配置可裁剪，方便控制安装包大小；支持 硬件加速解码，更加省电。而DanmakuFlameMaster 架构清晰，简单易用，支持多种高效率绘制方式选择，支持多种自定义功能设置。
Bilibili，也被称为哔哩哔哩、B 站，是中国大陆一个动画、游戏相关的弹幕视频分享网站，因为其深厚的宅文化和实时评论功能，已经在 90 后中收到广泛的欢迎。据悉，B 站的程序员也多为 90 后。
