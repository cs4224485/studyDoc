# 一 Docker简介

Docker是基于Go语言实现的云开源项目
Docker的主要目标是"Build, Ship and Run Any App, Anywhere"， 也就是通过对应用组件的封装、分发、部署、运行等生命周期的管理，使用户的APP(可以是一个WEB应用或数据库应用等等)及其运行环境能够做到"一次封装，到处运行"

Linux容器技术的出现解决了这样一个问题， 而Docker就是在它的基础上发展过来的。将应用运行在Docker容器上面，而Docker容器在任何操作系统上都是一致的，这家ius实现了跨平台、跨服务器。
只需要一次配置好环境，换到别的机子上就可以一键部署好 

Docker和传统虚拟化方式的不同之处：
 * 传统虚拟机技术是虚拟出一套硬件后，在其上运行一个完整操作系统，在该系统上在运行所需应用的进程
 * 而容器内的应用进程直接运行于宿主的内核，容器内没有自己的内核，而且也没有进行硬件虚拟。 因此容器要比传统虚拟机更为轻便
 * 每个容器之间互相隔离，每个容器都有自己的文件系统，容器之间进程不会相互影响，能区分计算资源。

容器的组成

### 镜像

​	Docker 镜像（Image）就是一个只读的模板。镜像可以用来创建 Docker 容器，一个镜像可以创建很多容器。

### 容器

​	Docker 利用容器（Container）独立运行的一个或一组应用。容器是用镜像创建的运行实例。
​	它可以被启动、开始、停止、删除。每个容器都是相互隔离的、保证安全的平台。
​	可以把容器看做是一个简易版的 Linux 环境（包括root用户权限、进程空间、用户空间和网络空间等）和运行在其中的应用程序。
​	容器的定义和镜像几乎一模一样，也是一堆层的统一视角，唯一区别在于容器的最上面那一层是可读可写的。

### 仓库

​	仓库（Repository）是集中存放镜像文件的场所。
​	仓库(Repository)和仓库注册服务器（Registry）是有区别的。仓库注册服务器上往往存放着多个仓库，每个仓库中又包含了多个镜像，每个镜像有不同的标签（tag）。
​	仓库分为公开仓库（Public）和私有仓库（Private）两种形式。
​	最大的公开仓库是 Docker Hub(https://hub.docker.com/)，
​	存放了数量庞大的镜像供用户下载。国内的公开仓库包括阿里云 、网易云 等

### 容器与虚拟机的对比

由于前面虚拟机存在某些缺点，Linux发展出了另一种虚拟化技术：
Linux容器(Linux Containers，缩写为 LXC)
Linux容器是与系统其他部分隔离开的一系列进程，从另一个镜像运行，并由该镜像提供支持进程所需的全部文件。容器提供的镜像包含了应用的所有依赖项，因而在从开发到测试再到生产的整个过程中，它都具有可移植性和一致性。

Linux 容器不是模拟一个完整的操作系统而是对进程进行隔离。有了容器，就可以将软件运行所需的所有资源打包到一个隔离的容器中。容器与虚拟机不同，不需要捆绑一整套操作系统，只需要软件工作所需的库资源和设置。系统因此而变得高效轻量并保证部署在任何环境中的软件都能始终如一地运行。

![image-20220207094328794](\images\image-20220207094328794.png)

![image-20220207094510853](\images\image-20220207094510853.png)

# 二 Docker的安装

![image-20220207094610541](\images\image-20220207094610541.png)

### 前提条件

目前，CentOS 仅发行版本中的内核支持 Docker。Docker 运行在CentOS 7 (64-bit)上，要求系统为64位、Linux系统内核版本为 3.8以上，这里选用Centos7.xss

uname命令用于打印当前系统相关信息（内核版本号、硬件架构、主机名称和操作系统类型等）。

![image-20220207095312438](\images\image-20220207095312438.png)

### Docker的基本组成

#### 镜像(image)

Docker 镜像（Image）就是一个只读的模板。镜像可以用来创建 Docker 容器，一个镜像可以创建很多容器。
它也相当于是一个root文件系统。比如官方镜像 centos:7 就包含了完整的一套 centos:7 最小系统的 root 文件系统。
相当于容器的“源代码”，docker镜像文件类似于Java的类模板，而docker容器实例类似于java中new出来的实例对象。

#### 容器(container)

1 从面向对象角度
	Docker 利用容器（Container）独立运行的一个或一组应用，应用程序或服务运行在容器里面，容器就类似于一个虚拟化的运行环境，容器是用镜像创建的运行实例。就像是Java中的类和实例对象一样，镜像是静态的定义，容器是镜像运行时的实体。容器为镜像提供了一个标准的和隔离的运行环境，它可以被启动、开始、停止、删除。每个容器都是相互隔离的、保证安全的平台

2 从镜像容器角度
	可以把容器看做是一个简易版的 Linux 环境（包括root用户权限、进程空间、用户空间和网络空间等）和运行在其中的应用程序

#### 仓库(repository)

仓库（Repository）是集中存放镜像文件的场所。

类似于
Maven仓库，存放各种jar包的地方；
github仓库，存放各种git项目的地方；
Docker公司提供的官方registry被称为Docker Hub，存放各种镜像模板的地方。

仓库分为公开仓库（Public）和私有仓库（Private）两种形式。
最大的公开仓库是 Docker Hub(https://hub.docker.com/)，
存放了数量庞大的镜像供用户下载。国内的公开仓库包括阿里云 、网易云等

### Docker平台架构图解(架构版)

Docker 是一个 C/S 模式的架构，后端是一个松耦合架构，众多模块各司其职。 

![image-20220207100413487](\images\image-20220207100413487.png)

![image-20220207100429319](\images\image-20220207100429319.png)

### CentOS7安装Docke

官网：https://docs.docker.com/engine/install/centos/

确定你是CentOS7及以上版本

#### 卸载旧版本

![image-20220207100742287](\images\image-20220207100742287.png)

#### yum安装gcc相关y

```
yum -y install gcc
yum -y install gcc-c++
```

#### 安装需要的软件包

![image-20220207101011386](\images\image-20220207101011386.png)

执行命令

```
yum install -y yum-utils
```

#### 设置stable镜像仓库

```
[root@docker-01 ~]# yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

```

#### 更新yum软件包索引

```
yum makecache fast
```

#### 安装DOCKER CE

```
yum -y install docker-ce docker-ce-cli containerd.io
```

官网要求

![image-20220207101341891](\images\image-20220207101341891.png)

执行结果

![image-20220207101424593](\images\image-20220207101424593.png)

#### 启动docker

```
[root@docker-01 ~]# systemctl start docker
```

#### 测试

```
[root@docker-01 ~]# docker version
```

![image-20220207101624907](\images\image-20220207101624907.png)

docker run hello-world

```
docker run hello-world
```

![image-20220207101806586](\images\image-20220207101806586.png)

#### 卸载

```
systemctl stop docker
yum remove docker-ce docker-ce-cli containerd.io
rm -rf /var/lib/docker
rm -rf /var/lib/containerd
```

### 阿里云镜像加速

https://promotion.aliyun.com/ntms/act/kubernetes.html

注册一个属于自己的阿里云账户(可复用淘宝账号)

获得加速器地址连接

点击控制台,选择容器镜像服务,获取加速器地址

![image-20220207102411184](\images\image-20220207102411184.png)

```
mkdir -p /etc/docker
tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://aa25jngu.mirror.aliyuncs.com"]
}
EOF
```

```
#网易云
{"registry-mirrors": ["http://hub-mirror.c.163.com"] }

#阿里云
{
"registry-mirrors": ["https://｛自已的编码｝.mirror.aliyuncs.com"]
}
```

#### 重启服务器

```
[root@docker-01 ~]# systemctl daemon-reload
[root@docker-01 ~]# systemctl restart docker
```

### docker run都干了什么

![image-20220207102830733](\images\image-20220207102830733.png)

### 为什么Docker会比VM虚拟机快

(1)docker有着比虚拟机更少的抽象层
   由于docker不需要Hypervisor(虚拟机)实现硬件资源虚拟化,运行在docker容器上的程序直接使用的都是实际物理机的硬件资源。因此在CPU、内存利用率上docker将会在效率上有明显优势。

(2)docker利用的是宿主机的内核,而不需要加载操作系统OS内核
   当新建一个容器时,docker不需要和虚拟机一样重新加载一个操作系统内核。进而避免引寻、加载操作系统内核返回等比较费时费资源的过程,当新建一个虚拟机时,虚拟机软件需要加载OS,返回新建过程是分钟级别的。而docker由于直接利用宿主机的操作系统,则省略了返回过程,因此新建一个docker容器只需要几秒钟。

![image-20220207103028196](\images\image-20220207103028196.png)

# 三 Docker常用的命令

### 帮助启动命令

```
启动docker： systemctl start docker
停止docker： systemctl stop docker
重启docker： systemctl restart docker
查看docker状态： systemctl status docker
开机启动： systemctl enable docker
查看docker概要信息： docker info
查看docker总体帮助文档： docker --help
查看docker命令帮助文档： docker 具体命令 --help
```

### 镜像命令

```
docker images
-a :列出本地所有的镜像（含历史映像层）
-q :只显示镜像ID
```

各个选项说明:
REPOSITORY：表示镜像的仓库源
TAG：镜像的标签版本号
IMAGE ID：镜像ID
CREATED：镜像创建时间
SIZE：镜像大小
 同一仓库源可以有多个 TAG版本，代表这个仓库源的不同个版本，我们使用 REPOSITORY:TAG 来定义不同的镜像。
如果你不指定一个镜像的版本标签，例如你只使用 ubuntu，docker 将默认使用 ubuntu:latest 镜像

![image-20220207103650470](\images\image-20220207103650470.png)

```
docker search 某个XXX镜像名字
https://hub.docker.com
docker search [OPTIONS] 镜像名
--limit : 只列出N个镜像，默认25个
docker search --limit 5 redis
```

![image-20220207103754677](\images\image-20220207103754677.png)

![image-20220207103840171](\images\image-20220207103840171.png)

docker pull 某个XXX镜像名字

```
docker pull 镜像名字[:TAG]
docker pull 镜像名字
	没有TAG就是最新版 等价于 docker pull 镜像名字:latest
docker pull ubuntu
```

![image-20220207104704785](\images\image-20220207104704785.png)

```
docker system df 查看镜像/容器/数据卷所占的空间
```

![image-20220207104801333](\images\image-20220207104801333.png)

```
docker rmi 某个XXX镜像名字ID
```

删除单个

```
docker rmi  -f 镜像ID
```

删除多个

```
docker rmi -f 镜像名1:TAG 镜像名2:TAG
```

删除全部

```
docker rmi -f $(docker images -qa)
```

面试题：谈谈docker虚悬镜像是什么

仓库名、标签都是<none>的镜像，俗称虚悬镜像dangling 

![image-20220207105029634](\images\image-20220207105029634.png)

### 容器命令

有镜像才能创建容器，这是根本前提(下载一个CentOS或者ubuntu镜像演示)

![image-20220207105140077](\images\image-20220207105140077.png)

```
docker pull centos
docker pull ubuntu
```

新建+启动容器

```
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

OPTIONS说明（常用）：有些是一个减号，有些是两个减号
--name="容器新名字"       为容器指定一个名称；
-d: 后台运行容器并返回容器ID，也即启动守护式容器(后台运行)；
 
-i：以交互模式运行容器，通常与 -t 同时使用；
-t：为容器重新分配一个伪输入终端，通常与 -i 同时使用；
也即启动交互式容器(前台有伪终端，等待交互)；
 
-P: 随机端口映射，大写P
-p: 指定端口映射，小写p

```

![image-20220207105259074](\images\image-20220207105259074.png)

#使用镜像centos:latest以交互模式启动一个容器,在容器内执行/bin/bash命令。
docker run -it centos /bin/bash 

```
参数说明：
-i: 交互式操作。
-t: 终端。
centos : centos 镜像。
/bin/bash：放在镜像名后的是命令，这里我们希望有个交互式 Shell，因此用的是 /bin/bash。
要退出终端，直接输入 exit:
```

```
[root@docker-01 ~]# docker run -it ubuntu /bin/bash
```

![image-20220207105507512](\images\image-20220207105507512.png)

列出当前所有正在运行的容器

```
docker ps [OPTIONS]
-a :列出当前所有正在运行的容器+历史上运行过的
-l :显示最近创建的容器。
-n：显示最近n个创建的容器。
-q :静默模式，只显示容器编号。
```

退出容器

两种退出方式

```
run进去容器，exit退出，容器停止
run进去容器，ctrl+p+q退出，容器不停止
```

启动已停止运行的容器

```
docker start 容器ID或者容器名
```

重启容器

```
docker restart 容器ID或者容器名
```

停止容器

```
docker stop 容器ID或者容器名
```

强制停止容器

```
docker kill 容器ID或容器名
```

删除已停止的容器

```
docker rm 容器ID
docker rm -f $(docker ps -a -q)
docker ps -a -q | xargs docker rm
```

### 实列

有镜像才能创建容器，这是根本前提(下载一个Redis6.0.8镜像演示)

启动守护式容器(后台服务器)，在大部分的场景下，我们希望 docker 的服务是在后台运行的，
我们可以过 -d 指定容器的后台运行模式。

```
docker run -d 容器名

#使用镜像centos:latest以后台模式启动一个容器
docker run -d centos
 
问题：然后docker ps -a 进行查看, 会发现容器已经退出
很重要的要说明的一点: Docker容器后台运行,就必须有一个前台进程.
容器运行的命令如果不是那些一直挂起的命令（比如运行top，tail），就是会自动退出的。
 
这个是docker的机制问题,比如你的web容器,我们以nginx为例，正常情况下,
我们配置启动服务只需要启动响应的service即可。例如service nginx start
但是,这样做,nginx为后台进程模式运行,就导致docker前台没有运行的应用,
这样的容器后台启动后,会立即自杀因为他觉得他没事可做了.
所以，最佳的解决方案是,将你要运行的程序以前台进程的形式运行
```

redis 前后台启动演示case

前台交互式启动

```
docker run -it redis:6.0.8
```

后台守护式启动

```
docker run -d redis:6.0.8
```

查看容器日志

```
docker logs 容器ID
[root@docker-01 ~]# docker logs ac56de4ff7c5

```

![image-20220207111536379](\images\image-20220207111536379.png)

查看容器内运行的进程

```
docker top 容器ID
[root@docker-01 ~]# docker top ac56de4ff7c5
```

![image-20220207111818906](\images\image-20220207111818906.png)

查看容器内部细节

```
docker inspect 容器ID
[root@docker-01 ~]# docker inspect ac56de4ff7c5
```

进入正在运行的容器并以命令行交互

```
docker exec -it 容器ID bashShell
[root@docker-01 ~]# docker exec -it 1c9cf2eae29f /bin/bash
```

![image-20220207113218438](\images\image-20220207113218438.png)

重新进入docker attach 容器ID

```
[root@docker-01 ~]# docker attach 1c9cf2eae29f
```

上述两个区别

attach 直接进入容器启动命令的终端，不会启动新的进程
用exit退出，会导致容器的停止。

![image-20220207113807770](\images\image-20220207113807770.png)

exec 是在容器中打开新的终端，并且可以启动新的进程
用exit退出，不会导致容器的停止。

![image-20220207113834581](\images\image-20220207113834581.png)

推荐使用 docker exec 命令，因为退出容器终端，不会导致容器的停止。

用之前的redis容器实例进入试试

```
[root@docker-01 ~]# docker exec -it ac56de4ff7c5 redis-cli
一般用-d后台启动的程序，再用exec进入对应容器实例
```

### 从容器内拷贝文件到主机上

docker cp  容器ID:容器内路径 目的主机路径

公式：docker cp  容器ID:容器内路径 目的主机路径

```
[root@docker-01 ~]# docker run -it ubuntu
root@29e1ad015d71:/# mkdir test
root@29e1ad015d71:/# cd test/
root@29e1ad015d71:/test# echo docker-content > test.txt
root@29e1ad015d71:/test# cat test.txt
docker-content

[root@docker-01 ~]# docker cp 53849a56af4d:/test/test.txt /root/test.txt
```

### 导入和导出容器

export 导出容器的内容留作为一个tar归档文件[对应import命令]

import 从tar包中的内容创建一个新的文件系统再导入为镜像[对应export

docker export 容器ID > 文件名.tar

![image-20220209095718119](\images\image-20220209095718119.png)

![image-20220209095744689](\images\image-20220209095744689.png)

```
[root@docker-01 ~]# docker export 53849a56af4d > abcd.tar.gz
```

![image-20220209095859447](\images\image-20220209095859447.png)

cat 文件名.tar | docker import - 镜像用户/镜像名:镜像版本号

```
[root@docker-01 ~]# docker rmi -f ubuntu
Untagged: ubuntu:latest
Untagged: ubuntu@sha256:669e010b58baf5beb2836b253c1fd5768333f0d1dbcb834f7c07a4dc93f474be
[root@docker-01 ~]# cat abcd.tar.gz | docker import - harry/ubuntu:2.1
sha256:39df89bd317635ed4a7ad245c769f824aad17a641cbcea7bb0292591c967291e
```

![image-20220209100132865](\images\image-20220209100132865.png)

### 常用命令

![image-20220209101121386](\images\image-20220209101121386.png)

> attach    Attach to a running container                 # 当前 shell 下 attach 连接指定运行镜像
> build     Build an image from a Dockerfile              # 通过 Dockerfile 定制镜像
> commit    Create a new image from a container changes   # 提交当前容器为新的镜像
> cp        Copy files/folders from the containers filesystem to the host path   #从容器中拷贝指定文件或者目录到宿主机中
> create    Create a new container                        # 创建一个新的容器，同 run，但不启动容器
> diff      Inspect changes on a container's filesystem   # 查看 docker 容器变化
> events    Get real time events from the server          # 从 docker 服务获取容器实时事件
> exec      Run a command in an existing container        # 在已存在的容器上运行命令
> export    Stream the contents of a container as a tar archive   # 导出容器的内容流作为一个 tar 归档文件[对应 import ]
> history   Show the history of an image                  # 展示一个镜像形成历史
> images    List images                                   # 列出系统当前镜像
> import    Create a new filesystem image from the contents of a tarball # 从tar包中的内容创建一个新的文件系统映像[对应export]
> info      Display system-wide information               # 显示系统相关信息
> inspect   Return low-level information on a container   # 查看容器详细信息
> kill      Kill a running container                      # kill 指定 docker 容器
> load      Load an image from a tar archive              # 从一个 tar 包中加载一个镜像[对应 save]
> login     Register or Login to the docker registry server    # 注册或者登陆一个 docker 源服务器
> logout    Log out from a Docker registry server          # 从当前 Docker registry 退出
> logs      Fetch the logs of a container                 # 输出当前容器日志信息
> port      Lookup the public-facing port which is NAT-ed to PRIVATE_PORT    # 查看映射端口对应的容器内部源端口
> pause     Pause all processes within a container        # 暂停容器
> ps        List containers                               # 列出容器列表
> pull      Pull an image or a repository from the docker registry server   # 从docker镜像源服务器拉取指定镜像或者库镜像
> push      Push an image or a repository to the docker registry server    # 推送指定镜像或者库镜像至docker源服务器
> restart   Restart a running container                   # 重启运行的容器
> rm        Remove one or more containers                 # 移除一个或者多个容器
> rmi       Remove one or more images       # 移除一个或多个镜像[无容器使用该镜像才可删除，否则需删除相关容器才可继续或 -f 强制删除]
> run       Run a command in a new container              # 创建一个新的容器并运行一个命令
> save      Save an image to a tar archive                # 保存一个镜像为一个 tar 包[对应 load]
> search    Search for an image on the Docker Hub         # 在 docker hub 中搜索镜像
> start     Start a stopped containers                    # 启动容器
> stop      Stop a running containers                     # 停止容器
> tag       Tag an image into a repository                # 给源中镜像打标签
> top       Lookup the running processes of a container   # 查看容器中运行的进程信息
> unpause   Unpause a paused container                    # 取消暂停容器
> version   Show the docker version information           # 查看 docker 版本号
> wait      Block until a container stops, then print its exit code   # 截取容器停止时的退出状态值

# 四 Docker镜像

镜像是一种轻量级、可执行的独立软件包，它包含运行某个软件所需的所有内容，我们把应用程序和配置依赖打包好形成一个可交付的运行环境(包括代码、运行时需要的库、环境变量和配置文件等)，这个打包好的运行环境就是image镜像文件。

只有通过这个镜像文件才能生成Docker容器实例(类似Java中new出来一个对象)。

以我们的pull为例，在下载的过程中我们可以看到docker的镜像好像是在一层一层的在下载

![image-20220209101610987](\images\image-20220209101610987.png)

### UnionFS（联合文件系统）

UnionFS（联合文件系统）：Union文件系统（UnionFS）是一种分层、轻量级并且高性能的文件系统，它支持对文件系统的修改作为一次提交来一层层的叠加，同时可以将不同目录挂载到同一个虚拟文件系统下(unite several directories into a single virtual filesystem)。Union 文件系统是 Docker 镜像的基础。镜像可以通过分层来进行继承，基于基础镜像（没有父镜像），可以制作各种具体的应用镜像。

特性：一次同时加载多个文件系统，但从外面看起来，只能看到一个文件系统，联合加载会把各层文件系统叠加起来，这样最终的文件系统会包含所有底层的文件和目录

### Docker镜像加载原理

Docker的镜像实际上由一层一层的文件系统组成，这种层级的文件系统UnionFS。
bootfs(boot file system)主要包含bootloader和kernel, bootloader主要是引导加载kernel, Linux刚启动时会加载bootfs文件系统，在Docker镜像的最底层是引导文件系统bootfs。这一层与我们典型的Linux/Unix系统是一样的，包含boot加载器和内核。当boot加载完成之后整个内核就都在内存中了，此时内存的使用权已由bootfs转交给内核，此时系统也会卸载bootfs。

rootfs (root file system) ，在bootfs之上。包含的就是典型 Linux 系统中的 /dev, /proc, /bin, /etc 等标准目录和文件。rootfs就是各种不同的操作系统发行版，比如Ubuntu，Centos等等。

对于一个精简的OS，rootfs可以很小，只需要包括最基本的命令、工具和程序库就可以了，因为底层直接用Host的kernel，自己只需要提供 rootfs 就行了。由此可见对于不同的linux发行版, bootfs基本是一致的, rootfs会有差别, 因此不同的发行版可以公用bootfs。

镜像分层最大的一个好处就是共享资源，方便复制迁移，就是为了复用。

比如说有多个镜像都从相同的 base 镜像构建而来，那么 Docker Host 只需在磁盘上保存一份 base 镜像；
同时内存中也只需加载一份 base 镜像，就可以为所有容器服务了。而且镜像的每一层都可以被共享。

当容器启动时，一个新的可写层被加载到镜像的顶部。这一层通常被称作“容器层”，“容器层”之下的都叫“镜像层”。
所有对容器的改动 - 无论添加、删除、还是修改文件都只会发生在容器层中。只有容器层是可写的，容器层下面的所有镜像层都是只读的

### Docker镜像commit操作案例

docker commit提交容器副本使之成为一个新的镜像

docker commit -m="提交的描述信息" -a="作者" 容器ID 要创建的目标镜像名:[标签名

#### 案例演示ubuntu安装vim

从Hub上下载ubuntu镜像到本地并成功运行，原始的默认Ubuntu镜像是不带着vim命令的，外网连通的情况下，安装vim，安装完成后，commit我们自己的新镜像，启动我们的新镜像并和原来的对比。

```
[root@docker-01 ~]# docker run -it centos
[root@9fb857840e2a /]# yum install -y vim
[root@docker-01 yum.repos.d]# docker commit -m "add vim cmd" -a="harry" 9fb857840e2a harry/mycentos:1.1
```

![image-20220209110826448](\images\image-20220209110826448.png)

```
[root@docker-01 yum.repos.d]# docker run -it e9b5fd8ae0b3
[root@d9f19a94b05c /]# vim
```

我们自己commit构建的镜像，新增加了vim功能，可以成功使用

# 五 本地镜像发布到私有库

 1 官方Docker Hub地址：https://hub.docker.com/，中国大陆访问太慢了且准备被阿里云取代的趋势，不太主流。

 2 Dockerhub、阿里云这样的公共镜像仓库可能不太方便，涉及机密的公司不可能提供镜像给公网，所以需要创建一个本地私人仓库供给团队使用，基于公司内部项目构建镜像。

Docker Registry是官方提供的工具，可以用于构建私有镜像仓库

### 下载镜像Docker Registry

```
[root@docker-01 yum.repos.d]# docker pull registry
```

![image-20220209111430653](\images\image-20220209111430653.png)

### 运行私有库Registry，相当于本地有个私有Docker hub

```
[root@docker-01 yum.repos.d]# docker run -d -p 5000:5000 -v /root/:/tmp/registry --privileged=true registry
默认情况，仓库被创建在容器的/var/lib/registry目录下，建议自行用容器卷映射，方便于宿主机联调
```

![image-20220209111653258](\images\image-20220209111653258.png)

### 案例演示创建一个新镜像，ubuntu安装ifconfig命令

docker容器内执行上述两条命令：
apt-get update
apt-get install net-tools

![image-20220209112033157](\images\image-20220209112033157.png)

![image-20220209112053645](\images\image-20220209112053645.png)

安装完成后，commit我们自己的新镜像

公式：
docker commit -m="提交的描述信息" -a="作者" 容器ID 要创建的目标镜像名:[标签名]
命令：在容器外执行，记得

```
[root@docker-01 yum.repos.d]# docker commit -m="ifconfig cmd add" -a="harry" 2538b8f36ac7 harry-ubuntu:1.2
```

### curl验证私服库上有什么镜像

```
[root@docker-01 yum.repos.d]#  curl -XGET http://192.168.31.40:5000/v2/_catalog
```

可以看到，目前私服库没有任何镜像上传过。。。。。。

![image-20220209112402889](\images\image-20220209112402889.png)

将新镜像harry-ubuntu:1.2修改符合私服规范的Tag

按照公式： docker   tag   镜像:Tag   Host:Port/Repository:Tag

```
[root@docker-01 yum.repos.d]# docker tag harry-ubuntu:1.2 192.168.31.40:5000/harry-ubuntu:1.2
```

![image-20220209112605906](\images\image-20220209112605906.png)

### 修改配置文件使之支持http

```json
{
  "registry-mirrors": ["http://hub-mirror.c.163.com"],
  "insecure-registries": ["192.168.31.40:5000"]
}

```

上述理由：docker默认不允许http方式推送镜像，通过配置选项来取消这个限制。====> 修改完后如果不生效，建议重启docker

### push推送到私服库

```
[root@docker-01 yum.repos.d]# docker push 192.168.31.40:5000/harry-ubuntu:1.2
```

![image-20220209113336464](\images\image-20220209113336464.png)

### curl验证私服库上有什么镜像2

```
[root@docker-01 yum.repos.d]#  curl -XGET http://192.168.31.40:5000/v2/_catalog
```

![image-20220209113408372](\images\image-20220209113408372.png)

### Pull到本地运行

```
[root@docker-01 yum.repos.d]# docker pull 192.168.31.40:5000/harry-ubuntu:1.2
```

![image-20220209113721773](\images\image-20220209113721773.png)



# 六 Docker容器数据卷

卷就是目录或文件，存在于一个或多个容器中，由docker挂载到容器，但不属于联合文件系统，因此能够绕过Union File System提供一些用于持续存储或共享数据的特性：
卷的设计目的就是数据的持久化，完全独立于容器的生存周期，因此Docker不会在容器删除时删除其挂载的数据卷

坑：容器卷记得加入 --privileged=true， Docker挂载主机目录访问如果出现cannot open directory .: Permission denied，解决办法：在挂载目录后多加一个--privileged=true参数即可

如果是CentOS7安全模块会比之前系统版本加强，不安全的会先禁止，所以目录挂载的情况被默认为不安全的行为，
在SELinux里面挂载目录被禁止掉了额，如果要开启，我们一般使用--privileged=true命令，扩大容器的权限解决挂载目录没有权限的问题，也即
使用该参数，container内的root拥有真正的root权限，否则，container内的root只是外部的一个普通用户权限。

运行一个带有容器卷存储功能的容器实例   docker run -it --privileged=true -v /宿主机绝对路径目录:/容器内目录      镜像名

 将运用与运行的环境打包镜像，run后形成容器实例运行 ，但是我们对数据的要求希望是持久化的

Docker容器产生的数据，如果不备份，那么当容器实例删除后，容器内的数据自然也就没有了。
为了能保存数据在docker中我们使用卷。

特点：
	1：数据卷可在容器之间共享或重用数据
	2：卷中的更改可以直接实时生效，爽
	3：数据卷中的更改不会包含在镜像的更新中
	4：数据卷的生命周期一直持续到没有容器使用它为

### 数据卷案例

#### 宿主vs容器之间映射添加容器卷

```
[root@docker-01 ~]# docker run -it --name myu3 --privileged=true -v /tmp/myHostData:/tmp/myDockerData ubuntu /bin/bash
```

![image-20220210142717273](\images\image-20220210142717273.png)

![image-20220210142746074](\images\image-20220210142746074.png)

查看数据卷是否挂载成功

![image-20220210143025481](\images\image-20220210143025481.png)

容器和宿主机之间数据共享

1  docker修改，主机同步获得 
2 主机修改，docker同步获得
3 docker容器stop，主机修改，docker容器重启看数据同步。

#### 读写规则映射添加说明

读写(默认）

![image-20220210143929656](\images\image-20220210143929656.png)

docker run -it --privileged=true -v /宿主机绝对路径目录:/容器内目录:rw

只读

容器实例内部被限制，只能读取不能写

![image-20220210144039963](\images\image-20220210144039963.png)

此时如果宿主机写入内容，可以同步给容器内，容器可以读取到。

#### 卷的继承和共享

容器1完成和宿主机的映射

![image-20220210144315631](\images\image-20220210144315631.png)

容器2继承容器1的卷规则  docker run -it  --privileged=true --volumes-from 父类  --name u2 ubuntu

```
[root@docker-01 ~]# docker run -it --privileged=true --volumes-from u1 --name u2 ubuntu  
```

![image-20220210144559844](\images\image-20220210144559844.png)

# 七 Docker常规安装简介

总体步骤

![image-20220210144916243](\images\image-20220210144916243.png)

### 安装tomcat

docker hub上面查找tomcat镜像

![image-20220210145201334](\images\image-20220210145201334.png)

从docker hub上拉取tomcat镜像到本地

```
docker pull tomcat
```

docker images查看是否有拉取到的tomcat

![image-20220210145441595](\images\image-20220210145441595.png)

使用tomcat镜像创建容器实例(也叫运行镜像)

```
docker run -it -p 8080:8080 tomcat
```

访问猫首页

问题

![image-20220210145755833](\images\image-20220210145755833.png)

解决

可能没有映射端口或者没有关闭防火墙

把webapps.dist目录换成webapps,查看webapps 文件夹查看为空

![image-20220210150022557](\images\image-20220210150022557.png)

![image-20220210150059327](\images\image-20220210150059327.png)

免修改版说明

```
[root@docker-01 myHostData]# docker pull billygoo/tomcat8-jdk8
[root@docker-01 myHostData]# docker run -d -p 8080:8080 --name mytomcat8-test billygoo/tomcat8-jdk8

```

### 安装mysql

docker hub上面查找mysql镜像

![image-20220210151217023](\images\image-20220210151217023.png)

从docker hub上(阿里云加速器)拉取mysql镜像到本地标签为5.7

```
[root@docker-01 myHostData]# docker pull mysql:5.7
```

![image-20220210151639837](\images\image-20220210151639837.png)

#### 使用mysql5.7镜像创建容器(也叫运行镜像)

命令出处

![image-20220210151734596](\images\image-20220210151734596.png)

#### 简单版

使用mysql镜像

```
[root@docker-01 myHostData]# docker run -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7
```

![image-20220210151928522](\images\image-20220210151928522.png)

![image-20220210152102247](\images\image-20220210152102247.png)

建库建表插入数据

![image-20220210152419397](\images\image-20220210152419397.png)

外部Win10也来连接运行在dokcer上的mysql容器实例服务

![image-20220210152858705](\images\image-20220210152858705.png)

插入中文数据试试

![image-20220210153039105](\images\image-20220210153039105.png)

docker上默认字符集编码隐患

![image-20220210153131843](\images\image-20220210153131843.png)

问题删除容器后，里面的mysql数据也会被删除

#### 实战版

新建mysql容器实例

```
[root@docker-01 mysql]# docker run -d -p 3306:3306 --privileged=true -v /harry/mysql/log/:/var/log/mysql -v /harry/mysql/data:/var/lib/mysql -v /harry/mysql/conf/:/etc/mysql/conf.d -e MYSQL_ROOT_PASSWORD=123456  --name mysql mysql:5.7
```

新建my.cnf，通过容器卷同步给mysql容器实例

```
[client]
default_character_set=utf8
[mysqld]
collation_server = utf8_general_ci
character_set_server = utf8

```

![image-20220210153909999](\images\image-20220210153909999.png)

重新启动mysql容器实例再重新进入并查看字符编码

```
[root@docker-01 ~]# docker restart mysql
```

![image-20220210154149580](\images\image-20220210154149580.png)

再新建库新建表再插入中文测试

![image-20220210154326245](\images\image-20220210154326245.png)



结论

> 之前的DB  无效
>
> 修改字符集操作+重启mysql容器实例
>
> 之后的DB  有效，需要新建
>
> 结论：docker安装完MySQL并run出容器后，建议请先修改完字符集编码后再新建mysql库-表-插数据

如将当前容器实例删除，再重新来一次，之前建的db01实例仍然存在

![image-20220210155417223](\images\image-20220210155417223.png)

### 安装redis

从docker hub上(阿里云加速器)拉取redis镜像到本地标签为6.0.8

```
[root@docker-01 ~]# docker pull redis:6.0.8
```

![image-20220210155627595](\images\image-20220210155627595.png)

入门命令

```
[root@docker-01 ~]# docker run -d -p 6379:6379 redis:6.0.8
```

![image-20220210155908766](\images\image-20220210155908766.png)

在CentOS宿主机下新建目录/app/redis

```
[root@docker-01 data]# mkdir -p /app/redis/
```

redis.conf文件模板拷贝进/app/redis目录下

/app/redis目录下修改redis.conf文件

3 /app/redis目录下修改redis.conf文件
  3.1 开启redis验证    可选
    requirepass 123

  3.2 允许redis外地连接  必须
     注释掉 # bind 127.0.0.1

![image-20220210160925440](\images\image-20220210160925440.png)

  3.3   daemonize no
     将daemonize yes注释起来或者 daemonize no设置，因为该配置和docker run中-d参数冲突，会导致容器一直启动失败

![image-20220210161051137](\images\image-20220210161051137.png)

  3.4 开启redis数据持久化  appendonly yes  可选

使用redis6.0.8镜像创建容器(也叫运行镜像)

```
[root@docker-01 ~]# docker run  -p 6379:6379 --name myr3 --privileged=true -v /app/redis/redis.conf:/etc/redis/redis.conf -v /app/redis/data:/data -d redis:6.0.8 redis-server /etc/redis/redis.conf
```

测试redis-cli连接上来

![image-20220210161344994](\images\image-20220210161344994.png)

证明docker启动使用了我们自己指定的配置文件

修改前我们用的配置文件，数据库默认是16个

![image-20220210161513576](\images\image-20220210161513576.png)

修改配置文件databases为10 宿主机的修改会同步给docker容器里面的配置。

![image-20220210161624511](\images\image-20220210161624511.png)

```
[root@docker-01 ~]# docker restart myr3
[root@docker-01 ~]# docker exec -it myr3 /bin/bash
```

![image-20220210161916818](\images\image-20220210161916818.png)

# 八 Docker复杂安装

### 安装mysql主从复制

#### 新建主服务器容器实例3307

```
[root@docker-01 ~]# docker run -p 3307:3306 --name mysql-master \
> -v /mydata/mysql-master/log:/var/log/mysql \
> -v /mydata/mysql-master/data:/var/lib/mysql \
> -v /mydata/mysql-master/conf:/etc/mysql \
> -e MYSQL_ROOT_PASSWORD=root  \
> -d mysql:5.7
```

#### 进入/mydata/mysql-master/conf目录下新建my.cnf

```
[mysqld]
## 设置server_id，同一局域网中需要唯一
server_id=101 
## 指定不需要同步的数据库名称
binlog-ignore-db=mysql  
## 开启二进制日志功能
log-bin=mall-mysql-bin  
## 设置二进制日志使用内存大小（事务）
binlog_cache_size=1M  
## 设置使用的二进制日志格式（mixed,statement,row）
binlog_format=mixed  
## 二进制日志过期清理时间。默认值为0，表示不自动清理。
expire_logs_days=7  
## 跳过主从复制中遇到的所有错误或指定类型的错误，避免slave端复制中断。
## 如：1062错误是指一些主键重复，1032错误是因为主从数据库数据不一致
slave_skip_errors=1062
```

#### 修改完配置后重启master实例

```
[root@docker-01 conf]# docker restart mysql-master
```

#### 进入mysql-master容器

```
[root@docker-01 conf]# docker exec -it mysql-master /bin/bash
root@a68e52b03207:/# mysql -uroot -proot
```

#### master容器实例内创建数据同步用户

```
mysql> CREATE USER 'slave'@'%' IDENTIFIED BY '123456'
mysql> GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'slave'@'%';
```

#### 新建从服务器容器实例3308

```
[root@docker-01 conf]# docker run -p 3308:3306 --name mysql-slave \
> -v /mydata/mysql-slave/log:/var/log/mysql \
> -v /mydata/mysql-slave/data:/var/lib/mysql \
> -v /mydata/mysql-slave/conf:/etc/mysql \
> -e MYSQL_ROOT_PASSWORD=root  \
> -d mysql:5.7
```

#### 进入/mydata/mysql-slave/conf目录下新建my.cnf

```
[mysqld]
## 设置server_id，同一局域网中需要唯一
server_id=102
## 指定不需要同步的数据库名称
binlog-ignore-db=mysql  
## 开启二进制日志功能，以备Slave作为其它数据库实例的Master时使用
log-bin=mall-mysql-slave1-bin  
## 设置二进制日志使用内存大小（事务）
binlog_cache_size=1M  
## 设置使用的二进制日志格式（mixed,statement,row）
binlog_format=mixed  
## 二进制日志过期清理时间。默认值为0，表示不自动清理。
expire_logs_days=7  
## 跳过主从复制中遇到的所有错误或指定类型的错误，避免slave端复制中断。
## 如：1062错误是指一些主键重复，1032错误是因为主从数据库数据不一致
slave_skip_errors=1062  
## relay_log配置中继日志
relay_log=mall-mysql-relay-bin  
## log_slave_updates表示slave将复制事件写进自己的二进制日志
log_slave_updates=1  
## slave设置为只读（具有super权限的用户除外）
read_only=1
```

#### 修改完配置后重启slave实例

```
[root@docker-01 conf]# docker restart mysql-slave
```

#### 在主数据库中查看主从同步状态

```
mysql> show master status;
```

![image-20220212095620556](\images\image-20220212095620556.png)

#### 进入mysql-slave容器

```
[root@docker-01 ~]# docker exec -it mysql-slave /bin/bash
root@a1e0158e0431:/# mysql -uroot -proot
```

#### 在从数据库中配置主从复制

![image-20220212095901342](\images\image-20220212095901342.png)

```
change master to master_host='宿主机ip', master_user='slave', master_password='123456', master_port=3307, master_log_file='mall-mysql-bin.000001', master_log_pos=617, master_connect_retry=30
```

主从复制命令参数说明

master_host：主数据库的IP地址；
master_port：主数据库的运行端口；
master_user：在主数据库创建的用于同步数据的用户账号；
master_password：在主数据库创建的用于同步数据的用户密码；
master_log_file：指定从数据库要复制数据的日志文件，通过查看主数据的状态，获取File参数；
master_log_pos：指定从数据库从哪个位置开始复制数据，通过查看主数据的状态，获取Position参数；
master_connect_retry：连接失败重试的时间间隔，单位为秒。

![image-20220212100609813](\images\image-20220212100609813.png)

#### 在从数据库中开启主从同步

```
mysql> start slave;
```

![image-20220212100758290](\images\image-20220212100758290.png)

#### 查看从数据库状态发现已经同步

![image-20220212100842105](\images\image-20220212100842105.png)

#### 主从复制测试

主机新建库-使用库-新建表-插入数据，ok

```
mysql> create database testdb;
mysql> use testdb;
mysql> create table t1(id int,  name varchar(20));
mysql> insert into t1 values(1,"harry");
mysql> insert into t1 values(2,"cat");

```

从机使用库-查看记录，ok

![image-20220212101331580](\images\image-20220212101331580.png)

### 安装redis集群

cluster(集群)模式-docker版,哈希槽分区进行亿级数据存储

面试题.1~2亿条数据需要缓存，请问如何设计这个存储案例: 单机单台100%不可能，肯定是分布式存储，用redis如何落地？ 一般业界有3种解决方案

#### 哈希取余分区

![image-20220212101541949](\images\image-20220212101541949.png)

2亿条记录就是2亿个k,v，我们单机不行必须要分布式多机，假设有3台机器构成一个集群，用户每次读写操作都是根据公式：
hash(key) % N个机器台数，计算出哈希值，用来决定数据映射到哪一个节点上。

优点：
    简单粗暴，直接有效，只需要预估好数据规划好节点，例如3台、8台、10台，就能保证一段时间的数据支撑。使用Hash算法让固定的一部分请求落到同一台服务器上，这样每台服务器固定处理一部分请求（并维护这些请求的信息），起到负载均衡+分而治之的作用。

缺点：
   原来规划好的节点，进行扩容或者缩容就比较麻烦了额，不管扩缩，每次数据变动导致节点有变动，映射关系需要重新进行计算，在服务器个数固定不变时没有问题，如果需要弹性扩容或故障停机的情况下，原来的取模公式就会发生变化：Hash(key)/3会变成Hash(key) /?。此时地址经过取余运算的结果将发生很大变化，根据公式获取的服务器也会变得不可控。
某个redis机器宕机了，由于台数数量变化，会导致hash取余全部数据重新洗牌。

#### 一致性哈希算法分区

一致性Hash算法背景
　　一致性哈希算法在1997年由麻省理工学院中提出的，设计目标是为了解决分布式缓存数据变动和映射问题，某个机器宕机了，分母数量改变了，自然取余数不OK了。提出一致性Hash解决方案。目的是当服务器个数发生变动时，尽量减少影响客户端到服务器的映射关系

##### 三大步骤

算法构建一致性哈希环

​    一致性哈希算法必然有个hash函数并按照算法产生hash值，这个算法的所有可能哈希值会构成一个全量集，这个集合可以成为一个hash空间[0,2^32-1]，这个是一个线性空间，但是在算法中，我们通过适当的逻辑控制将它首尾相连(0 = 2^32),这样让它逻辑上形成了一个环形空间

​    它也是按照使用取模的方法，前面笔记介绍的节点取模法是对节点（服务器）的数量进行取模。而一致性Hash算法是对2^32取模，简单来说，一致性Hash算法将整个哈希值空间组织成一个虚拟的圆环，如假设某哈希函数H的值空间为0-2^32-1（即哈希值是一个32位无符号整形），整个哈希环如下图：整个空间按顺时针方向组织，圆环的正上方的点代表0，0点右侧的第一个点代表1，以此类推，2、3、4、……直到2^32-1，也就是说0点左侧的第一个点代表2^32-1， 0和2^32-1在零点中方向重合，我们把这个由2^32个点组成的圆环称为Hash环。

![image-20220212101817361](\images\image-20220212101817361.png)

服务器IP节点映射

   将集群中各个IP节点映射到环上的某一个位置。
   将各个服务器使用Hash进行一个哈希，具体可以选择服务器的IP或主机名作为关键字进行哈希，这样每台机器就能确定其在哈希环上的位置。假如4个节点NodeA、B、C、D，经过IP地址的哈希函数计算(hash(ip))，使用IP地址哈希后在环空间的位置如下：  

![image-20220212101852364](\images\image-20220212101852364.png)

##### 优点

一致性哈希算法的容错性

假设Node C宕机，可以看到此时对象A、B、D不会受到影响，只有C对象被重定位到Node D。一般的，在一致性Hash算法中，如果一台服务器不可用，则受影响的数据仅仅是此服务器到其环空间中前一台服务器（即沿着逆时针方向行走遇到的第一台服务器）之间数据，其它不会受到影响。简单说，就是C挂了，受到影响的只是B、C之间的数据，并且这些数据会转移到D进行存储。

![image-20220212102004233](\images\image-20220212102004233.png)

一致性哈希算法的扩展性

数据量增加了，需要增加一台节点NodeX，X的位置在A和B之间，那收到影响的也就是A到X之间的数据，重新把A到X的数据录入到X上即可，
不会导致hash取余全部数据重新洗牌。

![image-20220212102045778](\images\image-20220212102045778.png)

##### 缺点

一致性哈希算法的数据倾斜问题

Hash环的数据倾斜问题
一致性Hash算法在服务节点太少时，容易因为节点分布不均匀而造成数据倾斜（被缓存的对象大部分集中缓存在某一台服务器上）问题，例如系统中只有两台服务器：

![image-20220212102133579](\images\image-20220212102133579.png)

##### 总结

为了在节点数目发生改变时尽可能少的迁移数据

将所有的存储节点排列在收尾相接的Hash环上，每个key在计算Hash后会顺时针找到临近的存储节点存放。
而当有节点加入或退出时仅影响该节点在Hash环上顺时针相邻的后续节点。  

优点
加入和删除节点只影响哈希环中顺时针方向的相邻的节点，对其他节点无影响。

缺点 
数据的分布和节点的位置有关，因为这些节点不是均匀的分布在哈希环上的，所以数据在进行存储时达不到均匀分布的效果。

### 配置Redis 3主3从集群

#### 新建6个docker容器redis实例

```
docker run -d --name redis-node-1 --net host --privileged=true -v /data/redis/share/redis-node-1:/data redis:6.0.8 --cluster-enabled yes --appendonly yes --port 6381
 
docker run -d --name redis-node-2 --net host --privileged=true -v /data/redis/share/redis-node-2:/data redis:6.0.8 --cluster-enabled yes --appendonly yes --port 6382
 
docker run -d --name redis-node-3 --net host --privileged=true -v /data/redis/share/redis-node-3:/data redis:6.0.8 --cluster-enabled yes --appendonly yes --port 6383
 
docker run -d --name redis-node-4 --net host --privileged=true -v /data/redis/share/redis-node-4:/data redis:6.0.8 --cluster-enabled yes --appendonly yes --port 6384
 
docker run -d --name redis-node-5 --net host --privileged=true -v /data/redis/share/redis-node-5:/data redis:6.0.8 --cluster-enabled yes --appendonly yes --port 6385
 
docker run -d --name redis-node-6 --net host --privileged=true -v /data/redis/share/redis-node-6:/data redis:6.0.8 --cluster-enabled yes --appendonly yes --port 6386

```

如果运行成功，效果如下：

![image-20220212102456152](\images\image-20220212102456152.png)

![image-20220212102523031](\images\image-20220212102523031.png)

#### 进入容器redis-node-1并为6台机器构建集群关系

```
[root@docker-01 conf]# docker exec -it redis-node-1 /bin/bash
```

构建主从关系

/注意，进入docker容器后才能执行一下命令，且注意自己的真实IP地址

```
redis-cli --cluster create 192.168.31.40:6381 192.168.31.40:6382 192.168.31.40:6383 192.168.31.40:6384 192.168.31.40:6385 192.168.31.40:6386 --cluster-replicas 1
```

--cluster-replicas 1 表示为每个master创建一个slave节点

![image-20220212102832249](\images\image-20220212102832249.png)

![image-20220212102847608](\images\image-20220212102847608.png)

主从映射：

M6381     ---->   S 6384

M6382     ---->    S 6385

M6383    ----->   S 6386

#### 链接进入6381作为切入点，查看集群状态

```
root@docker-01:/data# redis-cli -p 6381
```

![image-20220212103627833](\images\image-20220212103627833.png)

![image-20220212103715292](\images\image-20220212103715292.png)

### 主从容错切换迁移案例

#### 数据读写存储

启动6机构成的集群并通过exec进入

对6381新增两个key 防止路由失效加参数-c并新增两个key

![image-20220212103925276](\images\image-20220212103925276.png)

![image-20220212104045737](\images\image-20220212104045737.png)

查看集群信息

![image-20220212104318241](\images\image-20220212104318241.png)

![image-20220212104439500](\images\image-20220212104439500.png)

#### 容错切换迁移

主6381和从机切换，先停止主机6381，6381主机停了，对应的真实从机上位，6381作为1号主机分配的从机以实际情况为准，具体是几号机器就是几号

```
[root@docker-01 conf]# docker rm -f redis-node-1
```

![image-20220212104843041](\images\image-20220212104843041.png)

6381宕机了，6384上位成为了新的master。
每次案例下面挂的从机以实际情况为准，具体是几号机器就是几号

先还原之前的3主3从

先启6381

![image-20220212105247611](\images\image-20220212105247611.png)

6381仍然是slave 6384仍然是master

再停6384

```
[root@docker-01 conf]# docker stop redis-node-4
```

![image-20220212105431773](\images\image-20220212105431773.png)

6381变成master

再启6384

```
[root@docker-01 conf]# docker start redis-node-4
```

![image-20220212105604709](\images\image-20220212105604709.png)

查看集群状态redis-cli --cluster check 自己IP:6381

![image-20220212105809276](\images\image-20220212105809276.png)

### 主从扩容案例

#### 新建6387、6388两个节点+新建后启动+查看是否8节点

```
[root@docker-01 conf]# docker run -d --name redis-node-7 --net host --privileged=true -v /data/redis/share/redis-node-7:/data redis:6.0.8 --cluster-enabled yes --appendonly yes --port 6387

[root@docker-01 conf]# docker run -d --name redis-node-8 --net host --privileged=true -v /data/redis/share/redis-node-8:/data redis:6.0.8 --cluster-enabled yes --appendonly yes --port 6388

```

进入6387容器实例内部

```
docker exec -it redis-node-7 /bin/bash
```

#### 将新增的6387节点(空槽号)作为master节点加入原集群

将新增的6387作为master节点加入集群
redis-cli --cluster add-node 自己实际IP地址:6387 自己实际IP地址:6381
6387 就是将要作为master新增节点
6381 就是原来集群节点里面的领路人，相当于6387拜拜6381的码头从而找到组织加入集群

![image-20220212110314491](\images\image-20220212110314491.png)

#### 检查集群情况第1次

![image-20220212110445869](\images\image-20220212110445869.png)

#### 重新分派槽号

重新分派槽号
命令:redis-cli --cluster reshard IP地址:端口号
redis-cli --cluster reshard 192.168.31.40:6381

![image-20220212111304912](\images\image-20220212111304912.png)

#### 检查集群情况第2次

redis-cli --cluster check 真实ip地址:6381

其他节点的哈希槽平均分配给了新加入的6387 

![image-20220212111423554](\images\image-20220212111423554.png)

为什么6387是3个新的区间，以前的还是连续？
重新分配成本太高，所以前3家各自匀出来一部分，从6381/6382/6383三个旧节点分别匀出1364个坑位给新节点6387

#### 为主节点6387分配从节点6388

命令：redis-cli --cluster add-node ip:新slave端口 ip:新master端口 --cluster-slave --cluster-master-id 新主机节点ID

redis-cli --cluster add-node 192.168.31.40:6388 192.168.31.40:6387 --cluster-slave --cluster-master-id  6be55bb740583762238edb2787a78b6b33b920bc -------这个是6387的编号，按照自己实际情况

![image-20220212111902151](\images\image-20220212111902151.png)

#### 检查集群情况第3次

![image-20220212112144444](\images\image-20220212112144444.png)

### 主从缩容案例

目的：6387和6388下线

检查集群情况1获得6388的节点ID

![image-20220212112254923](\images\image-20220212112254923.png)

#### 从集群中将4号从节点6388删除

命令：redis-cli --cluster del-node ip:从机端口 从机6388节点ID

```
redis-cli --cluster del-node 192.168.31.40:6388 f255e016e68cd4d3688133a4f990816998928f61 
```

![image-20220212112628099](\images\image-20220212112628099.png)

 检查一下发现，6388被删除了，只剩下7台机器了。

![image-20220212112707383](\images\image-20220212112707383.png)

#### 将6387的槽号清空，重新分配，本例将清出来的槽号都给6381

```
redis-cli --cluster reshard 192.168.31.40:6381
```

![image-20220212113107954](\images\image-20220212113107954.png)

#### 检查集群情况第二次

redis-cli --cluster check 192.168.31.40:6381

4096个槽位都指给6381，它变成了8192个槽位，相当于全部都给6381了，不然要输入3次，一锅端

![image-20220212113315925](\images\image-20220212113315925.png)

#### 将6387删除

命令：redis-cli --cluster del-node ip:端口 6387节点ID

redis-cli --cluster del-node 192.168.31.40:6387 6be55bb740583762238edb2787a78b6b33b920bc 1

![image-20220212113424748](\images\image-20220212113424748.png)

#### 检查集群情况第三次

![image-20220212113541527](\images\image-20220212113541527.png)

# 九 DockerFile解析

Dockerfile是用来构建Docker镜像的文本文件，是由一条条构建镜像所需的指令和参数构成的脚本。

![image-20220212113829036](\images\image-20220212113829036.png)

官网 https://docs.docker.com/engine/reference/builder/

构建三步骤 

编写Dockerfile文件 --> docker build命令构建镜像 --> docker run依镜像运行容器实例

### DockerFile构建过程解析

Dockerfile内容基础知识:

1：每条保留字指令都必须为大写字母且后面要跟随至少一个参数

2：指令按照从上到下，顺序执行

3：#表示注释

4：每条指令都会创建一个新的镜像层并对镜像进行提交

Docker执行Dockerfile的大致流程:

（1）docker从基础镜像运行一个容器

（2）执行一条指令并对容器作出修改

（3）执行类似docker commit的操作提交一个新的镜像层

（4）docker再基于刚提交的镜像运行一个新容器

（5）执行dockerfile中的下一条指令直到所有指令都执行完成

从应用软件的角度来看，Dockerfile、Docker镜像与Docker容器分别代表软件的三个不同阶段，
*  Dockerfile是软件的原材料
*  Docker镜像是软件的交付品
*  Docker容器则可以认为是软件镜像的运行态，也即依照镜像运行的容器实例

Dockerfile面向开发，Docker镜像成为交付标准，Docker容器则涉及部署与运维，三者缺一不可，合力充当Docker体系的基石。

![image-20220212114144061](\images\image-20220212114144061.png)

1 Dockerfile，需要定义一个Dockerfile，Dockerfile定义了进程需要的一切东西。Dockerfile涉及的内容包括执行代码或者是文件、环境变量、依赖包、运行时环境、动态链接库、操作系统的发行版、服务进程和内核进程(当应用进程需要和系统服务和内核进程打交道，这时需要考虑如何设计namespace的权限控制)等等;

2 Docker镜像，在用Dockerfile定义一个文件之后，docker build时会产生一个Docker镜像，当运行 Docker镜像时会真正开始提供服务;

3 Docker容器，容器是直接提供服务的

### DockerFile常用保留字指令

参考tomcat8的dockerfile入门 https://github.com/docker-library/tomcat

#### FROM

基础镜像，当前新镜像是基于哪个镜像的，指定一个已经存在的镜像作为模板，第一条必须是from

#### MAINTAINER

镜像维护者的姓名和邮箱地址

#### RUN

容器构建时需要运行的命令,RUN是在 docker build时运行

shell格式:

![image-20220212114321405](\images\image-20220212114321405.png)

RUN yum -y install vim

exec格式:

![image-20220212114354212](\images\image-20220212114354212.png)

#### EXPOSE

当前容器对外暴露出的端口

#### WORKDIR

指定在创建容器后，终端默认登陆的进来工作目录，一个落脚点

#### USER

指定该镜像以什么样的用户去执行，如果都不指定，默认是root

#### ENV

用来在构建镜像过程中设置环境变量


ENV MY_PATH /usr/mytest
这个环境变量可以在后续的任何RUN指令中使用，这就如同在命令前面指定了环境变量前缀一样；
也可以在其它指令中直接使用这些环境变量，

比如：WORKDIR $MY_PATH

#### ADD

将宿主机目录下的文件拷贝进镜像且会自动处理URL和解压tar压缩包

#### COPY

类似ADD，拷贝文件和目录到镜像中。
将从构建上下文目录中 <源路径> 的文件/目录复制到新的一层的镜像内的 <目标路径> 位置

```
COPY src des
COPY ["src", "dest"]
<src源路径>：源文件或者源目录
<dest目标路径>：容器内的指定路径，该路径不用事先建好，路径不存在的话，会自动创建。
```

#### VOLUME

容器数据卷，用于数据保存和持久化工作

#### CMD

指定容器启动后的要干的事情

![image-20220212114723143](\images\image-20220212114723143.png)

注意

Dockerfile 中可以有多个 CMD 指令，但只有最后一个生效，CMD 会被 docker run 之后的参数替换

参考官网Tomcat的dockerfile演示讲解,官网最后一行命令

![image-20220212114819658](\images\image-20220212114819658.png)

我们演示自己的覆盖操作

```
[root@docker-01 ~]# docker run -it -p 8080:8080 billygoo/tomcat8-jdk8 /bin/bash
```

它和前面RUN命令的区别

CMD是在docker run 时运行,RUN是在 docker build时运行

#### ENTRYPOINT

也是用来指定一个容器启动时要运行的命令,类似于 CMD 指令，但是ENTRYPOINT不会被docker run后面的命令覆盖，而且这些命令行参数会被当作参数送给 ENTRYPOINT 指令指定的程序

命令格式和案例说明

![image-20220212115141361](\images\image-20220212115141361.png)

ENTRYPOINT可以和CMD一起用，一般是变参才会使用 CMD ，这里的 CMD 等于是在给 ENTRYPOINT 传参。
当指定了ENTRYPOINT后，CMD的含义就发生了变化，不再是直接运行其命令而是将CMD的内容作为参数传递给ENTRYPOINT指令，他两个组合会变成

![image-20220212115204365](\images\image-20220212115204365.png)

案例如下：假设已通过 Dockerfile 构建了 nginx:test 镜像：

![image-20220212115220033](\images\image-20220212115220033.png)

![image-20220212115251894](\images\image-20220212115251894.png)

优点：在执行docker run的时候可以指定 ENTRYPOINT 运行所需的参数

注意：如果 Dockerfile 中如果存在多个 ENTRYPOINT 指令，仅最后一个生效

![image-20220212115340098](\images\image-20220212115340098.png)

### 自定义镜像mycentosjava8

Centos7镜像具备vim+ifconfig+jdk8，JDK的下载镜像地址：https://mirrors.yangxingzhen.com/jdk/

#### 准备编写Dockerfile文件

![image-20220213100614207](\images\image-20220213100614207.png)

```dockerfile
FROM centos
MAINTAINER harry<caishuang0413@gmail.com>

ENV MYPATH /usr/local
WORKDIR $MYPATH

#安装vim编辑器
RUN yum -y install vim
#安装ifconfig命令查看网络IP
RUN yum -y install net-tools
#安装java8及lib库
RUN yum -y install glibc.i686
RUN mkdir /usr/local/java
#ADD 是相对路径jar,把jdk-8u171-linux-x64.tar.gz添加到容器中,安装包必须要和Dockerfile文件在同一位置
ADD jdk-8u171-linux-x64.tar.gz /usr/local/java/
#配置java环境变量
ENV JAVA_HOME /usr/local/java/jdk1.8.0_171
ENV JRE_HOME $JAVA_HOME/jre
ENV CLASSPATH $JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib:$CLASSPATH
ENV PATH $JAVA_HOME/bin:$PATH

EXPOSE 80

CMD echo $MYPATH
CMD echo "success--------------ok"
CMD /bin/bash

```

```
docker build -t 新镜像名字:TAG .
```

注意，上面TAG后面有个空格，有个点

![image-20220213102539285](\images\image-20220213102539285.png)

运行  docker run -it 新镜像名字:TAG

![image-20220213102650815](\images\image-20220213102650815.png)

![image-20220213102838819](\images\image-20220213102838819.png)

### 虚悬镜像

仓库名、标签都是<none>的镜像，俗称dangling image

Dockerfile写一个

```
FROM ubuntu
CMD echo 'action is success'
```

docker build .

![image-20220213103228877](\images\image-20220213103228877.png)

```
docker image ls -f dangling=true
```

![image-20220213103517954](\images\image-20220213103517954.png)

删除

docker image prune

虚悬镜像已经失去存在价值，可以删除

![image-20220213103635712](\images\image-20220213103635712.png)

# 十、Docker微服务实战

#### 通过IDEA新建一个普通微服务模块

pom

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.6.3</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.harry.docker_boot</groupId>
    <artifactId>docker_boot</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>docker_boot</name>
    <description>Demo project for Spring Boot</description>
    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <maven.compiler.source>1.8</maven.compiler.source>
        <maven.compiler.target>1.8</maven.compiler.target>
        <junit.version>4.12</junit.version>
        <log4j.version>1.2.17</log4j.version>
        <lombok.version>1.16.18</lombok.version>
        <mysql.version>5.1.47</mysql.version>
        <druid.version>1.1.16</druid.version>
        <mapper.version>4.1.5</mapper.version>
        <mybatis.spring.boot.version>1.3.0</mybatis.spring.boot.version>
    </properties>

    <dependencies>
        <!--SpringBoot通用依赖模块-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <!--test-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>



    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>

```

yml

```
server.port=6001
```

启动类

```java
package com.harry.docker_boot;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DockerBootApplication {

    public static void main(String[] args) {
        SpringApplication.run(DockerBootApplication.class, args);
    }

}

```

controller

```java
package com.harry.springboot.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;


@Controller
public class HelloController {
    @RequestMapping("/hello")
    @ResponseBody
    public String HelloSpringBoot(){
        return "hello World";
    }
}

```



#### 通过dockerfile发布微服务部署到docker容器

docker_boot-0.0.1-SNAPSHOT.jar

编写Dockerfile

```dockerfile
# 基础镜像使用java
FROM java:8
# 作者
MAINTAINER harry
# VOLUME 指定临时文件目录为/tmp，在主机/var/lib/docker目录下创建了一个临时文件并
链接到容器的/tmp
VOLUME /tmp
# 将jar包添加到容器中并更名为harry_docker.jar
ADD docker_boot-0.0.1-SNAPSHOT.jar harry_docker.jar
# 运行jar包
RUN bash -c 'touch /zzyy_docker.jar'
ENTRYPOINT ["java","-jar","/harry_docker.jar"]
#暴露6001端口作为微服务
EXPOSE 6001

```

将微服务jar包和Dockerfile文件上传到同一个目录下/mydocker

![image-20220213111406526](\images\image-20220213111406526.png)

```
[root@docker-01 docker_boot]# docker build -t harry_docker:1.6 .
```

![image-20220213111656372](\images\image-20220213111656372.png)

运行容器

```
[root@docker-01 docker_boot]# docker run -d -p 6001:6001 harry_docker:1.6
```

![image-20220213111945781](\images\image-20220213111945781.png)

# 十一 Docker网络

容器间的互联和通信以及端口映射，容器IP变动时候可以通过服务名直接网络通信而不受到影响

docker不启动，默认网络情况

![image-20220213112249283](\images\image-20220213112249283.png)

docker启动后，网络情况，会产生一个名为docker0的虚拟网桥

![image-20220213112333389](\images\image-20220213112333389.png)

查看docker网络模式命令，默认创建3大网络模式

![image-20220213112428921](\images\image-20220213112428921.png)

### 常用基本命令

All命令

![image-20220213112544717](\images\image-20220213112544717.png)

查看网络

```
docker network ls
```

查看网络源数据

docker network inspect  XXX网络名字

```
[root@docker-01 docker_boot]# docker network inspect bridge
```

![image-20220213112906718](\images\image-20220213112906718.png)

案例

![image-20220213113535805](\images\image-20220213113535805.png)

![image-20220213113632979](\images\image-20220213113632979.png)

### 网络模式

#### 总体介绍

![image-20220213113729396](\images\image-20220213113729396.png)

bridge模式：使用--network  bridge指定，默认使用docker0

host模式：使用--network host指定

none模式：使用--network none指定

container模式：使用--network container:NAME或者容器ID指定

#### 容器实例内默认网络IP生产规则

1 先启动两个ubuntu容器实例

![image-20220213113957013](\images\image-20220213113957013.png)

2 docker inspect 容器ID or 容器名字

![image-20220213114049488](\images\image-20220213114049488.png)

![image-20220213114118794](\images\image-20220213114118794.png)

3  关闭ube实例，新建u3，查看ip变化

![image-20220213114305598](\images\image-20220213114305598.png)

结论：docker容器内部的ip是有可能会发生改变的

### 案例说明

#### bridge

Docker 服务默认会创建一个 docker0 网桥（其上有一个 docker0 内部接口），该桥接网络的名称为docker0，它在内核层连通了其他的物理或虚拟网卡，这就将所有容器和本地主机都放到同一个物理网络。Docker 默认指定了 docker0 接口 的 IP 地址和子网掩码，让主机和容器之间可以通过网桥相互通信。

查看 bridge 网络的详细信息，并通过 grep 获取名称项

docker network inspect bridge | grep name

![image-20220213114451669](\images\image-20220213114451669.png)

ifconfig

![image-20220213114534870](\images\image-20220213114534870.png)

说明

> 1 Docker使用Linux桥接，在宿主机虚拟一个Docker容器网桥(docker0)，Docker启动一个容器时会根据Docker网桥的网段分配给容器一个IP地址，称为Container-IP，同时Docker网桥是每个容器的默认网关。因为在同一宿主机内的容器都接入同一个网桥，这样容器之间就能够通过容器的Container-IP直接通信。
>
> 2 docker run 的时候，没有指定network的话默认使用的网桥模式就是bridge，使用的就是docker0。在宿主机ifconfig,就可以看到docker0和自己create的network(后面讲)eth0，eth1，eth2……代表网卡一，网卡二，网卡三……，lo代表127.0.0.1，即localhost，inet addr用来表示网卡的IP地址
>
> 3 网桥docker0创建一对对等虚拟设备接口一个叫veth，另一个叫eth0，成对匹配。
>    3.1 整个宿主机的网桥模式都是docker0，类似一个交换机有一堆接口，每个接口叫veth，在本地主机和容器内分别创建一个虚拟接口，并让他们彼此联通（这样一对接口叫veth pair）；
>    3.2 每个容器实例内部也有一块网卡，每个接口叫eth0；
>    3.3 docker0上面的每个veth匹配某个容器实例内部的eth0，两两配对，一一匹配。
>  通过上述，将宿主机上的所有容器都连接到这个内部网络上，两个容器在同一个网络下,会从这个网关下各自拿到分配的ip，此时两个容器的网络是互通的。

![image-20220213114629214](\images\image-20220213114629214.png)

```
docker run -d -p 8081:8080   --name tomcat81 billygoo/tomcat8-jdk8
docker run -d -p 8082:8080   --name tomcat82 billygoo/tomcat8-jdk8
```

![image-20220213114752859](\images\image-20220213114752859.png)

![image-20220213114844720](\images\image-20220213114844720.png)

![image-20220213115010573](\images\image-20220213115010573.png)

#### host

直接使用宿主机的 IP 地址与外界进行通信，不再需要额外进行NAT 转换。

案例

容器将不会获得一个独立的Network Namespace， 而是和宿主机共用一个Network Namespace。容器将不会虚拟出自己的网卡而是使用宿主机的IP和端口。

![image-20220213115213570](\images\image-20220213115213570.png)

警告

```
[root@docker-01 docker_boot]# docker run -d -p 8083:8080 --network host --name tomcat83 billygoo/tomcat8-jdk8
```

![image-20220213115533388](\images\image-20220213115533388.png)

问题：
     docke启动时总是遇见标题中的警告
原因：
    docker启动时指定--network=host或-net=host，如果还指定了-p映射端口，那这个时候就会有此警告，
并且通过-p设置的参数将不会起到任何作用，端口号会以主机端口号为主，重复时则递增。
解决:
    解决的办法就是使用docker的其他网络模式，例如--network=bridge，这样就可以解决问题，或者直接无视。

正确

```
[root@docker-01 docker_boot]# docker run -d --network host --name tomcat83 billygoo/tomcat8-jdk8
```

无之前的配对显示了，看容器实例内部

![image-20220213122415963](\images\image-20220213122415963.png)

没有设置-p的端口映射了，如何访问启动的tomcat83？？

http://宿主机IP:8080/

在CentOS里面用默认的火狐浏览器访问容器内的tomcat83看到访问成功，因为此时容器的IP借用主机的，
所以容器共享宿主机网络IP，这样的好处是外部主机与容器可以直接通信。

#### none

在none模式下，并不为Docker容器进行任何网络配置。 
也就是说，这个Docker容器没有网卡、IP、路由等信息，只有一个lo
需要我们自己为Docker容器添加网卡、配置IP等。

禁用网络功能，只有lo标识(就是127.0.0.1表示本地回环)

```
[root@docker-01 docker_boot]# docker run -d -p 8084:8080 --network none --name tomcat84 billygoo/tomcat8-jdk8
```

 进入容器内部查看

![image-20220213123036518](\images\image-20220213123036518.png)

#### container

新建的容器和已经存在的一个容器共享一个网络ip配置而不是和宿主机共享。新创建的容器不会创建自己的网卡，配置自己的IP，而是和一个指定的容器共享IP、端口范围等。同样，两个容器除了网络方面，其他的如文件系统、进程列表等还是隔离的。

![image-20220213123153776](\images\image-20220213123153776.png)

