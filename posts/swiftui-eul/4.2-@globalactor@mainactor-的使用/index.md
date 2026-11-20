# 4.2 @GlobalActor、@MainActor 的使用


# GlobalActor

状态隔离使得 actor 成为在并发环境中安全使用的引用类型，但它的作用范围仅限于单个 actor 类型。如果某些变量、函数分散在不同的地方，actor 无法将它们置于同一个隔离环境中。因此，Swift 引入了 [GlobalActor 协议](https://developer.apple.com/documentation/swift/globalactor)，将状态隔离的概念扩展至全局范围。

使用 `@globaActor` 修饰的结构体、枚举、actor 或 `final` class 被称作全局 actor，它会隐式地遵循 `GlobaActor` 协议，该协议有一个关联类型为 `Actor` 的 `static` 属性要必须实现：

```swift
associatedtype ActorType : Actor

static var shared: Self.ActorType { get }
```

如下是一个自定义的全局 actor：

```swift
@globalActor
public struct GlobalAdder {
  
  public actor AdderActor {}
  
  public static let shared = AdderActor()
}
```

这样的写法非常类似单例，实际上也确实如此，全局 actor 只会生成唯一的 `shared` 实例用于同步外部对内部可变状态的访问。`shared` 是实现 `Actor` 协议的具体类型，而 `Actor` 协议内部有个默认的遵循 [Executor](https://developer.apple.com/documentation/swift/executor) 协议的序列化调度器 [SerialExecutor](https://developer.apple.com/documentation/swift/serialexecutor)，它是将并发访问事件序列化的幕后工作者。

假设我们有一个全局变量 *globalNumber* ，它会分散在程序的各个角落，多个不同的线程都可能会更新该变量。为了保证 *globalNumber* 被并发访问时的数据一致性，我们可以使用 `@GlobalAdder` 来修饰相关的属性和方法。

```swift
var globalNumber = 0

class Adder1 {
  
  @GlobalAdder
  func add() {
    globalNumber += 1
  }
  
  func nonisolatedAdd() {
    globalNumber += 1
  }
}

@GlobalAdder
struct Adder2 {
  
  func add() {
    globalNumber += 1
  }
  
  func isolatedAdd() {
    globalNumber += 1
  }
}
```

*Adder2* 整个类都使用 `@GlobalAdder` 修饰，那么它内部的所有属性、方法都默认是处于同一隔离环境中，无需显式地使用 `@GlobalAdder` 修饰。而 *Adder1* 只是一个普通的类，`add()` 方法使用了 `@GlobalAdder` 修饰，它可以消除数据竞争，但 `nonisolatedAdd()` 方法却不行，它就是一个类中的普通方法，没有任何同步机制保障 *globalNumber* 的数据一致性。

以上只是举例说明全局 actor 的使用，实际上为了消除数据竞争对  *globalNumber* 的影响。正确的写法如下：

```swift
@GlobalAdder var globalNumber = 0
```

所有调用该变量的地方，如果是写操作，那么相关代码必须在 `GlobalAdder` 的隔离环境中执行，如果只是读取，则无需使用 `@GlobalAdder` 进行状态隔离，但该访问是异步的，需要使用 `await` 标记。

如果代码有安全隐患，编译器会自动提示错误信息，这有助于我们在编译期最大程度地保证数据安全。

全局 actor 还具备推断能力，比如某个类的方法使用 `@SomeGlobalActor` 修饰，其子类在重写该方法时，会隐式地被 `@SomeGlobalActor` 修饰而无需显式声明。这些比较简单，更多内容请参考 [SE-0316/Global actor inference](https://github.com/apple/swift-evolution/blob/main/proposals/0316-global-actors.md#global-actor-inference)。

# MainActor

## @MainActor 的使用

截止至 Swift 5.6，系统内置的 GlobalActor 只有一个：[MainActor](https://developer.apple.com/documentation/swift/mainactor)，它是 GlobalActor 的典型运用，也是最为重要的全局 actor。

在 `MainActor` 出现之前，我们通常使用这样的写法从其它线程回到主线程：

```swift
DispatchQueue.main.async {
  // update UI
}
```

现在我们可以这样写：

```swift
@MainActor func updateUI() {
  
}
```

MainActor 就是一个全局的主线程 actor，使用 `@MainActor` 进行标记会将相关工作放回主线程执行。

如果某个变量更新会驱动视图刷新，可以使用 `@MainActor` 标记：

```swift
@MainActor var text: String = ""
```

在执行完某个耗时事件后，回到主线程更新 UI：

```swift
// 全局 actor 可以用于修饰函数，闭包只不过是匿名函数罢了
func updateUI(completion: @MainActor @escaping () -> ()) {
  Task.detached {
    await completion()
  }
}
```

将某个类使用 `@MainActor` 修饰意味着它的属性、方法等都会被隐式地被标记为 `@MainActor`。同普通的 actor 一样，如果某些工作不需要被状态隔离，可以使用 `nonisolated` 标记：

```swift
@MainActor
class SomeClass {
  
  nonisolated func noisolatedWork() {
    
  }
}
```

其实，在 *9.3 SwiftUI 中常见的异步 API* 这一节我们就已经见过 `MainActor` 的身影了。在理解本节内容后，相信你能更好地驾驭它。

## @MainActor 可能导致的性能问题

Concurrency 并不是在原有的 GCD 基础上构建的，而是基于新的线程模型。Swift 提供了一个默认的可协作线程池，负责调度和执行任务。线程池可以生成的线程数量最多不超过设备的 CPU 核心数，也就是说一个 CPU 核心最多只需要负责一个线程，这避免了线程爆炸。

当一个线程暂停执行一个 actor 的任务，线程不会阻塞，转而执行另一个 actor 的任务时，我们称之为“actor 跳转”。actor 在可协作线程池内发生跳转不需要上下文切换，就像调用函数一样简单而轻快。但是，主线程是特殊的，它独立于线程池之外。普通的 actor 和 MainActor 之间存在上下文切换，这会带来性能损耗。

我们来看一个获取缓存的图片并展示在界面上的例子（这里仅以此为例，你可以把获取缓存图片类比为其它比较轻量的异步任务）：

```swift
actor ImageCache {
  
  func retrieveImage(id: String) -> Image {
    // retrieving...
    return Image(id)
  }
}

class ListImagesViewModel: ObservableObject {
  @Published var images = [Image]()
  private var cache = ImageCache()
  
  func retrieveImages(ids: [String]) async {
    for id in ids {
      let image = await cache.retrieveImage(id: id)
      images.append(image)
    }
  }
}

struct ListImagesView: View {
  @StateObject var vm = ListImagesViewModel()
  
  var body: some View {
    List(0..<vm.images.count, id: \.self) { i in
      vm.images[i]
    }
    .task {
      let ids = (0..<100).map { "\($0)" }
      await vm.retrieveImages(ids: ids)
    }
  }
}
```

`vm.images` 每次发生变化的时候，都会触发主线程的视图重绘。而 `retrieveImages(ids:)` 方法中，每异步获取一张缓存图片，就会更新一次 `vm.images` 的值，这会导致程序在 `ImageCache` actor 和 MainActor 之间频繁地进行上下文切换，但异步获取缓存图片是非常快速的（也可以类比为其它轻量的异步任务），如此频繁地切换可能会导致性能问题。

我们可以将多个轻量的异步任务合并起来，等它们都完成后再刷新 UI，这样就减少了上下文切换的频率，从而降低了性能损耗的风险。根据这个思路，上面的代码优化如下：

```swift
actor ImageCache {
  
  func retrieveImages(ids: [String]) -> [Image] {
    // retrieving...
    return ids.map { Image($0) }
  }
}


class ListImagesViewModel: ObservableObject {
  @Published var images = [Image]()
  private var cache = ImageCache()
  
  func retrieveImages(ids: [String]) async {
    let res = await cache.retrieveImages(ids: ids)
    images.append(contentsOf: res)
  }
}
```



---

> 作者: 宋明  
> URL: https://apolla.cc/posts/swiftui-eul/4.2-@globalactor@mainactor-%E7%9A%84%E4%BD%BF%E7%94%A8/  

