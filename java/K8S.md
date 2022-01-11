# 一 Kubernetes基础概念

![image-20220106170132193](\images\image-20220106170132193.png)

kubernetes具有以下特性：

- **服务发现和负载均衡**
  Kubernetes 可以使用 DNS 名称或自己的 IP 地址公开容器，如果进入容器的流量很大， Kubernetes 可以负载均衡并分配网络流量，从而使部署稳定。
- **存储编排**
  Kubernetes 允许你自动挂载你选择的存储系统，例如本地存储、公共云提供商等。

- **自动部署和回滚**
  你可以使用 Kubernetes 描述已部署容器的所需状态，它可以以受控的速率将实际状态 更改为期望状态。例如，你可以自动化 Kubernetes 来为你的部署创建新容器， 删除现有容器并将它们的所有资源用于新容器。
- **自动完成装箱计算**
  Kubernetes 允许你指定每个容器所需 CPU 和内存（RAM）。 当容器指定了资源请求时，Kubernetes 可以做出更好的决策来管理容器的资源。

- **自我修复**
  Kubernetes 重新启动失败的容器、替换容器、杀死不响应用户定义的 运行状况检查的容器，并且在准备好服务之前不将其通告给客户端。
- **密钥与配置管理**
  Kubernetes 允许你存储和管理敏感信息，例如密码、OAuth 令牌和 ssh 密钥。 你可以在不重建容器镜像的情况下部署和更新密钥和应用程序配置，也无需在堆栈配置中暴露密钥

Kubernetes 为你提供了一个可弹性运行分布式系统的框架。 Kubernetes 会满足扩展要求、故障转移、部署模式等。 例如，Kubernetes 可以轻松管理系统的 Canary 部署。

## 组件建构

![image-20220106170327243](\images\image-20220106170327243.png)

### 1、控制平面组件（Control Plane Components）

控制平面的组件对集群做出全局决策(比如调度)，以及检测和响应集群事件（例如，当不满足部署的 `replicas` 字段时，启动新的 [pod](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/)）。

控制平面组件可以在集群中的任何节点上运行。 然而，为了简单起见，设置脚本通常会在同一个计算机上启动所有控制平面组件， 并且不会在此计算机上运行用户容器。 

#### kube-apiserver

API 服务器是 Kubernetes [控制面](https://kubernetes.io/zh/docs/reference/glossary/?all=true#term-control-plane)的组件， 该组件公开了 Kubernetes API。 API 服务器是 Kubernetes 控制面的前端。

Kubernetes API 服务器的主要实现是 [kube-apiserver](https://kubernetes.io/zh/docs/reference/command-line-tools-reference/kube-apiserver/)。 kube-apiserver 设计上考虑了水平伸缩，也就是说，它可通过部署多个实例进行伸缩。 你可以运行 kube-apiserver 的多个实例，并在这些实例之间平衡流量。

#### etcd

etcd 是兼具一致性和高可用性的键值数据库，可以作为保存 Kubernetes 所有集群数据的后台数据库。

 Kubernetes 集群的 etcd 数据库通常需要有个备份计划。

#### kube-scheduler

控制平面组件，负责监视新创建的、未指定运行节点（node）的 Pods，选择节点让 Pod 在上面运行。

调度决策考虑的因素包括单个 Pod 和 Pod 集合的资源需求、硬件/软件/策略约束、亲和性和反亲和性规范、数据位置、工作负载间的干扰和最后时限。

#### kube-controller-manager

在主节点上运行 控制器 的组件。

从逻辑上讲，每个控制器都是一个单独的进程， 但是为了降低复杂性，它们都被编译到同一个可执行文件，并在一个进程中运行。

这些控制器包括:

- 节点控制器（Node Controller）: 负责在节点出现故障时进行通知和响应
- 任务控制器（Job controller）: 监测代表一次性任务的 Job 对象，然后创建 Pods 来运行这些任务直至完成

- 端点控制器（Endpoints Controller）: 填充端点(Endpoints)对象(即加入 Service 与 Pod)
- 服务帐户和令牌控制器（Service Account & Token Controllers）: 为新的命名空间创建默认帐户和 API 访问令牌

#### cloud-controller-manager

云控制器管理器是指嵌入特定云的控制逻辑的 控制平面组件。 云控制器管理器允许您链接集群到云提供商的应用编程接口中， 并把和该云平台交互的组件与只和您的集群交互的组件分离开。

`cloud-controller-manager` 仅运行特定于云平台的控制回路。 如果你在自己的环境中运行 Kubernetes，或者在本地计算机中运行学习环境， 所部署的环境中不需要云控制器管理器。

与 `kube-controller-manager` 类似，`cloud-controller-manager` 将若干逻辑上独立的 控制回路组合到同一个可执行文件中，供你以同一进程的方式运行。 你可以对其执行水平扩容（运行不止一个副本）以提升性能或者增强容错能力。

下面的控制器都包含对云平台驱动的依赖：

- 节点控制器（Node Controller）: 用于在节点终止响应后检查云提供商以确定节点是否已被删除
- 路由控制器（Route Controller）: 用于在底层云基础架构中设置路由

- 服务控制器（Service Controller）: 用于创建、更新和删除云提供商负载均衡器

### 2、Node 组件 

节点组件在每个节点上运行，维护运行的 Pod 并提供 Kubernetes 运行环境。

#### kubelet

一个在集群中每个节点（node上运行的代理。 它保证容器containers)都 运行在 [Pod](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/) 中。

kubelet 接收一组通过各类机制提供给它的 PodSpecs，确保这些 PodSpecs 中描述的容器处于运行状态且健康。 kubelet 不会管理不是由 Kubernetes 创建的容器。

#### kube-proxy

[kube-proxy](https://kubernetes.io/zh/docs/reference/command-line-tools-reference/kube-proxy/) 是集群中每个节点上运行的网络代理， 实现 Kubernetes [服务（Service）](https://kubernetes.io/zh/docs/concepts/services-networking/service/) 概念的一部分。

kube-proxy 维护节点上的网络规则。这些网络规则允许从集群内部或外部的网络会话与 Pod 进行网络通信。

如果操作系统提供了数据包过滤层并可用的话，kube-proxy 会通过它来实现网络规则。否则， kube-proxy 仅转发流量本身。

![img](https://cdn.nlark.com/yuque/0/2021/png/1613913/1626605698082-bf4351dd-6751-44b7-aaf7-7608c847ea42.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_37%2Ctext_YXRndWlndS5jb20gIOWwmuehheiwtw%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10)

### 3、Pod

运行中的一组容器，Pod是kubernetes中应用的最小单位

Pod分为自主pod和控制器管理的pod

#### pod控制器类型

##### ReplicationController & ReplicaSet & Deployment

ReplicationController 用来确保容器应用的副本数始终保持在用户定义的副本数，即如果
有容器异常退出，会自动创建新的 Pod 来替代；而如果异常多出来的容上并且



ReplicaSet 跟 ReplicationController 没有本质的不同，只是名字不一样，并且
ReplicaSet 支持集合式的 selector



虽然 ReplicaSet 可以独立使用，但一般还是建议使用 Deployment 来自动管理
ReplicaSet ，这样就无需担心跟其他机制的不兼容问题（比如 ReplicaSet 不支持
rolling-update 但 Deployment 支持

##### Deployment（ReplicaSet）


Deployment 为 Pod 和 ReplicaSet 提供了一个声明式定义 (declarative) 方法，用来替
代以前的 ReplicationController 来方便的管理应用。典型的应用场景包括：

​	定义 Deployment 来创建 Pod 和 ReplicaSet
​	滚动升级和回滚应用
​	扩容和缩容
​	暂停和继续 Deployment

##### HPA（HorizontalPodAutoScale）

HPA（HorizontalPodAutoScale）
Horizontal Pod Autoscaling 仅适用于 Deployment 和 ReplicaSet ，在 V1 版本中仅支持根据 Pod
的 CPU 利用率扩所容，在 v1alpha 版本中，支持根据内存和用户自定义的 metric 扩缩容

##### StatefulSet

StatefulSet 是为了解决有状态服务的问题（对应 Deployments 和 ReplicaSets 是为无状态服务而设
计），其应用场景包括：

稳定的持久化存储，即 Pod 重新调度后还是能访问到相同的持久化数据，基于 PVC 来实现
稳定的网络标志，即 Pod 重新调度后其 PodName 和 HostName 不变，基于 Headless Service
（即没有 Cluster IP 的 Service ）来实现

有序部署，有序扩展，即 Pod 是有顺序的，在部署或者扩展的时候要依据定义的顺序依次依次进
行（即从 0 到 N-1，在下一个 Pod 运行之前所有之前的 Pod 必须都是 Running 和 Ready 状态），
基于 init containers 来实现

有序收缩，有序删除（即从 N-1 到 0）

##### DaemonSet

DaemonSet 确保全部（或者一些）Node 上运行一个 Pod 的副本。当有 Node 加入集群时，也会为他们
新增一个 Pod 。当有 Node 从集群移除时，这些 Pod 也会被回收。删除 DaemonSet 将会删除它创建
的所有 Pod

使用 DaemonSet 的一些典型用法：

​	运行集群存储 daemon，例如在每个 Node 上运行 glusterd、ceph。
​    在每个 Node 上运行日志收集 daemon，例如fluentd、logstash。
​    在每个 Node 上运行监控 daemon，例如 Prometheus Node Exporte

##### Job，Cronjob

Job 负责批处理任务，即仅执行一次的任务，它保证批处理任务的一个或多个 Pod 成功结束

Cron Job 管理基于时间的 Job，即：
	 在给定时间点只运行一次
	 周期性地在给定时间点运行

### 4、网络通讯方式

Kubernetes 的网络模型假定了所有 Pod 都在一个可以直接连通的扁平的网络空间中，这在
GCE（Google Compute Engine）里面是现成的网络模型，Kubernetes 假定这个网络已经存在。
而在私有云里搭建 Kubernetes 集群，就不能假定这个网络已经存在了。我们需要自己实现这
个网络假设，将不同节点上的 Docker 容器之间的互相访问先打通，然后运行 Kubernetes

同一个 Pod 内的多个容器之间：lo
各 Pod 之间的通讯：Overlay Network
Pod 与 Service 之间的通讯：各节点的 Iptables 规则

#### 网络解决方案 Kubernetes + Flannel

lannel 是 CoreOS 团队针对 Kubernetes 设计的一个网络规划服务，简单来说，它的功能是
让集群中的不同节点主机创建的 Docker 容器都具有全集群唯一的虚拟IP地址。而且它还能在
这些 IP 地址之间建立一个覆盖网络（Overlay Network），通过这个覆盖网络，将数据包原封
不动地传递到目标容器内

![image-20220110151250366](\images\image-20220110151250366.png)

ETCD 之 Flannel 提供说明：

	> 存储管理 Flannel 可分配的 IP 地址段资源
	> 监控 ETCD 中每个 Pod 的实际地址，并在内存中建立维护 Pod 节点路由表

同一个 Pod 内部通讯：同一个 Pod 共享同一个网络命名空间，共享同一个 Linux 协议栈

Pod1 至 Pod2

> ​	Pod1 与 Pod2 不在同一台主机，Pod的地址是与docker0在同一个网段的，但docker0网段与宿主机网卡是两个完全不同的IP网段，并且不同Node之间的通信只能通过宿主机的物理网卡进行。将Pod的IP和所在Node的IP关联起来，通过这个关联让Pod可以互相访问
> ​	Pod1 与 Pod2 在同一台机器，由 Docker0 网桥直接转发请求至 Pod2，不需要经过 Flannel

Pod 至 Service 的网络：目前基于性能考虑，全部为 iptables 维护和转发

Pod 到外网：Pod 向外网发送请求，查找路由表, 转发数据包到宿主机的网卡，宿主网卡完成路由选择后，iptables执行Masquerade，把源 IP 更改为宿主网卡的 IP，然后向外网服务器发送请求

外网访问 Pod：Service

![image-20220110152432212](\images\image-20220110152432212.png)



# 二 安装K8S

## 1、系统初始化

### 设置系统主机名以及Host文件的相互解析

```
[root@k8s-master01 ~]# hostnamectl set-hostname k8s-master01
```

### 安装依赖包

```
yum install -y conntrack ntpdate ntp ipvsadm ipset jq iptables curl sysstat libseccomp wget vim net-tools git
```

### 设置防火墙为Iptables并设置空规则

```
[root@k8s-master01 ~]# systemctl stop firewalld && systemctl disable firewalld
[root@k8s-master01 ~]# yum -y install iptables-services && systemctl start iptables
[root@k8s-master01 ~]# systemctl start iptables
[root@k8s-master01 ~]# systemctl enable iptables
[root@k8s-master01 ~]# iptables -F && service iptables save
```

### 关闭 SELINUX

```
[root@k8s-master01 ~]# swapoff -a && sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
[root@k8s-master01 ~]# setenforce 0 && sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config
```

```
cat > kubernetes.conf <<EOF
net.bridge.bridge-nf-call-iptables=1
net.bridge.bridge-nf-call-ip6tables=1
net.ipv4.ip_forward=1 
net.ipv4.tcp_tw_recycle=0 
vm.swappiness=0 # 禁止使用 swap 空间，只有当系统 OOM 时才允许使用它
vm.overcommit_memory=1 # 不检查物理内存是否够用 
vm.panic_on_oom=0 # 开启OOM
fs.inotify.max_user_instances=8192 
fs.inotify.max_user_watches=1048576
fs.file-max=52706963
fs.nr_open=52706963 
net.ipv6.conf.all.disable_ipv6=1 
net.netfilter.nf_conntrack_max=2310720
EOF

cp kubernetes.conf /etc/sysctl.d/kubernetes.conf
modprobe br_netfilter
sysctl -p /etc/sysctl.d/kubernetes.conf
```

### 调整系统时区

```
# 设置系统时区为 中国/上海
timedatectl set-timezone Asia/Shanghai
# 将当前的 UTC 时间写入硬件时钟
timedatectl set-local-rtc 0
# 重启依赖于系统时间的服务
systemctl restart rsyslog
systemctl restart crond
```

### 关闭系统不需要服务

```
[root@k8s-master01 ~]# systemctl stop postfix && systemctl disable postfix
```

### 设置 rsyslogd 和 systemd journald

```
[root@k8s-master01 ~]# mkdir /var/log/jounal #持久化保存日志目录
[root@k8s-master01 ~]# mkdir /etc/systemd/journald.conf.d
cat > /etc/systemd/journald.conf.d/99-prophet.conf <<EOF
[Journal]
# 持久化保存到磁盘
Storage=persistent
# 压缩历史日志
Compress=yes
SyncIntervalSec=5m
RateLimitInterval=30s
RateLimitBurst=1000
# 最大占用空间 10G
SystemMaxUse=10G
# 单日志文件最大 200M
SystemMaxFileSize=200M
# 日志保存时间 2 周
MaxRetentionSec=2week
# 不将日志转发到 syslog
ForwardToSyslog=no
EOF
[root@k8s-master01 ~]# systemctl restart systemd-journald
```

### 升级系统内核为 4.44

关闭系统不需要服务
设置 rsyslogd 和 systemd journald
升级系统内核为 4.44
CentOS 7.x 系统自带的 3.10.x 内核存在一些 Bugs，导致运行的 Docker、Kubernetes 不稳定，例如： rpm -Uvh
http://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm

```
rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-3.el7.elrepo.noarch.rpm
# 安装完成后检查 /boot/grub2/grub.cfg 中对应内核 menuentry 中是否包含 initrd16 配置，如果没有，再安装一次！
[root@k8s-master01 ~]# yum --enablerepo=elrepo-kernel install -y kernel-lt
# 设置开机从新内核启动
grub2-set-default 'CentOS Linux (4.4.189-1.el7.elrepo.x86_64) 7 (Core)'
```

## 2、kubeadm部署安装

```
modprobe br_netfilter
cat > /etc/sysconfig/modules/ipvs.modules <<EOF
#!/bin/bash
modprobe -- ip_vs
modprobe -- ip_vs_rr
modprobe -- ip_vs_wrr
modprobe -- ip_vs_sh
modprobe -- nf_conntrack_ipv4
EOF
chmod 755 /etc/sysconfig/modules/ipvs.modules && bash /etc/sysconfig/modules/ipvs.modules &&
lsmod | grep -e ip_vs -e nf_conntrack_ipv4
```

![image-20220106201119447](\images\image-20220106201119447.png)

### 安装 Docker 软件

```
[root@k8s-master01 ~]# yum install -y yum-utils device-mapper-persistent-data lvm2
[root@k8s-master01 ~]# yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
[root@k8s-master01 ~]# yum update -y && yum install -y docker-ce
[root@k8s-master01 docker]# mkdir /etc/docker
# 配置 daemon.
cat > /etc/docker/daemon.json <<EOF
{
"exec-opts": ["native.cgroupdriver=systemd"],
"log-driver": "json-file",
"log-opts": {
"max-size": "100m"
}
}
EOF
mkdir -p /etc/systemd/system/docker.service.d
# 重启docker服务
systemctl daemon-reload && systemctl restart docker && systemctl enable docker
```

如果docker启动不起来

![img](https://img2018.cnblogs.com/blog/934739/201901/934739-20190109092526136-1606452937.png)

还有其他报错信息，解决方案大致相同，网上很多是说修改daemon.json，改成国内docker源，但是却没什么用，出现这种错误，docker卸载都卸载不了，当时郁闷的一批，只能重启下网卡，

然后把docker文件全部干掉，这是我当时能想到的解决方案了，自己做开发测试还好，生产千万别乱搞。(注：此方案为最终解决方案，使用此方案时，一定要参考其他方案能不能解决你的问题)

```
service network restart
```

重新开机，然后删除docker安装包(注：做如下操作时，一定要提前备份，不然你docker容器中数据会全部丢失)

```
rm -rf /var/lib/docker
```

 然后重新安装下docker

```
sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
sudo yum install docker-ce
```

为避免再次出现问题，我们做如下配置

配置DOCKER_HOST

```
sudo vim /etc/profile.d/docker.sh
```

添加下面内容：

```
export DOCKER_HOST=tcp://localhost:2375  
```

使配置文件生效

```
source /etc/profile
source /etc/bashrc
```

配置启动文件

```
sudo vim /lib/systemd/system/docker.service
```

修改下面语句

```
ExecStart=/usr/bin/dockerd -H unix://
```

修改为：

```
ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock -H tcp://0.0.0.0:7654
```

重载配置和重启

```
sudo systemctl daemon-reload
sudo systemctl restart docker.service
```

查看

```
docker version
```

![img](https://img2018.cnblogs.com/blog/934739/201901/934739-20190109095001000-1462270554.png)

说明已经正常。



### 安装 Kubeadm （主从配置）

```
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=http://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=http://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF

yum -y install kubeadm-1.15.1 kubectl-1.15.1 kubelet-1.15.1
systemctl enable kubelet.service
```

### 初始化主节点

#注意初始化K8S需要去Google拉取镜像这里要先导入需要的镜像

kubeadm-basic.images.tar

```
[root@k8s-master01 ~]# tar zxvf kubeadm-basic.images.tar.gz
kubeadm-basic.images/
kubeadm-basic.images/coredns.tar
kubeadm-basic.images/etcd.tar
kubeadm-basic.images/pause.tar
kubeadm-basic.images/apiserver.tar
kubeadm-basic.images/proxy.tar
kubeadm-basic.images/kubec-con-man.tar
kubeadm-basic.images/scheduler.tar
```

load image脚本

```bash
[root@k8s-master01 ~]# vim load-images.sh
#!/bin/bash

ls /root/kubeadm-basic.images > /tmp/image-list.txt

cd /root/kubeadm-basic.images

for i in $( cat /tmp/image-list.txt )
dot
   docker load -i $i
done

rm -rf /tmp/image-list.txt
```

![image-20220108115131255](D:\studyDoc\java\images\image-20220108115131255.png)

```
kubeadm config print init-defaults > kubeadm-config.yaml
# 更改后的配置文件
apiVersion: kubeadm.k8s.io/v1beta2
bootstrapTokens:
- groups:
  - system:bootstrappers:kubeadm:default-node-token
  token: abcdef.0123456789abcdef
  ttl: 24h0m0s
  usages:
  - signing
  - authentication
kind: InitConfiguration
localAPIEndpoint:
  advertiseAddress: 192.168.31.10
  bindPort: 6443
nodeRegistration:
  criSocket: /var/run/dockershim.sock
  name: k8s-master01
  taints:
  - effect: NoSchedule
    key: node-role.kubernetes.io/master
---
apiServer:
  timeoutForControlPlane: 4m0s
apiVersion: kubeadm.k8s.io/v1beta2
certificatesDir: /etc/kubernetes/pki
clusterName: kubernetes
controllerManager: {}
dns:
  type: CoreDNS
etcd:
  local:
    dataDir: /var/lib/etcd
imageRepository: k8s.gcr.io
kind: ClusterConfiguration
kubernetesVersion: v1.15.1
networking:
  dnsDomain: cluster.local
  serviceSubnet: 10.96.0.0/12
  podSubnet: 10.244.0.0/16
scheduler: {}
---
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
featureGates:
  SupportIPVSProxyMode: true
mode: ipvs

kubeadm init --config=kubeadm-config.yaml --experimental-upload-certs | tee kubeadm-init.log

```

![image-20220108120710672](\images\image-20220108120710672.png)

```
[root@k8s-master01 ~]# mkdir -p $HOME/.kube
[root@k8s-master01 ~]# sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
[root@k8s-master01 ~]#  sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

![image-20220108121030622](\images\image-20220108121030622.png)

```
[root@k8s-master01 install-k8s]# mv kubeadm-init.log kubeadm-config.yaml install-k8s/core
```

### 后期加入NODE

由于kubeadm前期安装完成后join使用 token 过期时间为(24小时过期)，所以需要重新生成token

重新生成新的token

```
[root@k8s-master01 core]# kubeadm token create
rwy6yz.eczjz9g7zq5bztts
```

查看是否存在有效的 token 值

```
[root@k8s-master01 core]# kubeadm token list
```

![image-20220110194550072](\images\image-20220110194550072.png)

获取CA证书 sha256 编码 hash 值

```
[root@k8s-master01 core]# openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'
c3d65da426f2df824be6a08897ff6e6cf7e0e1240d744679542610873f846f5f
```

执行node节点加入c

```
kubeadm join 192.168.31.10:6443 --token atyqdb.ny54v98ew1hf5a21     --discovery-token-ca-cert-hash sha256:c3d65da426f2df824be6a08897ff6e6cf7e0e1240d744679542610873f846f5f  --v=2
```

如何删除节点（master端）

```
[root@master ~]# kubectl drain node03.linux.com --delete-local-data --force --ignore-daemonsets
[root@master ~]# kubectl delete node node03.linux.com
```



### 部署网络

```
kubectl apply -f 
wget https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
[root@k8s-master01 flannel]# kubectl create -f kube-flannel.yml
```

![image-20220108123136373](\images\image-20220108123136373.png)

![image-20220108123307568](\images\image-20220108123307568.png)

![image-20220108123400317](D:\studyDoc\java\images\image-20220108123400317.png)

### 【kubeadm初始化报错】failed to run Kubelet: misconfiguration: kubelet cgroup driver: "cgroupfs" is different from docker cgroup driver: "systemd" 

![image-20220109130940456](\images\image-20220109130940456.png)

分别修改docker与控制平台的kubelet为systemd 【官方推荐】

```
[root@k8s-master01 manifests]# vim /var/lib/kubelet/kubeadm-flags.env
KUBELET_KUBEADM_ARGS="--cgroup-driver=systemd --network-plugin=cni --pod-infra-container-image=k8s.gcr.io/pause:3.1"
```

### K8S清理

#### 自动清理节点

将节点添加到集群时后，会创建容器、虚拟网络接口等资源和证书、配置文件。从集群中正常删除节点时(如果处于 Active 状态)，将自动清除这些资源，并且只需重新启动节点即可。当节点无法访问且无法使用自动清理，或者异常导致节点脱离集群后，如果需要再次将节点加入集群，那么需要手动进行节点初始化操作。

#### 手动清理节点

**警告:** 以下操作将删除节点中的数据，在执行命令之前，请确保已进行数据备份。

```bash
#!/bin/bash

KUBE_SVC='
kubelet
kube-scheduler
kube-proxy
kube-controller-manager
kube-apiserver
'

for kube_svc in ${KUBE_SVC};
do
  # 停止服务
  if [[ `systemctl is-active ${kube_svc}` == 'active' ]]; then
    systemctl stop ${kube_svc}
  fi
  # 禁止服务开机启动
  if [[ `systemctl is-enabled ${kube_svc}` == 'enabled' ]]; then
    systemctl disable ${kube_svc}
  fi
done

# 停止所有容器
docker stop $(docker ps -aq)

# 删除所有容器
docker rm -f $(docker ps -qa)

# 删除所有容器卷
docker volume rm $(docker volume ls -q)

# 卸载 mount 目录
for mount in $(mount | grep tmpfs | grep '/var/lib/kubelet' | awk '{ print $3 }') /var/lib/kubelet /var/lib/rancher;
do
  umount $mount;
done

# 备份目录
mv /etc/kubernetes /etc/kubernetes-bak-$(date +"%Y%m%d%H%M")
mv /var/lib/etcd /var/lib/etcd-bak-$(date +"%Y%m%d%H%M")
mv /var/lib/rancher /var/lib/rancher-bak-$(date +"%Y%m%d%H%M")
mv /opt/rke /opt/rke-bak-$(date +"%Y%m%d%H%M")

# 删除残留路径
rm -rf /etc/ceph \
    /etc/cni \
    /opt/cni \
    /run/secrets/kubernetes.io \
    /run/calico \
    /run/flannel \
    /var/lib/calico \
    /var/lib/cni \
    /var/lib/kubelet \
    /var/log/containers \
    /var/log/kube-audit \
    /var/log/pods \
    /var/run/calico

# 清理网络接口
no_del_net_inter='
lo
docker0
eth
ens
bond
'

network_interface=`ls /sys/class/net`

for net_inter in ${network_interface};
do
  if ! echo "${no_del_net_inter}" | grep -qE ${net_inter:0:3}; then
    ip link delete $net_inter
  fi
done

# 清理残留进程
port_list='
80
443
6443
2376
2379
2380
8472
9099
10250
10254
'

for port in ${port_list};
do
  pid=`netstat -atlnup | grep -w ${port} | grep -v - | awk '{print $7}' | awk -F '/' '{print $1}' | sort -rnk2 | uniq`
  if [[ -n ${pid} ]]; then
    kill -15 ${pid}
  fi
done

kube_pid=`ps -ef | grep -v grep | grep kube | awk '{print $2}'`

if [[ -n ${kube_pid} ]]; then
  kill -15 ${kube_pid}
fi

# 清理 Iptables 表
## 注意：如果节点 Iptables 有特殊配置，以下命令请谨慎操作
sudo iptables --flush
sudo iptables --flush --table nat
sudo iptables --flush --table filter
sudo iptables --table nat --delete-chain
sudo iptables --table filter --delete-chain
systemctl restart docker
```

## 3、安装私有仓库

安装底层需求

​	Python应该是2.7或更高版本 

​	Docker引擎应为1.10或更高版本

​	DockerCompose需要为1.6.0或更高版本

docker daemon文件

```
{
    "exec-opts": ["native.cgroupdriver=systemd"],
    "log-driver": "json-file",
    "log-opts": {
        "max-size": "100m"
    }
	"insecure-registeries": ["https://hub.harry.com"]
}
```

### 导入 docker-compose

```
[root@k8s-habor ~]# mv docker-compose /usr/local/bin/
[root@k8s-habor ~]# chmod a+x /usr/local/bin/docker-compose
```

导入habor压缩包

```
[root@k8s-habor ~]# tar -zxvf harbor-offline-installer-v1.2.0.tgz
[root@k8s-habor ~]# mv harbor /usr/local/
#创建存储证书目录
[root@k8s-habor harbor]# mkdir -p /data/cert

```

### 配置harbor.cfg

必选参数、必选参数

```
hostname：目标的主机名或者完全限定域名：目标的主机名或者完全限定域名
ui_url_protocol：：http或或https。默认为。默认为http
db_password：用于：用于db_auth的的MySQL数据库的根密码。更改此密码进行任何生产用途数据库的根密码。更改此密码进行任何生产用途
max_job_workers：（默认值为：（默认值为3）作业服务中的复制工作人员的最大数量。对于每个映像复制作业，）作业服务中的复制工作人员的最大数量。对于每个映像复制作业，
工作人员将存储库的所有标签同步到远程目标。增加此数字允许系统中更多的并发复制作业。但是，由于每个工工作人员将存储库的所有标签同步到远程目标。增加此数字允许系统中更多的并发复制作业。但是，由于每个工
作人员都会消耗一定数量的网络作人员都会消耗一定数量的网络/ CPU / IO资源，请根据主机的硬件资源，仔细选择该属性的值资源，请根据主机的硬件资源，仔细选择该属性的值
customize_crt：（：（on或或off。默认为。默认为on）当此属性打开时，）当此属性打开时，prepare脚本将为注册表的令牌的生成脚本将为注册表的令牌的生成/验证创验证创
建私钥和根证书建私钥和根证书
ssl_cert：：SSL证书的路径，仅当协议设置为证书的路径，仅当协议设置为https时才应用时才应用
ssl_cert_key：：SSL密钥的路径，仅当协议设置为密钥的路径，仅当协议设置为https时才应用时才应用
secretkey_path：用于在复制策略中加密或解密远程注册表的密码的密钥路径：用于在复制策略中加密或解密远程注册表的密码的密钥路
```

### 创建 https 证书以及配置相关目录权限证书以及配置相关目录权限

```
openssl genrsa -des3 -out server.key 2048
openssl req -new -key server.key -out server.csr
cp server.key server.key.org
openssl rsa -in server.key.org -out server.key
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
mkdir /data/cert
chmod -R 777 /data/cert
```

进入harbor目录下安装

```
[root@k8s-habor harbor]# ./install.sh
```

其他k8s节点添加host文件

192.168.31.100 hub.harry.com

访问测试
默认管理员用户名认管理员用户名/密码为密码为admin / Harbor12345

![image-20220109114749347](\images\image-20220109114749347.png)

### harbor修改配置文件后重启

```
# docker-compose down
# ./prepare
# docker-compose up -d
```

### 上传镜像进行上传测试

其他节点指定镜像仓库地址

vim/etc/docker/daemon.json
{
	"insecure-registries": ["serverip"]
}

```
docker pull hello-world
```

![image-20220109115206663](\images\image-20220109115206663.png)

```
docker tag hello-world hub.harry.com/library/myhellowrod-v1 # 打一个标签
```

登录进行上传

```
docker login hub.harry.com
docker push hub.harry.com/library/myhellowrod:v1
```

![image-20220109123252429](\images\image-20220109123252429.png)

k8s 部署一个nginx

```
[root@k8s-master01 ~]# kubectl run nginx-deployement --image=hub.harry.com/library/mynginx:v1 --port=80 --replicas=1
```

![image-20220109141755545](\images\image-20220109141755545.png)

![image-20220109141829585](\images\image-20220109141829585.png)

![image-20220109141910897](\images\image-20220109141910897.png)

[root@k8s-master01 ~]# kubectl get pod -o wide # 查看详细

### Harbor 原理说明原理说明

Harbor是是VMware公司开源的企业级公司开源的企业级DockerRegistry项目，项目地址为项目，项目地址为https://github.com/vmware/harbor。

其目标是帮助用户迅速搭建一个企业级的Dockerregistry服务。它以Docker公司开源的公司开源的registry为基础，提供了管理管理UI，基于角色的访问控制，AD/LDAP集成、以及审计日志等企业用户需求的功等企业用户需求的功能，同时还原生支持中文。Harbor的每个组件都是以Docker容器的形式构建的，使用Docker Compose来对它进行部署。用于部署Harbor的的Docker Compose模板位于 /Deployer/docker-compose.yml，由5个容器组成，这几个容器通过Docker link的形式连接在一起，在容器之间通过容器名字互相访问。对终端用户而言，只需要暴露的形式连接在一起，在容器之间通过容器名字互相访问。对终端用户而言，只需要暴露 proxy （（ 即
Nginx）的服务端口）的服务端

Proxy：由Nginx 服务器构成的反向代理。 

Registry：由Docker官方的开源 registry 镜像构成的容器实例。

 UI：即架构中的 core services， 构成此容器的代码是 Harbor项目的主体。

 MySQL：由官方 MySQL镜像构成的数据库容器。 

Log：运行着 rsyslogd的容器，通过 log-driver的形式收集其他容器的日志

#### Harbor特性

 a、基于角色控制：用户和仓库都是基于项目进行组织的， 而用户基于项目可以拥有不同的权限

 b、基于镜像的复制策略：镜像可以在多个Harbor实例之间进行复制 

 c、支持LDAP：Harbor的用户授权可以使用已经存在LDAP用户 

 d、镜像删除 & 垃圾回收：Image可以被删除并且回收Image占用的空间，绝大部分的用户操作API， 方便 用户对系统进行扩展

e、用户UI：用户可以轻松的浏览、搜索镜像仓库以及对项目进行管理

 f、轻松的部署功能：Harbor提供了online、offline安装，除此之外还提供了virtualappliance安装

 g、Harbor和 dockerregistry 关系：Harbor实质上是对 dockerregistry 做了封装，扩展了自己的业务模块

![image-20220109124410636](\images\image-20220109124410636.png)

## 4、部署一个镜像测试

```
[root@k8s-master01 ~]# docker tag wangyanglinux/myapp:v1 hub.harry.com/library/myapp:v1
[root@k8s-master01 ~]# docker pull wangyanglinux/myapp:v1
[root@k8s-master01 ~]# docker push hub.harry.com/library/myapp:v1
```

先删除一下这两个镜像

```
[root@k8s-master01 ~]# docker rmi -f hub.harry.com/library/myapp:v1
```

![image-20220111192353060](\images\image-20220111192353060.png)

```
[root@k8s-master01 ~]# kubectl run nginx-deployment --image=hub.harry.com/library/myapp:v1 --replicas=1 
kubectl run --generator=deployment/apps.v1 is DEPRECATED and will be removed in a future version. Use kubectl run --generator=run-pod/v1 or kubectl create instead.
deployment.apps/nginx-deployment created

```

![image-20220111193138050](\images\image-20220111193138050.png)

![image-20220111193218986](\images\image-20220111193218986.png)

![image-20220111195333774](\images\image-20220111195333774.png)

![image-20220111195457543](\images\image-20220111195457543.png)

访问一下pod的nginx服务

```
[root@k8s-master01 ~]# curl 10.244.1.10
```

![image-20220111195609999](\images\image-20220111195609999.png)

对pod进行扩容

```
[root@k8s-master01 ~]# kubectl scale --replicas=3 deployment/nginx-deployment
deployment.extensions/nginx-deployment scaled
```

![image-20220111195904798](\images\image-20220111195904798.png)

创建service暴露服务

![image-20220111200014630](\images\image-20220111200014630.png)

```
[root@k8s-master01 ~]# kubectl expose deployment nginx-deployment --port=30000 --target-port=80
```

![image-20220111200214817](\images\image-20220111200214817.png)

![image-20220111200325183](\images\image-20220111200325183.png)

# 三、 Kbuernetes资源清单

K8s 中所有的内容都抽象为资源， 资源实例化之后，叫做对象

### 名称空间级别

工作负载型资源( workload )： Pod、ReplicaSet、Deployment、StatefulSet、DaemonSet、Job、
CronJob ( ReplicationController 在 v1.11 版本被废弃 )

服务发现及负载均衡型资源( ServiceDiscovery LoadBalance ): Service、Ingress、...

配置与存储型资源： Volume( 存储卷 )、CSI( 容器存储接口,可以扩展各种各样的第三方存储卷 )

特殊类型的存储卷：ConfigMap( 当配置中心来使用的资源类型 )、Secret(保存敏感数据)、
DownwardAPI(把外部环境中的信息输出给容器)

集群级资源：Namespace、Node、Role、ClusterRole、RoleBinding、ClusterRoleBinding

元数据型资源：HPA、PodTemplate、LimitRange

### 资源清单

在 k8s 中，一般使用 yaml 格式的文件来创建符合我们预期期望的 pod ，这样的 yaml 文件我们一般
称为资源清单

常用字段的解释

![image-20220110153322327](\images\image-20220110153322327.png)

![image-20220110153541014](\images\image-20220110153541014.png)

![image-20220110153614153](\images\image-20220110153614153.png)

![image-20220110153641973](\images\image-20220110153641973.png)

![image-20220110153708446](\images\image-20220110153708446.png)

