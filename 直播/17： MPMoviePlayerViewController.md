MPMoviePlayerViewController 解释：视频播放器

iOS开发中播放音乐可以使用MPMusicPlayerController类来实现，播放视频可以使用MPMoviePlayerController和MPMoviePlayerViewController类来实现，MPMediaPickerController类可以用于从系统媒体库中选择媒体播放。这几个类都包含与MediaPlayer.framework框架中。

首先，将视频（video2.mov）导入到项目中，拖拽即可

## 1、导入头文件
```objectivec
#import <MediaPlayer/MediaPlayer.h>
```

## 2、设置Xlb,拖拽一个View，连接取名为movieView
```objectivec
@property (weak, nonatomic) IBOutlet UIView *movieView;
```


## 3、加载视频
```objectivec
NSString *videoPath = [[NSBundle mainBundle] pathForResource:@"video2" ofType:@"mov"];
```


## 4、初始化视频播放器
```objectivec
@interface ViewController ()
{
//视频
MPMoviePlayerViewController *_moviePlayerVC;
}
_moviePlayerVC = [[MPMoviePlayerViewController alloc] initWithContentURL:[NSURL fileURLWithPath:videoPath]];
```


## 5、设置视频播放器
```objectivec
//设置尺寸
[_moviePlayerVC.view setFrame:self.movieView.bounds];
//设置播放类型
[_moviePlayerVC.moviePlayer setControlStyle:MPMovieControlStyleFullscreen];
```


## 6、将播放器添加至View
```objectivec
[self.movieView addSubview:_moviePlayerVC.view];
```


## 7、播放视频
```objectivec
[_moviePlayerVC.moviePlayer play];
```


## 实现：

此时，当视频播放完成后，会暂停在View上。
可使用消息机制相应视频播放完成后的状态

//当视频播放完成后，由MPMoviePlayer内部发出，传递视频，我们只负责接收即可
```objectivec
[[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(movieFinish:) name:MPMoviePlayerPlaybackDidFinishNotification object:_moviePlayerVC.moviePlayer];


- (void)movieFinish:(NSNotification *)notification
{
MPMoviePlayerController *controller = notification.object;
//删除消息观察者
[[NSNotificationCenter defaultCenter] removeObserver:self name:MPMoviePlayerPlaybackDidFinishNotification object:controller];
[controller stop];//停止视频
_moviePlayerVC = nil;

}
```

