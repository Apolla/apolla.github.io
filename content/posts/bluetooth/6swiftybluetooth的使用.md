---
title: "6：SwiftyBluetooth的使用"
date: 2024-03-09T23:21:58+08:00
lastmod: 2024-03-09T23:21:58+08:00
draft: false
categories: ["蓝牙"]
tags: ["SwiftyBluetooth", "Swift", "CoreBluetooth"]
---

# 简介
`SwiftyBluetooth`是`Swift`中封装`CoreBluetooth`框架的一个开源库[SwiftyBluetooth](https://link.juejin.cn?target=https%3A%2F%2Fgithub.com%2Fjordanebelanger%2FSwiftyBluetooth),个人觉得比较好用，是对`CoreBluetooth`的封装，可自行查看代码，下面来讲讲它的使用。 
## 首先需要判断蓝牙打开的状态，蓝牙打开了才可进行下一步：
```swift
     SwiftyBlutooth.asyncState { state in
            switch state {
            case .poweredOn:
                print("蓝牙打开了,去搜索要连接设备")
             break

            case .poweredOff:
                print("蓝牙未打开，添加提示")
                break
            default:
                break

            }
        }
```
# 第二步，搜索蓝牙设备
```swift
// withServiceUUIDs：需要搜索的设备`CBUUID`数组，默认为nil,则搜索附近所有的蓝牙设备，浪费时间，所以最好传入`[CBUUIDConvertible]`
// timeoutAfter 搜索时长
SwiftyBluetooth.scanForPeripherals(withServiceUUIDs: nil, timeoutAfter: 15) { scanResult in
    switch scanResult {
        case .scanStarted:
            // The scan started meaning CBCentralManager scanForPeripherals(...) was called 
        case .scanResult(let peripheral, let advertisementData, let RSSI):
            // 解析`advertisementData`,找到要连接的设备，然后连接设备 
            self.peripheral = peripheral
        case .scanStopped(let error):
            // The scan stopped, an error is passed if the scan stopped unexpectedly
    }
}        
```
# 第三步，连接设备
```swift
   guard let peripheral = self.peripheral  else { return }
        // 开始连接设备
   peripheral.connect(withTimeout: time) {  result in
            switch result {
            case .success:  
                //连接成功,
                break      
            case .failure(let error):
                break
            }
        }
```
设备连接成功后，就可以进行readValue、setNotifyValue、writeValue的操作了，有不明白的同学可参考我[这篇文章](https://www.yuque.com/wuniansuogui/lkz693/gzcyw8hamzfq5swn)剩余常用的API如下：
```swift
peripheral.discoverServices(withUUIDs: nil) { result in
    switch result {
    case .success(let services):
        break // An array containing all the services requested
    case .failure(let error):
        break // A connection error or an array containing the UUIDs of the services that we're not found
    }
}
peripheral.discoverCharacteristics(withUUIDs: nil, ofServiceWithUUID: "180A") { result in
    // The characteristics discovered or an error if something went wrong.
    switch result {
    case .success(let services):
        break // An array containing all the characs requested.
    case .failure(let error):
        break // A connection error or an array containing the UUIDs of the charac/services that we're not found.
    }
}
```

