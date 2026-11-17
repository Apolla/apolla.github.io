---
title: "8：FFmpeg在iOS上完美编译"
date: 2024-03-09T23:21:58+08:00
lastmod: 2024-03-09T23:21:58+08:00
draft: false
categories: ["直播"]
aliases:
  - "/posts/8ffmpeg在ios上完美编译/"
---

最近刚接触ffmpeg,找了很多相关的编译资料，都没有编译成功，前几天在 github上找到一个脚本（[https://github.com/kewlbear/FFmpeg-iOS-build-script](https://github.com/kewlbear/FFmpeg-iOS-build-script)），就可完美编译
**准备条件**

   - 先下载文件：[https://github.com/libav/gas-preprocessor](https://github.com/libav/gas-preprocessor)，
复制gas-preprocessor.pl到/usr/sbin下，
修改文件权限：chmod 777 /usr/local/bin/gas-preprocessor.pl
   - 安装yasm

**具体步骤如下：**
1. 下载脚本：[https://github.com/kewlbear/FFmpeg-iOS-build-script](https://github.com/kewlbear/FFmpeg-iOS-build-script)
2. 解压，找到文件 build-ffmpeg.sh
3. 执行服本文件：./build-ffmpeg.sh, 由于本人没有事先安装Yasm 执行脚本文件会出错，
如下：

| 1
2
3
4
5
6
7
8 | MAC:FFmpeg-iOS-build-script-master-2 jinsonglnan$ ./build-ffmpeg.sh 
Yasm not found
Homebrew not found. Trying to install...
Whoops, the Homebrew installer has moved! Please instead run:
ruby -e "$(curl -fsSL [https://raw.githubusercontent.com/Homebrew/install/master/install](https://raw.githubusercontent.com/Homebrew/install/master/install))"
Also, please ask wherever you got **this** link from to update it to the above.
Trying to install Yasm...
./build-ffmpeg.sh: line 67: brew: command not found |
| --- | --- |

意思就是说，没有yasm, 看到提示执行 ruby -e "$(curl -fsSL [https://raw.githubusercontent.com/Homebrew/install/master/install)"安装](https://raw.githubusercontent.com/Homebrew/install/master/install)%22安装)
4.编译完成后，终端进入FFmpeg-iOS-build-script目录，然后输入./build-ffmpeg.sh lipo，这个命令是讲.a文件合并成一个
5.把ffmpeg-iOS文件加入到工程中
6.添加一个头文件引用 #include "avformat.h"
添加一个api语句：av_register_all();给一个类文件.m后缀改为.mm，开启混编模式。
运行工程，如果没有报错，则表明编译成功
7.其他注意细节 
编译的时候报错： 'libavcodec/avcodec.h' file not found ，修改Header search paths 里的路径：$(PROJECT_DIR)/FFmpeg-iOS/include
加入External libraries：

| 1
2
3 | libz.dylib
libbz2.dylib
libiconv.dylib |
| --- | --- |

8.编译好，写了个demo：[点此下载](http://download.csdn.net/detail/baitxaps/8657935)

