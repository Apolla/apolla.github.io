---
title: "1.3.0 TabView 的使用"
date: 2022-11-23T08:00:00+08:00
lastmod: 2022-11-23T08:00:00+08:00
draft: false
categories: ["SwiftUI"]
tags: ["Xcode 14", "iOS 16", "macOS 13"]
weight: 1
---

<br>


# 基础使用

[TabView](https://developer.apple.com/documentation/swiftui/tabview) 等同于 UIKit 中的 UITabBar，先来看看它的基础使用：

```swift
struct ContentView: View {
  @State private var selection = TabType.home
  
  var body: some View {
    TabView(selection: $selection) {
      ForEach(TabType.allCases, id: \.self) { tab in
        tab.view.tag(tab)
      }
    }
  }
}

enum TabType: String, CaseIterable {
  case home = "Home"
  case search = "Search"
  case settings = "Settings"
  
  var systemImage: String {
    switch self {
    case .home:
      return "house"
    case .search:
      return "magnifyingglass"
    case .settings:
      return "gear"
    }
  }
  
  var view: some View {
    Text(self.rawValue)
      .tabItem {
        Label(self.rawValue, systemImage: self.systemImage)
      }
  }
}
```

TabView 的闭包内使用 ForEach 构建视图，这里有 Home、Search、Settings 三个视图，每个视图使用 `.tabItem` 配置对应的文字、图标。

tabView 有个可选的绑定参数 `selection`，用来控制当前选中的 tab。前提是 tabView 中的每个子视图分配了唯一的标签（使用 `.tag` 方法），这样才能让 tabView 找到对应的视图。

示例中还演示了使用 `.tabViewStyle` 改变 TabView 的风格样式，都是基本操作。

如果需要给 tab 增加角标，可以使用 `.badge` 方法，传参可用整形数字或字符串，入参为 `0` 或者 `nil` 时 角标不显示。`.badge` 还可以用在 List 或者 Form 中，后面的章节会有演示。

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>

# 自定义 TabView

当系统提供的 TabView 样式无法满足设计需求时，则需要自定义 TabView。如示例，我们手动实现了一个带阴影的浮动样式的 TabView。

TabView 中的子视图如果不设置 tabItem，那么 tab 是不会显示的。利用这一点，我们可以自定义一个视图去替换原有的 tab 栏，但 TabView 的子视图的切换逻辑依然由系统维护。大致的思路就是这样，以下是实现代码：

```swift
ZStack(alignment: .bottom) {
  TabView(selection: $selection) {
    ForEach(TabType.allCases, id: \.self) { tab in
      tab.view
        .tag(tab)
        .toolbar(.hidden, for: .tabBar)
    }
  }
  
  CustomTabView(selection: $selection)
}
.ignoresSafeArea(.all, edges: [.bottom])
```

这里没有给 `tab.view` 设置 tabItem，借助于 ZStack，自定义的 CustomTabView 是叠在 TabView 上的，这样就形成了视觉上的浮动效果，而且不管 TabView 的子视图如何切换，都能保证自定义的 tab 栏始终显示。

虽然没有给子视图设置 tabItem，但是系统带分隔线的磨砂效果的 tab 栏依然是存在的，`.toolbar(.hidden, for: .tabBar)` 的作用就是为了隐藏系统的 tab 栏。

`.ignoresSafeArea(.all, edges: [.bottom])` 是为了优化屏幕适配，我们先来看看自定义 tab 栏的实现代码：

```swift
fileprivate struct CustomTabView: View {
  @Binding var selection: TabType
  
  var body: some View {
    HStack {
      ForEach(0..<TabType.allCases.count, id: \.self) { idx in
        Button {
          self.selection = TabType.allCases[idx]
        } label: {
          Image(systemName: TabType.allCases[idx].systemImage)
            .font(.title3)
            .foregroundColor(
              selection == TabType.allCases[idx]
              ? .orange
              : .gray
            )
            .frame(maxWidth: .infinity)
        }
      }
    }
    .frame(maxWidth: .infinity)
    .frame(height: 54)
    .background(Color.black)
    .cornerRadius(27)
    .shadow(radius: 10)
    .padding(.init(top: 10, leading: 44, bottom: 32, trailing: 44))
  }
}
```

最后一行设置了  padding ，如果没有调用 .ignoresSafeArea，在具有 safeArea 的机型上，底部间距会过大。如果设置了 .ignoresSafeArea 而没有设置 padding，在没有 safeArea 的机型上，底部没有间距则毫无美感。二者的结合使用，可以更好地适配不同机型。

CustomTabView 要解决的核心问题就一件事：TabView 进行切换时（比如可以滑动的 TabView），自定义 tab 栏更新样式；自定义 tab 栏点击时，将事件回传给 TabView 去刷新界面。这里是通过 @Binding 变量 `selection` 和 TabView 进行双向绑定来实现的，关于 @Binding 的用法，可以参考：《SwiftUI 中的属性包装器》。

以上思路仅为抛砖引玉，更多的探索有待读者自行发掘。






