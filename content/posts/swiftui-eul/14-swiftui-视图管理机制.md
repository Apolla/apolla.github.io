---
title: "1.4 SwiftUI 视图管理机制"
date: 2023-08-02T08:00:00+08:00
lastmod: 2023-08-02T08:00:00+08:00
draft: false
categories: ["SwiftUI"]
tags: ["Xcode 15b5", "iOS 17", "macOS 14"]
weight: 1
aliases:
  - "/posts/1.4-swiftui-视图管理机制/"
---

<br>


# 视图的身份标识（Identity）

在 UIKit/AppKit 的世界，UIView/NSView 实例是引用类型（class），程序通过指针来引用和区分对象。要实现界面的更新，我们首先需要找到对应的视图，然后下达相应的指令，比如改变视图的位置或者颜色，然后界面才会随之更新，这是典型的命令式编程。

而 SwiftUI 是响应式编程框架，我们只需声明 UI 的布局并将其和状态（或者叫数据）绑定，然后只需要维护状态即可。**状态**是响应式编程的核心概念，它的改变会驱动视图的更新。在 SwiftUI 中，视图都是 View 协议的具体实现，状态的流转会触发 `body` 的重新计算，反映的结果就是视图的重绘。状态的变化会实时反馈在 view 上，view 其实是状态的一部分。

但 SwiftUI 中的 View 实例是值类型（struct），之前的引用机制已经不再适用。那么它是如何找到和区分视图并重新渲染界面的呢？答案是 Identity（以下简称 id）。

SwiftUI 具有多个场景（scene），它们组成了程序的界面。而每个 scene 独立管理自身的生命周期和视图层级，这些视图的结构类似于一个**树形结构**，而 scene 就是根节点。这颗树上的任何一个 view 都有一个表明身份的 id，便于 SwiftUI 查找、比对和更新视图。id 有两种表现形式：显式 id 和结构化 id（也可以称作隐式 id）。

关于 Scene 的详细介绍，详见《SwiftUI 中的场景》。

## 显式 id

下面是一个使用 List 实现的天气列表：

```swift
struct Weather {
  var name: String
  var icon: String
  
  static var mock: [Self] {
    [
      .init(name: "Sun", icon: "sun.max.fill"),
      .init(name: "Rain", icon: "cloud.rain.fill"),
      .init(name: "Snow", icon: "snowflake"),
    ]
  }
}

struct WeatherView: View {
  
  @State private var weathers = Weather.mock
  
  var body: some View {
    List(weathers, id: \.name) {
      Label($0.name, systemImage: $0.icon)
    }
  }
}
```

List 初始化时的 id 参数是显式分配的，它通过 keyPath 的形式获取到数据源 weathers 中的每条数据的 name 属性，将其与每个 Label 实例绑定起来。如此一来，SwiftUI 就可以很方便地根据 id 去渲染和更新相应的 label。

不过，上面的代码有潜在问题。比如，weathers 中存在多条 name 相同的数据时，如果只想对其中一条数据操作，那么根据 name 就无法区分了。所以，为每条数据分配一个唯一的标识符是较为明智的做法，很容易想到使用 `Identifiable` 协议来解决这个问题。

```diff
- struct Weather {
+ struct Weather: Identifiable {
+   let id = UUID()
}
```

如上，使 Weather 实现 Identifiable 协议后。将 List 初始化方法中的 `\.name` 改为 `\.id` ，就能解决上述潜在问题。

SwiftUI 中的 List 支持多个初始化方法，如果数据集合中的元素已经实现了 Identifiable 协议，则无需显示指定 `id`，SwiftUI 会找到对应的 id 自动分配。也就是说下面的代码也是合理的：

```swift
List(weathers) {
  Label($0.name, systemImage: $0.icon)
}
```

id 有助于 SwiftUI 更好地构建和管理视图，当我们需要操作指定的视图时，也需要借助 id 来实现。比如 ScrollView 根据 id 跳转到相应的视图：

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>

## 结构化 id

上文说到使用 id 告知 SwiftUI 如何区分 List 中的条目，但 List 实例本身似乎并没有 id，SwiftUI 如何在视图层级中找到它呢？实际上，SwiftUI 会为其隐式分配 id，又称结构化 id。

多数情况下，SwiftUI 会使用结构化 id 为视图隐式表明身份。然而，SwiftUI 并非全知全能，它有时也需要借助我们为视图显式指定 id：

- 结构化 id 无法明确区分视图时，比如 List 的数据源如有重复时，可能会导致无法预期的结果。因此对于动态加载的视图（List、ForEach 等），无论数据源是否有实现 Identifiable 协议，推荐显式指定 id，使之成为习惯。
- 需要手动调用指定视图时，比如上面的 ScrollView。

# 视图的生命周期

SwiftUI 是一个由数据驱动的声明式框架，当数据变化时，与之绑定的视图会发生重绘。这里的重绘又分为两种情况：

1. 原视图销毁，重新创建新视图。
2. 原视图保留，只更新外观样式。

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>

为了演示二者的区别，示例的源码中为 Text 实例显式指定了一个 id，当没有打开改变 id 的开关时，动画非常流畅。而打开开关时，动画非常生硬，过渡效果不尽人意。

这是因为，SwiftUI 中视图的身份标识是与 view 唯一对应的。改变 text 的 id 后，SwiftUI 会认定原有的 text 并非它要查找的视图，它会销毁原来的 text，重新创建新的 text 替代原来的 text 并将其更新至视图层级。由于前后两个 text 并非同一个对象，SwiftUI 就无法找到一个作动画的锚点进行平滑的过渡，所以视觉上呈现的就只是两个 text 的渐变而已。而没有改变 text 的 id 时，该实例一直存活于视图层级中，它的生命延续着，SwiftUI 根据 id 找到该视图，然后对该视图的属性做插值动画，视觉上就是平滑的过渡效果。

前文提到，SwiftUI 中的视图层级类似于一个树形结构。当某个视图所依附的节点被销毁时，它的生命周期自然也就结束了。视图的销毁会导致它的身份标识不复存在，身份标识的改变也会导致视图的销毁。因此可以认为，view 的生命周期几乎等同于其身份标识（id）。

# 视图的更新和优化

程序运行时，视图的频繁更新是非常常见的。虽然 SwiftUI 中的 view 是值类型的结构体，它们非常轻量、安全，但我们应该尽可能地为 view 提供稳定的 id，这有助于提高程序性能。因为稳定的 id 有助于维持视图的生命周期，这避免了视图的频繁销毁和重建，也为流畅的动画提供了基础。另一方面，SwiftUI 在更新视图树时会进行快照比对，如果某个视图的身份标识没有变化，而且数据也没有变化，它就不必为此进行无谓的计算了。

## 条件渲染的隐患

SwiftUI 支持使用 `if` 或者 `if/else` 进行条件渲染，比如下面的代码表示的是如果是 vip，则展示用户的 vip 标识：

```swift
@State private var isVip1 = false

HStack {
  if isVip1 {
    HStack {
      Text("Bruce")
      Text(Image(systemName: "crown.fill"))
    }
    .padding(10)
    .background(Color.blue)
    .cornerRadius(10)
  } else {
    Text("Bruce")
  }
  
  Spacer()
  
  Toggle("", isOn: $isVip1.animation(.easeInOut(duration: 0.5)))
}
```

这里为 isVip1 添加了绑定值动画，当开关打开时，与 isVip1 属性相关的视图会有动画效果。然而，动画过渡地不够平滑。原因和上文类似，条件渲染会造成视图的销毁和重建。不过条件渲染有点特别，编译器会将 `if/else` 语句转化成 `ConditionalConent<TrueView, FalseView>` 这样的实例，虽然从外表上看，视图类型（ConditionalConent）是一致的，但渲染条件的变化会导致其内部的视图身份发生改变，故而动画变得生硬了。至于 SwiftUI 为何会设计 ConditionalConent 来进行条件渲染，有一种说法是这样的：为了更高效的进行差异对比。对此，笔者并未进行更深入的研究，如果你有更高明的解释，欢迎探讨。

即然知道了问题所在，那么解决方法就有了：避免使用条件渲染，维持视图的稳定 id 和生命周期。代码比较简单，请查看示例中的源码。

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>

## 避免使用 AnyView

如果遇到需要返回不同类型的 View 时，AnyView 也许是一种解决方法。它能够擦除视图的类型信息，但它会使代码变得难以读写，更糟糕的是带来了性能损耗，因此应该尽量避免使用它。

这里先不展开介绍 AnyView，先记住尽量避免使用它。遇到需要返回不同类型的视图时，笔者提供三个解决思路供参考：

- 使用 @ViewBuilder 构建视图。

- 使用 Group 包装视图保持类型一致。

- 借助泛型（View）来传参

## 合理使用 EquatableView

上文说到，如果视图的身份和数据都没有变化，那么 SwiftUI 不会对它进行无谓的计算和渲染。不过这里面有个隐含条件，我们先来看一个示例。

```swift
struct CityNameView: View {
  
  let name: String
  
  var body: some View {
    printLog("refresh")
    return Text(name).font(.title)
  }
}

struct WeatherView: View, Equatable {
  
  let weather: Weather
  
  var body: some View {
    printLog("refresh")
    return Label(
      // 温度数字 格式化
      weather.temperature.celsiusFormat,
      systemImage: weather.icon
    )
  }
}
```

为观察 SwiftUI 是否对视图进行了重绘，这里定义的两个视图在计算属性 `body` 内使用 print 输出。视图重绘时会重新计算 body，控制台输出 "refresh" ，反之没有任何输出。

然后根据这两个视图构建一个新的视图（这里只贴出关键代码，示例完整代码可查看源码）：

```swift
@State private var cityName = "Shenzhen"
@State private var weather = Weather.mock.first!

VStack(spacing: 10) {
  CityNameView(name: cityName)
  WeatherView(weather: weather).equatable()
  
  Button("刷新视图") {
    cityName = "Shenzhen"
    weather = Weather.mock.first!
  }
  .buttonStyle(.borderless)
}
```

按钮点击时，其实什么也没做，只是把同样的值重新赋值给 cityName 和 weather。然而，神奇的事情发生了：CityNameView 不会重绘，而 WeatherView 会一直重绘。这就是前文提到的隐含条件：数据需要实现 Equatable 协议。

这里的 cityName 是 String 类型，本身就实现了 [Equatable](https://developer.apple.com/documentation/swift/equatable) 协议。而 Weather 并没有实现 Equatable 协议，所以 weather 发生赋值行为时，虽然视图的身份稳定而且前后数据看上去一致，但 SwiftUI 并不知道如何进行数据的比对。

顺着这个思路，我们为 Weather 实现 Equatable 协议：

```swift
extension Weather: Equatable {
  
  static func == (lhs: Self, rhs: Self) -> Bool {
    lhs.name == rhs.name && lhs.temperature == rhs.temperature
  }
}
```

然后，重新运行程序，发现 WeatherView 不会频繁刷新了。

虽然目前实现了想要的效果，但是直接去更改 Weather 的行为会影响到所有调用者，这非常不合理。假设我们只希望 WeatherView 数据发生变化时刷新视图，而其它使用 Weather 作为数据的视图不受影响。该如何实现呢？答案是：EquatableView。

修改的代码如下：

```diff
- struct WeatherView: View {
+ struct WeatherView: View, Equatable {
+   static func == (lhs: Self, rhs: Self) -> Bool {
+     lhs.weather.name == rhs.weather.name &&
+     lhs.weather.temperature == rhs.weather.temperature
+   }

- WeatherView(weather: weather)
+ WeatherView(weather: weather).equatable()
+ // 上面是的写法等同于：
+ // EquatableView(content: WeatherView(weather: weather))

- weather = Weather.mock.first!
+ weather = Weather.mock.randomElement()!

- extension Weather: Equatable {
-
-   static func == (lhs: Self, rhs: Self) -> Bool {
-     lhs.name == rhs.name && lhs.temperature == rhs.temperature
-   }
- }
```

这次我们让 WeatherView 实现 Equatable 协议，然后为 weatherView 添加修饰器方法 `.equatable()` 即可。经笔者测试，即使没有调用 `.equatable()` ，也能实现同样的效果。不过还是建议显式调用，有利于提高程序的可读性。

合理地使用 EquatableView 非常适合某些局部视图不需要频繁刷新的场景，这也有利于提高程序性能。鉴于这个刷新机制是由我们自己根据 Equatable 协议实现的，所以要当心数据发生变化而视图不刷新的问题。

------

*本文参考：*

- *[WWDC21/Demystify SwiftUI](https://developer.apple.com/videos/play/wwdc2021/10022/)*
- *[WWDC23/Demystify SwiftUI performance](https://developer.apple.com/wwdc23/10160)*

