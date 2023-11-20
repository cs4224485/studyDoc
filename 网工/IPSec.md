## 一 IPSec介绍

### 定义

IPSec是Internet工程任务组（IETF）制定的一个开放的网络层安全框架协议。它并不是一个单独的协议，而是一系列为IP网络提供安全性的协议和服务的集合。IPSec主要包括安全协议AH（Authentication Header）和ESP（Encapsulating Security Payload），密钥管理交换协议IKE（Internet Key Exchange）以及用于网络认证及加密的一些算法等。

### 目的

在IPv4协议诞生之时，Internet网络的规模还非常小，Internet网络的安全完全可以通过物理隔离的方式来保证。另一方面，所有人都未预料到以后Internet网络会爆炸式的增长，所以在[设计](https://www.isolves.com/it/rj/ps/)和开发IPv4协议时，没有考虑IPv4协议的安全保护手段。

由于IP报文本身并不集成任何安全特性，恶意用户很容易便可伪造IP报文的地址、修改报文内容、重播以前的IP数据包以及在传输途中拦截并查看数据包的内容。因此，传统IP层协议不能担保收到的IP数据包的安全。在应用层保证网络安全的方法只对特定的应用有效，不够通用。人们迫切需要能够在IP层提供安全服务的协议，这样可以使TCP/IP高层的所有协议受益。IPSec（Internet Protocol Security）正是用来解决IP层安全性问题的技术。

IPSec主要通过加密与验证等方式，为IP数据包提供安全服务。IPSec可以提供的安全服务包括：

- 数据加密通过数据加密提供数据私密性。
- 数据源验证通过对发送数据的源进行身份验证，保证数据来自真实的发送者。
- 防止数据重放通过在接收方拒绝重复的数据包防止恶意用户通过重复发送捕获到的数据包进行攻击。

### 受益

IPSec具有以下优点：

- 所有使用IP协议进行协议报文传输的应用系统和服务都可以使用IPsec，而不必对这些应用系统和服务本身做任何修改。
- 对协议报文的加密是以数据包为单位的，而不是以整个数据流为单位，这不仅灵活而且有助于进一步提高协议报文的安全性，可以有效防范网络攻击。

### 运营商场景

#### 点到点VPN（Site-to-Site VPN）

IPSec可以为任何基于IP的通信提供安全保护，既可以保护传统的固定网络，也可以保护LTE等移动网络。

点到点VPN也称网关到网关VPN（Gateway to Gateway VPN），可以保证两个网关之间IP流量的安全性

点到点VPN部署非常灵活，而且当两个IPSec网关之间存在NAT设备时，支持IPSec NAT穿越。

### 企业场景

企业场景里IPSec主要用于公司之间通过IPSec VPN网络互连，典型应用是点到点VPN。企业场景里IPSec的组网更加灵活多样。

#### 点到点VPN（Site-to-Site VPN）

点到点VPN主要用于公司总部与分支机构之间建立IPSec隧道，从而实现局域网之间互通

#### 点到多点VPN（Hub-Spoke VPN）

实际组网中最常见的是公司总部与多个分支机构通过点到多点IPSec VPN互通

在这种组网中，用户可以根据实际需求配置IPSec。

此时网络内数据流量可能存在如下两种情况：

- 各分支机构之间不需要通信只有总部和分支之间部署IPSec VPN，也只有总部和分支之间存在业务流量。
- 各分支机构之间需要通信分支机构之间通过总部进行通信

## 二 安全协议

 

IPSec通过AH（Authentication Header，验证头）和ESP（Encapsulating Security Payload，封装安全载荷）两个安全协议实现IP报文的封装/解封装。

- AH是报文头验证协议，主要提供数据源验证、数据完整性验证和防报文重放功能，不提供加密功能。
- ESP是封装安全载荷协议，主要提供加密、数据源验证、数据完整性验证和防报文重放功能。

虽然AH协议和ESP协议都可以提供数据源验证和数据完整性校验服务，但是两者不能互相取代。两者之间的差别在于验证报文的范围不同，验证范围请参见封装模式。

![img](images\20100422_960611_image001_624140_30003_0.png)

![image-20231112132326247](images\image-20231112132326247.png)

### 隧道模式

在隧道模式下，原始IP数据报文被封装成一个新的IP数据报文，并在旧IP报文头和新IP报文头之间插入一个IPSec报文头（AH或ESP），原IP地址被当作有效载荷的一部分受到IPSec的安全保护

隧道模式隐藏了原始IP报文头信息，因此主要应用于两台VPN网关之间或一台主机与一台VPN网关之间的通信。

隧道模式下，AH协议的完整性验证范围为包括新增IP头在内的整个IP报文。ESP协议验证报文的完整性检查部分包括ESP头、原IP头、传输层协议头、数据和ESP尾，但不包括新IP头，因此ESP协议无法保证新IP头的安全。ESP的加密部分包括传输层协议头、数据和ESP尾。

当安全协议同时采用AH和ESP时，AH和ESP协议必须采用相同的封装模式。

### 认证算法与加密算法

1) 认证算法

IPSec采用Hmac（Keyed-Hash Message Authentication Code）功能进行认证。HMAC是HASH函数（单向散列函数）和消息认证码MAC（Message Authentication Code）的结合，HMAC利用Hash函数，以一个对称密钥和一个数据包作为输入，生成一个固定长度的输出，这个输出被称为完整性校验值ICV（Integrity Check Value）。接收方通过比较自身生成的ICV和对端发送的ICV来判断数据的完整性和真实性。

用于验证的对称密钥可以手工配置，也可以通过DH算法生成并在两端设备共享。有关DH算法具体能够生成哪些密钥及密钥的作用请参见IKEv1协商安全联盟的过程。

一般来说IPSec使用以下几种认证算法：

- MD5（Message Digest 5）：输入任意长度的消息，产生一个128比特的消息摘要。
- SHA-1（Secure Hash Algorithm）：输入长度小于264比特的消息，然后生成一个160比特的消息摘要。
- SHA2-256：通过输入长度小于264比特的消息，产生256比特的消息摘要。
- SHA2-384：通过输入长度小于2128比特的消息，产生384比特的消息摘要。
- SHA2-512：通过输入长度小于2128比特的消息，产生512比特的消息摘要。

SHA-2的消息摘要长于MD5和SHA-1，因此，SHA-2比MD5和SHA-1更安全。

​    2.加密算法

用于加密的对称密钥可以手工配置，也可以通过DH算法生成并在两端设备共享。有关DH算法具体能够生成哪些密钥及密钥的作用请参见IKEv1 Phase-1 Negotiation。

一般来说IPSec使用以下加密算法：

- DES（Data Encryption Standard）：使用64bit的密钥对一个64bit的明文块进行加密。
- 3DES（Triple Data Encryption Standard）：使用三个64bit的DES密钥（共192bit密钥）对明文形式的IP报文进行加密。
- AES-CBC-128（Advanced Encryption Standard Cipher Block Chaining 128）：使用128bit加密算法对IP报文进行加密。
- AES-CBC-192（Advanced Encryption Standard Cipher Block Chaining 192）：使用192bit加密算法对IP报文进行加密。
- AES-CBC-256（Advanced Encryption Standard Cipher Block Chaining 256）：使用256bit加密算法对IP报文进行加密。

3DES比DES安全得多，但是其加密速度慢于DES。AES比3DES更安全。

3. 协商方式

有如下两种协商方式建立SA：

​       手工方式（manual）配置比较复杂，创建SA所需的全部信息都必须手工配置，而且不支持一些高级特性（例如定时更新密钥），但优点是可以不依赖IKE而单独实现IPsec功能。

​       IKE自动协商（isakmp）方式相对比较简单，只需要配置好IKE协商安全策略的信息，由IKE自动协商来创建和维护SA。

当与之进行通信的对等体设备数量较少时，或是在小型静态环境中，手工配置SA是可行的。对于中、大型的动态网络环境中，推荐使用IKE协商建立SA。

4. 密钥交换

IKEv1和IKEv2的协商过程中，隧道两端需要进行密钥材料的交换，以便使用相同密钥进行正确的加密和解密。

使用对称密钥进行加密、验证时，如何安全地共享密钥是一个很重要的问题。有两种方法解决这个问题：

- 带外共享密钥在发送、接收设备上手工配置静态的加密、验证密钥。双方通过带外共享的方式（例如通过电话或邮件方式）保证密钥一致性。这种方式的缺点是可扩展性差，在点到多点组网中配置密钥的工作量成倍增加。另外，为提升网络安全性需要周期性修改密钥，这种方式下也很难实施。
- 使用一个安全的连接分发密钥IPSec使用IKE协议在发送、接收设备之间安全地协商密钥。IKE采用DH算法在不安全的网络上安全地交换密钥信息，并生成加密、验证密钥。这种方式配置简单，可扩展性好，特别是在大型动态的网络环境下此优点更加突出。

IKE提供密钥交换，自动协商建立安全联盟等服务。采用IKE协议可以使IPSec配置和管理更简单、更灵活。

Internet安全联盟和密钥管理协议ISAKMP（Internet Security Association and Key Management Protocol）是IKE的基础，IKE使用ISAKMP协议定义密钥交换的过程。ISAKMP提供了对安全服务进行协商的方法，密钥交换时交换信息的方法，以及对对等体身份进行验证的方法。

IKE的精髓在于它永远不在不安全的网络上传送密钥，而是通过一些数据的交换，通信双方最终计算出共享的密钥，并且即使第三方截获了双方用于计算密钥的所有交换数据，也无法计算出真正的密钥。其中的核心技术就是DH（Diffie Hellman）交换技术。

DH用于产生密钥材料，并通过ISAKMP消息在发送和接收设备之间进行密钥材料交换。然后，两端设备各自计算出完全相同的对称密钥。该对称密钥用于加密和验证密钥的计算。在任何时候，双方都不交换真正的密钥。

1. 进行DH交换的双方各自产生一个随机数，如a和b。
2. 使用双方确认的共享的公开的两个参数：底数g和模数p各自用随机数a和b进行幂和模运算，得到结果c和d，计算公式如下：c=gamod(p)d=gbmod(p)
3. 交换计算所得的结果c和d
4. 各自进一步计算，得到一个共同的DH公有值：damod(p)=cbmod(p)=gabmod(p)，此公式可以从数学上证明。DH公有值就是双方的密钥。

若网络上的第三方截获了双方的模c和d，那么要计算出DH公有值gabmod(p)还需要获得a或b，a和b始终没有直接在网络上传输过。如果想由模c和d计算a或b就需要进行离散对数运算，而p为素数，当p足够大时（一般为768位以上的二进制数），数学上已经证明，其计算复杂度非常高，从而认为是不可实现的。所以，DH交换技术可以保证双方能够安全地获得密钥信息。

DH使用密钥组来定义自己产生的密钥长度。密钥长度越长，产生的密钥就越安全，但所需的计算时间也依次递增。

### IPSec安全联盟

IPSec在两个端点之间提供安全通信，这两个端点被称为IPSec对等体。

安全联盟（Security Association）是通信对等体间对某些要素的约定。它定义了保护IP报文安全的协议（AH或者ESP）、IP报文的封装模式、认证算法、保护IP报文的共享密钥等。通过安全联盟实现了IPSec对IP报文的保护。安全联盟是IPSec的基础，也是IPSec的本质。

SA是单向的，输入的IP报文和输出的IP报文由入方向安全联盟和出方向安全联盟分别处理。

安全联盟还与协议相关。如果主机A和主机B同时使用AH和ESP进行安全通信，对于主机A就需要四个SA，AH协议的两个SA（入方向和出方向上各一个SA）和ESP协议的两个SA（入方向和出方向上各一个SA）。同样地，主机B也需要四个SA。

安全联盟由一个三元组来唯一标识。这个三元组包括：安全参数索引SPI（Security Parameter Index）、目的IP地址、安全协议号（AH或ESP）。SPI是为唯一标识SA而生成的一个32比特的数值，它在AH和ESP头中传输。

### IKE的安全机制

DH密钥交换。

完善的前向安全性PFS（Perfect Forward Secrecy）：指一个密钥被破解，并不影响其他密钥的安全性，因为这些密钥间没有派生关系。PFS是由DH算法保障的。此特性是通过在IKE阶段2的协商中增加密钥交换来实现的。

身份验证：身份验证用于确认通信双方的身份。对于pre-shared key验证方法，验证字用来作为一个输入产生密钥，验证字不同是不可能在双方产生相同的密钥的。验证字是验证双方身份的关键。

身份保护：身份数据在密钥产生之后加密传送，实现了对身份数据的保护。

### IKEv1协商阶段1

IKEv1阶段1主要协商下面三个任务：

1. 协商建立IKE SA所使用的参数。加密算法、完整性验证算法、身份认证方法和认证字、DH组、IKE SA生存周期等等。这些参数在IKE安全提议中定义。
2. 使用DH算法交换与密钥相关的信息（生成各种密钥的材料）。对等体双方设备能够使用这些密钥信息各自生成用于ISAKMP消息加密、验证的对称密钥。
3. 对等体之间验证彼此身份。使用预共享密钥或数字证书来验证设备身份。

这三个任务都协商成功后，IKE SA就建立成功了。

IKEv1阶段1支持两种协商模式：主模式（Main Mode）和野蛮模式（Aggressive Mode）

#### **主模式**

主模式采用三个步骤来完成上述三个任务。每个步骤需要2个ISAKMP报文，共6个ISAKMP报文。交换密钥相关信息的操作在身份认证之前完成，故设备的身份信息受到已生成的共享密钥的保护。

![详解IPSec介绍](images\9d2c0aaa0769395ca7f0d23609200696.jpg)

下面对这三个步骤进行详细说明：

1. 协商对等体之间使用的IKE安全提议。DeviceA发送ISAKMP消息，携带建立IKE SA所使用的参数（由IKE安全提议定义）。DeviceB对DeviceA的IKE安全提议进行协商。在协商时将从优先级最高的提议开始匹配，协商双方必须至少有一条匹配的IKE安全提议才能协商成功。匹配的原则为协商双方具有相同的加密算法、认证算法、认证方法和Diffie-Hellman组标识。DeviceB响应ISAKMP消息，携带经协商匹配的安全提议及参数。 如果没有匹配的安全提议，DeviceB将拒绝发起方的安全提议。
2. 使用DH算法交换与密钥相关的信息，并生成密钥。两个对等体通过两条ISAKMP消息（3、4）交换与密钥相关的信息。由获得的密钥信息推导出4个密钥。其中SKEYID为基础密钥，通过它可以推导出SKEYID_a，为ISAKMP消息完整性验证密钥；可以推导出SKEYID_e，为ISAKMP消息加密密钥；可以推导出SKEYID_d，用于衍生出IPSec报文加密、验证密钥。预共享密钥方式和数字证书方式下SKEYID的计算公式不同。
3. 对等体之间验证彼此身份。两个对等体通过两条ISAKMP消息（5、6）交换身份信息（预共享密钥方式下为IP地址或名称，数字证书方式下还需要传输证书的内容），身份信息通过SKEYID_e加密，故可以保证身份信息的安全性。两个对等体使用IKE安全提议中定义的加密算法、验证算法、身份验证方法和SKEYID_a、SKEYID_e对IKE消息进行加解密和验证。IKEv1支持如下身份验证方法：预共享密钥这种方法要求对等体双方必须要有相同的预共享密钥（该密钥直接参与SKEYID的生成计算）。对于设备数量较少的VPN网络来说易于配置，在大型VPN网络中，不建议采用预共享密钥来做身份验证。RSA签名（通常称为数字证书）数字证书需要由CA服务器来颁发。这种方法适用于大型动态的VPN网络。证书验证和预共享密钥验证的主要区别在于SKEYID的计算和交换的身份信息，其他的交换和计算过程和预共享密钥验证方式相同。数字信封认证在数字信封认证中，发起方采用对称密钥加密信息内容，并通过非对称密钥的公钥加密对称密钥，从而保证只有特定的对端才能阅读通信的内容，从而确定对端的身份。此认证方法只能在IKEv1的主模式协商过程中使用，不能在IKEv1野蛮模式协商过程中使用。

#### **野蛮模式**

野蛮模式仅交换3个消息就可以完成IKE SA的建立。

![详解IPSec介绍](images\20761238a9e4483ae1c22d6883223ef8.jpg)

野蛮模式时IKEv1阶段1的协商过程：

1. DeviceA发送ISAKMP消息，携带建立IKE SA所使用的参数、与密钥生成相关的信息和身份验证信息。
2. DeviceB对收到的第一个数据包进行确认，查找并返回匹配的参数、密钥生成信息和身份验证信息。
3. DeviceA回应验证结果，并建立IKE SA。

与主模式相比，野蛮模式的优点是建立IKE SA的速度较快。但是由于密钥交换与身份认证一起进行，野蛮模式无法提供身份保护。

**主模式与野蛮模式的区别**

野蛮模式安全性比主模式差。但是野蛮模式可以满足某些特定场合的网络环境的需求。例如：

- 远程访问时，如果响应者（服务器端）无法预先知道发起者（终端用户）的地址、或者发起者的地址总在变化时，而双方都希望采用预共享密钥验证方法来创建IKE SA，此时可以采用野蛮模式。NE采用预共享认证方式，若是可以获取出口网关的代理IP，也可以在此种情形下采用主模式下配置代理IP的方式。
- 如果发起者已知响应者的策略，或者对响应者的策略有全面的了解，采用野蛮模式能够更快地创建IKE SA。

### IKEv1协商阶段2

IKEv1阶段2的目的就是建立用来传输数据的IPSec SA.IKEv1阶段2通过快速交换模式完成。由于快速交换模式使用IKEv1阶段1中生成的密钥SKEYID_a对ISAKMP消息的完整性和身份进行验证，使用密钥SKEYID_e对ISAKMP消息进行加密，故保证了交换的安全性。

在快速交换模式中，对等体两端协商IPSec SA的各项参数，并为数据传输衍生出密钥。

快速模式共有3条消息完成双方IPSec SA的建立。

1. 消息1发送本端的安全参数和身份认证信息。安全参数包括被保护的数据流和IPSec安全提议等需要协商的参数。身份认证信息包括第一阶段计算出的密钥和第二阶段产生的密钥材料等，可以再次认证对等体。
2. 消息2响应消息1，发送响应方的安全参数和身份认证信息并生成新的密钥。对等体双方通过交换密钥材料生成新的共享密钥，并最终衍生出IPSec的加密密钥。此时响应者和发送者各有两个SA。IPSec SA数据传输需要的加密、验证密钥由SKEYID_d、SPI、协议等参数衍生得出，以保证每个IPSec SA都有自己独一无二的密钥。当启用PFS时，要再次应用DH算法计算出一个共享密钥，然后参与上述计算，因此在参数协商时要为PFS协商DH密钥组。
3. 消息3响应消息2，确认与响应方可以通信，协商结束。

## 三 IPsec特性

### DPD

当两个对等体之间采用IKE和IPSec进行通信时，对等体之间可能会由于路由问题、对等体重启或其他原因等导致连接断开。IKE协议本身没有提供对等体状态检测机制，一旦发生对等体不可达的情况，只能等待安全联盟的生存周期到期。生存周期到期之前，对等体之间的安全联盟将一直存在。安全联盟连接的对等体不可达将引发“黑洞”，导致数据流被丢弃。通常情况下，迫切需要识别和检测到这些“黑洞”，以便尽快的恢复IPSec通信。

Keepalive机制可以解决这个问题。Keepalive机制是指IKE对等体间通过周期性的交换Hello/Ack消息来告知对方自己处于活动状态。但是在设备上的IKE SA数量很大时，发送的Hello/Ack消息将会大量消耗设备的CPU资源，限制了这种机制的应用。

失效对等体检测DPD（Dead Peer Detect）是Keepalive机制的一种替代机制，它利用IPSec流量使对等体状态检测所需消息的数量达到最小化。DPD规定每个IKE peer的状态和对端状态是完全独立的，当IKE peer想知道对端是否在线时，随时请求，不需要等待间隔时间的到来。当peer之间有正常的IPSec流量时，证明对端肯定在线，此时没有必要去发送额外的消息探测对端是否在线。只有一段时间内没有流量发生，peer的活动状态才值得怀疑，那么本端在发送流量前应该发送一次DPD消息来检测对端的状态。

DPD有两种模式可以选择：interval和on-demand。

interval：表示DPD工作在轮询模式，在check-interval时间内，如果没有收到对端发过来的流量就会以check-interval为周期循环发送DPD检测报文。如果期间收到对端的响应报文，那么本次DPD流程结束，进入新的DPD检测周期。如果期间没有收到对端的响应报文，则会进行报文重传。重传结束后，如果依然没有收到响应则会删除本端SA表项，重新执行隧道新建流程。

on-demand：表示DPD工作在流量触发模式，如果本端没有加密流量发送，那么是不会发送DPD报文的，这是和轮询模式的最大区别。如果本端有加密流量需要发送，并且发送后在check-interval时间内没有收到对端发过来的流量，那么就会以check-interval为周期循环发送DPD检测报文。如果期间收到对端的响应报文，那么本次DPD流程结束，进入新的DPD检测周期。如果期间没有收到对端的响应报文，则会进行报文重传。重传结束后，如果依然没有收到响应则会删除本端SA表项，重新执行隧道新建流程。

### IPSec NAT穿越

NAT技术主要用于解决IPv4地址紧缺问题，在目前网络中NAT应用非常广泛，特别是在企业网出口网关大都使用了NAT技术解决公网地址不足的问题。IPSec提供了端到端的IP通信的安全性，可以实现同一企业集团不同地域分支之间的低成本安全互连。但是IPSec和NAT技术本身存在不兼容的问题。

- 从NAT的角度上说，为了完成地址转换，势必会修改IP报文头中的IP地址。
- 从IPSec的角度上说，IPSec要保证数据的安全，因此它会加密和校验数据。AH主要用于保护消息的完整性，其验证范围包含IP报文头，而NAT修改IP报文头会导致AH检查失败，因此使用AH保护的IPSec隧道是不能穿越NAT网关的。但是ESP协议保护的报文不存在该问题，因为ESP保护的部分不包含IP报文头（对隧道方式而言是外层IP报文头）。

但是还是有新的不兼容问题，当NAT改变了某个包的IP地址和（或）端口号时，它通常要更新TCP或UDP校验和。当TCP或UDP校验和使用了ESP来加密时，它就无法更新这个校验和。

- ESP封装的隧道模式：ESP隧道模式将整个原始的IP包整个进行了加密，且在ESP的头部外面新加了一层IP头部，所以NAT如果只改变最前面的IP地址对后面受到保护的部分是不会有影响的。因此，IPSec采用ESP的隧道模式来封装数据时可以与NAT共存。

### IPSec穿越NAT的处理

IPSec NAT穿越的流程是：

- NAT穿越（NAT-Traversal，简称NAT-T）能力检测：建立IPSec隧道的两端需要进行NAT穿越能力协商，这是在IKE协商的前两个消息中进行的，通过Vendor ID载荷指明的一组数据来标识。
- NAT网关发现：通过NAT-D（NAT-Discovery）载荷来实现的，该载荷用于在IKE Peer之间发现NAT网关的存在以及确定NAT设备在Peer的哪一侧。NAT侧的Peer作为发起者，需要定期发送NAT-Keepalive报文，以使NAT网关确保安全隧道处于激活状态。
- ESP报文正常穿越NAT网关：IPSec穿越NAT，简单来说就是在原报文的IP头和ESP头（不考虑AH方式）间增加一个标准的UDP报文头。这样，当ESP报文穿越NAT网关时，NAT对该报文的外层IP头和增加的UDP报头进行地址和端口号转换；转换后的报文到达IPSec隧道对端时，与普通IPSec处理方式相同，但在发送响应报文时也要在IP头和ESP头之间增加一个UDP报文头。。

### IKEv2与NAT穿越

**NAT-T能力检测**

NAT-T能力检测在IKE协商的前两个消息中交换完成，通过在消息中插入一个标识NAT-T能力的Vendor ID载荷来告诉对方自己对该能力的支持。如果双方都在各自的消息中包含了该载荷，说明双方对NAT-T都是支持的。只有双方同时支持NAT-T能力，才能继续进行其他协商。

**NAT网关发现**

当存在NAT设备时必须使用UDP传输，所以在IKEv2中的第一阶段协商中必须先探测是否存在NAT设备，也就是NAT探测。

通过发送NAT-D载荷来实现NAT探测是目前比较流行的方法。

在传统IKE中NAT-D载荷包括在主模式的第三个和第四个信息中以及野蛮模式的第二个和第三个信息中。对于创建VPN连接的双方来说，发送的信息中一般要包括两个连续的NAT-D载荷，第一个是关于目的地址，第二个是关于源地址。如果发送方不知道自己的确切地址(发送方有多个接口，应用程序并不知道数据包从哪个接口出去)，则需要多个NAT-D载荷，从第二个载荷开始，每个载荷和发送方的一个地址相关。对方接收到NAT-D载荷后重新根据收到的包的实际地址端口来计算hash值后进行比较，就可以知道是否有NAT设备以及哪一方在NAT设备之后了。这种方法虽然能检测两个IKE对端之间NAT设备的存在，但存在着明显的缺陷。因为在主模式和野蛮模式中，NAT-D载荷没有被认证，这意味着入侵者可以删除、改变、增加这些载荷，这将导致DoS攻击。通过改变NAT-D载荷，攻击者可以使两方使用UDP封装的模式，而不是使用正常的模式，导致浪费带宽。

为了解决上述缺陷，探测通信链路中是否存在NAT设备，可在协商双方增加两个Notify载荷，一个包括NAT_DETECTION_SOURCE_IP，标识发起方的IP地址；一个包括NAT_DETECTION_DESTINATION_IP，标识目的方的IP地址。这两个载荷主要是为了探测通信双方是否存在NAT设备，并且确定哪一方处在NAT设备之后。

这一过程在IKEv2协商的第一组交换中进行。具体过程如下：

在IKEv2中，NAT_DETECTION_SOURCE_IP和NAT_DETECTION_DESTINATION_IP在Notify消息类型中的编号分别为：16388和16389。载荷使用通用的ISAKMP载荷头，载荷的值是SPIs、IP地址、发送数据包的端口号的hash值(IKEv2规定使用SHA-1)，hash值的计算如下：hash=SHA-1(SPIs|IP|Port)。其中：

- SPIs为HDR载荷中的安全索引参数。
- IP为数据包发出方或接收方的IP地址。
- Port为数据包发出方或接收方的端口号。

当接受方收到数据包后，对数据包中的SPIs、IP地址、端口号进行hash运算，并与Notify载荷进行比较，如果不匹配，则说明通信链路中存在NAT设备：如果与NAT_DETECTION_SOURCE_IP不匹配，则说明发起端在NAT设备之后；如果与NAT_DETECTION_DESTINATION_IP不匹配，则说明接受端在NAT设备之后。

**NAT穿越的启用**

在第一阶段协商完成之后，协商双方均已经明确是否存在NAT，以及NAT的位置。至于是否启用NAT穿越，则由快速模式协商决定。

NAT穿越的启用协商在快速模式的SA载荷中进行。

**NAT-keepalive**

在NAT网关上NAT会话有一定的存活时间，因此，隧道建立后如果中间长时间没有报文穿越，就会导致NAT会话被删除，这样将导致无法通过隧道传输数据。解决方法是在NAT会话超时前，发送一个NAT-keepalive给对端，维持NAT会话的存活。

### GRE over IPSec

IPSec本身不支持封装组播、广播和非IP报文，GRE无法对报文进行认证加密，通过GRE over IPSec技术可以将组播、广播报文先封装GRE后，然后再进行IPSec加密处理。同时采用GRE的接口对接收到的加解密流量来进行统计。当网关之间采用GRE over IPSec连接时，先进行GRE封装，再进行IPSec封装

IPSec封装过程中增加的IP头即源地址为IPSec网关应用IPSec策略的接口地址，目的地址即IPSec对等体中应用IPSec策略的接口地址。

IPSec需要保护的数据流为从GRE起点到GRE终点的数据流。GRE封装过程中增加的IP头即源地址为GRE隧道的源端地址，目的地址为GRE隧道的目的端地址。

基于GRE over IPSec的应用很多，比如BGP、LDP、OSPF、IS-IS和IPv6等协议，这些应用的原理相同，都是将协议报文使用GRE封装成IP报文，然后再在IPSec隧道里传输。

IPSec和GRE结合，还有一种IPSec over GRE方案，即先使用IPSec对报文进行封装，然后再使用GRE封装。但是，这种封装方式既没有充分利用IPSec和GRE的优势，也无法支持组播、广播和非IP报文，因此一般不推荐使用。

![封装](images\gre over IPSec)

IPSec封装过程中增加的IP头即源地址为IPSec网关应用IPSec安全策略的接口地址，目的地址即IPSec对等体中应用IPSec安全策略的接口地址。

IPSec需要保护的数据流为从GRE起点到GRE终点的数据流。GRE封装过程中增加的IP头即源地址为GRE隧道的源端地址，目的地址为GRE隧道的目的端地址。

#### 实验一：IPSec策略在物理接口调用：

```
第一步： 完成接口基本配置。
第二步：分别创建GRE隧道接口，并配置 GRE 隧道接口的 IP 地址、源地址和目的地址。
FW1:
interface Tunnel0
 ip address 172.16.1.1 255.255.255.0 
 tunnel-protocol gre
 source 202.100.1.10
 destination 202.100.1.11

FW2
interface Tunnel0
 ip address 172.16.1.2 255.255.255.0 
 tunnel-protocol gre
 source 202.100.1.11
 destination 202.100.1.10
  
第三步：配置静态路由，将出接口指定为 GRE 隧道接口，将流量引入到隧道中。
注意：也可以动态路由方式
FW1:
 ip route-static 10.1.2.0 255.255.255.0 Tunnel0

FW2
 ip route-static 10.1.1.0 255.255.255.0 Tunnel0

第四步：配置 IPSec 隧道。包括配置 IPSec 策略的基本信息、配置待加密的数据流和配置安全提议。
IPSEC配置：
阶段一：
ike proposal 10
 authentication-algorithm sha2-256
 integrity-algorithm aes-xcbc-96 hmac-sha2-256

ike peer 10           
 pre-shared-key Huawei@123
 ike-proposal 10  
 remote-address 202.100.1.11

阶段二：
acl number 3000
 rule 5 permit ip source 202.100.1.10 0 destination 202.100.1.11 0
注意: 保护的是GRE的隧道 

ipsec proposal 10  
 encapsulation-mode auto
 esp authentication-algorithm sha2-256
#
ipsec policy ipsec_policy 10 isakmp
 security acl 3000
 ike-peer 10  
 proposal 10  

interface GigabitEthernet0/0/2  --------------在物理接口调用 
 ip address 202.100.1.10 255.255.255.0
 ipsec policy ipsec_policy
```

**安全策略的放行：**

![安全策略](images\安全策略.png)

**注意：关于需不需要放行gre流量的问题。**
**因为gre头部是在esp头部或公网IP头部中封装的，实际流量会被esp加密传输。应该是不需要放行gre的，但是在实际测试中需要放行。**

**在华为防火墙实际测试中，放行gre流量后IPSec SA可以正常建立，双方的主机也可以互相通信。而不放行gre的话，IPSec SA可以正常建立，但是双方的主机不能互相通信。**

#### 实验二：IPSec策略在Tunnel口调用：

```
IPSEC 配置思路：  
阶段一: 
ike proposal 10
 authentication-algorithm sha2-256
 integrity-algorithm aes-xcbc-96 hmac-sha2-256
#
ike peer 10            
 pre-shared-key Huawei@123
 ike-proposal 10
 
注意：不能配置remote-address.

阶段二:
不需要感兴趣流 
ipsec proposal 10
 encapsulation-mode auto
 esp
#
ipsec profile ipsec_pro
 ike-peer 10
 proposal 10

不能调用ACL 

调用：
interface Tunnel0
 ipsec profile ipsec_pro

放行策略：
security-policy
 rule name IPSEC1
  source-zone local
  source-zone untrust
  destination-zone local
  destination-zone untrust
  source-address 202.100.1.10 mask 255.255.255.255
  source-address 202.100.1.11 mask 255.255.255.255
  destination-address 202.100.1.10 mask 255.255.255.255
  destination-address 202.100.1.11 mask 255.255.255.255
  service ISAKMP
  service esp
  action permit

 rule name IPSEC2
  source-zone trust
  source-zone vpn
  destination-zone trust
  destination-zone vpn
  source-address 10.1.1.0 mask 255.255.255.0
  source-address 10.1.2.0 mask 255.255.255.0
  destination-address 10.1.1.0 mask 255.255.255.0
  destination-address 10.1.2.0 mask 255.255.255.0
  action permit    
                       
  rule name vpn_local  ----------只需要放行VPN-LOCAL
  source-zone vpn
  destination-zone local 
  service gre
  action permit
```

**注意：当在Tunnel口调用IPSec后，可以成功建立IPSec SA，需要流量的触发。但是在防火墙的Web管理界面的IPSec监控中看不到有关IPSec的信息，只能通过命令行查看。**

**在配置IPSec Profile（模板）的时候：**

- **不能配置远端的IP地址**
- **不能绑定ACL，即感兴趣流**

## 四 实验配置GRE OVER IPsec

![image-20231112115858562](images\image-20231112115858562.png)

首先配置GRE Tunnel

```
[R1]dis current-configuration int tunn 0/0/1
[V200R003C00]
interface Tunnel0/0/1
 description 200.20.20.2
 ip address 192.168.1.1 255.255.255.0 
 tunnel-protocol gre
 source 100.10.10.1
 destination 200.20.20.2

```

```
[R3]dis current-configuration int t0/0/1
[V200R003C00]
#
interface Tunnel0/0/1
 description 100.10.10.1
 ip address 192.168.1.2 255.255.255.0 
 tunnel-protocol gre
 source 200.20.20.2
#
```

gre抓包

![image-20231112120113453](images\image-20231112120113453.png)

配置 IPSec 

```
[R1-GigabitEthernet0/0/0]ipsec policy ipse_policy配置1阶段
[R1]ike proposal 10
[R1-ike-proposal-10]authentication-method ?
  digital-envelope  Select digital envelope  key as the authentication method
  pre-share         Select pre-shared key as the authentication method
  rsa-signature     Select rsa-signature key as the authentication method
[R1-ike-proposal-10]authentication-method pre-share 
配置ike对等体
[R1]ike peer 10 v1
[R1-ike-peer-10]pre-shared-key ?
  cipher  Pre-shared-key with cipher text
  simple  Pre-shared-key with plain text
[R1-ike-peer-10]pre-shared-key simple huawei
[R1-ike-peer-10]ike-proposal 10
[R1-ike-peer-10]remote-address 200.20.20.2

配置2阶	
[R1-acl-adv-3000]rule 5 permit ip source 100.10.10.1 0 destination 200.20.20.2 0
[R1]ipsec proposal 10
[R1-ipsec-proposal-10]encapsulation-mode ?
  transport  Only the payload of IP packet is protected(transport mode)
  tunnel     The entire IP packet is protected(tunnel mode)
[R1-ipsec-proposal-10]encapsulation-mode transport 
[R1-ipsec-proposal-10]esp authentication-algorithm sh?
  sha1      Use HMAC-SHA1-96 algorithm
  sha2-256  Use SHA2-256 algorithm
  sha2-384  Use SHA2-384 algorithm
  sha2-512  Use SHA2-512 algorithm
[R1-ipsec-proposal-10]esp authentication-algorithm sha2-512
[R1]ipsec policy ipse_policy 10 isakmp 
[R1-ipsec-policy-isakmp-ipse_policy-10]security acl 3000
[R1-ipsec-policy-isakmp-ipse_policy-10]ike-peer 10	
[R1-ipsec-policy-isakmp-ipse_policy-10]proposal 10

在物理接口调用
[R1-GigabitEthernet0/0/0]ipsec policy ipse_policy
```

![image-20231112121955931](images\image-20231112121955931.png)

![image-20231112131845569](images\image-20231112131845569.png)