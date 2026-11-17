---
title: "4.1 形状（Shapes）的使用"
date: 2023-01-07T08:00:00+08:00
lastmod: 2023-01-07T08:00:00+08:00
draft: false
categories: ["SwiftUI"]
tags: ["Xcode 14", "iOS 16", "macOS 13"]
weight: 1
aliases:
  - "/posts/4.1-形状shapes的使用/"
---

<br>


# 常用的内置形状及样式

## 内置形状

SwiftUI 内置了一些常用的形状，比如矩形、椭圆、正圆等。

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>

RoundedRectangle 和 Capsule 都有一个初始化参数 `style` ，它是枚举类型 `RoundedCornerStyle`，其默认值是 `.continuous`，相比另一个枚举值 `.circular`，它的圆角曲线更为平滑。

AnyShape 是一种擦除类型信息的形状，这在需要返回不同类型的形状时非常有用。如示例所示：

```swift
fileprivate struct AnyShapeView: View {
  @Binding var isCircular: Bool
  
  var body: some View {
    isCircular
    ? AnyShape(Circle())
    : AnyShape(Capsule())
  }
}
```

## 样式与行为

### 填充

以下两个 `.fill` 方法用于填充 Shape：

```swift
func fill(style: FillStyle = FillStyle()) -> some View

func fill<S>(
    _ content: S,
    style: FillStyle = FillStyle()
) -> some View where S : ShapeStyle
```

FillStyle 一般使用默认值，SwiftUI 内置的颜色、渐变效果等都已经实现了 ShapeStyle 协议。此处先不展开来讲，后文会详细介绍 FillStyle 和 ShapeStyle 的具体用法。

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>

### 描边

系统提供了多个 `.stroke` 修饰器方法用于为形状添加描边。

遗憾的是，由于 `.stroke` 和 `.fill` 方法返回的是不同的类型，所以无法使用链式调用的方式同时为一个形状添加描边和填充效果。示例中演示了使用 `.background` 和 `.overlay` 将二者结合起来，当然也有其它思路来实现，比如使用 ZStack 或者自定义 ViewModifier 等。

### containerShape

`.containerShape` 修饰器方法声明如下：

```swift
func containerShape<T>(_ shape: T) -> some View where T : InsettableShape
```

它可以为容器内的视图形状设定相对关系，比如示例中子视图的圆角大小不是绝对的，系统会根据子视图自身尺寸大小设置一个相对值，这种动态适配的形状可以提供更好的视觉体验。

SwiftUI 中内置的形状都已经实现 InsettableShape 协议，我们也可以通过实现该协议来自定义相对关系。

### 裁剪视图

`clipShape(_:style:)` 方法可以裁剪视图，`style` 参数遵循 Shape 协议，只要是实现该协议的形状都可以使用。

### 变换

一些常用的视图变换操作，比如 transform、offset、scale、rotation 等，对 Shape 同样是适用的。

示例中演示了`trim(from:to:)` 的使用，它可以根据比例值绘制形状的一部分。

更多的变换操作及使用可以参考 [Shape](https://developer.apple.com/documentation/swiftui/shape)  协议。

# 使用 Path 绘制自定义形状

无论是内置形状还是自定义形状，都需要实现 [Shape](https://developer.apple.com/documentation/swiftui/shape) 协议。该协议有一个必须实现的方法：

```swift
func path(in rect: CGRect) -> Path
```

rect 参数是视图的尺寸，返回的是 [Path](https://developer.apple.com/documentation/swiftui/path) 类型的实例，它自身也实现了 Shape 协议。

比如我们自定义一个三角形：

```swift
fileprivate struct Triangle: Shape {
  
  func path(in rect: CGRect) -> Path {
    Path { path in
      path.move(to: CGPoint(x: rect.midX, y: 0))
      path.addLine(to: CGPoint(x: rect.maxX, y: rect.maxY))
      path.addLine(to: CGPoint(x: 0, y: rect.maxY))
      path.closeSubpath()
    }
  }
}
```

把 path 想象成一只画笔，先将画笔移动至画布上的某个点，然后开始绘制线条，这些点和线组成的路径就是最终绘制的形状。

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>

Path 提供了许多常用的方法，可以绘制直线、曲线、圆弧等各种形状。

前面提到 Shape 可以使用 `.fill(_:style:)`  方法进行填充，其中 style 是 FillStyle 类型，它有如下初始化方法：

```swift
init(
    eoFill: Bool = false,
    antialiased: Bool = true
)
```

`antialiased` 表示是否抗锯齿，默认为 true，可以使绘制的形状更为平滑。

`eoFill` 表示是否根据奇偶相间的规则进行填充。示例中自定义一个由三个圆叠加的形状 ThreeCircles，当指定 `eoFill` 为 true 时，圆的相交部分会根据奇偶相间的规律进行反色填充。

```swift
ThreeCircles()
  .fill(.blue.gradient, style: .init(eoFill: eoFill))
```

示例还演示了如何绘制一个太极图，供参考。




