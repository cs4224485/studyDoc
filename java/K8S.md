删除 Pod 不会删除其 pvc，手动删除 pvc 将自动释放 pv

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

高版本的centos内核nf_conntrack_ipv4被nf_conntrack替换了，所以装不了。解决方法

```
[root@k8s-master02 ~]# modprobe -- nf_conntrack
```



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
imageRepository: registry.aliyuncs.com/google_containers
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

> apiserver 用户通过kubectl命令向apiserver发送创建service的命令，apiserver接收到请求后将数据存储到etcd中
>
> kube-proxy kubernetes的每个节点中都有一个叫做kube-porxy的进程，这个进程负责感知service，pod的变化，并将变化的信息写入本地的iptables规则中
>
> iptables 使用NAT等技术将virtualIP的流量转至endpoint中

创建 myapp-deploy.yaml 文件

```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deploy
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      release: stabel
  template:
    metadata:
      labels:
        app: myapp
        release: stabel
        env: test
    spec:
      containers:
      - name: myapp
        image: wangyanglinux/myapp:v2
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: 80
```

创建 Service 信息

```yml
apiVersion: v1
kind: Service
metadata:
  name: myapp
  namespace: default
spec:
  type: ClusterIP
  selector:
    app: myapp
    release: stabel
  ports:
  - name: http
    port: 80
    targetPort: 80

```

![image-20220116103812721](\images\image-20220116103812721.png)

![image-20220116105227050](\images\image-20220116105227050.png)

### Headless Service

有时不需要或不想要负载均衡，以及单独的 Service IP 。遇到这种情况，可以通过指定 ClusterIP(spec.clusterIP) 的值为 “None” 来创建 Headless Service 。这类 Service 并不会分配 Cluster IP， kube-proxy 不会处理它们，而且平台也不会为它们进行负载均衡和路由

```yml
apiVersion: v1
kind: Service
metadata:
  name: myapp-headless
  namespace: default
spec:
  selector:
    app: myapp
  clusterIP: "None"
  ports:
  - port: 80
    targetPort: 80

```

![image-20220116105659808](\images\image-20220116105659808.png)

![image-20220116105917998](\images\image-20220116105917998.png)

![image-20220116110350072](\images\image-20220116110350072.png)

### NodePort

nodePort 的原理在于在 node 上开了一个端口，将向该端口的流量导入到 kube-proxy，然后由 kube-proxy 进
一步到给对应的 pod

```yml
apiVersion: v1
kind: Service
metadata:
  name: myapp
  namespace: default
spec:
  type: NodePort
  selector:
    app: myapp
    release: stabel
  ports:
  - name: http
    port: 80
    targetPort: 80

```

![image-20220116111050787](\images\image-20220116111050787.png)

![image-20220116111156418](\images\image-20220116111156418.png)

![image-20220116111654398](\images\image-20220116111654398.png)

### LoadBalancer

loadBalancer 和 nodePort 其实是同一种方式。区别在于 loadBalancer 比 nodePort 多了一步，就是可以调用
cloud provider 去创建 LB 来向节点导流

![image-20220116111815385](\images\image-20220116111815385.png)

### ExternalName

这种类型的 Service 通过返回 CNAME 和它的值，可以将服务映射到 externalName 字段的内容( 例如hub.harry.com )。ExternalName Service 是 Service 的特例，它没有 selector，也没有定义任何的端口和
Endpoint。相反的，对于运行在集群外部的服务，它通过返回该外部服务的别名这种方式来提供服务

```yml
kind: Service
apiVersion: v1
metadata:
  name: my-service-1
  namespace: default
spec:
  type: ExternalName
  externalName: hub.harry.com
```

当查询主机 my-service.defalut.svc.cluster.local ( SVC_NAME.NAMESPACE.svc.cluster.local )时，集群的DNS 服务将返回一个值 my.database.example.com 的 CNAME 记录。访问这个服务的工作方式和其他的相同，唯一不同的是重定向发生在 DNS 层，而且不会进行代理或转发

### Ingress

#### 资料信息

Ingress-Nginx github 地址：https://github.com/kubernetes/ingress-nginx
Ingress-Nginx 官方网站：https://kubernetes.github.io/ingress-nginx/

![image-20220117191943102](\images\image-20220117191943102.png)

![image-20220117192003502](\images\image-20220117192003502.png)

#### Ingress 工作原理

​	1.ingress controller通过和kubernetes api交互，动态的去感知集群中ingress规则变化，

​	2.然后读取它，按照自定义的规则，规则就是写明了哪个域名对应哪个service，生成一段nginx配置，

​	3.再写到nginx-ingress-control的pod里，这个Ingress controller的pod里运行着一个Nginx服务，控制器会把生成的nginx配置写入/etc/nginx.conf文件中，

​	4.然后reload一下使配置生效。以此达到域名分配置和动态更新的问题。

#### Ingress可以解决什么问题

1.动态配置服务

　　如果按照传统方式, 当新增加一个服务时, 我们可能需要在流量入口加一个反向代理指向我们新的k8s服务. 而如果用了Ingress, 只需要配置好这个服务, 当服务启动时, 会自动注册到Ingress的中, 不需要而外的操作.

2.减少不必要的端口暴露

　　配置过k8s的都清楚, 第一步是要关闭防火墙的, 主要原因是k8s的很多服务会以NodePort方式映射出去, 这样就相当于给宿主机打了很多孔, 既不安全也不优雅. 而Ingress可以避免这个问题, 除了Ingress自身服务可能需要映射出去, 其他服务都不要用NodePort方式

#### 部署 Ingress-Nginx

```
[root@k8s-master01 install-k8s]# mkdir ingress
[root@k8s-master01 install-k8s]# cd ingress/
[root@k8s-master01 ingress]# wget https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/mandatory.yaml
```

自己做实验的时候因为下载不到mandatory.yml所以直接把内容复制下来

```yml
apiVersion: v1
kind: Namespace
metadata:
  name: ingress-nginx
  labels:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx

---

kind: ConfigMap
apiVersion: v1
metadata:
  name: nginx-configuration
  namespace: ingress-nginx
  labels:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx

---
kind: ConfigMap
apiVersion: v1
metadata:
  name: tcp-services
  namespace: ingress-nginx
  labels:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx

---
kind: ConfigMap
apiVersion: v1
metadata:
  name: udp-services
  namespace: ingress-nginx
  labels:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx

---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nginx-ingress-serviceaccount
  namespace: ingress-nginx
  labels:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx

---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRole
metadata:
  name: nginx-ingress-clusterrole
  labels:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
rules:
  - apiGroups:
      - ""
    resources:
      - configmaps
      - endpoints
      - nodes
      - pods
      - secrets
    verbs:
      - list
      - watch
  - apiGroups:
      - ""
    resources:
      - nodes
    verbs:
      - get
  - apiGroups:
      - ""
    resources:
      - services
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - ""
    resources:
      - events
    verbs:
      - create
      - patch
  - apiGroups:
      - "extensions"
      - "networking.k8s.io"
    resources:
      - ingresses
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - "extensions"
      - "networking.k8s.io"
    resources:
      - ingresses/status
    verbs:
      - update

---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: Role
metadata:
  name: nginx-ingress-role
  namespace: ingress-nginx
  labels:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
rules:
  - apiGroups:
      - ""
    resources:
      - configmaps
      - pods
      - secrets
      - namespaces
    verbs:
      - get
  - apiGroups:
      - ""
    resources:
      - configmaps
    resourceNames:
      # Defaults to "<election-id>-<ingress-class>"
      # Here: "<ingress-controller-leader>-<nginx>"
      # This has to be adapted if you change either parameter
      # when launching the nginx-ingress-controller.
      - "ingress-controller-leader-nginx"
    verbs:
      - get
      - update
  - apiGroups:
      - ""
    resources:
      - configmaps
    verbs:
      - create
  - apiGroups:
      - ""
    resources:
      - endpoints
    verbs:
      - get

---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: RoleBinding
metadata:
  name: nginx-ingress-role-nisa-binding
  namespace: ingress-nginx
  labels:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: nginx-ingress-role
subjects:
  - kind: ServiceAccount
    name: nginx-ingress-serviceaccount
    namespace: ingress-nginx

---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: nginx-ingress-clusterrole-nisa-binding
  labels:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: nginx-ingress-clusterrole
subjects:
  - kind: ServiceAccount
    name: nginx-ingress-serviceaccount
    namespace: ingress-nginx

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-ingress-controller
  namespace: ingress-nginx
  labels:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: ingress-nginx
      app.kubernetes.io/part-of: ingress-nginx
  template:
    metadata:
      labels:
        app.kubernetes.io/name: ingress-nginx
        app.kubernetes.io/part-of: ingress-nginx
      annotations:
        prometheus.io/port: "10254"
        prometheus.io/scrape: "true"
    spec:
      serviceAccountName: nginx-ingress-serviceaccount
      containers:
        - name: nginx-ingress-controller
          image: quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.25.1
          args:
            - /nginx-ingress-controller
            - --configmap=$(POD_NAMESPACE)/nginx-configuration
            - --tcp-services-configmap=$(POD_NAMESPACE)/tcp-services
            - --udp-services-configmap=$(POD_NAMESPACE)/udp-services
            - --publish-service=$(POD_NAMESPACE)/ingress-nginx
            - --annotations-prefix=nginx.ingress.kubernetes.io
          securityContext:
            allowPrivilegeEscalation: true
            capabilities:
              drop:
                - ALL
              add:
                - NET_BIND_SERVICE
            # www-data -> 33
            runAsUser: 33
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
          ports:
            - name: http
              containerPort: 80
            - name: https
              containerPort: 443
          livenessProbe:
            failureThreshold: 3
            httpGet:
              path: /healthz
              port: 10254
              scheme: HTTP
            initialDelaySeconds: 10
            periodSeconds: 10
            successThreshold: 1
            timeoutSeconds: 10
          readinessProbe:
            failureThreshold: 3
            httpGet:
              path: /healthz
              port: 10254
              scheme: HTTP
            periodSeconds: 10
            successThreshold: 1
            timeoutSeconds: 10

---
```

```
[root@k8s-master01 ingress]# kubectl apply -f mandatory.yaml
[root@k8s-master01 ingress]# kubectl apply -f service-nodeport.yaml
```

![image-20220117203959572](\images\image-20220117203959572.png)

![image-20220117204353810](\images\image-20220117204353810.png)

#### Ingress HTTP 代理访问

deployment、Service、Ingress Yaml 文件

```yml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-dm
spec:
  replicas: 2
  template:
    metadata:
      labels:
        name: nginx
    spec:
      containers:
      - name: nginx
        image: wangyanglinux/myapp:v1
        imagePullPolicy: IfNotPresent
        ports:
          - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-svc
spec:
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
  selector:
     name: nginx


```

```
[root@k8s-master01 ingress]# kubectl apply -f ingress.http.yml
deployment.extensions/nginx-dm unchanged
service/nginx-svc created
```

![image-20220117205402814](\images\image-20220117205402814.png)

![image-20220117205447531](\images\image-20220117205447531.png)

![image-20220117205521634](\images\image-20220117205521634.png)

![image-20220117205712667](\images\image-20220117205712667.png)

```yml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: nginx-test
spec:
  rules:
  - host: www1.harry.com
    http:
      paths:
      - path: /
        backend:
          serviceName: nginx-svc
          servicePort: 80

```

```
[root@k8s-master01 ingress]# kubectl apply -f ingress.yml
ingress.extensions/nginx-test created
```

![image-20220117210115208](\images\image-20220117210115208.png)

接下来就可以通过域名来访问了(注意关闭自己电脑的代理)

![image-20220117220027763](\images\image-20220117220027763.png)

创建另外一个www2.harry.com

```yml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-dm2
spec:
  replicas: 2
  template:
    metadata:
      labels:
        name: nginx2
    spec:
      containers:
      - name: nginx2
        image: wangyanglinux/myapp:v2
        imagePullPolicy: IfNotPresent
        ports:
          - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-svc2
spec:
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
  selector:
     name: nginx2
---
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: nginx-test2
spec:
  rules:
  - host: www2.harry.com
    http:
      paths:
      - path: /
        backend:
          serviceName: nginx-svc2
          servicePort: 80


```

![image-20220117220804815](\images\image-20220117220804815.png)

![image-20220117220849184](\images\image-20220117220849184.png)

![image-20220117220930326](\images\image-20220117220930326.png)

![image-20220117221042577](\images\image-20220117221042577.png)

#### Ingress HTTPS 代理访问

创建证书，以及 cert 存储方式

```
[root@k8s-master01 ~]# openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=nginxsvc/O=nginxsvc"
[root@k8s-master01 ~]# kubectl create secret tls tls-secret --key tls.key --cert tls.crt
secret/tls-secret created
```


deployment、Service、Ingress Yaml 文件

```yml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: nginx-test
spec:
  tls:
    - hosts:
      - foo.bar.com
      secretName: tls-secret
  rules:
    - host: foo.bar.com
      http:
        paths:
        - path: /
          backend:
            serviceName: nginx-svc
            servicePort: 80

```



![image-20220118161459949](\images\image-20220118161459949.png)

![image-20220118161706443](\images\image-20220118161706443.png)

Nginx 进行 BasicAuth

```
[root@k8s-master01 ~]# yum install -y httpd
[root@k8s-master01 ~]# htpasswd -c auth foo
New password:
Re-type new password:
Adding password for user foo
[root@k8s-master01 ~]# kubectl create secret generic basic-auth --from-file=auth
secret/basic-auth created
```

```yml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress-with-auth
  annotations:
    nginx.ingress.kubernetes.io/auth-type: basic
    nginx.ingress.kubernetes.io/auth-secret: basic-auth
    nginx.ingress.kubernetes.io/auth-realm: 'Authentication Required - foo'
spec:
  rules:
  - host: foo2.bar.com
    http:
      paths:
      - path: /
        backend:
          serviceName: nginx-svc
          servicePort: 80

```



![image-20220118162607687](\images\image-20220118162607687.png)

#### Nginx 进行重写

![image-20220118163327976](\images\image-20220118163327976.png)

```yml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: nginx-test
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: http://foo.bar.com:31795/hostname.html
spec:
  rules:
  - host: foo10.bar.com
    http:
      paths:
      - path: /
        backend:
          serviceName: nginx-svc
          servicePort: 80
```



# 六、Kubernetes存储

## 1、configMap

### configMap 描述信息

ConfigMap 功能在 Kubernetes1.2 版本中引入，许多应用程序会从配置文件、命令行参数或环境变量中读取配置信息。ConfigMap API 给我们提供了向容器中注入配置信息的机制，ConfigMap 可以被用来保存单个属性，也可以用来保存整个配置文件或者 JSON 二进制大对象

### ConfigMap 的创建

#### 使用目录创建

```
[root@k8s-master01 dir]# ls
game.properties  ui.properties

[root@k8s-master01 dir]# cat game.properties
enemies=aliens
lives=3
enemies.cheat=true
enemies.cheat.level=noGoodRotten
secret.code.passphrase=UUDDLRLRBABAS
secret.code.allowed=true
secret.code.lives=30

[root@k8s-master01 dir]# cat ui.properties
color.good=purple
color.bad=yellow
allow.textmode=true
how.nice.to.look=fairlyNice

[root@k8s-master01 configmap]# kubectl create configmap game-config --from-file=dir/
configmap/game-config created

```

![image-20220118204704090](\images\image-20220118204704090.png)

—from-file 指定在目录下的所有文件都会被用在 ConfigMap 里面创建一个键值对，键的名字就是文件名，值就
是文件

#### 使用文件创建

只要指定为一个文件就可以从单个文件中创建 ConfigMa

```
[root@k8s-master01 configmap]# kubectl create configmap game-config-2 --from-file=dir/game.properties
configmap/game-config-2 created
```

![image-20220118205355631](\images\image-20220118205355631.png)

—from-file 这个参数可以使用多次，你可以使用两次分别指定上个实例中的那两个配置文件，效果就跟指定整个
目录是一样的

#### 使用字面值创建

```
[root@k8s-master01 configmap]# kubectl create configmap special-config --from-literal=special.how=very --from-literal=special.type=charm
configmap/special-config created

```

### Pod 中使用 ConfigMap

#### 使用 ConfigMap 来替代环境变量

```yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: special-config
  namespace: default
data:
  special.how: very
  special.type: char
```

![image-20220118210411066](\images\image-20220118210411066.png)

```yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: env-config
  namespace: default
data:
  log_level: INFO

```

```
[root@k8s-master01 log]# kubectl apply -f log.yml
configmap/env-config created
```

```yml
apiVersion: v1
kind: Pod
metadata:
  name: dapi-test-pod
spec:
  containers:
    - name: test-container
      image: hub.harry.com/library/myapp:v1
      command: [ "/bin/sh", "-c", "env" ]
      env:
        - name: SPECIAL_LEVEL_KEY
          valueFrom:
            configMapKeyRef:
              name: special-config
              key: special.how
        - name: SPECIAL_TYPE_KEY
          valueFrom:
            configMapKeyRef:
              name: special-config
              key: special.type
      envFrom:
        - configMapRef:
            name: env-config
  restartPolicy: Never

```

![image-20220118211905417](\images\image-20220118211905417.png)

#### 用 ConfigMap 设置命令行参数

```yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: special-config
  namespace: default
data:
  special.how: very
  special.type: charm
```

```yml
apiVersion: v1
kind: Pod
metadata:
  name: dapi-test-pod
spec:
  containers:
    - name: test-container2
      image: hub.harry.com/library/myapp:v1
      command: [ "/bin/sh", "-c", "echo $(SPECIAL_LEVEL_KEY) $(SPECIAL_TYPE_KEY)" ]
      env:
        - name: SPECIAL_LEVEL_KEY
          valueFrom:
            configMapKeyRef:
              name: special-config
              key: special.how
        - name: SPECIAL_TYPE_KEY
          valueFrom:
            configMapKeyRef:
              name: special-config
              key: special.type
  restartPolicy: Never

```

![image-20220118213153984](\images\image-20220118213153984.png)

#### 通过数据卷插件使用ConfigMap

在数据卷里面使用这个 ConfigMap，有不同的选项。最基本的就是将文件填入数据卷，在这个文件中，键就是文
件名，键值就是文件内容

```yml
apiVersion: v1
kind: Pod
metadata:
  name: dapi-test-pod2
spec:
  containers:
    - name: test-container2
      image: wangyanglinux/myapp:v2
      command: [ "/bin/sh", "-c", "sleep 6000" ]
      volumeMounts:
      - name: config-volume
        mountPath: /etc/config
  volumes:
    - name: config-volume
      configMap:
        name: special-config
  restartPolicy: Never

```

![image-20220119164213595](\images\image-20220119164213595.png)

![image-20220119164238969](\images\image-20220119164238969.png)

#### ConfigMap 的热更新

```yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: log-config1
  namespace: default
data:
  log_level: INFO
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: my-nginx
spec:
  replicas: 1
  template:
    metadata:
      labels:
        run: my-nginx
    spec:
      containers:
      - name: my-nginx
        image: hub.harry.com/library/myapp:v1
        ports:
        - containerPort: 80
        volumeMounts:
        - name: config-volume
          mountPath: /etc/config
      volumes:
        - name: config-volume
          configMap:
            name: log-config1

```



```
[root@k8s-master01 ~]# kubectl exec `kubectl get pods -l run=my-nginx -o=name|cut -d "/" -f2` cat /etc/config/log_level
# 输出INFO
```

修改 ConfigMap

```
kubectl edit configmap log-config1
```

修改 log_level 的值为 DEBUG 等待大概 10 秒钟时间，再次查看环境变量的值

![image-20220119165817946](\images\image-20220119165817946.png)

ConfigMap 更新后滚动更新 Pod

更新 ConfigMap 目前并不会触发相关 Pod 的滚动更新，可以通过修改 pod annotations 的方式强制触发滚动更新

```
kubectl patch deployment my-nginx --patch '{"spec": {"template": {"metadata": {"annotations":{"version/config": "20190411" }}}}}'
```

个例子里我们在 .spec.template.metadata.annotations 中添加 version/config ，每次通过修改version/config 来触发滚动更新

更新 ConfigMap 后：
	使用该 ConfigMap 挂载的 Env 不会同步更新
	使用该 ConfigMap 挂载的 Volume 中的数据需要一段时间（实测大概10秒）才能同步更新

## 2、Secret

### Secret 存在意义

Secret 解决了密码、token、密钥等敏感数据的配置问题，而不需要把这些敏感数据暴露到镜像或者 Pod Spe中。Secret 可以以 Volume 或者环境变量的方式使用

secret 有三种类型：

> ​	Service Account ：用来访问 Kubernetes API，由 Kubernetes 自动创建，并且会自动挂载到 Pod 的/run/secrets/kubernetes.io/serviceaccount 目录中
>
> ​	Opaque ：base64编码格式的Secret，用来存储密码、密钥等
>
> ​	kubernetes.io/dockerconfigjson ：用来存储私有 docker registry 的认证信息

### Service Account

Service Account 用来访问 Kubernetes API，由 Kubernetes 自动创建，并且会自动挂载到 Pod的/run/secrets/kubernetes.io/serviceaccount 目录中

```
[root@k8s-master01 ~]# kubectl run nginx --image nginx
kubectl run --generator=deployment/apps.v1 is DEPRECATED and will be removed in a future version. Use kubectl run --generator=run-pod/v1 or kubectl create instead.
deployment.apps/nginx created

[root@k8s-master01 ~]# kubectl get pods
NAME                        READY   STATUS    RESTARTS   AGE
my-nginx-7bd5bbc7-cn5pn     1/1     Running   0          12m
nginx-7bb7cd8db5-4r5p5      1/1     Running   0          42s


[root@k8s-master01 ~]# kubectl exec nginx-7bb7cd8db5-4r5p5  ls /run/secrets/kubernetes.io/serviceaccount
ca.crt
namespace
token

```

### Opaque Secret

#### 创建说明

Opaque 类型的数据是一个 map 类型，要求 value 是 base64 编码格式：

```
[root@k8s-master01 ~]# echo -n "admin" | base64
YWRtaW4=
[root@k8s-master01 ~]# echo -n "1f2d1e2e67df" | base64
MWYyZDFlMmU2N2Rm

```

secrets.yml

```
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  password: MWYyZDFlMmU2N2Rm
  username: YWRtaW4=

```



![image-20220119175732670](\images\image-20220119175732670.png)

#### 使用方式

##### 1 将 Secret 挂载到 Volume 中

```yml
apiVersion: v1
kind: Pod
metadata:
  labels:
    name: seret-test
  name: seret-test
spec:
  volumes:
  - name: secrets
    secret:
      secretName: mysecret
  containers:
  - image: hub.harry.com/library/myapp:v1
    name: db
    volumeMounts:
    - name: secrets
      mountPath: "/etc/secrets"
      readOnly: true

```

![image-20220119183009129](\images\image-20220119183009129.png)

##### 2、将 Secret 导出到环境变量中

```yml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: pod-deployment
spec:
  replicas: 2
  template:
    metadata:
      labels:
        app: pod-deployment
    spec:
      containers:
      - name: pod-1
        image: hub.harry.com/library/myapp:v1
        ports:
        - containerPort: 80
        env:
        - name: TEST_USER
          valueFrom:
            secretKeyRef:
              name: mysecret
              key: username
        - name: TEST_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysecret
              key: password

```



![image-20220119184230642](\images\image-20220119184230642.png)

### kubernetes.io/dockerconfigjson

把Harbor仓库的镜像设置成private

![image-20220119190209116](\images\image-20220119190209116.png)

注意现在其他节点把这个docker镜像删掉

```
[root@k8s-node02 ~]# docker rmi hub.harry.com/library/myapp:v1
```

![image-20220119191300192](\images\image-20220119191300192.png)

使用 Kuberctl 创建 docker registry 认证的 secret

```
[root@k8s-master01 ~]#  kubectl create secret docker-registry myregistrykey2 --docker-server=hub.harry.com --docker-username=admin --docker-password=Harbor12345 --docker-email=414804000@qq.com

secret/myregistrykey2 created

```

![image-20220119192203769](\images\image-20220119192203769.png)

在创建 Pod 的时候，通过 imagePullSecrets 来引用刚创建的 `myregistrykey2`

```yml
apiVersion: v1
kind: Pod
metadata:
  name: foo2
spec:
  containers:
    - name: foo
      image: roc/awangyang:v1
  imagePullSecrets:
    - name: myregistrykey2

```

![image-20220119192316396](\images\image-20220119192316396.png)

## 3、volume

​    容器磁盘上的文件的生命周期是短暂的，这就使得在容器中运行重要应用时会出现一些问题。首先，当容器崩溃时，kubelet 会重启它，但是容器中的文件将丢失——容器以干净的状态（镜像最初的状态）重新启动。其次，在Pod 中同时运行多个容器时，这些容器之间通常需要共享文件。Kubernetes 中的 Volume 抽象就很好的解决了
这些问题

​    Kubernetes 中的卷有明确的寿命 —— 与封装它的 Pod 相同。所f以，卷的生命比 Pod 中的所有容器都长，当这个容器重启时数据仍然得以保存。当然，当 Pod 不再存在时，卷也将不复存在。也许更重要的是，Kubernetes
支持多种类型的卷，Pod 可以同时使用任意数量的卷

### 卷的类型

Kubernetes 支持以下类型的卷：

> awsElasticBlockStore azureDisk azureFile cephfs csi downwardAPI emptyDir fc flocker 
>
> gcePersistentDisk gitRepo glusterfs hostPath iscsi local nfs
>
> persistentVolumeClaim projected portworxVolume quobyte rbd scaleIO secret
>
> storageos vsphereVolume

### emptyDir

​    当 Pod 被分配给节点时，首先创建 emptyDir 卷，并且只要该 Pod 在该节点上运行，该卷就会存在。正如卷的名字所述，它最初是空的。Pod 中的容器可以读取和写入 emptyDir 卷中的相同文件，尽管该卷可以挂载到每个容器中的相同或不同路径上。当出于任何原因从节点中删除 Pod 时， emptyDir 中的数据将被永久删除

emptyDir 的用法有：
	暂存空间，例如用于基于磁盘的合并排序
	用作长时间计算崩溃恢复时的检查点
	Web服务器容器提供数据时，保存内容管理器容器提取的文件

```yml
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - name: test-container
    image: wangyanglinux/myapp:v1
    volumeMounts:
    - mountPath: /cache
      name: cache-volume
  - name: liveness-exec-container
    image: busybox
    imagePullPolicy: IfNotPresent
    command: ["/bin/sh","-c","touch /tmp/live ; sleep 60; rm -rf /tmp/live; sleep 36000"]
    volumeMounts:
    - mountPath: /test
      name: cache-volume
  volumes:
  - name: cache-volume
    emptyDir: {}

```

![image-20220120191105024](\images\image-20220120191105024.png)

去另外一个容器发现index.htnl还在

![image-20220120193009721](\images\image-20220120193009721.png)

### hostPath

hostPath 卷将主机节点的文件系统中的文件或目录挂载到集群中

hostPath 的用途如下：

> 运行需要访问 Docker 内部的容器；使用 /var/lib/docker 的 hostPath
>
> 在容器中运行 cAdvisor；使用 /dev/cgroups 的 hostPath
>
> 允许 pod 指定给定的 hostPath 是否应该在 pod 运行之前存在，是否应该创建，以及它应该以什么形式存在

除了所需的 path 属性之外，用户还可以为 hostPath 卷指定 type



![image-20220121141825340](\images\image-20220121141825340.png)

使用这种卷类型是请注意，因为：

> 由于每个节点上的文件都不同，具有相同配置（例如从 podTemplate 创建的）的 pod 在不同节点上的行为可能会有所不同
>
> 当 Kubernetes 按照计划添加资源感知调度时，将无法考虑 hostPath 使用的资源
>
> 在底层主机上创建的文件或目录只能由 root 写入。您需要在特权容器中以 root 身份运行进程，或修改主机上的文件权限以便写入 hostPath 卷

```
# 每个节点创建一个date
[root@k8s-node01 /]# mkdir /data
[root@k8s-node01 /]# date >> index.html

[root@k8s-node02 ~]# mkdir /data
[root@k8s-node02 ~]#

```

```yml
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: wangyanglinux/myapp:v1
    name: test-container
    volumeMounts:
    - mountPath: /test-pd
      name: test-volume
  volumes:
  - name: test-volume
    hostPath:
      # directory location on host
      path: /data
      # this field is optional
      type: Directory

```

## 4、PVC

### PersistentVolume （PV）

是由管理员设置的存储，它是群集的一部分。就像节点是集群中的资源一样，PV 也是集群中的资源。 PV 是Volume 之类的卷插件，但具有独立于使用 PV 的 Pod 的生命周期。此 API 对象包含存储实现的细节，即 NFS、
iSCSI 或特定于云供应商的存储系统

### PersistentVolumeClaim （PVC）

用户存储的请求。它与 Pod 相似。Pod 消耗节点资源，PVC 消耗 PV 资源。Pod 可以请求特定级别的资源（CPU 和内存）。声明可以请求特定的大小和访问模式（例如，可以以读/写一次或 只读多次模式挂载

### 静态 pv

集群管理员创建一些 PV。它们带有可供群集用户使用的实际存储的细节。它们存在于 Kubernetes API 中，可用
于消费

### 动态PV

当管理员创建的静态 PV 都不匹配用户的 PersistentVolumeClaim 时，集群可能会尝试动态地为 PVC 创建卷。此配置基于 StorageClasses ：PVC 必须请求 [存储类]，并且管理员必须创建并配置该类才能进行动态创建。声明该类为 "" 可以有效地禁用其动态配置

启用基于存储级别的动态存储配置，集群管理员需要启用 API server 上的 DefaultStorageClass [准入控制器]。例如，通过确保 DefaultStorageClass 位于 API server 组件的 --admission-control 标志，使用逗号分隔的有序值列表中，可以完成此操作

### 绑定

master 中的控制环路监视新的 PVC，寻找匹配的 PV（如果可能），并将它们绑定在一起。如果为新的 PVC 动态调配 PV，则该环路将始终将该 PV 绑定到 PVC。否则，用户总会得到他们所请求的存储，但是容量可能超出要求的数量。一旦 PV 和 PVC 绑定后， PersistentVolumeClaim 绑定是排他性的，不管它们是如何绑定的。 PVC 跟PV 绑定是一对一的映

PersistentVolume 类型以插件形式实现。Kubernetes 目前支持以下插件类型

> GCEPersistentDisk AWSElasticBlockStore AzureFile AzureDisk FC (Fibre Channel)
>
> FlexVolume Flocker NFS iSCSI RBD (Ceph Block Device) CephFS
>
> Cinder (OpenStack block storage) Glusterfs VsphereVolume Quobyte Volumes
>
> HostPath VMware Photon Portworx Volumes ScaleIO Volumes StorageOS

### 持久卷演示代码

```yml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv0003
spec:
  capacity:
    storage: 5Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Recycle
  storageClassName: slow
  mountOptions:
    - hard
    - nfsvers=4.1
  nfs:
    path: /tmp
    server: 192.168.31.100

```

![image-20220122092142992](\images\image-20220122092142992.png)

### PV 访问模式

PersistentVolume 可以以资源提供者支持的任何方式挂载到主机上。如下表所示，供应商具有不同的功能，每个PV 的访问模式都将被设置为该卷支持的特定模式。例如，NFS 可以支持多个读/写客户端，但特定的 NFS PV 可能
以只读方式导出到服务器上。每个 PV 都有一套自己的用来描述特定功能的访问模式

​	ReadWriteOnce——该卷可以被单个节点以读/写模式挂载
​	ReadOnlyMany——该卷可以被多个节点以只读模式挂载
​	ReadWriteMany——该卷可以被多个节点以读/写模式挂载

在命令行中，访问模式缩写为：

​	RWO - ReadWriteOnce

​	ROX - ReadOnlyMany
​	RWX - ReadWriteMany

![image-20220122092630191](\images\image-20220122092630191.png)

### 回收策略

Retain（保留）——手动回收
Recycle（回收）——基本擦除（ rm -rf /thevolume/* ）
Delete（删除）——关联的存储资产（例如 AWS EBS、GCE PD、Azure Disk 和 OpenStack Cinder 卷）将被删除

当前，只有 NFS 和 HostPath 支持回收策略。AWS EBS、GCE PD、Azure Disk 和 Cinder 卷支持删除策略

### 状态

卷可以处于以下的某种状态：

> ​	Available（可用）——一块空闲资源还没有被任何声明绑定
>
> ​	Bound（已绑定）——卷已经被声明绑定
>
> ​	Released（已释放）——声明被删除，但是资源还未被集群重新声明
>
> ​	Failed（失败）——该卷的自动回收失败

命令行会显示绑定到 PV 的 PVC 的名称

### 持久化演示说明 - NFS

#### 安装 NFS 服务器

```
[root@k8s-habor ~]# yum install -y nfs-common nfs-utils rpcbind
[root@k8s-habor ~]# mkdir /nfsdata
[root@k8s-habor ~]# chmod 666 /nfsdata/
[root@k8s-habor ~]# chown nfsnobody /nfsdata
[root@k8s-habor ~]# cat /etc/exports
/nfsdata *(rw,no_root_squash,no_all_squash,sync)
[root@k8s-habor ~]# systemctl start rpcbind
[root@k8s-habor ~]# systemctl start nfs

```

其他K8S节点安装和挂载NFS

```
[root@k8s-master01 ~]# yum install -y nfs-common nfs-utils rpcbind
[root@k8s-master01 ~]# showmount -e 192.168.31.100
Export list for 192.168.31.100:
/nfsdata *
# 测试挂载
[root@k8s-master01 ~]# mount -t nfs 192.168.31.100:/nfsdata /data/nfs

```



#### 部署PV

```yml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfspv1
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs
  nfs:
    path: /nfsdata # nfs server挂载点目录
    server: 192.168.31.100

```

![image-20220122102411143](\images\image-20220122102411143.png)

创建多个pv

```yml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfspv-2
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadOnlyMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs
  nfs:
    path: /nfsdata1 # nfs server挂载点目录
    server: 192.168.31.100
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfspv-3
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadOnlyMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs
  nfs:
    path: /nfsdata2 # nfs server挂载点目录
    server: 192.168.31.100
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfspv-4
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs
  nfs:
    path: /nfsdata3 # nfs server挂载点目录
    server: 192.168.31.100


```

![image-20220122104052866](\images\image-20220122104052866.png)

#### 创建PVC

```yml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  ports:
  - port: 80
    name: web
  clusterIP: None
  selector:
    app: nginx

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  selector:
    matchLabels:
      app: nginx
  serviceName: "nginx"
  replicas: 3
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: wangyanglinux/myapp:v1
        ports:
        - containerPort: 80
          name: web
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: "nfs"
      resources:
        requests:
          storage: 1Gi

```

web-1的这个pod并没有绑定pv成功， 因为满足RWO的pv只有一个

![image-20220122105318886](\images\image-20220122105318886.png)

![image-20220122105339733](\images\image-20220122105339733.png)

![image-20220122105543942](\images\image-20220122105543942.png)

再创建两个RWO的pv 看到已经绑定成功

![image-20220122110357393](\images\image-20220122110357393.png)

#### 关于 StatefulSet

> 匹配 Pod name ( 网络标识 ) 的模式为：$(statefulset名称)-$(序号)，比如上面的示例：web-0，web-1，web-2
>
> StatefulSet 为每个 Pod 副本创建了一个 DNS 域名，这个域名的格式为： $(podname).(headless servername)，也就意味着服务间是通过Pod域名来通信而非 Pod IP，因为当Pod所在Node发生故障时， Pod 会被飘移到其它 Node 上，Pod IP 会发生变化，但是 Pod 域名不会有变化
>
> StatefulSet 使用 Headless 服务来控制 Pod 的域名，这个域名的 FQDN 为：$(servicename).$(namespace).svc.cluster.local，其中，“cluster.local” 指的是集群的域名
>
> 根据 volumeClaimTemplates，为每个 Pod 创建一个 pvc，pvc 的命名规则匹配模式：(volumeClaimTemplates.name)-(pod_name)，比如上面的 volumeMounts.name=www， Pod
> name=web-[0-2]，因此创建出来的 PVC 是 www-web-0、www-web-1、www-web-2
>
> 删除 Pod 不会删除其 pvc，手动删除 pvc 将自动释放 pv

![image-20220122111311946](\images\image-20220122111311946.png)



Statefulset的启停顺序：

> 有序部署：部署StatefulSet时，如果有多个Pod副本，它们会被顺序地创建（从0到N-1）并且，在下一个
> Pod运行之前所有之前的Pod必须都是Running和Ready状态。
>
> 有序删除：当Pod被删除时，它们被终止的顺序是从N-1到0。
>
> 有序扩展：当对Pod执行扩展操作时，与部署一样，它前面的Pod必须都处于Running和Ready状态



StatefulSet使用场景：

> 稳定的持久化存储，即Pod重新调度后还是能访问到相同的持久化数据，基于 PVC 来实现。
>
> 稳定的网络标识符，即 Pod 重新调度后其 PodName 和 HostName 不变。
>
> 有序部署，有序扩展，基于 init containers 来实现。
>
> 有序收缩

# 七、K8S调度器

## 简介

Scheduler 是 kubernetes 的调度器，主要的任务是把定义的 pod 分配到集群的节点上。听起来非常简单，但有很多要考虑的问题：

> 公平：如何保证每个节点都能被分配资源
> 资源高效利用：集群所有资源最大化被使用
> 效率：调度的性能要好，能够尽快地对大批量的 pod 完成调度工作
> 灵活：允许用户根据自己的需求控制调度的逻辑

Sheduler 是作为单独的程序运行的，启动之后会一直坚挺 API Server，获取 PodSpec.NodeName 为空的 pod，对每个 pod 都会创建一个 binding，表明该 pod 应该放到哪个节点上

### 调度过程

调度分为几个部分：首先是过滤掉不满足条件的节点，这个过程称为  predicate ；然后对通过的节点按照优先级排序，这个是  priority ；最后从中选择优先级最高的节点。如果中间任何一步骤有错误，就直接返回错误

Predicate 有一系列的算法可以使用：

> PodFitsResources ：节点上剩余的资源是否大于 pod 请求的资源
> PodFitsHost ：如果 pod 指定了 NodeName，检查节点名称是否和 NodeName 匹配
> PodFitsHostPorts ：节点上已经使用的 port 是否和 pod 申请的 port 冲突
> PodSelectorMatches ：过滤掉和 pod 指定的 label 不匹配的节点
> NoDiskConflict ：已经 mount 的 volume 和 pod 指定的 volume 不冲突，除非它们都是只读

如果在 predicate 过程中没有合适的节点，pod 会一直在  pending  状态，不断重试调度，直到有节点满足条件。
经过这个步骤，如果有多个节点满足条件，就继续 priorities 过程： 按照优先级大小对节点排序

优先级由一系列键值对组成，键是该优先级项的名称，值是它的权重（该项的重要性）。这些优先级选项包括：

> LeastRequestedPriority ：通过计算 CPU 和 Memory 的使用率来决定权重，使用率越低权重越高。换句话
> 说，这个优先级指标倾向于资源使用比例更低的节点
>
> BalancedResourceAllocation ：节点上 CPU 和 Memory 使用率越接近，权重越高。这个应该和上面的一起
> 使用，不应该单独使用
>
> ImageLocalityPriority ：倾向于已经有要使用镜像的节点，镜像总大小值越大，权重越高

### 自定义调度器

除了 kubernetes 自带的调度器，你也可以编写自己的调度器。通过 spec:schedulername 参数指定调度器的名字，可以为 pod 选择某个调度器进行调度。比如下面的 pod 选择 my-scheduler 进行调度，而不是默认default-schedulera ：

```yml
apiVersion: v1
kind: Pod
metadata:
  name: annotation-second-scheduler
  labels:
    name: multischeduler-example
spec:
  schedulername: my-scheduler
  containers:
  - name: pod-with-second-annotation-container
    image: gcr.io/google_containers/pause:2.0
```

## 节点亲和性

pod.spec.nodeAffinity

> referredDuringSchedulingIgnoredDuringExecution：软策略
> requiredDuringSchedulingIgnoredDuringExecution：硬策略

requiredDuringSchedulingIgnoredDuringExecution

```yml
apiVersion: v1
kind: Pod
metadata:
  name: affinity
  labels:
    app: node-affinity-pod
spec:
  containers:
  - name: with-node-affinity
    image: hub.harry.com/library/myapp:v1
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: kubernetes.io/hostname
            # 不能在node1上运行
            operator: NotIn
            values:
            - k8s-node01

```

![image-20220124162311239](\images\image-20220124162311239.png)

preferredDuringSchedulingIgnoredDuringExecution

![image-20220124164136687](\images\image-20220124164136687.png)

```yml
apiVersion: v1
kind: Pod
metadata:
  name: affinity
  labels:
    app: node-affinity-pod
spec:
  containers:
  - name: with-node-affinity
    image: hub.harry.com/library/myapp:v1
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        preference:
          matchExpressions:
          - key: kubernetes.io/hostname
            operator: In
            values:
            - k8s-node02

```

![image-20220124164520497](\images\image-20220124164520497.png)

合体

```yml
apiVersion: v1
kind: Pod
metadata:
  name: affinity
  labels:
    app: node-affinity-pod
spec:
  containers:
  - name: with-node-affinity
    image: hub.harry.com/library/myapp:v1
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: kubernetes.io/hostname
            # 不能在node1上运行
            operator: NotIn
            values:
             - k8s-node01
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        preference:
          matchExpressions:
          - key: kubernetes.io/hostname
            operator: In
            values:
            - k8s-node02

```

键值运算关系

> In：label 的值在某个列表中
> NotIn：label 的值不在某个列表中
> Gt：label 的值大于某个值
> Lt：label 的值小于某个值
> Exists：某个 label 存在
> DoesNotExist：某个 label 不存在p

## Pod 亲和性

pod.spec.affinity.podAffinity/podAntiAffinity

preferredDuringSchedulingIgnoredDuringExecution：软策略

```yml
apiVersion: v1
kind: Pod
metadata:
  name: pod-4
  labels:
    app: pod-4
spec:
  containers:
  - name: pod-4
    image: hub.harry.com/library/myapp:v1
  affinity:
    podAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        podAffinityTerm:
          labelSelector:
            matchExpressions:
            - key: app
              operator: In
              values:
              - pod-2
          topologyKey: kubernetes.io/hostname

```

requiredDuringSchedulingIgnoredDuringExecution：硬策略

```yml
apiVersion: v1
kind: Pod
metadata:
  name: pod-3
  labels:
    app: pod-3
spec:
  containers:
  - name: pod-3
    image: hub.harry.com/library/myapp:v1
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - pod-1
        topologyKey: kubernetes.io/hostname

```

因为现在的pod里面没有一个标签app=pod-1所有pod一直是peddling状态

![image-20220124173054748](\images\image-20220124173054748.png)

修改affinity的标签

```
[root@k8s-master01 ~]# kubectl label pod affinity app=pod-1 --overwrite=true
pod/affinity labeled

```

![image-20220124173249695](\images\image-20220124173249695.png)

亲和性/反亲和性调度策略比较如下：

![image-20220124171926859](\images\image-20220124171926859.png)

## Taint 和 Toleration

节点亲和性，是 pod 的一种属性（偏好或硬性要求），它使 pod 被吸引到一类特定的节点。Taint 则相反，它使节点能够 排斥 一类特定的 pod

aint 和 toleration 相互配合，可以用来避免 pod 被分配到不合适的节点上。每个节点上都可以应用一个或多个taint ，这表示对于那些不能容忍这些 taint 的 pod，是不会被该节点接受的。如果将 toleration 应用于 pod上，则表示这些 pod 可以（但不要求）被调度到具有匹配 taint 的节点上

### 污点(Taint)

污点 ( Taint ) 的组成

使用 kubectl taint 命令可以给某个 Node 节点设置污点，Node 被设置上污点之后就和 Pod 之间存在了一种相
斥的关系，可以让 Node 拒绝 Pod 的调度执行，甚至将 Node 已经存在的 Pod 驱逐出去

每个污点的组成如下：

```
key=value:effect
```

每个污点有一个 key 和 value 作为污点的标签，其中 value 可以为空，effect 描述污点的作用。当前 tainteffect 支持如下三个选项：

> NoSchedule ：表示 k8s 将不会将 Pod 调度到具有该污点的 Node 上
>
> PreferNoSchedule ：表示 k8s 将尽量避免将 Pod 调度到具有该污点的 Node 上
>
> NoExecute ：表示 k8s 将不会将 Pod 调度到具有该污点的 Node 上，同时会将 Node 上已经存在的 Pod 驱
> 逐出去

污点的设置、查看和去除

```
# 设置污点
kubectl taint nodes node1 key1=value1:NoSchedule
[root@k8s-master01 ~]# kubectl taint nodes k8s-node01 check=harry:NoSchedule

# 节点说明中，查找 Taints 字段
[root@k8s-master01 ~]# kubectl describe node k8s-node01
# 去除污点
kubectl taint nodes node1 key1:NoSchedule
[root@k8s-master01 ~]# kubectl taint node k8s-node01 check:NoSchedule-

```

![image-20220124180353011](\images\image-20220124180353011.png)

### 容忍(Tolerations)

设置了污点的 Node 将根据 taint 的 effect：NoSchedule、PreferNoSchedule、NoExecute 和 Pod 之间产生互斥的关系，Pod 将在一定程度上不会被调度到 Node 上。 但我们可以在 Pod 上设置容忍 ( Toleration ) ，意思是设置了容忍的 Pod 将可以容忍污点的存在，可以被调度到存在污点的 Node 上

pod.spec.tolerations

```yml
tolerations:
- key: "key1"
  operator: "Equal"
  value: "value1"
  effect: "NoSchedule"
  tolerationSeconds: 3600
- key: "key1"
  operator: "Equal"
  value: "value1"
  effect: "NoExecute"
- key: "key2"
  operator: "Exists"
  effect: "NoSchedule"
```

其中 key, vaule, effect 要与 Node 上设置的 taint 保持一致
operator 的值为 Exists 将会忽略 value 值
tolerationSeconds 用于描述当 Pod 需要被驱逐时可以在 Pod 上继续保留运行的时间

当不指定 key 值时，表示容忍所有的污点 key：

```
tolerations:
- operator: "Exists"
```

当不指定 effect 值时，表示容忍所有的污点作用

```
tolerations:
- key: "key"
  operator: "Exists"
```

有多个 Master 存在时，防止资源浪费，可以如下设置

```
kubectl taint nodes Node-Name node-role.kubernetes.io/master=:PreferNoSchedule
```

# 八、K8S集群安全

## 机制说明

Kubernetes 作为一个分布式集群的管理工具，保证集群的安全性是其一个重要的任务。API Server 是集群内部
各个组件通信的中介，也是外部控制的入口。所以 Kubernetes 的安全机制基本就是围绕保护 API Server 来设计
的。Kubernetes 使用了认证（Authentication）、鉴权（Authorization）、准入控制（AdmissionControl）三步来保证API Server的安全

![image-20220125153045679](\images\image-20220125153045679.png)

## Authentication

HTTP Token 认证：通过一个 Token 来识别合法用户

> HTTP Token 的认证是用一个很长的特殊编码方式的并且难以被模仿的字符串 - Token 来表达客户的一
> 种方式。Token 是一个很长的很复杂的字符串，每一个 Token 对应一个用户名存储在 API Server 能访
> 问的文件中。当客户端发起 API 调用请求时，需要在 HTTP Header 里放入 Token

HTTP Base 认证：通过 用户名+密码 的方式认证

> 用户名+：+密码 用 BASE64 算法进行编码后的字符串放在 HTTP Request 中的 HeatherAuthorization 域里发送给服务端，服务端收到后进行编码，获取用户名及密码

最严格的 HTTPS 证书认证：基于 CA 根证书签名的客户端身份认证方式

### HTTPS 证书认证：

![image-20220125153403823](\images\image-20220125153403823.png)

### 需要认证的节点

![image-20220125153438004](\images\image-20220125153438004.png)

两种类型

Kubenetes 组件对 API Server 的访问：kubectl、Controller Manager、Scheduler、kubelet、kube-proxy

Kubernetes 管理的 Pod 对容器的访问：Pod（dashborad 也是以 Pod 形式运行）

安全性说明

Controller Manager、Scheduler 与 API Server 在同一台机器，所以直接使用 API Server 的非安全端口访问， --insecure-bind-address=127.0.0.1

kubectl、kubelet、kube-proxy 访问 API Server 就都需要证书进行 HTTPS 双向认证

证书颁发

手动签发：通过 k8s 集群的跟 ca 进行签发 HTTPS 证书

自动签发：kubelet 首次访问 API Server 时，使用 token 做认证，通过后，Controller Manager 会为kubelet 生成一个证书，以后的访问都是用证书做认证

### kubeconfig

kubeconfig 文件包含集群参数（CA证书、API Server地址），客户端参数（上面生成的证书和私钥），集群
context 信息（集群名称、用户名）。Kubenetes 组件通过启动时指定不同的 kubeconfig 文件可以切换到不同
的集群

### ServiceAccount

Pod中的容器访问API Server。因为Pod的创建、销毁是动态的，所以要为它手动生成证书就不可行了。
Kubenetes使用了Service Account解决Pod 访问API Server的认证问题

### Secret 与 SA 的关系

Kubernetes 设计了一种资源对象叫做 Secret，分为两类，一种是用于 ServiceAccount 的 service-account-
token， 另一种是用于保存用户自定义保密信息的 Opaque。ServiceAccount 中用到包含三个部分：Token、
ca.crt、namespace

> token是使用 API Server 私钥签名的 JWT。用于访问API Server时，Server端认证
>
> ca.crt，根证书。用于Client端验证API Server发送的证书
>
> namespace, 标识这个service-account-token的作用域名空间

```
[root@k8s-master01 ~]# kubectl get secret --all-namespaces
```

![image-20220125154352318](\images\image-20220125154352318.png)

```
[root@k8s-master01 ~]# kubectl describe secret default-token-r6fs8  --namespace=kube-system
```

![image-20220125154719357](\images\image-20220125154719357.png)

默认情况下，每个 namespace 都会有一个 ServiceAccount，如果 Pod 在创建时没有指定 ServiceAccount，就会使用 Pod 所属的 namespace 的 ServiceAccount

### 总结

![image-20220125154826416](\images\image-20220125154826416.png)

## Authorization

上面认证过程，只是确认通信的双方都确认了对方是可信的，可以相互通信。而鉴权是确定请求方有哪些资源的权
限。API Server 目前支持以下几种授权策略 （通过 API Server 的启动参数 “--authorization-mode” 设置）

> AlwaysDeny：表示拒绝所有的请求，一般用于测试
> AlwaysAllow：允许接收所有请求，如果集群不需要授权流程，则可以采用该策略
> ABAC（Attribute-Based Access Control）：基于属性的访问控制，表示使用用户配置的授权规则对用户
> 请求进行匹配和控制
> Webbook：通过调用外部 REST 服务对用户进行授权
> RBAC（Role-Based Access Control）：基于角色的访问控制，现行默认规则

### RBAC 授权模式

BAC（Role-Based Access Control）基于角色的访问控制，在 Kubernetes 1.5 中引入，现行版本成为默认标
准。相对其它访问控制方式，拥有以下优势：

> 对集群中的资源和非资源均拥有完整的覆盖
>
> 整个 RBAC 完全由几个 API 对象完成，同其它 API 对象一样，可以用 kubectl 或 API 进行操作
>
> 可以在运行时进行调整，无需重启 API Server

### RBAC 的 API 资源对象说明

RBAC 引入了 4 个新的顶级资源对象：Role、ClusterRole、RoleBinding、ClusterRoleBinding，4 种对象类型
均可以通过 kubectl 与 API 操作

![image-20220125165304793](\images\image-20220125165304793.png)

需要注意的是 Kubenetes 并不会提供用户管理，那么 User、Group、ServiceAccount 指定的用户又是从哪里
来的呢？ Kubenetes 组件（kubectl、kube-proxy）或是其他自定义的用户在向 CA 申请证书时，需要提供一个
证书请求文件



```json

"CN": "admin",
"hosts": [],
"key": {
   "algo": "rsa",
   "size": 2048
},
"names": [
  {
    "C": "CN",
    "ST": "HangZhou",
    "L": "XS",
    "O": "system:masters",
   "OU": "System"
   }
  ]
}
```

API Server会把客户端证书的 CN 字段作为User，把 names.O 字段作为Group

kubelet 使用 TLS Bootstaping 认证时，API Server 可以使用 Bootstrap Tokens 或者 Token authentication file 验证 =token，无论哪一种，Kubenetes 都会为 token 绑定一个默认的 User 和 Group

Pod使用 ServiceAccount 认证时，service-account-token 中的 JWT 会保存 User 信息

有了用户信息，再创建一对角色/角色绑定(集群角色/集群角色绑定)资源对象，就可以完成权限绑定了

### Role and ClusterRole

在 RBAC API 中，Role 表示一组规则权限，权限只会增加(累加权限)，不存在一个资源一开始就有很多权限而通过
RBAC 对其进行减少的操作；Role 可以定义在一个 namespace 中，如果想要跨 namespace 则可以创建ClusterRole

```yml
kind: Role
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""] # "" indicates the core API group
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

ClusterRole 具有与 Role 相同的权限角色控制能力，不同的是 ClusterRole 是集群级别的，ClusterRole 可以用
于:

> 集群级别的资源控制( 例如 node 访问权限 )
> 非资源型 endpoints( 例如 /healthz 访问 ）
>
> 所有命名空间资源控制(例如 pods ）

```yml
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  # "namespace" omitted since ClusterRoles are not namespaced
  name: secret-reader
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "watch", "list"]
```

### RoleBinding and ClusterRoleBinding

RoloBinding 可以将角色中定义的权限授予用户或用户组，RoleBinding 包含一组权限列表(subjects)，权限列
表中包含有不同形式的待授予权限资源类型(users, groups, or service accounts)；RoloBinding 同样包含对被
Bind 的 Role 引用；RoleBinding 适用于某个命名空间内授权，而 ClusterRoleBinding 适用于集群范围内的授
权

```yml
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: User
  name: jane
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.aut
```

RoleBinding 同样可以引用 ClusterRole 来对当前 namespace 内用户、用户组或 ServiceAccount 进行授权，
这种操作允许集群管理员在整个集群内定义一些通用的 ClusterRole，然后在不同的 namespace 中使用
RoleBinding 来引用

例如，以下 RoleBinding 引用了一个 ClusterRole，这个 ClusterRole 具有整个集群内对 secrets 的访问权限；
但是其授权用户  dave  只2能访问 development 空间中的 secrets(因为 RoleBinding 定义在 development 命
名空间)

```yml
# This role binding allows "dave" to read secrets in the "development" namespace.
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: read-secrets
  # This only grants permissions within the "development" namespace.
  namespace: development 
subjects:
- kind: User
  name: dave
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```

使用 ClusterRoleBinding 可以对整个集群中的所有命名空间资源权限进行授权；以下 ClusterRoleBinding 样例
展示了授权 manager 组内所有用户在全部命名空间中对 secrets 进行访问

```yml
# This cluster role binding allows anyone in the "manager" group to read secrets in any
namespace.
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: read-secrets-global
subjects:
- kind: Group
  name: manager
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```

### Resources

Kubernetes 集群内一些资源一般以其名称字符串来表示，这些字符串一般会在 API 的 URL 地址中出现；同时某些资源也会包含子资源，例如 logs 资源就属于 pods 的子资源，API 中 URL 样例

```
GET /api/v1/namespaces/{namespace}/pods/{name}/log
```

如果要在 RBAC 授权模型中控制这些子资源的访问权限，可以通过 / 分隔符来实现，以下是一个定义 pods 资资源
logs 访问权限的 Role 定义样例

```yml
kind: Role
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  namespace: default
  name: pod-and-pod-logs-reader
rules:
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get", "list"]
```

### to Subjects

RoleBinding 和 ClusterRoleBinding 可以将 Role 绑定到 Subjects；Subjects 可以是 groups、users 或者service accounts

Subjects 中 Users 使用字符串表示，它可以是一个普通的名字字符串，如 “alice”；也可以是 email 格式的邮箱地址，如 “wangyanglinux@163.com”；甚至是一组字符串形式的数字 ID 。但是 Users 的前缀 system: 是系统保留的，集群管理员应该确保普通用户不会使用这个前缀格式

Groups 书写格式与 Users 相同，都为一个字符串，并且没有特定的格式要求；同样 system: 前缀为系统保留

### 实践：创建一个用户只能管理 dev空间

```
{
  "CN": "devuser",
  "hosts": [],
  "key": {
     "algo": "rsa",
     "size": 2048
  },
  "names": [
    {
      "C": "CN",
     "ST": "BeiJing",
      "L": "BeiJing",
      "O": "k8s",
     "OU": "System"
    }
  ]
}
#创建dev用户
[root@k8s-master01 install-k8s]# useradd devuser
[root@k8s-master01 install-k8s]# passwd devuser
[root@k8s-master01 devuser]# pwd
/root/install-k8s/cert/devuser

# 下载证书生成工具
[root@k8s-master01 devuser]# wget https://pkg.cfssl.org/R1.2/cfssl_linux-amd64
[root@k8s-master01 devuser]# mv cfssl_linux-amd64 /usr/local/bin/cfssl 

[root@k8s-master01 devuser]# wget https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64
[root@k8s-master01 devuser]# mv cfssljson_linux-amd64 /usr/local/bin/cfssljson

[root@k8s-master01 devuser]# wget https://pkg.cfssl.org/R1.2/cfssl-certinfo_linux-amd64
[root@k8s-master01 devuser]# mv cfssl-certinfo_linux-amd64 /usr/local/bin/cfssl-certinfo
[root@k8s-master01 devuser]# cd /etc/kubernetes/pki/
[root@k8s-master01 pki]# cfssl gencert -ca=ca.crt -ca-key=ca.key -profile=kubernetes /root/install-k8s/cert/devuser/user-csr.json | cfssljson -bare devuser

# 设置集群参数
[root@k8s-master01 devuser]# export KUBE_APISERVER="https://192.168.31.10:6443"
[root@k8s-master01 devuser]# kubectl config set-cluster kubernetes --certificate-authority=/etc/kubernetes/pki/ca.crt --embed-certs=true --server=${KUBE_APISERVER} --kubeconfig=devuser.kubeconfig

```

![image-20220125210306905](\images\image-20220125210306905.png)

```
# 设置客户端认证参数
[root@k8s-master01 devuser]# kubectl config set-credentials devuser \
> --client-certificate=/etc/kubernetes/pki/devuser.pem \
> --client-key=/etc/kubernetes/pki/devuser-key.pem \
> --embed-certs=true \
> --kubeconfig=devuser.kubeconfig
User "devuser" set.

# 设置上下文参数
[root@k8s-master01 devuser]# kubectl create namespace dev
namespace/dev created

[root@k8s-master01 devuser]# kubectl config set-context kubernetes \
> --cluster=kubernetes \
> --user=devuser \
> --namespace=dev \
> --kubeconfig=devuser.kubeconfig
Context "kubernetes" created.

# rolebinding 绑定权限， 相当于dev用户在dev的名称空间下有管理员权限
[root@k8s-master01 devuser]# kubectl create rolebinding devuser-admin-binding --clusterrole=admin --user=devuser --namespace=dev
rolebinding.rbac.authorization.k8s.io/devuser-admin-binding created
[root@k8s-master01 devuser]# cp devuser.kubeconfig /home/devuser/.kube/
[root@k8s-master01 devuser]# chown devuser:devuser /home/devuser/.kube/devuser.kubeconfig
[devuser@k8s-master01 .kube]$ mv devuser.kubeconfig config

# 设置默认上文
[devuser@k8s-master01 .kube]$ kubectl config use-context kubernetes --kubeconfig=config
Switched to context "kubernetes".


```

在default名称空间下可以看到没有任何pod

![image-20220125211602509](\images\image-20220125211602509.png)

创建一个pod在当前名称空间下

```
[devuser@k8s-master01 .kube]$ kubectl run nginx --image=wangyanglinux/myapp:v1

```

![image-20220125211952902](\images\image-20220125211952902.png)

## 准入控制

准入控制是API Server的插件集合，通过添加不同的插件，实现额外的准入控制规则。甚至于API Server的一些主
要的功能都需要通过 Admission Controllers 实现，比如 ServiceAccount

官方文档上有一份针对不同版本的准入控制器推荐列表，其中最新的 1.14 的推荐列表是

```
amespaceLifecycle,LimitRanger,ServiceAccount,DefaultStorageClass,DefaultTolerationSeconds,MutatingAdmissionWebhook,ValidatingAdmissionWebhook,ResourceQuota
```

列举几个插件的功能：

> NamespaceLifecycle： 防止在不存在的 namespace 上创建对象，防止删除系统预置 namespace，删除
> namespace 时，连带删除它的所有资源对象。
> LimitRanger：确保请求的资源不会超过资源所在 Namespace 的 LimitRange 的限制。
> ServiceAccount： 实现了自动化添加 ServiceAccount。
> ResourceQuota：确保请求的资源不会超过资源的 ResourceQuota 限制。

# 九、Helm

## 什么是 Helm

在没使用 helm 之前，向 kubernetes 部署应用，我们要依次部署 deployment、svc 等，步骤较繁琐。况且随着很多项目微服务化，复杂的应用在容器中部署以及管理显得较为复杂，helm 通过打包的方式，支持发布的版本管理和控制，很大程度上简化了 Kubernetes 应用的部署和管理

Helm 本质就是让 K8s 的应用管理（Deployment,Service 等 ) 可配置，能动态生成。通过动态生成 K8s 资源清单文件（deployment.yaml，service.yaml）。然后调用 Kubectl 自动执行 K8s 资源部

Helm 是官方提供的类似于 YUM 的包管理器，是部署环境的流程封装。Helm 有两个重要的概念：chart 和
release

> chart 是创建一个应用的信息集合，包括各种 Kubernetes 对象的配置模板、参数定义、依赖关系、文档说明等。chart 是应用部署的自包含逻辑单元。可以将 chart 想象成 apt、yum 中的软件安装包
>
> release 是 chart 的运行实例，代表了一个正在运行的应用。当 chart 被安装到 Kubernetes 集群，就生成一个 release。chart 能够多次安装到同一个集群，每次安装都是一个 release

Helm 包含两个组件：Helm 客户端和 Tiller 服务器，如下图所示

![image-20220126134842520](\images\image-20220126134842520.png)

Helm 客户端负责 chart 和 release 的创建和管理以及和 Tiller 的交互。Tiller 服务器运行在 Kubernetes 集群
中，它会处理 Helm 客户端的请求，与 Kubernetes API Server 交互

## Helm 部署

越来越多的公司和团队开始使用 Helm 这个 Kubernetes 的包管理器，我们也将使用 Helm 安装 Kubernetes 的常用组件。 Helm 由客户端命 helm 令行工具和服务端 tiller 组成，Helm 的安装十分简单。 下载 helm 命令行工具到master 节点 node1 的 /usr/local/bin 下，这里下载的 2.13. 1版本：

```
[root@k8s-master01 ~]# wget https://storage.googleapis.com/kubernetes-helm/helm-v2.13.1-linux-amd64.tar.gz
[root@k8s-master01 ~]# tar -zxvf helm-v2.13.1-linux-amd64.tar.gz
[root@k8s-master01 linux-amd64]# cd linux-amd64/
[root@k8s-master01 linux-amd64]# cp helm /usr/local/bin

```

为了安装服务端 tiller，还需要在这台机器上配置好 kubectl 工具和 kubeconfig 文件，确保 kubectl 工具可以
在这台机器上访问 apiserver 且正常使用。 这里的 node1 节点以及配置好了 kubectl

因为 Kubernetes APIServer 开启了 RBAC 访问控制，所以需要创建 tiller 使用的 service account: tiller 并分
配合适的角色给它。  这里简单起见直接分配cluster- admin 这个集群内置的 ClusterRole 给它。创建 rbac-config.yaml 文件：

```yml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: tiller
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: tiller
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
  - kind: ServiceAccount
    name: tiller
    namespace: kube-system

```

```
[root@k8s-master01 install-k8s]# kubectl create -f rbac-config.yml
serviceaccount/tiller created
clusterrolebinding.rbac.authorization.k8s.io/tiller created

```

```
[root@k8s-master01 install-k8s]# helm init --service-account tiller --skip-refresh

```

![image-20220126140706105](\images\image-20220126140706105.png)

tiller 默认被部署在 k8s 集群中的 kube-system 这个namespace 下

![image-20220126140859780](\images\image-20220126140859780.png)

![image-20220126140934406](\images\image-20220126140934406.png)

## Helm 自定义模板

```
[root@k8s-master01 hellowrold]# mkdir hellowrold
# 创建自描述文件 Chart.yaml , 这个文件必须有 name 和 version 定
```

```
cat <<'EOF' > ./Chart.yaml
name: hello-world
version: 1.0.0
EOF
```

```
# 创建模板文件， 用于生成 Kubernetes 资源清单（manifests）
[root@k8s-master01 hellowrold]# mkdir  templates

```

```yml
cat <<'EOF' > ./templates/deployment.yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: hello-world
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: hello-world
    spec:
      containers:
        - name: hello-world
          image: wangyanglinux/myapp:v1
          ports:
            - containerPort: 80
              protocol: TCP
EOF
```



```YML
cat <<'EOF' > ./templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-world
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
  selector:
    app: hello-world
EOF
```

```
# 使用命令 helm install RELATIVE_PATH_TO_CHART 创建一次Release
[root@k8s-master01 hellowrold]# helm install .

```

![image-20220126190524176](\images\image-20220126190524176.png)

```
# 列出已经部署的 Release
[root@k8s-master01 hellowrold]# helm list

```

![image-20220126191401346](\images\image-20220126191401346.png)

```
# 查询一个特定的 Release 的状态
[root@k8s-master01 hellowrold]# helm status exasperated-ibex
```

![image-20220126192006741](\images\image-20220126192006741.png)

```
# 移除所有与这个 Release 相关的 Kubernetes 资源
[root@k8s-master01 hellowrold]# helm delete exasperated-ibex
release "exasperated-ibex" deleted

```

![image-20220126192214058](\images\image-20220126192214058.png)

```
[root@k8s-master01 hellowrold]# helm rollback exasperated-ibex 1
Rollback was a success! Happy Helming!
```

使用 helm delete --purge RELEASE_NAME 移除所有与指定 Release 相关的 Kubernetes 资源和所有这个
Release 的记录

```
helm delete --purge exasperated-ibex
```

```yml
 #配置体现在配置文件 values.yaml
 image:
  repository: wangyanglinux/myapp
  tag: 'v2'
# 这个文件中定义的值，在模板文件中可以通过 .VAlues对象访问到
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: hello-world
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: hello-world
    spec:
      containers:
        - name: hello-world
          image: {{ .Values.image.repository }}:{{ .Values.image.tag }}
          ports:
            - containerPort: 80
              protocol: TCP

# 在 values.yaml 中的值可以被部署 release 时用到的参数 --values YAML_FILE_PATH 或 --set
key1=value1, key2=value2 覆盖掉
$ helm install --set image.tag='latest' 
```

### Debug

```
# 使用模板动态生成K8s资源清单，非常需要能提前预览生成的结果。
# 使用--dry-run --debug 选项来打印出生成的清单文件内容，而不执行部署
helm install . --dry-run --debug --set image.tag=latest
```

### Failed to fetch https://kubernetes-charts.storage.googleapis.com/index.yaml : 403 Forbidden

```
$ helm repo remove stable
$ helm repo add stable https://charts.helm.sh/stable
$ helm repo update
```

## 使用Helm部署 dashboard

```
[root@k8s-node01 ~]# docker load -i dashboard.tar
```

kubernetes-dashboard.yaml

```yml
image:
  repository: k8s.gcr.io/kubernetes-dashboard-amd64
  tag: v1.10.1
ingress:
  enabled: true
  hosts:
    - k8s.frognew.com
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
  tls:
    - secretName: frognew-com-tls-secret
      hosts:
      - k8s.frognew.com
rbac:
  clusterAdminRole: true

```

```
[root@k8s-master01 dashboard]# helm install stable/kubernetes-dashboard -n kubernetes-dashboard --namespace kube-system -f kubernets-dashboard.yml

```

![image-20220127145914834](\images\image-20220127145914834.png)

```shell
修改 ClusterIP 为 NodePort
[root@k8s-master01 plugin]# kubectl edit svc kubernetes-dashboard -n kube-system
service/kubernetes-dashboard edited
```

![image-20220127150624294](\images\image-20220127150624294.png)

![image-20220127152736469](\images\image-20220127152736469.png)

## 部署部署 prometheus

Prometheus github 地址：https://github.com/coreos/kube-prometheus

### 组件说明

> 1.MetricServer：是kubernetes集群资源使用情况的聚合器，收集数据给kubernetes集群内使用，如
> kubectl,hpa,scheduler等。 
>
> 2.PrometheusOperator：是一个系统监测和警报工具箱，用来存储监控数据。
>
> 3.NodeExporter：用于各node的关键度量指标状态数据。
>
> 4.KubeStateMetrics：收集kubernetes集群内资源对象数据，制定告警规则。 
>
> 5.Prometheus：采用pull方式收集apiserver，scheduler，controller-manager，kubelet组件数
> 据，通过http协议传输。
>
> 6.Grafana：是可视化数据统计和监控平台

### 构建记录

```
[root@k8s-master01 prometheus]# git clone https://github.com/coreos/kube-prometheus.git
[root@k8s-master01 prometheus]# cd kube-prometheus/manifests/

```

修改 grafana-service.yaml 文件，使用 nodepode 方式访问 grafana：

```yml
apiVersion: v1
kind: Service
metadata:p
  labels:
    app: grafana
  name: grafana
  namespace: monitoring
spec:
  type: NodePort # 添加内容
  ports:
  - name: http
    port: 3000
    targetPort: http
    nodePort: 30100 # 添加内容
  selector:
    app: grafana

```

修改 prometheus-service.yaml，改为 nodepode

```yml
apiVersion: v1
kind: Service
metadata:
  labels:
    prometheus: k8s
  name: prometheus-k8s
  namespace: monitoring
spec:
  type: NodePort
  ports:
  - name: web
    port: 9090
    targetPort: web
  selector:
    app: prometheus
    prometheus: k8s
  sessionAffinity: ClientIP


```

修改 alertmanager-service.yaml，改为 nodepode

```yml
apiVersion: v1
kind: Service
metadata:
  labels:
    alertmanager: main
  name: alertmanager-main
  namespace: monitoring
spec:
  type: NodePort
  ports:
  - name: web
    port: 9093
    targetPort: web
  selector:
    alertmanager: main
    app: alertmanager
  sessionAffinity: ClientIP


```

### 

```bash
# load容器
#!/bin/bash
cd /root/prometheus
ls /root/prometheus | grep -v load-images.sh > /tmp/k8s-images.txt
for i in $( cat  /tmp/k8s-images.txt )
do
    docker load -i $i
done
rm -rf /tmp/k8s-images.txt

[root@k8s-master01 manifests]# kubectl apply -f /root/installk8s/helm/plugin/prometheus/kube-prometheus/manifests/


```

![image-20220127163448716](\images\image-20220127163448716.png)

![image-20220127163653899](\images\image-20220127163653899.png)



![image-20220127165642322](\images\image-20220127165642322.png)



![image-20220127165624545](\images\image-20220127165624545.png)

### Horizontal Pod Autoscaling

创建 HPA 控制器

```
[root@k8s-master01 manifests]# kubectl run php-apache --image=gcr.io/google_containers/hpa-example --requests=cpu=200m --expose --port=80 --image-pull-policy=Never

```

```

[root@k8s-master01 manifests]# kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=10

```

![image-20220127191715356](\images\image-20220127191715356.png)

开启一个pod进行压测

```
[root@k8s-master01 manifests]# kubectl run -i --tty load-generator --image=busybox /bin/sh


```

自动扩容pod

![image-20220127191955268](\images\image-20220127191955268.png)





### 资源限制 - Pod

Kubernetes 对资源的限制实际上是通过 cgroup 来控制的，cgroup 是容器的一组用来控制内核如何运行进程的
相关属性集合。针对内存、CPU 和各种设备都有对应的 cgroup

默认情况下，Pod 运行没有 CPU 和内存的限额。 这意味着系统中的任何 Pod 将能够像执行该 Pod 所在的节点一
样，消耗足够多的 CPU 和内存 。一般会针对某些应用的 pod 资源进行资源限制，这个资源限制是通过
resources 的 requests 和 limits 来实现

```yml
  spec:
    containers:
    - image: xxxx
      imagePullPolicy: Always
      name: auth
      ports:
      - containerPort: 8080
        protocol: TCP
      resources:
        limits:
          cpu: "4"
          memory: 2Gi
        requests:
          cpu: 250m
          memory: 250Mi
```

requests 要分分配的资源，limits 为最高请求的资源值。可以简单理解为初始值和最大值

### 资源限制 - 名称空间

计算资源配额

```yml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-resources
  namespace: spark-cluster
spec:
  hard:
    pods: "20"
    requests.cpu: "20"
    requests.memory: 100Gi
    limits.cpu: "40"
    limits.memory: 200Gi
```



![image-20220127193201113](\images\image-20220127193201113.png)

配置对象数量配额限制

```yml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: object-counts
  namespace: spark-cluster
spec:
  hard:
    configmaps: "10"
    persistentvolumeclaims: "4"
    replicationcontrollers: "20"
    secrets: "10"
    services: "10"
    services.loadbalancers: "2"
```

配置 CPU 和 内存 LimitRange

```yml
apiVersion: v1
kind: LimitRange
metadata:
  name: mem-limit-range
spec:
  limits:
  - default:
      memory: 50Gi
      cpu: 5
    defaultRequest:
      memory: 1Gi
      cpu: 1
    type: Containe
```

default 即 limit 的值
defaultRequest 即 request 的

### 访问 prometheus

以看到 prometheus 已经成功连接上了 k8s 的 apiserver

![image-20220127193553791](\images\image-20220127193553791.png)

查看 service-discovery

![image-20220127193659549](\images\image-20220127193659549.png)

Prometheus 自己的指标

![image-20220127193801929](\images\image-20220127193801929.png)

prometheus 的 WEB 界面上提供了基本的查询 K8S 集群中每个 POD 的 CPU 使用情况，查询条件如下：

```
sum by (pod_name)( rate(container_cpu_usage_seconds_total{image!="", pod_name!=""}[1m]
```

![image-20220127194041289](\images\image-20220127194041289.png)

上述的查询有出现数据，说明 node-exporter 往 prometheus 中写入数据正常，接下来我们就可以部署
grafana 组件，实现更友好的 we展示数据了

### 访问 grafanaa

查看 grafana 服务暴露的端口号

```
[root@k8s-master01 ~]# kubectl get service -n monitoring | grep grafana
```

如上可以看到 grafana 的端口号是 30100，浏览器访问 http://MasterIP:30100 用户名密码默认 admin/admi

修改密码并登陆

添加数据源 grafana 默认已经添加了 Prometheus 数据源，grafana 支持多种时序数据源，每种数据源都有各自
的查询编辑器

![image-20220127194652474](\images\image-20220127194652474.png)

![image-20220127195356789](\images\image-20220127195356789.png)

![image-20220127195423699](\images\image-20220127195423699.png)

## 部署EFK平台

```
helm repo add stable http://mirror.azure.cn/kubernetes/charts/
```

### 部署 Elasticsearch

```
[root@k8s-master01 elasticsearch]# kubectl create namespace efk
namespace/efk created
[root@k8s-master01 elasticsearch]# helm fetch stable/elasticsearch
[root@k8s-master01 elasticsearch]# helm install --name els1 --namespace=efk -f values.yaml stable/elasticsearch
# 机器性能限制把values的改 MINIMUM_MASTER_NODES: "1"  client下的replicas: 1 master下的replicas: 1   persistence: enabled: false
[root@k8s-master01 ~]# kubectl run cirror-$RANDOM --rm -it --image=cirros -- /bin/sh
# 测试es连通性
/ # curl 10.108.203.253:9200/_cat/nodes



```

![image-20220128174658726](\images\image-20220128174658726.png)

![image-20220128202932577](\images\image-20220128202932577.png)

![image-20220128214934643](\images\image-20220128214934643.png)

### 部署 Fluentd

```
[root@k8s-master01 ~]# helm fetch stable/fluentd-elasticsearch
[root@k8s-master01 fluentd-elasticsearch]# vim values.yaml
elasticsearch:
  host: '10.108.203.253' # 更改es地址
[root@k8s-master01 fluentd-elasticsearch]# helm install --name flu1 --namespace=efk -f values.yaml .


```

![image-20220128220455163](\images\image-20220128220455163.png)

### 部署 kibana

```
# 注意kibana的版本要与es版本匹配
https://www.elastic.co/cn/support/matrix#matrix_compatibility

[root@k8s-master01 kibana]# helm fetch stable/kibana  --version=xxx
[root@k8s-master01 kibana]# helm install --name kib1 --namespace=efk -f values.yaml .

```

# 十、 修改证书时间

### go环境部署

```
[root@k8s-master01 elasticsearch]# wget https://dl.google.com/go/go1.12.7.linux-amd64.tar.gz
[[root@k8s-master01 elasticsearch]# tar zxvf go1.12.7.linux-amd64.tar.gz -C /usr/local
[root@k8s-master01 go]# vim /etc/profile
	export PATH=$PATH:/usr/local/go/bin
source /etc/profile
```

### 下载源码

```
cd /data && git clone https://github.com/kubernetes/kubernetes.git
[root@k8s-master01 kubernetes]# git checkout -b remotes/origin/release-1.15.1 v1.15.1

```

### 修改 Kubeadm 源码包更新证书策略

```
# 查看修改前证书日期
[root@k8s-master01 go]# openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout

```

![image-20220129100219395](\images\image-20220129100219395.png)

```
vim staging/src/k8s.io/client-go/util/cert/cert.go # kubeadm 1.14 版本之前
vim cmd/kubeadm/app/util/pkiutil/pki_helpers.go # 
	kubconst duration365d = time.Hour * 24 * 365 * 10
	NotAfter: time.Now().Add(ration365d).UTC()
[root@k8s-master01 kubernetes]# make WHAT=cmd/kubeadm GOFLAGS=-v
[root@k8s-master01 kubernetes]# cp _output/bin/kubeadm /root/kubeadm-new

```

### 更新 kubeadm

```
[root@k8s-master01 kubernetes]# cp /usr/bin/kubeadm /usr/bin/kubeadm.old
[root@k8s-master01 kubernetes]# cp /root/kubeadm-new /usr/bin/kubeadm
[root@k8s-master01 kubernetes]# chmod a+x /usr/bin/kubeadm

```

### 更新各节点证书至 Master 节点

```
[root@k8s-master01 pki]# cp -r /etc/kubernetes/pki /etc/kubernetes/pki.old
[root@k8s-master01 pki]# cd /etc/kubernetes/pki
[root@k8s-master01 pki]# kubeadm alpha certs renew all --config=/root/install-k8s/core/kubeadm-config.yaml
[root@k8s-master01 pki]# openssl x509 -in apiserver.crt -text -noout

```

![image-20220129102445577](\images\image-20220129102445577.png)

### HA集群其余 mater 节点证书更新

```shell
#!/bin/bash
masterNode="192.168.66.20 192.168.66.21"
#for host in ${masterNode}; do
  # scp /etc/kubernetes/pki/{ca.crt,ca.key,sa.key,sa.pub,front-proxy-ca.crt,front-proxy-ca.key} "${USER}"@$host:/etc/kubernetes/pki/
  # scp /etc/kubernetes/pki/etcd/{ca.crt,ca.key} "root"@$host:/etc/kubernetes/pki/etcd
  # scp /etc/kubernetes/admin.conf "root"@$host:/etc/kubernetes/
#done
for host in ${CONTROL_PLANE_IPS}; do
    scp /etc/kubernetes/pki/{ca.crt,ca.key,sa.key,sa.pub,front-proxy-ca.crt,front-proxy-ca.key}"${USER}"@$host:/root/pki/
    scp /etc/kubernetes/pki/etcd/{ca.crt,ca.key} "root"@$host:/root/etcd
    scp /etc/kubernetes/admin.conf "root"@$host:/root/kubernetes/
done
```

# 十一、部署高可用K8S

![image-20220129180616420](\images\image-20220129180616420.png)

![image-20220129180731803](\images\image-20220129180731803.png)

Kubernetes 作为容器集群系统，通过健康检查+重启策略实现了 Pod 故障自我修复能力，通过调度算法实现将 Pod 分布式部署，监控其预期副本数，并根据 Node 失效状态自动在正常 Node 启动 Pod，实现了应用层的高可用性

针对 Kubernetes 集群，高可用性还应包含以下两个层面的考虑：Etcd 数据库的高可用性和 Kubernetes Master 组件的高可用性。 而 Etcd 我们已经采用 3 个节点组建集群实现高可用，本节将对 Master 节点高可用进行说明和实施

Master 节点扮演着总控中心的角色，通过不断与工作节点上的 Kubelet 和 kube-proxy 进行通信来维护整个集群的健康工作状态。如果 Master 节点故障，将无法使用 kubectl 工具或者 API 任何集群管理

Master 节点主要有三个服务 kube-apiserver、kube-controller-mansger 和 kube-scheduler，其中 kube-controller-mansger 和 kube-scheduler 组件自身通过选择机制已经实现了高可用，所以 Master 高可用主要针对 kube-apiserver 组件，而该组件是以 HTTPAPI 提供服务，因此对他高可用与 Web 服务器类似，增加负载均衡器对其负载均衡即可，并且可水平扩容。

多 Master 架构图：

![image-20220129181142278](\images\image-20220129181142278.png)

## 1、系统初始化

步骤同第二章第一节，添加一个关闭NUMA的配置



## 2、安装keeplive在master节点上

### 安装相关包

```
[root@k8s-master01 pki]# yum install -y conntrack-tools libsecomp libtool-ltb1
[root@k8s-master01 pki]# yum install -y keepalived

```

### 配置Master节点

添加master1的配置

```bash
cat > /etc/keepalived/keepalived.conf <<EOF 
! Configuration File for keepalived

global_defs {
   router_id k8s
}

vrrp_script check_haproxy {
    script "killall -0 haproxy"
    interval 3
    weight -2
    fall 10
    rise 2
}

vrrp_instance VI_1 {
    state MASTER 
    interface ens33 
    virtual_router_id 51
    priority 250
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass ceb1b3ec013d66163d6ab
    }
    virtual_ipaddress {
        192.168.31.200
    }
    track_script {
        check_haproxy
    }

}
EOF
```

添加master2的配置

```bash
cat > /etc/keepalived/keepalived.conf <<EOF 
! Configuration File for keepalived

global_defs {
   router_id k8s
}

vrrp_script check_haproxy {
    script "killall -0 haproxy"
    interval 3
    weight -2
    fall 10
    rise 2
}

vrrp_instance VI_1 {
    state BACKUP 
    interface ens33 
    virtual_router_id 51
    priority 200
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass ceb1b3ec013d66163d6ab
    }
    virtual_ipaddress {
        192.168.31.200
    }
    track_script {
        check_haproxy
    }

}
EOF
```

###  启动和检查

master节点上执行

```
# 启动keepalived
systemctl start keepalived.service
# 设置开机启动
systemctl enable keepalived.service
# 查看启动状态
systemctl status keepalived.service
```

启动后查看master的网卡信息

```
[root@k8s-master02 conf]# ip a s ens33
```

![image-20220130150134651](\images\image-20220130150134651.png)

###  部署haproxy

Haproxy主要做负载的作用，将我们的请求分担到不同的node节点上

在两个master节点安装 haproxy

```
# 安装haproxy
yum install -y haproxy
# 启动 haproxy
systemctl start haproxy
# 开启自启
systemctl enable haproxy
```

###  配置haproxy

两台master节点的配置均相同，配置中声明了后端代理的两个master节点服务器，指定了haproxy运行的端口为16443等，因此16443端口为集群的入口

```
cat > /etc/haproxy/haproxy.cfg << EOF
#---------------------------------------------------------------------
# Global settings
#---------------------------------------------------------------------
global
    # to have these messages end up in /var/log/haproxy.log you will
    # need to:
    # 1) configure syslog to accept network log events.  This is done
    #    by adding the '-r' option to the SYSLOGD_OPTIONS in
    #    /etc/sysconfig/syslog
    # 2) configure local2 events to go to the /var/log/haproxy.log
    #   file. A line like the following can be added to
    #   /etc/sysconfig/syslog
    #
    #    local2.*                       /var/log/haproxy.log
    #
    log         127.0.0.1 local2
    
    chroot      /var/lib/haproxy
    pidfile     /var/run/haproxy.pid
    maxconn     4000
    user        haproxy
    group       haproxy
    daemon 
       
    # turn on stats unix socket
    stats socket /var/lib/haproxy/stats
#---------------------------------------------------------------------
# common defaults that all the 'listen' and 'backend' sections will
# use if not designated in their block
#---------------------------------------------------------------------  
defaults
    mode                    http
    log                     global
    option                  httplog
    option                  dontlognull
    option http-server-close
    option forwardfor       except 127.0.0.0/8
    option                  redispatch
    retries                 3
    timeout http-request    10s
    timeout queue           1m
    timeout connect         10s
    timeout client          1m
    timeout server          1m
    timeout http-keep-alive 10s
    timeout check           10s
    maxconn                 3000
#---------------------------------------------------------------------
# kubernetes apiserver frontend which proxys to the backends
#--------------------------------------------------------------------- 
frontend kubernetes-apiserver
    mode                 tcp
    bind                 *:16443
    option               tcplog
    default_backend      kubernetes-apiserver    
#---------------------------------------------------------------------
# round robin balancing between the various backends
#---------------------------------------------------------------------
backend kubernetes-apiserver
    mode        tcp
    balance     roundrobin
    server      master01.k8s.io   192.168.31.10:6443 check
    server      master02.k8s.io   192.168.31.11:6443 check
#---------------------------------------------------------------------
# collection haproxy statistics message
#---------------------------------------------------------------------
listen stats
    bind                 *:1080
    stats auth           admin:awesomePassword
    stats refresh        5s
    stats realm          HAProxy\ Statistics
    stats uri            /admin?stats
EOF
```

###  启动后，我们查看对应的端口是否包含 16443

```
netstat -tunlp | grep haproxy
```

![image-20220130150412595](\images\image-20220130150412595.png)

### 安装Docker、Kubeadm、kubectl

所有节点安装Docker/kubeadm/kubelet ，Kubernetes默认CRI（容器运行时）为Docker，因此先安装Docker

首先配置一下Docker的阿里yum源

```
cat >/etc/yum.repos.d/docker.repo<<EOF
[docker-ce-edge]
name=Docker CE Edge - \$basearch
baseurl=https://mirrors.aliyun.com/docker-ce/linux/centos/7/\$basearch/edge
enabled=1
gpgcheck=1
gpgkey=https://mirrors.aliyun.com/docker-ce/linux/centos/gpg
EOF
```

然后yum方式安装docker

```
# yum安装
yum -y install docker-ce

# 查看docker版本
docker --version  

# 启动docker
systemctl enable docker
systemctl start docker
```

配置docker的镜像源

```
cat >> /etc/docker/daemon.json << EOF
{
  "registry-mirrors": ["https://b9pmyelo.mirror.aliyuncs.com"]
}
EOF
```

然后重启docker

```
systemctl restart dockers
```

###  添加kubernetes软件源

然后我们还需要配置一下yum的k8s软件源

```bash
cat > /etc/yum.repos.d/kubernetes.repo << EOF
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF
```

### 安装kubeadm，kubelet和kubectl

由于版本更新频繁，这里指定版本号部署：

```
# 安装kubelet、kubeadm、kubectl，同时指定版本
yum install -y kubelet-1.18.0 kubeadm-1.18.0 kubectl-1.18.0
# 设置开机启动
systemctl enable kubelet
```

##  3、部署Kubernetes Master【master节点】

###  创建kubeadm配置文件

在具有vip的master上进行初始化操作，这里为master1

```
 创建文件夹
mkdir /usr/local/kubernetes/manifests -p
# 到manifests目录
cd /usr/local/kubernetes/manifests/
# 新建yaml文件
vi kubeadm-config.yaml
```

yaml内容如下所示：

```
apiServer:
  # apiServerCertSANs：填写所有kube-apiserver节点的hostname、IP、VIP
  certSANs:
    - master1
    - master2
    - master.k8s.io
    - 192.168.31.200
    - 192.168.31.10
    - 192.168.31.11
    - 127.0.0.1
  extraArgs:
    authorization-mode: Node,RBAC
  timeoutForControlPlane: 4m0s
apiVersion: kubeadm.k8s.io/v1beta1
certificatesDir: /etc/kubernetes/pki
clusterName: kubernetes
# ha vip的地址
controlPlaneEndpoint: "192.168.31.200:16443"
controllerManager: {}
dns: 
  type: CoreDNS
etcd:
  local:    
    dataDir: /var/lib/etcd
imageRepository: registry.aliyuncs.com/google_containers
kind: ClusterConfiguration
kubernetesVersion: v1.16.3
networking: 
  dnsDomain: cluster.local  
  podSubnet: 10.244.0.0/16
  serviceSubnet: 10.1.0.0/16
scheduler: {}
```

然后我们在 master1 节点执行

```
kubeadm init --config kubeadm-config.yaml
```

执行完成后，就会在拉取我们的进行了【需要等待...】



按照提示配置环境变量，使用kubectl工具

```
# 执行下方命令
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
# 查看节点
kubectl get nodes
# 查看pod
kubectl get pods -n kube-system
```

**按照提示保存以下内容，一会要使用：**

```
 kubeadm join 192.168.31.200:16443 --token abcdef.0123456789abcdef \
    --discovery-token-ca-cert-hash sha256:3f011195e503f7ec12a1943ebce2e93a14f6f45aac7881b0a4903f8bcae15620 \
    --control-plane --certificate-key f3e01a1bca95a622be34befa7a324fe1a3aad82aa13979c8cfbbbc74edff2196

```

--control-plane ： 只有在添加master节点的时候才有

查看集群状态

```
# 查看集群状态
kubectl get cs
# 查看pod
kubectl get pods -n kube-system
```

###  安装集群网络

从官方地址获取到flannel的yaml，在master1上执行

```
# 创建文件夹
mkdir flannel
cd flannel
# 下载yaml文件
wget -c https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

安装flannel网络

```
kubectl apply -f kube-flannel.yml 
```

检查

```
kubectl get pods -n kube-system
```

###  master2节点加入集群

从master1复制密钥及相关文件到master2

```
# ssh root@192.168.31.11 mkdir -p /etc/kubernetes/pki/etcd

# scp /etc/kubernetes/admin.conf root@192.168.31.11:/etc/kubernetes

# scp /etc/kubernetes/pki/{ca.*,sa.*,front-proxy-ca.*} root@192.168.31.11:/etc/kubernetes/pki
   
# scp /etc/kubernetes/pki/etcd/ca.* root@192.168.31.11:/etc/kubernetes/pki/etcd
```

执行在master1上init后输出的join命令,需要带上参数`--control-plane`表示把master控制节点加入集群

```
 kubeadm join 192.168.31.200:16443 --token abcdef.0123456789abcdef \
    --discovery-token-ca-cert-hash sha256:3f011195e503f7ec12a1943ebce2e93a14f6f45aac7881b0a4903f8bcae15620 \
    --control-plane --certificate-key f3e01a1bca95a622be34befa7a324fe1a3aad82aa13979c8cfbbbc74edff2196
```

检查状态

```
kubectl get cs
# 查看pod
kubectl get pods -n kube-system
```

![image-20220130152245045](\images\image-20220130152245045.png)

![image-20220130152302312](\images\image-20220130152302312.png)

###  ![image-20220130163002559](\images\image-20220130163002559.png)

### Etcd 集群状态查看

```
[root@k8s-master02 .kube]# kubectl -n kube-system exec etcd-k8s-master01 -- etcdctl --endpoints=https://192.168.31.10:2379 --ca-file=/etc/kubernetes/pki/etcd/ca.crt --cert-file=/etc/kubernetes/pki/etcd/server.crt --key-file=/etc/kubernetes/pki/etcd/server.key cluster-health

```

![image-20220130163535306](\images\image-20220130163535306.png)

```
[root@k8s-master02 .kube]# kubectl get endpoints kube-controller-manager --namespace=kube-system -o yaml

```

![image-20220130163632206](\images\image-20220130163632206.png)

```
[root@k8s-master02 .kube]# kubectl get endpoints kube-scheduler --namespace=kube-system -o yaml

```

### 加入Kubernetes Node

在node1上执行

向集群添加新节点，执行在kubeadm init输出的kubeadm join命令：

```
kubeadm join 192.168.31.200:16443 --token abcdef.0123456789abcdef \
    --discovery-token-ca-cert-hash sha256:3f011195e503f7ec12a1943ebce2e93a14f6f45aac7881b0a4903f8bcae15620
```

####  [k8s join 集群报错之error execution phase kubelet-start: error uploading crisocket:]

```
[root@k8s-node01 ~]# swapoff -a
[root@k8s-node01 ~]# kubeadm reset
[root@k8s-node01 ~]# rm /etc/cni/net.d/* -f
[root@k8s-node01 ~]#  systemctl daemon-reload
[root@k8s-node01 ~]# systemctl restart kubelet
[root@k8s-node01 ~]#  iptables -F && iptables -t nat -F && iptables -t mangle -F && iptables -X

```

![image-20220130153518800](\images\image-20220130153518800.png)

### 测试kubernetes集群

在Kubernetes集群中创建一个pod，验证是否正常运行：

```
# 创建nginx deployment
kubectl create deployment nginx --image=nginx
# 暴露端口
kubectl expose deployment nginx --port=80 --type=NodePort
# 查看状态
kubectl get pod,svc
```

![image-20220130153626426](\images\image-20220130153626426.png)

### 排查 k8s 集群 master 节点无法正常工作的问题

搭建的是 k8s 高可用集群，用了 3 台 master 节点，2 台 master 节点宕机后，仅剩的 1 台无法正常工作。

运行 kubectl get nodes 命令出现下面的错误

```
The connection to the server k8s-api:6443 was refused - did you specify the right host or port?
```

运行 netstat -lntp 命令发现 kube-apiserver 根本没有运行，同时发现 etcd 与 kube-proxy 也没运行。

通过 docker ps 命令发现 etcd , kube-apiserver, kube-proxy 这 3 个容器都没有运行，etcd 容器在不停地启动->失败->重启->又失败......

etcd 启动失败是由于 etcd 在 3 节点集群模式在启动却无法连接另外 2 台 master 节点的 etcd ，要解决这个问题需要改为单节点集群模式。开始不知道如何将 etcd 改为单节点模式，后来在网上找到 2 个参数 `--initial-cluster-state=new` 与 `--force-new-cluster` ，在 /etc/kubernetes/manifests/etcd.yaml 中给 etcd 命令加上这 2 个参数，并重启服务器后，master 节点就能正常运行了。

```
 containers:
  - command:
    - etcd
    - --advertise-client-urls=https://192.168.31.11:2379
    - --cert-file=/etc/kubernetes/pki/etcd/server.crt
    - --client-cert-auth=true
    - --data-dir=/var/lib/etcd
    - --initial-advertise-peer-urls=https://192.168.31.11:2380
    - --initial-cluster=k8s-master01=https://192.168.31.10:2380,k8s-master02=https://192.168.31.11:2380
    - --initial-cluster-state=existing
    - --key-file=/etc/kubernetes/pki/etcd/server.key
    - --listen-client-urls=https://127.0.0.1:2379,https://192.168.31.11:2379
    - --listen-peer-urls=https://192.168.31.11:2380
    - --name=k8s-master02
    - --peer-cert-file=/etc/kubernetes/pki/etcd/peer.crt
    - --peer-client-cert-auth=true
    - --peer-key-file=/etc/kubernetes/pki/etcd/peer.key
    - --peer-trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
    - --snapshot-count=10000
    - --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
    - --initial-cluster-state=new
    - --force-new-cluster

```

注意 master 正常运行后，需要去掉刚刚添加的这 2 个 etcd 参数。

# 十二、通过K8S部署一个java应用

![image-20220130184445828](\images\image-20220130184445828.png)

### 准备好java项目打包

```
mvn clean package
```

### 编写dockerfile

```
[root@k8s-master01 java-docekr]# vim Dockerfile
FROM openjdk:8-jdk-alpine
VOLUME /tmp
ADD ./target/01-SpringBootHelloWorld-1.5.9.RELEASE.jar 01-SpringBootHelloWorld-1.5.9.RELEASE.jar
ENTRYPOINT ["java","-jar","01-SpringBootHelloWorld-1.5.9.RELEASE.jar", "&"]

```

### 创建dokcer镜像

```
[root@k8s-master01 java-docekr]# docker build -t java-demo-01:latest .
```

![image-20220130190457049](\images\image-20220130190457049.png)

run一下镜像测试

```
[root@k8s-master01 java-docekr]# docker run -d -p 8088:8080 java-demo-01:latest
```

![](\images\image-20220130191326606.png)

上传镜像到habor

```
[root@k8s-master01 java-docekr]# docker tag java-demo-01:latest hub.harry.com/library/java-demo:v1
[root@k8s-master01 java-docekr]# docker push hub.harry.com/library/java-demo:v1

```

### k8s部署暴露服务

```
[root@k8s-master01 java-docekr]# kubectl create deployment javademo1 --image=hub.harry.com/library/java-demo:v1  --dry-run -o yaml > javademo1.ymal
[root@k8s-master01 java-docekr]# kubectl create -f javademo1.ymal

```

```yml

apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: javademo1
  name: javademo1
spec:
  replicas: 1
  selector:
    matchLabels:
      app: javademo1
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: javademo1
    spec:
      containers:
      - image: hub.harry.com/library/java-demo:v1
        name: java-demo
        resources: {}
status: {}

```

```

[root@k8s-master01 java-docekr]# kubectl expose deployment javademo1 --port=8111 --target-port=8080 --type=NodePort

```

![image-20220130193912142](\images\image-20220130193912142.png)