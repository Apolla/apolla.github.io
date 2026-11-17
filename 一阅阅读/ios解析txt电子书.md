昨天上线新版本因为Other-Other账号审核被拒了，估计要等待几天了，正好抽时间把最近写的东西整理一下。

> 附上APP地址： [一阅阅读](https://apps.apple.com/cn/app/%E4%B8%80%E9%98%85%E9%98%85%E8%AF%BB/id1573880428)有想看小说的小伙伴可以试下 支持换源 支持自定义书源


言归正传，TXT电子书解析主要靠正则，筛选出文件内所有章节，并划分range，对于正则表达式的基础内容我不做过多描述，各位有兴趣可以去 [菜鸟教程正则表达式](https://www.runoob.com/regexp/regexp-syntax.html)自己去看下一下。

##正则

```
(\\s+?)([#☆、【0-9]{0,10})(第[0-9零一二两三四五六七八九十百千万壹贰叁肆伍陆柒捌玖拾佰仟\\s]{1,10}[章节回集卷])(.*)
```

## 用法

```objc

+ (void)parseLocalBookWithFilePath:(NSString *)filePath bookId:(NSString *)bookId success:(void (^)(NSArray<TJChapterModel *> * _Nonnull chapters))success failure:(TJFailureHandler)failure {
    if (!filePath) {
        !failure ?: failure([NSError errorWithDomain:NSCocoaErrorDomain code:-1 userInfo:@{NSUnderlyingErrorKey : @"文件路径为空"}]);
        return;
    }
    
    if (![filePath hasSuffix:@"txt"]) {
        !failure ?: failure([NSError errorWithDomain:NSCocoaErrorDomain code:-1 userInfo:@{NSUnderlyingErrorKey : @"文件格式不正确"}]);
        return;
    }
    
    NSString *content = [self contentWithFilePath:filePath];
    if (TJIsEmptyObject(content)) {
        !failure ?: failure([NSError errorWithDomain:NSCocoaErrorDomain code:-1 userInfo:@{NSUnderlyingErrorKey : @"书籍内容为空或者书籍格式错误"}]);
        return;
    }
    NSRegularExpression *expression = [NSRegularExpression regularExpressionWithPattern:kParseLocalBookPattern options:NSRegularExpressionCaseInsensitive error:nil];
    NSArray *matches = [expression matchesInString:content options:NSMatchingReportCompletion range:NSMakeRange(0, content.length)];
    NSMutableArray *chapters = [[NSMutableArray alloc] init];
    if (matches.count == 0) {
        // 全书分为一章
        TJChapterModel *chapter = [[TJChapterModel alloc] init];
        chapter.chapterId = [bookId stringByAppendingFormat: @"1000000"];
        chapter.chapterIndex = 1;
        chapter.chapterName = @"开始";
        chapter.content = content;
        [chapters addObject:chapter];
    } else {
        // 当前标题在全文中的位置
        NSRange currentRange = NSMakeRange(0, 0);
        // 当前章节编号
        NSInteger chapterIndex = 1;
        // 循环处理章节
        for (NSInteger i = 0; i < matches.count; i++) {
            @autoreleasepool {  // 自动释放池保证瞬时内存不会过高
                NSTextCheckingResult *result = matches[i];
                // 下一个标题在全文中的位置
                NSRange resultRange = result.range;
                // 截取两个标题之间内容为当前章节内容
                NSString *chapterContent = [content substringWithRange:NSMakeRange(currentRange.location + currentRange.length, resultRange.location - currentRange.location - currentRange.length)];
                if (!TJIsEmptyObject(chapterContent) && resultRange.length <= 70) {
                    // 章节内容不为空并且章节标题长度不超过70
                    TJChapterModel *chapterModel = [[TJChapterModel alloc] init];
                    chapterModel.chapterIndex = chapterIndex;
                    chapterModel.chapterId = [bookId stringByAppendingFormat: [NSString stringWithFormat:@"%@", @(1000000 + chapterIndex)]];
                    chapterModel.chapterName = (chapterIndex == 1) ? @"开始" : [[content substringWithRange:currentRange] stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]];
                    chapterModel.content = [self resetContent:chapterContent];
                    [chapters addObject:chapterModel];
                    chapterIndex += 1;
                    currentRange = resultRange;
                }
            };
        }
        NSString *endChapterContent = [content substringWithRange:NSMakeRange(currentRange.location + currentRange.length, content.length - currentRange.location - currentRange.length)];
        if (!TJIsEmptyObject(endChapterContent)) {
            // 最后一章
            TJChapterModel *endChapterModel = [[TJChapterModel alloc] init];
            endChapterModel.chapterIndex = chapterIndex;
            endChapterModel.chapterId = [bookId stringByAppendingFormat: [NSString stringWithFormat:@"%@", @(1000000 + chapterIndex)]];
            endChapterModel.chapterName = [[content substringWithRange:currentRange] stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]];
            endChapterModel.content = [self resetContent:endChapterContent];
            [chapters addObject:endChapterModel];
        }
    }
    if (chapters.count > 0 && success) {
        success(chapters);
    }
}

/// 处理章节内容
/// @param content 内容
+ (NSString *)resetContent:(NSString *)content {
    if (!content || content.length == 0) {
        return @"";
    }
    // 替换单换行
    content = [content stringByReplacingOccurrencesOfString:@"r" withString:@""];
    
    // 替换换行和多个换行（换行加空格）
    NSRegularExpression *regularExpression = [[NSRegularExpression alloc] initWithPattern:@"\\s*\\n+\\s*" options:NSRegularExpressionCaseInsensitive error:nil];
    content = [regularExpression stringByReplacingMatchesInString:content options:NSMatchingReportProgress range:NSMakeRange(0, content.length) withTemplate:@"\n　　"];
    
    // 去掉首尾空格和换行
    content = [content stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]];
    
    // 章节开头添加空格
    content = [@"　　" stringByAppendingString:content];
    
    return content;
}
```
