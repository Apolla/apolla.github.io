# Error


## 自定义错误
* Swift中可以通过Error协议自定义运行时的错误信息
* 函数内部通过throw抛出自定义Error，可能会抛出Error的函数必须加上throws声明
* 需要使用try调用可能会抛出Error的函数
```swift
enum SomeError : Error {
    case illegalArg(String)
    case outOfBounds(Int, Int)
    case outOfMemory

}

func divide(_ num1: Int, _ num2: Int) throws -> Int {

    if num2 == 0 {
        throw SomeError.illegalArg("0不能作为除数")
    }
    return num1 / num2
}

 var value = try divide(20,10)
```

## do-catch 捕捉异常
> 抛出Error后， try下一句直到作用域结束的代码都将停止运行
```swift
func test() {

    print("1")

    do {
        print("2")
        print(try divide(200, 0))
        print("3")
    } catch let SomeError.illegalArg(msg) {
        print("参数异常:", msg)
    } catch let SomeError.outOfBounds(size, index) {
        print("下标越界:", "size=\(size)", "index=\(index)")
    } catch SomeError.outOfMemory {
        print("内存溢出")
    } catch {
        print("其他错误")
    }
    print("4")
}

test()
```

## 处理Error
处理Error的2种方式
* 通过do-catch捕捉Error
* 不捕捉Error，在当前函数增加throws声明， Error将自动抛给上层函数,如果最顶层函数（ main函数）依然没有捕捉Error，那么程序将终止
!

## try?、 try!
可以使用`try?`、 `try!`调用可能会抛出Error的函数，这样就不用去处理Error
!

## rethrows
`rethrows`表明：函数本身不会抛出错误，但调用闭包参数抛出错误，那么它会将错误向上抛
!


---

> 作者: 宋明  
> URL: https://apolla.cc/posts/swift/error/  

