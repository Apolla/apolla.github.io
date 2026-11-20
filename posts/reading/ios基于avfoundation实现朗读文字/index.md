# IOS基于AVFoundation实现朗读文字


##1.心理建设

众所周知AVFoundation的朗读是个智障语气，所以想不花钱就只能忍着。

##2.speechManager

```objc
@import AVFoundation;

@protocol TJSpeechManagerDelegate <NSObject>
@optional
- (void)didStartSpeechUtterance:(AVSpeechUtterance*)utterance;
- (void)didFinishSpeechUtterance:(AVSpeechUtterance*)utterance;
- (void)didPauseSpeechUtterance:(AVSpeechUtterance*)utterance;
- (void)didCancelSpeechUtterance:(AVSpeechUtterance*)utterance;
- (void)willSpeakRangeOfSpeechString:(NSRange)characterRange utterance:(AVSpeechUtterance *)utterance;

- (void)needRepeatSpeech:(AVSpeechUtterance *)utterance;
@end

@interface TJSpeechManager : NSObject <AVSpeechSynthesizerDelegate>


@property (nonatomic, strong) AVSpeechSynthesizer *avSpeech;
@property (nonatomic, strong) AVSpeechUtterance *speechUtt;

@property (nonatomic, assign) id <TJSpeechManagerDelegate> delegate;


- (void)setSpeechContent:(NSString *)content;


- (void)pauseSpeech;


- (void)beginSpeech;

- (void)continueSpeech;

- (void)endSpeech;

@end


#import "TJSpeechManager.h"

@implementation TJSpeechManager

- (void)setSpeechContent:(NSString *)content {
    AVSpeechUtterance *speechUtt = [AVSpeechUtterance speechUtteranceWithString:content];
    speechUtt.rate = 0.5;
    speechUtt.pitchMultiplier = 1;
            
    //设置音量,[0-1] 默认 = 1
    speechUtt.volume = 1;

    //读一段前的停顿时间
    speechUtt.preUtteranceDelay = 1;
    //读完一段后的停顿时间
    speechUtt.postUtteranceDelay = 1;
    AVSpeechSynthesisVoice *voice = [AVSpeechSynthesisVoice voiceWithLanguage:@"zh-CN"];
    speechUtt.voice = voice;
    self.speechUtt = speechUtt;
}

- (void)beginSpeech {
    //这里需要注意一下，一个avspeech对象只能播放一次，同一个对象中途不能重新播放。
    AVSpeechSynthesizer *avSpeech = [[AVSpeechSynthesizer alloc] init];
    avSpeech.delegate = self;
    [avSpeech speakUtterance:self.speechUtt];
    self.avSpeech = avSpeech;
}

- (void)pauseSpeech {
    [self.avSpeech pauseSpeakingAtBoundary:AVSpeechBoundaryImmediate];
}

- (void)continueSpeech {
    if(self.avSpeech.isPaused) {
        [self.avSpeech continueSpeaking];
        [NSThread sleepForTimeInterval:0.25f];
    }
}

- (void)endSpeech {
    if(self.avSpeech.isSpeaking) {
        [self.avSpeech stopSpeakingAtBoundary:AVSpeechBoundaryImmediate];
        [NSThread sleepForTimeInterval:0.25f];
    }
}

//代理主要是返回给controller，用来和UI交互
#pragma mark - AVSpeechSynthesizerDelegate;
- (void)speechSynthesizer:(AVSpeechSynthesizer*)synthesizer didStartSpeechUtterance:(AVSpeechUtterance*)utterance{
    NSLog(@"---开始播放");
    if(self.delegate && [self.delegate respondsToSelector:@selector(didStartSpeechUtterance:)]) {
        [self.delegate didStartSpeechUtterance:utterance];
    }
}

- (void)speechSynthesizer:(AVSpeechSynthesizer*)synthesizer didFinishSpeechUtterance:(AVSpeechUtterance*)utterance{
    NSLog(@"---完成播放");
    if(self.delegate && [self.delegate respondsToSelector:@selector(didFinishSpeechUtterance:)]) {
        [self.delegate didFinishSpeechUtterance:utterance];
    }
}

- (void)speechSynthesizer:(AVSpeechSynthesizer*)synthesizer didPauseSpeechUtterance:(AVSpeechUtterance*)utterance{
    NSLog(@"---播放中止");
    if(self.delegate && [self.delegate respondsToSelector:@selector(didPauseSpeechUtterance:)]) {
        [self.delegate didPauseSpeechUtterance:utterance];
    }
}

- (void)speechSynthesizer:(AVSpeechSynthesizer*)synthesizer didContinueSpeechUtterance:(AVSpeechUtterance*)utterance{
    NSLog(@"---恢复播放");
    
}

- (void)speechSynthesizer:(AVSpeechSynthesizer*)synthesizer didCancelSpeechUtterance:(AVSpeechUtterance*)utterance{
    NSLog(@"---播放取消");
    if(self.delegate && [self.delegate respondsToSelector:@selector(didCancelSpeechUtterance:)]) {
        [self.delegate didCancelSpeechUtterance:utterance];
    }
}

- (void)speechSynthesizer:(AVSpeechSynthesizer *)synthesizer willSpeakRangeOfSpeechString:(NSRange)characterRange utterance:(AVSpeechUtterance *)utterance {
    if(self.delegate && [self.delegate respondsToSelector:@selector(willSpeakRangeOfSpeechString:utterance:)]) {
        [self.delegate willSpeakRangeOfSpeechString:characterRange utterance:utterance];
    }
}

@end
```

##3.使用范例

```objc
//分页控制器获取到当前页内容
-(void)pageReadViewControllerSpeechContent:(NSString *)content
{
//先停止语音 防止用户翻页造成声音重叠
    [self.speechManager endSpeech];
    //当期是否开启了朗读功能
    if (self.isSpeechNextPage == YES ) {
    //内容不为空 代表可以朗读下一页
        if ( content && content.length > 0) {
        //设置朗读内容
            [self.speechManager setSpeechContent:content];
            //开始朗读
            [self.speechManager beginSpeech];
        }else{
            self.isSpeechNextPage = NO;
            [self.speechManager endSpeech];
        }
    }
}

///朗读按钮开启
-(void)readMenuDidOpenSpeechRead
{
    self.isSpeechNextPage = YES;
    //用于刷新当前页内容 从而调用pageReadViewControllerSpeechContent
    [self speechNextPage:self.book.page];
}
//用户关闭朗读
-(void)readMenuDidCloseSpeechRead
{
    [self.speechManager pauseSpeech];
    self.isSpeechNextPage = NO;
}
//当前页内容读完
- (void)didFinishSpeechUtterance:(AVSpeechUtterance *)utterance
{
    //我这里的逻辑是用于控制翻页还是下一章
        //下一章或者下一页都会重绘pageViewControl内容 从而继续响应 pageReadViewControllerSpeechContent 的回调代理
    if ([TJReadRecordManager recordWithBookId:self.book.bookId].page + 2 > [TJReadRecordManager recordWithBookId:self.book.bookId].chapter.pageModels.count) {

        [self readMenuDidChangeChapter:YES];
    }else{
        [self speechNextPage:[TJReadRecordManager recordWithBookId:self.book.bookId].page + 1];
    }
}
```

##4.简单使用

如果各位想简单应用一下

初始化 manager

```objc
-(TJSpeechManager *)speechManager
{
    if (!_speechManager) {
        _speechManager = [[TJSpeechManager alloc]init];
        _speechManager.delegate = self;
    }
    return _speechManager;
}
```

然后直接开始朗读就行了

```objc

      [self.speechManager setSpeechContent:@"想说的话"];
            //开始朗读
            [self.speechManager beginSpeech];
```

##5.退出

退出页面记得停止播放

```objc
-(void)dealloc
{
    self.speechManager.delegate = nil;
   
    [self.speechManager endSpeech];
}
```

> 附上APP地址： [一阅阅读](https://apps.apple.com/cn/app/%E4%B8%80%E9%98%85%E9%98%85%E8%AF%BB/id1573880428)有想看小说的小伙伴可以试下 支持换源 支持自定义书源




---

> 作者: 宋明  
> URL: https://apolla.cc/posts/reading/ios%E5%9F%BA%E4%BA%8Eavfoundation%E5%AE%9E%E7%8E%B0%E6%9C%97%E8%AF%BB%E6%96%87%E5%AD%97/  

