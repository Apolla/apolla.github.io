# 基础语法


  > 用var定义变量，let定义常量，编译器能自动推断出变量\常量的类型

## 常量
1. 只能赋值1次
2. 它的值不要求在编译时期确定，但使用之前必须赋值1次
!
## 常见数据类型
!
## 字面量
!

## 元祖
```swift

let error = (404, "Not Found")
print("code is\(error.0) message is \(error.1)")
  

let (code,msg) = error
print("code is\(code) message is \(msg)")

  

let httpResponse = (code:200,msg:"请求成功")
print("code is\(httpResponse.code) message is \(httpResponse.msg)")
```
 



---

> 作者: 宋明  
> URL: https://apolla.cc/posts/swift/%E5%9F%BA%E7%A1%80%E8%AF%AD%E6%B3%95/  

