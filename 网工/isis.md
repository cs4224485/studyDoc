# 一 IS-IS原理和简介

中间系统到中间系统IS-IS（Intermediate System to Intermediate System）属于内部网关协议IGP（Interior Gateway Protocol），用于自治系统内部。IS-IS也是一种链路状态协议，使用最短路径优先SPF（Shortest Path First）算法进行路由计算。‘



## IS-IS的拓扑结构

**IS-IS的整体拓扑**

为了支持大规模的路由网络，IS-IS在自治系统内采用骨干区域与非骨干区域两级的分层结构。一般来说，将Level-1路由器部署在非骨干区域，Level-2路由器和Level-1-2路由器部署在骨干区域。每一个非骨干区域都通过Level-1-2路由器与骨干区域相连。

![image-20230619204305620](images\image-20230619204305620.png)

![image-20230619204340579](images\image-20230619204340579.png)

通过以上两种拓扑结构图可以体现IS-IS与OSPF的不同点：

- 在IS-IS中，每个路由器都只属于一个区域；而在OSPF中，一个路由器的不同接口可以属于不同的区域。
- 在IS-IS中，单个区域没有骨干与非骨干区域的概念；而在OSPF中，Area0被定义为骨干区域。
- 在IS-IS中，Level-1和Level-2级别的路由都采用SPF算法，分别生成最短路径树SPT（Shortest Path Tree）；而在OSPF中，只有在同一个区域内才使用SPF算法，区域之间的路由需要通过骨干区域来转发。

## **IS-IS路由器的分类**

- Level-1路由器

  Level-1路由器负责区域内的路由，它只与属于同一区域的Level-1和Level-1-2路由器形成邻居关系，属于不同区域的Level-1路由器不能形成邻居关系。Level-1路由器只负责维护Level-1的链路状态数据库LSDB（Link State Database），该LSDB包含本区域的路由信息，到本区域外的报文转发给最近的Level-1-2路由器。

- Level-2路由器

  Level-2路由器负责区域间的路由，它可以与同一或者不同区域的Level-2路由器或者其它区域的Level-1-2路由器形成邻居关系。Level-2路由器维护一个Level-2的LSDB，该LSDB包含区域间的路由信息。

  所有Level-2级别（即形成Level-2邻居关系）的路由器组成路由域的骨干网，负责在不同区域间通信。路由域中Level-2级别的路由器必须是物理连续的，以保证骨干网的连续性。只有Level-2级别的路由器才能直接与区域外的路由器交换数据报文或路由信息。

- Level-1-2路由器

  同时属于Level-1和Level-2的路由器称为Level-1-2路由器，它可以与同一区域的Level-1和Level-1-2路由器形成Level-1邻居关系，也可以与其他区域的Level-2和Level-1-2路由器形成Level-2的邻居关系。Level-1路由器必须通过Level-1-2路由器才能连接至其他区域。

  Level-1-2路由器维护两个LSDB，Level-1的LSDB用于区域内路由，Level-2的LSDB用于区域间路由。

## **IS-IS的网络类型**

IS-IS只支持两种类型的网络，根据物理链路不同可分为：

- 广播链路：如Ethernet、Token-Ring等。 
- 点到点链路：如PPP、HDLC等。 

**DIS和伪节点**

在广播网络中，IS-IS需要在所有的路由器中选举一个路由器作为DIS（Designated Intermediate System）。DIS用来创建和更新伪节点（Pseudonodes），并负责生成伪节点的链路状态协议数据单元LSP（Link state Protocol Data Unit），用来描述这个网络上有哪些网络设备。

伪节点是用来模拟广播网络的一个虚拟节点，并非真实的路由器。在IS-IS中，伪节点用DIS的System ID和一个字节的Circuit ID（非0值）标识。

![image-20230619205322367](images\image-20230619205322367.png)

用伪节点可以简化网络拓扑，使路由器产生的LSP长度较小。另外，当网络发生变化时，需要产生的LSP数量也会较少，减少SPF的资源消耗。

Level-1和Level-2的DIS是分别选举的，用户可以为不同级别的DIS选举设置不同的优先级。DIS优先级数值最大的被选为DIS。如果优先级数值最大的路由器有多台，则其中MAC地址最大的路由器会被选中。不同级别的DIS可以是同一台路由器，也可以是不同的路由器。

IS-IS协议中DIS与OSPF协议中DR（Designated Router）的区别：

- 在IS-IS广播网中，优先级为0的路由器也参与DIS的选举，而在OSPF中优先级为0的路由器则不参与DR的选举。
- 在IS-IS广播网中，当有新的路由器加入，并符合成为DIS的条件时，这个路由器会被选中成为新的DIS，原有的伪节点被删除。此更改会引起一组新的LSP泛洪。而在OSPF中，当一台新路由器加入后，即使它的DR优先级值最大，也不会立即成为该网段中的DR。
- 在IS-IS广播网中，同一网段上的同一级别的路由器之间都会形成邻接关系，包括所有的非DIS路由器之间也会形成邻接关系。而在OSPF中，路由器只与DR和BDR建立邻接关系。

## IS-IS的地址结构

网络服务访问点NSAP（Network Service Access Point）是OSI协议中用于定位资源的地址。NSAP的地址结构由IDP（Initial Domain Part）和DSP（Domain Specific Part）组成。IDP和DSP的长度都是可变的，NSAP总长最多是20个字节，最少8个字节。

- IDP相当于IP地址中的主网络号。它是由ISO规定，并由AFI（Authority and Format Identifier）与IDI（Initial Domain Identifier）两部分组成。AFI表示地址分配机构和地址格式，IDI用来标识域。
- DSP相当于IP地址中的子网号和主机地址。它由High Order DSP、System ID和SEL三个部分组成。High Order DSP用来分割区域，System ID用来区分主机，SEL（NSAP Selector）用来指示服务类型。

![image-20230619205810281](images\image-20230619205810281.png)

### Area Address

IDP和DSP中的High Order DSP一起，既能够标识路由域，也能够标识路由域中的区域，因此，它们一起被称为区域地址（Area  Address），相当于OSPF中的区域编号。同一Level-1区域内的所有路由器必须具有相同的区域地址，Level-2区域内的路由器可以具有不同的区域地址。

一般情况下，一个路由器只需要配置一个区域地址，且同一区域中所有节点的区域地址都要相同。为了支持区域的平滑合并、分割及转换，在设备的实现中，一个IS-IS进程下最多可配置3个区域地址。

### System ID

System ID用来在区域内唯一标识主机或路由器。在设备的实现中，它的长度固定为48bit（6字节）。

在实际应用中，一般使用Router ID与System ID进行对应。假设一台路由器使用接口Loopback0的IP地址192.168.1.1作为Router ID，则它在IS-IS中使用的System ID可通过如下方法转换得到：

- 将IP地址192.168.1.1的每个十进制数都扩展为3位，不足3位的在前面补0，得到192.168.001.001。
- 将扩展后的地址分为3部分，每部分由4位数字组成，得到1921.6800.1001。重新组合的1921.6800.1001就是System ID。

实际System ID的指定可以有不同的方法，但要保证能够唯一标识主机或路由器。

### SEL

SEL的作用类似IP中的“协议标识符”，不同的传输协议对应不同的SEL。在IP上SEL均为00。

# 二 IS-IS的报文类型



报文头部内容：

![image-20230619210050847](images\image-20230619210050847.png)

域内路由协议鉴别符： IS -IS 的网络层标识，值为 Ox83

头长度: 数据包报头的字节数。

版本或协议号扩展名: 当前设置为 l 。

SystemID Length： 用来表示 system ID 长度

PDU type： 标识 PDU 类型

IS-IS报文有以下几种类型：HELLO PDU（Protocol Data Unit）、LSP和SNP。

Version： 固定值为 1

MAX.Areas： 最多区域地址。默认为 0，表示最多支持 3 个区域地址数。使用多个区域 ID 可以实现平滑过滤

### Hello PDU

Hello报文用于建立和维持邻居关系，也称为IIH（IS-to-IS Hello PDUs）。其中，广播网中的Level-1  IS-IS使用Level-1 LAN IIH；广播网中的Level-2 IS-IS使用Level-2 LAN IIH；非广播网络中则使用P2P  IIH。它们的报文格式有所不同。P2P IIH中相对于LAN IIH来说，多了一个表示本地链路ID的Local Circuit  ID字段，缺少了表示广播网中DIS的优先级的Priority字段以及表示DIS和伪节点System ID的LAN ID字段。

### LSP

链路状态报文LSP（Link State PDUs）用于交换链路状态信息。LSP分为两种：Level-1 LSP和Level-2  LSP。Level-1 LSP由Level-1 IS-IS传送，Level-2 LSP由Level-2 IS-IS传送，Level-1-2  IS-IS则可传送以上两种LSP。

LSP报文中主要字段的解释如下：

- ATT字段：当Level-1-2 IS-IS在Level-1区域内传送Level-1 LSP时，如果Level-1 LSP中设置了ATT位，则表示该区域中的Level-1 IS-IS可以通过此Level-1-2 IS-IS通往外部区域。

- OL（LSDB Overload）字段：过载标志位。

  设置了过载标志位的LSP虽然还会在网络中扩散，但是在计算通过过载路由器的路由时不会被采用。即对路由器设置过载位后，其它路由器在进行SPF计算时不会使用这台路由器做转发，只计算该节点上的直连路由。

- IS Type字段：用来指明生成此LSP的IS-IS类型是Level-1还是Level-2 IS-IS（01表示Level-1，11表示Level-2）。

### SNP

序列号报文SNP（Sequence Number PDUs）通过描述全部或部分数据库中的LSP来同步各LSDB（Link-State DataBase），从而维护LSDB的完整与同步。

SNP包括全序列号报文CSNP（Complete SNP）和部分序列号报文PSNP（Partial SNP），进一步又可分为Level-1 CSNP、Level-2 CSNP、Level-1 PSNP和Level-2 PSNP。

CSNP包括LSDB中所有LSP的摘要信息，从而可以在相邻路由器间保持LSDB的同步。在广播网络上，CSNP由DIS定期发送（缺省的发送周期为10秒）；在点到点链路上，CSNP只在第一次建立邻接关系时发送。

PSNP只列举最近收到的一个或多个LSP的序号，它能够一次对多个LSP进行确认，当发现LSDB不同步时，也用PSNP来请求邻居发送新的LSP。

IS-IS报文中的变长字段部分是多个TLV（Type-Length-Value）三元组

| TLV Type | 名称                                      | 所应用的PDU类型 |
| -------- | ----------------------------------------- | --------------- |
| 1        | Area Addresses                            | IIH、LSP        |
| 2        | IS Neighbors（LSP）                       | LSP             |
| 4        | Partition Designated Level2 IS            | L2 LSP          |
| 6        | IS Neighbors（MAC Address）               | LAN IIH         |
| 7        | IS Neighbors（SNPA Address）              | LAN IIH         |
| 8        | Padding                                   | IIH             |
| 9        | LSP Entries                               | SNP             |
| 10       | Authentication Information                | IIH、LSP、SNP   |
| 128      | IP Internal Reachability Information      | LSP             |
| 129      | Protocols Supported                       | IIH、LSP        |
| 130      | IP External Reachability Information      | LSP             |
| 131      | Inter-Domain Routing Protocol Information | L2 LSP          |
| 132      | IP Interface Address                      | IIH、LSP        |

# 三 IS-IS基本原理

IS-IS是一种链路状态路由协议，每一台路由器都会生成一个LSP，它包含了该路由器所有使能IS-IS协议接口的链路状态信息。通过跟相邻设备建立IS-IS邻接关系，互相更新本地设备的LSDB，可以使得LSDB与整个IS-IS网络的其他设备的LSDB实现同步。然后根据LSDB运用SPF算法计算出IS-IS路由。如果此IS-IS路由是到目的地址的最优路由，则此路由会下发到IP路由表中，并指导报文的转发。

## IS-IS邻居关系的建立

两台运行IS-IS的路由器在交互协议报文实现路由功能之前必须首先建立邻居关系。在不同类型的网络上，IS-IS的邻居建立方式并不相同。

- 广播链路邻居关系的建立

 广播链路邻居关系建立过程

![image-20230619210517390](images\image-20230619210517390.png)

1. RouterA广播发送Level-2 LAN IIH，此报文中无邻居标识。
2. RouterB收到此报文后，将自己和RouterA的邻居状态标识为Initial。然后，RouterB再向RouterA回复Level-2 LAN IIH，此报文中标识RouterA为RouterB的邻居。
3. RouterA收到此报文后，将自己与RouterB的邻居状态标识为Up。然后RouterA再向RouterB发送一个标识RouterB为RouterA邻居的Level-2 LAN IIH。
4. RouterB收到此报文后，将自己与RouterA的邻居状态标识为Up。这样，两个路由器成功建立了邻居关系。

因为是广播网络，需要选举DIS，所以在邻居关系建立后，路由器会等待两个Hello报文间隔，再进行DIS的选举。Hello报文中包含Priority字段，Priority值最大的将被选举为该广播网的DIS。若优先级相同，接口MAC地址较大的被选举为DIS。

P2P链路邻居关系的建立

在P2P链路上，邻居关系的建立不同于广播链路。分为两次握手机制和三次握手机制。

- 两次握手机制

  只要路由器收到对端发来的Hello报文，就单方面宣布邻居为Up状态，建立邻居关系。

- 三次握手机制

  此方式通过三次发送P2P的IS-IS Hello PDU最终建立起邻居关系，类似广播邻居关系的建立。

两次握手机制存在明显的缺陷。当路由器间存在两条及以上的链路时，如果某条链路上到达对端的单向状态为Down，而另一条链路同方向的状态为Up，路由器之间还是能建立起邻接关系。SPF在计算时会使用状态为UP的链路上的参数，这就导致没有检测到故障的路由器在转发报文时仍然试图通过状态为Down的链路。三次握手机制解决了上述不可靠点到点链路中存在的问题。这种方式下，路由器只有在知道邻居路由器也接收到它的报文时，才宣布邻居路由器处于Up状态，从而建立邻居关系。

IS-IS按如下原则建立邻居关系：

- 只有同一层次的相邻路由器才有可能成为邻居。
- 对于Level-1路由器来说，区域号必须一致。
- 链路两端IS-IS接口的网络类型必须一致。
- 链路两端IS-IS接口的地址必须处于同一网段。

由于IS-IS是直接运行在数据链路层上的协议，并且最早设计是给CLNP使用的，IS-IS邻居关系的形成与IP地址无关。但在实际的实现中，由于只在IP上运行IS-IS，所以是要检查对方的IP地址的。如果接口配置了从IP，那么只要双方有某个IP（主IP或者从IP）在同一网段，就能建立邻居，不一定要主IP相同。

## IS-IS的LSP交互过程

**LSP产生的原因**

IS-IS路由域内的所有路由器都会产生LSP，以下事件会触发一个新的LSP：

- 邻居Up或Down
- IS-IS相关接口Up或Down
- 引入的IP路由发生变化
- 区域间的IP路由发生变化
- 接口被赋了新的metric值
- 周期性更新

**收到邻居新的LSP的处理过程**

1. 将接收的新的LSP合入到自己的LSDB数据库中，并标记为flooding。
2. 发送新的LSP到除了收到该LSP的接口之外的接口。
3. 邻居再扩散到其他邻居。

**LSP的“泛洪”**

LSP报文的“泛洪”（flooding）是指当一个路由器向相邻路由器通告自己的LSP后，相邻路由器再将同样的LSP报文传送到除发送该LSP的路由器外的其它邻居，并这样逐级将LSP传送到整个层次内所有路由器的一种方式。通过这种“泛洪”，整个层次内的每一个路由器就都可以拥有相同的LSP信息，并保持LSDB的同步。

每一个LSP都拥有一个标识自己的4字节的序列号。在路由器启动时所发送的第一个LSP报文中的序列号为1，以后当需要生成新的LSP时，新LSP的序列号在前一个LSP序列号的基础上加1。更高的序列号意味着更新的LSP。

### **广播链路中新加入路由器与DIS同步LSDB数据库的过程**

![image-20230619211026813](images\image-20230619211026813.png)

1. 新加入的路由器RouterC首先发送Hello报文，与该广播域中的路由器建立邻居关系。
2. 建立邻居关系之后，RouterC等待LSP刷新定时器超时，然后将自己的LSP发往组播地址（Level-1：01-80-C2-00-00-14；Level-2：01-80-C2-00-00-15）。这样网络上所有的邻居都将收到该LSP。
3. 该网段中的DIS会把收到RouterC的LSP加入到LSDB中，并等待CSNP报文定时器超时并发送CSNP报文，进行该网络内的LSDB同步。
4. RouterC收到DIS发来的CSNP报文，对比自己的LSDB数据库，然后向DIS发送PSNP报文请求自己没有的LSP。
5. DIS收到该PSNP报文请求后向RouterC发送对应的LSP进行LSDB的同步。 

在上述过程中DIS的LSDB更新过程如下：

1. DIS接收到LSP，在数据库中搜索对应的记录。若没有该LSP，则将其加入数据库，并广播新数据库内容。
2. 若收到的LSP序列号大于本地LSP的序列号，就替换为新报文，并广播新数据库内容；若收到的LSP序列号小本地LSP的序列号，就向入端接口发送本地LSP报文。
3. 若两个序列号相等，则比较Remaining Lifetime。若收到的LSP的Remaining Lifetime小于本地LSP的Remaining Lifetime，就替换为新报文，并广播新数据库内容；若收到的LSP的Remaining Lifetime大于本地LSP的Remaining Lifetime，就向入端接口发送本地LSP报文。
4. 若两个序列号和Remaining  Lifetime都相等，则比较Checksum。若收到的LSP的Checksum大于本地LSP的Checksum，就替换为新报文，并广播新数据库内容；若收到的LSP的Checksum小于本地LSP的Checksum，就向入端接口发送本地LSP报文。
5. 若两个序列号、Remaining Lifetime和Checksum都相等，则不转发该报文。

### **P2P链路上LSDB数据库的同步过程**

![image-20230619211157012](images\image-20230619211157012.png)

1. RouterA先与RouterB建立邻居关系。
2. 建立邻居关系之后，RouterA与RouterB会先发送CSNP给对端设备。如果对端的LSDB与CSNP没有同步，则发送PSNP请求索取相应的LSP。
3. 假定RouterB向RouterA索取相应的LSP。RouterA发送RouterB请求的LSP的同时启动LSP重传定时器，并等待RouterB发送的PSNP作为收到LSP的确认。
4. 如果在接口LSP重传定时器超时后，RouterA还没有收到RouterB发送的PSNP报文作为应答，则重新发送该LSP直至收到PSNP报文。

在P2P链路中设备的LSDB更新过程如下：

1. 若收到的LSP比本地LSP的序列号大，则将这个新的LSP存入自己的LSDB，并发送PSNP报文来确认收到此LSP，之后将这新的LSP发送给除了发送该LSP的邻居以外的邻居。
2. 若收到的LSP比本地的序列号小，则将本地LSP发送给对方，然后等待对方发送的PSNP报文作为确认。
3. 若收到的LSP序列号和本地LSP的序列号相同，则比较Remaining Lifetime，若收到的LSP报文的Remaining Lifetime为0，则将收到的LSP存入LSDB中并发送PSNP报文来确认收到此LSP，然后将该LSP发送给除了发送该LSP的邻居以外的邻居；若收到的LSP报文的Remaining Lifetime不为0而本地LSP报文的Remaining Lifetime为0，则直接给对方发送本地的LSP，然后等待对方给自己一个PSNP报文作为确认。
4. 若收到的LSP和本地LSP的序列号相同且Remaining  Lifetime都不为0，则比较Checksum，若收到LSP的Checksum大于本地LSP的Checksum，则将收到的LSP存入LSDB中并发送PSNP报文来确认收到此LSP，然后将该LSP发送给除了发送该LSP的邻居以外的邻居；若收到LSP的Checksum小于本地LSP的Checksum，则直接给对方发送本地的LSP，然后等待对方给自己一个PSNP报文作为确认。
5. 若收到的LSP和本地LSP的Checksum也相等，则不转发该报文。

## IS-IS路由渗透

通常情况下，Level-1区域内的路由通过Level-1路由器进行管理。所有的Level-2和Level-1-2路由器构成一个连续的骨干区域。Level-1区域必须且只能与骨干区域相连，不同的Level-1区域之间并不相连。

Level-1-2路由器将学习到的Level-1路由信息装进Level-2  LSP，再泛洪LSP给其他Level-2和Level-1-2路由器。因此，Level-1-2和Level-2路由器知道整个IS-IS路由域的路由信息。但是，为了有效减小路由表的规模，在缺省情况下，Level-1-2路由器并不将自己知道的其他Level-1区域以及骨干区域的路由信息通报给它所在的Level-1区域。这样，Level-1路由器将不了解本区域以外的路由信息，可能导致与本区域之外的目的地址通信时无法选择最佳的路由。

为解决上述问题，IS-IS提供了路由渗透功能。通过在Level-1-2路由器上定义ACL（Access Control  List）、路由策略、Tag标记等方式，将符合条件的路由筛选出来，实现将其他Level-1区域和骨干区域的部分路由信息通报给自己所在的Level-1区域。

![image-20230619214240062](images\image-20230619214240062.png)

RouterA发送报文给RouterF，选择的最佳路径应该是RouterA->RouterB->RouterD->RouterE->RouterF。因为这条链路上的cost值为40，但在RouterA上查看发送到RouterF的报文选择的路径是：RouterA->RouterC->RouterE->RouterF，其cost值为70，不是RouterA到RouterF的最优路由。 

RouterA作为Level-1路由器并不知道本区域外部的路由，那么发往区域外的报文都会选择由最近的Level-1-2路由器产生的缺省路由发送出去，所以会出现RouterA选择次最优路由转发报文的情况。

如果分别在Level-1-2路由器RouterC和RouterD上使能路由渗透功能，Aera10中的Level-1路由器就会拥有经这两个Level-1-2路由器通向区域外的路由信息。经过路由计算，选择的转发路径为RouterA->RouterB->RouterD->RouterE->RouterF，即RouterA到RouterF的最优路由。 

## IS-IS网络收敛

为了提高IS-IS网络的收敛，有快速收敛和按优先级收敛两种方式。快速收敛侧重于从路由的计算角度加快收敛速度；按优先级收敛侧重于从路由优先级角度提高网络性能。

## 快速收敛

IS-IS快速收敛是为了提高路由的收敛速度而做的扩展特性。它包括以下几个功能：

增量最短路径优先算法I-SPF（Incremental SPF）：是指当网络拓扑改变的时候，只对受影响的节点进行路由计算，而不是对全部节点重新进行路由计算，从而加快了路由的计算。当网络拓扑中有一个节点发生变化时，这种算法需要重新计算网络中的所有节点，计算时间长，占用过多的CPU资源，影响整个网络的收敛速度。

部分路由计算PRC（Partial Route Calculation）：是指当网络上路由发生变化的时候，只对发生变化的路由进行重新计算。PRC的原理与I-SPF相同，都是只对发生变化的路由进行重新计算。不同的是，PRC不需要计算节点路径，而是根据I-SPF算出来的SPT来更新路由。在路由计算中，叶子代表路由，节点则代表路由器。如果I-SPF计算后的SPT改变，PRC会只处理那个变化的节点上的所有叶子；如果经过I-SPF计算后的SPT并没有变化，则PRC只处理变化的叶子信息。比如一个节点使能一个IS-IS接口，则整个网络拓扑的SPT是不变的，这时PRC只更新这个节点的接口路由，从而节省CPU占用率。PRC和I-SPF配合使用可以将网络的收敛性能进一步提高，它是原始SPF算法的改进，已经代替了原有的算法。

智能定时器：在进行SPF计算和产生LSP的时候用到的一种智能定时器。该定时器首次超时时间是一个固定的时间。如果在定时器超时前，又有触发定时器的事件发生，则该定时器下一次的超时时间会增加。改进了路由算法后，如果触发路由计算的时间间隔较长，同样会影响网络的收敛速度。使用毫秒级定时器可以缩短这个间隔时间，但如果网络变化比较频繁，又会造成过度占用CPU资源。SPF智能定时器既可以对少量的外界突发事件进行快速响应，又可以避免过度的占用CPU。通常情况下，一个正常运行的IS-IS网络是稳定的，发生大量的网络变动的几率很小，IS-IS不会频繁的进行路由计算，所以第一次触发的时间可以设置的非常短（毫秒级）。如果拓扑变化比较频繁，智能定时器会随着计算次数的增加，间隔时间也会逐渐延长，从而避免占用大量的CPU资源。

LSP快速扩散：此特性可以加快LSP的扩散速度。正常情况下，当IS-IS收到其它路由器发来的LSP时，如果此LSP比本地LSDB中相应的LSP要新，则更新LSDB中的LSP，并用一个定时器定期将LSDB内已更新的LSP扩散出去。

## 域间路由

ISIS的物理区域和逻辑区域不同，即物理上看不出是否是骨干区域和非骨干区域（无法通过Area ID来区分区域是否为骨干区域、非骨干区域），需要自己去判断。

如何判断：

由L2邻居连接起来的区域为骨干区域，由L1邻居连接起来的区域为非骨干区域

所以可知：骨干区域内可以有多个不同的Area ID

![image-20230620215416988](images\image-20230620215416988.png)

**注意：**

L2的邻居关系一定要连续，保证骨干区域的连续性

L1/L2路由器一定要和L1路由器在同一区域

ISIS协议的区域边界在整个Router，OSPF的区域边界在Router的接口上

### 区域间路由如何互通

非骨干到骨干

默认情况下：

L1/2路由器不会将L2的路由泄露到L1区域（即每个L1的区域默认为完全末节区域）

​     ATT 骨干区域连接符

​     L1/2路由器在自己的L1 LSP中，将ATT 置1，用于描述自身连接着的骨干区域

​     L1的路由器根据ATT-1的标识，产生一条去往L1/2路由器的缺省路由（如果从多个L1/2路由器收到ATT置位，则会产生一条去往最近的L1/2路由器的缺省路由）

骨干到非骨干

默认情况下：

   L1/2路由器将自身在L1内的路由以一条实LSP的形式在骨干区域进行泛洪

（L1/L2将自身L1内的路由都认为是自身直连的路由发送到骨干区域）


## ISIS认证

据对何种报文做认证分类：

​	接口认证： 是指使能 IS-IS 协议的接口以指定方式和密码对 Level-1 和Level-2 的 Hello 报文进行认证。

​	区域认证：是指运行 IS-IS 的区域以指定方式和密码对 Level-1 的 SNP 和LSP 报文进行认证。

​	路由域认证：是指运行IS-IS的路由域以指定方式和密码对Level-2的SNP和 LSP 报文进行认证。

根据对报文的认证方式分类

​	不认证

​	简单认证：密码为明文，加入到报文中

​	MD5认证：密码进行MD5算法加密后，加入到报文中

​	Keychian认证：定期修改报文的认证和加密算法

​	HMAC-SHA256认证：将密码进行HMAC-SHA256算法后，加入到报文中
认证信息的携带形式:

IS-IS 通过 TLV 的形式携带认证信息，认证 TLV 的类型为 10，具体格式如下：

Type： 

​	ISO 定义认证报文的类型值为 10，长度为 1 字节。

​	0：保留的类型

​	1：明文认证

​	54：MD5认证

​	255：路由域私有认证方式

Length：指定认证 TLV 值的长度，长度 1 字节。

Value：指定认证的具体内容，其中包括了认证的类型和认证的密码，长度为 1～254 字节。

## 影响ISIS建立邻居的因素

1、区域

L1的路由器只能建立L1的邻居关系

2、路由器级别

L1只能和L1、L1-2建立，L2只能和L2、L1-2建立，L1-2可以和L1-2、L1、L2建立

3、System-id

必须不一致，唯一标识一台ISIS路由器，具有唯一性

4、同一子网下，掩码可以不一致

由于Hello不携带掩码，携带IP，路由器用收到的IP与本地接口的掩码进行与运算，判断是否为同一子网


5、MTU

以太网接口MTU值小于ISIS-LSP报文的max size+3字节（3字节为ISIS的报文头长度）会影响邻居建立

P2P接口MTU值小于ISIS-LSP的报文长度会影响邻居建立

默认情况下，MA的MTU不小于1500，P2P不能小于1497

6、网络接口类型

由于MA和P2P建立邻居所需的TLV不一致（TLV6和TLV240）

所以网络接口类型不一致无法建立邻居

7、认证方式

认证的类型和密钥要一致

8、3次握手情况

三次握手（兼容二次握手）和三次握手only（不兼容三次握手）可以建立邻居关系

P2P的两次握手和三次握手之间可以建立邻居关系（3次握手兼容2次握手）P2P的两次握手和三次握手Only（只支持3次握手，不兼容二次握手）不会建立邻居

会导致一边Up，一边Down

9、Cost-type开销类型

不同的Cost-type可以建立邻居但是无法传递路由

Narrow的TLV为2，128，130

Wide的TLV为22，135

# 四 ISIS高级特性——LSP分片扩展与过载

## LSP分片扩展

当ISIS要发布的PDU信息量太大时，ISIS路由器将会生成多个LSP分片，用来携带更多的ISIS信息

ISIS分片由LSP ID中的分片号（LSP ID）字段标识，长度为1Byte，所以一个ISIS进程最多可以产生256个LSP分片

**为什么要LSP分片扩展**

LSP分片扩展增大了LSP分片数量，具体实现方式如下

由于每个系统最多可生成256个分片，通过增加附加系统（最多可以增加50个），ISIS进程可以多生成13056个LSP分片

## **LSP扩展涉及基本概念**

### 初始系统（Originating System）

初始系统是实际运行IS-IS协议的路由器（实路由器）

### 虚拟系统（Virtual System）

此虚拟系统指的是启动虚拟ISIS进程

由附加系统ID标识的系统，用来生成扩展LSP分片（虚路由器）

这些分片在其LSP ID中携带附加系统ID

附加系统与初始系统一样，每个附加系统都可携带256个LSP分片

### 系统ID（Normal System-ID）

初始系统的系统ID。

### 附加系统ID（Additional System-ID）

虚拟系统的系统ID，由网络管理器统一分配。

### 24号TLV（IS Alias ID TLV）

用来表示初始系统与虚拟系统的关系。

附加系统ID和系统ID一样，在整个路由域中必须唯一


## **LSP 两种工作模式**

当R2不支持LSP分片扩展，即识别不了TLV24时，R2会认为R1.1和R1.2是两台真实的设备（即：R2认为有3台真实的设备给自己发送了LSP）

当R2收到R1、R1.1、R1.2设备发来的LSP时，都进行正常的路由计算

Mode-2  用于网络中所有设备都支持LSP分片扩展的场景

当R2支持LSP扩展，即可以识别TLV24时，会认为R1.1和R1.2是两台虚拟的设备，其真实的路由器是R1

当R2收到R1.1和R1.2设备发来的LSP时，通过24号TLV了解到它们的初始系统是R1，认为R1.1和R1.2其实就是R1设备，则R2只与R1进行路由计算


## **LSP 配置命令**

第一步：使能ISIS路由器的LSP扩展功能

ISIS视图下：Lsp-fragments-extend [level1/level-2/level-1-2] [mode-1 mode-2]     

        Level-1   指定在Level-1级别使能分片扩展
    
        Mode-1  工作模式为mode-1
    
        默认开启分片扩展后的配置为：level-1-2与mode-1

第二步：配置ISIS进程的虚拟系统ID

Virtual-system [id]        

第三步：重启ISIS进程

reset isis all   

配置注意事项

在配置虚拟进程前，要在ISIS进程下配置好NET地址

只有使能了LSP分片扩展，并用reset isis all命令重启了IS-IS进程后，配置的虚拟系统ID才会生效

如果没有使能LSP分片扩展和重启IS-IS进程，则只能对虚拟系统ID进行配置，但不会生效

LSP分片扩展举例--在设备上添加额外两个虚拟系统，承载更多的LSP

```
isis 10
 network-entity 49.0001.0000.0000.0001.00   配置ISIS网络的NET地址
 lsp-fragments-extend level-1-2 mode-1         配置LSP扩展（使用mode-1模式）
 virtual-system 1111.1111.1111.1111         配置三个虚拟系统（三个虚拟系统的ID必须路由域唯一）
 virtual-system 1111.1111.1111.1112

reset isis all                                            重启ISIS
```

## ISIS Overload

SIS Overload使用ISIS过载标记位来表示过载状态，过载标识位存在LSP报文信息中OL字段

当对设备设置过载标志位后，设备在进行SPF计算时不会使用这台设备做转发，只计算该设备上的直连路由

![image-20230620220437529](images\image-20230620220437529.png)

**设备如何进入过载状态**

自动进入过载：设备异常时会自动进入过载状态，此时系统会删除全部引入或者渗透的路由信息

手动配置设备进入过载状态：此时系统会根据用户的配置决定是否删除全部引入或渗透的路由信息

**手动设置命令举例（在ISSI进程下配置）**

```
例1：为ISIS进程配置过载标志位
isis 10
set-overload 
 
例2：表示ISIS进程10启动后进入过载位，指导bgp邻居up后才取消过载（最多等待BGP 10s，即最多处于过载状态10
isis 10
set-overload on-startup wait-for-bgp 10    ）
 
例3：表示ISSI进程10启动后进入过载位，允许发布从ISIS学来的IP地址前缀，禁止发布从其它协议学来的IP地址前缀
isis 10
set-overload on-startup allow interlevel   
 
字段讲解
   on-startup     表示满足哪些情况设备取消过载（即设置最大过载时间）
   allow          表示允许发布地址前缀（缺省过载状态不允许发送地址前缀）
   interlevel     跟在allow字段后，表示允许发布从ISIS学来的地址前缀
   external       跟在allow字段后，表示允许发布从其它协议学来的地址前缀
```

# 五 ISIS配置命令

## 配置ISIS邻居建立

```
AR1
isis 1
 network-entity 49.0001.0000.0001.00   ISIS区域为49.0001，ID为0000.0001
interface GigabitEthernet0/0/0
 isis enable 1                        此接口运行ISIS
 
AR2
interface GigabitEthernet0/0/0
 isis enable 1
isis 1
 network-entity 49.0001.0000.0002.00
```

## 配置认证

```
R8
interface GigabitEthernet0/0/0
 isis authentication-mode md5 cipher admin@123
AR1
interface GigabitEthernet0/0/2
 isis authentication-mode md5 cipher admin@123
配置在AR2和AR7之间对L2的SNP、LSP报文进行认证（路由域认证）
AR2和AR7
isis 1
 domain-authentication-mode md5 cipher admin@123
配置在AR5和AR6对L1的SNP、LSP报文进行认证（区域认证）
AR5和AR6
isis 1
 area-authentication-mode md5 cipher admin@123

```

## 配置路由扩散

```
配置LSP快速扩散
在49.0001区域的设备上都开启
isis 1
 flash-flood 10 max-timer-interval 20 level-2
LSP发送最大间隔为20ms，每次最多发送10个LSP
修改接口的网络类型（以AR1为例子）
interface GigabitEthernet0/0/0
 isis circuit-type p2p

```

## 配置路由过滤

```
配置路由引入（不引入10.0.3.1）
acl number 2000 
 rule 5 permit source 10.0.0.1 0
 rule 10 permit source 10.0.1.1 0
 rule 15 permit source 10.0.2.1 0
 rule 20 deny
route-policy 1 permit node 10
 if-match acl 2000
 
isis 1
 import-route direct level-2 route-policy 1 
在R5上过滤10.0.0.1的路由
acl number 2000 
 rule 5 deny source 10.0.0.1 0
 rule 10 permit
isis 1
 filter-policy 2000 import （只对自己生效，OSPF对自己和邻居都生效）
在R5配置路由泄露（将L2引入到L1）
isis 1
 import-route isis level-2 into level-1
```

## 配置定时器

```
配置SPF计算时间
isis 1
 timer spf 1 20 100
配置LSP定时器
isis 1
 timer lsp-generation 2 100 200 level-2
```

