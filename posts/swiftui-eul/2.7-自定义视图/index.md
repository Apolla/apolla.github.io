# 2.7 自定义视图


<br>


# 自定义 view

SwiftUI 中的视图都是实现 View 协议的结构体，比如需要自定义一个垂直布局的 Label：

```swift
struct VLabel: View {
  let image: Image
  let text: String
  
  var body: some View {
    VStack {
      image
      Text(text)
    }
  }
}
```

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>

有时视图比较轻量，我们想通过计算属性或者函数直接返回视图：

```swift
@ViewBuilder var buttonOrText: some View {
  if Bool.random() {
    Button("I'm a button") {}
      .buttonStyle(.borderless)
  } else {
    Text("I'm a text")
  }
}
```

这里如果不使用 @ViewBuilder 进行标记是无法通过编译的，因为 buttonOrText 返回的是不透明类型 `some View` ，它的具体类型可能是 Button 或者 Text，我们需要使用 @ViewBuilder 进行标记来生成不同的的视图。

而 VLabel 中的 body 无需使用 @ViewBuilder 标记就可以进行条件编译，是因为它已经被标记过了。View 的定义如下：

```swift
public protocol View {
  associatedtype Body : View
  @ViewBuilder @MainActor var body: Self.Body { get }
}
```

关于不透明类型，参考 《Swift 中的不透明类型和存在类型》 。

[ViewBuilder](https://developer.apple.com/documentation/swiftui/viewbuilder) 其实是一个结果生成器，关于结果生成器，参考 《Swift 中的 Result builders》 。

@ViewBuilder 还能修饰闭包参数并从中构建视图，比如想要自定义一个可以自由地在水平或竖直方向上布局的容器视图：

```swift
struct HVStack<Content: View>: View {
  private let axis: Axis
  private let content: () -> Content
  
  init(
    axis: Axis,
    @ViewBuilder content: @escaping () -> Content
  ) {
    self.axis = axis
    self.content = content
  }
  
  var body: some View {
    if axis == .horizontal {
      HStack {
        content()
      }
    } else {
      VStack {
        content()
      }
    }
  }
}
```

如示例中所示，当切换布局方向时，HVStack 实例会刷新视图和布局。

如果 HVStack 不需要在初始化时做额外的操作，可以简写成这样：

```diff
- private let axis: Axis
- private let content: () -> Content
+ let axis: Axis
+ @ViewBuilder let content: () -> Content

- init(
-   axis: Axis,
-   @ViewBuilder content: @escaping () -> Content
- ) {
-   self.axis = axis
-   self.content = content
- }
```

后面还能通过使用 AnyLayout 切换布局来实现 HVStack 的效果，这里仅为说明自定义view 的使用。

# 自定义 Modifier

要自定义 Modifier，需要实现 [ViewModifier](https://developer.apple.com/documentation/swiftui/viewmodifier) 协议。

比如想要通过 Modifier 为任意视图添加一个卡片效果：

```swift
struct CardStyle: ViewModifier {
  
  func body(content: Content) -> some View {
    content
      .padding(30)
      .background(.regularMaterial)
      .cornerRadius(10)
      .shadow(radius: 8)
  }
}
```

然后就可以在进行调用了：

```swift
Text("Hello").modifier(CardStyle())
```

这样还不够方便，我们可以通过扩展 View 来支持点语法调用：

```swift
extension View {
  func cardStyle() -> some View {
    modifier(CardStyle())
  }
}

Image(systemName: "applelogo").cardStyle()
ProgressView().cardStyle()
```

 



---

> 作者: 宋明  
> URL: https://apolla.cc/posts/swiftui-eul/2.7-%E8%87%AA%E5%AE%9A%E4%B9%89%E8%A7%86%E5%9B%BE/  

