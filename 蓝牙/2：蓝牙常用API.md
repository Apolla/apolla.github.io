上篇讲了蓝牙相关的基本概念，现在结合代码讲讲具体实现。首先需要创建一个CBCentralManager对象，检查蓝牙的状态，只有蓝牙为poweredOn状态，才可进行下一步连接动作。
### CBCentralManager 初始化

```swift
//先导入`CoreBluetooth` 框架
 var centralManager: CBCentralManager!
    //设置deleagte、queue、可选参数options，options可以为nil,也可设置CBCentralManagerOptionShowPowerAlertKey蓝牙提醒弹窗和CBCentralManagerOptionRestoreIdentifierKey字符串(一个唯一的标识符，用来恢复蓝牙连接的，在后台的长连接中可能用到)
    override init() {
        super.init()
        
        self.centralManager = CBCentralManager(delegate: self, queue: nil)
    }
    
    init(stateRestoreIdentifier: String) {
        super.init()
        
        self.centralManager = CBCentralManager(delegate: self, queue: nil, options: [CBCentralManagerOptionRestoreIdentifierKey: stateRestoreIdentifier])
    }

```
### 主要API的使用
```swift
  // 获取已连接的设备
    open func retrieveConnectedPeripherals(withServices serviceUUIDs: [CBUUID]) -> [CBPeripheral]
  // 扫描设备(serviceUUIDs:需要扫描的设备serviceUUID数组，设置为nil,则扫描附近所有蓝牙设备，通常为了提高效率，填入特定的serviceUUID数组)
   open func scanForPeripherals(withServices serviceUUIDs: [CBUUID]?, options: [String : Any]? = nil)
  // 停止扫描
    open func stopScan()
  // 连接设备
    open func connect(_ peripheral: CBPeripheral, options: [String : Any]? = nil)
 // 断开连接
    open func cancelPeripheralConnection(_ peripheral: CBPeripheral)

```
### CBCentralManagerDelegate的回调
```swift
// 蓝牙状态变更
 func centralManagerDidUpdateState(_ central: CBCentralManager) {
        switch central.state.rawValue {
        case 0: // .unknown
            
        case 1: // .resetting
            
        case 2: // .unsupported
            
        case 3: // .unauthorized
            
        case 4: // .poweredOff(蓝牙关闭)
            
        case 5: // .poweredOn(蓝牙打开)
            
        default:
            fatalError("Unsupported BLE CentralState")
        }
    }

// 扫描到设备  advertisementData：广播包数据 RSSI：信号强度
  func centralManager(_ central: CBCentralManager,
                        didDiscover peripheral: CBPeripheral,
                        advertisementData: [String: Any],
                        rssi RSSI: NSNumber) {
        
    }
// 设备成功连接
 func centralManager(_ central: CBCentralManager, didConnect peripheral: CBPeripheral) {
       
    }

// 设备连接失败
optional func centralManager(_ central: CBCentralManager, didFailToConnect peripheral: CBPeripheral, error: Error?)  {

}
// 设备连接断开
 func centralManager(_ central: CBCentralManager, didDisconnectPeripheral peripheral: CBPeripheral, error: Error?) {

}
```
与设备连接成功后，会生成一个CBPeripheral对象，用来操作设备数据的读写和监听等。
### CBPeripheral的使用
```swift
public enum CBPeripheralState : Int, @unchecked Sendable {

    
    case disconnected = 0 // 连接断开

    case connecting = 1 // 正在连接中

    case connected = 2 // 已连接

    @available(watchOS 2.0, *)
    case disconnecting = 3 //断开连接中
}
// 设备写入服务类型，注意要根据设备读取的特征值来写入，否则写入报错。
public enum CBCharacteristicWriteType : Int, @unchecked Sendable {

    
    case withResponse = 0

    case withoutResponse = 1
}
open class CBPeripheral : CBPeer {
  // 蓝牙名称
    open var name: String? { get }
 // 信号强度
    open var rssi: NSNumber? { get }
// 连接状态
    open var state: CBPeripheralState { get }
// 扫描到的设备服务
    open var services: [CBService]? { get }
// 写入方式是withResponse还是withoutResponse
    open var canSendWriteWithoutResponse: Bool { get }
// 连接成功,检索当前连接的信号强度，回调方法：peripheral:didReadRSSI:error:
    open func readRSSI()
// 扫描设备可用的服务，serviceUUIDs 需要扫描的设备的服务的id，如果为nil，则扫描所有的服务，回调方法：peripheral:didDiscoverServices:
    open func discoverServices(_ serviceUUIDs: [CBUUID]?)
// includedServiceUUIDs  需要发现的服务service中的服务id列表，如果为nil，则扫描服务内所有的服务，较慢，不推荐使用。回调方法：peripheral:didDiscoverIncludedServicesForService:error:
    open func discoverIncludedServices(_ includedServiceUUIDs: [CBUUID]?, for service: CBService) 
//  characteristicUUIDs  数组，内含需要被发现的所有特征值类型，如果为nil，则为所有特征值。回调方法为:peripheral:didDiscoverCharacteristicsForService:error:
    open func discoverCharacteristics(_ characteristicUUIDs: [CBUUID]?, for service: CBService)
// characteristic   需要读取的服务特征值，回调方法：  peripheral:didUpdateValueForCharacteristic:error:
    open func readValue(for characteristic: CBCharacteristic)
// 获取向一个写服务可发送的最大字节数
    open func maximumWriteValueLength(for type: CBCharacteristicWriteType) -> Int
//   data:需要写入的数据 characteristic:写服务特征  type: 写服务的 类型(有/无响应)，需要注意的是，传入的type是根据characteristic!.properties.rawValue & CBCharacteristicProperties.writeWithoutResponse.rawValue 来决定，否则随意传入type会导致写入失败。
    open func writeValue(_ data: Data, for characteristic: CBCharacteristic, type: CBCharacteristicWriteType)
// 根据characteristic的properties来设置，若为true，说明只要有数据更新就会回调新数据。
    open func setNotifyValue(_ enabled: Bool, for characteristic: CBCharacteristic)
}
```
CBPeripheralDelegate的回调
```swift
// 设备名称更新
optional func peripheralDidUpdateName(_ peripheral: CBPeripheral) {

}
// peripheral :需要更新的设备 invalidatedServices:失效的服务
    optional func peripheral(_ peripheral: CBPeripheral, didModifyServices invalidatedServices: [CBService]) {

}
// peripheral :需要更新的设备 error：出现错误的原因。readRSSI的回调方法。
    optional func peripheralDidUpdateRSSI(_ peripheral: CBPeripheral, error: Error?) {

}
// peripheral :需要更新的设备 RSSI:设备的RSSI。readRSSI的回调方法
    optional func peripheral(_ peripheral: CBPeripheral, didReadRSSI RSSI: NSNumber, error: Error?) {

}
// peripheral：扫描到的设备  error ：错误原因。discoverServices的回调方法。
    optional func peripheral(_ peripheral: CBPeripheral, didDiscoverServices error: Error?) {

}
// peripheral：当前设备 service : 设备服务  error:错误原因。 discoverIncludedServices:forService的回调
    optional func peripheral(_ peripheral: CBPeripheral, didDiscoverIncludedServicesFor service: CBService, error: Error?) {

}
// peripheral：当前设备 service: 设备服务 error:错误原因。discoverCharacteristics:forService的回调
    optional func peripheral(_ peripheral: CBPeripheral, didDiscoverCharacteristicsFor service: CBService, error: Error?) {

}
//  peripheral：当前设备 characteristic：设备特征 error:错误原因。当前设备特征值有更新就回调。
    optional func peripheral(_ peripheral: CBPeripheral, didUpdateValueFor characteristic: CBCharacteristic, error: Error?) {

}
// peripheral：当前设备 characteristic：设备特征 error:错误原因。writeValue:forCharacteristic:type的回调
    optional func peripheral(_ peripheral: CBPeripheral, didWriteValueFor characteristic: CBCharacteristic, error: Error?) {

}
// peripheral：当前设备 characteristic：设备特征 error:错误原因。setNotifyValue:forCharacteristic的回调。
    optional func peripheral(_ peripheral: CBPeripheral, didUpdateNotificationStateFor characteristic: CBCharacteristic, error: Error?) {

}
```
一个设备有多个service，每个service都有多个characteristic,一层层找下来找到我们需要操作的characteristic，然后按硬件的要求进行读写和监听等操作。
