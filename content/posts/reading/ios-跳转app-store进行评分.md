---
title: "iOS 跳转App Store进行评分"
date: 2024-03-09T23:21:58+08:00
lastmod: 2024-03-09T23:21:58+08:00
draft: false
categories: ["一阅阅读"]
aliases:
  - "/posts/ios-跳转app-store进行评分/"
---

## 1.前言

遭遇4.2.2把我逼得没办法了，啥功能都怼上去了

## 2.实现

在 viewdidload 或者 viewwillappear 中判断是否需要显示评分，因为SKStoreReviewController 一年最多三次，所以我就无耻点相隔四个月调用一次

```
    NSDate *oldTime =  [[NSUserDefaults standardUserDefaults]objectForKey:@"storeStarTime"];
    if (oldTime) {
        //利用NSCalendar比较日期的差异
        NSCalendar *calendar = [NSCalendar currentCalendar];
   
        NSCalendarUnit unit = NSCalendarUnitMonth;//只比较月数差异
        //比较的结果是NSDateComponents类对象
        NSDateComponents *delta = [calendar components:unit fromDate:oldTime toDate:[NSDate date] options:0];
        if (delta.month >= 4) {
            [self showStore];
        }
    }else{
        [[NSUserDefaults standardUserDefaults]setObject:[NSDate date] forKey:@"storeStarTime"];
    }
```

唤起评分页

```
-(void)showStore{
    if (@available(iOS 10.3, *)) {
        if([SKStoreReviewController respondsToSelector:@selector(requestReview)]) {// iOS 10.3 以上支持
        //防止键盘遮挡
        [[UIApplication sharedApplication].keyWindow endEditing:YES];
        [SKStoreReviewController requestReview];
        }else{
            NSString * nsStringToOpen = [NSString stringWithFormat: @"itms-apps://itunes.apple.com/app/id%@?action=write-review",@"1573880428"];//替换为对应的APPID
            [[UIApplication sharedApplication] openURL:[NSURL URLWithString:nsStringToOpen] options:@{} completionHandler:^(BOOL success) {
                
            }];
        }

    } else {
        NSString * nsStringToOpen = [NSString stringWithFormat: @"itms-apps://itunes.apple.com/app/id%@?action=write-review",@"1573880428"];//替换为对应的APPID
        [[UIApplication sharedApplication] openURL:[NSURL URLWithString:nsStringToOpen] options:@{} completionHandler:^(BOOL success) {
            
        }];
    }
    [[NSUserDefaults standardUserDefaults]setObject:[NSDate date] forKey:@"storeStarTime"];
}
```

> 附上APP地址： [一阅阅读](https://apps.apple.com/cn/app/%E4%B8%80%E9%98%85%E9%98%85%E8%AF%BB/id1573880428)有想看小说的小伙伴可以试下 支持换源 支持自定义书源


