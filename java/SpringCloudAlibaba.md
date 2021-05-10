# 一、SpringCloud Alibaba入门简介

## why会出现SpringCloud alibaba

Spring Cloud Netflix项目进入到维护模式

什么是维护模式

![image-20210313112946357](\images\image-20210313112946357.png)

进入维护模式意味着什么

![image-20210313113023380](\images\image-20210313113023380.png)

![image-20210313113038074](\images\image-20210313113038074.png)

## SpringCloud Alibaba的服务介绍

- Nacos: 一个更易于构建云原生应用的动态服务发现, 配置管理和服务管理平台.
- Sentinel: 把流量作为切入点了, 从流量控制, 熔断降级, 系统负载保护等多个维度保护服务的稳定性.
- Seata: 阿里巴巴开源产品, 一个易于使用的高性能微服务分布式事务解决方案.
- RocketMQ: 一款开源的分布式消息系统, 基于高可用分布式集群技术, 提供低延时的, 高可靠的消息发布与订阅服务.
- Alibaba Cloud ACM: 一款在分布式架构环境中对应用配置进行集中管理和推送的应用配置中心产品.
- Alibaba Cloud OSS: 阿里云对象存储服务(Object Storage Service，简称 OSS), 是阿里云提供的海量, 安全, 低成本, 高可靠的云存储服务. 可以在任何应用, 任何时间, 任何地点存储和访问任意类型的数据.
- Alibaba Cloud SchedulerX: 阿里中间件团队开发的一款分布式任务调度产品, 提供秒级, 精准, 高可靠, 高可用的定时(基于 Cron 表达式)任务调度服务.
- Alibaba Cloud SMS: 覆盖全球的短信服务, 友好, 高效, 智能的互联化通讯能力, 帮助企业迅速搭建客户触达通道.

## **SpringCloud Alibaba带来了什么**

1. 2018年, SpringCloud Alibaba正式进入Cloud官方孵化器, 并在Maven中央库发布了第一个版本.
2. 能干什么
   - 服务限流降级: 默认支持Servlet, Feign, RestTemplate, Dubbo和RocketMQ限流降级功能的接入, 可以在运行时通过控制台实时修改限流降级规则, 还支持查看限流降级Metrics监控.
   - 服务注册与发现: 适配SpringCloud服务注册与发现标准, 默认集成了Ribbon的支持.
   - 分布式配置管理: 支持分布式系统中的外部化配置, 配置更改时自动刷新.
   - 消息驱动能力: 基于Spring Cloud Stream为微服务应用构建消息驱动能力.
   - 阿里云对象存储: 云存储服务, 支持在任何应用, 任何时间, 任何地点存储和访问任意类型的数据.
   - 分布式任务调度: 提供秒级, 精准, 高可靠, 高可用的定时任务调度服务. 同时提供分布式的任务执行模型, 如网格任务, 网格任务支持海量子任务均匀分配到所有Worker上执行.

# 二、SpringCloud Alibaba Nacos服务注册和配置中心

## Nacos简介

前四个字母为Nameing和Configuration的前两个字母,最后的s为Service

是一个更易于构建原生应用的动态服务发现、配置管理和服务管理平台，Nacos就是注册中心+配置中心的组合，等价于：Nacos=Eureka+Config+Bus， 替代Eureka做服务注册中心，替代Config做服务配置中心

下载地址：https://github.com/alibaba/Nacos

官方文档：https://nacos.io/zh-cn/       

​				   https://spring-cloud-alibaba-group.github.io/github-pages/greenwich/spring-cloud-alibaba.html#_spring_cloud_alibaba_nacos_discovery

### 各个注册中心对比

![image-20210313113516507](\images\image-20210313113516507.png)

## 安装并运行Nacos

本地Java8+Maven环境已经ok，官网下载Nacos，解压安装包，直接运行bin目录下的startup.cmd，命令运行成功后直接访问http://localhost:8848/nacos。默认用户名密码都是nacos

## 基于Nacos的服务提供者

### 新建**cloudalibaba-provider-payment9001**

#### 父工程pom

```xml
<!--spring cloud alibaba 2.1.0.RELEASE-->
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-alibaba-dependencies</artifactId>
    <version>2.2.0.RELEASE</version>
    <type>pom</type>
    <scope>import</scope>
</dependency>
```

#### pom

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <parent>
        <artifactId>NewSpringCloud</artifactId>
        <groupId>com.harry.springcloud</groupId>
        <version>1.0-SNAPSHOT</version>
    </parent>
    <modelVersion>4.0.0</modelVersion>

    <artifactId>cloudalibaba-provider-payment9001</artifactId>

    <dependencies>
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

#### yml

```yml
server:
  port: 9001

spring:
  application:
    name: nacos-payment-provider
  cloud:
    nacos:
      discovery:
        server-addr: localhost:8848

management:
  endpoints:
    web:
      exposure:
        include: "*"
```

#### 启动类

```java
package com.harry.springcloud;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@SpringBootApplication
@EnableDiscoveryClient
public class PaymentMain9001 {
    public static void main(String[] args) {
        SpringApplication.run(PaymentMain9001.class, args);
    }
}
```

#### Cotroller

```java
@RestController
public class PaymentController {
    @Value("${server.port}")
    private String serverPort;

    @GetMapping("/payment/nacos/{id}")
    public String getPayment(@PathVariable("id")Integer id){
        return "nacos register, serverport=" + serverPort + "\t id:" + id;
    }
}
```

#### 查看注册中心

![image-20210315195603020](\images\image-20210315195603020.png)

为了下一章演示nacos集群，参考9001新建9002

## 基于Nacos的服务消费者

### 新建**cloudalibaba-consumer-nacos-order83**

#### POM

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <parent>
        <artifactId>NewSpringCloud</artifactId>
        <groupId>com.harry.springcloud</groupId>
        <version>1.0-SNAPSHOT</version>
    </parent>
    <modelVersion>4.0.0</modelVersion>

    <artifactId>cloudalibaba-consumer-nacos-order83</artifactId>

    <dependencies>
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
        </dependency>
        <dependency>
            <groupId>com.harry.springcloud</groupId>
            <artifactId>cloud-api-common</artifactId>
            <version>1.0-SNAPSHOT</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

#### yml

```yml
server:
  port: 83

spring:
  application:
    name: nacos-order-consumer
  cloud:
    nacos:
      discovery:
        server-addr: localhost:8848

#消费者将要去访问的微服务名称（注册成功进nacos的微服务提供者）
service-url:
  nacos-user-service: http://nacos-payment-provider
```

#### 启动类

```java
package com.harry.springcloud;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@SpringBootApplication
@EnableDiscoveryClient
public class OrderNacosMain83 {
    public static void main(String[] args) {
        SpringApplication.run(OrderNacosMain83.class, args);
    }
}
```

#### config

```java
@Configuration
public class ApplicationContextConfig {
    @Bean
    @LoadBalanced
    public RestTemplate getRestTemplate(){
        return new RestTemplate();
    }
}
```

#### controller

```java
@RestController
public class OrderNacosController {

    @Autowired
    private RestTemplate restTemplate;

    @Value("${service-url.nacos-user-service}")
    private String serverUrl;

    @GetMapping("/consumer/payment/nacos/{id}")
    public String paymentInfo(@PathVariable("id") Integer id) {
        return restTemplate.getForObject(serverUrl + "/payment/nacos/" + id, String.class);
    }

}
```

#### 测试

http://localhost:83/consumer/payment/nacos/1

## 服务注册中心对比

Nacos和CAP

![image-20210315202431843](\images\image-20210315202431843.png)

![image-20210315202513067](\images\image-20210315202513067.png)

Nacos支持AP和CP模式的切换

![image-20210315202614750](\images\image-20210315202614750.png)

## Nacos作为服务配置中心演示

### Nacos作为配置中心-基础配置cloudalibaba-config-nacos-client3377

#### pom

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <parent>
        <artifactId>NewSpringCloud</artifactId>
        <groupId>com.harry.springcloud</groupId>
        <version>1.0-SNAPSHOT</version>
    </parent>
    <modelVersion>4.0.0</modelVersion>

    <artifactId>cloudalibaba-config-nacos-client3377</artifactId>
    <dependencies>
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
        </dependency>
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

</project>
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <parent>
        <artifactId>NewSpringCloud</artifactId>
        <groupId>com.harry.springcloud</groupId>
        <version>1.0-SNAPSHOT</version>
    </parent>
    <modelVersion>4.0.0</modelVersion>

    <artifactId>cloudalibaba-config-nacos-client3377</artifactId>
    <dependencies>
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
        </dependency>
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

</project>
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <parent>
        <artifactId>NewSpringCloud</artifactId>
        <groupId>com.harry.springcloud</groupId>
        <version>1.0-SNAPSHOT</version>
    </parent>
    <modelVersion>4.0.0</modelVersion>

    <artifactId>cloudalibaba-config-nacos-client3377</artifactId>
    <dependencies>
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
        </dependency>
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

</project>
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <parent>
        <artifactId>NewSpringCloud</artifactId>
        <groupId>com.harry.springcloud</groupId>
        <version>1.0-SNAPSHOT</version>
    </parent>
    <modelVersion>4.0.0</modelVersion>

    <artifactId>cloudalibaba-config-nacos-client3377</artifactId>
    <dependencies>
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
        </dependency>
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

</project>
```

#### bootstrap.yml

```yml
server:
  port: 3377
spring:
  application:
    name: nacos-config-client
  cloud:
    nacos:
      discovery:
        server-addr: localhost:8848 # 注册中心
      config:
        server-addr: localhost:8848 # 配置中心
        file-extension: yaml # 这里指定的文件格式需要和nacos上新建的配置文件后缀相同，否则读不到
#        group: TEST_GROUP #分组
#        namespace: 72fb1ea8-1f06-4daa-a283-bd3311876c3e

#  ${spring.application.name}-${spring.profile.active}.${spring.cloud.nacos.config.file-extension}
# 相当于  nacos-config-client-dev.yaml
```

#### application.yml

```yml
spring:
  profiles:
    active: dev # 开发环境
#    active: test # 测试环境
#    active: info # 开发环境
```

#### controller

```java
package com.harry.springcloud.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RefreshScope//实现配置自动更新
public class ConfigClientController {
    @Value("${config.info}")
    private String configInfo;

    @GetMapping("/config/info")
    public String getConfigInfo() {
        return configInfo;
    }
}
```

#### 在Nacos中添加配置信息

![image-20210315204101026](\images\image-20210315204101026.png)

##### Nacos中的匹配规则

Nacos中的dataid的组成格式及与SpringBoot配置文件中的匹配规则

![image-20210315204131448](\images\image-20210315204131448.png)

##### 设置DataId

公式：${spring.application.name}-${spring.profiles.active}.${spring.cloud.nacos.config.file-extension}

prefix默认为spring.application.name的值

spring.profile.active即为当前环境对应的profile，可以通过

file-exetension为配置内容的数据格式，可以通过配置项speing.cloud.nacos.config.file-extension配置

![image-20210315204248682](\images\image-20210315204248682.png)

http://localhost:3377/config/info

![image-20210315204525351](\images\image-20210315204525351.png)

历史配置：Nacos惠济路配置文件的历史版本默认保留30天，此外还有一件回滚功能

自带动态刷新：修改下Nacos中的yaml配置文件，再次调用查看配置的接口，就会发现配置已经刷新

#### Nacos作为配置中心-分类配置

多环境多项目管理

![image-20210315204843407](\images\image-20210315204843407.png)

##### Nacos的图形化管理界面

配置管理

![image-20210315204937921](\images\image-20210315204937921.png)

命名空间

![image-20210315205006205](\images\image-20210315205006205.png)

Namespace+group+data ID三者关系？为什么这么设计？

![image-20210315205031511](\images\image-20210315205031511.png)

![image-20210315205046066](\images\image-20210315205046066.png)

### 三种方案加载配置

#### DataID方案

指定spring.profile.active和配置文件的DataID来使不同环境下读取不同的配置

默认空间+默认分组+新建dev和test两个DataID

##### 新建dev配置DataID

![image-20210315205240402](\images\image-20210315205240402.png)

##### 新建test配置DataID

![image-20210315205306425](\images\image-20210315205306425.png)

通过spring.profile.acvice属性就能进行多环境下配置文件的读取

![image-20210315205335440](\images\image-20210315205335440.png)

#### Group方案

##### 通过Group实现环境区分

![image-20210315205414407](\images\image-20210315205414407.png)

##### 在nacos图形界面控制台上新建配置文件DataID

![image-20210315205438235](\images\image-20210315205438235.png)

##### bootstrap+application

在config下增加一条group的配置即可。可配置为DEV_GROUP或TEST_GROUP

![image-20210315205521844](\images\image-20210315205521844.png)

#### Namespace方案

##### 新建dev/test的Namespace

![image-20210315205605764](\images\image-20210315205605764.png)

##### 回到服务管理-服务列表查看

![image-20210315205628285](\images\image-20210315205628285.png)

![image-20210315205643946](\images\image-20210315205643946.png)

## Nacos集群和持久化配置(重要)

### 官网说明

https://nacos.io/zh-cn/docs

官网架构图

![image-20210315205828207](\images\image-20210315205828207.png)

上图翻译

![image-20210315205851872](\images\image-20210315205851872.png)

说明

![image-20210315205911664](\images\image-20210315205911664.png)

![image-20210315205935597](\images\image-20210315205935597.png)

### Nacos持久化配置解释

Nacos默认自带的是嵌入式数据库derby

#### derby到mysql切换配置步骤

nacos-server-1.1.4\nacos\conf目录下找到sql脚本， nacos-mysql.sql

nacos-server-1.1.4\nacos\conf目录下找到application.properties

启动Nacos，可以看到是个全新的空记录界面，以前是记录进derby

### Linux版Nacos+MySQL生产环境配置

预计需要，1个nginx+3个nacos注册中心，1个mysql

#### Nacos下载Liunx版

https://github.com/alibaba/nacos/releases

nacos-server-1.1.4.tar.gz

解压后安装

#### 集群配置步骤

##### 1.Linux服务器上mysql数据库配置

###### sql语句源文件,nacos-mysql.sql

```sql
/******************************************/
/*   数据库全名 = nacos_config   */
/*   表名称 = config_info   */
/******************************************/
CREATE TABLE `config_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `data_id` varchar(255) NOT NULL COMMENT 'data_id',
  `group_id` varchar(255) DEFAULT NULL,
  `content` longtext NOT NULL COMMENT 'content',
  `md5` varchar(32) DEFAULT NULL COMMENT 'md5',
  `gmt_create` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间',
  `src_user` text COMMENT 'source user',
  `src_ip` varchar(50) DEFAULT NULL COMMENT 'source ip',
  `app_name` varchar(128) DEFAULT NULL,
  `tenant_id` varchar(128) DEFAULT '' COMMENT '租户字段',
  `c_desc` varchar(256) DEFAULT NULL,
  `c_use` varchar(64) DEFAULT NULL,
  `effect` varchar(64) DEFAULT NULL,
  `type` varchar(64) DEFAULT NULL,
  `c_schema` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_configinfo_datagrouptenant` (`data_id`,`group_id`,`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='config_info';
```



##### 2.application.properties配置

位置

![image-20210315210246949](\images\image-20210315210246949.png)

内容

```properties
#*************** Config Module Related Configurations ***************#
### If use MySQL as datasource:
spring.datasource.platform=mysql
### Count of DB:
db.num=1
### Connect URL of DB:
db.url=jdbc:mysql://192.168.30.129:3306/nacos_config?characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true&useUnicode=true&useSSL=false&serverTimezone=UTC
db.user=root
db.password=123456
### Connection pool configuration: hikariCP
db.pool.config.connectionTimeout=30000
db.pool.config.validationTimeout=10000
db.pool.config.maximumPoolSize=20
db.pool.config.minimumIdle=2
```

![image-20210315210307278](\images\image-20210315210307278.png)

##### 3.Linux服务器上nacos的集群配置cluster.conf

梳理出3台nacos机器的不同服务端口号

复制出cluster.conf

![image-20210315210343352](\images\image-20210315210343352.png)

![image-20210315210402506](\images\image-20210315210402506.png)

这个IP不能写127.0.0.1，必须是Linux命令hostname -i能够识别的IP

![image-20210315210427505](\images\image-20210315210427505.png)

##### 4.编辑Nacos的启动脚本startup.sh,使他能够接受不同的启动端口

/mynacos/nacos/bin 目录下有startup.sh

![image-20210315210516198](\images\image-20210315210516198.png)

修改内容

```SHELL
while getopts ":m:f:s:c:p:P:" opt
do
    case $opt in
        m)
            MODE=$OPTARG;;
        f)
            FUNCTION_MODE=$OPTARG;;
        s)
            SERVER=$OPTARG;;
        c)
            MEMBER_LIST=$OPTARG;;
        p)
            EMBEDDED_STORAGE=$OPTARG;;
        P)
            PORT=$OPTARG;;
        ?)
        echo "Unknown parameter"
        exit 1;;
    esac
done

JAVA ${JAVA_OPT}" > ${BASE_DIR}/logs/start.out 2>&1 &
nohup $JAVA -Dserver.port=${PORT} ${JAVA_OPT} nacos.nacos >> ${BASE_DIR}/logs/start.out 2>&1 &
echo "nacos is starting，you can check the ${BASE_DIR}/logs/start.out"
```

![image-20210315210544262](\images\image-20210315210544262.png)

![image-20210315210555364](\images\image-20210315210555364.png)

![image-20210315210606152](\images\image-20210315210606152.png)

linux JAVA_HOME

```
export JAVA_HOME=/usr/lib/jvm/jre-1.8.0-openjdk-1.8.0.242.b08-0.el7_7.x86_64/
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH
```

执行方式

![image-20210315210623034](\images\image-20210315210623034.png)

##### 5.Nginx的配置，由他作为负载均衡器

修改nginx的配置文件

```bash
[root@MiWiFi-R4AC-srv nginx-1.12.2]#  /usr/local/nginx/sbin/nginx -c /opt/nginx-1.12.2/conf/nginx.conf
```

![image-20210315210700943](\images\image-20210315210700943.png)

![image-20210315210712066](\images\image-20210315210712066.png)

##### 6.截至到此为止，1个nginx+3个nacos注册中心+mysql

测试通过nginx访问nacos

新建一个配置测试

linux服务器的mysql插入一条记录

#### 测试

微服务springalibaba-provider-payment9002启动注册进nacos集群

![image-20210315210821778](\images\image-20210315210821778.png)

![image-20210315210845053](\images\image-20210315210845053.png)

# 三、SpringCloud Alibaba Sentinel实现熔断与限流

## 概述

官网：https://github.com/alibaba/Sentinel

中文：https://github.com/alibaba/Sentinel/wiki/

![image-20210317193109291](\images\image-20210317193109291.png)

一句话解释就是我们之前的hystrix

![image-20210317193410003](\images\image-20210317193410003.png)

## 安装Sentiel控制台

sentinel组件由两部分构成

![image-20210317193449645](\images\image-20210317193449645.png)

### 安装步骤

下载：https://github.com/alibaba/Sentinel/releases

运行命令：java -jar sentinel-dashboard-1.7.0.jar

http://localhost:8080  登录账号密码均为sentinel

## 初始化演示功能

### 创建cloudalibaba-sentinel-service8401

#### pom

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <parent>
        <artifactId>NewSpringCloud</artifactId>
        <groupId>com.harry.springcloud</groupId>
        <version>1.0-SNAPSHOT</version>
    </parent>
    <modelVersion>4.0.0</modelVersion>

    <artifactId>cloudalibaba-sentinel-service8401</artifactId>

    <dependencies>
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
        </dependency>
        <!--        持久化的时候用到jar-->
        <dependency>
            <groupId>com.alibaba.csp</groupId>
            <artifactId>sentinel-datasource-nacos</artifactId>
        </dependency>
        <dependency>
            <groupId>com.harry.springcloud</groupId>
            <artifactId>cloud-api-common</artifactId>
            <version>1.0-SNAPSHOT</version>
        </dependency>

        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-sentinel</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-openfeign</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

#### YML

```yml
server:
  port: 8401
spring:
  application:
    name: cloud-alibaba-sentinel-service
  cloud:
    nacos:
      discovery:
        #        Nacos服务注册中心地址
        server-addr: localhost:8848
    sentinel:
      transport:
        #        配置sentinel dashboard 地址
        dashboard: localhost:8080
        #        默认8719端口，假如被占用会自动从8719开始依次+1扫描，直至找到未被占用的端口
        port: 8719
        #配置sentinel持久化
      datasource:
        ds1:
          nacos:
            server-addr: localhost:8848
            dataId: cloud-alibaba-sentinel-service
            groupId: DEFAULT_GROUP
            data-type: json
            rule-type: flow

management:
  endpoints:
    web:
      exposure:
        include: '*'

feign:
  sentinel:
    enabled: true
```

#### 启动类

```java
@SpringBootApplication
@EnableDiscoveryClient
public class SentinelServiceMain8401 {
    public static void main(String[] args) {
        SpringApplication.run(SentinelServiceMain8401.class,args);
    }
}
```

#### 业务类FlowLimitController

```java
@RestController
@Slf4j
public class FlowLimitController {

    @GetMapping("/testA")
    public String testA() {
        return "----------------testA";
    }

    @GetMapping("/testB")
    public String testB() {
        return "----------------testB";
    }

    @GetMapping("/testD")
    public String testD() throws InterruptedException {
        TimeUnit.SECONDS.sleep(1);
       log.info("test 测试RT");
        return "----------------testD";
    }

    @GetMapping("/testE")
    public String testE() {
        log.info("test 测试异常比例");
        int i = 10/0;
        return "----------------testE  测试异常比例";
    }

    @GetMapping("/testF")
    public String testF() {
        log.info("test 测试异常数");
        int i = 10/0;
        return "----------------testF  测试异常数";
    }

    @GetMapping("/testHotKey")
    @SentinelResource(value = "testHotKey",blockHandler = "deal_testHotKey")
    public String testHotKey(@RequestParam(value = "p1",required = false) String p1,
                             @RequestParam(value = "p2",required = false) String p2) {
        return "----------------testHotKey";
    }
    public String deal_testHotKey(String p1, String p2, BlockException exception) {
        return "----------------deal_testHotKey/(ㄒoㄒ)/~~";
    }
}
```

启动8401微服务后台查看sentinel控制台，空空如也，啥也没有

Sentinel采用懒加载说明 执行一次访问 http://localhost:8401/testA    http://localhost:8401/testB

![image-20210320121929878](\images\image-20210320121929878.png)

## 流控规则

### 基本介绍

![image-20210321093633892](\images\image-20210321093633892.png)

![image-20210321093713784](\images\image-20210321093713784.png)

### 流控模式

#### 直接(默认)

配置及说明

![image-20210321093915375](\images\image-20210321093915375.png)

测试

快速点击访问http://localhost:8401/testA

结果 Blocked by Sentinel(flow limiting)

#### 关联

当关联的资源达到阈值时，就限流自己，当与A关联的资源B达到阈值后，就限流自己，B惹事，A挂了。

配置A

![image-20210321094236987](\images\image-20210321094236987.png)

postman模拟并发密集访问testB

访问B成功

![image-20210321094502906](\images\image-20210321094502906.png)

postman里新建多线程集合组

![image-20210321094621546](\images\image-20210321094621546.png)

大批量线程高并发访问B，导致A失效了

![image-20210321094734681](\images\image-20210321094734681.png)

运行后发现testA挂了

### 流控效果

直接->快速失败(默认的流控处理)

直接失败，抛出异常 ----> Blocked by Sentinel(flow limiting

源码：com.alibaba.csp.sentinel.slots.block.controller.DefaultControlle

#### 预热

公式:阈值除以coldFactor(默认值为3)，经过预热时长后才会达到阈值

![image-20210321095133703](\images\image-20210321095133703.png)

默认coldFactor为3，即请求QPS从threshold/3开始，经预热时长逐渐升至设定的QPS阈值

限流 冷启动：https://github.com/alibaba/Sentinel/wiki/%E9%99%90%E6%B5%81---%E5%86%B7%E5%90%AF%E5%8A%A8

#### WarmUp配置

![image-20210321095530658](\images\image-20210321095530658.png)

多次点击http://localhost:8401/testB 刚开始不行，后续慢慢OK

应用场景：秒杀系统在开启瞬间，会有很多流量上来，很可能把系统打死，预热方式就是为了保护系统，可慢慢的把流量放进来，慢慢的把阈值增长到设置的阈值。

### 排队等待

匀速排队，阈值必须设置为QPS

![image-20210321095642705](\images\image-20210321095642705.png)

源码:com.ailibaba.csp.sentinel.slots.block.controller.RateLimiterController

测试

![image-20210321100027668](\images\image-20210321100027668.png)

## 降级规则

官网:https://github.com/alibaba/Sentinel/wiki/%E7%86%94%E6%96%AD%E9%99%8D%E7%BA%A7

### 基本介绍

![image-20210321100428324](\images\image-20210321100428324.png)

QPS >=5且比例(秒级统计)超过阈值时，触发降级，时间窗口结束后，关闭降级

Sentinel的断路器是没有半开状态的,半开的状态系统自动去检测是否请求有异常，没有异常就关闭断路器恢复使用，有异常则继续打开断路器不可用，具体参考Hystrix

### 降级策略实战

#### RT

![image-20210321100538625](\images\image-20210321100538625.png)

测试

```java
@GetMapping("/testD")
public String testD() throws InterruptedException {
    TimeUnit.SECONDS.sleep(1);
    log.info("test 测试RT");
    return "----------------testD";
}
```

配置

![image-20210321100656068](\images\image-20210321100656068.png)

![image-20210321100713465](\images\image-20210321100713465.png)

后续停止了压力测试，断路器关闭微服务恢复正常

#### 异常比例

![image-20210321100856842](\images\image-20210321100856842.png)

![image-20210321100907599](\images\image-20210321100907599.png)

#### 测试

```java
@GetMapping("/testE")
public String testE() {
    log.info("test 测试异常比例");
    int i = 10/0;
    return "----------------testE  测试异常比例";
}
```

配置

![image-20210321102111807](\images\image-20210321102111807.png)

![image-20210321102136997](images\image-20210321102136997.png)

#### 异常数

![image-20210321102326563](\images\image-20210321102326563.png)

![image-20210321102338630](\images\image-20210321102338630.png)

测试

![image-20210321102409498](\images\image-20210321102409498.png)

## 热点key限流

### 基本介绍

![image-20210321102532905](\images\image-20210321102532905.png)

官网：https://github.com/alibaba/Sentinel/wiki/%E7%83%AD%E7%82%B9%E5%8F%82%E6%95%B0%E9%99%90%E6%B5%81

### 承上启下复习start  SentinelResource

![image-20210321102653538](\images\image-20210321102653538.png)

### 配置

![image-20210321102909163](\images\image-20210321102909163.png)

![image-20210321102936928](\images\image-20210321102936928.png)

SentinelResource(value = "testHotKey")，异常打到了前台用户界面看到，不友好

@SentinelResource(value = "testHotKey",blockHandler="dealHandler_testHotKey")，方法testHotKey里面第一个参数只要QPS超过每秒一次，马上降级处理

```java
@GetMapping("/testHotKey")
@SentinelResource(value = "testHotKey",blockHandler = "deal_testHotKey")
public String testHotKey(@RequestParam(value = "p1",required = false) String p1,
                         @RequestParam(value = "p2",required = false) String p2) {
    return "----------------testHotKey";
}
public String deal_testHotKey(String p1, String p2, BlockException exception) {
    return "----------------deal_testHotKey/(ㄒoㄒ)/~~";
}
```

### 测试

http://localhost:8401/testHotKey?p1=abc  error

http://localhost:8401/testHotKey?p1=abc&p2=33   error

http://localhost:8401/testHotKey?p2=abc  right

### 参数例外项

上述案例演示了第一个参数p1，当QPS超过1秒1次点击后马上被限流

特殊情况：超过1秒钟一个后，达到阈值1后马上被限流， 我们期望p1参数当它是某个特殊值时，它的限流值和平时不一样，假如当p1的值等于5时，它的阈值可以达到200

![image-20210321104339883](\images\image-20210321104339883.png)

当p1等于5的时候，阈值变为200

当p1不等于5的时候，阈值就是平常的1

前提条件：热点参数的注意点，参数必须是基本类型或者String

![image-20210321104915736](\images\image-20210321104915736.png)

## 系统规则

https://github.com/alibaba/Sentinel/wiki/系统自适应限流

各项配置说明

![image-20210321105005452](\images\image-20210321105005452.png)

配置全局QPS

![image-20210321105115316](\images\image-20210321105115316.png)

不合适,使用危险,一竹竿打死一船人

## @SentinelResource

### 按资源名称限流+后续处理

#### 业务类RateLimitController

```java
@RestController
public class RateLimitController {

    @GetMapping("/byResource")
    @SentinelResource(value = "byResource", blockHandler = "handlerException")
    public CommonResult byResource(){
        return new CommonResult(200, "按资源名称限流OK", new Payment(2020L, "seria1001"));
    }
    public CommonResult handlerException(BlockException exception){
        return new CommonResult(444,exception.getClass().getCanonicalName()+"\t 服务不可用");
    }

    @GetMapping("/rateLimit/byUrl")
    @SentinelResource(value = "byUrl")
    public CommonResult byUrl(){
        return new CommonResult(200,"按Url限流OK",new Payment(2020L,"serial001"));
    }

    @GetMapping("/rateLimit/customerBlockHandler")
    @SentinelResource(value = "customerBlockHandler",blockHandlerClass = CustomerBlockHandler.class,blockHandler = "handlerException2")
    public CommonResult customerBlockHandler(){
        return new CommonResult(200,"按客户自定义",new Payment(2020L,"serial001"));
    }
}
```

#### 配置流控规则

![image-20210321105619850](\images\image-20210321105619850.png)

表示1秒钟内查询次数大于1，就跑到我们自定义的限流处，限流

测试1秒钟点击1下，OK，超过上述，疯狂点击，返回了自己定义的限流处理信息，限流发生

### 按照Url地址限流+后续处理

通过访问URL来限流，会返回Sentinel自带默认的限流处理信息

Sentinel控制台配置

![image-20210321110037186](\images\image-20210321110037186.png)

疯狂点击http://localhost:8401/rateLimit/byUrl

![image-20210321110100467](\images\image-20210321110100467.png)

### 上面兜底方案面临的问题

![image-20210321111043521](\images\image-20210321111043521.png)

### 客户自定义限流处理逻辑

创建CustomerBlockHandler类用于自定义限流处理逻辑

自定义限流处理类：CustomerBlockHandler

```java
public class CustomerBlockHandler {
    public static CommonResult handlerException(BlockException exception){
        return new CommonResult(4444,"按客户自定义exception-------1");
    }
    public static CommonResult handlerException2(BlockException exception){
        return new CommonResult(4444,"按客户自定义exception-------2");
    }
}
```

RateLimitController

```java
@GetMapping("/rateLimit/customerBlockHandler")
@SentinelResource(value = "customerBlockHandler",blockHandlerClass = CustomerBlockHandler.class,blockHandler = "handlerException2")
public CommonResult customerBlockHandler(){
    return new CommonResult(200,"按客户自定义",new Payment(2020L,"serial001"));
}
```

启动微服务后再调用一次 http://localhost:8401/rateLimit/customerBlockHandler

Sentinel控制台配置

![image-20210321111322432](\images\image-20210321111322432.png)

![image-20210321111302300](\images\image-20210321111302300.png)

进一步说明图

![image-20210321111354327](\images\image-20210321111354327.png)

### 更多注解说明

https://github.com/alibaba/Sentinel/wiki/%E6%B3%A8%E8%A7%A3%E6%94%AF%E6%8C%81

## 服务熔断功能

sentinel整合ribbon+openFeign+fallback

### Ribbon系列

#### 新建cloudalibaba-consumer-nacos-order84

##### Pom

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <parent>
        <artifactId>NewSpringCloud</artifactId>
        <groupId>com.harry.springcloud</groupId>
        <version>1.0-SNAPSHOT</version>
    </parent>
    <modelVersion>4.0.0</modelVersion>

    <artifactId>cloudalibaba-consumer-nacos-order84</artifactId>

    <dependencies>
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
        </dependency>
        <!--        持久化的时候用到jar-->
        <dependency>
            <groupId>com.alibaba.csp</groupId>
            <artifactId>sentinel-datasource-nacos</artifactId>
        </dependency>
        <dependency>
            <groupId>com.harry.springcloud</groupId>
            <artifactId>cloud-api-common</artifactId>
            <version>1.0-SNAPSHOT</version>
        </dependency>
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-sentinel</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-openfeign</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

##### yml

```yml
server:
  port: 84

spring:
  application:
    name: nacos-order-consumer
  cloud:
    nacos:
      discovery:
        #        Nacos服务注册中心地址
        server-addr: localhost:8848
    sentinel:
      transport:
        #        配置sentinel dashboard 地址
        dashboard: localhost:8080
        #        默认8719端口，假如被占用会自动从8719开始依次+1扫描，直至找到未被占用的端口
        port: 8719

#消费者将要去访问的微服务名称（注册成功进nacos的微服务提供者）
service-url:
  nacos-user-service: http://nacos-payment-provider
```

##### controller

```java
@RestController
public class CircleBreakerController {
    public static final String SERVICE_URL = "http://nacos-payment-provider";

    @Autowired
    private RestTemplate restTemplate;

    @RequestMapping("/consumer/fallback/{id}")
    //@SentinelResource(value = "fallback")//没有配置
    //@SentinelResource(value = "fallback",fallback = "handlerFallback")//fallback只负责业务异常  handlerFallback()
    //@SentinelResource(value = "fallback",blockHandler = "blockHandler")//blockHandler只负责sentinel控制台配置违规
    //@SentinelResource(value = "fallback",fallback = "handlerFallback",blockHandler = "blockHandler")
    @SentinelResource(value = "fallback",fallback = "handlerFallback",blockHandler = "blockHandler",
            exceptionsToIgnore = {IllegalArgumentException.class})//exceptionsToIgnore 忽略错误类,如果报此异常没有降级效果
    public CommonResult<Payment> fallback(@PathVariable Long id){
        CommonResult result = restTemplate.getForObject(SERVICE_URL + "/paymentSQL/" + id, CommonResult.class, id);
        if(id==4){
            throw new IllegalArgumentException("IllegalArgumentException 非法参数异常");
        }else if (result.getData()==null){
            throw new NullPointerException("NullPointerException, 该ID，没有对应记录，空指针异常");
        }
        return result;
    }

    //本例fallback
    public CommonResult handlerFallback(@PathVariable Long id,Throwable throwable)  {
        Payment payment = new Payment(id, "null");
        return new CommonResult<>(444,"兜底异常handlerFallback"+throwable.getMessage(),payment);
    }

    //本例blockHandler
    public CommonResult blockHandler(@PathVariable Long id, BlockException throwable)  {
        Payment payment = new Payment(id, "null");
        return new CommonResult<>(445,"blockHandler------sentinel限流"+throwable.getMessage(),payment);
    }



}
```

##### config

```java
@Configuration
public class ApplicationContextConfig {

    @Bean
    @LoadBalanced
    public RestTemplate getRestTemplate(){
        return new RestTemplate();
    }
}
```

#### 创建9003 9004

```java
@RestController
public class PaymentController {
    @Value("${server.port}")
    private String serverPort;

    public static HashMap<Long, Payment> hashMap = new HashMap<>();
    static {
        hashMap.put(1L,new Payment(1L,"111111111111111"));
        hashMap.put(2L,new Payment(2L,"222222222222222"));
        hashMap.put(3L,new Payment(3L,"333333333333333"));
    }

    @GetMapping("/paymentSQL/{id}")
    public CommonResult<Payment> paymentSQL(@PathVariable(value = "id") Long id){
        Payment payment = hashMap.get(id);
        CommonResult<Payment> result = new CommonResult<>(200, "from mysql ,serverPort：" + serverPort, payment);
        return result;
    }
}
```

### Feign系列

#### 启动类

```java
@SpringBootApplication
@EnableDiscoveryClient
@EnableFeignClients
public class OrderNacosMain84 {
    public static void main(String[] args) {
        SpringApplication.run(OrderNacosMain84.class,args);
    }
}
```

#### yml

```yml
server:
  port: 84

spring:
  application:
    name: nacos-order-consumer
  cloud:
    nacos:
      discovery:
        #        Nacos服务注册中心地址
        server-addr: localhost:8848
    sentinel:
      transport:
        #        配置sentinel dashboard 地址
        dashboard: localhost:8080
        #        默认8719端口，假如被占用会自动从8719开始依次+1扫描，直至找到未被占用的端口
        port: 8719

#消费者将要去访问的微服务名称（注册成功进nacos的微服务提供者）
service-url:
  nacos-user-service: http://nacos-payment-provider


# 激活sentinel对feigh的支持
feign:
  sentinel:
    enabled: true
```

#### service

```java
@FeignClient(value = "nacos-payment-provider", fallback = PaymentServiceImpl.class)
public interface PaymentService {
    @GetMapping("/paymentSQL/{id}")
    public CommonResult<Payment> paymentSQL(@PathVariable("id") Long  id);
}
```

```java
@Component
public class PaymentServiceImpl implements PaymentService {
    @Override
    public CommonResult<Payment> paymentSQL(Long id) {
        return new CommonResult<>(4444444, "服务降级返回", new Payment(id, "errorSerial"));
    }
}
```

controller

```java
package com.harry.spring.cloud.controller;

import com.alibaba.csp.sentinel.annotation.SentinelResource;
import com.alibaba.csp.sentinel.slots.block.BlockException;
import com.harry.spring.cloud.service.PaymentService;
import com.harry.springcloud.entities.CommonResult;
import com.harry.springcloud.entities.Payment;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@RestController
public class CircleBreakerController {
    public static final String SERVICE_URL = "http://nacos-payment-provider";

    @Autowired
    private RestTemplate restTemplate;

    @RequestMapping("/consumer/fallback/{id}")
    //@SentinelResource(value = "fallback")//没有配置
    //@SentinelResource(value = "fallback",fallback = "handlerFallback")//fallback只负责业务异常  handlerFallback()
    //@SentinelResource(value = "fallback",blockHandler = "blockHandler")//blockHandler只负责sentinel控制台配置违规
    //@SentinelResource(value = "fallback",fallback = "handlerFallback",blockHandler = "blockHandler")
    @SentinelResource(value = "fallback",fallback = "handlerFallback",blockHandler = "blockHandler",
            exceptionsToIgnore = {IllegalArgumentException.class})//exceptionsToIgnore 忽略错误类,如果报此异常没有降级效果
    public CommonResult<Payment> fallback(@PathVariable Long id){
        CommonResult result = restTemplate.getForObject(SERVICE_URL + "/paymentSQL/" + id, CommonResult.class, id);
        if(id==4){
            throw new IllegalArgumentException("IllegalArgumentException 非法参数异常");
        }else if (result.getData()==null){
            throw new NullPointerException("NullPointerException, 该ID，没有对应记录，空指针异常");
        }
        return result;
    }

    //本例fallback
    public CommonResult handlerFallback(@PathVariable Long id,Throwable throwable)  {
        Payment payment = new Payment(id, "null");
        return new CommonResult<>(444,"兜底异常handlerFallback"+throwable.getMessage(),payment);
    }

    //本例blockHandler
    public CommonResult blockHandler(@PathVariable Long id, BlockException throwable)  {
        Payment payment = new Payment(id, "null");
        return new CommonResult<>(445,"blockHandler------sentinel限流"+throwable.getMessage(),payment);
    }

    //OpenFeigh

    @Autowired
    private PaymentService paymentService;

    @GetMapping("/consumer/paymentSQL/{id}")
    public CommonResult<Payment> paymentSQL(@PathVariable Long  id){
        return paymentService.paymentSQL(id);
    }


}
```

## 规则持久化

一旦我们重启应用,sentinel规则消失,生产环境需要将配置规则进行持久化

将限流规则持久进Nacos保存,只要刷新8401某个rest地址,sentinel控制台的流控规则就能看得到,只要Nacos里面的配置不删除,针对8401上的流控规则持续有效

### 步骤

修改cloudalibaba-sentinel-server8401

#### POM

```xml
<!--     sentinel-datasource-nacos 后续持久化用   -->
<dependency>
    <groupId>com.alibaba.csp</groupId>
    <artifactId>sentinel-datasource-nacos</artifactId>
</dependency>
```

#### YML

添加Nacos数据源配置

```yml
server:
  port: 8401
spring:
  application:
    name: cloud-alibaba-sentinel-service
  cloud:
    nacos:
      discovery:
        #        Nacos服务注册中心地址
        server-addr: localhost:8848
    sentinel:
      transport:
        #        配置sentinel dashboard 地址
        dashboard: localhost:8080
        #        默认8719端口，假如被占用会自动从8719开始依次+1扫描，直至找到未被占用的端口
        port: 8719
        #配置sentinel持久化
      datasource:
        ds1:
          nacos:
            server-addr: localhost:8848
            dataId: cloud-alibaba-sentinel-service
            groupId: DEFAULT_GROUP
            data-type: json
            rule-type: flow

management:
  endpoints:
    web:
      exposure:
        include: '*'

feign:
  sentinel:
    enabled: true
```

#### 添加Nacos业务规则配置

![image-20210323211827728](\images\image-20210323211827728.png)

内容解析

```json
[
   {
      "resource": "/rateLimit/byUrl",
      "limitApp": "default",
      "grade":1,
      "count":1,
      "strategy":0,
      "controlBehaabior":0,
      "clusterMode":false
   }
]
```

![image-20210323211912090](\images\image-20210323211912090.png)

#### 启动8401刷新sentinel发现业务规则变了

![image-20210323211949985](\images\image-20210323211949985.png)

#### 快速访问测试接口

http://localhost:8401/rateLimit/byUrl

#### 停止8401再看sentinel

![image-20210323212028249](\images\image-20210323212028249.png)

#### 重新启动8401再看sentinel

多次调用http://localhost:8401/rateLimit/byUrl

重新配置出现了,持久化验证通过

# 四、SpringCloud Alibaba Seata处理分布式事务

## 分布式事务问题

### 分布式之后

![image-20210329193758204](\images\image-20210329193758204.png)

![image-20210329193810575](\images\image-20210329193810575.png)

一次业务操作需要垮多个数据源或需要垮多个系统进行远程调用,就会产生分布式事务问题

### Seata简介

Seata是一款开源的分布式事务解决方案,致力于在微服务架构下提供高性能和简单易用的分布式事务服务

官网地址：http://seata.io/zh-cn/

一个典型的分布式事务过程

分布式事务处理过程-ID+三组件模型

![image-20210329193922693](\images\image-20210329193922693.png)

![image-20210329193937681](\images\image-20210329193937681.png)

### 三组件概念

Transaction Coordinator(TC)：事务协调器,维护全局事务的运行状态,负责协调并驱动全局事务的提交或回滚

Transaction Manager(TM)：控制全局事务的边界,负责开启一个全局事务,并最终发起全局提交或全局回滚的决议

Resource Manager(RM）：控制分支事务,负责分支注册、状态汇报,并接受事务协调的指令,驱动分支(本地)事务的提交和回滚

发布说明: https://github.com/seata/seata/releases

### 怎么用

本地@Transational

全局@GlobalTranstional

seata的分布式交易解决方案

![image-20210329194203518](\images\image-20210329194203518.png)

## Seata-Server安装

### 官网地址

https://seata.io/zh-cn/

### seata-server-0.9.0.zip解压到指定目录并修改conf目录下的file.conf配置文件

先备份原始file.conf文件

主要修改:自定义事务组名称+事务日志存储模式为db+数据库连接

service模块

![image-20210329194410083](\images\image-20210329194410083.png)

store模块

![image-20210329194432849](\images\image-20210329194432849.png)

![image-20210329194450346](\images\image-20210329194450346.png)

### mysql5.7数据库新建库seata

建表db_store.sql在seata-server-0.9.0\seata\conf目录里面 db_store.sql

```sql
-- the table to store GlobalSession data
drop table if exists `global_table`;
create table `global_table` (
  `xid` varchar(128)  not null,
  `transaction_id` bigint,
  `status` tinyint not null,
  `application_id` varchar(32),
  `transaction_service_group` varchar(32),
  `transaction_name` varchar(128),
  `timeout` int,
  `begin_time` bigint,
  `application_data` varchar(2000),
  `gmt_create` datetime,
  `gmt_modified` datetime,
  primary key (`xid`),
  key `idx_gmt_modified_status` (`gmt_modified`, `status`),
  key `idx_transaction_id` (`transaction_id`)
);

-- the table to store BranchSession data
drop table if exists `branch_table`;
create table `branch_table` (
  `branch_id` bigint not null,
  `xid` varchar(128) not null,
  `transaction_id` bigint ,
  `resource_group_id` varchar(32),
  `resource_id` varchar(256) ,
  `lock_key` varchar(128) ,
  `branch_type` varchar(8) ,
  `status` tinyint,
  `client_id` varchar(64),
  `application_data` varchar(2000),
  `gmt_create` datetime,
  `gmt_modified` datetime,
  primary key (`branch_id`),
  key `idx_xid` (`xid`)
);

-- the table to store lock data
drop table if exists `lock_table`;
create table `lock_table` (
  `row_key` varchar(128) not null,
  `xid` varchar(96),
  `transaction_id` long ,
  `branch_id` long,
  `resource_id` varchar(256) ,
  `table_name` varchar(32) ,
  `pk` varchar(36) ,
  `gmt_create` datetime ,
  `gmt_modified` datetime,
  primary key(`row_key`)
);
```

### 在seata库里新建表

### 修改seata-server-0.9.0\seata\conf目录下的registry.conf目录下的registry.conf配置文件

![image-20210329195410467](\images\image-20210329195410467.png)

### 先启动Nacos端口号8848

### 再启动seata-server

seata-server-0.9.0\seata\bin

seata-server.bat

## 订单/库存/账户业务数据库准备

以下演示都需要先启动Nacos后启动Seata,保证两个都OK 

### 分布式事务业务说明

![image-20210401203202607](\images\image-20210401203202607.png)

### 创建业务数据库

seata_order:存储订单的数据库

seata_storage:存储库存的数据库

seata_account:存储账户信息的数据库

```sql
create database seata_order;
create database seata_storage;
create database seata_account;
```

### 按照上述3库分别建立对应业务表

seata_order库下新建t_order表

```sql
DROP TABLE IF EXISTS `t_order`;
CREATE TABLE `t_order`  (
  `int` bigint(11) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) DEFAULT NULL COMMENT '用户id',
  `product_id` bigint(11) DEFAULT NULL COMMENT '产品id',
  `count` int(11) DEFAULT NULL COMMENT '数量',
  `money` decimal(11, 0) DEFAULT NULL COMMENT '金额',
  `status` int(1) DEFAULT NULL COMMENT '订单状态:  0:创建中 1:已完结',
  PRIMARY KEY (`int`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '订单表' ROW_FORMAT = Dynamic;
```

seata_storage库下新建t_storage表

```sql
DROP TABLE IF EXISTS `t_storage`;
CREATE TABLE `t_storage`  (
  `int` bigint(11) NOT NULL AUTO_INCREMENT,
  `product_id` bigint(11) DEFAULT NULL COMMENT '产品id',
  `total` int(11) DEFAULT NULL COMMENT '总库存',
  `used` int(11) DEFAULT NULL COMMENT '已用库存',
  `residue` int(11) DEFAULT NULL COMMENT '剩余库存',
  PRIMARY KEY (`int`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '库存' ROW_FORMAT = Dynamic;
INSERT INTO `t_storage` VALUES (1, 1, 100, 0, 100);
```

seata_account库下新建t_account表

```sql
CREATE TABLE `t_account`  (
  `id` bigint(11) NOT NULL COMMENT 'id',
  `user_id` bigint(11) DEFAULT NULL COMMENT '用户id',
  `total` decimal(10, 0) DEFAULT NULL COMMENT '总额度',
  `used` decimal(10, 0) DEFAULT NULL COMMENT '已用余额',
  `residue` decimal(10, 0) DEFAULT NULL COMMENT '剩余可用额度',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '账户表' ROW_FORMAT = Dynamic;

INSERT INTO `t_account` VALUES (1, 1, 1000, 0, 1000);
```

### 按照上述3库分别建立对应的回滚日志表

订单-库存-账户3个库下都需要建各自独立的回滚日志表

seata-server-0.9.0\seata\conf\目录下的db_undo_log.sql

```sql
CREATE TABLE `undo_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `branch_id` bigint(20) NOT NULL,
  `xid` varchar(100) NOT NULL,
  `context` varchar(128) NOT NULL,
  `rollback_info` longblob NOT NULL,
  `log_status` int(11) NOT NULL,
  `log_created` datetime NOT NULL,
  `log_modified` datetime NOT NULL,
  `ext` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ux_undo_log` (`xid`,`branch_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
```

![image-20210401203700215](\images\image-20210401203700215.png)

## 订单/库存/账户业务微服务准备

### 新建订单Order-Module seata-order-service2001

#### POM

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <parent>
        <artifactId>NewSpringCloud</artifactId>
        <groupId>com.harry.springcloud</groupId>
        <version>1.0-SNAPSHOT</version>
    </parent>
    <modelVersion>4.0.0</modelVersion>

    <artifactId>seata-order-service2001</artifactId>
    <dependencies>
        <!-- nacos -->
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
        </dependency>
        <!-- nacos -->

        <!-- seata-->
        <dependency>
            <groupId>com.alibaba.cloud</groupId>
            <artifactId>spring-cloud-starter-alibaba-seata</artifactId>
            <exclusions>
                <exclusion>
                    <groupId>io.seata</groupId>
                    <artifactId>seata-all</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
        <dependency>
            <groupId>io.seata</groupId>
            <artifactId>seata-all</artifactId>
            <version>0.9.0</version>
        </dependency>
        <!-- seata-->
        <!--feign-->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-openfeign</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.mybatis.spring.boot</groupId>
            <artifactId>mybatis-spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>druid-spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
        </dependency>
        <!--jdbc-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-jdbc</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

</project>
```

#### YML

```yml
server:
  port: 2001

spring:
  application:
    name: seata-order-service
  cloud:
    alibaba:
      seata:
        # 自定义事务组名称需要与seata-server中的对应
        tx-service-group: fsp_tx_group
    nacos:
      discovery:
        server-addr: localhost:8848
  datasource:
    # 当前数据源操作类型
    type: com.alibaba.druid.pool.DruidDataSource
    # mysql驱动类
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://localhost:3306/seata_order?useUnicode=true&characterEncoding=UTF-8&useSSL=false&serverTimezone=GMT%2B8
    username: root
    password: 123456
feign:
  hystrix:
    enabled: false
logging:
  level:
    io:
      seata: info

mybatis:
  mapper-locations: classpath:mapper/*.xml
 
```

#### file.conf

拷贝seata-server/conf目录下的file.conf

![image-20210401205209465](\images\image-20210401205209465.png)

#### registry.conf

拷贝seata-server/conf目录下的registry.conf

#### domain

Order

```java
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Order {

    private Long id;
    private Long userId;
    private long productId;
    private Integer count;
    private BigDecimal money;
    private Integer status;
}
```

CommonResult

```java
package com.harry.springcloud.domain;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class CommonResult<T> {

    private Integer code;
    private String message;
    private T data;

    public CommonResult(Integer code, String message) {
        this(code, message, null);
    }
}
```

#### Dao接口实现

orderDao

```java
package com.harry.springcloud.dao;

import com.harry.springcloud.domain.Order;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

@Mapper
public interface OrderDao {

    //1 新建订单
    void create(Order order);

    //2 修改订单状态
    void update(@Param("userId") Long userId, @Param("status") Integer status);

}
```

mapper

resources文件夹下新建mapper文件夹后添加

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.harry.springcloud.dao.OrderDao">
    <resultMap id="BaseResultMap" type="com.harry.springcloud.domain.Order">
        <id column="id" property="id" jdbcType="BIGINT"></id>
        <result column="user_id" property="userId" jdbcType="BIGINT"></result>
        <result column="product_id" property="productId" jdbcType="BIGINT"></result>
        <result column="count" property="count" jdbcType="INTEGER"></result>
        <result column="money" property="money" jdbcType="DECIMAL"></result>
        <result column="status" property="status" jdbcType="INTEGER"></result>
    </resultMap>

    <insert id="create" parameterType="com.harry.springcloud.domain.Order">
        insert into t_order(id,user_id,product_id,count,money,status) values (null,#{userId},#{productId},#{count},#{money},0);
    </insert>

    <update id="update">
        update t_order set status =1 where user_id =#{userId} and status=#{status};
    </update>
</mapper>
```

#### Service接口及实现

AccountService

```java
package com.harry.springcloud.service;

import com.harry.springcloud.domain.CommonResult;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.math.BigDecimal;

@FeignClient(value = "seata-account-service")
public interface AccountService {
    @PostMapping(value = "account/decrease")
    CommonResult decrease(@RequestParam("userId") Long userId,
                          @RequestParam("money") BigDecimal money);
}
```

StorageService

```java
package com.harry.springcloud.service;

import com.harry.springcloud.domain.CommonResult;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@FeignClient(value = "seata-storage-service")
public interface StorageService {

    @PostMapping("storage/decrease")
    CommonResult decrease(@RequestParam("productId") Long productId,
                          @RequestParam("count") Integer count);

}
```

OrderService

```java
package com.harry.springcloud.service;

import com.harry.springcloud.domain.Order;

public interface OrderService {
    void create(Order order);
}
```

#### OrderServiceImpl

```java
package com.harry.springcloud.service.impl;

import com.harry.springcloud.dao.OrderDao;
import com.harry.springcloud.domain.Order;
import com.harry.springcloud.service.AccountService;
import com.harry.springcloud.service.OrderService;
import com.harry.springcloud.service.StorageService;
import io.seata.spring.annotation.GlobalTransactional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;

/**
 * 创建订单-> 调用库存服务器扣减库存->调用账户服务扣减账户余额->修改订单状态
 *
 * 下订单->减库存->减余额->该状态
 * @author 81509
 */
@Service
@Slf4j
public class OrderServiceImpl implements OrderService {

    @Resource
    private OrderDao orderDao;
    @Resource
    private AccountService accountService;
    @Resource
    private StorageService storageService;

    @Override
    @GlobalTransactional(name = "fsp-create-order",rollbackFor = Exception.class)
    public void create(Order order) {
        log.info("--------->开始新建订单");
        //1 新建订单
        orderDao.create(order);


        //2 扣减库存
        log.info("------------->订单微服务开始调用库存,做扣减Count");
        storageService.decrease(order.getProductId(), order.getCount());
        log.info("------------->订单微服务开始调用库存,做扣减end");


        //3 扣减账户
        log.info("------------->订单微服务开始调用账户,做扣减Money");
        accountService.decrease(order.getUserId(), order.getMoney());
        log.info("------------->订单微服务开始调用账户,做扣减end");


        //4 修改订单状态
        log.info("------------->修改订单状态开始");
        orderDao.update(order.getUserId(),0);
        log.info("------------->修改订单状态结束");

        log.info("------------->下订单结束了");
    }
}
```

#### Controller

OrderController

```java
package com.harry.springcloud.controller;

import com.harry.springcloud.domain.CommonResult;
import com.harry.springcloud.domain.Order;
import com.harry.springcloud.service.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class OrderController {

    @Autowired
    private OrderService orderService;

    @GetMapping("/order/create")
    public CommonResult create(Order order) {
        orderService.create(order);
        return new CommonResult(200, "订单创建完成");
    }



}
```

#### Config配置

```java
@Configuration
@MapperScan("com.harry.springcloud.dao")
public class MyBatisConfig {
}
```

DataSourceProxyConfig

```java
package com.harry.springcloud.config;

import com.alibaba.druid.pool.DruidDataSource;
import io.seata.rm.datasource.DataSourceProxy;
import org.apache.ibatis.session.SqlSessionFactory;
import org.mybatis.spring.SqlSessionFactoryBean;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.core.io.support.ResourcePatternResolver;

import javax.sql.DataSource;

@Configuration
public class DataSourceProxyConfig {

    @Value("${mybatis.mapper-locations}")
    private String mapperLocations;


    @Bean
    @ConfigurationProperties(prefix = "spring.datasource")
    public DataSource druidDataSource() {
        return new DruidDataSource();
    }


    @Primary
    @Bean("dataSource")
    public DataSourceProxy dataSourceProxy(DataSource druidDataSource) {
        return new DataSourceProxy(druidDataSource);
    }

    @Bean(name = "sqlSessionFactory")
    public SqlSessionFactory sqlSessionFactoryBean(DataSourceProxy dataSourceProxy) throws Exception {
        SqlSessionFactoryBean bean = new SqlSessionFactoryBean();
        bean.setDataSource(dataSourceProxy);
        ResourcePatternResolver resolver = new PathMatchingResourcePatternResolver();
        bean.setMapperLocations(resolver.getResources(mapperLocations));

        SqlSessionFactory factory;
        try {
            factory = bean.getObject();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        return factory;
    }

}
```

#### 主启动

```java
package com.harry.springcloud;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.openfeign.EnableFeignClients;

@SpringBootApplication(exclude = DataSourceAutoConfiguration.class) // 取消数据源的自动创建
@EnableDiscoveryClient
@EnableFeignClients
public class SeataOrderMainApp2001 {
    public static void main(String[] args) {
        SpringApplication.run(SeataOrderMainApp2001.class, args);
    }
}
```



## Test

### 下订单->减库存->扣余额->改(订单)状态

![image-20210401211907730](\images\image-20210401211907730.png)

### 正常下单

http://localhost:2001/order/create?userId=1&productId=1&count=10&money=100

![image-20210401211933404](\images\image-20210401211933404.png)

### 超时异常,没加@GlobalTransactional

AccountServiceImpl添加超时

![image-20210401212111181](\images\image-20210401212111181.png)

故障情况

当库存和账户金额扣减后,订单状态并没有设置为已经完成,没有从零改为1

而且由于feign的重试机制,账户余额还有可能被多次扣减

### 超时异常,添加@GlobalTransactional

AccountServiceImpl添加超时

OrderServiceImpl@GlobalTransactional

![image-20210401212316789](\images\image-20210401212316789.png)

## 一部分补充

### Seata

Simple Extensible Autonomous Transaction Architecture,简单可扩展自治事务框架

2020起始,参加工作后用1.0以后的版本

### 再看TC/TM/RM三个组件

分布式事务的执行流程：

TM开启分布式事务(TM向TC注册全局事务记录)

按业务场景,编排数据库、服务等事务内资源(RM向TC汇报资源准备状态)

TM结束分布式事务,事务一阶段结束(TM通知TC提交/回滚分布式事务)

TC汇报事务信息,决定分布式事务是提交还是回滚

TC通知所有RM提交/回滚资源,事务二阶段结束

### AT模式如何做到对业务的无侵入

![image-20210401212457888](\images\image-20210401212457888.png)

一阶段加载

![image-20210401212540318](\images\image-20210401212540318.png)

![image-20210401212601171](\images\image-20210401212601171.png)

二阶段提交

![image-20210401212619469](\images\image-20210401212619469.png)

三阶段回滚

![image-20210401212641507](\images\image-20210401212641507.png)

![image-20210401212656300](\images\image-20210401212656300.png)

AccountServiceImpl

![image-20210401212719951](\images\image-20210401212719951.png)

![image-20210401212732623](\images\image-20210401212732623.png)

undo.log

![image-20210401212800365](\images\image-20210401212800365.png)

before image

![image-20210401212818457](\images\image-20210401212818457.png)

![image-20210401212845834](\images\image-20210401212845834.png)

