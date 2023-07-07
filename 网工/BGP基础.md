# 一 基本概念

1.BGP 是路径矢量协议，是自治系统间的路由协议

2.BGP采用TCP  179号端口，工作在应用层的协议，BGP路由器之间基于TCP建立BGP会话

3.运行BGP的路由器称为BGP Spearker，他们之间建立对等体关系后(邻居关系)才可以交换路由，进行路由学习

4.BGP具有大量丰富的路径属性和强大的策略工具

## 自治系统

1.我们通常使用AS号来表示不同的自治系统

2.在同一个自治系统内，一般使用相同内部路由协议——IGB协议（OSPF、IS-IS等）

3.自治系统间使用外部路由协议——通常是BGP协议

4.一台路由器只能运行在同一个AS内

AS号有两种表示方法

​	1.使用2子节来表示AS号       范围为1~65535     其中64512~65535是私有AS号（类似私有IP地址）   

​	2.但是使用2字节的AS号会觉得未来不够用，所以又推出了4字节的AS号

​	3.使用4子节来表示AS号       范围为1~4294967295  （目前是这种给方式）

## BGP对等体概述

> BGP Speakers          运行BGP的路由器
>
> BGP Peers/Neighbors     BGP对等体/邻居 

1.要想建立对等体关系，前提是TCP对等体之间的TCP连接建立成功

2.BGP的对等体之间无需直连，只需要IP可达就可以——一般使用IGP来使得IP可达，最后在使用BGP协议建立对等体

3.BGP基于TCP协议，所以对等体建立关系需要手动配置

4.BGP是一种单播通信，DIP需要事先知道——例如：Peer  邻居IP地址

5.BGP的对等体关系建立后，不会周期性的更新，只发增量更新或者触发更新

> IBGP    AS内建立邻居    ——一般通过环回口来建立IBGP对等体关系

## 建立对等体关系的条件

1.邻居地址可达

2.自己配置的AS号                 =     邻居声明的AS号

3.数据包的源IP（更新源）    =     邻居配置的邻居IP

4.Open报文携带的地址族一致

5.BGP版本号一致

6.更新源的问题------使用环回接口建立BGP邻居时有此问题，此时需要手动将更新源改为环回接口

                                peer 邻居IP地址  connect-interface LoopBack 0

7.eBGP跳数问题-----eBGP建立eBGP邻居时的默认TTL为1，建立iBGP默认TTL为255。所以如果使用环回口建立eBGP邻居关系时需要增加TTL

                                peer 邻居IP地址  ebgp-max-hop 跳数

8.BGP认证要一致

9.TCP 的179号端口要放通

## 对等体信息参数讲解

![image-20230521170353479](images\image-20230521170353479.png)

![image-20230521170426405](images\image-20230521170426405.png)

# 二 6种邻居状态讲解

## TCP建立阶段

### Idle

> **BGP连接的第一个状态，也是初始化状态，复位TCP连接的重连计时器（通常是60s），准备发起TCP连接**
>
> 发起连接的目的地址为邻居地址，源为更新源地址（默认为去往邻居路由的下一跳）
>
> **一直停留在此状态的原因：**
>
> 无法发起 TCP连接。
>
> 通常是没有去往邻居地址的路由

### Connect

当收不到邻居发来的TCP应答报文时，会停留在此状态。

在Connect状态，BGP发送第一个TCP连接，如果TCP连接的重连计时器（Connect-Retry）超时，就重新发起TCP连接，并继续保持在Connect状态。

如果TCP连接成功，就转为Opensent状态，如果TCP连接失败，就转为Active状态

一直停留在此状态的原因：

通常是由于邻居缺乏到本端的路由，或者邻居回复的应答报文在中途被丢弃

当无法收到邻居的TCP回应报文时：

​    会卡在Connect状态
​    并且5s后重传一次TCP连接请求
​    再等待32s后，重新发起TCP连接请求

### Active

当自身可以发送TCP连接，也可以收到邻居的应答报文，但是依然无法建立起TCP的三次握手，会进入此状态。

在此状态，BGP总是试图建立TCP连接。

如果TCP连接的重连计时器，就退回到Connect状态

如果TCP连接建立成功，就转入到Opensent状态

如果TCP连接失败，重新发起TCP连接，并待在此状态

一直停留在此状态的原因：

本端主动发起TCP连接的源地址和对端指定的邻居地址不匹配

本端与邻居配置的AS号可能有误

### OpentSent

**TCP连接建立成功后进入此状态，发送Open报文**

Opensent状态，发送第一个Open报文，并等待接收邻居的Open报文

### OpenCofirm

**代表收到邻居的Open报文，并发送了Keepalive报文，等待接收邻居的Keepalive报文**

# BGP——6种邻居状态讲解

![img](https://csdnimg.cn/release/blogv2/dist/pc/img/original.png)

​                    [静下心来敲木鱼](https://blog.csdn.net/m0_49864110)                    ![img](https://csdnimg.cn/release/blogv2/dist/pc/img/newUpTime2.png)                    已于 2022-08-01 18:46:40 修改                    ![img](https://csdnimg.cn/release/blogv2/dist/pc/img/articleReadEyes2.png)                    1873                                            ![img](https://csdnimg.cn/release/blogv2/dist/pc/img/tobarCollect2.png)                                                收藏                                                    11                                                                

​                            分类专栏：                                [路由交换协议理论讲解](https://blog.csdn.net/m0_49864110/category_11694606.html)                            文章标签：                                [网络](https://so.csdn.net/so/search/s.do?q=网络&t=all&o=vip&s=&l=&f=&viparticle=)                                [tcp/ip](https://so.csdn.net/so/search/s.do?q=tcp%2Fip&t=all&o=vip&s=&l=&f=&viparticle=)                                [网络协议](https://so.csdn.net/so/search/s.do?q=网络协议&t=all&o=vip&s=&l=&f=&viparticle=)                                [BGP](https://so.csdn.net/so/search/s.do?q=BGP&t=all&o=vip&s=&l=&f=&viparticle=)                    

​                    版权                

​                        [                             ![img](https://img-blog.csdnimg.cn/9990405b77e74cee88af57dd8931afaf.jpeg?x-oss-process=image/resize,m_fixed,h_224,w_224)                                                                                               路由交换协议理论讲解                                     专栏收录该内容                                                                                       ](https://blog.csdn.net/m0_49864110/category_11694606.html)                    

​                        62 篇文章                        44 订阅                    

​                            订阅专栏                    

**目录**

[TCP建立阶段](https://blog.csdn.net/m0_49864110/article/details/126107254?csdn_share_tail={"type"%3A"blog"%2C"rType"%3A"article"%2C"rId"%3A"126107254"%2C"source"%3A"m0_49864110"}&ctrtid=uJYPb#t0)

[Idle](https://blog.csdn.net/m0_49864110/article/details/126107254?csdn_share_tail={"type"%3A"blog"%2C"rType"%3A"article"%2C"rId"%3A"126107254"%2C"source"%3A"m0_49864110"}&ctrtid=uJYPb#t1)

[Connect](https://blog.csdn.net/m0_49864110/article/details/126107254?csdn_share_tail={"type"%3A"blog"%2C"rType"%3A"article"%2C"rId"%3A"126107254"%2C"source"%3A"m0_49864110"}&ctrtid=uJYPb#t2)

[Active](https://blog.csdn.net/m0_49864110/article/details/126107254?csdn_share_tail={"type"%3A"blog"%2C"rType"%3A"article"%2C"rId"%3A"126107254"%2C"source"%3A"m0_49864110"}&ctrtid=uJYPb#t3)

[BGP参数协商邻居建立阶段](https://blog.csdn.net/m0_49864110/article/details/126107254?csdn_share_tail={"type"%3A"blog"%2C"rType"%3A"article"%2C"rId"%3A"126107254"%2C"source"%3A"m0_49864110"}&ctrtid=uJYPb#t4)

[OpentSent](https://blog.csdn.net/m0_49864110/article/details/126107254?csdn_share_tail={"type"%3A"blog"%2C"rType"%3A"article"%2C"rId"%3A"126107254"%2C"source"%3A"m0_49864110"}&ctrtid=uJYPb#t5)

[OpenCofirm](https://blog.csdn.net/m0_49864110/article/details/126107254?csdn_share_tail={"type"%3A"blog"%2C"rType"%3A"article"%2C"rId"%3A"126107254"%2C"source"%3A"m0_49864110"}&ctrtid=uJYPb#t6)

[Established](https://blog.csdn.net/m0_49864110/article/details/126107254?csdn_share_tail={"type"%3A"blog"%2C"rType"%3A"article"%2C"rId"%3A"126107254"%2C"source"%3A"m0_49864110"}&ctrtid=uJYPb#t7)

[BGP邻居状态机](https://blog.csdn.net/m0_49864110/article/details/126107254?csdn_share_tail={"type"%3A"blog"%2C"rType"%3A"article"%2C"rId"%3A"126107254"%2C"source"%3A"m0_49864110"}&ctrtid=uJYPb#t8)

------



# TCP建立阶段

## Idle

> **BGP连接的第一个状态，也是初始化状态，复位TCP连接的重连计时器（通常是60s），准备发起TCP连接**
>
> 发起连接的目的地址为邻居地址，源为更新源地址（默认为去往邻居路由的下一跳）
>
> **一直停留在此状态的原因：**
>
> 无法发起 TCP连接。
>
> 通常是没有去往邻居地址的路由

## Connect

> **当收不到邻居发来的TCP应答报文时，会停留在此状态。**
>
> 在Connect状态，[BGP](https://so.csdn.net/so/search?q=BGP&spm=1001.2101.3001.7020)发送第一个TCP连接，如果TCP连接的重连计时器（Connect-Retry）超时，就重新发起TCP连接，并继续保持在Connect状态。
>
> 如果TCP连接成功，就转为Opensent状态，如果TCP连接失败，就转为Active状态
>
> **一直停留在此状态的原因：**
>
> 通常是由于邻居缺乏到本端的路由，或者邻居回复的应答报文在中途被丢弃
>
> **当无法收到邻居的TCP回应报文时：**
>
> 1. 会卡在Connect状态
> 2. 并且5s后重传一次TCP连接请求
> 3. 再等待32s后，重新发起TCP连接请求

## Active

> **当自身可以发送TCP连接，也可以收到邻居的应答报文，但是依然无法建立起TCP的三次握手，会进入此状态。**
>
> 在此状态，BGP总是试图建立TCP连接。
>
> 如果TCP连接的重连计时器，就退回到Connect状态
>
> 如果TCP连接建立成功，就转入到Opensent状态
>
> 如果TCP连接失败，重新发起TCP连接，并待在此状态
>
> **一直停留在此状态的原因：**
>
> 本端主动发起TCP连接的源地址和对端指定的邻居地址不匹配
>
> 本端与邻居配置的AS号可能有误

## OpentSent

**TCP连接建立成功后进入此状态，发送Open报文**

Opensent状态，发送第一个Open报文，并等待接收邻居的Open报文

## OpenCofirm

**代表收到邻居的Open报文，并发送了Keepalive报文，等待接收邻居的Keepalive报文**

## Established

**收到了邻居发来的Keepalive报文**

之后可以通过Update报文通告路由信息 路径属性

通过Keeplive报文进行邻居保活（60s发一次，180s保活）

![image-20230521170837655](images\image-20230521170837655.png)

# 三 图解5种报文

## BGP的报文头部

1.Marter：检查BGP对等体的同步信息是否完整，不使用此验证时所有比特均为1

　　　　　　----此处就是不使用此验证

2.Length：BGP消息的总长度，包括报文头部在内

　　　　　　----长度为19~4096

3.Type：BGP的消息类型

　　　　　　----此处指的就是Open报文

| 1    | OPEN                                                         |
| ---- | ------------------------------------------------------------ |
| 2    | UPDATE                                                       |
| 3    | [NOTIFICATION](https://so.csdn.net/so/search?q=NOTIFICATION&spm=1001.2101.3001.7020) |
| 4    | KEEPALIVE                                                    |
| 5    | REFRESH（RFC2918）                                           |

## BGP的5种报文

### Open 只有邻居建立时会发送此报文

![image-20230521171042578](images\image-20230521171042578.png)

**以下三个可选字段默认会携带** 

![image-20230521171126162](images\image-20230521171126162.png)

### Keepalive 邻居建立时、建立后都会发送此报文

- 维持邻居关系，确认对方发送的OPEN包（对它认可）
- 发送间隔在Open报文中确认，如果两端的Hold time间隔不一致，取最小的
- 当Hold time时间为0时，不发送Keepalive报文
- 根据Hold time的缺省时间，Keepalice的缺省间隔是60s，保活时间是180s

![image-20230521171258795](images\image-20230521171258795.png)

### Update 邻居建立成功后才会发送此报文

- 连接建立后，在对等体之间交换路由信息 以及路径属性
- 可以发送可达路由信息，也可以撤销不可达的路由信息
- 主要包含NLRI、路径属性、撤销路由信息

![image-20230521171338172](images\image-20230521171338172.png)

### Notification 邻居建立成功后才会发送此报文

- 当BGP检测到错误状态之后就向对等体发出Notification信息，BGP连接立即中断
- 收到该报文只有一个结果，那就是断开TCP连接

![image-20230521171444521](images\image-20230521171444521.png)

![image-20230521171503950](images\image-20230521171503950.png)

### Route-refresh 邻居建立成功后才会发送此报文

- 此消息用来要求对等体重新发送指定地址族的路由信息（即 要求对等体重新发布Update报文，进行路由更新）
- 当路由策略发生变化时，触发请求邻居重新通告路由（报文具体的含义不是很清楚）
- 可以用于手动进行BGP路由的触发更新，也可以用于ORF（出站路由过滤）功能

![image-20230521171548521](images\image-20230521171548521.png)

# 四 BGP路由属性

## BGP路由属性主要分为4大类

> BGP的路由属性是人为设计的，是对BGP路由的进一步描述
>
> **作用：**实现BGP路由的控制、选路、防环、管理

## 公认必遵属性

- **所有BGP路由器都必须识别**  
- **Update消息中必须包含的属性**

### Origin   路由起源属性

起源属性用来定义路由的来源，通过修改此属性可以控制BGP路径的选择。

目前BGP的路由来源主要有三种类型：

    i   （internal）代表通过Network宣告学到的路由
    ? （incomplete）代表通过Import-route引入学习到的路由
    e   （EGP）代表通过EGP协议引入的路由    --EGP已淘汰

注意：

3种起源属性的优先级为：i＞e＞？（network＞EGP协议引入＞import-route引入）

### AS_Path  AS路径属性

AS路径属性，主要用来进行路由防环、路由选路。

具体原理如下：

    从EBGP邻居得到路由时，会检查该路由的AS_Path属性，如果此属性存在自身的AS号，则丢弃此路由——用于AS之间防环。
    可以通过命令 peer 邻居地址 allow-as-loop来使得EBGP邻居可以忽略AS_Path属性的检查。
    经过AS数量越少的路径越优——用于BGP路由选路。

注意：

    EBGP在传递路由时会更新AS_Path，会将自己的AS号添加到AS_Path属性的最前面
    IBGP在传递路由时，不会更新AS——Path
    EBGP邻居之间进行AS_Path检测，IBGP邻居之间不进行AS_Path检测

例如：

        AR1和AR2建立EBGP邻居关系，AR2和AR4建立EBGP邻居关系
    
        此时AR4将自己的环回接口地址宣告到BGP中
![image-20230521171835768](images\image-20230521171835768.png)

在AR2收到的4.4.4.4的AS_Path 为200

![image-20230521171906212](images\image-20230521171906212.png)

### Next_nop  下一跳

默认情况下，凡是自身起源的BGP路由，在传递给任何BGP邻居时，都会更改路由的下一跳为自己发往邻居的更新源地址。
默认情况下，在向EBGP邻居传送BGP路由时，其下一跳会更改，会更改为自己发送给此邻居的更新源地址
默认情况下，从EBGP邻居得到的BGP路由再传送给IBGP邻居时，此BGP路由的下一跳不会更改（可以使用peer 邻居地址 next-hop-local 命令来实现更改下一跳）**注意：**

​	此字段为0.0.0.0 代表是自身起源的BGP路由

​	在IBGP、EBGP邻居之间，也可以通过import、export使用策略对BGP的下一跳做更改，但是要注意设置的下一跳一定要可达。

## 公认任意属性

- **所有BGP路由器都必须识别**  
- **不要求必须存在于Update报文中，可根据需求自由选择**

### Local_Pref  本地优先级

- 仅传递给IBGP邻居，不会传递给EBGP邻居，即只在AS内传递，不会传递给其它AS
- 默认优先级为100，越大越优先
- 用于判断流量离开AS时的最佳路由（控制整个AS内设备的流量如何流出AS）

### Atomic_aggregate  

聚合路由丢失明细路由属性

当手动聚合并抑制明细路由时会有此属性，或者自动聚合后会直接产生此属性 

## 可选过度属性

- **不会被所有BGP路由器识别**    
- **所有BGP路由器都可以接收此属性，并传给邻居**

### Aggregator

聚合路由不丢失明细路由属性

### Community  团体属性主要有两个作用

团体属性，表示具有相同特征的路由信息，与所在AS无关

不同于Tag，Tag只能打一个标签，团体属性可以打多个标签

    限定路由的传播范围——公认团体属性
    对路由打标记，便于对相同条件的路由进行统一处理——扩展的团体属性

团体属性分类：

公认团体属性分为4类

Internet      缺省属性。此属性的路由可以向任何BGP邻居宣告（不管邻居是IBGP还EBGP）

No-export         收到此属性路由不向EBGP邻居宣告，但是可以向联盟内的EBGP邻居宣告

No-exportsubconfed   收到此属性路由不向任何EBGP邻居宣告，包括联盟内的EBGP邻居也不宣告（在联盟中使用，仅在成员AS内传递）

No-advertise     收到此属性路由不向任何邻居宣告

扩展团体属性

    用一组4字节为单位的列表来表示，格式为aa:nn或着团体号
    aa通常为AS编号，nn是管理员定义的团体属性标识
    团体号范围为0~4294967295，在RFC1997中，0~65535、4294901760~4294967295为预留值。

注意

可以在宣告路由时应用团体属性（这样本地的路由也会具备此团体属性）

也可以在Peer邻居时应用此团体属性（这样本地的路由无此团体属性，邻居才有此团体属性）


## 可选非过度属性

- **不会所有BGP路由器识别**    
- **BGP路由器可以不接受（忽略）此属性，并不向邻居发送**

MED

特点

    仅在相邻两个AS之间传递，并且收到此属性的AS不会再将其通告给任何第三方AS
    根据不同实际情况有不同的默认优先级，优先级越小越优
    一般用于判断流量进入AS时的最佳路径（其实可以和本地优先级达到相同的目的，只是应用的方向和位置有区别）

MED通告规则

    默认从EBGP邻居学到的路由再通告给EBGP邻居或者IBGP邻居时，MED会被清除，即不发送此属性（除非手动指定可以传给的IBGP邻居以及成员EBGP邻居）
    默认从IBGP邻居学习到的路由再通告给EBGP邻居时，MED会被清除。（除非手动指定可以传给的EBGP邻居）
    默认本地引入的直连、静态、IGP路由如果有MED值，那么可以直接传递给EBGP邻居、IBGP邻居、成员EBGP邻居。
    默认从联盟EBGP邻居或联盟内始发的路由，其MED值在整个联盟内保持传递

注意

缺省情况下，不会比较来自不同AS邻居的路由信息中的MED值，除非能够确认不同的AS采用了IGP和路由选择方式，或者手动开启MED的比较

# 五 路由引入、防环、路由通告原则、路由选路

BGP不对路由进行计算，只是路由的搬运工，通过对已有路由进行宣告来得到BGP路由

## BGP路由宣告方式

本地宣告：network

    此命令不再具备将接口加入到BGP进程的逻辑（即不同于OSPF的network）
    此命令就是将路由表中的路由引入到BGP路由表中
    此命令可以精确控制引入哪些路由到BGP中

引入宣告：import-route

    将路由表的路由引入到BGP中，高效快捷
    将其它协议引入到BGP，默认开销为IGP的度量值，路由优先级为255（可以通过default med修改初始度量值）

引入缺省路由：Default-route、Default-rote-advertise

    default-route imported  将本地IP路由表中已存在的缺省路由引入到BGP路由表中（default-route imported命令需要必须要与import-route命令配合使用，才能引入缺省路由）
    peer 对等体 default-route-advertise  可以针对对等体引入缺省路由（并且可以通过字段来实现满足特定条件时引入缺省路由）
    peer 对等体 default-route-advertise  conditional-route-match-all  条件当匹配所有条件时，下发缺省路由
    peer 对等体 default-route-advertise  conditional-route-match-any  条件当匹配任一条件路由时，发送缺省路由

## BGP的下一跳

在EBGP间传递时会修改下一跳为自己的更新源

在IBGP间传递时不会修改下一跳为自己的更新源（可以修改使其传递时修改）

## BGP防环机制

AS内：通过水平分割  通过IBGP邻居得到的路由不会再传递给IBGP邻居

AS间：AS_Path属性

补充：BGP SoO属性

## BGP路由信息处理流程

1.邻居表                                        BGP邻居名单

2.Local-RIB（BGP路由表）        从邻居获取到以及自己宣告的所有路由及其属性

3.IP-RIB（IP路由表）                  从BGP路由表中选取最佳路由加入IP路由表项（如果IP路由表有优于此BGP路由的其它路由，则BGP的路由无法加入到IP路由中）

4.Adj-RIB-In（入）                      邻居宣告给本地的未处理的路由信息库

5.Adj-RIB-Out（出）                  本地宣告给指定邻居的路由信息库

## BGP路由通告原则

1.到达同一目的 有多条路由时，只会选取最优的（Best）路由来给自己使用

​	----就比如到达同一网段的路由有多个下一跳，此时只会选择最优的下一跳给自己使用

2.BGP只把自己使用的路由，也就是自己认为最优的路由传给BGP对等体

3.BGP从EBGP对等体获得的路由会向他所有BGP对等体宣告（IBGP和EBGP对等体）

4.BGP路由器从IBGP对等体获知的路由不向它的IBGP对等体通告（水平分割规则，出现路由反射器的情况除外）

5.BGP路由器从IBGP对等体获知的路由是否通告给它的EBGP对等体要视IGP和BGP同步的情况来决定。

​	---即自己的IGP是否有此需要通告的路由，如果IGP有，则通告，如果IGP没有，则不通告。

​	---如果此规则不打开，就会造成路由黑洞问题（默认此同步规则关闭的）

​	---BGP协议下：synchronization开启同步规则（华为设备不支持此规则，思科支持）
6.BGP进行路由更新时，BGP设备只发送更新的BGP路由**

注意：

BGP路由传递给EBGP邻居时，下一跳会自动修改

从EBGP邻居学到的路由传递给IBGP邻居时默认不更改路由的下一跳，会导致IBGP邻居收到的路由不是有效路由（下一跳不可达）

​	---使用Peer 邻居IP地址 next-hop-local 命令来解决，该命令只对IBGP邻居生效

​	---在从EBGP邻居得到的路由在传递给IBGP邻居时，将下一跳更改为自身向该IBGP邻居发送BGP报文的源地址

## BGP路由状态码

*-----表示路由为有效路由

　　不可用的原因：

    　　下一跳不可达
    　　已经通过更优的方式学习到了该路由

＞----表示此路由为最优路由

d-----表示此路由为惩罚路由——当路由一会Down，一会Up就会被惩罚

s-----抑制路由，即路由不生效——聚合路由时，可以选择抑制明细路由

## BGP选路原则

1.如果该路由是到目的地址的唯一路由，直接优选

2.到达同一目的地有多条路由，优选有效路由

3.到达同一目的地有多条有效路由，有更细的原则比较

1)    丢弃下一条不可达路由
2)    优选私有属性（Prefernce）最高的路由——私有路由属性仅本地有效
3)    优选本地优先级（Local_Preference）最高的路由
4)    当有聚合路由时，手动聚合＞自动聚合＞network＞import＞从对等体学到的路由
5)    优选AS_Path最短的路由
6)    Orign：i＞e＞？（network＞EGP协议引入＞import-route引入）
7)    对相同同一AS的路由，优选MED最小的
8)    优选从EBGP学来的路由（EBGP＞IBGP）
9)    优选AS内部IGP的Metric最小的路由——Metric  从此路由器到下一跳的度量值
10)    Cluster_List最短
11)    起源ID最小
12)    Router_ID最小
13)    IP地址最小的

## BGP负载均衡

默认BGP不进行负载分担，如果①到⑨都一致，并且AS_Path必须一致，则为等价路由，可以负载均担

　　Maximum  load-balancing  1          允许一条最优路由（缺省）

　　Load-balancing   as-path-ignore    忽略AS_PATH，不一致也可以

当BGP开启负载均衡后

　　在BGP的路由表中还是只有一条最优路由，但是在IP路由表中会形成负载分担


## Preference_Value属性

> - Preference_Value是BGP的私有属性（华为私有）
> - 仅在本地生效，即仅可用于自己选路
> - 越大越优先

# 五 路由聚合

## BGP路由聚合

### 静态聚合

**如何实现**

通过配置静态路由进行路由聚合（配置汇总后的黑洞路由），然后再宣告这个汇总后的路由

  1、Ip route-static 汇总路由 Null 0        

  2、Network 汇总路由

![image-20230521173052388](images\image-20230521173052388.png)

特点

    并不是真正意义上BGP路由汇总，只是通过BGP发布路由的特点来实现了路由汇总的效果
    此方式进行汇总，明细路由不会被抑制，也会一同传往邻居（需要通过策略将明细过滤）
    由于宣告的汇总路由是静态配置，此汇总和明细路由其实是没有关系的，因此：
        此方式使得汇总路由无法携带明细路由的属性
        当明细路由失效时，汇总路由还是存在，倒是汇总路由不能真实的反应网络的现状
### 自动聚合

如何实现

    直接在BGP协议的地址族视图下 使用 Summary automatic命令，自动将明细路由汇总
    特点
    	只对引入（import）的IGP路由进行聚合，对本地宣告（network）的路由不做聚合
    	明细路由会被抑制，不会优选和发送给邻居
    	只可以对明细路由做主类聚合——因此现网一般不使用此聚合方式
### 手动聚合

**如何实现**

在BGP协议的地址族视图下 使用 aggregate 聚合路由 {detail-suppressed | as-set | attribute-policy | suppress-policy | origin-policy } 进行路由汇总

**as-set**

在聚合的路由中携带明细路由的As_Path属性信息，可以用于防环。

![image-20230521184156217](D:\study\studyDoc\网工\images\image-20230521184156217.png)

当多个明细路由有不同的As_Path属性时，汇总的as-set遵循以下规则

相同就取一个相同的值，不同的值则全部取

例如：

明细路由1的as_path：1 2 3

明细路由2的as_path：1 4 5

汇总后的as_path： {1 2 3 4 5 }

as-set值与as-path的区别

as-path  有序的，表明路由传递的AS的顺序

as-set    {}中的值，代表无序的as_path，也就是as-set

              只是用于汇总后的路由防环，并且{}内的AS号无论有多少个，只能算作1个AS长度

注意事项

当策略中配置了As_Path属性，并且aggregate设置了as-set属性，那么策略中的As_Path属性不会生效

detail-suppressed

仅通告聚合路由，抑制明细路由，只向邻居发送聚合后的路由

并且聚合路由不会继承明细路由的团体属性

suppress-policy

指定抑制路由通告的策略名称，对满足ACL或者perfix-list的明细路由做抑制，不满足的明细路由不做抑制

suppress-policy优先于detail-suppressed

origin-policy

指定允许生成聚合路由的策略名称，对满足ACL或者perfix-list的明细路由生成聚合路由

attribute-policy

指定设置聚合路由的属性策略名称。通过peer route-policy也可以完成此工作

> **特点**
>
> - 只要在BGP表中存在的路由都能够被手动汇总
> - 可以实现精确汇总，并且支持CIDR（无类域间路由）
> - 可以对汇总路由的属性做编辑
> - 可以继承明细路由的As_Path属性，防止环路
> - 当明细路由全部失效时，汇总路由才会失效
> - 默认情况下不抑制明细路由，不携带明细路由的As_Path属性

# 六 BGP高级特性——快速收敛、路由震荡、AS_Path、Community Filte

## 路由快速收敛

### TCP连接重传定时器

BGP通过TCP建立三次握手时会使用到TCP连接重传定时器；缺省的TCP重传定时器为32s

如果TCP连接建立失败，则会在TCP连接重传定时器超时后重新尝试建立连接

如果TCP连接建立成功，则会关闭TCP连接重传定时器

TCP连接重传定时器的大小对BGP连接建立的影响

定时器较小，可以减小下次连接的建立时间，加快连接失败后的重建速度

定时器较大，可以减少由于邻居反复震荡引起的路由震荡

配置TCP连接定时器

BGP视图下

bgp 100

timer connect-retry 10 配置全局TCP连接重传定时器为10s（对所有对等体生效）

针对对等体或对等体组单独配置

peer 1.1.1.1 timer connect-retrt 10


### Keepalive定时器

Keepalive定时器主要包含两种

Keepalive发送间隔（缺省60s）

Keepalive老化时间（缺省3倍的发送间隔，180s）

BGP的keepalive消息可以用来维持BGP连接关系

通过调整keepalive定时器，可以改变BGP的存活时间（Keepalive发送间隔）和BGP邻居的保持时间（Keepalive老化时间）

BGP邻居建立成功后每存活一段时间就需要发送Keepalive消息来维持BGP邻居关系

BGP邻居如果在Keepalive老化时间结束后未收到Keepalive报文，则邻居失效；在老化时间结束前会一直保持邻居关系

Keepalive定时器的大小对BGP的影响

如果减少keepalive发送间隔和老化时间，bgp能够快速的检测到链路故障，加快收敛；但是过短的发送间隔和老化时间会导致网络中的keepalive消息增多，增加设备负担

如果增打keepalive发送间隔和老化时间，bgp能够减轻设备负担；但是过长的发送间隔和老化时间使得BGP无法及时检测到链路状态的变化

如果对等体两端的Keepalive定时器不同，如何选举

老化时间取双方最小值

发送间隔为 协商的老化时间/3 与 本地配置的发送间隔最比较，取最小的为发送间隔

配置Keepalive定时器

BGP视图下

bgp 100

timer keepalive 30 hold 90  配置全局keepalive发送间隔为30s，老化时间为90s（对所有对等体生效）

针对对等体或对等体组单独配置

peer 1.1.1.1 timer keepalive 30 hold 90


### Update定时器

当BGP路由发生变化时，会发送Update消息更新路由表

当BGP路由没有发生变化时，会每隔一段时间定期发送Update消息（IBGP对等体为15秒，EBGP对等体为30s）

Update定时器的大小对BGP的影响

减小Update更新报文时间，bgp能够更快速的检测到路由变化，加快bgp网络收敛。

增大Update更新报文时间，可以减轻设备负担和减少网络带宽的占用，避免不必要的路由振荡

配置Update定时器

针对对等体或对等体组单独配置

peer 1.1.1.1 timer route-update-interval 10  配置Update更新报文间隔为10s


### EBGP连接快速复位

当bgp接口故障时，如果收不到对等体发来的keepalive报文，则需要等待keepalive老化时间结束后才会进行网络收敛

此时可以通过配置EBGP连接快速复位，使得BGP协议不再等待Keepalive老化时间，立即响应接口故障，删除接口上的EBGP直连会话，加快网络收敛

如果EBGP连接所使用的接口震荡，则可以关闭EBGP连接快速复位，避免BGP网络震荡

配置EBGP连接快速复位

bgp

ebgp-interface-sensitive  使能EBGP连接快速复位（缺省使能）

### BGP下一跳延迟响应

下一跳响应只适用于设备去往同一目的地址有多条路径的场景

当设备检测到去往目的地的的下一跳A不可达时，可以通过配置BGP下一跳延迟响应来延迟撤销路由

即发现下一跳不可达后，先不撤销下一跳为A的路由，先等待延迟，让网络先收敛，学习到通过下一跳为B的路由后，再撤销下一跳为A的路由

可以减少流量损失

配置BGP下一跳延迟响应

bgp

nexthop recursive-lookup delay 10 配置BGP下一跳延迟响应时间为10s


### BGP路由震荡抑制

当路由表中的某条路由反复消失和重现，会造成路由震荡，消耗设备资源

通过配置BGP路由震荡抑制来方式路由震荡带来的不利影响

配置BGP路由震荡抑制

dampening [ ibgp ] half-life-reach reuse suppress ceiling 

ibgp： 只对BGP的Vpnv4路由生效（默认只对EBGP生效）

half-life-reach：可达路由的半衰期

每经过一个half-life-reach时间，路由的惩罚值会被减半（单位为分钟）

reuse：路由解除抑制状态的阈值

当路由的惩罚值减少到reuse或小于reuse时，路由被重新使用

suppress：路由进入抑制状态的阈值

路由每震荡一次，惩罚值会加一定的值（华为是加1000），当惩罚值超过阈值时会进入抑制状态（不会通告给对等体，不加入到路由表，不会进行数据转发）

如果此路由进入抑制前的报文是Update报文，打上d标签（当惩罚值降到解除抑制的阈值时，路由重新使用）

如果此路有进入抑制前的报文时撤销报文，打上h标签（当惩罚值降到0时删除此路由）

ceiling：路由惩罚上限值

  当一个路由的惩罚值超过此上限值，则路由被丢弃

BGP地址族下配置

dampening ibgp 10 200 300 5000

路由半衰期为10min

路由解除抑制阈值200

路由进入抑制阈值300

路由最大阈值5000


## **BGP路由控制**

BGP路由控制一般通过路由策略来实现，通过路由匹配工具匹配特定路由，再通过路由策略工具对路由的发布和接收进行控制

对于BGP而言，路由匹配工具有ACL、IP Prefix List、AS_Path Filter、Community Filter

路由策略工具有：Filter-Policy 和 Route-Policy

### 正则表达式

正则表达式就是按照一定的模板来匹配字符串的公式，由普通字符和特殊字符组成

在BGP中应用正则表达式一般用来匹配AS号或者团体属性的团体号

![image-20230521184629087](images\image-20230521184629087.png)

### Community Filter

Community Filter团队属性过滤器，用来与Community属性配合使用控制路由

Communoty是可选过渡属性，不是报文必须携带的属性，需要自己来定义Community属性

匹配Community的两种方式

基本Community Filter：匹配团体号或公认Community

高级Community Filter：使用正则表达式匹配团体号

Community Filter配置命令

先针对路由设置团体属性

在路由策略中设置路由的Community属性值

Apply  community  [团体号 | aa:nn | 公认属性]

在BGP视图下，设置将团体属性发布给对等体（缺省不发布给对等体）

Peer  [ip-address] advertise-community

配置Community Filter

创建基本的Community Filter

Ip Community-filter basic  [name | number]  [permit | deny]  [团体号 | aa:nn | 公认属性]

       Name|number：过滤器的名字或编号（1~99）

创建高级的Community Filter

Ip community-filter advanced [name | number] [permit | deny] [正则表达式]

       name|number：过滤器的名字或编号（100~199）

在路由策略中应用Community Filter

If-match community-filter [basic-num | name] [whole-match] 

If-match community-filter [adv-num]

       Whole-match：表示完全匹配，即所有的团体都必须出现（只对基本团体过滤器生效）
    
       Basic-num：基本团体属性过滤器号
    
       Name：团体过滤属性名称（基本和高级）
    
       Adv-num：高级团体属性过滤器号

在向对等体发送路由时引用此路由策略

Peer [ip-address] route-policy [name] [export | import]

       Import：对从此对等体接收的路由进行过滤
    
       Export：对向此对等体发送的路由进行过滤
### AS_Path Filter

AS_Path Filter  AS路径过滤器，与AS_Path属性配合使用控制路由

AS_Path属性时BGP公认必遵属性，所有的BGP路由都必须携带，不需要我们再去定义，只需要通过匹配工具匹配就可以

配置命令

系统视图下创建AS_Path Filter

ip as-path-filter  [number | name]  [deny | permit]  [正则表达式]

       number：指定AS路径过滤属性的AS号（1~256）
    
       name：指定AS路径过滤属性的名称
    
       默认AS路径过滤属性的动作为拒绝

应用AS_Path Filter两种方式

1、直接在指定对等体的时候应用AS_Path属性

Peer [ip-address] as-path-filer [import | export]

2、通过路由策略调用，然后应用在对等体中

在路由策略中应用AS_Path Filter

If-match as-path-filter [number-name]

在BGP视图下应用路由策略

Peer [ip-address] route-policy [name] [export | import]


# 七 BGP路由反射器

我们知道，在IBGP 2 设备收到IBGP 1设备传输过来的IBGP路由后，不会将此IBGP路由传递给其它的IBGP设备，所以当其它的IBGP设备需要获得此跳IBGP路由时，就需要与IBGP 1设备建立IBGP邻居关系。

在网络较大的情况下，使用IBGP全互联的话，就会很复杂，所以出现了路由反射器


## 路由反射器角色

![image-20230521184800967](images\image-20230521184800967.png)

1.RR-----------路由反射器----允许把从IBGP对等体学来的路由反射到其它IBGP对等体设备

2.Client--------客户机--------与RR形成反射邻居关系的IBGP设备（在AS内只需要与RR直连）

3.Non-Client--非客户机------既不是RR也不是客户机的IBGP设备（在AS内部需要与RR之间、以及所有的非客户机之间仍然需要全互联）

4.Originator---始发者--------在AS内部始发路由的设备（Originator_ID属性用于防止集群内产生路由环路）

5.Cluster-------集群----------路由反射器与客户机的集合（Cluster_List属性用于防止集群间产生路由环路）

## 路由反射器原理

> 1.RR从非客户机学到的路由，会反射给所有的客户机
>
> 2.RR从客户机学习到的路由，发布给所有的客户机和非客户机（除了发起此路由的客户机除外）
>
> 3.从EBGP对等体学习到的路由，发布给所有的非客户机和客户机

## 路由反射器的防环机制

### Originator_ID用于防止集群内产生路由环路

 当一条路由第一次被RR反射的时候，RR将Originator_ID属性加入这条路由，标识这条路由的发起设备。如果一条路由中已经存在了Originator_ID属性，则RR将不会创建新的Originator_ID属性
当设备接收到这条路由的时候，将比较收到的Originator ID和本地的Router ID，如果两个ID相同，则不接收此路由。

### Cluster_List用于防止集群间产生路由环路---Cluster-ID就类似于[OSPF](https://so.csdn.net/so/search?q=OSPF&spm=1001.2101.3001.7020)中的Router-id

    当一条路由第一次被RR反射的时候，RR会把本地Cluster ID添加到Cluster List的前面。如果没有Cluster_List属性，RR就创建一个。
    
    当RR接收到一条更新路由时，RR会检查Cluster List。如果Cluster List中已经有本地Cluster ID，丢弃该路由；如果没有本地Cluster ID，将其加入Cluster List，然后反射该更新路由。

注意：

当一个网络中有多个RR（防止单点故障）时，可以通过此网络中的RR配置相同的集群ID（Cluster_ID）来减少各RR接收的路由数量

 ipv4-family unicast

  reflector cluster-id 1.1.1.5     配置Cluster-id为1.1.1.5
配置命令

以下的配置只需要在RR上进行路由反射器的配置（客户机只需要配置与RR做IBGP邻居的配置）

对于客户机来说，客户机是不知道自己时客户机的，只有RR知道

    Bgp as号
       Peer  reflect-client              配置自己为RR，并将指定的对等体最为Client
       Peer  ip地址   reflect-client      配置此对等体为客户机
       reflector cluster-id       配置集群ID
