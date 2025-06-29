## 一 MPLS简介

### MPLS的定义

MPLS位于TCP/IP协议栈中的链路层和网络层之间，用于向IP层提供连接服务，同时又从链路层得到服务。MPLS以标签交换替代IP转发，标签是一个短而定长的、只具有本地意义的连接标识符，与ATM的VPI/VCI以及Frame Relay的DLCI类似。

MPLS不局限于任何特定的链路层协议，能够使用任意二层介质传输网络分组。MPLS起源于IPv4（Internet Protocol version 4），其核心技术可扩展到多种网络协议，包括IPv6（Internet Protocol version 6）、IPX（Internet Packet Exchange）、Appletalk、DECnet、CLNP（Connectionless Network Protocol）等。MPLS中的“Multiprotocol”指的就是支持多种网络协议。

由此可见，MPLS并不是一种业务或者应用，它实际上是一种隧道技术，在一定程度上可以保证信息传输的安全性。

### MPLS的工作原理

MPLS个工作原理主要包含两部分内容：

- MPLS的体系结构是指运行MPLS的单个设备内部的独立工作原理。
- MPLS的网络结构是指运行MPLS的多个设备互连的联合工作原理。

### MPLS的体系结构

MPLS的体系结构由控制平面（Control Plane）和转发平面（Forwarding Plane）组成：

- 控制平面是无连接的，主要功能是负责标签的分配、LFIB（标签转发表，Lable Forwarding Information Base）的建立、 LSP（标签交换路径，Label Switched Path）的建立、拆除等工作。
- 转发平面也称为数据平面（Data Plane），是面向连接的，可以使用ATM、Ethernet等二层网络承载，主要功能是对IP包进行标签的添加和删除，同时依据标签转发表对收到的分组进行转发。

![img](images\mpls-1)

- A：IP路由协议建立邻居，交互路由信息，生成IP路由表。
- B：标签交换协议从IP路由表中获取路由信息。IP路由表中的路由前缀匹配了FEC（转发等价类，Forwarding Equivalence Class），在传统的采用最长匹配算法的IP转发中，到同一条路由的所有报文就是一个FEC。
- C：IP路由表中激活的最优路由生成IP转发表。
- D：标签转换协议建立邻居，为FEC分配标签并发布给邻居，同时获取邻居发布的标签，生成标签转发表。

MPLS转发平面建立以后，设备中已经生成了IP转发表和标签转发表，就可以对于接收到的数据包进行转发

### MPLS的实现原理

MPLS的实现原理是指：为FEC（转发等价类，Forwarding Equivalence Class）分配标签来建立LSP（标签交换路径，Label Switched Path）。

#### MPLS LSP

**IP包在MPLS网络中经过的路径称为MPLS的LSP，即标签交换的路径**

MPLS LSP是一个单向路径，与数据流的方向一致。

- LSP的起始节点称为入节点（Ingress）：LSP的起始节点，一条LSP只能有一个Ingress。

  Ingress的主要功能是给报文压入一个新的标签，封装成MPLS报文进行转发。

- 位于LSP中间的节点称为中间节点（Transit）：LSP的中间节点，一条LSP可能有0个或多个Transit。

  Transit的主要功能是查找标签转发信息表，通过标签交换完成MPLS报文的转发。

- LSP的末节点称为出节点（Egress）：LSP的末节点，一条LSP只能有一个Egress。

  Egress的主要功能是弹出标签，恢复成原来的报文进行相应的转发。

其中Ingress和Egress既是LSR，又是LER；Transit是LSR。

根据数据传送的方向，LSR可以分为上游和下游。

- 上游：以指定的LSR为视角，根据数据传送的方向，所有往本LSR发送MPLS报文的LSR都可以称为上游LSR。
- 下游：以指定的LSR为视角，根据数据传送的方向，本LSR将MPLS报文发送到的所有下一跳LSR都可以称为下游LSR。

#### MPLS标签

标签是一个短而定长的、只具有本地意义的标识符，用于唯一标识一个分组所属的FEC。在某些情况下，例如要进行负载分担，对应一个FEC可能会有多个入标签，但是一台LSR上，一个标签只能代表一个FEC。

标签长度为4个字节

![img](images\mpls-2)

标签共有4个域：

- Label：20bit，标签值域。
- Exp：3bit，用于扩展。现在通常用做CoS（Class of Service），其作用与Ethernet802.1p的作用类似。
- BoS：1bit，栈底标识。MPLS支持多层标签，即标签嵌套。S值为1时表明为最底层标签。
- TTL：8bit，和IP分组中的TTL（Time To Live）意义相同。

标签封装在链路层和网络层之间。这样，标签能够被任意的链路层所支持

标签在分组中的封装位置

![img](images\mpls-3)

标签栈（Label stack）也称为多层标签，是指标签的排序集。靠近二层首部的标签称为栈顶标签或外层标签；靠近IP首部的标签称为栈底标签，或内层标签。理论上，MPLS标签可以无限嵌套。

![img](images\mpls-5)

签栈按后进先出（Last In First Out）方式组织标签，从栈顶开始处理标签。

标签的操作类型包括标签压入（Push）、标签交换（Swap）和标签弹出（Pop），它们是标签转发的基本动作，是标签转发信息表的组成部分。

- Push：指当IP报文进入MPLS域时，MPLS边界设备在报文二层首部和IP首部之间插入一个新标签；或者MPLS中间设备根据需要，在标签栈顶增加一个新的标签（即标签嵌套封装）。
- Swap：当报文在MPLS域内转发时，根据标签转发表，用下一跳分配的标签，替换MPLS报文的栈顶标签。
- Pop：当报文离开MPLS域时，将MPLS报文的标签去掉；或者MPLS倒数第二跳节点处去掉栈顶标签，减少标签栈中的标签数目。

在最后一跳节点，标签已经没有使用价值。这种情况下，可以利用倒数第二跳弹出特性PHP（Penultimate Hop Popping），在倒数第二跳节点处将标签弹出，减少最后一跳的负担。最后一跳节点直接进行IP转发或者下一层标签转发。PHP在Egress节点上配置，通过分配特殊的标签值3来实现。标签值3表示隐式空标签（implicit-null），这个值不会出现在标签栈中。当一个LSR发现自己被分配了隐式空标签时，它并不用这个值替代栈顶原来的标签，而是直接执行Pop操作。Egress节点直接进行IP转发或下一层标签转发。

#### 分配标签来建立LSP

MPLS需要为报文事先分配好标签，建立一条MPLS LSP，才能进行报文转发。标签由下游分配，按从下游到上游的方向分发。

LSP分为静态LSP和动态LSP两种：静态LSP由手工配置，动态LSP则利用路由协议和标签发布协议动态建立。

MPLS可以使用多种标签发布协议，例如LDP（Label Distribution Protocol）、RSVP-TE（Resource Reservation Protocol Traffic Engineering）和MP-BGP（Multiprotocol Border Gateway Protocol）。

LDP是专为标签发布而制定的协议，也是其中使用较广的一种。LDP规定了标签分发过程中的各种消息以及相关的处理过程。LSR之间将依据转发表中对应于一个特定FEC的入标签、下一跳节点、出标签等信息联系在一起，从而形成标签交换路径LSP。

![img](images\mpls-6)

## 二 LDP

### MPLS LDP简介

标签分发协议LDP（Label Distribution Protocol）是多协议标签交换MPLS的一种控制协议，相当于传统网络中的信令协议，负责转发等价类FEC（Forwarding Equivalence Class）的分类、标签的分配以及标签交换路径LSP（Label Switched Path）的建立和维护等操作。LDP规定了标签分发过程中的各种消息以及相关处理过程。

### 目的

MPLS支持多层标签，并且转发平面面向连接，故具有良好的扩展性，使在统一的MPLS/IP基础网络架构上为客户提供各类服务成为可能。通过LDP协议，标签交换路由器LSR（Label Switched Router）可以把网络层的路由信息直接映射到数据链路层的交换路径上，动态建立起网络层的LSP。

目前，LDP广泛地应用在VPN服务上，具有组网、配置简单、支持基于路由动态建立LSP、支持大容量LSP等优点。

### LDP基本概念

**LDP对等体：**

LDP对等体是指相互之间存在LDP会话、使用LDP来交换标签消息的两个LSR。LDP对等体通过它们之间的LDP会话获得对方的标签。

**LDP邻居体：**

当一台LSR接收到对端发送过来的Hello消息后LDP邻接体建立。LDP邻接体存在两种类型：

- 本地邻接体（Local Adjacency）：以组播形式发送Hello消息（即链路Hello消息）发现的邻接体叫做本地邻接体。
- 远端邻接体（Remote Adjacency）：以单播形式发送Hello消息（即目标Hello消息）发现的邻接体叫做远端邻接体。

LDP通过邻接体来维护对等体的存在，对等体的类型取决于维护它的邻接体的类型。一个对等体可以由多个邻接体来维护，如果由本地邻接体和远端邻接体两者来维护，则对等体类型为本远共存对等体。

**LDP会话：**

LDP会话用于LSR之间交换标签映射、释放等消息。只有存在对等体才能建立LDP会话，LDP会话分为两种类型：

- 本地LDP会话（Local LDP Session）：建立会话的两个LSR之间是直连的。
- 远端LDP会话（Remote LDP Session）：建立会话的两个LSR之间可以是直连的，也可以是非直连的。

本地LDP会话和远端LDP会话可以共存。

### LDP消息类型

LDP协议主要使用四类消息：

- 发现（Discovery）消息：用于通告和维护网络中LSR的存在，如Hello消息。
- 会话（Session）消息：用于建立、维护和终止LDP对等体之间的会话，如Initialization消息、Keepalive消息。
- 通告（Advertisement）消息：用于创建、改变和删除FEC的标签映射。
- 通知（Notification）消息：用于提供建议性的消息和差错通知。

为保证LDP消息的可靠发送，除了Discovery消息使用UDP（User Datagram Protocol）传输外，LDP的Session消息、Advertisement消息和Notification消息都使用TCP（Transmission Control Protocol）传输。

### LDP消息作用

![LDP消息作用：](images\LDP消息作用-ldp)

### LDP工作过程

LDP工作过程主要分为两个阶段：

1. LDP会话的建立

   通过Hello消息发现邻居后，LSR之间开始建立LDP会话。会话建立后，LDP对等体之间通过不断地发送Hello消息和Keepalive消息来维护这个会话。

   - LDP对等体之间，通过周期性发送Hello消息表明自己希望继续维持这种邻接关系。如果Hello保持定时器超时仍没有收到新的Hello消息，则删除Hello邻接关系。邻接关系被删除后，本端LSR将发送Notification消息，结束该LDP会话。
   - LDP对等体之间通过LDP会话连接上传送的Keepalive消息来维持LDP会话。如果会话保持定时器(Keepalive保持定时器)超时仍没有收到任何Keepalive消息，则关闭TCP连接，本端LSR将发送Notification消息，结束LDP会话。

2. LDP LSP的建立

   会话建立后，LDP通过发送标签请求和标签映射消息，在LDP对等体之间通告FEC和标签的绑定关系，从而建立LSP。

### LDP会话的建立

通过LDP发现机制发现LDP对等体用来建立LDP会话。只有建立了LDP会话后，才能建立LDP LSP来承载业务。

### LDP发现机制

LDP发现机制用于LSR发现潜在的LDP对等体。LDP有两种发现机制：

- 基本发现机制：用于发现链路上直连的LSR。

  LSR通过周期性地发送LDP链路Hello消息（LDP Link Hello），实现LDP基本发现机制，建立本地LDP会话。

  LDP链路Hello消息使用UDP报文，目的地址是组播地址224.0.0.2。如果LSR在特定接口接收到LDP链路Hello消息，表明该接口存在LDP对等体。

- 扩展发现机制：用于发现链路上非直连LSR。

  LSR周期性地发送LDP目标Hello消息（LDP Targeted Hello）到指定IP地址，实现LDP扩展发现机制，建立远端LDP会话。

  LDP目标Hello消息使用UDP报文，目的地址是指定IP地址。如果LSR接收到LDP目标Hello消息，表明该LSR存在LDP对等体。

### LDP会话的建立过程

两台LSR之间交换Hello消息触发LDP会话的建立。

LDP会话的建立过程如下图所示：

![LDP会话建立过程](images\LDP会话建立过程.png)

1. 两个LSR之间互相发送Hello消息。

   Hello消息中携带传输地址（即设备的IP地址），双方使用传输地址建立LDP会话。

2. **传输地址较大的一方作为主动方，发起建立TCP连接**。

   如上图所示，LSR_1作为主动方发起建立TCP连接，LSR_2作为被动方等待对方发起连接。

3. TCP连接建立成功后，由主动方LSR_1发送初始化消息，协商建立LDP会话的相关参数。

   LDP会话的相关参数包括LDP协议版本、标签分发方式、Keepalive保持定时器的值、最大PDU长度和标签空间等。

4. 被动方LSR_2收到初始化消息后，LSR_2接受相关参数，则发送初始化消息，同时发送Keepalive消息给主动方LSR_1。

   如果被动方LSR_2不能接受相关参数，则发送Notification消息终止LDP会话的建立。

   初始化消息中包括LDP协议版本、标签分发方式、Keepalive保持定时器的值、最大PDU长度和标签空间等。

5. 主动方LSR_1收到初始化消息后，接受相关参数，则发送Keepalive消息给被动方LSR_2。

   如果主动方LSR_1不能接受相关参数，则发送Notification消息给被动方LSR_2终止LDP会话的建立。

当双方都收到对端的Keepalive消息后，LDP会话建立成功。

### LDP LSP的建立

LDP通过发送标签请求和标签映射消息，在LDP对等体之间通告FEC和标签的绑定关系来建立LSP，而标签的发布和管理由标签发布方式、标签分配控制方式和标签保持方式来决定。

#### 标签的发布和管理

**标签发布方式（Label Advertisement Mode）**

在MPLS体系中，由下游LSR决定将标签分配给特定FEC，再通知上游LSR，即标签由下游指定，标签的分配按从下游到上游的方向分发。

标签发布方式有两种方式。具有标签分发邻接关系的上游LSR和下游LSR必须对使用的标签发布方式达成一致。

![标签发布方式](images\标签发布方式.png)

| 标签发布方式                             | 含义                                                         | 描述                                                         |
| :--------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| 下游自主方式DU（Downstream Unsolicited） | 对于一个特定的FEC，LSR无需从上游获得标签请求消息即进行标签分配与分发。 | 如上图所示，对于目的地址为192.168.1.1/32的FEC，下游（Egress）通过标签映射消息主动向上游（Transit）通告自己的主机路由192.168.1.1/32的标签。 |
| 下游按需方式DoD（Downstream on Demand）  | 对于一个特定的FEC，LSR获得标签请求消息之后才进行标签分配与分发。 | 如上图所示，对于目的地址为192.168.1.1/32的FEC，上游（Ingress）向下游发送标签请求消息，下游（Egress）收到标签请求消息后，才会向上游发送标签映射消息。 |

**标签分配控制方式（Label Distribution Control Mode）**

标签分配控制方式是指在LSP的建立过程中，LSR分配标签时采用的处理方式。

- 独立标签分配控制方式（Independent）：本地LSR可以自主地分配一个标签绑定到某个FEC，并通告给上游LSR，而无需等待下游的标签。
- 有序标签分配控制方式（Ordered）：对于LSR上某个FEC的标签映射，只有当该LSR已经具有此FEC下一跳的标签映射消息、或者该LSR就是此FEC的出节点时，该LSR才可以向上游发送此FEC的标签映射。

**标签分配控制方式和标签发布方式的组合：**

| 标签分配控制方式                        | 下游自主方式DU（Downstream Unsolicited）                     | 下游按需方式DoD（Downstream on Demand）                      |
| :-------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **独立标签分配控制方式（Independent）** | DU ＋ Independent：LSR（Transit）无需等待下游（Egress）的标签，就会直接向上游（Ingress）分发标签。 | DoD ＋ Independent：发送标签请求的LSR（Ingress）的直连下游（Transit）会直接回应标签，而不必等待来自最终下游（Egress）的标签。 |
| **有序标签分配控制方式（Ordered）**     | DU ＋ Ordered：LSR（Transit）只有收到下游（Egress）的标签映射消息，才会向上游（Ingress）分发标签。 | DoD ＋ Ordered：发送标签请求的LSR（Ingress）的直连下游（Transit）只有收到最终下游（Egress）的标签映射消息，才会向上游（Ingress）分发标签。 |

**标签保持方式（Label Retention Mode）**

标签保持方式是指LSR对收到的、但目前暂时不需要的标签映射的处理方式。

LSR收到的标签映射可能来自下一跳，也可能来自非下一跳。

标签保持方式：

1. 自由标签保持方式（Liberal）

   对于从邻居LSR收到的标签映射，无论邻居LSR是不是自己的下一跳都保留。

2. 保守标签保持方式（Conservative）

   对于从邻居LSR收到的标签映射，只有当邻居LSR是自己的下一跳时才保留。

**目前设备支持如下组合方式：**

- 下游自主方式（DU）＋ 有序标签分配控制方式（Ordered）＋ 自由标签保持方式（Liberal），该方式为缺省方式。
- 下游按需方式（DoD）＋ 有序标签分配控制方式（Ordered）＋ 保守标签保持方式（Conservative）。
- 下游自主方式（DU）＋ 独立标签分配控制方式（Independent）＋ 自由标签保持方式（Liberal）。
- 下游按需方式（DoD）＋ 独立标签分配控制方式（Independent）＋ 保守标签保持方式（Conservative）。

#### LDP LSP的建立过程

LSP的建立过程实际就是将FEC和标签进行绑定，并将这种绑定通告LSP上相邻LSR的过程。如下图所示，下面结合下游自主标签发布方式和有序标签控制方式来说明其主要步骤。

![LSP的建立过程](images\LSP的建立过程.png)

1. 缺省情况下，网络的路由改变时，如果有一个边缘节点（Egress）发现自己的路由表中出现了新的主机路由，并且这一路由不属于任何现有的FEC，则该边缘节点需要为这一路由建立一个新的FEC。
2. 如果MPLS网络的Egress有可供分配的标签，则为FEC分配标签，并主动向上游发出标签映射消息，标签映射消息中包含分配的标签和绑定的FEC等信息。
3. Transit收到标签映射消息后，判断标签映射的发送者（Egress）是否为该FEC的下一跳。若是，则在其标签转发表中增加相应的条目，然后主动向上游LSR发送对于指定FEC的标签映射消息。
4. Ingress收到标签映射消息后，判断标签映射的发送者（Transit）是否为该FEC的下一跳。若是，则在标签转发表中增加相应的条目。这时，就完成了LSP的建立，接下来就可以对该FEC对应的数据报文进行标签转发。

上面介绍的是普通LDP LSP的建立，还有一种代理Egress LSP。代理Egress（Proxy Egress）是能够针对非本地路由触发建立LSP的Egress节点，当路由器使能倒数第二跳弹出时，倒数第二跳节点实际上就是一种特殊的代理Egress。一般情况下，代理Egress由配置产生。代理Egress可以应用于网络中有不支持MPLS特性的路由器场景，也可用于解决BGP路由负载分担问题。

### LDP的安全机制

为了提高LDP报文的安全性，MPLS提供了三种保护机制：LDP MD5认证、LDP Keychain认证和LDP GTSM。

LDP Keychain认证是比LDP MD5认证更安全的加密认证，对于同一邻居，只能选择其中一个加密认证；而LDP GTSM用来防止设备受到非法LDP报文的攻击，其可以与前面两个配合使用。

#### LDP MD5认证

MD5（Message-Digest Algorithm 5）是RFC1321定义的国际标准摘要密码算法。MD5的典型应用是针对一段信息计算出对应的信息摘要，从而防止信息被篡改。MD5信息摘要是通过不可逆的字符串变换算法产生的，结果唯一。因此，不管信息内容在传输过程中发生任何形式的改变，只要重新计算就会产生不同的信息摘要，接收端就可以由此判定收到的是一个不正确的报文。

LDP MD5应用其对同一信息段产生唯一摘要信息的特点来实现LDP报文防篡改校验，比一般意义上TCP校验和更为严格。其实现过程如下：

1. LDP会话消息在经TCP发出前，会在TCP头后面填充一个唯一的信息摘要再发出。而这个信息摘要就是把TCP头、LDP会话消息以及用户设置的密码一起作为原始信息，通过MD5算法计算出的。
2. 当接收端收到这个TCP报文时，首先会取得报文的TCP头、信息摘要、LDP会话消息，并结合TCP头、LDP会话消息以及本地保存的密码，利用MD5计算出信息摘要，然后与报文携带的信息摘要进行比较，从而检验报文是否被篡改过。

#### LDP Keychain认证

Keychain是一种增强型加密算法，类似于MD5，Keychain也是针对同一段信息计算出对应的信息摘要，实现LDP报文防篡改校验。

Keychain允许用户定义一组密码，形成一个密码串，并且分别为每个密码指定加解密算法（包括MD5，SHA-1等）及密码使用的有效时间。在收发报文时，系统会按照用户的配置选出一个当前有效的密码，并按照与此密码相匹配的加密解密算法以及密码的有效时间，进行发送时加密和接收时解密报文。此外，系统可以依据密码使用的有效时间，自动完成有效密码的切换，避免了长时间不更改密码导致的密码易破解问题。

Keychain的密码、所使用的加解密算法以及密码使用的有效时间可以单独配置，形成一个Keychain配置节点，每个Keychain配置节点至少需要配置一个密码，并指定加解密算法。

#### LDP GTSM

通用TTL安全保护机制GTSM（Generalized TTL Security Mechanism）是一种通过检查IP报文头中的TTL值是否在一个预先定义好的范围内来实现对IP业务进行保护的机制。使用GTSM的两个前提：

- 设备之间正常报文的TTL值确定
- 报文的TTL值很难被修改

LDP GTSM是GTSM在LDP方面的具体应用。

GTSM通过判定报文的TTL值，确定报文是否有效，从而保护设备免受攻击。LDP GTSM是对相邻或相近（基于只要跳数确定的原则）设备间的LDP消息报文应用此种机制。用户预先在各设备上设定好针对其他设备报文的有效范围，使能GTSM，这样当相应设备之间应用LDP时，如果LDP消息报文的TTL不符合之前设置的范围要求，设备就认为此报文为非法攻击报文予以丢弃，进而实现对上层协议的保护。

### LDP扩展

#### LDP跨域扩展

LDP跨域扩展通过使能LDP按最长匹配原则查找路由，使LDP能够依据聚合后的路由建立起跨越多个IGP区域的LDP LSP。

#### 产生原因

当网络规模比较大时，通常需要部署多个IGP区域来达到灵活部署和快速收敛的目的。在这种情况下，IGP区域间进行路由通告时，为了避免路由数量多而引起的对资源的过多占用，区域边界路由器（ABR）需要将区域内路由聚合，再通告给相邻的IGP区域。然而，LDP在建立LSP的时候，会在路由表中查找与收到的标签映射消息中携带的FEC精确匹配的路由，对于聚合路由，LDP只能建立Liberal LSP，无法建立跨越IGP区域的LDP LSP。因此，引入LDP跨域扩展来解决这个问题。

**注：已经被分配标签，但是没有建立成功的LSP叫做Liberal LSP。**

#### 实现过程

如下图所示,存在Area10和Area20两个IGP区域。在Area10区域边缘的LSR_2的路由表中，存在到LSR_3和LSR_4的两条主机路由，为了避免路由数量多而引起的对资源的过多占用，在LSR_2上通过ISIS路由协议将这两条路由聚合为1.3.0.0/24发送到Area20区域。

![LDP跨域](images\LDP跨域.png)

LDP在建立LSP的时候，会在路由表中查找与收到的标签映射消息中携带的FEC精确匹配的路由，对于上图中的情况，LSR_1的路由表中只有这条聚合后的路由，而没有32位的主机路由。

对于聚合路由，LDP只能建立Liberal LSP，无法建立跨越IGP区域的LDP LSP，以至于无法提供必要的骨干网隧道。

因此，在LSR_1上需要按照最长匹配方式查找路由建立LSP。在LSR_1的路由表中，已经存在聚合路由1.3.0.0/24。当LSR_1收到Area10区域的标签映射消息时（例如携带的FEC为1.3.0.1/32），按照最长匹配的查找方式，LSR_1能够找到聚合路由1.3.0.0/24的信息，把该路由的出接口和下一跳作为到FEC 1.3.0.1/32的出接口和下一跳。这样，LDP就可以建立跨越IGP区域的LDP LSP。

### LDP-IGP 同步

LDP 通常用于使用 OSPF 或 IS-IS 等 IGP 在整个网络域中建立 MPLS 标签交换路径 （LSP）。在这样的网络中，域中的所有链路都有 IGP 邻接和 LDP 邻接。LDP 在 IP 转发确定的目标最短路径上建立 LSP。

如果未同步 IGP 和 LDP，则可能发生数据包丢失。对于不采用 BGP 的核心网络等应用，这个问题尤其重要。另一个示例是 MPLS VPN，其中每个提供商边缘 （PE） 路由器都依赖于其服务的每个 VPN 到另一个 PE 设备的完整 MPLS 转发路径的可用性。这意味着，在 PE 路由器之间的最短路径上，每个链路都必须具有可操作的 hello 邻接和可操作的 LDP 会话，并且 MPLS 标签绑定必须在每个会话之间交换。

LDP 沿着 IP 转发确定的最短路径建立 MPLS LSP。在第 2 层 VPN 或第 3 层 VPN 场景中，如果 PE 设备之间尚未形成 LSP，则依赖于 MPLS 转发的服务将失败。当 LDP 尚未与 IGP 下一跃点交换标签绑定时，由于假定 LSP 已就位，因此 LSP 前端转发流量将被丢弃。

无法启动 LSP 的原因有很多，如下所示：

- 配置错误和实施问题。
- 当 LDP 的邻接或与对等方建立的 LDP 会话丢失时，由于某个错误，而 IGP 仍然指向该对等方。与 LDP 对等方关联的 IGP 链路上继续执行流量的 IP 转发，而不是转移到同步 LDP 的另一个 IGP 链路上。
- 出现新 IGP 链路时，导致特定目标的下一跃点在 IGP 的最短路径优先 （SPF） 计算中发生变化。尽管新链路上可能已启动 IGP，但 LDP 可能尚未完成所有路由的标签交换。这种情况可能是暂时的，也可能是由于配置错误造成的。

在 LDP 会话尚未完全建立时，LDP-IGP 同步阻止使用链路。当某个链路上的 LDP 无法完全运行时，IGP 会播发链路的最大成本，从而防止流量通过该链路。在与链路上的对等方完成 LDP 标签交换或配置的时间量（暂侯期）之前，IGP 不会播发链路的原始成本或指标。

配置同步后，当发生以下某个触发事件时，LDP 会通知 IGP 播发链路的最大成本：

- LDP 邻接关闭。
- LDP 会话关闭。
- 接口上未配置 LDP。

如果配置了暂停计时器，则计时器在发生触发事件时开始。计时器到期后，LDP 会通知 IGP 继续通告原始成本。

如果未配置暂侯计时器，IGP 将等待（无休止），直到从下游路由器接收该接口上有下一跃点的所有转发等效类 （FEC） 的绑定。只有在此之后，LDP 才会通知 IGP 以降低接口成本。

#### LDP可靠性简介

| 技术分类                                                     | 说明                                                         | 包含特性                                 |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------------------------------- |
| 故障检测技术                                                 | 对MPLS网络中的路径进行快速检测，故障时确保快速触发保护技术生效。 | BFD for LDP LSP                          |
| 流量保护技术                                                 | MPLS网络端到端路径故障时，确保流量切换到备份路径，尽可能地避免流量的丢失。 | LDP-IGP联动
LDP Auto FRR
本远端LDP会话共存 |
| MPLS网中的节点控制层面故障时，保证转发层面不中断，从而确保流量转发不中断。 | [LDP GR]                                                     |                                          |

#### BFD for LDP LSP

BFD可以对LSP进行快速的故障检测，触发LSP在发生故障时进行快速主备路径倒换，提高整网可靠性。

当采用LDP LSP承载流量时，如果LSP路径上的节点或链路发生故障时，流量会向备份路径切换。切换的速度依赖于故障的检测速度以及流量的切换速度，如果切换的速度很慢，将会导致长时间的流量丢失。其中流量的切换速度可以由Auto LDP FRR来保证，但是由于LDP协议自身的故障检测机制检测速度较慢，仅仅采用LDP FRR技术并不能完全解决上述问题。



![img](images\BFD-LDP)

因此引入了BFD这种快速检测机制，以便对LDP LSP进行快速的故障检测，触发流量快速向备份路径切换，使得流量丢失最少，进一步提高业务的可靠性。

实现过程

BFD for LDP LSP是指在LSP链路上建立BFD会话，并将会话与LSP绑定。利用BFD快速检测LSP链路的故障，触发LSP的流量切换。使用BFD检测单向LSP路径时，反向链路可以是IP链路、LSP或TE隧道。

检测LDP LSP的连通性时，BFD会话使用静态协商方式：通过手工配置BFD的本地标识符和远端标识符，由BFD本身的协商机制建立会话。用户需要指定待检测的LSP的下一跳IP地址以及BFD会话的对端地址，BFD会话将与LSP绑定。

之后，BFD会采用异步模式检测LSP的连通性，即在Ingress和Egress之间相互周期性地发送BFD报文。如果任何一端在检测时间内没有收到对端发来的BFD报文，就认为LSP发生了故障，并向LDP管理模块上报LSP故障事件。

![img](images\BFD-LDP2)

#### LDP-IGP联动

产生背景

LDP-IGP同步是一种通过同步LDP和IGP之间的状态，来保证在网络发生故障时，LDP和IGP配合将流量丢失时间减到最低。

在存在主备链路的组网中，当主链路发生故障时，IGP和LSP均切换到备份链路上。但当主链路从故障中恢复时，由于IGP比LDP收敛速度快，IGP会先于LDP切换回主链路，而此时主链路的LSP无法立刻建立，需要一些时间进行建立前准备工作，如邻接体恢复等，因此造成LSP流量丢失。当主链路节点间的LDP会话或邻接体发生故障时，主链路上的LSP被删除，但是IGP仍然使用主链路，导致LSP流量不能切换到备份链路，流量持续丢失。

LDP-IGP同步仅支持OSPFv2和IS-IS的IPv4部分。

LDP和IGP同步的基本原理是：通过设置IGP的cost值来推迟路由的回切，直至LDP完成收敛。也就是在主链路的LSP建立之前，先保留备份链路LSP，让流量继续从备份链路转发。直至主链路的LSP建立成功，再删除备份LSP。

LDP和IGP同步的定时器为：

- Hold-max-cost timer
- Delay timer

![img](images\LDP-IGP)





在存在主备链路的组网中，当主链路故障恢复后，流量从备份链路切换到主链路。对于这样的回切流量，本来是有一个可以正常转发的路径，但是如果当IGP收敛之后，备份LSP无法再被使用时，主链路的LSP还没有建立，则在这个时间差内，流量被丢弃。在这种情况下，可以通过配置LDP-IGP同步，令IGP推迟路由的回切，直至LDP完成收敛。即在主链路的LSP没有收敛之前，保持备份LSP，让流量继续从备份LSP转发，直至主链路的LSP建立成功，再删除备份LSP。具体过程如下：

1. 链路故障恢复；
2. IGP在主链路发布最大开销值，推迟IGP路由的回切；
3. 流量仍然会按照备份LSP转发；
4. LDP会话和LDP邻接体都建立成功后，交换标签消息，通告IGP启动同步；
5. IGP在主链路发布正常开销值，IGP收敛到原转发路径上，LSP重新建立并下发转发表（一般在毫秒级）。

当主链路节点间的LDP会话或LDP邻接体发生故障时，主链路上的LSP被删除，但是IGP仍然使用主链路，导致LSP流量不能切换到备份链路，流量持续丢失。在这种情况下，可以配置LDP-IGP联动。在LDP会话或LDP邻接体发生故障时，LDP向IGP通告LDP会话或LDP邻接体故障，这样IGP就会在该链路上发布最大开销值，实现路由切换至备份链路，从而LSP也切换至备份链路，具体过程如下：

1. 主链路节点间LDP会话或LDP邻接体故障；
2. LDP通告IGP主链路LDP会话或LDP邻接体故障，IGP在主链路发布最大开销值；
3. IGP路由切换至备份链路；
4. LSP在备份链路重新建立并下发转发表项。

为防止LDP会话或LDP邻接体一直不能重新建立，可通过配置Hold-max-cost定时器为永久发布最大开销值，使流量在主链路的LDP会话和LDP邻接体重新建立之前，一直都使用备份链路。

![img](images\IGP-LDP)

#### Auto LDP FRR

Auto LDP FRR（Fast Reroute）为MPLS网络提供快速重路由功能，实现了链路备份；当主LSP故障时，流量快速切换到备份路径，从而最大程度上避免流量的丢失。

**产生原因**

在MPLS网络中，当主链路故障时，虽然有IP FRR使IGP路由快速收敛，切换到备份路径，但对MPLS网络还需重新建立LSP，而这个过程无法避免流量的丢失。另外当LSP故障（非主链路故障引起）时，只能等待重新建立LSP后恢复流量转发，这会引起MPLS流量长时间中断。因此需要一种能够在MPLS网络中提供快速重路由的解决方案，即Auto LDP FRR。

Auto LDP FRR通过LDP信令的自由标签保持方式（Liberal），先获取Liberal Label，为该标签申请转发表项资源，并将转发信息下发到转发平面作为主LSP的备用转发表项。当接口故障（接口自己感知或者结合BFD检测）或者主LSP不通（结合BFD检测）时，可以快速的将流量切换至备份路径，从而实现了对主LSP的保护。

**相关概念**

Auto LDP FRR：依赖IP FRR的实现。只有Liberal Label的来源匹配存在的备份路由，即保留的Liberal Label来自备份路由出接口和下一跳，并且满足备份LSP触发策略，才能够为之建立备份LSP并下发转发表项。Auto LDP FRR策略默认是32位的备份路由触发LDP建立备份LSP。

**实现过程**

在自由标签保持方式下，LSR可以从任何相邻LSR收到对于FEC的标签映射消息，但只有从FEC对应路由的下一跳发送来的标签映射会生成标签转发表，从而建立LSP。通过LDP Auto FRR也可以为来自非下一跳的标签映射生成LSP，并作为主LSP的备份，建立转发表项，下发到转发表中，作为主转发表项的备份。当主LSP故障时，能快速切换到备份LSP，避免流量的丢失。

![img](images\SDFSDF)

LSR_1到LSR_2的优选路由为LSR_1-LSR_2，次优路由为LSR_1-LSR_3-LSR_2。当LSR_1收到LSR_3发来的标签后，会和路由比较，因为LSR_1到LSR_2的路由下一跳不是LSR_3，所以LSR_1会把这个标签存为Liberal Label，如果该Liberal Label的来源对应的备份路由存在，就可以为该Liberal Label申请一个转发表项资源，创建备份LSP作为主LSP的备用转发表项，和主LSP一起下发到转发平面，这样主LSP就和这条备份LSP关联起来了。

接口感知接口故障、BFD感知接口故障、或者BFD感知主LSP不通等，都能触发Auto LDP FRR切换。当Auto LDP FRR切换后，流量根据备用转发表项切换到备份LSP上，至此Auto LDP FRR生效。之后的变化过程是路由从LSR_1-LSR_2收敛到LSR_1-LSR_3-LSR_2，在新的路径（原来的备份路径）上根据路由新建LSP，再把原来的主LSP删除，流量按照LSR_1-LSR_3-LSR_2上新建的LSP进行转发。



### LDP可以为以下协议分配标签

- LDP：可以为直连、静态和IGP路由分配标签。
- RSVR-TE：为TE预留资源和分配标签。
- MPBGP：可以为私网路由分配标签。
- BGP：可以为BGP路由分配标签。

### FEC简介

转发等价类FEC（Forwarding Equivalence Class）是一组具有某些共性的数据流的集合。这些数据流在转发过程中被LSR以相同的方式出。

FEC可以根据地质、业务类型、QoS等要素进行划分。例如，在传统的采用最常匹配算法的IP转发中，到同一条路由的所有报文就是一个转发等价类。

Cisco定义：

- LFIB：标签转发表。
- LIB：标签信息数据库。
- FIB：转发信息数据库。

华为定义：

- FTN（FEC to NHLFE）：FIB。
- NHLFE（Next hop lable forward entry）
- ILM（Incoming lable map）：LFIB+LIB。

### LDP配置命令

```
fec-list
//来创建动态BFD检测LDP LSP的FEC列表。
fec-node
//增加BFD会话的FEC节点。
gtsm peer valid-ttl-hops
//在指定的LDP对等体上配置GTSM功能。
label advertise { explicit-null | implicit-null | non-null }
//配置出节点向倒数第二跳分配的标签。
//explicit-null:不支持PHP特性，出节点向倒数第二跳分配显式空标签。显式空标签的值为0。
//implicit-null:支持PHP特性，出节点向倒数第二跳分配隐式空标签。隐式空标签的值为3。
//non-null:不支持PHP特性，出节点向倒数第二跳正常分配标签。分配的标签值不小于16。
label distribution control-mode { independent | ordered }
//配置LDP标签分配控制方式。
//缺省情况下，LDP标签分配控制方式为有序标签分配控制（Ordered）。
label-withdraw-delay
//使能Label Withdraw消息延迟发送功能。
//执行此命令后,Label Withdraw消息延迟发送的时间默认为5秒，
label-withdraw-delay timer 5
//设置Label Withdraw消息延迟发送的时间。
ldp-sync enable
//使能IS-IS进程下所有接口的LDP和IS-IS联动功能。
longest-match
//配置LDP跨域扩展功能，使能LDP按照最长匹配方式查找路由建立LSP。
//缺省情况下，LDP按照精确匹配方式查找路由建立LSP。
lsp-trigger bgp-label-route
//配置LDP为带标签的公网BGP路由分标签的能力。
lsp-trigger
//设置触发建立LSP的策略。
lsr-id
//配置LDP实例的LSR ID。
md5-password
//配置在建立LDP会话时，TCP连接所使用的密码。
md5-password all
//对所有对等体批量配置LDP MD5认证。
mpls
//使能本节点的全局MPLS能力
mpls bfd enable
//在LDP LSP的源端设备上使能动态创建BFD会话的功能。
mpls bfd
//设置BFD会话的相关参数
mpls ldp advertisement { dod | du }
//配置标签发布模式。
//缺省情况下，标签发布模式为下游自主标签分发（Downstream Unsolicited）。
mpls ldp
//来使能本节点的LDP能力
mpls ldp remote-peer
//创建远端对等体并进入远端对等体视图。
mpls ldp timer hello-hold 45
//设置Hello保持定时器的值。
mpls ldp timer hello-send 15
//配置Hello发送定时器的值。
mpls ldp timer igp-sync-delay 10
//配置LDP会话建立后等待LSP建立的时间间隔。
mpls ldp timer keepalive-hold 45
//配置Keepalive保持定时器的值。
mpls ldp timer keepalive-send 15
//配置Keepalive发送定时器的值。
mpls ldp transport-address
//配置LDP传输地址。
mpls-passive
//在LSP的目的端设备上使能被动动态创建BFD会话功能。
remote-ip
//配置LDP远端对等体的IP地址。
remote-ip auto-dod-request
//配置在采用DoD的标签发布方式下，自动向下游指定的远端对等体请求标签映射消息。
remote-peer pwe3
//配置禁止向所有远端邻居分发公网标签。
route recursive-lookup tunnel
//使能迭代隧道功能。
static-lsp egress
//在出口节点配置静态LSP。
static-lsp ingress
//为入口节点配置静态LSP。
static-lsp transit
//为中间转发节点配置静态LSP。
ttl expiration pop
//配置MPLS TTL超时后ICMP响应报文沿本地IP路由转发。
undo ttl expireation pop
//ICMP超时应答报文会沿着LSP继续往下传，由边界设备回送给发送源
ttl propagate
//配置MPLS报文中TTL传播模式为uniform。
//缺省情况下，ttl propagate命令使能，MPLS报文中TTL传播模式是uniform。 
ttl propagate public
//使能MPLS公网报文的IP TTL复制功能。
//缺省情况下，对公网报文使能TTL复制功能。
```

