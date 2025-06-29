# 一 RouterOS安装和简介

RouterOS(简称ROS)是拉脱维亚MikroTik公司开发的一 种基于Linux 内核的路由操作系统。
通过该软件可以将标准的PC电脑变成专业路由器，在软件RouterOS 软路由图的开发和应用上不断的更新和发展，软件经历了多次更新和改进，使其功能在不断增强和完善。特别在无线、认证、策略路由、带宽控制和防火墙过滤等功能上有着非常突出的功能，其极高的性价比，受到许多网络人士的青睐。

官方的下载地址如下文所示：

（注意：RouterOS是要和Winbox搭配一起使用的，这两个都能在下方的这个地址里找到下载，另外，这个是试用版，只能用24小时，所以请记得做好快照）

**首先在官网上下载RouterOS的镜像（选择CDROM可获取ISO镜像文件）和winbox**

![image-20230919203935132](D:\study\studyDoc\网工\images\image-20230919203935132.png)

![image-20230919204008542](D:\study\studyDoc\网工\images\image-20230919204008542.png)

**新建ROS虚拟机**

![image-20230919204307242](images\image-2023091920430722为2)

 系统会自动进入安装界面，根据提示按下“i”即可进行安装。**（部分RouterOS会需要你进行功能的选择，这种情况下如果想全选那就按下"a"即可）**

![image-20230919204352876](images\image-20230919204352876.png)

用户名默认为admin，没有密码

到这一步，RouterOS系统就算全部安装完毕了，接下来要用WinBox去操作RouterOS。

![](images\image-20230919205119261.png)

WinBox无需安装，可以直接打开：

打开WinBox后，选择下方的Neighbors，就可以搜索到正在运行的ROS系统，选择你要使用的ROS系统，输入用户名和密码即可进入用户界面。(默认用户是admin，没有密码)

![image-20230919205559281](images\image-20230919205559281.png)

## 命令行配置

###  

命令行可采用缩写方式，如命令完整输入应位ip address print， 可缩写位ip addr pri

ROS命令行采用类似linux中文件目录层级结构，即上述命令可采取先输入ip层级，再直接输入addr进入ip地址层，再直接输入print

也可以采用绝对路径方式在任一层级直接输入/ip addr pri或/ip/address/print命令输入



### 基本命令

修改当前登录用户名密码

```
[admin@MikroTik] > password
old-password: *********
new-password: *********
```

修改接口ip地址

```
[admin@MikroTik] /ip/address> add address=192.168.1.222/24 interface=Lan  
```

![image-20230919214134722](images\image-20230919214134722.png)



查看当前设备配置

```
[admin@MikroTik] /ip/address> export
# 2023-09-19 21:42:13 by RouterOS 7.11.2
# software id = DJ21-EIQP
#
/ip address
add address=192.168.1.222 interface=Lan network=192.168.1.222

```

![image-20230919214225463](images\image-20230919214225463.png)

![image-20230919214349057](images\image-20230919214349057.png)



### 更改网卡的名称以方便区分不同的网络接口

接入互联网的网络接口命名为Wan，接入[局域网](https://so.csdn.net/so/search?q=局域网&spm=1001.2101.3001.7020)的互联网接口我们命名为Lan，命令执行过程和显示界面如下：

![image-20230919205918469](images\image-20230919205918469.png)

### 对网卡的命名和启用（如果你的网卡没有启用的话）

输入print查看网卡是否启用

![image-20230919205946820](images\image-20230919205946820.png)

默认是启用的，标志是网卡名字前面显示R，比如我的网卡ether1前面显示R。若没有启动，则显示X。

第一步：启用网卡
en 0 回车
en 1 回车

第二步：设置网卡名称
set 0 name=Lan 回车
set 1 name=Wan 回车

![image-20230919210048893](images\image-20230919210048893.png)

第三步：输入命令
print
看下命令是否执行成功。
命令解释：将0和1的网卡启用，设置ID为0的网卡为内网，名字为LAN，设置ID为1的网卡为外网，名字为WAN

![image-20230919210116711](images\image-20230919210116711.png)

输入 / 退回到根目录，设定网卡地址等信息。 输入setup进入网卡配置界面



综合配置

![image-20230919215824048](C:\Users\cs1\AppData\Roaming\Typora\typora-user-images\image-20230919215824048.png)



### 物理设备登录

winbox登录方式

![image-20230919210552483](C:\Users\cs1\AppData\Roaming\Typora\typora-user-images\image-20230919210552483.png)

web登录

![image-20230919211013369](images\image-20230919211013369.png)

命令行方式

![image-20230919211224064](images\image-20230919211224064.png)



### 安全模式

通常情况下我们是通过网络连接到 RouterOS，并操作修改配置，然而错误的配置，会造成路由器不能访问（除了本地终端控制），但这个时候已经
不能使用 undo 撤销来还原操作，在此时已经与路由器断开连接。为了将这一的风险降低到最低，我们可以使用 Safe 模式。

在命令行 Safe 模式通过组合键[Ctrl]+[X]开启，退出 safe 模式，再一次按[Ctrl]+[X]

![image-20230923112044347](images\image-20230923112044347.png)

当在命令行开启 Safe 模式，Safe Mode taken 消息提示在屏幕上，所有配置修改都会被执行，虽然路由器在 Safe 模式下，但如果 Safe 模式连接异常中
断，Safe 模式下的配置将自动解除，你可以看到所有的配置在历史记录里都会有一个 F 标记，如下，我们添加了一个默认网关，然后进入/system history
查看，能看到 route added前有一个 F 标记：

![image-20230923112128044](images\image-20230923112128044.png)



现在，如果 **telnet** 连接或者 **winbox** 连接中断，这时连接超时 9 分钟后，所有在 **Safe** 模式下的配置修改将会被自动解除。退出 **Safe** 模式可以使用 **[Ctrl]+[D]**

解除，因此，最好在 **Safe** 模式下做一些小范围的修改

# 二 用户管理

### read用户组

顾名思义，此用户组用户仅仅只能进行配置查看不能配置进行修改，可用如下命令查看red用户组能够查看的配置内容：

```
[admin@MikroTik] > /user/group/print where name="read"
 0 name="read" policy=local,telnet,ssh,reboot,read,test,winbox,password,web,sniff,
       sensitive,api,romon,rest-api,!ftp,!write,!policy 
   skin=default 

```

### write用户组

write用户组用户可进行配置修改，但对特定特性雾权限操作

```bash
[admin@MikroTik] > /user/group/print where name="write"    
 1 name="write" policy=local,telnet,ssh,reboot,read,write,test,winbox,password,web
,
       sniff,sensitive,api,romon,rest-api,!ftp,!policy 
   skin=default 

```

### full用户组

```bash
[admin@MikroTik] > /user/group/print where name="full"       
 2 name="full" policy=local,telnet,ssh,ftp,reboot,read,write,policy,test,winbox,
       password,web,sniff,sensitive,api,romon,rest-api 
   skin=default 

```

```bash
[admin@MikroTik] /user/group> print 
 0 name="read" policy=local,telnet,ssh,reboot,read,test,winbox,password,web,sniff,
       sensitive,api,romon,rest-api,!ftp,!write,!policy 
   skin=default 

 1 name="write" policy=local,telnet,ssh,reboot,read,write,test,winbox,password,web
,
       sniff,sensitive,api,romon,rest-api,!ftp,!policy 
   skin=default 

 2 name="full" policy=local,telnet,ssh,ftp,reboot,read,write,policy,test,winbox,
       password,web,sniff,sensitive,api,romon,rest-api 
   skin=default 
```

```bash
[admin@MikroTik] /user/group> print where name="read" 
 0 name="read" policy=local,telnet,ssh,reboot,read,test,winbox,password,web,sniff,
       sensitive,api,romon,rest-api,!ftp,!write,!policy 
   skin=default 

```

### 添加新用户

```bash
[admin@MikroTik] > /user add name=harry group=read password=123456
// 添加一个harry 用户
```

### 显示当前登录用户

```bash
[admin@MikroTik] > /user/active/print detail 
Flags: R - radius; M - by-romon 
 0    when=2023-09-20 20:52:09 name="admin" via=console group=full 

 1    when=2023-09-20 20:52:32 name="admin" address=84:A9:38:0F:9D:E0 via=winbox 
      group=full 

 2    when=2023-09-20 20:52:38 name="admin" via=console group=full 

```

# 三 ROS系统管理

### 系统升级

确定自己所用设备的cpu架构

```
[admin@MikroTik] > sys resource print
                   uptime: 14m51s
                  version: 7.11.2 (stable)
               build-time: Aug/31/2023 13:55:47
         factory-software: 7.1
              free-memory: 139.3MiB
             total-memory: 192.0MiB
                      cpu: AMD
                cpu-count: 1
            cpu-frequency: 3194MHz
                 cpu-load: 0%
           free-hdd-space: 15.8GiB
          total-hdd-space: 15.8GiB
  write-sect-since-reboot: 1544
         write-sect-total: 1544
        architecture-name: x86_64
               board-name: x86
                 platform: MikroTik

```

根据自己所用cpu的架构

![image-20230920211437361](images\image-20230920211437361.png)

将软件包copy到设备存储空间

![image-20230920211906827](images\image-20230920211906827.png)

系统监测自动升级方式



### 系统降级

![image-20230920212919580](images\image-20230920212919580.png)

### 设置主机名

![image-20230921205241551](C:\Users\cs1\AppData\Roaming\Typora\typora-user-images\image-20230921205241551.png)

### 系统资源管理

操作路径：/system resource

查看系统资源可以了解 RouterOS 的运行情况

![image-20230923111428863](images\image-20230923111428863.png)

通过 monitor 命令实时的 CPU 占用率、内存和硬盘等使用情况。

![image-20230923111504981](images\image-20230923111504981.png)

实时查看系统 CPU 和空闲内存使用情况：

![image-20230923111525126](images\image-20230923111525126.png)

使用 winbox 查看：

![image-20230923111546215](images\image-20230923111546215.png)

**CPU**

操作路径: /system resource cpu

在 RouterOS v5 版本后增加了CPU菜单，该菜单显示每个CPU使用率，也包括IRQ和Disk使用率

![image-20230923111632671](images\image-20230923111632671.png)

在 Winbox 中查看每个 CPU 的占用情况：

![image-20230923111655897](images\image-20230923111655897.png)

在tool里还增加了每个功能的CPU占用情况，进入tool profile下可以查看RouterOS各个功能CPU使用情况，和windows资源管理器类似

![image-20230923111725778](images\image-20230923111725778.png)

### Watchdog 监测

Watchdog 监测系统运行情况，一旦系统软件故障或停止响应，将会自动重启，由此来避免死机和停止工作。



通过 **watchdog** 可以监控一个 IP 地址没有响应或者系统被锁死，一旦发生这样的情况将发出重启指令。软件计时器是用来提供上一次的记录, 但是在特殊的

情况下(由硬件故障引起的) 它能锁定自己. 对于 **RouterBOARD**的硬件监测设备来说它能在任何异常情况下重启。

**属性描述**

 **auto-send-supout (yes | no;** 默认: **no**) – 技术支持文件将通过邮件发送到指定邮箱。

 **automatic-supout (yes | no;** 默认: **yes**) –当软件错误发生时, 将是自动生成，如果新的技术支持文件产生将命名为**"autosupout.rif"** ，而之前的文件，

 **no-ping-delay** (时间; 默认: **5m**) – 在重启以后多久去测试和 **ping watch-address.** 默认设置是如果

 **watch-address** 被设置为不可达，这时路由器将在 6 分钟的时候重启.

**send-email-from** (文本; 默认: "") – 发送邮件的来源地址，确定**/tool e-mail** 功能开启。

 **send-email-to** ( 文本 ; 默认: "") – 接收技术支持文件的邮件地址。

 **send-smtp-server** ( 文本 ; 默认: "") – **SMTP** 服务地址，如果没有设置可以通过操作路径**/tool e-mail** 开启功能。

 **watch-address** (**IP** 地址 ; 默认: **none**) – 如果设置这功能了的话，一旦 **6** 个连续的 **ping** 包没有响应，系统会重启。

 **watchdog-timer (yes | no**; 默认: **no**) – 是否启用 **watchdog** 功能。

下面是一个系统崩溃的邮件发送配置，一旦系统崩溃，自动产生的 supout.rif 技术支持文件，并自动通过192.0.2.1 发送到 support@example.com:

![image-20230923111915761](images\image-20230923111915761.png)

如我们通过 ping 监控 IP 地址 192.168.88.5，当在 5 分钟后没有回应，路由器会自动重启。

![image-20230923111943021](images\image-20230923111943021.png)

### 设置NTP服务器

![image-20230923112341891](images\image-20230923112341891.png)

![image-20230923112849790](images\image-20230923112849790.png)

![image-20230923112906204](images\image-20230923112906204.png)

### RouterOS 备份与复位管理

**RouterOS** 可以通过 **backup** 下的 **save** 命令将系统备份为二进制文件，采用 **FTP** 访问或在 **winbox** 中的 **file** 列表中下载备份文件，并可以通过备份文件恢复路由器设置。

**RouterOS** 通过 **export** 命令导出配置文件，可生成文本文件（可编辑脚本），同样使用 **FTP** 或通过在 **winbox**中的 **file** 中下载文件，导入配置则将脚本文本文件导入路由器。

**reset-configuration** 系统复位命令将所有的配置信息从 **RouterOS** 中全部删除掉，在做此操作前，最好先将路由器的配置备份一次。

注 ： 为了保证备份不会失败，请在将备份的文件恢复到同样的软件版本和同样的硬件配置上去.

操作路径：/system backup
Save 指令是保存当前配置到一个备份文件中，显示文件在/file 目录中。如果需要恢复指定的备份文件，可通过/system backup 中的 load 指令载入配置，
还原当前备份文件的配置。
从 RouterOS v6.13 开始可以对备份文件做加密，增加了 don't-encrypt 和 password 命令
命令 描述:
load name=[filename] – 载入备份文件的配置
save name=[filename] – 保存当前的配置到文件中
dont-encrypt – 告诉系统不使用任何加密，并生成可查看的编辑文本（此方式不安全）
password – 当 password 没有设定，在恢复时要求输入当前管理员的密码，当 password 被设定，密码输入则替换为当前设置密码。

#### 二进制方式备份

![image-20230923122133376](images\image-20230923122133376.png)

​    

配置恢复

![image-20230923122655940](images\image-20230923122655940.png)

#### 文本配置备份

配置备份

![image-20230923123526276](images\image-20230923123526276.png)

配置恢复

![image-20230923123655043](images\image-20230923123655043.png)

### Log 日志管理

**RouterOS** 中的日志有不同的分组或项目，日志信息来至于系统各个功能的运行状态。系统默认日志存储到内存中，在**/log** 下可以查看，当系统重启或者断电后日志会丢失，如果要保存日志可以在 **system logging**里配置日志记录类型到本地磁盘。

**属性描述**

♣ message( 只读 : 文本 ) – 信息文本
♣ time( 只读 : 文本 ) – 事件的日期和时间
♣ topics( 只读 : 文本 ) – 项目信息的从属
查看本地日志，如下面可以查看到系统 info 类型的日志，如 admin 从那个 IP，通过什么方式登出设备，admin修改了什么规则等：

![image-20230923123954080](images\image-20230923123954080.png)

### Logging 日志管理

**logging** 是用于管理各项 **RouterOS** 的系统运行和 **debug** 记录日志，即 **logging** 是用于管理在**/log** 显示和存储日志内容信息的方式，日志可以用于系统分析和故障排查。

操作路径: **/system logging**

**属性描述**

**action** ( 名称 ; 默认: **memory**) – 用户可选择在**/system logging action** 指定操作的类型

**prefix** ( 文本 ) – 本地日志前缀

**topics (info | critical | firewall | keepalive | packet | read | timer | write | ddns | hotspot | l2tp |ppp | route | update |**

**account | debug | ike | manager | pppoe | script | warning | async | dhcp | notification | pptp | state | watchdog | bgp | error |**

**ipsec | RADIUS | system | web-proxy | calc | event | isdn | ospf | raw | telephony | wireless | e-mail | gsm | mme | ntp | open |**

**ovpn | pim | radvd | rip | sertcp | ups; 默认: info)** – 指定日志组或者日志信息类型。

默认情况下日志是被存储在内存中，我们进入**/system logging**查看，默认的进行日志类型**action**都是**memory**，即存储在内容，当路由器重启后会自动清除。

![image-20230923131743517](images\image-20230923131743517.png)

为保证日志内被存储下来，并导出用于分析，可设置日志存在到本地磁盘中，我们将 **info** 日志类型设置**action=disk**，即存储在本地磁盘，配置如下：

![image-20230923131802544](images\image-20230923131802544.png)

我们可以在 **RouterOS /files** 目录下找到 **log.0.txt** 文件，该文件可以通过 **winbox** 或者 **ftp** 下载

![image-20230923131825557](images\image-20230923131825557.png)

默认日志记录中，只有 **info、error、warnimg、critical** 等 4 种日志类型，我们可以通过手动添加方式，将 **firewall**日志记录到 **log** 中，下面是在**logging** 中添加 **firewall** 产生的日志信息，并存储到系统内存中。

![image-20230923131854674](images\image-20230923131854674.png)

# 四 防火墙应用

在 RouterOS 通过 ip firewall filter 能对 IP 数据包、P2P 协议、源和目标 IP、端口、IP 协议、协议（ICMP、TCP、MSS 等）、网络接口,对内部的数据包和连接作标记、ToS 字节、关键内容、时间控制和包长度进行过滤控制

RouterOS 是基于 iptables，如果你熟悉 linux 的 iptables 操作，那 RouterOS 防火墙就能很快上手，RouterO 的防火墙规则从数据包来源方向上分类：分为 input、foreward 和 output 三种链表（chain）过滤，不管是二层或者三层过滤上都包含这三个链表。RouterOS 的防火墙包括了对address-list 和 L7-protocol 等调用。

 添加一条 firewall 规则，将所有通过路由器到目标协议为 TCP 端口为 135 的数据包全部丢弃掉：

![9-01.png](images\9-01.png)

 拒绝通过 Telnet 访问路由器(协议 TCP, 端口 23)：

![image-20230926202838412](images\image-20230926202838412.png)

### Firewall 过滤

网络防火墙始终保持对那些有威胁敏感的数据进入内部网络中，无论怎样网络都是连接在一起的，总是会有某些从外闯入你的 LAN，窃取资料和破坏内部网络，同时也根据网络管理员的要去配置 ACL，适当的配置防火墙可以有效的保护网络。

**基本过滤规则**

防火墙操作是借助于防火墙的策略，一个策略规则是告诉路由器如何处理一个 IP 数据包，每一条策略都由两部分组成，一部份是传输状态配置和定义如何操作数据包。数据链（Chains）是为更好的管理和组织策略。

滤功能有三个默认的数据链（chains）：input, forward 和 output 他们分别负责从哪里进入路由器的、通过路由器转发的与从路由器发出的数据。用户也可用自定义添加链，当然这些链没有默认的传输配置，需要在三条默认的链中对 action=jump 策略中相关的 jump-target 进行配置。

**过滤链**

下面是三条预先设置好了的 chains，他们是不被能删除的：

 input – 用于处理进入路由器的数据包，即数据包目标 IP 地址是到达路由器一个接口的 IP 地址，经过路由器的数据包不会在 input-chains 处理。

forward – 用于处理通过路由器的数据包

output – 用于处理源于路由器并从其中一个接口出去的数据包。

IP 数据包进入 input 链表的数据工作流程，阴影部分代表经过的处理部件：



![9-03.png](images\sddfsadfsf)



IP 数据包进入 output 链表的流程，阴影部分代表经过的处理部件：

![9-04.png](images\9-04.png)

IP 数据进入 forward 链表的流程，阴影部分代表经过的处理部件



![9-05.png](images\9-05.png)

**规则条件执行**

RouterOS 防火墙规则构成是 if – then 的方式：if=（条件）then action=（执行），通过前面的各种 条件参数定义规则，最后选择执行方式

![16.1.png](images\16.1.png)



**基本配置事例**

添加一条 firewall 规则，将所有通过路由器到目标协议为 TCP，端口为 445 和 135 的数据包丢弃掉：

![16.2.png](images\16.2.png)

拒绝通过 Telnet 访问路由器(协议 TCP, 端口 23)：

进入 ip firewall filter 中，选择 chain=forward 链表，设置内网源地址为 192.168.0.11，action=drop

![16.4.png](images\16.4.png)

如何访问目标 IP 地址

进入 ip firewall filter 中，选择 chain=forward 链表，创建禁止访问目标 IP 地址.8.8.8.8，设置 action=drop

![16.5.png](images\16.5.png)



### Input 事例

![9-10.png](images\9-10.png)

从 input 链表的第一条开始执行，这里一共有 7 条规则，配置命令如下：

![9-41.png](images\9-41.png)

### Forward 事例

Input 是对进入路由器方向数据处理，即 input 的作用更多的是在为保护路由器做配置，而 forward 链表，则是在对由外向内或由内向外的一种过滤方式

forward 链表，一共有 4 条规则，包括两个跳转到自定义链表 ICMP 和 virus 链表：

![9-13.png](images\9-13.png)

forward 规则仍然包含了丢弃非法数据包和 ICMP，也是我们常见的基本配置，在后面我们增加了一个自定义的病毒过滤链表 virus，在这个表里面包含了常见的或及时发现的一些入侵端口或应用协议

![9-14.png](images\9-14.png)

最后一条规则是“限制每个主机 TCP/UDP 连接数为 150 条”，这里我们可以和前面的 input 规则定义的“限制所有 TCP 连接数为 10”，限制连接数，设置的是 connection-limit 这个参数，我们可以对比下这两条规则的配置。

![9-1111.jpg](images\9-1111.jpg)

限制所有 TCP 连接数为 10：

![9-16.png](images\9-16.png)

限制每个主机 TCP/UDP 连接数为 150 条:

![9-17.png](images\9-17.png)

从这两条规则对比出，限制所有主机连接数 connection-limit=20,0，而限制每个主机connection-limit=150,32，即每个主机用 32 表示，所有主机用 0 表示。

### Jump 规则的使用

在 filter 规则总我们多次使用到 jump 指令，该指令可以让我们将指定的数据转向我们自定义的链表中，进行过滤，下面我们举例 forward 链表中通过 jump

![9-18.png](images\9-18.png)

在 winbox 中 jump 的设置

![9-19.png](images\9-19.png)

虽然我们可以一次将所有规则在 forward 或 input 等链表中配置，但对于分类管理和查找非常不便，Jump 操作让我们可以将各类过滤规则分类，如我们企业网络，可以将员工 IP 地址段和经理 IP 地址段区分开；在校园网络可以将学生 IP 段和教师 IP 段分开；在 ISP 网络中可以将应用数据进行特点分类等等…

例如我们定义一个 classes 分类的过滤链表，下面是通过 winbox 配置，我们对学生的 ip 地址段192.168.10.0/24 进行分类跳转：

![9-20.png](images\9-20.png)

设置 action 为 jump，jump-target 用于指定链表，也可以用于创建一个新链表，这里取名 classes

![9-21.png](images\9-21.png)



这样我们可以进入 classes 里设置所需的规则，由于 jump 规则已经选择了 192.168.10.0/24 的用户地址，在classes 链表中，我们无需设置 src-address 的 ip地址，简化了配置。

![9-22.png](images\9-22.png)



通过点击下拉菜单进入 classes 链表

![9-23.png](images\9-23.png)

在自定义链表 ICMP 中，定义所有 ICMP（Internet 控制报文协议），例如：ping、traceroute、trace TTL 等。我们通过 ICMP 链表来过滤所有的 ICMP 协议，限制 ICMP 的连接数，当然根据你需要也可以拒绝掉 ICMP：

![9-24.png](images\9-24.png)



### 源IP地址与目标IP地址

通常我们拒绝一个 IP 访问或者端口访问，仅仅过滤到他源地址/端口或目标地址/端口即可，因为单向通行已经被阻断，但如果我们是先接受后丢弃的方式，就会涉及到如何判断源地址/端口和目标地址/端口，与他们在 ip firewall filter 的链表，我们先看看下面的图：

![9-31.png](images\9-31.png)



我们从该图上可以看到，内网主机192.168.10.88与web服务器218.88.88.88通信的情况，内网主机192.168.10.88向路由器请求连接，不同情况下源目标IP 地址的转变。

当主机 192.168.10.88 请求向 web 服务器 218.88.88.88 连接，这时站在 web 服务器角度而言 192.168.10.88 是源IP 地址，web 服务器目标地址，这个请求是主机发出的，通过路由器 forward 链表转发，web 服务器收到后会回应主机192.168.10.88，这时 web 服务器回应发送数据变成了 web 服务器是源地址，主机是目标地址。所以在这里要记住任何通信是双向的，而不仅只有源到目标一条链路。

如果我们在配置先接受后丢弃方式时，我们需要允许 192.168.10.88 访问路由器，其他数据都拒绝，按照之前的双向通信的原则，我们需要配置两条 accept规则，一条 drop 规则。

第一条接受 src-address=192.168.10.88

![9-32.png](images\9-32.png)

![9-33.png](images\9-33.png)

第二条规则，接受 dst-address=192.168.10.88

![9-34.png](images\9-34.png)

第三条规则，丢弃所有的数据，这里我们直接配置一条 action=drop 规则

![9-35.png](images\9-35.png)

规则如下：

![9-36.png](images\9-36.png)



脚本配置如下：

![9-37.png](images\9-37.png)

![9-38.png](images\9-38.png)



### 配置示例



![image-20230924105646115](images\image-20230924105646115.png)

input过滤器



![image-20230924105928765](images\image-20230924105928765.png)

forward 过滤器

![image-20230924113953272](images\image-20230924113953272.png)

# 五 NAT

### **两种NAT类型**

 **源 NAT 或 srcnat**. 该 NAT 类型表现为从路由器发出时替换一个数据包的源 IP 地址，即一个 NAT 路由器将发到公网的私网 IP 地址替换为路由器的公网 IP，同样反向的操作也可以应用于内网方向。地址代替了其私有源地址。相反的操作适用于响应包从相反方向通过路由器时。

 **目标 NAT 或 dstnat**. 该 NAT 类型表现为从进入路由器时替换一个数据包的目标 IP 地址，即一个 NAT 路由器从公网访问路由器的 IP 替换为内网访问私网地址。

基于 iptables 的 RouterOS 是按照目的地址来选择的，因此 dst-nat 是在 PREROUTING 链表上进行的，而src-nat 是在数据包发送出去的时候才进行，因此是在 POSTROUTING 链表上进行的。当主机在一个启用 NAT 的路由器后面时，无法实现端到端的互联互通。因此一些互联网协议无法工作在 NAT 环境下。一些 TCP 协议请求连接初始化从外网到内网或者如无连接协议 UDP，可能被破坏，例如 P2P 下载和 IPsec的 AH 协议等 ，这样的问题可以通过 RouterOS 提供的 NAT Helpers 解决，NAT 透明协议。

### **Masquerade**

Nat 设置中 masquerade 一种独特的 srcnat 类型，应用于公网 IP 地址随机变动的环境，用发送数据的网卡上的 IP 来替换源 IP，例如 PPPoE 拨号动态获取 IP 和 DHCP 动态获取 IP 等每次路由器接口连接中断或 IP 地址变动，将清除发出接口的 masquerade 连接跟踪，该方式有助于尽快恢复公网 IP 地址变动

注意：选择 masquerade 后，会导致一些问题，如多线路情况下，线路中断后造成连接会话不稳定，在中断后，所有相关连接跟踪会被清除；例如线路闪断会导致会有连接跟踪会话被清楚，如果这样的情况出现在action=srcnat，中断会保存连接，如果在超时时间内恢复。

### **重定向与伪装**

重定向和伪装分别是目的 nat 和源 nat 的特殊形式。重定向类似与普通的目的网络地址翻译就好比伪装类似与源网络地址翻译——伪装是一种不需要指定 to-addresses 的源网络地址翻译的特殊形式——对外接口地址将被自动使用。重定向同理——进入接口地址将被使用。注意，to-ports 对于重定向规则来说很有意义——这就是在路由器起上处理这些请求的的服务端口。（比如：web 代理）

当数据报进行了目的网络地址翻译（dst-nat）时（不论 action=nat 或者 action=redirect），目的地址都将改变。有关地址翻译的任何信息（包括初始的目的地址）将被保存在路由器的内部维护表。当 web 请求被复位性到路由器的代理端口时，工作在路由器上的透明 web 代理将访问从内部表这个信息并从其中取得 web 服务器的地址。如果你正在对几个不同的代理服务器进行目的网络地址翻译，那你将不会从 IP 包头找到 web 服务器的地址，因为 IP 包的目的地址之前是 web 服务器的地址但现在已经变成了代理服务器的地址。从HTTP/1.1开始在 HTTP 请求中出现了特殊的可以告知 web 服务器地址的包头，于是代理服务器使用它取代了IP 包的目的地址

### 源 nat

如果你想在 ISP 给你的 10.5.8.109 地址后“隐藏”你的 192.168.0.0/24 的专用局域网，你应该使用MikroTik 路由器的源网络地址翻译特性。当数据包通过路由器时，伪装将把从 192.168.0.0/24 产生的源 IP地址和包端口改变成路由器的 10.5.8.109 地址。为了使用伪装，必须向 nat 配置中添加一个带有“隐藏”动作的的源网络地址翻译规则：

![10-02.png](images\10-02.png)

所有从 192.168.0.0/24 出去的向外连接都将使用路由器的 10.5.8.109 作为源地址，1024 作为源端口。因特网将不可能访问本地地址。如果你允许对本地网络服务器访问，你应该使用目的网络地址翻译（nat）。

RouterOS 支持两种隐藏私有网络方式，‗masquerade‘与‘src-nat‘都是改变源 IP 地址或一个数据包的端口，Masquerade 和 source nat 典型的应用都是将私有网络隐藏在一个或多个外网后，设置一个新的源地址 nat

 'masquerade'使用的是路由器默认的 IP 地址

 'src-nat'需要明确指定转换的对外 IP 地址，即‗to-address‘

![image-20230927204910335](images\image-20230927204910335.png)

### Same nat

在 srcnat 的 action 选项中，有一项 same，该规则对于中大型运营商是非常有用的，应用场景主要是当运营商给你分配了同一子网掩码的 IP 段，

你需要通过它们来对私网用户做 nat 转换，普通情况下我们用 src-nat 和masquerade 只能将私网地址转换到一个运营商 IP 地址上，但当我们从运营

商那里分配到多个或者一段 IP 地址时，我们需要使用 same 的 nat 规则，即将所以 IP 地址都应用到私网 IP 地址的 nat 转换中，由于单个 IP 的nat

端口只有 65535-1024=64511 个，但私网地址过多后，一个运营商 IP 地址端口将无法满足使用，因此需要多个运营商 IP 地址密码端口不足的情况。

例如运营商提供了 11.22.33.0/29 的 ip 地址，网关是 11.22.33.1，运营商分配可用 IP 地址为11.22.33.2-11.22.33.6

![image-20230927205027650](images\image-20230927205027650.png)

### 目标 nat

目标 nat 是常见的 nat 规则，通常端口映射、数据重定向、一对一地址映射等都会使用到目标 nat，即 dst-nat功能。

这里有一个简单的一对一地址映射事例，如你想使用公网IP地址10.5.8.200访问本地地址192.168.0.109，需要使用目标 nat 和原 nat 翻译。

![image-20230927205116729](images\image-20230927205116729.png)

#### 端口映射配置

![image-20230927205140361](images\image-20230927205140361.png)

#### dst-nat 数据转移

![image-20230927205217959](images\image-20230927205217959.png)

#### dst-nat 数据重定向

![image-20230927205240569](images\image-20230927205240569.png)

#### DNS 重定向

![image-20230927205341754](images\image-20230927205341754.png)

#### 1:1 nat 实例

![image-20230927205404131](images\image-20230927205404131.png)

在命令行里可以通过/ip firewall nat print stats 查看每条规则的状态

通过 pirnt stats 可以查看静态规则的状态

![image-20230927205442200](images\image-20230927205442200.png)

查看所有规则包括动态规则 print all stats。

![image-20230927205503239](images\image-20230927205503239.png)

仅查看动态规则 print stats dynamic

![image-20230927205522933](images\image-20230927205522933.png)

### 示例

![image-20230927205813741](images\image-20230927205813741.png)

![image-20230927205837499](images\image-20230927205837499.png)



# 六 带宽控制

### 什么是Mangle

mangle的主要作用是对数据包进行标记，以方便后续的其他模块（如nat ，路由模块）对做了标记的数据包进行处理

mangle表在5个链表中均存在，同时mangle标记仅在路由器本地生效不会传递给外部设备，也可以使用mangle对数据包头的一些字段（如ttl，mtu）进行修改

### 流量突发

流量突发是指允许在特定时间段内流量可以突发到一个比接口限定速率（在ros中称为max limit）更高的速率值

流量突发功能可以让用户在短时间内拥有比限定速率更高的带宽，可以在一定程度上提高用户网络的体验

### 带宽控制的应用场景

1. 简单队列（Simple Queue）

简单队列是对一个特定目标进行流量控制，这个target可以是一个ip地址也可以是一个或多个网段

2. 流量调整（Packet Mangling）

流量调整需要对数据包打赏标记这个过程分为两步

​    对需打标记数据包所属的网络连接进行分类

​    针对上述连接中所包含的数据包进行标记处理

3. 流量优先级（Packet Prioritiazation）

流量优先是对一些网络延时和抖动比较敏感的流量（如语音和视频流）进行优先处理，在处理完这些高优先级流量后再处理其他的低优先级流量。

再给流量进行优先级分级时，需要先使用mangle规则匹配出需要优先处理的流量对其赋予高优先级

### 带宽控制配置实例

1.简单队列

![image-20231018201932937](images\image-20231018201932937.png)

2.流量调整

![image-20231018202232883](images\image-20231018202232883.png)

![image-20231018203021659](images\image-20231018203021659.png)

3.PCQ队列

![image-20231018203204874](images\image-20231018203204874.png)

# 七 网络工具

### 带宽测速工具

BTest的局限是仅能再routeros设备间（或者安装了BTest的windows电脑）进行。 BTest的测试协议模式有TCP和UDP两种，主要区别如下：

#### Btest带宽测试中的Tcp模式

因为TCP协议本具备流量控制机制，会影响吞吐率测试的准确性。所以如果希望看到较为准确的带宽吞吐率，建议使用UDP模式。TCP模式测试时使用了整个的TCP数据流

#### Btest带宽测试中的UDP模式

UDP模式测试时计算数据包的：IP头+UDP头+UDP荷载。 TCP模式测试时计算数据包的TCP载荷不包含IP头和UDP头部信息

![image-20231018210521867](images\image-20231018210521867.png)



![image-20231019191618061](images\image-20231019191618061.png)



### 接口流量查看工具（Torch）

Torch所起的作用类似于企业级网络设备中的show interface/display interface所展示的效果，但比较起来实时性会更强

![image-20231018210532882](images\image-20231018210532882.png)

![image-20231019201718692](images\image-20231019201718692.png)

### 流量图形化显示工具（Graping）

Graphing的作用类似于网管软件所展示特定时间段内的设备流量图

![image-20231019201150967](images\image-20231019201150967.png)

![image-20231019201737654](images\image-20231019201737654.png)



### Email工具

Emali工具可以作为系统告警发送，设备配置定期备份的接收端工具

 ![image-20231023202925525](images\image-20231023202925525.png)

### Netwatch

Netwatch工具可检测接口链路的可用性，一旦所监测接口的状态为down或up，可根据接口的up和down状态执行特定的脚本任务

### Profile

profile是ROS中的资源占用查看器，可以查看系统中哪些进程占用了较多的cpu资源

 ![image-20231024195911301](images\image-20231024195911301.png)

# 八 局域网

### 1 ARP

静态arp

默认情况下路由器的arp表项为动态学习获得的，如果处于管理或安全方面的考虑，可以将路由器中的一些ip地址设置为静态方式，也把这种方式成为arp绑定

arp的reply only模式

处于这种模式下的接口只会回应收到的arp请求，接口本身不会往外部发arp请求，在这种模式下路由器中也不会存在arp动态表项，要让设备正常工作只能依赖设备中的静态表项

![image-20231023201851212](images\image-20231023201851212.png)

![image-20231023202354473](images\image-20231023202354473.png)

### 2 DNS

可以将mikotik路由设备设为本地的dns服务器，前提条件是需要在路由器dns合作中打开远程dns请求功能（默认关闭）

![image-20231023201931789](C:\Users\cs1\AppData\Roaming\Typora\typora-user-images\image-20231023201931789.png)

![image-20231023202415321](images\image-20231023202415321.png)

### 3 DHCP

miikotik路由器本身即可作为DHCP客户端也可以作为DHCP服务器，ros的DHCP服务器配置稍复杂，在三个地方需要配置

* 在IP -> pool中创建地址池

  地址池中包含分配给客户端的ip地址，没有网关/DNS等信息

* 在IP—>dhcp server的network页中创建dhcp网络信息

  其中包含了网段地址，网关，DNS等信息

* 在IP->dhcp server 的network页中创建dhcp网段信息

  其中包含了哪个接口开启dhcp，同时在此引用第一步中的地址池

![image-20231023202113961](images\image-20231023202113961.png)

![image-20231023202445942](images\image-20231023202445942.png)

### 4 Hotspot热点

热点功能类同于国内的认证网关产品，让用户在无线/有线上网环境下需提供认证信息才能上网，从而进一步对用户进行认证/计费/授权管理

![image-20231023202206446](images\image-20231023202206446.png)

### 5 web代理

ROS支持传统的http proxy代理功能，也支持socket代理，其他主流厂家路由器/防火墙直接支持http代理的很少，这算是ROS的一个特色功能

![image-20231023202240463](images\image-20231023202240463.png)