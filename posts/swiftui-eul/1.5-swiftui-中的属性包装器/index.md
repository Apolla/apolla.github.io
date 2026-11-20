# 1.5 SwiftUI 中的属性包装器


<br>


<br>

> 以下内容适用于 iOS 16/macOS 13 以上的系统，iOS 17/macOS 14 新增的 [Observation](https://developer.apple.com/documentation/observation) 框架简化了 SwiftUI 的状态管理，苹果的文档有非常详细的使用说明和迁移教程，笔者也写了一篇关于 Observation 的文章以供参考：[《有了 Observation，SwiftUI 还需要 Combine 吗》](https://www.woter.xyz/blog/ios/swiftui/swiftui-observation-combine)。

属性包装器（Property Wrappers）是 Swift 5.1 的新特性之一（详见 [SE-0258](https://github.com/apple/swift-evolution/blob/main/proposals/0258-property-wrappers.md)），它的主要作用是将通用的模板代码封装成一种简洁的表达形式，极大地提高了编码的效率。

SwiftUI 内置了大量的属性包装器，熟悉它们的用法和区别，是熟练使用 SwiftUI 的必要条件之一。接下来先讲解 SwiftUI 中常用的属性包装器，然后介绍如何自定义属性包装器。

本节示例通过 section 区分，将它们集合在了一起。

<span style="background: #007BFF; color: white; padding: 3px 10px; border-radius: 5px">> 查看示例</span>

# SwiftUI 常用的属性包装器

以下根据属性包装器作用和使用场景做了粗略的分类。

## 模型数据

### [@State](https://developer.apple.com/documentation/swiftui/state)

在当前 view 内修饰属性，当属性值发生改变时，与之相关的视图会更新。@State 只能修饰简单的数据类型，比如 String、Bool 或 Array 等。

@State 被设计为存储 view 的当前状态，因此不宜对外暴露，一般使用 private 限定使用范围。同时要避免在 view 中使用 init 方法初始化 @State 变量，这可能会导致 SwiftUI 的状态管理冲突。

示例中显示温度的开关属性是这样声明的：

```swift
@State private var showTemperature = true
```

该属性绑定在一个开关上：

```swift
Toggle("显示温度", isOn: $showTemperature.animation())
  .toggleStyle(.switch)
```

温度的显隐逻辑：

```swift
Text(v.temperature.celsiusFormat)
  .opacity(showTemperature ? 1 : 0)
```

当开关的状态发生改变时，与之绑定的 `showTemperature` 会改变，这会触发温度视图的重绘。

### [@Binding](https://developer.apple.com/documentation/swiftui/binding)

上面的示例代码其实已经提到了 Binding，体现在将属性 `showTemperature` 绑定在开关控件上。其作用也非常明显：双向绑定。具体点说，当 A 视图将某个属性 p 注入 B 视图时，在 B 视图中将 p 使用 `@Binding` 修饰，那么在 B 视图中改变 p 值时，A 视图会监听到 p 的变化，并刷新视图。

示例中的“天气随机顺序”也是使用双向绑定实现的，在 BindingView 中有如下声明：

```swift
@Binding var weathers: [Weather]
```

weathers 数据的注入方式：

```swift
BindingView(weathers: $soVM.weathers)
```

这里的美元符号 `$` 和上面提到的开关控件的绑定属性 `$showTemperature` 是一样的，这其实是 SwiftUI 提供的一个语法糖，方便我们快速地进行绑定操作。

State 和 Binding 中都有如下两个属性：

```swift
var wrappedValue: Value

var projectedValue: Binding<Value>
```

当使用 @State 或 @Binding 修饰某个属性时，该属性值会存储在变量 wrappedValue 中。需要读写属性值时，直接调用即可，读写的自然也是 wrappedValue 的值。而进行绑定操作时，实际上绑定的是 projectedValue，为了方便调用 projectedValue，SwiftUI 将其简化成了语法糖： `$`。

在本节后面的内容中，会介绍如何使用它们自定义属性包装器。

除了以上基础用法之外，有时还需要自定义 Binding 来实现更为复杂的功能。正如示例所示，分别有一个开关控制“记住密码”和“自动登录”。这两个选项之间有着逻辑上的关联，“自动登录”跟用户名以及密码输入框的值也有关联。诚然，通过 `onChange(of:perform:)` 方法去监听每个开关的状态并做相应的逻辑处理可以实现功能。但代码和逻辑过于分散，而且不方便复用。

以下代码截取自示例中的源码，自定义的 `loginBinding` 和“自动登录”开关进行了绑定。当开关状态变化时，`set` 闭包会返回新的值，该值变化涉及到的相关业务逻辑就是在这里集中处理的。`get` 闭包用于返回绑定的值，这里直接返回了 `isAutoLogin`，当然我们也可以在这里根据实际需要做更多的工作。

```swift
// 自定义 Binding
// 通过泛型约束要绑定的数据类型
// 实现 get 和 set 即可
private var loginBinding: Binding<Bool> {
  Binding {
    self.isAutoLogin
  } set: { value in
    if value && !self.isPwdRemembered {
      self.isPwdRemembered = true
    }
    self.isAutoLogin = value
    
    if self.isAutoLogin {
      username = "zzzwco"
      pwd = "20221110"
    } else {
      username = ""
      pwd = ""
    }
  }
}

// 调用
Toggle("自动登录", isOn: loginBinding)
```

这个自定义 Binding 的示例主要解决的关联状态的变化问题，所以主要逻辑集中在 `set` 闭包中。苹果提供了一个 [官方示例](https://developer.apple.com/tutorials/swiftui-concepts/defining-the-source-of-truth-using-a-custom-binding)，演示的是通过 `get` 闭包进行绑定变量的转换。这里截取了其中一段核心代码并添加了注释：

```swift
// 外部注入的变量
@Binding var recipeId: Recipe.ID?

// 实际需要的是 Recipe 类型的绑定变量
private var recipe: Binding<Recipe> {
    Binding {
      	// set 内做转换处理
        if let id = recipeId {
            return recipeBox.recipe(with: id) ?? Recipe.emptyRecipe()
        } else {
            return Recipe.emptyRecipe()
        }
    } set: { updatedRecipe in
        recipeBox.update(updatedRecipe)
    }
}
```

### [@StateObject](https://developer.apple.com/documentation/swiftui/stateobject)、[@Published](https://developer.apple.com/documentation/combine/published)

@State 只能修饰简单的数据类型，而且使用的范围比较有限。而实际情况是数据（无论是本地还是服务端返回）通常会转换成模型对象，这比简单的数据类型要复杂的多，而且对象应该具备监听属性变化的能力，这样才能使 SwiftUI 视图响应变化并刷新视图。

[ObservableObject](https://developer.apple.com/documentation/combine/observableobject) 协议正是我们所需要的，实现该协议的类实例具备了我们所需要的特性。如下：

```swift
fileprivate final class WeathersVM: ObservableObject {
  @Published var weathers: [Weather] = []
  
  init() {
    weathers = Weather.mock
  }
}
```

- 只有 class 能够遵循 ObservableObject 协议，因为 class 是引用类型，当实例在多个视图之间进行传递时，它们引用的是同一个实例，能够共享数据状态的变化，保证不同界面的数据一致性。

- 通常会使用 final 关键字修饰 ObservableObject 协议的具体实现类，这是为了防止继承的侵入性导致意想不到的后果。
- 对于需要监听的属性，使用 @Published 修饰，当属性值发生变化时，相应的视图会重绘。

这里先提一句，@Published 实际上是后面 **Combine** 部分内容介绍的 **Publisher** 的语法糖，比如 `@Published var str = ""` 中的 `str` 是 `String` 类型，而 `$str` 的类型是 `Published<String>.Publisher`，实际上就是一个 Publisher 实例，系统提供的 Publisher 实例方法它都是可以调用的。

其它的属性包装器基本是类似的，比如上面提到的 `@Binding var value: String` , `value` 是 `String` 类型，而 `$value` 是 `Binding<String>` 类型。

实现 ObservableObject 的具体类之后，使用时用 @StateObject 修饰相应的实例：

```swift
@StateObject private var soVM = WeathersVM()
```

@StateObject 和 @State 的命名只差了一个 Object（对象），命名上的细微差别也暗示了它可以监听对象的状态变化。 StateObject 使用泛型约束其修饰的对象必须遵循 ObservableObject 协议，如果修饰的实例没有实现该协议，编译器会提示错误。剩下的使用就很简单了，和 @State 修饰的属性是一样的，具体可以参考源码中对 `soVM` 的调用。

有时我们想要在属性值发生变化时做一些额外的操作，比如后面关于 NavgationPath 的讲解中就有这样的需求：当导航栈的数据发生变化时，保存当前导航状态，在下次进入页面时恢复当前的导航状态。

以下是对 weathers 的改写示例：

```swift
@Published var weathers: [Weather] = []

/**
 手动调用 `objectWillChange.send()`
 同样可以实现 @Published 的效果
 但是可以在属性值变化时，做一些额外的附加操作
 */
var weathers: [Weather] = [] {
  willSet {
    objectWillChange.send()
  }
  didSet {
    // 值更新之后的附加操作
  }
}
```

### [@ObservedObject](https://developer.apple.com/documentation/swiftui/observedobject)

@ObservedObject 和 @StateObject 的使用是完全一样的，唯一的区别在于它们的生命周期不同。

@StateObject 修饰的对象只会在所属的 view 中创建一次并在 view 的生命周期内存续，而 @ObservedObject 修饰的对象会随着 view 的重绘生成新的对象。在示例中通过开关可以在 @StateObject 和 @ObservedObject 之间切换，可以明显地看到，当切换至 @ObservedObject 后，点击“天气随机顺序”按钮时，数据不再产生联动效果，因为每次视图重绘时，@ObservedObject 对象（这里指 ooVm）都会生成新的 WeathersVM 初始化实例。

虽然多数情况下都是使用 @StateObject，但是理解它和 @ObservedObject 的区别，有助于在需要时选择合理的方法实现功能。

## 环境变量

### [@Environment](https://developer.apple.com/documentation/swiftui/environment)

@Environment 可以在任何视图中访问系统预设的环境变量，比如是否暗黑模式、系统日历、时区等。

示例演示了获取系统预设的 colorScheme 来判定是否暗黑模式：

```swift
@Environment(\.colorScheme) private var colorScheme

LabeledContent("ColorScheme") {
  Text(colorScheme == .light ? "Light" : "Dark")
}
```

当切换系统的外观样式时，界面会随之刷新。

更多系统预设的环境变量请参考：[EnvironmentValues](https://developer.apple.com/documentation/swiftui/environmentvalues) 。

除了使用系统预设的环境变量外，还可以向视图树注入自定义的环境变量，实现方式：首先 [EnvironmentKey](https://developer.apple.com/documentation/swiftui/environmentkey) 协议，然后为 EnvironmentValues 扩展一个对应的属性即可。

```swift
private struct UserIdKey: EnvironmentKey {
  static var defaultValue: String = ""
}

extension EnvironmentValues {
  var userId: String {
    get { self[UserIdKey.self] }
    set { self[UserIdKey.self] = newValue }
  }
}
```

如示例所示的三个渐变色块分别对应的是：AView、BView、CView，它们的关系是嵌套的。我们在 AView 实例中注入自定义的环境变量 `userId`：

```swift
AView()
  .environment(\.userId, "zzzwco")
```

然后可以直接在 CView 中获取，而无需通过 BView 层层传递：

```swift
@Environment(\.userId) private var userId

Text(userId)
  .foregroundStyle(
    .linearGradient(
      colors: [.gray, .white, .gray, .white],
      startPoint: .leading,
      endPoint: .trailing
    )
  )
```

### [@EnvironmentObject](https://developer.apple.com/documentation/swiftui/environmentobject)

上面虽然演示了自定义 @Environment 变量，但它实现起来较为繁琐而且只适合传递轻量化数据。所以一般我们使用系统预设的 @Environment 变量，对于需要自定义的环境变量，更推荐使用 @EnvironmentObject 实现。

@EnvironmentObject 和 上面提到的 @StateObject 的使用几乎一样，不过鉴于它是从环境中获取的变量，所以首先需要在视图树中注入它。示例中是在 List 注入的：

```swift
@StateObject private var envWeathersObject = WeathersVM()

List {
  ...
}
.environmentObject(envWeathersObject)
```

然后，在跨层级的视图 SampleEnvironmentValues 中，获取并使用它：

```swift
@EnvironmentObject private var weatherVm: WeathersVM

VStack {
  Text("通过 @EnvironmentObject 注入：")
    .frame(maxWidth: .infinity, alignment: .leading)
  HStack {
    ForEach(weatherVm.weathers.indices, id: \.self) { i in
      Label(
        weatherVm.weathers[i].name,
        systemImage: weatherVm.weathers[i].icon
      )
      Divider()
        .opacity(i == weatherVm.weathers.count - 1 ? 0 : 1)
    }
  }
}
```

> 如果要在导航控制的跳转页面中获取环境变量，需要在 NavigationStack 中注入。
>
> 另外，环境变量在视图层级中是自上向下传递的。如果你在某个子视图重新注入了新的变量，那么它自身以及所有的子视图就会使用这个新的变量。换言之，当前视图使用的环境变量，是离它最近的父视图（包括自身）的变量。
>
> 还有一点值得注意的是，即使在一个视图中只是声明了环境变量而并没有使用它，视图就能够监听到环境变量的状态变化，从而触发视图刷新。[SwiftUI 应用内切换 app 语言](https://www.woter.xyz/blog/ios/swiftui/swiftui-switch-language) 这个示例可以很好地说明这一点。

## 数据持久化

### [@AppStorage](https://developer.apple.com/documentation/swiftui/appstorage)

@AppStorage 可以很方便地读写 [UserDefaults](https://developer.apple.com/documentation/foundation/userdefaults) ，比如示例中的代码：

```swift
@AppStorage("sample_app_text") private var appText = "appText"

TextField("AppStorage", text: $appText)
```

由于 appText 和 TextField 实例进行了绑定，所以当文本内容改变时，appText 会自动保存在 UserDefaults 中。当退出 app 后，重新打开 app 时，文本框内会自动填充之前保存的内容。

这里面有个小细节，使用 @AppStorage 声明的属性值，不一定会写入 UserDefaults。比如上面的 appText 只有代码第一次运行时，才会将 "appText" 写入 UserDefaults。后面再次启动 app 后，appText 会读取 UserDefaults 的值，而不是将 "appText" 赋值给 appText。

@AppStorage 默认写入的是 `UserDefaults.standard`，如果需要自定义存储区域，可以通过 store 参数指定：

```swift
@AppStorage("value", store: UserDefaults(suiteName: "User"))
private var value = ""
```

### [@SceneStorage](https://developer.apple.com/documentation/swiftui/scenestorage)

@AppStorage 只能针对 app 保存一份数据，不适用于多个场景。@SceneStorage 的作用就是为每个场景持久化数据，这些数据独立于各个场景。

另外，SceneStorage 只适合存储轻量的、不敏感的数据，因为当场景销毁时，该值也会销毁，这也是它和 AppStorage 的显著不同。

### [@FetchRequest](https://developer.apple.com/documentation/swiftui/fetchrequest)、[@SectionedFetchRequest](https://developer.apple.com/documentation/swiftui/sectionedfetchrequest)

用于查询 Core Data 数据，后面有空会补充示例加以说明。

## 交互

### [@GestureState](https://developer.apple.com/documentation/swiftui/gesturestate)

@GestureState 用于追踪手势的状态变化。

如示例中所示，dragOffset 绑定在 DragGesture 实例上，当拖拽手势发生变化时，dragOffset 会实时更新，渐变圆圈也会随之移动。

```swift
@GestureState private var dragOffset = CGSize.zero
@State private var position = CGSize.zero

LinearGradient(...)
.offset(
  x: position.width + dragOffset.width,
  y: position.height + dragOffset.height
)
.gesture(
  DragGesture()
    .updating($dragOffset) { (currentState, gestureState, transaction)
      gestureState = currentState.translation
    }
    .onEnded { value in
      // 保存当前位置
      self.position.width += value.translation.width
      self.position.height += value.translation.height
    }
)
```

这里声明了另一个属性 position，用于保存视图的当前位置。因为 @GestureState 变量在手势结束后会重置为初始状态，如果没有使用 position 进行存储，松开手势后，视图无法停留在当前位置。

### [@Namespace](https://developer.apple.com/documentation/swiftui/namespace)

@Namespace 可以创建一个命名空间，主要是给 [matchedGeometryEffect](https://developer.apple.com/documentation/swiftui/text/matchedgeometryeffect(id:in:properties:anchor:issource:)) 用来做动画的。

matchedGeometryEffect 修饰器可以使用简洁的代码实现流畅的动画，该方法有两个必须的核心入参：

- id：视图的身份标识。
- namespace：id 所属的命名空间。

以下是从示例中截取的部分核心代码：

```swift
fileprivate struct SampleNameSpace: View {
  @Namespace private var profileTransition
  @State private var isVertical = false
  
  var body: some View {
    VStack(spacing: 40) {
      if isVertical {
        VStack {
          RoundedRectangle(cornerRadius: 20)
            .matchedGeometryEffect(id: "avatar", in: profileTransition)
            .foregroundColor(.purple)
            .frame(width: 200, height: 200)
          HStack {...}
        }
      } else {
        HStack {
          RoundedRectangle(cornerRadius: 22)
            .matchedGeometryEffect(id: "avatar", in: profileTransition)
            .foregroundColor(.blue)
            .frame(width: 44, height: 44)
          VStack(alignment: .leading) {...}
        }
      }
    }
    .onTapGesture {
      withAnimation(.linear(duration: duration)) {
        isVertical.toggle()
      }
    }
  }
}
```

当点击头像（这里使用 RoundedRectangle 替代）时，matchedGeometryEffect 会根据 id 和 namespace 去找到需要做动画的视图，计算视图的首尾状态的差异，据此添加插值动画。id 这个参数很好理解，通过它才能找到需要做动画的视图。namespace 的存在是为了给 id 的唯一性提供安全保障，因为不同的视图会有被指定为同样 id 的潜在风险，这会使 SwiftUI 变得困惑，无法计算差值动画。所以 matchedGeometryEffect 要求显式传入 id 和 namespace，是为了尽最大可能地消除这种风险。

使用 matchedGeometryEffect 时有个需要注意的地方，尽量在需要做动画的视图后紧接着调用这个修饰器方法。假设将上面的代码调整一下顺序：

```swift
RoundedRectangle(cornerRadius: 20)
  .foregroundColor(.purple)
  .frame(width: 200, height: 200)
  .matchedGeometryEffect(id: "avatar", in: profileTransition)
```

结果令人失望，动画不再平滑。因为 SwiftUI 中的 [frame](https://developer.apple.com/documentation/swiftui/view/frame(width:height:alignment:)) 不同于 UIKit 中的概念，它其实是一个返回 `some View` 的修饰器方法，其作用是向父视图或它所在的容器提供尺寸信息作布局用。改变代码顺序后，matchedGeometryEffect 作用的视图其实不再是 RoundedRectangle 了。

以下代码呈现的 Text 的背景是蓝色的，而紫色背景的尺寸取决于 frame 提供的尺寸信息：

```swift
Text("Hello")
  .background(Color.blue)
  .frame(width: 300, height: 300)
  .background(Color.purple)
```

### [@ScaledMetric](https://developer.apple.com/documentation/swiftui/scaledmetric)

一个可以根据系统设置动态缩放的属性。

如下，使用 @ScaledMetric 变量后，调整系统文字大小（iOS：*设置 > 显式与亮度 > 文字大小*，macOS：*设置 > 显示器 > 缩放分辨率*）后，苹果的 logo 会动态缩放。如果不使用 @ScaledMetric，那么字体的 size 会固定为 60，不具备动态缩放的效果。

```swift
fileprivate struct SampleScaledMetric: View {
  @ScaledMetric private var scaledFontSize = 60
  
  var body: some View {
    Image(systemName: "apple.logo")
      .font(.system(size: scaledFontSize))
  }
}
```

示例还演示了对图片大小进行动态缩放。

### [@FocusState](https://developer.apple.com/documentation/swiftui/focusstate)

@FocusState 可以控制当前程序的焦点，比如示例中的注册界面，只有三个输入框都有值时，才能进行注册操作，如果有输入框没有填写，当点击注册按钮时，会自动激活没有值的输入框。

如果想让键盘消失，可以滑动视图，当激活的输入框要移出屏幕时，键盘会收起。这是因为示例中的 list 做了如下设置：

```swift
List {...}
  .scrollDismissesKeyboard(.interactively)
```

@FocusState 不仅可以作用于 TextField，也可能是一个视图区域，比如在 tvOS 上，它可以聚焦在电视上的某个卡片。

### [@FocusedValue](https://developer.apple.com/documentation/swiftui/focusedvalue)

FocusedValue 和 EnvironmentValue 很像，但是它更灵活，也提供了更多的功能。

EnvironmentValue 和 EnvironmentObject  的注入方式都是从上至下，如果顺序反了，就无法获取到环境变量。而 FocusedValue 不依赖于视图层级的顺序，它可以被全局访问，而且还能监听到绑定的 view 是否处于聚焦状态。

和环境变量一样，首先需要自定义 FocusedValueKey：

```swift
struct FocusedMemoValue: FocusedValueKey {
  typealias Value = String
}

extension FocusedValues {
  var memo: FocusedMemoValue.Value? {
    get { self[FocusedMemoValue.self] }
    set { self[FocusedMemoValue.self] = newValue }
  }
}
```

然后在需要聚焦的视图（MemoInput）上调用 `.focusedValue` 方法注入变量，其它视图（MemoPreview）就可以通过 `@FocusedValue` 访问该变量了。如果视图失去焦点，@FocusedValue 变量会变成 nil。

```swift
fileprivate struct SampleFocusedValue: View {
  
  var body: some View {
    VStack {
      MemoInput()
      MemoPreview()
    }
  }
  
  struct MemoInput: View {
    @State private var memo = "memo"
    
    var body: some View {
      TextField("memo", text: $memo)
        .textFieldStyle(.roundedBorder)
        .focusedValue(\.memo, memo)
    }
  }
  
  struct MemoPreview: View {
    @FocusedValue(\.memo) var memo
    
    var body: some View {
      Text(memo ?? "MemoInput is not focused now.")
        .font(.footnote)
        .foregroundColor(.secondary)
    }
  }
}
```

### [@FocusedBinding](https://developer.apple.com/documentation/swiftui/focusedbinding)

@FocusedValue 是只读的，@FocusedBinding 则是可读写的。

如示例所示，点击 “Reset” 按钮时，可以改变 @FocusedBinding 变量的值。

@FocusedBinding 一般在 mac 上配合快捷键使用，比如示例中添加了如下快捷键：

```swift
struct TestCommands: Commands {
  @FocusedBinding(\.bindingMemo) private var bindingMemo
  
  var body: some Commands {
    CommandMenu("Test") {
      Button("Reset Memo") {
        bindingMemo = "bindingMemo"
      }
      .keyboardShortcut("r", modifiers: [.command, .shift])
      .disabled(bindingMemo == nil)
    }
  }
}
```

在 app 入口处添加快捷键：

```swift
WindowGroup {
  ...
}
#if os(macOS)
.commands {
  TestCommands()
}
#endif
```

该快捷键为 ⌘ + ⇧ + R，在 Eul 的 Mac 版菜单栏的路径为 *Test > Reset Memo*。当你处于示例窗口时，如果 bindingMemo 输入框处于激活状态，使用该快捷键能够重置文本内容。如果 bindingMemo 输入框失去焦点，该快捷键将无法使用，菜单栏中的选项也是置灰的。

### [@FocusedObject](https://developer.apple.com/documentation/swiftui/focusedobject)

熟悉了 EnvironmentValue、EnvironmentObject 以及 FocusedValue 后，就不难理解 FocusedObject 了，此处略过。

## 桥接

在 《生命周期的演变》 中，已经介绍过了，以下略。

### [@UIApplicationDelegateAdaptor](https://developer.apple.com/documentation/swiftui/uiapplicationdelegateadaptor)

### [@NSApplicationDelegateAdaptor](https://developer.apple.com/documentation/swiftui/nsapplicationdelegateadaptor)

### [@WKApplicationDelegateAdaptor](https://developer.apple.com/documentation/swiftui/wkapplicationdelegateadaptor)

### [@WKExtensionDelegateAdaptor](https://developer.apple.com/documentation/swiftui/wkextensiondelegateadaptor)

# 自定义属性包装器

前文提到，属性包装器的作用是将通用的模板代码封装成一种简洁的表达形式。如何实现一个自定义的属性包装器呢？

在此之前，需要先了解一下 `nonmutating` 这个关键字。`mutating` 较为常用的，`nonmutating` 却不常用，这里通过一个简单的示例了解其作用。

```swift
struct ContentView: View {
  private var p = Person(name: "Bruce")
  
  var body: some View {
    Text(p.name)
    .onAppear {
      p.name = "zzzwco"
    }
  }
}

struct Person {
  var name: String
}
```

以上代码无法通过编译，提示错误：

```
❌ Cannot assign to property: 'self' is immutable
```

因为 ContentView 本身也是值类型 struct ，它是不可变对象，所以无法直接修改变量 p。

但是在使用 @State 修饰后，代码却可以成功运行：

```swift
@State private var p = Person(name: "Bruce")
```

这又是为什么呢？在查看 State 的内部结构后，发现 @State 变量的值其实是 wrappedValue，它的定义如下：

```swift
var wrappedValue: Value { get nonmutating set }
```

答案很明显了，在使用 `nonmutating`之后，在不可变环境中对 struct 变量的修改可以通过编译器检查。根据这个思路，对 Person 进行改写：

```swift
final class Ref<T> {
  var val: T
  init(_ v: T) { val = v }
}

struct Person {
  private var _name = Ref("")
  
  var name: String {
    get { _name.val }
    nonmutating set {
      _name.val = newValue
    }
  }
}

let p = Person()
p.name = "zzzwco"
print(p.name) // “zzzwco"
```

经过以上探索，大致可以了解到 `nonmutating` 的作用：修饰 setter 方法使其成为一个可变环境，这保证了值类型实例的无法被随意修改，因此可以通过编译器的检查。

言归正传，我们继续看自定义属性包装器的实现方式。

首先需要使用 `@propertyWrapper` 修饰将属性包装起来的结构体，如下是一个将字符串进行 base64 编码的属性包装器：

```swift
@propertyWrapper
fileprivate struct EncodedBase64 {
  @State private var value: String = ""

  var wrappedValue: String {
    get {
      value
    }
    nonmutating set {
      value = newValue
        .data(using: .utf8)?
        .base64EncodedString() ?? "base64 is nil"
    }
  }
}
```

@propertyWrapper 要求必须实现一个 wrappedValue 属性，这里将其类型声明为 String。由于 value 使用 @State 修饰，所以这里的 wrappedValue 也需要使用 `nonmutating set` 修饰。

到这里为止，已经实现了对字符串进行 base64 编码的功能。但 @EncodedBase64 变量的改变，无法通知 SwiftUI 中的视图进行更新。要实现这个功能，需要让属性包装器遵循 [DynamicProperty](https://developer.apple.com/documentation/swiftui/dynamicproperty) 协议：

```swift
fileprivate struct EncodedBase64: DynamicProperty {
  ...
}
```

DynamicProperty 协议无需实现任何属性或方法，它有个默认的实现方法 `update()`，其作用就是在 SwiftUI 重新计算 view 的 body 属性进行视图重绘之前，将最新的属性值传递至相应的 view。当然，我们可以根据实际需要在这个方法内进行一些附加操作。

至此，一个自定义的属性包装器已基本实现。以下是使用示例：

```swift
fileprivate struct SampleCustomPropertyWrappers: View {
  @State private var text = ""
  @EncodedBase64 private var base64Text
  
  var body: some View {
    VStack(alignment: .leading) {
      TextField("", text: $text)
        .textFieldStyle(.roundedBorder)
      Text("Base64: \(base64Text)")
    }
    .onChange(of: text) { newValue in
      base64Text = newValue
    }
  }
}
```

但这还不够，因为 @EncodedBase64 不具备双向绑定的特性。方法很简单，只需实现一个 `projectedValue` ：

```swift
var projectedValue: Binding<String> {
  .init {
    wrappedValue
  } set: {
    wrappedValue = $0
  }
}
```

使用效果见示例。






---

> 作者: 宋明  
> URL: https://apolla.cc/posts/swiftui-eul/1.5-swiftui-%E4%B8%AD%E7%9A%84%E5%B1%9E%E6%80%A7%E5%8C%85%E8%A3%85%E5%99%A8/  

