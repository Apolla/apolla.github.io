# 4.7 动画的进阶使用


<br>


<br>

# [Transaction](https://developer.apple.com/documentation/swiftui/transaction)

事务（Transaction）是当前状态更新的上下文，包含状态变化过程中的动画。

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>

事务可以用于在视图层级中管理动画，比如：

```swift
Rectangle()
  .fill(.red)
  .rotationEffect(.degrees(degrees))
  .animation(.default, value: degrees)

Button("rotate") {
  // 使用 withTransaction 重写动画
  var t = Transaction(animation: .linear(duration: 1))
  t.disablesAnimations = true
  
  withTransaction(t) {
    degrees += 45
  }
}
```

这里使用 withTransaction 将旧动画 `.default` 重写为 `.linear`。

或是使用 `.transaction` 方法重写旧的动画：

```swift
Rectangle()
  .fill(.orange)
  .rotationEffect(.degrees(degrees))
  .transaction { t in
    // 在已有的 animation 基础上修改
    t.animation = t.animation?.speed(3)
  }
```

也可以使用新的动画替代旧动画：

```swift
t.animation = .interactiveSpring().delay(0.5)
```

如果将 `t.animation` 设置为 `nil`，则表示禁用动画。

# GeometryEffect

[GeometryEffect](https://developer.apple.com/documentation/swiftui/geometryeffect) 是一个遵循 Animatable 和 ViewModifier 协议的协议，允许使用几何变换创建自定义效果来改变视图的位置、大小等。

比如示例中的 CircleEffect ，它可以使视图沿着圆形路径运动：

```swift
fileprivate struct CircleEffect: GeometryEffect {
  var progress: CGFloat
  var radius: CGFloat
  
  var animatableData: CGFloat {
    get { progress }
    set { progress = newValue }
  }
  
  func effectValue(size: CGSize) -> ProjectionTransform {
    let angle = CGFloat.pi * progress * 2
    return .init(.init(
      translationX: radius * cos(angle),
      y: radius * sin(angle))
    )
  }
}
```

计算并不复杂，主要是根据三角函数计算出视图的偏移量。使用时只需调用该修饰器方法并添加动画即可，该效果可以方便地在任意视图上进行复用。

# matchedGeometryEffect

参考 《SwiftUI 中的属性包装器》 中关于属性包装器 @NameSpace 的介绍。

# TimelineView

[TimelineView](https://developer.apple.com/documentation/swiftui/timelineview) 可以根据指定的时间调度器更新视图，其构建方法如下：

```swift
init(
    _ schedule: Schedule,
    content: @escaping (TimelineView<Schedule, Content>.Context) -> Content
)
```

`schedule` 参数就是指定的时间调度器，它遵循 [TimelineSchedule](https://developer.apple.com/documentation/swiftui/timelineschedule) 协议。`content` 闭包内构建的视图会根据 schedule 的设定来按照一定的频率不断地重绘视图，频率可以是周期性的，也可以是非周期性的。只要频率足够高，就可以实现帧动画的效果。

content 闭包内返回的是一个 [TimelineView.Context](https://developer.apple.com/documentation/swiftui/timelineview/context) 类型的结构体，其中有一个重要的属性：`date`，它表示触发视图更新的时间点。视图每次更新时，都可以通过该属性获取到当前的时间。

系统内置了多个常用的时间调度器，具体效果和使用见示例及代码。

自定义时间调度器需要实现 TimelineSchedule 协议，该协议要求实现 `entries(from:mode:)` 方法来指定时间调度的规则，示例中演示了一个特殊的时钟，每间隔 1/2/3 秒更新一次。

以上介绍了 TimelineView 的基本概念，如果将上面示例中展示时间的 Text 换成其它视图，以 TimelineView.Context 中的 date 属性作为变量因子去不断地生成和变换视图，那么就可以创建一些比较酷炫的粒子效果。这里只是提供一个思路，有兴趣的读者可以自行实现。

示例还演示了 TimelineView 和 Canvas 结合使用来创建一个波浪动画，供参考。




---

> 作者: 宋明  
> URL: https://apolla.cc/posts/swiftui-eul/4.7-%E5%8A%A8%E7%94%BB%E7%9A%84%E8%BF%9B%E9%98%B6%E4%BD%BF%E7%94%A8/  

