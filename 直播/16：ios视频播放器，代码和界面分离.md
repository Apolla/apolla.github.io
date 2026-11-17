最近业余时间整理的一个ios播放器，界面采用storyboard,以前几乎都是用代码布局，但是用过一个项目storyboard后，就感觉storyboard很靠谱，团队合作版本控制的问题解决其实很简单，每个人一个storyboard就可以了。播放代码使用的是avplayer，最大的优化就是播放界面和播放代码完全分离。
```objectivec
-(void)createPlayer
{
 
    self.playBackView=[[AVPlayerDemoPlaybackView alloc] initWithFrame:viewBounds];
    [self.view addSubview:self.playBackView];
     
    self.playerManager=[[AVPlayerManager alloc] init];
    //设置url
    //self.playerManager.URL=[[NSBundle mainBundle] URLForResource:@"1" withExtension:@"mp4"];
    //self.playerManager.URL=[[NSBundle mainBundle] URLForResource:@"2" withExtension:@"mov"];
    self.playerManager.URL=[NSURL URLWithString:@"http://static.tripbe.com/videofiles/20121214/9533522808.f4v.mp4"];
    //设置播放界面
    self.playerManager.mPlaybackView=self.playBackView;
    //设置时间轴
    self.playerManager.scrubSlider=self.scrubSlider;
    //播放出错回调
    self.playerManager.failedBlock=^(NSError *error){
        if (error) {
            UIAlertView *alert=[[UIAlertView alloc] initWithTitle:[error description] message:[error debugDescription] delegate:nil cancelButtonTitle:@"OK" otherButtonTitles:nil, nil];
            [alert show];
        }
    };
    __weak ViewController *weakself=self;
    //播放状态改变
    self.playerManager.statusChangeBlock=^(BOOL isPlaying){
        weakself.playBtn.hidden=isPlaying;
        weakself.pauseBtn.hidden=!isPlaying;
    };
    //播放结束
    self.playerManager.playEndBlock=^(){
        NSLog(@"播放结束");
    };
    //准备好播放
    self.playerManager.readyToPlayBlock=^(){
        weakself.totalTimeLabel.text=[weakself convertTimetoString:weakself.playerManager.duration];
        weakself.playBtn.enabled=YES;
        weakself.pauseBtn.enabled=YES;
        [weakself.playerManager play];
    
         
    };
    //播放过程时间改变
    self.playerManager.timeChangedBlock=^(double time)
    {
        weakself.currentTimeLabel.text=[weakself convertTimetoString:time];
    };
    //声音发生改变
    self.playerManager.volumeChangedBlock=^(){
        weakself.volumeSlider.value=weakself.playerManager.volume;
    };
    //缓冲时间
    self.playerManager.bufferChangedBlock=^(double buffered){
        weakself.processBar.progress=buffered/weakself.playerManager.duration;
        weakself.speedLabel.text=[NSString stringWithFormat:@"%0.0fkb/s",weakself.playerManager.bufferSpeed];
    };
     
    //初始化完毕，准备播放
    [self.playerManager prepare];
    
     
}
```

![](7079fb0b5aa0fd2f62df621b955484f6.png)![](849f72386eee20a591896ac50806f308.png)

代码下载：http://pan.baidu.com/s/1eyVMm
