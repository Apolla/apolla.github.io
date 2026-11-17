---
title: "1.3.4 工具栏（Toolbars）"
date: 2022-12-01T08:00:00+08:00
lastmod: 2022-12-01T08:00:00+08:00
draft: false
categories: ["SwiftUI"]
tags: ["Xcode 14", "iOS 16", "macOS 13"]
weight: 1
---

<br>


<br>

SwiftUI 将 navigationBar、bottomBar、tabBar、windowToolbar 等视图的功能和样式都整合在了工具栏中，使用时调用的 api 都是以 .toolbar 开头的。

比如要给导航栏右侧添加一个分享按钮：

```swift
#if os(iOS)
NavigationStack {
  ContentView()
  .toolbar {
    ToolbarItem(placement: .navigationBarTrailing) {
      Button {
      } label: {
        Image(systemName: "square.and.arrow.up")
      }
    }
  }
}
#endif
```

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>

placement 参数是 [ToolbarItemPlacement](https://developer.apple.com/documentation/swiftui/toolbaritemplacement) 类型，表示 item 放置的位置。如果需要在同一位置放置多个 item，可以使用 ToolbarItemGroup ：

```swift
ToolbarItemGroup(placement: groupPlacement) {
  Button {
  } label: {
    Image(systemName: "square.and.arrow.up")
  }
  Menu {
    Button("Menu 1") {}
    Button("Menu 2") {}
  } label: {
    Image(systemName: "pencil")
  }
}

var groupPlacement: ToolbarItemPlacement {
  #if os(iOS)
  .navigationBarTrailing
  #else
  .primaryAction
  #endif
}
```

如果需要改变 toolbar 的背景，可以这样设置：

```swift
#if os(iOS)
.toolbarBackground(.yellow, for: .navigationBar)
.toolbarBackground(.visible, for: .navigationBar)
#elseif os(macOS)
.toolbarBackground(.linearGradient(
  colors: [.blue, .purple],
  startPoint: .leading,
  endPoint: .trailing), for: .windowToolbar)
#endif
```

这里的 for 参数是 [ToolbarPlacement](https://developer.apple.com/documentation/swiftui/toolbarplacement) 类型，表示 toolbar 的位置。

toolbar 还支持以下特性：

- [toolbarColorScheme(_:for:)](https://developer.apple.com/documentation/swiftui/view/toolbarcolorscheme(_:for:))：指定 toolbar 的 ColorScheme。
- [toolbar(_:for:) ](https://developer.apple.com/documentation/swiftui/view/toolbar(_:for:))：设置 toolbar 的显示和隐藏。
- toolbarTitleMenu(content:)：给 toolbar 的标题设置下拉菜单。

以上在示例中都有演示，都是比较简单的操作，就不再展开来讲了。

更多关于工具栏的特性，可以探索：[Toolbars](https://developer.apple.com/documentation/swiftui/toolbars)。

不过 Toolbars 除灵活性不足之外，还有不少明显的问题，比如 `.toolbarTitleMenu` 只在 iOS 和 iPadOS 上有效，设置 `.toolbarBackground` 时需要同时指定 `.toolbarBackground(.visible, for: ToolbarPlacement...)` 才仅在部分 ToolbarPlacement 生效。诸如此类，亟待完善。




