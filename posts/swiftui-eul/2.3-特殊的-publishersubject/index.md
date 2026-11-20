# 2.3 特殊的 Publisher：Subject


Subject 协议继承自 Publisher 协议，遵循 Subject 协议的 Publisher 是一种特定类型的 Publisher，它有如下方法：

```swift
/** Subject 协议方法 */

/** 向订阅者发送数据 */
// 发送指定值
func send(Self.Output)
// 发送空值（此时 Output 类型为 Void）
func send()

/** 向订阅者发送生命周期事件 */
// 发送 subscription 实例
func send(subscription: Subscription)

// 发送 completion 信号
func send(completion: Subscribers.Completion<Self.Failure>)
```

Subject 的特别之处在于，我们可以手动调用 send  方法向数据流注入新的值。

Combine 内置了如下两种 Subject：**CurrentValueSubject** 和 **PassthroughSubject**。

# CurrentValueSubject

CurrentValueSubject 需要一个初始化的值，并将该值暂存，当我们注入新值时，暂存的值也会更新。除了使用 send 方法来实现注入和更新值，我们还能给 value 属性赋值来达到同样的目的。

```swift
let subject = CurrentValueSubject<Int, Never>(0)
subject.send(1)

// 0 是订阅前已经生产的数据，没有订阅者可以接收该值，它会被丢弃
// 被暂存的 1 会成为 cancellableA 接收到的第一个值
let cancellableA = subject.sink(receiveValue: {
  print("cancellableA receiveValue:\($0)")
})
subject.send(2)
print("Current value: ", subject.value)

let cancellableB = subject.sink(receiveValue: {
  print("cancellableB receiveValue:\($0)")
})

subject.value = 3
print("Current value: ", subject.value)

// print
cancellableA receiveValue:1
cancellableA receiveValue:2
Current value:  2
cancellableB receiveValue:2
cancellableA receiveValue:3
cancellableB receiveValue:3
Current value:  3
```

# PassthroughSubject

PassthroughSubject 和 CurrentValueSubject 是类似的，区别在于它不要初始化值，也不会保存值。

```swift
let subject = PassthroughSubject<Int, Never>()

subject.send(0)

// 订阅前发送的 0 同样会被丢弃
// cancellableA 只能接收此后发送的所有数据
let cancellableA = subject.sink(receiveValue: {
  print("cancellableA receiveValue:\($0)")
})

subject.send(1)

let cancellableB = subject.sink(receiveValue: {
  print("cancellableB receiveValue:\($0)")
})

subject.send(2)

// print
cancellableA receiveValue:1
cancellableA receiveValue:2
cancellableB receiveValue:2
```

小结：

- CurrentValueSubject：订阅者会接收它发布的最近一个暂存数据和之后所有数据
- PassthroughSubject：订阅者会接收它之后发布的所有数据








---

> 作者: 宋明  
> URL: https://apolla.cc/posts/swiftui-eul/2.3-%E7%89%B9%E6%AE%8A%E7%9A%84-publishersubject/  

