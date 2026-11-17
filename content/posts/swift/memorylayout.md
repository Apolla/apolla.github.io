---
title: "MemoryLayout"
date: 2024-04-09T14:44:05+08:00
lastmod: 2024-04-09T14:44:05+08:00
draft: false
categories: ["Swift"]
weight: 5
---

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
