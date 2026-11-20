# 3.3 布局的调整


<br>


<br>

调整视图布局的方法是多样的，本文主要介绍通过调整 view 的尺寸、位置以及对齐方式等来实现布局的基础调整，在实际开发中，需要选择合适的方法来实现不同的布局效果。除此以外，后面还会介绍自定义 layout 来实现更加高级和灵活地布局。

# 尺寸

## padding

SwiftUI 提供了多个 padding 方法，可以方便地调整视图各个方向上的内边距，从而影响布局和空间的分配。

```swift
// 上下左右内边距都为 5
.padding(5)

// 上、左内边距为 5
.padding([.top, .leading], 5)

// 上下内边距为 5，左右内边距为 10
.padding(EdgeInsets(top: 5, leading: 10, bottom: 5, trailing: 10))
```

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>

## frame

frame 有两个方法，一是为视图设置固定的尺寸：

```swift
Text("Hello")
  .frame(width: 60, height: 40, alignment: .topLeading)
```

`alignment` 参数表示的是 view 在该 frame 中的对齐方式，比如上面的代码表示的是文本在 60 * 40 的区域内左上对齐。

另一个方法支持多个参数，可以设置 view 的最小、最大以及理想尺寸，如果空间足够，view 会按照最大尺寸布局，如果空间不够，view 会按照最小尺寸布局。

```swift
func frame(
    minWidth: CGFloat? = nil,
    idealWidth: CGFloat? = nil,
    maxWidth: CGFloat? = nil,
    minHeight: CGFloat? = nil,
    idealHeight: CGFloat? = nil,
    maxHeight: CGFloat? = nil,
    alignment: Alignment = .center
) -> some View
```



## fixedSize

fixedSize 可以将 view 调整至理想尺寸。

比如下面的文本，由于 frame 的限制，文本会被压缩。使用 fixedSize 修饰后，文本内容则可以完整展示。

```swift
Text("Hello World")
  .fixedSize()
  .frame(minWidth: 30, maxWidth: 50, maxHeight: 30)
```

前面提到 frame 可以指定 view 的理想尺寸，这通常和 fixedSize 结合使用：

```swift
Text("Hello World")
  .frame(minWidth: 50, idealWidth: 100,
         maxWidth: 150, maxHeight: 30)
  .fixedSize()
```

在使用 fixedSize 修饰后，文本宽度会使用指定的 idealWidth 值。

注意这里 fixedSize 的顺序和上面是不一样的。

## layoutPriority

[layoutPriority(_:)](https://developer.apple.com/documentation/swiftui/view/layoutpriority(_:)) 可以指定视图布局的优先级，系统默认所有 view 的 layoutPriority 都是 0。

比如示例中的文本视图由于空间不足会被压缩显示成省略号，使用 layoutPriority 可以为 view 指定更高的布局优先级，系统将优先为其分配布局空间。

# 位置

## Spacer

[Spacer](https://developer.apple.com/documentation/swiftui/spacer) 是贪婪的，它会自动在 Stack 主轴方向上扩展，以此改变 view 的位置。在非 Stack 容器中，Spacer   会在 x、y 两个方向上同时延展。

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>

## Divider

[Divider](https://developer.apple.com/documentation/swiftui/divider) 用于将视图分隔开以获得更好的视觉体验。

要改变 divider 的尺寸和颜色，可以这样设置：

```swift
Divider()
  .frame(height: 2)
  .overlay(.blue)
```

## position

positon 用于调整 view 的中心点在父视图中的位置。

## offset

offset 用于调整 view 的偏移量。

# 对齐方式

alignment 主要是指水平或垂直方向上视图的对齐方式，系统内置了一些常用的对齐方式。

示例中演示了 iOS 16/macOS 13 新增的一个对齐方式：

```swift
Label("Swift", systemImage: "swift")
  .alignmentGuide(.listRowSeparatorLeading) { _ in 0 }
```

`.listRowSeparatorLeading` 用于使列表中条目的分隔线从左边开始对齐。

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>

有时系统内置的对齐方式无法满足需求时，我们需要适当地调整 alignmentGuide，比如示例中的方块，在水平和垂直方向上分别做了微调，以实现一些特殊的对齐效果。

```swift
Rectangle()
  .frame(width: 50, height: 50)
  .alignmentGuide(.top) { d in -d.height * 0.5 }
```

alignmentGuide 的 computeValue 闭包中返回的是一个 [ViewDimensions](https://developer.apple.com/documentation/swiftui/viewdimensions) 结构体实例，它包括 view 的 height、width 属性，还可以通过下标获取到具体的 [HorizontalAlignment](https://developer.apple.com/documentation/swiftui/horizontalalignment) 或 [VerticalAlignment](https://developer.apple.com/documentation/swiftui/verticalalignment) 并在此基础上调整对齐方式。

为了方便地复用一些特殊的对齐方式，还可以通过实现 [AlignmentID](https://developer.apple.com/documentation/swiftui/alignmentid) 协议来自定义对齐方式：

```swift
extension HorizontalAlignment {
  struct CustomAlignment: AlignmentID {
    static func defaultValue(in context: ViewDimensions) -> CGFloat {
      return context[.trailing]
    }
  }
  
  static let custom = HorizontalAlignment(CustomAlignment.self)
}

fileprivate struct CustomAlignmentGuide: View {
  var body: some View {
    VStack(alignment: .custom) {
      HStack {
        Text("手机")
          .alignmentGuide(.custom) { $0[.trailing] }
        Text("155********")
      }
      
      HStack {
        Text("电子邮箱")
          .alignmentGuide(.custom) { $0[.trailing] }
        Text("xxxxxx@gmail.com")
      }
    }
  }
}
```

上面的代码实现的效果是将“手机”和“电子邮箱”的尾部对齐。

# SafeArea

SwiftUI 会自动根据设备屏幕为视图调整安全区域，使用 [ignoresSafeArea](https://developer.apple.com/documentation/swiftui/view/ignoressafearea(_:edges:)) 可以显示地忽略指定方向上的安全区域，使用 safeAreaInset 可以在指定方向上扩展安全区域。

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>

# 自适应布局

## 根据屏幕自适应

SwiftUI 提供了两个环境变量 `.horizontalSizeClass` 和 `.verticalSizeClass`，分别对应iOS 设备水平和竖直方向上的 Size Class，我们可以据此实现不同的布局以提供更好的用户体验。

关于 iOS 设备的尺寸信息，可以查看 [Device size classes](https://developer.apple.com/design/human-interface-guidelines/foundations/layout/#best-practices)。

如果你手持的是 Max 或 Plus 系列的 iPhone，旋转屏幕时可以看到不同的布局效果。

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>

## 根据尺寸自适应

ViewThatFits 是 iOS 16/macOS 13 新推出的功能，它能根据可利用的空间自动选择合适的视图。通常在构建 ViewThatFits 视图时按照从大至小的顺序提供视图选项，示例直接借鉴了官方样例：

```swift
ViewThatFits(in: .horizontal) {
  HStack {
    Text("\(uploadProgress.formatted(.percent))")
    ProgressView(value: uploadProgress)
      .frame(width: 100)
  }
  ProgressView(value: uploadProgress)
    .frame(width: 100)
  Text("\(uploadProgress.formatted(.percent))")
}
```

上面的代码表示的是一个根据尺寸自适应的进度视图，如果尺寸足够，会以左右布局的形式展示进度和数字，如果空间局限，则只展示简单的数字。

另一个示例也是 ViewThatFits 的具体运用：

```swift
ViewThatFits {
  HStack {
    Color.red
      .frame(minWidth: 300, minHeight: 100)
    Color.blue
      .frame(minWidth: 300, minHeight: 100)
  }
  VStack {
    Color.red
      .frame(minWidth: 300, minHeight: 100)
    Color.blue
      .frame(minWidth: 300, minHeight: 100)
  }
}
```

在 iPhone 上横竖屏切换或者在 mac 上调整窗口大小时，布局会自动进行切换。我们无需监听任何尺寸信息的变化，ViewThatFits 会自动根据视图尺寸选择最合适的布局，这非常方便。如此灵活的布局，意味着它的使用不那么可控，在实际开发中，需要尽可能地在不同设备上进行测试，以提供更好的用户体验。






---

> 作者: 宋明  
> URL: https://apolla.cc/posts/swiftui-eul/3.3-%E5%B8%83%E5%B1%80%E7%9A%84%E8%B0%83%E6%95%B4/  

