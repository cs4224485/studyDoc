# 一 基础知识

## 分布式基础理论

### 什么是分布式系统？

分布式系统原理与范型》定义：

“分布式系统是若干独立计算机的集合，这些计算机对于用户来说就像单个相关系统”

分布式系统（distributed system）是建立在网络之上的软件系统。

随着互联网的发展，网站应用的规模不断扩大，常规的垂直应用架构已无法应对，分布式服务架构以及流动计算架构势在必行，亟需**一个治理系统**确保架构有条不紊的演进。

### 发展演变

![image-20220607174621949](images\image-20220607174621949.png)

#### 单一应用架构

当网站流量很小时，只需一个应用，将所有功能都部署在一起，以减少部署节点和成本。此时，用于简化增删改查工作量的数据访问框架(ORM)是关键。

![image-20220607174704948](images\image-20220607174704948.png)

适用于小型网站，小型管理系统，将所有功能都部署到一个功能里，简单易用。

缺点： 1、性能扩展比较难

​             2、协同开发问题

​            3、不利于升级维护

#### 垂直应用架构

当访问量逐渐增大，单一应用增加机器带来的加速度越来越小，将应用拆成互不相干的几个应用，以提升效率。此时，用于加速前端页面开发的Web框架(MVC)是关键。

![image-20220607174757454](images\image-20220607174757454.png)

通过切分业务来实现各个模块独立部署，降低了维护和部署的难度，团队各司其职更易管理，性能扩展也更方便，更有针对性。

缺点： 公用模块无法重复利用，开发性的浪费

#### 分布式服务架构

当垂直应用越来越多，应用之间交互不可避免，将核心业务抽取出来，作为独立的服务，逐渐形成稳定的服务中心，使前端应用能更快速的响应多变的市场需求。此时，用于提高业务复用及整合的**分布式服务框架**(RPC)是关键。

![image-20220607174911630](images\image-20220607174911630.png)

#### 流动计算架构

当服务越来越多，容量的评估，小服务资源的浪费等问题逐渐显现，此时需增加一个调度中心基于访问压力实时管理集群容量，提高集群利用率。此时，用于**提高机器利用率的资源调度和治理中心**(SOA)[ Service Oriented Architecture]是关键。

![image-20220607175009455](images\image-20220607175009455.png)

### RPC

#### 什么叫RPC

RPC【Remote Procedure Call】是指远程过程调用，是一种进程间通信方式，他是一种技术的思想，而不是规范。它允许程序调用另一个地址空间（通常是共享网络的另一台机器上）的过程或函数，而不用程序员显式编码这个远程调用的细节。即程序员无论是调用本地的还是远程的函数，本质上编写的调用代码基本相同。

#### RPC基本原理

![image-20220607175102306](images\image-20220607175102306.png)

![image-20220607175120932](images\image-20220607175120932.png)

## dubbo核心概念

### 简介

Apache Dubbo (incubating) |ˈdʌbəʊ| 是一款高性能、轻量级的开源Java RPC框架，它提供了三大核心能力：面向接口的远程方法调用，智能容错和负载均衡，以及服务自动注册和发现。

官网：

http://dubbo.apache.org/

### 基本概念

![image-20220607175404123](images\image-20220607175404123.png)

​	**服务提供者（Provider**）：暴露服务的服务提供方，服务提供者在启动时，向注册中心注册自己提供的服务。

​    **服务消费者（Consumer**）: 调用远程服务的服务消费方，服务消费者在启动时，向注册中心订阅自己所需的服务，服务消费者，从提供者地址列表中，基于软负载均衡算法，选一台提供者进行调用，如果调用失败，再选另一台调用。

​    **注册中心（Registry**）：注册中心返回服务提供者地址列表给消费者，如果有变更，注册中心将基于长连接推送变更数据给消费者

​    **监控中心（Monitor**）：服务消费者和提供者，在内存中累计调用次数和调用时间，定时每分钟发送一次统计数据到监控中心

调用关系说明

​	服务容器负责启动，加载，运行服务提供者。

​	服务提供者在启动时，向注册中心注册自己提供的服务。

​	服务消费者在启动时，向注册中心订阅自己所需的服务。

​	注册中心返回服务提供者地址列表给消费者，如果有变更，注册中心将基于长连接推送变更数据给消费者。

​	服务消费者，从提供者地址列表中，基于软负载均衡算法，选一台提供者进行调用，如果调用失败，再选另一台调用。

   服务消费者和提供者，在内存中累计调用次数和调用时间，定时每分钟发送一次统计数据到监控中心。

## dubbo环境搭建

### 【windows】-安装zookeeper

##### 1、下载zookeeper

网址 https://archive.apache.org/dist/zookeeper/zookeeper-3.4.13/

##### 2、解压zookeeper

解压运行zkServer.cmd ，初次运行会报错，没有zoo.cfg配置文件

##### 3、修改zoo.cfg配置文件

将conf下的zoo_sample.cfg复制一份改名为zoo.cfg即可。

注意几个重要位置：

dataDir=./  临时数据存储的目录（可写相对路径）

clientPort=2181  zookeeper的端口号

修改完成后再次启动zookeeper

##### 4、使用zkCli.cmd测试

ls /：列出zookeeper根下保存的所有节点

create –e /atguigu 123：创建一个atguigu节点，值为123

get /atguigu：获取/atguigu节点的值

### 【windows】-安装dubbo-admin管理控制台

dubbo本身并不是一个服务软件。它其实就是一个jar包能够帮你的java程序连接到zookeeper，并利用zookeeper消费、提供服务。所以你不用在Linux上启动什么dubbo服务。

但是为了让用户更好的管理监控众多的dubbo服务，官方提供了一个可视化的监控程序，不过这个监控即使不装也不影响使用。

##### 1、下载dubbo-admin

https://github.com/apache/incubator-dubbo-ops

![image-20220607180528307](images\image-20220607180528307.png)

##### 2、进入目录，修改dubbo-admin配置

修改 src\main\resources\application.properties 指定zookeeper地址

![image-20220607180558966](images\image-20220607180558966.png)

##### 3、打包dubbo-admin

mvn clean package -Dmaven.test.skip=true 

##### 4、运行dubbo-admin

java -jar dubbo-admin-0.0.1-SNAPSHOT.jar

**注意：【有可能控制台看着启动了，但是网页打不开，需要在控制台按下**ctrl+c即可】

默认使用root/root 登陆

### 【linux】-安装zookeeper

#### 1、安装jdk

##### 1、下载jdk

http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

![image-20220607180803047](images\image-20220607180803047.png)

##### 2、上传到服务器并解压

![image-20220607180909287](images\image-20220607180909287.png)

##### 3、设置环境变量

```
/usr/local/java/jdk1.8.0_171
 
文件末尾加入下面配置
export JAVA_HOME=/usr/local/java/jdk1.8.0_171
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH

```

![image-20220607180940956](images\image-20220607180940956.png)

##### 4、使环境变量生效&测试JDK

![image-20220607181014844](images\image-20220607181014844.png)

#### 2、安装zookeeper

##### 1、下载zookeeper

网址 https://archive.apache.org/dist/zookeeper/zookeeper-3.4.11/

wget https://archive.apache.org/dist/zookeeper/zookeeper-3.4.11/zookeeper-3.4.11.tar.gz

##### 2、解压

```
[root@MiWiFi-R4AC-srv soft]# tar zxvf zookeeper-3.4.11.tar.gz
```

##### 3、移动到指定位置并改名为zookeeper

![image-20220607182156371](images\image-20220607182156371.png)

#### 3、开机启动zookeeper

1）-复制如下脚本

```bash
#!/bin/bash
#chkconfig:2345 20 90
#description:zookeeper
#processname:zookeeper
ZK_PATH=/usr/local/zookeeper
export JAVA_HOME=/usr/local/java/jdk1.8.0_171
case $1 in
         start) sh  $ZK_PATH/bin/zkServer.sh start;;
         stop)  sh  $ZK_PATH/bin/zkServer.sh stop;;
         status) sh  $ZK_PATH/bin/zkServer.sh status;;
         restart) sh $ZK_PATH/bin/zkServer.sh restart;;
         *)  echo "require start|stop|status|restart"  ;;
esac

```



2）-把脚本注册为Service

![image-20220607182419182](images\image-20220607182419182.png)

3）-增加权限

![image-20220607182437023](images\image-20220607182437023.png)

#### 4、配置zookeeper

##### 1、初始化zookeeper配置文件

拷贝/usr/local/zookeeper/conf/zoo_sample.cfg  

到同一个目录下改个名字叫zoo.cfg

##### 2、启动zookeeper

![image-20220607182627191](images\image-20220607182627191.png)

![image-20220607182747406](images\image-20220607182747406.png)

### 【linux】-安装dubbo-admin管理控制台

#### 1、安装Tomcat8（旧版dubbo-admin是war，新版是jar不需要安装Tomcat）

##### 1、下载Tomcat8并解压

https://tomcat.apache.org/download-80.cgi

wget http://mirrors.shu.edu.cn/apache/tomcat/tomcat-8/v8.5.32/bin/apache-tomcat-8.5.32.tar.gz

##### 2、解压移动到指定位置



##### 3、开机启动tomcat8

![image-20220607182925379](images\image-20220607182925379.png)

```bash
#!/bin/bash
#chkconfig:2345 21 90
#description:apache-tomcat-8
#processname:apache-tomcat-8
CATALANA_HOME=/opt/apache-tomcat-8.5.32
export JAVA_HOME=/opt/java/jdk1.8.0_171
case $1 in
start)
    echo "Starting Tomcat..."  
    $CATALANA_HOME/bin/startup.sh
    ;;

stop)
    echo "Stopping Tomcat..."  
    $CATALANA_HOME/bin/shutdown.sh
    ;;

restart)
    echo "Stopping Tomcat..."  
    $CATALANA_HOME/bin/shutdown.sh
    sleep 2
    echo  
    echo "Starting Tomcat..."  
    $CATALANA_HOME/bin/startup.sh
    ;;
*)
    echo "Usage: tomcat {start|stop|restart}"  
    ;; esac

```

##### 4、注册服务&添加权限

![image-20220607183033578](images\image-20220607183033578.png)

##### 5、启动服务&访问tomcat测试

![image-20220607183050822](images\image-20220607183050822.png)

#### 2、安装dubbo-admin

dubbo本身并不是一个服务软件。它其实就是一个jar包能够帮你的java程序连接到zookeeper，并利用zookeeper消费、提供服务。所以你不用在Linux上启动什么dubbo服务。

但是为了让用户更好的管理监控众多的dubbo服务，官方提供了一个可视化的监控程序，不过这个监控即使不装也不影响使用。

##### 1、下载dubbo-admin

https://github.com/apache/incubator-dubbo-ops

![image-20220607183136982](images\image-20220607183136982.png)

##### 2、进入目录，修改dubbo-admin配置

修改 src\main\resources\application.properties 指定zookeeper地址



##### 3、打包dubbo-admin

mvn clean package -Dmaven.test.skip=true 

##### 4、运行dubbo-admin

java -jar dubbo-admin-0.0.1-SNAPSHOT.jar

默认使用root/root 登陆

![image-20220607193008561](images\image-20220607193008561.png)

![image-20220607193242735](images\image-20220607193242735.png)

## dubbo-helloworld

### 提出需求

某个电商系统，订单服务需要调用用户服务获取某个用户的所有地址；

我们现在 需要创建两个服务模块进行测试 

| 模块                | 功能           |
| ------------------- | -------------- |
| 订单服务web模块     | 创建订单等     |
| 用户服务service模块 | 查询用户地址等 |

测试预期结果：

订单服务web模块在A服务器，用户服务模块在B服务器，A可以远程调用B的功能。

### 工程架构

根据 dubbo《服务化最佳实践》

#### 分包

建议将服务接口，服务模型，服务异常等均放在 API 包中，因为服务模型及异常也是 API 的一部分，同时，这样做也符合分包原则：重用发布等价原则(REP)，共同重用原则(CRP)。

如果需要，也可以考虑在 API 包中放置一份 spring 的引用配置，这样使用方，只需在 spring 加载过程中引用此配置即可，配置建议放在模块的包目录下，以免冲突，如：com/alibaba/china/xxx/dubbo-reference.xml。

#### 粒度

服务接口尽可能大粒度，每个服务方法应代表一个功能，而不是某功能的一个步骤，否则将面临分布式事务问题，Dubbo 暂未提供分布式事务支持。

服务接口建议以业务场景为单位划分，并对相近业务做抽象，防止接口数量爆炸。

不建议使用过于抽象的通用接口，如：Map query(Map)，这样的接口没有明确语义，会给后期维护带来不便。

![image-20220607193431070](images\image-20220607193431070.png)

### 创建模块

#### gmall-interface：公共接口层（model，service，exception…）

UserService

```java
package com.harry.dubbo.service;

import com.harry.dubbo.bean.UserAddress;

import java.util.List;

public interface UserService {
    public List<UserAddress> getUserAddressList(String userId);
}

```

 UserAddress

```java
package com.harry.dubbo.bean;

import com.sun.tracing.dtrace.ArgsAttributes;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class UserAddress implements Serializable {
    private Integer id;
    private String userAddress;
    private String userId;
    private String consignee;
    private String phoneNum;
    private String isDefault;
}

```

#### gmall-user：用户模块（对用户接口的实现）

pom

```XML
    <dependencies>
        <dependency>
            <groupId>com.harry.dubbo</groupId>
            <artifactId>gmall-interface</artifactId>
            <version>1.0-SNAPSHOT</version>
        </dependency>
    </dependencies>
```



Service

```java
package com.harry.dubbo.service;

import com.harry.dubbo.bean.UserAddress;
import com.harry.dubbo.dao.userAddressDao;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

public class UserServiceImpl implements UserService{

    @Autowired
    userAddressDao userAddressDao;

    @Override
    public List<UserAddress> getUserAddressList(String userId) {
        return userAddressDao.getUserAddressById(userId);
    }
}

```



dao

```java
public class userAddressDao {
    public static List<UserAddress> userAddresses = new ArrayList<>(); 
    static{

        userAddresses.add(new UserAddress(1, "西安高新区", "id-1", "harry", "18629090745", "1"));
        userAddresses.add(new UserAddress(2, "北京海淀区", "id-2", "sam", "18629090745", "0"));
    }
    
    public List<UserAddress> getUserAddressById(String userId){
        return userAddresses;
    }

}

```

#### gmall-order-web：订单模块（调用用户模块）

pom

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <parent>
        <artifactId>DubboDemon</artifactId>
        <groupId>org.example</groupId>
        <version>1.0-SNAPSHOT</version>
    </parent>
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.harry.dubbo</groupId>
    <artifactId>gmall-order-web</artifactId>
    <dependencies>
        <dependency>
            <groupId>com.harry.dubbo</groupId>
            <artifactId>gmall-interface</artifactId>
            <version>1.0-SNAPSHOT</version>
        </dependency>
    </dependencies>

    <properties>
        <maven.compiler.source>8</maven.compiler.source>
        <maven.compiler.target>8</maven.compiler.target>
    </properties>

</project>
```

service

```java
package com.harry.dubbo.service;

import com.harry.dubbo.bean.UserAddress;

import java.util.List;

public class OrderService {
    UserService userService;

    /**
     * 初始化订单，查询用户的所有地址并返回
     * @param userId
     * @return
     */
    public List<UserAddress> initOrder(String userId){
        return userService.getUserAddressList(userId);
    }

}

```

现在这样是无法进行调用的。我们gmall-order-web引入了gmall-interface，但是interface的实现是gmall-user，我们并没有引入，而且实际他可能还在别的服务器中。

### 使用dubbo改造

#### 改造gmall-user作为服务提供者

```xml
    <dependencies>
        <dependency>
            <groupId>com.harry.dubbo</groupId>
            <artifactId>gmall-interface</artifactId>
            <version>1.0-SNAPSHOT</version>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-core</artifactId>
            <version>5.2.2.RELEASE</version>
        </dependency>
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>dubbo</artifactId>
            <version>2.6.2</version>
        </dependency>

    </dependencies>
```

配置提供者spring-beans

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:dubbo="http://dubbo.apache.org/schema/dubbo"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
		http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-4.3.xsd
		http://dubbo.apache.org/schema/dubbo http://dubbo.apache.org/schema/dubbo/dubbo.xsd
		http://code.alibabatech.com/schema/dubbo http://code.alibabatech.com/schema/dubbo/dubbo.xsd">

    <context:component-scan base-package="com.harry.dubbo"/>
    <bean id="userServiceImpl" class="com.harry.dubbo.service.UserServiceImpl"></bean>
    <!--当前应用的名字  -->
    <dubbo:application name="gmall-user"></dubbo:application>
    <!--指定注册中心的地址  -->
    <dubbo:registry address="zookeeper://192.168.31.96:2181" />
    <!--使用dubbo协议，将服务暴露在20880端口  -->
    <dubbo:protocol name="dubbo" port="20880" />
    <!-- 指定需要暴露的服务 -->
    <dubbo:service interface="com.harry.dubbo.service.UserService" ref="userServiceImpl" />

</beans>



```

启动服务

```java

public class Application {
    public static void main(String[] args) throws IOException {
        ClassPathXmlApplicationContext context =
                new ClassPathXmlApplicationContext("classpath:spring-beans.xml");

        System.in.read();

    }
}

```

#### 改造gmall-order-web作为服务消费者

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <parent>
        <artifactId>DubboDemon</artifactId>
        <groupId>org.example</groupId>
        <version>1.0-SNAPSHOT</version>
    </parent>
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.harry.dubbo</groupId>
    <artifactId>gmall-user</artifactId>
    <dependencies>
        <dependency>
            <groupId>com.harry.dubbo</groupId>
            <artifactId>gmall-interface</artifactId>
            <version>1.0-SNAPSHOT</version>
        </dependency>
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>dubbo</artifactId>
            <version>2.6.2</version>
        </dependency>
        <dependency>
            <groupId>org.apache.curator</groupId>
            <artifactId>curator-framework</artifactId>
            <version>2.6.0</version>
        </dependency>
    </dependencies>

    <properties>
        <maven.compiler.source>8</maven.compiler.source>
        <maven.compiler.target>8</maven.compiler.target>
    </properties>

</project>

```

配置消费者信息

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:dubbo="http://dubbo.apache.org/schema/dubbo"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
		http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-4.3.xsd
		http://dubbo.apache.org/schema/dubbo http://dubbo.apache.org/schema/dubbo/dubbo.xsd
		http://code.alibabatech.com/schema/dubbo http://code.alibabatech.com/schema/dubbo/dubbo.xsd">

    <context:component-scan base-package="com.harry.dubbo"/>
    <!--当前应用的名字  -->
    <dubbo:application name="gmall-order-web"></dubbo:application>
    <!--指定注册中心的地址  -->
    <dubbo:registry address="zookeeper://192.168.31.96:2181" />
    <!--使用dubbo协议，将服务暴露在20880端口  -->
    <dubbo:protocol name="dubbo" port="20880" />
    <!-- 生成远程服务代理，可以和本地bean一样使用demoService -->
    <dubbo:reference id="userService" interface="com.harry.dubbo.service.UserService"></dubbo:reference>

</beans>



```

orederservice

```java
package com.harry.dubbo.service;

import com.alibaba.dubbo.config.annotation.Reference;
import com.harry.dubbo.bean.UserAddress;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class OrderService {

    @Autowired
    UserService userService;
    /**
     * 初始化订单，查询用户的所有地址并返回
     * @param userID
     * @return
     */
    public List<UserAddress> initOrder(String userID){
        System.out.println(userService);
        List<UserAddress> userAddressList = userService.getUserAddressList(userID);
        System.out.println("当前接收到的userId=> "+userID);
        System.out.println("**********");
        System.out.println("查询到的所有地址为：");
        for (UserAddress userAddress : userAddressList) {
            //打印远程服务地址的信息
            System.out.println(userAddress.getUserAddress());
        }

        return userAddressList;
    }

    public static void main(String[] args) {
        OrderService orderService = new OrderService();
        orderService.initOrder("10");

    }
}
```

启动

```java
package com.harry.dubbo;

import org.springframework.context.support.ClassPathXmlApplicationContext;

import java.io.IOException;

public class Application {
    public static void main(String[] args) throws IOException {
        ClassPathXmlApplicationContext context =
                new ClassPathXmlApplicationContext("classpath:spring-beans.xml");

        System.in.read();

    }
}

```



![image-20220607205422939](images\image-20220607205422939.png)

![image-20220608172457196](images\image-20220608172457196.png)

### dubbo-monitor-simple简易监控中心

##### 1、下载 dubbo-ops

https://github.com/apache/incubator-dubbo-ops

##### 2、修改配置指定注册中心地址

进入 dubbo-monitor-simple\src\main\resources\conf

修改 dubbo.properties文件

![image-20220608172753600](images\image-20220608172753600.png)

##### 3、打包dubbo-monitor-simple

mvn clean package -Dmaven.test.skip=true

##### 4、解压 tar.gz 文件，并运行start.bat

![image-20220608172849566](images\image-20220608172849566.png)

##### 5、启动访问8080

#### 监控中心配置

```xml
所有服务配置连接监控中心，进行监控统计
    <!-- 监控中心协议，如果为protocol="registry"，表示从注册中心发现监控中心地址，否则直连监控中心 -->
	<dubbo:monitor protocol="registry"></dubbo:monitor>

```

Simple Monitor 挂掉不会影响到 Consumer 和 Provider 之间的调用，所以用于生产环境不会有风险。

Simple Monitor 采用磁盘存储统计信息，请注意安装机器的磁盘限制，如果要集群，建议用mount共享磁盘。

## 整合SpringBoot

![image-20220608173054681](images\image-20220608173054681.png)

### **创建Maven项目 `boot-user-service-provider`** 服务提供者

导入以下依赖

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.harry.dubbo</groupId>
    <artifactId>boot-user-service-provider</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>boot-user-service-provider</name>
    <description>boot-user-service-provider</description>

    <properties>
        <java.version>1.8</java.version>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <spring-boot.version>2.4.1</spring-boot.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>

        <dependency>
            <groupId>com.alibaba.boot</groupId>
            <artifactId>dubbo-spring-boot-starter</artifactId>
            <version>0.2.0</version>
        </dependency>
        <dependency>
            <groupId>com.harry.dubbo</groupId>
            <artifactId>gmall-interface</artifactId>
            <version>1.0-SNAPSHOT</version>
        </dependency>
    </dependencies>
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>${spring-boot.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
    <repositories>
        <repository>
            <id>spring-milestones</id>
            <name>Spring Milestones</name>
            <url>https://repo.spring.io/milestone</url>
            <snapshots>
                <enabled>false</enabled>
            </snapshots>
        </repository>
        <repository>
            <id>spring-snapshots</id>
            <name>Spring Snapshots</name>
            <url>https://repo.spring.io/snapshot</url>
            <releases>
                <enabled>false</enabled>
            </releases>
        </repository>
    </repositories>
    <pluginRepositories>
        <pluginRepository>
            <id>spring-milestones</id>
            <name>Spring Milestones</name>
            <url>https://repo.spring.io/milestone</url>
            <snapshots>
                <enabled>false</enabled>
            </snapshots>
        </pluginRepository>
        <pluginRepository>
            <id>spring-snapshots</id>
            <name>Spring Snapshots</name>
            <url>https://repo.spring.io/snapshot</url>
            <releases>
                <enabled>false</enabled>
            </releases>
        </pluginRepository>
    </pluginRepositories>

</project>

```

把 `user-service-provider` 中的service拿到此项目中。

```java
package com.harry.dubbo.service;

import com.alibaba.dubbo.config.annotation.Service;
import com.harry.dubbo.bean.UserAddress;
import com.harry.dubbo.dao.UserAddressDao;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

@Service
public class UserServiceImpl implements UserService{

    @Autowired
    UserAddressDao userAddressDao;

    @Override
    public List<UserAddress> getUserAddressList(String userId) {
        return userAddressDao.getUserAddressById(userId);
    }
}

```

启动类

```java
package com.harry.dubbo;


import com.alibaba.dubbo.config.spring.context.annotation.EnableDubbo;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@EnableDubbo
public class BootUserServiceProviderApplication {

    public static void main(String[] args) {
        SpringApplication.run(BootUserServiceProviderApplication.class, args);
    }

}

```

配置 `application.properties`

```properties
server.port=9092
spring.application.name=boot-order-service-provider
dubbo.application.name=boot-order-service-provider
dubbo.protocol.name=dubbo
dubbo.protocol.port=20880
dubbo.registry.address=192.168.31.96:2181
dubbo.registry.protocol=zookeeper
dubbo.registry.file=dubbo-registry/dubbo-registry.properties
#连接监控中心
dubbo.monitor.protocol=registry
```

启动注册中心，启动当前服务提供者，可以在浏览器看到一个服务提供者。

### boot-order-service-consumer 服务消费者

导入以下依赖

```xml
  <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>

        <dependency>
            <groupId>com.alibaba.boot</groupId>
            <artifactId>dubbo-spring-boot-starter</artifactId>
            <version>0.2.0</version>
        </dependency>
        <dependency>
            <groupId>com.harry.dubbo</groupId>
            <artifactId>gmall-interface</artifactId>
            <version>1.0-SNAPSHOT</version>
        </dependency>
    </dependencies>
```

把order-service-consumer项目中的service复制到当前项目。

```java
package com.harry.dubbo.service;

import com.alibaba.dubbo.config.annotation.Reference;
import com.harry.dubbo.bean.UserAddress;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class OrderService {

    @Reference
    UserService userService;
    /**
     * 初始化订单，查询用户的所有地址并返回
     * @param userID
     * @return
     */
    public List<UserAddress> initOrder(String userID){
        System.out.println(userService);
        List<UserAddress> userAddressList = userService.getUserAddressList(userID);
        System.out.println("当前接收到的userId=> "+userID);
        System.out.println("**********");
        System.out.println("查询到的所有地址为：");
        for (UserAddress userAddress : userAddressList) {
            //打印远程服务地址的信息
            System.out.println(userAddress.getUserAddress());
        }

        return userAddressList;
    }

    public static void main(String[] args) {
        OrderService orderService = new OrderService();
        orderService.initOrder("10");

    }
}

```

controller

```java
package com.harry.dubbo.controller;

import com.harry.dubbo.bean.UserAddress;
import com.harry.dubbo.service.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.List;

@Controller
public class OrderController {

    @Autowired
    OrderService orderService;

    @RequestMapping(value = "/order")
    @ResponseBody
    public    List<UserAddress> getUserAddress(@RequestParam("userId") String userId){
        List<UserAddress> userAddresses = orderService.initOrder(userId);
        return userAddresses;
    }
}

```

创建application.properties 配置

```properties
# 应用名称
spring.application.name=boot-order-service-consumer
# 应用服务 WEB 访问端口
server.port=9091

dubbo.application.name=boot-order-service-consumer
dubbo.registry.address=192.168.31.96:2181
dubbo.registry.protocol=zookeeper
dubbo.registry.file=dubbo-registry/dubbo-registry.properties
#连接监控中心 注册中心协议
dubbo.monitor.protocol=registry

```

启动类

```java
package com.harry.dubbo;

import com.alibaba.dubbo.config.spring.context.annotation.EnableDubbo;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@EnableDubbo
public class BootOrderServiceConsumerApplication {

    public static void main(String[] args) {
        SpringApplication.run(BootOrderServiceConsumerApplication.class, args);
    }

}

```

配置完毕，此时启动zookeeper注册中心及监控。
启动springboot配置的服务提供者和消费者

![image-20220608185014392](images\image-20220608185014392.png)



# 二 Dubbo配置

dubbo配置官网参考：http://dubbo.apache.org/zh-cn/docs/user/references/xml/dubbo-service.html

## **1、配置原则**

![image-20220608185216081](images\image-20220608185216081.png)

JVM 启动 -D 参数优先，这样可以使用户在部署和启动时进行参数重写，比如在启动时需改变协议的端口。
XML 次之，如果在 XML 中有配置，则 dubbo.properties 中的相应配置项无效。
Properties 最后，相当于缺省值，只有 XML 没有配置时，dubbo.properties 的相应配置项才会生效，通常用于共享公共配置，比如应用名。


## 2、重试次数

失败自动切换，当出现失败，重试其它服务器，但重试会带来更长延迟。可通过 retries="2" 来设置重试次数(不含第一次)。

```xml
重试次数配置如下：
<dubbo:service retries="2" />
或
<dubbo:reference retries="2" />
或
<dubbo:reference>
    <dubbo:method name="findFoo" retries="2" />
</dubbo:reference>

```

## 3、超时时间

由于网络或服务端不可靠，会导致调用出现一种不确定的中间状态（超时）。为了避免超时导致客户端资源（线程）挂起耗尽，必须设置超时时间。

### Dubbo消费端 

```xml
全局超时配置
<dubbo:consumer timeout="5000" />

指定接口以及特定方法超时配置
<dubbo:reference interface="com.foo.BarService" timeout="2000">
    <dubbo:method name="sayHello" timeout="3000" />
</dubbo:reference>

```

### Dubbo服务端 

```xml
全局超时配置
<dubbo:provider timeout="5000" />

指定接口以及特定方法超时配置
<dubbo:provider interface="com.foo.BarService" timeout="2000">
    <dubbo:method name="sayHello" timeout="3000" />
</dubbo:provider>

```

### 配置原则

dubbo推荐在Provider上尽量多配置Consumer端属性：

```
1、作服务的提供者，比服务使用方更清楚服务性能参数，如调用的超时时间，合理的重试次数，等等
2、在Provider配置后，Consumer不配置则会使用Provider的配置值，即Provider配置可以作为Consumer的缺省值。否则，Consumer会使用Consumer端的全局设置，这对于Provider不可控的，并且往往是不合理的
```

配置的覆盖规则：

1) 方法级配置别优于接口级别，即小Scope优先 

2) Consumer端配置 优于 Provider配置 优于 全局配置，

3) 最后是Dubbo Hard Code的配置值（见配置文档）

![image-20220608185855639](images\image-20220608185855639.png)

## 4、版本号

当一个接口实现，出现不兼容升级时，可以用版本号过渡，版本号不同的服务相互间不引用。

​	可以按照以下的步骤进行版本迁移：

​	在低压力时间段，先升级一半提供者为新版本

​	再将所有消费者升级为新版本

​	然后将剩下的一半提供者升级为新版本

```xml
老版本服务提供者配置：
<dubbo:service interface="com.foo.BarService" version="1.0.0" />

新版本服务提供者配置：
<dubbo:service interface="com.foo.BarService" version="2.0.0" />

老版本服务消费者配置：
<dubbo:reference id="barService" interface="com.foo.BarService" version="1.0.0" />

新版本服务消费者配置：
<dubbo:reference id="barService" interface="com.foo.BarService" version="2.0.0" />

如果不需要区分版本，可以按照以下的方式配置：
<dubbo:reference id="barService" interface="com.foo.BarService" version="*" />
```

![image-20220608190312906](images\image-20220608190312906.png)



# 三、高可用

## 1、zookeeper宕机与dubbo直连

现象：zookeeper注册中心宕机，还可以消费dubbo暴露的服务。

原因：

> ```
> 健壮性
> 	监控中心宕掉不影响使用，只是丢失部分采样数据
> 	数据库宕掉后，注册中心仍能通过缓存提供服务列表查询，但不能注册新服务
> 	注册中心对等集群，任意一台宕掉后，将自动切换到另一台
> 	注册中心全部宕掉后，服务提供者和服务消费者仍能通过本地缓存通讯
> 	服务提供者无状态，任意一台宕掉后，不影响使用
> 	服务提供者全部宕掉后，服务消费者应用将无法使用，并无限次重连等待服务提供者恢复
> 
> ```

高可用：通过设计，减少系统不能提供服务的时间；

## 2、集群下dubbo负载均衡配置

在集群负载均衡时，Dubbo 提供了多种均衡策略，缺省为 random 随机调用。

**负载均衡策略如下**

### **Random LoadBalance 基于权重的随机负载均衡机制**3

![image-20220608190440828](images\image-20220608190440828.png)

随机，按权重设置随机概率。 在一个截面上碰撞的概率高，但调用量越大分布越均匀，而且按概率使用权重后也比较均匀，有利于动态调整提供者权重。

### **RoundRobin LoadBalance 基于权重的轮询负载均衡机制**

![image-20220608190540743](images\image-20220608190540743.png)

轮循，按公约后的权重设置轮循比率。 存在慢的提供者累积请求的问题，比如：第二台机器很慢，但没挂，当请求调到第二台时就卡在那，久而久之，所有请求都卡在调到第二台上。

### **LeastActive LoadBalance最少活跃数负载均衡机制**

最少活跃调用数，相同活跃数的随机，活跃数指调用前后计数差。 使慢的提供者收到更少请求，因为越慢的提供者的调用前后计数差会越大。

![image-20220608190702941](images\image-20220608190702941.png)

### **ConsistentHash LoadBalance一致性hash 负载均衡机制**

![image-20220608190724786](images\image-20220608190724786.png)

## 3、整合hystrix，服务熔断与降级处理

### 1、服务降级

**什么是服务降级？**

**当服务器压力剧增的情况下，根据实际业务情况及流量，对一些服务和页面有策略的不处理或换种简单的方式处理，从而释放服务器资源以保证核心交易正常运作或高效运作。**

可以通过服务降级功能临时屏蔽某个出错的非关键服务，并定义降级后的返回策略。

向注册中心写入动态配置覆盖规则：

```java
RegistryFactory registryFactory = ExtensionLoader.getExtensionLoader(RegistryFactory.class).getAdaptiveExtension();
Registry registry = registryFactory.getRegistry(URL.valueOf("zookeeper://10.20.153.10:2181"));
registry.register(URL.valueOf("override://0.0.0.0/com.foo.BarService?category=configurators&dynamic=false&application=foo&mock=force:return+null"));

```

其中：

​	mock=force:return+null 表示消费方对该服务的方法调用都直接返回 null 值，不发起远程调用。用来屏蔽不重要服务不可用时对调用方的影响。

​	还可以改为 mock=fail:return+null 表示消费方对该服务的方法调用在失败后，再返回 null 值，不抛异常。用来容忍不重要服务不稳定时对调用方的影响

### 2、集群容错

在集群调用失败时，Dubbo 提供了多种容错方案，缺省为 failover 重试。

**集群容错模式**

**Failover Cluster**

失败自动切换，当出现失败，重试其它服务器。通常用于读操作，但重试会带来更长延迟。可通过 retries="2" 来设置重试次数(不含第一次)。

```xml
重试次数配置如下：
<dubbo:service retries="2" />
或
<dubbo:reference retries="2" />
或
<dubbo:reference>
    <dubbo:method name="findFoo" retries="2" />
</dubbo:reference>

```

**Failfast Cluster**

快速失败，只发起一次调用，失败立即报错。通常用于非幂等性的写操作，比如新增记录。

**Failsafe Cluster**

失败安全，出现异常时，直接忽略。通常用于写入审计日志等操作。

**Failback Cluster**

失败自动恢复，后台记录失败请求，定时重发。通常用于消息通知操作。

**Forking Cluster**

并行调用多个服务器，只要一个成功即返回。通常用于实时性要求较高的读操作，但需要浪费更多服务资源。可通过 forks="2" 来设置最大并行数。

**Broadcast Cluster**

广播调用所有提供者，逐个调用，任意一台报错则报错 [2]。通常用于通知所有提供者更新缓存或日志等本地资源信息。

**集群模式配置**

按照以下示例在服务提供方和消费方配置集群模式

```xml
<dubbo:service cluster="failsafe" />
或
<dubbo:reference cluster="failsafe" />

```

### 3、整合hystrix

Hystrix 旨在通过控制那些访问远程系统、服务和第三方库的节点，从而对延迟和故障提供更强大的容错能力。Hystrix具备拥有回退机制和断路器功能的线程和信号隔离，请求缓存和请求打包，以及监控和配置等功能

#### 配置spring-cloud-starter-netflix-hystrix

spring boot官方提供了对hystrix的集成，直接在pom.xml里加入依赖：

```xml
  <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
            <version>1.4.4.RELEASE</version>
        </dependency>

```

然后在Application类上增加@EnableHystrix来启用hystrix starter：

```java
@SpringBootApplication
@EnableHystrix
public class ProviderApplication {


```

#### 配置Provider端

在Dubbo的Provider上增加@HystrixCommand配置，这样子调用就会经过Hystrix代理。

```java
@Service(version = "1.0.0")
public class HelloServiceImpl implements HelloService {
    @HystrixCommand(commandProperties = {
     @HystrixProperty(name = "circuitBreaker.requestVolumeThreshold", value = "10"),
     @HystrixProperty(name = "execution.isolation.thread.timeoutInMilliseconds", value = "2000") })
    @Override
    public String sayHello(String name) {
        // System.out.println("async provider received: " + name);
        // return "annotation: hello, " + name;
        throw new RuntimeException("Exception to show hystrix enabled.");
    }
}

```

#### 配置Consumer端

对于Consumer端，则可以增加一层method调用，并在method上配置@HystrixCommand。当调用出错时，会走到fallbackMethod = "reliable"的调用里。

```java
 @Reference(version = "1.0.0")
    private HelloService demoService;

    @HystrixCommand(fallbackMethod = "reliable")
    public String doSayHello(String name) {
        return demoService.sayHello(name);
    }
    public String reliable(String name) {
        return "hystrix fallback value";
    }

```

# 四、dubbo原理 

### RPC原理

![image-20220608191844383](images\image-20220608191844383.png)

> 一次完整的RPC调用流程（同步调用，异步另说）如下：
>
> **1**）服务消费方（client）调用以本地调用方式调用服务；
>
> 2）client stub接收到调用后负责将方法、参数等组装成能够进行网络传输的消息体； 
>
> 3）client stub找到服务地址，并将消息发送到服务端； 
>
> 4）server stub收到消息后进行解码； 
>
> 5）server stub根据解码结果调用本地的服务； 
>
> 6）本地服务执行并将结果返回给server stub； 
>
> 7）server stub将返回结果打包成消息并发送至消费方； 
>
> 8）client stub接收到消息，并进行解码； 
>
> **9**）服务消费方得到最终结果。
>
> RPC框架的目标就是要2~8这些步骤都封装起来，这些细节对用户来说是透明的，不可见的

### netty通信原理

Netty是一个异步事件驱动的网络应用程序框架， 用于快速开发可维护的高性能协议服务器和客户端。它极大地简化并简化了TCP和UDP套接字服务器等网络编程。

BIO：(Blocking IO)

![image-20220608192033050](images\image-20220608192033050.png)

NIO (Non-Blocking IO)

![image-20220608192055834](images\image-20220608192055834.png)

Selector 一般称 为**选择器** ，也可以翻译为 **多路复用器，**

Connect（连接就绪）、Accept（接受就绪）、Read（读就绪）、Write（写就绪）

Netty基本原理：

![image-20220608192116710](images\image-20220608192116710.png)

### dubbo原理

dubbo原理   -框架设计 

![image-20220608192157242](images\image-20220608192157242.png)

​	config 配置层：对外配置接口，以 ServiceConfig, ReferenceConfig 为中心，可以直接初始化配置类，也可以通过 spring 解析配置生成配置类

​	proxy 服务代理层：服务接口透明代理，生成服务的客户端 Stub 和服务器端 Skeleton, 以 ServiceProxy 为中心，扩展接口为 ProxyFactory

​	registry 注册中心层：封装服务地址的注册与发现，以服务 URL 为中心，扩展接口为 RegistryFactory, Registry, RegistryService

​	cluster 路由层：封装多个提供者的路由及负载均衡，并桥接注册中心，以 Invoker 为中心，扩展接口为 Cluster, Directory, Router, LoadBalance

​	monitor 监控层：RPC 调用次数和调用时间监控，以 Statistics 为中心，扩展接口为 MonitorFactory, Monitor, MonitorService

​	protocol 远程调用层：封装 RPC 调用，以 Invocation, Result 为中心，扩展接口为 Protocol, Invoker, Exporter

​	exchange 信息交换层：封装请求响应模式，同步转异步，以 Request, Response 为中心，扩展接口为 Exchanger, ExchangeChannel, ExchangeClient, ExchangeServer

​	transport 网络传输层：抽象 mina 和 netty 为统一接口，以 Message 为中心，扩展接口为 Channel, Transporter, Client, Server, Codec

​	serialize 数据序列化层：可复用的一些工具，扩展接口为 Serialization, ObjectInput, ObjectOutput, ThreadPool

### dubbo原理   -启动解析、加载配置信息 

![image-20220608192309440](images\image-20220608192309440.png)

### dubbo原理   -服务暴露

![image-20220608192330197](images\image-20220608192330197.png)

### dubbo原理   -服务引用

![image-20220608192405449](images\image-20220608192405449.png)

### dubbo原理   -服务调用

![image-20220608192436112](images\image-20220608192436112.png)