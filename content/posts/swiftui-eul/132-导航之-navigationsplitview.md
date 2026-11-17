---
title: "1.3.2 导航之 NavigationSplitView"
date: 2022-11-21T08:00:00+08:00
lastmod: 2022-11-21T08:00:00+08:00
draft: false
categories: ["SwiftUI"]
tags: ["Xcode 14", "iOS 16", "macOS 13"]
weight: 1
aliases:
  - "/posts/1.3.2-导航之-navigationsplitview/"
---

<br>


<br>

[NavigationSplitView](https://developer.apple.com/documentation/swiftui/navigationsplitview) 用于快速构建多栏视图，它支持在 Apple 全平台上使用。根据设备屏幕尺寸（Size Class）的差异，NavigationSplitView 的样式有所不同。

Size Class 分为 regular 和 compact，NavigationSplitView 相应的表现分别是分栏和导航栈。正如示例所示，在 iPhone 14 Plus 或 iPhone 14 Pro Max 机型上，竖屏时 Size Class 是 compact，导航行为就是常见的 push 和 pop。而横屏时，Size Class 是 regular，视图会变成分栏样式。

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>

关于 iOS 设备的尺寸信息，可以查看 [Device size classes](https://developer.apple.com/design/human-interface-guidelines/foundations/layout/#best-practices)。

相比 NavigationStack，NavigationSplitView 的使用相对简单。它包含如下初始化方法：

```swift
init(sidebar: () -> Sidebar, detail: () -> Detail)

init(sidebar: () -> Sidebar, content: () -> Content, detail: () -> Detail)

init(columnVisibility: Binding<NavigationSplitViewVisibility>, sidebar: () -> Sidebar, detail: () -> Detail)

init(columnVisibility: Binding<NavigationSplitViewVisibility>, sidebar: () -> Sidebar, content: () -> Content, detail: () -> Detail)
```

sidebar 和 detail 分别对应第一栏和最后一栏，content 是中间一栏。后一栏的数据依赖于前一栏的选择，sidebar 和 content 通常使用 [List](https://developer.apple.com/documentation/swiftui/list) 来构建视图，因为它可以很方便地获取到当前选中的条目。需要注意的是，List 有许多的初始化方法，各个方法之间有非常细微的差别，支持的平台也不尽相同，所以使用时需要小心一些，遇到疑问时及时查看文档。

如果需要控制分栏视图的可见性，可以绑定参数至 columnVisibility。[NavigationSplitViewVisibility](https://developer.apple.com/documentation/swiftui/navigationsplitviewvisibility) 有如下样式：

- automatic：根据设备自适应。
- all：显示所有分栏。
- doubleColumn：双栏都显示，三栏显示后面两栏。
- detailOnly：只显示最后一栏。

NavigationSplitView 的每一栏都可以使用下面的方法设置宽度：

- [navigationSplitViewColumnWidth(_:)](https://developer.apple.com/documentation/swiftui/group/navigationsplitviewcolumnwidth(_:))：设置固定宽度。
- [navigationSplitViewColumnWidth(min:ideal:max:)](https://developer.apple.com/documentation/swiftui/group/navigationsplitviewcolumnwidth(min:ideal:max:))：设置可变宽度。

以上所介绍的在示例中都有体现，代码也不复杂，关于 NavigationSplitView 就简单介绍到这里。

此外，NavigationSplitView 中的 detail 可以嵌套使用 NavigationStack 来实现更加复杂的导航行为。


