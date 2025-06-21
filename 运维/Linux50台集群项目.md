一、环境搭建

## 1、环境规划

| **架构组成**      | **数量** | **作用说明**                                                 |
| ----------------- | :------: | ------------------------------------------------------------ |
| 负载均衡服务器    |   两台   | 对访问网站的流量进行分流，减少流量对某台服务器的压力         |
| Web服务器         |   三台   | 处理用户页面访问请求                                         |
| NFS存储服务器     |   一台   | 存储图片、附件、头像等用户上传的静态数据资源                 |
| Rsync备份服务器   |   一台   | 对全网服务器数据进行实时与定时备份                           |
| MySQL数据库服务器 |   一台   | 对动态变化数据进行存储(文本内容)                             |
| 管理服务器        |   一台   | 1、作为yum仓库服务器，提供全网服务器的软件下载  2、跳板机、操作审计  3、vpn(pptp)  4、监控(nagios,zabbix)  5、兼职批量分发和管理（ssh key+ansible） |

| **服务器说明**  | **外网**IP（NAT） | **内网IP（LAN区段）** | **主机名称** |
| --------------- | ----------------- | --------------------- | ------------ |
| nginx负载服务器 | 10.0.0.5/24       | 172.16.1.5/24         | lb01         |
| nginx负载服务器 | 10.0.0.6/24       | 172.16.1.6/24         | lb02         |
| Nginx网站服务器 | 10.0.0.7/24       | 172.16.1.7/24         | web01        |
| Nginx网站服务器 | 10.0.0.8/24       | 172.16.1.8/24         | web02        |
| Nginx网站服务器 | 10.0.0.9/24       | 172.16.1.9/24         | web03        |

| **服务器说明**    | **外网IP（NAT）** | **内网IP（LAN**区段）** | **主机名称** |
| ----------------- | ----------------- | ----------------------- | ------------ |
| MySQL数据库服务器 | 10.0.0.51/24      | 172.16.1.51/24          | db01         |
| NFS存储服务器     | 10.0.0.31/24      | 172.16.1.31/24          | nfs01        |
| Rsync备份服务器   | 10.0.0.41/24      | 172.16.1.41/24          | backup       |
| 管理服务器        | 10.0.0.61/24      | 172.16.1.61/24          | m01          |

## 2、虚拟软件主机虚拟网络配置

第一步：在虚拟软件中配置虚拟局域网
配置虚拟网段信息，以及虚拟网关信息

第二步：在虚拟软件中虚拟机添加网卡
虚拟主机中设置了两块网卡：
eth0：nat模式网卡
eth1：LAN区段网卡（区段名称为 172.16.1.0/24）

第三步：在虚拟软件中虚拟机网卡配置

第四步：在虚拟软件中虚拟机系统优化

```bash
cp /etc/hosts{,.bak}
cat >/etc/hosts<<EOF
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
172.16.1.5      lb01
172.16.1.6      lb02
172.16.1.7      web01
172.16.1.8      web02
172.16.1.9      web03
172.16.1.51     db01
172.16.1.31     nfs01
172.16.1.41     backup
172.16.1.61     m01
EOF
```

模板机优化配置---更改yum源

```bash
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-6.repo
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-6.repo
#PS：yum repolist 列出yum源信息；讲解什么是epel源

```

模板机优化配置---关闭selinux

```bash
#关闭selinux
sed -i.bak 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
grep SELINUX=disabled /etc/selinux/config 
setenforce 0
getenforce
```

模板机优化配置---关闭iptables

```bash
#关闭iptables         
/etc/init.d/iptables stop
/etc/init.d/iptables stop
chkconfig iptables off
```

模板机优化配置---精简开机自启动服务

```bash
#精简开机自启动服务
export LANG=en
chkconfig|egrep -v "crond|sshd|network|rsyslog|sysstat"|awk '{print "chkconfig",$1,"off"}'|bash
chkconfig --list|grep 3:on
```

模板机优化配置---英文字符集

```bash
#英文字符集
cp /etc/sysconfig/i18n /etc/sysconfig/i18n.ori
echo 'LANG="en_US.UTF-8"'  >/etc/sysconfig/i18n 
source /etc/sysconfig/i18n
echo $LANG
```

模板机优化配置---时间同步

```bash
echo '#time sync by lidao at 2017-03-08' >>/var/spool/cron/root
echo '*/5 * * * * /usr/sbin/ntpdate pool.ntp.org >/dev/null 2>&1' >>/var/spool/cron/root
crontab -l
```

模板机优化配置---加大文件描述

```bash
#加大文件描述
echo '*               -       nofile          65535 ' >>/etc/security/limits.conf 
tail -1 /etc/security/limits.conf 
```

模板机优化配置---内核优化

```bash
cat >>/etc/sysctl.conf<<EOF
net.ipv4.tcp_fin_timeout = 2
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_tw_recycle = 1
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_keepalive_time = 600
net.ipv4.ip_local_port_range = 4000    65000
net.ipv4.tcp_max_syn_backlog = 16384
net.ipv4.tcp_max_tw_buckets = 36000
net.ipv4.route.gc_timeout = 100
net.ipv4.tcp_syn_retries = 1
net.ipv4.tcp_synack_retries = 1
net.core.somaxconn = 16384
net.core.netdev_max_backlog = 16384
net.ipv4.tcp_max_orphans = 16384
#以下参数是对iptables防火墙的优化，防火墙不开会提示，可以忽略不理。
net.nf_conntrack_max = 25000000
net.netfilter.nf_conntrack_max = 25000000
net.netfilter.nf_conntrack_tcp_timeout_established = 180
net.netfilter.nf_conntrack_tcp_timeout_time_wait = 120
net.netfilter.nf_conntrack_tcp_timeout_close_wait = 60
net.netfilter.nf_conntrack_tcp_timeout_fin_wait = 120
EOF
sysctl -p
```

模板机优化配置---安装其他小软件

```bash
#安装其他小软件
yum install lrzsz nmap tree dos2unix nc telnet sl -y
```

模板机优化配置---ssh连接速度慢优化

```bash
#ssh连接速度慢优化          
sed -i.bak 's@#UseDNS yes@UseDNS no@g;s@^GSSAPIAuthentication yes@GSSAPIAuthentication no@g'  /etc/ssh/sshd_config
/etc/init.d/sshd reload
```

## 3、虚拟主机克隆

第一步：调整虚拟主机网络配置信息
	         一清空 两删除
            两删除：删除网卡（eth0 eth1）中，UUID（硬件标识信息）和HWADDR（网络mac地址）进行删除
			sed -ri '/UUID|HWADDR/d'  /etc/sysconfig/network-scripts/ifcfg-eth[01]
			一清空：清空网络规则配置文件
			echo '>/etc/udev/rules.d/70-persistent-net.rules' >>/etc/rc.local 

第二步：关闭虚拟模板机
shutdown -h now

第三步：进行模板机的克隆操作
	链接克隆：
	优势：节省系统资源  克隆效率较高
	劣势：模板主机不能出现问题，一旦模板主机失效，所有克隆主机也无法正常工作
	完整克隆：
	优势：模板主机和克隆主机相互独立，模板主机出现问题，克隆主机依旧可以正常使用
	劣势：浪费系统资源  克隆效率较低

第四步：开启克隆后虚拟主机（一台一台开启，确认模板主机关闭），设置虚拟主机地址和网卡

​	hostname backup
​	sed -i "s#主机名称#backup#g" /etc/sysconfig/network
​	说明：主机名称需要填写为当前系统主机名，然后进行一下替换即可

# 二 备份服务

rsync官方网站: https://www.samba.org/ftp/rsync/rsync.html

rsync是可以实现增量备份的工具。配合任务计划，rsync能实现定时或间隔同步，配合inotify或sersync，可以实现触发式的实时同步。

rsync可以实现scp的远程拷贝(rsync不支持远程到远程的拷贝，但scp支持)、cp的本地拷贝、rm删除和"ls -l"显示文件列表等功能。但需要注意的是，rsync的最终目的或者说其原始目的是实现两端主机的文件同步，因此实现的scp/cp/rm等功能仅仅只是同步的辅助手段，且rsync实现这些功能的方式和这些命令是不一样的。事实上，rsync有一套自己的算法，其算法原理以及rsync对算法实现的机制可能比想象中要复杂一些。平时使用rsync实现简单的备份、同步等功能足以，没有多大必要去深究这些原理性的内容。但是想要看懂rsync命令的man文档、使用"-vvvv"分析rsync执行过程，以及实现rsync更强大更完整的功能，没有这些理论知识的支持是绝对不可能实现的。本篇文章将简单介绍rsync的使用方法和它常用的功能

## 1、rsync服务命令简单应用

copy效果

```bash
[root@backup ~]# # rsync == cp效果
[root@backup ~]# cp -a /etc/hosts /tmp/
[root@backup ~]# ll /tmp/
total 4
-rw-r--r--. 1 root root 352 Jan 27 01:15 hosts
[root@backup ~]# rsync -a /etc/sysconfig/network /tmp/
[root@backup ~]# ll /tmp/
total 8
-rw-r--r--. 1 root root 352 Jan 27 01:15 hosts
-rw-r--r--  1 root root  31 Jan 26 18:16 network
```

scp

```bash
[root@backup ~]# scp -rp /tmp/ 172.16.1.31:/tmp/
    The authenticity of host '172.16.1.31 (172.16.1.31)' can't be established.
    RSA key fingerprint is 5b:9b:e6:79:a9:95:4f:be:06:41:e3:bb:7a:12:ee:b4.
    Are you sure you want to continue connecting (yes/no)? yes
    Warning: Permanently added '172.16.1.31' (RSA) to the list of known hosts.
    root@172.16.1.31's password: 
    network                                                                                                                              100%   31     0.0KB/s   00:00    
    hosts                                                                                                                                100%  352     0.3KB/s   00:00    
[root@backup ~]# ll /tmp/
    total 8
    -rw-r--r--. 1 root root 352 Jan 27 01:15 hosts
    -rw-r--r--  1 root root  31 Jan 26 18:16 network
[root@backup ~]# rsync -rp /tmp/ 172.16.1.31:/tmp/
    root@172.16.1.31's password: 

```

说明：同步数据时，/tmp/目录后有/信息，表示将目录下面的数据内容进行备份同步
      	  同步数据时，/tmp目录后没有/信息，表示将目录及目录下面的数据内容进行备份同步

rm

说明：rsync实现删除目录中数据内容过程，就将一个空目录和一个有数据的目录进行同步最终，会将有数据的目录中的文件进行清空

```bash
[root@backup ~]# mkdir /null
[root@backup ~]# rsync --delete /null/ /tmp/
rsync: --delete does not work without -r or -d.
rsync error: syntax or usage error (code 1) at main.c(1422) [client=3.0.6]
[root@backup ~]# 
[root@backup ~]# rsync -r --delete /null/ /tmp/
[root@backup ~]# ll /tmp/
total 0
```

ls

```bash
[root@backup ~]# ls /etc/hosts
/etc/hosts
[root@backup ~]# ls -l /etc/hosts
-rw-r--r--. 2 root root 352 Jan 27 01:15 /etc/hosts
[root@backup ~]# rsync /etc/hosts
-rw-r--r--         352 2018/01/27 01:15:59 hosts
```

## 2、rsync软件工作方式

### 本地数据备份方式

   Local:  rsync [OPTION...] SRC... [DEST]
   rsync    --- 数据备份传输命令
   option   --- 可以输入一下和rsync传输数据有关的参数
   src      --- 要进行备份的数据（文件/目录）
   dest     --- 将数据信息备份到什么位置（相应路径中）

```bash
   实践练习：
   [root@backup ~]# rsync -a /etc/hosts /tmp/ok.txt
   [root@backup ~]# ll /tmp/ok.txt 
   -rw-r--r-- 1 root root 352 Jan 27 01:15 /tmp/ok.txt
```

### 远程数据备份方式

   Access via remote shell:
         Pull: rsync [OPTION...] [USER@]HOST:SRC... [DEST]
         Push: rsync [OPTION...] SRC... [USER@]HOST:DEST

   pull方式语法说明：
   rsync    --- 数据备份传输命令
   option   --- 可以输入一下和rsync传输数据有关的参数
   [USER@]HOST:     --- 需要指定以什么用户身份登录到远程主机，
                        如果省略USER信息，表示以当前用户身份进行登录
						登录主机地址或域名信息
   SRC      --- 指定远程主机要传输过来到本地的数据信息
   dest     --- 将数据保存到本地的什么路径中

 push方式语法说明：
   rsync    --- 数据备份传输命令
   option   --- 可以输入一下和rsync传输数据有关的参数
   [USER@]HOST:     --- 需要指定以什么用户身份登录到远程主机，
                        如果省略USER信息，表示以当前用户身份进行登录
						登录主机地址或域名信息
   SRC      --- 指定本地主机要传输到远程主机的数据
   dest     --- 将本地数据保存到远端的什么路径中

![image-20200924214600728](images\image-20200924214600728.png)

### 守护进程传输模式

   Access via rsync daemon:
         Pull: rsync [OPTION...] [USER@]HOST::SRC... [DEST]
               rsync [OPTION...] rsync://[USER@]HOST[:PORT]/SRC... [DEST]
         Push: rsync [OPTION...] SRC... [USER@]HOST::DEST
               rsync [OPTION...] SRC... rsync://[USER@]HOST[:PORT]/DEST

```bash
pull：rsync [OPTION...] [USER@]HOST::SRC... [DEST]
[USER@]HOST::       --- 指定远程连接的认证用户
SRC                 --- 指定相应的模块信息
[DEST]              --- 将远程数据保存到本地的路径信息
```

```bash
Push: rsync [OPTION...] SRC... [USER@]HOST::DEST
	[USER@]HOST::       --- 指定远程连接的认证用户
	SRC                 --- 指定本地要进行推送的数据信息
	[DEST]              --- 远程进行保存数据的模块信息
```

### rsync守护进程部署流程

(1) 检查软件是否安装

```bash
[root@backup ~]# rpm -qa rsync
rsync-3.1.2-10.el7.x86_64
```

(2) 编写配置文件

```bash
vim /etc/rsyncd.conf
```

```
uid = rsync              # 指定rsync服务运行的时候，向磁盘进行读取和写入操作的操作者
gid = rsync 	         # 指定rsync服务运行的时候，向磁盘进行读取和写入操作的操作者
use chroot = no          # 进行数据同步存储时，安全相关参数，默认内网进行数据同步，可以关闭
max connections = 200    # 定义向备份服务器进行数据存储的并发连接数
pid file = /var/run/rsyncd.pid   # 服务程序运行时，会将进程的pid信息存储到一个指定的pid文件中
lock file = /var/run/rsync.lock  # 定义锁文件，主要用于配合max connections 参数，当达到最大连接就禁止继续访问
log file = /var/log/rsyncd.log   # 定义服务的日志文件保存路径信息
ignore errors					 # 在进行数据备份传输过程过程中，忽略一些I/O产生的传输错误
read only = false				 # 设置对备份的目录的具有读写权限，即将只读模式进行关闭
hosts allow = 172.16.1.0/24 	 # 设置备份目录允许进行网络数据备份的主机地址或网段信息，即设置白名单
hosts deny = 0.0.0.0/32			 # 设置备份目录禁止进行网络数据备份的主机地址或网段信息，即设置黑名单
auth users = rsync_backup       # 指定访问备份数据目录的认证用户信息，为虚拟定义的用户，不需要进行创建

secrets file = /etc/rsync.password  设置访问备份数据目录进行认证用户的密码文件信息，会在文件中设置认证用户密码信息
[backup]					      # 指定备份目录的模块名称信息
comment = "backup dir by oldboy"   
path = /backup
read only = true
[nfs]
comment = "backup dir by oldboy"
path = /nfs
timeout = 200            # 定义与备份服务器建立的网络连接，在多长时间没有数据传输时，就释放连接
```

（3） 创建备份目录管理用户

```bash
[root@backup ~]# useradd rsync -M -s /sbin/nologin
```

  (4)  创建备份目录

```bash
[root@backup ~]# mkdir /backup
[root@backup ~]# chown -R rsync:rsync /backup
```

 (5)  创建认证文件

```bash
[root@backup ~]# echo "rsync_backup:cs1993413" >> /etc/rsync.password
[root@backup ~]# chmod 600 /etc/rsync.password
```

 (6) 启动rsync服务

```bash
[root@backup ~]# rsync --daemon
```

### rsync守护进程客户端

```bash
[root@nfs /]# rpm -qa rsync
rsync-3.1.2-10.el7.x86_64
```

```bash
[root@nfs /]# echo "cs1993413" >> /etc/rsync.password
```

```bash
[root@nfs /]# rsync -rltDvz /etc/hosts rsync_backup@172.16.0.41::backup --password-file=/etc/rsync.password
```

## 3、Rsync服务常见问题汇总

### rsync服务端开启的iptables防火墙

  【客户端的错误】
   No route to host
  【错误演示过程】
   [root@nfs01 tmp]# rsync -avz /etc/hosts rsync_backup@172.16.1.41::backup
   rsync: failed to connect to 172.16.1.41: No route to host (113)
   rsync error: error in socket IO (code 10) at clientserver.c(124) [sender=3.0.6]
  【异常问题解决】
   关闭rsync服务端的防火墙服务（iptables）
   [root@backup mnt]# /etc/init.d/iptables stop
   iptables: Setting chains to policy ACCEPT: filter          [  OK  ]
   iptables: Flushing firewall rules:                         [  OK  ]
   iptables: Unloading modules:                               [  OK  ]
   [root@backup mnt]# /etc/init.d/iptables status
   iptables: Firewall is not running.

### rsync客户端执行rsync命令错误

 【客户端的错误】
   The remote path must start with a module name not a / 
  【错误演示过程】
   [root@nfs01 tmp]# rsync -avz /etc/hosts rsync_backup@172.16.1.41::/backup
   ERROR: The remote path must start with a module name not a /
   rsync error: error starting client-server protocol (code 5) at main.c(1503) [sender=3.0.6]
  【异常问题解决】
   rsync命令语法理解错误，::/backup是错误的语法，应该为::backup(rsync模块)

### rsync服务认证用户失败

  【客户端的错误】
   auth failed on module oldboy
  【错误演示过程】
   [root@nfs01 tmp]# rsync -avz /etc/hosts rsync_backup@172.16.1.41::backup
   Password: 
   @ERROR: auth failed on module backup
   rsync error: error starting client-server protocol (code 5) at main.c(1503) [sender=3.0.6]
  【异常问题解决】

      1. 密码真的输入错误，用户名真的错误
      2. secrets file = /etc/rsync.password指定的密码文件和实际密码文件名称不一致
      3. /etc/rsync.password文件权限不是600
      4. rsync_backup:123456密码配置文件后面注意不要有空格
      5. rsync客户端密码文件中只输入密码信息即可，不要输入虚拟认证用户名称

### rsync服务位置模块错误

  【客户端的错误】
   Unknown module 'backup'   
  【错误演示过程】  
   [root@nfs01 tmp]# rsync -avz /etc/hosts rsync_backup@172.16.1.41::backup
   @ERROR: Unknown module 'backup'
   rsync error: error starting client-server protocol (code 5) at main.c(1503) [sender=3.0.6]
  【异常问题解决】

      1. /etc/rsyncd.conf配置文件模块名称书写错误

### rsync服务权限阻止问题

  【客户端的错误】
   Permission denied
  【错误演示过程】 
   [root@nfs01 tmp]# rsync -avz /etc/hosts rsync_backup@172.16.1.41::backup
   Password: 
   sending incremental file list
   hosts
   rsync: mkstemp ".hosts.5z3AOA" (in backup) failed: Permission denied (13) 
   sent 196 bytes  received 27 bytes  63.71 bytes/sec
   total size is 349  speedup is 1.57
   rsync error: some files/attrs were not transferred (see previous errors) (code 23) at main.c(1039) [sender=3.0.6]   
  【异常问题解决】

      1. 备份目录的属主和属组不正确，不是rsync
      2. 备份目录的权限不正确，不是755

### rsync服务备份目录异常

  【客户端的错误】
   chdir failed   
  【错误演示过程】   
   [root@nfs01 tmp]# rsync -avz /etc/hosts rsync_backup@172.16.1.41::backup
   Password: 
   @ERROR: chdir failed
   rsync error: error starting client-server protocol (code 5) at main.c(1503) [sender=3.0.6]
  【异常问题解决】  

      1. 备份存储目录没有建立
      2. 建立的备份存储目录和配置文件定义不一致
         说明：如果没有备份存储目录

### rsync服务无效用户信息

  【客户端的错误】
   invalid uid rsync
  【错误演示过程】    
   [root@nfs01 tmp]# rsync -avz /etc/hosts rsync_backup@172.16.1.41::backup
   Password: 
   @ERROR: invalid uid rsync
   rsync error: error starting client-server protocol (code 5) at main.c(1503) [sender=3.0.6]
  【异常问题解决】  
   rsync服务对应rsync虚拟用户不存在了

### 客户端已经配置了密码文件，但免秘钥登录方式，依旧需要输入密码

  【客户端的错误】
   password file must not be other-accessible
  【错误演示过程】 
   [root@nfs01 tmp]# rsync -avz /etc/hosts rsync_backup@172.16.1.41::backup --password-file=/etc/rsync.password
   password file must not be other-accessible
   continuing without password file
   Password: 
   sending incremental file list
   sent 26 bytes  received 8 bytes  5.23 bytes/sec
   total size is 349  speedup is 10.26
  【异常问题解决】  
   rsync客户端的秘钥文件也必须是600权限

### rsync客户端连接慢问题

   IP   ===  域名    反向DNS解析
  【错误日志信息】 
   错误日志输出
   2017/03/08 20:14:43 [3422] params.c:Parameter() - Ignoring badly formed line in configuration file: ignore errors
   2017/03/08 20:14:43 [3422] name lookup failed for 172.16.1.31: Name or service not known
   2017/03/08 20:14:43 [3422] connect from UNKNOWN (172.16.1.31)
   2017/03/08 20:14:43 [3422] rsync to backup/ from rsync_backup@unknown (172.16.1.31)
   2017/03/08 20:14:43 [3422] receiving file list
   2017/03/08 20:14:43 [3422] sent 76 bytes  received 83 bytes  total size 349
   正确日志输出
   2017/03/08 20:16:45 [3443] params.c:Parameter() - Ignoring badly formed line in configuration file: ignore errors
   2017/03/08 20:16:45 [3443] connect from nfs02 (172.16.1.31)
   2017/03/08 20:16:45 [3443] rsync to backup/ from rsync_backup@nfs02 (172.16.1.31)
   2017/03/08 20:16:45 [3443] receiving file list
   2017/03/08 20:16:45 [3443] sent 76 bytes  received 83 bytes  total size 349
  【异常问题解决】
   查看日志进行分析，编写rsync服务端hosts解析文件

### rsync服务没有正确启动

  【错误日志信息】 
   Connection refused (111)
  【错误演示过程】 
   [root@oldboy-muban ~]#  rsync -avz /etc/hosts rsync_backup@172.16.1.41::backup
   rsync: failed to connect to 172.16.1.41: Connection refused (111)
   rsync error: error in socket IO (code 10) at clientserver.c(124) [sender=3.0.6]
  【异常问题解决】
   [root@oldboy-muban ~]# rsync --daemon
   [root@oldboy-muban ~]# ss -lntup |grep rsync
   tcp    LISTEN     0      5                     :::873                  :::*      users:(("rsync",1434,5))
   tcp    LISTEN     0      5                      *:873                   *:*      users:(("rsync",1434,4))
   [root@oldboy-muban ~]# rsync -avz /etc/hosts rsync_backup@172.16.1.41::backup
   Password: 
   sending incremental file list
   hosts  
   sent 196 bytes  received 27 bytes  49.56 bytes/sec
   total size is 349  speedup is 1.57

# 三、NFS网络文件共享

## 1、NFS简介 

​      NFS 是 Network File System 的缩写，中文意思是网络文件系统。它的主要功能是通过网络（一 般是局域网）让不同的主机系统之间可以共享文件或目录。NFS 客户端（一般为应用服务器，例如 web）可以通过挂载（mount）的方式将 NFS 服务器端共享的数据目录挂载到 NFS 客户端本地系统 中（就是某一个挂载点下）。从客户端本地看，NFS 服务器端共享的目录就好像是客户端自己的磁 盘分区或者目录一样，而实际上却是远端的 NFS 服务器的目录。 

实现共享存储好处：

​	实现数据统一致

​	节省网站磁盘资源

​	节省网站访问带宽

​    NFS共享存储服务的原理：
​       ①. nfs服务端创建共享存储目录
​       ②. nfs客户端创建远程挂载点目录
​       ③. nfs客户端进行远程挂载
​       ④. 实现客户端数据信息统一一致

## 2、NFS系统原理介绍

​      在 NFS 服务器端设置好一个共享目录/video 后，其他有权限访问 NFS 服务器 端的客户端都可以将这个共享目录/video 挂载到客户端本地的某个挂载点（其实就是一个目录，这 个挂载点目录可以自己随意指定），配置两个 NFS 客户端本地的挂载点分别为/v/video 和 /video，不同客户端的挂载点可以不相同

​      客户端正确挂载完毕后，就进入到了 nfs 客户端的挂载点所在的/v/video 或/video 目录，此时就 可以看到 NFS 服务器端/video 共享出来的目录下的所有数据。在客户端上查看时，NFS 服务器端的 /video 目录就相当于客户端本地的磁盘分区或目录，几乎感觉不到使用上的区别，根据 NFS 服务端 授予的 NFS 共享权限以及共享目录的本地系统权限，只要在指定的 NFS 客户端操作挂载/v/video 或 /video 的目录，就可以将数据轻松地存取到 NFS 服务器端上的/video 目录中了

提示：mount 源 目标 

```bash
 mount 10.0.0.31:/video /app/video 

[root@nfs-client ~]# df -h 
Filesystem            Size  Used Avail Use% Mounted on 
/dev/sda1             1.1T  467G  544G  47% / 
tmpfs                 7.9G     0  7.9G   0% /dev/shm 
10.0.0.7:/video       1002G   59G  892G   7% /app/video  #<==10.0.0.7 为 nfs server 的 ip 地址 
```

我们知道 NFS 系统是通过网络来进行数据传输的（所以叫做网络文件系统 嘛！），因此，NFS 会使用一些端口来传输数据，那么，NFS 到底使用什么方式来进行数据传输呢？ 答案就是通过 RPC（中文意思远程过程调用，英文 Remote Procedure Call 简称 RPC）协议/服务来实现

### RPC简介

   因为 NFS 支持的功能相当多，而不同的功能都会使用不同的程序来启动，每启动一个功能就会 启用一些端口来传输数据，因此，NFS 的功能所对应的端口无法固定，它会随机取用一些未被使用 的端口来作为传输之用

   因为端口不固定，这样一来就会造成 NFS 客户端与 NFS 服务端的通信障碍，因为 NFS 客户端 必须要知道 NFS 服务器端的数据传输端口才能进行通信，才能交互数据。 要解决上面的困扰，就需要通过远程过程调用 RPC 服务来帮忙了，NFS 的 RPC 服务最主要的 

​    功能就是记录每个 NFS 功能所对应的端口号，并且在 NFS 客户端请求时将该端口和功能对应的信 息传递给请求数据的 NFS 客户端，从而确保客户端可以连接到正确的 NFS 端口上去，达到实现数 据传输交互数据目的。这个 RPC 服务类似 NFS 服务端和 NFS 客户端之间的一个中介

### NFS 的工作流程原理 

![image-20200926115425740](D:images\image-20200926115425740.png)

当访问程序通过 NFS 客户端向 NFS 服务端存取文件时，其请求数据流程大致如下： 
	1) 首先用户访问网站程序，由程序在 NFS 客户端上发出存取 NFS 文件的请求，这时 NFS 客户
端（即执行程序的服务器）的 RPC 服务（rpcbind 服务）就会通过网络向 NFS 服务器端的 RPC
服务（rpcbind 服务）的 111 端口发出 NFS 文件存取功能的询问请求。 
	2) NFS 服务器端的 RPC 服务（rpcbind 服务）找到对应的已注册的 NFS 端口后，通知 NFS 客户
端的 RPC 服务（rpcbind 服务）。 
	3) 此时 NFS 客户端获取到正确的端口，并与 NFS daemon 联机存取数据。 
	4) NFS 客户端把数据存取成功后，返回给前端访问程序，告知给用户存取结果，作为网站用户， 	

## 3、NFS服务部署实践过程

### 服务端部署流程

检查服务软件是否安装

```bash
rpm -qa|egrep “nfs-utils|rpcbind”
```

进行软件服务安装

```bash
yum install -y nfs-utils rpcbind
```

补充说明：nfs-utils 和 rpcbind两个软件大礼包

	rpm -ql nfs-utils
	/etc/rc.d/init.d/nfs     <-- nfs服务启动脚本文件
	/usr/sbin/showmount      <-- 检查nfs服务共享目录信息
	
	rpm -ql rpcbind
	/etc/rc.d/init.d/rpcbind   <-- rpcbind服务启动脚本文件
	/usr/sbin/rpcbind          <-- 检查nfs服务向rpc服务注册信息

编写nfs服务配置文件

```bash
[root@nfs01 ~]# ll /etc/exports 
-rw-r--r-- 1 root root 30 2018-02-25 13:30 /etc/exports   <-- nfs服务配置文件，默认已经存在
[root@nfs01 ~]# vim /etc/exports 
/data  172.16.1.0/24(rw,sync)
说明：配置文件信息 指定共享目录   指定共享目录访问控制网段或主机信息(共享目录参数信息)
```

创建nfs服务共享目录，并且进行授权

```bash
mkdir /data
chown -R nfsnobody.nfsnobody /data
```

启动nfs和rpc服务

```bash
/etc/init.d/rpcbind start       <- 首先启动rpcbind服务
/etc/init.d/nfs start           <- 其次启动nfs服务
```

进行服务配置检查

先检查房源信息是否注册

```bash
rpcinfo -p 172.16.1.31
```

检查是否存在可用的共享目录

```bash
[root@nfs01 ~]# showmount -e 10.0.0.31
Export list for 10.0.0.31:
/data 172.16.1.0/24
```

### NFS客户端部署流程

检查服务软件是否安装

```bash
rpm -qa|egrep “nfs-utils|rpcbind”
```

进行软件服务安装

```bash
yum install -y nfs-utils rpcbind
```

进行共享目录挂载

```bash
[root@web02 ~]# mount -t nfs 172.16.1.31:/data /mnt
[root@web02 ~]# df -h
Filesystem         Size  Used Avail Use% Mounted on
172.16.1.31:/data  8.6G  1.9G  6.4G  23% /mnt
```

进行共享存储测试

```bash
[root@web01 mnt]# touch test.txt
[root@web01 mnt]# ls
test.txt

[root@nfs01 ~]# cd /data/
[root@nfs01 data]# ls
test.txt

[root@web02 ~]# ls /mnt
test.txt
说明：在web01的mnt目录中创建的数据，在nfs和web02服务器上都可以看到，即已经实现数据共享存储
```

### NFS服务部署进程信息详述

```bash
[root@oldboy ~]# ps -ef|egrep "rpc|nfs"
rpc        1564      1  0 09:32 ?        00:00:00 rpcbind
rpc        1065      1  0 09:32 ?        00:00:00 rpc statd		<- 检查数据存储一致性
root       4736      2  0 21:31 ?        00:00:00 [rpciod/0]
root       5363      1  0 21:47 ?        00:00:00 rpc.rquotad	<- 磁盘配额进程（remote quote server）
root       5368      1  0 21:47 ?        00:00:00 rpc.mountd	<- 权限管理验证等（NFS mount daemon）
root       5375      2  0 21:47 ?        00:00:00 [nfsd4]
root       5376      2  0 21:47 ?        00:00:00 [nfsd4_callbacks]
root       5377      2  0 21:47 ?        00:00:00 [nfsd]		<- NFS主进程
root       5378      2  0 21:47 ?        00:00:00 [nfsd] 		<- NFS主进程
root       5379      2  0 21:47 ?        00:00:00 [nfsd] 		<- NFS主进程，管理登入，ID身份判别等。
root       5380      2  0 21:47 ?        00:00:00 [nfsd]
root       5381      2  0 21:47 ?        00:00:00 [nfsd]
root       5382      2  0 21:47 ?        00:00:00 [nfsd]
root       5383      2  0 21:47 ?        00:00:00 [nfsd]
root       5384      2  0 21:47 ?        00:00:00 [nfsd]		<- NFS主进程
root       5415      1  0 21:47 ?        00:00:00 rpc.idmapd	<- name mapping daemon
                                                                用户压缩/用户映射（记录）
root       5512   4670  0 22:02 pts/0    00:00:00 egrep rpc|nfs
```

### 配置 NFS 服务端服务开机自启动 

配置 NFS 及 rpcbind 服务在系统开机或重新启动后自动运行的命令如下： 

```bash
[root@nfs-server ~]# chkconfig rpcbind on 
[root@nfs-server ~]# chkconfig nfs on 
```

下面来查看 chkconfig 设置开机启动后的结果。不同的机器可能会有中英文显示差别，可以统一设置
好英文字符集后查看

```bash
[root@nfs-server ~]# LANG=en 
[root@nfs-server ~]# chkconfig --list rpcbind 
rpcbind         0:off   1:off   2:on    3:on    4:on    5:on    6:off 
[root@nfs-server ~]# chkconfig --list nfs 
nfs             0:off   1:off   2:on    3:on    4:on    5:on    6:off 
```

下面的方法和上面相当，但是效率不如上面的命令。因为要先输出所有的，再过滤需要的，而上面
的直接查看对应服务名，更精确。 
#查看是否开机自启动

```bash
[root@nfs-server ~]# chkconfig --list|egrep "nfs|rpcbind" 
nfs             0:off   1:off   2:on    3:on    4:on    5:on    6:off 
rpcbind         0:off   1:off   2:on    3:on    4:on    5:on    6:off 
```



## 4、 NFS共享文件系统配置文件格式说明


nfs权限（共享目录【借给你手机】） nfs配置的/etc/exports /data 172.16.1.0/24(rw)
本地文件系统权限（【手机密码不告诉你】） 挂载目录的权限rwxr-xr-x root root /data

EXAMPLE 

```
sample /etc/exports file 
/               master(rw) trusty(rw,no_root_squash) 
/projects       proj*.local.domain(rw) 
/usr            *.local.domain(ro) @trusted(rw) 
/home/joe       pc001(rw,all_squash,anonuid=150,anongid=100) 
/pub            (ro,insecure,all_squash) 
```

上述各个列的参数含义如下： 
	NFS 共享的目录：为 NFS 服务端要共享的实际目录，要用绝对路径，如（/data）。注意共享目
录的本地权限，如果需要读写共享，一定要让本地目录可以被 NFS 客户端的用户（nfsnobody）
读写。 

​    NFS 客户端地址：为 NFS 服务端授权的可访问共享目录的 NFS 客户端地址，可以为单独的 IP 地
址或主机名、域名等，也可以为整个网段地址，还可以用“*”来匹配所有客户端服务器，这里所
谓的客户端一般来说是前端的业务服务器，例如：Web 服务。

权限参数集：对授权的 NFS 客户端的访问权限设置。参数具体说明见后文。 
    nfs 共享权限（共享权限（借给你手机）） nfs 配置的/etc/exports   /data 172.16.1.0/24(rw) 
    本地文件系统权限（不告诉你密码）  挂在目录的权限 rwxr-xr-x nfsnobody nfsnobody 
/nfsbackup

### 服务端配置

创建共享目录/data 

```bash
mkdir -p /data 
ls -ld /data 
id  nfsnobody 
chown -R  nfsnobody.nfsnobody /data 
```

创建配置文件

vim  /etc/exports 

```bash
#share  /data by oldboy for bingbing at 20160425 
/data 172.16.1.0/24(rw,sync) 
```

优雅重启，平滑重启-不影响正在使用的客户

```bash
/etc/init.d/nfs reload 
```

 第四个里程碑-服务端自我检查 

```bash
rpcinfo -p 172.16.1.31 
showmount -e 172.16.1.31 
Export list for 172.16.1.31: 
/data 172.16.1.0/24 
```

### 客户的配置 

 启动 rpcbind 服务并加入开机自启动 

```bash
/etc/init.d/rpcbind start 
chkconfig rpcbind on 
```

检查远端 showmount 

```bash
showmount -e 172.16.1.31
```

客户端挂载

```bash
mount -t nfs  172.16.1.31:/data  /mnt 
```

## 5、NFS共享文件系统配置文件案例说明	

配置例一	/data 10.0.0.0/24（rw,sync）

>     说明：允许客户端读写，并且数据同步写入到服务器端的磁盘里
>     注意：24和“（”之间不能有空格

配置例二	/data 10.0.0.0/24（rw,sync,all_squash,anonuid=2000,anongid=2000）

> 说明：允许客户端读写，并且数据同步写到服务器端的磁盘里，并且指定客户端的用户UID和GID。
> 	      早期生产环境的一种配置，适合多客户端共享一个NFS服务单目录，
> 		  如果所有服务器的nfsnobody账户UID都是65534，则本例没什么必要了。
> 		  早期centos5.5的系统默认情况下nfsnobody的UID不一定是65534，此时如果这些服务器共享一个NFS目录， 就会出现访问权限问题。

配置例三	/home/oldboy 10.0.0.0/24（ro）   <-- 是为开发人员想查看线数据准备配置方式

> 说明：只读共享
>  用途：例如在生产环境中，开发人员有查看生产服务器日志的需求，但又不希望给开发生产服务器的权限，
> 	      那么就可以给开发提供从某个测试服务器NFS客户端上查看某个生产服务器的日志目录（NFS共享）的权限，
> 		  当然这不是唯一的方法，
> 		  例如可以把程序记录的日志发送到测试服务器供开发查看或者通过收集日志等其它方式展现

## 6、NFS 配置参数权限 

NFS 服务器端的权限设置，即/etc/exports 文件配置格式中小括号( )里的参数集

| 参数名称       | 参数用途                                                     |
| -------------- | ------------------------------------------------------------ |
| rw*            | Read-write，表示可读写权限                                   |
| ro             | Read-only，表示只读权限                                      |
| sync*          | (同步，实时)请求或写入数据时，数据同步写入到 NFS <br/>Server 的硬盘后才返回。优点，数据安全不会丢，缺点，性能比不启用该参数要差 |
| async          | 异步）写入时数据会先写到内存缓冲区，只到硬盘有空档<br/>才会再写入磁盘，这样可以提升写入效率！风险为若服务器<br/>宕机或不正常关机，会损失缓冲区中未写入磁盘的数据（解<br/>决办法：服务器主板电池或加 UPS，AB（双路电源）不间断<br/>电源） |
| no_root_squash | 保持 root 用户不压缩访问 NFS Server 共享目录的用户如果是 root 的话，它对该共<br/>享目录具有 root 权限。这个配置原本是为无盘客户端准备<br/>的。用户应避免使用！ <br/>如果是 root 则保持 root 权限 |
| root_squash    | 如果访问 NFS Server 共享目录的用户是 root，则它的权限将<br/>被压缩成匿名用户，同时它的 UID 和 GID 通常会变成<br/>nfsnobody 帐号身份。 <br/>如果是 root 压缩为匿名用户 |
| all_squash     | 不管访问 NFS Server 共享目录的用户身份如何，它的权限都<br/>将被压缩成匿名用户(nfsnobody)，同时它的 UID 和 GID 都会<br/>变成 nfsnobody 帐号身份。在早期多个 NFS 客户端同时读写<br/>NFS Server 数据时，这个参数很有用。※ <br/>在生产中配置 NFS 的重要技巧： <br/>1）确保所有客户端服务器对 NFS 共享目录具备相同的用户<br/>访问权限 <br/>  a. all_squash 把所有客户端都压缩成固定的匿名用户（UID<br/>相同）。 <br/>  b.就是 anonuid，anongid 指定的 UID 和 GID 的用户。 <br/>2）所有的客户端和服务端（所有服务器上面）都需要有一<br/>个相同的 UID 和 GID 的用户，即 nfsnobody(UID 必须 |
| anonuid        | 指定的是匿名用户的 uid 或 gid 数字。 <br/>所有服务器上面，匿名用户（nfsnobody rsync www）uid 和<br/>gid。 <br/> <br/>参数以 anon*开头即指 anonymous 匿名用户，这个用户的<br/>UID 设置值通常为 nfsnobody 的 UID 值，当然也可以自行设<br/>置这个 UID 值。但是，UID 必须存在于/etc/passwd 中。在多<br/>NFS Clients 时，如多台 Web Server 共享一个 NFS 目录，通过这个参数可以使得不同的 NFS Clients 写入的数据对所有<br/>NFS Clients 保持同样的用户权限，即为配置的匿名 UID 对应<br/>用户权限，这个参数很有用，一般默认即可 |
| anongid        | 同 anonuid，区别就是把 uid（用户 id）换成 gid（组 id         |

# 四、实时同步服务

## 1、实时同步服务软件部署

### inotify+rsync实现实时同步备份

(1) 将inotify软件安装成功

```bash
yum install -y inotify-tools
```

说明：操作系统的yum源文件中，是否存在epel源

```bash
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-6.repo

[root@nfs01 ~]# rpm -ql inotify-tools
/usr/bin/inotifywait                <--- 实现对数据目录信息变化监控（重点了解的命令）
/usr/bin/inotifywatch               <--- 监控数据信息变化，对变化的数据进行统计

[root@nfs01 ~]# cd /proc/sys/fs/inotify/
[root@nfs01 inotify]# ll
    总用量 0
    -rw-r--r-- 1 root root 0 2018-02-25 19:45 max_queued_events    
    -rw-r--r-- 1 root root 0 2018-02-25 19:45 max_user_instances
    -rw-r--r-- 1 root root 0 2018-02-25 19:45 max_user_watches
    max_user_watches:	设置inotifywait或inotifywatch命令可以监视的文件数量（单进程）
	                    默认只能监控8192个文件

    max_user_instances:	设置每个用户可以运行的inotifywait或inotifywatch命令的进程数
	                    默认每个用户可以开启inotify服务128个进程
	
    max_queued_events:	设置inotify实例事件（event）队列可容纳的事件数量
                        默认监控事件队列长度为16384
	
```

(2) 将rsync守护进程模式部署完毕

	rsync服务端部署
	a 检查rsync软件是否已经安装
	b 编写rsync软件主配置文件
	c 创建备份目录管理用户
	d 创建备份目录，并进行授权
	e 创建认证文件，编写认证用户和密码信息，设置文件权限为600
	f 启动rsync守护进程服务
	
	rsync客户端部署
	a 检查rsync软件是否已经安装	
	b 创建认证文件，编写认证用户密码信息即可，设置文件权限为600
	c 利用客户端进行数据同步测试

（3） 要让inotify软件和rsync软件服务建立连接（shell脚本）

rsync软件应用命令：

```bash
rsync -avz /etc/hosts rsync_backup@172.16.1.41::backup --password-file=/etc/rsync.password
```

inotify软件应用命令：

inotifywait 

```bash
	-m|--monitor	         始终保持事件监听状态
	-r                       进行递归监控
	-q|--quiet               将无用的输出信息，不进行显示
	--timefmt \<fmt>          设定日期的格式
	                         man strftime 获取更多时间参数信息
	--format \<fmt>           命令执行过程中，输出的信息格式
    -e                       指定监控的事件信息
	man inotifywait 查看所有参数说明和所有可以监控的事件信息
	
```

总结主要用到的事件信息：

create创建、delete删除、moved_to移入、close_write修改

```bash
inotifywait -mrq --timefmt "%F" --format "%T %w%f 事件信息：%e" /data  <-- 相对完整的命令应用
inotifywait -mrq --timefmt "%F" --format "%T %w%f 事件信息：%e" -e create /data   <-- 指定监控什么事件信息
inotifywait -mrq --format "%w%f" -e create,delete,moved_to,close_write  /data   
以上为实现实时同步过程，所需要的重要监控命令
```

```bash
编写脚本：实现inotify与rsync软件结合
#!/bin/bash
####################    
inotifywait -mrq --format "%w%f" -e create,delete,moved_to,close_write  /data|\
while read line
do
rsync -az --delete /data/ rsync_backup@172.16.1.41::backup --password-file=/etc/rsync.password
done
```

（4）最终的测试

	sh -x intofy.sh

### sersync+rsync实现实时同步备份

(1) 下载安装sersync软件

```bash
先进行软件下载，把软件包上传到系统中
unzip sersync_installdir_64bit.zip
cd sersync_installdir_64bit
mv sersync /usr/local/
tree
```

（2） 编写sersync配置文件

```bash
[root@nfs01 sersync]# cd /usr/local/sersync/conf/
[root@nfs01 conf]# ll
 总用量 4
-rw-r--r-- 1 root root 2214 2011-10-26 11:54 confxml.xml
```

```xml
6     <filter start="false">
7         <exclude expression="(.*)\.svn"></exclude>
8         <exclude expression="(.*)\.gz"></exclude>
9         <exclude expression="^info/*"></exclude>
10         <exclude expression="^static/*"></exclude>
11     </filter>
   说明：实现同步数据过滤排除功能
12     <inotify>
13         <delete start="true"/>
14         <createFolder start="true"/>
15         <createFile start="false"/>
16         <closeWrite start="true"/>
17         <moveFrom start="true"/>
18         <moveTo start="true"/>
19         <attrib start="false"/>
20         <modify start="false"/>
21     </inotify>
说明：类似于inotify的-e参数功能，指定监控的事件信息

23     <sersync>
24         <localpath watch="/data">
25             <remote ip="172.16.1.41" name="backup"/>
26             <!--<remote ip="192.168.8.39" name="tongbu"/>-->
27             <!--<remote ip="192.168.8.40" name="tongbu"/>-->
28         </localpath>
29         <rsync>
30             <commonParams params="-az"/>
31             <auth start="true" users="rsync_backup" passwordfile="/etc/rsync.password"/>
32             <userDefinedPort start="false" port="874"/><!-- port=874 -->
33             <timeout start="false" time="100"/><!-- timeout=100 -->
34             <ssh start="false"/>
35         </rsync>
 说明：以上内容是数据相关的配置信息，是必须进行修改调整配置
```

(3) 应用sersync软件，实现实时同步

```bash
 [root@nfs01 conf]# cd /usr/local/sersync/
 [root@nfs01 sersync]# cd bin/
 [root@nfs01 bin]# ll
 总用量 1768
 -rw-r--r-- 1 root root 1810128 2011-10-26 14:19 sersync
 sersync命令参数：
 参数-d:              启用守护进程模式
 参数-r:              在监控前，将监控目录与远程主机用rsync命令推送一遍（测试）
 参数-n:              指定开启守护线程的数量，默认为10个
 参数-o:              指定配置文件，默认使用confxml.xml文件
	
```

	./sersync -dro /usr/local/sersync/conf/confxml.xml

## 2、实时同步软件概念介绍

    inotify软件
    Inotify是一种强大的，细粒度的。异步的文件系统事件监控机制，linux内核从2.6.13起，
    加入了Inotify支持，通过Inotify可以监控文件系统中添加、删除，修改、移动等各种事件，
    利用这个内核接口，第三方软件就可以监控文件系统下文件的各种变化情况，
    而inotify-tools正是实施这样监控的软件	
    软件参考链接：https://github.com/rvoicilas/inotify-tools/wiki
    
    sersync软件
    Sersync项目利用inotify与rsync技术实现对服务器数据实时同步的解决方案，
    其中inotify用于监控sersync所在服务器上文件系统的事件变化，
    rsync是目前广泛使用的本地及异地数据同步工具，
    其优点是只对变化的目录数据操作，甚至是一个文件不同的部分进行同步，
    所以其优势大大超过使用挂接文件系统或scp等方式进行镜像同步。
    软件参考链接：https://github.com/wsgzao/sersync

# 五、SSH远程管理服务

##  1、远程管理服务知识介绍

  SSH是Secure Shell Protocol的简写，由 IETF 网络工作小组（Network Working Group）制定；
		在进行数据传输之前，SSH先对联机数据包通过加密技术进行加密处理，加密后在进行数据传输。
		确保了传递的数据安全。

SH是专为远程登录会话和其他网络服务提供的安全性协议。
		利用SSH协议可以有效的防止远程管理过程中的信息泄露问题，在当前的生产环境运维工作中，
		绝大多数企业普遍采用SSH协议服务来代替传统的不安全的远程联机服务软件，如telnet(23端口，非加密的)等。
		在默认状态下，SSH服务主要提供两个服务功能：
	

SSH远程登录服务功能作用
	    a 一是提供类似telnet远程联机服务器的服务，即上面提到的SSH服务；
	    b 另一个是类似FTP服务的sftp-server，借助SSH协议来传输数据的，提供更安全的SFTP服务(vsftp,proftp)。

## 	2、远程管理服务概念详解

### SSH远程管理服务加密技术

ssh连接登录过程
	①. ssh客户端发出连接请求
	    >/root/.ssh/known_hosts
	②. ssh服务端会发出确认信息，询问客户端你是否真的要连接我
	③. ssh客户端输入完成yes，会等到一个公钥信息
	    cat /root/.ssh/known_hosts
	④. ssh服务端将公钥信息发送给ssh客户端
	⑤. ssh客户端利用密码进行登录

​    加密技术分为v1和v2两个版本   

	sshv1版本不会经常更换锁头和钥匙，因此会有安全隐患
	sshv2版本会经常更换锁头和钥匙，因此提高了远程连接安全性

### SSH远程管理服务认证类型

 基于密钥方式实现远程登录
	   ①. ssh管理服务器上创建密钥对信息（公钥 私钥）
	   ②. ssh管理服务器上将公钥发送给被管理服务器
	   ③. ssh管理服务器向被管理服务器发送连接请求
	   ④. ssh被管理服务器向管理服务器发送公钥质询
	   ⑤. ssh管理服务器处理公钥质询请求，将公钥质询结果发送给被管理主机
	   ⑥. ssh被管理服务器接收公钥质询响应信息，从而确认认证成功
	   ⑦. ssh管理服务端可以和被管理服务端建立基于密钥连接登录

### 基于密钥登录方式部署流程

(1) 在管理主机上创建密钥对信息

```bash
ssh-keygen -t dsa      <-- 创建密钥对命令 -t dsa表示指定密钥对加密类型
Generating public/private dsa key pair.
Enter file in which to save the key (/root/.ssh/id_dsa):      <-- 确认私钥文件所保存的路径
/root/.ssh/id_dsa already exists.
Overwrite (y/n)? y                                            <-- 如果已经存在了密钥对信息，是否进行覆盖
Enter passphrase (empty for no passphrase):                   <-- 确认是否给私钥设置密码信息（一般为空）
Enter same passphrase again:                                  
Your identification has been saved in /root/.ssh/id_dsa.
Your public key has been saved in /root/.ssh/id_dsa.pub.
The key fingerprint is:
46:c8:21:b9:99:6e:0c:59:39:66:38:7a:97:29:51:76 root@m01
The key's randomart image is:
+--[ DSA 1024]----+
|   o+oE          |
|  +.B+ o         |
| . B Bo .        |
|. = B  .         |
| . *    S        |
|    +  .         |
|   .             |
|                 |
|                 |
+-----------------+
```

（2）将管理主机上公钥信息发送给被管理主机

```bash
ssh-copy-id -i /root/.ssh/id_dsa.pub 172.16.1.31
    root@172.16.1.31's password: 
    Now try logging into the machine, with "ssh '172.16.1.31'", and check in:
.ssh/authorized_keys
to make sure we haven't added extra keys that you weren't expecting.
```

（3）进行远程管理测试（基于密钥的方式进行远程管理）

```bash
ssh 172.16.1.31        <-- 可以不用输入密码信息，就能登陆成功
ssh 172.16.1.31 uptime <-- 可以不用登陆到远程主机，就可以直接查看远程主机信息
```

### SSH服务端配置文件信息说明(/etc/ssh/sshd_config)

```bash
Port 52113	                 <- 修改ssh服务端口号信息			
ListenAddress 0.0.0.0        <- 主要作用提升网络连接安全性
PS：监听地址只能配置为服务器网卡上拥有的地址    
PermitRootLogin no	         <- 是否允许root用户远程登录	
PermitEmptyPasswords no	     <- 是否允许空密码
UseDNS no                    <- 是否进行DNS反向解析（提升ssh远程连接效率） 					
GSSAPIAuthentication no		 <- 是否进行远程GSSAPI认证（提升ssh远程连接效率）
```

### sftp常用操作命令总结

```bash
 bye             Quit sftp	                          <-- 表示退出sftp传输模式
 cd path         Change remote directory to 'path'     <-- 改变远程目录信息
 pwd             Display remote working directory      <-- 显示远程主机当前目录信息
 lcd path        Change local directory to 'path'      <-- 改变本地目录路径信息
 lpwd            Print local working directory         <-- 输出本地目录路径信息
 get [-P] remote-path [local-path]  
 Download file                       				   <-- 下载文件命令
 put [-P] local-path [remote-path]                     <-- 上传文件命令
 Upload file 
```

# 六、ansible批量管理服务介绍

## 1、批量管理服务知识介绍

a. ansible是一个基于Python开发的自动化运维工具
b. ansible是一个基于ssh协议实现远程管理的工具
c. ansible软件可以实现多种批量管理操作（批量系统配置、批量软件部署、批量文件拷贝、批量运行命令）
saltstack puppet

批量管理服务特征介绍

    a ansible软件服务端（管理端）：不需要启动任何服务 默认服务端不需要任何的配置
    b ansible软件客户端（受控端）：没有客户端软件安装

## 2、 ansible软件安装部署

### ansible软件自动化环境架构规划

```bash
  管理主机1台：
  10.0.0.61   m01
  受控主机3台：
  10.0.0.41   backup
  10.0.0.31   nfs01
  10.0.0.7    web01
```

ansible软件自动化部署条件

  建议基于ssh密钥方式建立远程连接

### ssh密钥对创建（管理主机）

```bash
ssh-keygen -t dsa
影响免交互创建密钥对创建因素：
1）需要指定私钥存放路径
-f /root/.ssh/id_dsa
2）需要进行私钥文件密码设定
-N/-P  
-N ""/-P ""

免交互创建密钥对方法
ssh-keygen -t dsa -f /root/.ssh/id_dsa -N ""
```

### 分发公钥文件（管理主机进行分发）

ssh-copy-id -i /root/.ssh/id_dsa.pub 172.16.1.31

影响免交互批量分发密钥因素
1）需要有确认连接过程，需要输入yes/no

```bash
-o StrictHostKeyChecking=no
sshpass -p123456 ssh-copy-id -i /root/.ssh/id_dsa.pub "-o StrictHostKeyChecking=no 172.16.1.31"
```

2）需要解决密码问题

```bash
sshpass -p123456 ssh-copy-id -i /root/.ssh/id_dsa.pub 172.16.1.31
Now try logging into the machine, with "ssh '172.16.1.31'", and check in:
.ssh/authorized_keys
to make sure we haven't added extra keys that you weren't expecting.
```

免交互批量分发公钥脚本：

```bash
#!/bin/bash
rm /root/.ssh/id_dsa
ssh-keygen -t dsa -f /root/.ssh/id_dsa -N ""

for ip in 31 41 7
do
sshpass -p123456 ssh-copy-id -i /root/.ssh/id_dsa.pub "-o StrictHostKeyChecking=no 172.16.1.$ip"
done
```

### 检查是否可以进行基于密钥远程管理

```bash
ssh 172.16.1.31 uptime
免交互批量检查测试脚本
#!/bin/bash
rm /root/.ssh/id_dsa
ssh-keygen -t dsa -f /root/.ssh/id_dsa -N ""
for ip in 31 41 7
do
sshpass -p123456 ssh-copy-id -i /root/.ssh/id_dsa.pub "-o StrictHostKeyChecking=no 172.16.1.$ip"
done
```

 基于ssh口令方式建立远程连接（也可以）

```bash
vim /etc/ansible/hosts
[oldboy]
172.16.1.7
172.16.1.31 ansible_user=root ansible_password=123456
172.16.1.41

ansible 172.16.1.31 -m command -a "hostname" -k     --- 实现口令交互式远程管理
SSH password: 
172.16.1.31 | SUCCESS | rc=0 >>
nfs01
```

### ansible软件下载安装

```bash
  ansible管理主机软件安装：
  yum install -y ansible
  ansible受控主机软件安装：（可选）
  yum install -y libselinux-python
```

## 3、ansible软件应用过程	

​	ansible 管理主机信息或者主机组信息  -m 模块名称 -a 相关模块参数

ansible的简单使用格式

ansible HOST-PATTERN  -m MOD_NAME  -a MOD_ARGS

主机信息：远程主机IP地址  远程主机组名称  远程所有主机all
	-m 指定相应模块
	-a 利用模块中某些参数功能

示例：

```bash
]# ansible all -m ping

]# ansible all -m command -a 'ls /var'

]# ansible all -m copy -a "src=/etc/fstab dest=/tmp/fstab"

]# ansible all -m cron -a "minute=*/5 job='/bin/echo hello world' name=Hellow"

]# ansible all -m file -a "src=/tmp/fstab path=/tmp/fstab.link state=link"

]# ansible all -m service -a 'name=httpd state=started'
```

命令类型模块：

### 第一个模块：command

```bash
官方参考链接：http://docs.ansible.com/ansible/latest/modules/command_module.html
参数：chdir---在执行莫个命令前，先切换目录
[root@m01 ansible]# ansible 172.16.1.31 -m command -a "chdir=/tmp/ pwd"
172.16.1.31 | SUCCESS | rc=0 >>
/tmp
```

```bash
参数：creates---判断一个文件是否存在，如果已经存在了，后面的命令就不会执行
[root@m01 ansible]# ansible 172.16.1.41 -m command -a "creates=/etc/rsyncd.conf hostname"
172.16.1.41 | SUCCESS | rc=0 >>
skipped, since /etc/rsyncd.conf exists

[root@m01 ansible]# ansible 172.16.1.41 -m command -a "creates=/etc/rsyncd.conf.bak hostname"
172.16.1.41 | SUCCESS | rc=0 >>
skipped, since /etc/rsyncd.conf.bak exists

[root@m01 ansible]# ansible 172.16.1.41 -m command -a "creates=/etc/rsyncd.123456 hostname"
172.16.1.41 | SUCCESS | rc=0 >>
backup

参数：removes---判断一个文件是否存在，如果不存在，后面的命令就不会执行
[root@m01 ansible]# ansible 172.16.1.41 -m command -a "removes=/etc/rsyncd.conf hostname"
172.16.1.41 | SUCCESS | rc=0 >>
backup

[root@m01 ansible]# ansible 172.16.1.41 -m command -a "removes=/etc/rsyncd.1212213123 hostname"
172.16.1.41 | SUCCESS | rc=0 >>
skipped, since /etc/rsyncd.1212213123 does not exist

参数（必须要有的）：free_form---表示执行command模块时，必须要有linux合法命令信息
ansible 172.16.1.41 -m command -a "ls"
172.16.1.41 | SUCCESS | rc=0 >>
1
anaconda-ks.cfg
dead.letter
heqing
```

### 第二个模块：shell模块(万能模块)

参数：chdir---在执行莫个命令前，先切换目录
参数：creates---判断一个文件是否存在，如果已经存在了，后面的命令就不会执行
参数：removes---判断一个文件是否存在，如果不存在，后面的命令就不会执行
参数（必须要有的）：free_form---表示执行command模块时，必须要有linux合法命令信息

```bash
[root@m01 ansible]# ansible 172.16.1.41 -m shell -a "ls;pwd"
172.16.1.41 | SUCCESS | rc=0 >>
1
anaconda-ks.cfg
dead.letter
/root
说明：shell模块可以满足command模块所有功能，并且可以支持识别特殊字符信息 < > | ; 
```

###  第三个模块：script---专门运行脚本模块

参数：chdir---在执行莫个命令前，先切换目录
参数：creates---判断一个文件是否存在，如果已经存在了，后面的命令就不会执行
参数：removes---判断一个文件是否存在，如果不存在，后面的命令就不会执行
参数（必须要有的）：free_form---表示执行command模块时，必须要有linux合法命令信息

### copy----复制模块

参数：backup---对数据信息进行备份

```bash
[root@m01 ansible]# ansible 172.16.1.41 -m copy -a "src=/tmp/file01.txt dest=/tmp/ backup=yes"
172.16.1.41 | SUCCESS => {
"backup_file": "/tmp/file01.txt.71887.2018-04-02@23:33:19~", 
"changed": true, 
"checksum": "029b054db136cc36d5605e3818305825ff4b8ffb", 
"dest": "/tmp/file01.txt", 
"gid": 0, 
"group": "root", 
"md5sum": "434660b5ad7deeba8815349f71409405", 
"mode": "0644", 
"owner": "root", 
"size": 6, 
"src": "/root/.ansible/tmp/ansible-tmp-1522683197.05-52744169892601/source", 
"state": "file", 
"uid": 0
}
```

参数：src---定义要推送数据信息
参数：dest---定义将数据推送到远程主机什么目录中

```bash
[root@m01 ansible]# touch /tmp/file01.txt
[root@m01 ansible]# ansible 172.16.1.41 -m copy -a "src=/tmp/file01.txt dest=/tmp/"
172.16.1.41 | SUCCESS => {
    "changed": true, 
    "checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709", 
    "dest": "/tmp/file01.txt", 
    "gid": 0, 
    "group": "root", 
    "md5sum": "d41d8cd98f00b204e9800998ecf8427e", 
    "mode": "0644", 
    "owner": "root", 
    "size": 0, 
    "src": "/root/.ansible/tmp/ansible-tmp-1522682948.27-60532389065095/source", 
    "state": "file", 
    "uid": 0
}
[root@m01 ansible]# ansible 172.16.1.41 -m shell -a "ls -l /tmp/"
172.16.1.41 | SUCCESS | rc=0 >>
total 24
-rw-r--r-- 1 root root    0 Apr  2 23:29 file01.txt
```

	参数：owner---设置复制后的文件属主权限
	参数：group---设置复制后的文件属组权限
	参数：mode---设置复制后的文件权限（600 755）

### file----文件属性修改/目录创建/文件创建

参数：owner---设置复制后的文件属主权限
参数：group---设置复制后的文件属组权限
参数：mode---设置复制后的文件权限（600 755）

```bash
ansible 172.16.1.41 -m file -a "dest=/tmp/file01.txt owner=oldboy group=oldboy mode=600"
172.16.1.41 | SUCCESS => {
"changed": true, 
"gid": 500, 
"group": "oldboy", 
"mode": "0600", 
"owner": "oldboy", 
"path": "/tmp/file01.txt", 
"size": 6, 
"state": "file", 
"uid": 500
}
```

参数：state---用于指定创建目录或文件

创建文件

```bash
ansible 172.16.1.41 -m file -a "dest=/tmp/file01.txt state=touch"
172.16.1.41 | SUCCESS => {
    "changed": true, 
    "dest": "/tmp/file01.txt", 
    "gid": 0, 
    "group": "root", 
    "mode": "0644", 
    "owner": "root", 
    "size": 0, 
    "state": "file", 
    "uid": 0
}
```

创建目录

```bash
ansible 172.16.1.41 -m file -a "dest=/tmp/dir01 state=directory"
172.16.1.41 | SUCCESS => {
    "changed": true, 
    "gid": 0, 
    "group": "root", 
    "mode": "0755", 
    "owner": "root", 
    "path": "/tmp/dir01", 
    "size": 4096, 
    "state": "directory", 
    "uid": 0
}
```

### yum---安装软件包模块

name：执行要安装软件的名称，以及软件的版本
state：installed安装  absent(卸载)

```bash
ansible 172.16.1.41 -m yum -a "name=iftop state=installed"
ansible 172.16.1.41 -m yum -a "name=iftop state=absent"
list：指定软件名称，查看软件是否可以安装，以及是否已经安装过了
ansible 172.16.1.41 -m yum -a "list=iftop"
```

### service---管理服务状态模块

name: 指定要管理的服务名称（管理的服务一定在chkconfig中可以看到）
state：stopped started restarted reloaded
enabled：yes表示服务开机自启动 no表示服务开机不要自动启动

```bash
ansible 172.16.1.41 -m service -a "name=crond state=started enabled=yes"
```

### cron---定时任务模块

minute=0-59 * */n , -   hour  day  month weekday  job='/bin/sh /server/scripts/test.sh &>/dev/null'

```bash
添加定时任务
ansible 172.16.1.41 -m cron -a "minute=0 hour=0 job='/bin/sh /server/scripts/test.sh &>/dev/null'"
ansible 172.16.1.41 -m cron -a "name=oldboy02 minute=0 hour=0 job='/bin/sh /server/scripts/test.sh &>/dev/null'"

删除定时任务
ansible 172.16.1.41 -m cron -a "name=oldboy02 minute=0 hour=0 job='/bin/sh /server/scripts/test.sh &>/dev/null' state=absent"
ansible 172.16.1.41 -m cron -a "name=oldboy01 state=absent"

注释定时任务
ansible 172.16.1.41 -m cron -a "name=oldboy01 minute=0 hour=0 job='/bin/sh /server/scripts/test.sh &>/dev/null' disabled=yes"
ansible 172.16.1.41 -m cron -a "name=oldboy01 job='/bin/sh /server/scripts/test.sh &>/dev/null' disabled=no"
```

总结ansible颜色信息：

	绿色：查看远程主机信息，不会对远程主机系统做任何修改
	红色：执行操作出现异常错误
	黄色：对远程主机系统进行修改操作
	粉色：警告或者忠告信息

## 4、ansible软件剧本

编写剧本规范：
	http://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html



\- 用法说明，表示列表显示的内容
    水果信息：
	 \- 苹果
	 \- 香蕉
	 \- 西瓜

\. : 用法说明：
	    姓名: 张三
		性别: 男
		人员信息:
		\- 运维人员: sa
		\- 开发人员: dev
		\- 存储人员: dba

. 空格 用法说明：
	    对内容进行分级时，需要有两个空格表示分级
		软件安装步骤:
		 \- 服务端安装步骤:
		    第一个里程碑: 检查软件是否安装
			第二个里程碑: 编写配置文件内容
		 \- 客户端安装步骤:
	    补充：必须使用空格分隔ansible剧本级别，一定不要使用tab键进行分割

执行脚本方法：

```bash
ansible-playbook /etc/ansible/ansible-playbook/test.yaml
ansible-playbook -C /etc/ansible/ansible-playbook/test.yaml
```

playbook的核心元素

​	Tasks

​	Variables

​	Templates：包含了模板语法的文本文件

​	Handlers：由特定条件触发的任务

​	Roles

playbook的基础组件

​	Hosts：运行指定任务的目标主机

​	remote_user：在远程主机上执行任务的用户

​		sudo_user：

​	tasks：任务列表

​		模块, 模块参数

​		格式：

​			action：module arguments

​			module：arguments

   任务可以通过”tag“打标签，而后在ansible-playbook命令上使用-t进行调用

示例：

```
- hosts: all              运行在哪些主机上
  remote_user: root	      远程主机以什么身份运行
  tasks:			      任务
  - name: create a user 	任务名称
  user: name=user3 system=true uid=307
```

httpd示例

```YML
- hosts: webservs
- hosts: web
  remote_user: root
  tasks:
    - name: install httpd
    yum: name=httpd state=present
    - name: install configure file
    copy: src=/root/working/http.conf dest=/etc/httpd/conf/
    - name: start httpd service
    service: name=httpd state=started
```

handlers

任务，在特定条件下触发

接收到其他任务的通知时被触发

某任务的状态在运行后为changed时，可通过notify通知给响应的handlers

task下要添加一个notify：restart httpd（也是就handlers的name）

handlers：

   \- name： restart httpd

​     service： name=httpd state=restart

variables：

1 facts：可直接调用

2 ansible-playbook命令的命令行中的自定义变量

​	e VARS, --extar-vars=VARS

3 通过role传递变量

4 Host Inventory

​	a 向不同的主机传递不同的变量

 	  IP/HOSTNAME  varaiable=value  var2=value2

​	b 向组中的主机传递相同的变量

 	 [groupname：vars]

  	 variable=value

  示例：

```
- hosts: web
  rsmote_user: root
  tasks:
   - name: install {{ pkname }}
   yum: name={{ pkname }} state=present
~]# ansible-playbook -e pkname=memcached --check vartest.yaml 
```

templates

文本文件，嵌套有脚本（使用模板编程语言编写）

jinja2：

字面量：

字符串：使用单引号或双引号

数字：整数， 浮点数

列表：[item1， item2， ...]

元祖：(item1,   item2, ...]

字典：{key：value1， key2：value2, ...}

布尔型：true/false

算术：

+，- *， /, //

条件测试：

when语句：在task中使用， jinja2的语法格式

```YML
tasks：
   -name：install conf file to centos7
    template：src=files/nginx.conf.c7.j2 dest=/etc/nginx/nginx.conf
    when：ansible_distribution_major_version == "7"
   -name：install conf file to centos6
    template：src=files/nginx.conf.c6.j2 dest=/etc/nginx/nginx.conf
    when：ansible_distribution_major_version == "
```

循环：迭代，需要重复执行的任务

对迭代项的引用， 固定变量名为“item”

而后在task中使用with_items给定要迭代的元素列表

示例1：

```yml
-name：install some packages
yum：name={{ item }} state=present
with_items:
  -nginx
  -memcached
  -php-fpm
```

示例2：

```yml
-name：add some groups
group：name={{ item }} state=present
with_items:
 - group11
 - group12
 - group13
-name: add some users
 user: name={{ item.name }} group={{ item.group }} state=present
 with_items
	-{ name: "user11", group: 'group11'}
	-{ name: 'user12", group: 'group12'}
	-{ name: 'user13", group: 'group13'}
```

角色(roles):

每个角色，以特定的层级目录结构进行组织：

mysql/

​	files/ ：存放由copy或script模块等调用的文件

​	templates/： template模块查找所需的模板文件的目录

​	tasks/：至少应该包含一个以main.yml的文件， 其他的文件需要在此文件通过include进行包含

​	handlers/ 至少应该包含一个以main.yml的文件， 其他的文件需要在此文件通过include进行包含、

​	vars/ 至少应该包含一个以main.yml的文件， 其他的文件需要在此文件通过include进行包含

​	meta/ 至少应该包含一个以main.yml的文件，定义当前角色的特殊设定及其依赖关系  其他的文件需要在此文件通过include进行包含	

​	default/： 设定默认变量时使用此目录的main.yml文件

在playbook调用角色 1

```
-hosts：webservs
  remote_user：root
  roles：
    - mysql
    - memcache
    - nginx
```



# 七、LNMP构建安装

## LNMP架构说明

1）使前端web服务和后端存储服务进行串联
2）主要实现处理PHP程序动态请求

## LNMP架构部署

 1）安装LNMP相关软件
	①. 部署Linux系统
	    基础优化操作要完成（防火墙关闭 关闭selinux /tmp权限为1777）
	②. 部署nginx服务
	    暂时忽略
	③. 部署mysql服务

  yum部署软件  编译安装软件 二进制包方式部署mysql服务

```bash
第一个里程：下载并解压mysql软件程序
mysql官方下载链接地址：ftp://ftp.jaist.ac.jp/pub/mysql/Downloads/MySQL-5.6/
上传mysql软件程序，进行利用xftp软件进行上传
tar xf mysql-5.6.34-linux-glibc2.5-x86_64.tar.gz
mv mysql-5.6.34-linux-glibc2.5-x86_64 /application/mysql-5.6.34
		
第二个里程：创建软件程序软链接
ln -sf /application/mysql-5.6.34/ /application/mysql

第三个里程：创建数据库管理用户，并授权数据目录
useradd mysql -M -s /sbin/nologin 
chown -R mysql.mysql /application/mysql/data/

第四个里程：对数据库服务进行初始化
/application/mysql/scripts/mysql_install_db --basedir=/application/mysql --datadir=/application/mysql/data/ --user=mysql

第五个里程：启动mysql服务
cp /application/mysql/support-files/mysql.server /etc/init.d/mysqld
sed -ri 's#/usr/local#/application#g' /etc/init.d/mysqld /application/mysql/bin/mysqld_safe
cp /application/mysql/support-files/my-default.cnf /etc/my.cnf
/etc/init.d/mysqld start

第六个里程：设置数据库root用户登录密码
/application/mysql/bin/mysqladmin -uroot password "oldboy123"
/application/mysql/bin/mysql -uroot -poldboy123
```

④. PHP软件安装部署过程

   第一里程：解决PHP软件的依赖关系 



    yum install -y zlib-devel libxml2-devel libjpeg-devel libjpeg-turbo-devel libiconv-devel freetype-devel libpng-devel gd-devel libcurl-devel libxslt-devel
    
    libiconv软件安装---字符集转换库(默认可以不进行安装了)
    cd /server/tools
    #wget http://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.14.tar.gz
    tar zxf libiconv-1.14.tar.gz
    cd libiconv-1.14
    ./configure --prefix=/usr/local/libiconv
    make
    make install
    cd ../
    
    #wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-6.repo
    yum -y install libmcrypt-devel mhash mcrypt
    rpm -qa libmcrypt-devel mhash mcrypt
    
    第二个里程：下载解压PHP软件
    php官方网站下载：php.net
    cd /server/tools/
    tar xf php-5.5.32.tar.gz
    cd php-5.5.32
    ./configure \
    --prefix=/application/php-5.5.32 \
    --with-mysql=/application/mysql-5.6.34 \
    --with-pdo-mysql=mysqlnd \
    --with-iconv-dir=/usr/local/libiconv \
    --with-freetype-dir \
    --with-jpeg-dir \
    --with-png-dir \
    --with-zlib \
    --with-libxml-dir=/usr \
    --enable-xml \
    --disable-rpath \
    --enable-bcmath \
    --enable-shmop \
    --enable-sysvsem \
    --enable-inline-optimization \
    --with-curl \
    --enable-mbregex \
    --enable-fpm \
    --enable-mbstring \
    --with-mcrypt \
    --with-gd \
    --enable-gd-native-ttf \
    --with-openssl \
    --with-mhash \
    --enable-pcntl \
    --enable-sockets \
    --with-xmlrpc \
    --enable-soap \
    --enable-short-tags \
    --enable-static \
    --with-xsl \
    --with-fpm-user=www \
    --with-fpm-group=www \
    --enable-ftp \
    --enable-opcache=no
    ##防错(以下信息可以不进行配置了)
    ln -s /application/mysql/lib/libmysqlclient.so.18  /usr/lib64/
    touch ext/phar/phar.phar
    make
    make install
    ln -s /application/php-5.5.32/ /application/php
    
    第三个里程：设置PHP程序配置文件
    php.ini php-fpm.ini
    cp php.ini-production /application/php-5.5.32/lib/
    cd /application/php/etc/
    cp php-fpm.conf.default php-fpm.con
    
    第四个里程：启动php程序服务
    /application/php/sbin/php-fpm
    netstat -lntup|grep php
    tcp        0      0 127.0.0.1:9000              0.0.0.0:*                   LISTEN      6251/php-fpm

## 进行软件直接的结合

nginx与php结合：编写nginx配置文件

```
location ~* .*\.(php|php5)?$ {
	fastcgi_pass  127.0.0.1:9000;
	fastcgi_index index.php;
	include fastcgi.conf;
}
	   
```

   php与mysql结合：编写php程序代码

```php
<?php
//$link_id=mysql_connect('主机名','用户','密码');
//mysql -u用户 -p密码 -h 主机
$link_id=mysql_connect('localhost','root','oldboy123') or mysql_error();
if($link_id){
	echo "mysql successful by oldboy !\n";
}else{
	echo mysql_error();
	}
?>
```

# 八、iptables防火墙网路安全实践配置

## 1、iptables防火墙概念介绍

Netfilter/Iptables（以下简称Iptables）是unix/linux自带的一款优秀且开放源代码的完全自由的基于包过滤
的防火墙工具，它的功能十分强大，使用非常灵活，可以对流入和流出服务器的数据包进行很精细的控制。

iptables是linux2.4及2.6内核中集成的服务。
iptables主要工作在OSI七层的二、三、四层，如果重新编译内核，iptables也可以支持7层控制

### iptables防火墙使用时名词概念理解


容器：装东西的器皿，docker容器技术，将镜像装在了一个系统中，这个系统就称为容器
    iptables称为一个容器---装着防火墙的表
    防火墙的表又是一个容器---装着防火墙的链
    防火墙的链也是一个容器---装着防火墙的规则
    iptables---表---链---规则

规则：防火墙一条一条安全策略
       1.	防火墙是层层过滤的，实际是按照配置规则的顺序从上到下，从前到后进行过滤的。
       2.	如果匹配上规则，即明确表示是阻止还是通过，数据包就不再向下匹配新的规则。
       3.	如果规则中没有明确表明是阻止还是通过的，也就是没有匹配规则，向下进行匹配，直到匹配默认规则得到明确的阻止还是通过。
       4.	防火墙的默认规则是所有规则执行完才执行的。

表和链说明：4表5链

Filter： 实现防火墙安全过滤功能
	 INPUT	         对于指定到本地套接字的包，即到达本地防火墙服务器的数据包    外面---->（门）房子iptables
	 FORWARD	  路由穿过的数据包，即经过本地防火墙服务器的数据包   外面-----（前门）房子（后门）---房子                    	 OUTPUT	     本地创建的数据包                                                外面<-----（门）房子iptables

 NAT：    实现将数据包中IP地址或者端口信息，内网到外网进行改写/外网到内网进行改写
	 PREROUTING     一进来就对数据包进行改变 在路由之前，进行数据包IP地址或端口信息的转换          
	 OUTPUT	         本地创建的数据包在路由之前进行改变   本地防火墙要出去的流量进行相应转换（了解）
	 POSTROUTING	在数据包即将出去时改变数据包信息     在路由之后，进行数据包IP地址或端口信息的转换
 Managle  对数据进行标记
 raw	     忽略不计

## 2、iptables防火墙操作实践练习

iptables  [-t table] SUBCOMMAND  chain  [matches....] [target]

链管理：

​	-N：新增一条自定义的链

​	-X：delete，删除自定义的空链

​	-P：policy,设置链的默认策略

​		ACCEPT：结束

​		DROP：丢弃

​		REJECT：拒绝

​		示例：~]# iptables -t filter -P FORWARD DROP

​	-E：rename，重命名自定义未被引用的链

规则管理：

​	-A：apend，追加

​	-I：insert 插入，默认为最开始处

​	-D：delete 删除

​		(1) 规则

​       (2)规则number

​	-R：replace，替换

​	-F：flush 清洗

​	-Z：zero，置0

​		iptab的每条规则都有两个计数器

​			(1)由本规则匹配到的所有的packets

​			(2)由本规则匹配到的所有的bytes

​	-S: seletcted,以iptables-sava命令格式显示链上的规则

查看：

​	-L：list,列出规则

​    -n：num以数字格式显示地址和端口

​    -v：verbose，详细信息

​    -x：exactly，显示计数器的精确值，而非换算后的结果

​	--line-numbers：行编号，显示链上的行编号

匹配条件

​      [!取反]-s，--source address[/mask]

​      [!取反]-d，--Destination address[/mask]

​      [!取反]-i，--in-interface name：限制报文流入的接口

​      [!取反]-o，--out-interface name：限制报文流出的接口 

​       ~]# iptables -A INPUT -s 192.168.31.1/32 -j DROP

扩展匹配：经由扩展模块引入的匹配机制  -m matchname

隐式扩展：可以不使用-m选项专门加载相应模块，前提是要使用-p选项可匹配何种协议

​	 [!取反]-p{tcp|udp|icmp}：限制协议

 tcp：隐含指明了‘-m tcp’，有专用选项

​		[!] --source-port,--sport  port[:port]: 匹配报文中的TCP源端口，可以是范围端口

​		[!] --destination-port,--dport  port[:port]: 匹配报文中的TCP目标端口，可以是范围端口

​		[!]--tcp-flags mask comp: 检查报文中mask指明的tcp标志位，这些标志位comp中必须为1

​			--tcp-flags  syn,fin,ack,rst  syn 三次握手的第一次

​		[!] --syn：相当于 --tcp-flags  syn,fin,ack,rst  syn

udp：隐含指明了‘-m udp’，有专用选项

icmp:隐含指明了‘-m icmp’，有专用选项

​		[!]  --icmp-type {type[/code]|typename}

显式扩展：需要加载扩展模块

multiport：多端口匹配，以离散方式定义多端口匹配，最多可指定15个端口

​    [!] --source-ports,--sports port[,port|,port:port]...

​    [!] --destination-ports,--dports port[,port|,port:port]...

​    [!] --ports port[,port|,port:port]...

```bash
示例：]# iptables -I INPUT -s 0/0 -d 192.168.31.238  -p tcp -m multiport --dports 22,80 -j ACCEPT
```

 iprange：指明一段连续的ip地址范围作为源地址或目标地址匹配

​	[!] --src-range from[-to]

​	[!] --dst-range from[-to]

```bash
	示例：]# iptables -A INPUT  -d 0/0 -j ACCEPT -m iprange --src-range 192.168.31.5-192.168.31.222
```

string：对报文中的应用层数据做字符串匹配检测：

​	--algo {bm|kmp}

​	[!] --string  pattern：给定检测字符串模式

​	[!] --hex-string  pattern：给定要检测的字符串模式

```bash
	示例：]# iptables -I OUTPUT -s 192.168.31.238 -d 0/0 -p tcp --sport 80 -m string --algo bm --string "old" -j DROP
```

time：根据收到报文的时间/日期与指定的时间/日期范围进行匹配

​	--datestart YYYY[-MM[-DD[Thh[:mm[:ss]]]]]

​	--datestop YYYY[-MM[-DD[Thh[:mm[:ss]]]]]

​	--timestart hh:mm[:ss]

​	--timestop hh:mm[:ss]

​	[!] --monthdays day[,day...]

​	[!] --weekdays day[,day...]

```bash
	示例：]# iptables -I INPUT -d 192.168.31.238 -p tcp --dport 80 -m iprange --src-range 192.168.31.1-192.168.31.200 -m time --timestart 09:00 --timestop 18:00 -j REJECT
```

1）iptables防火墙配置初始化

```bash
/etc/init.d/iptables start
chkconfig iptables on
iptables -F              --- 清除防火墙默认规则
iptables -X              --- 清除防火墙自定义链
iptables -Z              --- 清除防火墙技术器信息
```

2）iptables防护墙信息查看方法

```bash
/etc/init.d/iptables status
iptables -L              --- -L 以列表形式显示所有规则信息
iptables -L -n           --- -n 以数字形式显示IP地址或端口信息，不要转换为字符串显示
iptables -t nat -L -n    --- -t 表示指定查看或者配置相应的表
iptables -L -n -v        --- -v 表示显示详细规则信息，包含匹配计数器数值信息
iptables  -L -n --line-number      --- --line-number 显示规则序号信息
```

3）iptables防火墙端口规则配置：

```bash
实践01：阻止用户访问服务器的22端口
iptables -t filter -A INPUT -p tcp --dport 22 -j DROP   --- -A 表示添加规则到相应链上，默认表示添加规则到结尾
iptables -t filter -D INPUT -p tcp --dport 22 -j DROP   --- -D 表示删除规则从相应链上。
iptables -t filter -D INPUT 规则序号
iptables -t filter -I INPUT -p tcp --dport 22 -j DROP   --- -I 表示插入规则到相应链上，默认表示插入规则到首部
iptables -t filter -I INPUT 3 -p tcp --dport 22 -j DROP --- 指定规则插入位置
iptables -t filter -R INPUT 6 -p tcp --dport 8080 -j DROP   --- -R 指定将配置好的规则信息进行替换
```

总结防火墙参数信息：
	   -A   --- 表示将规则添加到指定链上
	   -I   --- 表示将规则插入到指定链上
	   -D   --- 表示将规则从指定链上删除
	   -R   --- 表示将规则信息进行修改
	   -p   --- 指定相应服务协议信息（tcp udp icmp all）
	        --dport    --- 表示指定目标端口信息
			--sport    --- 表示指定源端口号信息
	   -j   --- 指定对相应匹配规则执行什么操作（ACCEPT DROP* REJECT）
	   

实践02：阻止相应网段主机访问服务端指定端口服务

```bash
10.0.0.0/24 -- 22端口（阻止）
iptables -t filter -A INPUT -s 10.0.0.0/24 -p tcp --dport 22 -j DROP   
iptables -t filter -A INPUT -s 10.0.0.9 -p tcp --dport 22 -j DROP 
iptables -t filter -A INPUT -i eth0 -s 10.0.0.9 -p tcp --dport 22 -j DROP 
```

	   总结参数信息：
	   -s   --- 指定匹配的源地址网段信息，或者匹配的主机信息
	   -d   --- 指定匹配的目标地址网段信息，或者匹配的主机信息
	   -i   --- 指定匹配的进入流量接口信息 只能配置在INPUT链上
	   -o   --- 指定匹配的发出流量接口信息 只能配置在OUTPUT链上
实践03：除了莫个地址可以访问22端口之外，其余地址都不能访问

```bash
10.0.0.1 10.0.0.253    10.0.0.9（只允许）
iptables -t filter -A INPUT -s 10.0.0.9 -p tcp --dport 22 -j ACCEPT
iptables -t filter -A INPUT -s 10.0.0.0/24 -p tcp --dport 22 -j DROP 
iptables -t filter -A INPUT ! -s 10.0.0.9 -p tcp --dport 22 -j ACCEPT
通过利用 ！进行规则取反，进行策略控制
```
 实践04：指定阻止访问多个端口服务

```BASH
 22--80 22,24,25
 iptables -A INPUT -s 10.0.0.9 -p tcp --dport 22:80 -j DROP    --- 匹配连续的端口号访问
 iptables -A INPUT -s 10.0.0.9 -m multiport -p tcp --dport 22,24,25 -j DROP   --- 匹配不连续的端口号访问
```

   总结参数信息：
	   -m   --- 指定应用扩展模块参数
	        multiport   --- 可以匹配多个不连续端口信息

​      实现ping功能测试链路是否正常，基于icmp协议实现的

 icmp协议有多种类型：
       icmp-type 8：请求类型  icmp-type 0：回复类型	   

 情况一：实现禁止主机访问防火墙服务器（禁ping）

```BASH
 iptables -A INPUT -p icmp --icmp-type 8 -j DROP
 iptables -A OUTPUT -p icmp --icmp-type 0 -j DROP
```

情况二：实现禁止防火墙访问主机服务器（禁ping）

```BASH
iptables -A OUTPUT -p icmp --icmp-type 8 -j DROP
iptables -A INPUT -p icmp --icmp-type 0 -j DROP
```
 默认情况：所有icmp类型都禁止

```BASH
iptables -A INPUT -p icmp -m icmp --icmp-type any -j DROP
iptables -A OUTPUT -p icmp -m icmp --icmp-type any -j DROP
```
实现防火墙状态机制控制

NEW: 发送数据包里面控制字段为syn=1，发送第一次握手的数据包
ESTABLISHED: 请求数据包发出之后，响应回来的数据包称为回复的包
RELATED: 基于一个连接，然后建立新的连接
INVALID: 无效的的数据包，数据包结构不符合正常要求的

```BASH
 iptables -A INPUT -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
```

## 3、 企业当中应用防火墙方法

​    项目：部署一个最安全的企业级防火墙（案例）
​    两种思想：针对默认规则而言。
​    逛公园：黑名单
​    1、默认规则默认是允许的状态。
​    看电影：白名单（更安全，推荐配置）
​    2、默认规则默认是不允许的状态。更安全。
​    看电影的思想更安全。

1）保存防火墙配置文件信息

```bash
cp /etc/sysconfig/iptables{,.bak}
```
2）清除配置规则

```bash
iptables -F    <- 清空iptables所有规则信息（清除filter）
iptables -X    <- 清空iptables自定义链配置（清除filter）
iptables -Z    <- 清空iptables计数器信息（清除filter）
```
3）别把自己踢出到门外

```bash
iptables -A INPUT -s 10.0.0.1 -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -s 10.0.0.0/24 -p tcp --dport 22 -j ACCEPT
```
4）配置防火墙filter上各个链的默认规则

```bash
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT
```
-P   --- 指定相应链的默认规则策略，是允许还是阻止

5）允许iptables服务端ping自己的网卡地址

```bash
iptables -A INPUT -i lo -j ACCEPT   --- 让自己可以ping自己
```

 6）指定外网可以访问的端口信息

```bash
iptables -A INPUT -p tcp -m multiport --dport 80,443 -j ACCEPT 
```

7）企业中内网之间不要配置防火墙策略

```bash
iptables -A INPUT -s 172.16.1.0/24 -j ACCEPT  --- 允许架构内部服务进行访问
```

 8）企业之间有合作关系的，不要将友商的网络禁止（主要经常改动）

```bash
iptables -A INPUT -s 10.0.1.0/24 -j ACCEPT    --- 允许一些合作企业的外网服务器进行访问
iptables -A INPUT -s 10.0.2.0/24 -j ACCEPT
```
9）如果防火墙上配置了FTP服务，需要配置网络状态机制

```bash
 iptables -A INPUT  -m state --state ESTABLISHED,RELATED -j ACCEPT  --- 允许web服务与ftp服务器建立连接
```

10）实现iptables策略配置永久保存

```bash
①. 利用防火墙启动脚本命令参数，实现永久保存
/etc/init.d/iptables save

②. 利用防火墙配置信息保存命令，实现永久保存
iptables-save >/etc/sysconfig/iptables
```
实例拓展：避免自己被踢出门外
       1. 去机房重启系统或者登陆服务器删除刚才的禁止规则
       2. 让机房人员重启服务器或者让机房人员拿用户密码登录进去
       3. 通过服务器的远程管理卡管理（推荐）
       4. 先写一个定时任务，每5分钟就停止防火墙
       5. 测试环境测试好，写成脚本，批量执行

## 4、防火墙nat表的配置实践

iptables NAT:（配置NAT表示就是配置以下两个链）
       1. postrouting（内网---外网-NAT  源私网IP地址---源公网IP地址）
          路由之后，进行地址映射转换，把源地址进行转换（源私网地址==>源公网地址）
       2. prerouting（外网---内网-NAT  目标公网IP地址---目标私网IP地址  映射目标端口）
          路由之前，进行地址映射转换，把目标地址进行转换（目标公网地址==>目标变为私网地址）

```bash
~]# iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -j SNAT --to-source 192.168.31.238
```

MASQUERADE：如果转换的外网IP是动态的可使用MASQUERADE

实践一：iptables实现共享上网方法(postrouting)

第一个历程：配置内网服务器，设置网关地址

```bash
/etc/init.d/iptables stop    --- 内网服务器停止防火墙服务
ifdown eth0                  --- 模拟关闭内网服务器外网网卡
setup                        --- 修改内网网卡网关和DNS地址信息
[root@oldboyedu42-lnb-02 ~]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
172.16.1.0      0.0.0.0         255.255.255.0   U     0      0        0 eth1
169.254.0.0     0.0.0.0         255.255.0.0     U     1003   0        0 eth1
0.0.0.0         172.16.1.7      0.0.0.0         UG    0      0        0 eth1
说明：内网服务器网关地址指定为共享上网服务器内网网卡地址
```

第二个历程：配置共享上网服务器，开启共享上网服务器路由转发功能

```bash
[root@oldboyedu42-lnb-02 ~]# vim /etc/sysctl.conf 
[root@oldboyedu42-lnb-02 ~]# sysctl -p
net.ipv4.ip_forward = 1
```

第三个历程：配置共享上网服务器，实现内网访问外网的NAT映射

```bash
iptables -t nat -A POSTROUTING -s 172.16.1.0/24 -o eth0 -j SNAT --to-source 10.0.0.7
-s 172.16.1.0/24		  --- 指定将哪些内网网段进行映射转换
-o eth0				      --- 指定在共享上网哪个网卡接口上做NAT地址转换
-j SNAT                   --- 将源地址进行转换变更
-j DNAT                   --- 将目标地址进行转换变更
--to-source ip地址         --- 将源地址映射为什么IP地址
--to-destination ip地址    --- 将目标地址映射为什么IP地址
```

 扩展如果开启：forward默认drop策略，如果配置forward链

```bash
iptables -A FORWARD -i eth1 -s 172.16.1.0/24 -j ACCEPT
iptables -A FORWARD -o eth0 -s 172.16.1.0/24 -j ACCEPT
iptables -A FORWARD -i eth0 -d 172.16.1.0/24 -j ACCEPT
iptables -A FORWARD -o eth1 -d 172.16.1.0/24 -j ACCEPT
```

 实践二：iptables实现共享上网方法(postrouting)

```bash
iptables -t nat -A POSTROUTING -s 172.16.1.0/24 -o eth0 -j MASQUERADE		<- 伪装共享上网
```

   说明：在企业中如何没有固定外网IP地址，可以采取以上伪装映射的方式进行共享上网

   总结：配置映射方法
   01. 指定哪些网段需要进行映射    -s 172.16.1.0/24 
   02. 指定在哪做映射               -o eth0
   03. 用什么方法做映射             -j SNAT/DNAT
   04. 映射成什么地址               --to-source  ip地址/--to-destination ip地址

   实践三：iptables实现外网IP的端口映射到内网IP的端口

   需求：将网关的IP和9000端口映射到内网服务器的22端口
   端口映射 10.0.0.7:9000 -->172.16.1.8:22  
   实现命令：

```bash
   iptables -t nat -A PREROUTING -d 10.0.0.7  -i eth0 -p tcp --dport 9000 -j DNAT --to-destination 172.16.1.8:22
```


