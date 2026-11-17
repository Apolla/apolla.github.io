---
title: "3.9 自定义布局（Layout）"
date: 2023-01-07T08:00:00+08:00
lastmod: 2023-01-07T08:00:00+08:00
draft: false
categories: ["SwiftUI"]
tags: ["Xcode 14", "iOS 16", "macOS 13"]
weight: 1
---

<br>


<br>

SwiftUI 内置了丰富的布局容器，也支持简单的布局调整，它们能够解决大多数常用的布局需求。但仍然有所限制，比如 HStack 或者 VStack，它们只能在单一线性轴上进行布局，Grid 虽然可以兼顾横向和纵向，但子视图的位置不能随意调整。

而 Layout 协议支持自定义布局，我们可以使用它随心所欲地实现各种纷繁的布局效果。

# 自定义 Layout

要实现自定义布局，需要实现 [Layout](https://developer.apple.com/documentation/swiftui/layout) 协议，它有两个必须实现的方法：

```swift
func sizeThatFits(
    proposal: ProposedViewSize,
    subviews: Self.Subviews,
    cache: inout Self.Cache
) -> CGSize

func placeSubviews(
    in bounds: CGRect,
    proposal: ProposedViewSize,
    subviews: Self.Subviews,
    cache: inout Self.Cache
)
```

`sizeThatFits` 负责计算和返回自定义 layout 容器所需的尺寸，`placeSubviews` 则用于将子视图放置在布局容器内指定的位置。在布局过程中，这两个方法会被多次调用，sizeThatFits 计算出布局容器所需的尺寸后，然后调用 placeSubviews 方法放置各个子视图。

`proposal` 参数是 [ProposedViewSize](https://developer.apple.com/documentation/swiftui/proposedviewsize) 类型，表示父视图可以为某个子视图能够提供的建议尺寸。ProposedViewSize 内置了三种建议的尺寸：

- zero：子视图只使用最小尺寸的空间进行布局。
- infinity：子视图尽可能地占用父视图可利用的空间进行布局。
- unspecified：子视图使用理想的尺寸进行布局，即不拮据也不贪婪，只要空间够用就行。

除此之外，ProposedViewSize 也提供了使用具体的宽高指定子视图尺寸的初始化方法。

`subviews` 是子视图的集合，可以获取到每个子视图的尺寸、间距，对齐方式等信息。

`cache` 是可选的，一般用不上，必要时可以缓存计算的结果，在更新布局时可以提高性能。

`placeSubviews` 中的 `bounds` 参数实际上就是 `sizeThatFits` 计算出的布局容器所需的尺寸。

示例中演示的是一个自定义的格子视图，可以根据间距和父视图尺寸进行动态布局。实现思路就是上面介绍的，首先在 `sizeThatFits` 方法中计算出所有子视图所占用的宽高（包括间距），然后在 `placeSubviews` 方法中根据布局容器的尺寸和设定的间距计算出各个子视图应该放置的位置。

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>

自定义 Layout 的基础的使用思路就是这样，核心就在于计算父视图布局容器的尺寸和子视图的位置。当然，Layout 提供的功能远不止如此，更深入的用法有待进一步探究。

# AnyLayout

AnyLayout 是一个擦除类型信息的 Layout，它可以让视图在不同 Layout 之间通过动画平滑地切换。

如下是旧有的条件布局代码：

```swift
if condition {
  HStack {}
} else {
  VStack {}
}
```

当切换布局时，旧的视图和布局信息会被摧毁，新的视图会被创建并重新布局。这个切换是一个重新计算的过程，视图身份的变化也导致切换过程无法平滑地使用动画过渡。

而 AnyLayout 不会摧毁旧的视图，它只是改变视图的布局，视图身份的稳定性得以维持，这减少了不必要的计算，而且可以在切换不同布局时进行流畅的过渡。

```swift
let layout = condition
? AnyLayout(HStackLayout())
: AnyLayout(VStackLayout())
return layout {
  content
}
```

SwiftUI 内置了一些常用的 layout 供 AnyLayout 使用，如 HStackLayout、VStackLayout、ZStackLayout 和 GridLayout，它们都实现了 Layout 协议，我们也可以使用自定义的 Layout。

AnyLayout 之所以能够支持使用动画平滑过渡，是因为它已经实现了动画的核心协议：[Animatable](https://developer.apple.com/documentation/swiftui/animatable) ，在后面的动画部分会再次见到该协议的使用。

# WaterFall 的一种实现思路

实际开发中常用的瀑布流布局，似乎也可以使用自定义 Layout 实现。但实际上不太合适，因为 Layout 无法进行惰性计算，如果瀑布流视图的数据量很大，这会导致性能问题。因此，自定义 Layout 目前只适合相对简单和静态的布局，对于动态加载的视图，需要考虑数据规模和关注程序性能。

示例中提供了一种使用 HStack + LazyVStack 实现瀑布流的思路，LazyVStack 的惰性计算特性解决了自定义 Layout 导致的性能问题。经测试，数据规模的显著增大并不会导致性能问题。其核心原理其实还是数学计算，具体可以参考示例中的源码。



