# 一 OSPF简介

1、OSPF是典型的链路状态路由协议，是目前业内使用非常广泛的IGP协议之一。

2、目前针对IPv4协议使用的是OSPF Version 2（RFC2328）；针对IPv6协议使用OSPF Version 3（RFC2740）。如无特殊说明本章后续所指的OSPF均为OSPF Version 2。

3、运行OSPF路由器之间交互的是LS（Link State，链路状态）信息，而不是直接交互路由。LS信息是OSPF能够正常进行拓扑及路由计算的关键信息。

4、OSPF路由器将网络中的LS信息收集起来，存储在LSDB中。路由器都清楚区域内的网络拓扑结构，这有助于路由器计算无环路径。

5、每台OSPF路由器都采用SPF算法计算达到目的地的最短路径。路由器依据这些路径形成路由加载到路由表中。

6、OSPF支持VLSM（Variable Length Subnet Mask，可变长子网掩码），支持手工路由汇总。

7、多区域的设计使得OSPF能够支持更大规模的网络。

## **OSPF区域**

OSPF Area用于标识一个OSPF的区域。

区域是从逻辑上将设备划分为不同的组，每个组用区域号（Area ID）来标识

## Router-ID

OSPF Router-ID用于在OSPF domain中唯一地表示一台OSPF路由器，从OSPF网络设计的角度，我们要求全OSPF域内，禁止出现两台路由器拥有相同的OSPF Router-ID。
 OSPF Router-ID的设定可以通过手工配置的方式，或者通过协议自动选取的方式。当然，在实际网络部署中，强烈建议手工配置OSPF的Router-ID，因为这关系到协议的稳定。
 在路由器运行了OSPF并由系统自动选定Router-ID之后，如果该Router-ID对应的接口DOWN掉，或出现一个更大的IP，OSPF仍然保持原Router-ID（也就是说，Router-ID值是非抢占的，稳定第一），即使此时reset ospf process重启OSPF进程，Router-ID也不会发生改变；除非重新手工配置Router-ID（OSPF进程下手工敲router-id xxx），并且重启OSPF进程方可。

### 注意事项：

 如果该Router-ID对应的接口IP 地址消失，例如undo ip address，则reset ospf process后，RouterID也会发生改变。

## COST

OSPF使用cost“开销”作为路由度量值。
每一个激活OSPF的接口都有一个cost值。OSPF接口cost=100M /接口带宽，其中100M为OSPF的参考带宽（reference-bandwidth）。
一条OSPF路由的cost由该路由从路由的起源一路到达本地的所有入接口cost值的总和。
![image-20230216202308335](images\image-20230216202308335.png)

上图只是为了帮助大家理解路由cost的计算过程，我们都知道OSPF实际的路由计算是由LSA经过计算得来的，所以这里只是形象化的帮助大家理解而已：R1将路由更新出来，Cost=1，R2从Serial4/0/0口收到这条路由，最终这条路由在R2的路由表中的cost等于1加上serial4/0/0接口的cost 50也就是51，再将这条路由更新给R3，那么这条路由在R3上的cost=51+1也就是52。

由于默认的参考带宽是100M，这意味着更高带宽的传输介质（高于100M）在OSPF协议中将会计算出一个小于1的分数，这在OSPF协议中是不允许的（会被四舍五入为1）。而现今网络设备满地都是大于100M带宽的接口，这时候路由COST的计算其实就不精确了。所以可以使用bandwidth-reference 1000命令修改，但是这条命令要谨慎使用，一旦要配置，则建议全网OSPF路由器都配置。

## ospf网络类型

运行Ospf协议的接口都存在自己的网络类型，而链路的网络类型默认由接口的链路层协议所决定

![image-20230513115821469](images\image-20230513115821469.png)





## ospf特点

在OSPF网络中，每台路由器根据自己周围的网络拓扑结构生成链路状态通告LSA（Link State Advertisement），并通过更新报文将LSA发送给网络中的其它路由器。

OSPF交互的是链路状态信息。也就是说，RIP中，路由器的选路依赖于邻居路由器的路由信息，但不管邻居路由器传达的信息是否正确；而OSPF中，路由器的选路是一种“自主行为”，LSA只是一种选路的参考信息。

每台路由器都通过链路状态数据库LSDB(Link State DataBase)掌握全网的拓扑结构。如图所示，每台路由器都会收集其它路由器发来的LSA，所有的LSA放在一起便组成了链路状态数据库LSDB。LSA是对路由器周围网络拓扑结构的描述，LSDB则是对整个自治系统的网络拓扑结构的描述。路由器将LSDB转换成一张带权的有向图，这张图便是对整个网络拓扑结构的真实反映。在网络拓扑稳定的情况下，各个路由器得到的有向图是完全相同的。

![image-20230220195240662](images\image-20230220195240662.png)

路由器根据最短路径优先(Shortest Path First)算法计算到达目的网络的路径，而不是根据路由通告来获取路由信息。如图2所示，每台路由器根据有向图，使用SPF算法计算出一棵以自己为根的最短路径树，这棵树给出了到自治系统中各节点的路由。相对于RIP，这种机制极大地提升了路由器的自主选路能力，使得路由器不再依靠路由通告进行选路。

![image-20230220195306869](images\image-20230220195306869.png)





# 二 OSPF报文分析

OSPF的五种报文：
 	1. Hello : 建立和维护OSPF邻居与邻接关系,周期收发，周期保活，默认hello 包的hello time 为10s或30s , dead time 为hello time的4倍 ; 邻居间hello包中hello time和dead time必须是完全一致的参数.
 	2. DBD : 链路状态数据库描述信息（描述LSDB中LSA头部信息）
 	3. LSR : 链路状态请求，用于向OSPF邻居请求链路状态信息
 	4. LSU : 链路状态更新（携带一条或多条LSA）
 	5. LSAck : 对LSU中的LSA进行确认

ospf报文头

ospf这五种报文具有相同的报文头部，长度为24字节

Version：8bit OSPFv2值为2， OSPFv3值为3

Type： 8bit OSFP报文总长度，包括报文头在内1.hello，2,DD  3,LSR  4.LSU  5,LSACK

Packet length：16bit，OSPF报文总长度包括报文头部在内单位Byte

RouterID：32bit 发送该报文的路由器标识，刚好为ip地址长度

AreaID: 32bit，发送该报文的路由器接口所属区域

Checksum：16bit 校验和，包括除了认证字段的正报文校验和

Authtype：16bit验证类型 0不验证 1简单认证 2MD5认证

Authentication：64bit 鉴定字段。其数值根据验证类而定。

![image-20230216203600827](images\image-20230216203600827.png)

## Hellow报文

Hello报文被周期性（默认为10秒）地发向邻居路由器接口发送，如果在设定时间（默认为40秒，通常至少是Hello包发送时间间接4倍）内没有收到对方OSPF路由器发送来的Hello报文，则本地路由器会认为该对方路由器无效。报文内容包括一些定时器设置、DR、BDR以及本路由器已知的邻居路由器。

路由器运行OSPF协议后，会从所有启动OSPF协议的接口上发送Hello报文。如果两台路由器共享一条公共数据链路，并且能够成功协商各自Hello报文中所指定的某些参数，就能形成邻居关系。

![image-20230220195348910](images\image-20230220195348910.png)

![image-20230216203630359](images\image-20230216203630359.png)

Network Mask：32bit，发送Hello报文接口所在的子网掩码

Hello Interval：16bit，发送hello报文的时间间隔

Options：8bit，可选项, E：允许泛洪AS-External-LSAS, MC: 转发ip组播报文， N/P:处理Type7 LSAs DC:处理按需链路

Rtr Pri：8bit，DR优先级，默认为1，如果0不参与DR/BDR选举

Desiginated Router：32bit 本网段DR的接口地址

Neighbor：32bit 邻居列表 以routerID标识

## DBD报文



![image-20230216212202594](images\image-20230216212202594.png)

两台路由器在邻接关系初始化时，用DD报文描述自己的LSDB，进行数据库的同步。报文内容包括LSDB的每一条LSA的Header（LSA的header可以唯一标识一条LSA）。LSA Header只占一条LSA整个数据量的一小部分，这样可以减少路由器之间的协商报文浏览，对端路由器根据LSA Header就可以判断是否已有这条LSA。两台路由器在交换DD报文过程中，一台为Master，一台为Slave，Master规定起始序列号，每发送一个DD报文序列号加1，Slave方使用Master的序列号作为确认。

InterfaceMTU: 16bit，表示不分片情况下，此接口可发出的最大IP报文长度默认不填充时为0

Opstions：8bit 同hello报文opstion

​		I(Inititalzation)位：1bit，初始位，当发送连续多个DD报文时，如果这是第一个DD报文，则置为1，否则置位0

​	  M（More）位：1bit，当发送连续多个DD报文时，如果这是最后一个DD报文，则置为0，否则置为1，表示后面还有其他的DD报文

​	M/S（Master/Slave）位：1bit，当两台OSPF路由器交换DD报文时，首先需要确定双方的主从关系，Router ID大的一方会成为Master。

​	DD sequence number：32bit DD报文序列号。主从双方利用序列号来保证DD报文传输的可靠性和完整性。

​	LSA Headers：可变, 该DD报文中包含的LSA的头部信息

## LSR报文

![image-20230217203117396](images\image-20230217203117396.png)

两台路由器互相交换过DD报文之后，知道对端的路由器有哪些LSA是本地的LSDB所缺少的和哪些LSA已经失效的，这时需要发送LSR报文向对方请求所需的LSA。内容包括所需要的LSA的摘要

LS type：32bit LSA的类型号

Link State ID： 32bit 根据LSA中的LS Type和LSA description在路由域中描述一个LSA

Advertising Router：32bit 产生此LSA的路由器的Router ID

## LSU报文

![image-20230217203659993](C:\Users\cs1\AppData\Roaming\Typora\typora-user-images\image-20230217203659993.png)





用来向对端路由器发送其所需要的LSA或者泛洪自己更新的LSA，内容是多条LSA的集合。LSU报文在支持组播和广播的链路上是以组播形式将LSA泛洪出去。为了实现Flooding的可靠性传输，需要LSAack报文对其进行确认。对没有收到确认报文的LSA进行重传，重传的LSA是直接发送到邻居的。

Number of LSAs：32bit LSA的数量

## LSA报文头

![image-20230217205614378](images\image-20230217205614378.png)

所有的LSA都有相同的报文头

LS age：16bit LSA产生后所经过的时间，单位秒，无论是链路上传送还是保存在LSDB，其值是一直增长的，默认没经过一台路由器加1，如果LS age高位1， 代表进入LSDB后不老化，仅出现在DemandCircui（按需）链路上

Options：8bit 同hello的option

Ls type：8bit LSA类型

Link State ID： 32bit 与LSA中的LS Type和LSA

Advertising number：32bit LSA产生的router id

# 三 配置OSPF

```bash
Huawei]ospf 1 router-id 10.1.1.1  //动OSPF进程，进入OSPF视图,手动输入router-id
[Huawei-ospf-1]area 0  //创建并进入OSPF区域视图(骨干区域)
[Huawei-ospf-1-area-0.0.0.0]network 10.0.1.0 0.0.0.255  //配置区域所包含的网段
[Huawei-GigabitEthernet0/0/1]ospf enable 1 area 0  //在接口上使能OSPF
[Huawei-ospf-1-area-0.0.0.0]vlink-peer 10.1.1.2  //创建并配置虚连接,在虚连接的另一端也需要配置此命令
[Huawei-ospf-1]flooding-control number 50 timer-interval 30  //配置对OSPF更新LSA的泛洪限制,缺省泛洪更新LSA的数量的缺省值是50，泛洪更新LSA的时间间隔是30秒。
[Huawei]display ospf peer   //查看OSPF邻居的信息
[Huawei]display ospf  interface   //查看OSPF接口的信息
[Huawei]display ospf routing   //查看OSPF路由表的信息
[Huawei]display ospf lsdb   //查看OSPF的LSDB信息
[Huawei-ospf-1]retransmission-limit 30  //配置OSPF重传限制功能
[Huawei-GigabitEthernet0/0/1]ospf mtu-enable  //使能接口发送DD报文时填充MTU值，同时还会检查邻居DD报文所携带的MTU是否超过本端的MTU值,缺省接口发送DD报文的MTU值为0
[Huawei]display ospf retrans-queue  //查看OSPF重传列表
[Huawei-GigabitEthernet0/0/1]ospf network-type broadcast   //配置OSPF接口的网络类型,缺省以太网接口的网络类型为广播
[Huawei-GigabitEthernet0/0/1]ospf network-type nbma
[Huawei-GigabitEthernet0/0/1]ospf network-type p2mp
[Huawei-GigabitEthernet0/0/1]ospf network-type p2p
[Huawei-GigabitEthernet0/0/1]ospf network-type p2mp  -ospf p2mp-mask-ignore  //配置在P2MP网络上忽略对网络掩码的检查
[Huawei-ospf-1]filter-lsa-out peer 10.1.1.1 all  //配置在P2MP网络中对发送的LSA进行过滤
[Huawei-GigabitEthernet0/0/1]ospf network-type nbma  -ospf timer poll 120  //在NBMA接口上配置发送轮询报文的时间间隔,缺省为120秒
[Huawei-ospf-1]peer 10.1.1.1  //配置NBMA网络的邻居
[Huawei]display ospf nexthop  //查看OSPF的下一跳信息
[Huawei]display ospf routing router-id 10.0.1.1  //查看OSPF的路由表信息
[Huawei]display ospf interface all  //查看OSPF的接口信息
[Huawei-ospf-1-area-0.0.0.1]stub  //配置当前区域为STUB区域
[Huawei-ospf-1-area-0.0.0.1]stub no-summary  //配置当前区域为STUB区域, 禁止ABR向Stub区域内发送Type-3 LSA（Summary LSA）
[Huawei-ospf-1-area-0.0.0.1]stub -default-cost 1  //配置发送到Stub区域缺省路由的开销,缺省值为1
[Huawei]display ospf abr-asbr  //查看OSPF ABR及ASBR信息
[Huawei-ospf-1-area-0.0.0.2]nssa  //配置当前区域为NSSA区域
[Huawei-ospf-1-area-0.0.0.2]nssa default-route-advertise  //在ASBR上配置产生缺省的Type7 LSA到NSSA区域
[Huawei-ospf-1-area-0.0.0.2]nssa flush-waiting-timer 1  //产生老化时间被置为最大值（3600秒）的Type5 LSA，这个LSA可以及时清除其他交换机上已经没用的Type5 LSA
[Huawei-ospf-1-area-0.0.0.2]nssa no-import-route  //当ASBR同时还是ABR时，使OSPF通过import-route命令引入的外部路由不被通告到NSSA区域
[Huawei-ospf-1-area-0.0.0.2]nssa no-summary  //禁止ABR向NSSA区域内发送Summary LSA（Type3 LSA）
[Huawei-ospf-1-area-0.0.0.2]nssa set-n-bit  //交换机会与邻居交换机同步时在DD报文中设置N-bit位的标志
[Huawei-ospf-1-area-0.0.0.2]nssa translator-always  //当NSSA区域中有多个ABR时，系统会根据规则自动选择一个ABR作为转换器（通常情况下NSSA区域选择Router ID最大的设备），将Type7 LSA转换为Type5 LSA。此命令可以将某一个ABR指定为转换器。如果需要指定某两个ABR进行负载分担，可以通过配置translator-always来指定两个转换器同时工作。如果需要某一个固定的转换器，防止由于转换器变动引起的LSA重新泛洪，可以预先使用此命令指定。
[Huawei-ospf-1-area-0.0.0.2]nssa translator-interval 100  //用于转换器切换过程，保障切换平滑进行,参数的缺省间隔要大于泛洪的时间
[Huawei-ospf-1-area-0.0.0.2]default-cost 1  //配置ABR发送到NSSA区域的Type3 LSA的缺省路由的开销, 缺省为1
[Huawei-GigabitEthernet0/0/1]ospf cost 1  //设置OSPF接口的开销值
[Huawei-ospf-1]bandwidth-reference 100  //配置带宽参考值
[Huawei-ospf-1]maximum load-balancing 8  //配置最大等价路由数量
[Huawei-ospf-1]nexthop 10.1.1.1 weight 1  //配置OSPF的负载分担优先级,weight值越小，路由优先级越高,weight的缺省值是255，表示等价路由间进行负载分担，不区分优先级
[Huawei-ospf-1]undo rfc1583 compatible  //将RFC1583配置成RFC2328，配置OSPF域的路由选路规则,缺省交换机支持RFC1583的选路规则
[Huawei-ospf-1]import-route ***  //配置OSPF引入其它协议的路由
[Huawei-ospf-1]default ***  //配置OSPF引入路由时的相关参数, OSPF引入外部路由的缺省度量值为1，引入的外部路由类型为Type2，设置缺省标记值为1
[Huawei-ospf-1]default-route-advertise  //将缺省路由通告到OSPF路由区域
[Huawei-ospf-1]default-route-advertise always  //无论本机是否存在激活的非本OSPF进程的缺省路由，都会产生并发布一个描述缺省路由的LSA
[Huawei-ospf-1]default-route-advertise permit-calculate-other  //在发布缺省路由后，仍允许计算其他交换机发布的缺省路由
[Huawei-ospf-1-area-0.0.0.0]abr-summary 10.1.1.0 255.255.0.0   //配置OSPF的ABR路由聚合
[Huawei-ospf-1]asbr-summary 10.1.1.0 255.255.0.0  //配置OSPF的ASBR路由聚合
[Huawei-ospf-1]filter-policy 2000 import  //配置对接收的路由进行过滤
[Huawei-ospf-1]filter-policy ip-prefix 16 import
[Huawei-ospf-1]filter-policy acl-name A1 import
[Huawei-ospf-1]filter-policy 2000 export  //配置对发布的路由进行过滤
[Huawei-ospf-1]filter-policy ip-prefix 16 export
[Huawei-ospf-1]filter-policy acl-name A1 export
[Huawei-GigabitEthernet0/0/1]ospf filter-lsa-out all  //配置对出方向的LSA进行过滤
[Huawei-ospf-1]mesh-group enable  //使能Mesh-Group特性, 当交换机和邻居存在并行链路时，使能Mesh-Group特性，可以减轻链路的压力
[Huawei-ospf-1]lsdb-overflow-limit 100  //配置LSDB中External LSA的最大数量
[Huawei]display ospf asbr-summary   //查看OSPF ASBR聚合信息
[Huawei]bfd  //配置全局BFD功能并进入到全局BFD视图
[Huawei-ospf-1]bfd all-interfaces enable  //打开OSPF BFD特性的开关，建立BFD会话
[Huawei-ospf-1]bfd all-interfaces min-rx-interval 10 min-tx-interval 10 detect-multiplier 10  //指定需要建立BFD会话的各个参数值
[Huawei-GigabitEthernet0/0/1]ospf bfd block  //阻止接口动态创建BFD会话
[Huawei-GigabitEthernet0/0/1]ospf bfd enable   //打开接口BFD特性的开关，建立BFD会话
[Huawei-GigabitEthernet0/0/1]ospf bfd min-rx-interval 10 min-tx-interval 10 detect-multiplier 10  //指定BFD会话的参数值
[Huawei]display ospf bfd session all  //查看OSPF与BFD联动的会话信息
[Huawei-ospf-1]frr  //进入OSPF IP FRR视图
[Huawei-ospf-1-frr]loop-free-alternate  //使能OSPF IP FRR特性，生成无环的备份链路
[Huawei-ospf-1-frr]frr-policy route a1  //配置OSPF IP FRR过滤策略
[Huawei-ospf-1]bfd all-interfaces frr-binding  //配置OSPF进程下的IP FRR和BFD绑定
[Huawei-GigabitEthernet0/0/1]ospf bfd frr-binding  //配置接口下的IP FRR和BFD绑定
[Huawei-GigabitEthernet0/0/1]ospf frr block  //在指定接口上禁止OSPF IP FRR功能
[Huawei-ospf-1]prefix-priority critical ip-prefix 1  //配置OSPF路由的收敛优先级
[Huawei-ospf-1]prefix-priority high ip-prefix 1
[Huawei-ospf-1]prefix-priority medium ip-prefix 1
[Huawei-GigabitEthernet0/0/1]ospf timer hello 10  //配置接口发送Hello报文的时间间隔。缺省，P2P、Broadcast类型接口发送Hello报文的时间间隔的值为10秒；P2MP、NBMA类型接口发送Hello报文的时间间隔的值为30秒；且同一接口上邻居失效时间是Hello间隔时间的4倍
[Huawei-GigabitEthernet0/0/1]ospf timer dead 40  //设置相邻邻居失效的时间,缺省，P2P、Broadcast类型接口的OSPF邻居失效时间为40秒，P2MP、NBMA类型接口的OSPF邻居失效时间为120秒；且同一接口上失效时间是Hello间隔时间的4倍
[Huawei-GigabitEthernet0/0/1]ospf smart-discover  //配置接口的Smart-discover功能, 网络中邻居状态，或者DR、BDR发生变化时，设备不必等到Hello定时器到就可以立刻主动的向邻居发送Hello报文。从而提高建立邻居的速度，达到网络快速收敛的目的
[Huawei-ospf-1]lsa-originate-interval intelligent-timer 5000 500 1000 other-type  5  //配置LSA的更新时间间隔
[Huawei-ospf-1]lsa-arrival-interval 10  //配置LSA接收的时间间隔
[Huawei-ospf-1]lsa-arrival-interval intelligent-timer 1000 500 500  //配置LSA接收的时间间隔, 使能智能定时器intelligent-timer
[Huawei-ospf-1]spf-schedule-interval 1  //设置SPF计算间隔
[Huawei-ospf-1]spf-schedule-interval intelligent-timer 10000 500 1000  //设置SPF计算间隔, 使能智能定时器intelligent-timer
[Huawei-ospf-1]opaque-capability enable  //使能opaque-LSA特性,因为OSPF中通过Type-9类LSA对OSPF GR支持，所以需要首先使能OSPF的opauqe-LSA特性
[Huawei-ospf-1]graceful-restart  //使能OSPF GR特性
[Huawei-ospf-1]graceful-restart period 120  //配置Restarter端GR的周期,缺省为120秒
[Huawei-ospf-1]graceful-restart planned-only  //配置Restarter只支持Planned GR,缺省支持Planned GR和Unplanned GR
[Huawei-ospf-1]graceful-restart partial  //配置Restarter支持Partial GR,缺省支持Totally GR
[Huawei-ospf-1]graceful-restart helper-role acl-name A1  //配置Helper端GR的acl过滤策略
[Huawei-ospf-1]graceful-restart helper-role ip-prefix 16  //配置Helper端GR的ip-prefix过滤策略
[Huawei-ospf-1]graceful-restart helper-role ignore-external-lsa  //配置Helper不对自治系统外部的LSA（AS-external LSA）进行检查
[Huawei-ospf-1]graceful-restart helper-role planned-only  //用来配置Helper只支持Planned GR
[Huawei-ospf-1]graceful-restart helper-role never  //配置交换机不支持Helper模式
[Huawei]display ospf graceful-restart  //查看OSPF GR信息
[Huawei-ospf-1]preference 10  //配置OSPF协议的优先级, 缺省为10
[Huawei-ospf-1]preference ase 150  //设置AS-External路由的优先级, 缺省为150
[Huawei-ospf-1]preference route-policy 1  //对特定的路由通过路由策略设置优先级
[Huawei-GigabitEthernet0/0/1]ospf trans-delay 1  //配置接口传送LSA的延迟时间,缺省为1秒
[Huawei-GigabitEthernet0/0/1]ospf timer retransmit 5  //设置邻接交换机重传LSA的间隔,缺省为5秒
[Huawei-ospf-1]stub-router  //配置Stub路由器,缺省保持为Stub路由器的时间间隔是500秒
[Huawei-ospf-1]silent-interface all  //禁止OSPF接口发送和接收协议报文, 只对本进程已经使能的接口起作用，对其它进程的接口不起作用
[Huawei]ospf valid-ttl-hops 255  //配置OSPF GTSM功能和需要检测的TTL值
[Huawei-ospf-1-area-0.0.0.0]authentication-mode simple cipher abc@123  //配置OSPF区域的验证模式（简单验证）
[Huawei-ospf-1-area-0.0.0.0]authentication-mode hmac-md5  //配置OSPF区域的验证密文模式
[Huawei-ospf-1-area-0.0.0.0]authentication-mode keychain a1  //配置OSPF区域的Keychain验证模式
[Huawei-GigabitEthernet0/0/1]ospf authentication-mode simple cipher abc@123  //配置OSPF接口的验证模式（简单验证）
[Huawei-GigabitEthernet0/0/1]ospf authentication-mode hmac-md5  //配置OSPF接口的验证密文模式
[Huawei-GigabitEthernet0/0/1]ospf authentication-mode null  //不对OSPF接口进行验证
[Huawei-GigabitEthernet0/0/1]ospf authentication-mode keychain a1  //配置OSPF接口的Keychain验证模式
[Huawei]display ospf request-queue  //查看OSPF请求列表
[Huawei]display ospf retrans-queue  //查看OSPF重传列表
[Huawei]display ospf error  //查看OSPF的错误信息
[Huawei]ospf mib-binding 1  //配置OSPF MIB绑定
[Huawei]snmp-agent trap enable feature-name ospf  //打开OSPF模块的告警开关
[Huawei-ospf-1]enable log  //使能日志信息
[Huawei]display ospf brief  //查看OSPF MIB绑定信息
[Huawei]display snmp-agent trap feature-name ospf all  //命令查看OSPF模块的所有告警信息
reset ospf 1 counters  //清除OSPF计数器
reset ospf 1 counters neighbor   ////清除OSPF计数器和指定接口上邻居的信息
reset ospf redistribution  //重新引入路由
reset ospf process  //重启OSPF进程
```

## OSPF的三张表

### 邻居表（Peer table）：

OSPF是一种可靠的路由协议，要求在路由器之间传递链路状态通告之前，需先建立OSPF邻居关系，hello报文用于发现直连链路上的其他OSPF路由器，再经过一系列的OSPF消息交互最终建立起全毗邻的邻居关系，其中两者之间需要经历几个邻居关系状态，这也是一个重要的知识点。路由器在各个激活的OSPF的接口上维护的邻居都列在邻居表中，通过观察邻居表，能够进一步了解OSPF路由器之间的邻居状态。


![image-20230217210427626](images\image-20230217210427626.png)

### 链路状态数据库LSDB（Link-state database）

OSPF用LSA（link state Advertisement 链路状态通告）来描述网络拓扑信息，然后OSPF路由器用链路状态数据库来存储网络的这些LSA。OSPF将自己产生的以及邻居通告的LSA搜集并存储在链路状态数据库LSDB中。掌握LSDB的查看以及对LSA的深入分析才能够深入理解OSPF。


![image-20230217210503979](images\image-20230217210503979.png)

自己产生的1类ls

![image-20230217210553514](images\image-20230217210553514.png)

### OSPF路由表（Routing table）

对链路状态数据库进行SPF（Dijkstra）计算，而得出的OSPF路由表。

![image-20230217210658975](images\image-20230217210658975.png)

## OSPF邻接关系建立过程

![image-20230217210804390](images\image-20230217210804390.png)

OSPF邻居关系的建立过程是我们在学习OSPF过程中的一个重点，而且非常具有研究价值，就OSPF的实际部署而言，掌握这里头的机制也是很有必要的，因为邻居关系的建立是OSPF工作的基本，如果连邻居关系都建立不起来，就别谈其他的了。

1、启动配置完成后，运行ospf协议的路由器，将组播收发hello包；若hello包中存在本地的RID，视为对端已经认识本地，故标志邻居关系建立,生成邻居表；
2、进行条件匹配：匹配失败将停留于邻居关系，仅hello周期保活即可；
3、匹配成功者后：将建立邻接（毗邻）关系；首先使用不携带数据库目录的DBD进行主从关系选举；之后主优先与从进行DBD目录交换；交换后再使用LSR/LSU/LSack来获取未知的LSA信息；直到邻接间数据库完全一致；生成LSDB表；-链路状态数据库（该网络所有LSA的集合）
4、当数据库的同步完成后：本地将所有的LSA进行组合；生成有向图—>最短路径树将最佳路径加载到本地的路由表中；网络收敛完成，hello包周期保活；之后的每30min邻接关系间周期比对下一数据库目录；（查漏补缺）
![image-20230217210955399](images\image-20230217210955399.png)

Down：这是邻居的初始状态，表示没有从邻居收到任何信息。在NBMA网络上，此状态下仍然可以向静态配置的邻居发送Hello报文，发送间隔为PollInterval，通常和Router DeadInterval间隔相同。

Attempt：此状态只在NBMA网络上存在，表示没有收到邻居的任何信息，但是已经周期性的向邻居发送报文，发送间隔为HelloInterval。如果Router DeadInterval间隔内未收到邻居的Hello报文，则转为Down状态。

Init：在此状态下，路由器已经从邻居收到了Hello报文，但是自己不在所收到的Hello报文的邻居列表中，表示尚未与邻居建立双向通信关系。在此状态下的邻居要被包含在自己所发送的Hello报文的邻居列表中。

2-Way Received：此事件表示路由器发现与邻居的双向通信已经开始（发现自己在邻居发送的Hello报文的邻居列表中）。Init状态下产生此事件之后，如果需要和邻居建立邻接关系则进入ExStart状态，开始数据库同步过程，如果不能与邻居建立邻接关系则进入2-Way。

2-Way：在此状态下，双向通信已经建立，但是没有与邻居建立邻接关系。这是建立邻接关系以前的最高级状态。

1-Way Received：此事件表示路由器发现自己没有在邻居发送Hello报文的邻居列表中，通常是由于对端邻居重启造成的。

ExStart：这是形成邻接关系的第一个步骤，邻居状态变成此状态以后，路由器开始向邻居发送DD报文。主从关系是在此状态下形成的；初始DD序列号是在此状态下决定的。在此状态下发送的DD报文不包含链路状态描述。

Exchange：此状态下路由器相互发送包含链路状态信息摘要的DD报文，描述本地LSDB的内容。

Loading：相互发送LS Request报文请求LSA，发送LS Update通告LSA。

Full：两台路由器的LSDB已经同步。

## OSPF网络类型

OSPF是一个**“接口敏感型”协议**，这句话非常值得细细品味。在上面我们介绍ospf cost的时候，就曾经讲过，路由的cost实际上得累加上入接口的cost。而OSPF中后续要介绍的DR、BDR的概念，实际上也是基于接口的，另外邻居关系的建立，也是与接口有关，因此其实很多机制着眼点都与接口有关。一旦我们在某个接口上激活了OSPF，那么这个接口将会根据该接口的二层（数据链路层）封装，捆绑对应的OSPF网络类型，注意，不同的OSPF接口网络类型，OSPF在该接口上的操作将有所不同。OSPF支持的网络类型：

​	· 点到点网络（PPP/HDLC GRE , 串线）

​	· 广播型多路访问网络（BMA , 以太网）

​	· 非广播型多路访问网路（NBMA，MGRE）

​	· P2MP网络

如果一个接口是以太网接口，那么该接口激活OSPF后，该接口的缺省OSPF网络类型为Broadcast也就是广播型多路访问网络。而如果一个接口是serial接口，二层封装为HDLC或者PPP，那么激活OSPF后，其缺省的OSPF网络类型就是Point-to-Point也就是点对点。
接口的OSPF网络类型是可以通过命令修改的。

### DR、BDR

![image-20230217211243611](images\image-20230217211243611.png)

在广播多路访问网络（Multi Access）中，例如以太接口，所有的路由器的接口都是相同网段、处于同一个广播网络中，这些接口如果两两建立OSPF邻居关系，这就意味着，网络有：**n(n-1)/2**这么多个OSPF邻居关系，维护如此多的邻居关系不仅仅**额外消耗设备资源**，更是**增加了网络中LSA的泛洪数量**

为减小多路访问网络中的 OSPF 流量，OSPF 会在每一个MA网络（多路访问网络）选举一个指定路由器 (DR) 和一个备用指定路由器 (BDR)。

DR选举规则：最高OSPF接口优先级拥有者被选作DR，如果优先级相等（默认为1），具有最高的OSPF Router-ID的路由器被选举成DR，并且DR具有非抢占性，也就是说如果该MA网络中，已经选举完成、并且选举出了一个DR，那么后续即使有新的、更高优先级的设备加入，也不会影响DR的选举，除非DR挂掉。

**指定路由器 (DR)：**DR 负责侦听多路访问网络中的拓扑变更信息并将变更信息通知给其他路由器，同时负责代表该MA网络发送LSA类型2。**MA网络中，所有的OSPF路由器都与DR建立全毗邻的OSPF邻接关系。**

**备用指定路由器 (BDR)**：BDR 会监控 DR 的状态，并在当前 DR 发生故障时接替其角色

注意OSPF为“接口敏感型协议”，**DR及BDR的身份状态是基于OSPF接口的**，所以如果我们说：“这台路由器是DR”实际上这种说法是不严谨的，严格的说，应该是：“**这台路由器的这个接口，在这个MA网络上是DR**”。

MA网络中，所有的DRother路由器均只与DR和BDR建立全毗邻的邻接关系，DRother间不建立全毗邻邻接关系，如此一来，该多路访问网络中设备需要维护的OSPF邻居关系大幅减小：**M= (n-2)×2+1**，LSA的泛洪问题也可以得到一定的缓解

路由器的接口如果网络类型为**广播多路访问**或者**非广播多路访问**型，那么**都会进行DR/BDR的选举**。所以我们看，OSPF接口网络类型的不同，OSPF的操作是有所不同的。**在P2P或者P2MP类型的接口上，就不选举DR\BDR**。

接下去看看在MA网络中，有了DR、BDR的存在后，LSA的泛洪：

![image-20230217211620837](images\image-20230217211620837.png)

假设网络已经完成了OSPF收敛，现在突然R3下挂的一个网络发生了故障
路由器R3用224.0.0.6通知DR及BDR
DR、BDR监听224.0.0.6这一组播地址
DR向组播地址224.0.0.5发送更新以通知其它路由器
所有的OSPF路由器监听224.0.0.5这一组播地址
路由器收到包含变化后的LSA的LSU后，更新自己的LSDB，过一段时间(SPF延迟)，对更新的链路状态数据库执行SPF算法，必要时更新路由表。
这里有个知识点要记住，OSPF使用两个well-know的组播地址：224.0.0.5及224.0.0.6，这是一个常识，需熟记。所有的OSPF路由器（的接口）都会侦听发向224.0.0.5这个组播地址的报文，所有DR/BDR都会侦听224.0.0.6

### **广播链路或者NBMA链路上DR和BDR的选举过程如下：**

1. 接口UP后，发送Hello报文，同时进入到Waiting状态。在Waiting状态下会有一个WaitingTimer，该计时器的长度与DeadTimer是一样的。默认值为40秒，用户不可自行调整。OSPF接口状态的详细描述，请参见OSPF接口状态机。
2. 在WaitingTimer触发前，发送的Hello报文是没有DR和BDR字段的。在Waiting阶段，如果收到Hello报文中有DR和BDR，那么直接承认网络中的DR和BDR，而不会触发选举。直接离开Waiting状态，开始邻居同步。
3. 假设网络中已经存在一个DR和一个BDR，这时新加入网络中的路由器，不论它的Router ID或者DR优先级有多大，都会承认现网中已有的DR和BDR。
4. 当DR因为故障Down掉之后，BDR会继承DR的位置，剩下的优先级大于0的路由器会竞争成为新的BDR。
5. 只有当不同Router ID，或者配置不同DR优先级的路由器同时起来，在同一时刻进行DR选举才会应用DR选举规则产生DR。该规则是：优先选择DR优先级最高的作为DR，次高的作为BDR。DR优先级为0的路由器只能成为DR Other；如果优先级相同，则优先选择Router ID较大的路由器成为DR，次大的成为BDR，其余路由器成为DR Other。



## OSPF 区域（area）的概念

### 单区域存在的问题

设想一下，如果OSPF没有区域的概念，或者整个OSPF网络就是一个区域，那么会有什么问题？在一个区域内，LSA会被泛洪，并且同一个区域的OSPF路由器，关于该区域的LSA会同步，这样一来，如果整个网络就一个单独的区域的话，如果规模非常庞大，那么LSA的泛洪会很严重，OSPF路由器的负担很大，因为OSPF要求区域内的所有路由器，LSDB必须统一，这样以便计算出一个统一的、无环的拓扑；


区域内部动荡会影响全网路由器的SPF计算；
LSDB庞大，资源消耗过多，设备性能下降，影响数据转发；
每台路由器都需要维护的路由表越来越大，单区域内路由无法汇总

### OSPF多区域

![image-20230217211845075](images\image-20230217211845075.png)

基于上述原因，OSPF设计了区域area的概念
多区域的设计减少了LSA洪泛的范围，有效地把拓扑变化控制在区域内，达到网络优化的目的
在区域边界可以做路由汇总，减小了路由表
充分利用OSPF特殊区域的特性，进一步减少LSA泛洪，从而优化路由
多区域提高了网络的扩展性，有利于组建大规模的网络

在部署OSPF时，要求全OSPF域，必须有且只能有一个area0，Area 0为骨干区域，骨干区域负责在非骨干区域之间发布由区域边界路由器汇总的路由信息（并非详细的链路状态信息），为避免区域间路由环路，非骨干区域之间不允许直接相互发布区域间路由。因此，所有区域边界路由器都至少有一个接口属于Area 0，即每个区域都必须连接到骨干区域。

OSPF路由器的角色：
	区域内路由器Internal Router
	区域边界路由器Area Border Router
	骨干路由器Backbone Router
	AS边界路由器AS Boundary Router

​	

# 四 OSPF LSAs及特殊区域

前面我们已经介绍过了，对于OSPF这类的链路状态路由协议而言，LSA链路状态通告是工作在底层、最为关键、最为核心的构件，正因为有了LSA，OSPF能够准确的描述网络拓扑并且最终计算出最优的路由。OSPF设计了多种LSA，以便描述网络拓扑及各种类型的路由。

## LSA详解

### LSA类型1-路由器LSA（Router SLA）

每一台运行OSPF的路由器均会产生1类LSA，1类LSA怎么理解？其实很简单，就是每台路由器描述一下自己“家门口的状况”，并且只会告诉给“全村的人”（**本区域内泛洪**）

**1类LSA主要的功能有以下两点：**

描述路由器的特殊角色，如Virtual-link、ABR、ASBR：
这是通过1类LSA中相关的V、B、E位的置1来体现的，例如如果本台设备是ABR，那么它产生的1类LSA中B位会置1。
描述本路由器在某个区域内部的直连链路（接口）及接口COST值。

1类LSA的链路状态信息主要由链路类型、Link ID、Link Data、Cost三个值来进行描述。

描述P2P型网络自身的邻居，以及广播型网络自身连着的伪节点

![image-20230217212553083](images\image-20230217212553083.png)

例如上图中，所有OSPF路由器都会产生1类LSA，并且在本区域内泛洪。我们以R1举例，它会产生一个类型1的LSA，那么在这个LSA1中，包含两个链路的描述，一个用于描述Loopback接口以及接口的COST值，另一个是描述GE0/0/0接口以及COST值。这个1类LSA会在area1内泛洪。
![image-20230217212708055](images\image-20230217212708055.png)

实际上在area1内，OSPF路由器关于area1的LSDB都是统一的。在上面的LSDB中我们观察到了1、2、3类LSA。重点来看一下自己产生的1类LSA：

![image-20230217212812074](images\image-20230217212812074.png)

![image-20230217213106345](images\image-20230217213106345.png)



我们来总结一下，针对不同的链路类型，OSPF 1类LSA在描述不同链路类型的时候，LSID及Data字段的内容有不同：

![image-20230217212914289](images\image-20230217212914289.png)

### LSA类型2-网络LSA（Network LSA）

在多路访问型MA网络中（例如以太网，或者帧中继网络），会选举DR、BDR，而所有的Drother都只能和DR及BDR建立邻接关系，Drother也就是非DR、BDR路由器之间不会建立全毗邻的OSPF邻接关系。

从某种层面上说，DR实际上代表了这个MA网络，在本区域内泛洪2类LSA，来呈现该MA网络中的所有路由器。因此2类LSA仅存在于有MA网络的area中，并且由DR发送，用来描述这个MA网络中的所有路由器（的Router-ID）。
![image-20230217213222613](images\image-20230217213222613.png)

在上例中，R3的GE0/0/0口是123.0网络的DR，因此R1、R2都只和R3建立全毗邻的邻接关系。这时候R3就成了这个MA网络的代表者，其发送2类LSA，该LSA包含的内容如图，详细信息见下，**注意该2类LSA也只是在area1内泛洪**。

总结一下：
2类LSA，也就是网络LSA，由DR产生，描述其在该MA网络上连接的所有路由器的RouterID（包括DR自己）以及该MA网络的掩码。
2类LSA只在本区域Area内洪泛，不允许跨越ABR。而且只有在MA网络才会出现。
2类LSA中没有COST字段（因此需借助1类LSA来进行SPF算法）

得益于1、2类LSA，OSPF在一个区域内的路由计算就没有问题了。

![image-20230513120055106](images\image-20230513120055106.png)

### LSA类型3-网络汇总LSA（Network Summary LSA）

两类LSA解决了区域内路由计算的问题，那么区域间呢？如果路由器需要访问其他区域呢？
这时就需要3类LSA。3类LSA是网络汇总LSA，这里的“汇总”二字，其实翻译为“归纳”更贴切，它和路由汇总是完全不同的概念。由于ABR同时属于两个以上的区域（其中必须有骨干区域），它知道这些区域的1、2类LSA，那么就能做件事：将某个区域的1、2类LSA，做个归纳，然后为其他区域生成3类LSA并泛洪到其他区域中，如此一来，区域间的路由计算就没问题了。
因此3类LSA，由ABR产生：


![image-20230217213327955](images\image-20230217213327955.png)

上图中，R3将area0内的LSA1做了归纳，然后为area1注入LSA3，这个LSA3实际上是描述的192.168.34.0/24这个网段，以及cost值，当然，这个cost值实则为R3的Serial4/0/0口的接口cost。

![image-20230217213405893](images\image-20230217213405893.png)

上图是R3将area1内的网络信息通过LSA3注入到了area0中，其中包含三个网段信息，分别是192.168.123.0/24、1.1.1.1/32、2.2.2.2/32。那么这样一来R4就能进行计算，得出三条路由。

### LSA类型4-ASBR汇总LSA（ASBR Summary LSA）

![image-20230217213448909](images\image-20230217213448909.png)

为了讲解LSA4及LSA5，我们需要将配置做点小变更。在R4上，我们开设一个新的Loopback接口，配置一个IP地址，子网位44.44.44.0/24，现在我们使用import-route的方式，将44.44.44.0/24的直连路由重发布进OSPF。然后继续我们的讲解：
4类LSA是一个指向ASBR的LSA，由该ASBR所在的area中的ABR产生（这点要格外留意）。
ASBR作为域边界路由器，将外部的路由通过重发布的方式注入了OSPF域，这些外部路由在OSPF中进行传递（这些外部路由是以5类LSA的形式在域内传播），而我们OSPF内部的路由器如果想前往这些外部网段，则需要同时具备两个条件：

· 知道外部的路由（这通过重发布的动作，已经完成了注入，借助5类LSA完成传播）

· 知道完成这个重分发动作的ASBR的位置

也就是说，我们在围城里，想要去围城外的某个地方，需具备两个条件，1是你要知道外头有什么，2是你要知道城门在哪里，所以**5类LSA告诉你外头有啥**，**4类LSA告诉你城门是谁**。

关键在于第二点。与ASBR在同一区域的区域内部路由器（例如本实验中的R3），能通过ASBR（R4）产生的1类LSA知道该ASBR的位置（1类LSA中E位=1，所以与ASBR同区域的路由器都知道），但是问题来了，1类LSA的泛洪范围是本区域内，那么该区域外的路由器（如area1中的R1、R2），如何得知这台ASBR的位置呢？那么就需要借助4类LSA了。
![image-20230217213541863](images\image-20230217213541863.png)

因此**4类LSA由ABR产生，用来告诉与ASBR不在同一个区域内的其他OSPF Router关于 ASBR的信息**。

上图中R4作为ASBR，做了路由import，将直连路由4.4.4.4/32引入了OSPF。这些路由通过5类LSA的形式在OSPF Domain里扩散。但是4.4.4.4/32的路由要真正加载进OSPF路由表，还需要一个重要因素，那就是他们得知道注入这条外部路由的ASBR在哪儿。我们已经说了，与ASBR R4同处一个area的R3已经通过LSA1知道了ASBR，但是area1内的路由器却并不知道，因为R4产生的1类LSA只能够在area0内泛洪。

在这个时候，R3作为ABR，就扮演一个重要作用，它自己得知ASBR的位置后，会向area1注入4类LSA，用于描述ASBR。这样一来area1内的R1及R2就既通过LSA5学习到了路由4.4.4.4/32，又通过LSA4了解到了ASBR的位置，因此这条外部路由才能够被加载进他们的路由表中。

### LSA类型5-AS外部LSA AS External LSA）

![image-20230217213642540](images\image-20230217213642540.png)

R4此刻已经是一台ASBR了，因为它将外部路由44.44.44.0/24通过import-route的方式注入到了OSPF中，这条外部路由实际上是通过LSA5在整个OSPF domain内泛洪。

### LSA类型7：NSSA外部LSA（NSSA External LSA）

类LSA是一种非常特殊的LSA，要注意的是这种LSA作为一种描述外部路由的LSA它只能被在NSSA中进行泛洪，不能跨越NSSA进入骨干区域0。特殊区域NSSA会阻挡从骨干区域area0中过来的5类LSA进入，同时允许NSSA本地始发外部路由，这些外部路由以7类LSA的形式在本地NSSA中进行泛洪，当这些7类LSA到达NSSA的ABR时，由该ABR负责将这些7类LSA转换成5类LSA，方可注入骨干区域
![image-20230217213715473](images\image-20230217213715473.png)

留意一下上图，我们将配置做一点变更：将area1配置为NSSA。然后在R1上再创建一个Loopback1，配置一个11.11.11.0/24的子网IP，然后将这个直连路由import到OSPF中：

![image-20230217213737161](images\image-20230217213737161.png)

这样一来，这条外部路由由于是在特殊区域NSSA中被注入的，那么它是以LSA类型7注入进来，并在NSSA area1内泛洪的。

与5类LSA没有明显的差别。两者都用于描述外部路由。但是**7类LSA只能够存在于NSSA中，不能被泛洪到常规区域中**

但是7类LSA是不能进入area0的，那么area0内的用户如何能够学习到这条外部路由呢？R3作为一台ABR，就发挥了很重要的作用，它会做一个“7转5”的动作，也就是将7类LSA转换成5类LSA，然后在泛洪到area0中，从而泛洪到其他常规区域中：

![image-20230217213827912](images\image-20230217213827912.png)

### 如何判断LSA的新旧

Seq越大的越新
Seq相同，则比较Checksum，越大越新
checksum相同，判断LSA age，age为3600s为最新（用于删除此LSA）
LSA age都不为3600s，则判断LSA age的差值。差值大于900s，小的最新。差值小于等于900s，LSA的新旧相同（此LSA不需要交换）

## Stub area末梢区域

**区域里面允许出现1类、2类、3类LSA ，不允许出现4/5类 LSA，会生成 一条默认的三类LSA**

STUB特点：

 1、骨干区域不能被配置为Stub区域。

 2、如果要将一个区域配置成Stub区域，则该区域中的所有路由器必须都要配置成Stub路由器。

 3、Stub区域内不能存在ASBR，自治系统外部路由不能在本区域内传播。

 4、该区域没有虚链路穿越。

 5、当外部网络发生变化后，Stub区域内的路由器是不会直接受到影响

 6、所有STUB区域的路由器上均做STUB配置。

 7、该区域存在一个或多个ABR。**STUB作用：**

 1、拒绝四类、五类LSA

 2、下发三类LSA默认路由。

 **配置：**

```
AR4P配置
[Huawei]ospf 1
[Huawei-ospf-1]area  1
[Huawei-ospf-1-area-0.0.0.1]stub       //区域内所有设备都配置

AR1配置
[Huawei]ospf 1
[Huawei-ospf-1]area 1
[Huawei-ospf-1-area-0.0.0.1]stub      //区域内所有设备都配置  
[Huawei-ospf-1-area-0.0.0.1]quit
[Huawei]display  ospf lsdb               //查看ospf数据库

```

## Totally stub area完全末梢区域

**区域里面允许出现1/2类LSA ，不允许出现3/4/5类LSA ，但是会生成一条默认的3类LSA**

**作用：**

1、拒绝三类、四类、五类LSA

2、下发三类LSA默认路由。

```
AR4配置
[Huawei]ospf 1
[Huawei-ospf-1]area  1
[Huawei-ospf-1-area-0.0.0.1]stub  no-summary       //在STUB 基础上 ，ABR上追加此命令

AR1配置
[Huawei]ospf 1
[Huawei-ospf-1]area  1
[Huawei-ospf-1-area-0.0.0.1]stub  no-summary        //在STUB 基础上 ，ABR上追加此命令

[Huawei]display  ospf lsdb                 查看ospf数据库
	 OSPF Process 1 with Router ID 1.1.1.1
		 Link State Database 

		         Area: 0.0.0.1
 Type      LinkState ID    AdvRouter          Age  Len   Sequence   Metric
 Router    2.2.2.2         2.2.2.2             86  36    8000000A       1
 Router    1.1.1.1         1.1.1.1             81  48    8000000E       1
 Network   192.168.2.1     1.1.1.1             81  32    80000002       0
 Sum-Net   0.0.0.0         2.2.2.2            454  28    80000001       1

```

## Not-So-Stubby Area 非完全末梢区域（NSSA）

允许出现1/2/3/7类LSA , 会生成一条缺省的7类LSA ，不允许出现的4/5LSA，在ABR上 7类自动转为5类

​	允许存在ASBR；
​	该区域ASBR引入的外部路由产生七类LSA；
​	区域所有的设备均需配置；
​	该区域七类LSA传播到其他区域时，将有此区域的ABR转换成五类LSA；
​	默认，该区域的ABR不会向此区域通告缺省路由

**作用：**

 过滤三类、四类、五类LSA（远端传递过来的）

```
配置命令
[Huawei]ospf 1
[Huawei-ospf-1]area  1
[Huawei-ospf-1-area-0.0.0.1]nssa
```

## totally-NSSA

**区域里面允许出现1/2/7类LSA 以及一条 缺省的7类LSA 和一条缺省的3类LSA ，不允许出现的是3/4/5类LSA**

```
配置命令
[R3]ospf 1
[R3-ospf-1]area 2
[R3-ospf-1-area-0.0.0.2]nssa no-summary    //在NSSA 基础上 ，ABR上追加此命令

```

OSPF特殊区域类型（优化OSPF数据库和路由表）：

![image-20230217214132731](images\image-20230217214132731.png)

## **OSPF区域间环路及防环方法**

OSPF在区域内部运行的是SPF算法，这个算法能够保证区域内部的路由不会成环。

然而划分区域后，区域之间的路由传递实际上是一种类似距离矢量算法的方式，这种方式容易产生环路。

为了避免区域间的环路，OSPF规定直接在两个非骨干区域之间发布路由信息是不允许的，只允许在一个区域内部或者在骨干区域和非骨干区域之间发布路由信息。

因此，每个ABR都必须连接到骨干区域。

假设OSPF允许非骨干区域之间直接传递路由，则可能会导致区域间环路。

如图所示，骨干区连接到其他网络的路由信息会传递至Area 1。

![image-20230220204827018](images\image-20230220204827018.png)



假设非骨干区之间允许直接传递路由信息，那么这条路由信息最终又被传递回去，形成区域间的路由环路。

为了防止这种区域间环路，OSPF禁止Area 1和Area 3，以及Area 2和Area 3之间直接进行路由交互，而必须通过骨干区域进行路由交互。这样就能防止区域间环路的产生。

## **OSPF缺省路由**

缺省路由是指目的地址和掩码都是0的路由。

当设备无精确匹配的路由时，就可以通过缺省路由进行报文转发。

由于OSPF路由的分级管理，Type3缺省路由的优先级高于Type5或Type7路由。

OSPF缺省路由通常应用于下面两种情况：

​	由区域边界路由器（ABR）发布Type3缺省Summary LSA，用来指导区域内设备进行区域之间报文的转发。

​	由自治系统边界路由器（ASBR）发布Type5外部缺省ASE LSA，或者Type7外部缺省NSSA LSA，用来指导自治系统（AS）内设备进行自治系统外报文的转发。

OSPF缺省路由的发布原则如下：

​	OSPF路由器只有具有对区域外的出口时，才能够发布缺省路由LSA。

​	如果OSPF路由器已经发布了缺省路由LSA，那么不再学习其它路由器发布的相同类型的缺省路由LSA。

即路由计算时不再计算其它路由器发布的相同类型的缺省路由LSA，但数据库中存有对应LSA。- 外部缺省路由的发布如果要依赖于其它路由，那么被依赖的路由不能是本OSPF路由域内的路由，即不是本进程OSPF学习到的路由。因为外部缺省路由的作用是用于指导报文的域外转发，而本OSPF路由域的路由的下一跳都指向了域内，不能满足指导报文域外转发的要求。

不同区域缺省路由发布原则:

**普通区域**

缺省情况下，普通OSPF区域内的OSPF路由器是不会产生缺省路由的，即使它有缺省路由。当网络中缺省路由通过其他路由进程产生时，路由器必须将缺省路由通告到整个OSPF自治系统中。

实现方法是在ASBR上手动通过命令进行配置，产生缺省路由。配置完成后，路由器会产生一个缺省ASE LSA（Type5 LSA），并且通告到整个OSPF自治系统中。

**Stub区域**

Stub区域不允许自治系统外部的路由（Type5 LSA）在区域内传播。区域内的路由器必须通过ABR学到自治系统外部的路由。实现方法是ABR会自动产生一条缺省的Summary LSA（Type3 LSA）通告到整个Stub区域内。这样，到达自治系统的外部路由就可以通过ABR到达。

**Totally Stub区域**

Totally Stub区域既不允许自治系统外部的路由（Type5 LSA）在区域内传播，也不允许区域间路由（Type3 LSA）在区域内传播。区域内的路由器必须通过ABR学到自治系统外部和其他区域的路由。实现方法是配置Totally Stub区域后，ABR会自动产生一条缺省的Summary LSA（Type3 LSA）通告到整个Stub区域内。这样，到达自治系统外部的路由和其他区域间的路由都可以通过ABR到达。

**NSSA区域**

NSSA区域允许引入通过本区域的ASBR到达的少量外部路由，但不允许其他区域的外部路由ASE LSA（Type5 LSA）在区域内传播。即到达自治系统外部的路由只能通过本区域的ASBR到达。

只配置了NSSA区域是不会自动产生缺省路由的。

此时，有两种选择：

​	如果希望到达自治系统外部的路由通过该区域的ASBR到达，而其它外部路由通过其它区域出去。此时，ABR会产生一条Type7 LSA的缺省路由，通告到整个NSSA区域内。这样，除了某少部分路由通过NSSA的ASBR到达，其它路由都可以通过NSSA的ABR到达其它区域的ASBR出去。

​	如果希望所有的外部路由只通过本区域NSSA的ASBR到达。则必须在ASBR上手动通过命令进行配置，使ASBR产生一条缺省的NSSA LSA（Type7 LSA），通告到整个NSSA区域内。这样，所有的外部路由就只能通过本区域NSSA的ASBR到达。

上面两种情况的区别是：

​	在ABR上无论路由表中是否存在缺省路由0.0.0.0，都会产生Type7 LSA的缺省路由。

​	在ASBR上只有当路由表中存在缺省路由0.0.0.0时，才会产生Type7 LSA的缺省路由。

因为缺省路由只是在本NSSA区域内泛洪，并没有泛洪到整个OSPF域中，所以本NSSA区域内的路由器在找不到路由之后可以从该NSSA的ASBR出去，但不能实现其他OSPF域的路由从这个出口出去。Type7 LSA缺省路由不会在ABR上转换成Type5 LSA缺省路由泛洪到整个OSPF域。

**Totally NSSA区域**

Totally NSSA区域既不允许其他区域的外部路由ASE LSA（Type5 LSA）在区域内传播，也不允许区域间路由（Type3 LSA）在区域内传播。

区域内的路由器必须通过ABR学到其他区域的路由。

实现方法是配置Totally NSSA区域后，ABR会自动产生一条缺省的Type3 LSA通告到整个NSSA区域内。

这样，其他区域的外部路由和区域间路由都可以通过ABR在区域内传播。



# 五 OSPF状态机

## **接口状态机**

OSPF设备从接口获取链路信息后，与相邻设备建立邻接关系，交互这些信息。在建立邻接关系之前，邻居设备间需要明确角色分工才能正常建立连接。OSPF接口信息的State字段（可通过display ospf interface命令查看）表明了OSPF设备在对应链路中的作用。

### **OSPF接口共有以下七种状态：**

- **Down**：接口的初始状态。表明此时接口不可用，不能用于收发流量。
- **Loopback**：设备到网络的接口处于环回状态。环回接口不能用于正常的数据传输，但可以通过Router-LSA进行通告。因此，进行连通性测试时能够发现到达这个接口的路径。
- **Waiting**：设备正在判定网络上的DR和BDR。在设备参与DR和BDR选举前，接口上会启动Waiting定时器。在这个定时器超时前，设备发送的Hello报文不包含DR和BDR信息，设备不能被选举为DR或BDR。这样可以避免不必要地改变链路中已存在的DR和BDR。仅NMBA网络、广播网络有此状态。
- **P-2-P**：接口连接到物理点对点网络或者是虚拟链路，这个时候设备会与链路连接的另一端设备建立邻接关系。仅P2P、P2MP网络有此状态。
- **DROther**：设备没有被选为DR或BDR，但连接到广播网络或NBMA网络上的其他设备被选举为DR。它会与DR和BDR建立邻接关系。
- **BDR**：设备是相连的网络中的BDR，并将在当前的DR失效时成为DR。该设备与接入该网络的所有其他设备建立邻接关系。
- **DR**：设备是相连的网络中的DR。该设备与接入该网络的所有其他设备建立邻接关系。

OSPF接口根据不同的情况（即输入事件）在各状态中进行灵活转换，这样就形成了一个高效运作的接口状态机

![image-20230220195813508](images\image-20230220195813508.png)

## **邻居状态机**

在OSPF网络中，相邻设备间通过不同的邻居状态切换，最终可以形成完全的邻接关系，完成LSA信息的交互。

OSPF邻居信息的State字段（可通过display ospf peer命令查看）表明了OSPF设备的邻居状态。

### **OSPF邻居共有以下八种状态：**

Down：邻居会话的初始阶段。

​	表明没有在邻居失效时间间隔内收到来自邻居设备的Hello报文。

​	除了NBMA网络OSPF路由器会每隔PollInterval时间对外轮询发送Hello报文，包括向处于Down状态的邻居路由器（即失效的邻居路由器）发送之外，其他网络是不会向失效的邻居路由器发送Hello报文的。

Attempt：这种状态适用于NBMA网络，邻居路由器是手工配置的。

​	邻居关系处于本状态时，路由器会每隔HelloInterval时间向自己手工配置的邻居发送Hello报文，尝试建立邻居关系。

init：本状态表示已经收到了邻居的Hello报文，但是对端并没有收到本端发送的Hello报文，收到的Hello报文的邻居列表并没有包含本端的Router ID，双向通信仍然没有建立。

2-Way：互为邻居。本状态表示双方互相收到了对端发送的Hello报文，报文中的邻居列表也包含本端的Router ID，邻居关系建立。如果不形成邻接关系则邻居状态机就停留在此状态，否则进入ExStart状态。

DR和BDR只有在邻居状态处于2-Way及之后的状态才会被选举出来。

ExStart：协商主从关系。建立主从关系主要是为了保证在后续的DD报文交换中能够有序的发送。邻居间从此时才开始正式建立邻接关系。

Exchange：交换DD报文。本端设备将本地的LSDB用DD报文来描述，并发给邻居设备。

Loading：正在同步LSDB。两端设备发送LSR报文向邻居请求对方的LSA，同步LSDB。

Full：建立邻接。两端设备的LSDB已同步，本端设备和邻居设备建立了完全的邻接关系。

![image-20230220200016538](images\image-20230220200016538.png)

### **OSPF邻接关系的建立**

#### **邻居关系**

使能OSPF功能的接口会周期性地发送Hello报文，与网络中其他收到Hello报文的路由器协商报文中的指定参数，包括区域号、验证模式、发送Hello报文的时间间隔、路由器失效时间等参数。

如果协商一致，则在返回的Hello报文的邻居列表中添加发送该Hello报文的设备的Router ID，双方建立双向通信，邻居关系建立。

邻居关系建立后，如果在路由器失效时间内没有收到邻居发来的Hello报文，则中断邻居关系。

#### **邻接关系**

OSPF邻接关系位于邻居关系之上，两端需要进一步交换DD报文、交互LSA信息时才建立邻接关系。

并非所有邻居都会建立邻接关系，是否建立邻接关系主要取决网络类型和DR/BDR。

在P2P链路和P2MP链路上，每一台设备都需要交换LSA信息，因此只存在邻接关系。

在广播链路和NBMA链路上，因为DR Other之间不需要交换LSA信息，所以建立的是邻居关系。

而DR与BDR之间，DR、BDR与DR Other之间需要交互LSA信息，所以建立的是邻接关系。

如图1所示，两台DR Other各有三个邻居，但是分别只有两个邻接。

#### **邻接关系建立过程**

不同类型的网络，OSPF邻接关系建立过程不同。

#### **广播网络**

在广播网络中，DR、BDR和网段内的每一台路由器都形成邻接关系，但DR other之间只形成邻居关系。

邻接关系建立的过程如图所示。

![image-20230220200329498](images\image-20230220200329498.png)

### 建立邻居关系

 RouterA连接到广播类型网络的接口上使能了OSPF协议，并发送了一个Hello报文（使用组播地址224.0.0.5）。此时，RouterA认为自己是DR设备（DR=1.1.1.1），但不确定邻居是哪台设备（Neighbors Seen=0）。

RouterB收到RouterA发送的Hello报文后，发送一个Hello报文回应给RouterA，并且在报文中的Neighbors Seen字段中填入RouterA的Router ID（Neighbors Seen=1.1.1.1），表示已收到RouterA的Hello报文，并且宣告DR设备是RouterB（DR=2.2.2.2），然后RouterB的邻居状态机置为Init

RouterA收到RouterB回应的Hello报文后，将邻居状态机置为2-Way状态，下一步双方开始发送各自的链路状态数据库。

在广播网络中，两个接口状态是DR Other的设备之间将停留在此步骤。

##### 主从关系协商、DD报文交换

RouterA首先发送一个DD报文，宣称自己是Master（即将DD报文中的MS字段置为1），并规定序列号Seq=X。I=1表示这是第一个DD报文，报文中并不包含LSA的摘要，只是为了协商主从关系。M=1说明这不是最后一个报文。

为了提高发送的效率，RouterA和RouterB首先了解对端数据库中哪些LSA是需要更新的。如果某一条LSA在LSDB中已经存在，就不再需要请求更新了。为了达到这个目的，RouterA和RouterB先发送DD报文，DD报文中包含了对LSDB中LSA的摘要描述（每一条摘要可以唯一标识一条LSA）。为了保证报文在传输过程中的可靠性，在DD报文的发送过程中需要确定双方的主从关系，作为Master的一方定义一个序列号Seq，每发送一个新的DD报文将Seq加1，作为Slave的一方，每次发送DD报文时使用接收到的上一个Master的DD报文中的Seq。

RouterB在收到RouterA的DD报文后，将邻居状态机改为ExStart，并且回应一个DD报文（该报文中同样不包含LSA的摘要信息）。由于RouterB的Router ID较大，所以在报文中RouterB认为自己是Master，并且重新规定了序列号Seq=Y。

RouterA收到报文后，同意了RouterB为Master，并将邻居状态机改为Exchange。RouterA使用RouterB的序列号Seq=Y来发送新的DD报文，该报文开始正式传送LSA的摘要。在报文中RouterA将MS字段置为0，说明自己是Slave。

RouterB收到报文后，将邻居状态机改为Exchange，并发送新的DD报文来描述自己的LSA摘要，此时RouterB将报文的序列号改为Seq=Y+1。上述过程持续进行，RouterA通过重复RouterB的序列号来确认已收到RouterB的报文。

RouterB通过将序列号Seq加1来确认已收到RouterA的报文。当RouterB发送最后一个DD报文时，在报文中写上M=0。

##### LSDB同步（LSA请求、LSA传输、LSA应答）

RouterA收到最后一个DD报文后，发现RouterB的数据库中有许多LSA是自己没有的，将邻居状态机改为Loading状态。此时RouterB也收到了RouterA的最后一个DD报文，但RouterA的LSA，RouterB都已经有了，不需要再请求，所以直接将RouterA的邻居状态机改为Full状态。

RouterA发送LSR报文向RouterB请求更新LSA。RouterB用LSU报文来回应RouterA的请求。RouterA收到后，发送LSAck报文确认。

# 六 OSPF高级特性——控制OSPF路由信息

## 控制OSPF的路由信息

### 配置等价路由数量

路由表中存在到达同一目的地址有多条路由，并且这些路由的开销值、路由协议类型和路由优先级是相同的，那么这些路由就是等价路由，当进行数据传输时可以负载分担

不同设备支持的最大等价路由数量不一致（一般有4、8、16等）

配置命令

OSPF视图：

maximum load-balacing [number]    配置最大等价路由数量

nexthop [ip-address] weight [value]   配置指定OSPF路由的负载分担优先级

当网络中存在的等价路由数量超过配置的等价路由数量时，会选取weight小（优先级高）的路由进行负载分担

Weight 缺省是255，表示等价路由间不区分优先级，随机选取有效路由进行负载分担

### 配置将缺省路由引入到OSPF区域

通过配置缺省路由减少路由表的容量，保证网络的高可用性

一般在网络边界配置缺省路由，并将其引入到内网中（此处是引入到OSPF内网中）

引入缺省路由两种情况

区域边界路由器ABR发布Type3 LSA，用来指导区域内路由器进行区域之间报文的转发

自治系统边界路由器ASBR发布Type5 LSA或Type7 LSA，指导区域内路由器进行域外报文的转发

注意：Type 3的缺省路由高于Type 5的缺省路由
不同区域缺省路由发布方式不同

自动产生

Stub/Totally Stub区域  此区域的ABR会自动产生一条Type 3缺省路由，在Stub区域泛洪

Tollay NSSA区域   此区域的ABR自动产生产生一条Type 3缺省路由，在NSSA区域泛洪

通过命令手动产生

NSSA区域       引入缺省路由后，ASBR产生一条Type 7缺省路由，在NSSA区域泛洪

普通区域         引入缺省路由后，ASBR产生一条Type5缺省路由，在普通区域泛洪

普通区域引入缺省路由命令

Ospf视图：

default-route-advertise [always/permit-calculate-other]  将缺省路由通告到OSPF路由区域

always     表示无论本机是否存在激活的缺省路由，都会产生并发布一条描述缺省路由的LSA

permit-calculate-other   本机必须存在激活的缺省路由，才会产生并发布一条描述缺省路由的LSA，并且设备允许计算来自其他路由器的缺省路由

缺省只有本机存在激活的缺省才会发布一条描述缺省路由的LSA，并且设备不允许计算来自其他路由器的缺省路由

### 配置对OSPF接口发送的LSA进行过滤

当两台路由器之间存在多条链路时，可以在某些链路对发送的LSA进行过滤，减少不必要的重传，从而减少邻居LSDB的大小，提高网络收敛速度，节约带宽资源

配置命令

接口视图

Ospf filter-lsa-out [all/summary/ase/nassa]

All        对除了Grace LSA（Type 9）外的所有LSA进行过滤

Summary  对Type3 LSA进行过滤

Ase       对Type5 LSA进行过滤

Nssa      对Type7 LSA进行过滤

注意事项

在接口配置了此命令后，该接口的OSPF邻居会自动重建

### 配置对ABR产生的3类LSA进行过滤

通过对区域内出、入方向的3类LSA进行过滤，避免了向邻居发送无用的LSA，减少LSDB的大小，提高网络收敛速度

配置命令

Ospf区域视图：

Filter [acl/ip-prefix/route-policy] export   配置区域内出方向的3类LSA

Filter [acl/ip-prefix/route-policy] import   配置区域内入方向的3类LSA

### 配置OSPF对路由进行过滤

通过Filter-policy对OSPF接收、发布的路由进行过滤

在ABR上通过Filter-policy import过滤3类LSA，对自己和其它路由器都生效

在ASBR上通过Fulter-policy export过滤5/7类LSA，对自己和其它路由器都生效

Filter-policy过滤原则

### 配置OSPF汇总

配置OSPF汇总，可以优先减少路由表中的条目，减少对系统资源的占用

汇总主要分为对区域间的路由做汇总，对外部路由做汇总

配置命令

OSPF区域视图

Abr-summary 汇总IP地址  汇总掩码 [no-advertise]   配置区域间路由聚合

OSPF进程视图

Asbr-summary 汇总IP地址  汇总掩码 [no-advertise]  配置外部路由聚合

No-advertise  设置不发布聚合路由（缺省会发布聚合路由）

### OSPF Database Overflow

由于OSPF同一区域中的路由器需要保存相同的LSDB，随着网络中路由数量的不断增加，一些路由器由于资源有限，不能承载如此多的路由信息，这种状态就被称为数据库超限（OSPF Database Overflow）

解决办法

1、配置特殊区域   ---不能解决动态路由增长导致的数据库朝鲜问题

2、动态限制数据库的规模

工作原理

为OSPF同一区域内的所有设备配置相同的数据库规模上限，只要路由器上外部路由的数量达到该上限，路由器就进入Overflow状态，并启动Overflow状态定时器（默认5s），定时器超时后自动退出OverFlow状态***\*配置命令\****

OSPF视图

Lsdb-overflow-limit [number] 设置LSDB中LSA的最大条目数

### LSA过滤总结

```
1、2类LSA过滤
接口下过滤
ospf filter-lsa-out all

3类LSA过滤
接口下过滤

ospf filter-lsa-out summary

路由所属的区域中过滤

filter [acl/ip-prefix] import/export

通过汇总的方式过滤

abr-summary 汇总后的路由 not-advertise

在ABR设备的OSPF进程中过滤

filter-policy ip-prefix import/export

4类LSA过滤

接口下过滤

ospf filter-lsa-out all 过滤

5、7类LSA过滤

接口下过滤

ospf filter-lsa-out ase/nssa

ASBR的OSPF进程下过滤

filter-policy ip-prefix import/export

汇总时过滤

asbr-summary 汇总路由 not-advertise

引入时过滤

import-route 协议 route-policy


```

# Forwarding Address

## Forwarding Address

FA（Forwarding Address，转发地址），存在于Type5和Type7的LSA中

可以使得OSPF在某些特殊场景下避免次优路径以及环路的问题。

FA携带的内容

FA地址携带的是到达（5类/7类LSA）所通告的目的地址数据包应该转发到的地址（缺省是ASBR）

如果此地址为0.0.0.0，则表示数据包被转发到始发ASBR上

如果此字段不为0.0.0.0，则表示数据包应该被转发到FA填充的

FA所携带的地址是自动填充的


## 5类LSA（普通区域）场景

类LSA的FA填充条件

ASBR在去往外部路由下一跳的出接口必须发布在OSPF中（保证FA地址有路由）

ASBR在去往外部路由下一跳的出接口为非静默接口

ASBR在去往外部路由下一跳的出接口的网络类型为广播或者NBMA（P2P网络不会存在次优情况）

满足以上条件，ASBR在发布5类LSA时才会自动填充FA地址


![image-20230514093159834](images\image-20230514093159834.png)

![image-20230514093230072](images\image-20230514093230072.png)

### FA地址避免次优路径

![image-20230514093310454](images\image-20230514093310454.png)

### FA解决环路问题

![image-20230514093405021](images\image-20230514093405021.png)

## 7类LSA（NSSA区域）场景

当NSSA区域有多个ABR时，router-id大的做7类转5类

### 7类LSA的FA填充条件

7类LSA如果满足5类LSA的填充条件，也会按照5类LSA一样填充0.0.0.0或者目的网段下一跳地址

如果不满足5类LSA的填充条件，会填充自己的Loopback或物理接口最大地址

### FA地址避免次优路径

![image-20230514093505252](images\image-20230514093505252.png)

![image-20230514093524325](images\image-20230514093524325.png)

### FA解决环路问题

![image-20230514093558542](images\image-20230514093558542.png)

![image-20230514093635467](images\image-20230514093635467.png)
