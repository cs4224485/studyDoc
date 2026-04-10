# 一 基本架构

## 什么是 Prometheus？

Prometheus 是由前 Google 工程师从 2012 年开始在 Soundcloud 以开源软件的形式进行研发的系统监控和告警工具包，自此以后，许多公司和组织都采用了 Prometheus 作为监控告警工具。Prometheus 的开发者和用户社区非常活跃，它现在是一个独立的开源项目，可以独立于任何公司进行维护。为了证明这一点，Prometheus 于 2016 年 5 月加入 CNCF 基金会，成为继 Kubernetes 之后的第二个 CNCF 托管项目。



## Prometheus 的组件

Prometheus 生态系统由多个组件组成，其中有许多组件是可选的：

- [Prometheus Server](https://github.com/prometheus/prometheus) 作为服务端，用来存储时间序列数据。
- [客户端库](https://github.com/yangchuansheng/prometheus-handbook/tree/c6e1e12588ec63c20345090368b37654ef30922a/5-instrumenting/clientlibs.html)用来检测应用程序代码。
- 用于支持临时任务的[推送网关](https://github.com/prometheus/pushgateway)。
- [Exporter](https://github.com/yangchuansheng/prometheus-handbook/tree/c6e1e12588ec63c20345090368b37654ef30922a/5-instrumenting/exporters.html) 用来监控 HAProxy，StatsD，Graphite 等特殊的监控目标，并向 Prometheus 提供标准格式的监控样本数据。
- [alartmanager](https://github.com/prometheus/alertmanager) 用来处理告警。
- 其他各种周边工具。

其中大多数组件都是用 [Go](https://golang.org/) 编写的，因此很容易构建和部署为静态二进制文件。

## Prometheus 的架构

Prometheus 的整体架构以及生态系统组件如下图所示：

![image-20250404104310650](images\image-20250404104310650.png)

## 数据模型

Prometheus 所有采集的监控数据均以指标（metric）的形式保存在内置的时间序列数据库当中（TSDB）：属于同一指标名称，同一标签集合的、有时间戳标记的数据流。除了存储的时间序列，Prometheus 还可以根据查询请求产生临时的、衍生的时间序列作为返回结果。

每一条时间序列由指标名称（Metrics Name）以及一组标签（键值对）唯一标识。其中指标的名称（metric name）可以反映被监控样本的含义（例如，`http_requests_total` — 表示当前系统接收到的 HTTP 请求总量），指标名称只能由 ASCII 字符、数字、下划线以及冒号组成，同时必须匹配正则表达式 `[a-zA-Z_:][a-zA-Z0-9_:]*`。

通过如下表达方式表示指定指标名称和指定标签集合的时间序列：

```
<metric name>{<label name>=<label value>, ...}
```

例如，指标名称为 `api_http_requests_total`，标签为 `method="POST"` 和 `handler="/messages"` 的时间序列可以表示为：

```
api_http_requests_total{method="POST", handler="/messages"}
```

# 二 安装Prometheus 

Prometheus基于Golang编写，编译后的软件包，不依赖于任何的第三方依赖。用户只需要下载对应平台的二进制包，解压并且添加基本的配置即可正常启动Prometheus Server。

## 从二进制包安装

```bash
export VERSION=2.13.0

curl -LO https://github.com/prometheus/prometheus/releases/download/v$VERSION/prometheus-$VERSION.darwin-amd64.tar.gz
```

解压，并将Prometheus相关的命令，添加到系统环境变量路径即可：

```
tar -xzf prometheus-${VERSION}.darwin-amd64.tar.gz
cd prometheus-${VERSION}.darwin-amd64
```

解压后当前目录会包含默认的Prometheus配置文件promethes.yml:

```yml
# my global config
global:
  scrape_interval:     15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      # - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
    - targets: ['localhost:9090']
```

Promtheus作为一个时间序列数据库，其采集的数据会以文件的形似存储在本地中，默认的存储路径为`data/`，因此我们需要先手动创建该目录：

```
mkdir -p data
```

用户也可以通过参数`--storage.tsdb.path="data/"`修改本地数据存储的路径。

启动prometheus服务，其会默认加载当前路径下的prometheus.yaml文件：

```
./prometheus
```

正常的情况下，你可以看到以下输出内容：

```bash
level=info ts=2018-10-23T14:55:14.499484Z caller=main.go:554 msg="Starting TSDB ..."
level=info ts=2018-10-23T14:55:14.499531Z caller=web.go:397 component=web msg="Start listening for connections" address=0.0.0.0:9090
level=info ts=2018-10-23T14:55:14.507999Z caller=main.go:564 msg="TSDB started"
level=info ts=2018-10-23T14:55:14.508068Z caller=main.go:624 msg="Loading configuration file" filename=prometheus.yml
level=info ts=2018-10-23T14:55:14.509509Z caller=main.go:650 msg="Completed loading of configuration file" filename=prometheus.yml
level=info ts=2018-10-23T14:55:14.509537Z caller=main.go:523 msg="Server is ready to 
```

## 使用容器安装

对于Docker用户，直接使用Prometheus的镜像即可启动Prometheus Server：

```
docker run -p 9090:9090 -v /etc/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
```

启动完成后，可以通过[http://localhost:9090](http://localhost:9090/)访问Prometheus的UI界面：

![image-20250405111821583](images\image-20250405111821583.png)

## 使用Node Exporter采集主机运行数据

## 安装Node Exporter

在Prometheus的架构设计中，Prometheus Server并不直接服务监控特定的目标，其主要任务负责数据的收集，存储并且对外提供数据查询支持。因此为了能够能够监控到某些东西，如主机的CPU使用率，我们需要使用到Exporter。Prometheus周期性的从Exporter暴露的HTTP服务地址（通常是/metrics）拉取监控样本数据。

从上面的描述中可以看出Exporter可以是一个相对开放的概念，其可以是一个独立运行的程序独立于监控目标以外，也可以是直接内置在监控目标中。只要能够向Prometheus提供标准格式的监控样本数据即可。

这里为了能够采集到主机的运行指标如CPU, 内存，磁盘等信息。

Node Exporter同样采用Golang编写，并且不存在任何的第三方依赖，只需要下载，解压即可运行。

```bash
curl -OL https://github.com/prometheus/node_exporter/releases/download/v0.17.0/node_exporter-0.17.0.linux-amd64.tar.gz
tar -xzf node_exporter-0.17.0.linux-amd64.tar.gz
cd node_exporter-0.17.0.linux-amd64/
mv node_exporter /usr/local/bin/
```

配置脚本

```bash
cat >> /etc/rc.d/init.d/node_exporter <<EOF
#!/bin/bash
#
# /etc/rc.d/init.d/node_exporter
#
#  Prometheus node exporter
#
#  description: Prometheus node exporter
#  processname: node_exporter

# Source function library.
. /etc/rc.d/init.d/functions

PROGNAME=node_exporter
PROG=/opt/prometheus/$PROGNAME
USER=root
LOGFILE=/var/log/prometheus.log
LOCKFILE=/var/run/$PROGNAME.pid

start() {
    echo -n "Starting $PROGNAME: "
    cd /opt/prometheus/
    daemon --user $USER --pidfile="$LOCKFILE" "$PROG &>$LOGFILE &"
    echo $(pidofproc $PROGNAME) >$LOCKFILE
    echo
}

stop() {
    echo -n "Shutting down $PROGNAME: "
    killproc $PROGNAME
    rm -f $LOCKFILE
    echo
}


case "$1" in
    start)
    start
    ;;
    stop)
    stop
    ;;
    status)
    status $PROGNAME
    ;;
    restart)
    stop
    start
    ;;
    reload)
    echo "Sending SIGHUP to $PROGNAME"
    kill -SIGHUP $(pidofproc $PROGNAME)#!/bin/bash
    ;;
    *)
        echo "Usage: service node_exporter {start|stop|status|reload|restart}"
        exit 1
    ;;
esac
EOF
```

运行node exporter

```bash
service node_exporter start
```

启动成功后，查看端口

```
netstat -anplt|grep 9100
```

访问http://localhost:9100/可以看到以下页面：

![image-20250405113005186](images\image-20250405113005186.png)

每一个监控指标之前都会有一段类似于如下形式的信息：

```
# HELP node_cpu Seconds the cpus spent in each mode.
# TYPE node_cpu counter
node_cpu{cpu="cpu0",mode="idle"} 362812.7890625
# HELP node_load1 1m load average.
# TYPE node_load1 gauge
node_load1 3.0703125
```

其中HELP用于解释当前指标的含义，TYPE则说明当前指标的数据类型。在上面的例子中node_cpu的注释表明当前指标是cpu0上idle进程占用CPU的总时间，CPU占用时间是一个只增不减的度量指标，从类型中也可以看出node_cpu的数据类型是计数器(counter)，与该指标的实际含义一致。又例如node_load1该指标反映了当前主机在最近一分钟以内的负载情况，系统的负载情况会随系统资源的使用而变化，因此node_load1反映的是当前状态，数据可能增加也可能减少，从注释中可以看出当前指标类型为仪表盘(gauge)，与指标反映的实际含义一致。

除了这些以外，在当前页面中根据物理主机系统的不同，你还可能看到如下监控指标：

- node_boot_time：系统启动时间
- node_cpu：系统CPU使用量
- node*disk**：磁盘IO
- node*filesystem**：文件系统用量
- node_load1：系统负载
- node*memeory**：内存使用量
- node*network**：网络带宽
- node_time：当前系统时间
- go_*：node exporter中go相关指标
- process_*：node exporter自身进程相关运行指标

## 从Node Exporter收集监控数据

为了能够让Prometheus Server能够从当前node exporter获取到监控数据，这里需要修改Prometheus配置文件。编辑prometheus.yml并在scrape_configs节点下添加以下内容:

```
scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  # 采集node exporter监控数据
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
```

重新启动Prometheus Server

访问[http://localhost:9090](http://localhost:9090/)，进入到Prometheus Server。如果输入“up”并且点击执行按钮以后，可以看到如下结果：

![image-20250405113711576](images\image-20250405113711576.png)

如果Prometheus能够正常从node exporter获取数据，则会看到以下结果：

```
up{instance="localhost:9090",job="prometheus"}    1
up{instance="localhost:9100",job="node"}    1
```

其中“1”表示正常，反之“0”则为异常。

## 使用PromQL查询监控数据

Prometheus UI是Prometheus内置的一个可视化管理界面，通过Prometheus UI用户能够轻松的了解Prometheus当前的配置，监控任务运行状态等。 通过`Graph`面板，用户还能直接使用`PromQL`实时查询监控数据：

切换到`Graph`面板，用户可以使用PromQL表达式查询特定监控指标的监控数据。如下所示，查询主机负载变化情况，可以使用关键字`node_load1`可以查询出Prometheus采集到的主机负载的样本数据，这些样本数据按照时间先后顺序展示，形成了主机负载随时间变化的趋势图表：

![image-20250405122255028](images\image-20250405122255028.png)

PromQL是Prometheus自定义的一套强大的数据查询语言，除了使用监控指标作为查询关键字以为，还内置了大量的函数，帮助用户进一步对时序数据进行处理。例如使用`rate()`函数，可以计算在单位时间内样本数据的变化情况即增长率，因此通过该函数我们可以近似的通过CPU使用时间计算CPU的利用率：

```
rate(node_cpu[2m])
```

![image-20250405122705316](images\image-20250405122705316.png)

## 使用Grafana创建可视化Dashboard

Prometheus UI提供了快速验证PromQL以及临时可视化支持的能力，而在大多数场景下引入监控系统通常还需要构建可以长期使用的监控数据可视化面板（Dashboard）。这时用户可以考虑使用第三方的可视化工具如Grafana，Grafana是一个开源的可视化平台，并且提供了对Prometheus的完整支持。

```
docker run -d -p 3000:3000 grafana/grafana
```

访问http://localhost:3000就可以进入到Grafana的界面中，默认情况下使用账户admin/admin进行登录。在Grafana首页中显示默认的使用向导，包括：安装、添加数据源、创建Dashboard、邀请成员、以及安装应用和插件等主要流程

这里将添加Prometheus作为默认的数据源，如下图所示，指定数据源类型为Prometheus并且设置Prometheus的访问地址即可，在配置正确的情况下点击“Add”按钮，会提示连接成功的信息：

![image-20250405125314073](images\image-20250405125314073.png)

在完成数据源的添加之后就可以在Grafana中创建我们可视化Dashboard了。Grafana提供了对PromQL的完整支持，如下所示，通过Grafana添加Dashboard并且为该Dashboard添加一个类型为“Graph”的面板。

## 任务和实例

通过在prometheus.yml配置文件中，添加如下配置。我们让Prometheus可以从node exporter暴露的服务中获取监控指标数据。

```yaml
scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
```

当我们需要采集不同的监控指标(例如：主机、MySQL、Nginx)时，我们只需要运行相应的监控采集程序，并且让Prometheus Server知道这些Exporter实例的访问地址。在Prometheus中，每一个暴露监控样本数据的HTTP服务称为一个实例。例如在当前主机上运行的node exporter可以被称为一个实例(Instance)。

而一组用于相同采集目的的实例，或者同一个采集进程的多个副本则通过一个一个任务(Job)进行管理。

```
* job: node
    * instance 2: 1.2.3.4:9100
    * instance 4: 5.6.7.8:9100
```

当前在每一个Job中主要使用了静态配置(static_configs)的方式定义监控目标。除了静态配置每一个Job的采集Instance地址以外，Prometheus还支持与DNS、Consul、E2C、Kubernetes等进行集成实现自动发现Instance实例，并从这些Instance上获取监控数据。

除了通过使用“up”表达式查询当前所有Instance的状态以外，还可以通过Prometheus UI中的Targets页面查看当前所有的监控采集任务，以及各个任务下所有实例的状态:


![image-20250406192301192](images\image-20250406192301192.png)

## 表示方式

数据指标指定了数据指标名称和一组标签，通常使用如下表示方式来标识时间序列：

复制

```
<metric name>{<label name>=<label value>, ...}
```

例如，包含数据指标名称`api_http_requests_total`和标签`method="POST""`，`handler="/messages"`的时间序列可以这样写：

```
api_http_requests_total{method="POST", handler="/messages"}
```

# 三 探索PromQL

探秘Prometheus的自定义查询语言PromQL。通过PromQL用户可以非常方便地对监控样本数据进行统计分析，PromQL支持常见的运算操作符，同时PromQL中还提供了大量的内置函数可以实现对数据的高级处理。当然在学习PromQL之前，用户还需要了解Prometheus的样本数据模型。PromQL作为Prometheus的核心能力除了实现数据的对外查询和展现，同时告警监控也是依赖PromQL实现的。

## 初识PromQL

Prometheus通过指标名称（metrics name）以及对应的一组标签（labelset）唯一定义一条时间序列。指标名称反映了监控样本的基本标识，而label则在这个基本特征上为采集到的数据提供了多种特征维度。用户可以基于这些特征维度过滤，聚合，统计从而产生新的计算后的一条时间序列。

## 查询时间序列

当Prometheus通过Exporter采集到相应的监控指标样本数据后，我们就可以通过PromQL对监控样本数据进行查询。

当我们直接使用监控指标名称查询时，可以查询该指标下的所有时间序列。如：

```
http_requests_total
```

等同于：

```
http_requests_total{}
```

该表达式会返回指标名称为http_requests_total的所有时间序列：

```
http_requests_total{code="200",handler="alerts",instance="localhost:9090",job="prometheus",method="get"}=(20889@1518096812.326)
http_requests_total{code="200",handler="graph",instance="localhost:9090",job="prometheus",method="get"}=(21287@1518096812.326)
```

PromQL还支持用户根据时间序列的标签匹配模式来对时间序列进行过滤，目前主要支持两种匹配模式：完全匹配和正则匹配。

PromQL支持使用`=`和`!=`两种完全匹配模式：

- 通过使用`label=value`可以选择那些标签满足表达式定义的时间序列；
- 反之使用`label!=value`则可以根据标签匹配排除时间序列；

例如，如果我们只需要查询所有http_requests_total时间序列中满足标签instance为localhost:9090的时间序列，则可以使用如下表达式：

```
http_requests_total{instance="localhost:9090"}
```

反之使用`instance!="localhost:9090"`则可以排除这些时间序列：

```
http_requests_total{instance!="localhost:9090"}
```



除了使用完全匹配的方式对时间序列进行过滤以外，PromQL还可以支持使用正则表达式作为匹配条件，多个表达式之间使用`|`进行分离：

- 使用`label=~regx`表示选择那些标签符合正则表达式定义的时间序列；
- 反之使用`label!~regx`进行排除；

例如，如果想查询多个环节下的时间序列序列可以使用如下表达式：

```
http_requests_total{environment=~"staging|testing|development",method!="GET"}
```

## 范围查询



直接通过类似于PromQL表达式`http_requests_total`查询时间序列时，会选择出所有属于该度量指标的时序的当前采样值，这样的返回结果我们称之为__瞬时向量__。而相应的这样的表达式称之为__瞬时向量表达式__。

而如果我们想过去一段时间范围内的样本数据时，我们则需要使用__区间向量表达式__。区间向量表达式和瞬时向量表达式之间的差异在于在区间向量表达式中我们需要定义时间选择的范围，时间范围通过时间范围选择器`[]`进行定义。例如，通过以下表达式可以选择最近5分钟内的所有样本数据：

```
http_requests_total{}[5m]
```

该表达式将会返回查询到的时间序列中最近5分钟的所有样本数据：

```
http_requests_total{code="200",handler="alerts",instance="localhost:9090",job="prometheus",method="get"}=[
    1@1518096812.326
    1@1518096817.326
    1@1518096822.326
    1@1518096827.326
    1@1518096832.326
    1@1518096837.325
]
http_requests_total{code="200",handler="graph",instance="localhost:9090",job="prometheus",method="get"}=[
    4 @1518096812.326
    4@1518096817.326
    4@1518096822.326
    4@1518096827.326
    4@1518096832.326
    4@1518096837.325
]
```

通过区间向量表达式查询到的结果我们称为__区间向量__。

除了使用m表示分钟以外，PromQL的时间范围选择器支持其它时间单位：

- s - 秒

- m - 分钟

- h - 小时

- d - 天

- w - 周

  

  
