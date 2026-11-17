---
title: "iOS 电脑WiFi传输文件到iphone"
date: 2024-03-09T23:21:58+08:00
lastmod: 2024-03-09T23:21:58+08:00
draft: false
categories: ["一阅阅读"]
---

##1.前言

这个功能早已开发好，但是博客为什么今天才更新，说起来一把鼻涕一把泪，我的小说APP更新提审遭遇了各种悲剧性的问题，关键词违规，内容被认为包含色情等待，就是那部 《我的绝色房东》审核人员打开的正好是这本，这半个月天天和审核人员勾心斗角，目前就剩下一个4.2.2 最低功能要求死活过不去，我明明是更新啊！！！

##2.准备

我采用的是 GCDWebUploader 这个第三库，所以项目中需要

```objc
//引入库
#import <GCDWebUploader.h>
//遵守代理
@interface TJUploadBookViewController ()<GCDWebUploaderDelegate>
```

##3.功能实现

```objc

//
//  TJUploadBookViewController.m
//  TJReader
//
//  Created by songming on 2020/12/19.
//  Copyright © 2020 song. All rights reserved.
//

#import "TJUploadBookViewController.h"

#import "TJReadParser.h"
#import "TJChapterDataManager.h"
#import "TJReadHelper.h"

#import "TJBookModel.h"
#import "TJChapterModel.h"

#import <GCDWebUploader.h>

@interface TJUploadBookViewController ()<GCDWebUploaderDelegate>

@property (nonatomic, strong) GCDWebUploader *uploader;
//显示ip地址
@property (nonatomic, strong) UILabel *ipLabel;
//复制ip地址按钮
@property (nonatomic, strong) UIButton *ipCopy;
//复制正则表达式地址 这个正则的作用是用于提供给用户自行判断书籍是否符合拆分规则
@property (nonatomic, strong) UIButton *patternCopy;
@end

@implementation TJUploadBookViewController

#pragma mark - Life cycle
- (void)viewDidLoad {
    [super viewDidLoad];
    
    self.title = @"WiFi传书";
    self.view.backgroundColor = TJReadBackgroundColor8;
    [self.view addSubview:self.ipLabel];
    [self.ipLabel mas_makeConstraints:^(MASConstraintMaker *make) {
        make.centerY.equalTo(self.view);
        make.leading.equalTo(self.view.mas_leading).mas_offset(30);
        make.trailing.equalTo(self.view.mas_trailing).mas_offset(-30);
    }];
    [self.view addSubview:self.ipCopy];
    [self.ipCopy mas_makeConstraints:^(MASConstraintMaker *make) {
        make.bottom.equalTo(self.view);
        make.leading.equalTo(self.view.mas_leading);
        make.size.mas_equalTo(CGSizeMake(self.view.frame.size.width / 2.0, 45));
    }];
    [self.view addSubview:self.patternCopy];
    [self.patternCopy mas_makeConstraints:^(MASConstraintMaker *make) {
        make.bottom.equalTo(self.view);
        make.trailing.equalTo(self.view.mas_trailing);
        make.size.mas_equalTo(CGSizeMake(self.view.frame.size.width / 2.0, 45));

    }];
}
///复制ip到剪切板
-(void)copyIp{
    UIPasteboard *pab = [UIPasteboard generalPasteboard];
    pab.string = self.uploader.serverURL.absoluteString;
    if (pab == nil) {
        [SVProgressHUD showInfoWithStatus:@"复制失败"];
    } else {
        [SVProgressHUD showInfoWithStatus:@"已复制"];
    }
}
///复制正则表达式到剪切板
-(void)copypattern{
    UIPasteboard *pab = [UIPasteboard generalPasteboard];
    pab.string = @"(\\s+?)([#☆、【0-9]{0,10})(第[0-9零一二两三四五六七八九十百千万壹贰叁肆伍陆柒捌玖拾佰仟\\s]{1,10}[章节回集卷])(.*)";
    if (pab == nil) {
        [SVProgressHUD showInfoWithStatus:@"复制失败"];
    } else {
        [SVProgressHUD showInfoWithStatus:@"已复制"];
    }
}


- (void)viewWillAppear:(BOOL)animated {
    [super viewWillAppear:animated];
    if ([self.uploader start]) {
        self.ipLabel.text = [NSString stringWithFormat:@"保证电脑和手机在同一网络下\n\n在电脑浏览器中访问以下地址：\n\n%@ \n\n章节划分正则如下 不匹配的整本书归为一章 \n \n(\\s+?)([#☆、【0-9]{0,10})(第[0-9零一二两三四五六七八九十百千万壹贰叁肆伍陆柒捌玖拾佰仟\\s]{1,10}[章节回集卷])(.*)", self.uploader.serverURL.absoluteString];
    } else {
        self.ipLabel.text = @"启动服务失败，请检查网络";
    }
}
- (void)viewDidDisappear:(BOOL)animated {
    [super viewDidDisappear:animated];
    if (self.uploader) {
        [self.uploader stop];
        self.uploader.delegate = nil;
        _uploader = nil;
    }
}

- (void)dealloc {
    
}

#pragma mark - GCDWebUploaderDelegate
- (void)webUploader:(GCDWebUploader *)uploader didUploadFileAtPath:(NSString *)path {
    // 上传完成解析书籍
    if (path) {
        NSString *bookId = [NSString stringWithFormat:@"%@", @([[NSDate date] timeIntervalSince1970] * 1000)];
        [TJReadParser parseLocalBookWithFilePath:path bookId:bookId  success:^(NSArray<TJChapterModel *> * _Nonnull chapters) {
            // 创建书籍模型
            TJBookModel *bookModel = [[TJBookModel alloc] init];
            bookModel.bookType = TJBookTypeLocal;
            bookModel.bookName = path.lastPathComponent;
            // 本地书随机生成ID
            bookModel.bookId = bookId;
            bookModel.chapterCount = chapters.count;
            for (TJChapterModel *chapter in chapters) {
                chapter.bookId = bookModel.bookId;
            }
            [TJReadHelper addToBookStackWithBook:bookModel complete:^{
                [TJChapterDataManager insertChaptersWithModels:chapters];
                [SVProgressHUD showSuccessWithStatus:@"书籍已经成功加入书架"];
            }];
        } failure:^(NSError *error) {
            [SVProgressHUD showErrorWithStatus:error.userInfo[NSUnderlyingErrorKey]];
        }];
    }
}

#pragma mark - Getters
- (GCDWebUploader *)uploader {
    if (!_uploader) {
        _uploader = [[GCDWebUploader alloc] initWithUploadDirectory:TJFilePath(@"books")];
        _uploader.allowedFileExtensions = @[@"txt"];
        _uploader.delegate = self;
    }
    return _uploader;
}
- (UILabel *)ipLabel {
    if (!_ipLabel) {
        _ipLabel = [[UILabel alloc] init];
        _ipLabel.textColor = TJReadTitleColor;
        _ipLabel.font = [UIFont boldSystemFontOfSize:16];
        _ipLabel.textAlignment = NSTextAlignmentCenter;
        _ipLabel.numberOfLines = 0;
    }
    return _ipLabel;
}

- (UIButton *)ipCopy {
    if (!_ipCopy) {
        _ipCopy = [UIButton buttonWithType:UIButtonTypeCustom];
        [_ipCopy setTitle:@"复制地址" forState:UIControlStateNormal];
        [_ipCopy setBackgroundColor:TJReadBackgroundColor_button];
        [_ipCopy setTitleColor:TJReadTitleColor forState:UIControlStateNormal];
        [_ipCopy addTarget:self action:@selector(copyIp) forControlEvents:UIControlEventTouchUpInside];
    }
    return _ipCopy;
}

- (UIButton *)patternCopy {
    if (!_patternCopy) {
        _patternCopy = [UIButton buttonWithType:UIButtonTypeCustom];
        [_patternCopy setTitle:@"复制正则" forState:UIControlStateNormal];
        [_patternCopy setBackgroundColor:TJReadBackgroundColor_button];
        [_patternCopy setTitleColor:TJReadTitleColor forState:UIControlStateNormal];
        [_patternCopy addTarget:self action:@selector(copypattern) forControlEvents:UIControlEventTouchUpInside];
    }
    return _patternCopy;
}

@end
```

```objc
///去重并且返回完整地址
#define TJDocumentDirectory NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES).lastObject
static inline NSString * TJFilePath(NSString *name) {
    if (!name) {
        return TJDocumentDirectory;
    }
    NSString *path = [TJDocumentDirectory stringByAppendingPathComponent:name];
    BOOL isDirectory;
    if (![[NSFileManager defaultManager] fileExistsAtPath:path isDirectory:&isDirectory]) {
        [[NSFileManager defaultManager] createDirectoryAtPath:path withIntermediateDirectories:YES attributes:nil error:nil];
    }
    return path;
}
```

