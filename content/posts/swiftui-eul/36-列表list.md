---
title: "3.6 列表（List）"
date: 2023-06-05T08:00:00+08:00
lastmod: 2023-06-05T08:00:00+08:00
draft: false
categories: ["SwiftUI"]
tags: ["Xcode 14.3", "iOS 16.4", "macOS 13.3"]
weight: 1
---

<br>


# List

## 构建

### 基础

[List](https://developer.apple.com/documentation/swiftui/list) 提供了非常多的构建方法，各方法的入参有细微的差别，支持的平台也不尽相同，所以使用时需要小心一些，遇到疑问时及时查看文档。

鉴于篇幅有限，无法一一例举各个构建方法的使用和详述其区别所在。但无论使用何种构建方式，都要记住保持视图身份 id 的稳定性，关于视图身份标识，可以参考 《SwiftUI 视图及状态管理机制》 。

在 《导航之 NavigationSplitView》  中也演示过 List 的使用，其初始化方法中可以绑定 selection，这在需要保存选中项的场景（比如 NavigationSplitView）非常有用，详细使用可参考：

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> NavigationSplitView</span>

示例中使用支持 selection 的构建方法分别演示了单选和多选列表，这需要和 `EditButton` 配合使用，仅支持 iOS 平台而且需要在导航视图中使用：

```swift
.toolbar {
  EditButton()
}
```

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>

### 可展开列表

List 可以直接从树形结构的集合数据中构建可展开列表。

比如先定义一个可嵌套的树形数据结构：

```swift
fileprivate struct ExpandWeather: Identifiable, Hashable {
  let id = UUID()
  var name: String
  var icon: String
  var weathers: [ExpandWeather]?
}
```

然后定义相应的数据并用于构建 List：

```swift
fileprivate struct ExpandedList: View {
  private let expandWeather: [ExpandWeather] = [
    ExpandWeather(name: "Weather", icon: "", weathers: [
      ExpandWeather(name: "Sunshine", icon: "sun.max.fill"),
      ExpandWeather(name: "Cloud", icon: "cloud"),
      ExpandWeather(name: "Snow", icon: "snow"),
      ExpandWeather(name: "Rain", icon: "cloud.rain.fill")
    ])
  ]
  
  var body: some View {
    List(expandWeather, children: \.weathers) { weather in
      if weather.icon.isEmpty {
        Text(weather.name)
      } else {
        Label(weather.name, systemImage: weather.icon)
      }
    }
  }
}
```

List 会自动根据 children 属性生成可展开的列表，这里只构建了简单地二级嵌套列表，你可以尝试嵌套层级更深的数据，List 会自动根据层级深度构建更复杂的可展开列表。

## 样式

List 提供了多重 listStyle，具体效果可以在示例中切换查看。

示例还例举了 List 一些常用的样式设置：

- listRowInsets：设置 listRow 边距。
- listRowBackground：设置 listRow 背景。
- listRowSeparatorTint：设置 listRow 分割线颜色。
- listRowSeparator：设置分割线的显隐。
- badge：设置角标，支持数字和 Text。
- scrollContentBackground：隐藏系统风格的背景，和 background 结合使用可以自定义 list 背景。

## 交互

### 下拉刷新

修饰器方法 [refreshable(action:)](https://developer.apple.com/documentation/swiftui/view/refreshable(action:)) 可以为 List 添加下拉刷新事件，该方法同样适用于 ScrollView。不过，该行为在 macOS 下并没有明显的表现形式。

refreshable 的使用非常简单，只需在 action 闭包内执行异步事件即可，示例中使用 Task.sleep 模拟了一个异步事件，`fetch()` 执行完后 list 会刷新。

```swift
.refreshable {
  await fetch()
}
```

关于 async/await 以及异步事件的相关知识，在后面的 Concurrency 部分会有详细介绍，这里了解即可。

### 搜索

```swift
.searchable(
  text: $searchText,
  placement: searchFieldPlacement,
  prompt: "Input something..."
)
.searchSuggestions {
  ForEach(searchResults, id: \.self) { v in
    Text("Looking for \(v.name)?")
      .searchCompletion(v.name)
    Text("Looking for \(Image(systemName: v.icon))")
      .searchCompletion(v.name)
  }
}

private var searchFieldPlacement: SearchFieldPlacement {
  #if os(iOS)
  .navigationBarDrawer(displayMode: .always)
  #else
  .toolbar
  #endif
}
```

`.searchable` 可以为 List 增加搜索功能，`placement` 用于控制搜索框的位置和显隐藏。

修饰器方法 `.searchSuggestions` 还能为搜索提供推荐的结果，`.searchCompletion` 可以将任意视图绑定至匹配的搜索结果。

更多关于搜索的使用请参考：[Search modifiers](https://developer.apple.com/documentation/swiftui/view-search) 。

`.searchScopes` 方法可以实现按范围查找，比如如 Eul 在 iOS 上的查找：


> ⚠️ 原文图片缺失：list_1.jpg


使用比较简单，可参考文档 [Scoping a search operation](https://developer.apple.com/documentation/swiftui/scoping-a-search-operation)。

### 编辑

前面提到在导航视图中为 List 添加 EditButton 后，就可以实现单选和多选操作了。其实它还支持列表条目的 delete 和 move 操作：

```swift
List {
  ForEach(weathers, id: \.id) { v in
    Label(v.name, systemImage: v.icon)
  }
  .onDelete(perform: onDelete)
  .onMove(perform: onMove)
}
.toolbar {
  EditButton()
}
```

onDelete 并不依赖于 EditButton，只要为 list 添加了 onDelete 事件，列表就已经支持侧滑删除了。

# 层级列表

除了直接使用 List 提供的初始化方法构建可展开列表之外，系统还提供了 [OutlineGroup](https://developer.apple.com/documentation/swiftui/outlinegroup) 和 [DisclosureGroup](https://developer.apple.com/documentation/swiftui/disclosuregroup) 来构建层级列表。使用上和 List 并无二致，但后面二者的使用范围更广，它门可以在任意 view 中使用。

DisclosureGroup 相比 OutlineGroup 则更为灵活，它不必使用树形结构的数据源来构建视图，而且还能通过绑定的 `isExpanded` 属性，更灵活地控制视图的显示与隐藏。

OutlineGroup 和 DiclosureGroupView 还可以相互嵌套使用，以实现更为复杂的层级视图。

官方文档中已有详细示例，这里不再例举。


