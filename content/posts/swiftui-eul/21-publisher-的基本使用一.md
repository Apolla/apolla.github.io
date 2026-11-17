---
title: "2.1 Publisher 的基本使用（一）"
date: 2024-04-19T15:20:05+08:00
lastmod: 2024-04-19T15:20:05+08:00
draft: false
categories: ["SwiftUI"]
weight: 3
---

在前面的章节中，实际上我们已经多次使用过 Publisher，只是我们不曾察觉。比如我们之前使用的 ObservedObject，它的定义如下：

```swift
@propertyWrapper @frozen struct ObservedObject<ObjectType> where ObjectType : ObservableObject
```

其中的泛型 ObjectType 遵循 **ObservableObject** 协议，该协议的定义中只有一个属性：

```swift
// A publisher that emits before the object has changed.
var objectWillChange: Self.ObjectWillChangePublisher

// The type of publisher that emits before the object has changed.
associatedtype ObjectWillChangePublisher : Publisher = ObservableObjectPublisher
```

其中的关联类型 ObjectWillChangePublisher 正是遵循 **Publisher** 协议。也就是说，当我们使用 ObservedObject 时，系统会隐式地生成 objectWillChange 这样一个 Publisher，一旦遵循 ObservableObject 的 class 中标记为 @Published 的属性值发生变化，就会通过该 Publisher 告知相关的对象。

其它属性包装器如 @EnvironmentObject、@StateObject 等，其原理是一致的。

Combine 为我们提供了许多便利的 Publisher，以下将一一介绍它们的基本使用。

# Future

使用闭包初始化，可以异步返回 Result，可能是单个的值然后结束，也可能因为遇到错误而终止。其初始化方法如下：

```swift
init(_ attemptToFulfill: @escaping (@escaping Future<Output, Failure>.Promise) -> Void)

typealias Promise = (Result<Output, Failure>) -> Void
```

要注意的是，Future 适合于单次返回结果的场景，一旦异步返回结果，发布者和订阅者的生命周期就结束了。如果遇到需要随时间推移发送多个数据给订阅者的情况，Future 这种类型的 Publisher 就不适用了，关于这种情况，后面的内容会做相应的讲解。

下面的示例代码供参考，建议读者自己在工程中实践：

```swift
import SwiftUI
import Combine

enum SomeError: Error {
  case someError
  
  var localizedDescription: String {
    return "Some Error"
  }
}

struct FutureView: View {
  @State private var buttonTitle = "Tap me!"
  
  var body: some View {
    Button(buttonTitle) {
      let publisher = Future<String, SomeError>({ (promise) in
        if Bool.random() {
          promise(.success("Succeed"))
        } else {
          promise(.failure(.someError))
        }
      })
      
      _ = publisher.sink(receiveCompletion: {
        switch $0 {
          case .finished:
            print($0)
          case .failure(let error):
            print(error)
            self.buttonTitle = error.localizedDescription
        }
      }, receiveValue: {
        print($0)
        self.buttonTitle = $0
      })
    }
  }
}
```

我们创建了一个按钮，点击这个按钮的时候，会随机返回成功或失败的结果。成功时，控制台会打印 "Success"，然后打印 "finished"，表示事件已经结束。失败时，控制台只打印 "Some Error"。也就是说，无论返回结果是成功或失败，该订阅事件都会结束。

这里我们使用了 Publisher 协议中的方法：`sink(receiveCompletion:receiveValue:)`，它的作用是生成订阅者来接收发布者发送的数据，该订阅者在 receiveCompletion 闭包中返回事件结束的消息，在 receiveValue 闭包中返回接收到的数据值。

# Just

Just 是非异步的，它会向每个订阅者发送一个值，并且只发送一次，然后就结束了。Just 关联的 Failure 类型是 Never，表明它永远不会返回失败的结果。

Just 通常用于错误处理场景，比如当 publisher 遇到错误时（[Publishers.Catch](https://developer.apple.com/documentation/combine/publishers/catch)），我们可以使用 Just 生成一个新的 publisher，并发送一个默认的值。这个值是一定会发送给订阅者的，因为 Just 不会返回失败的结果。

```swift
publisher // 某个 Publisher
	.catch { err in
  	return Just(placeholder) // placeholder 是默认值
  }
```

上面的伪代码表示，一旦 publisher 捕获到错误，就使用 Just 立即发送一个新的默认值 placeholder，这样的话，订阅者就不会收到错误信息。

# Deferred

Deferred 使用一个 Publisher 初始化，可以延迟执行传入的 Publisher 的闭包。

前面提到的 Future，虽然它可以异步返回结果，但是它在创建的时候就会立即执行闭包，我们无法控制闭包的执行时机。如果我们不想立即执行该闭包，可以使用 Deferred 来包装一下。

我们先看看下面的代码：

```swift
import SwiftUI
import Combine

enum SomeError: Error {
  case someError
  
  var localizedDescription: String {
    return "Some Error"
  }
}

struct ContentView: View {
  
  var body: some View {
    Button("Tap Me") {
      let publisher = Future<String, SomeError> { promise in
        if Bool.random() {
          print("true")
          DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            print("time is out")
            promise(.success("success"))
          }
        } else {
          print("false")
          promise(.failure(.someError))
        }
      }
    }
  }
}

```

当我们点击按钮时，Future 闭包会立即执行，随机打印 "true" 或 "false"，如果是 true，还会在 2 秒之后继续打印 "time is out"。

我们将代码改造一下：

```swift
struct ContentView: View {
  // 用于持有实例，保证其不被立即销毁
  @State private var cancellable: AnyCancellable?
  
  var body: some View {
    Button("Tap Me") {
      let publisher = Deferred {
        Future<String, SomeError> { promise in
          if Bool.random() {
            print("true")
            DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
              print("time is out")
              promise(.success("success"))
            }
          } else {
            print("false")
            promise(.failure(.someError))
          }
        }
      }
      
//      cancellable = publisher.sink {
//        switch $0 {
//        case .finished:
//          print("finished")
//        case .failure(let err):
//          print(err)
//        }
//      } receiveValue: {
//        print($0)
//      }
    }
  }
}
```

再次执行代码时，控制台没有任何反应，因为 Future 闭包被延迟执行了。只有当我们给 publisher 绑定订阅者的时候，才会执行发布事件。试试打开注释掉的代码，一切又变得正常了。

# Empty

永远不会发送任何数据，可以立即结束，或不会结束。

Empty 的初始化方法中有一个参数 completeImmediately，当设置为 true 时，发布事件将立即结束。当设置为 false 时，该发布事件永远不会结束。

当你需要返回一个 Publisher，但是又不希望发送数据，或者不希望发布事件结束时，使用 Empty 是非常合适的。比如我们遇到需要处理的错误时，又不希望发送错误，就可以使用 Empty 来实现。

# Fail

以指定的错误立即结束发布事件。

比如当我们需要检查一组数据是否符合要求时，一旦遇到不符合要求的数据，就要告知订阅者这组数据不合法，这个时候就可以在发现非法数据时，使用 Fail 来告知订阅者具体的错误并立即结束发布事件。如果所有的数据都是合法的，那么 Fail 不会被执行。

# Record

Record 可以记录一系列的值和结束事件，然后发送给订阅者。

示例代码：

```swift
import SwiftUI
import Combine

struct ContentView: View {
  
  var body: some View {
    Button("Tap Me") {
      Record<Int, Never> { record in
        record.receive(1)
        record.receive(2)
        record.receive(3)
        record.receive(completion: .finished)
      }.sink {
        print($0) // 接收到事件结束
      } receiveValue: {
        print($0) // 接收到发送的值
      }
    }
  }
}

//print
//1
//2
//3
//finished
```
