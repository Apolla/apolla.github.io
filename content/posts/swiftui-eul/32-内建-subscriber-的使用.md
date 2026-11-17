---
title: "3.2 内建 Subscriber 的使用"
date: 2024-04-19T15:20:05+08:00
lastmod: 2024-04-19T15:20:05+08:00
draft: false
categories: ["SwiftUI"]
weight: 3
aliases:
  - "/posts/3.2-内建-subscriber-的使用/"
---

Combine 内建了两个 Subscriber：sink、assign，SwiftUI 框架中有一个内建的 Subscriber：onReceive。

# sink

关于 sink，前面我们已经介绍过了。这里只做复习：它的作用是生成订阅者来接收发布者发送的数据，该订阅者在 receiveCompletion 闭包中返回事件结束的消息，在 receiveValue 闭包中返回接收到的数据值。

# assign

assign 可以将发布者的发送的数据分发给一个对象的属性，前提是该属性遵循 [ReferenceWritableKeyPath](https://developer.apple.com/documentation/swift/referencewritablekeypath) 协议，这意味着这个对象必须是引用类型，也就是说，assign 只适用于 class ，不适用于 struct。

```swift
class SomeObject {
  var value: Int = 0 {
    didSet {
      print(value)
    }
  }
}

let obj = SomeObject()
let publisher = [1, 2, 3].publisher
let cancellable = publisher.assign(to: \.value, on: obj)

// print
1
2
3
```

# onReceive

在 SwiftUI 部分讲解定时器时，我们已经接触过 onReceive 了，它以 modifier 的形式赋予了 View 响应 publisher 的能力。

这里我们再举例加深对它的印象，同时学习一下 NotificationCenter 的用法。

Combine 拓展了 NotificationCenter 的能力，我们可以直接调用 `.publisher`  生成 Publisher 实例以供订阅。

```swift
struct ContentView: View {
  
  var body: some View {
    Text("Hello")
      .onReceive(NotificationCenter.default.publisher(for: UIApplication.willResignActiveNotification), perform: { _ in
        // app 将进入后台
        print("willResignActiveNotification")
      })
      .onReceive(NotificationCenter.default.publisher(for: UIApplication.didBecomeActiveNotification), perform: { _ in
        // app 将进入前台
        print("didBecomeActiveNotification")
      })
  }
}
```
