---
title: "iOS利用多线程进行网络请求"
date: 2024-03-09T23:21:58+08:00
lastmod: 2024-03-09T23:21:58+08:00
draft: false
categories: ["一阅阅读"]
aliases:
  - "/posts/ios利用多线程进行网络请求/"
---

## 1.前言

这两天忙着对付Other-Other的问题，今天才抽空给APP新增了一个离线缓存的功能，由于我的APP是对书源进行转码格式化阅读，所以缓存这里是个很头疼的问题，稍不慎就会503.目前的方案就是动态切换UA和利用多线程 一章一章下 收到失败就等待一会再继续，目前测试没什么问题。

## 2.多线程缓存

```objc
+ (void)downloadChaptersContentWithBookModel:(TJBookModel *)bookModel chapterIds:(NSArray *)chapterIds progress:(void (^)(NSInteger progress)) progress complete:(nullable void (^)(BOOL, NSString * _Nonnull, NSArray * _Nullable))complete {
    if (TJIsEmptyObject(bookModel.bookId)) {
        !complete ?: complete(NO, @"未知书籍", nil);
    }
    if (chapterIds.count == 0) {
        !complete ?: complete(NO, @"未知章节", nil);
    }
    // 统计下载章节数量
    __block NSInteger downloadCount = 0;
    // 统计下载失败章节ID
    __block NSMutableArray *failureArray = [[NSMutableArray alloc] init];
    
    
    //创建串行队列
    dispatch_queue_t customQuue = dispatch_queue_create("cpm.apolla.download", DISPATCH_QUEUE_SERIAL);
     //创建信号量并初始化总量为1
    dispatch_semaphore_t semaphoreLock = dispatch_semaphore_create(0);
    //添加任务
    dispatch_async(customQuue, ^{


        for (NSString *chapterId in chapterIds) {
            if (TJIsEmptyObject(chapterId)) {
                downloadCount += 1;
                if (downloadCount == chapterIds.count) {
                    !complete ?: complete(YES, @"下载完成", failureArray);
                } else {
                    !progress ?: progress(downloadCount);
                }
                continue;
            }


                [self chapterWithBookModel:bookModel chapterId:chapterId success:^(TJChapterModel * _Nonnull chapter) {
                    downloadCount +=1;
                    !progress ?: progress(downloadCount);
                    //缓存成功就0.5s后继续缓存
                    dispatch_time_t timer = dispatch_time(DISPATCH_TIME_NOW, 0.5 * NSEC_PER_SEC);

                    dispatch_after(timer, dispatch_get_main_queue(), ^{

  //相当于解锁                      dispatch_semaphore_signal(semaphoreLock);

                    });


                } failure:^(NSString * _Nonnull tip) {
                    downloadCount+=1;
                    // 保存失败章节ID
                    [failureArray addObject:chapterId];
                    !progress ?: progress(downloadCount);
                    //缓存失败就5秒回再缓存
                    dispatch_time_t timer = dispatch_time(DISPATCH_TIME_NOW, 5 * NSEC_PER_SEC);

                    dispatch_after(timer, dispatch_get_main_queue(), ^{

    //解锁                    dispatch_semaphore_signal(semaphoreLock);

                    });
                }];
                //加锁
//使用 DISPATCH_TIME_FOREVER 要注意线程问题 可能会造成APP卡死，我这里是因为作为网络请求 肯定会有结果返回，所以问题不大
            dispatch_semaphore_wait(semaphoreLock, DISPATCH_TIME_FOREVER);

        }


        dispatch_async(dispatch_get_main_queue(), ^{
        complete(YES, @"下载完成", failureArray);
        });
    });
  
}
```

## 3.错误的使用

想抄代码的这段不用看，我最开始用GCDGroup作为管理的，但是不知道为啥会控制不住请求，有大神可以为小弟解读下不

```objc
+ (void)downloadChaptersContentWithBookModel:(TJBookModel *)bookModel chapterIds:(NSArray *)chapterIds progress:(void (^)(NSInteger progress)) progress complete:(nullable void (^)(BOOL, NSString * _Nonnull, NSArray * _Nullable))complete {
    if (TJIsEmptyObject(bookModel.bookId)) {
        !complete ?: complete(NO, @"未知书籍", nil);
    }
    if (chapterIds.count == 0) {
        !complete ?: complete(NO, @"未知章节", nil);
    }
    // 统计下载章节数量
    __block NSInteger downloadCount = 0;
    // 统计下载失败章节ID
    __block NSMutableArray *failureArray = [[NSMutableArray alloc] init];
    
    
    dispatch_group_t group =  dispatch_group_create();
    dispatch_queue_t queue = dispatch_queue_create("com.wumeng.network", DISPATCH_QUEUE_SERIAL);
    for (NSString *chapterId in chapterIds) {
        if (TJIsEmptyObject(chapterId)) {
            downloadCount += 1;
            if (downloadCount == chapterIds.count) {
                !complete ?: complete(YES, @"下载完成", failureArray);
            } else {
                !progress ?: progress(downloadCount);
            }
            continue;
        }
        dispatch_group_enter(group);
        dispatch_group_async(group,queue, ^{
            [self chapterWithBookModel:bookModel chapterId:chapterId success:^(TJChapterModel * _Nonnull chapter) {
                downloadCount +=1;
                dispatch_time_t timer = dispatch_time(DISPATCH_TIME_NOW, 0.5 * NSEC_PER_SEC);
                dispatch_after(timer, queue, ^{
                    !progress ?: progress(downloadCount);
                    dispatch_group_leave(group);

                });

            } failure:^(NSString * _Nonnull tip) {
                downloadCount+=1;
                // 保存失败章节ID
                [failureArray addObject:chapterId];
                dispatch_time_t timer = dispatch_time(DISPATCH_TIME_NOW, 5 * NSEC_PER_SEC);
                dispatch_after(timer, queue, ^{
                    !progress ?: progress(downloadCount);
                    dispatch_group_leave(group);

                });
            }];
        });
    }



    dispatch_group_notify(group, dispatch_get_main_queue(), ^{
        complete(YES, @"下载完成", failureArray);
    });

    
}
```

##4.动态切换UA

其实思路很简单，动态设置User-Agent

```objc
    NSArray *uas = @[
        @"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        @"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        @"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        @"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        @"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        @"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        @"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        @"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        @"Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        @"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        @"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        @"Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        @"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        @"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        @"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        @"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        @"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        @"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        @"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        @"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        @"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        @"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        @"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        @"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        @"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        @"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        @"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        @"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        @"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        @"Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        @"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        @"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        @"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        @"Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ];
    [self.manager.requestSerializer setValue:uas[(arc4random() % [uas count])] forHTTPHeaderField:@"User-Agent"];
```

> 附上APP地址： [一阅阅读](https://apps.apple.com/cn/app/%E4%B8%80%E9%98%85%E9%98%85%E8%AF%BB/id1573880428)有想看小说的小伙伴可以试下 支持换源 支持自定义书源


