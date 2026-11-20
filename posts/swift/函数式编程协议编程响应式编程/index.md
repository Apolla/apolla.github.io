# 函数式编程、协议编程、响应式编程


### 1、函数式编程

##### 1、Array 常见方法

```swift
var arr = [1, 2, 3, 4]

var arr2 = arr.map { $0 * 2 }

var arr3 = arr.filter { $0 % 2 == 0 }

var arr4 = arr.reduce(0) { $0 + $1 }

var arr5 = arr.reduce(0, +) 
```

```swift
func double(_ i: Int) -> Int { i * 2 }
var arr = [1, 2, 3, 4]

print(arr.map(double)) 
```

```swift
var arr = [1, 2, 3]

var arr2 = arr.map { Array.init(repeating: $0, count: $0) }

var arr3 = arr.flatMap { Array.init(repeating: $0, count: $0) } 
```

```swift
var arr = ["123", "test", "jack", "-30"]

var arr2 = arr.map { Int($0) }

var arr3 = arr.compactMap { Int($0) } 
```

```swift
// 使用reduce实现map、filter的功能
var arr = [1, 2, 3, 4]
// [2, 4, 6, 8]
print(arr.map { $0 * 2 })
print(arr.reduce([]) { $0 + [$1 * 2] })
// [2, 4]
print(arr.filter { $0 % 2 == 0 })
print(arr.reduce([]) { $1 % 2 == 0 ? $0 + [$1] : $0 }) 
```

##### 2、lazy 的优化

```swift
let arr = [1, 2, 3]
let result = arr.lazy.map { (i: Int) -> Int in
    print("mapping \(i)")
    return i * 2
}
print("begin-----")
print("mapped", result[0])
print("mapped", result[1])
print("mapped", result[2])
print("end----")

begin-----
mapping 1
mapped 2
mapping 2
mapped 4
mapping 3
mapped 6
end---- 
```

##### 3、Optional 的 map 和 flatMap

```swift
var num1: Int? = 10

var num2 = num1.map { $0 * 2 }
var num3: Int? = nil

var num4 = num3.map { $0 * 2 } 
```

```swift
var num1: Int? = 10

var num2 = num1.map { Optional.some($0 * 2) }

var num3 = num1.flatMap { Optional.some($0 * 2) } 
```

```swift
var num1: Int? = 10
var num2 = (num1 != nil) ? (num1! + 10) : nil
var num3 = num1.map { $0 + 10 } 
```

```swift
var fmt = DateFormatter()
fmt.dateFormat = "yyyy-MM-dd"
var str: String? = "2011-09-10"

var date1 = str != nil ? fmt.date(from: str!) : nil

var date2 = str.flatMap(fmt.date) 
```

```swift
var score: Int? = 98

var str1 = score != nil ? "socre is \(score!)" : "No score"

var str2 = score.map { "score is \($0)" } ?? "No score" 
```

```swift
struct Person {
    var name: String
    var age: Int
}
var items = [
    Person(name: "jack", age: 20),
    Person(name: "rose", age: 21),
    Person(name: "kate", age: 22)
]

func getPerson1(_ name: String) -> Person? {
    let index = items.firstIndex { $0.name == name }
    return index != nil ? items[index!] : nil
}

func getPerson2(_ name: String) -> Person? {
    return items.firstIndex { $0.name == name }.map { items[$0] }
} 
```

```swift
struct Person {
    var name: String
    var age: Int
    init?(_ json: [String : Any]) {
        guard let name = json["name"] as? String, let age = json["age"] as? Int else {
            return nil
        }
        self.name = name
        self.age = age
    }
}
var json: Dictionary? = ["name" : "Jack", "age" : 10]

var p1 = json != nil ? Person(json!) : nil

var p2 = json.flatMap(Person.init) 
```

##### 4、函数式编程

函数式编程（Funtional Programming，简称FP）是一种编程范式，也就是如何编写程序的方法论。  
主要思想：`把计算过程尽量分解成一系列可复用函数的调用`。  
主要特征：函数是`第一等公民`。函数与其他数据类型一样的地位，可以赋值给其他变量，也可以作为函数参数、函数返回值。

函数式编程中几个常用的概念：Higher-Order Function、Function Currying、Functor、Applicative Functor、Monad。

**示例**

```swift
 var num = 1
func add(_ v1: Int, _ v2: Int) -> Int { v1 + v2 }
func sub(_ v1: Int, _ v2: Int) -> Int { v1 - v2 }
func multiple(_ v1: Int, _ v2: Int) -> Int { v1 * v2 }
func divide(_ v1: Int, _ v2: Int) -> Int { v1 / v2 }
func mod(_ v1: Int, _ v2: Int) -> Int { v1 % v2 }
divide(mod(sub(multiple(add(num, 3), 5), 1), 10), 2) 
```

**函数式编程**

```swift
func add(_ v: Int) -> (Int) -> Int { { $0 + v } }
func sub(_ v: Int) -> (Int) -> Int { { $0 - v } }
func multiple(_ v: Int) -> (Int) -> Int { { $0 * v } }
func divide(_ v: Int) -> (Int) -> Int { { $0 / v } }
func mod(_ v: Int) -> (Int) -> Int { { $0 % v } } 
```

```swift
infix operator >>> : AdditionPrecedence
func >>><A, B, C>(_ f1: @escaping (A) -> B, _ f2: @escaping (B) -> C) -> (A) -> C { { f2(f1($0)) } }

var fn = add(3) >>> multiple(5) >>> sub(1) >>> mod(10) >>> divide(2)
fn(num) 
```

**高阶函数**  
接受一个或多个函数作为参数（如：map、filter、reduce 等）或者返回值是一个函数。

```swift
func add(_ v: Int) -> (Int) -> Int { { $0 + v } } 
```

**柯里化（Currying）**  
将一个接受多参数的函数变换为一系列只接受单个参数的函数。

```swift
 func add(_ v1: Int, _ v2: Int) -> Int { v1 + v2 }
add(10, 20)

func add(_ v: Int) -> (Int) -> Int { { $0 + v } }
add(10)(20) 
```

Array、Optional 的 map 方法接收的参数就是一个柯里化函数。

```swift
 func add1(_ v1: Int, _ v2: Int) -> Int { v1 + v2 }
func add2(_ v1: Int, _ v2: Int, _ v3: Int) -> Int { v1 + v2 + v3 }
func currying<A, B, C>(_ fn: @escaping (A, B) -> C) -> (B) -> (A) -> C {
    { b in { a in fn(a, b) } }
}
func currying<A, B, C, D>(_ fn: @escaping (A, B, C) -> D) -> (C) -> (B) -> (A) -> D { { c in { b in { a in fn(a, b, c) } } } }
let curriedAdd1 = currying(add1)
print(curriedAdd1(10)(20))
let curriedAdd2 = currying(add2)
print(curriedAdd2(10)(20)(30)) 
```

```swift
func add(_ v1: Int, _ v2: Int) -> Int { v1 + v2 }
func sub(_ v1: Int, _ v2: Int) -> Int { v1 - v2 }
func multiple(_ v1: Int, _ v2: Int) -> Int { v1 * v2 }
func divide(_ v1: Int, _ v2: Int) -> Int { v1 / v2 }
func mod(_ v1: Int, _ v2: Int) -> Int { v1 % v2 }

prefix func ~<A, B, C>(_ fn: @escaping (A, B) -> C) -> (B) -> (A) -> C { { b in { a in fn(a, b) } } }

infix operator >>> : AdditionPrecedence
func >>><A, B, C>(_ f1: @escaping (A) -> B, _ f2: @escaping (B) -> C) -> (A) -> C { { f2(f1($0)) } }

var num = 1
var fn = (~add)(3) >>> (~multiple)(5) >>> (~sub)(1) >>> (~mod)(10) >>> (~divide)(2)
fn(num) 
```

**函子**  
像 Array、Optional 这样支持 map 运算的类型，称为函子（Functor）。

```swift
 public func map<T>(_ transform: (Element) -> T) -> Array<T>

public func map<U>(_ transform: (Wrapped) -> U) -> Optional<U> 
```

**适用函子（Applicative Functor）**  
对任意一个函子 F，如果能支持以下运算，该函子就是一个适用函子。

```
func pure<A>(_ value: A) -> F<A>
func <*><A, B>(fn: F<(A) -> B>, value: F<A>) -> F<B> 
```

1、Optional 可以成为适用函子

```swift
func pure<A>(_ value: A) -> A? { value }
infix operator <*> : AdditionPrecedence
func <*><A, B>(fn: ((A) -> B)?, value: A?) -> B? {
    guard let f = fn, let v = value else { return nil }
    return f(v)
}

var value: Int? = 10
var fn: ((Int) -> Int)? = { $0 * 2}

print(fn <*> value as Any) 
```

2、Array 可以成为适用函子

```swift
func pure<A>(_ value: A) -> [A] { [value] }
func <*><A, B>(fn: [(A) -> B], value: [A]) -> [B] {
    var arr: [B] = []
    if fn.count == value.count {
        for i in fn.startIndex..<fn.endIndex {
            arr.append(fni)
        }
    }
    return arr
}

print(pure(10))  
var arr = [{ $0 * 2}, { $0 + 10 }, { $0 - 5 }] <*> [1, 2, 3]
print(arr) 
```

**单子（Monad）**  
对任意一个类型 F，如果能支持以下运算，那么就可以称为是一个单子（Monad）。很显然，Array、Optional 都是单子。

```swift
func pure<A>(_ value: A) -> F<A>
func flatMap<A, B>(_ value: F<A>, _ fn: (A) -> F<B>) -> F<B> 
```

### 2、面向协议编程

面向协议编程（Protocol Oriented Programming，简称 POP），Swift 既是一门面向协议编程语言也是一门面向对象的编程语言（Object Oriented Programming，简称 OOP）。在 Swift 开发中，OOP 和 POP 是相辅相成的，任何一方并不能取代另一方，POP 能弥补 OOP 一些设计上的不足。

##### 1、OOP

OOP 的三大特性：封装、继承、多态。  
OOP 的不足：会导致公共类越来越臃肿。

##### 2、POP

**使用特点**  
1、优先考虑创建协议，而不是父类（基类）。  
2、优先考虑值类型（struct、enum），而不是引用类型（class）。  
3、巧用协议的扩展功能。  
4、不要为了面向协议而使用协议。

**利用协议实现前缀效果**

```swift
var string = "123fdsf434"
print(string.mj.numberCount()) 
```

```swift
struct MJ<Base> {
    let base: Base
    init(_ base: Base) {
        self.base = base
    }
}
protocol MJCompatible {}
extension MJCompatible {
    static var mj: MJ<Self>.Type {
        get { MJ<Self>.self }
        set {}
    }
    var mj: MJ<Self> {
        get { MJ(self) }
        set {}
    }
} 
```

```swift
extension String: MJCompatible {}
extension MJ where Base == String {
    func numberCount() -> Int {
        var count = 0
        for c in base where ("0"..."9").contains(c) {
            count += 1
        }
        return count
    }
} 
```

**Base: 类**

```swift
class Person {}
class Student: Person {}
extension Person: MJCompatible {}
extension MJ where Base: Person {
    func run() {}
    static func test() {}
} 
```

```swift
Person.mj.test()
Student.mj.test()
let p = Person()
p.mj.run()
let s = Student()
s.mj.run() 
```

**Base: 协议**

```swift
var s1: String = "123fdsf434"
var s2: NSString = "123fdsf434"
var s3: NSMutableString = "123fdsf434"
print(s1.mj.numberCount())
print(s2.mj.numberCount())
print(s3.mj.numberCount()) 
```

```swift
extension String: MJCompatible {}
extension NSString: MJCompatible {}
extension MJ where Base: ExpressibleByStringLiteral {
    func numberCount() -> Int {
        let string = base as! String
        var count = 0
        for c in string where ("0"..."9").contains(c) {
            count += 1
        }
        return count
    }
} 
```

**利用协议实现类型判断**

```swift
func isArray(_ value: Any) -> Bool { value is [Any] }
isArray( [1, 2] )
isArray( ["1", 2] )
isArray( NSArray() )
isArray( NSMutableArray() ) 
```

```swift
protocol ArrayType {}
extension Array: ArrayType {}
extension NSArray: ArrayType {}
func isArrayType(_ type: Any.Type) -> Bool { type is ArrayType.Type }
isArrayType([Int].self)
isArrayType([Any].self)
isArrayType(NSArray.self)
isArrayType(NSMutableArray.self) 
```

### 3、响应式编程

响应式编程（Reactive Programming，简称RP），是一种编程范式，可以简化异步编程，提供更优雅的数据绑定。一般与函数式融合在一起，所以也会叫做：函数响应式编程（Functional Reactive Programming，简称FRP）。如：  
ReactiveCocoa：简称 RAC，有 Objective-C、Swift 版本。  
ReactiveX：简称 Rx，有众多编程语言的版本，比如 RxJava、RxKotlin、RxJS、RxCpp、RxPHP、RxGo、RxSwift 等等。

##### 1、RxSwift

RxSwift（ReactiveX for Swift），ReactiveX 的 Swift 版本。主要包含以下模块：  
RxSwift：Rx 标准 API 的 Swift 实现，不包括任何 iOS 相关的内容。  
RxCocoa：基于 RxSwift，给 iOS UI 控件扩展了很多 Rx 特性。

**RxSwift 的核心角色**  
Observable：负责发送事件（Event）。  
Observer：负责订阅 Observable，监听 Observable 发送的事件（Event）。  

![](https://upload-images.jianshu.io/upload_images/1742120-c2d76e755060af38.png)

事件流程

```swift
public enum Event<Element> {
    
    case next(Element)
    
    case error(Swift.Error)
    
    case completed
} 
```

Event 有 3 种  
next：携带具体数据。  
error：携带错误信息，表明 Observable 终止，不会再发出事件。  
completed：表明 Observable 终止，不会再发出事件。

**创建、订阅 Observable**

```swift
var observable = Observable<Int>.create { observer in
    observer.onNext(1)
    observer.onCompleted()
    return Disposables.create()
}

observable = Observable.just(1)
observable = Observable.of(1)
observable = Observable.from([1]) 
```

```swift
var observable = Observable<Int>.create { observer in
    observer.onNext(1)
    observer.onNext(2)
    observer.onNext(3)
    observer.onCompleted()
    return Disposables.create()
}

observable = Observable.of(1, 2, 3)
observable = Observable.from([1, 2, 3]) 
```

```swift
observable.subscribe { event in
    print(event)
}.dispose() 
```

```swift
observable.subscribe(onNext: {
    print("next", $0)
}, onError: {
    print("error", $0)
}, onCompleted: {
    print("completed")
}, onDisposed: {
    print("dispose")
}).dispose() 
```

```swift
let observable = Observable<Int>.timer(.seconds(3), period: .seconds(1), scheduler: MainScheduler.instance)
observable.map { "数值是\($0)" }
          .bind(to: label.rx.text)
          .disposed(by: bag) 
```

**创建 Observer**

```swift
let observer = AnyObserver<Int>.init { event in
    switch event {
    case .next(let data):
        print(data)
    case .completed:
        print("completed")
    case .error(let error):
        print("error", error)
    }
}
Observable.just(1).subscribe(observer).dispose() 
```

```swift
let binder = Binder<String>(label) { label, text in
    label.text = text
}
Observable.just(1).map { "数值是\($0)" }.subscribe(binder).dispose()
Observable.just(1).map { "数值是\($0)" }.bind(to: binder).dispose() 
```

**扩展 Binder 属性**

```swift
extension Reactive where Base: UIView {
    var hidden: Binder<Bool> {
        Binder<Bool>(base) { view, value in
            view.isHidden = value
        }
    }
} 
```

```swift
let observable = Observable<Int>.interval(.seconds(1), scheduler: MainScheduler.instance)
observable.map { $0 % 2 == 0 }.bind(to: button.rx.hidden).disposed(by: bag) 
```

**传统的状态监听方案**  
KVO、Target-Action、Notification、Delegate、Block Callback  
缺点：错综复杂的依赖关系，耦合性较高，编写重复的非业务代码。

**RxSwift 的状态监听**

```swift
button.rx.tap.subscribe(onNext: {
    print("按钮被点击了1")
}).disposed(by: bag) 
```

```swift
let data = Observable.just([
    Person(name: "Jack", age: 10),
    Person(name: "Rose", age: 20)
])

data.bind(to: tableView.rx.items(cellIdentifier: "cell")) { row, person, cell in
    cell.textLabel?.text = person.name
    cell.detailTextLabel?.text = "\(person.age)"
}.disposed(by: bag)

tableView.rx.modelSelected(Person.self)
            .subscribe(onNext: { person in
                print("点击了", person.name)
            }).disposed(by: bag) 
```

```swift
class Dog: NSObject {
    @objc dynamic var name: String?
}
dog.rx.observe(String.self, "name")
   .subscribe(onNext: { name in
        print("name is", name ?? "nil")
   }).disposed(by: bag)
dog.name = "larry"
dog.name = "wangwang" 
```

```swift
NotificationCenter.default.rx
    .notification(UIApplication.didEnterBackgroundNotification)
    .subscribe(onNext: { notification in
        print("APP进入后台", notification)
    }).disposed(by: bag) 
```

**既是 Observable，又是 Observer**

```swift
Observable.just(0.8).bind(to: slider.rx.value).dispose() 
```

```swift
slider.rx.value.map {
    "当前数值是：\($0)"
}.bind(to: textField.rx.text).disposed(by: bag) 
```

```swift
textField.rx.text
    .subscribe(onNext: { text in
        print("text is", text ?? "nil")
    }).disposed(by: bag) 
```

诸如 UISlider.rx.value、UTextField.rx.text 这类属性值，既是 Observable，又是 Observer，它们是 RxCocoa.ControlProperty 类型。

**Disposable**  
每当 Observable 被订阅时，都会返回一个 Disposable 实例，当调用 Disposable 的 dispose，就相当于取消订阅。在不需要再接收事件时，建议取消订阅，释放资源。有 3 种常见方式取消订阅：

```swift
 observable.subscribe { event in
    print(event)
}.dispose() 
```

```swift
 observable.subscribe { event in
    print(event)
}.disposed(by: bag) 
```

```swift
 let _ = observable.takeUntil(self.rx.deallocated).subscribe { event in
    print(event)
} 
```




---

> 作者: 宋明  
> URL: https://apolla.cc/posts/swift/%E5%87%BD%E6%95%B0%E5%BC%8F%E7%BC%96%E7%A8%8B%E5%8D%8F%E8%AE%AE%E7%BC%96%E7%A8%8B%E5%93%8D%E5%BA%94%E5%BC%8F%E7%BC%96%E7%A8%8B/  

