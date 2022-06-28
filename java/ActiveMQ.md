# 一、MQ介绍和对比

## 1、MQ产品种类和对比

MQ就是消息中间件。MQ是一种理念，ActiveMQ是MQ的落地产品。不管是哪款消息中间件，都有如下一些技术维度：

![img](images\clip_image002.jpg)

![img](images\clip_image003.jpg)

### (1) kafka

编程语言：scala。

大数据领域的主流MQ。

### (2) rabbitmq

编程语言：erlang

基于erlang语言，不好修改底层，不要查找问题的原因，不建议选用。

### (3) rocketmq

编程语言：java

适用于大型项目。适用于集群。

### (4) activemq

编程语言：java

适用于中小型项目。

## 2、MQ的产生背景

​     微服务架构后，链式调用是我们在写程序时候的一般流程,为了完成一个整体功能会将其拆分成多个函数(或子模块)，比如模块A调用模块B,模块B调用模块C,模块C调用模块D。但在大型分布式应用中，系统间的RPC交互繁杂，一个功能背后要调用上百个接口并非不可能，从单机架构过渡到分布式微服务架构的通例。这些架构会有哪些问题？

### **(1)**  系统之间接口耦合比较严重

每新增一个下游功能，都要对上游的相关接口进行改造；

举个例子：如果系统A要发送数据给系统B和系统C，发送给每个系统的数据可能有差异，因此系统A对要发送给每个系统的数据进行了组装，然后逐一发送；

当代码上线后又新增了一个需求：把数据也发送给D，新上了一个D系统也要接受A系统的数据，此时就需要修改A系统，让他感知到D系统的存在，同时把数据处理好再给D。在这个过程你会看到，每接入一个下游系统，都要对系统A进行代码改造，开发联调的效率很低。其整体架构如下图：

![img](images\clip_image004.jpg)

 

### **(2)**  **面对大流量并发时，容易被冲垮**

每个接口模块的吞吐能力是有限的，这个上限能力如果是堤坝，当大流量（洪水）来临时，容易被冲垮。

举个例子秒杀业务：上游系统发起下单购买操作，就是下单一个操作，很快就完成。然而，下游系统要完成秒杀业务后面的所有逻辑（读取订单，库存检查，库存冻结，余额检查，余额冻结，订单生产，余额扣减，库存减少，生成流水，余额解冻，库存解冻）。

### **(3)**  **等待同步存在性能问题**

RPC接口上基本都是同步调用，整体的服务性能遵循“木桶理论”，即整体系统的耗时取决于链路中最慢的那个接口。比如A调用B/C/D都是50ms，但此时B又调用了B1，花费2000ms，那么直接就拖累了整个服务性能。

![img](images\clip_image006.jpg)

根据上述的几个问题，在设计系统时可以明确要达到的目标：

1，要做到系统解耦，当新的模块接进来时，可以做到代码改动最小；能够解耦

2，设置流量缓冲池，可以让后端系统按照自身吞吐能力进行消费，不被冲垮；能削峰

3，强弱依赖梳理能将非关键调用链路的操作异步化并提升整体系统的吞吐能力；能够异步

## 3、MQ的主要作用

(1) 异步。调用者无需等待。

(2) 解耦。解决了系统之间耦合调用的问题。

(3) 消峰。抵御洪峰流量，保护了主业务。

### MQ的定义

​     面向消息的中间件（message-oriented middleware）MOM能够很好的解决以上问题。是指利用高效可靠的消息传递机制与平台无关的数据交流，并基于数据通信来进行分布式系统的集成。通过提供消息传递和消息排队模型在分布式环境下提供应用解耦，弹性伸缩，冗余存储、流量削峰，异步通信，数据同步等功能。

​    大致的过程是这样的：发送者把消息发送给消息服务器，消息服务器将消息存放在若干队列/主题topic中，在合适的时候，消息服务器会将消息转发给接受者。在这个过程中，发送和接收是异步的，也就是发送无需等待，而且发送者和接受者的生命周期也没有必然的关系；尤其在发布pub/订阅sub模式下，也可以完成一对多的通信，即让一个消息有多个接受者。

![img](images\clip_image007.jpg)

### MQ的特点

#### **(1)**  **采用异步处理模式**

消息发送者可以发送一个消息而无须等待响应。消息发送者将消息发送到一条虚拟的通道(主题或者队列)上；

消息接收者则订阅或者监听该爱通道。一条消息可能最终转发给一个或者多个消息接收者，这些消息接收者都无需对消息发送者做出同步回应。整个过程都是异步的。

案例：

也就是说，一个系统跟另一个系统之间进行通信的时候，假如系统A希望发送一个消息给系统B，让他去处理。但是系统A不关注系统B到底怎么处理或者有没有处理好，所以系统A把消息发送给MQ，然后就不管这条消息的“死活了”，接着系统B从MQ里面消费出来处理即可。至于怎么处理，是否处理完毕，什么时候处理，都是系统B的事儿，与系统A无关。

#### **(2)**  **应用系统之间解耦合**

发送者和接受者不必了解对方，只需要确认消息。

发送者和接受者不必同时在线。

#### **(3)**  **整体架构**

![img](images\clip_image008.jpg)

#### **(4)**  **MQ**的缺点

两个系统之间不能同步调用，不能实时回复，不能响应某个调用的回复。

# 二、ActiveMQ安装和控制台

## 1、ActiveMQ安装

### **(1)**   **官方下载**

官网地址： http://activemq.apache.org/

点击下面，开始下载。

![img](images\clip_image09.jpg)

### **(2)**   **安装步骤**

安装步骤：

```
[root@localhost opt]# tar -zxvf apache-activemq-5.16.0-bin.tar.gz

[root@localhost opt]# cd /etc/init.d/

root@localhost init.d]# vim activemq
```

注意：将下面内容全部复制。 要先安装jdk，在下面配置jdk的安装目录。

```bash
#!/bin/sh
#
# /etc/init.d/activemq
# chkconfig: 345 63 37
# description: activemq servlet container.
# processname: activemq 5.14.3
# Source function library.
#. /etc/init.d/functions
# source networking configuration.
#. /etc/sysconfig/network

export JAVA_HOME=/usr/local/jdk1.8.0_131
export CATALINA_HOME=/opt/apache-activemq-5.16.0


case $1 in
    start)
        sh $CATALINA_HOME/bin/activemq start
    ;;
    stop)
        sh $CATALINA_HOME/bin/activemq stop
    ;;
    restart)
        sh $CATALINA_HOME/bin/activemq stop
        sleep 1
        sh $CATALINA_HOME/bin/activemq start
    ;;

esac
exit 0


```

设置开机启动

```
[root@localhost init.d]# chmod 777 activemq
[root@localhost init.d]# chkconfig activemq on
```

启动服务

```
[root@localhost init.d]# service activemq start
INFO: Loading '/opt/apache-activemq-5.16.0//bin/env'
INFO: Using java '/bin/java'
INFO: Starting - inspect logfiles specified in logging.properties and log4j.properties to get details
INFO: pidfile created : '/opt/apache-activemq-5.16.0//data/activemq.pid' (pid '5316')
```

### (3)**启动时指定日志输出文件**

activemq日志默认的位置是在：%activemq安装目录%/data/activemq.log

这是我们启动时指定日志输出文件：

```
[root@localhost init.d]# service activemq start > /var/log/actimemq.log
```

### **(4)**   **查看程序启动是否成功的**3**种方式（通用）**

进入console看log

```
[root@localhost bin]# ./activemq console
```

```
[root@localhost bin]# ps -ef | grep activemq
root      7990     1 27 13:09 pts/2    00:00:03 /usr/bin/java -Xms64M -Xmx1G -Djava.util.logging.config.file=logging.properties -Djava.security.auth.login.config=/opt/apache-activemq-5.16.0//conf/login.config -Dcom.sun.management.jmxremote -Djava.awt.headless=true -Djava.io.tmpdir=/opt/apache-activemq-5.16.0//tmp -Dactivemq.classpath=/opt/apache-activemq-5.16.0//conf:/opt/apache-activemq-5.16.0//../lib/: -Dactivemq.home=/opt/apache-activemq-5.16.0/ -Dactivemq.base=/opt/apache-activemq-5.16.0/ -Dactivemq.conf=/opt/apache-activemq-5.16.0//conf -Dactivemq.data=/opt/apache-activemq-5.16.0//data -jar /opt/apache-activemq-5.16.0//bin/activemq.jar start
root      8032  4423  0 13:09 pts/2    00:00:00 grep --color=auto activemq
```

2.查看netstat端口

```
[root@localhost bin]# netstat -an | grep 61616
tcp6       0      0 :::61616                :::*                    LISTEN
```

3. lsof

```
[root@localhost bin]# lsof -i:61616
COMMAND  PID USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
java    7990 root  130u  IPv6 1742891      0t0  TCP *:61616 (LISTEN)
```

## 2、ActiveMQ控制台

### （1）访问activemq管理页面地址：http://IP地址:8161/  admin/admin

### （2）进入

修改监听的地址在./conf/jetty.xml

```xml
<bean id="jettyPort" class="org.apache.activemq.web.WebConsolePort" init-method="start">
         <!-- the default port number for the web console -->
    <property name="host" value="0.0.0.0"/>
    <property name="port" value="8161"/>
</bean>
```
![image-20201115132429082](images\image-20201115132429082.png)

## 3、**入门案例、MQ标准、API详解**

### 导入pom.xml

```xml
<dependencies>
    <!--  activemq  所需要的jar 包-->
    <dependency>
        <groupId>org.apache.activemq</groupId>
        <artifactId>activemq-all</artifactId>
        <version>5.15.9</version>
    </dependency>
    <!--  activemq 和 spring 整合的基础包 -->
    <dependency>
        <groupId>org.apache.xbean</groupId>
        <artifactId>xbean-spring</artifactId>
        <version>3.16</version>
    </dependency>
</dependencies>
```

### JMS编码总体规范

![img](images\clip_image010.jpg)

![img](images\clip_image0011.jpg)

### Destination简介

Destination是目的地。下面拿jvm和mq，做个对比。目的地，我们可以理解为是数据存储的地方。

![img](images\clip_image012.jpg)

Destination分为两种：队列和主题。下图介绍：

![img](images\clip_image013.jpg)

### 队列消息生产者的入门案例

```java
package com.harry.activemq;


import org.apache.activemq.ActiveMQConnectionFactory;

import javax.jms.*;

public class JmsProduce {
    // Linux上部署的activemq的IP地址+activemq的端口号
    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616";
    // 目的地的名称
    public static final String QUEUE_NAME = "queue_demon";

    public static void main(String[] args) throws JMSException {
        // 1 按照给定的url创建连接工厂，这个构造器采用默认的用户名密码。该类的其他构造方法可以指定用户名和密码。
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        // 2 通过连接工厂, 获取连接connection并启动访问。
        Connection connection = activeMQConnectionFactory.createConnection();
        connection.start();
        // 3 创建会话session。 第一参数是是否开启事务， 第二参数是消息签收的方式
        Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        // 4 创建目的地(两种：队列/主题)。Destination是Queue和Topic的父类
        Queue queue = session.createQueue(QUEUE_NAME);
        // 5 创建消费的生产者
        MessageProducer messageProducer = session.createProducer(queue);
        // 6 通过messageProducer生产3条 消息发送到消息队列中
        for (int i = 1; i < 4; i++) {
            // 7 创建消息
            TextMessage textMessage = session.createTextMessage("msg" + i);
            // 8 通过messageProducer发送给mq
            messageProducer.send(textMessage);
        }
        // 9 关闭资源
        messageProducer.close();
        session.close();
        connection.close();
        System.out.println("*** 消息发送到MQ完成 ***");
    }
}
```

###  ActiveMQ控制台之队列

运行上面代码，控制台显示如下：

![image-20201115143920528](images\image-20201115143920528.png)

Number Of Pending Messages：

等待消费的消息，这个是未出队列的数量，公式=总接收数-总出队列数。

Number Of Consumers：

消费者数量，消费者端的消费者数量。

Messages Enqueued：

进队消息数，进队列的总消息量，包括出队列的。这个数只增不减。

Messages Dequeued：

出队消息数，可以理解为是消费者消费掉的数量。

总结：

当有一个消息进入这个队列时，等待消费的消息是1，进入队列的消息是1。

当消息消费后，等待消费的消息是0，进入队列的消息是1，出队列的消息是1。

### 队列消息消费者的入门案例

```java
// 消息的消费者
public class JmsConsumer {

    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616";

    public static final String QUEUE_NAME = "queue_demon";

    public static void main(String[] args) throws JMSException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        Connection connection = activeMQConnectionFactory.createConnection();
        connection.start();
        Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        Queue queue = session.createQueue(QUEUE_NAME);
        // 创建消息的消费者
        MessageConsumer messageConsumer = session.createConsumer(queue);
        while (true){
            // receive() 一直等待接收消息，在能够接收到消息之前将一致阻塞。是同步阻塞方式。和socket的accept方法类似的
            // receive（Long time）: 等待n毫秒之后没有收到消息，就结束阻塞。
            // 因为消息发送者是TextMessage 所以消息接受者也要是TextMessage
            TextMessage message = (TextMessage) messageConsumer.receive();
            if(null != message){
                System.out.println("****消费者的消息："+ message.getText());
            }else {
                break;
            }


        }
        messageConsumer.close();
        session.close();
        connection.close();
    }

}
```

控制台显示：

![image-20201115145604021](images\image-20201115145604021.png)

### 异步监听式消费者（MessageListener）

```java
package com.harry.activemq;

import org.apache.activemq.ActiveMQConnectionFactory;

import javax.jms.*;
import java.io.IOException;

public class JmsConsumerListener {
    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616";

    public static final String QUEUE_NAME = "queue_demon";

    public static void main(String[] args) throws JMSException, IOException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        Connection connection = activeMQConnectionFactory.createConnection();
        connection.start();
        Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        Queue queue = session.createQueue(QUEUE_NAME);
        // 创建消息的消费者
        MessageConsumer messageConsumer = session.createConsumer(queue);
        /***
         * 通过监听的方式来消费消息，是异步非阻塞的方式消费消息。
         * 通过messageConsumer的setMessageListener注册一个监听，当有消费发送来时，系统自动调用MessageListener的onMessage方法处理消息
         */
        messageConsumer.setMessageListener(new MessageListener() {
            @Override
            public void onMessage(Message message) {
                // instanceof 判断是否A对象是否是B类的子类
                if (null != message && message instanceof TextMessage) {
                    TextMessage textMessage = (TextMessage) message;
                    try {
                        System.out.println("****消费者的消息：" + textMessage.getText());
                    } catch (JMSException e) {
                        e.printStackTrace();
                    }

                }
            }
        });
        // 让主线程不要结束。因为一旦主线程结束了，其他的线程（如此处的监听消息的线程）也都会被迫结束。
        // 实际开发中，我们的程序会一直运行，这句代码都会省略。
        System.in.read();
        messageConsumer.close();
        session.close();
        connection.close();

    }
}
```

### 队列消息（Queue）总结

#### **(1)**    **两种消费方式**

同步阻塞方式(receive)

订阅者或接收者抵用MessageConsumer的receive()方法来接收消息，receive方法在能接收到消息之前（或超时之前）将一直阻塞。

异步非阻塞方式（监听器onMessage()）

订阅者或接收者通过MessageConsumer的setMessageListener(MessageListener listener)注册一个消息监听器，当消息到达之后，系统会自动调用监听器MessageListener的onMessage(Message message)方法。

#### **(2)**    **队列的特点：**

![img](images\clip_image014.jpg)

#### **(3)**   **消息消费情况**

![img](images\clip_image0015.jpg)

情况1：只启动消费者1。

结果：消费者1会消费所有的数据。

情况2：先启动消费者1，再启动消费者2。

结果：消费者1消费所有的数据。消费者2不会消费到消息。

情况3：生产者发布6条消息，在此之前已经启动了消费者1和消费者2。

结果：消费者1和消费者2平摊了消息。各自消费3条消息。

## 4、Topic介绍、入门案例、控制台

### **(1)**   **topic**介绍

在发布订阅消息传递域中，目的地被称为主题（topic）

发布/订阅消息传递域的特点如下：

（1）生产者将消息发布到topic中，每个消息可以有多个消费者，属于1：N的关系；

（2）生产者和消费者之间有时间上的相关性。订阅某一个主题的消费者只能消费自它订阅之后发布的消息。

（3）生产者生产时，topic不保存消息它是无状态的不落地，假如无人订阅就去生产，那就是一条废消息，所以，一般先启动消费者再启动生产者。

默认情况下如上所述，但是JMS规范允许客户创建持久订阅，这在一定程度上放松了时间上的相关性要求。持久订阅允许消费者消费它在未处于激活状态时发送的消息。一句话，好比我们的微信公众号订阅

![img](images\clip_image017.jpg)

### **(2)**   **生产者案例**

```java
public class JnsProduceTopic {
    // Linux上部署的activemq的IP地址+activemq的端口号
    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616";
    // 目的地的名称
    public static final String QUEUE_NAME = "topic_demon";

    public static void main(String[] args) throws JMSException {
        // 1 按照给定的url创建连接工厂，这个构造器采用默认的用户名密码。该类的其他构造方法可以指定用户名和密码。
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        // 2 通过连接工厂, 获取连接connection并启动访问。
        Connection connection = activeMQConnectionFactory.createConnection();
        connection.start();
        // 3 创建会话session。 第一参数是是否开启事务， 第二参数是消息签收的方式
        Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        // 4 创建目的地(两种：队列/主题)。Destination是Queue和Topic的父类
       Topic topic = session.createTopic(QUEUE_NAME);
        // 5 创建消费的生产者
        MessageProducer messageProducer = session.createProducer(topic);
        // 6 通过messageProducer生产3条 消息发送到消息队列中
        for (int i = 1; i < 4; i++) {
            // 7 创建消息
            TextMessage textMessage = session.createTextMessage("msg" + i);
            // 8 通过messageProducer发送给mq
            messageProducer.send(textMessage);
        }
        // 9 关闭资源
        messageProducer.close();
        session.close();
        connection.close();
        System.out.println("*** 消息发送到MQ完成 ***");
    }
}
```

### **(3)**   **消费者入门案例**

```java
import javax.jms.*;
import java.io.IOException;

public class JmsConsumerTopic {
    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616";

    public static final String TOPIC_NAME = "topic_demon";

    public static void main(String[] args) throws JMSException, IOException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        Connection connection = activeMQConnectionFactory.createConnection();
        connection.start();
        Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        Topic topic = session.createTopic(TOPIC_NAME);
        // 创建消息的消费者
        MessageConsumer messageConsumer = session.createConsumer(topic);
        /***
         * 通过监听的方式来消费消息，是异步非阻塞的方式消费消息。
         * 通过messageConsumer的setMessageListener注册一个监听，当有消费发送来时，系统自动调用MessageListener的onMessage方法处理消息
         */
        messageConsumer.setMessageListener(new MessageListener() {
            @Override
            public void onMessage(Message message) {
                // instanceof 判断是否A对象是否是B类的子类
                if (null != message && message instanceof TextMessage) {
                    TextMessage textMessage = (TextMessage) message;
                    try {
                        System.out.println("****消费者的消息：" + textMessage.getText());
                    } catch (JMSException e) {
                        e.printStackTrace();
                    }

                }
            }
        });
        // 让主线程不要结束。因为一旦主线程结束了，其他的线程（如此处的监听消息的线程）也都会被迫结束。
        // 实际开发中，我们的程序会一直运行，这句代码都会省略。
        System.in.read();
        messageConsumer.close();
        session.close();
        connection.close();

    }
}
```

### (4)ActiveMQ控制台

topic有多个消费者时，消费消息的数量 ≈ 在线消费者数量*生产消息的数量。

![image-20201115152304714](images\image-20201115152304714.png)



## 5、tpoic和queue对比

![img](images\clip_image022.jpg)

# 三、JMS规范

## 1、JMS是什么

​     java消息服务指的是两个应用程序之间进行异步通信的API，它为标准协议和消息服务提供了一组通用接口，包括创建、发送、读取消息等，用于支持Java应用程序开发。在JavaEE中，当两个应用程序使用JMS进行通信时，它们之间不是直接相连的，而是通过一个共同的消息收发服务组件关联起来以达到解耦/异步削峰的效果。

![img](images\clip_image023.jpg)

![img](images\clip_image0024.jpg)

## 2、消息头

JMS的消息头有哪些属性：

​	JMSDestination：消息目的地

​	JMSDeliveryMode：消息持久化模式

​	JMSExpiration：消息过期时间

​	JMSPriority：消息的优先级

​	JMSMessageID：消息的唯一标识符。后面我们会介绍如何解决幂等性。

说明： 消息的生产者可以set这些属性，消息的消费者可以get这些属性。

​			这些属性在send方法里面也可以设置。

```java
import org.apache.activemq.ActiveMQConnectionFactory;

import javax.jms.*;

public class JnsProduceTopic {
    // Linux上部署的activemq的IP地址+activemq的端口号
    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616";
    // 目的地的名称
    public static final String QUEUE_NAME = "topic_demon";

    public static void main(String[] args) throws JMSException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        Connection connection = activeMQConnectionFactory.createConnection();
        connection.start();
        Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        Topic topic = session.createTopic(QUEUE_NAME);
        MessageProducer messageProducer = session.createProducer(topic);
        for (int i = 1; i < 4; i++) {
            TextMessage textMessage = session.createTextMessage("msg" + i);
            // 这里可以指定每个消息的目的地
            textMessage.setJMSDestination(topic);
            /*
            持久模式和非持久模式。
            一条持久性的消息：应该被传送“一次仅仅一次”，这就意味着如果JMS提供者出现故障，该消息并不会丢失，它会在服务器恢复之后再次传递。
            一条非持久的消息：最多会传递一次，这意味着服务器出现故障，该消息将会永远丢失。
             */
            textMessage.setJMSDeliveryMode(0);
            /*
            可以设置消息在一定时间后过期，默认是永不过期。
            消息过期时间，等于Destination的send方法中的timeToLive值加上发送时刻的GMT时间值。
            如果timeToLive值等于0，则JMSExpiration被设为0，表示该消息永不过期。
            如果发送后，在消息过期时间之后还没有被发送到目的地，则该消息被清除。
             */
            textMessage.setJMSExpiration(1000);
            /*  消息优先级，从0-9十个级别，0-4是普通消息5-9是加急消息。
            JMS不要求MQ严格按照这十个优先级发送消息但必须保证加急消息要先于普通消息到达。默认是4级。
             */
            textMessage.setJMSPriority(10);
            // 唯一标识每个消息的标识。MQ会给我们默认生成一个，我们也可以自己指定。
            textMessage.setJMSMessageID("ABCD");
            // 上面有些属性在send方法里也能设置
            messageProducer.send(textMessage);
        }
        messageProducer.close();
        session.close();
        connection.close();
        System.out.println("*** 消息发送到MQ完成 ***");
    }
}
```

## 3、消息体

![img](images\clip_image025.jpg)

5种消息体格式：

![img](images\clip_image028.jpg)

下面我们演示MapMessage的用法

```java
public class JmsProduceMapMessage {
    // Linux上部署的activemq的IP地址+activemq的端口号
    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616";
    // 目的地的名称
    public static final String QUEUE_NAME = "topic_demon";

    public static void main(String[] args) throws JMSException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        Connection connection = activeMQConnectionFactory.createConnection();
        connection.start();
        Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        Topic topic = session.createTopic(QUEUE_NAME);
        MessageProducer messageProducer = session.createProducer(topic);
        for (int i = 1; i < 4; i++) {
            // 发送MapMessage  消息体。set方法: 添加，get方式：获取
            MapMessage  mapMessage = session.createMapMessage();
            mapMessage.setString("name", "张三"+i);
            mapMessage.setInt("age", 18+i);
            messageProducer.send(mapMessage);
        }
        messageProducer.close();
        session.close();
        connection.close();
        System.out.println("*** 消息发送到MQ完成 ***");
    }
}
```

consumer

```java
public class JmsConsumerMapMessage {
    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616";

    public static final String TOPIC_NAME = "topic_demon";

    public static void main(String[] args) throws JMSException, IOException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        Connection connection = activeMQConnectionFactory.createConnection();
        connection.start();
        Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        Topic topic = session.createTopic(TOPIC_NAME);
        // 创建消息的消费者
        MessageConsumer messageConsumer = session.createConsumer(topic);
        /***
         * 通过监听的方式来消费消息，是异步非阻塞的方式消费消息。
         * 通过messageConsumer的setMessageListener注册一个监听，当有消费发送来时，系统自动调用MessageListener的onMessage方法处理消息
         */
        messageConsumer.setMessageListener(new MessageListener() {
            @Override
            public void onMessage(Message message) {
                // instanceof 判断是否A对象是否是B类的子类
                if (null != message && message instanceof TextMessage) {
                    TextMessage textMessage = (TextMessage) message;
                    try {
                        System.out.println("****消费者的消息：" + textMessage.getText());
                    } catch (JMSException e) {
                        e.printStackTrace();
                    }
                }
                if (null != message  && message instanceof MapMessage){
                    MapMessage mapMessage = (MapMessage)message;
                    try {
                        System.out.println("****消费者的map消息："+mapMessage.getString("name"));
                        System.out.println("****消费者的map消息："+mapMessage.getInt("age"));
                    }catch (JMSException e) {
                    }
                }

            }
        });
        // 让主线程不要结束。因为一旦主线程结束了，其他的线程（如此处的监听消息的线程）也都会被迫结束。
        // 实际开发中，我们的程序会一直运行，这句代码都会省略。
        System.in.read();
        messageConsumer.close();
        session.close();
        connection.close();

    }
}
```

## 4、消息属性

​     如果需要除消息头字段之外的值，那么可以使用消息属性。他是识别/去重/重点标注等操作，非常有用的方法。

​      他们是以属性名和属性值对的形式制定的。可以将属性是为消息头得扩展，属性指定一些消息头没有包括的附加信息，比如可以在属性里指定消息选择器。消息的属性就像可以分配给一条消息的附加消息头一样。它们允许开发者添加有关消息的不透明附加信息。它们还用于暴露消息选择器在消息过滤时使用的数据。

下图是设置消息属性的API：

![img](images\clip_image026.jpg)

消息生产者

```java
public class JmsProduceProperty {
    // Linux上部署的activemq的IP地址+activemq的端口号
    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616";
    // 目的地的名称
    public static final String QUEUE_NAME = "topic_demon";

    public static void main(String[] args) throws JMSException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        Connection connection = activeMQConnectionFactory.createConnection();
        connection.start();
        Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        Topic topic = session.createTopic(QUEUE_NAME);
        MessageProducer messageProducer = session.createProducer(topic);
        for (int i = 1; i < 4; i++) {
            // 发送MapMessage  消息体。set方法: 添加，get方式：获取
            MapMessage  mapMessage = session.createMapMessage();
            mapMessage.setString("name", "张三"+i);
            mapMessage.setInt("age", 18+i);
            // 调用Message的set*Property()方法，就能设置消息属性。根据value的数据类型的不同，有相应的API。
            mapMessage.setStringProperty("From","ZhangSan@qq.com");
            mapMessage.setByteProperty("Spec", (byte) 1);
            mapMessage.setBooleanProperty("Invalide",true);
            messageProducer.send(mapMessage);
        }
        messageProducer.close();
        session.close();
        connection.close();
        System.out.println("*** 消息发送到MQ完成 ***");
    }
}
```

消息消费者

```java
public class JmsConsumerProperty {
    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616";

    public static final String TOPIC_NAME = "topic_demon";

    public static void main(String[] args) throws JMSException, IOException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        Connection connection = activeMQConnectionFactory.createConnection();
        connection.start();
        Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        Topic topic = session.createTopic(TOPIC_NAME);
        // 创建消息的消费者
        MessageConsumer messageConsumer = session.createConsumer(topic);
        /***
         * 通过监听的方式来消费消息，是异步非阻塞的方式消费消息。
         * 通过messageConsumer的setMessageListener注册一个监听，当有消费发送来时，系统自动调用MessageListener的onMessage方法处理消息
         */
        messageConsumer.setMessageListener(new MessageListener() {
            @Override
            public void onMessage(Message message) {
                // instanceof 判断是否A对象是否是B类的子类
                if (null != message && message instanceof TextMessage) {
                    TextMessage textMessage = (TextMessage) message;
                    try {
                        System.out.println("****消费者的消息：" + textMessage.getText());
                    } catch (JMSException e) {
                        e.printStackTrace();
                    }
                }
                if (null != message  && message instanceof MapMessage){
                    MapMessage mapMessage = (MapMessage)message;
                    try {
                        System.out.println("****消费者的map消息："+mapMessage.getString("name"));
                        System.out.println("****消费者的map消息："+mapMessage.getInt("age"));
                        System.out.println("消息属性："+mapMessage.getStringProperty("From"));
                        System.out.println("消息属性："+mapMessage.getByteProperty("Spec"));
                        System.out.println("消息属性："+mapMessage.getBooleanProperty("Invalide"));

                    }catch (JMSException e) {
                    }
                }

            }
        });
        // 让主线程不要结束。因为一旦主线程结束了，其他的线程（如此处的监听消息的线程）也都会被迫结束。
        // 实际开发中，我们的程序会一直运行，这句代码都会省略。
        System.in.read();
        messageConsumer.close();
        session.close();
        connection.close();

    }
}
```

## 5、消息的持久化

什么是持久化消息？

保证消息只被传送一次和成功使用一次。在持久性消息传送至目标时，消息服务将其放入持久性数据存储。如果消息服务由于某种原因导致失败，它可以恢复此消息并将此消息传送至相应的消费者。虽然这样增加了消息传送的开销，但却增加了可靠性。

### queue消息非持久和持久

![img](images\clip_image032.jpg)

运行结果证明：当生产者成功发布消息之后，MQ服务端宕机重启，消息生产者就收不到该消息了

```java
public class JmsProduce {
    // Linux上部署的activemq的IP地址+activemq的端口号
    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616";
    // 目的地的名称
    public static final String QUEUE_NAME = "queue_demon";

    public static void main(String[] args) throws JMSException {
        // 1 按照给定的url创建连接工厂，这个构造器采用默认的用户名密码。该类的其他构造方法可以指定用户名和密码。
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        // 2 通过连接工厂, 获取连接connection并启动访问。
        Connection connection = activeMQConnectionFactory.createConnection();
        connection.start();
        // 3 创建会话session。 第一参数是是否开启事务， 第二参数是消息签收的方式
        Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        // 4 创建目的地(两种：队列/主题)。Destination是Queue和Topic的父类
        Queue queue = session.createQueue(QUEUE_NAME);
        // 5 创建消费的生产者
        MessageProducer messageProducer = session.createProducer(queue);
        // 设置消息持久化
        messageProducer.setDeliveryMode(DeliveryMode.PERSISTENT);
        // 6 通过messageProducer生产3条 消息发送到消息队列中
        for (int i = 1; i < 4; i++) {
            // 7 创建消息
            TextMessage textMessage = session.createTextMessage("msg" + i);
            // 8 通过messageProducer发送给mq
            messageProducer.send(textMessage);
        }
        // 9 关闭资源
        messageProducer.close();
        session.close();
        connection.close();
        System.out.println("*** 消息发送到MQ完成 ***");
    }
}
```

### topic消息持久化

topic默认就是非持久化的，因为生产者生产消息时，消费者也要在线，这样消费者才能消费到消息。

topic消息持久化，只要消费者向MQ服务器注册过，所有生产者发布成功的消息，该消费者都能收到，不管是MQ服务器宕机还是消费者不在线。

 注意：

1. 一定要先运行一次消费者，等于向MQ注册，类似我订阅了这个主题。

2. 然后再运行生产者发送消息。

3. 之后无论消费者是否在线，都会收到消息。如果不在线的话，下次连接的时候，会把没有收过的消息都接收过来。

```java
public class JmsProduceTopic {
    // Linux上部署的activemq的IP地址+activemq的端口号
    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616";
    // 目的地的名称
    public static final String QUEUE_NAME = "topic_demon";

    public static void main(String[] args) throws JMSException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        Connection connection = activeMQConnectionFactory.createConnection();
        connection.start();
        Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        Topic topic = session.createTopic(QUEUE_NAME);
        MessageProducer messageProducer = session.createProducer(topic);
        // 设置持久化topic 
        messageProducer.setDeliveryMode(DeliveryMode.PERSISTENT);
        // 设置持久化topic之后再，启动连接
        connection.start();
        for (int i = 1; i < 4; i++) {
            TextMessage textMessage = session.createTextMessage("msg" + i);
            // 这里可以指定每个消息的目的地
            textMessage.setJMSDestination(topic);
            /*
            持久模式和非持久模式。
            一条持久性的消息：应该被传送“一次仅仅一次”，这就意味着如果JMS提供者出现故障，该消息并不会丢失，它会在服务器恢复之后再次传递。
            一条非持久的消息：最多会传递一次，这意味着服务器出现故障，该消息将会永远丢失。
             */
            textMessage.setJMSDeliveryMode(0);
            /*
            可以设置消息在一定时间后过期，默认是永不过期。
            消息过期时间，等于Destination的send方法中的timeToLive值加上发送时刻的GMT时间值。
            如果timeToLive值等于0，则JMSExpiration被设为0，表示该消息永不过期。
            如果发送后，在消息过期时间之后还没有被发送到目的地，则该消息被清除。
             */
            textMessage.setJMSExpiration(1000);
            /*  消息优先级，从0-9十个级别，0-4是普通消息5-9是加急消息。
            JMS不要求MQ严格按照这十个优先级发送消息但必须保证加急消息要先于普通消息到达。默认是4级。
             */
            textMessage.setJMSPriority(10);
            // 唯一标识每个消息的标识。MQ会给我们默认生成一个，我们也可以自己指定。
            textMessage.setJMSMessageID("ABCD");
            // 上面有些属性在send方法里也能设置
            messageProducer.send(textMessage);
        }
        messageProducer.close();
        session.close();
        connection.close();
        System.out.println("*** 消息发送到MQ完成 ***");
    }
}
```

持久化topic消费者代码

```java
import org.apache.activemq.ActiveMQConnectionFactory;

import javax.jms.*;
import java.io.IOException;

public class JmsConsumerTopicPersistent {
    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616";

    public static final String TOPIC_NAME = "topic_demon";

    public static void main(String[] args) throws JMSException, IOException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        Connection connection = activeMQConnectionFactory.createConnection();
        // 设置客户端ID。向MQ服务器注册自己的名称
        connection.setClientID("harry");
        connection.start();
        Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        Topic topic = session.createTopic(TOPIC_NAME);
        // 创建一个topic订阅者对象。一参是topic，二参是订阅者名称
        TopicSubscriber topicSubscriber = session.createDurableSubscriber(topic,"remark...");
        // 之后再开启连接
        connection.start();
        Message message = topicSubscriber.receive();
        while (null != message){
            TextMessage textMessage = (TextMessage)message;
            System.out.println(" 收到的持久化 topic ："+textMessage.getText());
            message = topicSubscriber.receive();
        }
        session.close();
        connection.close();
    }

}

```

## 6、消息的事务性

![img](images\clip_image042.jpg)

(1) 生产者开启事务后，执行commit方法，这批消息才真正的被提交。不执行commit方法，这批消息不会提交。执行rollback方法，之前的消息会回滚掉。生产者的事务机制，要高于签收机制，当生产者开启事务，签收机制不再重要。

(2)消费者开启事务后，执行commit方法，这批消息才算真正的被消费。不执行commit方法，这些消息不会标记已消费，下次还会被消费。执行rollback方法，是不能回滚之前执行过的业务逻辑，但是能够回滚之前的消息，回滚后的消息，下次还会被消费。消费者利用commit和rollback方法，甚至能够违反一个消费者只能消费一次消息的原理。

(1) 问：消费者和生产者需要同时操作事务才行吗？  

​     答：消费者和生产者的事务，完全没有关联，各自是各自的事务。

生产者：

```java
public class Jms_TX_Producer {

    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616";
    public static final String QUEUE_NAME = "Queue-TX";

    public static void main(String[] args) throws JMSException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        Connection connection = activeMQConnectionFactory.createConnection();
        connection.start();
        //1.创建会话session，两个参数transacted=事务,acknowledgeMode=确认模式(签收)
        //设置为开启事务
        Session session = connection.createSession(true, Session.AUTO_ACKNOWLEDGE);
        Queue queue = session.createQueue(QUEUE_NAME);
        MessageProducer producer = session.createProducer(queue);
        try {
            for (int i = 0; i < 3; i++) {
                TextMessage textMessage = session.createTextMessage("tx msg--" + i);
                producer.send(textMessage);
                if(i == 2){
                    throw new RuntimeException("GG.....");
                }
            }
            // 2. 开启事务后，使用commit提交事务，这样这批消息才能真正的被提交。
            session.commit();
            System.out.println("消息发送完成");
        } catch (Exception e) {
            System.out.println("出现异常,消息回滚");
            // 3. 工作中一般，当代码出错，我们在catch代码块中回滚。这样这批发送的消息就能回滚。
            session.rollback();
        } finally {
            //4. 关闭资源
            producer.close();
            session.close();
            connection.close();
        }

    }
}
```

消费者：

```java
public class Jms_TX_Consumer {
    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616";
    public static final String QUEUE_NAME = "Queue-TX";

    public static void main(String[] args) throws JMSException, IOException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        Connection connection = activeMQConnectionFactory.createConnection();
        connection.start();
        // 创建会话session，两个参数transacted=事务,acknowledgeMode=确认模式(签收)
        // 消费者开启了事务就必须手动提交，不然会重复消费消息
        final Session session = connection.createSession(true, Session.AUTO_ACKNOWLEDGE);
        Queue queue = session.createQueue(QUEUE_NAME);
        MessageConsumer messageConsumer = session.createConsumer(queue);
        int a = 0;
        messageConsumer.setMessageListener((message -> {
            TextMessage textMessage = (TextMessage) message;
            try {
                System.out.println("***消费者接收到的消息:   " + textMessage.getText());
                if (a == 0) {
                    System.out.println("commit");
                    session.commit();
                }
                if (a == 2){
                    System.out.println("rollback");
                }
            } catch (JMSException e) {
                e.printStackTrace();
                System.out.println("出现异常，消费失败，放弃消费");
                try {
                    session.rollback();
                } catch (JMSException jmsException) {
                    jmsException.printStackTrace();
                }
            }
        }
        ));
        //关闭资源
        System.in.read();
        messageConsumer.close();
        session.close();
        connection.close();

    }
}
```

## 7、消费的签收机制

### 签收的几种方式

①　自动签收（Session.AUTO_ACKNOWLEDGE）：该方式是默认的。该种方式，无需我们程序做任何操作，框架会帮我们自动签收收到的消息。

②　手动签收（Session.CLIENT_ACKNOWLEDGE）：手动签收。该种方式，需要我们手动调用Message.acknowledge()，来签收消息。如果不签收消息，该消息会被我们反复消费，只到被签收。

③　允许重复消息（Session.DUPS_OK_ACKNOWLEDGE）：多线程或多个消费者同时消费到一个消息，因为线程不安全，可能会重复消费。该种方式很少使用到。

④　事务下的签收（Session.SESSION_TRANSACTED）：开始事务的情况下，可以使用该方式。该种方式很少使用到。

### 事务和签收的关系

①　在事务性会话中，当一个事务被成功提交则消息被自动签收。如果事务回滚，则消息会被再次传送。事务优先于签收，开始事务后，签收机制不再起任何作用。

②　非事务性会话中，消息何时被确认取决于创建会话时的应答模式。

③　生产者事务开启，只有commit后才能将全部消息变为已消费。

④　事务偏向生产者，签收偏向消费者。也就是说，生产者使用事务更好点，消费者使用签收机制更好点。

producer

```java
public class Jms_TX_Producer {

    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616";
    public static final String QUEUE_NAME = "Queue-TX";

    public static void main(String[] args) throws JMSException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        Connection connection = activeMQConnectionFactory.createConnection();
        connection.start();
        //1.创建会话session，两个参数transacted=事务,acknowledgeMode=确认模式(签收)
        //设置为开启事务
        Session session = connection.createSession(true, Session.CLIENT_ACKNOWLEDGE);
        Queue queue = session.createQueue(QUEUE_NAME);
        MessageProducer producer = session.createProducer(queue);
        try {
            for (int i = 0; i < 3; i++) {
                TextMessage textMessage = session.createTextMessage("tx msg--" + i);
                producer.send(textMessage);
            }
            // 2. 开启事务后，使用commit提交事务，这样这批消息才能真正的被提交。
            session.commit();
            System.out.println("消息发送完成");
        } catch (Exception e) {
            System.out.println("出现异常,消息回滚");
            // 3. 工作中一般，当代码出错，我们在catch代码块中回滚。这样这批发送的消息就能回滚。
            session.rollback();
        } finally {
            //4. 关闭资源
            producer.close();
            session.close();
            connection.close();
        }

    }
}
```

consumer

```java
public class Jms_TX_Consumer {
    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616";
    public static final String QUEUE_NAME = "Queue-TX";

    public static void main(String[] args) throws JMSException, IOException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        Connection connection = activeMQConnectionFactory.createConnection();
        connection.start();
        // 创建会话session，两个参数transacted=事务,acknowledgeMode=确认模式(签收)
        // 消费者开启了事务就必须手动提交，不然会重复消费消息
        final Session session = connection.createSession(true, Session.CLIENT_ACKNOWLEDGE);
        Queue queue = session.createQueue(QUEUE_NAME);
        MessageConsumer messageConsumer = session.createConsumer(queue);
        int a = 0;
        messageConsumer.setMessageListener((message -> {
            TextMessage textMessage = (TextMessage) message;
            try {
                System.out.println("***消费者接收到的消息:   " + textMessage.getText());
                textMessage.acknowledge();
            } catch (JMSException e) {
                e.printStackTrace();
                System.out.println("出现异常，消费失败，放弃消费");
                try {
                    session.rollback();
                } catch (JMSException jmsException) {
                    jmsException.printStackTrace();
                }
            }
        }
        ));
        //关闭资源
        System.in.read();
        messageConsumer.close();
        session.close();
        connection.close();

    }
}
```

## 8、JMS的点对点总结

​    点对点模型是基于队列的，生产者发消息到队列，消费者从队列接收消息，队列的存在使得消息的异步传输成为可能。和我们平时给朋友发送短信类似。

​    如果在Session关闭时有部分消息己被收到但还没有被签收(acknowledged),那当消费者下次连接到相同的队列时，这些消息还会被再次接收

​    队列可以长久地保存消息直到消费者收到消息。消费者不需要因为担心消息会丢失而时刻和队列保持激活的连接状态，充分体现了异步传输模式的优势

## 9、JMS的发布订阅总结

(1) JMS的发布订阅总结

​    JMS Pub/Sub 模型定义了如何向一个内容节点发布和订阅消息，这些节点被称作topic。

   主题可以被认为是消息的传输中介，发布者（publisher）发布消息到主题，订阅者（subscribe）从主题订阅消息。

​    主题使得消息订阅者和消息发布者保持互相独立不需要解除即可保证消息的传送

(2) 非持久订阅

​    非持久订阅只有当客户端处于激活状态，也就是和MQ保持连接状态才能收发到某个主题的消息。

​    如果消费者处于离线状态，生产者发送的主题消息将会丢失作废，消费者永远不会收到。

​     一句话：先订阅注册才能接受到发布，只给订阅者发布消息。

(3) 持久订阅

​    客户端首先向MQ注册一个自己的身份ID识别号，当这个客户端处于离线时，生产者会为这个ID保存所有发送到主题的消息，当客户再次连接到MQ的时候，会根据消费者的ID得到所有当自己处于离线时发送到主题的消息

​    当持久订阅状态下，不能恢复或重新派送一个未签收的消息。

​    持久订阅才能恢复或重新派送一个未签收的消息。

(4) 非持久和持久化订阅如何选择

​    当所有的消息必须被接收，则用持久化订阅。当消息丢失能够被容忍，则用非持久订阅。

# 四、ActiveMQ的broker

## 1、broker是什么

​    相当于一个ActiveMQ服务器实例。说白了，Broker其实就是实现了用代码的形式启动ActiveMQ将MQ嵌入到Java代码中，以便随时用随时启动，在用的时候再去启动这样能节省了资源，也保证了可用性。这种方式，我们实际开发中很少采用，因为他缺少太多了东西，如：日志，数据存储等等。

## 2、启动broker时指定配置文件

启动broker时指定配置文件，可以帮助我们在一台服务器上启动多个broker。实际工作中一般一台服务器只启动一个broker。

![image-20201116205146856](images\image-20201116205146856.png)

## 3、嵌入式的broker启动

用ActiveMQ Broker作为独立的消息服务器来构建Java应用。

ActiveMQ也支持在vm中通信基于嵌入的broker，能够无缝的集成其他java应用。

pom.xml添加一个依赖

```xml
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.10.1</version>
</dependency>
```

嵌入式broke的启动类

```java
public class EmbedBroker {
    public static void main(String[] args) throws Exception {
        //ActiveMQ也支持在vm中通信基于嵌入的broker
        BrokerService brokerService = new BrokerService();
        brokerService.setPopulateJMSXUserID(true);
        brokerService.addConnector("tcp://127.0.0.1:61616");
        brokerService.start();
    }
}
```

# 五、Spring整合ActiveMQ

## 1、pom.xml添加依赖

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <parent>
        <artifactId>ActiveMQ-demon</artifactId>
        <groupId>org.example</groupId>
        <version>1.0-SNAPSHOT</version>
    </parent>
    <modelVersion>4.0.0</modelVersion>

    <artifactId>Spring-ActiveMQ</artifactId>

    <dependencies>
        <!-- spring支持jms的包 -->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-jms</artifactId>
            <version>4.3.23.RELEASE</version>
        </dependency>
        <!--spring相关依赖包-->
        <dependency>
            <groupId>org.apache.xbean</groupId>
            <artifactId>xbean-spring</artifactId>
            <version>4.15</version>
        </dependency>
        <!-- Spring核心依赖 -->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-core</artifactId>
            <version>4.3.23.RELEASE</version>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-context</artifactId>
            <version>4.3.23.RELEASE</version>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-aop</artifactId>
            <version>4.3.23.RELEASE</version>
        </dependency>
        <dependency>
            <groupId>org.aspectj</groupId>
            <artifactId>aspectjrt</artifactId>
            <version>1.6.1</version>
        </dependency>
        <dependency>
            <groupId>aspectj</groupId>
            <artifactId>aspectjweaver</artifactId>
            <version>1.5.3</version>
        </dependency>
        <dependency>
            <groupId>cglib</groupId>
            <artifactId>cglib</artifactId>
            <version>2.1_2</version>
        </dependency>
        <!-- activemq连接池 -->
        <dependency>
            <groupId>org.apache.activemq</groupId>
            <artifactId>activemq-pool</artifactId>
            <version>5.15.10</version>
        </dependency>
    </dependencies>
</project>
```

## 2、Spring的ActiveMQ配置文件

  src/main/resources/spring-activemq.xml  

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd http://www.springframework.org/schema/context https://www.springframework.org/schema/context/spring-context.xsd">

    <!-- 开启包的自动扫描 -->
    <context:component-scan base-package="com.harry.spring.mq"/>
    <!-- 配置生产者 -->
    <bean id="connectionFactory" class="org.apache.activemq.pool.PooledConnectionFactory" destroy-method="stop">
        <property name="connectionFactory">
            <!-- 正真可以生产Connection的ConnectionFactory，由对应的JMS服务提供 -->
            <bean class="org.apache.activemq.spring.ActiveMQConnectionFactory">
                <property name="brokerURL" value="tcp://192.168.30.128:61616"/>
            </bean>
        </property>
        <property name="maxConnections" value="100"/>
     </bean>
    <!--  这个是队列目的地,点对点的Queue  -->
    <bean id="destinationQueue" class="org.apache.activemq.command.ActiveMQQueue">
        <!--    通过构造注入Queue名    -->
        <constructor-arg index="0" value="spring-active-queue"/>
    </bean>

    <!--  这个是队列目的地,  发布订阅的主题Topic-->
    <bean id="destinationTopic" class="org.apache.activemq.command.ActiveMQTopic">
        <constructor-arg index="0" value="spring-active-topic"/>
    </bean>

    <!--  Spring提供的JMS工具类,他可以进行消息发送,接收等  -->
    <bean id="jmsTemplate" class="org.springframework.jms.core.JmsTemplate">
        <!--    传入连接工厂    -->
        <property name="connectionFactory" ref="connectionFactory"/>
        <!--    传入目的地    -->
        <property name="defaultDestination" ref="destinationQueue"/>
        <!--    消息自动转换器    -->
        <property name="messageConverter">
            <bean class="org.springframework.jms.support.converter.SimpleMessageConverter"/>
        </property>
    </bean>
</beans>
```

## 3、队列生产者

```java
import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.springframework.jms.core.JmsTemplate;
import org.springframework.stereotype.Service;


@Service
public class SpringMQ_Produce {

    @Autowired
    private JmsTemplate jmsTemplate;

    public static void main(String[] args) {
        ClassPathXmlApplicationContext applicationContext = new ClassPathXmlApplicationContext("spring-activemq.xml");
        SpringMQ_Produce springMQProduce = (SpringMQ_Produce) applicationContext.getBean(SpringMQ_Produce.class);
        springMQProduce.jmsTemplate.send((session -> {
            return session.createTextMessage("***Spring和ActiveMQ的整合case111.....");
        }));
        System.out.println("********send task over");
    }
}

```

## 4、队列消费者

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.springframework.jms.core.JmsTemplate;
import org.springframework.stereotype.Service;

@Service
public class SpringMQ_Consumer {

    @Autowired
    private JmsTemplate jmsTemplate;

    public static void main(String[] args) {
        ClassPathXmlApplicationContext applicationContext = new ClassPathXmlApplicationContext("spring-activemq.xml");
        SpringMQ_Consumer springMQConsumer = (SpringMQ_Consumer ) applicationContext.getBean("springMQ_Consumer");
        String retValue = (String) springMQConsumer.jmsTemplate.receiveAndConvert();
        System.out.println("****消费者收到的消息"+ retValue);
    }
}

}
```

## 5、Topic生产者和消费者

修改spring配置文件

```xml
<!--  这个是队列目的地,  发布订阅的主题Topic-->
<bean id="destinationTopic" class="org.apache.activemq.command.ActiveMQTopic">
    <constructor-arg index="0" value="spring-active-topic"/>
</bean>

<!--  Spring提供的JMS工具类,他可以进行消息发送,接收等  -->
<bean id="jmsTemplate" class="org.springframework.jms.core.JmsTemplate">
    <!--    传入连接工厂    -->
    <property name="connectionFactory" ref="connectionFactory"/>
    <!--    传入目的地    -->
    <property name="defaultDestination" ref="destinationTopic"/>
    <!--    消息自动转换器    -->
    <property name="messageConverter">
        <bean class="org.springframework.jms.support.converter.SimpleMessageConverter"/>
    </property>
</bean>
```

生产者和消费者代码不用修改即可实现

## 6、配置消费者监听类

配置文件加入监听器bean

```xml
<!--  Spring提供的JMS工具类,他可以进行消息发送,接收等  -->
<bean id="jmsTemplate" class="org.springframework.jms.core.JmsTemplate">
    <!--    传入连接工厂    -->
    <property name="connectionFactory" ref="connectionFactory"/>
    <!--    传入目的地    -->
    <property name="defaultDestination" ref="destinationTopic"/>
    <!--    消息自动转换器    -->
    <property name="messageConverter">
        <bean class="org.springframework.jms.support.converter.SimpleMessageConverter"/>
    </property>
</bean>

<!-- 配置监听程序-->
<bean id="jmsContainer" class="org.springframework.jms.listener.DefaultMessageListenerContainer">
    <property name="connectionFactory" ref="connectionFactory"/>
    <property name="destination" ref="destinationTopic"/>
    <property name="messageListener" ref="myMessageListener"/>
</bean>
```

写一个监听器类，实现自动监听消息

```java
import org.springframework.stereotype.Component;

import javax.jms.JMSException;
import javax.jms.Message;
import javax.jms.MessageListener;
import javax.jms.TextMessage;

@Component
public class MyMessageListener implements MessageListener {
    @Override
    public void onMessage(Message message) {
        if (null != message && message instanceof TextMessage){
            TextMessage textMessage = (TextMessage) message;
            try {
                String text = textMessage.getText();
                System.out.println(text);
            } catch (JMSException e) {
                e.printStackTrace();
            }
        }
    }
}
```



# 六、SpringBoot整合ActiveMQ



## 1、queue生产者

pom.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.4.0</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.harry.activemq</groupId>
    <artifactId>demo</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>demo</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>1.8</java.version>
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

        <!--spring boot整合activemq的jar包-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-activemq</artifactId>
            <version>2.1.5.RELEASE</version>
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

application.yml

```yml
server:
  port: 7777

spring:
  activemq:
    # activemq的broker的url
    broker-url: tcp://192.168.30.128:61616
    # 连接activemq的broker所需的账号和密码
    user: admin
    password: admin
  jms:
    # 目的地是queue还是topic， false（默认） = queue    true =  topic
    pub-sub-domain: false

#  自定义队列名称。这只是个常量
myqueue: boot-activemq-queue
```

配置目的地的bean

```java
import org.apache.activemq.command.ActiveMQQueue;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
// 开启jms适配
@EnableJms
public class ConfigBean {
    
    // 注入配置文件中的myqueue
    @Value("${myqueue}")
    private String myQueue;
    
    @Bean
    public ActiveMQQueue queue(){
        return new ActiveMQQueue(myQueue);
    }
    
}
```

队列生产者代码

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jms.core.JmsMessagingTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import javax.jms.Queue;
import java.util.UUID;

@Component
public class Queue_Produce {
    // JMS模板
    @Autowired
    private JmsMessagingTemplate jmsMessagingTemplate;
    
    // 这个是我们配置队列的目的地
    @Autowired
    private Queue queue;
    
    // 发送消息
    public  void  produceMessage(){
        // 一参是目的地， 二参是消息的内容
        jmsMessagingTemplate.convertAndSend(queue, "****"+ UUID.randomUUID().toString().substring(0,6));
        
    }
    
    // 定时任务。每3秒执行一次
    @Scheduled(fixedDelay = 30000)
    public void produceMessageScheduled(){
        produceMessage();
    }
}
```

主启动类

```java
@SpringBootApplication
@EnableScheduling
public class DemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }

}
```

单元测试

```JAVA
import com.harry.activemq.mq.Queue_Produce;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.web.WebAppConfiguration;

import javax.annotation.Resource;

// 加载spring的junit
@SpringBootTest
@WebAppConfiguration
public class TestActiveMQ {
    @Resource // 这个是java的注解， 而Autowried是spring的
    private Queue_Produce queue_produce;

    @Test
    public void testSend(){
        queue_produce.produceMessage();
    }
}
```

## 2、queue消费者

pom.xml和application.yml文件和前面一样。唯一不同就是下面代码

```java
import org.springframework.jms.annotation.JmsListener;
import org.springframework.stereotype.Component;

import javax.jms.JMSException;
import javax.jms.TextMessage;

@Component
public class Queue_consumer {
    // 注册一个监听器。destination指定监听的队列
    @JmsListener(destination = "${myqueue}")
    public void receive(TextMessage textMessage) throws JMSException {
        System.out.println("*** 消费者接受消息 ***"+ textMessage.getText());
    }
}
```

## 3、topic生产者

application.yml



```yml
server:
  port: 6666

spring:
  activemq:
    # activemq的broker的url
    broker-url: tcp://192.168.30.128:61616
    # 连接activemq的broker所需的账号和密码
    user: admin
    password: admin
  jms:
    # 目的地是queue还是topic， false（默认） = queue    true =  topic
    pub-sub-domain: true

# 自定义主题名称
mytopic: boot-activemq-topic
```

配置类

```java
@Configuration
@EnableJms
public class ConfigTopicBean {
    @Value("${mytopic}")
    private String  topicName ;

    @Bean
    public Topic topic() {
        return new ActiveMQTopic(topicName);
    }

}
```

生产者代码

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jms.core.JmsMessagingTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import javax.jms.Topic;
import java.util.UUID;

@Component
public class Topic_Produce {
    @Autowired
    private JmsMessagingTemplate jmsMessagingTemplate ;

    @Autowired
    private Topic topic ;

    @Scheduled(fixedDelay = 3000)
    public void produceTopic(){
        jmsMessagingTemplate.convertAndSend(topic,"主题消息"+ UUID.randomUUID().toString().substring(0,6));
    }

}
```

消费者代码

```java
import org.springframework.jms.annotation.JmsListener;
import org.springframework.stereotype.Component;

import javax.jms.TextMessage;

@Component
public class Topic_consumer {
    @JmsListener(destination = "${mytopic}")
    public void receive(TextMessage textMessage) throws  Exception{
        System.out.println("消费者受到订阅的主题："+textMessage.getText());
    }

}
```

## 4、SpringBoot之ActiveMQ实现延迟消息

### 修改activeMQ配置文件

 broker新增配置信息  schedulerSupport="true"

```xml
<broker xmlns="http://activemq.apache.org/schema/core" brokerName="localhost" dataDirectory="${activemq.data}" schedulerSupport="true" >

<destinationPolicy>
    <policyMap>
        <policyEntries>
            <policyEntry topic=">" >
                <!-- The constantPendingMessageLimitStrategy is used to prevent
                     slow topic consumers to block producers and affect other consumers
                     by limiting the number of messages that are retained
                     For more information, see:

                     http://activemq.apache.org/slow-consumer-handling.html

                -->
                <pendingMessageLimitStrategy>
                    <constantPendingMessageLimitStrategy limit="1000"/>
                </pendingMessageLimitStrategy>
            </policyEntry>
        </policyEntries>
    </policyMap>
</destinationPolicy>
```

### 配置ActiveMQ工厂消息，信任包必须配置否则会报错

```java
import org.apache.activemq.ActiveMQConnectionFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.ArrayList;
import java.util.List;

@Configuration
public class ActiveMQConfig {
    @Bean
    public ActiveMQConnectionFactory factory(@Value("${spring.activemq.broker-url}") String url){
        ActiveMQConnectionFactory factory = new ActiveMQConnectionFactory(url);
        // 设置信任序列化包集合
        List<String> models = new ArrayList<>();
        models.add("com.harry.activemq");
        factory.setTrustedPackages(models);

        return factory;
    }

}
```

### 消息实体类

```java
public class MessageModel {
    private String titile;
    private String message;

    public String getTitile() {
        return titile;
    }

    public void setTitile(String titile) {
        this.titile = titile;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}
```

### 延迟队列生产者

```java
@Service
public class DelayProducer {
    public static final Destination DEFAULT_QUEUE = new ActiveMQQueue("delay.queue");

    @Autowired
    private JmsMessagingTemplate template;

    /**
     * 发送消息
     *
     * @param destination destination是发送到的队列
     * @param message     message是待发送的消息
     */
    public <T extends Serializable> void send(Destination destination, T message) {
        template.convertAndSend(destination, message);
    }

    /**
     * 延时发送
     *
     * @param destination 发送的队列
     * @param data        发送的消息
     * @param time        延迟时间
     */
    public <T extends Serializable> void delaySend(Destination destination, T data, Long time) {
        Connection connection = null;
        Session session = null;
        MessageProducer producer = null;
        // 获取连接工厂
        ConnectionFactory connectionFactory = template.getConnectionFactory();
        try {
            // 获取连接
            connection = connectionFactory.createConnection();
            connection.start();
            // 获取session，true开启事务，false关闭事务
            session = connection.createSession(Boolean.TRUE, Session.AUTO_ACKNOWLEDGE);
            // 创建一个消息队列
            producer = session.createProducer(destination);
            producer.setDeliveryMode(JmsProperties.DeliveryMode.PERSISTENT.getValue());
            ObjectMessage message = session.createObjectMessage(data);
            //设置延迟时间
            message.setLongProperty(ScheduledMessage.AMQ_SCHEDULED_DELAY, time);
            // 发送消息
            producer.send(message);
            session.commit();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (producer != null) {
                    producer.close();
                }
                if (session != null) {
                    session.close();
                }
                if (connection != null) {
                    connection.close();
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
```

### 消费者

```java
@Component
public class DelayConsumer {
    @JmsListener(destination = "delay.queue")
    public void receiveQueue(MessageModel message) {
        System.out.println("收到消息:"+message);
    }
}
```

### 单元测试

```java
@SpringBootTest(classes = DemoApplication.class)
@RunWith(SpringRunner.class)
public class DemoDelayActivemq {
    /**
     * 消息生产者
     */
   @Autowired
    private DelayProducer producer;

    /**
     * 及时消息队列测试
     */
    @Test
    public void test() {
        MessageModel messageModel = new MessageModel();
        messageModel.setMessage("测试消息");
        messageModel.setTitile("消息0000");
        System.out.println("发送消息" + messageModel.getMessage());
        // 发送消息
        producer.send(DelayProducer.DEFAULT_QUEUE, messageModel);
    }


    /**
     * 延时消息队列测试
     */
    @Test
    public void test2() {
        for (int i = 0; i < 5; i++) {
            MessageModel messageModel = new MessageModel();
            messageModel.setMessage("测试消息");
            messageModel.setTitile("消息0000");
            System.out.println("发送延迟消息+" + messageModel.getMessage());
            // 发送延迟消息
            producer.delaySend(DelayProducer.DEFAULT_QUEUE, messageModel, 30000L);
        }
        try {
            // 休眠100秒，等等消息执行
            Thread.currentThread().sleep(100000L);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

## 5、ActiveMQ连接相关配置

新建一个 BeanConfig 类用来配置 ActiveMQ 连接相关配置。在工厂中设置开启手动消息确认模式。注意：ActiveMQ 默认是开启事务的，且在事务开启的时候消息为自动确认模式，就算是设置了手动确认也无效，因此想要开启手动确认消息模式，还需关掉事务。

```java
import org.apache.activemq.ActiveMQConnectionFactory;
import org.apache.activemq.ActiveMQSession;
import org.apache.activemq.command.ActiveMQQueue;
import org.apache.activemq.command.ActiveMQTopic;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jms.config.JmsListenerContainerFactory;
import org.springframework.jms.config.SimpleJmsListenerContainerFactory;
import org.springframework.jms.core.JmsMessagingTemplate;

import javax.jms.ConnectionFactory;
import javax.jms.Queue;
import javax.jms.Topic;

@Configuration
public class BeanConfig {

    @Value("${spring.activemq.broker-url}")
    private String brokerUrl;

    @Value("${spring.activemq.user}")
    private String username;

    @Value("${spring.activemq.password}")
    private String password;

    @Bean(name = "queue")
    public Queue queue() {
        return new ActiveMQQueue("queue-test");
    }

    @Bean(name = "delayQueue")
    public Queue delayQueue() {
        return new ActiveMQQueue("delay-queue-test");
    }

    @Bean
    public Topic topic() {
        return new ActiveMQTopic("topic-test");
    }

    @Bean
    public ConnectionFactory connectionFactory() {
        return new ActiveMQConnectionFactory(username, password, brokerUrl);
    }

    @Bean
    public JmsMessagingTemplate jmsMessageTemplate() {
        return new JmsMessagingTemplate(connectionFactory());
    }

    // 在Queue模式中，对消息的监听需要对containerFactory进行配置
    @Bean("queueListener")
    public JmsListenerContainerFactory<?> queueJmsListenerContainerFactory(ConnectionFactory connectionFactory) {
        SimpleJmsListenerContainerFactory factory = new SimpleJmsListenerContainerFactory();
        // 关闭事务
        factory.setSessionTransacted(false);
        // 设置手动确认，默认配置中Session是开启了事物的，即使我们设置了手动Ack也是无效的
        factory.setSessionAcknowledgeMode(ActiveMQSession.INDIVIDUAL_ACKNOWLEDGE);
        factory.setPubSubDomain(false);
        factory.setConnectionFactory(connectionFactory);
        return factory;
    }

    //在Topic模式中，对消息的监听需要对containerFactory进行配置
    @Bean("topicListener")
    public JmsListenerContainerFactory<?> topicJmsListenerContainerFactory(ConnectionFactory connectionFactory) {
        SimpleJmsListenerContainerFactory factory = new SimpleJmsListenerContainerFactory();
        factory.setConnectionFactory(connectionFactory);
        factory.setPubSubDomain(true);
        return factory;
    }
}
```



# 七、ActiveMQ的传输协议

## 1、简介

ActiveMQ支持的client-broker通讯协议有：TVP、NIO、UDP、SSL、Http(s)、VM。其中配置Transport Connector的文件在ActiveMQ安装目录的conf/activemq.xml中的\<transportConnectors>标签之内。

activemq传输协议的官方文档：http://activemq.apache.org/configuring-version-5-transports.html

  这些协议参见文件：%activeMQ安装目录%/conf/activemq.xml，下面是文件的重要的内容  

```xml
<transportConnectors>
    <!-- DOS protection, limit concurrent connections to 1000 and frame size to 100MB -->
    <transportConnector name="openwire" uri="tcp://0.0.0.0:61616?maximumConnections=1000&amp;wireFormat.maxFrameSize=104857600"/>
    <transportConnector name="amqp" uri="amqp://0.0.0.0:5672?maximumConnections=1000&amp;wireFormat.maxFrameSize=104857600"/>
    <transportConnector name="stomp" uri="stomp://0.0.0.0:61613?maximumConnections=1000&amp;wireFormat.maxFrameSize=104857600"/>
    <transportConnector name="mqtt" uri="mqtt://0.0.0.0:1883?maximumConnections=1000&amp;wireFormat.maxFrameSize=104857600"/>
    <transportConnector name="ws" uri="ws://0.0.0.0:61614?maximumConnections=1000&amp;wireFormat.maxFrameSize=104857600"/>
</transportConnectors>
```

在上文给出的配置信息中，URI描述信息的头部都是采用协议名称：例如

​	描述amqp协议的监听端口时，采用的URI描述格式为“amqp://······”；

​	描述Stomp协议的监听端口时，采用URI描述格式为“stomp://······”；

​	唯独在进行openwire协议描述时，URI头却采用的“tcp://······”。这是因为ActiveMQ中默认的消息协议就是openwire

## 2、支持的传输协议

​	除了tcp和nio协议，其他的了解就行。各种协议有各自擅长该协议的中间件，工作中一般不会使用activemq去实现这些协议。如： mqtt是物联网专用协议，采用的中间件一般是mosquito。ws是websocket的协议，是和前端对接常用的，一般在java代码中内嵌一个基站（中间件）。stomp好像是邮箱使用的协议的，各大邮箱公司都有基站（中间件）

![img](images\clip_image102.jpg)

### TCP协议

(1) Transmission Control Protocol(TCP)是默认的。TCP的Client监听端口61616

(2) 在网络传输数据前，必须要先序列化数据，消息是通过一个叫wire protocol的来序列化成字节流。

(3) TCP连接的URI形式如：tcp://HostName:port?key=value&key=value，后面的参数是可选的。

(4) TCP传输的的优点：

​	TCP协议传输可靠性高，稳定性强

​	高效率：字节流方式传递，效率很高

​	有效性、可用性：应用广泛，支持任何平台

(5) 关于Transport协议的可选配置参数可以参考官网http://activemq.apache.org/tcp-transport-reference

### NIO协议

(1) New I/O API Protocol(NIO)

(2) NIO协议和TCP协议类似，但NIO更侧重于底层的访问操作。它允许开发人员对同一资源可有更多的client调用和服务器端有更多的负载。

(3) 适合使用NIO协议的场景：

​	可能有大量的Client去连接到Broker上，一般情况下，大量的Client去连接Broker是被操作系统的线程所限制的。因此，NIO的实现比TCP需要更少的线程去运行，所以建议使用NIO协议。

​	可能对于Broker有一个很迟钝的网络传输，NIO比TCP提供更好的性能。

(4) NIO连接的URI形式：nio://hostname:port?key=value&key=value

(5) 关于Transport协议的可选配置参数可以参考官网http://activemq.apache.org/configuring-version-5-transports.html

![img](images\clip_image05.jpg)

### AMQP协议

![img](images\clip_image052.jpg)

### STOMP协议

![img](images\222.jpg)

### MQTT协议

![img](images\clip_image0552.jpg)

## 3、NIO协议案例

### **(1)**   **修改配置文件**activemq.xml

![img](images\clip_image00222.jpg)

①　修改配置文件activemq.xml在\<transportConnectors>节点下添加如下内容：

\<transportConnector name="nio" uri="nio://0.0.0.0:61618?trace=true" />

②　修改完成后重启activemq: 

service activemq restart

③　查看管理后台，可以看到页面多了nio

![img](images\clip_image2002.jpg)

## （2）代码

生产者

```java
public class NioProducer {


    public static final String ACTIVEMQ_URL = "nio://192.168.30.128:61616";
    public static final String QUEUE_NAME = "nio-test";

    public static void main(String[] args) throws JMSException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        Connection connection = activeMQConnectionFactory.createConnection();
        connection.start();
        //1.创建会话session，两个参数transacted=事务,acknowledgeMode=确认模式(签收)
        //设置为开启事务
        Session session = connection.createSession(true, Session.CLIENT_ACKNOWLEDGE);
        Queue queue = session.createQueue(QUEUE_NAME);
        MessageProducer producer = session.createProducer(queue);
        try {
            for (int i = 0; i < 3; i++) {
                TextMessage textMessage = session.createTextMessage("tx msg--" + i);
                producer.send(textMessage);
            }
            // 2. 开启事务后，使用commit提交事务，这样这批消息才能真正的被提交。
            session.commit();
            System.out.println("消息发送完成");
        } catch (Exception e) {
            System.out.println("出现异常,消息回滚");
            // 3. 工作中一般，当代码出错，我们在catch代码块中回滚。这样这批发送的消息就能回滚。
            session.rollback();
        } finally {
            //4. 关闭资源
            producer.close();
            session.close();
            connection.close();
        }

    }


}
```

消费者

```java
public class NioConsumer {
    public static final String ACTIVEMQ_URL = "nio://192.168.30.128:61616";
    public static final String QUEUE_NAME = "nio-test";

    public static void main(String[] args) throws JMSException, IOException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        Connection connection = activeMQConnectionFactory.createConnection();
        connection.start();
        // 创建会话session，两个参数transacted=事务,acknowledgeMode=确认模式(签收)
        // 消费者开启了事务就必须手动提交，不然会重复消费消息
        Session session = connection.createSession(Boolean.TRUE, Session.CLIENT_ACKNOWLEDGE);
        Queue queue = session.createQueue(QUEUE_NAME);
        MessageConsumer messageConsumer = session.createConsumer(queue);
        int a = 0;
        messageConsumer.setMessageListener((message -> {
            TextMessage textMessage = (TextMessage) message;
            try {
                System.out.println("***消费者接收到的消息:   " + textMessage.getText());
                textMessage.acknowledge();
            } catch (JMSException e) {
                e.printStackTrace();
                System.out.println("出现异常，消费失败，放弃消费");
                try {
                    session.rollback();
                } catch (JMSException jmsException) {
                    jmsException.printStackTrace();
                }
            }
        }
        ));
        //关闭资源
        System.in.read();
        messageConsumer.close();
        session.close();
        connection.close();

    }
}
```

## 4、 NIO协议案例增强

### **(1)**   目的

上面是Openwire协议传输底层使用NIO网络IO模型。 如何让其他协议传输底层也使用NIO网络IO模型呢？

![img](images\clip_image020222.jpg)

![img](images\clip_image21002.jpg)

### **(2)**   **修改配置文件**activemq.xml



```xml
<transportConnectors>
    <transportConnector name="openwire" uri="tcp://0.0.0.0:61626?maximumConnections=1000&amp;wireFormat.maxFrameSize=104857600"/>
    <transportConnector name="amqp" uri="amqp://0.0.0.0:5682?maximumConnections=1000&amp;wireFormat.maxFrameSize=104857600"/>
    <transportConnector name="stomp" uri="stomp://0.0.0.0:61623?maximumConnections=1000&amp;wireFormat.maxFrameSize=104857600"/>
    <transportConnector name="mqtt" uri="mqtt://0.0.0.0:1893?maximumConnections=1000&amp;wireFormat.maxFrameSize=104857600"/>
    <transportConnector name="ws" uri="ws://0.0.0.0:61624?maximumConnections=1000&amp;wireFormat.maxFrameSize=104857600"/>
    <transportConnector name="nio" uri="nio://0.0.0.0:61618?trace=true" />
    <transportConnector name="auto+nio" uri="auto+nio://0.0.0.0:61608?maximumConnections=1000&amp;wireFormat.maxFrameSize=104857600&amp;org.apache.activemq.transport.nio.SelectorManager.corePoolSize=20&amp;org.apache.activemq.transport.nio.Se1ectorManager.maximumPoo1Size=50"/>
</transportConnectors>
```

auto  : 针对所有的协议，他会识别我们是什么协议。

nio   ：使用NIO网络IO模型

修改配置文件后重启activemq。



# 八、ActiveMQ的消息存储和持久化

## 1、介绍

### **(1)**   此处持久化和之前的持久化的区别

![img](images\clip_imadsge002.jpg)

MQ高可用：事务、可持久、签收，是属于MQ自身特性，自带的。这里的持久化是外力，是外部插件。之前讲的持久化是MQ的外在表现，现在讲的的持久是是底层实现。

### (2) 持久化是什么

​	官网文档：http://activemq.apache.org/persistence

​	持久化是什么？一句话就是：ActiveMQ宕机了，消息不会丢失的机制。

​	说明：为了避免意外宕机以后丢失信息，需要做到重启后可以恢复消息队列，消息系统一半都会采用持久化机制。ActiveMQ的消息持久化机制有JDBC，AMQ，KahaDB和LevelDB，无论使用哪种持久化方式，消息的存储逻辑都是一致的。就是在发送者将消息发送出去后，消息中心首先将消息存储到本地数据文件、内存数据库或者远程数据库等。再试图将消息发给接收者，成功则将消息从存储中删除，失败则继续尝试尝试发送。消息中心启动以后，要先检查指定的存储位置是否有未成功发送的消息，如果有，则会先把存储位置中的消息发出去。

## 2、持久化有哪些

###  (1) AMQ Message Store

基于文件的存储机制，是以前的默认机制，现在不再使用。

AMQ是一种文件存储形式，它具有写入速度快和容易恢复的特点。消息存储再一个个文件中文件的默认大小为32M，当一个文件中的消息已经全部被消费，那么这个文件将被标识为可删除，在下一个清除阶段，这个文件被删除。AMQ适用于ActiveMQ5.3之前的版本

### （2）kahaDB

现在默认的。下面我们再详细介绍。

### （3）JDBC消息存储

下面我们再详细介绍

#### （4）LevelDB消息存储

过于新兴的技术，现在有些不确定

![img](images\clip_image0222302.jpg)

## 3、kahaDB消息存储

### 介绍

基于日志文件，从ActiveMQ5.4（含）开始默认的持久化插件。

官网文档：http://activemq.aache.org/kahadb

官网上还有一些其他配置参数。

配置文件activemq.xml中，如下

```xml
<persistenceAdapter>
    <kahaDB directory="${activemq.data}/kahadb"/>
</persistenceAdapter>
```

日志文件的存储目录在：%activemq安装目录%/data/kahadb

### 说明

![img](images\clip_image00222332.jpg)





###  KahaDB的存储原理

![img](images\clip_image002dd2.jpg)



![img](images\clip_image034302.jpg)

## 4、JDBC消息存储

### 原理图

![image-20201122140604614](images\image-20201122140604614.png)

### 添加mysql数据库的驱动包到lib文件夹

![image-20201122140915790](images\image-20201122140915790.png)



### **jdbcPersistenceAdapter配置**

![img](images\clip_image00sss2.jpg)

修改配置文件activemq.xml。将之前的替换为jdbc的配置。如下：

```xml
<!--  
<persistenceAdapter>
     <kahaDB directory="${activemq.data}/kahadb"/>
</persistenceAdapter>
-->
<persistenceAdapter>
  <jdbcPersistenceAdapter dataSource="#mysql-ds" createTablesOnStartup="true"/>
</persistenceAdapter>
```

### 数据库连接池配置

需要我们准备一个mysql数据库，并创建一个名为activemq的数据库。

![image-20201122141147926](images\image-20201122141147926.png)

在\</broker>标签和\<import>标签之间插入数据库连接池配置

![image-20201122141230646](images\image-20201122141230646.png)

具体操作如下：

```xml
<bean id="mysql-ds" class="org.apache.commons.dbcp2.BasicDataSource" destroy-method="close">
  <property name="driverClassName" value="com.mysql.jdbc.Driver"/>
  <property name="url" value="jdbc:mysql://mysql数据库URL/activemq?relaxAutoCommit=true"/>
  <property name="username" value="mysql数据库用户名"/>
  <property name="password" value="mysql数据库密码"/>
  <property name="poolPreparedStatements" value="true"/>
</bean>
```

之后需要建一个数据库，名为activemq。新建的数据库要采用latin1 或者ASCII编码。https://blog.csdn.net/JeremyJiaming/article/details/88734762

默认是的dbcp数据库连接池，如果要换成其他数据库连接池，需要将该连接池jar包，也放到lib目录下。

### 创建SQL和创建表名

​	重启activemq。会自动生成如下3张表。如果没有自动生成，需要我们手动执行SQL。我个人建议要自动生成，我在操作过程中查看日志文件，发现了不少问题，最终解决了这些问题后，是能够自动生成的。如果不能自动生成说明你的操作有问题。如果实在不行，下面是手动建表的SQL:

```sql
create table ACTIVEMQ_ACKS
(
  CONTAINER   varchar(250)   not null comment '消息的Destination',
  SUB_DEST   varchar(250)   null comment '如果使用的是Static集群，这个字段会有集群其他系统的信息',
  CLIENT_ID   varchar(250)   not null comment '每个订阅者都必须有一个唯一的客户端ID用以区分',
  SUB_NAME   varchar(250)   not null comment '订阅者名称',
  SELECTOR   varchar(250)   null comment '选择器，可以选择只消费满足条件的消息，条件可以用自定义属性实现，可支持多属性AND和OR操作',
  LAST_ACKED_ID bigint      null comment '记录消费过消息的ID',
  PRIORITY   bigint default 5 not null comment '优先级，默认5',
  XID      varchar(250)   null,
  primary key (CONTAINER, CLIENT_ID, SUB_NAME, PRIORITY)
)
 comment '用于存储订阅关系。如果是持久化Topic，订阅者和服务器的订阅关系在这个表保存';

create index ACTIVEMQ_ACKS_XIDX
  on ACTIVEMQ_ACKS (XID);

-- auto-generated definition
create table ACTIVEMQ_LOCK
(

  ID     bigint    not null
  primary key,
  TIME    bigint    null,
  BROKER_NAME varchar(250) null
);

-- auto-generated definition
create table ACTIVEMQ_MSGS

(
  ID     bigint    not null
  primary key,
  CONTAINER varchar(250) not null,
  MSGID_PROD varchar(250) null,
  MSGID_SEQ bigint    null,
  EXPIRATION bigint    null,
  MSG    blob     null,
  PRIORITY  bigint    null,
  XID    varchar(250) null
);


create index ACTIVEMQ_MSGS_CIDX
  on ACTIVEMQ_MSGS (CONTAINER);
  
create index ACTIVEMQ_MSGS_EIDX
  on ACTIVEMQ_MSGS (EXPIRATION);

create index ACTIVEMQ_MSGS_MIDX
  on ACTIVEMQ_MSGS (MSGID_PROD, MSGID_SEQ);

create index ACTIVEMQ_MSGS_PIDX
  on ACTIVEMQ_MSGS (PRIORITY);

create index ACTIVEMQ_MSGS_XIDX
  on ACTIVEMQ_MSGS (XID);
```

#### ACTIVEMQ_MSGS数据表

![image-20201122141807823](images\image-20201122141807823.png)

#### **ACTIVEMQ_ACKS数据表**

![img](images\clip_imagessssd002.jpg)

#### **ACTIVEMQ_LOCK数据表**

![img](images\clip_imagesdsf002.jpg)



### Queeue验证和数据表变化

![image-20201122142041593](images\image-20201122142041593.png)

queue模式，非持久化不会将消息持久化到数据库。

queue模式，持久化会将消息持久化数据库。

我们使用queue模式持久化，发布3条消息后，发现ACTIVEMQ_MSGS数据表多了3条数据。

![img](images\clip_image002dsdfs.jpg)

启动消费者，消费了所有的消息后，发现数据表的数据消失了。

### topic验证和说明

```java
public class JmsConsumerTopicPersistent {
    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616";

    public static final String TOPIC_NAME = "topic_demon";

    public static void main(String[] args) throws JMSException, IOException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        Connection connection = activeMQConnectionFactory.createConnection();
        // 设置客户端ID。向MQ服务器注册自己的名称
        connection.setClientID("harry");
        connection.start();
        Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
        Topic topic = session.createTopic(TOPIC_NAME);
        // 创建一个topic订阅者对象。一参是topic，二参是订阅者名称
        TopicSubscriber topicSubscriber = session.createDurableSubscriber(topic,"remark...");
        // 之后再开启连接
        connection.start();
        Message message = topicSubscriber.receive();
        while (null != message){
            TextMessage textMessage = (TextMessage)message;
            System.out.println(" 收到的持久化 topic ："+textMessage.getText());
            message = topicSubscriber.receive();
        }
        session.close();
        connection.close();
    }

}
```

我们先启动一下持久化topic的消费者。看到ACTIVEMQ_ACKS数据表多了一条消息。

![image-20201123203128213](images\image-20201123203128213.png)

   我们启动持久化生产者发布3个数据，ACTIVEMQ_MSGS数据表新增3条数据，消费者消费所有的数据后，ACTIVEMQ_MSGS数据表的数据并没有消失。持久化topic的消息不管是否被消费，是否有消费者，产生的数据永远都存在，且只存储一条。这个是要注意的，持久化的topic大量数据后可能导致性能下降。这里就像公总号一样，消费者消费完后，消息还会保留。  

### 总结

![image-20201123203330967](images\image-20201123203330967.png)

![image-20201123203358400](images\image-20201123203358400.png)

## 5、 JDBC Message Store with ActiveMQ Journal

### 说明

​    这种方式克服了JDBC Store的不足，JDBC每次消息过来，都需要去写库读库。ActiveMQ Journal，使用高速缓存写入技术，大大提高了性能。当消费者的速度能够及时跟上生产者消息的生产速度时，journal文件能够大大减少需要写入到DB中的消息。

​    举个例子：生产者生产了1000条消息，这1000条消息会保存到journal文件，如果消费者的消费速度很快的情况下，在journal文件还没有同步到DB之前，消费者已经消费了90%的以上消息，那么这个时候只需要同步剩余的10%的消息到DB。如果消费者的速度很慢，这个时候journal文件可以使消息以批量方式写到DB。

​    为了高性能，这种方式使用日志文件存储+数据库存储。先将消息持久到日志文件，等待一段时间再将未消费的消息持久到数据库。该方式要比JDBC性能要高。

### 配置

面是基于上面JDBC配置，再做一点修改：

![image-20201123203614756](images\image-20201123203614756.png)



![image-20201123203637146](images\image-20201123203637146.png)

# 九、Zookeeper搭建ActiveMQ集群服务

## 原理说明

使用Zookeeper集群注册所有的ActiveMQ Broker但只有其中一个Broker可以提供服务他将被视为Master，其他的Broker处于待机状态被视为Slave

如果Mster因故障而不能提供服务，ZooKeeper会从Slave中选举出一个Broker充当master

Slave连接Master 并同步他们的存储状态，Slave不接受客户端连接。所有存储操作都将被复制到连接至Master和Slaves。

如果Mster宕机得到了最新更新的Slave会成为Mster。故障节点恢复后重新进入到集群并连接Master进入Slave模式

所有需要同步的消息操作都将等待存储状态被复制到其他法定节点的操作完成才能完成。

所以如果配置了repicas=3，那么法定大小是(3/2)+1=2。Master将会存储并更新然后等待(2-1)=1个slave存储和更新完成，再汇报success。

有一个node要做作为观察者存在。当一个新的Master被选中，至少需要保障一个法定的node在线一能够找到拥有最新状态的node。这个node才可以成为想的Master

## Zooker集群搭建

### 安装zookeeper

```
[root@localhost opt]# tar -zxvf apache-zookeeper-3.6.2-bin.tar.gz
[root@localhost opt]# cp apache-zookeeper-3.6.2-bin /opt/zookeeper1
[root@localhost opt]# cp -r /opt/zookeeper1/ /opt/zookeeper2
[root@localhost opt]# cp -r /opt/zookeeper1/ /opt/zookeeper3


```

### 配置服务器编号

在/opt/zookeeper1 下创建zkData目录 touch一个mydi

```bash
[root@localhost zookeeper1]# mkdir -p zkData
[root@localhost zookeeper1]# ls
bin  conf  docs  lib  LICENSE.txt  NOTICE.txt  README.md  README_packaging.md  zkData
[root@localhost zookeeper1]# cd zkData/
[root@localhost zkData]# ls
[root@localhost zkData]# touch myid
[root@localhost zkData]# vim myid
```

在文件中添加与server对应的编号：2

其他两个节点同理

### 修改配置文件

修改配置文件的文件名

```bash
[root@localhost conf]# mv zoo_sample.cfg zoo.cfg
```

zookeeper1

注：因为是在一台机器上模拟集群，所以端口不能重复，这里用2181~2183，2287~2289，以及3387~3389相互错开。另外每个zk的instance

/opt/zookeeper1/conf/zoo_sample.cfg

[root@localhost conf]# vim zoo_sample.cfg

```bash
# The number of milliseconds of each tick
tickTime=2000
# The number of ticks that the initial
# synchronization phase can take
initLimit=10
# The number of ticks that can pass between
# sending a request and getting an acknowledgement
syncLimit=5
# the directory where the snapshot is stored.
# do not use /tmp for storage, /tmp here is just
# example sakes.
dataDir=/opt/zookeeper1/zkData
# the port at which the clients will connect
clientPort=2181
server.2=192.168.30.128:2887:3887
server.3=192.168.30.128:2888:3888
server.4=192.168.30.128:2889:3889
```

zookeeper2

```bash
# increase this if you need to handle more clients
dataDir=/opt/zookeeper2/zkData
# the port at which the clients will connect
clientPort=2182
server.2=192.168.30.128:2887:3887
server.3=192.168.30.128:2888:3888
server.4=192.168.30.128:2889:3889
#maxClientCnxns=60

```

zookeeper3

```bash
# increase this if you need to handle more clients
dataDir=/opt/zookeeper3/zkData
# the port at which the clients will connect
clientPort=2183
server.2=192.168.30.128:2887:3887
server.3=192.168.30.128:2888:3888
server.4=192.168.30.128:2889:3889
```

生产环境中，分布式集群部署的步骤与上面基本相同，只不过因为各zk server分布在不同的机器，分布在不同的机器后，不存在端口冲突问题，可以让每个服务器的zk均采用相同的端口，这样管理起来比较方便。

### 分别启动Zookeeper

```bash
[root@localhost conf]# /opt/zookeeper1/bin/zkServer.sh start
[root@localhost conf]# /opt/zookeeper2/bin/zkServer.sh start
[root@localhost conf]# /opt/zookeeper3/bin/zkServer.sh start
```

查看状态：

```bash
[root@localhost conf]# /opt/zookeeper1/bin/zkServer.sh status
/usr/bin/java
ZooKeeper JMX enabled by default
Using config: /opt/zookeeper1/bin/../conf/zoo.cfg
Client port found: 2181. Client address: localhost. Client SSL: false.
Mode: leader
[root@localhost conf]# /opt/zookeeper2/bin/zkServer.sh status
/usr/bin/java
ZooKeeper JMX enabled by default
Using config: /opt/zookeeper2/bin/../conf/zoo.cfg
Client port found: 2182. Client address: localhost. Client SSL: false.
Mode: follower
[root@localhost conf]# /opt/zookeeper3/bin/zkServer.sh status
/usr/bin/java
ZooKeeper JMX enabled by default
Using config: /opt/zookeeper3/bin/../conf/zoo.cfg
Client port found: 2183. Client address: localhost. Client SSL: false.
Mode: follower
```



## 创建MQ集群

### 创建MQ目录

```bash
mkdir /mq_cluster/
cd /mq_cluster/
cp -r /opt/acpche-activemq  mq_node01
cp -r mq_node01  mq_node02
cp -r mq_node01  mq_node03
```

### 修改管理控制台端口

mq_node01全部默认不动

修改其他MQ的控制端口

![image-20201121110805903](images\image-20201121110805903.png)

### Hostname名字的映射

![image-20201121111202969](images\image-20201121111202969.png)

### ActiveMQ集群配置

![image-20201121111338404](images\image-20201121111338404.png)

3个节点的BrokerName要求全部一致

![image-20201121111459720](images\image-20201121111459720.png)

3个节点的持久化配置

![image-20201121111746024](images\image-20201121111746024.png)

![ ](images\image-20201121111812073.png)

```xml
<!-- 持久化的部分为ZooKeeper集群连接地址-->  
<persistenceAdapter>  
    <replicatedLevelDB  
      directory="${activemq.data}/leveldb"  
      replicas="3"  
      bind="tcp://0.0.0.0:0:63631"  
      zkAddress="localhost:2181,localhost:2182,localhost:2183"   
      zkPath="/activemq/leveldb-stores"  
      hostname="zzyymq-server"  
      />  
</persistenceAdapter>
<!-- 

# directory： 存储数据的路径
# replicas：集群中的节点数【(replicas/2)+1公式表示集群中至少要正常运行的服务数量】，3台集群那么允许1台宕机， 另外两台要正常运行  
# bind：当该节点成为master后，它将绑定已配置的地址和端口来为复制协议提供服务。还支持使用动态端口。只需使用tcp://0.0.0.0:0进行配置即可，默认端口为61616。 
# zkAddress：ZK的ip和port， 如果是集群，则用逗号隔开(这里作为简单示例ZooKeeper配置为单点， 这样已经适用于大多数环境了， 集群也就多几个配置) 
# zkPassword：当连接到ZooKeeper服务器时用的密码，没有密码则不配置。 
# zkPah：ZK选举信息交换的存贮路径，启动服务后actimvemq会到zookeeper上注册生成此路径   
# hostname： ActiveMQ所在主机的IP
# 更多参考：http://activemq.apache.org/replicated-leveldb-store.html
```



### 修改各个节点的消息端口

![image-20201121112318194](images\image-20201121112318194.png)

### 按顺序启动3个ActiveMQ节点，到这一步前提是zk集群已经成功启动运行

vim amq_batch.sh

 ![image-20201121112553672](images\image-20201121112553672.png)

### 查看ZK的节点状态

3台zk集群链接任意一台

![image-20201121112959886](images\image-20201121112959886.png)

查看master

![image-20201121113059397](images\image-20201121113059397.png)

```bash
[zk: 127.0.0.1:2181(CONNECTED) 1] ls /actimemq/leveldb-stores
Node does not exist: /actimemq/leveldb-stores
[zk: 127.0.0.1:2181(CONNECTED) 2] ls /activemq/leveldb-stores
[00000000000, 00000000001, 00000000002]
[zk: 127.0.0.1:2181(CONNECTED) 3] ls /activemq/leveldb-stores/00000000000
[]
[zk: 127.0.0.1:2181(CONNECTED) 4] get /activemq/leveldb-stores/00000000000
{"id":"zzyymq","container":null,"address":null,"position":-1,"weight":1,"elected":"0000000000"}
[zk: 127.0.0.1:2181(CONNECTED) 5] get /activemq/leveldb-stores/00000000001
{"id":"zzyymq","container":null,"address":null,"position":-1,"weight":1,"elected":null}
[zk: 127.0.0.1:2181(CONNECTED) 6] get /activemq/leveldb-stores/00000000002
{"id":"zzyymq","container":null,"address":null,"position":-1,"weight":1,"elected":null}
[zk: 127.0.0.1:2181(CONNECTED) 7]
```



## 集群可用性测试

ActiveMQ的客户端只能访问Master的Broker，其他处于Slave和Broker不能访问，所以客户端连接的Broker应该使用failover协议(失败转移)

当一个ActiveMQ节点挂掉或者一个Zookeeper节点挂掉，ActiveMQ服务依然正常运转，如果仅剩一个ActiveMQ节点，由于不能选举Master，所以ActiveMQ不能正常运行

同样的，如果Zookeeper仅剩一个节点活动，不管ActiveMQ各节点存活，ActiveMQ也不能正常提供服务。(ActiveMQ的高可用依赖于Zookeeper集群的高可用)

### 代码生成者和消费者都修改

![image-20201121121109878](images\image-20201121121109878.png)

### 干掉一台ActiveMQ节点，它会自动切换到另外一个活着的

![image-20201121121649146](images\image-20201121121649146.png)

# 十、高级特性

## 1、异步投递

### 异步投递是什么

![image-20201123203901678](images\image-20201123203901678.png)

自我理解：此处的异步是指生产者和broker之间发送消息的异步。不是指生产者和消费者之间异步。

官网介绍：http://activemq.apache.org/async-sends

总结：

​	①　异步发送可以让生产者发的更快。

​	②　如果异步投递不需要保证消息是否发送成功，发送者的效率会有所提高。如果异步投递还需要保证消息是否成功发送，并采用了回调的方式，发送者的效率提高不多，这种就有些鸡肋。

### 代码实现

![image-20201123204447376](images\image-20201123204447376.png)

生产者代码

```java
public class JmsAsyncProduce {

    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616?jms.useAsyncSend=true";
    public static final String QUEUE_NAME = "Async";

    public static void main(String[] args) throws JMSException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        // 方式1
        activeMQConnectionFactory.setUseAsyncSend(true);

        Connection connection = activeMQConnectionFactory.createConnection();
        // 方式2
        ((ActiveMQConnection)connection).setUseAsyncSend(true);
        connection.start();

        //设置为开启事务
        Session session = connection.createSession(false, Session.CLIENT_ACKNOWLEDGE);
        Queue queue = session.createQueue(QUEUE_NAME);
        MessageProducer producer = session.createProducer(queue);
        try {
            for (int i = 0; i < 3; i++) {
                TextMessage textMessage = session.createTextMessage("tx msg--" + i);
                producer.send(textMessage);
            }

            session.commit();
            System.out.println("消息发送完成");
        } catch (Exception e) {
            System.out.println("出现异常,消息回滚");

            session.rollback();
        } finally {
            producer.close();
            session.close();
            connection.close();
        }
    }
}
```

### 异步发送如何确认发送成功

![image-20201123204930150](images\image-20201123204930150.png)

下面演示异步发送的回调

```java
public class JmsAsyncProduce {

    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616?jms.useAsyncSend=true";
    public static final String QUEUE_NAME = "Async";

    public static void main(String[] args) throws JMSException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        // 方式1
        activeMQConnectionFactory.setUseAsyncSend(true);

        Connection connection = activeMQConnectionFactory.createConnection();
        // 方式2
        ((ActiveMQConnection)connection).setUseAsyncSend(true);
        connection.start();

        //设置为开启事务
        Session session = connection.createSession(true, Session.CLIENT_ACKNOWLEDGE);
        Queue queue = session.createQueue(QUEUE_NAME);
        ActiveMQMessageProducer activeMQMessageProducer = (ActiveMQMessageProducer)session.createProducer(queue);
        try {
            for (int i = 0; i < 3; i++) {
                TextMessage textMessage = session.createTextMessage("tx msg--" + i);
                textMessage.setJMSMessageID(UUID.randomUUID().toString()+"orderTEST");
                final String  msgId = textMessage.getJMSMessageID();
                activeMQMessageProducer.send(textMessage, new AsyncCallback() {
                    @Override
                    public void onSuccess() {
                        System.out.println("成功发送消息Id:"+msgId);
                    }

                    @Override
                    public void onException(JMSException e) {
                        System.out.println("失败发送消息Id:"+msgId);
                    }
                });
            }

            session.commit();
            System.out.println("消息发送完成");
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("出现异常,消息回滚");
            session.rollback();
        } finally {
            activeMQMessageProducer.close();
            session.close();
            connection.close();
        }
    }
}
```

控制台观察发送消息的信息(未消费的消息)：

![image-20201123210427330](images\image-20201123210427330.png)

## 2、延迟投递和定时投递

### 介绍

官网文档：http://activemq.apache.org/delay-and-schedule-message-delivery.html

![image-20201123210548530](images\image-20201123210548530.png)

![image-20201123210615465](images\image-20201123210615465.png)

### 修改配置文件并重启

![image-20201123210657383](images\image-20201123210657383.png)

### 代码实现

java代码里面封装的辅助消息类型：ScheduleMessage

```java
public class DelayQueueProducer {
    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616";
    public static final String QUEUE_NAME = "Delay";

    public static void main(String[] args) throws JMSException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        Connection connection = activeMQConnectionFactory.createConnection();
        connection.start();
        Session session = connection.createSession(true, Session.CLIENT_ACKNOWLEDGE);
        Queue queue = session.createQueue(QUEUE_NAME);
        MessageProducer producer = session.createProducer(queue);
        long delay =  10*1000;
        long period = 5*1000;
        int repeat = 3 ;
        try {
            for (int i = 0; i < 3; i++) {
                TextMessage textMessage = session.createTextMessage("tx msg--" + i);
                // 延迟的时间
                textMessage.setLongProperty(ScheduledMessage.AMQ_SCHEDULED_DELAY, delay);
                // 重复投递的时间间隔
                textMessage.setLongProperty(ScheduledMessage.AMQ_SCHEDULED_PERIOD, period);
                // 重复投递的次数
                textMessage.setIntProperty(ScheduledMessage.AMQ_SCHEDULED_REPEAT, repeat);
                producer.send(textMessage);
            }
            session.commit();
            System.out.println("消息发送完成");
        } catch (Exception e) {
            System.out.println("出现异常,消息回滚");
            session.rollback();
        } finally {
            producer.close();
            session.close();
            connection.close();
        }

    }
}
```

  消费者代码。和之前代码都一样  

## 3、消费的重试机制

### 是什么

官网文档：http://activemq.apache.org/redelivery-policy

是什么： 消费者收到消息，之后出现异常了，没有告诉broker确认收到该消息，broker会尝试再将该消息发送给消费者。尝试n次，如果消费者还是没有确认收到该消息，那么该消息将被放到死信队列重，之后broker不会再将该消息发送给消费者。

### 具体哪些情况会引发消息重发

①　Client用了transactions且再session中调用了rollback

②　Client用了transactions且再调用commit之前关闭或者没有commit

③　Client再CLIENT_ACKNOWLEDGE的传递模式下，session中调用了recover

### 消息重发时间间隔和重发次数

间隔：1

次数：6

每秒发6次

### 有毒消息Poison ACK

一个消息被redelivedred超过默认的最大重发次数（默认6次）时，消费者会给MQ发一个“poison ack”表示这个消息有毒，告诉broker不要再发了。这个时候broker会把这个消息放到DLQ（死信队列）。

### 属性说明

![image-20201123211853179](images\image-20201123211853179.png)

### 代码验证

  生产者。发送3条数据。代码省略.....  

消费者。开启事务，却没有commit。重启消费者，前6次都能收到消息，到第7次，不会再收到消息。代码：

```java
public class DeadQueueConsumer {
    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616";
    public static final String QUEUE_NAME = "dead";

    public static void main(String[] args) throws JMSException, IOException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        Connection connection = activeMQConnectionFactory.createConnection();
        connection.start();
        // 创建会话session，两个参数transacted=事务,acknowledgeMode=确认模式(签收)
        // 消费者开启了事务就必须手动提交，不然会重复消费消息
        final Session session = connection.createSession(true, Session.CLIENT_ACKNOWLEDGE);
        Queue queue = session.createQueue(QUEUE_NAME);
        MessageConsumer messageConsumer = session.createConsumer(queue);
        int a = 0;
        messageConsumer.setMessageListener((message -> {
            TextMessage textMessage = (TextMessage) message;
            try {
                System.out.println("***消费者接收到的消息:   " + textMessage.getText());
//                session.commit();
            } catch (JMSException e) {
                e.printStackTrace();
                System.out.println("出现异常，消费失败，放弃消费");
                try {
                    session.rollback();
                } catch (JMSException jmsException) {
                    jmsException.printStackTrace();
                }
            }
        }
        ));
        //关闭资源
        System.in.read();
        messageConsumer.close();
        session.close();
        connection.close();

    }
}
```

  activemq管理后台。多了一个名为ActiveMQ.DLQ队列，里面多了3条消息。  

![image-20201123212405536](images\image-20201123212405536.png)

### 代码修改默认参数

```java
public class DeadQueueConsumer {
    public static final String ACTIVEMQ_URL = "tcp://192.168.30.128:61616";
    public static final String QUEUE_NAME = "dead";

    public static void main(String[] args) throws JMSException, IOException {
        ActiveMQConnectionFactory activeMQConnectionFactory = new ActiveMQConnectionFactory(ACTIVEMQ_URL);
        // 修改默认参数，设置消息消费重试3次
        RedeliveryPolicy redeliveryPolicy = new RedeliveryPolicy();
        redeliveryPolicy.setMaximumRedeliveries(3);
        activeMQConnectionFactory.setRedeliveryPolicy(redeliveryPolicy);

        Connection connection = activeMQConnectionFactory.createConnection();
        connection.start();
        // 创建会话session，两个参数transacted=事务,acknowledgeMode=确认模式(签收)
        // 消费者开启了事务就必须手动提交，不然会重复消费消息
        final Session session = connection.createSession(true, Session.CLIENT_ACKNOWLEDGE);
        Queue queue = session.createQueue(QUEUE_NAME);
        MessageConsumer messageConsumer = session.createConsumer(queue);
        int a = 0;
        messageConsumer.setMessageListener((message -> {
            TextMessage textMessage = (TextMessage) message;
            try {
                System.out.println("***消费者接收到的消息:   " + textMessage.getText());
//                session.commit();
            } catch (JMSException e) {
                e.printStackTrace();
                System.out.println("出现异常，消费失败，放弃消费");
                try {
                    session.rollback();
                } catch (JMSException jmsException) {
                    jmsException.printStackTrace();
                }
            }
        }
        ));
        //关闭资源
        System.in.read();
        messageConsumer.close();
        session.close();
        connection.close();

    }
}
```

###   **整合**spring

![image-20201123212548193](images\image-20201123212548193.png)

## 4、死信队列

官网文档： http://activemq.apache.org/redelivery-policy

死信队列：异常消息规避处理的集合，主要处理失败的消息。

![image-20201123212640143](images\image-20201123212640143.png)

![image-20201123212718506](images\image-20201123212718506.png)

### 死信队列的配置(一般采用默认)

#### sharedDeadLetterStrategy

不管是queue还是topic，失败的消息都放到这个队列中。下面修改activemq.xml的配置，可以达到修改队列的名字。

![image-20201123212840769](images\image-20201123212840769.png)

#### individualDeadLetterStrategy

可以为queue和topic单独指定两个死信队列。还可以为某个话题，单独指定一个死信队列。

![image-20201123212932691](images\image-20201123212932691.png)

![image-20201123212953949](images\image-20201123212953949.png)

#### 自动删除过期消息

过期消息是指生产者指定的过期时间，超过这个时间的消息

![image-20201123213101797](images\image-20201123213101797.png)

#### 存放费持久消息到死信队列中

![image-20201123213147816](images\image-20201123213147816.png)

## 5、消息不被重复消费，幂等性

![image-20201123213252084](images\image-20201123213252084.png)

