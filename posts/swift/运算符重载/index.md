# 运算符重载


在C++中, 运算符是可以重载的, Swift也是支持的

**注：`=`和三目运算符`a ? b : c`不可重载**

**重载双目运算符**

```swift
class Vector {
    var x: Double = 0.0
    var y: Double = 0.0
    var z: Double = 0.0
    
    init(x: Double, y: Double, z: Double) {
        self.x = x
        self.y = y
        self.z = z
    }
    
    convenience init() {
        self.init(x: 0, y: 0, z: 0) 
    }
    
    
    
    static func +(v1: Vector, v2: Vector) -> Vector {
        let vector: Vector = Vector()
        vector.x = v1.x + v2.x
        vector.y = v1.y + v2.y
        vector.z = v1.z + v2.z
        return vector
    }
} 
```

**单目运算符**

类和结构体也可以实现单目运算符，单目运算符只运算一个值。  
运算符出现在值之前为前缀运算符(prefix, 如 -a)，出现在值之后为后缀运算符(postfix, 如a!)。

```swift
struct Coordinate {
    var x: Double = 0.0
    var y: Double = 0.0
    
    static prefix func +(coordinate: Coordinate) -> Coordinate {
        return Coordinate(x: +coordinate.x, y: +coordinate.y)
    }
    
    static prefix func -(coordinate: Coordinate) -> Coordinate {
        return Coordinate(x: -coordinate.x, y: -coordinate.y)
    }
}

func test() {
    let p1 = Coordinate(x: 1.0, y: 1.0)
    let p2 = Coordinate(x: 2.0, y: 2.0)
    print(-p1) 
    print(+p2) 
} 
```

**复合赋值运算符**

复合赋值运算符是赋值运算符（=）和其他运算符进行结合, 如 +=、-=

```swift
struct Coordinate {
    var x: Double = 0.0
    var y: Double = 0.0
    
    
    static func +=(left: inout Coordinate, right: Coordinate) {
        left = Coordinate(x: left.x + right.x, y: left.y + right.y)
    }
    
    static func -=(c1: inout Coordinate, c2: Coordinate) {
        left = Coordinate(x: left.x - right.x , y: left.y - right.y)
    }
}

func test() {
    var p1 = Coordinate(x: 1.0, y: 1.0)
    let p2 = Coordinate(x: 2.0, y: 2.0)
    p1 += p2
    print(p1) 
} 
```

**等价运算符 ==**

自定义类和结构体没有对等价运算符进行默认的实现。等价运算符一般被称为相等运算符`==`和不等运算符 `!=`

```swift
struct Coordinate {
    var x: Double = 0.0
    var y: Double = 0.0
    
    static func ==(c1: Coordinate, c2: Coordinate) -> Bool {
        return c1.x == c2.x && c1.y == c2.y
    }
    
    static func !=(left: Coordinate, right: Coordinate) -> Bool {
        return left.x != right.x || left.y != right.y
    }
}

func test() {
    let p1 = Coordinate(x: 1.0, y: 1.0)
    var p2 = Coordinate(x: 2.0, y: 2.0)
    
    print(p1 == p2) 
    p2.x -= 1
    p2.y -= 1
    print(p1 == p2) 
} 
```

**自定义运算符**

可以自定义前置运算符prefix、后置运算符postfix、中置运算符infix, 约束条件：

1.  只能使用如下字符：  
    `- + * / = % < > ! & | ^ . ~`
2.  只有中置运算符可以继承优先级组 precdence(后面介绍)
3.  自定义运算符不可放在类中，必须放在文件作用域中

自定义后置运算符
```swift
struct Coordinate {
    var x: Double = 0.0
    var y: Double = 0.0
}

prefix operator +++
prefix func +++(coordinate: inout Coordinate) -> Coordinate {
    coordinate.x = coordinate.x + coordinate.x
    coordinate.y = coordinate.y + coordinate.y
    return coordinate
}

func test() {
    var p1 = Coordinate(x: 1.0, y: 1.0)
    print(+++p1) 
} 
```

自定义前置运算符和自定义后置运算符类似
```swift
postfix operator +++
postfix func +++(coordinate: inout Coordinate) -> Coordinate {
    coordinate.x = coordinate.x + coordinate.x
    coordinate.y = coordinate.y + coordinate.y
    return coordinate
} 
```

自定义中置运算符

```swift
precedencegroup MyPrecedence {
    
    lowerThan: AdditionPrecedence       
    associativity: none                 
    assignment: false                   
}

infix operator +++ : MyPrecedence  
func +++(left: Int, right: Int) -> Int {
    return (left + right) * 2
}

func test() {
    print(3+++2)
} 
```

借助自定义运算符，我们可以浪一浪，定义一个操作符，当有值是使用此值，无值时使用想要的默认值，如下所示：
```swift
postfix operator <<<
postfix func <<<(a: String?) -> String { return a ?? "" }

func test() {
    print(getStr()<<<)
}

func getStr() -> String? {
    return nil
} 
```

示例

```swift
postfix operator <<<

postfix func <<<(a: String?)              -> String              { return a ?? "" }
postfix func <<<(a: Int?)                 -> Int                 { return a ?? 0 }
postfix func <<<(a: Int8?)                -> Int8                { return a ?? 0 }
postfix func <<<(a: Int16?)               -> Int16               { return a ?? 0 }
postfix func <<<(a: Int32?)               -> Int32               { return a ?? 0 }
postfix func <<<(a: Int64?)               -> Int64               { return a ?? 0 }
postfix func <<<(a: UInt?)                -> UInt                { return a ?? 0 }
postfix func <<<(a: Double?)              -> Double              { return a ?? 0.0 }
postfix func <<<(a: Float?)               -> Float               { return a ?? 0.0 }
postfix func <<<(a: [AnyObject]?)         -> [AnyObject]         { return a ?? [] }
postfix func <<<(a: [String]?)            -> [String]            { return a ?? [] }
postfix func <<<(a: [Int]?)               -> [Int]               { return a ?? [] }
postfix func <<<(a: [String: AnyObject]?) -> [String: AnyObject] { return a ?? [:]}
postfix func <<<(a: [String: String]?)    -> [String: String]    { return a ?? [:] } 
```



---

> 作者: 宋明  
> URL: https://apolla.cc/posts/swift/%E8%BF%90%E7%AE%97%E7%AC%A6%E9%87%8D%E8%BD%BD/  

