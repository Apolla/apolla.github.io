# MemoryLayout


> 可以使用MemoryLayout获取数据类型占用的内存大小
```swift
enum Password {

    case number(Int, Int, Int, Int) // 32

    case other

}

var pwd = Password.number(5, 6, 4, 7) // 33
pwd = .other // 0

MemoryLayout<Password>.size // 33
MemoryLayout<Password>.stride // 40
MemoryLayout<Password>.alignment // 8
```


---

> 作者: 宋明  
> URL: https://apolla.cc/posts/swift/memorylayout/  

