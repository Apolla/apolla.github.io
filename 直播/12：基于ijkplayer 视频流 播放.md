**之前开始使用ijk进行了一些简单的播放器实现，不过因为项目需要，所以又重新花了一些时间完善了一个demo**
主要是对工具栏的逻辑进行了优化，顺便封装了一下，不过第一次做播放器，难免在一些地方有所疏漏，而且时间仓促，一些细节部分暂时还未完善。 
主要的一些文件：（参考ijk自带demo） 
![image.png](2e4035c9f7a7626982e53bafc0e4e915.png)

首先在工具栏部分主要是以下的一些东西 
包含了工具栏的自动消失以及工具栏上面的button的初始化（这部分还没有做autolayout，全屏后工具栏暂时未优化）
```objectivec
#import <UIKit/UIKit.h>

@protocol IJKMediaPlayback;

@interface PlayerViewControl : UIControl
@property (weak, nonatomic) id<IJKMediaPlayback> delegatePlayer;

@property (strong, nonatomic) UIButton* switchBut;
@property (strong, nonatomic) UISlider* slider;
@property (strong, nonatomic) UILabel * timer;
@property (strong, nonatomic) UIButton* danmakuBut;
@property (strong, nonatomic) UIButton* fullScreenBut;
@property (strong, nonatomic) UIButton* playBut;
@property (strong, nonatomic) UIView* overlay;
@property (strong, nonatomic) UIView* buttomlay;

@property (strong, nonatomic) UIActivityIndicatorView* indicator;
- (void)refreshPlayerContrl;
- (void)showNoFade;
- (void)showAndFade;
- (void)hide;

- (void)beginDragMediaSlider;
- (void)endDragMediaSlider;
- (void)continueDragMediaSlider;

@end
```


因为要像bilibili那样能过最小化播放，于是在之前的基础上进行了修改，把ijkplayer封装成了一个uiview类型，之前的demo里面是一个controller：主要实现的还是播放器加载，以及全屏、切换源等逻辑（那个滑动调节音量和亮度的需要真机测试。。。没试过行不行）
```objectivec
#import <UIKit/UIKit.h>
#import <Foundation/Foundation.h>
#import <IJKMediaFramework/IJKMediaFramework.h>
#import "PlayerViewControl.h"
@class PlayerViewControl;

@interface PlayerViewController : UIView
@property (atomic, strong) NSURL *url;
@property (atomic, retain) id <IJKMediaPlayback> player;
@property (strong, nonatomic) PlayerViewControl *playerControl;
@property (strong, nonatomic) UIView *playerView;

- (instancetype)initWithURL:(NSURL*)url withFrame:(CGRect)frame;

@end
```


另外，我把ijk必要notification部分分离了出来，方便维护和增加功能
```objectivec
#import "PlayerViewController.h"

@interface PlayerViewController (Notification)

- (void)setupNotification;

- (void)removeNotification;


@end
```


需要调用的时候就只需要：
```objectivec
PlayerViewController *vc = [[PlayerViewController alloc] initWithURL:[NSURL URLWithString:@"http://live.hkstv.hk.lxdns.com/live/hks/playlist.m3u8"] withFrame:CGRectMake(0, 64, self.view.frame.size.width, 200)];

[self.view addSubview:vc];
```

就可以了。当然，这只是简单的封装，更多需求自然要自己增加

详细的代码可以下载我的demo进行参考：
demo链接：[http://download.csdn.net/detail/atomic123/9414750](http://download.csdn.net/detail/atomic123/9414750)

