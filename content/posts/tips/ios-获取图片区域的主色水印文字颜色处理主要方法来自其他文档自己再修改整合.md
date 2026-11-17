---
title: "iOS 获取图片、区域的主色。水印文字颜色处理,主要方法来自其他文档，自己再修改整合"
date: 2024-03-09T23:21:58+08:00
lastmod: 2024-03-09T23:21:58+08:00
draft: false
categories: ["碎片芝士收藏"]
aliases:
  - "/posts/ios-获取图片区域的主色水印文字颜色处理主要方法来自其他文档自己再修改整合/"
---

```objectivec
//添加水印
+ (UIImage *)getWaterMarkWith:(UIImage *)image waterText:(NSString *)str{

    CGSize imageSize = image.size;
    CGFloat imageWidth = imageSize.width;
    CGFloat imageHeight = imageSize.height;

    UIGraphicsBeginImageContextWithOptions(imageSize, NO, 0);
    [image drawAtPoint:CGPointZero];
    CGFloat textFont = 10 * ceilf(imageWidth / [UIScreen mainScreen].bounds.size.width);
    CGSize perSize = [self getSize:imageWidth font:[UIFont systemFontOfSize:textFont] str:str lineSpace:0];
    CGRect rect = CGRectMake(ceilf(imageWidth - perSize.width - 20),
                             ceilf(imageHeight - perSize.height - 20),
                             ceilf(perSize.width + 10),
                             ceilf(perSize.height + 5));

    NSDictionary *colorInfo = [self mostColor:image scale:1 rect:rect];
    CGFloat red = [colorInfo[@"red"] floatValue];
    CGFloat green = [colorInfo[@"green"] floatValue];
    CGFloat blue = [colorInfo[@"blue"] floatValue];
    CGFloat alpha = [colorInfo[@"alpha"] floatValue];
    BOOL colorDark = [self isDarkColor:[UIColor colorWithRed:red green:green blue:blue alpha:alpha]];
    [str drawAtPoint:rect.origin withAttributes:@{NSFontAttributeName:[UIFont systemFontOfSize:textFont], NSForegroundColorAttributeName:colorDark ? [UIColor whiteColor] : [UIColor blackColor]}];
    image = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();

    return image;
}

// 获取图片、区域的主色
+ (NSDictionary *)mostColor:(UIImage *)image scale:(CGFloat)scale rect:(CGRect)rect{

    #if __IPHONE_OS_VERSION_MAX_ALLOWED > __IPHONE_6_1
    int bitmapInfo = kCGBitmapByteOrderDefault | kCGImageAlphaPremultipliedLast;
    #else
    int bitmapInfo = kCGImageAlphaPremultipliedLast;
    #endif
    if (scale <= 0.1) {
        scale = 0.1;
    }else if(scale >= 1){
        scale = 1;
    }

    if (rect.size.width > 0 && rect.size.height > 0) {
        image = [self cropSquareImage:image rect:rect];
    }

    //第一步 先把图片缩小 加快计算速度. 但越小结果误差可能越大
    CGSize thumbSize = CGSizeMake([image size].width * scale, [image size].height * scale);
    CGColorSpaceRef colorSpace = CGColorSpaceCreateDeviceRGB();
    CGContextRef context = CGBitmapContextCreate(NULL,
                                                 thumbSize.width,
                                                 thumbSize.height,
                                                 8,//bits per component
                                                 thumbSize.width*4,
                                                 colorSpace,
                                                 bitmapInfo);

    CGRect drawRect = CGRectMake(0, 0, thumbSize.width, thumbSize.height);
    CGContextDrawImage(context, drawRect, image.CGImage);
    CGColorSpaceRelease(colorSpace);

    //第二步 取每个点的像素值
    unsigned char* data = CGBitmapContextGetData (context);

    if (data == NULL){
        CGContextRelease(context);
        return nil;
    }

    NSCountedSet *cls = [NSCountedSet setWithCapacity:thumbSize.width*thumbSize.height];

    for (int x=0; x<thumbSize.height; x++) {
        for (int y=0; y<thumbSize.width; y++) {
            int offset = 4*(x*thumbSize.width + y);
            int red = data[offset];
            int green = data[offset+1];
            int blue = data[offset+2];
            int alpha =  data[offset+3];

            NSArray *clr=@[@(red),@(green),@(blue),@(alpha)];
            [cls addObject:clr];
        }
    }
    CGContextRelease(context);

    //第三步 找到出现次数最多的那个颜色
    NSEnumerator *enumerator = [cls objectEnumerator];
    NSArray *curColor = nil;

    NSArray *MaxColor=nil;
    NSUInteger MaxCount=0;

    while ( (curColor = [enumerator nextObject]) != nil ){
        NSUInteger tmpCount = [cls countForObject:curColor];
        if ( tmpCount < MaxCount ) continue;
        MaxCount=tmpCount;
        MaxColor=curColor;
    }
    //返回三色值+透明度
    NSMutableDictionary *dic = [[NSMutableDictionary alloc] initWithCapacity:0];
    [dic setValue:@([MaxColor[0] intValue]/255.0f) forKey:@"red"];
    [dic setValue:@([MaxColor[1] intValue]/255.0f) forKey:@"green"];
    [dic setValue:@([MaxColor[2] intValue]/255.0f) forKey:@"blue"];
    [dic setValue:@([MaxColor[3] intValue]/255.0f) forKey:@"alpha"];
    return dic;
}
  //裁剪图片
  + (UIImage *)cropSquareImage:(UIImage *)image rect:(CGRect)rect{
    CGImageRef sourceImageRef = [image CGImage];
    CGImageRef newImageRef = CGImageCreateWithImageInRect(sourceImageRef, rect);
    UIImage *newImage = [UIImage imageWithCGImage:newImageRef];
    return newImage;
}


  //判断颜色深浅
  + (BOOL)isDarkColor:(UIColor *)newColor{
    const CGFloat *componentColors = CGColorGetComponents(newColor.CGColor);
    CGFloat colorBrightness = ((componentColors[0] * 299) + (componentColors[1] * 587) + (componentColors[2] * 114)) / 1000;
    if (colorBrightness < 0.5){
        //深色
        return YES;
    } else{
        //浅色
        return NO;
    }
}
```

