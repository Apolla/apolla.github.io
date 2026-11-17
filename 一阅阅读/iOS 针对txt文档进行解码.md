如我上一篇文章记录，我加了打开其他APPtxt文件的小功能，紧接着碰到新问题了，我在测试过程中发现用户上传的TXT编码格式很多不单单是utf-8和gb2312,针对TXT文档进行解码，我一共经历过两个阶段，如下

##1.通过循环 解码不为空就返回字符串

```objc
  NSArray *encodings = @[
        @(NSUTF8StringEncoding),
        @(0x80000632),
        @(0x80000631),
        @(kCFStringEncodingGB_2312_80),
        @(kCFStringEncodingHZ_GB_2312),
        @(kCFStringEncodingMacChineseSimp),
        @(kCFStringEncodingDOSChineseSimplif),
        @(kCFStringEncodingGB_18030_2000),
        @(NSUTF16StringEncoding),
        @(NSUTF16LittleEndianStringEncoding),
        @(NSUTF16BigEndianStringEncoding),
        @(NSUTF32StringEncoding),
        @(NSUTF32LittleEndianStringEncoding),
        @(NSUTF32BigEndianStringEncoding)
    ];

    NSString *result = nil;
    for (NSInteger i = 0; i < encodings.count; i++) {
        unsigned int encoding = [encodings[i] unsignedIntValue];
        NSError *error = nil;
        NSString *content = [NSString stringWithContentsOfFile:filePath encoding:CFStringConvertEncodingToNSStringEncoding(encoding) error:&error];
        if (!error && !TJIsEmptyObject(content)) {
            result = content;
            break;
        }
    }
    return result;
```

> 此版本对于代码会碰到 编码成功 但是会是乱码的情况。


##2.第二阶段 通过encodingOptions 进行处理

`stringEncodingForData: encodingOptions: convertedString: usedLossyConversion` 会自动挑选编码数组内合适的编码对字符串进行处理，目前尚未发现问题

```objc
    NSArray *encodings = @[
        @(NSUTF8StringEncoding),
        @(0x80000632),
        @(0x80000631),
        @(CFStringConvertEncodingToNSStringEncoding(kCFStringEncodingGB_2312_80)),
        @(CFStringConvertEncodingToNSStringEncoding(kCFStringEncodingHZ_GB_2312)),
        @(CFStringConvertEncodingToNSStringEncoding(kCFStringEncodingMacChineseSimp)),
        @(CFStringConvertEncodingToNSStringEncoding(kCFStringEncodingDOSChineseSimplif)),
        @(CFStringConvertEncodingToNSStringEncoding(kCFStringEncodingGB_18030_2000)),
        @(NSUTF16StringEncoding),
        @(NSUTF16LittleEndianStringEncoding),
        @(NSUTF16BigEndianStringEncoding),
        @(NSUTF32StringEncoding),
        @(NSUTF32LittleEndianStringEncoding),
        @(NSUTF32BigEndianStringEncoding)
    ];
   
         NSData * data = [NSData dataWithContentsOfFile:filePath];
         NSString * chapterContent = @"";
         BOOL lossy = NO;
          [NSString stringEncodingForData:data
         encodingOptions:@{NSStringEncodingDetectionSuggestedEncodingsKey:encodings}
         convertedString:&chapterContent  usedLossyConversion:&lossy];
 
    return chapterContent;
```

> 附上APP地址： [一阅阅读](https://apps.apple.com/cn/app/%E4%B8%80%E9%98%85%E9%98%85%E8%AF%BB/id1573880428)

有想看小说的小伙伴可以试下 支持换源 支持自定义书源

