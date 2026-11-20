# 2.8 使用 UIKit、AppKit


<br>


<br>

SwiftUI 目前仍在发展中，相比古老而健壮的 UIKit/AppKit，它相对年轻，在生产实践中，有时我们需要借助 UIKit/AppKit 来实现 SwiftUI 难以实现的功能。

以下仅以 UIKit 为例进行说明，AppKit 与此类似。

# 使用 UIKit

## [UIViewRepresentable](https://developer.apple.com/documentation/swiftui/uiviewrepresentable)

SwiftUI 通过 UIViewRepresentable 协议可以调用 UIKit 中的视图，比如想使用 UISearchBar：

```swift
struct SearchBarView: UIViewRepresentable {
  func makeUIView(context: Context) -> UISearchBar {
    let uiView = UISearchBar()
    uiView.placeholder = "Input something..."
    uiView.searchBarStyle = .minimal
    return uiView
  }
  
  func updateUIView(_ uiView: UISearchBar, context: Context) {
    uiView.text = searchText
  }
}
```

`makeUIView` 只有在实例初始化的时候调用一次，`updateUIView` 会在 SearchBarView 视图的状态发生改变时调用。

关于 `updateUIView` 的调用时机，可以参考下面的代码及注释：

```swift
struct ContentView: View {
  @State private var text = "Label"
  @State private var fontSize = 18.0
  @State private var flag = true
  
  var body: some View {
    VStack {
      MyLabel(text: text, fontSize: fontSize)
      Button("Update") {
        flag.toggle()
      }
    }
  }
}

struct MyLabel: UIViewRepresentable {
  // 如果 `text` 和 `fontSize` 的值没有发生改变
  // 不会调用 `updateUIView` 方法
  let text: String
  let fontSize: CGFloat
  
  // 如果没有使用 `ContentView` 中的 flag
  // 无论它是否改变，都不会调用 `updateUIView` 方法
  // 只要构建时用到了 `ContentView` 中的 flag
  // 无论是否使用，都会调用 `updateUIView` 方法
  // let flag: Bool
  
  // 总结：只有 uiView 的视图状态发生改变时，
  // 才会调用 `updateUIView` 方法，其命名也暗示了一切
  
  func makeUIView(context: Context) -> UILabel {
    let label = UILabel()
    label.text = text
    label.font = .systemFont(ofSize: fontSize)
    return label
  }
  
	
  /// Updates the state of the specified view with new information from SwiftUI.
  func updateUIView(_ uiView: UILabel, context: Context) {
    print("update")
    uiView.text = text
    uiView.font = .systemFont(ofSize: fontSize)
  }
}
```

然后就可以调用 **SearchBarView** 了，但是这还不够，如果要实时获取搜索框的文字内容，怎么办？在 UIKit 中，我们可以通过代理方法获取，接下来的问题就是怎么将值传给 SwiftUI。

UIViewRepresentable 协议中有个方法可以将 UIKit 的变化传出去告诉 SwiftUI

```swift
func makeCoordinator() -> Self.Coordinator
```

我们只需要实现一个中间调度器，然后在这个方法内实例化调度器，并带上需要传给 SwiftUI 的内容即可。最后实现的所有代码如下：

```swift
struct SearchBarView: UIViewRepresentable {
  @Binding var searchText: String
  
  class Coordinator: NSObject, UISearchBarDelegate {
    var searchBarView: SearchBarView
    
    init(_ searchBarView: SearchBarView) {
      self.searchBarView = searchBarView
    }
    
    func searchBar(
      _ searchBar: UISearchBar,
      textDidChange searchText: String
    ) {
      searchBarView.searchText = searchText
    }
    
    func searchBarSearchButtonClicked(
      _ searchBar: UISearchBar
    ) {
      searchBar.endEditing(true)
    }
  }
  
  func makeCoordinator() -> Coordinator {
    Coordinator(self)
  }
  
  func makeUIView(context: Context) -> UISearchBar {
    let uiView = UISearchBar()
    uiView.placeholder = "Input something..."
    uiView.searchBarStyle = .minimal
    uiView.delegate = context.coordinator
    return uiView
  }
  
  func updateUIView(_ uiView: UISearchBar, context: Context) {
    uiView.text = searchText
  }
}
```

## [UIViewControllerRepresentable](https://developer.apple.com/documentation/swiftui/uiviewcontrollerrepresentable)

UIViewControllerRepresentable 与 UIViewRepresentable 类似，它赋予 SwiftUI 调用控制器的能力，示例中演示了在 SwiftUI 中调用 SFSafariViewController。

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>

# 使用 AppKit

SwiftUI 可以通过 [NSViewRepresentable](https://developer.apple.com/documentation/swiftui/nsviewrepresentable)、[NSViewControllerRepresentable](https://developer.apple.com/documentation/swiftui/nsviewcontrollerrepresentable) 这两个协议在 mac 上调用 AppKit 提供的功能，使用上和调用 UIKit 是类似的。



---

> 作者: 宋明  
> URL: https://apolla.cc/posts/swiftui-eul/2.8-%E4%BD%BF%E7%94%A8-uikitappkit/  

