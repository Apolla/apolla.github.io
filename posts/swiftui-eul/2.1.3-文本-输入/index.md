# 2.1.3 文本-输入


<br>


# [TextField](https://developer.apple.com/documentation/swiftui/textfield)

## 构建及样式

TextField 具有多个构建方法，最简单的如下：

```swift
@State private var text1 = ""

TextField("text1", text: $text1)
```

`$text1` 和 Text 的绑定是双向的，输入框变化时，text1 随之变化，如果主动变更 text1 的值，输入框也会更新。

通过 `.textFieldStyle` 方法可以改变 TextField 的样式，效果见示例。

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>

iOS 16/macOS 13 开始，TextField 还支持文本的自动扩充，由参数 `axis` 指定水平/垂直方向。比如：

```swift
@State private var axisSelection: Axis = .vertical

TextField("text2", text: $text2, axis: axisSelection)
  .lineLimit(3) // 最多三行
```

如果输入框有多行内容，TextField 会自动在 `.vertical` 方向上扩充，但最多三行，超过三行的内容可以滑动呈现。

此外，TextField 还能便捷地进行格式转换：

```swift
TextField("text3", value: $text3, format: .number)
```

如上代码用于将输入文字转换成数字，需注意的是，当输入框失去焦点结束编辑时，才会触发格式转换，而且只有转换成功时，才会更新相应的值。

## 状态监听、键盘处理

[onSubmit(of:_:)](https://developer.apple.com/documentation/swiftui/view/onsubmit(of:_:)) 可以监听键盘的回车事件：

```swift
TextField("text4", text: $text4)
  .onSubmit {
    printLog("return")
  }
```

of 参数是可选的，默认值是 `.text` ，表示监听的是 TextField 的回车事件。另一个可选的值是 `.search`，表示监听搜索栏的回车事件，后文介绍滑动视图中使用 `.searchable` 构建搜索栏时会使用到。

如果一个视图中有多个 TextField，其中一个不想被监听回车事件，可以调用 [.submitScope()](https://developer.apple.com/documentation/swiftui/view/submitscope(_:)) 进行显示声明。

要更改回车按键的样式，可以使用 [submitLabel(_:)](https://developer.apple.com/documentation/swiftui/view/submitlabel(_:)) 。

键盘的隐藏有三种方式：

1. 使用 @FocusState。

   在 《SwiftUI 中的属性包装器》 中就详细介绍过 @FocusState 的使用了，本文也增加了一个示例供参考。

2. 在滑动视图中使用 [.scrollDismissesKeyboard](https://developer.apple.com/documentation/swiftui/timelineview/scrolldismisseskeyboard(_:))。

   当滑动视图时，键盘会消失，消失的策略有好几种，效果见示例。这里说明一下 `.interactively` 这一策略的作用，滑动视图时，只有 TextField 移除屏幕显示区域时，才会触发键盘的消失。

3. 使用 UIKit 中的全局通知。

   将以下代码封装成方法供全局调用：

   ```swift
   #if canImport(UIKit)
   UIApplication.shared.sendAction(
     #selector(UIResponder.resignFirstResponder),
     to: nil, from: nil, for: nil
   )
   #endif
   ```

# [SecureField](https://developer.apple.com/documentation/swiftui/securefield)

SecureField 用于输入密码的场景，以上提到以及未提到的 TextField 的方法都适用于它。

# [TextEditor](https://developer.apple.com/documentation/swiftui/texteditor)

理解了TextEditor 使用较为简单，此处略过。

示例实现的是一个具有 placeholder 的 TextEditor，供参考。

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>






---

> 作者: 宋明  
> URL: https://apolla.cc/posts/swiftui-eul/2.1.3-%E6%96%87%E6%9C%AC-%E8%BE%93%E5%85%A5/  

