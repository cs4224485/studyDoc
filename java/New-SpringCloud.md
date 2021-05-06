# 一 、微服务概括

## 微服务概述

### 什么是微服务

- 目前的微服务并没有一个统一的标准，一般是以业务来划分
- 将传统的一站式应用，拆分成一个个的服务，彻底去耦合，一个微服务就是单功能业务，只做一件事。
- 与微服务相对的叫巨石

### 微服务与微服务架构

- 微服务是一种架构模式或者一种架构风格，提倡将单一应用程序划分成一组小的服务==独立部署==，服务之间相互配合、相互协调，每个服务运行于自己的进程中。
- 服务与服务间采用轻量级通讯，如HTTP的RESTful API等
- 避免统一的、集中式的服务管理机制

### 微服务的优缺点

#### 优点

1. 每个服务足够内聚，足够小，比较容易聚焦
2. 开发简单且效率高，一个服务只做一件事情
3. 开发团队小，一般2-5人足以（当然按实际为准）
4. 微服务是松耦合的，无论开发还是部署都可以独立完成
5. 微服务能用不同的语言开发
6. 易于和第三方集成，微服务允许容易且灵活的自动集成部署（持续集成工具有Jenkins,Hudson,bamboo等）
7. 微服务易于被开发人员理解，修改和维护，这样可以使小团队更加关注自己的工作成果，而无需一定要通过合作才能体现价值
8. 微服务允许你融合最新的技术
9. 微服务只是业务逻辑的代码，不会和HTML,CSS或其他界面组件融合。
10. 每个微服务都可以有自己的存储能力，数据库可自有也可以统一，十分灵活。

#### 缺点

1. 开发人员要处理分布式系统的复杂性
2. 多服务运维难度，随着服务的增加，运维的压力也会增大
3. 依赖系统部署
4. 服务间通讯的成本
5. 数据的一致性
6. 系统集成测试
7. 性能监控的难度

###  微服务的技术栈

| 微服务条目                               | 落地技术                                                     |
| ---------------------------------------- | ------------------------------------------------------------ |
| 服务开发                                 | SpringBoot,Spring,SpringMVC                                  |
| 服务配置与管理                           | Netflix公司的Archaius、阿里的Diamond等                       |
| 服务注册与发现                           | Eureka、Consul、Zookeeper等                                  |
| 服务调用                                 | Rest、RPC、gRPC                                              |
| 服务熔断器                               | Hystrix、Envoy等                                             |
| 负载均衡                                 | Ribbon、Nginx等                                              |
| 服务接口调用（客户端调用服务的简化工具） | Feign等                                                      |
| 消息队列                                 | Kafka、RabbitMQ、ActiveMQ等                                  |
| 服务配置中心管理                         | SpringCloudConfig、Chef等                                    |
| 服务路由（API网关）                      | Zuul等                                                       |
| 服务监控                                 | Zabbix、Nagios、Metrics、Specatator等                        |
| 全链路追踪                               | Zipkin、Brave、Dapper等                                      |
| 服务部署                                 | Docker、OpenStack、Kubernetes等                              |
| 数据流操作开发包                         | SpringCloud Stream(封装与Redis，Rabbit，Kafka等发送接收消息) |
| 事件消息总线                             | SpringCloud Bus                                              |

###  为什么选SpringCloud作为微服务架构

#### 选型依据

1. 整体解决方案和框架的成熟度
2. 社区热度
3. 可维护性
4. 学习曲线

#### 当前各大IT公司的微服务架构

1. 阿里Dubbo/HSF
2. 京东JSF
3. 新浪Motan
4. 当当DubboX

#### 各微服务的框架对比

| 功能点/服务框架 | Netflix/SpringCloud                                          | Motan                                                        | gRPC                      | Thrift   | Dubbo/DubboX    |
| --------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------- | -------- | --------------- |
| 功能定位        | 完整的微服务架构                                             | RPC框架，但整合了ZK或Consul，实现集群环境的基本服务注册/发现 | RPC框架                   | RPC框架  | 服务框架        |
| 支持Rest        | 是，Ribbon支持多种可插拔的序列化选择                         | 否                                                           | 否                        | 否       | 否              |
| 支持RPC         | 否                                                           | 是                                                           | 是                        | 是       | 是              |
| 支持多语言      | 是（Rest形式）                                               | 否                                                           | 是                        | 是       | 否              |
| 服务注册/发现   | 是（Eureka） Eureka服务注册表，Karyon服务端框架支持服务自注册和健康检查 | 是（zookeeper/consul）                                       | 否                        | 否       | 是              |
| 负载均衡        | 是（服务端zuul+客户端Ribbon） zuul-服务，动态路由 云端负载均衡 Eureka（针对中间层服务器） | 是（客户端）                                                 | 否                        | 否       | 是（客户端）    |
| 配置服务        | Netflix Archaius SpringCloud Config Server集中配置           | 是（zookeeper提供）                                          | 否                        | 否       | 否              |
| 服务调用链监控  | 是（zuul） Zuul提供边缘服务，API网关                         | 否                                                           | 否                        | 否       | 否              |
| 高可用/容错     | 是（服务端Hystrix+客户端Ribbon）                             | 是（客户端）                                                 | 否                        | 否       | 是（客户端）    |
| 典型应用案例    | Netflix                                                      | Sina                                                         | Google                    | Facebook |                 |
| 社区活跃度      | 高                                                           | 一般                                                         | 高                        | 一般     | 2017年7月才重启 |
| 学习难度        | 中等                                                         | 一般                                                         | 高                        | 一般     | 低              |
| 文档丰富度      | 高                                                           | 一般                                                         | 一般                      | 一般     | 高              |
| 其他            | Spring Cloud Bus为我们应用程序带来了更多管理端点             | 支持降级                                                     | Netflix内部在开发集成gRPC | IDL定义  | 实              |

# 二 、SpringCloud入门概述

### SpringCloud是什么

- 分布式系统的简化版（官方介绍）
- SpringCloud基于SpringBoot提供了一整套微服务的解决方案，包括服务注册与发现，配置中心，全链路监控，服务网关，负载均衡，熔断器等组件，除了基于Netflix的开源组件做高度抽象封装之外，还有一些选型中立的开源组件
- SpringCloud利用SpringBoot的开发便利性巧妙地简化了分布式系统的基础设施开发，SpringCloud为开发人员提供了快速构建分布式系统的一些工具，包括配置管理、服务发现、断路器、路由、微代理、事件总线，全局所、决策精选、分布式会话等等，他们都可以用SpringBoot的开发风格做到一键启动和部署。
- 一句话概括：SpringCloud是分布式微服务架构下的一站式解决方案，是各个微服务架构落地技术的几何体，俗称微服务全家桶==

### SpringCloud和SpringBoot的关系

SpringBoot：专注于快速方便的开发单个个体微服务（关注微观）

SpringCloud：关注全局的微服务协调治理框架，将SpringBoot开发的一个个单体微服务组合并管理起来（关注宏观）

SpringBoot可以离开SpringCloud独立使用，但是SpringCloud不可以离开SpringBoot，属于依赖关系

### Dubbo是怎么到SpringCloud的？哪些优缺点去技术选型

#### 目前成熟都互联网架构（分布式+服务治理Dubbo）

#### 对比

|              | Dubbo         | Spring                       |
| ------------ | ------------- | ---------------------------- |
| 服务注册中心 | Zookeeper     | Spring Cloud Netfilx Eureka  |
| 服务调用方式 | RPC           | REST API                     |
| 服务监控     | Dubbo-monitor | Spring Boot Admin            |
| 断路器       | 不完善        | Spring Cloud Netflix Hystrix |
| 服务网关     | 无            | Spring Cloud Netflix Zuul    |
| 分布式配置   | 无            | Spring Cloud Config          |
| 服务跟踪     | 无            | Spring Cloud Sleuth          |
| 消息总线     | 无            | Spring Cloud Bus             |
| 数据流       | 无            | Spring Cloud Stream          |
| 批量任务     | 无            | Spring Cloud Task            |

**最大区别：**

- Spring Cloud抛弃了RPC通讯，采用基于HTTP的REST方式。Spring Cloud牺牲了服务调用的性能，但是同时也避免了原生RPC带来的问题。REST比RPC更为灵活，不存在代码级别的强依赖，在强调快速演化的微服务环境下，显然更合适。
- 一句话：Dubbo像组装机，Spring Cloud像一体机
- 社区的支持与力度：Dubbo曾经停运了5年，虽然重启了，但是对于技术发展的新需求，还是需要开发者自行去拓展，对于中小型公司，显然显得比较费时费力，也不一定有强大的实力去修改源码

### SpringBoot版本选择

SpringBoot2.0新特性

```
https:github.com/spring-projects/spring-boot/wiki/Spring-Boot-2.0-Release-Notes
```

通过上面官网发现 Boot官方强烈建议你升级到2.X以上版本

![image-20210227150027970](\images\image-20210227150027970.png)

### SpringCloud版本选择

官网 htts://spring.io/projects/spring-cloud

Cloud命名规则

![image-20210227150141505](\images\image-20210227150141505.png)

### Springcloud和Springboot之间的依赖关系如何看

https://spring.io/projects/spring-cloud#overview

![image-20210227150213553](\images\image-20210227150213553.png)

# 三、微服务架构编码 构建

### IDEA新建project工作空间

父工程步骤

#### 1.New Project

![image-20210227150526556](\images\image-20210227150526556.png)

#### 2.聚合总父工程名字

#### 3.Maven选版本

#### 4.工程名字

#### 5.字符编码

![image-20210227150656071](images\image-20210227150656071.png)

#### 6.注解生效激活

![image-20210227150725615](\images\image-20210227150725615.png)

#### 7. File Type过滤

![image-20210227150801751](\images\image-20210227150801751.png)

### 父工程POM文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.harry.springcloud</groupId>
    <artifactId>NewSpringCloud</artifactId>
    <version>1.0-SNAPSHOT</version>
    <modules>
        <module>cloud-provider-payment8001</module>
        <module>cloud-consumer-order80</module>
        <module>cloud-eureka-server7001</module>
        <module>cloud-api-common</module>
        <module>cloud-eureka-server7002</module>
        <module>cloud-provider-payment8002</module>
        <module>cloud-provider-payment8004</module>
        <module>cloud-consumerzk-order80</module>
    </modules>
    <packaging>pom</packaging>

    <!--统一管理jar包和版本-->
    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <maven.compiler.source>1.8</maven.compiler.source>
        <maven.compiler.target>1.8</maven.compiler.target>
        <junit.version>4.12</junit.version>
        <log4j.version>1.2.17</log4j.version>
        <lombok.version>1.16.18</lombok.version>
        <mysql.version>8.0.18</mysql.version>
        <druid.verison>1.1.16</druid.verison>
        <mybatis.spring.boot.verison>1.3.0</mybatis.spring.boot.verison>
    </properties>

    <dependencyManagement>
        <dependencies>
            <!--spring boot 2.2.2-->
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>2.2.2.RELEASE</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
            <!--spring cloud Hoxton.SR1-->
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>Hoxton.SR1</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
            <!--spring cloud alibaba 2.1.0.RELEASE-->
            <dependency>
                <groupId>com.alibaba.cloud</groupId>
                <artifactId>spring-cloud-alibaba-dependencies</artifactId>
                <version>2.2.0.RELEASE</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
            <!-- MySql -->
            <dependency>
                <groupId>mysql</groupId>
                <artifactId>mysql-connector-java</artifactId>
                <version>${mysql.version}</version>
            </dependency>
            <!-- Druid -->
            <dependency>
                <groupId>com.alibaba</groupId>
                <artifactId>druid-spring-boot-starter</artifactId>
                <version>${druid.verison}</version>
            </dependency>
            <!-- mybatis-springboot整合 -->
            <dependency>
                <groupId>org.mybatis.spring.boot</groupId>
                <artifactId>mybatis-spring-boot-starter</artifactId>
                <version>${mybatis.spring.boot.verison}</version>
            </dependency>
            <!--lombok-->
            <dependency>
                <groupId>org.projectlombok</groupId>
                <artifactId>lombok</artifactId>
                <version>${lombok.version}</version>
            </dependency>
            <!--junit-->
            <dependency>
                <groupId>junit</groupId>
                <artifactId>junit</artifactId>
                <version>${junit.version}</version>
            </dependency>
            <!-- log4j -->
            <dependency>
                <groupId>log4j</groupId>
                <artifactId>log4j</artifactId>
                <version>${log4j.version}</version>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <fork>true</fork>
                    <addResources>true</addResources>
                </configuration>
            </plugin>
        </plugins>
    </build>

    <!--第三方maven私服-->
    <repositories>
        <repository>
            <id>nexus-aliyun</id>
            <name>Nexus aliyun</name>
            <url>http://maven.aliyun.com/nexus/content/groups/public</url>
            <releases>
                <enabled>true</enabled>
            </releases>
            <snapshots>
                <enabled>false</enabled>
            </snapshots>
        </repository>
    </repositories>

</project>
```

### Maven工程落地细节复习

Maven中的DependencyManagement和Dependencies

![image-20210227150947536](images\image-20210227150947536.png)

![image-20210227151016281](\images\image-20210227151016281.png)

这样做的好处就是: 如果有多个子项目都引用同一样的依赖,则可以避免在每个使用的子项目里都声明一个版本号,这样想升级或切换到另一个版本时,只需在顶层父容器里更新,而不需要一个一个子项目的修改;另外如果某个子项目需要另外的一个版本,只需声明version版本 

### cloud-provider-payment8001 微服务提供者Module模块

#### pom文件

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

    <artifactId>cloud-provider-payment8001</artifactId>

    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
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
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-jdbc</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
            <scope>runtime</scope>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
        </dependency>


        <dependency>
            <groupId>com.harry.springcloud</groupId>
            <artifactId>cloud-api-common</artifactId>
            <version>1.0-SNAPSHOT</version>
        </dependency>
    </dependencies>

</project>
```

#### yml配置文件

```yml
server:
  port: 8001
spring:
  application:
    name: cloud-payment-service
  datasource:
    type: com.alibaba.druid.pool.DruidDataSource  #当前数据源操作类型
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://192.168.30.129:3306/db2021?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: root
    password: 123456

mybatis:
  mapper-locations: classpath:mapper/*.xml
  type-aliases-package: com.harry.springcloud.entities

```

#### 建表sql

```sql
CREATE TABLE `payment`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `serial` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '支付流水号',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '支付表' ROW_FORMAT = Dynamic;
```

#### emtities

```java
package com.harry.springcloud.entities;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Payment implements Serializable {
    private Long id;
    private String serial;
}
```

```java
package com.harry.springcloud.entities;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class CommonResult <T>{
    private Integer code;
    private String message;
    private T data;
    public CommonResult(Integer code, String message){
        this(code,message,null);
    }
}
```

#### dao

```java
package com.harry.springcloud.Dao;

import com.harry.springcloud.entities.Payment;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

@Mapper
public interface PaymentDao {
    public int create(Payment payment);
    public Payment getPaymentById(@Param("id")Long id);
}
```

#### mapper

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.harry.springcloud.Dao.PaymentDao">
    <insert id="create" parameterType="Payment" useGeneratedKeys="true" keyProperty="id">
        insert into payment (serial) values (#{serial});
    </insert>
    <resultMap id="BaseResultMap" type="com.harry.springcloud.entities.Payment">
        <id column="id" property="id" jdbcType="BIGINT"/>
        <id column="serial" property="serial" jdbcType="VARCHAR"/>
    </resultMap>
    <select id="getPaymentById" parameterType="Long" resultMap="BaseResultMap">
        select * from payment where id=#{id};
    </select>
</mapper>
```

#### service

```java
package com.harry.springcloud.service;

import com.harry.springcloud.entities.Payment;
import org.apache.ibatis.annotations.Param;

public interface PaymentService {
    int create(Payment payment);
    Payment getPaymentById(@Param("id") Long id);
}
```

```java
package com.harry.springcloud.service.Impl;

import com.harry.springcloud.Dao.PaymentDao;
import com.harry.springcloud.entities.Payment;
import com.harry.springcloud.service.PaymentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class PaymentServiceImpl implements PaymentService {

    @Autowired
    private PaymentDao paymentDao;

    @Override
    public int create(Payment payment) {
        return paymentDao.create(payment);
    }

    @Override
    public Payment getPaymentById(Long id) {
        return paymentDao.getPaymentById(id);
    }
}
```

#### controller

```java
package com.harry.springcloud.controller;


import com.harry.springcloud.entities.CommonResult;
import com.harry.springcloud.entities.Payment;
import com.harry.springcloud.service.PaymentService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.client.ServiceInstance;
import org.springframework.cloud.client.discovery.DiscoveryClient;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@Slf4j
@RequestMapping("/payment")
public class PaymentController {

    @Autowired
    private PaymentService paymentService;

    @Value("${server.port}")
    private String serverPort;

    @PostMapping("/create")
    public CommonResult create(@RequestBody Payment payment){
        int result = paymentService.create(payment);
        log.info("插入数据的ID:\t" + payment.getId());
        log.info("插入结果：" + result);
        log.info("111111111");
        if (result > 0) {
            return new CommonResult(200, "插入数据成功", result);
        } else {
            return new CommonResult(444, "插入数据失败,", null);
        }

    }

    @GetMapping("/get/{id}")
    public CommonResult getPaymentById(@PathVariable("id") long id){
        Payment payment = paymentService.getPaymentById(id);
        if (payment != null) {
            return new CommonResult(200, "查询数据成功,serverPort："+serverPort, payment);
        } else {
            return new CommonResult(444, "没有对应记录,serverPort："+serverPort, null);
        }
    }
}
```

#### 测试

http://localhost:8001/payment/get/31

通过修改idea的workspace.xml的方式快速打开Run Dashboard窗口

开启Run DashBoard

![image-20210227152009187](\images\image-20210227152009187.png)

```xml
<component name="RunDashboard">
    <option name="configurationTypes">
      <set>
        <option value="SpringBootApplicationConfigurationType" />
      </set>
    </option>
  </component> 
```

![image-20210227152041878](\images\image-20210227152041878.png)

![image-20210227152101129](\images\image-20210227152101129.png)

### 热部署Devtools

#### 1.Adding devtools to your project

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-devtools</artifactId>
    <scope>runtime</scope>
    <optional>true</optional>
</dependency>
```

#### 2.Adding plugin to your pom.xml

下面配置我们粘贴进聚合父类总工程的pom.xml里

```xml
<build>
    <fileName>你自己的工程名字<fileName>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
            <configuration>
                <fork>true</fork>
                <addResources>true</addResources>
            </configuration>
        </plugin>
    </plugins>
</build>
     
```

#### 3.Enabling automatic build

![image-20210227152355947](\images\image-20210227152355947.png)

####  4.Update the value 

![image-20210227152423274](\images\image-20210227152423274.png)

### cloud-consumer-order80 微服务消费者订单Module模块

#### 改POM

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

    <artifactId>cloud-consumerzk-order80</artifactId>
    <dependencies>
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
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
            <scope>runtime</scope>
            <optional>true</optional>
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

#### 写YML

```yml
server:
  port: 80
spring:
  application:
    name: cloud-order-service
  datasource:
    type: com.alibaba.druid.pool.DruidDataSource  #当前数据源操作类型
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://192.168.30.129:3306/db2021?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: root
    password: 123456

mybatis:
  mapper-locations: classpath:mapper/*.xml
  type-aliases-package: com.harry.springcloud.entities
```

#### 主启动

```java
package com.harry.springcloud;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class OrderApplication {
    public static void main(String[] args) {
        SpringApplication.run(OrderApplication.class, args);
    }
}
```

#### Resttemplate

![image-20210227152813083](images\image-20210227152813083.png)

#### config配置类

```java
package com.harry.springcloud.config;

import org.springframework.cloud.client.loadbalancer.LoadBalanced;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
public class ApplicationContextConfig {
    @Bean
    public RestTemplate restTemplate(){
        return new RestTemplate();
    }
}
```

#### controller

```java
package com.harry.springcloud.controller;

import com.harry.springcloud.entities.CommonResult;
import com.harry.springcloud.entities.Payment;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@RestController
@Slf4j
public class OrderController {
    @Autowired
    RestTemplate restTemplate;

//    private final static String PAYMENT_URL = "http://localhost:8001";//不集群
    public static final String PAYMENT_URL="http://CLOUD-PAYMENT-SERVICE";

    @GetMapping("/consumer/payment/get/{id}")
    public CommonResult<Payment> getPaymentById(@PathVariable("id") Long id){
        return restTemplate.getForObject(PAYMENT_URL + "/payment/get/" + id, CommonResult.class, id);
    }

    @GetMapping("/consumer/payment/create")
    public CommonResult<Payment> create(Payment payment){
        return restTemplate.postForObject(PAYMENT_URL + "/payment/create", payment, CommonResult.class);
    }
}
```

#### 测试

http://localhost/consumer/payment/get/1

不要忘记@RequestBody注解

### 工程重构

#### 新建cloud-api-common

pom

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-devtools</artifactId>
        <scope>runtime</scope>
        <optional>true</optional>
    </dependency>
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <optional>true</optional>
    </dependency>
    <dependency>
        <groupId>cn.hutool</groupId>
        <artifactId>hutool-all</artifactId>
        <version>5.1.0</version>
    </dependency>
</dependencies>
```

#### Payment实体

```java
package com.harry.springcloud.entities;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Payment implements Serializable {
    private Long id;
    private String serial;
}
```

#### CommonResult通用封装类

```java
package com.harry.springcloud.entities;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class CommonResult <T>{
    private Integer code;
    private String message;
    private T data;
    public CommonResult(Integer code, String message){
        this(code,message,null);
    }
}
```

#### maven命令clean install

#### 订单80和支付8001分别改造

```xml
<dependency>
    <groupId>com.harry.springcloud</groupId>
    <artifactId>cloud-api-common</artifactId>
    <version>1.0-SNAPSHOT</version>
</dependency>
```

# 四、 Eureka服务注册与发现

###  Eureka介绍及原理

#### 理解

Eureka就像一个物业管理公司，其他微服务就像小区的住户，每个住户入住时都要向物业管理公司注册，并定时向物业公司交管理费

#### 介绍

- Eureka是一个基于REST的服务，用于定位服务，以实现云端中间层服务发现和故障转移。
- Eureka主管服务注册与发现，在微服务中，以后了这两者，只需要使用服务的标识符（就是那个在每个服务的yml文件中取得服务名称），就可以访问到服务，不需要修改服务调用的配置文件
- Eureka遵循AP原则（高可用，分区容错性），因为使用了自我保护机制所以保证了高可用

#### 原理

- Eureka使用的是C-S结构（客户端-服务端）
- 两大组件：Eureka Server（提供注册服务）、 Eureka Client（JAVA客户端，负责发送心跳）
- 系统中的其他微服务使用Eureka客户端连接到Eureka服务端维持心跳连接（即注册）。SpringCloud的其他模块可以通过Eureka Server 来发现系统中的微服务并加以调用

![image-20210227153457183](\images\image-20210227153457183.png)

###  Eureka服务注册中心构建

#### 创建cloud-eureka-server7001

####  加入服务端依赖

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
    </dependency>
</dependencies>
```

####  配置yml

```yml
server:
  port: 7001

eureka:
  instance:
    hostname: eureka7001.com #eureka服务端实例名称
  client:
    register-with-eureka: false #表示不向注册中心注册自己
    fetch-registry: false #false表示自己就是注册中心，我的职责就是维护服务实例,并不区检索服务
    service-url:
      defaultZone: http://eureka7002.com:7002/eureka/
#      defaultZone: http://eureka7001.com:7001/eureka/ # 不搭建集群 单机 指向自己
#      defaultZone: http://eureka7002.com:7002/eureka/,http://eureka7001.com:7001/eureka/ # 搭建集群 集群是指向其他eureka
#  server:
#    enable-self-preservation: false # 关闭自我保护机制 保证不可用服务及时清除
#    eviction-interval-timer-in-ms: 2000
```

####  添加启动类

```java
package com.harry.springcloud;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.server.EnableEurekaServer;

@SpringBootApplication
@EnableEurekaServer
public class EurekaApplication7001 {
    public static void main(String[] args) {
        SpringApplication.run(EurekaApplication7001.class, args);
    }
}
```

#### 微服务注册名配置说明

![image-20210227153942649](\images\image-20210227153942649.png)

###  向Eureka注册中心注册微服务

#### cloud-provider-payment8001 将注册进EurekaServer成为服务提供者provider

##### 改POM

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
</dependency>
```

##### 写YML

```yml
server:
  port: 8001
spring:
  application:
    name: cloud-payment-service
  datasource:
    type: com.alibaba.druid.pool.DruidDataSource  #当前数据源操作类型
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://192.168.30.129:3306/db2021?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: root
    password: 123456

mybatis:
  mapper-locations: classpath:mapper/*.xml
  type-aliases-package: com.harry.springcloud.entities

eureka:
  client:
    register-with-eureka: true
    fetch-registry: true
    service-url:
      # 集群版
      defaultZone: http://eureka7001.com:7001/eureka,http://eureka7002.com:7002/eureka
  instance:
    instance-id: payment8001
    prefer-ip-address: true # 访问路径可以显示IP
```

##### 修改主启动

```java
package com.harry.springcloud;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;


@SpringBootApplication
@EnableEurekaClient
@EnableDiscoveryClient
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

#### EurekaClient端cloud-consumer-order80 将注册进EurekaServer成为服务消费者consume

##### 改POM

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
</dependency>
```

##### 写YML

```yml
eureka:
  client:
    register-with-eureka: true
    fetch-registry: true
    service-url:
      # 集群版
      defaultZone: http://eureka7001.com:7001/eureka,http://eureka7002.com:7002/eureka
```

##### 修改主启动

```java
package com.harry.springcloud;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;

@SpringBootApplication
@EnableEurekaClient
public class OrderApplication {
    public static void main(String[] args) {
        SpringApplication.run(OrderApplication.class, args);
    }
}
```

### 集群Eureka构建步骤

#### Eureka集群原理说明

![image-20210227154547081](images\image-20210227154547081.png)

#### Eureka集群环境构建步骤

##### 新建cloud-eureka-server70021

##### 改POM

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

    <artifactId>cloud-eureka-server7002</artifactId>

    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
        </dependency>
    </dependencies>

</project>
```

##### C:\Windows\System32\drivers\etc路径下的hosts文件

```
127.0.0.1 eureka7001.com
127.0.0.1 eureka7002.com
```

刷新hosts文件ipconfig /flushdns

7001yml

```yml
server:
  port: 7001
spring:
  application:
    name: cloud-eureka-service
eureka:
  instance:
eureka服务端的实例名称
    hostname: eureka7001.com
  client:
    # false表示不向注册中心注册自己
    register-with-eureka: false
    # false表示自己端就是注册中心,我的职责就是维护服务实例,并不需要检索服务
    fetch-registry: false
    service-url:
      # 设置与Eureka Server交互的地址查询服务和注册服务都需要依赖这个地址
      defaultZone: http://eureka7002.com:7002/eureka/s
```

7002yml

```yml
server:
  port: 7002
spring:
  application:
    name: cloud-eureka-service2
eureka:
  instance:
    hostname:  eureka7002.com
  client:
    register-with-eureka: false
    fetch-registry: false
    service-url:
      defaultZone: http://eureka7001.com:7001/eureka/
```

##### 将支付服务8001微服务发布到上面2台Eureka集群配置中

```yml
eureka:
  client:
    register-with-eureka: true
    fetch-registry: true
    service-url:
      defaultZone: http://eureka7001.com:7001/eureka,http://eureka7002.com:7002/eureka
```

##### 修改8001/8002的controller

```java
package com.harry.springcloud.controller;


import com.harry.springcloud.entities.CommonResult;
import com.harry.springcloud.entities.Payment;
import com.harry.springcloud.service.PaymentService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.client.ServiceInstance;
import org.springframework.cloud.client.discovery.DiscoveryClient;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@Slf4j
@RequestMapping("/payment")
public class PaymentController {

    @Autowired
    private PaymentService paymentService;

    @Autowired
    private DiscoveryClient discoveryClient;

    @Value("${server.port}")
    private String serverPort;

    @PostMapping("/create")
    public CommonResult create(@RequestBody Payment payment){
        int result = paymentService.create(payment);
        log.info("插入数据的ID:\t" + payment.getId());
        log.info("插入结果：" + result);
        log.info("111111111");
        if (result > 0) {
            return new CommonResult(200, "插入数据成功", result);
        } else {
            return new CommonResult(444, "插入数据失败,", null);
        }

    }

    @GetMapping("/get/{id}")
    public CommonResult getPaymentById(@PathVariable("id") long id){
        Payment payment = paymentService.getPaymentById(id);
        if (payment != null) {
            return new CommonResult(200, "查询数据成功,serverPort："+serverPort, payment);
        } else {
            return new CommonResult(444, "没有对应记录,serverPort："+serverPort, null);
        }
    }
}
```

##### 负载均衡

```java
package com.harry.springcloud.config;

import org.springframework.cloud.client.loadbalancer.LoadBalanced;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
public class ApplicationContextConfig {
    @Bean
    @LoadBalanced
    public RestTemplate restTemplate(){
        return new RestTemplate();
    }
}
```

### actuator微服务信息完善

#### 主机名称:服务名称修改

```yml
eureka:
  client:
    register-with-eureka: true
    fetch-registry: true
    service-url:
      # 集群版
      defaultZone: http://eureka7001.com:7001/eureka,http://eureka7002.com:7002/eureka
  instance:
    instance-id: payment8001
```

#### 访问信息有IP信息提示

```yml
eureka:
  client:
    register-with-eureka: true
    fetch-registry: true
    service-url:
      # 集群版
      defaultZone: http://eureka7001.com:7001/eureka,http://eureka7002.com:7002/eureka
  instance:
    prefer-ip-address: true # 访问路径可以显示IP
```

### 服务发现Discovery

对于注册eureka里面的微服务,可以通过服务发现来获得该服务的信息

修改cloud-provider-payment8001的Controller

```java
package com.harry.springcloud.controller;


import com.harry.springcloud.entities.CommonResult;
import com.harry.springcloud.entities.Payment;
import com.harry.springcloud.service.PaymentService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.client.ServiceInstance;
import org.springframework.cloud.client.discovery.DiscoveryClient;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@Slf4j
@RequestMapping("/payment")
public class PaymentController {

    @Autowired
    private PaymentService paymentService;

    @Autowired
    private DiscoveryClient discoveryClient;

    @Value("${server.port}")
    private String serverPort;
    
    @GetMapping(value = "/discovery")
    public Object discovery(){
        List<String> services = discoveryClient.getServices();
        for (String element : services) {
            log.info("element:\t" + element);
        }
        List<ServiceInstance> instances = discoveryClient.getInstances("CLOUD-PAYMENT-SERVICE");
        for (ServiceInstance instance : instances) {
            log.info(instance.getServiceId() + "\t" + instance.getHost() + "\t" + instance.getPort() + "\t" + instance.getUri());
        }
        return discoveryClient;
    }
}
```

启动类

```java
package com.harry.springcloud;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;


@SpringBootApplication
@EnableEurekaClient
@EnableDiscoveryClient
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

效果图

![image-20210227155727559](\images\image-20210227155727559.png)

### eureka自我保护

#### 故障现象

![image-20210227155805293](\images\image-20210227155805293.png)

#### 导致原因

![image-20210227155835647](\images\image-20210227155835647.png)

![image-20210227155848893](\images\image-20210227155848893.png)

![image-20210227155902594](\images\image-20210227155902594.png)

使用eureka.server.enable-self-preservation=false 可以禁用自我保护模式

Eureka服务端在收到最后一次心跳后等待时间上限 ,单位为秒(默认是90秒),超时剔除服务

eureka.instance.lease-expiration-duration-in-seconds=90

# 五、Zookeeper服务注册与发现

### 注册中心Zookeeper

Zookeeper是一个分布式协调工具,可以实现注册中心功能，Zookeeper服务器取代Eureka服务器,zk作为服务注册中心

### 新建cloud-provider-payment8004

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

    <artifactId>cloud-provider-payment8004</artifactId>

    <dependencies>
        <dependency>
            <groupId>com.harry.springcloud</groupId>
            <artifactId>cloud-api-common</artifactId>
            <version>1.0-SNAPSHOT</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <!--SpringBoot整合Zookeeper客户端-->

        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-zookeeper-discovery</artifactId>
            <exclusions>
                <!--先排除自带的zookeeper3.5.3-->
                <exclusion>
                    <groupId>org.apache.zookeeper</groupId>
                    <artifactId>zookeeper</artifactId>
                </exclusion>
            </exclusions>
        </dependency>

        <dependency>
            <groupId>org.apache.zookeeper</groupId>
            <artifactId>zookeeper</artifactId>
            <version>3.4.11</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
            <scope>runtime</scope>
            <optional>true</optional>
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
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-jdbc</artifactId>
        </dependency>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
        </dependency>
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>druid-spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.mybatis.spring.boot</groupId>
            <artifactId>mybatis-spring-boot-starter</artifactId>
        </dependency>
    </dependencies>
</project>
```

#### YML

```yml
server:
  port: 8004
spring:
  application:
    name: cloud-provider-payment
  datasource:
    type: com.alibaba.druid.pool.DruidDataSource  #当前数据源操作类型
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://192.168.30.129:3306/db2021?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: root
    password: 123456
  cloud:
    zookeeper:
      # 默认localhost:2181
      connect-string: 192.168.31.97:2181

mybatis:
  mapper-locations: classpath:mapper/*.xml
  type-aliases-package: com.harry.springcloud.entities
```

#### 主启动类

```java
package com.harry.springcloud;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@SpringBootApplication
@EnableDiscoveryClient
public class PaymentApplication8004 {
    public static void main(String[] args) {
        SpringApplication.run(PaymentApplication8004.class,args);
    }
}
```

#### Controller

```java
package com.harry.springcloud.controller;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;
import java.util.UUID;

@RestController
@Slf4j
public class PaymentController {
    @Value("${server.port}")
    private String serverPort;

    @RequestMapping(value = "payment/zk")
    public String paymentZk() {
        return "SpringCloud with zookeeper:" + serverPort + "\t" + UUID.randomUUID().toString();
    }
}
```

### 启动8004注册进zookeeper

启动zk

```
zkServer.sh star
```

### 启动后出现的问题

![image-20210227160451271](\images\image-20210227160451271.png)

### 解决zookeeper版本jar包冲突问题

![image-20210227160520508](\images\image-20210227160520508.png)

### 新建cloud-consumerzk-order80

#### Pom

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

    <artifactId>cloud-consumerzk-order80</artifactId>
    <dependencies>
        <dependency>
            <groupId>com.harry.springcloud</groupId>
            <artifactId>cloud-api-common</artifactId>
            <version>1.0-SNAPSHOT</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <!--SpringBoot整合Zookeeper客户端-->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-zookeeper-discovery</artifactId>
            <exclusions>
                <!--先排除自带的zookeeper3.5.3-->
                <exclusion>
                    <groupId>org.apache.zookeeper</groupId>
                    <artifactId>zookeeper</artifactId>
                </exclusion>
            </exclusions>
        </dependency>
        <!--添加zookeeper3.4.9版本-->
        <dependency>
            <groupId>org.apache.zookeeper</groupId>
            <artifactId>zookeeper</artifactId>
            <version>3.4.11</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
            <scope>runtime</scope>
            <optional>true</optional>
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

```YML
server:
  port: 80
spring:
  application:
    # 服务别名
    name: cloud-consumer-order
  cloud:
    zookeeper:
      # 注册到zookeeper地址
      connect-string: 192.168.31.97:2181
```

#### 主启动

```java
package com.harry.springcloud;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@SpringBootApplication
@EnableDiscoveryClient
public class OrderZkMain80 {
    public static void main(String[] args) {
        SpringApplication.run(OrderZkMain80.class, args);
    }
}
```

#### controller

```java
package com.harry.springcloud.controller;

import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import javax.annotation.Resource;

@RestController
@Slf4j
public class OrderZkController {

    public static final String INVOKE_URL = "http://cloud-provider-payment";
    @Resource
    private RestTemplate restTemplate;


    /**
     * http://localhost/consumer/payment/zk
     *
     * @return
     */
    @GetMapping("/consumer/payment/zk")
    public String paymentInfo() {
        return restTemplate.getForObject(INVOKE_URL + "/payment/zk", String.class);
    }
}
```

# 六、Consul服务注册与发现

### Consul的简介

官网：https://www.consul.io/intro/index.html

![image-20210301192411149](\images\image-20210301192411149.png)

![image-20210301192450097](\images\image-20210301192450097.png)

![image-20210301192527955](\images\image-20210301192527955.png)

下载地址：https://www.consul.io/downloads.html

官方文档：https://www.springcloud.cc/spring-cloud-consul.html

使用开发模式启动

```
consul agent -dev
```

通过以下地址可以访问Consul的首页:  http://localhost:8500

### 新建Module支付服务provider8006

#### pom.xml

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

    <artifactId>cloud-provider-payment8006</artifactId>

    <dependencies>
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
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
            <scope>runtime</scope>
            <optional>true</optional>
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
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-jdbc</artifactId>
        </dependency>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
        </dependency>
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>druid-spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.mybatis.spring.boot</groupId>
            <artifactId>mybatis-spring-boot-starter</artifactId>
        </dependency>

        <!--SpringCloud consul-server-->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-consul-discovery</artifactId>
        </dependency>
    </dependencies>
</project>
```

#### YML

```YML
server:
  # consul服务端口
  port: 8006
spring:
  application:
    name: cloud-provider-payment
  datasource:
    type: com.alibaba.druid.pool.DruidDataSource  #当前数据源操作类型
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://192.168.30.129:3306/db2021?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: root
    password: 123456
    
  cloud:
    consul:
      # consul注册中心地址
      host: 192.168.31.97
      port: 8500
      discovery:
      	# healthcheck地址
        hostname: 127.0.0.1
        service-name: ${spring.application.name}
```

#### 启动类

```java
package com.harry.springcloud;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@SpringBootApplication
@EnableDiscoveryClient
public class PaymentMain8006 {
    public static void main(String[] args) {
        SpringApplication.run(PaymentMain8006.class, args);
    }
}
```

#### Controller

```java
@RestController
@Slf4j
public class PaymentController {
    @Value("${server.port}")
    private String serverPort;

    @RequestMapping(value = "payment/consul")
    public String paymentConsul() {
        return "SpringCloud with consul:" + serverPort + "\t" + UUID.randomUUID().toString();
    }
}
```

### 新建Module消费服务order80

#### pom.xml

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

    <artifactId>cloud-consumerconsul-order80</artifactId>

    <dependencies>
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
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
            <scope>runtime</scope>
            <optional>true</optional>
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
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-jdbc</artifactId>
        </dependency>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
        </dependency>
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>druid-spring-boot-starter</artifactId>
        </dependency>
        <dependency>
            <groupId>org.mybatis.spring.boot</groupId>
            <artifactId>mybatis-spring-boot-starter</artifactId>
        </dependency>

        <!--SpringCloud consul-server-->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-consul-discovery</artifactId>
        </dependency>
    </dependencies>
</project>
```

#### YML

```yml
server:
  port: 80
spring:
  application:
    name: cloud-order-service
  datasource:
    type: com.alibaba.druid.pool.DruidDataSource  #当前数据源操作类型
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://192.168.30.129:3306/db2021?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: root
    password: 123456

  cloud:
    consul:
      # consul注册中心地址
      host: 192.168.31.97
      port: 8500
      discovery:
        service-name: ${spring.application.name}
        hostname: 192.168.31.188
```

#### 启动类

```java
package com.harry.springcloud;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

@SpringBootApplication
@EnableDiscoveryClient
public class OrderConsulMain80 {
    public static void main(String[] args) {
        SpringApplication.run(OrderConsulMain80.class, args);
    }
}
```

#### Controller

```java
package com.harry.springcloud.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@RestController
@RequestMapping("/consumer")
public class OrderConsulController {

    private static final String INVOKE_URL = "http://cloud-provider-payment";

    @Autowired
    private RestTemplate restTemplate;

    @RequestMapping("/payment/consul")
    public String get() {
        String result = restTemplate.getForObject(INVOKE_URL + "/payment/consul", String.class);
        return result;
    }

}
```

### AP(eureka)

![image-20210301211737333](\images\image-20210301211737333.png)

### CP(Zookeeper/Consul)

![image-20210301211825424](\images\image-20210301211825424.png)

# 七、Ribbon负载均衡调用

### 概述

Spring Cloud Ribbon是基于Netflix Ribbon实现的一套客户端负载均衡工具。Ribbon会自动帮助你基于某种规则（简单轮询、随机连接等），也可以实现自定义的负载均衡算法。

###  负载均衡

- 英文名称：Load Balance，微服务或分布式集群中常用的一种应用
- 简单来说负载均衡就是将用户的请求ping平摊的分配到多个任务上，从而是系统达到HA（高可用）
- 两种负载均衡：
  1. 集中式LB：偏硬件，服务的消费方和提供方之间使用独立的LB设施，由该设施负责把访问请求以某种策略转发至服务的提供方。
  2. 进程内LB：骗软件， 将LB逻辑集成到消费方，消费方从服务注册中心指导哪些地址可用，再自己选择一个合适的服务器

### 架构说明

![image-20210301212141642](\images\image-20210301212141642.png)

![image-20210301212213317](\images\image-20210301212213317.png)

#### POM文件说明

![image-20210301212534147](\images\image-20210301212534147.png)

![image-20210301212556483](C:\Users\harry.cai\AppData\Roaming\Typora\typora-user-images\image-20210301212615530.png)

#### RestTemplate的使用

![image-20210301212648105](\images\image-20210301212648105.png)

##### getForObject方法/getForEntity方法

##### ![image-20210301212719686](\images\image-20210301212719686.png)

![image-20210301212738914](\images\image-20210301212738914.png)

```java
@GetMapping("/consumer/payment/get/{id}")
public CommonResult<Payment> getPaymentById(@PathVariable("id") Long id){
    return restTemplate.getForObject(PAYMENT_URL + "/payment/get/" + id, CommonResult.class, id);
}


@GetMapping("/consumer/payment/get_entity/{id}")
public CommonResult<Payment> getPaymentById2(@PathVariable("id") Long id){
    ResponseEntity<CommonResult> entity = restTemplate.getForEntity(PAYMENT_URL + "/payment/get/" + id, CommonResult.class, id);
    if(entity.getStatusCode().is2xxSuccessful()){
        return entity.getBody();
    }else {
        return new CommonResult<>(444, "操作失败");
    }
}
```

###  Ribbon核心组件IRule

IRule：根据特定算法从服务列表中选取一个需要访问的服务

![image-20210301213658131](\images\image-20210301213658131.png)

####  七大方法

IRule是一个接口，七大方法是其自带的落地实现类==

- RoundRobinRule：轮询（默认方法）
- RandomRule：随机
- AvailabilityFilteringRule：先过滤掉由于多次访问故障而处于断路器跳闸状态的服务，还有并发的连接数量超过阈值的服务，然后对剩余的服务进行轮询
- WeightedResponseTimeRule：根据平均响应时间计算服务的权重。统计信息不足时会按照轮询，统计信息足够会按照响应的时间选择服务
- RetryRule：正常时按照轮询选择服务，若过程中有服务出现故障，在轮询一定次数后依然故障，则会跳过故障的服务继续轮询。
- BestAvailableRule：先过滤掉由于多次访问故障而处于断路器跳闸状态的服务，然后选择一个并发量最小的服务
- ZoneAvoidanceRule：默认规则，符合判断server所在的区域的性能和server的可用性选择服务

#### 如何替换

修改cloud-consumer-order80

注意细节：

![image-20210301213837075](\images\image-20210301213837075.png)

新建package com.harry.myrule

上面包下新建MySelfRule规则类

```java
@Configuration
public class MySelfRule {
    @Bean
    public IRule myRule() {
        // 定义为随机
        return new RoundRobinRule();
    }
}
```

主启动类添加@RibbonClient

```java
@SpringBootApplication
@EnableEurekaClient
@RibbonClient(name = "CLOUD-PAYMENT-SERVICE", configuration = MySelfRule.class)
public class OrderMain80 {
    public static void main(String[] args) {
        SpringApplication.run(OrderMain80.class, args);
    }
}
```

### Ribbon负载均衡算法

![image-20210302192119920](\images\image-20210302192119920.png)

### 手写负载均衡算法

#### 80订单微服务改造

1.ApplicationContextBean去掉注解@LoadBalanced

2.LoadBalancer接口

```java
public interface LoadBalance {
    public ServiceInstance instances(List<ServiceInstance> serviceInstances);
}
```

3.MyLB

```java
@Component
public class MyLB implements LoadBalance {
    private AtomicInteger atomicInteger = new AtomicInteger(0);

    public final int getAndIncrement(){
        int current;
        int next;
        do {
            current = this.atomicInteger.get();
            next = current >= 2147483647 ? 0 : current +1;
        }while (this.atomicInteger.compareAndSet(current,next));
        System.out.println("****第几次访问，次数next:"+ next);
        return next;
    }

    @Override
    public ServiceInstance instances(List<ServiceInstance> serviceInstances) {
       int index = getAndIncrement() % serviceInstances.size();

       return serviceInstances.get(index);
    }
}
```

4.OrderController

```java
    @GetMapping(value = "/consumer/payment/lb")
    public String getPaymentLB(){
        List<ServiceInstance> instances = discoveryClient.getInstances("cloud-payment-service");
        if(instances == null || instances.size() <= 0){
            return null;
        }
        ServiceInstance serviceInstance = loadBalance.instances(instances);
        serviceInstance.getUri();
        return restTemplate.getForObject(PAYMENT_URL+"/payment/lb",String.class);
    }
}
```

5.测试

http://localhost/consumer/payment/lb

# 八、OpenFeign服务接口调用

### 概述

Feign是一个声明式WebService客户端，使用方法时定义一个接口并在上面添加注解即可。Feign支持可拔插式的编码器和解码器。Spring Cloud对Feign进行了封装，使其支持SpringMVC和HttpMessageConverters。Feign可以与Eureka和Ribbon组合使用以支持负载均衡。

### Feign和OpenFeign两者区别

![image-20210304191054066](\images\image-20210304191054066.png)

### OpenFeign使用步骤

接口+注解

微服务调用接口+@FeignClient

### 新建cloud-consumer-feign-order80

#### pom

```xml
<dependencies>

    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
    </dependency>
    <!--openfeign-->
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
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-jdbc</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-devtools</artifactId>
        <scope>runtime</scope>
        <optional>true</optional>
    </dependency>
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <optional>true</optional>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
    </dependency>
    <dependency>
        <groupId>com.harry.springcloud</groupId>
        <artifactId>cloud-api-common</artifactId>
        <version>1.0-SNAPSHOT</version>
    </dependency>
</dependencies>
```

#### yml

```yml
server:
  port: 80
spring:
  application:
    name: cloud-order-service
  datasource:
    type: com.alibaba.druid.pool.DruidDataSource  #当前数据源操作类型
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://192.168.30.129:3306/db2021?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: root
    password: 123456

eureka:
  client:
    register-with-eureka: true
    fetch-registry: true
    service-url:
      # 集群版
      defaultZone: http://eureka7001.com:7001/eureka,http://eureka7002.com:7002/eureka
```

#### 主启动类

```java
@SpringBootApplication
@EnableEurekaClient
@EnableFeignClients
public class OrderFeignMain80 {
    public static void main(String[] args) {
        SpringApplication.run(OrderFeignMain80.class, args);
    }
}
```

#### 业务类

业务逻辑接口+@FeignClient配置调用provider服务

新建PaymentFeignService接口并新增注解@FeignClient

```java
@FeignClient(value = "cloud-payment-service")
@Component
public interface PaymentFeignService {
    @GetMapping("/get/{id}")
    public CommonResult getPaymentById(@PathVariable("id") long id);
    /**
     * 模拟feign超时
     *
     * @return
     */
    @GetMapping(value = "/payment/feign/timeout")
    String paymentFeignTimeout();

}
```

#### 控制层

```java
@RestController
@RequestMapping("/consumer")
public class PaymentController {
    @Autowired
    private PaymentFeignService paymentFeignService;

    /**
     * 根据id查询
     *
     * @param id
     * @return
     */
    @GetMapping(value = "/payment/get/{id}")
    public CommonResult getPaymentById(@PathVariable("id") Long id) {
        return paymentFeignService.getPaymentById(id);
    }

    /**
     * 模拟feign超时
     *
     * @return
     */
    @GetMapping(value = "/payment/feign/timeout")
    public String paymentFeignTimeout() {
        // openfeign-ribbon, 客户端一般默认等待1秒钟
        return paymentFeignService.paymentFeignTimeout();
    }
}
```

####  测试

http://localhost/consumer/payment/get/31

Feign自带负载均衡配置项

### OpenFeign超时控制

![image-20210304193435020](\images\image-20210304193435020.png)

超时设置,故意设置超时演示出错情况

1.服务提供方8001故意写暂停程序

2.服务消费方80添加超时方法PaymentFeignService

3.服务消费方80添加超时方法OrderFeignController

测试：http://localhost/consumer/payment/feign/timeout

```yml
# 设置feign客户端超时时间(OpenFeign默认支持ribbon)
ribbon:
  # 指的是建立连接所用的时间,适用于网络状态正常的情况下,两端连接所用的时间
  ReadTimeout: 5000
  # 指的是建立连接后从服务器读取到可用资源所用的时间
  ConnectTimeout: 5000
```

### OpenFeign日志打印功能

![image-20210304193604789](\images\image-20210304193604789.png)

#### 日志级别

![image-20210304193634311](\images\image-20210304193634311.png)

#### 配置日志bean

```JAVA
import feign.Logger;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class FeignConfig {
    /**
     * feignClient配置日志级别
     *
     * @return
     */
    @Bean
    public Logger.Level feignLoggerLevel() {
        // 请求和响应的头信息,请求和响应的正文及元数据
        return Logger.Level.FULL;
    }
}
```

#### YML文件里需要开启日志的Feign客户端

```YML
# 设置feign客户端超时时间(OpenFeign默认支持ribbon)
ribbon:
  # 指的是建立连接所用的时间,适用于网络状态正常的情况下,两端连接所用的时间
  ReadTimeout: 5000
  # 指的是建立连接后从服务器读取到可用资源所用的时间
  ConnectTimeout: 5000
  
logging:
  level:
    # feign日志以什么级别监控哪个接口
    com.atguigu.springcloud.service.PaymentFeignService: debug
 
```

# 九、Hystrix熔断器

### 概述

### 分布式系统面临的问题

#### 扇出

多个微服务互相调用的时候，如果A调用B、C，而B、C又继续调用其他微服务，这就是扇出（像一把扇子一样慢慢打开。

#### 服务雪崩

- 扇出过程中，如果某一个环节的服务出现故障或连接超时，就会导致前面的服务占用越来越多的资源，进而引起系统崩溃，就是“雪崩效应”。
- 对于高流量的应用来说，单一的后端依赖会导致服务器所有的资源都在几秒钟内饱和。比失败更糟糕的是，这些应用程序还可能导致服务之间的延迟增加，备份队列，线程和其他系统资源紧张，导致整个系统发生更多的级联故障。这些都表示需要==对故障

![image-20210304201908291](\images\image-20210304201908291.png)

![image-20210304202022561](\images\image-20210304202022561.png)

###  Hystrix介绍

- Hystrix是一个用于处理分布式系统延迟和容错的开源库。分布式系统中，依赖避免不了调用失败，比如超时，异常等。Hystrix能保证在出现问题的时候，不会导致整体服务失败，避免级联故障，以提高分布式系统的弹性。
- Hystrix类似一个“断路器”，当系统中异常发生时，断路器给调用返回一个符合预期的，可处理的FallBack，这样就可以避免长时间无响应或抛出异常，使故障不能再系统中蔓延，造成雪崩

#### 服务熔断

- 熔断机制的注解是@HystrixCommand
- 熔断机制是应对雪崩效应的一种链路保护机制，一般存在于服务端
- 当扇出链路的某个服务出现故障或响应超时，会进行服务降级，进而熔断该节点的服务调用，快速返回“错误”的相应信息。
- Hystrix的熔断存在阈值，缺省是5秒内20次调用失败就会触发

#### 服务降级

服务器忙,请稍后再试,不让客户端等待并立刻返回一个友好提示,fallback

#### 服务限流

秒杀高并发等操作,严禁一窝蜂的过来拥挤,大家排队,一秒钟N个,有序进行

### 新建cloud-provider-hystrix-payment8001

#### POM

```XML
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

    <artifactId>cloud-provider-hystrix-payment8001</artifactId>
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
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
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-jdbc</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
            <scope>runtime</scope>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
        </dependency>
        <!--hystrix-->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
        </dependency>

        <dependency>
            <groupId>com.harry.springcloud</groupId>
            <artifactId>cloud-api-common</artifactId>
            <version>1.0-SNAPSHOT</version>
        </dependency>
    </dependencies>

</project>
```

#### YML

```YML
server:
  port: 8001
spring:
  application:
    name: cloud-provider-hystrix-payment
  datasource:
    type: com.alibaba.druid.pool.DruidDataSource  #当前数据源操作类型
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://192.168.30.129:3306/db2021?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: root
    password: 123456

mybatis:
  mapper-locations: classpath:mapper/*.xml
  type-aliases-package: com.harry.springcloud.entities

eureka:
  client:
    register-with-eureka: true
    fetch-registry: true
    service-url:
      # 集群版
      defaultZone: http://eureka7001.com:7001/eureka,http://eureka7002.com:7002/eureka
  instance:
    instance-id: payment8002
    prefer-ip-address: true # 访问路径可以显示IP
```

#### 启动类

```java
@SpringBootApplication
@EnableEurekaClient
public class PaymentHystrixMain8001 {
    public static void main(String[] args) {
        SpringApplication.run(PaymentHystrixMain8001.class, args);
    }
}
```

#### Controller

```java
package com.harry.springcloud.controller;

import com.harry.springcloud.service.PaymentService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Slf4j
public class PaymentController {
    @Autowired
    PaymentService paymentService;


    @Value("${server.port}")
    private String servicePort;

    /**
     * 正常访问
     *
     * @param id
     * @return
     */
    @GetMapping("/payment/hystrix/ok/{id}")
    public String paymentInfo_OK(@PathVariable("id") Integer id) {
        String result = paymentService.paymentInfo_OK(id);
        log.info("*****result:" + result);
        return result;
    }

}
```

#### Service

```java
package com.harry.springcloud.service;

import org.springframework.stereotype.Service;

import java.util.concurrent.TimeUnit;

@Service
public class PaymentService {
    /**
     * 正常访问
     *
     * @param id
     * @return
     */
    public String paymentInfo_OK(Integer id) {
        return "线程池:" + Thread.currentThread().getName() + " paymentInfo_OK,id:" + id + "\t" + "O(∩_∩)O哈哈~";
    }

    /**
     * 超时访问
     *
     * @param id
     * @return
     */
    public String paymentInfo_TimeOut(Integer id) {
        int timeNumber = 3;
        try {
            // 暂停3秒钟
            TimeUnit.SECONDS.sleep(timeNumber);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return "线程池:" + Thread.currentThread().getName() + " paymentInfo_TimeOut,id:" + id + "\t" +
                "O(∩_∩)O哈哈~  耗时(秒)" + timeNumber;
    }
}
```

#### 访问

success的方法

http://localhost:8001/payment/hystrix/ok/31

每次调用耗费5秒钟

http://localhost:8001/payment/hystrix/timeout/31

### 高并发测试

#### Jmeter压测测试

下载地址
https://jmeter.apache.org/download_jmeter.cgi

开启Jmeter,来20000个并发压死8001,20000个请求都去访问paymentInfo_TimeOut服务

![image-20210306103940772](\images\image-20210306103940772.png)

为什么会被卡死

tomcat的默认工作线程数被打满了,没有多余的线程来分解压力和处理

#### Jmeter压测结论

上面还只是服务提供者8001自己测试,假如此时外部的消费者80也来访问,那消费者只能干等,最终导致消费端80不满意,服务端8001直接被拖死

### 新建cloud-consumer-feign-hystrix-order80

#### POM

```XML
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

    <artifactId>cloud-consumer-feign-hystrix-order80</artifactId>

    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
        </dependency>
        <!--openfeign-->
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
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-jdbc</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
            <scope>runtime</scope>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
        </dependency>
        <dependency>
            <groupId>com.harry.springcloud</groupId>
            <artifactId>cloud-api-common</artifactId>
            <version>1.0-SNAPSHOT</version>
        </dependency>

    </dependencies>
</project>
```

#### YML

```YML
server:
  port: 80
spring:
  application:
    name: cloud-order-service
  datasource:
    type: com.alibaba.druid.pool.DruidDataSource  #当前数据源操作类型
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://192.168.30.129:3306/db2021?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: root
    password: 123456

eureka:
  client:
    register-with-eureka: true
    fetch-registry: true
    service-url:
      # 集群版
      defaultZone: http://eureka7001.com:7001/eureka,http://eureka7002.com:7002/eureka

# 设置feign客户端超时时间(OpenFeign默认支持ribbon)
ribbon:
  # 指的是建立连接所用的时间,适用于网络状态正常的情况下,两端连接所用的时间
  ReadTimeout: 5000
  # 指的是建立连接后从服务器读取到可用资源所用的时间
  ConnectTimeout: 5000

logging:
  level:
    # feign日志以什么级别监控哪个接口
    com.atguigu.springcloud.service.PaymentFeignService: debug
```

#### 启动类

```java
@SpringBootApplication
@EnableEurekaClient
@EnableFeignClients
public class OrderHystrixMain80 {
    public static void main(String[] args) {
        SpringApplication.run(OrderHystrixMain80.class, args);
    }
}
```

#### Service

```java
package com.harry.springcloud.service;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@Component
@FeignClient(value = "CLOUD-PROVIDER-HYSTRIX-PAYMENT")
public interface PaymentHystrixService {


    /**
     * 正常访问
     *
     * @param id
     * @return
     */
    @GetMapping("/payment/hystrix/ok/{id}")
    String paymentInfo_OK(@PathVariable("id") Integer id);

    /**
     * 超时访问
     *
     * @param id
     * @return
     */
    @GetMapping("/payment/hystrix/timeout/{id}")
    String paymentInfo_TimeOut(@PathVariable("id") Integer id);

}
```

#### Controller

```java
package com.harry.springcloud.controller;

import com.harry.springcloud.entities.CommonResult;
import com.harry.springcloud.service.PaymentHystrixService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Slf4j
@RequestMapping("/consumer")
public class PaymentController {

    @Autowired
    PaymentHystrixService paymentHystrixService;

    @GetMapping(value = "/payment/get/{id}")
    public String getPaymentById(@PathVariable("id") Integer id) {
        return  paymentHystrixService.paymentInfo_OK(id);
    }

    @GetMapping(value = "/hystrix/timeout/{id}")
    public String paymentFeignTimeout(@PathVariable("id") Integer id) {
        // openfeign-ribbon, 客户端一般默认等待1秒钟
        return paymentHystrixService.paymentInfo_TimeOut(id);
    }

}
```

#### 高并发测试

2w个线程压8001

消费者80微服务再去访问的OK服务8001地址

要么转圈圈，要么消费端报超时错误

![image-20210306110641645](\images\image-20210306110641645.png)

#### 故障和导致现象

8001同一层次的其他接口被困死,因为tomcat线程池里面的工作线程已经被挤占完毕

80此时调用8001,客户端访问响应缓慢,转圈圈

#### 解决

对方服务(8001)超时了,调用者(80)不能一直卡死等待,必须有服务降级

对方服务(8001)down机了,调用者(80)不能一直卡死等待,必须有服务降级

对方服务(8001)ok,调用者(80)自己有故障或有自我要求(自己的等待时间小于服务提供者)

### 服务降级

降级配置：@HystrixCommand

8001先从自身找问题，设置自身调用超时时间的峰值,峰值内可以正常运行,  超过了需要有兜底的方法处理,做服务降级fallback

8001fallback

#### 业务类启用

```java
@HystrixCommand(fallbackMethod = "payment_TimeOutHandler", 
        commandProperties = {
        @HystrixProperty(name = "execution.isolation.thread.timeoutInMilliseconds", value = "3000"),
        })
@GetMapping("/payment/hystrix/timeout/{id}")
public String paymentInfo_TimeOut(@PathVariable("id") Integer id) {
    String result = paymentService.paymentInfo_TimeOut(id);
    log.info("*****result:" + result);
    return result;
}
```

```java
public String payment_TimeOutHandler (Integer id){
    return "调用支付接口超时或异常:\t"+"\t当前线程池名字" + Thread.currentThread().getName();
}
```

#### @HystrixCommand报异常后如何处理

一旦调用服务方法失败并抛出了错误信息后,会自动调用@HystrixCommand标注好的fallbckMethod调用类中的指定方法

#### 主启动类激活@EnableCircuitBreaker

```java
@SpringBootApplication
@EnableEurekaClient
@EnableCircuitBreaker
public class PaymentHystrixMain8001 {
    public static void main(String[] args) {
        SpringApplication.run(PaymentHystrixMain8001.class, args);
    }
}
```

#### 80订单微服务,也可以更好的保护自己,自己也依样画葫芦进行客户端端降级保护

#### 80pom添加配置

```xml
<!--hystrix-->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
</dependency>
```

#### yml添加

```yml
feign:
  hystrix:
    enabled: true
```

主启动：@EnableHystrix

#### 业务类

```java
@GetMapping("/consumer/payment/hystrix/timeout/{id}")
@HystrixCommand(fallbackMethod = "paymentTimeOutFallbackMethod", commandProperties = {
        @HystrixProperty(name = "execution.isolation.thread.timeoutInMilliseconds", value = "1500")
})
public String paymentInfo_TimeOut(@PathVariable("id") Integer id) {
    //int age = 10/0;
    return paymentHystrixService.paymentInfo_TimeOut(id);
}

public String paymentTimeOutFallbackMethod(@PathVariable("id") Integer id) {
    return "我是消费者80,对方支付系统繁忙请10秒种后再试或者自己运行出错请检查自己,o(╥﹏╥)o";
}
```

#### 目前问题

每个业务方法对应一个兜底的方法,代码膨胀

统一和自定义的分开

#### 解决办法

##### 每个方法配置一个???膨胀

@DefaultProperties(defaultFallback="")

![image-20210306112904343](\images\image-20210306112904343.png)

```java
@RestController
@Slf4j
@RequestMapping("/consumer")
@DefaultProperties(defaultFallback="paymentTimeOutFallbackMethod")
public class PaymentController {

    @Autowired
    PaymentHystrixService paymentHystrixService;
    
    
    /**
     * 超时访问全局fallback
     *
     * @param id
     * @return
     */
    @GetMapping("/payment/hystrix/timeout/global/{id}")
    @HystrixCommand
    public String paymentInfo_TimeOut_Global(@PathVariable("id") Integer id) {
        int age =10/0;
        return paymentHystrixService.paymentInfo_TimeOut(id);
    }

    @GetMapping(value = "/payment/get/{id}")
    public String getPaymentById(@PathVariable("id") Integer id) {
        return  paymentHystrixService.paymentInfo_OK(id);
    }

    @GetMapping(value = "/hystrix/timeout/{id}")
    public String paymentFeignTimeout(@PathVariable("id") Integer id) {
        // openfeign-ribbon, 客户端一般默认等待1秒钟
        return paymentHystrixService.paymentInfo_TimeOut(id);
    }

    @GetMapping("/consumer/payment/hystrix/timeout/{id}")
    @HystrixCommand(fallbackMethod = "paymentTimeOutFallbackMethod", commandProperties = {
            @HystrixProperty(name = "execution.isolation.thread.timeoutInMilliseconds", value = "1500")
    })
    public String paymentInfo_TimeOut(@PathVariable("id") Integer id) {
        //int age = 10/0;
        return paymentHystrixService.paymentInfo_TimeOut(id);
    }

    public String paymentTimeOutFallbackMethod(@PathVariable("id") Integer id) {
        return "我是消费者80,对方支付系统繁忙请10秒种后再试或者自己运行出错请检查自己,o(╥﹏╥)o";
    }
    /**
     * 全局fallback
     *
     * @return
     */
    public String payment_Global_FallbackMethod() {
        return "Global异常处理信息,请稍后重试.o(╥﹏╥)o";
    }
}
```

##### 和业务逻辑混在一起???混乱

次案例服务降级处理是在客户端80实现完成,与服务端8001没有关系  只需要为Feign客户端定义的接口添加一个服务降级处理的实现类即可实现解耦

修改cloud-consumer-feign-hystrix-order80

根据cloud-consumer-feign-hystrix-order80已经有的PaymentHystrixService接口,重新新建一个类(PaymentFallbackService)实现接口,统一为接口里面的方法进行异常处理

```java
package com.harry.springcloud.service;

import org.springframework.stereotype.Component;

@Component
public class PaymentFallbackService implements PaymentHystrixService{
    @Override
    public String paymentInfo_OK(Integer id) {
        return "----PaymentFallbackService fall back--paymentInfo_OK";
    }

    @Override
    public String paymentInfo_TimeOut(Integer id) {
        return "----PaymentFallbackService fall back--paymentInfo_TimeOut";
    }
}
```

PaymentFeignClientService接口

```java
@Component
@FeignClient(value = "CLOUD-PROVIDER-HYSTRIX-PAYMENT", fallback = PaymentHystrixService.class)
public interface PaymentHystrixService {

    /**
     * 正常访问
     *
     * @param id
     * @return
     */
    @GetMapping("/payment/hystrix/ok/{id}")
    String paymentInfo_OK(@PathVariable("id") Integer id);

    /**
     * 超时访问
     *
     * @param id
     * @return
     */
    @GetMapping("/payment/hystrix/timeout/{id}")
    String paymentInfo_TimeOut(@PathVariable("id") Integer id);

}
```

##### 测试

PaymentHystrixMain8001启动

正常访问测试：http://localhost/consumer/payment/hystrix/ok/32

故意关闭微服务8001

客户端自己调用提示：此时服务端provider已经downl ,但是我们做了服务降级处理,  让客户端在服务端不可用时也会获得提示信息而不会挂起耗死服务器

### 服务熔断

#### 熔断是什么

![image-20210306121930732](\images\image-20210306121930732.png)

大神论文：https://martinfowler.com/bliki/CircuitBreaker.html

#### 修改cloud-provider-hystrix-payment8001

##### PaymentService

```java
//====服务熔断

/**
 * 在10秒窗口期中10次请求有6次是请求失败的,断路器将起作用
 *
 * @param id
 * @return
 */
@HystrixCommand(
        fallbackMethod = "paymentCircuitBreaker_fallback", commandProperties = {
        @HystrixProperty(name = "circuitBreaker.enabled", value = "true"),// 是否开启断路器
        @HystrixProperty(name = "circuitBreaker.requestVolumeThreshold", value = "10"),// 请求次数
        @HystrixProperty(name = "circuitBreaker.sleepWindowInMilliseconds", value = "10000"),// 时间窗口期/时间范文
        @HystrixProperty(name = "circuitBreaker.errorThresholdPercentage", value = "60")// 失败率达到多少后跳闸
}
)
public String paymentCircuitBreaker(@PathVariable("id") Integer id) {
    if (id < 0) {
        throw new RuntimeException("*****id不能是负数");
    }
    String serialNumber = IdUtil.simpleUUID();
    return Thread.currentThread().getName() + "\t" + "调用成功,流水号:" + serialNumber;
}

public String paymentCircuitBreaker_fallback(@PathVariable("id") Integer id) {
    return "id 不能负数,请稍后重试,o(╥﹏╥)o id:" + id;
}
```

##### PaymentController

```java
/**
 * 服务熔断
 * http://localhost:8001/payment/circuit/1
 *
 * @param id
 * @return
 */
@GetMapping("/circuit/{id}")
public String paymentCircuitBreaker(@PathVariable("id") Integer id) {
    String result = paymentService.paymentCircuitBreaker(id);
    log.info("***result:" + result);
    return result;
}
```

##### 测试

自测cloud-provider-hystrix-payment8001

正确：http://localhost:8001/payment/circuit/31

错误：http://localhost:8001/payment/circuit/-31

重点测试：多次错误,然后慢慢正确,发现刚开始不满足条件,就算是正确的访问也不能进行

##### 大神结论

![image-20210306122816911](\images\image-20210306122816911.png)

##### 熔断类型

熔断打开：请求不再调用当前服务,内部设置一般为MTTR(平均故障处理时间),当打开长达导所设时钟则进入半熔断状态

熔断关闭：熔断关闭后不会对服务进行熔断

熔断半开：部分请求根据规则调用当前服务,如果请求成功且符合规则则认为当前服务恢复正常,关闭熔断

##### 官网断路器流程图

![image-20210306124412440](\images\image-20210306124412440.png)

![image-20210306124451850](\images\image-20210306124451850.png)

##### 断路器在什么情况下开始起作用

![image-20210306124516540](\images\image-20210306124516540.png)

##### 断路器开启或者关闭的条件

当满足一定的阈值的时候(默认10秒钟超过20个请求次数)

当失败率达到一定的时候(默认10秒内超过50%的请求次数)

到达以上阈值,断路器将会开启

当开启的时候,所有请求都不会进行转发

一段时间之后(默认5秒),这个时候断路器是半开状态,会让其他一个请求进行转发. 如果成功,断路器会关闭,若失败,继续开启.重复4和5

##### 断路器打开之后

![image-20210306124634465](\images\image-20210306124634465.png)

##### ALl配置

![image-20210306124708379](\images\image-20210306124708379.png)

![image-20210306124742641](\images\image-20210306124742641.png)

![image-20210306124755587](\images\image-20210306124755587.png)

![image-20210306124808782](\images\image-20210306124808782.png)

#### 工作流程

![image-20210308185306417](\images\image-20210308185306417.png)

### 服务监控hystrixDashboard

#### 概述

![image-20210308185425991](\images\image-20210308185425991.png)

#### 新建cloud-consumer-hystrix-dashboard9001

##### pom

```xml
<dependencies>
    <!--hystrix dashboard-->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-netflix-hystrix-dashboard</artifactId>
    </dependency>
    <!--监控-->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
    <!--热部署-->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-devtools</artifactId>
        <scope>runtime</scope>
        <optional>true</optional>
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
```

##### yml

```yml
server:
  port: 9001
```

##### hystrixDashboardMain9001+新注解@EnableHystrixDashboard

```java
@SpringBootApplication
@EnableHystrixDashboard
public class hystrixDashboardMain9001 {
    public static void main(String[] args) {
        SpringApplication.run(hystrixDashboardMain9001.class, args);
    }
}
```

##### 启动该微服务后续将监控微服务8001

http://localhost:9001/hystrix

#### 修改cloud-provider-hystrix-payment8001

##### 注意:新版本Hystrix需要在主启动MainAppHystrix8001中指定监控路径

```JAVA
@SpringBootApplication
@EnableEurekaClient
@EnableCircuitBreaker
@EnableHystrixDashboard
public class PaymentHystrixMain8001 {
    public static void main(String[] args) {
        SpringApplication.run(PaymentHystrixMain8001.class, args);
    }

    /**
     * 此配置是为了服务监控而配置，与服务容错本身无观，springCloud 升级之后的坑
     * ServletRegistrationBean因为springboot的默认路径不是/hystrix.stream
     * 只要在自己的项目中配置上下面的servlet即可
     * @return
     */
    @Bean
    public ServletRegistrationBean getServlet(){
        HystrixMetricsStreamServlet streamServlet = new HystrixMetricsStreamServlet();
        ServletRegistrationBean<HystrixMetricsStreamServlet> registrationBean = new ServletRegistrationBean<>(streamServlet);
        registrationBean.setLoadOnStartup(1);
        registrationBean.addUrlMappings("/hystrix.stream");
        registrationBean.setName("HystrixMetricsStreamServlet");
        return registrationBean;
    }
}
```

##### 监控测试

9001监控8001http://localhost:8001/hystrix.stream

![image-20210308193701623](\images\image-20210308193701623.png)

如何看?

7色

![image-20210308193919993](\images\image-20210308193919993.png)

1圈

![image-20210308193940975](\images\image-20210308193940975.png)

1线

![image-20210308194001048](\images\image-20210308194001048.png)

整图说明

![image-20210308194027740](\images\image-20210308194027740.png)

![image-20210308194046695](\images\image-20210308194046695.png)

![image-20210308194112971](\images\image-20210308194112971.png)

# 十、Gateway新一代网关

### 概述

![image-20210308194320342](\images\image-20210308194320342.png)

![image-20210308194334672](\images\image-20210308194334672.png)

![image-20210308194352071](\images\image-20210308194352071.png)

![image-20210308194405627](\images\image-20210308194405627.png)

SpringCloud Gateway使用的是Webflux中的reactor-netty响应

![image-20210308194454120](\images\image-20210308194454120.png)

### 微服务架构中网关在哪里

![image-20210308194522915](\images\image-20210308194522915.png)

### 有Zuull了怎么又出来gateway

我们为什么选择Gateway?

1.netflix不太靠谱,zuul2.0一直跳票,迟迟不发布

2.SpringCloud Gateway具有如下特性

![image-20210308194627714](\images\image-20210308194627714.png)

3.SpringCloud Gateway与Zuul的区别

![image-20210308194654181](\images\image-20210308194654181.png)

#### Zuul1.x模型

![image-20210308194742604](\images\image-20210308194742604.png)

![image-20210308194802500](\images\image-20210308194802500.png)

#### Gateway模型

![image-20210308194854294](\images\image-20210308194854294.png)

### 三大核心概念

#### Route(路由)

路由是构建网关的基本模块,它由ID,目标URI,一系列的断言和过滤器组成,如断言为true则匹配该路由

#### Predicate(断言)

参考的是Java8的java.util.function.Predicate
开发人员可以匹配HTTP请求中的所有内容(例如请求头或请求参数),如果请求与断言相匹配则进行路由

#### Filter(过滤)

指的是Spring框架中GatewayFilter的实例,使用过滤器,可以在请求被路由前或者之后对请求进行修改.

#### 总结

![image-20210308195020767](\images\image-20210308195020767.png)

### Gateway工作流程

![image-20210308195059531](\images\image-20210308195059531.png)

![image-20210308195112038](\images\image-20210308195112038.png)

### 入门配置

#### cloud-gateway-gateway9527

##### pom

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-gateway</artifactId>
    </dependency>
    <!--gateway无需web和actuator-->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
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
    <dependency>
        <groupId>com.harry.springcloud</groupId>
        <artifactId>cloud-api-common</artifactId>
        <version>1.0-SNAPSHOT</version>
    </dependency>
</dependencies>
```

##### yml

```yml
server:
  port: 9527

spring:
  application:
    name: cloud-gateway
  cloud:
    gateway:
      discovery:
        locator:
          enabled: true # 开启从注册中心动态创建路由的功能，利用微服务名称j进行路由
      routes:
        - id: payment_route # 路由的id,没有规定规则但要求唯一,建议配合服务名
          #匹配后提供服务的路由地址
          #uri: http://localhost:8001
          uri: lb://cloud-payment-service
          predicates:
            - Path=/payment/get/** # 断言，路径相匹配的进行路由
              #- After=2017-01-20T17:42:47.789-07:00[America/Denver]
              #- Before=2017-01-20T17:42:47.789-07:00[America/Denver]
              #- Cookie=username,zzyy
              #- Header=X-Request-Id, \d+ #请求头要有X-Request-Id属性，并且值为正数
              #- Host=**.atguigu.com
              #- Method=GET
              #- Query=username, \d+ # 要有参数名username并且值还要是正整数才能路由
            # 过滤
            #filters:
            #  - AddRequestHeader=X-Request-red, blue
        - id: payment_route2
          #uri: http://localhost:8001
          uri: lb://cloud-payment-service
          predicates:
            Path=/payment/lb/** #断言,路径相匹配的进行路由

eureka:
  instance:
    hostname: cloud-gateway-service
  client:
    fetch-registry: true
    register-with-eureka: true
    service-url:
      defaultZone: http://eureka7001.com:7001/eureka/, http://eureka7002.com:7002/eureka/ 
```

##### 主启动类

```java
@SpringBootApplication
@EnableEurekaClient
public class GateWayMain9527 {
    public static void main(String[] args) {
        SpringApplication.run(GateWayMain9527.class, args);
    }
}
```

cloud-provider-payment8001看看controller的访问地址

我们目前不想暴露8001端口,希望在8001外面套一层9527

##### 测试

添加网关前  http://localhost:8001/payment/get/31

添加网关后 http://localhost:9527/payment/get/31

##### YML配置说明

Gateway网关路由有两种配置方式:

1.在配置文件yaml中配置

2.代码中注入RouteLocator的Bean

官网案例

![image-20210308201156798](\images\image-20210308201156798.png)

自己写一个，通过9527网关访问到外网的百度新闻网址

```java
@Configuration
public class GateWayConfig {
    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder){
        RouteLocatorBuilder.Builder routes = builder.routes();
        routes.route("path_route_harry", r -> r.path("/guonei").uri("http://news.baidu.com/guonei"));
        return routes.build();
    }
}
```

#### 通过服务名实现动态

默认情况下Gatway会根据注册中心注册的服务列表,  以注册中心上微服务名为路径创建动态路由进行转发,从而实现动态路由的功能

##### pom添加

```xml
<!--gateway无需web和actuator-->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
```

##### YML

```yml
spring:
  application:
    name: cloud-gateway
  cloud:
    gateway:
      discovery:
        locator:
          enabled: true # 开启从注册中心动态创建路由的功能，利用微服务名称j进行路由
      routes:
        - id: payment_route # 路由的id,没有规定规则但要求唯一,建议配合服务名
          #匹配后提供服务的路由地址
          #uri: http://localhost:8001
          uri: lb://cloud-payment-service
          predicates:
            - Path=/payment/get/** # 断言，路径相匹配的进行路由
              #- After=2017-01-20T17:42:47.789-07:00[America/Denver]
              #- Before=2017-01-20T17:42:47.789-07:00[America/Denver]
              #- Cookie=username,zzyy
              #- Header=X-Request-Id, \d+ #请求头要有X-Request-Id属性，并且值为正数
              #- Host=**.atguigu.com
              #- Method=GET
              #- Query=username, \d+ # 要有参数名username并且值还要是正整数才能路由
            # 过滤
            #filters:
            #  - AddRequestHeader=X-Request-red, blue
        - id: payment_route2
          #uri: http://localhost:8001
          uri: lb://cloud-payment-service
          predicates:
            Path=/payment/lb/** #断言,路径相匹配的进行路由
```

lb://serverName是spring cloud  gatway在微服务中自动为我们创建的负载均衡ur

#### Predicate

##### Route Predicate Factories这个是什么

![image-20210308202028308](\images\image-20210308202028308.png)

##### 常用的Route Predicate

![image-20210308202054129](\images\image-20210308202054129.png)

###### 1.After Route Predicate 

![image-20210308202127098](\images\image-20210308202127098.png)

![image-20210308202144471](\images\image-20210308202144471.png)

###### 2.Before Route Predicate

在某个时间之后，同上

###### 3.Between Route Predicate

在某个时间之间

###### 4.Cookie Route Predicate

![image-20210308202301457](\images\image-20210308202301457.png)

###### 5.Header Route Predicate 

![image-20210308202326264](\images\image-20210308202326264.png)

![image-20210308202357612](\images\image-20210308202357612.png)

###### 6.Host Route Predicate

![image-20210308202420209](\images\image-20210308202420209.png)

###### 7.Method Route Predicate 

![image-20210308202443840](\images\image-20210308202443840.png)

###### 8.Path Route Predicate

###### 9.Query Route Predicate

![image-20210308202525149](\images\image-20210308202525149.png)

#### Filter的使用

![image-20210308202603464](\images\image-20210308202603464.png)

##### Spring Cloud Gateway的filter

生命周期,Only Two：pre，post

种类,Only Two

GatewayFilter https://cloud.spring.io/spring-cloud-static/spring-cloud-gateway/2.2.1.RELEASE/reference/html/#gatewayfilter-factories

![image-20210308202701944](\images\image-20210308202701944.png)

GlobalFilter https://cloud.spring.io/spring-cloud-static/spring-cloud-gateway/2.2.1.RELEASE/reference/html/#global-filters

![image-20210308202741959](\images\image-20210308202741959.png)

##### 常用的GatewayFilter

#### ![image-20210308202842789](\images\image-20210308202842789.png)

##### 自定义过滤器

两个主要接口介绍 mplments GlobalFilter,Ordered

###### 案例代码

```JAVA
@Component
@Slf4j
public class MyLogGatewayFilter implements GlobalFilter, Ordered {
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        log.info("come in global filter: {}", new Date());
        ServerHttpRequest request = exchange.getRequest();
        String username = request.getQueryParams().getFirst("username");
        if (username == null){
            log.info("用户名为null，非法用户");
            exchange.getResponse().setStatusCode(HttpStatus.NOT_ACCEPTABLE);
            return exchange.getResponse().setComplete();
        }
        // 放行
        return chain.filter(exchange);
    }

    /**
     * 过滤器加载的顺序 越小,优先级别越高
     *
     * @return
     */
    @Override
    public int getOrder() {
        return 0;
    }
}
```

测试

正确：http://localhost:9527/payment/lb?username=z3

错误： http://localhost:9527/payment/lb

# 十一、SpringCloud config分布式配置中心

### 概述

![image-20210310194052380](\images\image-20210310194052380.png)

![image-20210310194146090](\images\image-20210310194146090.png)

![image-20210310194200670](C:\Users\harry.cai\AppData\Roaming\Typora\typora-user-images\image-20210310194200670.png)

#### 能干嘛

集中管理配置文件

不同环境不同配置，动态化的配置更新，分环境比如dev/test/prod/beta/release

运行期间动态调整配置，不再需要在每个服务部署的机器上编写配置文件，服务会向配置中心同意拉去配置自己的信息

当配置发生改变时，服务不需要重启即可感知到配置的变化并应用新的配置

将配置信息以REST接口的形式暴露

### Config服务端配置与测试

用你自己的账号在GitHub上新建一个名为springcloud-config的新Repository

由上一步获得刚新建的git地址

本地硬盘目录上新建git仓库并clone

此时在本地盘符下的文件

#### 新建Module模块cloud-config-center-3344，它即为Cloud的配置中心模块cloudConfig Center

##### pom

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

    <artifactId>cloud-config-center-3344</artifactId>

    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-bus-amqp</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-config-server</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
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
  port: 3344

spring:
  application:
    name: cloud-config-center
  cloud:
    config:
      server:
        git:
          #          skipSslValidation: true # 跳过ssl认证
          uri: https://github.com/cs4224485/springcloud-config.git
          ### 搜索目录
          search-paths:
            - springcloud-config
      ### 读取分支
      label: master


eureka:
  client:
    service-url:
      defaultZone: http://eureka7001.com:7001/eureka
      
#暴露监控端点
management:
  endpoints:
    web:
      exposure:
        include: "*"
```

##### 主启动类

```java
package com.harry.springcloud;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.config.server.EnableConfigServer;

@SpringBootApplication
@EnableConfigServer
public class MainConfigCenter3344 {
    public static void main(String[] args) {
        SpringApplication.run(MainConfigCenter3344.class, args);
    }
}
```

##### windows下修改hosts文件，增加映射

127.0.0.1 config-3344.com

##### 测试通过Config微服务是否可以从GitHub是否可以从GitHub上获取配置内容

http://config-3344.com:3344/master/config-dev.yml

#### 读取配置规则

/{label}/{application}-{profile}.yml

/{application}-{profile}.yml

/{application}/{profile}/{/label}

![image-20210310204519232](\images\image-20210310204519232.png)

### Config客户端配置与测试

#### 新建cloud-config-client-3355

##### POM

```XML
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

    <artifactId>cloud-config-client-3355</artifactId>

    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-bus-amqp</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-config</artifactId>
            <version>2.2.2.RELEASE</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
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

##### bootstrap.yml

```yml
server:
  port: 3355

spring:
  application:
    name: config-client
  cloud:
    config:
      label: master # 分支名称
      name: config #配置文件名称
      profile: dev # 读取的后缀，上述三个综合，为master分支上的config-dev.yml的配置文件被读取，http://config-3344.com:3344/master/config-dev.yml
      uri: http://localhost:3344 #配置中心的地址


eureka:
  client:
    service-url:
      defaultZone: http://eureka7001.com:7001/eureka
      
#暴露监控端点
management:
  endpoints:
    web:
      exposure:
        include: "*"
```

##### 修改config-dev.yml配置并提交到GitHub中，比如加个变量age或者版本号version

##### 主启动

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;

@SpringBootApplication
@EnableEurekaClient
public class ConfigClientMain3355 {
    public static void main(String[] args) {
        SpringApplication.run(ConfigClientMain3355.class, args);
    }
}
```

##### 业务类

```java
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RefreshScope
public class ConfigClientController {

    @Value("${config.info}")
    private String configInfo;

    @GetMapping("/configInfo")
    public String getConfigInfo() {
        return configInfo;
    }
}
```

成功实现了客户端3355访问SpringCloud Config3344通过GitHub获取信息配置

### Config客户端之动态刷新

避免每次更新配置都要重启客户端服务3355

#### 动态刷新

修改3355模块

POM引入actuator监控

修改YML，暴露监控端口

@refreshScope业务类Controller修改

此时修改github3344--->3355

需要运维发送Post请求刷新3355 curl -X POST "http://localhost:3355/actuator/refresh"

# 十二、SpringCloud Bus消息总线

#### 概述

![image-20210310205924100](\images\image-20210310205924100.png)

Bus支持两种消息代理:RabbitMQ和Kafka

作用

![image-20210310205950785](\images\image-20210310205950785.png)

![image-20210310210012282](\images\image-20210310210012282.png)

#### RabbitMQ环境配置

安装Elang，下载地址：https://www.erlang.org/downloads

安装RabbitMQ，下载地址：https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.8.3/rabbitmq-server-3.8.3.exe

进入RabbitMQ安装目录下的sbin目录

输入以下命令启动管理功能：

​	rabbitmq-plugins enable rabbitmq_management

访问地址看是否成功安装：http://localhost:15672

输入账号并登录 guest guest

#### SpringCloud Bus动态刷新全局广播

演示广播效果，增加复杂度，再以3355位模板制作一个3366

设计思想

​	1.利用消息总线触发一个客户端/bus/refresh，从而刷新所有客户端配置

![image-20210310211245507](\images\image-20210310211245507.png)2.利用消息总线触发一个服务端ConfigServer的/bus/refresh端点，从而刷新所有客户端配置

![image-20210310211326207](\images\image-20210310211326207.png)

图二的架构显然更加合适，图一不合适原因如下：

​	打破了微服务的职责单一性，因为微服务本身是业务模块，它本不应该承担配置刷新的职责

​	破坏了微服务各节点的对等性

​	有一定的局限性，例如，微服务在迁移时，它的网络地址常常会发生变化，此时如果想要做到自动刷新那就会增加更多的修改

#### 给cloud-config-center-3344配置中心服务端添加消息总线支持

```yml
server:
  port: 3344

spring:
  application:
    name: cloud-config-center
  cloud:
    config:
      server:
        git:
          #          skipSslValidation: true # 跳过ssl认证
          uri: https://github.com/cs4224485/springcloud-config.git
          ### 搜索目录
          search-paths:
            - springcloud-config
      ### 读取分支
      label: master

eureka:
  client:
    service-url:
      defaultZone: http://eureka7001.com:7001/eureka

rabbitmq: #rabbitmq相关配置，15672是web管理端口，5672是mq访问端口
  port: 5672
  host: localhost
  username: guest
  password: guest

#暴露监控端点
management:
  endpoints:
    web:
      exposure:
        include: "*"
```

#### 给cloud-config-center-3355配置中心服务端添加消息总线支持

```yml
server:
  port: 3355

spring:
  application:
    name: config-client
  cloud:
    config:
      label: master # 分支名称
      name: config #配置文件名称
      profile: dev # 读取的后缀，上述三个综合，为master分支上的config-dev.yml的配置文件被读取，http://config-3344.com:3344/master/config-dev.yml
      uri: http://localhost:3344 #配置中心的地址


eureka:
  client:
    service-url:
      defaultZone: http://eureka7001.com:7001/eureka

rabbitmq: #rabbitmq相关配置，15672是web管理端口，5672是mq访问端口
  port: 5672
  host: localhost
  username: guest
  password: guest

#暴露监控端点
management:
  endpoints:
    web:
      exposure:
        include: "*"
```

#### 给cloud-config-center-3366配置中心服务端添加消息总线支持

```yml
server:
  port: 3366

spring:
  application:
    name: cloud-config-center
  cloud:
    config:
      server:
        git:
          #          skipSslValidation: true # 跳过ssl认证
          uri: https://github.com/cs4224485/springcloud-config.git
          ### 搜索目录
          search-paths:
            - springcloud-config
      ### 读取分支
      label: master

eureka:
  client:
    service-url:
      defaultZone: http://eureka7001.com:7001/eureka

rabbitmq: #rabbitmq相关配置，15672是web管理端口，5672是mq访问端口
  port: 5672
  host: localhost
  username: guest
  password: guest

#暴露监控端点
management:
  endpoints:
    web:
      exposure:
        include: "*"
```

#### 测试

发送Post请求 curl -X POST "http://localhost:3344/actuator/bus-refresh"

http://lconfig-3344.com:3344/config-dev.yml     一次发送，处处生效

#### SpringCloud Bus动态刷新定点通知

不想全部通知，只想定点通知， 只通知3355

定某一实例生效而不是全部， 公式：http://localhost:3344/actutor/bus-refresh/{destination}，/bus/refresh请求不再发送到具体的服务实力上，而是发给config server通过destination参数指定需要更新配置的服务或实例

curl -X POST "http://localhost:3344/actuator/bus-refresh/config-client:3355"

通知总结All

![image-20210311192739384](\images\image-20210311192739384.png)



# 十三、SpringCloud Stream消息驱动

#### 消息驱动概述

![image-20210311193803644](\images\image-20210311193803644.png)

屏蔽底层消息中间件的差异，降低切换成本，统一消息的编程模型

官网：https://spring.io/projects/spring-cloud-stream

Spring Cloud Stream中文指导手册：https://blog.csdn.net/qq_32734365/article/details/81413218#spring-cloud-stream%E4%B8%AD%E6%96%87%E6%8C%87%E5%AF%BC%E6%89%8B%E5%86%8C

#### 设计思想

##### 标准MQ

![image-20210311193926003](\images\image-20210311193926003.png)

生产者/消费者之间靠消息媒介传递信息内容   Message

消息必须走特定的通道	消息通道MessageChannel

消息通道里的消息如何被消费呢，谁负责收发处理	消息通道MessageChannel的子接口SubscribableChannel，由MessageHandler消息处理器所订阅

##### 为什么使用Cloud Stream

#### ![image-20210311194110515](\images\image-20210311194110515.png)

![image-20210311194126581](\images\image-20210311194126581.png)

![image-20210311194142275](\images\image-20210311194142275.png)

Stream中的消息通信方式遵循了发布-订阅模式，在RabbitMQ就是Exchange，在Kafka中就是Topic。

##### pring Cloud Stream标准流程套路

Binder：很方便的连接中间件，屏蔽差异

Channel: 通道，是队列Queue的一种抽象，在消息通讯系统中就是实现存储和转发的媒介，通过Channel对队列进行配置

Source和Sink: 简单的可以理解为参照对象是Spring Cloud Stream 自身，从Stream发布消息就是输出，接受消息就是输入

编码API和常用注解

![image-20210311194408660](\images\image-20210311194408660.png)

#### 消息驱动之生产者cloud-stream-rabbitmq-provider8801

##### pom

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

    <artifactId>cloud-stream-rabbitmq-provider8801</artifactId>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-stream-rabbit</artifactId>
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
  port: 8801

spring:
  application:
    name: cloud-stream-provider
  cloud:
    stream:
      binders: # 在此处配置要绑定的rabbitMQ的服务信息
        defaultRabbit: # 表示定义的名称，用于binding的整合
          type: rabbit # 消息中间件类型
          environment: # 设置rabbitMQ的相关环境配置
            spring:
              rabbitmq:
                host: localhost
                port: 5672
                username: guest
                password: guest
      bindings: # 服务的整合处理
        output: # 这个名字是一个通道的名称
          destination: studyExchange # 表示要使用的exchange名称定义
          content-type: application/json # 设置消息类型，本次为json，文本则设为text/plain
          binder: defaultRabbit # 设置要绑定的消息服务的具体设置

eureka:
  client:
    service-url:
      defaultZone: http://eureka7001.com:7001/eureka
  instance:
    lease-renewal-interval-in-seconds: 2 # 设置心跳的间隔时间，默认30
    lease-expiration-duration-in-seconds: 5 # 超过5秒间隔，默认90
    instance-id: send-8801.com # 主机名
    prefer-ip-address: true # 显示ip
```

##### 启动类

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class StreamMQMain8801 {
    public static void main(String[] args) {
        SpringApplication.run(StreamMQMain8801.class, args);
    }
}
```

##### service

```java
import com.harry.springcloud.service.IMessageProvider;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cloud.stream.annotation.EnableBinding;
import org.springframework.cloud.stream.messaging.Source;
import org.springframework.messaging.MessageChannel;
import org.springframework.messaging.support.MessageBuilder;

@EnableBinding(Source.class)
public class MessageProviderImpl implements IMessageProvider {
    @Autowired
    private MessageChannel output;

    @Override
    public String send() {
        String serial = UUID.randomUUID().toString();
        output.send(MessageBuilder.withPayload(serial).build());
        System.out.println("*****serial***" + serial);
        return serial;
    }
}
```

##### controller

```java
@RestController
public class SendMessageController {
    @Autowired
    private IMessageProvider messageProvider;

    @GetMapping("/sendMessage")
    public String send() {
        return messageProvider.send();
    }
}
```

#### 消息驱动之消费者cloud-stream-rabbitmq-consumer8802

##### pom

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

    <artifactId>cloud-stream-rabbitmq-consumer8802</artifactId>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-stream-rabbit</artifactId>
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
  port: 8802

spring:
  application:
    name: cloud-stream-consumer
  cloud:
    stream:
      binders: # 在此处配置要绑定的rabbitMQ的服务信息
        defaultRabbit: # 表示定义的名称，用于binding的整合
          type: rabbit # 消息中间件类型
          environment: # 设置rabbitMQ的相关环境配置
            spring:
              rabbitmq:
                host: localhost
                port: 5672
                username: guest
                password: guest
      bindings: # 服务的整合处理
        input: # 这个名字是一个通道的名称
          destination: studyExchange # 表示要使用的exchange名称定义
          content-type: application/json # 设置消息类型，本次为json，文本则设为text/plain
          binder: defaultRabbit # 设置要绑定的消息服务的具体设置
          group: yangluyaoA # 不同的组存在重复消费，相同的组之间竞争消费。

eureka:
  client:
    service-url:
      defaultZone: http://eureka7001.com:7001/eureka
  instance:
    lease-renewal-interval-in-seconds: 2 # 设置心跳的间隔时间，默认30
    lease-expiration-duration-in-seconds: 5 # 超过5秒间隔，默认90
    instance-id: receive-8802.com #主机名
    prefer-ip-address: true # 显示ip
```

##### controller

```jade
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.stream.annotation.EnableBinding;
import org.springframework.cloud.stream.annotation.StreamListener;
import org.springframework.cloud.stream.messaging.Sink;
import org.springframework.messaging.Message;
import org.springframework.stereotype.Component;

@Component
@EnableBinding(Sink.class)
public class ReceiveMessageListenerController {

    @Value("${server.port}")
    private String serverPort;

    @StreamListener(Sink.INPUT)
    public void input(Message<String> message) {
        System.out.println("消费者1，-------" + message.getPayload() + "\t port:" + serverPort);
    }

}
```

cloud-stream-rabbitmq-consumer8803 同上

#### 分组消费与持久化

目前是8802/8803同时收到了，存在重复消费问题

分组和持久化属性group 生产实际案例

![image-20210313111611030](\images\image-20210313111611030.png)

同一组内会发生竞争关系，只有其中一个可以消费

##### 分组

微服务应用放置于同一个group中，就能够保证消息只会被其中一个应用消费一次。不同的组是可以消费的，同一个组内会发生竞争关系，只有其中一个可以消费

8802/8803都变成不同组，group两个不同

group：HarryA，HarryA

8802/8803实现了轮询分组，每次只有一个消费者，8801模块的发的消息只能被8802或8803其中一个接收到，这样避免了重复消费

##### 持久化

停止8802/8803并去除掉8802分组group：HarryA

8801先发送4条消息到rabbitmq

先启动8802，无分组属性配置，后台没有打出来消息

再启动8803，无分组属性配置，后台打出来了MQ上的消息

# 十四、SpringCloud Sleuth分布式链路跟踪

#### 概述

为什么会出现这个技术？需要解决哪些问题？

![image-20210313112052478](\images\image-20210313112052478.png)

https://cloud.spring.io/spring-cloud-sleuth/reference/html/

spring Cloud Sleuth提供了一套完整的服务跟踪的解决方案,在分布式系统中提供追踪解决方案并且兼容支持了zipkin

![image-20210313112134802](\images\image-20210313112134802.png)

#### 搭建链路监控步骤

1、SpringCloud从F版已不需要自己构建Zipkin Server了，只需要调用jar包即可，https://dl.bintray.com/openzipkin/maven/io/zipkin/java/zipkin-server/

​	 运行命令：java -jar zipkin-server-2.12.9-exec.jar

​	 运行控制台： http://localhost:9411/zipkin/

​	![image-20210313112339503](\images\image-20210313112339503.png)

![image-20210313112359145](images\image-20210313112359145.png)

Trace：类似于树结构的Span结合，表示一条调用链路，存在唯一标识

span：标识调用链路来源，通俗的理解span就是一次请求信息

2.服务提供者

3.服务消费者

4.依次启动eureka7001/8001/80，80调用8001几次测试下

5.打开浏览器访问http://localhost:9411

会出现以下界面

![image-20210313112524509](\images\image-20210313112524509.png)

