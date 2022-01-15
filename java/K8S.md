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

### 资源清单格式

```
apiVersion: group/apiversion # 如果没有给定 group 名称，那么默认为 core，可以使用 kubectl api-
versions # 获取当前 k8s 版本上所有的 apiVersion 版本信息( 每个版本可能不同 )
kind: #资源类别
metadata： #资源元数据
	name
	namespace
	lables
	annotations # 主要目的是方便用户阅读查找
spec: # 期望的状态（disired state）
status：# 当前状态，本字段有 Kubernetes 自身维护，用户不能去定义
```

### 资源清单的常用命令

#### 获取 apiversion 版本信息

```
[root@k8s-master01 ~]# kubectl api-versions
admissionregistration.k8s.io/v1beta1
apiextensions.k8s.io/v1beta1
apiregistration.k8s.io/v1
apiregistration.k8s.io/v1beta1
apps/v1
......(以下省略
```



#### 获取字段设置帮助文档

```
[root@k8s-master01 ~]# kubectl explain pod
KIND: Pod
VERSION: v1
DESCRIPTION:
Pod is a collection of containers that can run on a host. This resource is
created by clients and scheduled onto hosts.
FIELDS:
apiVersion <string>
........
........
```

#### 字段配置格式

```
piVersion <string> #表示字符串类型
metadata <Object> #表示需要嵌套多层字段
labels <map[string]string> #表示由k:v组成的映射
finalizers <[]string> #表示字串列表
ownerReferences <[]Object> #表示对象列表
hostPID <boolean> #布尔类型
priority <integer> #整型
name <string> -required- #如果类型后面接 -required-，表示为必填字段
```

#### 通过定义清单文件创建 Pod

```yml
apiVersion: v1
kind: Pod
metadata:
	name: pod-demo
	namespace: default
	labels:
		app: myapp
spec:
	containers:
	- name: myapp-1
		image: hub.harry.com/library/myapp:v1
	- name: busybox-1
		image: busybox:latest
		command:
		- "/bin/sh"
		- "-c"
		- "sleep 3600"
```

```
kubectl get pod xx.xx.xx -o yaml
<!--使用 -o 参数 加 yaml，可以将资源的配置以 yaml的格式输出出来，也可以使用json，输出为json格式-->
```



### pod的生命周期

![image-20220112160346055](\images\image-20220112160346055.png)

#### init容器

Pod 能够具有多个容器，应用运行在容器里面，但是它也可能有一个或多个先于应用容器启动的 Init
容器

Init 容器与普通的容器非常像，除了如下两点：
	Init 容器总是运行到成功完成为止
	每个 Init 容器都必须在下一个 Init 容器启动之前成功完成

如果 Pod 的 Init 容器失败，Kubernetes 会不断地重启该 Pod，直到 Init 容器成功为止。然而，
如果 Pod 对应的 restartPolicy 为 Never，它不会重新启动

Init 容器的作用

因为 Init 容器具有与应用程序容器分离的单独镜像，所以它们的启动相关代码具有如下优势：

> ​	它们可以包含并运行实用工具，但是出于安全考虑，是不建议在应用程序容器镜像中包含这些实用工具
>
> ​	它们可以包含使用工具和定制化代码来安装，但是不能出现在应用程序镜像中。例如，创建镜像没必要FROM 另一个镜像，只需要在安装过程中使用类似 sed、 awk、 python 或 dig这样的工具。
>
> ​    应用程序镜像可以分离出创建和部署的角色，而没有必要联合它们构建一个单独的镜像。
>
> ​	Init 容器使用 Linux Namespace，所以相对应用程序容器来说具有不同的文件系统视图。因此，它们能够具有访问 Secret 的权限，而应用程序容器则不能。
>
> ​	它们必须在应用程序容器启动之前运行完成，而应用程序容器是并行运行的，所以 Init 容器能够提供了一种简单的阻塞或延迟应用容器的启动的方法，直到满足了一组先决条件。

特殊说明 

> ​	在 Pod 启动过程中，Init 容器会按顺序在网络和数据卷初始化之后启动。每个容器必须在下一个容器启动之前成功退出
> ​	如果由于运行时或失败退出，将导致容器启动失败，它会根据 Pod 的 restartPolicy 指定的策略进行重试。然而，如果 Pod 的 restartPolicy 设置为 Always，Init 容器失败时会使用RestartPolicy 策略
>
> ​	在所有的 Init 容器没有成功之前，Pod 将不会变成 Ready 状态。Init 容器的端口将不会在Service 中进行聚集。 正在初始化中的 Pod 处于 Pending 状态，但应该会将 Initializing 状态设置为 true
>
> ​	如果 Pod 重启，所有 Init 容器必须重新执行
>
> ​	对 Init 容器 spec 的修改被限制在容器 image 字段，修改其他字段都不会生效。更改 Init容器的 image 字段，等价于重启该 Pod
>
> ​	Init 容器具有应用容器的所有字段。除了 readinessProbe，因为 Init 容器无法定义不同于完成（completion）的就绪（readiness）之外的其他状态。这会在验证过程中强制执行
>
> ​	在 Pod 中的每个 app 和 Init 容器的名称必须唯一；与任何其它容器共享同一个名称，会在验证时抛出错误



#### 容器探针

探针是由 kubelet 对容器执行的定期诊断。要执行诊断，kubelet 调用由容器实现的 Handler。有三种类型的处理程序：

> ExecAction：在容器内执行指定命令。如果命令退出时返回码为 0 则认为诊断成功。
>
> TCPSocketAction：对指定端口上的容器的 IP 地址进行 TCP 检查。如果端口打开，则诊断被认为是成功的。
>
> HTTPGetAction：对指定的端口和路径上的容器的 IP 地址执行 HTTP Get 请求。如果响应的状态码大于等于200 且小于 400，则诊断被认为是成功的
>
> 

每次探测都将获得以下三种结果之一：

> 成功：容器通过了诊断。
> 失败：容器未通过诊断。
> 未知：诊断失败，因此不会采取任何行动

#### 探测方式

livenessProbe：指示容器是否正在运行。如果存活探测失败，则 kubelet 会杀死容器，并且容器将受到其 重启策略 的影响。如果容器不提供存活探针，则默认状态为 Success

readinessProbe：指示容器是否准备好服务请求。如果就绪探测失败，端点控制器将从与 Pod 匹配的所有Service 的端点中删除该 Pod 的 IP 地址。初始延迟之前的就绪状态默认为 Failure。如果容器不提供就绪探针，则默认状态为 Success

#### Pod hook

Pod hook（钩子）是由 Kubernetes 管理的 kubelet 发起的，当容器中的进程启动前或者容器中的进程终止之前运行，这是包含在容器的生命周期之中。可以同时为 Pod 中的所有容器都配置 hook

Hook 的类型包括两种：

	exec：执行一段命令
	HTTP：发送HTTP请求

#### 重启策略

PodSpec 中有一个 restartPolicy 字段，可能的值为 Always、OnFailure 和 Never。默认为Always。 restartPolicy 适用于 Pod 中的所有容器。restartPolicy 仅指通过同一节点上的kubelet 重新启动容器。失败的容器由 kubelet 以五分钟为上限的指数退避延迟（10秒，20秒，40秒...）重新启动，并在成功执行十分钟后重置。如 Pod 文档 中所述，一旦绑定到一个节点，Pod 将永远不会重新绑定到另一个节点。

#### Pod phase

Pod 的 status 字段是一个 PodStatus 对象，PodStatus中有一个 phase 字段。

Pod 的相位（phase）是 Pod 在其生命周期中的简单宏观概述。该阶段并不是对容器或 Pod 的综合汇总，也不是为了做为综合状态机

Pod 相位的数量和含义是严格指定的。除了本文档中列举的状态外，不应该再假定 Pod 有其他的phase 值

> 
>
> 挂起（Pending）：Pod 已被 Kubernetes 系统接受，但有一个或者多个容器镜像尚未创建。等待时间包括调度 Pod 的时间和通过网络下载镜像的时间，这可能需要花点时间
>
> 运行中（Running）：该 Pod 已经绑定到了一个节点上，Pod 中所有的容器都已被创建。至少有一个容器正在运行，或者正处于启动或重启状态
>
> 成功（Succeeded）：Pod 中的所有容器都被成功终止，并且不会再重启
>
> 失败（Failed）：Pod 中的所有容器都已终止了，并且至少有一个容器是因为失败终止。也就是说，容器以非 0 状态退出或者被系统终止
>
> 未知（Unknown）：因为某些原因无法取得 Pod 的状态，通常是因为与 Pod 所在主机通信失败

### Init容器

init 模板

```yml
apiVersion: v1
kind: Pod
metadata:
    name: myapp-pod
    labels:
        app: myapp
spec:
    containers:
    - name: myapp-container
    image: busybox
    command: ['sh', '-c', 'echo The app is running! && sleep 3600']
    initContainers:
    - name: init-myservice
    image: busybox
    command: ['sh', '-c', 'until nslookup myservice; do echo waiting for myservice; sleep 2; done;']
    - name: init-mydb
    image: busybox
    command: ['sh', '-c', 'until nslookup mydb; do echo waiting for mydb sleep 2; done;']

```

```
# 通过模板运行一个 pod会先去运行init的容器
[root@k8s-master01 ~]# kubectl create -f ini-pod.yml
pod/myapp-pod created
```

目前可以看到两个init容器还没成功

![image-20220112201513155](\images\image-20220112201513155.png)



```
[root@k8s-master01 ~]# kubectl describe pod myapp-pod
```

![image-20220112201718483](\images\image-20220112201718483.png)

```
[root@k8s-master01 ~]# kubectl log myapp-pod -c init-myservice
```

![image-20220112201920459](\images\image-20220112201920459.png)

发现一直没找到服务应答所以运行失败，这里运行一个service

```yml
kind: Service
apiVersion: v1
metadata:
    name: myservice
spec:
    ports:
      - protocol: TCP
        port: 80
        targetPort: 9376
---
kind: Service
apiVersion: v1
metadata:
    name: mydb
spec:
    ports:
      - protocol: TCP
        port: 80
        targetPort: 9377

```

```
[root@k8s-master01 ~]# kubectl create -f myservice.yml
service/myservice created
service/mydb created
```

这两个pod 会作为dns服务器解析service的ip

![image-20220112204105208](\images\image-20220112204105208.png)

![image-20220112204138225](\images\image-20220112204138225.png)

状态变成了running

![image-20220112204224091](\images\image-20220112204224091.png)

### 检测探针 - 就绪检测

readinessProbe-httpget

```yml
apiVersion: v1
kind: Pod
metadata:
  name: readiness-httpget-pod
  namespace: default
spec:
  containers:
  - name: readiness-httpget-container
    image: wangyanglinux/myapp:v1
    imagePullPolicy: IfNotPresent
    readinessProbe:
      httpGet:
        port: 80
        path: /index1.html
      initialDelaySeconds: 1
      periodSeconds: 3
```

```
[root@k8s-master01 ~]# kubectl create -f read.yml
pod/readiness-httpget-pod created
```

![image-20220112205809852](\images\image-20220112205809852.png)

![image-20220112205908960](\images\image-20220112205908960.png)

进入容器创建一个html

```
[root@k8s-master01 ~]# kubectl exec readiness-httpget-pod  -c readiness-httpget-container -it -- /bin/sh
/ # cd home/
/home # cd ..
/ # cd /usr/share/nginx/
/usr/share/nginx # ls
html
/usr/share/nginx # cd html/
/usr/share/nginx/html # ls
50x.html    index.html
/usr/share/nginx/html # echo "123" >> index1.html
```

![image-20220112210206637](\images\image-20220112210206637.png)

### 检测探针 - 存活检测

livenessProbe-exec

```yml
apiVersion: v1
kind: Pod
metadata:
  name: liveness-exec-pod
  namespace: default
spec:
  containers:
  - name: liveness-exec-container
    image: busybox
    imagePullPolicy: IfNotPresent
    command: ["/bin/sh","-c","touch /tmp/live ; sleep 60; rm -rf /tmp/live; sleep 3600"]
    livenessProbe:
      exec:
        command: ["test","-e","/tmp/live"]
      initialDelaySeconds: 1
      periodSeconds: 3
```

```
[root@k8s-master01 ~]# kubectl delete pod --all
pod "myapp-pod" deleted
pod "nginx-deployment-585bd494df-47h6b" deleted
pod "nginx-deployment-585bd494df-fc8qg" deleted
pod "nginx-deployment-585bd494df-ps24r" deleted
pod "readiness-httpget-pod" deleted
[root@k8s-master01 ~]# kubectl delete svc --all
service "kubernetes" deleted
service "mydb" deleted
service "myservice" deleted
service "nginx-deployment" deleted
[root@k8s-master01 ~]# kubectl create -f liveless.yml

```

![image-20220112211408716](\images\image-20220112211408716.png)

发现pod重启了， 因为livenessProbe发现容器创建的文件已经不存在了

![image-20220112211716660](\images\image-20220112211716660.png)

livenessProbe-httpget

```yml
apiVersion: v1
kind: Pod
metadata:
  name: liveness-httpget-pod
  namespace: default
spec:
  containers:
  - name: liveness-httpget-container
    image: wangyanglinux/myapp:v1
    imagePullPolicy: IfNotPresent
    ports:
    - name: http
      containerPort: 80
    livenessProbe:
      httpGet:
        port: http
        path: /index.html
      initialDelaySeconds: 1
      periodSeconds: 3
      timeoutSeconds: 10

```

目前看到pod正常运行

![image-20220112213120138](\images\image-20220112213120138.png)

![image-20220112213221046](\images\image-20220112213221046.png)

现在进入容器把index.html干掉

![image-20220112213500209](\images\image-20220112213500209.png)

livenessProbe-tcp

```yml
apiVersion: v1
kind: Pod
metadata:
  name: probe-tcp
spec:
  containers:
  - name: nginx
    image: hub.harry.com/library/myapp:v1
    livenessProbe:
      initialDelaySeconds: 5
      timeoutSeconds: 1
      tcpSocket:
        port: 80
```

![image-20220113200856058](\images\image-20220113200856058.png)

### 就绪和存货检查共存

```yml
apiVersion: v1
kind: Pod
metadata:
  name: liveness-httpget-pod
  namespace: default
spec:
  containers:
  - name: liveness-httpget-container
    image: wangyanglinux/myapp:v1
    imagePullPolicy: IfNotPresent
    ports:
    - name: http
      containerPort: 80
    livenessProbe:
      httpGet:
        port: http
        path: /index.html
      initialDelaySeconds: 1
      periodSeconds: 3
      timeoutSeconds: 10
    readinessProbe:
      httpGet:
        port: 80
        path: /index1.html
      initialDelaySeconds: 1
      periodSeconds: 3
```

### 启动、退出动作

```yml
apiVersion: v1
kind: Pod
metadata:
  name: lifecycle-demo
spec:
  containers:
  - name: lifecycle-demo-container
    image: nginx
    lifecycle:
      postStart:
        exec:
          command: ["/bin/sh", "-c", "echo Hello from the postStart handler >/usr/share/message"]
      preStop:
        exec:
          command: ["/bin/sh", "-c", "echo Hello from the poststop handler >/usr/share/message"]


```

![image-20220113212046482](\images\image-20220113212046482.png)

# 四、K8S控制器

## 1、Deployment控制器

### RS 与 RC 与 Deployment 关联

RC （ReplicationController ）主要的作用就是用来确保容器应用的副本数始终保持在用户定义的副本数 。即如
果有容器异常退出，会自动创建新的Pod来替代；而如果异常多出来的容器也会自动回收

Kubernetes 官方建议使用 RS（ReplicaSet ） 替代 RC （ReplicationController ） 进行部署，RS 跟 RC 没有
本质的不同，只是名字不一样，并且 RS 支持集合式的 selector

```yml

apiVersion: extensions/v1beta1
kind: ReplicaSet
metadata:
  name: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      labels:
        tier: frontend
    spec:
      containers:
      - name: myapp
        image: hub.harry.com/library/myapp:v1
        env:
        - name: GET_HOSTS_FROM
          value: dns
        ports:
        - containerPort: 80

```

![image-20220115093358758](\images\image-20220115093358758.png)

修改pod标签

```
[root@k8s-master01 ~]# kubectl label pod frontend-htwrl  tier=frontend1 --overwrite=true
```

![image-20220115093601941](\images\image-20220115093601941.png)

### RS 与 Deployment 的关联

![image-20220115093733731](\images\image-20220115093733731.png)

#### Deployment

Deployment 为 Pod 和 ReplicaSet 提供了一个声明式定义(declarative)方法，用来替代以前的
ReplicationController 来方便的管理应用。典型的应用场景包括：

​	定义Deployment来创建Pod和ReplicaSet
​	滚动升级和回滚应用
​	扩容和缩容
​	暂停和继续Deployment

#### 部署一个简单的 Nginx 应

```yml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80
```

```
[root@k8s-master01 ~]# kubectl create -f dep-rs.yml --record
## --record参数可以记录命令，我们可以很方便的查看每次 revision 的变化
```

![image-20220115094704107](\images\image-20220115094704107.png)

![image-20220115094736831](\images\image-20220115094736831.png)

#### 扩容

```
[root@k8s-master01 ~]# kubectl scale deployment nginx-deployment --replicas 10
deployment.extensions/nginx-deployment scaled
```

![image-20220115094953414](D:\studyDoc\java\images\image-20220115094953414.png)

更新deployment的镜像

```
[root@k8s-master01 ~]# kubectl set image deployment/nginx-deployment nginx=wangyanglinux/myapp:v2                                                              deployment.extensions/nginx-deployment image updated
```

更新镜像会创建出来一个RS

![image-20220115100120498](\images\image-20220115100120498.png)

回滚操作

```
[root@k8s-master01 ~]# kubectl rollout undo deployment/nginx-deployment
deployment.extensions/nginx-deployment rolled back
```

#### 更新 Deployment

假如我们现在想要让 nginx pod 使用 nginx:1.9.1 的镜像来代替原来的 nginx:1.7.9 的镜像

```
[root@k8s-master01 ~]# kubectl set image deployment/nginx-deployment nginx=nginx:1.9.1
```

可以使用 edit 命令来编辑 Deployment

```
[root@k8s-master01 ~]# kubectl edit deployment/nginx-deployment
```

查看rollout状态

```
[root@k8s-master01 ~]# kubectl rollout status deployment/nginx-deployment
deployment "nginx-deployment" successfully rolled out
```

查看历史 RS

![image-20220115101134593](\images\image-20220115101134593.png)

#### Deployment 更新策略

Deployment 可以保证在升级时只有一定数量的 Pod 是 down 的。默认的，它会确保至少有比期望的Pod数量少
一个是up状态（最多一个不可用）

Deployment 更新策略
Deployment 可以保证在升级时只有一定数量的 Pod 是 down 的。默认的，它会确保至少有比期望的Pod数量少
一个是up状态（最多一个不可用）
Deployment 同时也可以确保只创建出超过期望数量的一定数量的 Pod。默认的，它会确保最多比期望的Pod数
量多一个的 Pod 是 up 的（最多1个 surge ）

将来的 Kuberentes 版本中，将从1-1变成25%-25%

#### Rollover（多个rollout并行）

假如您创建了一个有5个 niginx:1.7.9  replica的 Deployment，但是当还只有3个 nginx:1.7.9 的 replica 创建
出来的时候您就开始更新含有5个 nginx:1.9.1  replica 的 Deployment。在这种情况下，Deployment 会立即
杀掉已创建的3个 nginx:1.7.9 的 Pod，并开始创建 nginx:1.9.1 的 Pod。它不会等到所有的5个 nginx:1.7.9 的
Pod 都创建完成后才开始改变航道

#### 回退 Deployment

```
[root@k8s-master01 ~]# kubectl set image deployment/nginx-deployment nginx=nginx:1.91
[root@k8s-master01 ~]# kubectl rollout status deployments nginx-deployment
[root@k8s-master01 ~]# kubectl rollout history deployment/nginx-deployment
```

![image-20220115101439756](\images\image-20220115101439756.png)

可以用 kubectl rollout status 命令查看 Deployment 是否完成。如果 rollout 成功完成， kubectl rollout
status 将返回一个0值的 Exit Code

```
kubectl rollout undo deployment/nginx-deployment
kubectl rollout undo deployment/nginx-deployment --to-revision=2 ## 可以使用 --revision参数指定
某个历史版本
kubectl rollout pause deployment/nginx-deployment ## 暂停 deployment 的更新
```

![image-20220115101602418](\images\image-20220115101602418.png)

## 2、Deamonset

DaemonSet 确保全部（或者一些）Node 上运行一个 Pod 的副本。当有 Node 加入集群时，也会为他们新增一
个 Pod 。当有 Node 从集群移除时，这些 Pod 也会被回收。删除 DaemonSet 将会删除它创建的所有 Pod

使用 DaemonSet 的一些典型用法：

​	运行集群存储 daemon，例如在每个 Node 上运行 glusterd 、 ceph
​	在每个 Node 上运行日志收集 daemon，例如 fluentd 、 logstash
​	在每个 Node 上运行监控 daemon，例如 Prometheus Node Exporter、 collectd 、Datadog 代理、New Relic 代理，或 Ganglia gmon

```
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: deamonset-example
  labels:
    app: daemonset
spec:
  selector:
    matchLabels:
      name: deamonset-example
  template:
    metadata:
      labels:
        name: deamonset-example
    spec:
      containers:
      - name: daemonset-example
        image: wangyanglinux/myapp
```

![image-20220115102603274](\images\image-20220115102603274.png)

## 3、Job

job 负责批处理任务，即仅执行一次的任务，它保证批处理任务的一个或多个 Pod 成功结束

特殊说明

> spec.template格式同Pod
> RestartPolicy仅支持Never或OnFailure
> 单个Pod时，默认Pod成功运行后Job即结束
> .spec.completions 标志Job结束需要成功运行的Pod个数，默认为1
> .spec.parallelism 标志并行运行的Pod的个数，默认为1
> spec.activeDeadlineSeconds 标志失败Pod的重试最大时间，超过这个时间不会继续重试

Example

```yml
apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  template:
    metadata:
      name: pi
    spec:
      containers:
      - name: pi
        image: perl
        command: ["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never

```

![image-20220115104936741](\images\image-20220115104936741.png)

任务完成后job退出

![image-20220115105051357](\images\image-20220115105051357.png)

### CroncJob Spec

> spec.template格式同Pod
> RestartPolicy仅支持Never或OnFailure
> 单个Pod时，默认Pod成功运行后Job即结束
> .spec.completions 标志Job结束需要成功运行的Pod个数，默认为1
> .spec.parallelism 标志并行运行的Pod的个数，默认为1
> spec.activeDeadlineSeconds 标志失败Pod的重试最大时间，超过这个时间不会继续重试

Cron Job 管理基于时间的 Job，即：

​	在给定时间点只运行一次

​	周期性地在给定时间点运行

典型的用法如下所示：

​	在给定的时间点调度 Job 运行
​	创建周期性运行的 Job，例如：数据库备份、发送邮件

> spec.schedule ：调度，必需字段，指定任务运行周期，格式同 Cron
>
> .spec.jobTemplate ：Job 模板，必需字段，指定需要运行的任务，格式同 Job
>
> .spec.startingDeadlineSeconds ：启动 Job 的期限（秒级别），该字段是可选的。如果因为任何原因而错
> 过了被调度的时间，那么错过执行时间的 Job 将被认为是失败的。如果没有指定，则没有期限
>
> .spec.concurrencyPolicy ：并发策略，该字段也是可选的。它指定了如何处理被 Cron Job 创建的 Job 的
> 并发执行。只允许指定下面策略中的一种：
>
> ​	Allow （默认）：允许并发运行 Job
> ​	Forbid ：禁止并发运行，如果前一个还没有完成，则直接跳过下一个
> ​	Replace ：取消当前正在运行的 Job，用一个新的来替换
>
> ​	注意，当前策略只能应用于同一个 Cron Job 创建的 Job。如果存在多个 Cron Job，它们创建的 Job 之间总
> 是允许并发运行。
>
> .spec.suspend ：挂起，该字段也是可选的。如果设置为 true ，后续所有执行都会被挂起。它对已经开始
> 执行的 Job 不起作用。默认值为 false
>
> 
>
> .spec.successfulJobsHistoryLimit 和 .spec.failedJobsHistoryLimit ：历史限制，是可选的字段。它
> 们指定了可以保留多少完成和失败的 Job。默认情况下，它们分别设置为 3 和 1 。设置限制的值为 0 ，相
> 关类型的 Job 完成后将不会被保留。

Example

```yml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: hello
spec:
  schedule: "*/1 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: hello
            image: busybox
            args:
            - /bin/sh
            - -c
            - date; echo Hello from the Kubernetes cluster
          restartPolicy: OnFailure
```

![image-20220115105815761](\images\image-20220115105815761.png)

![image-20220115110508029](\images\image-20220115110508029.png)

# 五、K8S Service

Kubernetes  Service  定义了这样一种抽象：一个  Pod  的逻辑分组，一种可以访问它们的策略 —— 通常称为微
服务。 这一组  Pod  能够被  Service  访问到，通常是通过  Label Selector

![image-20220115110828763](\images\image-20220115110828763.png)

Service能够提供负载均衡的能力，但是在使用上有以下限制：

​	只提供 4 层负载均衡能力，而没有 7 层功能，但有时我们可能需要更多的匹配规则来转发请求，这点上 4 层负载均衡是不支持的

### Service 的类型

Service 在 K8s 中有以下四种类型

> ClusterIp：默认类型，自动分配一个仅 Cluster 内部可以访问的虚拟 IP
>
> NodePort：在 ClusterIP 基础上为 Service 在每台机器上绑定一个端口，这样就可以通过 : NodePort 来访问该服务
>
> LoadBalancer：在 NodePort 的基础上，借助 cloud provider 创建一个外部负载均衡器，并将请求转发到: NodePort
>
> ExternalName：把集群外部的服务引入到集群内部来，在集群内部直接使用。没有任何类型代理被创建，这只有 kubernetes 1.7 或更高版本的 kube-dns 才支持

![image-20220115111010676](\images\image-20220115111010676.png)

### VIP 和 Service 代理

在 Kubernetes 集群中，每个 Node 运行一个  kube-proxy  进程。 kube-proxy  负责为  Service  实现了一种
VIP（虚拟 IP）的形式，而不是  ExternalName  的形式。 在 Kubernetes v1.0 版本，代理完全在 userspace。在
Kubernetes v1.1 版本，新增了 iptables 代理，但并不是默认的运行模式。 从 Kubernetes v1.2 起，默认就是
iptables 代理。 在 Kubernetes v1.8.0-beta.0 中，添加了 ipvs 代理

在 Kubernetes 1.14 版本开始默认使用 ipvs 代理

在 Kubernetes v1.0 版本， Service 是 “4层”（TCP/UDP over IP）概念。 在 Kubernetes v1.1 版本，新增了
Ingress API（beta 版），用来表示 “7层”（HTTP）服务

### 代理模式的分类

I、userspace 代理模式

![image-20220115111236494](\images\image-20220115111236494.png)

II、iptables 代理模式

![image-20220115111302990](\images\image-20220115111302990.png)

这种模式，kube-proxy 会监视 Kubernetes Service 对象和 Endpoints ，调用 netlink 接口以相应地创建
ipvs 规则并定期与 Kubernetes Service 对象和 Endpoints 对象同步 ipvs 规则，以确保 ipvs 状态与期望一
致。访问服务时，流量将被重定向到其中一个后端 Pod

与 iptables 类似，ipvs 于 netfilter 的 hook 功能，但使用哈希表作为底层数据结构并在内核空间中工作。这意
味着 ipvs 可以更快地重定向流量，并且在同步代理规则时具有更好的性能。此外，ipvs 为负载均衡算法提供了更
多选项，例如：

> rr ：轮询调度
> lc ：最小连接数
> dh ：目标哈希
> sh ：源哈希
> sed ：最短期望延迟
> nq ： 不排队调度

![image-20220115115041737](\images\image-20220115115041737.png)

### ClusterIP

clusterIP 主要在每个 node 节点使用 iptables，将发向 clusterIP 对应端口的数据，转发到 kube-proxy 中。然
后 kube-proxy 自己内部实现有负载均衡的方法，并可以查询到这个 service 下对应 pod 的地址和端口，进而把
数据转发给对应的 pod 的地址和端口

![image-20220115115131697](\images\image-20220115115131697.png)

为了实现图上的功能，主要需要以下几个组件的协同工作：

> piserver 用户通过kubectl命令向apiserver发送创建service的命令，apiserver接收到请求后将数据存储到etcd中
>
> kube-proxy kubernetes的每个节点中都有一个叫做kube-porxy的进程，这个进程负责感知service，pod的变化，并将变化的信息写入本地的iptables规则中
>
> iptables 使用NAT等技术将virtualIP的流量转至endpoint中

