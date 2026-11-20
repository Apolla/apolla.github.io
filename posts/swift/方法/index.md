# 方法


* 枚举、结构体、类都可以定义实例方法、类型方法
	* 实例方法（ Instance Method）： 通过实例对象调用
	* 类型方法（ Type Method）： 通过类型调用，用static或者class关键字定义
!

## mutating
* 结构体和枚举是值类型，默认情况下，值类型的属性不能被自身的实例方法修改
*  在func关键字前加mutating可以允许这种修改行为
!

## @discardableResult
> 在func前面加个`@discardableResult`  ， 可以消除：函数调用后返回值未被使用的警告⚠
!


---

> 作者: 宋明  
> URL: https://apolla.cc/posts/swift/%E6%96%B9%E6%B3%95/  

