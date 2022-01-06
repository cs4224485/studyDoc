# 一 进程与线程

## 1 简介

### 进程 

​	 程序由指令和数据组成，但这些指令要运行，数据要读写，就必须将指令加载至 CPU，数据加载至内存。在 指令运行过程中还需要用到磁盘、网络等设备。进程就是用来加载指令、管理内存、管理 IO 

​	 当一个程序被运行，从磁盘加载这个程序的代码至内存，这时就开启了一个进程。

​	 进程就可以视为程序的一个实例。大部分程序可以同时运行多个实例进程（例如记事本、画图、浏览器 等），也有的程序只能启动一个实例进程（例如网易云音乐、360 安全卫士等）

### 线程 

​	一个进程之内可以分为一到多个线程。

​	 一个线程就是一个指令流，将指令流中的一条条指令以一定的顺序交给 CPU 执行

​	 Java 中，线程作为最小调度单位，进程作为资源分配的最小单位。 在 windows 中进程是不活动的，只是作 为线程的容器

### 二者对比

进程基本上相互独立的，而线程存在于进程内，是进程的一个子集 

进程拥有共享的资源，如内存空间等，供其内部的线程共享 

进程间通信较为复杂 

​	同一台计算机的进程通信称为 IPC（Inter-process communication） 

​	不同计算机之间的进程通信，需要通过网络，并遵守共同的协议，例如 HTTP

线程通信相对简单，因为它们共享进程内的内存，一个例子是多个线程可以访问同一个共享变量 

线程更轻量，线程上下文切换成本一般上要比进程上下文切换低

## 2 并行与并发

单核 cpu 下，线程实际还是 串行执行 的。操作系统中有一个组件叫做任务调度器，将 cpu 的时间片（windows 下时间片最小约为 15 毫秒）分给不同的程序使用，只是由于 cpu 在线程间（时间片很短）的切换非常快，人类感 觉是 同时运行的 。总结为一句话就是： 微观串行，宏观并行 ， 一般会将这种 线程轮流使用 CPU 的做法称为并发， concurrent

![image-20211030095600691](\images\image-20211030095600691.png)

多核 cpu下，每个 核（core） 都可以调度运行线程，这时候线程可以是并行的。

## 3 应用

​	应用之异步调用（案例1） 以调用方角度来讲，如果 需要等待结果返回，才能继续运行就是同步 不需要等待结果返回，就能继续运行就是异步

​	1) 设计

​	 多线程可以让方法执行变为异步的（即不要巴巴干等着）比如说读取磁盘文件时，假设读取操作花费了 5 秒钟，如 果没有线程调度机制，这 5 秒 cpu 什么都做不了，其它代码都得暂停...

​	2) 结论 

​	比如在项目中，视频文件需要转换格式等操作比较费时，这时开一个新线程处理视频转换，避免阻塞主线程 tomcat 的异步 servlet 也是类似的目的，让用户线程处理耗时较长的操作，避免阻塞 tomcat 的工作线程 ui 程序中，开线程进行其他操作，避免阻塞 ui 线程

# 二、Java线程

开始之前pom文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>JUC</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>1.8</maven.compiler.source>
        <maven.compiler.target>1.8</maven.compiler.target>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>1.18.10</version>
        </dependency>
        <dependency>
            <groupId>ch.qos.logback</groupId>
            <artifactId>logback-classic</artifactId>
            <version>1.2.3</version>
        </dependency>
    </dependencies>

</project>
```

logback.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration
        xmlns="http://ch.qos.logback/xml/ns/logback"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://ch.qos.logback/xml/ns/logback logback.xsd">
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%date{HH:mm:ss} [%t] %logger - %m%n</pattern>
        </encoder>
    </appender>
    <logger name="c" level="debug" additivity="false">
        <appender-ref ref="STDOUT"/>
    </logger>
    <root level="ERROR">
        <appender-ref ref="STDOUT"/>
    </root>
</configuration>
```

## 1 创建和运行线程

### 方式一，直接使用Thread

```java
@Slf4j(topic = "c.Sync")
public class TestThread {
    @Test
    public void test1(){
        Thread thread = new Thread("t1"){
            public void run(){
                log.debug("hello");
            }
        };
        thread.start();
    }
}
```

### 方法二，使用 Runnable 配合 Thread

把【线程】和【任务】（要执行的代码）

 分开 Thread 代表线程

 Runnable 可运行的任务（线程要执行的代码）

```java
@Test
public void test2(){
    // 创建任务对象
    Runnable task2 = new Runnable() {
        @Override
        public void run() {
            log.debug("hello");
        }
    };
    // 参数1 是任务对象; 参数2 是线程名字，推荐
    Thread t2 = new Thread(task2, "t2");
    t2.start();
}
```

### 方法三，FutureTask 配合 Thread

FutureTask 能够接收 Callable 类型的参数，用来处理有返回结果的情况

```java
@Test
public void test3() throws ExecutionException, InterruptedException {
    // 创建任务对象
    FutureTask<Integer> task3 = new FutureTask<>(() -> {
        log.debug("hello");
        return 100;
    });
    // 参数1 是任务对象; 参数2 是线程名字，推荐
    new Thread(task3, "t3").start();
    // 主线程阻塞，同步等待 task 执行完毕的结果
    Integer result = task3.get();
    log.debug("结果是:{}", result);
}
```

## 2 查看进程线程的方法

Windows 

​	任务管理器可以查看进程和线程数，也可以用来杀死进程 tasklist 查看进程 taskkill 杀死进程

linux 
	ps -fe 查看所有进程 

​	ps -fT -p  查看某个进程（PID）的所有线程 

​	kill 杀死进程 

​	top 按大写 H 切换是否显示线程 top -H -p  查看某个进程（PID）的所有线程

Java
        jps 命令查看所有 Java 进程
        jstack <PID> 查看某个 Java 进程（PID）的所有线程状态
        jconsole 来查看某个 Java 进程中线程的运行情况（图形界面）

jconsole 

​	远程监控配置 需要以如下方式运行你的 java 类

```
java -Djava.rmi.server.hostname=`ip地址` -Dcom.sun.management.jmxremote
-Dcom.sun.management.jmxremote.port=`连接端口` -Dcom.sun.management.jmxremote.ssl=是否安全连接 -Dcom.sun.management.jmxremote.authenticate=是否认证 java类
```

​	修改 /etc/hosts 文件将 127.0.0.1 映射至主机名

如果要认证访问，还需要做如下步骤 复制 jmxremote.password 文件 修改 jmxremote.password 和 jmxremote.access 文件的权限为 600 即文件所有者可读写 连接时填入 controlRole（用户名），R&D（密码）

### 线程上下文切换（Thread Context Switch）

因为以下一些原因导致 cpu 不再执行当前的线程，转而执行另一个线程的代码 

​	线程的 cpu 时间片用完 

​	垃圾回收 

​	有更高优先级的线程需要运行 

​	线程自己调用了 sleep、yield、wait、join、park、synchronized、lock 等方法

当 Context Switch 发生时，需要由操作系统保存当前线程的状态，并恢复另一个线程的状态，Java 中对应的概念 就是程序计数器（Program Counter Register），它的作用是记住下一条 jvm 指令的执行地址，是线程私有的

​	状态包括程序计数器、虚拟机栈中每个栈帧的信息，如局部变量、操作数栈、返回地址等

​	 Context Switch 频繁发生会影响性能

##  3 start 与 run

### 调用 run

```java
@Test
public void test4(){
    Thread t1 = new Thread("t1") {
        @Override
        public void run() {
            log.debug(Thread.currentThread().getName());
            FileReader.read(Constants.MP4_FULL_PATH);
        }
    };
    t1.run();
    log.debug("do other things ...");

}
```

程序仍在 main 线程运行， FileReader.read() 方法调用还是同步的

### 调用 start

将上述代码的 t1.run() 改为

```
19:41:30 [main] c.TestStart - do other things ...
19:41:30 [t1] c.TestStart - t1
19:41:30 [t1] c.FileReader - read [1.mp4] start ...
19:41:35 [t1] c.FileReader - read [1.mp4] end ... cost: 4542 ms
```

直接调用 run 是在主线程中执行了 run，没有启动新的线程 

使用 start 是启动新的线程，通过新的线程间接执行 run 中的代码

## 4 sleep与yield

### sleep

1. 调用 sleep 会让当前线程从 Running 进入 Timed Waiting 状态（阻塞）
2. 其它线程可以使用 interrupt 方法打断正在睡眠的线程，这时 sleep 方法会抛出 InterruptedException 
3. 睡眠结束后的线程未必会立刻得到执行 
4. 建议用 TimeUnit 的 sleep 代替 Thread 的 sleep 来获得更好的可读性

### yield

​	1. 调用 yield 会让当前线程从 Running 进入 Runnable 就绪状态，然后调度执行其它线程 

2. 具体的实现依赖于操作系统的任务调度器

### 线程优先级

线程优先级会提示（hint）调度器优先调度该线程，但它仅仅是一个提示，调度器可以忽略它 

如果 cpu 比较忙，那么优先级高的线程会获得更多的时间片，但 cpu 闲时，优先级几乎没作用

```java
// taks1的会被执行次数多 count也就越高
@Test
public void test5(){
    Runnable task1 = ()->{
        int count = 0;
        for (;;){
            System.out.println("---->1 " + count++);
        }
    };
    Runnable task2 = ()->{
        int count = 0;
        for (;;){
            Thread.yield();
            System.out.println("---->2 " + count++);
        }
    };
    Thread t1 = new Thread(task1, "t1");
    Thread t2 = new Thread(task2, "t2");
    t1.start();
    t2.start();


}
```

## 5、join方法详解

### 为什么需要 join 

下面的代码执行，打印 r 是什么？

```java
static int r = 0;
@Test
public void test6(){
    log.debug("开始");
    Thread t1 = new Thread(() -> {
        log.debug("Start");
        try {
            Thread.sleep(1);
            log.debug("结束");
            r = 10;
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    });
    t1.start();
    log.debug("结果为：{}", r);
    log.debug("结束");
}
```

分析
        因为主线程和线程 t1 是并行执行的，t1 线程需要 1 秒之后才能算出 r=10
        而主线程一开始就要打印 r 的结果，所以只能打印出 r=0

解决方法

​	 用join，加在 t1.start() 之后即可

```java
@Test
public void test6() throws InterruptedException {
    log.debug("开始");
    Thread t1 = new Thread(() -> {
        log.debug("Start");
        try {
            Thread.sleep(1);
            log.debug("结束");
            r = 10;
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    });
    t1.start();
    t1.join();
    log.debug("结果为：{}", r);
    log.debug("结束");
}
```

以调用方角度来讲，如果需要等待结果返回，才能继续运行就是同步，不需要等待结果返回，就能继续运行就是异步

![image-20211101192941339](\images\image-20211101192941339.png)

### 等待多个结果

下面代码 cost 大约多少秒？

```java
@Test
public void test7() throws InterruptedException{
    Thread t1 = new Thread(() -> {
        try {
            sleep(1);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        r1 = 10;
    });
    Thread t2 = new Thread(() -> {
        try {
            sleep(2);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        r2 = 20;
    });
    long start = System.currentTimeMillis();
    t1.start();
    t2.start();
    t1.join();
    t2.join();
    long end = System.currentTimeMillis();
    log.debug("r1: {} r2: {} cost: {}", r1, r2, end - start);
}
```

分析如下 

​	第一个 join：等待 t1 时, t2 并没有停止, 而在运行 

​	第二个 join：1s 后, 执行到此, t2 也运行了 1s, 因此也只需再等待 1s

```
19:33:13 [main] c.thread - r1: 10 r2: 20 cost: 2
```

![image-20211101193504347](\images\image-20211101193504347.png)

### 有时效的 join

等够时间

```JAVA
@Test
public void test8() throws InterruptedException{
    Thread t1 = new Thread(() -> {
        try {
            sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        r1 = 10;
    });
    long start = System.currentTimeMillis();
    t1.start();
    // 线程执行结束会导致 join 结束
    t1.join(1500);
    long end = System.currentTimeMillis();
    log.debug("r1: {} r2: {} cost: {}", r1, r2, end - start);
}
```

输出

19:39:18 [main] c.thread - r1: 10 r2: 0 cost: 1013

没等够时间

```java
public void test8() throws InterruptedException{
    Thread t1 = new Thread(() -> {
        try {
            sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        r1 = 10;
    });
    long start = System.currentTimeMillis();
    t1.start();
    // 线程执行结束会导致 join 结束
    t1.join(1500);
    long end = System.currentTimeMillis();
    log.debug("r1: {} r2: {} cost: {}", r1, r2, end - start);
}
```

输出

19:40:13 [main] c.thread - r1: 0 r2: 0 cost: 1510

## 6、interrupt方法

### 打断 sleep，wait，join 的线程

这几个方法都会让线程进入阻塞状态 打断 sleep 的线程, 会清空打断状态，以 sleep 为例

```java
@Test
public void test9() throws InterruptedException {
    Thread t1 = new Thread(()->{
        try {
            sleep(1);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }, "t1");
    t1.start();
    sleep((long) 0.5);
    t1.interrupt();
    log.debug(" 打断状态: {}", t1.isInterrupted());

}
```

输出

```
java.lang.InterruptedException: sleep interrupted
	at java.lang.Thread.sleep(Native Method)
	at com.harry.thread.TestThread.lambda$test9$7(TestThread.java:154)
	at java.lang.Thread.run(Thread.java:748)
19:42:21 [main] c.thread -  打断状态: true
```

### 打断正常运行的线程

打断正常运行的线程, 不会清空打断状态

```java
@Test
public void test10() throws InterruptedException {
    Thread t2 = new Thread(()->{
        while(true) {
            Thread current = Thread.currentThread();
            boolean interrupted = current.isInterrupted();
            if(interrupted) {
                log.debug(" 打断状态: {}", interrupted);
                break;
            }
        }
    }, "t2");
    t2.start();
    sleep((long) 0.5);
    t2.interrupt();
}
```

### 打断 park 线程

打断 park 线程, 不会清空打断状态

```java
@Test
public void test11() throws InterruptedException {
    Thread t1 = new Thread(() -> {
        log.debug("park...");
        LockSupport.park();
        log.debug("unpark...");
        log.debug("打断状态：{}", Thread.currentThread().isInterrupted());
    }, "t1");
    t1.start();
    Thread.sleep(1000);
    t1.interrupt();
}
```

输出：

```
19:46:53 [t1] c.thread - park...
19:46:54 [t1] c.thread - unpark...
19:46:54 [t1] c.thread - 打断状态：true
```

### 不推荐的方法

还有一些不推荐使用的方法，这些方法已过时，容易破坏同步代码块，造成线程死锁

stop（）   		停止线程运行

suspend（）	挂起(暂停)线程运行

resume()		   恢复线程运行



## 7、主线程和守护线程

默认情况下，Java 进程需要等待所有线程都运行结束，才会结束。有一种特殊的线程叫做守护线程，只要其它非守 护线程运行结束了，即使守护线程的代码没有执行完，也会强制结束。

```java
@Test
public void test12() throws InterruptedException {
    log.debug("开始运行...");
    Thread t1 = new Thread(() -> {
        log.debug("开始运行...");
        try {
            Thread.sleep(2);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        log.debug("运行结束...");
    }, "daemon");
    // 设置该线程为守护线程
    t1.setDaemon(true);
    t1.start();
    Thread.sleep(1000);
    log.debug("运行结束...");
}
```

输出：

```
20:09:57 [main] c.thread - 开始运行...
20:09:57 [daemon] c.thread - 开始运行...
20:09:57 [daemon] c.thread - 运行结束...
20:09:58 [main] c.thread - 运行结束...
```

注意 

​	垃圾回收器线程就是一种守护线程 

​	Tomcat 中的 Acceptor 和 Poller 线程都是守护线程，所以 Tomcat 接收到 shutdown 命令后，不会等 待它们处理完当前请求

## 8、五种状态

这是从 操作系统 层面来描述的

![image-20211101201121768](\images\image-20211101201121768.png)

【初始状态】仅是在语言层面创建了线程对象，还未与操作系统线程关联 

【可运行状态】（就绪状态）指该线程已经被创建（与操作系统线程关联），可以由 CPU 调度执行 

【运行状态】指获取了 CPU 时间片运行中的状态

​		当 CPU 时间片用完，会从【运行状态】转换至【可运行状态】，会导致线程的上下文切换	

【阻塞状态】

​		如果调用了阻塞 API，如 BIO 读写文件，这时该线程实际不会用到 CPU，会导致线程上下文切换，进入 【阻塞状态】

​	等 BIO 操作完毕，会由操作系统唤醒阻塞的线程，转换至【可运行状态】

​	与【可运行状态】的区别是，对【阻塞状态】的线程来说只要它们一直不唤醒，调度器就一直不会考虑 调度它们

【终止状态】表示线程已经执行完毕，生命周期已经结束，不会再转换为其它状态

## 9、六种状态

这是从 Java API 层面来描述的

![image-20211101201443631](\images\image-20211101201443631.png)

NEW 线程刚被创建，但是还没有调用 start() 方法 

RUNNABLE 当调用了 start() 方法之后，注意，Java API 层面的 RUNNABLE 状态涵盖了 操作系统 层面的 【可运行状态】、【运行状态】和【阻塞状态】（由于 BIO 导致的线程阻塞，在 Java 里无法区分，仍然认为 是可运行）

BLOCKED ， WAITING ， TIMED_WAITING 都是 Java API 层面对【阻塞状态】的细分，后面会在状态转换一节 详述

TERMINATED 当线程代码运行结束

# 三、共享模型之管程

## 1、Java 的体现

两个线程对初始值为 0 的静态变量一个做自增，一个做自减，各做 5000 次，结果是 0 吗？

```java
static int counter = 0;

@Test
public void test1() throws InterruptedException {
    Thread t1 = new Thread(() -> {
        for (int i = 0; i < 5000; i++) {
            counter++;
        }
    }, "t1");
    Thread t2 = new Thread(() -> {
        for (int i = 0; i < 5000; i++) {
            counter--;
        }
    }, "t2");
    t1.start();
    t2.start();
    t1.join();
    t2.join();
    log.debug("{}",counter);
}
```

### 问题分析

以上的结果可能是正数、负数、零。为什么呢？因为 Java 中对静态变量的自增，自减并不是原子操作，要彻底理 解，必须从字节码来进行分析

例如对于 i++ 而言（i 为静态变量），实际会产生如下的 JVM 字节码指令：

```
getstatic i // 获取静态变量i的值 
iconst_1 // 准备常量1 
iadd // 自增 
putstatic i // 将修改后的值存入静态变量i
```

而对应 i-- 也是类似：

```
getstatic i // 获取静态变量i的值 
iconst_1 // 准备常量1 
isub // 自减 
putstatici // 将修改后的值存入静态变量i
```

而 Java 的内存模型如下，完成静态变量的自增，自减需要在主存和工作内存中进行数据交换：

![image-20211106094300976](\images\image-20211106094300976.png)

如果是单线程以上 8 行代码是顺序执行（不会交错）没有问题

![image-20211106094335055](\images\image-20211106094335055.png)

但多线程下这 8 行代码可能交错运行：

出现负数的情况：

![image-20211106094411877](\images\image-20211106094411877.png)

出现正数的情况：

![image-20211106094447861](\images\image-20211106094447861.png)

临界区 Critical Section

一个程序运行多个线程本身是没有问题的,问题出在多个线程访问共享资源 多个线程读共享资源其实也没有问题 在多个线程对共享资源读写操作时发生指令交错，就会出现问题 一段代码块内如果存在对共享资源的多线程读写操作，称这段代码块为临界区

例如，下面代码中的临界区

```JAVA
static int counter = 0;
static void increment()
// 临界区
{
	counter++;
}
static void decrement()
// 临界区
{
	counter--;
}
```

## 2、synchronized 解决方案

### 应用之互斥 

为了避免临界区的竞态条件发生，有多种手段可以达到目的。 

​	阻塞式的解决方案：synchronized，Lock 

​	非阻塞式的解决方案：原子变量

synchronized即俗称的【对象锁】，它采用互斥的方式让同一 时刻至多只有一个线程能持有【对象锁】，其它线程再想获取这个【对象锁】时就会阻塞住。这样就能保证拥有锁 的线程可以安全的执行临界区内的代码，不用担心线程上下文切换

注意 虽然 java 中互斥和同步都可以采用 synchronized 关键字来完成，但它们还是有区别的：

​	 互斥是保证临界区的竞态条件发生，同一时刻只能有一个线程执行临界区代码

​	 同步是由于线程执行的先后、顺序不同、需要一个线程等待其它线程运行到某个点

### synchronize

```java
synchronized(对象) // 线程1， 线程2(blocked)
{
    临界区
}
```

解决

```java
final Object room = new Object();
@Test
public void test2() throws InterruptedException {

    Thread t1 = new Thread(() -> {
        for (int i = 0; i < 5000; i++) {
            synchronized (room){
                counter++;
            }

        }
    }, "t1");
    Thread t2 = new Thread(() -> {
        for (int i = 0; i < 5000; i++) {
            synchronized (room){
                counter--;
            }

        }
    }, "t2");
    t1.start();
    t2.start();
    t1.join();
    t2.join();
    log.debug("{}",counter);
    System.out.println(counter);
}
```

![image-20211106095301490](\images\image-20211106095301490.png)

synchronized(对象) 中的对象，可以想象为一个房间（room），有唯一入口（门）房间只能一次进入一人 进行计算，线程 t1，t2 想象成两个人

当线程 t1 执行到 synchronized(room) 时就好比 t1 进入了这个房间，并锁住了门拿走了钥匙，在门内执行 count++ 代码

这时候如果 t2 也运行到了 synchronized(room) 时，它发现门被锁住了，只能在门外等待，发生了上下文切 换，阻塞住了

这中间即使 t1 的 cpu 时间片不幸用完，被踢出了门外（不要错误理解为锁住了对象就能一直执行下去哦）， 这时门还是锁住的，t1 仍拿着钥匙，t2 线程还在阻塞状态进不来，只有下次轮到 t1 自己再次获得时间片时才 能开门进入

当 t1 执行完 synchronized{} 块内的代码，这时候才会从 obj 房间出来并解开门上的锁，唤醒 t2 线程把钥 匙给他。t2 线程这时才可以进入 obj 房间，锁住了门拿上钥匙，执行它的 count-- 代码

![image-20211106095430561](\images\image-20211106095430561.png)

### 面向对象改进

把需要保护的共享变量放入一个类

```java
class Room{
    int value = 0;
    public void increment() {
        synchronized (this) {
            value++;
        }
    }
    public void decrement() {
        synchronized (this) {
            value--;
        }
    }
    public int get() {
        synchronized (this) {
            return value;
        }
    }
}
```

```java
@Test
public void test2() throws InterruptedException {
    Room room = new Room();
    Thread t1 = new Thread(() -> {
        for (int i = 0; i < 5000; i++) {
            room.increment();
        }
    }, "t1");
    Thread t2 = new Thread(() -> {
        for (int i = 0; i < 5000; i++) {
          room.decrement();
        }
    }, "t2");
    t1.start();
    t2.start();
    t1.join();
    t2.join();
    log.debug("{}",counter);
    System.out.println(counter);
}
```

## 3、方法上的 synchronized

```java
class Test{
    public synchronized void test() {

    }
}
等价于
class Test{
    public void test() {
        synchronized(this) {

        }
    }
}
```

```java
class Test{
    public synchronized static void test() {
    }
}
等价于
class Test{
    public static void test() {
        synchronized(Test.class) {

        }
    }
```

不加 synchronzied 的方法就好比不遵守规则的人，不去老实排队（好比翻窗户进去的）

### 所谓的“线程八锁

其实就是考察 synchronized 锁住的是哪个对象

情况1：12 或 21

```java
@Slf4j(topic = "c.Number")
class Number{
    public synchronized void a() {
        log.debug("1");
    }
    public synchronized void b() {
        log.debug("2");
    }
}
public static void main(String[] args) {
    Number n1 = new Number();
    new Thread(()->{ n1.a(); }).start();
    new Thread(()->{ n1.b(); }).start();
}
```

情况2：1s后12，或 2 1s后 1

```java
@Slf4j(topic = "c.Number")
class Number{
    public synchronized void a() {
        sleep(1);
        log.debug("1");
    }
    public synchronized void b() {
        log.debug("2");
    }
}
public static void main(String[] args) {
    Number n1 = new Number();
    new Thread(()->{ n1.a(); }).start();
    new Thread(()->{ n1.b(); }).start();
}

```

情况3：3 1s 12 或 23 1s 1 或 32 1s 1

```java
class Number{
    public synchronized void a() {
        sleep(1);
        log.debug("1");
    }
    public synchronized void b() {
        log.debug("2");
    }
    public void c() {
        log.debug("3");
    }
}
public static void main(String[] args) {
	Number n1 = new Number();
	new Thread(()->{ n1.a(); }).start();
	new Thread(()->{ n1.b(); }).start();
	new Thread(()->{ n1.c(); }).start();
}
```

情况4：2 1s 后 1

```java
@Slf4j(topic = "c.Number")
class Number{
    public synchronized void a() {
        sleep(1);
        log.debug("1");
    }
    public synchronized void b() {
        log.debug("2");
    }
}
public static void main(String[] args) {
	Number n1 = new Number();
	Number n2 = new Number();
	new Thread(()->{ n1.a(); }).start();
	new Thread(()->{ n2.b(); }).start();
}
```

情况5：2 1s 后 1

```java
@Slf4j(topic = "c.Number")
class Number{
    public static synchronized void a() {
        sleep(1);
        log.debug("1");
    }
    public synchronized void b() {
        log.debug("2");
    }
}
public static void main(String[] args) {
    Number n1 = new Number();
    new Thread(()->{ n1.a(); }).start();
    new Thread(()->{ n1.b(); }).start();
}
```

情况6：1s 后12， 或 2 1s后 1

```java
@Slf4j(topic = "c.Number")
class Number{
    public static synchronized void a() {
        sleep(1);
        log.debug("1");
    }
    public static synchronized void b() {
        log.debug("2");
    }
}
public static void main(String[] args) {
	Number n1 = new Number();
	new Thread(()->{ n1.a(); }).start();
	new Thread(()->{ n1.b(); }).start();
}
```

情况7：2 1s 后 1

```java
@Slf4j(topic = "c.Number")
class Number{
    public static synchronized void a() {
        sleep(1);
        log.debug("1");
    }
    public synchronized void b() {
        log.debug("2");
    }
}
    public static void main(String[] args) {
        Number n1 = new Number();
        Number n2 = new Number();
        new Thread(()->{ n1.a(); }).start();
        new Thread(()->{ n2.b(); }).start();
}
```

情况8：1s 后12， 或 2 1s后 

```java
class Number{
    public static synchronized void a() {
        sleep(1);
        log.debug("1");
    }
    public static synchronized void b() {
        log.debug("2");
    }
}
public static void main(String[] args) {
	Number n1 = new Number();
	Number n2 = new Number();
	new Thread(()->{ n1.a(); }).start();
	new Thread(()->{ n2.b(); }).start();
}
```

## 4、变量的线程安全分析

成员变量和静态变量是否线程安全？

​	如果它们没有共享，则线程安全

​	如果它们被共享了，根据它们的状态是否能够改变，又分两种情况 如果只有读操作，则线程安全 如果有读写操作，则这段代码是临界区，需要考虑线程安全

局部变量是否线程安全？

​	局部变量是线程安全的

​	但局部变量引用的对象则未必 如果该对象没有逃离方法的作用访问，它是线程安全的 如果该对象逃离方法的作用范围，需要考虑线程安全

### 局部变量线程安全分析

```java
public static void test1() {
    int i = 10;
    i++;
}
```

每个线程调用 test1() 方法时局部变量 i，会在每个线程的栈帧内存中被创建多份，因此不存在共享

如图

![image-20211106101819714](\images\image-20211106101819714.png)

局部变量的引用稍有不同

先看一个成员变量的例子

其中一种情况是，如果线程2 还未 add，线程1 remove 就会报错：

```java
public class ThreadUnsafe {
    ArrayList<String> list = new ArrayList<>();
    public void  method1(int loopNumber){
        for (int i = 0; i < loopNumber; i++) {
            // 临界区， 会产生竞态条件
            method2();
            method3();
        }
    }
    private void method2() {
        list.add("1");
    }
    private void method3() {
        list.remove(0);
    }
    static final int THREAD_NUMBER = 2;
    static final int LOOP_NUMBER = 200;
    public static void main(String[] args) {
        ThreadUnsafe test = new ThreadUnsafe();
        for (int i = 0; i < THREAD_NUMBER; i++) {
            new Thread(() -> {
                test.method1(LOOP_NUMBER);
            }, "Thread" + i).start();
        }
    }
}
```

```
Exception in thread "Thread0" java.lang.IndexOutOfBoundsException: Index: 0, Size: 0
	at java.util.ArrayList.rangeCheck(ArrayList.java:657)
	at java.util.ArrayList.remove(ArrayList.java:496)
	at com.harry.thread.ThreadUnsafe.method3(ThreadUnsafe.java:18)
	at com.harry.thread.ThreadUnsafe.method1(ThreadUnsafe.java:11)
	at com.harry.thread.ThreadUnsafe.lambda$main$0(ThreadUnsafe.java:26)
	at java.lang.Thread.run(Thread.java:748)
```

分析： 无论哪个线程中的 method2 引用的都是同一个对象中的 list 成员变量 method3 与 method2 分析相同

![image-20211106102426964](\images\image-20211106102426964.png)

将 list 修改为局部变量

```java
public class ThreadUnsafe {

    public void  method1(int loopNumber){
        ArrayList<String> list = new ArrayList<>();
        for (int i = 0; i < loopNumber; i++) {
            // 临界区， 会产生竞态条件
            method2(list);
            method3(list);
        }
    }
    private void method2( ArrayList<String> list) {
        list.add("1");
    }
    private void method3( ArrayList<String> list) {
        list.remove(0);
    }
    static final int THREAD_NUMBER = 2;
    static final int LOOP_NUMBER = 200;
    public static void main(String[] args) {
        ThreadUnsafe test = new ThreadUnsafe();
        for (int i = 0; i < THREAD_NUMBER; i++) {
            new Thread(() -> {
                test.method1(LOOP_NUMBER);
            }, "Thread" + i).start();
        }
    }
}
```

分析：

list 是局部变量，每个线程调用时会创建其不同实例，没有共享 

而 method2 的参数是从 method1 中传递过来的，与 method1 中引用同一个对象

method3 的参数分析与 method2 相同

![image-20211106102615192](\images\image-20211106102615192.png)

方法访问修饰符带来的思考，如果把 method2 和 method3 的方法修改为 public 会不会代理线程安全问题？

情况1：有其它线程调用 method2 和 method3 

情况2：在 情况1 的基础上，为 ThreadSafe 类添加子类，子类覆盖 method2 或 method3 方法，即

```java
public class ThreadSafe {
    public final void method1(int loopNumber) {
        ArrayList<String> list = new ArrayList<>();
        for (int i = 0; i < loopNumber; i++) {
            method2(list);
            method3(list);
        }
    }
    private void method2( ArrayList<String> list) {
        list.add("1");
    }
    private void method3( ArrayList<String> list) {
        list.remove(0);
    }
}
class ThreadSafeSubClass extends ThreadSafe{

    public void method3(ArrayList<String> list) {
        new Thread(() -> {
            list.remove(0);
        }).start();
    }
}
```

从这个例子可以看出 private 或 final 提供【安全】的意义所在，请体会开闭原则中的【闭】

### 常见线程安全类

String 

Integer 

StringBuffer 

Random 

Vector

 Hashtable

 java.util.concurrent 包下的类

这里说它们是线程安全的是指，多个线程调用它们同一个实例的某个方法时，是线程安全的。也可以理解为

```java
Hashtable table = new Hashtable();
new Thread(()->{
	table.put("key", "value1");
}).start();
new Thread(()->{
	table.put("key", "value2");
}).start();
```

它们的每个方法是原子的，但注意它们多个方法的组合不是原子的

### 线程安全类方法的组合

分析下面代码是否线程安全？

```java
Hashtable table = new Hashtable();
// 线程1，线程2
if( table.get("key") == null) {
    table.put("key", value);
}
```

![image-20211106103937744](\images\image-20211106103937744.png)

### 不可变类线程安全性

String、Integer 等都是不可变类，因为其内部的状态不可以改变，因此它们的方法都是线程安全的

## 5、习题

### 卖票练习

```java
package com.harry.thread;

import com.sun.org.apache.bcel.internal.generic.NEW;
import lombok.extern.slf4j.Slf4j;

import java.util.ArrayList;
import java.util.Random;
import java.util.Vector;
@Slf4j(topic = "c.ExerciseSell")
public class ExerciseSell {
    public static void main(String[] args) {
        TicketWindow ticketWindow = new TicketWindow(2000);
        ArrayList<Thread> list = new ArrayList<>();
        // 用来存储卖出去多少票
        Vector<Integer> sellCount = new Vector<>();
        for (int i = 0; i < 2000; i++){
            Thread t = new Thread(() -> {
                // 分析这里的竞态条件
                int count = ticketWindow.sell(randomAmount());
                sellCount.add(count);
            });
            list.add(t);
            t.start();
        }
        list.forEach((t)->{
            try {
                t.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });
        // 买出去的票求和
        log.debug("selled count:{}",sellCount.stream().mapToInt(c -> c).sum());
        // 剩余票数
        log.debug("remainder count:{}", ticketWindow.getCount());
    }
    // Random 为线程安全
    static Random random = new Random();
    // 随机 1~5
    public static int randomAmount() {
        return random.nextInt(5) + 1;
    }
}
class TicketWindow{
    private int count;

    public TicketWindow(int count){
        this.count = count;
    }

    public int getCount(){
        return count;
    }

    public synchronized int sell(int amount){
        if (this.count >= amount){
            this.count -= amount;
            return amount;
        }else {
            return 0;
        }
    }
}
```

另外，用下面的代码行不行，为什么？ 因为ArrayList不是线程安全的所以不能使用

```
List sellCount = new ArrayList<>();
```

### 转账练习

```java
package com.harry.thread;

import lombok.extern.slf4j.Slf4j;

import java.util.Random;

import static com.harry.thread.ExerciseSell.random;
import static com.harry.thread.ExerciseSell.randomAmount;
@Slf4j(topic = "c.ExerciseTransfer")
public class ExerciseTransfer {
    public static void main(String[] args)  throws InterruptedException{
        Account a = new Account(1000);
        Account b = new Account(1000);
        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                a.transfer(b, randomAmount());
            }
        }, "t1");
        Thread t2 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                b.transfer(a, randomAmount());
            }
        }, "t2");
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        // 查看转账2000次后的总金额
        log.debug("total:{}",(a.getMoney() + b.getMoney()));

    }
    // Random 为线程安全
    static Random random = new Random();
    // 随机 1~100
    public static int randomAmount() {
        return random.nextInt(100) +1;
    }
}
class Account {
    private int money;
    public Account(int money) {
        this.money = money;
    }
    public int getMoney() {
        return money;
    }
    public void setMoney(int money) {
        this.money = money;
    }
    public  void transfer(Account target, int amount) {
       if (this.money > amount) {
           synchronized (Account.class){
               this.setMoney(this.getMoney() - amount);
               target.setMoney(target.getMoney() + amount);
           }

        }
    }
}
```

## 6、Monitor概念

### Java 对象头

 以 32 位虚拟机为例

普通对象

![image-20211108200310169](\images\image-20211108200310169.png)

数组对象

![image-20211108200341496](\images\image-20211108200341496.png)

其中 Mark Word 结构为

![image-20211108200405328](\images\image-20211108200405328.png)

64 位虚拟机 Mark Wor

![image-20211108200430199](\images\image-20211108200430199.png)

### Monitor 原理

Monitor 被翻译为监视器或管程

每个 Java 对象都可以关联一个 Monitor 对象，如果使用 synchronized 给对象上锁（重量级）之后，该对象头的 Mark Word 中就被设置指向 Monitor 对象的指针

Monitor 结构如下

![image-20211114095540122](\images\image-20211114095540122.png)

刚开始 Monitor 中 Owner 为 null 

当 Thread-2 执行 synchronized(obj) 就会将 Monitor 的所有者 Owner 置为 Thread-2，Monitor中只能有一 个 Owner

 在 Thread-2 上锁的过程中，如果 Thread-3，Thread-4，Thread-5 也来执行 synchronized(obj)，就会进入 EntryList BLOCKED 

Thread-2 执行完同步代码块的内容，然后唤醒 EntryList 中等待的线程来竞争锁，竞争的时是非公平的 

图中 WaitSet 中的 Thread-0，Thread-1 是之前获得过锁，但条件不满足进入 WAITING 状态的线程

注意：synchronized 必须是进入同一个对象的 monitor 才有上述的效果 不加 synchronized 的对象不会关联监视器，不遵从以上规则



## 7、原理之 wait / notif

![image-20211114100129587](\images\image-20211114100129587.png)



API 介绍 

​	obj.wait() 让进入 object 监视器的线程到 waitSet 等待 

​	obj.notify() 在 object 上正在 waitSet 等待的线程中挑一个唤醒 

​	obj.notifyAll() 让 object 上正在 waitSet 等待的线程全部唤醒

它们都是线程之间进行协作的手段，都属于 Object 对象的方法。必须获得此对象的锁，才能调用这几个方法

```java
package com.harry.thread;

import lombok.extern.slf4j.Slf4j;

import static java.lang.Thread.sleep;
@Slf4j(topic = "c.TestWaitNotify")
public class TestWaitNotify {
    final static Object obj = new Object();

    public static void main(String[] args) throws InterruptedException {
        new Thread(() -> {
            synchronized (obj) {
                log.debug("执行....");
                try {
                    obj.wait(); // 让线程在obj上一直等待下去
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                log.debug("其它代码....");
            }
        }).start();
        new Thread(() -> {
            synchronized (obj) {
                log.debug("执行....");
                try {
                    obj.wait(); // 让线程在obj上一直等待下去
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                log.debug("其它代码....");
            }
        }).start();
        // 主线程两秒后执行
        sleep(2);
        log.debug("唤醒 obj 上其它线程");
        synchronized (obj) {
            obj.notify(); // 唤醒obj上一个线程
            // obj.notifyAll(); // 唤醒obj上所有等待线程
        }
    }
}
```

```
20:09:37 [Thread-0] c.TestWaitNotify - 执行....
20:09:37 [main] c.TestWaitNotify - 唤醒 obj 上其它线程
20:09:37 [Thread-1] c.TestWaitNotify - 执行....
20:09:37 [Thread-0] c.TestWaitNotify - 其它代码....
```

wait() 方法会释放对象的锁，进入 WaitSet 等待区，从而让其他线程就机会获取对象的锁。无限制等待，直到 notify 为止

wait(long n) 有时限的等待, 到 n 毫秒后结束等待，或是被 notify

### wait notify 的正确使用

sleep(long n) 和 wait(long n) 的区别

​	1) sleep 是 Thread 方法，而 wait 是 Object 的方法 

​	2) sleep 不需要强制和 synchronized 配合使用，但 wait 需要 和 synchronized 一起用 

​	3) sleep 在睡眠的同时，不会释放对象锁的，但 wait 在等待的时候会释放对象锁 

​	4) 它们 状态 TIMED_WAITING

### step 1

```java
@Slf4j(topic = "c.WaitStep1")
public class WaitStep1 {
    static final Object room = new Object();
    static boolean hasCigarette = false;
    static boolean hasTakeout = false;

    public static void main(String[] args) throws InterruptedException {
        new Thread(() -> {
            synchronized (room) {
                log.debug("有烟没？[{}]", hasCigarette);
                if (!hasCigarette) {
                    log.debug("没烟，先歇会！");
                    try {
                        sleep(2);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
                log.debug("有烟没？[{}]", hasCigarette);
                if (hasCigarette) {
                    log.debug("可以开始干活了");
                }
            }
        }, "小南").start();
        
        for (int i = 0; i < 5; i++) {
            new Thread(() -> {
                synchronized (room) {
                    log.debug("可以开始干活了");
                }
            }, "其它人").start();
        }

        sleep(1);
        new Thread(() -> {
            // 这里能不能加 synchronized (room)？
            hasCigarette = true;
            log.debug("烟到了噢！");
        }, "送烟的").start();
    }
}
```

```
20:18:10 [小南] c.WaitStep1 - 有烟没？[false]
20:18:10 [送烟的] c.WaitStep1 - 烟到了噢！
20:18:10 [小南] c.WaitStep1 - 有烟没？[true]
20:18:10 [小南] c.WaitStep1 - 可以开始干活了
20:18:10 [其它人] c.WaitStep1 - 可以开始干活了
20:18:10 [其它人] c.WaitStep1 - 可以开始干活了
20:18:10 [其它人] c.WaitStep1 - 可以开始干活了
20:18:10 [其它人] c.WaitStep1 - 可以开始干活了
20:18:10 [其它人] c.WaitStep1 - 可以开始干活了
```

其它干活的线程，都要一直阻塞，效率太低

小南线程必须睡足 2s 后才能醒来，就算烟提前送到，也无法立刻醒来 

加了 synchronized (room) 后，就好比小南在里面反锁了门睡觉，烟根本没法送进门，main 没加 synchronized 就好像 main 线程是翻窗户进来的

解决方法，使用 wait - notify 机制

### step 2

```java
package com.harry.thread;

import lombok.extern.slf4j.Slf4j;

import static java.lang.Thread.sleep;

@Slf4j(topic = "c.WaitStep1")
public class WaitStep1 {
    static final Object room = new Object();
    static boolean hasCigarette = false;
    static boolean hasTakeout = false;

    public static void main(String[] args) throws InterruptedException {
        new Thread(() -> {
            synchronized (room) {
                log.debug("有烟没？[{}]", hasCigarette);
                if (!hasCigarette) {
                    log.debug("没烟，先歇会！");
                    try {
                        sleep(2);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
                log.debug("有烟没？[{}]", hasCigarette);
                if (hasCigarette) {
                    log.debug("可以开始干活了");
                }
            }
        }, "小南").start();

        for (int i = 0; i < 5; i++) {
            new Thread(() -> {
                synchronized (room) {
                    log.debug("可以开始干活了");
                }
            }, "其它人").start();
        }

        sleep(1);
        new Thread(() -> {
            // 这里能不能加 synchronized (room)？
            hasCigarette = true;
            log.debug("烟到了噢！");
        }, "送烟的").start();
    }
}
@Slf4j(topic = "c.step2")
class step2{
    static final Object room = new Object();
    static boolean hasCigarette = false;
    static boolean hasTakeout = false;

    public static void main(String[] args) throws InterruptedException {
        new Thread(() -> {
            synchronized (room) {
                log.debug("有烟没？[{}]", hasCigarette);
                if (!hasCigarette) {
                    log.debug("没烟，先歇会！");
                    try {
                        room.wait(2000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
                log.debug("有烟没？[{}]", hasCigarette);
                if (hasCigarette) {
                    log.debug("可以开始干活了");
                }
            }
        }, "小南").start();
        for (int i = 0; i < 5; i++) {
            new Thread(() -> {
                synchronized (room) {
                    log.debug("可以开始干活了");
                }
            }, "其它人").start();
        }
        sleep(1);
        new Thread(() -> {
            synchronized (room) {
                hasCigarette = true;
                log.debug("烟到了噢！");
                room.notify();
            }
        }, "送烟的").start();
    }
}
```

```
20:21:16 [小南] c.step2 - 有烟没？[false]
20:21:16 [小南] c.step2 - 没烟，先歇会！
20:21:16 [送烟的] c.step2 - 烟到了噢！
20:21:16 [其它人] c.step2 - 可以开始干活了
20:21:16 [其它人] c.step2 - 可以开始干活了
20:21:16 [其它人] c.step2 - 可以开始干活了
20:21:16 [其它人] c.step2 - 可以开始干活了
20:21:16 [其它人] c.step2 - 可以开始干活了
20:21:16 [小南] c.step2 - 有烟没？[true]
20:21:16 [小南] c.step2 - 可以开始干活了

Process finished with exit code 0
```

### step3

```java
@Slf4j(topic = "c.step3")
class step3{
    static final Object room = new Object();
    static boolean hasCigarette = false;
    static boolean hasTakeout = false;
    public static void main(String[] args) throws InterruptedException {
        new Thread(() -> {
            synchronized (room) {
                log.debug("有烟没？[{}]", hasCigarette);
                if (!hasCigarette) {
                    log.debug("没烟，先歇会！");
                    try {
                        room.wait();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
                log.debug("有烟没？[{}]", hasCigarette);
                if (hasCigarette) {
                    log.debug("可以开始干活了");
                } else {log.debug("没干成活...");
                }
            }
        }, "小南").start();
        new Thread(() -> {
            synchronized (room) {
                Thread thread = Thread.currentThread();
                log.debug("外卖送到没？[{}]", hasTakeout);
                if (!hasTakeout) {
                    log.debug("没外卖，先歇会！");
                    try {
                        room.wait();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
                log.debug("外卖送到没？[{}]", hasTakeout);
                if (hasTakeout) {
                    log.debug("可以开始干活了");
                } else {
                    log.debug("没干成活...");
                }
            }
        }, "小女").start();
        sleep(1);
        new Thread(() -> {
            synchronized (room) {
                hasTakeout = true;
                log.debug("外卖到了噢！");
                room.notify();
            }
        }, "送外卖的").start();
    }
}
```

```
20:24:22 [小南] c.step3 - 有烟没？[false]
20:24:22 [小南] c.step3 - 没烟，先歇会！
20:24:22 [送外卖的] c.step3 - 外卖到了噢！
20:24:22 [小女] c.step3 - 外卖送到没？[true]
20:24:22 [小女] c.step3 - 外卖送到没？[true]
20:24:22 [小女] c.step3 - 可以开始干活了
20:24:22 [小南] c.step3 - 有烟没？[false]
20:24:22 [小南] c.step3 - 没干成活...
```

notify 只能随机唤醒一个 WaitSet 中的线程，这时如果有其它线程也在等待，那么就可能唤醒不了正确的线 程，称之为【虚假唤醒】 

解决方法，改为 notifyAll

### step 4

```java
new Thread(() -> {
    synchronized (room) {
        hasTakeout = true;
        log.debug("外卖到了噢！");
        room.notifyAll();
    }
}, "送外卖的").start();
```

用 notifyAll 仅解决某个线程的唤醒问题，但使用 if + wait 判断仅有一次机会，一旦条件不成立，就没有重新 判断的机会了 解决方法，用 while + wait，当条件不成立，再次 wai

### step 5

将 if 改为 while

```java
new Thread(() -> {
    synchronized (room) {
        log.debug("有烟没？[{}]", hasCigarette);
        while (!hasCigarette) {
            log.debug("没烟，先歇会！");
            try {
                room.wait();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        log.debug("有烟没？[{}]", hasCigarette);
        if (hasCigarette) {
            log.debug("可以开始干活了");
        } else {log.debug("没干成活...");
        }
    }
}, "小南").start();
```

## 8、Park & Unpark

### 基本使用

```java
// 暂停当前线程
LockSupport.park();  
// 恢复某个线程的运行 
LockSupport.unpark(暂停线程对象)
```

先 park 再 unpark

```java
@Slf4j(topic = "test.park")
public class TestPark {
    @Test
    public void test1() throws InterruptedException {
        Thread t1 = new Thread(() -> {
            log.debug("start...");
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            log.debug("park...");
            LockSupport.park();
            log.debug("resume...");
        },"t1");
        t1.start();
        Thread.sleep(2000);
        log.debug("unpark...");
        LockSupport.unpark(t1);
    }
}
```

输出

```
09:46:51 [t1] c.park - start...
09:46:52 [t1] c.park - park...
09:46:53 [main] c.park - unpark...
09:46:53 [t1] c.park - resume...
```

先 unpark 再 park

```java
@Test
public void test2() throws InterruptedException {
    Thread t1 = new Thread(() -> {
        log.debug("start...");
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        log.debug("park...");
        LockSupport.park();
        log.debug("resume...");
    }, "t1");
    t1.start();
    Thread.sleep(1000);
    log.debug("unpark...");
    LockSupport.unpark(t1);

}
```

### 原理

每个线程都有自己的一个 Parker 对象，由三部分组成 _counter ， _cond 和 _mutex 打个比喻

线程就像一个旅人，Parker 就像他随身携带的背包，条件变量就好比背包中的帐篷。_counter 就好比背包中 的备用干粮（0 为耗尽，1 为充足）

调用 park 就是要看需不需要停下来歇息，如果备用干粮耗尽，那么钻进帐篷歇息 如果备用干粮充足，那么不需停留，继续前进

调用 unpark，就好比令干粮充足，如果这时线程还在帐篷，就唤醒让他继续前进，如果这时线程还在运行，那么下次他调用 park 时，仅是消耗掉备用干粮，不需停留继续前进，因为背包空间有限，多次调用 unpark 仅会补充一份备用干粮



![image-20211114095226021](\images\image-20211114095226021.png)

![image-20211114095251503](\images\image-20211114095251503.png)

![image-20211114095321875](\images\image-20211114095321875.png)

## 9、重新理解线程状态转换

![image-20211114100425088](\images\image-20211114100425088.png)



假设有线程 Thread t 

情况 1 NEW --> RUNNABLE 当调用 t.start() 方法时，由 NEW --> RUNNABLE

情况 2 RUNNABLE <--> WAITING t 线程用 synchronized(obj) 获取了对象锁后

​	调用 obj.wait() 方法时，t 线程从 RUNNABLE --> WAITING 

​	调用 obj.notify() ， obj.notifyAll() ， t.interrupt() 时

​	竞争锁成功，t 线程从 WAITING --> RUNNABLE 竞争锁失败，t 线程从 WAITING --> BLOCKED

情况 3 RUNNABLE <--> WAITING

​	当前线程调用 t.join() 方法时，当前线程从 RUNNABLE --> WAITING 注意是当前线程在t 线程对象的监视器上等待

​	t 线程运行结束，或调用了当前线程的 interrupt() 时，当前线程从 WAITING --> RUNNABLE

情况 4 RUNNABLE <--> WAITING，当前线程调用 LockSupport.park() 方法会让当前线程从 RUNNABLE --> WAITING 调用 LockSupport.unpark(目标线程) 或调用了线程 的 interrupt() ，会让目标线程从 WAITING -->  RUNNABLE

情况 5 RUNNABLE <--> TIMED_WAITING，t 线程用 synchronized(obj) 获取了对象锁后，调用 obj.wait(long n) 方法时，t 线程从 RUNNABLE --> TIMED_WAITING，t 线程等待时间超过了 n 毫秒，或调用 obj.notify() ， obj.notifyAll() ， t.interrupt() 时

​	竞争锁成功，t 线程从 TIMED_WAITING --> RUNNABLE 竞争锁失败，t 线程从 TIMED_WAITING --> BLOCKED

情况 6 RUNNABLE <--> TIMED_WAITING

​	当前线程调用 t.join(long n) 方法时，当前线程从 RUNNABLE --> TIMED_WAITING，注意是当前线程在t 线程对象的监视器上等待

​	当前线程等待时间超过了 n 毫秒，或t 线程运行结束，或调用了当前线程的 interrupt() 时，当前线程从 TIMED_WAITING --> RUNNABLE

情况 7 RUNNABLE <--> TIMED_WAITING 当前线程调用 Thread.sleep(long n) ，当前线程从 RUNNABLE --> TIMED_WAITING 当前线程等待时间超过了 n 毫秒，当前线程从 TIMED_WAITING --> RUNNABLE

情况 8 RUNNABLE <--> TIMED_WAITIN，当前线程调用 LockSupport.parkNanos(long nanos) 或 LockSupport.parkUntil(long millis) 时，当前线 程从 RUNNABLE --> TIMED_WAITING，调用 LockSupport.unpark(目标线程) 或调用了线程 的 interrupt() ，或是等待超时，会让目标线程从 TIMED_WAITING--> RUNNABLE

情况 9 RUNNABLE <--> BLOCKED，t 线程用 synchronized(obj) 获取了对象锁时如果竞争失败，从 RUNNABLE --> BLOCKED，持 obj 锁线程的同步代码块执行完毕，会唤醒该对象上所有 BLOCKED 的线程重新竞争，如果其中 t 线程竞争 成功，从 BLOCKED --> RUNNABLE ，其它失败的线程仍然 BLOCKED

情况 10 RUNNABLE <--> TERMINATED，当前线程所有代码运行完毕，进入 TERMINATED

## 10、多把锁

### 多把不相干的锁

一间大屋子有两个功能：睡觉、学习，互不相干。 现在小南要学习，小女要睡觉，但如果只用一间屋子（一个对象锁）的话，那么并发度很低 解决方法是准备多个房间（多个对象锁）

```java
package com.harry.thread;

import lombok.extern.slf4j.Slf4j;

public class TestDeadLock {
    public static void main(String[] args) {
        BigRoom bigRoom = new BigRoom();
        new Thread(() -> {
            try {
                bigRoom.study();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        },"小南").start();
        new Thread(() -> {
            try {
                bigRoom.sleep();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        },"小女").start();
    }
}

@Slf4j(topic = "c.room")
class BigRoom {
    public void sleep() throws InterruptedException {
        synchronized (this) {
            log.debug("sleeping 2 小时");
            Thread.sleep(2000);
        }
    }

    public void study() throws InterruptedException {
        synchronized (this) {
            log.debug("study 1 小时");
            Thread.sleep(1000);
        }
    }
}
```

```
10:17:57 [小南] c.room - study 1 小时
10:17:58 [小女] c.room - sleeping 2 小时
```

改进

```java
@Slf4j(topic = "c.room")
class BigRoom {
    private final Object studyRoom = new Object();
    private final Object bedRoom = new Object();
    public void sleep() throws InterruptedException {
        synchronized (bedRoom ) {
            log.debug("sleeping 2 小时");
            Thread.sleep(2000);
        }
    }

    public void study() throws InterruptedException {
        synchronized (studyRoom) {
            log.debug("study 1 小时");
            Thread.sleep(1000);
        }
    }
}
```

将锁的粒度细分 好处，是可以增强并发度 坏处，如果一个线程需要同时获得多把锁，就容易发生死锁

## 11、活跃性

### 死锁

有这样的情况：一个线程需要同时获取多把锁，这时就容易发生死锁

 t1 线程 获得 A对象 锁，接下来想获取 B对象 的锁 t2 线程 获得 B对象 锁，接下来想获取 A对象 的锁 例：

```java
@Slf4j(topic = "c.Test")
public class TestDeadLock {
    public static void main(String[] args) {
        Object A = new Object();
        Object B = new Object();
        Thread t1 = new Thread(() -> {
            synchronized (A) {
                log.debug("lock A");
                try {
                    sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                synchronized (B) {
                    log.debug("lock B");
                    log.debug("操作...");
                }
            }
        }, "t1");
        Thread t2 = new Thread(() -> {
            synchronized (B) {
                log.debug("lock B");
                try {
                    sleep(500);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                synchronized (A) {
                    log.debug("lock A");
                    log.debug("操作...");
                }
            }
        }, "t2");
        log.debug("deadlock");
        t1.start();
        t2.start();
    }

}
```

```
10:36:38 [main] c.Test - deadlock
10:36:38 [t2] c.Test - lock B
10:36:38 [t1] c.Test - lock A
```

定位死锁

检测死锁可以使用 jconsole工具，或者使用 jps 定位进程 id，再用 jstack 定位死锁：

```
D:\JavaCode\JUC>jps
17476 Bootstrap
29572 Jps
9876 Launcher
18040
22296 Launcher
23944 TestProduce
27460 TestDeadLock
```

```
D:\JavaCode\JUC>jstack 27460
2021-11-14 10:41:24
Full thread dump Java HotSpot(TM) 64-Bit Server VM (25.251-b08 mixed mode):

"DestroyJavaVM" #14 prio=5 os_prio=0 tid=0x0000000003473800 nid=0x5a3c waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"t2" #13 prio=5 os_prio=0 tid=0x000000001f8f4800 nid=0x3308 waiting for monitor entry [0x000000001fe5f000]
   java.lang.Thread.State: BLOCKED (on object monitor)
        at com.harry.thread.TestDeadLock.lambda$main$1(TestDeadLock.java:38)
        - waiting to lock <0x0000000771252568> (a java.lang.Object)
        - locked <0x0000000771252578> (a java.lang.Object)
        at com.harry.thread.TestDeadLock$$Lambda$2/984213526.run(Unknown Source)
        at java.lang.Thread.run(Thread.java:748)

"t1" #12 prio=5 os_prio=0 tid=0x000000001f8f0000 nid=0x196c waiting for monitor entry [0x000000001fd5e000]
   java.lang.Thread.State: BLOCKED (on object monitor)
        at com.harry.thread.TestDeadLock.lambda$main$0(TestDeadLock.java:24)
        - waiting to lock <0x0000000771252578> (a java.lang.Object)
        - locked <0x0000000771252568> (a java.lang.Object)
        at com.harry.thread.TestDeadLock$$Lambda$1/1207769059.run(Unknown Source)
        at java.lang.Thread.run(Thread.java:748)

"Service Thread" #11 daemon prio=9 os_prio=0 tid=0x000000001e67b000 nid=0x5c48 runnable [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"C1 CompilerThread3" #10 daemon prio=9 os_prio=2 tid=0x000000001e5dd000 nid=0x264c waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"C2 CompilerThread2" #9 daemon prio=9 os_prio=2 tid=0x000000001e5d2800 nid=0x4518 waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"C2 CompilerThread1" #8 daemon prio=9 os_prio=2 tid=0x000000001e5cc000 nid=0x49cc waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"C2 CompilerThread0" #7 daemon prio=9 os_prio=2 tid=0x000000001e5ab800 nid=0x6308 waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"Monitor Ctrl-Break" #6 daemon prio=5 os_prio=0 tid=0x000000001e583800 nid=0x6760 runnable [0x000000001edaf000]
   java.lang.Thread.State: RUNNABLE
        at java.net.SocketInputStream.socketRead0(Native Method)
        at java.net.SocketInputStream.socketRead(SocketInputStream.java:116)
        at java.net.SocketInputStream.read(SocketInputStream.java:171)
        at java.net.SocketInputStream.read(SocketInputStream.java:141)
        at sun.nio.cs.StreamDecoder.readBytes(StreamDecoder.java:284)
        at sun.nio.cs.StreamDecoder.implRead(StreamDecoder.java:326)
        at sun.nio.cs.StreamDecoder.read(StreamDecoder.java:178)
        - locked <0x0000000770828158> (a java.io.InputStreamReader)
        at java.io.InputStreamReader.read(InputStreamReader.java:184)
        at java.io.BufferedReader.fill(BufferedReader.java:161)
        at java.io.BufferedReader.readLine(BufferedReader.java:324)
        - locked <0x0000000770828158> (a java.io.InputStreamReader)
        at java.io.BufferedReader.readLine(BufferedReader.java:389)
        at com.intellij.rt.execution.application.AppMainV2$1.run(AppMainV2.java:61)

"Attach Listener" #5 daemon prio=5 os_prio=2 tid=0x000000001e4e8800 nid=0x5ac8 waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"Signal Dispatcher" #4 daemon prio=9 os_prio=2 tid=0x000000001e540800 nid=0x30bc runnable [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"Finalizer" #3 daemon prio=8 os_prio=1 tid=0x000000001e4d1800 nid=0x730c in Object.wait() [0x000000001eaae000]
   java.lang.Thread.State: WAITING (on object monitor)
        at java.lang.Object.wait(Native Method)
        - waiting on <0x0000000770588ee0> (a java.lang.ref.ReferenceQueue$Lock)
        at java.lang.ref.ReferenceQueue.remove(ReferenceQueue.java:144)
        - locked <0x0000000770588ee0> (a java.lang.ref.ReferenceQueue$Lock)
        at java.lang.ref.ReferenceQueue.remove(ReferenceQueue.java:165)
        at java.lang.ref.Finalizer$FinalizerThread.run(Finalizer.java:216)

"Reference Handler" #2 daemon prio=10 os_prio=2 tid=0x000000001e4d0800 nid=0x8a0 in Object.wait() [0x000000001e9af000]
   java.lang.Thread.State: WAITING (on object monitor)
        at java.lang.Object.wait(Native Method)
        - waiting on <0x0000000770586c00> (a java.lang.ref.Reference$Lock)
        at java.lang.Object.wait(Object.java:502)
        at java.lang.ref.Reference.tryHandlePending(Reference.java:191)
        - locked <0x0000000770586c00> (a java.lang.ref.Reference$Lock)
        at java.lang.ref.Reference$ReferenceHandler.run(Reference.java:153)

"VM Thread" os_prio=2 tid=0x000000001c699800 nid=0x41dc runnable

"GC task thread#0 (ParallelGC)" os_prio=0 tid=0x0000000003488800 nid=0x3204 runnable

"GC task thread#1 (ParallelGC)" os_prio=0 tid=0x000000000348a000 nid=0x3b4c runnable

"GC task thread#2 (ParallelGC)" os_prio=0 tid=0x000000000348c000 nid=0x119c runnable

"GC task thread#3 (ParallelGC)" os_prio=0 tid=0x000000000348d800 nid=0x6578 runnable

"GC task thread#4 (ParallelGC)" os_prio=0 tid=0x0000000003490800 nid=0x1c80 runnable

"GC task thread#5 (ParallelGC)" os_prio=0 tid=0x0000000003492000 nid=0x16b8 runnable

"GC task thread#6 (ParallelGC)" os_prio=0 tid=0x0000000003495000 nid=0x58f8 runnable

"GC task thread#7 (ParallelGC)" os_prio=0 tid=0x0000000003496000 nid=0x2f84 runnable

"VM Periodic Task Thread" os_prio=2 tid=0x000000001e68d800 nid=0x633c waiting on condition

JNI global references: 316


Found one Java-level deadlock:
=============================

"t2":
  waiting to lock monitor 0x000000000356e678 (object 0x0000000771252568, a java.lang.Object),
  which is held by "t1"
"t1":
  waiting to lock monitor 0x000000000356bc88 (object 0x0000000771252578, a java.lang.Object),
  which is held by "t2"

Java stack information for the threads listed above:
===================================================

"t2":
        at com.harry.thread.TestDeadLock.lambda$main$1(TestDeadLock.java:38)
        - waiting to lock <0x0000000771252568> (a java.lang.Object)
        - locked <0x0000000771252578> (a java.lang.Object)
        at com.harry.thread.TestDeadLock$$Lambda$2/984213526.run(Unknown Source)
        at java.lang.Thread.run(Thread.java:748)
"t1":
        at com.harry.thread.TestDeadLock.lambda$main$0(TestDeadLock.java:24)
        - waiting to lock <0x0000000771252578> (a java.lang.Object)
        - locked <0x0000000771252568> (a java.lang.Object)
        at com.harry.thread.TestDeadLock$$Lambda$1/1207769059.run(Unknown Source)
        at java.lang.Thread.run(Thread.java:748)

Found 1 deadlock.
```

避免死锁要注意加锁顺序， 另外如果由于某个线程进入了死循环，导致其它线程一直等待，对于这种情况 linux 下可以通过 top 先定位到 CPU 占用高的 Java 进程，再利用 top -Hp 进程id 来定位是哪个线程，最后再用 jstack 排查

### 哲学家就餐问题

有五位哲学家，围坐在圆桌旁。 他们只做两件事，思考和吃饭，思考一会吃口饭，吃完饭后接着思考。 吃饭时要用两根筷子吃，桌上共有 5 根筷子，每位哲学家左右手边各有一根筷子。 如果筷子被身边的人拿着，自己就得等待

筷子类

```java
class Chopstick {
    String name;
    public Chopstick(String name) {
        this.name = name;
    }
    @Override
    public String toString() {
        return "筷子{" + name + '}';
    }
}
```

哲学类

```java
@Slf4j(topic = "c.test")
class Philosopher extends Thread {
    Chopstick left;
    Chopstick right;
    public Philosopher(String name, Chopstick left, Chopstick right) {
        super(name);
        this.left = left;
        this.right = right;
    }
    private void eat() throws InterruptedException {
        log.debug("eating...");
        Thread.sleep(1000);
    }

    @Override
    public void run() {
        while (true) {
            // 获得左手筷子
            synchronized (left) {
                // 获得右手筷子
                synchronized (right) {
                    // 吃饭
                    try {
                        eat();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
                // 放下右手筷子
            }
            // 放下左手筷子
        }
    }
}
```

就餐

```java
public class DeadLock2 {
    public static void main(String[] args) {
        Chopstick c1 = new Chopstick("1");
        Chopstick c2 = new Chopstick("2");
        Chopstick c3 = new Chopstick("3");
        Chopstick c4 = new Chopstick("4");
        Chopstick c5 = new Chopstick("5");
        new Philosopher("苏格拉底", c1, c2).start();
        new Philosopher("柏拉图", c2, c3).start();
        new Philosopher("亚里士多德", c3, c4).start();
        new Philosopher("赫拉克利特", c4, c5).start();
        new Philosopher("阿基米德", c5, c1).start();
    }
}
```

执行不多会，就执行不下去了

```
10:46:00 [苏格拉底] c.test - eating...
10:46:00 [亚里士多德] c.test - eating...
10:46:01 [柏拉图] c.test - eating...
10:46:01 [阿基米德] c.test - eating...
10:46:02 [赫拉克利特] c.test - eating...
10:46:02 [柏拉图] c.test - eating...
10:46:03 [柏拉图] c.test - eating...
10:46:04 [苏格拉底] c.test - eating...
```

这种线程没有按预期结束，执行不下去的情况，归类为【活跃性】问题，除了死锁以外，还有活锁和饥饿者两种情 况

### 活锁

活锁出现在两个线程互相改变对方的结束条件，最后谁也无法结束，例如

```java
@Slf4j(topic = "c.test")
public class TestLiveLock {
    static volatile int count = 10;
    static final Object lock = new Object();
    public static void main(String[] args) {
        new Thread(() -> {
            // 期望减到 0 退出循环
            while (count > 0) {
                try {
                    Thread.sleep(200);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                count--;
                log.debug("count: {}", count);
            }
        }, "t1").start();
        new Thread(() -> {
            // 期望超过 20 退出循环
            while (count < 20) {
                try {
                    Thread.sleep(200);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                count++;
                log.debug("count: {}", count);
            }
        }, "t2").start();
    }
}
```

### 饥饿

很多教程中把饥饿定义为，一个线程由于优先级太低，始终得不到 CPU 调度执行，也不能够结束，饥饿的情况不 易演示，讲读写锁时会涉及饥饿问题 下面我讲一下我遇到的一个线程饥饿的例子，先来看看使用顺序加锁的方式解决之前的死锁问题

![image-20211114105008112](\images\image-20211114105008112.png)



顺序加锁的解决方案

![image-20211114105040818](\images\image-20211114105040818.png)



## 12、ReentrantLock

相对于 synchronized 它具备如下特点 

​	可中断 

​	可以设置超时时间 

​	可以设置为公平锁 支持多个条件变量

与 synchronized 一样，都支持可重入

```java
reentrantLock.lock();
try {
// 临界区
} finally {
// 释放锁
reentrantLock.unlock();
}
```

### 可重入

可重入是指同一个线程如果首次获得了这把锁，那么因为它是这把锁的拥有者，因此有权利再次获取这把锁 如果是不可重入锁，那么第二次获得锁时，自己也会被锁挡住

```java
import java.util.concurrent.locks.ReentrantLock;
@Slf4j(topic = "c.test")
public class TestReentrantLock {
    static ReentrantLock lock = new ReentrantLock();
    public static void main(String[] args) {
        method1();
    }
    public static void method1() {
        lock.lock();
        try {
            log.debug("execute method1");
            method2();
        } finally {
            lock.unlock();
        }
    }
    public static void method2() {
        lock.lock();
        try {
            log.debug("execute method2");
            method3();
        } finally {
            lock.unlock();
        }
    }
    public static void method3() {
        lock.lock();
        try {
            log.debug("execute method3");
        } finally {
            lock.unlock();
        }
    }
}
```

```
10:56:29 [main] c.test - execute method1
10:56:29 [main] c.test - execute method2
10:56:29 [main] c.test - execute method3
```

### 可打断

```java
@Slf4j(topic = "c.test")
public class TestReentrantLock2 {
    public static void main(String[] args) {
        ReentrantLock lock = new ReentrantLock();
        Thread t1 = new Thread(() -> { log.debug("启动...");
            try {
                lock.lockInterruptibly();
            } catch (InterruptedException e) {
                e.printStackTrace();
                log.debug("等锁的过程中被打断");
                return;
            }
            try {
                log.debug("获得了锁");
            } finally {
                lock.unlock();
            }
        }, "t1");
        lock.lock();
        log.debug("获得了锁");
        t1.start();
        try {
            Thread.sleep(1000);
            t1.interrupt();
            log.debug("执行打断");
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }

    }
}
```

输出

```
10:58:52 [main] c.test - 获得了锁
10:58:52 [t1] c.test - 启动...
10:58:53 [main] c.test - 执行打断
10:58:53 [t1] c.test - 等锁的过程中被打断
java.lang.InterruptedException
	at java.util.concurrent.locks.AbstractQueuedSynchronizer.doAcquireInterruptibly(AbstractQueuedSynchronizer.java:898)
	at java.util.concurrent.locks.AbstractQueuedSynchronizer.acquireInterruptibly(AbstractQueuedSynchronizer.java:1222)
	at java.util.concurrent.locks.ReentrantLock.lockInterruptibly(ReentrantLock.java:335)
	at com.harry.thread.TestReentrantLock2.lambda$main$0(TestReentrantLock2.java:13)
	at java.lang.Thread.run(Thread.java:748)
```

注意如果是不可中断模式，那么即使使用了 interrupt 也不会让等待中断

### 锁超时

立刻失败

```java
package com.harry.thread;

import lombok.extern.slf4j.Slf4j;

import java.util.concurrent.locks.ReentrantLock;
@Slf4j(topic = "c.test")
public class TestReentrantLock3 {
    public static void main(String[] args) {
        ReentrantLock lock = new ReentrantLock();
        Thread t1 = new Thread(() -> {
            log.debug("启动...");
            if (!lock.tryLock()) {
                log.debug("获取立刻失败，返回");
                return;
            }
            try {
                log.debug("获得了锁");
            } finally {
                lock.unlock();
            }
        }, "t1");
        lock.lock();
        log.debug("获得了锁");
        t1.start();
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }
    }
}
```

```
11:03:27 [main] c.test - 获得了锁
11:03:27 [t1] c.test - 启动...
11:03:27 [t1] c.test - 获取立刻失败，返回
```

超时失败

```java
@Test
public void test1(){
    ReentrantLock lock = new ReentrantLock();
    Thread t1 = new Thread(() -> {
        log.debug("启动...");
        try {
            if (!lock.tryLock(1, TimeUnit.SECONDS)) {
                log.debug("获取等待 1s 后失败，返回");
                return;
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        try {
            log.debug("获得了锁");
        } finally {
            lock.unlock();
        }
    }, "t1");
    lock.lock();
    log.debug("获得了锁");
    t1.start();
    try {
        Thread.sleep(2000);
    } catch (InterruptedException e) {
        e.printStackTrace();
    } finally {
        lock.unlock();
    }
}
```

```
11:04:55 [main] c.test - 获得了锁
11:04:55 [t1] c.test - 启动...
11:04:56 [t1] c.test - 获取等待 1s 后失败，返回
```

使用 tryLock 解决哲学家就餐问题

```java
class Chopstick extends ReentrantLock {
    String name;
    public Chopstick(String name) {
        this.name = name;
    }
    @Override
    public String toString() {
        return "筷子{" + name + '}';
    }
}
```

```java
@Override
public void run() {
    while (true) {
        // 尝试获得左手筷子
        if (left.tryLock()) {
            try {
                // 尝试获得右手筷子
                if (right.tryLock()) {
                    try {
                        eat();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    } finally {
                        right.unlock();
                    }
                }
            } finally {
                left.unlock();
            }
        }
    }
}
```

### 公平锁

ReentrantLock 默认是不公平的

```java
package com.harry.thread;

import lombok.extern.slf4j.Slf4j;
import org.junit.Test;

import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantLock;
@Slf4j(topic = "c.test")
public class TestReentrantLock3 {
    public static void main(String[] args) {
        ReentrantLock lock = new ReentrantLock();
        Thread t1 = new Thread(() -> {
            log.debug("启动...");
            if (!lock.tryLock()) {
                log.debug("获取立刻失败，返回");
                return;
            }
            try {
                log.debug("获得了锁");
            } finally {
                lock.unlock();
            }
        }, "t1");
        lock.lock();
        log.debug("获得了锁");
        t1.start();
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }
    }
    @Test
    public void test1(){
        ReentrantLock lock = new ReentrantLock();
        Thread t1 = new Thread(() -> {
            log.debug("启动...");
            try {
                if (!lock.tryLock(1, TimeUnit.SECONDS)) {
                    log.debug("获取等待 1s 后失败，返回");
                    return;
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            try {
                log.debug("获得了锁");
            } finally {
                lock.unlock();
            }
        }, "t1");
        lock.lock();
        log.debug("获得了锁");
        t1.start();
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }
    }
    public void test2() throws InterruptedException {
        ReentrantLock lock = new ReentrantLock(false);
        lock.lock();
        for (int i = 0; i < 500; i++) {
            new Thread(() -> {
                lock.lock();
                try {
                    System.out.println(Thread.currentThread().getName() + " running...");
                } finally {
                    lock.unlock();
                }
            }, "t" + i).start();
        }
        // 1s 之后去争抢锁
        Thread.sleep(1000);
        new Thread(() -> {
            System.out.println(Thread.currentThread().getName() + " start...");
            lock.lock();
            try {
                System.out.println(Thread.currentThread().getName() + " running...");
            } finally {
                lock.unlock();
            }
        }, "强行插入").start();
        lock.unlock();
    }
}
```

强行插入，有机会在中间输出

```
t0 running...
t2 running...
t1 running...
t18 running...
t19 running...
t3 running...
t22 running...
t12 running...
t6 running...
t7 running...
t10 running...
t11 running...
t14 running...
t15 running...
t4 running...
强行插入 start...
t5 running...
t23 running...
```

改为公平锁后

```
ReentrantLock lock = new ReentrantLock(true);
```

公平锁一般没有必要，会降低并发度

### 条件变量

synchronized 中也有条件变量，就是我们讲原理时那个 waitSet 休息室，当条件不满足时进入 waitSet 等待 ReentrantLock 的条件变量比 synchronized 强大之处在于，它是支持多个条件变量的，这就好比synchronized 是那些不满足条件的线程都在一间休息室等消息 而 ReentrantLock 支持多间休息室，有专门等烟的休息室、专门等早餐的休息室、唤醒时也是按休息室来唤 醒

使用要点：

​	await 前需要获得锁 

​	await 执行后，会释放锁，进入 conditionObject 等待

​	 await 的线程被唤醒（或打断、或超时）取重新竞争 lock 锁 

​	竞争 lock 锁成功后，从 await 后继续执行

例子：

```java
package com.harry.thread;

import lombok.extern.slf4j.Slf4j;

import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

@Slf4j(topic = "c.test")
public class TestReentrantLock4 {
    static ReentrantLock lock = new ReentrantLock();
    static Condition waitCigaretteQueue = lock.newCondition();
    static Condition waitbreakfastQueue = lock.newCondition();
    static volatile boolean hasCigrette = false;
    static volatile boolean hasBreakfast = false;
    public static void main(String[] args) throws InterruptedException {
        new Thread(() -> {
            try {
                lock.lock();
                while (!hasCigrette) {try {
                    waitCigaretteQueue.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                }
                log.debug("等到了它的烟");
            } finally {
                lock.unlock();
            }
        }).start();
        new Thread(() -> {
            try {
                lock.lock();
                while (!hasBreakfast) {
                    try {
                        waitbreakfastQueue.await();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
                log.debug("等到了它的早餐");
            } finally {
                lock.unlock();
            }
        }).start();
        Thread.sleep(1000);
        sendBreakfast();
        Thread.sleep(1000);
        sendCigarette();
    }
    private static void sendCigarette() {
        lock.lock();
        try {
            log.debug("送烟来了");
            hasCigrette = true;
            waitCigaretteQueue.signal();
        } finally {
            lock.unlock();
        }
    }
    private static void sendBreakfast() {
        lock.lock();
        try {
            log.debug("送早餐来了");
            hasBreakfast = true;
            waitbreakfastQueue.signal();
        } finally {
            lock.unlock();
        }
    }

}
```

```
11:29:05 [main] c.test - 送早餐来了
11:29:05 [Thread-1] c.test - 等到了它的早餐
11:29:06 [main] c.test - 送烟来了
11:29:06 [Thread-0] c.test - 等到了它的烟
```



# 四、设计模式

## 1、同步模式之保护性暂停

即 Guarded Suspension，用在一个线程等待另一个线程的执行结果

要点 

​	有一个结果需要从一个线程传递到另一个线程，让他们关联同一个 GuardedObject 

​	如果有结果不断从一个线程到另一个线程那么可以使用消息队列（见生产者/消费者） 

​	JDK 中，join 的实现、Future 的实现，采用的就是此模式

​	因为要等待另一方的结果，因此归类到同步模式

![image-20211109193546076](\images\image-20211109193546076.png)

### 实现

```java
package com.harry.thread;

public class GuardedObject {
    private Object response;

    private final Object lock = new Object();

    public Object get(){
        synchronized (lock){
            // 条件不满足则等待
            while (response == null){
                try {
                    lock.wait();
                }catch (InterruptedException e){
                    e.printStackTrace();
                }
            }
            return response;
        }
    }

    public void complete(Object response) {
        synchronized (lock) {
            // 条件满足，通知等待线程
            this.response = response;
            lock.notifyAll();
        }
    }

}
```

###  应用

一个线程等待另一个线程的执行结果

```java
public class Downloader {
    public static List<String> download() throws IOException {
        HttpURLConnection urlConnection = (HttpURLConnection)new URL("https://www.baidu.com/").openConnection();
        ArrayList<String> list = new ArrayList<>();
        try(BufferedReader reader = new BufferedReader(new InputStreamReader(urlConnection.getInputStream(), StandardCharsets.UTF_8))){
            String line;
            while ((line = reader.readLine()) != null){
                list.add(line);
            }
        }
        return list;
    }
}
```

```java
@Slf4j(topic = "c.test")
class Test{
    public static void main(String[] args) {
        GuardedObject guardedObject = new GuardedObject();
        new Thread(()->{
            // 子线程执行下载
            try {
                List<String> response = Downloader.download();
                log.debug("download complete");
                guardedObject.complete(response);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }).start();
        log.debug("waiting");
        // 主线程阻塞等待
        Object response = guardedObject.get();
        log.debug("get response:[{}] lines", ((List<String>) response).size());
    }
}
```

```
19:59:11 [main] c.test - waiting
19:59:13 [Thread-0] c.test - download complete
19:59:13 [main] c.test - get response:[3] lines
```



### 带超时版 GuardedObject

如果要控制超时时间呢

```java
package com.harry.thread;

import lombok.extern.slf4j.Slf4j;

@Slf4j(topic = "c.Guarde")
public class GuardedObjectV2 {
    private Object response;

    private final Object lock = new Object();

    public Object get(long millis){
        synchronized (lock){
            // 1) 记录最初时间
            long begin = System.currentTimeMillis();
            // 2) 已经经历的时间
            long timePassed = 0;
            while (response == null) {
                // 4) 假设 millis 是 1000，结果在 400 时唤醒了，那么还有 600 要等
                long waitTime = millis - timePassed;
                log.debug("waitTime: {}", waitTime);
                if (waitTime <= 0) {
                    log.debug("break...");
                    break;
                }
                try {
                    lock.wait(waitTime);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                // 3) 如果提前被唤醒，这时已经经历的时间假设为 400
                timePassed = System.currentTimeMillis() - begin;
                log.debug("timePassed: {}, object is null {}",
                        timePassed, response == null);
            }

            return response;
        }
    }

    public void complete(Object response) {
        synchronized (lock) {
            // 条件满足，通知等待线程
            this.response = response;
            lock.notifyAll();
        }
    }
}
```

## 2、原理之Join

### 多任务版 GuardedObject

图中 Futures 就好比居民楼一层的信箱（每个信箱有房间编号），左侧的 t0，t2，t4 就好比等待邮件的居民，右 侧的 t1，t3，t5 就好比邮递员

如果需要在多个类之间使用 GuardedObject 对象，作为参数传递不是很方便，因此设计一个用来解耦的中间类， 这样不仅能够解耦【结果等待者】和【结果生产者】，还能够同时支持多个任务的管理

![image-20211109201049969](\images\image-20211109201049969.png)

新增 id 用来标识 Guarded Object

```java
package com.harry.thread;

public class Guarded {
    private int id;

    public Guarded(int id) {
        this.id = id;
    }
    public int getId() {
        return id;
    }
    // 结果
    private Object response;
    // 获取结果
    // timeout 表示要等待多久 2000
    public Object get(long timeout) throws InterruptedException {
        synchronized (this) {
            // 开始时间 15:00:00
            long begin = System.currentTimeMillis();
            // 经历的时间
            long passedTime = 0;
            while (response == null) {
                // 这一轮循环应该等待的时间
                long waitTime = timeout - passedTime;
                // 经历的时间超过了最大等待时间时，退出循环
                if (timeout - passedTime <= 0) {
                    break;
                }
                this.wait(waitTime);
                // 求得经历时间
                passedTime = System.currentTimeMillis() - begin;
            }
            return response;
        }
    }
    // 产生结果
    public void complete(Object response) {
        synchronized (this) {
            // 给结果成员变量赋值
            this.response = response;
            this.notifyAll();
        }
    }

}
```

中间解耦类

```java
public class Guarded {
    private int id;

    public Guarded(int id) {
        this.id = id;
    }
    public int getId() {
        return id;
    }
    // 结果
    private Object response;
    // 获取结果
    // timeout 表示要等待多久 2000
    public Object get(long timeout) throws InterruptedException {
        synchronized (this) {
            // 开始时间 15:00:00
            long begin = System.currentTimeMillis();
            // 经历的时间
            long passedTime = 0;
            while (response == null) {
                // 这一轮循环应该等待的时间
                long waitTime = timeout - passedTime;
                // 经历的时间超过了最大等待时间时，退出循环
                if (timeout - passedTime <= 0) {
                    break;
                }
                this.wait(waitTime);
                // 求得经历时间
                passedTime = System.currentTimeMillis() - begin;
            }
            return response;
        }
    }
    // 产生结果
    public void complete(Object response) {
        synchronized (this) {
            // 给结果成员变量赋值
            this.response = response;
            this.notifyAll();
        }
    }

}
class Mailboxes{
    private static Map<Integer, Guarded> boxes = new Hashtable<>();
    private static int id = 1;
    // 产生唯一 id
    private static synchronized int generateId() {
        return id++;
    }
    public static Guarded getGuardedObject(int id) {
        return boxes.remove(id);
    }
    public static Guarded createGuardedObject() {
        Guarded go = new Guarded(generateId());
        boxes.put(go.getId(), go);
        return go;
    }
    public static Set<Integer> getIds() {
        return boxes.keySet();
    }

}
```

业务相关类

```java
@Slf4j(topic = "c.post")
class Postman extends Thread {
    private int id;
    private String mail;

    public Postman(int id, String mail) {
        this.id = id;
        this.mail = mail;
    }

    @Override
    public void run() {
        Guarded guardedObject = Mailboxes.getGuardedObject(id);
        log.debug("送信 id:{}, 内容:{}", id, mail);
        guardedObject.complete(mail);
    }
}
```

```java
@Slf4j(topic = "c.people")
class People extends Thread {
    @Override
    public void run() {
        // 收信
        Guarded guardedObject = Mailboxes.createGuardedObject();
        log.debug("开始收信 id:{}", guardedObject.getId());
        Object mail = null;
        try {
            mail = guardedObject.get(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        log.debug("收到信 id:{}, 内容:{}", guardedObject.getId(), mail);
    }


}
```

测试

```java
class Test2 {
    public static void main(String[] args) throws InterruptedException {

        for (int i = 0; i < 3; i++) {
            new People().start();
        }
        sleep(1000);
        for (Integer id : Mailboxes.getIds()) {
            new Postman(id, "内容" + id).start();
        }
    }

}
```

## 3、异步模式之生产者/消费者

### 定义

要点

​	与前面的保护性暂停中的 GuardObject 不同，不需要产生结果和消费结果的线程一一对应

​	消费队列可以用来平衡生产和消费的线程资源 

​	生产者仅负责产生结果数据，不关心数据该如何处理，而消费者专心处理结果数据 

​	消息队列是有容量限制的，满时不会再加入数据，空时不会再消耗数据 

​	JDK 中各种阻塞队列，采用的就是这种模式

![image-20211109211102768](\images\image-20211109211102768.png)

```java
package com.harry.thread.produce;

public class Message {
    private int id;
    private Object message;

    public Message(int id, Object message) {
        this.id = id;
        this.message = message;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public Object getMessage() {
        return message;
    }

    public void setMessage(Object message) {
        this.message = message;
    }
}
```

```java
package com.harry.thread.produce;

import lombok.extern.slf4j.Slf4j;

import java.util.LinkedList;

@Slf4j(topic = "c.messageQueue")
public class MessageQueue {
    private LinkedList<Message> queue;
    private int capacity;
    public MessageQueue(int capacity) {
        this.capacity = capacity;
        queue = new LinkedList<>();
    }
    public Message take() {
        synchronized (queue) {
            while (queue.isEmpty()) {
                log.debug("没货了, wait");
                try {
                    queue.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            Message message = queue.removeFirst();
            queue.notifyAll();
            return message;
        }
    }
    public void put(Message message) {
        synchronized (queue) {
            while (queue.size() == capacity) {
                log.debug("库存已达上限, wait");
                try {
                    queue.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            queue.addLast(message);
            queue.notifyAll();
        }
    }
}
```

应用

```java
package com.harry.thread.produce;

import com.harry.thread.Downloader;
import lombok.extern.slf4j.Slf4j;

import java.io.IOException;
import java.util.List;
@Slf4j(topic = "c.produce")
public class TestProduce {
    public static void main(String[] args) {
        MessageQueue messageQueue = new MessageQueue(2);
        for (int i = 0; i <4 ; i++) {
            int id = i;
            new Thread(()->{
                try {
                    log.debug("download...");
                    List<String> response = null;
                    response = Downloader.download();
                    log.debug("try put message({})", id);
                    messageQueue.put(new Message(id, response));
                } catch (IOException e) {
                    e.printStackTrace();
                }
            },"生产者"+i).start();
        }

        new Thread(()->{
            while (true){
                Message message = messageQueue.take();
                List<String> response = (List<String>) message.getMessage();
                log.debug("take message({}): [{}] lines", message.getId(), response.size());
            }
        }, "消费者").start();
    }
}
```

结果

```
21:21:59 [生产者2] c.produce - download...
21:21:59 [消费者] c.messageQueue - 没货了, wait
21:21:59 [生产者0] c.produce - download...
21:21:59 [生产者3] c.produce - download...
21:21:59 [生产者1] c.produce - download...
21:22:01 [生产者0] c.produce - try put message(0)
21:22:01 [生产者2] c.produce - try put message(2)
21:22:01 [生产者3] c.produce - try put message(3)
21:22:01 [生产者1] c.produce - try put message(1)
21:22:01 [生产者1] c.messageQueue - 库存已达上限, wait
21:22:01 [生产者3] c.messageQueue - 库存已达上限, wait
21:22:01 [生产者1] c.messageQueue - 库存已达上限, wait
21:22:01 [消费者] c.produce - take message(2): [3] lines
21:22:01 [消费者] c.produce - take message(0): [3] lines
21:22:01 [消费者] c.produce - take message(3): [3] lines
21:22:01 [消费者] c.produce - take message(1): [3] lines
21:22:01 [消费者] c.messageQueue - 没货了, wait
```

# 五、共享模式之内存

## 1、Java内存模型

JMM 即 Java Memory Model，它定义了主存、工作内存抽象概念，底层对应着 CPU 寄存器、缓存、硬件内存、 CPU 指令优化等。

JMM 体现在以下几个方面

原子性 - 保证指令不会受到线程上下文切换的影响 

可见性 - 保证指令不会受 cpu 缓存的影响 

有序性 - 保证指令不会受 cpu 指令并行优化的影响

## 2、可见性

退不出的循环 先来看一个现象，main 线程对 run 变量的修改对于 t 线程不可见，导致了 t 线程无法停止

1.初始状态， t 线程刚开始从主内存读取了 run 的值到工作内存。

![image-20211116205021352](\images\image-20211116205021352.png)

2.因为 t 线程要频繁从主内存中读取 run 的值，JIT 编译器会将 run 的值缓存至自己工作内存中的高速缓存中， 减少对主存中 run 的访问，提高效率

![image-20211116205352581](\images\image-20211116205352581.png)

3 1 秒之后，main 线程修改了 run 的值，并同步至主存，而 t 是从自己工作内存中的高速缓存中读取这个变量 的值，结果永远是旧值

![image-20211116205446319](\images\image-20211116205446319.png)

解决方法

它可以用来修饰成员变量和静态成员变量，他可以避免线程从自己的工作缓存中查找变量的值，必须到主存中获取 它的值，线程操作 volatile 变量都是直接操作主存

### 可见性 vs 原子性

前面例子体现的实际就是可见性，它保证的是在多个线程之间，一个线程对 volatile 变量的修改对另一个线程可 见， 不能保证原子性，仅用在一个写线程，多个读线程的情况： 上例从字节码理解是这样的：

```
getstatic run // 线程 t 获取 run true 
getstatic run // 线程 t 获取 run true 
getstatic run // 线程 t 获取 run true 
getstatic run // 线程 t 获取 run true 
putstatic run // 线程 main 修改 run 为 false， 仅此一次
getstatic run // 线程 t 获取 run false 
```

比较一下之前我们将线程安全时举的例子：两个线程一个 i++ 一个 i-- ，只能保证看到最新值，不能解决指令交错

注意 synchronized 语句块既可以保证代码块的原子性，也同时保证代码块内变量的可见性。但缺点是 synchronized 是属于重量级操作，性能相对更低

### 终止模式之两阶段终止模式

在一个线程 T1 中如何“优雅”终止线程 T2？这里的【优雅】指的是给 T2 一个料理后事的机会。

#### 错误思想

使用线程对象的 stop() 方法停止线程 stop 方法会真正杀死线程，如果这时线程锁住了共享资源，那么当它被杀死后就再也没有机会释放锁， 其它线程将永远无法获取锁

使用 System.exit(int) 方法停止线程 目的仅是停止一个线程，但这种做法会让整个程序都停止

#### 两阶段终止模式

![image-20211116210204439](\images\image-20211116210204439.png)

利用 isInterrupted

interrupt 可以打断正在执行的线程，无论这个线程是在 sleep，wait，还是正常运行

```java
package com.harry.thread;

import lombok.extern.slf4j.Slf4j;

@Slf4j(topic = "c.test")
public class TPTInterrupt {
    private Thread thread;

    public void start(){
        thread = new Thread(()->{
            while (true){
                Thread current = Thread.currentThread();
                if (current.isInterrupted()){
                    log.debug("料理后事");
                    break;
                }
                try {
                    Thread.sleep(1000);
                    log.debug("将结果保存");
                }catch (InterruptedException e) {
                    current.interrupt();
                }
            }
        },"线程监控");
        thread.start();
    }
    public void stop() {
        thread.interrupt();
    }

}
@Slf4j(topic = "c.test1")
class Test1{
    public static void main(String[] args) throws InterruptedException {
        TPTInterrupt t = new TPTInterrupt();
        t.start();
        Thread.sleep(3500);
        log.debug("stop");
        t.stop();

    }
}
```

结果

```
21:08:20 [线程监控] c.test - 将结果保存
21:08:21 [线程监控] c.test - 将结果保存
21:08:22 [线程监控] c.test - 将结果保存
21:08:22 [main] c.test1 - stop
21:08:22 [线程监控] c.test - 料理后事
```

利用停止标记

```java
package com.harry.thread;

import lombok.extern.slf4j.Slf4j;

// 停止标记用 volatile 是为了保证该变量在多个线程之间的可见性
// 我们的例子中，即主线程把它修改为 true 对 t1 线程可见
@Slf4j(topic = "c.test")
public class TPTInterrupt {
    private Thread thread;
    private volatile boolean stop = false;
    public void start() {
        thread = new Thread(() -> {
            while (true) {
                Thread current = Thread.currentThread();
                if (stop) {
                    log.debug("料理后事");
                    break;
                }
                try {
                    Thread.sleep(1000);
                    log.debug("将结果保存");
                } catch (InterruptedException e) {

                }
                
            }
        },"监控线程");
        thread.start();
    }
    public void stop() {
        stop = true;
    }

}
@Slf4j(topic = "c.test1")
class Test1{
    public static void main(String[] args) throws InterruptedException {
        TPTInterrupt t = new TPTInterrupt();
        t.start();
        Thread.sleep(3500);
        log.debug("stop");
        t.stop();

    }
}
```

#### 同步模式之 Balking

Balking （犹豫）模式用在一个线程发现另一个线程或本线程已经做了某一件相同的事，那么本线程就无需再做 了，直接结束返回

```java
@Slf4j(topic = "c.test1")
public class MonitorService {
    // 用来表示是否已经有线程已经在执行启动了
    private volatile boolean starting;
    public void start() {
        log.info("尝试启动监控线程...");
        synchronized (this) {
            if (starting) {
                return;
            }
            starting = true;
        }

        // 真正启动监控线程...
    }
}
```

它还经常用来实现线程安全的单例

```java
public class Singleton {
    private Singleton(){
        
    }
    private static Singleton INSTANCE = null;
    
    public static synchronized Singleton getInstance(){
        if (INSTANCE != null){
            return INSTANCE;
        }
        INSTANCE = new Singleton();
        return  INSTANCE;
    }
}
```

## 3、有序性

JVM 会在不影响正确性的前提下，可以调整语句的执行顺序，思考下面一段代

```
static int i;
static int j;
// 在某个线程内执行如下赋值操作
i = ...;
j = ...; 
```

可以看到，至于是先执行 i 还是 先执行 j ，对最终的结果不会产生影响。所以，上面代码真正执行时，既可以是

i = ...; 	 j = ...;

也可以是

j = ...; i = ...; 

这种特性称之为『指令重排』，多线程下『指令重排』会影响正确性。

### 诡异的结果

```java
int num = 0;
boolean ready = false;
// 线程1 执行此方法
public void actor1(I_Result r) {
    if(ready) {
        r.r1 = num + num;
    } else {
        r.r1 = 1;
    }
}
// 线程2 执行此方法
public void actor2(I_Result r) {
    num = 2;
    ready = true;
}
```

I_Result 是一个对象，有一个属性 r1 用来保存结果，这种情况下是：线程2 执行 ready = true，切换到线程1，进入 if 分支，相加为 0，再切回线程2 执行 num = 2

这种现象叫做指令重排，是 JIT 编译器在运行时的一些优化，这个现象需要通过大量测试才能复现：

借助 java 并发压测工具 jcstress https://wiki.openjdk.java.net/display/CodeTools/jcstress

```
mvn archetype:generate -DinteractiveMode=false -DarchetypeGroupId=org.openjdk.jcstress - DarchetypeArtifactId=jcstress-java-test-archetype -DarchetypeVersion=0.5 -DgroupId=cn.itcast - DartifactId=ordering -Dversion=1.0 
```

```java
@JCStressTest
@Outcome(id = {"1", "4"}, expect = Expect.ACCEPTABLE, desc = "ok")
@Outcome(id = "0", expect = Expect.ACCEPTABLE_INTERESTING, desc = "!!!!")
@State
public class VolatileTest {
    int num = 0;
    boolean ready = false;
    // 线程1 执行此方法
    public void actor1(I_Result r) {
        if(ready) {
            r.r1 = num + num;
        } else {
            r.r1 = 1;
        }
    }
    // 线程2 执行此方法
    public void actor2(I_Result r) {
        num = 2;
        ready = true;
    }
}
```

执行

```
mvn clean install  
java -jar target/jcstress.jar 
```

会输出我们感兴趣的结果，摘录其中一次结果：

```
*** INTERESTING tests
        Some interesting behaviors observed. This is for the plain curiosity.
        2 matching test results.
        [OK] test.ConcurrencyTest
        (JVM args: [-XX:-TieredCompilation])
        Observed state Occurrences Expectation Interpretation
        0 1,729 ACCEPTABLE_INTERESTING !!!!
        1 42,617,915 ACCEPTABLE ok
        4 5,146,627 ACCEPTABLE ok
        [OK] test.ConcurrencyTest
        (JVM args: [])
        Observed state Occurrences Expectation Interpretation
        0 1,652 ACCEPTABLE_INTERESTING !!!!
        1 46,460,657 ACCEPTABLE ok
        4 4,571,072 ACCEPTABLE ok 
```

可以看到，出现结果为 0 的情况有 638 次，虽然次数相对很少，但毕竟是出现了。

### 解决方法

volatile 修饰的变量，可以禁用指令重排volatile 修饰的变量，可以禁用指令重排

```java
int num = 0;
volatile boolean ready = false
// 线程1 执行此方法
public void actor1(I_Result r) {
    if(ready) {
        r.r1 = num + num;
    } else {
        r.r1 = 1;
    }
}
// 线程2 执行此方法
public void actor2(I_Result r) {
    num = 2;
    ready = true;
}
```

### 内存屏障

Memory Barrier（Memory Fence）

可见性 写屏障（sfence）保证在该屏障之前的，对共享变量的改动，都同步到主存当中 而读屏障（lfence）保证在该屏障之后，对共享变量的读取，加载的是主存中最新数据

有序性 写屏障会确保指令重排序时，不会将写屏障之前的代码排在写屏障之后 读屏障会确保指令重排序时，不会将读屏障之后的代码排在读屏障之前

![image-20211116213440218](\images\image-20211116213440218.png)

### volatile 原理

volatile 的底层实现原理是内存屏障，Memory Barrier（Memory Fence）

 对 volatile 变量的写指令后会加入写屏障

 对 volatile 变量的读指令前会加入读屏障

#### 保证可见性

写屏障（sfence）保证在该屏障之前的，对共享变量的改动，都同步到主存当

```java
public void actor2(I_Result r) {
    num = 2;
    ready = true; // ready 是 volatile 赋值带写屏障
    // 写屏障
}
```

而读屏障（lfence）保证在该屏障之后，对共享变量的读取，加载的是主存中最新数据

```java
public void actor1(I_Result r) {
    // 读屏障
    // ready 是 volatile 读取值带读屏障
    if(ready) {
        r.r1 = num + num;
    } else {
        r.r1 = 1;
    }
}
```

![image-20211116213726332](\images\image-20211116213726332.png)

#### 保证有序性

写屏障会确保指令重排序时，不会将写屏障之前的代码排在写屏障之后

```java
public void actor2(I_Result r) {
    num = 2;
    ready = true; // ready 是 volatile 赋值带写屏障
    // 写屏障
}
```

读屏障会确保指令重排序时，不会将读屏障之后的代码排在读屏障之前

```java
public void actor1(I_Result r) {
    // 读屏障
    // ready 是 volatile 读取值带读屏障
    if(ready) {
        r.r1 = num + num;
    } else {
        r.r1 = 1;
    }
}
```

![image-20211116214019111](\images\image-20211116214019111.png)

写屏障仅仅是保证之后的读能够读到最新的结果，但不能保证读跑到它前面去 而有序性的保证也只是保证了本线程内相关代码不被重排序

![image-20211116214059554](\images\image-20211116214059554.png)

#### double-checked locking 问题

以著名的 double-checked locking 单例模式为例

```JAVA
public class Singleton2 {
    private Singleton2(){
        
    }
    private static Singleton2 INSTANCE = null;
    public static Singleton2 getInstance(){
        if (INSTANCE == null){
            // 首次访问会同步，而之后的使用没有synchronized
            synchronized (Singleton2.class){
                if (INSTANCE == null){
                    INSTANCE  = new Singleton2();
                }
            }
        }
        return INSTANCE;
    }
}
```

以上的实现特点是：

​	懒惰实例化

​	首次使用 getInstance() 才使用 synchronized 加锁，后续使用时无需加锁 

​	有隐含的，但很关键的一点：第一个 if 使用了 INSTANCE 变量，是在同步块之外

但在多线程环境下，上面的代码是有问题的，getInstance 方法对应的字节码为：

```
0: getstatic #2 // Field INSTANCE:Lcn/itcast/n5/Singleton;
3: ifnonnull 37
6: ldc #3 // class cn/itcast/n5/Singleton
8: dup
9: astore_0
10: monitorenter
11: getstatic #2 // Field INSTANCE:Lcn/itcast/n5/Singleton;
14: ifnonnull 27
17: new #3 // class cn/itcast/n5/Singleton
20: dup
21: invokespecial #4 // Method "<init>":()V
24: putstatic #2 // Field INSTANCE:Lcn/itcast/n5/Singleton;
27: aload_0
28: monitorexit
29: goto 37
32: astore_1
33: aload_0
34: monitorexit
35: aload_1
36: athrow
37: getstatic #2 // Field INSTANCE:Lcn/itcast/n5/Singleton;
40: areturn
```

其中
        17 表示创建对象，将对象引用入栈 // new Singleton
        20 表示复制一份对象引用 // 引用地址
        21 表示利用一个对象引用，调用构造方法
        24 表示利用一个对象引用，赋值给 static INSTANCE

也许 jvm 会优化为：先执行 24，再执行 21。如果两个线程 t1，t2 按如下时间序列执行：

![image-20211116214850490](\images\image-20211116214850490.png)

关键在于 0: getstatic 这行代码在 monitor 控制之外，它就像之前举例中不守规则的人，可以越过 monitor 读取 INSTANCE 变量的值

这时 t1 还未完全将构造方法执行完毕，如果在构造方法中要执行很多初始化操作，那么 t2 拿到的是将是一个未初 始化完毕的单例

对 INSTANCE 使用 volatile 修饰即可，可以禁用指令重排，但要注意在 JDK 5 以上的版本的 volatile 才会真正有效

#### double-checked locking 解决

```java
public class Singleton2 {
    private Singleton2(){

    }
    private static volatile Singleton2 INSTANCE = null;
    public static Singleton2 getInstance(){
        if (INSTANCE == null){
            // 首次访问会同步，而之后的使用没有synchronized
            synchronized (Singleton2.class){
                if (INSTANCE == null){
                    INSTANCE  = new Singleton2();
                }
            }
        }
        return INSTANCE;
    }
}
```

如上面的注释内容所示，读写 volatile 变量时会加入内存屏障（Memory Barrier（Memory Fence）），保证下面 两点：

可见性 写屏障（sfence）保证在该屏障之前的 t1 对共享变量的改动，都同步到主存当中 而读屏障（lfence）保证在该屏障之后 t2 对共享变量的读取，加载的是主存中最新数据

有序性 写屏障会确保指令重排序时，不会将写屏障之前的代码排在写屏障之后 读屏障会确保指令重排序时，不会将读屏障之后的代码排在读屏障之前

更底层是读写变量时使用 lock 指令来多核 CPU 之间的可见性与有序性

![image-20211116215215526](\images\image-20211116215215526.png)

# 六、共享模型之无锁

## 1、问题提出

有如下需求，保证 account.withdraw 取款方法的线程安全

```java
package com.harry.thread;

import java.util.ArrayList;
import java.util.List;


interface Account2 {
    // 获取余额
    Integer getBalance();
    // 取款
    void withdraw(Integer amount);
    /**
     * 方法内会启动 1000 个线程，每个线程做 -10 元 的操作
     * 如果初始余额为 10000 那么正确的结果应当是 0
     */
    static void demo(Account2 account) {
        List<Thread> ts = new ArrayList<>();
        long start = System.nanoTime();
        for (int i = 0; i < 1000; i++) {
            ts.add(new Thread(() -> {
                account.withdraw(10);
            }));
        }
        ts.forEach(Thread::start);
        ts.forEach(t -> {
            try {
                t.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });
        long end = System.nanoTime();
        System.out.println(account.getBalance()
                + " cost: " + (end-start)/1000_000 + " ms");
    }

}
```

```java
package com.harry.thread;

public class AccountUnsafe implements Account2{
    private Integer balance;
    public AccountUnsafe(Integer balance) {
        this.balance = balance;
    }
    @Override
    public Integer getBalance() {
        return balance;
    }

    @Override
    public void withdraw(Integer amount) {
        balance -=amount;
    }
    public static void main(String[] args){
        Account2.demo(new AccountUnsafe(10000));
    }
}
```

执行结果：

230 cost: 189 ms

### 为什么不安全

withdraw 方法对应字节码

```
ALOAD 0 // <- this
ALOAD 0
GETFIELD cn/itcast/AccountUnsafe.balance : Ljava/lang/Integer; // <- this.balance
INVOKEVIRTUAL java/lang/Integer.intValue ()I // 拆箱
ALOAD 1 // <- amount
INVOKEVIRTUAL java/lang/Integer.intValue ()I // 拆箱
ISUB // 减法
INVOKESTATIC java/lang/Integer.valueOf (I)Ljava/lang/Integer; // 结果装箱
PUTFIELD cn/itcast/AccountUnsafe.balance : Ljava/lang/Integer; // -> this.balance
```

多线程执行流程

```
ALOAD 0 // thread-0 <- this
ALOAD 0
GETFIELD cn/itcast/AccountUnsafe.balance // thread-0 <- this.balance
INVOKEVIRTUAL java/lang/Integer.intValue // thread-0 拆箱
ALOAD 1 // thread-0 <- amount
INVOKEVIRTUAL java/lang/Integer.intValue // thread-0 拆箱
ISUB // thread-0 减法
INVOKESTATIC java/lang/Integer.valueOf // thread-0 结果装箱
PUTFIELD cn/itcast/AccountUnsafe.balance // thread-0 -> this.balance 


ALOAD 0 // thread-1 <- this 
ALOAD 0
GETFIELD cn/itcast/AccountUnsafe.balance // thread-1 <- this.balance 
INVOKEVIRTUAL java/lang/Integer.intValue // thread-1 拆箱
ALOAD 1 // thread-1 <- amount 
INVOKEVIRTUAL java/lang/Integer.intValue // thread-1 拆箱
ISUB // thread-1 减法
INVOKESTATIC java/lang/Integer.valueOf // thread-1 结果装箱
PUTFIELD cn/itcast/AccountUnsafe.balance // thread-1 -> this.balance 
```

单核的指令交错 多核的指令交错

### 解决思路-锁

首先想到的是给 Account 对象加锁

```java
@Override
public synchronized Integer getBalance() {
    return balance;
}

@Override
public synchronized void withdraw(Integer amount) {
    balance -=amount;
}
public static void main(String[] args){
    Account2.demo(new AccountUnsafe(10000));
}
```

### 解决思路-无锁

```java
public class AccountUnsafe implements Account2{
    private AtomicInteger balance;

    public AccountUnsafe(Integer balance) {
        this.balance = new AtomicInteger(balance);
    }
    @Override
    public synchronized Integer getBalance() {
        return balance.get();
    }

    @Override
    public synchronized void withdraw(Integer amount) {
        while (true){
            int prev = balance.get();
            int next = prev - amount;
            if (balance.compareAndSet(prev, next)){
                break;
            };
        }
        // 可以简化为下面的方法
        // balance.addAndGet(-1 * amount)
    }
    public static void main(String[] args){
        Account2.demo(new AccountUnsafe(10000));
    }
}
```

## 2、CAS与volatile

前面看到的 AtomicInteger 的解决方法，内部并没有用锁来保护共享变量的线程安全。那么它是如何实现的呢

```java
@Override
public synchronized void withdraw(Integer amount) {
    // 需要不断尝试，直到成功为止
    while (true){
        // 比如拿到了旧值 1000
        int prev = balance.get();
        // 在这个基础上 1000-10 = 990
        int next = prev - amount;
        /*
             compareAndSet 正是做这个检查，在 set 前，先比较 prev 与当前值
             - 不一致了，next 作废，返回 false 表示失败
             比如，别的线程已经做了减法，当前值已经被减成了 990
             那么本线程的这次 990 就作废了，进入 while 下次循环重试
             - 一致，以 next 设置为新值，返回 true 表示成功
         */
        if (balance.compareAndSet(prev, next)){
            break;
        };
    }
    // 可以简化为下面的方法
    // balance.addAndGet(-1 * amount)
}
```

其中的关键是 compareAndSet，它的简称就是 CAS （也有 Compare And Swap 的说法），它必须是原子操作

![image-20211122200616729](\images\image-20211122200616729.png)

注意 其实 CAS 的底层是 lock cmpxchg 指令（X86 架构），在单核 CPU 和多核 CPU 下都能够保证【比较-交 换】的原子性。在多核状态下，某个核执行到带 lock 的指令时，CPU 会让总线锁住，当这个核把此指令执行完毕，再 开启总线。这个过程中不会被线程的调度机制所打断，保证了多个线程对内存操作的准确性，是原子的。

慢动作分析

```java
@Slf4j
public class SlowMotion {
    public static void main(String[] args) {
        AtomicInteger balance = new AtomicInteger(10000);
        int mainPrev = balance.get();
        log.debug("try get {}", mainPrev);
        new Thread(() -> {
            sleep(1000);
            int prev = balance.get();
            balance.compareAndSet(prev, 9000);
            log.debug(balance.toString());
        }, "t1").start();
        sleep(2000);
        log.debug("try set 8000...");
        boolean isSuccess = balance.compareAndSet(mainPrev, 8000);
        log.debug("is success ? {}", isSuccess);
        if(!isSuccess){
            mainPrev = balance.get();
            log.debug("try set 8000...");
            isSuccess = balance.compareAndSet(mainPrev, 8000);
            log.debug("is success ? {}", isSuccess);
        }
    }
    private static void sleep(int millis) {
        try {
            Thread.sleep(millis);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

```
20:09:06 [main] c.slow - try get 10000
20:09:07 [t1] c.slow - 9000
20:09:08 [main] c.slow - try set 8000...
20:09:08 [main] c.slow - is success ? false
20:09:08 [main] c.slow - try set 8000...
20:09:08 [main] c.slow - is success ? true

Process finished with exit code 0
```

### volatile

获取共享变量时，为了保证该变量的可见性，需要使用 volatile 修饰。

它可以用来修饰成员变量和静态成员变量，他可以避免线程从自己的工作缓存中查找变量的值，必须到主存中获取 它的值，线程操作 volatile 变量都是直接操作主存。即一个线程对 volatile 变量的修改，对另一个线程可见。

注意 volatile 仅仅保证了共享变量的可见性，让其它线程能够看到最新值，但不能解决指令交错问题（不能保证原 子性）

CAS 必须借助 volatile 才能读取到共享变量的最新值来实现【比较并交换】的效果

### 为什么无锁效率高

无锁情况下，即使重试失败，线程始终在高速运行，没有停歇，而 synchronized 会让线程在没有获得锁的时候，发生上下文切换，进入阻塞。

但无锁情况下，因为线程要保持运行，需要额外 CPU 的支持，CPU 在这里就好比高速跑道，没有额外的跑道，线程想高速运行也无从谈起，虽然不会进入阻塞，但由于没有分到时间片，仍然会进入可运行状态，还是会导致上下文切换。

![image-20211122201702247](\images\image-20211122201702247.png)

### CAS 的特点

结合 CAS 和 volatile 可以实现无锁并发，适用于线程数少、多核 CPU 的场景下

CAS 是基于乐观锁的思想：最乐观的估计，不怕别的线程来修改共享变量，就算改了也没关系，我吃亏点再 重试呗

synchronized 是基于悲观锁的思想：最悲观的估计，得防着其它线程来修改共享变量，我上了锁你们都别想 改，我改完了解开锁，你们才有机会。

CAS 体现的是无锁并发、无阻塞并发，请仔细体会这两句话的意思 因为没有使用 synchronized，所以线程不会陷入阻塞，这是效率提升的因素之一 但如果竞争激烈，可以想到重试必然频繁发生，反而效率会受影响

## 3、原子整数

J.U.C 并发包提供了：

​	AtomicBoolean 

​	AtomicInteger 

​	AtomicLong

 以 AtomicInteger 为例

```java
AtomicInteger i = new AtomicInteger(0);
// 获取并自增（i = 0, 结果 i = 1, 返回 0），类似于 i++
System.out.println(i.getAndIncrement());
// 自增并获取（i = 1, 结果 i = 2, 返回 2），类似于 ++i
System.out.println(i.incrementAndGet());
// 自减并获取（i = 2, 结果 i = 1, 返回 1），类似于 --i
System.out.println(i.decrementAndGet());
// 获取并自减（i = 1, 结果 i = 0, 返回 1），类似于 i--
System.out.println(i.getAndDecrement());
// 获取并加值（i = 0, 结果 i = 5, 返回 0）
System.out.println(i.getAndAdd(5));
// 加值并获取（i = 5, 结果 i = 0, 返回 0）
System.out.println(i.addAndGet(-5));
// 获取并更新（i = 0, p 为 i 的当前值, 结果 i = -2, 返回 0）
// 其中函数中的操作能保证原子，但函数需要无副作用
System.out.println(i.getAndUpdate(p -> p - 2));
// 更新并获取（i = -2, p 为 i 的当前值, 结果 i = 0, 返回 0）
// 其中函数中的操作能保证原子，但函数需要无副作用
System.out.println(i.updateAndGet(p -> p + 2));
// 获取并计算（i = 0, p 为 i 的当前值, x 为参数1, 结果 i = 10, 返回 0）
// 其中函数中的操作能保证原子，但函数需要无副作用
// getAndUpdate 如果在 lambda 中引用了外部的局部变量，要保证该局部变量是 final 的
// getAndAccumulate 可以通过 参数1 来引用外部的局部变量，但因为其不在 lambda 中因此不必是 final
System.out.println(i.getAndAccumulate(10, (p, x) -> p + x));
// 计算并获取（i = 10, p 为 i 的当前值, x 为参数1, 结果 i = 0, 返回 0）
// 其中函数中的操作能保证原子，但函数需要无副作用
System.out.println(i.accumulateAndGet(-10, (p, x) -> p + x));
```

## 4、原子引用

AtomicReference 

AtomicMarkableReference 

AtomicStampedReference 

有如下方法

```java
package com.harry.thread;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

public interface DecimalAccount {
    // 获取余额
    BigDecimal getBalance();
    // 取款
    void withdraw(BigDecimal amount);
    /**
     * 方法内会启动 1000 个线程，每个线程做 -10 元 的操作
     * 如果初始余额为 10000 那么正确的结果应当是 0
     */
    static void demo(DecimalAccount account) {
        List<Thread> ts = new ArrayList<>();
        for (int i = 0; i < 1000; i++) {
            ts.add(new Thread(() -> {
                account.withdraw(BigDecimal.TEN);
            }));
        }
        ts.forEach(Thread::start);
        ts.forEach(t -> {
            try {
                t.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });
        System.out.println(account.getBalance());
    }

}
```

安全实现-使用 CAS

```java
package com.harry.thread;

import java.math.BigDecimal;
import java.util.concurrent.atomic.AtomicReference;

public class DecimalAccountSafeCas implements DecimalAccount {
    AtomicReference<BigDecimal> ref;
    public DecimalAccountSafeCas(BigDecimal balance) {
        ref = new AtomicReference<>(balance);
    }
    public BigDecimal getBalance() {
        return ref.get();
    }
    @Override
    public void withdraw(BigDecimal amount) {
        while (true) {
            BigDecimal prev = ref.get();
            BigDecimal next = prev.subtract(amount);
            if (ref.compareAndSet(prev, next)) {
                break;
            }
        }
    }
}


```

### ABA 问题及解决

```java
import static java.lang.Thread.sleep;
@Slf4j(topic = "c.test")
public class Aba {
    static AtomicReference<String> ref = new AtomicReference<>("A");
    public static void main(String[] args) throws InterruptedException {
        log.debug("main start...");
        // 获取值 A
        // 这个共享变量被它线程修改过？
        String prev = ref.get();
        other();
        sleep(1000);
        // 尝试改为 C
        log.debug("change A->C {}", ref.compareAndSet(prev, "C"));
    }
    private static void other() throws InterruptedException {
        new Thread(() -> {
            log.debug("change A->B {}", ref.compareAndSet(ref.get(), "B"));
        }, "t1").start();
        sleep(500);
        new Thread(() -> {
            log.debug("change B->A {}", ref.compareAndSet(ref.get(), "A"));
        }, "t2").start();
    }
}
```

20:54:29 [main] c.test - main start...
20:54:29 [t1] c.test - change A->B true
20:54:30 [t2] c.test - change B->A true
20:54:31 [main] c.test - change A->C true

主线程仅能判断出共享变量的值与最初值 A 是否相同，不能感知到这种从 A 改为 B 又 改回 A 的情况，如果主线程 希望：只要有其它线程【动过了】共享变量，那么自己的 cas 就算失败，这时，仅比较值是不够的，需要再加一个版本号

### AtomicStampedReference

```java
package com.harry.thread;

import lombok.extern.slf4j.Slf4j;

import java.util.concurrent.atomic.AtomicReference;
import java.util.concurrent.atomic.AtomicStampedReference;

import static java.lang.Thread.sleep;
@Slf4j(topic = "c.test")
public class Aba {
    static AtomicStampedReference<String> ref  = new AtomicStampedReference<>("A", 0);
    public static void main(String[] args) throws InterruptedException {
        log.debug("main start...");
        // 获取值 A
        String prev = ref.getReference();
        // 获取版本号
        int stamp = ref.getStamp();
        log.debug("版本 {}", stamp);
        // 如果中间有其它线程干扰，发生了 ABA 现象
        other();
        sleep(1000);
        // 尝试改为 C
        log.debug("change A->C {}", ref.compareAndSet(prev, "C", stamp, stamp + 1));
    }
    private static void other() throws InterruptedException {
        new Thread(() -> {
            log.debug("change A->B {}", ref.compareAndSet(ref.getReference(), "B",
                    ref.getStamp(), ref.getStamp() + 1));
            log.debug("更新版本为 {}", ref.getStamp());
        }, "t1").start();
        sleep(500);
        new Thread(() -> {
            log.debug("change B->A {}", ref.compareAndSet(ref.getReference(), "A",
                    ref.getStamp(), ref.getStamp() + 1));
            log.debug("更新版本为 {}", ref.getStamp());
        }, "t2").start();

    }
}
```

```
20:59:19 [main] c.test - main start...
20:59:19 [main] c.test - 版本 0
20:59:19 [t1] c.test - change A->B true
20:59:19 [t1] c.test - 更新版本为 1
20:59:20 [t2] c.test - change B->A true
20:59:20 [t2] c.test - 更新版本为 2
20:59:21 [main] c.test - change A->C false

Process finished with exit code 0
```

AtomicStampedReference 可以给原子引用加上版本号，追踪原子引用整个的变化过程，如： A -> B -> A -> C ，通过AtomicStampedReference，我们可以知道，引用变量中途被更改了几次。

但是有时候，并不关心引用变量更改了几次，只是单纯的关心是否更改过，所以就有了 AtomicMarkableReference

### AtomicMarkableReference

```java
public class GarbageBag {
    String desc;
    public GarbageBag(String desc) {
        this.desc = desc;
    }
    public void setDesc(String desc) {
        this.desc = desc; 
    }
    @Override
    public String toString() {
        return super.toString() + " " + desc;
    }

}
```

```java
@Slf4j
public class TestABAAtomicMarkableReference {
    public static void main(String[] args) throws InterruptedException {
        GarbageBag bag = new GarbageBag("装满了垃圾");
        // 参数2 mark 可以看作一个标记，表示垃圾袋满了
        AtomicMarkableReference<GarbageBag> ref = new AtomicMarkableReference<>(bag, true);
        log.debug("主线程 start...");
        GarbageBag prev = ref.getReference();
        log.debug(prev.toString());
        new Thread(() -> {
            log.debug("打扫卫生的线程 start...");
            bag.setDesc("空垃圾袋");
            while (!ref.compareAndSet(bag, bag, true, false)) {}
            log.debug(bag.toString());
        }).start();
        Thread.sleep(1000);
        log.debug("主线程想换一只新垃圾袋？");
        boolean success = ref.compareAndSet(prev, new GarbageBag("空垃圾袋"), true, false);
        log.debug("换了么？" + success);
        log.debug(ref.getReference().toString());
    }
}
```

```
21:04:51 [Thread-0] c.test - 打扫卫生的线程 start...
21:04:51 [Thread-0] c.test - com.harry.thread.GarbageBag@2280cdac 空垃圾袋
21:04:52 [main] c.test - 主线程想换一只新垃圾袋？
21:04:52 [main] c.test - 换了么？false
21:04:52 [main] c.test - com.harry.thread.GarbageBag@2280cdac 空垃圾袋
```

## 5、原子数组

AtomicIntegerArray 

AtomicLongArray 

AtomicReferenceArray

有如下方法

```java
    /**
     参数1，提供数组、可以是线程不安全数组或线程安全数组
     参数2，获取数组长度的方法
     参数3，自增方法，回传 array, index
     参数4，打印数组的方法
     */
// supplier 提供者 无中生有 ()->结果
// function 函数 一个参数一个结果 (参数)->结果 , BiFunction (参数1,参数2)->结果
// consumer 消费者 一个参数没结果 (参数)->void, BiConsumer (参数1,参数2)->
    private static <T> void demo(
            Supplier<T> arraySupplier,
            Function<T, Integer> lengthFun,
            BiConsumer<T, Integer> putConsumer,
            Consumer<T> printConsumer ) {
        List<Thread> ts = new ArrayList<>();
        T array = arraySupplier.get();
        int length = lengthFun.apply(array);
        for (int i = 0; i < length; i++) {
            // 每个线程对数组作 10000 次操作
            ts.add(new Thread(() -> {
                for (int j = 0; j < 10000; j++) {
                    putConsumer.accept(array, j%length);
                }
            }));
        }
        ts.forEach(t -> t.start()); // 启动所有线程
        ts.forEach(t -> {
            try {
                t.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }); // 等所有线程结束
        printConsumer.accept(array);
    }
```

### 不安全的数组

```java
   demo(
		()->new int[10],
        (array)->array.length,
        (array, index) -> array[index]++,
  		array-> System.out.println(Arrays.toString(array))
      );
```

### 安全的数组

```java
demo(
        ()-> new AtomicIntegerArray(10),
        (array) -> array.length(),
        (array, index) -> array.getAndIncrement(index),
        array -> System.out.println(array)
);
```

## 6、字段更新器

AtomicReferenceFieldUpdater // 域 字段 

AtomicIntegerFieldUpdater

AtomicLongFieldUpdater

利用字段更新器，可以针对对象的某个域（Field）进行原子操作，只能配合 volatile 修饰的字段使用，否则会出现 异常

```
Exception in thread "main" java.lang.IllegalArgumentException: Must be volatile type
```

```java
public class Test6 {
    private volatile int field;

    public static void main(String [] args){
        AtomicIntegerFieldUpdater fieldUpdater = AtomicIntegerFieldUpdater.newUpdater(Test6.class, "field");
        Test6 test6 = new Test6();
        fieldUpdater.compareAndSet(test6, 0, 10);
        // 修改成功 field = 10
        System.out.println(test6.field);
        // 修改成功 field = 20
        fieldUpdater.compareAndSet(test6, 10, 20);
        System.out.println(test6.field);
        // 修改失败 field = 20
        fieldUpdater.compareAndSet(test6, 10, 30);
        System.out.println(test6.field);
    }
}
```

## 7、原子累加器

### 累加器性能比较

```java
private static <T> void demo(Supplier<T> adderSupplier, Consumer<T> action) {
    T adder = adderSupplier.get();
    long start = System.nanoTime();
    List<Thread> ts = new ArrayList<>();
    // 4 个线程，每人累加 50 万
    for (int i = 0; i < 40; i++) {
        ts.add(new Thread(() -> {
            for (int j = 0; j < 500000; j++) {
                action.accept(adder);
            }
        }));
    }
    ts.forEach(t -> t.start());
    ts.forEach(t -> {
        try {
            t.join();
        } catch (InterruptedException e) {
            e.printStackTrace();}
    });
    long end = System.nanoTime();
    System.out.println(adder + " cost:" + (end - start)/1000_000);
}
```

比较 AtomicLong 与 LongAdder

```java
for (int i = 0; i < 5; i++) {
    demo(() -> new LongAdder(), adder -> adder.increment());
}
for (int i = 0; i < 5; i++) {
    demo(() -> new AtomicLong(), adder -> adder.getAndIncrement());
}
```

输出

```
20000000 cost:49
20000000 cost:51
20000000 cost:38
20000000 cost:37
20000000 cost:38

20000000 cost:357
20000000 cost:342
20000000 cost:305
20000000 cost:315
20000000 cost:299
```

性能提升的原因很简单，就是在有竞争时，设置多个累加单元，Therad-0 累加 Cell[0]，而 Thread-1 累加 Cell[1]... 最后将结果汇总。这样它们在累加时操作的不同的 Cell 变量，因此减少了 CAS 重试失败，从而提高性 能。

### 源码之 LongAdde

LongAdder 类有几个关键域

```java
// 累加单元数组, 懒惰初始化
transient volatile Cell[] cells;
// 基础值, 如果没有竞争, 则用 cas 累加这个域
transient volatile long base;
// 在 cells 创建或扩容时, 置为 1, 表示加锁
transient volatile int cellsBusy;

// 不要用于实践！！！
@Slf4j(topic = "c.test")
public class LockCas {
    private AtomicInteger state = new AtomicInteger(0);
    public void lock() {
        while (true) {
            if (state.compareAndSet(0, 1)) {
                break;
            }
        }
    }
    public void unlock() {
        log.debug("unlock...");
        state.set(0);
    }
}
```

```java
LockCas lock = new LockCas();
new Thread(() -> {
    log.debug("begin...");
    lock.lock();
    try {
        log.debug("lock...");
        sleep(1);
    } finally {
        lock.unlock();
    }
}).start();
new Thread(() -> {
    log.debug("begin...");
    lock.lock();
    try {
        log.debug("lock...");
    } finally {
        lock.unlock();
    }
}).start();
```

### 原理之伪共享

其中 Cell 即为累加单元

```java
// 防止缓存行伪共享
@sun.misc.Contended
static final class Cell {
    volatile long value;
    Cell(long x) { value = x; }

    // 最重要的方法, 用来 cas 方式进行累加, prev 表示旧值, next 表示新值
    final boolean cas(long prev, long next) {
        return UNSAFE.compareAndSwapLong(this, valueOffset, prev, next);
    }
    // 省略不重要代码
}
```

缓存与内存的速度比较

![image-20211123201422768](\images\image-20211123201422768.png)

因为 CPU 与 内存的速度差异很大，需要靠预读数据至缓存来提升效率。 而缓存以缓存行为单位，每个缓存行对应着一块内存，一般是 64 byte（8 个 long） 缓存的加入会造成数据副本的产生，即同一份数据会缓存在不同核心的缓存行中 CPU 要保证数据的一致性，如果某个 CPU 核心更改了数据，其它 CPU 核心对应的整个缓存行必须失效

![image-20211123201453766](\images\image-20211123201453766.png)

因为 Cell 是数组形式，在内存中是连续存储的，一个 Cell 为 24 字节（16 字节的对象头和 8 字节的 value），因 此缓存行可以存下 2 个的 Cell 对象。这样问题来了：

​	 Core-0 要修改 Cell[0]

​	 Core-1 要修改 Cell[1]

无论谁修改成功，都会导致对方 Core 的缓存行失效，比如 Core-0 中 Cell[0]=6000, Cell[1]=8000 要累加 Cell[0]=6001, Cell[1]=8000 ，这时会让 Core-1 的缓存行失效

@sun.misc.Contended 用来解决这个问题，它的原理是在使用此注解的对象或字段的前后各增加 128 字节大小的 padding，从而让 CPU 将对象预读至缓存时占用不同的缓存行，这样，不会造成对方缓存行的失效

![image-20211123201723292](\images\image-20211123201723292.png)

累加主要调用下面的方法

```java
public void add(long x) {
    // as 为累加单元数组
    // b 为基础值
    // x 为累加值
    Cell[] as; long b, v; int m; Cell a;
    // 进入 if 的两个条件
    // 1. as 有值, 表示已经发生过竞争, 进入 if
    // 2. cas 给 base 累加时失败了, 表示 base 发生了竞争, 进入 if
    if ((as = cells) != null || !casBase(b = base, b + x)) {
        // uncontended 表示 cell 没有竞争
        boolean uncontended = true;
        if ( // as 还没有创建
                as == null || (m = as.length - 1) < 0 ||
                        // 当前线程对应的 cell 还没有
                        (a = as[getProbe() & m]) == null ||
                   // cas 给当前线程的 cell 累加失败 uncontended=false ( a 为当前线程的 cell )
                        !(uncontended = a.cas(v = a.value, v + x))
        ) {
            // 进入 cell 数组创建、cell 创建的流程
            longAccumulate(x, null, uncontended);
        }
    }
}
```

add 流程图

![image-20211123201915246](\images\image-20211123201915246.png)

```java
final void longAccumulate(long x, LongBinaryOperator fn,
                          boolean wasUncontended) {
    int h;
    // 当前线程还没有对应的 cell, 需要随机生成一个 h 值用来将当前线程绑定到 cell
    if ((h = getProbe()) == 0) {
        // 初始化 probe
        ThreadLocalRandom.current();
        // h 对应新的 probe 值, 用来对应 cell
        h = getProbe();
        wasUncontended = true;
    }
    // collide 为 true 表示需要扩容
    boolean collide = false;
    for (;;) {
        Cell[] as; Cell a; int n; long v;
        // 已经有了 cells
        if ((as = cells) != null && (n = as.length) > 0) {
            // 还没有 cell
            if ((a = as[(n - 1) & h]) == null) {
                // 为 cellsBusy 加锁, 创建 cell, cell 的初始累加值为 x
                // 成功则 break, 否则继续 continue 循环
            }
            // 有竞争, 改变线程对应的 cell 来重试 cas
            else if (!wasUncontended)
                wasUncontended = true;
                // cas 尝试累加, fn 配合 LongAccumulator 不为 null, 配合 LongAdder 为 null
            else if (a.cas(v = a.value, ((fn == null) ? v + x : fn.applyAsLong(v, x))))
                break;
                // 如果 cells 长度已经超过了最大长度, 或者已经扩容, 改变线程对应的 cell 来重试 cas
            else if (n >= NCPU || cells != as)
                collide = false;
                // 确保 collide 为 false 进入此分支, 就不会进入下面的 else if 进行扩容了
            else if (!collide)
                collide = true;
                // 加锁
            else if (cellsBusy == 0 && casCellsBusy()) {
                // 加锁成功, 扩容
                continue;
            }
            // 改变线程对应的 cell
            h = advanceProbe(h);
        }
        // 还没有 cells, 尝试给 cellsBusy 加锁
        else if (cellsBusy == 0 && cells == as && casCellsBusy()) {
            // 加锁成功, 初始化 cells, 最开始长度为 2, 并填充一个 cell
            // 成功则 break;
        }
        // 上两种情况失败, 尝试给 base 累加
        else if (casBase(v = base, ((fn == null) ? v + x : fn.applyAsLong(v, x))))
            break;
    }
}
```

longAccumulate 流程图

![image-20211123202101442](\images\image-20211123202101442.png)

![image-20211123202121329](\images\image-20211123202121329.png)

获取最终结果通过 sum 方



```java
public long sum() {
    Cell[] as = cells; Cell a;
    long sum = base;
    if (as != null) {
        for (int i = 0; i < as.length; ++i) {
            if ((a = as[i]) != null)
                sum += a.value;
        }
    }
    return sum;
}
```

## 8、Unsafe

### 概述

Unsafe 对象提供了非常底层的，操作内存、线程的方法，Unsafe 对象不能直接调用，只能通过反射获得

```java
public class UnsafeAccessor {
    static Unsafe unsafe;
    static {
        try {
            Field theUnsafe = Unsafe.class.getDeclaredField("theUnsafe");
            theUnsafe.setAccessible(true);
            unsafe = (Unsafe) theUnsafe.get(null);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            throw new Error(e);
        }
    }
    static Unsafe getUnsafe() {
        return unsafe;
    }

}
```

Unsafe CAS 操作

```java
@Data
class Student {
    volatile int id;
    volatile String name;
}
```

```java
public static void main(String[] args) throws NoSuchFieldException {
    Unsafe unsafe = UnsafeAccessor.getUnsafe();
    Field id = Student.class.getDeclaredField("id");
    Field name = Student.class.getDeclaredField("name");
    // 获得成员变量的偏移量
    long idOffset = UnsafeAccessor.unsafe.objectFieldOffset(id);
    long nameOffset = UnsafeAccessor.unsafe.objectFieldOffset(name);
    Student student = new Student();
    // 使用 cas 方法替换成员变量的值
    UnsafeAccessor.unsafe.compareAndSwapInt(student, idOffset, 0, 20); // 返回 true
    UnsafeAccessor.unsafe.compareAndSwapObject(student, nameOffset, null, "张三"); // 返回 true
    System.out.println(student);

}
```

# 七、共享模型之不可变

## 1、日期转换的问题

### 问题提出

下面的代码在运行时，由于 SimpleDateFormat 不是线程安全的

```java
@Slf4j(topic = "c1.test")
public class TestSimpleDate {
    public static void main(String[] args) {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        for (int i = 0; i < 10; i++) {
            new Thread(() -> {
                try {
                    log.debug("{}", sdf.parse("1951-04-21"));
                } catch (Exception e) {
                    log.error("{}", e);
                }
            }).start();
        }
    }
}
```

有很大几率出现 java.lang.NumberFormatException 或者出现不正确的日期解析结果，例如：

```
19:45:43 [Thread-3] c.test - {}
java.lang.NumberFormatException: multiple points
	at sun.misc.FloatingDecimal.readJavaFormatString(FloatingDecimal.java:1890)
	at sun.misc.FloatingDecimal.parseDouble(FloatingDecimal.java:110)
	at java.lang.Double.parseDouble(Double.java:538)
	at java.text.DigitList.getDouble(DigitList.java:169)
	at java.text.DecimalFormat.parse(DecimalFormat.java:2089)
	at java.text.SimpleDateFormat.subParse(SimpleDateFormat.java:1869)
	at java.text.SimpleDateFormat.parse(SimpleDateFormat.java:1514)
	at java.text.DateFormat.parse(DateFormat.java:364)
	at com.harry.thread.TestSimpleDate.lambda$main$0(TestSimpleDate.java:14)
	at java.lang.Thread.run(Thread.java:748)
19:45:43 [Thread-4] c.test - {}
java.lang.NumberFormatException: multiple points
	at sun.misc.FloatingDecimal.readJavaFormatString(FloatingDecimal.java:1890)
	at sun.misc.FloatingDecimal.parseDouble(FloatingDecimal.java:110)
	at java.lang.Double.parseDouble(Double.java:538)
	at java.text.DigitList.getDouble(DigitList.java:169)
	at java.text.DecimalFormat.parse(DecimalFormat.java:2089)
	at java.text.SimpleDateFormat.subParse(SimpleDateFormat.java:1869)
	at java.text.SimpleDateFormat.parse(SimpleDateFormat.java:1514)
	at java.text.DateFormat.parse(DateFormat.java:364)
	at com.harry.thread.TestSimpleDate.lambda$main$0(TestSimpleDate.java:14)
	at java.lang.Thread.run(Thread.java:748)
19:45:43 [Thread-1] c.test - {}
java.lang.NumberFormatException: multiple points
	at sun.misc.FloatingDecimal.readJavaFormatString(FloatingDecimal.java:1890)
	at sun.misc.FloatingDecimal.parseDouble(FloatingDecimal.java:110)
	at java.lang.Double.parseDouble(Double.java:538)
	at java.text.DigitList.getDouble(DigitList.java:169)
	at java.text.DecimalFormat.parse(DecimalFormat.java:2089)
	at java.text.SimpleDateFormat.subParse(SimpleDateFormat.java:1869)
	at java.text.SimpleDateFormat.parse(SimpleDateFormat.java:1514)
	at java.text.DateFormat.parse(DateFormat.java:364)
	at com.harry.thread.TestSimpleDate.lambda$main$0(TestSimpleDate.java:14)
	at java.lang.Thread.run(Thread.java:748)
```

### 思路-同步锁

这样虽能解决问题，但带来的是性能上的损失，并不算很好：

```java
@Slf4j(topic = "c.test")
public class TestSimpleDate {
    public static void main(String[] args) {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        for (int i = 0; i < 10; i++) {
            new Thread(() -> {
                synchronized (sdf) {
                    try {
                        log.debug("{}", sdf.parse("1951-04-21"));
                    } catch (Exception e) {
                        log.error("{}", e);
                    }
                }
            }).start();
        }
    }
}
```

### 思路 - 不可变

如果一个对象在不能够修改其内部状态（属性），那么它就是线程安全的，因为不存在并发修改啊！这样的对象在 Java 中有很多，例如在 Java 8 后，提供了一个新的日期格式化类：

```java
@Slf4j(topic = "c.test")
public class TestSimpleDate {
    public static void main(String[] args) {
        DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        for (int i = 0; i < 10; i++) {
            new Thread(() -> {
                LocalDate date = dtf.parse("2018-10-01", LocalDate::from);
                log.debug("{}", date);
            }).start();
        }
    }
}
```

## 2、不可变设计

另一个 String 类也是不可变的，以它为例，说明一下不可变设计的要素

```java
public final class String
        implements java.io.Serializable, Comparable<String>, CharSequence {
    /** The value is used for character storage. */
    private final char value[];
    /** Cache the hash code for the string */
    private int hash; // Default to 0

    // ...

}
```

### final 的使用

发现该类、类中所有属性都是 final 的，属性用 final 修饰保证了该属性是只读的，不能修改类用 final 修饰保证了该类中的方法不能被覆盖，防止子类无意间破坏不可变性

### 保护性拷贝

使用字符串时，也有一些跟修改相关的方法啊，比如 substring 等，那么下面就看一看这些方法是 如何实现的，就以 substring 为例：

```java
public String substring(int beginIndex) {
    if (beginIndex < 0) {
        throw new StringIndexOutOfBoundsException(beginIndex);
    }
    int subLen = value.length - beginIndex;
    if (subLen < 0) {
        throw new StringIndexOutOfBoundsException(subLen);
    }
    return (beginIndex == 0) ? this : new String(value, beginIndex, subLen);
}
```

发现其内部是调用 String 的构造方法创建了一个新字符串，再进入这个构造看看，是否对 final char[] value 做出 了修改：

```java
public String(char value[], int offset, int count) {
    if (offset < 0) {
        throw new StringIndexOutOfBoundsException(offset);
    }
    if (count <= 0) {
        if (count < 0) {
            throw new StringIndexOutOfBoundsException(count);
        }
        if (offset <= value.length) {
            this.value = "".value;
            return;
        }
    }
    if (offset > value.length - count) {
        throw new StringIndexOutOfBoundsException(offset + count);
    }
    this.value = Arrays.copyOfRange(value, offset, offset+count);
}
```

结果发现也没有，构造新字符串对象时，会生成新的 char[] value，对内容进行复制 。这种通过创建副本对象来避 免共享的手段称之为【保护性拷贝（defensive copy）】

### 享元模式

定义 英文名称：Flyweight pattern. 当需要重用数量有限的同一类对象时 wikipedia： A flyweight is an object that minimizes memory usage by sharing as much data as possible with other similar objects

#### 体现

在JDK中 Boolean，Byte，Short，Integer，Long，Character 等包装类提供了 valueOf 方法，例如 Long 的 valueOf 会缓存 -128~127 之间的 Long 对象，在这个范围之间会重用对象，大于这个范围，才会新建 Long 对 象：

```java
public static Long valueOf(long l) {
    final int offset = 128;
    if (l >= -128 && l <= 127) { // will cache
        return LongCache.cache[(int)l + offset];
    }
    return new Long(l);
}
```

#### DIY

例如：一个线上商城应用，QPS 达到数千，如果每次都重新创建和关闭数据库连接，性能会受到极大影响。 这时 预先创建好一批连接，放入连接池。一次请求到达后，从连接池获取连接，使用完毕后再还回连接池，这样既节约 了连接的创建和关闭时间，也实现了连接的重用，不至于让庞大的连接数压垮数据库。

```java
import java.sql.*;
import java.util.Map;
import java.util.Properties;
import java.util.concurrent.Executor;
import java.util.concurrent.atomic.AtomicIntegerArray;
@Slf4j(topic = "c.test")
public class Pool {
    // 1. 连接池大小
    private final int poolSize;

    // 2. 连接对象数组
    private Connection[] connections;

    // 3. 连接状态数组0表示空闲 1表示繁忙
    private AtomicIntegerArray states;

    // 4. 构造方法初始化
    public Pool(int poolSize) {
        this.poolSize = poolSize;
        this.connections = new Connection[poolSize];
        this.states = new AtomicIntegerArray(new int[poolSize]);
        for (int i = 0; i < poolSize; i++) {
            connections[i] = new MockConnection("连接" + (i+1));
        }
    }

    // 5. 接连接
    public Connection borrow(){
        while (true){
            for (int i = 0; i < poolSize ; i++) {
                // 获取空闲连接
                if(states.get(i) == 0){
                    if (states.compareAndSet(i, 0, 1)){
                        log.debug("borrow {}", connections[i]);
                        return connections[i];
                    }
                }
            }
            // 如果没有空闲连接，当前线程进入等待
            synchronized (this) {
                try {
                    log.debug("wait...");
                    this.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }


    }
    // 6. 归还连接
    public void free(Connection conn) {
        for (int i = 0; i < poolSize; i++) {
            if (connections[i] == conn) {
                states.set(i, 0);
                synchronized (this) {
                    log.debug("free {}", conn);
                    this.notifyAll();
                }
                break;
            }
        }
    }

}
```

# 八、共享模式之工具

## 1、线程池

### 自定义线程池

![image-20211130195956720](\images\image-20211130195956720.png)

步骤1：自定义拒绝策略接口

```java
@FunctionalInterface // 拒绝策略
interface RejectPolicy<T> {
    void reject(BlockingQueue<T> queue, T task);
}
```

步骤2：自定义任务队列

```JAVA
@Slf4j(topic = "c.test")
class BlockingQueue<T>{
    //1. 任务队列
    private Deque<T> queue = new ArrayDeque<>();

    //2. 锁
    private ReentrantLock lock = new ReentrantLock();

    //3. 生产者条件变量
    private Condition fullWaitSet = lock.newCondition();

    //4. 消费者条件变量
    private Condition emptyWaitSet = lock.newCondition();
    // 5. 容量
    private int capcity;
    public BlockingQueue(int capcity) {
        this.capcity = capcity;
    }

    // 带超时阻塞获取
    public T poll(long timeout, TimeUnit unit)  {
        lock.lock();
        // 将 timeout 统一转换为 纳秒
        long nanos = unit.toNanos(timeout);
        while (queue.isEmpty()){
            if (nanos <= 0){
                return null;
            }
            try {
                nanos = emptyWaitSet.awaitNanos(nanos);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        T t = queue.removeFirst();
        fullWaitSet.signal();
        return t;
    }
    // 阻塞获取
    public T take() {
        lock.lock();
        try {
            while (queue.isEmpty()) {
                try {
                    emptyWaitSet.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            T t = queue.removeFirst();
            fullWaitSet.signal();
            return t;
        } finally {
            lock.unlock();
        }
    }
    // 阻塞添加
    public void put(T task){
        lock.lock();
        try {
            while (queue.size() == capcity) {
                try {
                    log.debug("等待加入任务队列 {} ...", task);
                    fullWaitSet.await();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            log.debug("加入任务队列 {}", task);
            queue.addLast(task);
            emptyWaitSet.signal();
        } finally {
            lock.unlock();
        }
    }
    // 带超时时间阻塞添加
    public boolean offer(T task, long timeout, TimeUnit timeUnit){
        lock.lock();
        try {
            long nanos = timeUnit.toNanos(timeout);
            while (queue.size() == capcity) {
                try {
                    if(nanos <= 0) {
                        return false;
                    }
                    log.debug("等待加入任务队列 {} ...", task);
                    nanos = fullWaitSet.awaitNanos(nanos);} 
                catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            log.debug("加入任务队列 {}", task);
            queue.addLast(task);
            emptyWaitSet.signal();
            return true;
        } finally {
            lock.unlock();
        }
    }

    public int size() {
        lock.lock();
        try {
            return queue.size();
        } finally {
            lock.unlock();
        }
    }
    public void tryPut(RejectPolicy<T> rejectPolicy, T task) {
        lock.lock();
        try {
            // 判断队列是否满
            if(queue.size() == capcity) {
                rejectPolicy.reject(this, task);
            } else { // 有空闲
                log.debug("加入任务队列 {}", task);
                queue.addLast(task);
                emptyWaitSet.signal();
            }
        } finally {
            lock.unlock();
        }
    }

}
```

测试



```java
@Slf4j(topic = "c.thread")
public class CustomizeThreadPool {
    public static void main(String[] args) {
        ThreadPool threadPool = new ThreadPool(1,
                1000, TimeUnit.MILLISECONDS, 1, (queue, task)->{
            // 1. 死等
            // queue.put(task);
            // 2) 带超时等待
            // queue.offer(task, 1500, TimeUnit.MILLISECONDS);
            // 3) 让调用者放弃任务执行
            // log.debug("放弃{}", task);
            // 4) 让调用者抛出异常
            // throw new RuntimeException("任务执行失败 " + task);
            // 5) 让调用者自己执行任务
            task.run();
        });
        for (int i = 0; i < 4; i++) {
            int j = i;
            threadPool.execute(() -> {
                try {
                    Thread.sleep(1000L);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                log.debug("{}", j);
            });
        }
    }
}
```

## 2、ThreadPoolExecutor

![image-20211201194716063](\images\image-20211201194716063.png)

### 线程池状态

ThreadPoolExecutor 使用 int 的高 3 位来表示线程池状态，低 29 位表示线程数量

![image-20211201195044718](\images\image-20211201195044718.png)

从数字上比较，TERMINATED > TIDYING > STOP > SHUTDOWN > RUNNING 

这些信息存储在一个原子变量 ctl 中，目的是将线程池状态与线程个数合二为一，这样就可以用一次 cas 原子操作 进行赋值

```java
// c 为旧值， ctlOf 返回结果为新值
ctl.compareAndSet(c, ctlOf(targetState, workerCountOf(c)))); /
// rs 为高 3 位代表线程池状态， wc 为低 29 位代表线程个数，ctl 是合并它们 
private static int ctlOf(int rs, int wc) { return rs | wc; }
```

### 构造方法

```java
public ThreadPoolExecutor(int corePoolSize,
                          int maximumPoolSize,
                          long keepAliveTime,
                          TimeUnit unit,
                          BlockingQueue<Runnable> workQueue,
                          ThreadFactory threadFactory,
                          RejectedExecutionHandler handler)
```

```
corePoolSize 核心线程数目 (最多保留的线程数)
maximumPoolSize 最大线程数目
keepAliveTime 生存时间 - 针对救急线程
unit 时间单位 - 针对救急线程
workQueue 阻塞队列
threadFactory 线程工厂 - 可以为线程创建时起个好名字
handler 拒绝策略
```

工作方式：

![image-20211201195305503](\images\image-20211201195305503.png)

线程池中刚开始没有线程，当一个任务提交给线程池后，线程池会创建一个新线程来执行任务。

当线程数达到 corePoolSize 并没有线程空闲，这时再加入任务，新加的任务会被加入workQueue 队列排 队，直到有空闲的线程。

如果队列选择了有界队列，那么任务超过了队列大小时，会创建 maximumPoolSize - corePoolSize 数目的线 程来救急。

如果线程到达 maximumPoolSize 仍然有新任务这时会执行拒绝策略。拒绝策略 jdk 提供了 4 种实现，其它 著名框架也提供了实现

​	AbortPolicy 让调用者抛出 RejectedExecutionException 异常，这是默认策略

​	CallerRunsPolicy 让调用者运行任务

​	DiscardPolicy 放弃本次任务

​	DiscardOldestPolicy 放弃队列中最早的任务，本任务取而代之

​	Dubbo 的实现，在抛出 RejectedExecutionException 异常之前会记录日志，并 dump 线程栈信息，方 便定位问题

​	Netty 的实现，是创建一个新线程来执行任务

​	ActiveMQ 的实现，带超时等待（60s）尝试放入队列，类似我们之前自定义的拒绝策

当高峰过去后，超过corePoolSize 的救急线程如果一段时间没有任务做，需要结束节省资源，这个时间由 keepAliveTime 和 unit 来控制。

![image-20211201195557337](\images\image-20211201195557337.png)

根据这个构造方法，JDK Executors 类中提供了众多工厂方法来创建各种用途的线程池

### newFixedThreadPool

```java
public static ExecutorService newFixedThreadPool(int nThreads) {
    return new ThreadPoolExecutor(nThreads, nThreads,
            0L, TimeUnit.MILLISECONDS,
            new LinkedBlockingQueue<Runnable>());
}
```

特点: 核心线程数 == 最大线程数（没有救急线程被创建），因此也无需超时时间 阻塞队列是无界的，可以放任意数量的任务,适用于任务量已知，相对耗时的任务

### newCachedThreadPool

```java
public static ExecutorService newCachedThreadPool() {
    return new ThreadPoolExecutor(0, Integer.MAX_VALUE,
            60L, TimeUnit.SECONDS,
            new SynchronousQueue<Runnable>());
}
```

特点 核心线程数是 0， 最大线程数是 Integer.MAX_VALUE，救急线程的空闲生存时间是 60s，意味着全部都是救急线程（60s 后可以回收）,救急线程可以无限创建

队列采用了 SynchronousQueue 实现特点是，它没有容量，没有线程来取是放不进去的（一手交钱、一手交 货）

```java
SynchronousQueue<Integer> integers = new SynchronousQueue<>();
new Thread(() -> {
    try {
        log.debug("putting {} ", 1);
        integers.put(1);
        log.debug("{} putted...", 1);
        log.debug("putting...{} ", 2);
        integers.put(2);
        log.debug("{} putted...", 2);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
},"t1").start();
sleep(1);
new Thread(() -> {
    try {
        log.debug("taking {}", 1);
        integers.take();
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
},"t2").start();
sleep(1);
new Thread(() -> {
    try {
        log.debug("taking {}", 2);
        integers.take();
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
},"t3").start();
```

整个线程池表现为线程数会根据任务量不断增长，没有上限，当任务执行完毕，空闲 1分钟后释放线 程。 适合任务数比较密集，但每个任务执行时间较短的情况

### newSingleThreadExecutor

```java
public static ExecutorService newSingleThreadExecutor() {
    return new FinalizableDelegatedExecutorService
            (new ThreadPoolExecutor(1, 1,
                    0L, TimeUnit.MILLISECONDS,
                    new LinkedBlockingQueue<Runnable>()));
}
```

使用场景： 希望多个任务排队执行。线程数固定为 1，任务数多于 1 时，会放入无界队列排队。任务执行完毕，这唯一的线程 也不会被释放。

区别： 自己创建一个单线程串行执行任务，如果任务执行失败而终止那么没有任何补救措施，而线程池还会新建一 个线程，保证池的正常工作

​	Executors.newSingleThreadExecutor() 线程个数始终为1，不能修改 FinalizableDelegatedExecutorService 应用的是装饰器模式，只对外暴露了 ExecutorService 接口，因 此不能调用 ThreadPoolExecutor 中特有的方法

​	Executors.newFixedThreadPool(1) 初始时为1，以后还可以修改 对外暴露的是 ThreadPoolExecutor 对象，可以强转后调用 setCorePoolSize 等方法进行修改

### 提交任务

```java
// 执行任务
void execute(Runnable command);
// 提交任务 task，用返回值 Future 获得任务执行结果
<T> Future<T> submit(Callable<T> task);
// 提交 tasks 中所有任务
<T> List<Future<T>> invokeAll(Collection<? extends Callable<T>> tasks)
        throws InterruptedException;
// 提交 tasks 中所有任务，带超时时间
<T> List<Future<T>> invokeAll(Collection<? extends Callable<T>> tasks,
                              long timeout, TimeUnit unit)
        throws InterruptedException;
// 提交 tasks 中所有任务，哪个任务先成功执行完毕，返回此任务执行结果，其它任务取消
<T> T invokeAny(Collection<? extends Callable<T>> tasks)
        throws InterruptedException, ExecutionException;
// 提交 tasks 中所有任务，哪个任务先成功执行完毕，返回此任务执行结果，其它任务取消，带超时时间
<T> T invokeAny(Collection<? extends Callable<T>> tasks,
                long timeout, TimeUnit unit)
        throws InterruptedException, ExecutionException, TimeoutException;
```

### 关闭线程池

shutdown

```java
/*
线程池状态变为 SHUTDOWN
- 不会接收新任务
- 但已提交任务会执行完
- 此方法不会阻塞调用线程的执行
*/
void shutdown();
```

```java
public void shutdown() {
    final ReentrantLock mainLock = this.mainLock;
    mainLock.lock();
    try {
        checkShutdownAccess();
        // 修改线程池状态
        advanceRunState(SHUTDOWN);
        // 仅会打断空闲线程
        interruptIdleWorkers();
        onShutdown(); // 扩展点 ScheduledThreadPoolExecutor
    } finally {
        mainLock.unlock();
    }
    // 尝试终结(没有运行的线程可以立刻终结，如果还有运行的线程也不会等)
    tryTerminate();
}
```

shutdownNow

```java
/*
线程池状态变为 STOP
- 不会接收新任务
- 会将队列中的任务返回
- 并用 interrupt 的方式中断正在执行的任务
*/
List<Runnable> shutdownNow();
```

```java
public List<Runnable> shutdownNow() {
    List<Runnable> tasks;
    final ReentrantLock mainLock = this.mainLock;
    mainLock.lock();
    try {
        checkShutdownAccess();
        // 修改线程池状态
        advanceRunState(STOP);
        // 打断所有线程
        interruptWorkers();
        // 获取队列中剩余任务
        tasks = drainQueue();
    } finally {
        mainLock.unlock();
    }
    // 尝试终结
    tryTerminate();
    return tasks;
}
```

### 其它方法

```java
// 不在 RUNNING 状态的线程池，此方法就返回 true
boolean isShutdown();
// 线程池状态是否是 TERMINATED
boolean isTerminated();
// 调用 shutdown 后，由于调用线程并不会等待所有任务运行结束，因此如果它想在线程池 TERMINATED 后做些事情，可以利用此方法等待
boolean awaitTermination(long timeout, TimeUnit unit) throws InterruptedException;
```

## 3、模式之 Worker Thread

### 定义

让有限的工作线程（Worker Thread）来轮流异步处理无限多的任务。也可以将其归类为分工模式，它的典型实现 就是线程池，也体现了经典设计模式中的享元模式。

例如，如果一个餐馆的工人既要招呼客人（任务类型A），又要到后厨做菜（任务类型B）显然效率不咋地，分成 服务员（线程池A）与厨师（线程池B）更为合理，当然你能想到更细致的分工

### 饥饿

固定大小线程池会有饥饿现象

两个工人是同一个线程池中的两个线程 他们要做的事情是：为客人点餐和到后厨做菜，这是两个阶段的工作 客人点餐：必须先点完餐，等菜做好，上菜，在此期间处理点餐的工人必须等待 后厨做菜：没啥说的，做就是了

比如工人A 处理了点餐任务，接下来它要等着 工人B 把菜做好，然后上菜，他俩也配合的蛮好

但现在同时来了两个客人，这个时候工人A 和工人B 都去处理点餐了，这时没人做饭了，饥饿

```java
package com.harry.thread;

import lombok.extern.slf4j.Slf4j;

import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

@Slf4j(topic = "c.dead")
public class TestDeadLock1 {

    static final List<String> MENU = Arrays.asList("地三鲜", "宫保鸡丁", "辣子鸡丁", "烤鸡翅");
    static Random RANDOM = new Random();
    static String cooking() {
        return MENU.get(RANDOM.nextInt(MENU.size()));
    }

    public static void main(String[] args) {
        ExecutorService executorService = Executors.newFixedThreadPool(2);
        executorService.execute(() ->{
            log.debug("处理点餐");
            Future<String> f = executorService.submit(() ->{
                log.debug("做菜");
                return cooking();
            });
            try {
                log.debug("上菜: {}", f.get());
            } catch (InterruptedException | ExecutionException e) {
                e.printStackTrace();
            }
        });

    }
}
```

输出

```
20:28:03 [pool-1-thread-1] c.dead - 处理点餐
20:28:03 [pool-1-thread-2] c.dead - 做菜
20:28:03 [pool-1-thread-1] c.dead - 上菜: 宫保鸡丁
```

还是前面提到的，不同的任务类型，采用不同的线程 池，例如：

```java
package com.harry.thread;

import lombok.extern.slf4j.Slf4j;

import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

@Slf4j(topic = "c.dead")
public class TestDeadLock1 {

    static final List<String> MENU = Arrays.asList("地三鲜", "宫保鸡丁", "辣子鸡丁", "烤鸡翅");
    static Random RANDOM = new Random();
    static String cooking() {
        return MENU.get(RANDOM.nextInt(MENU.size()));
    }

    public static void main(String[] args) {
        ExecutorService waiterPool = Executors.newFixedThreadPool(1);
        ExecutorService cookPool = Executors.newFixedThreadPool(1);

        waiterPool.execute(() ->{
            log.debug("处理点餐");
            Future<String> f = cookPool.submit(() ->{
                log.debug("做菜");
                return cooking();
            });
            try {
                log.debug("上菜: {}", f.get());
            } catch (InterruptedException | ExecutionException e) {
                e.printStackTrace();
            }
        });

        waiterPool.execute(() ->{
            log.debug("处理点餐");
            Future<String> f = cookPool.submit(() ->{
                log.debug("做菜");
                return cooking();
            });
            try {
                log.debug("上菜: {}", f.get());
            } catch (InterruptedException | ExecutionException e) {
                e.printStackTrace();
            }
        });
    }
}
```

### 创建多少线程池合适

过小会导致程序不能充分地利用系统资源、容易导致饥饿 过大会导致更多的线程上下文切换，占用更多内存

#### CPU 密集型运算

通常采用 cpu 核数 + 1 能够实现最优的 CPU 利用率，+1 是保证当线程由于页缺失故障（操作系统）或其它原因 导致暂停时，额外的这个线程就能顶上去，保证 CPU 时钟周期不被浪费

####  I/O 密集型运算

CPU 不总是处于繁忙状态，例如，当你执行业务计算时，这时候会使用 CPU 资源，但当你执行 I/O 操作时、远程 RPC 调用时，包括进行数据库操作时，这时候 CPU 就闲下来了，你可以利用多线程提高它的利用率。

经验公式如下：线程数 = 核数 * 期望 CPU 利用率 * 总时间(CPU计算时间+等待时间) / CPU 计算时间

例如 4 核 CPU 计算时间是 50% ，其它等待时间是 50%，期望 cpu 被 100% 利用，套用公式

4 * 100% * 100% / 50% = 8

例如4 核 CPU 计算时间是 10% ，其它等待时间是 90%，期望 cpu 被 100% 利用，套用公式

4 * 100% * 100% / 10% = 40

## 4、任务调度线程池

在『任务调度线程池』功能加入之前，可以使用 java.util.Timer 来实现定时功能，Timer 的优点在于简单易用，但 由于所有任务都是由同一个线程来调度，因此所有任务都是串行执行的，同一时间只能有一个任务在执行，前一个 任务的延迟或异常都将会影响到之后的任务。

```java
package com.harry.thread;

import lombok.extern.slf4j.Slf4j;

import java.util.Timer;
import java.util.TimerTask;

import static java.lang.Thread.sleep;

@Slf4j(topic = "c.test")
public class TestSchedule {
    public static void main(String[] args) {
        Timer timer = new Timer();
        TimerTask task1 = new TimerTask() {
            @Override
            public void run() {
                log.debug("task 1");
                try {
                    sleep(2000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        };
        TimerTask task2 = new TimerTask() {
            @Override
            public void run() {
                log.debug("task 2");
            }
        };
        // 使用 timer 添加两个任务，希望它们都在 1s 后执行
        // 但由于 timer 内只有一个线程来顺序执行队列中的任务，因此『任务1』的延时，影响了『任务2』的执行
        timer.schedule(task1, 1000);
        timer.schedule(task2, 1000);
    }
    }
}
```

### 使用 ScheduledExecutorService 改写：

```java
public static void main(String[] args) {
    ScheduledExecutorService executor = Executors.newScheduledThreadPool(2);
    // 添加两个任务，希望它们都在 1s 后执行
    System.out.println("start....");
    executor.schedule(() -> {
        System.out.println("任务1，执行时间：" + new Date());
        try { Thread.sleep(2000); } catch (InterruptedException e) { }
    }, 1000, TimeUnit.MILLISECONDS);
    executor.schedule(() -> {
        System.out.println("任务2，执行时间：" + new Date());
    }, 1000, TimeUnit.MILLISECONDS);

}
```

```
start....
任务1，执行时间：Mon Dec 06 20:03:13 CST 2021
任务2，执行时间：Mon Dec 06 20:03:13 CST 2021
```

### scheduleAtFixedRate 例子：

```java
public static void main(String[] args) {
    ScheduledExecutorService pool = Executors.newScheduledThreadPool(1);
    log.debug("start....");
    pool.scheduleAtFixedRate(() ->{
        log.debug("running");
    },1,1, TimeUnit.SECONDS);

}
```

输出分析：一开始，延时 1s，接下来，由于任务执行时间 > 间隔时间，间隔被『撑』到了 2s

```
输出20:04:48 [main] c.test - start....
20:04:49 [pool-1-thread-1] c.test - running
20:04:50 [pool-1-thread-1] c.test - running
20:04:51 [pool-1-thread-1] c.test - running
20:04:52 [pool-1-thread-1] c.test - running
20:04:53 [pool-1-thread-1] c.test - running
20:04:54 [pool-1-thread-1] c.test - running
```

### scheduleWithFixedDelay 例子：

输出分析：一开始，延时 1s，scheduleWithFixedDelay 的间隔是 上一个任务结束 <-> 延时 <-> 下一个任务开始 所 以间隔都是 3s

```java
public static void main(String[] args) {
    ScheduledExecutorService pool = Executors.newScheduledThreadPool(1);
    log.debug("start...");
    pool.scheduleWithFixedDelay(()-> {
        log.debug("running...");
        try {
            sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }, 1, 1, TimeUnit.SECONDS);
```

```
20:07:12 [main] c.test - start...
20:07:13 [pool-1-thread-1] c.test - running...
20:07:16 [pool-1-thread-1] c.test - running...
20:07:19 [pool-1-thread-1] c.test - running...
20:07:22 [pool-1-thread-1] c.test - running...
20:07:25 [pool-1-thread-1] c.test - running...
```

### 正确处理执行任务异常

方法1：主动捉异常

```java
public static void main(String[] args) {
    ExecutorService pool = Executors.newFixedThreadPool(1);
    pool.submit(() -> {
        try {
            log.debug("task1");
            int i = 1 / 0;
        } catch (Exception e) {
            log.error("error:", e);
        }
    });

}
```

输出

```
20:09:14 [pool-1-thread-1] c.test - task1
20:09:14 [pool-1-thread-1] c.test - error:
java.lang.ArithmeticException: / by zero
	at com.harry.thread.TestSchedule.lambda$main$0(TestSchedule.java:23)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
```

方法2：使用 Future

```java
public static void main(String[] args) throws ExecutionException, InterruptedException {
    ExecutorService pool = Executors.newFixedThreadPool(1);
    Future<Boolean> f = pool.submit(() -> {
        log.debug("task1");
        int i = 1 / 0;
        return true;
    });
    log.debug("result:{}", f.get());

}
```

```
20:10:36 [pool-1-thread-1] c.test - task1
Exception in thread "main" java.util.concurrent.ExecutionException: java.lang.ArithmeticException: / by zero
	at java.util.concurrent.FutureTask.report(FutureTask.java:122)
	at java.util.concurrent.FutureTask.get(FutureTask.java:192)
	at com.harry.thread.TestSchedule.main(TestSchedule.java:22)
Caused by: java.lang.ArithmeticException: / by zero
	at com.harry.thread.TestSchedule.lambda$main$0(TestSchedule.java:19)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at java.lang.Thread.run(Thread.java:748)
```

![image-20211230191405918](\images\image-20211230191405918.png)



## 5、定期任务

如何让每周四 18:00:00 定时执行任务

```java
public static void main(String[] args) throws ExecutionException, InterruptedException {
    ScheduledExecutorService executor = Executors.newScheduledThreadPool(2);
    // 获得当前时间
    LocalDateTime now = LocalDateTime.now();
    // 获取本周四 18:00:00.000
    LocalDateTime thursday =
            now.with(DayOfWeek.THURSDAY).withHour(18).withMinute(0).withSecond(0).withNano(0);
    // 如果当前时间已经超过 本周四 18:00:00.000， 那么找下周四 18:00:00.000
    if(now.compareTo(thursday) >= 0) {
        thursday = thursday.plusWeeks(1);
    }
    // 计算时间差，即延时执行时间
    long initialDelay = Duration.between(now, thursday).toMillis();
    // 计算间隔时间，即 1 周的毫秒值
    long oneWeek = 7 * 24 * 3600 * 1000;
    System.out.println("开始时间：" + new Date());
    executor.scheduleAtFixedRate(() -> {
        System.out.println("执行时间：" + new Date());
    }, initialDelay, oneWeek, TimeUnit.MILLISECONDS);
}
```

## 6、Tomcat线程池

### Tomcat用到线程池的地方

LimitLatch 用来限流，可以控制最大连接个数，类似 J.U.C 中的 Semaphore 

Acceptor 只负责【接收新的 socket 连接】 

Poller 只负责监听 socket channel 是否有【可读的 I/O 事件】

 一旦可读，封装一个任务对象（socketProcessor），提交给 Executor 线程池处理

 Executor 线程池中的工作线程最终负责【处理请求】

Tomcat 线程池扩展了 ThreadPoolExecutor，行为稍有不同 如果总线程数达到 maximumPoolSize 这时不会立刻抛 RejectedExecutionException 异常 而是再次尝试将任务放入队列，如果还失败，才抛出 RejectedExecutionException 异常

源码 tomcat-7.0.42

```JAVA
public void execute(Runnable command, long timeout, TimeUnit unit) {
    submittedCount.incrementAndGet();
    try {
        super.execute(command);
    } catch (RejectedExecutionException rx) {
        if (super.getQueue() instanceof TaskQueue) {
            final TaskQueue queue = (TaskQueue) super.getQueue();
            try {
                if (!queue.force(command, timeout, unit)) {
                    submittedCount.decrementAndGet();
                    throw new RejectedExecutionException("Queue capacity is full.");
                }
            } catch (InterruptedException x) {
                submittedCount.decrementAndGet();
                Thread.interrupted();
                throw new RejectedExecutionException(x);
            }
        } else {
            submittedCount.decrementAndGet();
            throw rx;
        }
    }
}
```

TaskQueue.java

```JAVA
public boolean force(Runnable o, long timeout, TimeUnit unit) throws InterruptedException {
    if ( parent.isShutdown() )
        throw new RejectedExecutionException(
                "Executor not running, can't force a command into the queue"
        );
    return super.offer(o,timeout,unit); //forces the item onto the queue, to be used if the task 
    is rejected
}
```

Connector 配置

![image-20211206202853568](\images\image-20211206202853568.png)

Executor 线程配置

![image-20211206202922932](\images\image-20211206202922932.png)

![image-20211206202937717](\images\image-20211206202937717.png)



## 7、Fork/Join

### 概念

Fork/Join 是 JDK 1.7 加入的新的线程池实现，它体现的是一种分治思想，适用于能够进行任务拆分的 cpu 密集型 运算

 所谓的任务拆分，是将一个大任务拆分为算法上相同的小任务，直至不能拆分可以直接求解。跟递归相关的一些计算，如归并排序、斐波那契数列、都可以用分治思想进行求解 Fork/Join 在分治的基础上加入了多线程，可以把每个任务的分解和合并交给不同的线程来完成，进一步提升了运 算效率 Fork/Join 默认会创建与 cpu 核心数大小相同的线程池

### 使用

提交给 Fork/Join 线程池的任务需要继承 RecursiveTask（有返回值）或 RecursiveAction（没有返回值），例如下 面定义了一个对 1~n 之间的整数求和的任务

```java
@Slf4j(topic = "c.task1")
public class AddTask1 extends RecursiveTask<Integer> {
    int n;
    public AddTask1(int n) {
        this.n = n;
    }
    @Override
    public String toString() {
        return "{" + n + '}';
    }

    @Override
    protected Integer compute() {
        // 如果 n 已经为 1，可以求得结果了
        if (n == 1) {
            log.debug("join() {}", n);
            return n;
        }

        // 将任务进行拆分(fork)
        AddTask1 t1 = new AddTask1(n - 1);
        t1.fork();
        log.debug("fork() {} + {}", n, t1);

        // 合并(join)结果
        int result = n + t1.join();
        log.debug("join() {} + {} = {}", n, t1, result);
        return result;

    }

    public static void main(String[] args) {
        ForkJoinPool forkJoinPool = new ForkJoinPool(4);
        System.out.println(forkJoinPool.invoke(new AddTask1(5)));
    }
}
```

结果

```
19:31:59 [ForkJoinPool-1-worker-0] c.task1 - fork() 2 + {1}
19:31:59 [ForkJoinPool-1-worker-3] c.task1 - fork() 3 + {2}
19:31:59 [ForkJoinPool-1-worker-2] c.task1 - fork() 4 + {3}
19:31:59 [ForkJoinPool-1-worker-1] c.task1 - fork() 5 + {4}
19:31:59 [ForkJoinPool-1-worker-0] c.task1 - join() 1
19:31:59 [ForkJoinPool-1-worker-0] c.task1 - join() 2 + {1} = 3
19:31:59 [ForkJoinPool-1-worker-3] c.task1 - join() 3 + {2} = 6
19:31:59 [ForkJoinPool-1-worker-2] c.task1 - join() 4 + {3} = 10
19:31:59 [ForkJoinPool-1-worker-1] c.task1 - join() 5 + {4} = 15
15
```

![image-20211208194012920](\images\image-20211208194012920.png)

### 改进

```java
package com.harry.thread;

import lombok.extern.slf4j.Slf4j;

import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveTask;
@Slf4j(topic = "c.task1")
public class AddTask extends RecursiveTask<Integer> {
    int begin;
    int end;

    public AddTask(int begin, int end) {
        this.begin = begin;
        this.end = end;
    }
    @Override
    public String toString() {
        return "{" + begin + "," + end + '}';
    }

    @Override
    protected Integer compute() {
        // 5, 5
        if (begin == end) {
            log.debug("join() {}", begin);
            return begin;
        }
        // 4, 5
        if (end - begin == 1) {
            log.debug("join() {} + {} = {}", begin, end, end + begin);
            return end + begin;
        }

        // 1 5
        int mid = (end + begin) / 2; // 3
        AddTask t1 = new AddTask(begin, mid); // 1,3
        t1.fork();
        AddTask t2 = new AddTask(mid + 1, end); // 4,5
        t2.fork();
        log.debug("fork() {} + {} = ?", t1, t2);
        int result = t1.join() + t2.join();
        log.debug("join() {} + {} = {}", t1, t2, result);
        return result;
    }

    public static void main(String[] args) {
        ForkJoinPool pool = new ForkJoinPool(4);
        System.out.println(pool.invoke(new AddTask(1, 5)));
    }
}
```

结果

```
19:47:27 [ForkJoinPool-1-worker-3] c.task1 - join() 4 + 5 = 9
19:47:27 [ForkJoinPool-1-worker-0] c.task1 - join() 1 + 2 = 3
19:47:27 [ForkJoinPool-1-worker-1] c.task1 - fork() {1,3} + {4,5} = ?
19:47:27 [ForkJoinPool-1-worker-2] c.task1 - fork() {1,2} + {3,3} = ?
19:47:27 [ForkJoinPool-1-worker-3] c.task1 - join() 3
19:47:27 [ForkJoinPool-1-worker-2] c.task1 - join() {1,2} + {3,3} = 6
19:47:27 [ForkJoinPool-1-worker-1] c.task1 - join() {1,3} + {4,5} = 15
15

Process finished with exit code 0
```

![image-20211208194813287](\images\image-20211208194813287.png)

# 九、JUC

## 1 AQS原理

### 概述

全称是 AbstractQueuedSynchronizer，是阻塞式锁和相关的同步器工具的框架

特点：用 state 属性来表示资源的状态（分独占模式和共享模式），子类需要定义如何维护这个状态，控制如何获取 锁和释放锁，

​		getState - 获取 state 

​		状态 setState - 设置 state 状态

​		compareAndSetState - cas 机制设置 state 状态 

​		独占模式是只有一个线程能够访问资源，而共享模式可以允许多个线程访问资源

提供了基于 FIFO 的等待队列，类似于 Monitor 的 EntryList

条件变量来实现等待、唤醒机制，支持多个条件变量，类似于 Monitor 的 WaitSet



子类主要实现这样一些方法（默认抛出 UnsupportedOperationException）

​	tryAcquire

​	tryRelease

​	tryAcquireShared

​	tryReleaseShared

​	isHeldExclusively

获取锁的姿势

```java
// 如果获取锁失败
if (!tryAcquire(arg)) {
// 入队, 可以选择阻塞当前线程 park unpark
}
```

释放锁的姿势

```java
// 如果释放锁成功
if (tryRelease(arg)) {
// 让阻塞线程恢复运行
}
```

### 实现不可重入锁

自定义同步器

```java
package com.harry.thread;

import java.util.concurrent.locks.AbstractQueuedSynchronizer;
import java.util.concurrent.locks.Condition;

public class MySync extends AbstractQueuedSynchronizer {
    @Override
    protected boolean tryAcquire(int acquires) {
        if (acquires ==1){
            if (compareAndSetState(0,1)){
                setExclusiveOwnerThread(Thread.currentThread());
                return true;
            }
        }
        return false;
    }

    @Override
    protected boolean tryRelease(int acquires) {
        if (acquires == 1){
            if (getState() == 0){
                throw new IllegalMonitorStateException();
            }
            setExclusiveOwnerThread(null);
            setState(0);
            return true;
        }
        return false;
    }
    
    protected Condition newCondition(){
        return new ConditionObject();
    }

    @Override
    protected boolean isHeldExclusively() {
        return getState() == 1;
    }
}
```

自定义锁

有了自定义同步器，很容易复用 AQS ，实现一个功能完备的自定义锁

```java
@Slf4j(topic = "c.test")
class MyLock implements Lock {
    static MySync sync = new MySync();

    @Override
    // 尝试不成功进入等待队列
    public void lock() {
        sync.acquire(1);
    }

    @Override
    // 尝试，不成功进入等待队列，可打断
    public void lockInterruptibly() throws InterruptedException {
        sync.acquireInterruptibly(1);
    }

    @Override
    // 尝试一次，不成功返回，不进入队列
    public boolean tryLock() {
        return sync.tryAcquire(1);
    }

    @Override
    // 尝试不成功，进入等待队列，有时限
    public boolean tryLock(long time, TimeUnit unit) throws InterruptedException {
        return sync.tryAcquireNanos(1, unit.toNanos(time));
    }

    @Override
    // 释放锁
    public void unlock() {
        sync.release(1);
    }

    @Override
    public Condition newCondition() {
        return sync.newCondition();
    }

    public static void main(String[] args) {
        MyLock myLock = new MyLock();
        new Thread(()->{
            myLock.lock();
            try {
                log.debug("locking");
            }finally {
                log.debug("unlocking");
                myLock.unlock();
            }
        }, "t1").start();

        new Thread(()->{
            myLock.lock();
            try {
                log.debug("locking");
            }finally {
                log.debug("unlocking");
                myLock.unlock();
            }
        }, "t2").start();
        
    }
}
```

输出

```
20:46:40 [t1] c.test - locking
20:46:40 [t1] c.test - unlocking
20:46:40 [t2] c.test - locking
20:46:40 [t2] c.test - unlocking
```

早期程序员会自己通过一种同步器去实现另一种相近的同步器，例如用可重入锁去实现信号量，或反之。这显然不 够优雅，于是在 JSR166（java 规范提案）中创建了 AQS，提供了这种通用的同步器机制。

### AQS 要实现的功能目标

阻塞版本获取锁 acquire 和非阻塞的版本尝试获取锁 tryAcquire

获取锁超时机制

通过打断取消机制

独占机制及共享机制

条件不满足时的等待机制

#### 设计

AQS 的基本思想其实很简单 获取锁的逻辑

```java
while(state 状态不允许获取) {
  if(队列中还没有此线程) {
        入队并阻塞
    }
 }
 当前线程出队
```

释放锁的逻辑

```java
if(state 状态允许了) {
        恢复阻塞的线程(s)
    }
```

要点

​	原子维护 state 状态

​	阻塞及恢复线程

​	维护队列

##### 1) state 设计

state 使用 volatile 配合 cas 保证其修改时的原子性 

state 使用了 32bit int 来维护同步状态，因为当时使用 long 在很多平台下测试的结果并不理想

##### 2) 阻塞恢复设计

早期的控制线程暂停和恢复的 api 有 suspend 和 resume，但它们是不可用的，因为如果先调用的 resume  那么 suspend 将感知不到 

解决方法是使用 park & unpark 来实现线程的暂停和恢复，先 unpark 再 park 也没 问题 

park & unpark 是针对线程的，而不是针对同步器的，因此控制粒度更为精细

park 线程还可以通过 interrupt 打断

##### 3）队列设计

使用了 FIFO 先入先出队列，并不支持优先级队列

设计时借鉴了 CLH 队列，它是一种单向无锁队列

![image-20211208210104979](\images\image-20211208210104979.png)

队列中有 head 和 tail 两个指针节点，都用 volatile 修饰配合 cas 使用，每个节点有 state 维护节点状态 入队伪代码，只需要考虑 tail 赋值的原子性



```java
do {
	// 原来的 tail
	Node prev = tail;
	// 用 cas 在原来 tail 的基础上改为 node
} while(tail.compareAndSet(prev, node))
```

CLH 好处： 无锁，使用自旋，快速，无阻

AQS 在一些方面改进了 CLH

```java
private Node enq(final Node node) {
    for (;;) {
        Node t = tail;
        // 队列中还没有元素 tail 为 null
        if (t == null) {
            // 将 head 从 null -> dummy
            if (compareAndSetHead(new Node()))
                tail = head;
        } else {
            // 将 node 的 prev 设置为原来的 tail
            node.prev = t;
            // 将 tail 从原来的 tail 设置为 node
            if (compareAndSetTail(t, node)) {
                // 原来 tail 的 next 设置为 node
                t.next = node;
                return t;
            }
        }
    }
}
```

主要用到 AQS 的并发工具类

![image-20211208210430336](\images\image-20211208210430336.png)

## 2、ReentrantLock 原理

![image-20211216152540692](\images\image-20211216152540692.png)

### 非公平锁实现原理

#### 加锁解锁流程

先从构造器开始看，默认为非公平锁实现

```java
public ReentrantLock() {
    sync = new NonfairSync();
}
```

NonfairSync 继承自 AQS

没有竞争时

![image-20211216152958684](\images\image-20211216152958684.png)

第一个竞争出现时

![image-20211216153027002](\images\image-20211216153027002.png)

Thread-1 执行了

​	1 CAS 尝试将 state 由 0 改为 1，结果失败 

​	2 进入 tryAcquire 逻辑，这时 state 已经是1，结果仍然失败

​	3 接下来进入 addWaiter 逻辑，构造 Node 队列

图中黄色三角表示该 Node 的 waitStatus 状态，其中 0 为默认正常状态 Node 的创建是懒惰的 其中第一个 Node 称为 Dummy（哑元）或哨兵，用来占位，并不关联线程

![image-20211216153232783](\images\image-20211216153232783.png)

当前线程进入 acquireQueued 逻辑

1. acquireQueued 会在一个死循环中不断尝试获得锁，失败后进入 park 阻塞 

2. 如果自己是紧邻着 head（排第二位），那么再次 tryAcquire 尝试获取锁，当然这时 state 仍为 1，失败 

3. 进入 shouldParkAfterFailedAcquire 逻辑，将前驱 node，即 head 的 waitStatus 改为 -1，这次返回 false

   ```java
   /**
    * Acquires in exclusive uninterruptible mode for thread already in
    * queue. Used by condition wait methods as well as acquire.
    *
    * @param node the node
    * @param arg the acquire argument
    * @return {@code true} if interrupted while waiting
    */
   final boolean acquireQueued(final Node node, int arg) {
       boolean failed = true;
       try {
           boolean interrupted = false;
           for (;;) {
               final Node p = node.predecessor();
               if (p == head && tryAcquire(arg)) {
                   setHead(node);
                   p.next = null; // help GC
                   failed = false;
                   return interrupted;
               }
               if (shouldParkAfterFailedAcquire(p, node) &&
                   parkAndCheckInterrupt())
                   interrupted = true;
           }
       } finally {
           if (failed)
               cancelAcquire(node);
       }
   }
   ```

![image-20211216153407845](\images\image-20211216153407845.png)

4. shouldParkAfterFailedAcquire 执行完毕回到 acquireQueued ，再次 tryAcquire 尝试获取锁，当然这时 state 仍为 1，失败 
5. 当再次进入 shouldParkAfterFailedAcquire 时，这时因为其前驱 node 的 waitStatus 已经是 -1，这次返回 true 
6. 进入 parkAndCheckInterrupt， Thread-1 park（灰色表示）

```java
/**
 * Checks and updates status for a node that failed to acquire.
 * Returns true if thread should block. This is the main signal
 * control in all acquire loops.  Requires that pred == node.prev.
 *
 * @param pred node's predecessor holding status
 * @param node the node
 * @return {@code true} if thread should block
 */
private static boolean shouldParkAfterFailedAcquire(Node pred, Node node) {
    int ws = pred.waitStatus;
    if (ws == Node.SIGNAL)
        /*
         * This node has already set status asking a release
         * to signal it, so it can safely park.
         */
        return true;
    if (ws > 0) {
        /*
         * Predecessor was cancelled. Skip over predecessors and
         * indicate retry.
         */
        do {
            node.prev = pred = pred.prev;
        } while (pred.waitStatus > 0);
        pred.next = node;
    } else {
        /*
         * waitStatus must be 0 or PROPAGATE.  Indicate that we
         * need a signal, but don't park yet.  Caller will need to
         * retry to make sure it cannot acquire before parking.
         */
        compareAndSetWaitStatus(pred, ws, Node.SIGNAL);
    }
    return false;
```

![image-20211216153827515](\images\image-20211216153827515.png)

```java
/**
 * Convenience method to park and then check if interrupted
 *
 * @return {@code true} if interrupted
 */
private final boolean parkAndCheckInterrupt() {
    LockSupport.park(this);
    return Thread.interrupted();
}
```

再次有多个线程经历上述过程竞争失败，变成这个样子

![image-20211216154137052](\images\image-20211216154137052.png)

#### Thread-0 释放锁，进入 tryRelease 流程，如果成功

设置 exclusiveOwnerThread 为 null 

state = 0

![image-20211216154240547](\images\image-20211216154240547.png)

当前队列不为 null，并且 head 的 waitStatus = -1，进入 unparkSuccessor 流程 找到队列中离 head 最近的一个 Node（没取消的），unpark 恢复其运行，本例中即为 Thread-1 回到 Thread-1 的 acquireQueued 流程

![image-20211216154732554](\images\image-20211216154732554.png)

如果加锁成功（没有竞争），会设置

exclusiveOwnerThread 为 Thread-1，state = 1

 head 指向刚刚 Thread-1 所在的 Node，该 Node 清空 Thread

 原本的 head 因为从链表断开，而可被垃圾回收

如果这时候有其它线程来竞争（非公平的体现），例如这时有 Thread-4 来了

![image-20211216154929806](\images\image-20211216154929806.png)

如果不巧又被 Thread-4 占了先

Thread-4 被设置为 exclusiveOwnerThread，state = 1

Thread-1 再次进入 acquireQueued 流程，获取锁失败，重新进入 park 阻塞

#### 加锁源码

```java

// Sync 继承自 AQS
static final class NonfairSync extends Sync {
    private static final long serialVersionUID = 7316153563782823691L;

    /**
     * Performs lock.  Try immediate barge, backing up to normal
     * acquire on failure.
     */
    final void lock() {
        // 首先用 cas 尝试（仅尝试一次）将 state 从 0 改为 1, 如果成功表示获得了独占锁
        if (compareAndSetState(0, 1))
            setExclusiveOwnerThread(Thread.currentThread());
        else
            // 如果尝试失败，进入 ㈠
            acquire(1);
    }

    protected final boolean tryAcquire(int acquires) {
        return nonfairTryAcquire(acquires);
    }
}
```

```java
// ㈠ AQS 继承过来的方法, 方便阅读, 放在此处
public final void acquire(int arg) {
    if (!tryAcquire(arg) &&
        // 当 tryAcquire 返回为 false 时, 先调用 addWaiter ㈣, 接着 acquireQueued ㈤
        acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
        selfInterrupt();
}
```

```java
// ㈡ 进入 ㈢
protected final boolean tryAcquire(int acquires) {
    return nonfairTryAcquire(acquires);
}
```

```java
// ㈢ Sync 继承过来的方法, 方便阅读, 放在此处
final boolean nonfairTryAcquire(int acquires) {
    final Thread current = Thread.currentThread();
    int c = getState();
    // 如果还没有获得锁
    if (c == 0) {
        // 尝试用 cas 获得, 这里体现了非公平性: 不去检查 AQS 队列
        if (compareAndSetState(0, acquires)) {
            setExclusiveOwnerThread(current);
            return true;
        }
    }
    // 如果已经获得了锁, 线程还是当前线程, 表示发生了锁重入
    else if (current == getExclusiveOwnerThread()) {
        // state++
        int nextc = c + acquires;
        if (nextc < 0) // overflow
            throw new Error("Maximum lock count exceeded");
        setState(nextc);
        return true;
    }
    // 获取失败, 回到调用处
    return false;
}
```

```java
// ㈣ AQS 继承过来的方法, 方便阅读, 放在此处
private Node addWaiter(Node mode) {
    // 将当前线程关联到一个 Node 对象上, 模式为独占模式
    Node node = new Node(Thread.currentThread(), mode);
    // 如果 tail 不为 null, cas 尝试将 Node 对象加入 AQS 队列尾部
    Node pred = tail;
    if (pred != null) {
        node.prev = pred;
        if (compareAndSetTail(pred, node)) {
            // 双向链表
            pred.next = node;
            return node;
        }
    }
    // 尝试将 Node 加入 AQS, 进入 ㈥
    enq(node);
    return node;
}
```

```java
private Node enq(final Node node) {
    for (;;) {
        Node t = tail;
        if (t == null) { // Must initialize
            // 还没有, 设置 head 为哨兵节点（不对应线程，状态为 0）
            if (compareAndSetHead(new Node()))
                tail = head;
        } else {
            // cas 尝试将 Node 对象加入 AQS 队列尾部
            node.prev = t;
            if (compareAndSetTail(t, node)) {
                t.next = node;
                return t;
            }
        }
    }
}
```

```java
// ㈤ AQS 继承过来的方法, 方便阅读, 放在此处
final boolean acquireQueued(final Node node, int arg) {
    boolean failed = true;
    try {
        boolean interrupted = false;
        for (;;) {
            final Node p = node.predecessor();
            // 上一个节点是 head, 表示轮到自己（当前线程对应的 node）了, 尝试获取
            if (p == head && tryAcquire(arg)) {
                // 获取成功, 设置自己（当前线程对应的 node）为 head
                setHead(node);
                p.next = null; // help GC
                // 返回中断标记 false
                failed = false;
                return interrupted;
            }
            if (
                // 判断是否应当 park, 进入 ㈦
                shouldParkAfterFailedAcquire(p, node) &&
                // park 等待, 此时 Node 的状态被置为 Node.SIGNAL ㈧
                parkAndCheckInterrupt())
                interrupted = true;
        }
    } finally {
        if (failed)
            cancelAcquire(node);
    }
}
```

```java
// ㈦ AQS 继承过来的方法, 方便阅读, 放在此处
private static boolean shouldParkAfterFailedAcquire(Node pred, Node node) {
    // 获取上一个节点的状态
    int ws = pred.waitStatus;
    if (ws == Node.SIGNAL)
   		// 上一个节点都在阻塞, 那么自己也阻塞好了
        return true;
    // > 0 表示取消状态
    if (ws > 0) {
     // 上一个节点取消, 那么重构删除前面所有取消的节点, 返回到外层循环重试
        do {
            node.prev = pred = pred.prev;
        } while (pred.waitStatus > 0);
        pred.next = node;
    } else {
        // 这次还没有阻塞
		// 但下次如果重试不成功, 则需要阻塞，这时需要设置上一个节点状态为 Node.SIGNAL
        compareAndSetWaitStatus(pred, ws, Node.SIGNAL);
    }
    return false;
}
```

```java
// ㈧ 阻塞当前线程
private final boolean parkAndCheckInterrupt() {
    LockSupport.park(this);
    return Thread.interrupted();
}
```

注意:是否需要 unpark 是由当前节点的前驱节点的 waitStatus == Node.SIGNAL 来决定，而不是本节点的 waitStatus 决定

#### 解锁源码

```java
// Sync 继承自 AQS
static final class NonfairSync extends Sync {
    // 解锁实现
    public void unlock() {
        sync.release(1);
    }

    // AQS 继承过来的方法, 方便阅读, 放在此处
    public final boolean release(int arg) {
        // 尝试释放锁, 进入 ㈠
        if (tryRelease(arg)) {
            // 队列头节点 unpark
            Node h = head;
            if (
                // 队列不为 null
                    h != null &&
                            // waitStatus == Node.SIGNAL 才需要 unpark
                            h.waitStatus != 0
            ) {
                // unpark AQS 中等待的线程, 进入 ㈡
                unparkSuccessor(h);
            }
            return true;
        }
        return false;
    }

    // ㈠ Sync 继承过来的方法, 方便阅读, 放在此处
    protected final boolean tryRelease(int releases) {
        // state--
        int c = getState() - releases;
        if (Thread.currentThread() != getExclusiveOwnerThread())
            throw new IllegalMonitorStateException();
        boolean free = false;
        // 支持锁重入, 只有 state 减为 0, 才释放成功
        if (c == 0) {
            free = true;
            setExclusiveOwnerThread(null);
        }
        setState(c);
        return free;
    }
```

```java
private void unparkSuccessor(Node node) {
    // 如果状态为 Node.SIGNAL 尝试重置状态为 0
	// 不成功也可以
    int ws = node.waitStatus;
    if (ws < 0)
        compareAndSetWaitStatus(node, ws, 0);

    // 找到需要 unpark 的节点, 但本节点从 AQS 队列中脱离, 是由唤醒节点完成的
    Node s = node.next;
    // 不考虑已取消的节点, 从 AQS 队列从后至前找到队列最前面需要 unpark 的节点
    if (s == null || s.waitStatus > 0) {
        s = null;
        for (Node t = tail; t != null && t != node; t = t.prev)
            if (t.waitStatus <= 0)
                s = t;
    }
    if (s != null)
        LockSupport.unpark(s.thread);
}
```

#### 可重入原理

```java
static final class NonfairSync extends Sync {
    // ...

    // Sync 继承过来的方法, 方便阅读, 放在此处
    final boolean nonfairTryAcquire(int acquires) {
        final Thread current = Thread.currentThread();
        int c = getState();
        if (c == 0) {
            if (compareAndSetState(0, acquires)) {
                setExclusiveOwnerThread(current);
                return true;
            }
        }
        // 如果已经获得了锁, 线程还是当前线程, 表示发生了锁重入
        else if (current == getExclusiveOwnerThread()) {
            // state++
            int nextc = c + acquires;
            if (nextc < 0) // overflow
                throw new Error("Maximum lock count exceeded");
            setState(nextc);
            return true;
        }
        return false;
    }

    // Sync 继承过来的方法, 方便阅读, 放在此处
    protected final boolean tryRelease(int releases) {
        // state--
        int c = getState() - releases;
        if (Thread.currentThread() != getExclusiveOwnerThread())
            throw new IllegalMonitorStateException();
        boolean free = false;
        // 支持锁重入, 只有 state 减为 0, 才释放成功
        if (c == 0) {
            free = true;
            setExclusiveOwnerThread(null);
        }
        setState(c);
        return free;
    }
}
```

####  可打断原理

不可打断模式

在此模式下，即使它被打断，仍会驻留在 AQS 队列中，一直要等到获得锁后方能得知自己被打断了

```java
// Sync 继承自 AQS
static final class NonfairSync extends Sync {
    // ...

    private final boolean parkAndCheckInterrupt() {
        // 如果打断标记已经是 true, 则 park 会失效
        LockSupport.park(this);
        // interrupted 会清除打断标记
        return Thread.interrupted();
    }

    final boolean acquireQueued(final Node node, int arg) {
        boolean failed = true;
        try {
            boolean interrupted = false;
            for (;;) {
                final Node p = node.predecessor();
                if (p == head && tryAcquire(arg)) {
                    setHead(node);
                    p.next = null;
                    failed = false;
                    // 还是需要获得锁后, 才能返回打断状态
                    return interrupted;
                }
                if (
                        shouldParkAfterFailedAcquire(p, node) &&
                                parkAndCheckInterrupt()
                ) {
                    // 如果是因为 interrupt 被唤醒, 返回打断状态为 true
                    interrupted = true;
                }
            }
        } finally {
            if (failed)
                cancelAcquire(node);
        }
    }

    public final void acquire(int arg) {
        if (
                !tryAcquire(arg) &&
                        acquireQueued(addWaiter(Node.EXCLUSIVE), arg)
        ) {
            // 如果打断状态为 true
            selfInterrupt();
        }
    }

    static void selfInterrupt() {
        // 重新产生一次中断
        Thread.currentThread().interrupt();
    }
}
```

可打断模式

```java
static final class NonfairSync extends Sync {
    public final void acquireInterruptibly(int arg) throws InterruptedException {
        if (Thread.interrupted())
            throw new InterruptedException();
        // 如果没有获得到锁, 进入 ㈠
        if (!tryAcquire(arg))
            doAcquireInterruptibly(arg);
    }

    // ㈠ 可打断的获取锁流程
    private void doAcquireInterruptibly(int arg) throws InterruptedException {
        final Node node = addWaiter(Node.EXCLUSIVE);
        boolean failed = true;
        try {
            for (;;) {
                final Node p = node.predecessor();
                if (p == head && tryAcquire(arg)) {
                    setHead(node);
                    p.next = null; // help GC
                    failed = false;
                    return;
                }
                if (shouldParkAfterFailedAcquire(p, node) &&
                        parkAndCheckInterrupt()) {
                    // 在 park 过程中如果被 interrupt 会进入此
                    // 这时候抛出异常, 而不会再次进入 for (;;)
                    throw new InterruptedException();
                }
            }
        } finally {
            if (failed)
                cancelAcquire(node);
        }
    }
}
```

#### 公平锁实现原理

```java
static final class FairSync extends Sync {
    private static final long serialVersionUID = -3000897897090466540L;
    final void lock() {
        acquire(1);
    }

    // AQS 继承过来的方法, 方便阅读, 放在此处
    public final void acquire(int arg) {
        if (
                !tryAcquire(arg) &&
                        acquireQueued(addWaiter(Node.EXCLUSIVE), arg)
        ) {
            selfInterrupt();
        }
    }
    // 与非公平锁主要区别在于 tryAcquire 方法的实现
    protected final boolean tryAcquire(int acquires) {
        final Thread current = Thread.currentThread();
        int c = getState();
        if (c == 0) {
            // 先检查 AQS 队列中是否有前驱节点, 没有才去竞争
            if (!hasQueuedPredecessors() &&
                    compareAndSetState(0, acquires)) {
                setExclusiveOwnerThread(current);
                return true;
            }
        }
        else if (current == getExclusiveOwnerThread()) {
            int nextc = c + acquires;
            if (nextc < 0)
                throw new Error("Maximum lock count exceeded");
            setState(nextc);
            return true;
        }
        return false;
    }

    // ㈠ AQS 继承过来的方法, 方便阅读, 放在此处
    public final boolean hasQueuedPredecessors() {
        Node t = tail;
        Node h = head;
        Node s;
        // h != t 时表示队列中有 Node
        return h != t &&
                (
                    // (s = h.next) == null 表示队列中还有没有老二
                    (s = h.next) == null ||
                            // 或者队列中老二线程不是此线程
                            s.thread != Thread.currentThread()
                );
    }
}
```

### 条件变量实现原理

每个条件变量其实就对应着一个等待队列，其实现类是 ConditionObject

#### await 流程

开始 Thread-0 持有锁，调用 await，进入 ConditionObject 的 addConditionWaiter 流程 创建新的 Node 状态为 -2（Node.CONDITION），关联 Thread-0，加入等待队列尾部

![image-20211216164818924](\images\image-20211216164818924.png)

接下来进入 AQS 的 fullyRelease 流程，释放同步器上的锁

![image-20211216164913607](\images\image-20211216164913607.png)

unpark AQS 队列中的下一个节点，竞争锁，假设没有其他竞争线程，那么 Thread-1 竞争成功

![image-20211216164944462](\images\image-20211216164944462.png)

park 阻塞 Thread-0

![image-20211216165049871](\images\image-20211216165049871.png)

#### signal 流程

假设 Thread-1 要来唤醒 Thread-0

![image-20211216172402807](\images\image-20211216172402807.png)

进入 ConditionObject 的 doSignal 流程，取得等待队列中第一个 Node，即 Thread-0 所在 Node

![image-20211216172520916](\images\image-20211216172520916.png)

执行 transferForSignal 流程，将该 Node 加入 AQS 队列尾部，将 Thread-0 的 waitStatus 改为 0，Thread-3 的 waitStatus 改为 -1

Thread-1 释放锁，进入 unlock 流程，略

源码

```java
public class ConditionObject implements Condition, java.io.Serializable {
    private static final long serialVersionUID = 1173984872572414699L;

    // 第一个等待节点
    private transient Node firstWaiter;

    // 最后一个等待节点
    private transient Node lastWaiter;
    public ConditionObject() { }
    // ㈠ 添加一个 Node 至等待队列
    private Node addConditionWaiter() {
        Node t = lastWaiter;
        // 所有已取消的 Node 从队列链表删除, 见 ㈡
        if (t != null && t.waitStatus != Node.CONDITION) {
            unlinkCancelledWaiters();
            t = lastWaiter;
        }
        // 创建一个关联当前线程的新 Node, 添加至队列尾部
        Node node = new Node(Thread.currentThread(), Node.CONDITION);
        if (t == null)
            firstWaiter = node;
        else
            t.nextWaiter = node;
        lastWaiter = node;
        return node;
    }
    // 唤醒 - 将没取消的第一个节点转移至 AQS 队列
    private void doSignal(Node first) {
        do {
            // 已经是尾节点了
            if ( (firstWaiter = first.nextWaiter) == null) {
                lastWaiter = null;
            }
            first.nextWaiter = null;
        } while (
            // 将等待队列中的 Node 转移至 AQS 队列, 不成功且还有节点则继续循环 ㈢
                !transferForSignal(first) &&
                        // 队列还有节点
                        (first = firstWaiter) != null
        );
    }

    // 外部类方法, 方便阅读, 放在此处
    // ㈢ 如果节点状态是取消, 返回 false 表示转移失败, 否则转移成功
    final boolean transferForSignal(Node node) {
        // 如果状态已经不是 Node.CONDITION, 说明被取消了
        if (!compareAndSetWaitStatus(node, Node.CONDITION, 0))
            return false;
        // 加入 AQS 队列尾部
        Node p = enq(node);
        int ws = p.waitStatus;
        if (
            // 上一个节点被取消
                ws > 0 ||
                        // 上一个节点不能设置状态为 Node.SIGNAL
                        !compareAndSetWaitStatus(p, ws, Node.SIGNAL)
        ) {
            // unpark 取消阻塞, 让线程重新同步状态
            LockSupport.unpark(node.thread);
        }
        return true;
    }
    // 全部唤醒 - 等待队列的所有节点转移至 AQS 队列
    private void doSignalAll(Node first) {
        lastWaiter = firstWaiter = null;
        do {
            Node next = first.nextWaiter;
            first.nextWaiter = null;
            transferForSignal(first);
            first = next;
        } while (first != null);
    }

    // ㈡
    private void unlinkCancelledWaiters() {
        // ...
    }
    // 唤醒 - 必须持有锁才能唤醒, 因此 doSignal 内无需考虑加锁
    public final void signal() {
        if (!isHeldExclusively())
            throw new IllegalMonitorStateException();
        Node first = firstWaiter;
        if (first != null)
            doSignal(first);
    }
    // 全部唤醒 - 必须持有锁才能唤醒, 因此 doSignalAll 内无需考虑加锁
    public final void signalAll() {
        if (!isHeldExclusively())
            throw new IllegalMonitorStateException();
        Node first = firstWaiter;
        if (first != null)
            doSignalAll(first);
    }
    // 不可打断等待 - 直到被唤醒
    public final void awaitUninterruptibly() {
        // 添加一个 Node 至等待队列, 见 ㈠
        Node node = addConditionWaiter();
        // 释放节点持有的锁, 见 ㈣
        int savedState = fullyRelease(node);
        boolean interrupted = false;
        // 如果该节点还没有转移至 AQS 队列, 阻塞
        while (!isOnSyncQueue(node)) {
            // park 阻塞
            LockSupport.park(this);
            // 如果被打断, 仅设置打断状态
            if (Thread.interrupted())
                interrupted = true;
        }
        // 唤醒后, 尝试竞争锁, 如果失败进入 AQS 队列
        if (acquireQueued(node, savedState) || interrupted)
            selfInterrupt();
    }
    // 外部类方法, 方便阅读, 放在此处
    // ㈣ 因为某线程可能重入，需要将 state 全部释放
    final int fullyRelease(Node node) {
        boolean failed = true;
        try {
            int savedState = getState();
            if (release(savedState)) {
                failed = false;
                return savedState;
            } else {
                throw new IllegalMonitorStateException();
            }
        } finally {
            if (failed)
                node.waitStatus = Node.CANCELLED;
        }
    }
    // 打断模式 - 在退出等待时重新设置打断状态
    private static final int REINTERRUPT = 1;
    // 打断模式 - 在退出等待时抛出异常
    private static final int THROW_IE = -1;
    // 判断打断模式
    private int checkInterruptWhileWaiting(Node node) {
        return Thread.interrupted() ?
                (transferAfterCancelledWait(node) ? THROW_IE : REINTERRUPT) :
                0;
    }
    // ㈤ 应用打断模式
    private void reportInterruptAfterWait(int interruptMode)
            throws InterruptedException {
        if (interruptMode == THROW_IE)
            throw new InterruptedException();
        else if (interruptMode == REINTERRUPT)
            selfInterrupt();
    }
    // 等待 - 直到被唤醒或打断
    public final void await() throws InterruptedException {
        if (Thread.interrupted()) {
            throw new InterruptedException();
        }
        // 添加一个 Node 至等待队列, 见 ㈠
        Node node = addConditionWaiter();
        // 释放节点持有的锁
        int savedState = fullyRelease(node);
        int interruptMode = 0;
        // 如果该节点还没有转移至 AQS 队列, 阻塞
        while (!isOnSyncQueue(node)) {
            // park 阻塞
            LockSupport.park(this);
            // 如果被打断, 退出等待队列
            if ((interruptMode = checkInterruptWhileWaiting(node)) != 0)
                break;
        }
        // 退出等待队列后, 还需要获得 AQS 队列的锁
        if (acquireQueued(node, savedState) && interruptMode != THROW_IE)
            interruptMode = REINTERRUPT;
        // 所有已取消的 Node 从队列链表删除, 见 ㈡
        if (node.nextWaiter != null)
            unlinkCancelledWaiters();
        // 应用打断模式, 见 ㈤
        if (interruptMode != 0)
            reportInterruptAfterWait(interruptMode);
    }
    // 等待 - 直到被唤醒或打断或超时
    public final long awaitNanos(long nanosTimeout) throws InterruptedException {
        if (Thread.interrupted()) {
            throw new InterruptedException();
        }
        // 添加一个 Node 至等待队列, 见 ㈠
        Node node = addConditionWaiter();
        // 释放节点持有的锁
        int savedState = fullyRelease(node);
        // 获得最后期限
        final long deadline = System.nanoTime() + nanosTimeout;
        int interruptMode = 0;
        // 如果该节点还没有转移至 AQS 队列, 阻塞
        while (!isOnSyncQueue(node)) {
            // 已超时, 退出等待队列
            if (nanosTimeout <= 0L) {
                transferAfterCancelledWait(node);
                break;
            }
            // park 阻塞一定时间, spinForTimeoutThreshold 为 1000 ns
            if (nanosTimeout >= spinForTimeoutThreshold)
                LockSupport.parkNanos(this, nanosTimeout);
            // 如果被打断, 退出等待队列
            if ((interruptMode = checkInterruptWhileWaiting(node)) != 0)
                break;
            nanosTimeout = deadline - System.nanoTime();
        }
        // 退出等待队列后, 还需要获得 AQS 队列的锁
        if (acquireQueued(node, savedState) && interruptMode != THROW_IE)
            interruptMode = REINTERRUPT;
        // 所有已取消的 Node 从队列链表删除, 见 ㈡
        if (node.nextWaiter != null)
            unlinkCancelledWaiters();
        // 应用打断模式, 见 ㈤
        if (interruptMode != 0)
            reportInterruptAfterWait(interruptMode);
        return deadline - System.nanoTime();
    }
    // 等待 - 直到被唤醒或打断或超时, 逻辑类似于 awaitNanos
    public final boolean awaitUntil(Date deadline) throws InterruptedException {
        // ...
    }
    // 等待 - 直到被唤醒或打断或超时, 逻辑类似于 awaitNanos
    public final boolean await(long time, TimeUnit unit) throws InterruptedException {
        // ...
    }
    // 工具方法 省略 ...
}
```

## 3、读写锁原理

### 图解流程

读写锁用的是同一个 Sycn 同步器，因此等待队列、state 等也是同一个

#### t1 w.lock，t2 r.lock

1） t1 成功上锁，流程与 ReentrantLock 加锁相比没有特殊之处，不同是写锁状态占了 state 的低 16 位，而读锁 使用的是 state 的高 16 位

![image-20211217151008950](\images\image-20211217151008950.png)

2）t2 执行 r.lock，这时进入读锁的 sync.acquireShared(1) 流程，首先会进入 tryAcquireShared 流程。如果有写 锁占据，那么 tryAcquireShared 返回 -1 表示失败

tryAcquireShared 返回值表示：

​	-1 表示失败

​	0 表示成功，但后继节点不会继续唤醒 

​	正数表示成功，而且数值是还有几个后继节点需要唤醒，读写锁返回 1

![image-20211217152300077](\images\image-20211217152300077.png)

3）这时会进入 sync.doAcquireShared(1) 流程，首先也是调用 addWaiter 添加节点，不同之处在于节点被设置为 Node.SHARED 模式而非 Node.EXCLUSIVE 模式，注意此时 t2 仍处于活跃状态

![image-20211217152819843](\images\image-20211217152819843.png)

4）t2 会看看自己的节点是不是老二，如果是，还会再次调用 tryAcquireShared(1) 来尝试获取锁

5）如果没有成功，在 doAcquireShared 内 for (;;) 循环一次，把前驱节点的 waitStatus 改为 -1，再 for (;;) 循环一 次尝试 tryAcquireShared(1) 如果还不成功，那么在 parkAndCheckInterrupt() 处 park

![image-20211217153409061](\images\image-20211217153409061.png)

#### t3 r.lock，t4 w.lock

这种状态下，假设又有 t3 加读锁和 t4 加写锁，这期间 t1 仍然持有锁，就变成了下面的样子

![image-20211217153515303](\images\image-20211217153515303.png)

#### t1 w.unlock

这时会走到写锁的 sync.release(1) 流程，调用 sync.tryRelease(1) 成功，变成下面的样子

![image-20211217153622823](\images\image-20211217153622823.png)

接下来执行唤醒流程 sync.unparkSuccessor，即让老二恢复运行，这时 t2 在 doAcquireShared 内 parkAndCheckInterrupt() 处恢复运行

这回再来一次 for (;;) 执行 tryAcquireShared 成功则让读锁计数加一

![image-20211217154023140](\images\image-20211217154023140.png)

这时 t2 已经恢复运行，接下来 t2 调用 setHeadAndPropagate(node, 1)，它原本所在节点被置为头节点

![image-20211217154106774](\images\image-20211217154106774.png)

事情还没完，在 setHeadAndPropagate 方法内还会检查下一个节点是否是 shared，如果是则调用 doReleaseShared() 将 head 的状态从 -1 改为 0 并唤醒老二，这时 t3 在 doAcquireShared 内 parkAndCheckInterrupt() 处恢复运行

![image-20211217154632673](\images\image-20211217154632673.png)

这回再来一次 for (;;) 执行 tryAcquireShared 成功则让读锁计数加一

![image-20211217154722094](\images\image-20211217154722094.png)

这时 t3 已经恢复运行，接下来 t3 调用 setHeadAndPropagate(node, 1)，它原本所在节点被置为头节点

![image-20211217155025491](\images\image-20211217155025491.png)

下一个节点不是 shared 了，因此不会继续唤醒 t4 所在节点

#### t2 r.unlock，t3 r.unlock

t2 进入 sync.releaseShared(1) 中，调用 tryReleaseShared(1) 让计数减一，但由于计数还不为零

![image-20211217155547665](\images\image-20211217155547665.png)

t3 进入 sync.releaseShared(1) 中，调用 tryReleaseShared(1) 让计数减一，这回计数为零了，进入 doReleaseShared() 将头节点从 -1 改为 0 并唤醒老二，即

![image-20211217155709994](\images\image-20211217155709994.png)

之后 t4 在 acquireQueued 中 parkAndCheckInterrupt 处恢复运行，再次 for (;;) 这次自己是老二，并且没有其他 竞争，tryAcquire(1) 成功，修改头结点，流程结束

![image-20211217155743013](\images\image-20211217155743013.png)

### 读写锁应用

#### ReentrantReadWriteLock

当读操作远远高于写操作时，这时候使用 读写锁 让 读-读 可以并发，提高性能。 类似于数据库中的 select ... from ... lock in share mode

提供一个 数据容器类 内部分别使用读锁保护数据的 read() 方法，写锁保护数据的 write() 方法

```java
@Slf4j(topic = "c1.test")
public class DataContainer {
    private Object data;
    private ReentrantReadWriteLock rw = new ReentrantReadWriteLock();
    private ReentrantReadWriteLock.ReadLock r = rw.readLock();
    private ReentrantReadWriteLock.WriteLock w = rw.writeLock();

    public Object read() throws InterruptedException {
        log.debug("获取读锁。。。。");
        r.lock();
        try {
            log.debug("读取");
            sleep(1000);
            return data;
        }finally {
            log.debug("释放读锁");
            r.unlock();
        }
    }
    public void write() throws InterruptedException {
        log.debug("获取写锁...");
        w.lock();
        try {
            log.debug("写入");
            sleep(1000);
        } finally {
            log.debug("释放写锁...");
            w.unlock();
        }
    }

}
```

测试 读锁-读锁 可以并发

```java
public static void main(String[] args) {
    public static void main(String[] args) throws InterruptedException {
        DataContainer dataContainer = new DataContainer();
        log.debug("main test");
        new Thread(() ->{
            try {
                log.debug("t1 read");
                dataContainer.read();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        },"t1").start();
        new Thread(() ->{
            try {
                log.debug("t2 read");
                dataContainer.read();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        },"t2").start();

    }
```

输出结果，从这里可以看到 Thread-0 锁定期间，Thread-1 的读操作不受影响

```
16:30:27 [main] c.test - main test
16:30:27 [t1] c.test - t1 read
16:30:27 [t1] c.test - 获取读锁。。。。
16:30:27 [t1] c.test - 读取
16:30:27 [t1] c.test - 释放读锁
16:30:27 [t2] c.test - t2 read
16:30:27 [t2] c.test - 获取读锁。。。。
16:30:27 [t2] c.test - 读取
16:30:27 [t2] c.test - 释放读锁.

Process finished with exit code 0
```

测试 读锁-写锁 相互阻塞

```java
public static void main(String[] args) throws InterruptedException {
        DataContainer dataContainer = new DataContainer();
        log.debug("main test");
        new Thread(() ->{
            try {
                log.debug("t1 read");
                dataContainer.read();

            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        },"t1").start();
//        Thread.sleep(1000);
        new Thread(() ->{
            try {
                log.debug("t2 write");
                dataContainer.write();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        },"t2").start();

    }
```

```
16:33:45 [main] c.test - main test
16:33:45 [t1] c.test - t1 read
16:33:45 [t1] c.test - 获取读锁。。。。
16:33:45 [t1] c.test - 读取
16:33:45 [t2] c.test - t2 write
16:33:45 [t2] c.test - 获取写锁...
16:33:46 [t1] c.test - 释放读锁
16:33:46 [t2] c.test - 写入
16:33:47 [t2] c.test - 释放写锁...
```

#### 注意事项

读锁不支持条件变量，重入时升级不支持：即持有读锁的情况下去获取写锁，会导致获取写锁永久等待

重入时降级支持：即持有写锁的情况下去获取读锁

```java
public class CacheData {
    Object data;
    // 是否有效，如果失效，需要重新计算 data
    volatile boolean cacheValid;
    final ReentrantReadWriteLock rwl = new ReentrantReadWriteLock();

    void processCachedData() {
        rwl.readLock().lock();
        if (!cacheValid) {
            // 获取写锁前必须释放读锁
            rwl.readLock().unlock();
            rwl.writeLock().lock();
            try {
                // 判断是否有其它线程已经获取了写锁、更新了缓存, 避免重复更新
                if (!cacheValid) {
                    data = "...";
                    cacheValid = true;
                }
                // 降级为读锁, 释放写锁, 这样能够让其它线程读取缓存
                rwl.readLock().lock();
            } finally {
                rwl.writeLock().unlock();
            }
        }
    }
}
```

#### 源码分析

##### 写锁上锁流程

```java
static final class NonfairSync extends Sync {
    // ... 省略无关代码

    // 外部类 WriteLock 方法, 方便阅读, 放在此处
    public void lock() {
        sync.acquire(1);
    }

    // AQS 继承过来的方法, 方便阅读, 放在此处
    public final void acquire(int arg) {
        if (
            // 尝试获得写锁失败
                !tryAcquire(arg) &&
                        // 将当前线程关联到一个 Node 对象上, 模式为独占模式
                        // 进入 AQS 队列阻塞
                        acquireQueued(addWaiter(Node.EXCLUSIVE), arg)
        ) {
            selfInterrupt();
        }
    }

    // Sync 继承过来的方法, 方便阅读, 放在此处
    protected final boolean tryAcquire(int acquires) {
        // 获得低 16 位, 代表写锁的 state 计数
        Thread current = Thread.currentThread();
        int c = getState();
        int w = exclusiveCount(c);

        if (c != 0) {
            if (
                // c != 0 and w == 0 表示有读锁, 或者
                    w == 0 ||
                            // 如果 exclusiveOwnerThread 不是自己
                            current != getExclusiveOwnerThread()
            ) {
                // 获得锁失败
                return false;
            }
            // 写锁计数超过低 16 位, 报异常
            if (w + exclusiveCount(acquires) > MAX_COUNT)
                throw new Error("Maximum lock count exceeded");
            // 写锁重入, 获得锁成功
            setState(c + acquires);
            return true;
        }
        if (
            // 判断写锁是否该阻塞, 或者
                writerShouldBlock() ||
                        // 尝试更改计数失败
                        !compareAndSetState(c, c + acquires)
        ) {
            // 获得锁失败
            return false;
        }
        // 获得锁成功
        setExclusiveOwnerThread(current);
        return true;
    }

    // 非公平锁 writerShouldBlock 总是返回 false, 无需阻塞
    final boolean writerShouldBlock() {
        return false;
    }
}
```

##### 写锁释放流程

```java
static final class NonfairSync extends Sync {
    // ... 省略无关代码

    // WriteLock 方法, 方便阅读, 放在此处
    public void unlock() {
        sync.release(1);
    }

    // AQS 继承过来的方法, 方便阅读, 放在此处
    public final boolean release(int arg) {
        // 尝试释放写锁成功
        if (tryRelease(arg)) {
            // unpark AQS 中等待的线程
            Node h = head;
            if (h != null && h.waitStatus != 0)
                unparkSuccessor(h);
            return true;
        }
        return false;
    }

    // Sync 继承过来的方法, 方便阅读, 放在此处
    protected final boolean tryRelease(int releases) {
        if (!isHeldExclusively())
            throw new IllegalMonitorStateException();
        int nextc = getState() - releases;
        // 因为可重入的原因, 写锁计数为 0, 才算释放成功
        boolean free = exclusiveCount(nextc) == 0;
        if (free) {
            setExclusiveOwnerThread(null);
        }
        setState(nextc);
        return free;
    }
}
```

##### 读锁上锁流程

```java
static final class NonfairSync extends Sync {

    // ReadLock 方法, 方便阅读, 放在此处
    public void lock() {
        sync.acquireShared(1);
    }

    // AQS 继承过来的方法, 方便阅读, 放在此处
    public final void acquireShared(int arg) {
        // tryAcquireShared 返回负数, 表示获取读锁失败
        if (tryAcquireShared(arg) < 0) {
            doAcquireShared(arg);
        }
    }

    // Sync 继承过来的方法, 方便阅读, 放在此处
    protected final int tryAcquireShared(int unused) {
        Thread current = Thread.currentThread();
        int c = getState();
        // 如果是其它线程持有写锁, 获取读锁失败
        if (
                exclusiveCount(c) != 0 &&
                        getExclusiveOwnerThread() != current
        ) {
            return -1;
        }
        int r = sharedCount(c);
        if (
            // 读锁不该阻塞(如果老二是写锁，读锁该阻塞), 并且
                !readerShouldBlock() &&
                        // 小于读锁计数, 并且
                        r < MAX_COUNT &&
                        // 尝试增加计数成功
                        compareAndSetState(c, c + SHARED_UNIT)
        ) {
            // ... 省略不重要的代码
            return 1;
        }
        return fullTryAcquireShared(current);
    }

    // 非公平锁 readerShouldBlock 看 AQS 队列中第一个节点是否是写锁
    // true 则该阻塞, false 则不阻塞
    final boolean readerShouldBlock() {
        return apparentlyFirstQueuedIsExclusive();
    }

    // AQS 继承过来的方法, 方便阅读, 放在此处
    // 与 tryAcquireShared 功能类似, 但会不断尝试 for (;;) 获取读锁, 执行过程中无阻塞
    final int fullTryAcquireShared(Thread current) {
        HoldCounter rh = null;
        for (;;) {
            int c = getState();
            if (exclusiveCount(c) != 0) {
                if (getExclusiveOwnerThread() != current)
                    return -1;
            } else if (readerShouldBlock()) {
                // ... 省略不重要的代码
            }
            if (sharedCount(c) == MAX_COUNT)
                throw new Error("Maximum lock count exceeded");
            if (compareAndSetState(c, c + SHARED_UNIT)) {
                // ... 省略不重要的代码
                return 1;
            }
        }
    }

    // AQS 继承过来的方法, 方便阅读, 放在此处
    private void doAcquireShared(int arg) {
        // 将当前线程关联到一个 Node 对象上, 模式为共享模式
        final Node node = addWaiter(Node.SHARED);
        boolean failed = true;
        try {
            boolean interrupted = false;
            for (;;) {
                final Node p = node.predecessor();
                if (p == head) {
                    // 再一次尝试获取读锁
                    int r = tryAcquireShared(arg);
                    // 成功
                    if (r >= 0) {
                        // ㈠
// r 表示可用资源数, 在这里总是 1 允许传播
                        //（唤醒 AQS 中下一个 Share 节点）
                        setHeadAndPropagate(node, r);
                        p.next = null; // help GC
                        if (interrupted)
                            selfInterrupt();
                        failed = false;
                        return;
                    }
                }
                if (
                    // 是否在获取读锁失败时阻塞（前一个阶段 waitStatus == Node.SIGNAL）
                        shouldParkAfterFailedAcquire(p, node) &&
                                // park 当前线程
                                parkAndCheckInterrupt()
                ) {
                    interrupted = true;
                }
            }
        } finally {
            if (failed)
                cancelAcquire(node);
        }
    }

    // ㈠ AQS 继承过来的方法, 方便阅读, 放在此处
    private void setHeadAndPropagate(Node node, int propagate) {
        Node h = head; // Record old head for check below
        // 设置自己为 head
        setHead(node);

        // propagate 表示有共享资源（例如共享读锁或信号量）
        // 原 head waitStatus == Node.SIGNAL 或 Node.PROPAGATE
        // 现在 head waitStatus == Node.SIGNAL 或 Node.PROPAGATE
        if (propagate > 0 || h == null || h.waitStatus < 0 ||
                (h = head) == null || h.waitStatus < 0) {
            Node s = node.next;
            // 如果是最后一个节点或者是等待共享读锁的节点
            if (s == null || s.isShared()) {
                // 进入 ㈡
                doReleaseShared();
            }
        }
    }

    // ㈡ AQS 继承过来的方法, 方便阅读, 放在此处
    private void doReleaseShared() {
        // 如果 head.waitStatus == Node.SIGNAL ==> 0 成功, 下一个节点 unpark
        // 如果 head.waitStatus == 0 ==> Node.PROPAGATE, 为了解决 bug, 见后面分析
        for (;;) {
            Node h = head;
            // 队列还有节点
            if (h != null && h != tail) {
                int ws = h.waitStatus;
                if (ws == Node.SIGNAL) {
                    if (!compareAndSetWaitStatus(h, Node.SIGNAL, 0))
                        continue; // loop to recheck cases
                    // 下一个节点 unpark 如果成功获取读锁
                    // 并且下下个节点还是 shared, 继续 doReleaseShared
                    unparkSuccessor(h);
                }
                else if (ws == 0 &&
                        !compareAndSetWaitStatus(h, 0, Node.PROPAGATE))
                    continue; // loop on failed CAS
            }
            if (h == head) // loop if head changed
                break;
        }
    }
}
```

##### 读锁释放流程

```java
static final class NonfairSync extends Sync {

    // ReadLock 方法, 方便阅读, 放在此处
    public void unlock() {
        sync.releaseShared(1);
    }

    // AQS 继承过来的方法, 方便阅读, 放在此处
    public final boolean releaseShared(int arg) {
        if (tryReleaseShared(arg)) {
            doReleaseShared();
            return true;
        }
        return false;
    }

    // Sync 继承过来的方法, 方便阅读, 放在此处
    protected final boolean tryReleaseShared(int unused) {
        // ... 省略不重要的代码
        for (;;) {
            int c = getState();
            int nextc = c - SHARED_UNIT;
            if (compareAndSetState(c, nextc)) {
                // 读锁的计数不会影响其它获取读锁线程, 但会影响其它获取写锁线程
                // 计数为 0 才是真正释放
                return nextc == 0;
            }
        }
    }

    // AQS 继承过来的方法, 方便阅读, 放在此处
    private void doReleaseShared() {
        // 如果 head.waitStatus == Node.SIGNAL ==> 0 成功, 下一个节点 unpark
        // 如果 head.waitStatus == 0 ==> Node.PROPAGATE 
        for (;;) {
            Node h = head;
            if (h != null && h != tail) {
                int ws = h.waitStatus;
                // 如果有其它线程也在释放读锁，那么需要将 waitStatus 先改为 0
                // 防止 unparkSuccessor 被多次执行
                if (ws == Node.SIGNAL) {
                    if (!compareAndSetWaitStatus(h, Node.SIGNAL, 0))
                        continue; // loop to recheck cases
                    unparkSuccessor(h);
                }
                // 如果已经是 0 了，改为 -3，用来解决传播性，见后文信号量 bug 分析
                else if (ws == 0 &&
                        !compareAndSetWaitStatus(h, 0, Node.PROPAGATE))
                    continue; // loop on failed CAS
            }
            if (h == head) // loop if head changed
                break;
        }
    }
}
```

## 4、StampedLock

该类自 JDK 8 加入，是为了进一步优化读性能，它的特点是在使用读锁、写锁时都必须配合【戳】使用

加解读锁

```java
long stamp = lock.readLock();
lock.unlockRead(stamp);
```

加解写锁

```java
long stamp = lock.writeLock();
lock.unlockWrite(stamp);
```

乐观读，StampedLock 支持 tryOptimisticRead() 方法（乐观读），读取完毕后需要做一次 戳校验 如果校验通 过，表示这期间确实没有写操作，数据可以安全使用，如果校验没通过，需要重新获取读锁，保证数据安全。

提供一个 数据容器类 内部分别使用读锁保护数据的 read() 方法，写锁保护数据的 write() 方法

```java
@Slf4j(topic = "c.test")
public class DataContainerStamped {
    private int data;

    private final StampedLock lock = new StampedLock();

    public DataContainerStamped(int data){
        this.data = data;
    }

    public int read(int readTime) throws InterruptedException {
        long stamp = lock.tryOptimisticRead();
        log.debug("optimistic read locking...{}", stamp);
        sleep(readTime);
        if (lock.validate(stamp)) {
            log.debug("read finish...{}, data:{}", stamp, data);
            return data;
        }
        // 锁升级 - 读锁
        log.debug("updating to read lock... {}", stamp);
        try {
            stamp = lock.readLock();
            log.debug("read lock {}", stamp);
            sleep(readTime);
            log.debug("read finish...{}, data:{}", stamp, data);
            return data;
        } finally {
            log.debug("read unlock {}", stamp);
            lock.unlockRead(stamp);
        }
        
    }

    public void write(int newData) {
        long stamp = lock.writeLock();
        log.debug("write lock {}", stamp);
        try {
            try {
                sleep(2000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            this.data = newData;
        } finally {
            log.debug("write unlock {}", stamp);
            lock.unlockWrite(stamp);
        }
    }


}
```

测试 读-读 可以优化

```java
public static void main(String[] args) throws InterruptedException {
    DataContainerStamped dataContainer = new DataContainerStamped(1);
    new Thread(() -> {
        try {
            dataContainer.read(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }, "t1").start();
    sleep(500);
    new Thread(() -> {
        try {
            dataContainer.read(0);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }, "t2").start();
}
```

输出结果，可以看到实际没有加读锁

```
16:10:19 [t1] c.test - optimistic read locking...256
16:10:19 [t2] c.test - optimistic read locking...256
16:10:19 [t2] c.test - read finish...256, data:1
16:10:20 [t1] c.test - read finish...256, data:1
```

测试 读-写 时优化读补加读锁

```java
public static void main(String[] args) throws InterruptedException {
    DataContainerStamped dataContainer = new DataContainerStamped(1);
    new Thread(() -> {
        try {
            dataContainer.read(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }, "t1").start();
    sleep(500);
    new Thread(() -> {
        dataContainer.write(3000);
    }, "t2").start();
}
```

输出结果

```
16:12:40 [t1] c.test - optimistic read locking...256
16:12:40 [t2] c.test - write lock 384
16:12:41 [t1] c.test - updating to read lock... 256
16:12:42 [t2] c.test - write unlock 384
16:12:42 [t1] c.test - read lock 513
16:12:43 [t1] c.test - read finish...513, data:3000
16:12:43 [t1] c.test - read unlock 513
```

注意 StampedLock 不支持条件变量 StampedLock 不支持可重入

## 5、Semaphore

### 基本使用

```java
@Slf4j(topic = "c.test")
public class TestSemaphore {
    public static void main(String[] args) {
        // 1. 创建 semaphore 对象
        Semaphore semaphore = new Semaphore(3);
        // 2. 10个线程同时运行
        for (int i = 0; i < 10; i++) {
            new Thread(() -> {
                // 3. 获取许可
                try {
                    semaphore.acquire();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                try {
                    log.debug("running...");
                    try {
                        sleep(1000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    log.debug("end...");
                } finally {
                    // 4. 释放许可
                    semaphore.release();
                }
            }).start();
        }
    }

}
```

输出

```
16:41:33 [Thread-0] c.test - running...
16:41:33 [Thread-2] c.test - running...
16:41:33 [Thread-1] c.test - running...
16:41:34 [Thread-2] c.test - end...
16:41:34 [Thread-3] c.test - running...
16:41:34 [Thread-0] c.test - end...
16:41:34 [Thread-1] c.test - end...
16:41:34 [Thread-7] c.test - running...
16:41:34 [Thread-6] c.test - running...
16:41:35 [Thread-7] c.test - end...
16:41:35 [Thread-4] c.test - running...
16:41:35 [Thread-6] c.test - end...
16:41:35 [Thread-5] c.test - running...
16:41:35 [Thread-3] c.test - end...
16:41:35 [Thread-8] c.test - running...
16:41:36 [Thread-8] c.test - end...
16:41:36 [Thread-5] c.test - end...
16:41:36 [Thread-9] c.test - running...
16:41:36 [Thread-4] c.test - end...
16:41:37 [Thread-9] c.test - end...

Process finished with exit code 0
```

### Semaphore 原理

#### 加锁解锁流程

Semaphore 有点像一个停车场，permits 就好像停车位数量，当线程获得了 permits 就像是获得了停车位，然后 停车场显示空余车位减一 刚开始，permits（state）为 3，这时 5 个线程来获取资源

![image-20211221164454903](\images\image-20211221164454903.png)

假设其中 Thread-1，Thread-2，Thread-4 cas 竞争成功，而 Thread-0 和 Thread-3 竞争失败，进入 AQS 队列 park 阻塞

![image-20211221164527042](\images\image-20211221164527042.png)

这时 Thread-4 释放了 permits，状态如下

![image-20211221164606039](\images\image-20211221164606039.png)

接下来 Thread-0 竞争成功，permits 再次设置为 0，设置自己为 head 节点，断开原来的 head 节点，unpark 接 下来的 Thread-3 节点，但由于 permits 是 0，因此 Thread-3 在尝试不成功后再次进入 park 状态

## 6、 CountdownLatch

用来进行线程同步协作，等待所有线程完成倒计时。 其中构造参数用来初始化等待计数值，await() 用来等待计数归零，countDown() 用来让计数减一

```java
@Slf4j(topic = "c.test")
public class CountdownLatchTest {
    public static void main(String[] args) throws InterruptedException {
        CountDownLatch lathch = new CountDownLatch(3);
        new Thread(() ->{
            try {
                log.debug("begin...");
                Thread.sleep(1000);
                lathch.countDown();
                log.debug("end...{}", lathch.getCount());
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }).start();

        new Thread(() ->{
            try {
                log.debug("begin...");
                Thread.sleep(2000);
                lathch.countDown();
                log.debug("end...{}", lathch.getCount());
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }).start();

        new Thread(() ->{
            try {
                log.debug("begin...");
                Thread.sleep(1500);
                lathch.countDown();
                log.debug("end...{}", lathch.getCount());
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }).start();
        log.debug("waiting...");
        lathch.await();
        log.debug("wait end...");
    }

}
```

输出

```
17:56:44 [main] c.test - waiting...
17:56:44 [Thread-1] c.test - begin...
17:56:44 [Thread-0] c.test - begin...
17:56:44 [Thread-2] c.test - begin...
17:56:45 [Thread-0] c.test - end...2
17:56:45 [Thread-2] c.test - end...1
17:56:46 [Thread-1] c.test - end...0
17:56:46 [main] c.test - wait end...
```

可以配合线程池使用，改进如下

```java
@Slf4j(topic = "c.test")
public class CountdownLatchTest {
    public static void main(String[] args) throws InterruptedException {
        CountDownLatch latch = new CountDownLatch(3);
        ExecutorService service = Executors.newFixedThreadPool(4);
        service.submit(() -> {
            log.debug("begin...");
            try {
                sleep(1);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            latch.countDown();
            log.debug("end...{}", latch.getCount());
        });
        service.submit(() -> {
            log.debug("begin...");
            try {
                sleep((long) 1.5);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            latch.countDown();
            log.debug("end...{}", latch.getCount());
        });
        service.submit(() -> {
            log.debug("begin...");
            try {
                sleep(2);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            latch.countDown();
            log.debug("end...{}", latch.getCount());
        });
        service.submit(()->{
            try {
                log.debug("waiting...");
                latch.await();
                log.debug("wait end...");
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });

    }

}
```

### 应用之同步等待多线程准备完毕

```java
public class CountdownLatchTest2 {
    public static void main(String[] args) throws InterruptedException {
        AtomicInteger num = new AtomicInteger();
        ExecutorService service = Executors.newFixedThreadPool(10, (r) -> {
            return new Thread(r, "t" + num.getAndIncrement());
        });

        CountDownLatch countDownLatch = new CountDownLatch(10);
        String[] all = new String[10];
        Random r = new Random();
        for (int j=0; j < 10; j++){
            int x = j;
            service.submit(() -> {
                for (int i = 0; i <= 100; i++) {
                    try {
                        Thread.sleep(r.nextInt(100));
                    } catch (InterruptedException e) {
                    }
                    all[x] = Thread.currentThread().getName() + "(" + (i + "%") + ")";
                    System.out.print("\r" + Arrays.toString(all));
                }
                countDownLatch.countDown();
            });
        }
        countDownLatch.await();
        System.out.println("\n游戏开始...");
        service.shutdown();
}}
```

要等待到所有线程到100后打印游戏开始

```
[t0(100%), t1(100%), t2(100%), t3(100%), t4(100%), t5(100%), t6(100%), t7(100%), t8(100%), t9(100%)]
游戏开始...
```

