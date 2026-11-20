# 3：Mac地址的获取及写入指令的处理


## Mac地址的获取
iOS7之后，苹果不支持获取Mac地址，只能用UUID来标识设备。若想获得Mac地址，可以跟硬件工程师沟通，增加一个指令获取，也可以让硬件工程师把Mac地址写到广播包里，在扫描的时候获取Mac地址，如下所示：
```swift
 func centralManager(_ central: CBCentralManager,
                        didDiscover peripheral: CBPeripheral,
                        advertisementData: [String: Any],
                        rssi RSSI: NSNumber)
{
// 在 advertisementData里读取，获取的manufacturerData是二进制数据，需要转换成UInt8数据，然后根据约定的格式解析成Mac地址。
let data = advertisementData["kCBAdvDataManufacturerData"] as? Data {             
  let macString = BlueUtil.getIOSMacString(data:UInt8 )
// FD:00:EA:00:85:9C
}
```
## 写入数据的处理
调用writeValue写入指令，可以看到，需要把指令转换成Data 数据。譬如217, 162, 3, 25, 188, 153。
```swift
 open func writeValue(_ data: Data, for characteristic: CBCharacteristic, type: CBCharacteristicWriteType)
// 对应的回调代理
 @objc func peripheral(_ peripheral: CBPeripheral, didWriteValueFor characteristic: CBCharacteristic, error: Error?) {
}
```
跟硬件交互涉及到大小端的问题。大端模式，是指数据的高字节保存在内存的低地址中，而数据的低字节保存在内存的高地址中。小端模式，是指数据的高字节保存在内存的高地址中，而数据的低字节保存在内存的低地址中，有兴趣的具体见[大小端](https://link.juejin.cn/?target=https%3A%2F%2Fblog.csdn.net%2Fmolaifeng%2Farticle%2Fdetails%2F117258030)。
```swift
    // 数据转换
   private func converSendData(send :[Int]) -> Data {
        
        var result = Data()
        for i in send {
            var bts = [i]
            let data = Data(bytes: &bts, count: 1)
            result.append(data)
        }
        return result
    }
```
需要注意的是使用Data(bytes: UnsafeRawPointer, count: Int)时，一定要注意传入的count,最后生成的二进制数据要符合硬件的要求(蓝牙一次能写入的最大数据为20bytes),否则写入失败。



---

> 作者: 宋明  
> URL: https://apolla.cc/posts/bluetooth/3mac%E5%9C%B0%E5%9D%80%E7%9A%84%E8%8E%B7%E5%8F%96%E5%8F%8A%E5%86%99%E5%85%A5%E6%8C%87%E4%BB%A4%E7%9A%84%E5%A4%84%E7%90%86/  

