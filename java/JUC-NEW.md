# 一 并发理念

##  1、Java多线程相关概念

### 进程

是程序的⼀次执⾏，是系统进⾏资源分配和调度的独⽴单位，每⼀个进程都有它⾃⼰的内存空间和系统资源

进程（Process）是计算机中的程序关于某数据集合上的一次运行活动，是系统进行资源分配和调度的基本单位，是操作系统结构的基础。程序是指令、数据及其组织形式的描述，进程是程序的实体。

**进程具有的特征：**

- **动态性**：进程是程序的一次执行过程，是临时的，有生命期的，是动态产生，动态消亡的
- **并发性**：任何进程都可以同其他进行一起并发执行
- **独立性**：进程是系统进行资源分配和调度的一个独立单位
- **结构性**：进程由程序，数据和进程控制块三部分组成

我们经常使用windows系统，经常会看见.exe后缀的文件，双击这个.exe文件的时候，这个文件中的指令就会被系统加载，那么我们就能得到一个关于这个.exe程序的进程。进程是**“活”**的，或者说是正在被执行的。

### 线程

在同⼀个进程内⼜可以执⾏多个任务，⽽这每⼀个任务我们就可以看做是⼀个线程 ⼀个进程会有1个或多个线程的

线程是轻量级的进程，是程序执行的最小单元，使用多线程而不是多进程去进行并发程序的设计，是因为线程间的切换和调度的成本远远小于进程。

### 进程与线程的一个简单解释

进程（process）和线程（thread）是操作系统的基本概念，但是它们比较抽象，不容易掌握。

1.计算机的核心是CPU，它承担了所有的计算任务。它就像一座工厂，时刻在运行。

2.假定工厂的电力有限，一次只能供给一个车间使用。也就是说，一个车间开工的时候，其他车间都必须停工。背后的含义就是，单个CPU一次只能运行一个任务。

3.进程就好比工厂的车间，它代表CPU所能处理的单个任务。任一时刻，CPU总是运行一个进程，其他进程处于非运行状态。

### 管程

Monitor(监视器)，也就是我们平时所说的锁

```java
// Monitor其实是一种同步机制，他的义务是保证（同一时间）只有一个线程可以访问被保护的数据和代码。
// JVM中同步是基于进入和退出监视器对象(Monitor,管程对象)来实现的，每个对象实例都会有一个Monitor对象，
Object o = new Object();
new Thread(() -> {
    synchronized (o){}
},"t1").start();
// Monitor对象会和Java对象一同创建并销毁，它底层是由C++语言来实现的。
```

### 线程状态

```java
// Thread.State
public enum State {
    NEW,(新建)
    RUNNABLE,（准备就绪）
    BLOCKED,（阻塞）
    WAITING,（不见不散）
    TIMED_WAITING,（过时不候）
    TERMINATED;(终结)
}
```

线程几个状态的介绍：

- **New**：表示刚刚创建的线程，这种线程还没有开始执行
- **RUNNABLE**：运行状态，线程的start()方法调用后，线程会处于这种状态
- **BLOCKED**：阻塞状态。当线程在执行的过程中遇到了synchronized同步块，但这个同步块被其他线程已获取还未释放时，当前线程将进入阻塞状态，会暂停执行，直到获取到锁。当线程获取到锁之后，又会进入到运行状态（RUNNABLE）
- **WAITING**：等待状态。和**TIME_WAITING**都表示等待状态，区别是WAITING会进入一个无时间限制的等，而TIME_WAITING会进入一个有限的时间等待，那么等待的线程究竟在等什么呢？一般来说，WAITING的线程正式在等待一些特殊的事件，比如，通过wait()方法等待的线程在等待notify()方法，而通过join()方法等待的线程则会等待目标线程的终止。一旦等到期望的事件，线程就会再次进入RUNNABLE运行状态。
- **TERMINATED**：表示结束状态，线程执行完毕之后进入结束状态。

**注意：从NEW状态出发后，线程不能在回到NEW状态，同理，处理TERMINATED状态的线程也不能在回到RUNNABLE状态**

### wait/sleep的区别？

功能都是当前线程暂停，有什么区别？

wait放开手去睡，放开手里的锁

sleep握紧手去睡，醒了手里还有锁

## 2、线程的基本操作

### 新建线程

```java
public class ThreadTest1 extends Thread{
    @Override
    public void run() {
        System.out.println("当前线程："+Thread.currentThread().getName());
    }

    public static void main(String[] args) {
        ThreadTest1 threadTest1 = new ThreadTest1();
        threadTest1.start();
        
    }
}

```

**start方法是启动一个线程，run方法只会在垫钱线程中串行的执行run方法中的代码。**

默认情况下， 线程的run方法什么都没有，启动一个线程之后马上就结束了，所以如果你需要线程做点什么，需要把代码写到run方法中，所以必须重写run方法。

通过匿名内部类实现线程

```java
public class ThreadTest2 {
    public static void main(String[] args) {
        Thread t1 = new Thread(() -> {
            System.out.println("线程："+ Thread.currentThread().getName());
        },"T1");
        t1.start();
    }

}

```

### 终止线程

一般来说线程执行完毕就会结束，无需手动关闭。但是如果我们想关闭一个正在运行的线程，有什么方法呢？可以看一下Thread类中提供了一个stop()方法，调用这个方法，就可以立即将一个线程终止，非常方便。

```java
@Slf4j
public class Demo01 {
    public static void main(String[] args) throws InterruptedException {
        Thread thread1 = new Thread() {
            @Override
            public void run() {
                log.info("start");
                boolean flag = true;
                while (flag) {
                    ;
                }
                log.info("end");
            }
        };
        thread1.setName("thread1");
        thread1.start();
        //当前线程休眠1秒
        TimeUnit.SECONDS.sleep(1);
        //关闭线程thread1
        thread1.stop();
        //输出线程thread1的状态
        log.info("{}", thread1.getState());
        //当前线程休眠1秒
        TimeUnit.SECONDS.sleep(1);
        //输出线程thread1的状态
        log.info("{}", thread1.getState());
    }
}
```

### 线程中断

在java中，线程中断是一种重要的线程写作机制，从表面上理解，中断就是让目标线程停止执行的意思，实际上并非完全如此。在上面中，我们已经详细讨论了stop方法停止线程的坏处，jdk中提供了更好的中断线程的方法。严格的说，线程中断并不会使线程立即退出，而是给线程发送一个通知，告知目标线程，有人希望你退出了！至于目标线程接收到通知之后如何处理，则完全由目标线程自己决定，这点很重要，如果中断后，线程立即无条件退出，我们又会到stop方法的老问题。

Thread提供了3个与线程中断有关的方法，这3个方法容易混淆，大家注意下：

```java
public void interrupt() //中断线程
public boolean isInterrupted() //判断线程是否被中断
public static boolean interrupted()  //判断线程是否被中断，并清除当前中断状态
```

**interrupt()方法是一个实例方法**，它通知目标线程中断，也就是设置中断标志位为true，中断标志位表示当前线程已经被中断了。

**isInterrupted()方法也是一个实例方法**，它判断当前线程是否被中断（通过检查中断标志位）。

最后一个方法**interrupted()是一个静态方法**，返回boolean类型，也是用来判断当前线程是否被中断，但是同时会清除当前线程的中断标志位的状态。

```java
ublic class ThreadTest2 {
    public static void main(String[] args) throws InterruptedException {
        Thread t1 = new Thread(() -> {
            try {
                sleep(5000);
                System.out.println("线程："+ Thread.currentThread().getName());
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        },"T1");


        while (true){
            if (t1.isInterrupted()){
                System.out.println("线程退出");
                break;
            }
        }
        t1.start();
        TimeUnit.SECONDS.sleep(2);
        t1.interrupt();

    }

}
```

上面代码中有个死循环，interrupt()方法被调用之后，线程的中断标志将被置为true，循环体中通过检查线程的中断标志是否为ture（`this.isInterrupted()`）来判断线程是否需要退出了。

再看一种中断的方法：

```java
       Thread t1 = new Thread() {
            @Override
            public void run() {
                while (true) {
                    //休眠100秒
                    try {
                        TimeUnit.SECONDS.sleep(100);
                    } catch (InterruptedException e) {
                        this.interrupt();
                        e.printStackTrace();
                    }
                    if (this.isInterrupted()) {
                        System.out.println("我要退出了!");
                        break;
                    }
                }
            }
        };
        t1.start();
        t1.interrupt();
    }
```

上面代码可以终止。

**注意：sleep方法由于中断而抛出异常之后，线程的中断标志会被清除（置为false），所以在异常中需要执行this.interrupt()方法，将中断标志位置为true**

### 等待（wait）和通知（notify）

为了支持多线程之间的协作，JDK提供了两个非常重要的方法：等待wait()方法和通知notify()方法。这2个方法并不是在Thread类中的，而是在Object类中定义的。这意味着所有的对象都可以调用者两个方法。

如果一个线程调用了object.wait()方法，那么它就会进出object对象的等待队列。这个队列中，可能会有多个线程，因为系统可能运行多个线程同时等待某一个对象。当object.notify()方法被调用时，它就会从这个队列中随机选择一个线程，并将其唤醒。这里希望大家注意一下，这个选择是不公平的，并不是先等待线程就会优先被选择，这个选择完全是随机的。

除notify()方法外，Object独享还有一个nofiyAll()方法，它和notify()方法的功能类似，不同的是，它会唤醒在这个等待队列中所有等待的线程，而不是随机选择一个。

```java

public class ThreadWaitNotify {

    public static Object object = new Object();
    public static void main(String[] args) {

        Thread t1 = new Thread(() -> {
            try {
                synchronized(object){
                    System.out.println(Thread.currentThread().getName()+"wait");
                    object.wait();
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }, "t1");

        Thread t2 = new Thread(() -> {
            synchronized(object){
                try {
                    TimeUnit.SECONDS.sleep(10 );
                    System.out.println(Thread.currentThread().getName() + "notify");
                    object.notify();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }, "t2");
        t1.start();
        t2.start();

    }
}

```

### 用户线程和守护线程

Java线程分为用户线程和守护线程，线程的daemon属性为true表示是守护线程，false表示是用户线程

守护线程是一种特殊的线程，在后台默默地完成一些系统性的服务，比如垃圾回收线程

用户线程是系统的工作线程，它会完成这个程序需要完成的业务操作

```java
public class DaemonDemo {

    public static void main(String[] args) {
        Thread t1 = new Thread(() -> {
            System.out.println(Thread.currentThread().getName() + "\t 开始运行，" + (Thread.currentThread().isDaemon() ? "守护线程" : "用户线程"));
            while (true) {

            }
        }, "t1");

        //线程的daemon属性为true表示是守护线程，false表示是用户线程
        t1.setDaemon(true);
        t1.start();

        //3秒钟后主线程再运行
        try {
            TimeUnit.SECONDS.sleep(3);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("----------main线程运行完毕");
    }

}
```

重点

当程序中所有用户线程执行完毕之后，不管守护线程是否结束，系统都会自动退出

如果用户线程全部结束了，意味着程序需要完成的业务操作已经结束了，系统可以退出了。所以当系统只剩下守护进程的时候，java虚拟机会自动退出

设置守护线程，需要在**start()方法之前**进

### Callable接口

#### 与runnable对比

```java
// 创建新类MyThread实现runnable接口
class MyThread implements Runnable{
 @Override
 public void run() {
 
 }
}
// 新类MyThread2实现callable接口
class MyThread2 implements Callable<Integer>{
 @Override
 public Integer call() throws Exception {
  return 200;
 } 
}
// 面试题:callable接口与runnable接口的区别？
 
// 答：（1）是否有返回值
//     （2）是否抛异常
//    （3）落地方法不一样，一个是run，一个是call

```

直接替换runnable是否可行？

![image-20221101204833750](images\image-20221101204833750.png)

不可行，因为：thread类的构造方法根本没有Callable

![image-20221101204858224](images\image-20221101204858224.png)

认识不同的人找中间人

![image-20221101204924328](images\image-20221101204924328.png)

```java
public class ThreadCallable {
    public static <V> void main(String[] args) throws ExecutionException, InterruptedException {
        FutureTask<Integer> futureTask = new FutureTask<>(() -> {
            System.out.println("This Callable");
            TimeUnit.SECONDS.sleep(5);
            return 100;
        });
        futureTask.run();
        while (futureTask.isDone()){
            Integer result = futureTask.get();
            if (result!=null){
                System.out.println(result);
                break;
            }
        }
    }
}

```

运行成功后如何获得返回值？

![image-20221101205839090](images\image-20221101205839090.png)

# 二 线程池

## 1、什么是线程池

线程池和数据库连接池的原理也差不多，创建线程去处理业务，可能创建线程的时间比处理业务的时间还长一些，如果系统能够提前为我们创建好线程，我们需要的时候直接拿来使用，用完之后不是直接将其关闭，而是将其返回到线程中中，给其他需要这使用，这样直接节省了创建和销毁的时间，提升了系统的性能。

## 2、线程池的使用

### Executors.newFixedThreadPool(int)

newFixedThreadPool创建的线程池corePoolSize和maximumPoolSize值是相等的，它使用的是LinkedBlockingQueue执行长期任务性能好，创建一个线程池，一池有N个固定的线程，有固定线程数的线程

```java
public static ExecutorService newFixedThreadPool(int nThreads) {
    return new ThreadPoolExecutor(nThreads, nThreads,
                                  0L, TimeUnit.MILLISECONDS,
                                  new LinkedBlockingQueue<Runnable>());
}

```

```java
blic class ThreadPool1 {

    public static void main(String[] args) {
        ExecutorService pool1 = Executors.newFixedThreadPool(2);
        LocalDateTime localDateTime = LocalDateTime.now();
        System.out.println(localDateTime);
        SimpleDateFormat format=new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

        for (int i = 0; i < 10; i++) {
            Future<?> task1 = pool1.submit(() -> {
                try {
                    TimeUnit.SECONDS.sleep(2);
                    System.out.println(format.format(new Date())+":"+Thread.currentThread().getName());
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            });
        }



    }
}
```

![image-20221102203124594](images\image-20221102203124594.png)

### Executors.newSingleThreadExecutor()

 newSingleThreadExecutor 创建的线程池corePoolSize和maximumPoolSize值都是1，它使用的是LinkedBlockingQueue一个任务一个任务的执行，一池一线程

```java
public static ExecutorService newSingleThreadExecutor() {
    return new FinalizableDelegatedExecutorService
        (new ThreadPoolExecutor(1, 1,
                                0L, TimeUnit.MILLISECONDS,
                                new LinkedBlockingQueue<Runnable>()));
}

```

```java
 ExecutorService pool2 = Executors.newSingleThreadExecutor();

        LocalDateTime localDateTime = LocalDateTime.now();
        System.out.println(localDateTime);
        SimpleDateFormat format=new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

        for (int i = 0; i < 10; i++) {
            Future<?> task1 = pool2.submit(() -> {
                try {
                    TimeUnit.SECONDS.sleep(2);
                    System.out.println(format.format(new Date())+":"+Thread.currentThread().getName());
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            });
        }

```

![image-20221102203511430](images\image-20221102203511430.png)

### Executors.newCachedThreadPool()

 newCachedThreadPool创建的线程池将corePoolSize设置为0，将maximumPoolSize设置为Integer.MAX_VALUE，它使用的是SynchronousQueue，也就是说来了任务就创建线程运行，当线程空闲超过60秒，就销毁线程。

执行很多短期异步任务，线程池根据需要创建新线程，但在先前构建的线程可用时将重用它们。可扩容，遇强则强

```java
public static ExecutorService newCachedThreadPool() {
    return new ThreadPoolExecutor(0, Integer.MAX_VALUE,
                                  60L, TimeUnit.SECONDS,
                                  new SynchronousQueue<Runnable>());
}
```

```java
     ExecutorService pool3 = Executors.newCachedThreadPool();

        LocalDateTime localDateTime = LocalDateTime.now();
        System.out.println(localDateTime);
        SimpleDateFormat format=new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

        for (int i = 0; i < 10; i++) {
            Future<?> task1 = pool3.submit(() -> {
                try {
                    TimeUnit.SECONDS.sleep(2);
                    System.out.println(format.format(new Date())+":"+Thread.currentThread().getName());
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            });
        }
```

![image-20221102203720071](images\image-20221102203720071.png)

### ThreadPoolExecutor底层原理

![image-20221102203757027](images\image-20221102203757027.png)

```java
public ThreadPoolExecutor(int corePoolSize,
                          int maximumPoolSize,
                          long keepAliveTime,
                          TimeUnit unit,
                          BlockingQueue<Runnable> workQueue,
                          ThreadFactory threadFactory,
                          RejectedExecutionHandler handler) {
    if (corePoolSize < 0 ||
        maximumPoolSize <= 0 ||
        maximumPoolSize < corePoolSize ||
        keepAliveTime < 0)
        throw new IllegalArgumentException();
    if (workQueue == null || threadFactory == null || handler == null)
        throw new NullPointerException();
    this.corePoolSize = corePoolSize;
    this.maximumPoolSize = maximumPoolSize;
    this.workQueue = workQueue;
    this.keepAliveTime = unit.toNanos(keepAliveTime);
    this.threadFactory = threadFactory;
    this.handler = handler;
}

```

1. corePoolSize：核心线程大小，当提交一个任务到线程池时，线程池会创建一个线程来执行任务，即使有其他空闲线程可以处理任务也会创新线程，等到工作的线程数大于核心线程数时就不会在创建了。如果调用了线程池的`prestartAllCoreThreads`方法，线程池会提前把核心线程都创造好，并启动
2. maximumPoolSize：线程池允许创建的最大线程数，此值必须大于等于1。如果队列满了，并且以创建的线程数小于最大线程数，则线程池会再创建新的线程执行任务。如果我们使用了无界队列，那么所有的任务会加入队列，这个参数就没有什么效果了
3. keepAliveTime：多余的空闲线程的存活时间,当前池中线程数量超过corePoolSize时，当空闲时间,达到keepAliveTime时，多余线程会被销毁直到只剩下corePoolSize个线程为止，如果任务很多，并且每个任务的执行时间比较短，避免线程重复创建和回收，可以调大这个时间，提高线程的利用率
4. unit：keepAliveTIme的时间单位，可以选择的单位有天、小时、分钟、毫秒、微妙、千分之一毫秒和纳秒。类型是一个枚举`java.util.concurrent.TimeUnit`，这个枚举也经常使用
5. workQueue：任务队列，被提交但尚未被执行的任务，用于缓存待处理任务的阻塞队列
6. threadFactory：表示生成线程池中工作线程的线程工厂，用于创建线程，一般默认的即可，可以通过线程工厂给每个创建出来的线程设置更有意义的名字
7. handler：拒绝策略，表示当队列满了，并且工作线程大于等于线程池的最大线程数（maximumPoolSize）时如何来拒绝请求执行的runnable的策略

**调用线程池的execute方法处理任务，执行execute方法的过程：**

1. 判断线程池中运行的线程数是否小于corepoolsize，是：则创建新的线程来处理任务，否：执行下一步
2. 试图将任务添加到workQueue指定的队列中，如果无法添加到队列，进入下一步
3. 判断线程池中运行的线程数是否小于`maximumPoolSize`，是：则新增线程处理当前传入的任务，否：将任务传递给`handler`对象`rejectedExecution`方法处理

```text
1、在创建了线程池后，开始等待请求。
2、当调用execute()方法添加一个请求任务时，线程池会做出如下判断：
  2.1如果正在运行的线程数量小于corePoolSize，那么马上创建线程运行这个任务；
  2.2如果正在运行的线程数量大于或等于corePoolSize，那么将这个任务放入队列；
  2.3如果这个时候队列满了且正在运行的线程数量还小于maximumPoolSize，那么还是要创建非核心线程立刻运行这个任务；
  2.4如果队列满了且正在运行的线程数量大于或等于maximumPoolSize，那么线程池会启动饱和拒绝策略来执行。
3、当一个线程完成任务时，它会从队列中取下一个任务来执行。
4、当一个线程无事可做超过一定的时间（keepAliveTime）时，线程会判断：
    如果当前运行的线程数大于corePoolSize，那么这个线程就被停掉。
    所以线程池的所有任务完成后，它最终会收缩到corePoolSize的大小。
```

```java
        ThreadPoolExecutor pool4 = new ThreadPoolExecutor(5, 10, 5,
                TimeUnit.SECONDS,
                new LinkedBlockingQueue<>(5),
                Executors.defaultThreadFactory(),new ThreadPoolExecutor.AbortPolicy());

        LocalDateTime localDateTime = LocalDateTime.now();
        System.out.println(localDateTime);
        SimpleDateFormat format=new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

        for (int i = 0; i < 10; i++) {
            Future<?> task1 = pool4.submit(() -> {
                try {
                    TimeUnit.SECONDS.sleep(2);
                    System.out.println(format.format(new Date())+":"+Thread.currentThread().getName());
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            });
        }
```

![image-20221102204726755](images\image-20221102204726755.png)

## 3、拒绝策略？生产中如设置合理参数

### 线程池的拒绝策略

 等待队列已经排满了，再也塞不下新任务了，同时，线程池中的max线程也达到了，无法继续为新任务服务。这个是时候我们就需要拒绝策略机制合理的处理这个问题。

### JDK内置的拒绝策略

AbortPolicy(默认)：直接抛出RejectedExecutionException异常阻止系统正常运行

CallerRunsPolicy：“调用者运行”一种调节机制，该策略既不会抛弃任务，也不会抛出异常，而是将某些任务回退到调用者，从而降低新任务的流量。

DiscardOldestPolicy：抛弃队列中等待最久的任务，然后把当前任务加入队列中尝试再次提交当前任务。

DiscardPolicy：该策略默默地丢弃无法处理的任务，不予任何处理也不抛出异常。如果允许任务丢失，这是最好的一种策略。

**以上内置拒绝策略均实现了RejectedExecutionHandle接口**

```java
     ThreadPoolExecutor pool4 = new ThreadPoolExecutor(5, 10, 5,
                TimeUnit.SECONDS,
                new LinkedBlockingQueue<>(5),
                Executors.defaultThreadFactory(),
                (r, executors) -> {
                    //自定义饱和策略
                    //记录一下无法处理的任务
                    System.out.println("无法处理的任务：" + r.toString());
                });

        LocalDateTime localDateTime = LocalDateTime.now();
        System.out.println(localDateTime);
        SimpleDateFormat format=new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

        for (int i = 0; i < 20; i++) {
            Future<?> task1 = pool4.submit(() -> {
                try {
                    TimeUnit.SECONDS.sleep(2);
                    System.out.println(format.format(new Date())+":"+Thread.currentThread().getName());
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            });
        }
```

![image-20221102205440677](images\image-20221102205440677.png)

## 4、生产中合理的设置参数

要想合理的配置线程池，需要先分析任务的特性，可以从以下几个角度分析：

- 任务的性质：CPU密集型任务、IO密集型任务和混合型任务
- 任务的优先级：高、中、低
- 任务的执行时间：长、中、短
- 任务的依赖性：是否依赖其他的系统资源，如数据库连接。

性质不同任务可以用不同规模的线程池分开处理。CPU密集型任务应该尽可能小的线程，如配置cpu数量+1个线程的线程池。由于IO密集型任务并不是一直在执行任务，不能让cpu闲着，则应配置尽可能多的线程，如：cup数量*2。混合型的任务，如果可以拆分，将其拆分成一个CPU密集型任务和一个IO密集型任务，只要这2个任务执行的时间相差不是太大，那么分解后执行的吞吐量将高于串行执行的吞吐量。可以通过`Runtime.getRuntime().availableProcessors()`方法获取cpu数量。优先级不同任务可以对线程池采用优先级队列来处理，让优先级高的先执行。

使用队列的时候建议使用有界队列，有界队列增加了系统的稳定性，如果采用无解队列，任务太多的时候可能导致系统OOM，直接让系统宕机。

线程池汇总线程大小对系统的性能有一定的影响，我们的目标是希望系统能够发挥最好的性能，过多或者过小的线程数量无法有消息的使用机器的性能。Java Concurrency inPractice书中给出了估算线程池大小的公式：

```
Ncpu = CUP的数量
Ucpu = 目标CPU的使用率，0<=Ucpu<=1
W/C = 等待时间与计算时间的比例
为保存处理器达到期望的使用率，最有的线程池的大小等于：
Nthreads = Ncpu × Ucpu × (1+W/C)
```

## 5、线程池中的2个关闭方法

线程池提供了2个关闭方法：`shutdown`和`shutdownNow`，当调用者两个方法之后，线程池会遍历内部的工作线程，然后调用每个工作线程的interrrupt方法给线程发送中断信号，内部如果无法响应中断信号的可能永远无法终止，所以如果内部有无线循环的，最好在循环内部检测一下线程的中断信号，合理的退出。调用者两个方法中任意一个，线程池的`isShutdown`方法就会返回true，当所有的任务线程都关闭之后，才表示线程池关闭成功，这时调用`isTerminaed`方法会返回true。

调用`shutdown`方法之后，线程池将不再接口新任务，内部会将所有已提交的任务处理完毕，处理完毕之后，工作线程自动退出。

而调用`shutdownNow`方法后，线程池会将还未处理的（在队里等待处理的任务）任务移除，将正在处理中的处理完毕之后，工作线程自动退出。

至于调用哪个方法来关闭线程，应该由提交到线程池的任务特性决定，多数情况下调用`shutdown`方法来关闭线程池，如果任务不一定要执行完，则可以调用`shutdownNow`方法

## 6、BlockingQueue阻塞队列

### 栈与队列

栈：先进后出，后进先出

队列：先进先出

### 阻塞队列

阻塞：必须要阻塞/不得不阻塞

![image-20221102210105952](images\image-20221102210105952.png)

线程1往阻塞队列里添加元素，线程2从阻塞队列里移除元素

当队列是空的，从队列中获取元素的操作将会被阻塞

当队列是满的，从队列中添加元素的操作将会被阻塞

试图从空的队列中获取元素的线程将会被阻塞，直到其他线程往空的队列插入新的元素

试图向已满的队列中添加新元素的线程将会被阻塞，直到其他线程从队列中移除一个或多个元素或者完全清空，使队列变得空闲起来并后续新增

### 种类分析

**ArrayBlockingQueue**：是一个基于数组结构的有界阻塞队列，此队列按照先进先出原则对元素进行排序

**LinkedBlockingQueue**：由链表结构组成的有界（但大小默认值为integer.MAX_VALUE）阻塞队列，此队列按照先进先出排序元素，吞吐量通常要高于ArrayBlockingQueue。静态工厂方法`Executors.newFixedThreadPool`使用了这个队列。

PriorityBlockingQueue：支持优先级排序的无界阻塞队列。

DelayQueue：使用优先级队列实现的延迟无界阻塞队列。

**SynchronousQueue**：不存储元素的阻塞队列，也即单个元素的队列,每个插入操作必须等到另外一个线程调用移除操作，否则插入操作一直处理阻塞状态，吞吐量通常要高于LinkedBlockingQueue，静态工厂方法`Executors.newCachedThreadPool`使用这个队列

LinkedTransferQueue：由链表组成的无界阻塞队列。

LinkedBlockingDeque：由链表组成的双向阻塞队列。

### BlockingQueue核心方法

![image-20221102210310407](images\image-20221102210310407.png)

| 抛出异常 | 当阻塞队列满时：在往队列中add插入元素会抛出 IIIegalStateException：Queue full 当阻塞队列空时：再往队列中remove移除元素，会抛出NoSuchException |
| -------- | ------------------------------------------------------------ |
| 特殊性   | 插入方法，成功true，失败false 移除方法：成功返回出队列元素，队列没有就返回空 |
| 一直阻塞 | 当阻塞队列满时，生产者继续往队列里put元素，队列会一直阻塞生产线程直到put数据or响应中断退出， 当阻塞队列空时，消费者线程试图从队列里take元素，队列会一直阻塞消费者线程直到队列可用。 |
| 超时退出 | 当阻塞队列满时，队里会阻塞生产者线程一定时间，超过限时后生产者线程会退出 |

```java
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.TimeUnit;

/**
 * 阻塞队列
 */
public class BlockingQueueDemo {

    public static void main(String[] args) throws InterruptedException {

//        List list = new ArrayList();

        BlockingQueue<String> blockingQueue = new ArrayBlockingQueue<>(3);
        //第一组
//        System.out.println(blockingQueue.add("a"));
//        System.out.println(blockingQueue.add("b"));
//        System.out.println(blockingQueue.add("c"));
//        System.out.println(blockingQueue.element());

        //System.out.println(blockingQueue.add("x"));
//        System.out.println(blockingQueue.remove());
//        System.out.println(blockingQueue.remove());
//        System.out.println(blockingQueue.remove());
//        System.out.println(blockingQueue.remove());
//    第二组
//        System.out.println(blockingQueue.offer("a"));
//        System.out.println(blockingQueue.offer("b"));
//        System.out.println(blockingQueue.offer("c"));
//        System.out.println(blockingQueue.offer("x"));
//        System.out.println(blockingQueue.poll());
//        System.out.println(blockingQueue.poll());
//        System.out.println(blockingQueue.poll());
//        System.out.println(blockingQueue.poll());
//    第三组        
//         blockingQueue.put("a");
//         blockingQueue.put("b");
//         blockingQueue.put("c");
//         //blockingQueue.put("x");
//        System.out.println(blockingQueue.take());
//        System.out.println(blockingQueue.take());
//        System.out.println(blockingQueue.take());
//        System.out.println(blockingQueue.take());
        
//    第四组        
        System.out.println(blockingQueue.offer("a"));
        System.out.println(blockingQueue.offer("b"));
        System.out.println(blockingQueue.offer("c"));
        System.out.println(blockingQueue.offer("a",3L, TimeUnit.SECONDS));

    }
}

```

## 7、扩展线程池

虽然jdk提供了`ThreadPoolExecutor`这个高性能线程池，但是如果我们自己想在这个线程池上面做一些扩展，比如，监控每个任务执行的开始时间，结束时间，或者一些其他自定义的功能，我们应该怎么办？

这个jdk已经帮我们想到了，`ThreadPoolExecutor`内部提供了几个方法`beforeExecute`、`afterExecute`、`terminated`，可以由开发人员自己去这些方法。看一下线程池内部的源码：

```java
try {
    beforeExecute(wt, task);//任务执行之前调用的方法
    Throwable thrown = null;
    try {
        task.run();
    } catch (RuntimeException x) {
        thrown = x;
        throw x;
    } catch (Error x) {
        thrown = x;
        throw x;
    } catch (Throwable x) {
        thrown = x;
        throw new Error(x);
    } finally {
        afterExecute(task, thrown);//任务执行完毕之后调用的方法
    }
} finally {
    task = null;
    w.completedTasks++;
    w.unlock();
}

```

**beforeExecute：任务执行之前调用的方法，有2个参数，第1个参数是执行任务的线程，第2个参数是任务**

```
protected void beforeExecute(Thread t, Runnable r) { }
```

**afterExecute：任务执行完成之后调用的方法，2个参数，第1个参数表示任务，第2个参数表示任务执行时的异常信息，如果无异常，第二个参数为null**

```
protected void afterExecute(Runnable r, Throwable t) { }
```

**terminated：线程池最终关闭之后调用的方法。所有的工作线程都退出了，最终线程池会退出，退出时调用该方法**

# 三 CompletableFuture

## 1、Future和Callable接口

Future接口定义了操作异步任务执行一些方法，如获取异步任务的执行结果、取消任务的执行、判断任务是否被取消、判断任务执行是否完毕等。

Callable接口中定义了需要有返回的任务需要实现的方法

比如主线程让一个子线程去执行任务，子线程可能比较耗时，启动子线程开始执行任务后，主线程就去做其他事情了，过了一会才去获取子任务的执行结果。

## 2、从之前的FutureTask开始

Future接口相关架构

![image-20221108201244903](images\image-20221108201244903.png)

```java
public class CompletableFutureDemo {
    public static void main(String[] args) throws ExecutionException, InterruptedException, TimeoutException {
        FutureTask<Integer> futureTask = new FutureTask<>(() -> {
            System.out.println("------come in FutureTask");
            try {
                TimeUnit.SECONDS.sleep(3);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            return ThreadLocalRandom.current().nextInt(100);
        });
        Thread t1 = new Thread(futureTask, "t1");
        t1.start();
        //3秒钟后才出来结果，还没有计算你提前来拿(只要一调用get方法，对于结果就是不见不散，会导致阻塞)
        //System.out.println(Thread.currentThread().getName()+"\t"+futureTask.get());
        //3秒钟后才出来结果，我只想等待1秒钟，过时不候
        System.out.println(Thread.currentThread().getName()+"\t"+futureTask.get(1L,TimeUnit.SECONDS));

        System.out.println(Thread.currentThread().getName()+"\t"+" run... here");
    }
}

```

get()阻塞 一旦调用get()方法，不管是否计算完成都会导致阻塞

### Code2

```java
public class CompletableFutureDemo2 {
    public static void main(String[] args) throws ExecutionException, InterruptedException {
        FutureTask<String> futureTask = new FutureTask<String>(() -> {
            System.out.println("----come in FutureTask");
            try {
                TimeUnit.SECONDS.sleep(3);
            } catch (Exception e) {
                e.printStackTrace();
            }
            return "" + ThreadLocalRandom.current().nextInt(100);
        });

        new Thread(futureTask,"t1").start();

        System.out.println(Thread.currentThread().getName()+"\t"+"线程完成任务");

        /**
         * 用于阻塞式获取结果,如果想要异步获取结果,通常都会以轮询的方式去获取结果
         */
        while (true){
            if(futureTask.isDone()){
                System.out.println(futureTask.get());
                break;
            }
        }
    }
}

```

isDone()轮询

轮询的方式会耗费无谓的CPU资源，而且也不见得能及时地得到计算结果.

如果想要异步获取结果,通常都会以轮询的方式去获取结果 尽量不要阻塞

不见不散 -- 过时不候 -- 轮询



## 3、对Future的改进

### 1、类CompletableFuture

![image-20221108202610917](images\image-20221108202610917.png)

![image-20221108202638843](images\image-20221108202638843.png)

#### CompletableFuture

在java8中，CompletableFuture提供了非常强大的Future的扩展功能，可以帮助我们简化异步编程的复杂性，并且提供了函数式编程的能力，可以通过回调的方式处理计算结果，也提供了转换和组合CompletableFuture的方法。

它可能代表一个明确的Future，也有可能代表一个完成阶段，它支持在计算完成以后触发一些函数或执行某些动作

它实现了Future和CompletionStage接口

### 2、接口CompletionStage

#### CompletionStage

CompletionStage代表异步计算过程中的某一个阶段，一个阶段完成以后可能回触发另外一个阶段

一个阶段的计算执行可以是一个Function，Consumer或者Runnable。比如：stage.thenApply(x->square(x)).thenAccept(x->System.out.print(x)).thenRun(()->System.out.printIn())

一个阶段的执行可能是被单个阶段的完成触发，也可能是由多个阶段一起触发

代表异步计算过程中的某一个阶段，一个阶段完成以后可能会触发另外一个阶段，有些类似Linux系统的管道分隔符传参数。

## 4、核心的四个静态方法

### runAsync 无 返回值

```java
public static CompletableFuture<Void> runAsync(Runnable runnable)
public static CompletableFuture<Void> runAsync(Runnable runnable,Executor executor)  
```

### supplyAsync 有 返回值

```java
public static <U> CompletableFuture<U> supplyAsync(Supplier<U> supplier)
public static <U> CompletableFuture<U> supplyAsync(Supplier<U> supplier,Executor executor)
```

上述Executor executor参数说明

没有指定Executor的方法，直接使用默认的ForkJoinPool.commonPool() 作为它的线程池执行异步代码。

如果指定线程池，则使用我们自定义的或者特别指定的线程池执行异步代码

### Code 无返回值

```java

public class CompletableFutureDemo3 {
    public static void main(String[] args) throws ExecutionException, InterruptedException {
        CompletableFuture<Void> future= CompletableFuture.runAsync(() -> {
            System.out.println(Thread.currentThread().getName() + "\t" + "-----come in");
            //暂停几秒钟线程
            try {
                TimeUnit.SECONDS.sleep(1);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println("-----task is over");
        });
        System.out.println(future.get());
    }
}

```

![image-20221108204003146](images\image-20221108204003146.png)

### Code 有返回值

```java
public class CompletableFutureDemo3 {
    public static void main(String[] args) throws ExecutionException, InterruptedException {
        CompletableFuture<Integer> future= CompletableFuture.supplyAsync(() -> {
            System.out.println(Thread.currentThread().getName() + "\t" + "-----come in");
            //暂停几秒钟线程
            try {
                TimeUnit.SECONDS.sleep(1);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println("-----task is over");
            return ThreadLocalRandom.current().nextInt(100);
        });
        System.out.println(future.get());
    }
}

```

![image-20221108204135481](images\image-20221108204135481.png)

### Code 减少阻塞和轮询

```java
public class CompletableFutureDemo3 {
    public static void main(String[] args) throws ExecutionException, InterruptedException {
        CompletableFuture<Integer> future= CompletableFuture.supplyAsync(() -> {
            System.out.println(Thread.currentThread().getName() + "\t" + "-----come in");
            int result = ThreadLocalRandom.current().nextInt(10);
            //暂停几秒钟线程
            try {
                TimeUnit.SECONDS.sleep(1);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println("-----计算结束耗时1秒钟，result： "+result);
            if(result > 6){
                int age = 10/0;
            }
            return result;
        }).whenComplete((v,e)->{
            if (e == null){
                System.out.println("---- result:" + v);
            }
        }).exceptionally(e->{
            System.out.println("-----exception: "+e.getCause()+"\t"+e.getMessage());
            return -44;
        });
        //主线程不要立刻结束，否则CompletableFuture默认使用的线程池会立刻关闭:暂停3秒钟线程
        try { TimeUnit.SECONDS.sleep(3); } catch (InterruptedException e) { e.printStackTrace(); }
    }
}

```

### CompletableFuture的优点

异步任务结束时，会自动回调某个对象的方法；

异步任务出错时，会自动回调某个对象的方法；

主线程设置好回调后，不再关心异步任务的执行，异步任务之间可以顺序执行

### join和get对比

get会抛出异常，join不需要

## 5 、案例精讲-从电商网站的比价需求说开去

经常出现在等待某条 SQL 执行完成后，再继续执行下一条 SQL ，而这两条 SQL 本身是并无关系的，可以同时进行执行的。我们希望能够两条 SQL 同时进行处理，而不是等待其中的某一条 SQL 完成后，再继续下一条。同理， 对于分布式微服务的调用，按照实际业务，如果是无关联step by step的业务，可以尝试是否可以多箭齐发，同时调用。我们去比同一个商品在各个平台上的价格，要求获得一个清单列表， 1 step by step，查完京东查淘宝，查完淘宝查天猫......

2 all 一口气同时查询。。。。。

```java
package com.harry.juc.thread;

import jdk.nashorn.internal.objects.annotations.Getter;

import java.util.Arrays;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

public class CompletableFutureDemo4 {
    static List<NetMall> list = Arrays.asList(
            new NetMall("jd"),
            new NetMall("tmall"),
            new NetMall("pdd"),
            new NetMall("mi")
    );
    public static  List<String> findPrices(List<NetMall> list, String productName){
        return list.stream().map(mail->
                        String.format(productName+"%s price is %.2f",
                        mail.getNetMallName(),
                        mail.getPriceByName(productName))).collect(Collectors.toList());
    }
    public static List<String> findPriceASync(List<NetMall> list,String productName){
        return list.stream().
                map(mall -> CompletableFuture.supplyAsync(() -> String.format(productName + " %s price is %.2f", mall.getNetMallName(), mall.getPriceByName(productName)))).
                    collect(Collectors.toList()).
                    stream().
                    map(CompletableFuture::join).
                    collect(Collectors.toList());
    }
    public static  void main(String[] args) throws Exception{
        long startTime = System.currentTimeMillis();
        List<String> list1 = findPrices(list, "thinking in java");
        for (String element : list1) {
            System.out.println(element);
        }
        long endTime = System.currentTimeMillis();
        System.out.println("----costTime: "+(endTime - startTime) +" 毫秒");
        long startTime2 = System.currentTimeMillis();
        List<String> list2 = findPriceASync(list, "thinking in java");
        for (String element : list2) {
            System.out.println(element);
        }
        long endTime2 = System.currentTimeMillis();
        System.out.println("----costTime: "+(endTime2 - startTime2) +" 毫秒");
    }
}
class NetMall{

    private String netMallName;

    public NetMall(String netMallName){
        this.netMallName = netMallName;
    }

    public double getPriceByName(String productName){
        return calcPrice(productName);
    }

    private double calcPrice(String productName){
        try { TimeUnit.SECONDS.sleep(1); } catch (InterruptedException e) { e.printStackTrace(); }
        return ThreadLocalRandom.current().nextDouble() + productName.charAt(0);
    }

    public String getNetMallName() {
        return netMallName;
    }

    public void setNetMallName(String netMallName) {
        this.netMallName = netMallName;
    }
}
```

## 6、CompletableFuture常用方法

### 获得结果和触发计算

获取结果

```java
// 不见不散
public T get()
    
// 过时不候
public T get(long timeout, TimeUnit unit)
    
// 没有计算完成的情况下，给我一个替代结果 
// 立即获取结果不阻塞 计算完，返回计算完成后的结果  没算完，返回设定的valueIfAbsent值
public T getNow(T valueIfAbsent)
  
public class CompletableFutureDemo2{
    public static void main(String[] args) throws ExecutionException, InterruptedException{
        CompletableFuture<Integer> completableFuture = CompletableFuture.supplyAsync(() -> {
            try { TimeUnit.SECONDS.sleep(1); } catch (InterruptedException e) { e.printStackTrace(); }
            return 533;
        });

        //去掉注释上面计算没有完成，返回444
        //开启注释上满计算完成，返回计算结果
        try { TimeUnit.SECONDS.sleep(2); } catch (InterruptedException e) { e.printStackTrace(); }

        System.out.println(completableFuture.getNow(444));
    }
}

public T join()
public class CompletableFutureDemo2{
    public static void main(String[] args) throws ExecutionException, InterruptedException{
        System.out.println(CompletableFuture.supplyAsync(() -> "abc").thenApply(r -> r + "123").join());
    }
}   

```

主动触发计算

```java
// 是否打断get方法立即返回括号值
public boolean complete(T value)
  
public class CompletableFutureDemo4{
    public static void main(String[] args) throws ExecutionException, InterruptedException{
        CompletableFuture<Integer> completableFuture = CompletableFuture.supplyAsync(() -> {
            try { TimeUnit.SECONDS.sleep(1); } catch (InterruptedException e) { e.printStackTrace(); }
            return 533;
        });

        //注释掉暂停线程，get还没有算完只能返回complete方法设置的444；暂停2秒钟线程，异步线程能够计算完成返回get
        try { TimeUnit.SECONDS.sleep(2); } catch (InterruptedException e) { e.printStackTrace(); }

        //当调用CompletableFuture.get()被阻塞的时候,complete方法就是结束阻塞并get()获取设置的complete里面的值.
        System.out.println(completableFuture.complete(444)+"\t"+completableFuture.get());
    }
}   

```

### 对计算结果进行处理

```java
package com.harry.juc.thread;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

// 计算结果存在依赖关系，这两个线程串行化
// 由于存在依赖关系(当前步错，不走下一步)，当前步骤有异常的话就叫停。
public class CompletableFutureDemo5 {
    public static void main(String[] args) {
        // 当一个线程依赖另一个线程时用thenApply 方法来把两个线程串行化;
        CompletableFuture.supplyAsync(() -> {
            //暂停几秒钟线程
            try { TimeUnit.SECONDS.sleep(1); } catch (InterruptedException e) { e.printStackTrace(); }
            System.out.println("111");
            return 1024;
        }).thenApply(f->{
            System.out.println("222");
            return f+1;
        }).thenApply(f ->{
            //int age = 10/0; // 异常情况：那步出错就停在那步。
            System.out.println("333");
            return f + 1;
        }).whenCompleteAsync((v,e) ->{
            System.out.println("*****v: "+v);
        }).exceptionally(e ->{
            e.printStackTrace();
            return null;
        });
        System.out.println("-----主线程结束，END");

        // 主线程不要立刻结束，否则CompletableFuture默认使用的线程池会立刻关闭:
        try { TimeUnit.SECONDS.sleep(2); } catch (InterruptedException e) { e.printStackTrace(); }
    }
}
```

```java
handle
// 有异常也可以往下一步走，根据带的异常参数可以进一步处理
public class CompletableFutureDemo4{

    public static void main(String[] args) throws ExecutionException, InterruptedException{
        //当一个线程依赖另一个线程时用 handle 方法来把这两个线程串行化,
        // 异常情况：有异常也可以往下一步走，根据带的异常参数可以进一步处理
        CompletableFuture.supplyAsync(() -> {
            //暂停几秒钟线程
            try { TimeUnit.SECONDS.sleep(1); } catch (InterruptedException e) { e.printStackTrace(); }
            System.out.println("111");
            return 1024;
        }).handle((f,e) -> {
            int age = 10/0;
            System.out.println("222");
            return f + 1;
        }).handle((f,e) -> {
            System.out.println("333");
            return f + 1;
        }).whenCompleteAsync((v,e) -> {
            System.out.println("*****v: "+v);
        }).exceptionally(e -> {
            e.printStackTrace();
            return null;
        });

        System.out.println("-----主线程结束，END");

        // 主线程不要立刻结束，否则CompletableFuture默认使用的线程池会立刻关闭:
        try { TimeUnit.SECONDS.sleep(2); } catch (InterruptedException e) { e.printStackTrace(); }
    }
}   

```

![image-20221108210850468](images\image-20221108210850468.png)

### 对计算结果进行消费

接收任务的处理结果，并消费处理，无返回结果

```java
//thenAccept
public static void main(String[] args) throws ExecutionException, InterruptedException{
    CompletableFuture.supplyAsync(() -> {
        return 1;
    }).thenApply(f -> {
        return f + 2;
    }).thenApply(f -> {
        return f + 3;
    }).thenApply(f -> {
        return f + 4;
    }).thenAccept(r -> System.out.println(r));
}  

```

Code之任务之间的顺序执行

```java
thenRun
thenRun(Runnable runnable)
// 任务 A 执行完执行 B，并且 B 不需要 A 的结果
    
thenAccept
thenAccept(Consumer action)
// 任务 A 执行完执行 B，B 需要 A 的结果，但是任务 B 无返回值
  
thenApply
thenApply(Function fn)
// 任务 A 执行完执行 B，B 需要 A 的结果，同时任务 B 有返回值
 
System.out.println(CompletableFuture.supplyAsync(() -> "resultA").thenRun(() -> {}).join());
System.out.println(CompletableFuture.supplyAsync(() -> "resultA").thenAccept(resultA -> {}).join());
System.out.println(CompletableFuture.supplyAsync(() -> "resultA").thenApply(resultA -> resultA + " resultB").join());

```

### 对计算速度进行选用

谁快用谁

applyToEither

```java
public class CompletableFutureDemo5{
    public static void main(String[] args) throws ExecutionException, InterruptedException{
        CompletableFuture<Integer> completableFuture1 = CompletableFuture.supplyAsync(() -> {
            System.out.println(Thread.currentThread().getName() + "\t" + "---come in ");
            //暂停几秒钟线程
            try { TimeUnit.SECONDS.sleep(2); } catch (InterruptedException e) { e.printStackTrace(); }
            return 10;
        });

        CompletableFuture<Integer> completableFuture2 = CompletableFuture.supplyAsync(() -> {
            System.out.println(Thread.currentThread().getName() + "\t" + "---come in ");
            try { TimeUnit.SECONDS.sleep(1); } catch (InterruptedException e) { e.printStackTrace(); }
            return 20;
        });

        CompletableFuture<Integer> thenCombineResult = completableFuture1.applyToEither(completableFuture2,f -> {
            System.out.println(Thread.currentThread().getName() + "\t" + "---come in ");
            return f + 1;
        });

        System.out.println(Thread.currentThread().getName() + "\t" + thenCombineResult.get());
    }
}

```

### 对计算结果进行合并

两个CompletionStage任务都完成后，最终能把两个任务的结果一起交给thenCombine 来处理

先完成的先等着，等待其它分支任务

thenCombine

code标准版，好理解先拆分

```java
public class CompletableFutureDemo2{
    public static void main(String[] args) throws ExecutionException, InterruptedException{
        CompletableFuture<Integer> completableFuture1 = CompletableFuture.supplyAsync(() -> {
            System.out.println(Thread.currentThread().getName() + "\t" + "---come in ");
            return 10;
        });

        CompletableFuture<Integer> completableFuture2 = CompletableFuture.supplyAsync(() -> {
            System.out.println(Thread.currentThread().getName() + "\t" + "---come in ");
            return 20;
        });

        CompletableFuture<Integer> thenCombineResult = completableFuture1.thenCombine(completableFuture2, (x, y) -> {
            System.out.println(Thread.currentThread().getName() + "\t" + "---come in ");
            return x + y;
        });
        
        System.out.println(thenCombineResult.get());
    }
}

```

code表达式

```java
public class CompletableFutureDemo6{
    public static void main(String[] args) throws ExecutionException, InterruptedException{
        CompletableFuture<Integer> thenCombineResult = CompletableFuture.supplyAsync(() -> {
            System.out.println(Thread.currentThread().getName() + "\t" + "---come in 1");
            return 10;
        }).thenCombine(CompletableFuture.supplyAsync(() -> {
            System.out.println(Thread.currentThread().getName() + "\t" + "---come in 2");
            return 20;
        }), (x,y) -> {
            System.out.println(Thread.currentThread().getName() + "\t" + "---come in 3");
            return x + y;
        }).thenCombine(CompletableFuture.supplyAsync(() -> {
            System.out.println(Thread.currentThread().getName() + "\t" + "---come in 4");
            return 30;
        }),(a,b) -> {
            System.out.println(Thread.currentThread().getName() + "\t" + "---come in 5");
            return a + b;
        });
        System.out.println("-----主线程结束，END");
        System.out.println(thenCombineResult.get());


        // 主线程不要立刻结束，否则CompletableFuture默认使用的线程池会立刻关闭:
        try { TimeUnit.SECONDS.sleep(10); } catch (InterruptedException e) { e.printStackTrace(); }
    }
}

```

## 7、分支合并框架

![image-20221108211124254](images\image-20221108211124254.png)

###  1、相关类

#### ForkJoinPool

![image-20221108211204709](images\image-20221108211204709.png)

#### ForkJoinTask

![image-20221108211229409](images\image-20221108211229409.png)

#### RecursiveTask

![image-20221108211247428](images\image-20221108211247428.png)

```java
// 递归任务：继承后可以实现递归(自己调自己)调用的任务
 class Fibonacci extends RecursiveTask<Integer> {
   final int n;
   Fibonacci(int n) { this.n = n; }
   Integer compute() {
     if (n <= 1)
       return n;
     Fibonacci f1 = new Fibonacci(n - 1);
     f1.fork();
     Fibonacci f2 = new Fibonacci(n - 2);
     return f2.compute() + f1.join();
   }
 }

```

# 四 Java的锁机制

## 1、Lock

![image-20221116202842022](images\image-20221116202842022.png)

## 2、synchronized与Lock的区别

1. 首先synchronized是java内置关键字，在jvm层面，Lock是个java类；
2. synchronized无法判断是否获取锁的状态，Lock可以判断是否获取到锁；
3. synchronized会自动释放锁(a 线程执行完同步代码会释放锁 ；b 线程执行过程中发生异常会释放锁)，Lock需在finally中手工释放锁（unlock()方法释放锁），否则容易造成线程死锁；
4. 用synchronized关键字的两个线程1和线程2，如果当前线程1获得锁，线程2线程等待。如果线程1阻塞，线程2则会一直等待下去，而Lock锁就不一定会等待下去，如果尝试获取不到锁，线程可以不用一直等待就结束了；
5. synchronized的锁可重入、不可中断、非公平，而Lock锁可重入、可判断、可公平（两者皆可）
6. Lock锁适合大量同步的代码的同步问题，synchronized锁适合代码少量的同步问题

## 3、synchronized

1. 修饰实例方法，作用于当前实例，进入同步代码前需要先获取实例的锁
2. 修饰静态方法，作用于类的Class对象，进入修饰的静态方法前需要先获取类的Class对象的锁
3. 修饰代码块，需要指定加锁对象(记做lockobj)，在进入同步代码块前需要先获取lockobj的锁

### synchronized作用于实例对象

所谓实例对象锁就是用synchronized修饰实例对象的实例方法，注意是**实例方法**，不是**静态方法**，如：

```java
public class Demo1 {
    int num = 0;
    public synchronized void add(){
        num++;
    }
    public static class T extends Thread{
        private Demo1 demo;
        public T(Demo1 demo){
            this.demo = demo;
        }

        @Override
        public void run() {
            for (int i = 0; i <10000 ; i++) {
                this.demo.add();
            }
        }

        public static void main(String[] args) throws InterruptedException {
            Demo1 demo1 = new Demo1();
            T t1 = new T(demo1);
            T t2 = new T(demo1);
            t1.start();
            t2.start();
            t1.join();
            t2.join();
            System.out.println(demo1.num);

        }
    }
}

```

main()方法中创建了一个对象demo2和2个线程t1、t2，t1、t2中调用demo2的add()方法10000次，add()方法中执行了num++，num++实际上是分3步，获取num，然后将num+1，然后将结果赋值给num，如果t2在t1读取num和num+1之间获取了num的值，那么t1和t2会读取到同样的值，然后执行num++，两次操作之后num是相同的值，最终和期望的结果不一致，造成了线程安全失败，因此我们对add方法加了synchronized来保证线程安全。

注意：m1()方法是实例方法，两个线程操作m1()时，需要先获取demo2的锁，没有获取到锁的，将等待，直到其他线程释放锁为止。

synchronize作用于实例方法需要注意：

1. 实例方法上加synchronized，线程安全的前提是，多个线程操作的是**同一个实例**，如果多个线程作用于不同的实例，那么线程安全是无法保证的
2. 同一个实例的多个实例方法上有synchronized，这些方法都是互斥的，同一时间只允许一个线程操作**同一个实例的其中的一个synchronized方法**

###  synchronized作用于静态方法

当synchronized作用于静态方法时，锁的对象就是当前类的Class对象。如：

```java

public class Demo3 {
    static int num = 0;
    public static synchronized void m1() {
        for (int i = 0; i < 10000; i++) {
            num++;
        }
    }
    public static class T1 extends Thread {
        @Override
        public void run() {
            Demo3.m1();
        }
    }
    public static void main(String[] args) throws InterruptedException {
        T1 t1 = new T1();
        T1 t2 = new T1();
        T1 t3 = new T1();
        t1.start();
        t2.start();
        t3.start();
        //等待3个线程结束打印num
        t1.join();
        t2.join();
        t3.join();
        System.out.println(Demo3.num);
        /**
         * 打印结果：
         * 30000
         */
    }
}

```

上面代码打印30000，和期望结果一致。m1()方法是静态方法，有synchronized修饰，锁用于与Demo3.class对象，和下面的写法类似：

```java
public static void m1() {
    synchronized (Demo4.class) {
        for (int i = 0; i < 10000; i++) {
            num++;
        }
    }
}

```

### synchronized同步代码块

除了使用关键字修饰实例方法和静态方法外，还可以使用同步代码块，在某些情况下，我们编写的方法体可能比较大，同时存在一些比较耗时的操作，而需要同步的代码又只有一小部分，如果直接对整个方法进行同步操作，可能会得不偿失，此时我们可以使用同步代码块的方式对需要同步的代码进行包裹，这样就无需对整个方法进行同步操作了，同步代码块的使用示例如下：

```java

public class Demo5 implements Runnable {
    public static  Demo5 instance = new Demo5();
    public static int i = 0;

    @Override
    public void run() {
        //省略其他耗时操作....
        //使用同步代码块对变量i进行同步操作,锁对象为instance
        synchronized (instance) {
            for (int j = 0; j < 10000; j++) {
                i++;
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread t1 = new Thread(instance);
        Thread t2 = new Thread(instance);
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        System.out.println(i);
    }
}
```

从代码看出，将synchronized作用于一个给定的实例对象instance，即当前实例对象就是锁对象，每次当线程进入synchronized包裹的代码块时就会要求当前线程持有instance实例对象锁，如果当前有其他线程正持有该对象锁，那么新到的线程就必须等待，这样也就保证了每次只有一个线程执行i++;操作。当然除了instance作为对象外，我们还可以使用this对象(代表当前实例)或者当前类的class对象作为锁，如下代码：

```java
//this,当前实例对象锁
synchronized(this){
    for(int j=0;j<1000000;j++){
        i++;
    }
}
//class对象锁
synchronized(Demo5.class){
    for(int j=0;j<1000000;j++){
        i++;
    }
}

```

分析代码是否互斥的方法，先找出synchronized作用的对象是谁，如果多个线程操作的方法中synchronized作用的锁对象一样，那么这些线程同时异步执行这些方法就是互斥的。如下代码:

```java
public class Demo6 {
    //作用于当前类的实例对象
    public synchronized void m1() {
    }
    //作用于当前类的实例对象
    public synchronized void m2() {
    }
    //作用于当前类的实例对象
    public void m3() {
        synchronized (this) {
        }
    }
    //作用于当前类Class对象
    public static synchronized void m4() {
    }
    //作用于当前类Class对象
    public static void m5() {
        synchronized (Demo6.class) {
        }
    }
    public static class T extends Thread{
        Demo6 demo6;
        public T(Demo6 demo6) {
            this.demo6 = demo6;
        }
        @Override
        public void run() {
            super.run();
        }
    }
    public static void main(String[] args) {
        Demo6 d1 = new Demo6();
        Thread t1 = new Thread(() -> {
            d1.m1();
        });
        t1.start();
        Thread t2 = new Thread(() -> {
            d1.m2();
        });
        t2.start();
        Thread t3 = new Thread(() -> {
            d1.m2();
        });
        t3.start();
        Demo6 d2 = new Demo6();
        Thread t4 = new Thread(() -> {
            d2.m2();
        });
        t4.start();
        Thread t5 = new Thread(() -> {
            Demo6.m4();
        });
        t5.start();
        Thread t6 = new Thread(() -> {
            Demo6.m5();
        });
        t6.start();
    }
}

```

main()方法中创建了一个对象demo2和2个线程t1、t2，t1、t2中调用demo2的add()方法10000次，add()方法中执行了num++，num++实际上是分3步，获取num，然后将num+1，然后将结果赋值给num，如果t2在t1读取num和num+1之间获取了num的值，那么t1和t2会读取到同样的值，然后执行num++，两次操作之后num是相同的值，最终和期望的结果不一致，造成了线程安全失败，因此我们对add方法加了synchronized来保证线程安全。

注意：m1()方法是实例方法，两个线程操作m1()时，需要先获取demo2的锁，没有获取到锁的，将等待，直到其他线程释放锁为止。

synchronize作用于实例方法需要注意：

1. 实例方法上加synchronized，线程安全的前提是，多个线程操作的是**同一个实例**，如果多个线程作用于不同的实例，那么线程安全是无法保证的
2. 同一个实例的多个实例方法上有synchronized，这些方法都是互斥的，同一时间只允许一个线程操作**同一个实例的其中的一个synchronized方法**

## 4、ReentrantLock

1. 可重入锁：可重入锁是指同一个线程可以多次获得同一把锁；ReentrantLock和关键字Synchronized都是可重入锁
2. 可中断锁：可中断锁时子线程在获取锁的过程中，是否可以相应线程中断操作。synchronized是不可中断的，ReentrantLock是可中断的
3. 公平锁和非公平锁：公平锁是指多个线程尝试获取同一把锁的时候，获取锁的顺序按照线程到达的先后顺序获取，而不是随机插队的方式获取。synchronized是非公平锁，而ReentrantLock是两种都可以实现，不过默认是非公平锁

### synchronized的局限性

synchronized是java内置的关键字，它提供了一种独占的加锁方式。synchronized的获取和释放锁由jvm实现，用户不需要显示的释放锁，非常方便，然而synchronized也有一定的局限性，例如：

1. 当线程尝试获取锁的时候，如果获取不到锁会一直阻塞，这个阻塞的过程，用户无法控制
2. 如果获取锁的线程进入休眠或者阻塞，除非当前线程异常，否则其他线程尝试获取锁必须一直等待

JDK1.5之后发布，加入了Doug Lea实现的java.util.concurrent包。包内提供了Lock类，用来提供更多扩展的加锁功能。Lock弥补了synchronized的局限，提供了更加细粒度的加锁功能

### ReentrantLock基本使用

我们使用3个线程来对一个共享变量++操作，先使用**synchronized**实现，然后使用**ReentrantLock**实现。

```java
import java.util.concurrent.locks.ReentrantLock;

public class Demo3 {
    private static int num = 0;
    private static ReentrantLock lock = new ReentrantLock();
    private static void add() {
        lock.lock();
        try {
            num++;
        } finally {
            lock.unlock();
        }
    }
    public static class T extends Thread {
        @Override
        public void run() {
            for (int i = 0; i < 10000; i++) {
                Demo3.add();
            }
        }
    }
    public static void main(String[] args) throws InterruptedException {
        T t1 = new T();
        T t2 = new T();
        T t3 = new T();
        t1.start();
        t2.start();
        t3.start();
        t1.join();
        t2.join();
        t3.join();
        System.out.println(Demo3.num);
    }
}

```

**ReentrantLock的使用过程：**

1. **创建锁：ReentrantLock lock = new ReentrantLock();**
2. **获取锁：lock.lock()**
3. **释放锁：lock.unlock();**

### ReentrantLock获取锁的过程是可中断的

对于synchronized关键字，如果一个线程在等待获取锁，最终只有2种结果：

1. 要么获取到锁然后继续后面的操作
2. 要么一直等待，直到其他线程释放锁为止

而ReentrantLock提供了另外一种可能，就是在等待获取锁的过程中（**发起获取锁请求到还未获取到锁这段时间内**）是可以被中断的，也就是说在等待锁的过程中，程序可以根据需要取消获取锁的请求。有些使用这个操作是非常有必要的。比如：你和好朋友越好一起去打球，如果你等了半小时朋友还没到，突然你接到一个电话，朋友由于突发状况，不能来了，那么你一定达到回府。中断操作正是提供了一套类似的机制，如果一个线程正在等待获取锁，那么它依然可以收到一个通知，被告知无需等待，可以停止工作了。

```java
package com.harry.lock;

import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantLock;

public class Demo6 {
    private static ReentrantLock lock1 = new ReentrantLock();
    private static ReentrantLock lock2 = new ReentrantLock();

    public static class T extends Thread{
        int lock;
        public T(String name, int lock){
            super(name);
            this.lock = lock;
        }

        @Override
        public void run() {
            try{
                if (this.lock == 1){
                    lock1.lockInterruptibly();
                    TimeUnit.SECONDS.sleep(1);
                    lock2.lockInterruptibly();
                }else {
                    lock2.lockInterruptibly();
                    TimeUnit.SECONDS.sleep(1);
                    lock1.lockInterruptibly();
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            }finally{
                if (lock1.isHeldByCurrentThread()) {
                    lock1.unlock();
                }
                if (lock2.isHeldByCurrentThread()) {
                    lock2.unlock();
                }
            }
        }

        public static void main(String[] args) {
            T t1 = new T("t1", 1);
            T t2 = new T("t2", 2);
            t1.start();
            t2.start();
        }
    }
}

```

先运行一下上面代码，发现程序无法结束，使用jstack查看线程堆栈信息，发现2个线程死锁了。

![image-20221116210927601](images\image-20221116210927601.png)

lock1被线程t1占用，lock2被线程t2占用，线程t1在等待获取lock2，线程t2在等待获取lock1，都在相互等待获取对方持有的锁，最终产生了死锁，如果是在synchronized关键字情况下发生了死锁现象，程序是无法结束的。

我们对上面代码改造一下，线程t2一直无法获取到lock1，那么等待5秒之后，我们中断获取锁的操作。主要修改一下main方法，如下：

```java
T t1 = new T("t1", 1);
T t2 = new T("t2", 2);
t1.start();
t2.start();
TimeUnit.SECONDS.sleep(5);
t2.interrupt();
```

程序可以结束了，运行结果：

![image-20221116211203507](images\image-20221116211203507.png)

t2在27行一直获取不到lock1的锁，主线程中等待了5秒之后，t2线程调用了`interrupt()`方法，将线程的中断标志置为true，此时31行会触发`InterruptedException`异常，然后线程t2可以继续向下执行，释放了lock2的锁，然后线程t1可以正常获取锁，程序得以继续进行。线程发送中断信号触发InterruptedException异常之后，中断标志将被清空。

关于获取锁的过程中被中断，注意几点:

1. **ReentrankLock中必须使用实例方法`lockInterruptibly()`获取锁时，在线程调用interrupt()方法之后，才会引发`InterruptedException`异常**
2. **线程调用interrupt()之后，线程的中断标志会被置为true**
3. **触发InterruptedException异常之后，线程的中断标志会被清空，即置为false**
4. **所以当线程调用interrupt()引发InterruptedException异常，中断标志的变化是:false->true->false**

### ReentrantLock锁申请等待限时

获取锁的时间我们是不知道的，synchronized关键字获取锁的过程中，只能等待其他线程把锁释放之后才能够有机会获取到锁。所以获取锁的时间有长有短。如果获取锁的时间能够设置超时时间，那就非常好了。

返回boolean类型的值，此方法会立即返回，结果表示获取锁是否成功，示例：

```java
package com.harry.lock;

import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantLock;

public class Demo8 {
    private static ReentrantLock lock1 = new ReentrantLock(false);
    public static class T extends Thread{
        public T(String name){
            super(name);
        }

        @Override
        public void run() {
            try {
                System.out.println(System.currentTimeMillis() + ":" + this.getName() + "开始获取锁!");
                //获取锁超时时间设置为3秒，3秒内是否能否获取锁都会返回
                if (lock1.tryLock()) {
                    System.out.println(System.currentTimeMillis() + ":" + this.getName() + "获取到了锁!");
                    //获取到锁之后，休眠5秒
                    TimeUnit.SECONDS.sleep(5);
                } else {
                    System.out.println(System.currentTimeMillis() + ":" + this.getName() + "未能获取到锁!");
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            } finally {
                if (lock1.isHeldByCurrentThread()) {
                    lock1.unlock();
                }
            }
        }

        public static void main(String[] args) {
            T t1 = new T("t1");
            T t2 = new T("t2");
            t1.start();
            t2.start();
        }
    }
}

```

代码中获取锁成功之后，休眠5秒，会导致另外一个线程获取锁失败，运行代码，输出：

![image-20221116211913138](images\image-20221116211913138.png)

**tryLock有参方法**

可以明确设置获取锁的超时时间，该方法签名

```java
public boolean tryLock(long timeout, TimeUnit unit) throws InterruptedException
```

该方法在指定的时间内不管是否可以获取锁，都会返回结果，返回true，表示获取锁成功，返回false表示获取失败。此方法有2个参数，第一个参数是时间类型，是一个枚举，可以表示时、分、秒、毫秒等待，使用比较方便，第1个参数表示在时间类型上的时间长短。此方法在执行的过程中，如果调用了线程的中断interrupt()方法，会触发InterruptedException异常。

```java
package com.harry.lock;

import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantLock;

public class Demo7 {
    private static ReentrantLock lock1 = new ReentrantLock(false);
    public static class T extends Thread {
        public T(String name) {
            super(name);
        }
        @Override
        public void run() {
            try {
                System.out.println(System.currentTimeMillis() + ":" + this.getName() + "开始获取锁!");
                //获取锁超时时间设置为3秒，3秒内是否能否获取锁都会返回
                if (lock1.tryLock(3, TimeUnit.SECONDS)) {
                    System.out.println(System.currentTimeMillis() + ":" + this.getName() + "获取到了锁!");
                    //获取到锁之后，休眠5秒
                    TimeUnit.SECONDS.sleep(5);
                } else {
                    System.out.println(System.currentTimeMillis() + ":" + this.getName() + "未能获取到锁!");
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            } finally {
                if (lock1.isHeldByCurrentThread()) {
                    lock1.unlock();
                }
            }
        }
    }
    public static void main(String[] args) throws InterruptedException {
        T t1 = new T("t1");
        T t2 = new T("t2");
        t1.start();
        t2.start();
    }
}

```

程序中调用了ReentrantLock的实例方法`tryLock(3, TimeUnit.SECONDS)`，表示获取锁的超时时间是3秒，3秒后不管是否能否获取锁，该方法都会有返回值，获取到锁之后，内部休眠了5秒，会导致另外一个线程获取锁失败。

**关于tryLock()方法和tryLock(long timeout, TimeUnit unit)方法，说明一下：**

1. 都会返回boolean值，结果表示获取锁是否成功
2. tryLock()方法，不管是否获取成功，都会立即返回；而有参的tryLock方法会尝试在指定的时间内去获取锁，中间会阻塞的现象，在指定的时间之后会不管是否能够获取锁都会返回结果
3. tryLock()方法不会响应线程的中断方法；而有参的tryLock方法会响应线程的中断方法，而触发`InterruptedException`异常，这个从2个方法的声明上可以看出来

## 5、悲观锁

认为自己在使用数据的时候一定有别的线程来修改数据，因此在获取数据的时候会先加锁，确保数据不会被别的线程修改。

synchronized关键字和Lock的实现类都是悲观锁

适合写操作多的场景，先加锁可以保证写操作时数据正确。

显式的锁定之后再操作同步资源

```java
//=============悲观锁的调用方式
public synchronized void m1()
{
    //加锁后的业务逻辑......
}

// 保证多个线程使用的是同一个lock对象的前提下
ReentrantLock lock = new ReentrantLock();
public void m2() {
    lock.lock();
    try {
        // 操作同步资源
    }finally {
        lock.unlock();
    }
}

```

##  6、乐观锁

```java
//=============乐观锁的调用方式
// 保证多个线程使用的是同一个AtomicInteger
private AtomicInteger atomicInteger = new AtomicInteger();
atomicInteger.incrementAndGet();

```

乐观锁认为自己在使用数据时不会有别的线程修改数据，所以不会添加锁，只是在更新数据的时候去判断之前有没有别的线程更新了这个数据。

如果这个数据没有被更新，当前线程将自己修改的数据成功写入。如果数据已经被其他线程更新，则根据不同的实现方式执行不同的操作

乐观锁在Java中是通过使用无锁编程来实现，最常采用的是CAS算法，Java原子类中的递增操作就通过CAS自旋实现的。

适合读操作多的场景，不加锁的特点能够使其读操作的性能大幅提升。

乐观锁则直接去操作同步资源，是一种无锁算法，得之我幸不得我命，再抢

乐观锁一般有两种实现方式：

1. 采用版本号机制
2. CAS（Compare-and-Swap，即比较并替换）算法实现

## 7、八锁案例

###  JDK源码(notify方法)

![image-20221117202326292](images\image-20221117202326292.png)

### 8种锁的案例实际体现在3个地方

1. 作用于实例方法，当前实例加锁，进入同步代码前要获得当前实例的锁；
2. 作用于代码块，对括号里配置的对象加锁。
3. 作用于静态方法，当前类加锁，进去同步代码前要获得当前类对象的锁；

#### 标准访问有ab两个线程，请问先打印邮件还是短信

```java
class Phone //资源类
{
    public synchronized void sendEmail()
    {
        System.out.println("-------sendEmail");
    }

    public synchronized void sendSMS()
    {
        System.out.println("-------sendSMS");
    }
}

public class Lock8Demo
{
    public static void main(String[] args)//一切程序的入口，主线程
    {
        Phone phone = new Phone();//资源类1

        new Thread(() -> {
            phone.sendEmail();
        },"a").start();

        //暂停毫秒
        try { TimeUnit.MILLISECONDS.sleep(300); } catch (InterruptedException e) { e.printStackTrace(); }

        new Thread(() -> {
            phone.sendSMS();
        },"b").start();

    }
}

```

```
-------sendEmail
-------sendSMS
```

#### sendEmail方法暂停3秒钟，请问先打印邮件还是短信

```java
class Phone //资源类
{
    public synchronized void sendEmail()
    {
        //暂停几秒钟线程
        try { TimeUnit.SECONDS.sleep(3); } catch (InterruptedException e) { e.printStackTrace(); }
        System.out.println("-------sendEmail");
    }

    public synchronized void sendSMS()
    {
        System.out.println("-------sendSMS");
    }
}

```

```
-------sendEmail
-------sendSMS
```

#### 1-2结论

```
一个对象里面如果有多个synchronized方法，某一个时刻内，只要一个线程去调用其中的一个synchronized方法了，
其它的线程都只能等待，换句话说，某一个时刻内，只能有唯一的一个线程去访问这些synchronized方法
锁的是当前对象this，被锁定后，其它的线程都不能进入到当前对象的其它的synchronized方法
```

#### 新增一个普通的hello方法，请问先打印邮件还是hello

```java
package com.harry.lock;

import java.util.concurrent.TimeUnit;

class Phone //资源类
{
    public synchronized void sendEmail()
    {
        //暂停几秒钟线程
        try { TimeUnit.SECONDS.sleep(3); } catch (InterruptedException e) { e.printStackTrace(); }
        System.out.println("-------sendEmail");
    }

    public synchronized void sendSMS()
    {
        System.out.println("-------sendSMS");
    }

    public void hello()
    {
        System.out.println("-------hello");
    }
}

public class Lock8Demo
{
    public static void main(String[] args)//一切程序的入口，主线程
    {
        Phone phone = new Phone();//资源类1

        new Thread(() -> {
            phone.sendEmail();
        },"a").start();

        //暂停毫秒
        try { TimeUnit.MILLISECONDS.sleep(300); } catch (InterruptedException e) { e.printStackTrace(); }

        new Thread(() -> {
            phone.hello();
        },"b").start();

    }
}

```

```
-------hello
-------sendEmail
```

#### 有两部手机，请问先打印邮件还是短信

```JAVA
class Phone //资源类
{
    public synchronized void sendEmail()
    {
        //暂停几秒钟线程
        try { TimeUnit.SECONDS.sleep(3); } catch (InterruptedException e) { e.printStackTrace(); }
        System.out.println("-------sendEmail");
    }

    public synchronized void sendSMS()
    {
        System.out.println("-------sendSMS");
    }

    public void hello()
    {
        System.out.println("-------hello");
    }
}

public class Lock8Demo
{
    public static void main(String[] args)//一切程序的入口，主线程
    {
        Phone phone = new Phone();//资源类1
        Phone phone2 = new Phone();//资源类2

        new Thread(() -> {
            phone.sendEmail();
        },"a").start();

        //暂停毫秒
        try { TimeUnit.MILLISECONDS.sleep(300); } catch (InterruptedException e) { e.printStackTrace(); }

        new Thread(() -> {
            phone2.sendSMS();
        },"b").start();
    }
}

```

```
-------sendSMS
-------sendEmail
加个普通方法后发现和同步锁无关,hello
换成两个对象后，不是同一把锁了，情况立刻变化。
```

#### 两个静态同步方法，同1部手机，请问先打印邮件还是短信

```java
class Phone //资源类
{
    public static synchronized void sendEmail()
    {
        //暂停几秒钟线程
        try { TimeUnit.SECONDS.sleep(3); } catch (InterruptedException e) { e.printStackTrace(); }
        System.out.println("-------sendEmail");
    }

    public static synchronized void sendSMS()
    {
        System.out.println("-------sendSMS");
    }

    public void hello()
    {
        System.out.println("-------hello");
    }
}

public class Lock8Demo
{
    public static void main(String[] args)//一切程序的入口，主线程
    {
        Phone phone = new Phone();//资源类1

        new Thread(() -> {
            phone.sendEmail();
        },"a").start();

        //暂停毫秒
        try { TimeUnit.MILLISECONDS.sleep(300); } catch (InterruptedException e) { e.printStackTrace(); }

        new Thread(() -> {
            phone.sendSMS();
        },"b").start();
    }
}

```

```
-------sendEmail
-------sendSMS
```

#### 两个静态同步方法， 2部手机，请问先打印邮件还是短信

```java
class Phone //资源类
{
    public static synchronized void sendEmail()
    {
        //暂停几秒钟线程
        try { TimeUnit.SECONDS.sleep(3); } catch (InterruptedException e) { e.printStackTrace(); }
        System.out.println("-------sendEmail");
    }

    public static synchronized void sendSMS()
    {
        System.out.println("-------sendSMS");
    }

    public void hello()
    {
        System.out.println("-------hello");
    }
}

public class Lock8Demo
{
    public static void main(String[] args)//一切程序的入口，主线程
    {
        Phone phone = new Phone();//资源类1
        Phone phone2 = new Phone();//资源类2

        new Thread(() -> {
            phone.sendEmail();
        },"a").start();

        //暂停毫秒
        try { TimeUnit.MILLISECONDS.sleep(300); } catch (InterruptedException e) { e.printStackTrace(); }

        new Thread(() -> {
            phone2.sendSMS();
        },"b").start();
    }
}

```

```
-------sendEmail
-------sendSMS

都换成静态同步方法后，情况又变化
三种 synchronized 锁的内容有一些差别:
对于普通同步方法，锁的是当前实例对象，通常指this,具体的一部部手机,所有的普通同步方法用的都是同一把锁——实例对象本身，
对于静态同步方法，锁的是当前类的Class对象，如Phone.class唯一的一个模板
对于同步方法块，锁的是 synchronized 括号内的对象
```

#### 1个静态同步方法，1个普通同步方法,同1部手机，请问先打印邮件还是短信

```java
class Phone //资源类
{
    public static synchronized void sendEmail()
    {
        //暂停几秒钟线程
        try { TimeUnit.SECONDS.sleep(3); } catch (InterruptedException e) { e.printStackTrace(); }
        System.out.println("-------sendEmail");
    }

    public synchronized void sendSMS()
    {
        System.out.println("-------sendSMS");
    }

    public void hello()
    {
        System.out.println("-------hello");
    }
}

public class Lock8Demo
{
    public static void main(String[] args)//一切程序的入口，主线程
    {
        Phone phone = new Phone();//资源类1

        new Thread(() -> {
            phone.sendEmail();
        },"a").start();

        //暂停毫秒
        try { TimeUnit.MILLISECONDS.sleep(300); } catch (InterruptedException e) { e.printStackTrace(); }

        new Thread(() -> {
            phone.sendSMS();
        },"b").start();
    }
}

```

```
-------sendSMS
-------sendEmail
```

#### 1个静态同步方法，1个普通同步方法,2部手机，请问先打印邮件还是短信

```java
class Phone //资源类
{
    public static synchronized void sendEmail()
    {
        //暂停几秒钟线程
        try { TimeUnit.SECONDS.sleep(3); } catch (InterruptedException e) { e.printStackTrace(); }
        System.out.println("-------sendEmail");
    }

    public synchronized void sendSMS()
    {
        System.out.println("-------sendSMS");
    }

    public void hello()
    {
        System.out.println("-------hello");
    }
}

public class Lock8Demo
{
    public static void main(String[] args)//一切程序的入口，主线程
    {
        Phone phone = new Phone();//资源类1
        Phone phone2 = new Phone();//资源类2

        new Thread(() -> {
            phone.sendEmail();
        },"a").start();

        //暂停毫秒
        try { TimeUnit.MILLISECONDS.sleep(300); } catch (InterruptedException e) { e.printStackTrace(); }

        new Thread(() -> {
            phone2.sendSMS();
        },"b").start();
    }
}

```

```
-------sendSMS
-------sendEmail

当一个线程试图访问同步代码时它首先必须得到锁，退出或抛出异常时必须释放锁。

所有的普通同步方法用的都是同一把锁——实例对象本身，就是new出来的具体实例对象本身,本类this
也就是说如果一个实例对象的普通同步方法获取锁后，该实例对象的其他普通同步方法必须等待获取锁的方法释放锁后才能获取锁。

所有的静态同步方法用的也是同一把锁——类对象本身，就是我们说过的唯一模板Class
具体实例对象this和唯一模板Class，这两把锁是两个不同的对象，所以静态同步方法与普通同步方法之间是不会有竞态条件的
但是一旦一个静态同步方法获取锁后，其他的静态同步方法都必须等待该方法释放锁后才能获取锁。

```

##  8、公平锁和非公平锁

在大多数情况下，锁的申请都是非公平的，也就是说，线程1首先请求锁A，接着线程2也请求了锁A。那么当锁A可用时，是线程1可获得锁还是线程2可获得锁呢？这是不一定的，系统只是会从这个锁的等待队列中随机挑选一个，因此不能保证其公平性。这就好比买票不排队，大家都围在售票窗口前，售票员忙的焦头烂额，也顾及不上谁先谁后，随便找个人出票就完事了，最终导致的结果是，有些人可能一直买不到票。而公平锁，则不是这样，它会按照到达的先后顺序获得资源。公平锁的一大特点是：它不会产生饥饿现象，只要你排队，最终还是可以等到资源的；synchronized关键字默认是有jvm内部实现控制的，是非公平锁。而ReentrantLock运行开发者自己设置锁的公平性

看一下jdk中ReentrantLock的源码，2个构造方法：

```java
public ReentrantLock() {
    sync = new NonfairSync();
}
public ReentrantLock(boolean fair) {
    sync = fair ? new FairSync() : new NonfairSync();
}

```

默认构造方法创建的是非公平锁。

第2个构造方法，有个fair参数，当fair为true的时候创建的是公平锁，公平锁看起来很不错，不过要实现公平锁，系统内部肯定需要维护一个有序队列，因此公平锁的实现成本比较高，性能相对于非公平锁来说相对低一些。因此，在默认情况下，锁是非公平的，如果没有特别要求，则不建议使用公平锁。

公平锁和非公平锁在程序调度上是很不一样，来一个公平锁示例看一下：

```java
import java.util.concurrent.locks.ReentrantLock;

public class Demo5 {
    private static int num = 0;
    private static ReentrantLock fairLock = new ReentrantLock(true);
    public static class T extends Thread {
        public T(String name) {
            super(name);
        }
        @Override
        public void run() {
            for (int i = 0; i < 5; i++) {
                fairLock.lock();
                try {
                    System.out.println(this.getName() + "获得锁!");
                } finally {
                    fairLock.unlock();
                }
            }
        }
    }
    public static void main(String[] args) throws InterruptedException {
        T t1 = new T("t1");
        T t2 = new T("t2");
        T t3 = new T("t3");
        t1.start();
        t2.start();
        t3.start();
        t1.join();
        t2.join();
        t3.join();
    }
}

```

看一下输出的结果，锁是按照先后顺序获得的。

修改一下上面代码，改为非公平锁试试，如下：

```java
ReentrantLock fairLock = new ReentrantLock(false);
```

从ReentrantLock票编码演示公平和非公平现象

```java
import java.util.concurrent.locks.ReentrantLock;

class Ticket
{
    private int number = 30;
    ReentrantLock lock = new ReentrantLock();

    public void sale()
    {
        lock.lock();
        try
        {
            if(number > 0)
            {
                System.out.println(Thread.currentThread().getName()+"卖出第：\t"+(number--)+"\t 还剩下:"+number);
            }
        }catch (Exception e){
            e.printStackTrace();
        }finally {
            lock.unlock();
        }
    }
}

public class SaleTicketDemo
{
    public static void main(String[] args)
    {
        Ticket ticket = new Ticket();

        new Thread(() -> { for (int i = 0; i <35; i++)  ticket.sale(); },"a").start();
        new Thread(() -> { for (int i = 0; i <35; i++)  ticket.sale(); },"b").start();
        new Thread(() -> { for (int i = 0; i <35; i++)  ticket.sale(); },"c").start();
    }
}

```

## 9、可重入锁(又名递归锁)

是指在同一个线程在外层方法获取锁的时候，再进入该线程的内层方法会自动获取锁(前提，锁对象得是同一个对象)，不会因为之前已经获取过还没释放而阻塞。

如果是1个有 synchronized 修饰的递归调用方法，程序第2次进入被自己阻塞了岂不是天大的笑话，出现了作茧自缚。所以Java中ReentrantLock和synchronized都是可重入锁，可重入锁的一个优点是可一定程度避免死锁。

#### 隐式锁（即synchronized关键字使用的锁）默认是可重入锁

```text
指的是可重复可递归调用的锁，在外层使用锁之后，在内层仍然可以使用，并且不发生死锁，这样的锁就叫做可重入锁。
简单的来说就是：在一个synchronized修饰的方法或代码块的内部调用本类的其他synchronized修饰的方法或代码块时，是永远可以得到锁的

与可重入锁相反，不可重入锁不可递归调用，递归调用就发生死锁。
```

同步块

```java
public class ReEntryLockDemo{
    public static void main(String[] args){
        final Object objectLockA = new Object();

        new Thread(() -> {
            synchronized (objectLockA){
                System.out.println("-----外层调用");
                synchronized (objectLockA){
                    System.out.println("-----中层调用");
                    synchronized (objectLockA){
                        System.out.println("-----内层调用");
                    }
                }
            }
        },"a").start();
    }
}

```

同步方法

```java
public class ReEntryLockDemo{
    public synchronized void m1(){
        System.out.println("-----m1");
        m2();
    }
    public synchronized void m2(){
        System.out.println("-----m2");
        m3();
    }
    public synchronized void m3(){
        System.out.println("-----m3");
    }

    public static void main(String[] args){
        ReEntryLockDemo reEntryLockDemo = new ReEntryLockDemo();

        reEntryLockDemo.m1();
    }
}

```

#### 显式锁（即Lock）也有ReentrantLock这样的可重入锁。

```java
public class Demo4 {
    private static int num = 0;
    private static ReentrantLock lock = new ReentrantLock();
    private static void add() {
        lock.lock();
        lock.lock();
        try {
            num++;
        } finally {
            lock.unlock();
            lock.unlock();
        }
    }
    public static class T extends Thread {
        @Override
        public void run() {
            for (int i = 0; i < 10000; i++) {
                Demo4.add();
            }
        }
    }
    public static void main(String[] args) throws InterruptedException {
        T t1 = new T();
        T t2 = new T();
        T t3 = new T();
        t1.start();
        t2.start();
        t3.start();
        t1.join();
        t2.join();
        t3.join();
        System.out.println(Demo4.num);
    }
}

```

上面代码中add()方法中，当一个线程进入的时候，会执行2次获取锁的操作，运行程序可以正常结束，并输出和期望值一样的30000，假如ReentrantLock是不可重入的锁，那么同一个线程第2次获取锁的时候由于前面的锁还未释放而导致死锁，程序是无法正常结束的。ReentrantLock命名也挺好的Re entrant Lock，和其名字一样，可重入锁。

代码中还有几点需要注意：

1. **lock()方法和unlock()方法需要成对出现，锁了几次，也要释放几次，否则后面的线程无法获取锁了；可以将add中的unlock删除一个事实，上面代码运行将无法结束**
2. **unlock()方法放在finally中执行，保证不管程序是否有异常，锁必定会释放**

#### Synchronized的重入的实现机理

每个锁对象拥有一个锁计数器和一个指向持有该锁的线程的指针。

当执行monitorenter时，如果目标锁对象的计数器为零，那么说明它没有被其他线程所持有，Java虚拟机会将该锁对象的持有线程设置为当前线程，并且将其计数器加1。

在目标锁对象的计数器不为零的情况下，如果锁对象的持有线程是当前线程，那么 Java 虚拟机可以将其计数器加1，否则需要等待，直至持有线程释放该锁。

当执行monitorexit时，Java虚拟机则需将锁对象的计数器减1。计数器为零代表锁已被释放。

##  10、死锁

死锁是指两个或两个以上的线程在执行过程中,因争夺资源而造成的一种互相等待的现象,若无外力干涉那它们都将无法推进下去，如果系统资源充足，进程的资源请求都能够得到满足，死锁出现的可能性就很低，否则就会因争夺有限的资源而陷入死锁。

### 产生死锁主要原因

1. 系统资源不足
2. 进程运行推进的顺序不合适
3. 资源分配不当

# 五、线程间通信

两个线程，一个线程打印1-52，另一个打印字母A-Z打印顺序为12A34B...5152

```java
package com.harry.share;

class ShareDataOne{
    private int number = 0;
    public synchronized void increment() throws InterruptedException {
        if (number != 0){
            this.wait();
        }
        ++number;
        System.out.println(Thread.currentThread().getName()+"\t"+number);
        //3通知
        this.notifyAll();
    }
    public synchronized void decrement() throws InterruptedException {
        // 1判断
        if (number == 0) {
            this.wait();
        }
        // 2干活
        --number;
        System.out.println(Thread.currentThread().getName() + "\t" + number);
        // 3通知
        this.notifyAll();
    }
}

/**
 *
 * @Description:
 *现在两个线程，
 * 可以操作初始值为零的一个变量，
 * 实现一个线程对该变量加1，一个线程对该变量减1，
 * 交替，来10轮。
 * @author xialei
 *
 * 1 多线程变成模板（套路）-----上
 *     1.1  线程    操作    资源类
 *     1.2  高内聚  低耦合
 * 2 多线程变成模板（套路）-----下
 *     2.1  判断
 *     2.2  干活
 *     2.3  通知

 */
public class NotifyWaitDemoOne {

    public static void main(String[] args) {
        ShareDataOne sd = new ShareDataOne();
        new Thread(()->{
            for (int i = 1; i < 10 ; i++) {
                try {
                    sd.increment();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        },"A").start();
        new Thread(()->{
            for (int i = 1; i <10 ; i++) {
                try {
                    sd.decrement();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        },"B").start();
        
    }
}

```

换成4个线程会导致错误，虚假唤醒

 原因：在java多线程判断时，不能用if，程序出事出在了判断上面，

突然有一添加的线程进到if了，突然中断了交出控制权，

没有进行验证，而是直接走下去了，加了两次，甚至多次

### 4个线程解决方案

解决虚假唤醒：查看API，java.lang.Object

![image-20221124193603806](images\image-20221124193603806.png)



中断和虚假唤醒是可能产生的，所以要用loop循环，if只判断一次，while是只要唤醒就要拉回来再判断一次。if换成while

```java
public class BoundedBuffer {
    final Lock lock = new ReentrantLock();
    final Condition notFull  = lock.newCondition();
    final Condition notEmpty = lock.newCondition();

    final Object[] items = new Object[100];
    int putptr, takeptr, count;

    public void put(Object x) throws InterruptedException {
        lock.lock();
        try {
            while (count == items.length) {
                notFull.await();
            }
            items[putptr] = x;
            if (++putptr == items.length) {
                putptr = 0;
            }
            ++count;
            notEmpty.signal();
        } finally {
            lock.unlock();
        }
    }
}

```

### 线程间定制化调用通信

1、有顺序通知，需要有标识位

2、有一个锁Lock，3把钥匙Condition

3、判断标志位

4、输出线程名+第几次+第几轮

5、修改标志位，通知下一个

```java
package com.xue.thread;
 
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
 
 
class ShareResource
{
  private int number = 1;//1:A 2:B 3:C 
  private Lock lock = new ReentrantLock();
  private Condition c1 = lock.newCondition();
  private Condition c2 = lock.newCondition();
  private Condition c3 = lock.newCondition();
 
  public void print5(int totalLoopNumber)
  {
     lock.lock();
     try 
     {
       //1 判断
       while(number != 1)
       {
          //A 就要停止
          c1.await();
       }
       //2 干活
       for (int i = 1; i <=5; i++) 
       {
          System.out.println(Thread.currentThread().getName()+"\t"+i+"\t totalLoopNumber: "+totalLoopNumber);
       }
       //3 通知
       number = 2;
       c2.signal();
     } catch (Exception e) {
       e.printStackTrace();
     } finally {
       lock.unlock();
     }
  }
  public void print10(int totalLoopNumber)
  {
     lock.lock();
     try 
     {
       //1 判断
       while(number != 2)
       {
          //A 就要停止
          c2.await();
       }
       //2 干活
       for (int i = 1; i <=10; i++) 
       {
          System.out.println(Thread.currentThread().getName()+"\t"+i+"\t totalLoopNumber: "+totalLoopNumber);
       }
       //3 通知
       number = 3;
       c3.signal();
     } catch (Exception e) {
       e.printStackTrace();
     } finally {
       lock.unlock();
     }
  }  
  
  public void print15(int totalLoopNumber)
  {
     lock.lock();
     try 
     {
       //1 判断
       while(number != 3)
       {
          //A 就要停止
          c3.await();
       }
       //2 干活
       for (int i = 1; i <=15; i++) 
       {
          System.out.println(Thread.currentThread().getName()+"\t"+i+"\t totalLoopNumber: "+totalLoopNumber);
       }
       //3 通知
       number = 1;
       c1.signal();
     } catch (Exception e) {
       e.printStackTrace();
     } finally {
       lock.unlock();
     }
  }  
}
 
 
/**
 * 
 * @Description: 
 * 多线程之间按顺序调用，实现A->B->C
 * 三个线程启动，要求如下：
 * 
 * AA打印5次，BB打印10次，CC打印15次
 * 接着
 * AA打印5次，BB打印10次，CC打印15次
 * ......来10轮  
 *
 */
public class ThreadOrderAccess
{
  public static void main(String[] args)
  {
     ShareResource sr = new ShareResource();
     
     new Thread(() -> {
       for (int i = 1; i <=10; i++) 
       {
          sr.print5(i);
       }
     }, "AA").start();
     new Thread(() -> {
       for (int i = 1; i <=10; i++) 
       {
          sr.print10(i);
       }
     }, "BB").start();
     new Thread(() -> {
       for (int i = 1; i <=10; i++) 
       {
          sr.print15(i);
       }
     }, "CC").start();   
  }
}

```

# 六、LockSupport与线程中断

## 1、线程中断机制

#### 如何停止、中断一个运行中的线程？？

![image-20221124195256092](images\image-20221124195256092.png)

#### 什么是中断？

首先 一个线程不应该由其他线程来强制中断或停止，而是应该由线程自己自行停止。所以，Thread.stop, Thread.suspend, Thread.resume 都已经被废弃了。

其次 在Java中没有办法立即停止一条线程，然而停止线程却显得尤为重要，如取消一个耗时操作。因此，Java提供了一种用于停止线程的机制——中断。

 中断只是一种协作机制，Java没有给中断增加任何语法，中断的过程完全需要程序员自己实现。若要中断一个线程，你需要手动调用该线程的interrupt方法，该方法也仅仅是将线程对象的中断标识设成true；接着你需要自己写代码不断地检测当前线程的标识位，如果为true，表示别的线程要求这条线程中断， 此时究竟该做什么需要你自己写代码实现。

 每个线程对象中都有一个标识，用于表示线程是否被中断；该标识位为true表示中断，为false表示未中断；通过调用线程对象的interrupt方法将该线程的标识位设为true；可以在别的线程中调用，也可以在自己的线程中调用

#### 中断的相关API方法

![image-20221124203036142](images\image-20221124203036142.png)

##  2、如何使用中断标识停止线程？

在需要中断的线程中不断监听中断状态，一旦发生中断，就执行相应的中断处理业务逻辑。

### 1、通过一个volatile变量实现

```java
package com.harry.interrupt;

import java.util.concurrent.TimeUnit;

public class InterruptDemo {

    private static volatile boolean isStop = false;

    public static void main(String[] args) {
        new Thread(()->{
            while (true){
                if (isStop){
                    System.out.println(Thread.currentThread().getName()+"线程------isStop = true,自己退出了");
                    break;
                }
                System.out.println("-------hello interrupt");
            }
        },"t1").start();
        //暂停几秒钟线程
        try { TimeUnit.SECONDS.sleep(1); } catch (InterruptedException e) { e.printStackTrace(); }
        isStop = true;
    }
}

```

### 2、通过AtomicBoolean

```java
public class StopThreadDemo {
    private final static AtomicBoolean atomicBoolean = new AtomicBoolean(true);

    public static void main(String[] args) {
        Thread t1 = new Thread(() -> {
            while (atomicBoolean.get()) {
                try {
                    TimeUnit.MILLISECONDS.sleep(500);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("-----hello");
            }
        }, "t1");
        t1.start();
        try { TimeUnit.SECONDS.sleep(3); } catch (InterruptedException e) { e.printStackTrace(); }
        atomicBoolean.set(false);
    }
}
```

### 3、通过Thread类自带的中断api方法实现

1. 实例方法interrupt()，没有返回值

|                         |                                                              |
| ----------------------- | ------------------------------------------------------------ |
| public void interrupt() | 实例方法， 调用interrupt()方法仅仅是在当前线程中打了一个停止的标记，并不是真正立刻停止线程。 |

![image-20221201202819493](images\image-20221201202819493.png)

![image-20221201202851697](images\image-20221201202851697.png)

![image-20221201202909082](images\image-20221201202909082.png)

2. 实例方法isInterrupted，返回布尔值

![image-20221201202946382](images\image-20221201202946382.png)

|                                |                                                              |
| ------------------------------ | ------------------------------------------------------------ |
| public boolean isInterrupted() | 实例方法， 获取中断标志位的当前值是什么， 判断当前线程是否被中断（通过检查中断标志位），默认是false |

```java
import java.util.concurrent.TimeUnit;

public class InterruptDemo2 {
    public static void main(String[] args) {
        Thread t1 = new Thread(() -> {
            while (true) {
                if (Thread.currentThread().isInterrupted()) {
                    System.out.println("-----t1 线程被中断了，break，程序结束");
                    break;
                }
                System.out.println("---hello");
            }
        }, "t1");
        t1.start();
        System.out.println("**************"+t1.isInterrupted());
        //暂停5毫秒
        try { TimeUnit.MILLISECONDS.sleep(5); } catch (InterruptedException e) { e.printStackTrace(); }
        t1.interrupt();
        System.out.println("**************"+t1.isInterrupted());
    }
}
```

### 4、当前线程的中断标识为true，是不是就立刻停止？

具体来说，当对一个线程，调用 interrupt() 时：

① 如果线程处于正常活动状态，那么会将该线程的中断标志设置为 true，仅此而已。 被设置中断标志的线程将继续正常运行，不受影响。所以， interrupt() 并不能真正的中断线程，需要被调用的线程自己进行配合才行。

② 如果线程处于被阻塞状态（例如处于sleep, wait, join 等状态），在别的线程中调用当前线程对象的interrupt方法， 那么线程将立即退出被阻塞状态，并抛出一个InterruptedException异常。

```java
package com.harry.interrupt;

import java.util.concurrent.TimeUnit;

public class InterruptDemo3 {
    public static void main(String[] args) {
        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 300; i++) {
                System.out.println("------" + i);
            }
            System.out.println("after t1.interrupt()--第2次---: " + Thread.currentThread().isInterrupted());
        }, "t1");
        t1.start();;
        System.out.println("before t1.interrupt()----: "+t1.isInterrupted());
        //实例方法interrupt()仅仅是设置线程的中断状态位设置为true，不会停止线程
        t1.interrupt();
        //活动状态,t1线程还在执行中
        try { TimeUnit.MILLISECONDS.sleep(3); } catch (InterruptedException e) { e.printStackTrace(); }
        System.out.println("after t1.interrupt()--第1次---: "+t1.isInterrupted());
        //非活动状态,t1线程不在执行中，已经结束执行了。
        try { TimeUnit.MILLISECONDS.sleep(3000); } catch (InterruptedException e) { e.printStackTrace(); }
        System.out.println("after t1.interrupt()--第3次---: "+t1.isInterrupted());
    }
}

```

![image-20221201204325262](images\image-20221201204325262.png)

**中断只是一种协同机制，修改中断标识位仅此而已，不是立刻stop打断**

### 5、静态方法Thread.interrupted()

```java

/**
 * 作用是测试当前线程是否被中断（检查中断标志），返回一个boolean并清除中断状态，
 * 第二次再调用时中断状态已经被清除，将返回一个false。
 */
public class InterruptedDemo {
    public static void main(String[] args) {
        System.out.println(Thread.currentThread().getName()+"-----"+Thread.interrupted());
        System.out.println(Thread.currentThread().getName()+"-----"+Thread.interrupted());
        System.out.println("111111");
        Thread.currentThread().interrupt();
        System.out.println("22222");
        System.out.println(Thread.currentThread().getName()+"---"+Thread.interrupted());
        System.out.println(Thread.currentThread().getName()+"---"+Thread.interrupted());
    }
}

```

|                                     |                                                              |
| ----------------------------------- | ------------------------------------------------------------ |
| public static boolean interrupted() | 静态方法，Thread.interrupted(); 判断线程是否被中断，并清除当前中断状态，类似i++ 这个方法做了两件事： 1 返回当前线程的中断状态 2 将当前线程的中断状态设为false  这个方法有点不好理解，因为连续调用两次的结果可能不一样。 |

![image-20221201205010558](images\image-20221201205010558.png)

都会返回中断状态，两者对比

![image-20221201205045207](images\image-20221201205045207.png)

### 6、总结

线程中断相关的方法：

interrupt()方法是一个实例方法 它通知目标线程中断，也就是设置目标线程的中断标志位为true，中断标志位表示当前线程已经被中断了。

isInterrupted()方法也是一个实例方法 它判断当前线程是否被中断（通过检查中断标志位）并获取中断标志

Thread类的静态方法interrupted() 返回当前线程的中断状态(boolean类型)且将当前线程的中断状态设为false，此方法调用之后会清除当前线程的中断标志位的状态（将中断标志置为false了），返回当前值并清零置false

## 3、LockSupport是什么

![image-20221201205425647](images\image-20221201205425647.png)

![image-20221201205444961](images\image-20221201205444961.png)

LockSupport是用来创建锁和其他同步类的基本线程阻塞原语。

## 4、线程等待唤醒机制

### 1、3种让线程等待和唤醒的方法

1. 使用Object中的wait()方法让线程等待，使用Object中的notify()方法唤醒线程
2. 使用JUC包中Condition的await()方法让线程等待，使用signal()方法唤醒线程
3. LockSupport类可以阻塞当前线程以及唤醒指定被阻塞的线程

### 2、Object类中的wait和notify方法实现线程等待和唤醒

```java
/**
 *
 * 要求：t1线程等待3秒钟，3秒钟后t2线程唤醒t1线程继续工作
 *
 * 1 正常程序演示
 *
 * 以下异常情况：
 * 2 wait方法和notify方法，两个都去掉同步代码块后看运行效果
 *   2.1 异常情况
 *   Exception in thread "t1" java.lang.IllegalMonitorStateException at java.lang.Object.wait(Native Method)
 *   Exception in thread "t2" java.lang.IllegalMonitorStateException at java.lang.Object.notify(Native Method)
 *   2.2 结论
 *   Object类中的wait、notify、notifyAll用于线程等待和唤醒的方法，都必须在synchronized内部执行（必须用到关键字synchronized）。
 *
 * 3 将notify放在wait方法前面
 *   3.1 程序一直无法结束
 *   3.2 结论
 *   先wait后notify、notifyall方法，等待中的线程才会被唤醒，否则无法唤醒
 */
public class LockSupportDemo {
    public static void main(String[] args) {
        Object objectLock = new Object();
        new Thread(()->{
            synchronized (objectLock) {
                try {
                    objectLock.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            System.out.println(Thread.currentThread().getName()+"\t"+"被唤醒了");
        },"t1").start();

        // 暂停几秒钟线程
        try { TimeUnit.SECONDS.sleep(3L); } catch (InterruptedException e) { e.printStackTrace(); }

        new Thread(()->{
            synchronized (objectLock) {
                objectLock.notify();
            }
        },"t2").start();
    }
}

```

#### 正常

```java
package com.harry.LockSupport;

import java.util.concurrent.TimeUnit;

public class LockSupportDemo2 {

    public static void main(String[] args) {
        Object objectLock = new Object();
        new Thread(()->{
            synchronized (objectLock) {
                try {
                    objectLock.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            System.out.println(Thread.currentThread().getName()+"\t"+"被唤醒了");
        },"t1").start();

        //暂停几秒钟线程
        try { TimeUnit.SECONDS.sleep(3L); } catch (InterruptedException e) { e.printStackTrace(); }

        new Thread(() -> {
            synchronized (objectLock) {
                objectLock.notify();
            }
        },"t2").start();
    }
}

```

#### 异常1

```java
package com.harry.LockSupport;

import java.util.concurrent.TimeUnit;

public class LockSupportDemo2 {

    public static void main(String[] args) {
        Object objectLock = new Object();
        new Thread(()->{

                try {
                    objectLock.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

            System.out.println(Thread.currentThread().getName()+"\t"+"被唤醒了");
        },"t1").start();

        //暂停几秒钟线程
        try { TimeUnit.SECONDS.sleep(3L); } catch (InterruptedException e) { e.printStackTrace(); }

        new Thread(() -> {

                objectLock.notify();

        },"t2").start();
    }
}

```

wait方法和notify方法，两个都去掉同步代码块

![image-20221201210638240](images\image-20221201210638240.png)

#### 异常2

```java
public class LockSupportDemo2 {

    public static void main(String[] args) {
        Object objectLock = new Object();
        new Thread(()->{
            synchronized (objectLock) {
                    objectLock.notify();
            }
            System.out.println(Thread.currentThread().getName()+"\t"+"被唤醒了");
        },"t1").start();

        //暂停几秒钟线程
        try { TimeUnit.SECONDS.sleep(3L); } catch (InterruptedException e) { e.printStackTrace(); }

        new Thread(() -> {
            synchronized (objectLock) {
                try {
                    objectLock.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        },"t2").start();
    }
}

```

将notify放在wait方法前面

程序无法执行，无法唤醒

#### 总结

wait和notify方法必须要在同步块或者方法里面，且成对出现使用

先wait后notify才OK

## 5、LockSupport类中的park等待和unpark唤醒

通过park()和unpark(thread)方法来实现阻塞和唤醒线程的操作

LockSupport是用来创建锁和其他同步类的基本线程阻塞原语。

LockSupport类使用了一种名为Permit（许可）的概念来做到阻塞和唤醒线程的功能， 每个线程都有一个许可(permit)， permit只有两个值1和零，默认是零。 可以把许可看成是一种(0,1)信号量（Semaphore），但与 Semaphore 不同的是，许可的累加上限是1

![image-20221201211101893](images\image-20221201211101893.png)

**阻塞**

park() /park(Object blocker)

![image-20221201211139594](images\image-20221201211139594.png)

阻塞当前线程/阻塞传入的具体线程

**唤醒**

unpark(Thread thread)

唤醒处于阻塞状态的指定线程

#### 代码

```java
package com.harry.LockSupport;

import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.LockSupport;

public class LockSupportDemo3 {
    public static void main(String[] args) {
        Thread t1 = new Thread(() -> {
            System.out.println(Thread.currentThread().getName() + " " + "1111111111111");
            LockSupport.park();
            System.out.println(Thread.currentThread().getName() + " " + "2222222222222------end被唤醒");
        }, "t1");
        t1.start();
        //暂停几秒钟线程
        try { TimeUnit.SECONDS.sleep(3); } catch (InterruptedException e) { e.printStackTrace(); }

        LockSupport.unpark(t1);
        System.out.println(Thread.currentThread().getName()+"   -----LockSupport.unparrk() invoked over");

    }
}


```

之前错误的先唤醒后等待，LockSupport照样支持

```java
public class T1
{
    public static void main(String[] args)
    {
        Thread t1 = new Thread(() -> {
            try { TimeUnit.SECONDS.sleep(3); } catch (InterruptedException e) { e.printStackTrace(); }
            System.out.println(Thread.currentThread().getName()+"\t"+System.currentTimeMillis());
            LockSupport.park();
            System.out.println(Thread.currentThread().getName()+"\t"+System.currentTimeMillis()+"---被叫醒");
        },"t1");
        t1.start();

        try { TimeUnit.SECONDS.sleep(1); } catch (InterruptedException e) { e.printStackTrace(); }

        LockSupport.unpark(t1);
        System.out.println(Thread.currentThread().getName()+"\t"+System.currentTimeMillis()+"---unpark over");
    }
}

```

# 七、集合不安全

## 1、线程不安全错误

```java
java.util.ConcurrentModificationException
ArrayList在迭代的时候如果同时对其进行修改就会
抛出java.util.ConcurrentModificationException异常 并发修改异常

```

##  2、List不安全

```java
List<String> list = new ArrayList<>();
for (int i = 0; i <30 ; i++) {
            new Thread(()->{
                list.add(UUID.randomUUID().toString().substring(0,8));
                System.out.println(list);
            },String.valueOf(i)).start();
        }
 
// 看ArrayList的源码
public boolean add(E e) {
    ensureCapacityInternal(size + 1);  // Increments modCount!!
    elementData[size++] = e;
    return true;
}
// 没有synchronized线程不安全

```

### 解决方案

#### Vector

```java
List list = new Vector<>();
```

![image-20221206201229103](images\image-20221206201229103.png)

```java
// 看Vector的源码
public synchronized boolean add(E e) {
    modCount++;
    ensureCapacityHelper(elementCount + 1);
    elementData[elementCount++] = e;
    return true;
}
// 有synchronized线程安全

```

#### Collections

```java
List list = Collections.synchronizedList(new ArrayList<>());
// Collections提供了方法synchronizedList保证list是同步线程安全的
// 那HashMap，HashSet是线程安全的吗？也不是,所以有同样的线程安全方法

```

#### 写时复制(JUC)

```java
List<String> list = new CopyOnWriteArrayList<>();
```

![image-20221206201346026](images\image-20221206201346026.png)

#### CopyOnWrite理论

```java
/**
 * Appends the specified element to the end of this list.
 *
 * @param e element to be appended to this list
 * @return {@code true} (as specified by {@link Collection#add})
 */
public boolean add(E e) {
    final ReentrantLock lock = this.lock;
    lock.lock();
    try {
        Object[] elements = getArray();
        int len = elements.length;
        Object[] newElements = Arrays.copyOf(elements, len + 1);
        newElements[len] = e;
        setArray(newElements);
        return true;
    } finally {
        lock.unlock();
    }
}

```

##  3、Set不安全

```java
Set<String> set = new HashSet<>();//线程不安全
 
Set<String> set = new CopyOnWriteArraySet<>();//线程安全
HashSet底层数据结构是什么？
HashMap  ?
 
但HashSet的add是放一个值，而HashMap是放K、V键值对
 
public HashSet() {
    map = new HashMap<>();
}
 
private static final Object PRESENT = new Object();
 
public boolean add(E e) {
    return map.put(e, PRESENT)==null;
}

```

## 4、Map不安全

```java
Map<String,String> map = new HashMap<>();//线程不安全

Map<String,String> map = new ConcurrentHashMap<>();//线程安全

```

```java
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.CopyOnWriteArraySet;

/**
 * 请举例说明集合类是不安全的
 */
public class NotSafeDemo {
    public static void main(String[] args) {

        Map<String,String> map = new ConcurrentHashMap<>();
        for (int i = 0; i <30 ; i++) {
            new Thread(()->{
                map.put(Thread.currentThread().getName(),UUID.randomUUID().toString().substring(0,8));
                System.out.println(map);
            },String.valueOf(i)).start();
        }


    }

    private static void setNoSafe() {
        Set<String> set = new CopyOnWriteArraySet<>();
        for (int i = 0; i <30 ; i++) {
            new Thread(()->{
                set.add(UUID.randomUUID().toString().substring(0,8));
                System.out.println(set);
            },String.valueOf(i)).start();
        }
    }

    private static void listNoSafe() {
        //        List<String> list = Arrays.asList("a","b","c");
        //        list.forEach(System.out::println);
        //写时复制
        List<String> list = new CopyOnWriteArrayList<>();
        // new CopyOnWriteArrayList<>();
        //Collections.synchronizedList(new ArrayList<>());
        //new Vector<>();//new ArrayList<>();

        for (int i = 0; i <30 ; i++) {
                    new Thread(()->{
                        list.add(UUID.randomUUID().toString().substring(0,8));
                        System.out.println(list);
                    },String.valueOf(i)).start();
                }
    }


}

    /**
     * 写时复制
     CopyOnWrite容器即写时复制的容器。往一个容器添加元素的时候，不直接往当前容器Object[]添加，
     而是先将当前容器Object[]进行Copy，复制出一个新的容器Object[] newElements，然后向新的容器Object[] newElements里添加元素。
     添加元素后，再将原容器的引用指向新的容器setArray(newElements)。
     这样做的好处是可以对CopyOnWrite容器进行并发的读，而不需要加锁，因为当前容器不会添加任何元素。
     所以CopyOnWrite容器也是一种读写分离的思想，读和写不同的容器。

     *
     *
     *
     *

    public boolean add(E e) {
        final ReentrantLock lock = this.lock;
        lock.lock();
        try {
            Object[] elements = getArray();
            int len = elements.length;
            Object[] newElements = Arrays.copyOf(elements, len + 1);
            newElements[len] = e;
            setArray(newElements);
            return true;
        } finally {
            lock.unlock();
        }
    }
     */

```

# 八、JUC强大的辅助类

## 1、CountDownLatch减少计数

```java
package com.xue.thread;
 
import java.util.concurrent.CountDownLatch;
 
 
/**
 * 
 * @Description:
 *  *让一些线程阻塞直到另一些线程完成一系列操作后才被唤醒。
 * 
 * CountDownLatch主要有两个方法，当一个或多个线程调用await方法时，这些线程会阻塞。
 * 其它线程调用countDown方法会将计数器减1(调用countDown方法的线程不会阻塞)，
 * 当计数器的值变为0时，因await方法阻塞的线程会被唤醒，继续执行。
 * 
 * 解释：6个同学陆续离开教室后值班同学才可以关门。
 * 
 * main主线程必须要等前面6个线程完成全部工作后，自己才能开干 
 */
public class CountDownLatchDemo
{
   public static void main(String[] args) throws InterruptedException
   {
         CountDownLatch countDownLatch = new CountDownLatch(6);
       
       for (int i = 1; i <=6; i++) //6个上自习的同学，各自离开教室的时间不一致
       {
          new Thread(() -> {
              System.out.println(Thread.currentThread().getName()+"\t 号同学离开教室");
              countDownLatch.countDown();
          }, String.valueOf(i)).start();
       }
       countDownLatch.await();
       System.out.println(Thread.currentThread().getName()+"\t****** 班长关门走人，main线程是班长");
          
   }
}

```

- CountDownLatch主要有两个方法，当一个或多个线程调用await方法时，这些线程会阻塞。
- 其它线程调用countDown方法会将计数器减1(调用countDown方法的线程不会阻塞)，
- 当计数器的值变为0时，因await方法阻塞的线程会被唤醒，继续执行。

## 2、CyclicBarrier循环栅栏

```java
package com.xue.thread;
 
import java.util.concurrent.BrokenBarrierException;
import java.util.concurrent.CyclicBarrier;
 
/**
 * 
 *
 * CyclicBarrier
 * 的字面意思是可循环（Cyclic）使用的屏障（Barrier）。它要做的事情是，
 * 让一组线程到达一个屏障（也可以叫同步点）时被阻塞，
 * 直到最后一个线程到达屏障时，屏障才会开门，所有
 * 被屏障拦截的线程才会继续干活。
 * 线程进入屏障通过CyclicBarrier的await()方法。
 * 
 * 集齐7颗龙珠就可以召唤神龙
 */
public class CyclicBarrierDemo
{
  private static final int NUMBER = 7;
  
  public static void main(String[] args)
  {
     //CyclicBarrier(int parties, Runnable barrierAction) 
     
     CyclicBarrier cyclicBarrier = new CyclicBarrier(NUMBER, ()->{System.out.println("*****集齐7颗龙珠就可以召唤神龙");}) ;
     
     for (int i = 1; i <= 7; i++) {
       new Thread(() -> {
          try {
            System.out.println(Thread.currentThread().getName()+"\t 星龙珠被收集 ");
            cyclicBarrier.await();
          } catch (InterruptedException | BrokenBarrierException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
          }
       
       }, String.valueOf(i)).start();
     }
     
 
  }
}

```

- CyclicBarrier的字面意思是可循环（Cyclic）使用的屏障（Barrier）。它要做的事情是，
- 让一组线程到达一个屏障（也可以叫同步点）时被阻塞，
- 直到最后一个线程到达屏障时，屏障才会开门，所有
- 被屏障拦截的线程才会继续干活。
- 线程进入屏障通过CyclicBarrier的await()方法。

## 3、Semaphore信号灯

```java
package com.xue.thread;
 
import java.util.Random;
import java.util.concurrent.Semaphore;
import java.util.concurrent.TimeUnit;
 
/**
 * 
 * @Description: TODO(这里用一句话描述这个类的作用)  
 * 
 * 在信号量上我们定义两种操作：
 * acquire（获取） 当一个线程调用acquire操作时，它要么通过成功获取信号量（信号量减1），
 *             要么一直等下去，直到有线程释放信号量，或超时。
 * release（释放）实际上会将信号量的值加1，然后唤醒等待的线程。
 * 
 * 信号量主要用于两个目的，一个是用于多个共享资源的互斥使用，另一个用于并发线程数的控制。
 */
public class SemaphoreDemo
{
  public static void main(String[] args)
  {
     Semaphore semaphore = new Semaphore(3);//模拟3个停车位
     
     for (int i = 1; i <=6; i++) //模拟6部汽车
     {
       new Thread(() -> {
          try 
          {
            semaphore.acquire();
            System.out.println(Thread.currentThread().getName()+"\t 抢到了车位");
            TimeUnit.SECONDS.sleep(new Random().nextInt(5));
            System.out.println(Thread.currentThread().getName()+"\t------- 离开");
          } catch (InterruptedException e) {
            e.printStackTrace();
          }finally {
            semaphore.release();
          }
       }, String.valueOf(i)).start();
     }
     
  }
}

```

在信号量上我们定义两种操作：

- acquire（获取） 当一个线程调用acquire操作时，它要么通过成功获取信号量（信号量减1），要么一直等下去，直到有线程释放信号量，或超时。
- release（释放）实际上会将信号量的值加1，然后唤醒等待的线程。
- 信号量主要用于两个目的，一个是用于多个共享资源的互斥使用，另一个用于并发线程数的控制。

# 九、Java内存模型之JMM

##  1、计算机硬件存储体系

计算机存储结构，从本地磁盘到主存到CPU缓存，也就是从硬盘到内存，到CPU。一般对应的程序的操作就是从数据库查数据到内存然后到CPU进行计算

因为有这么多级的缓存(cpu和物理主内存的速度不一致的)，CPU的运行并不是直接操作内存而是先把内存里边的数据读到缓存，而内存的读和写操作的时候就会造成不一致的问题

 Java虚拟机规范中试图定义一种Java内存模型（java Memory Model，简称JMM) 来屏蔽掉各种硬件和操作系统的内存访问差异，以实现让Java程序在各种平台下都能达到一致的内存访问效果。推导出我们需要知道JMM

## 2、Java内存模型Java Memory Model

​     JMM(Java内存模型Java Memory Model，简称JMM)本身是一种抽象的概念并不真实存在它仅仅描述的是一组约定或规范，通过这组规范定义了程序中(尤其是多线程)各个变量的读写访问方式并决定一个线程对共享变量的写入何时以及如何变成对另一个线程可见，关键技术点都是围绕多线程的原子性、可见性和有序性展开的。

原则： JMM的关键技术点都是围绕多线程的原子性、可见性和有序性展开的

能干嘛？ 1 通过JMM来实现线程和主内存之间的抽象关系。 2 屏蔽各个硬件平台和操作系统的内存访问差异以实现让Java程序在各种平台下都能达到一致的内存访问效果。

## 3、JMM规范下，三大特性

### 1、可见性

![image-20221206202620178](images\image-20221206202620178.png)

 Java中普通的共享变量不保证可见性，因为数据修改被写入内存的时机是不确定的，多线程并发下很可能出现"脏读"，所以每个线程都有自己的工作内存，线程自己的工作内存中保存了该线程使用到的变量的主内存副本拷贝，线程对变量的所有操作（读取，赋值等 ）都必需在线程自己的工作内存中进行，而不能够直接读写主内存中的变量。不同线程之间也无法直接访问对方工作内存中的变量，线程间变量值的传递均需要通过主内存来完成

![image-20221206202700527](images\image-20221206202700527.png)

线程脏读：如果没有可见性保证

![image-20221206202745408](images\image-20221206202745408.png)

### 2、原子性

指一个操作是不可中断的，即多线程环境下，操作不能被其他线程干扰

### 3、有序性

对于一个线程的执行代码而言，我们总是习惯性认为代码的执行总是从上到下，有序执行。 但为了提供性能，编译器和处理器通常会对指令序列进行重新排序。 指令重排可以保证串行语义一致，但没有义务保证多线程间的语义也一致，即可能产生"脏读"，简单说， 两行以上不相干的代码在执行的时候有可能先执行的不是第一条，不见得是从上到下顺序执行，执行顺序会被优化。

单线程环境里面确保程序最终执行结果和代码顺序执行的结果一致。 处理器在进行重排序时必须要考虑指令之间的数据依赖性 多线程环境中线程交替执行,由于编译器优化重排的存在，两个线程中使用的变量能否保证一致性是无法确定的,结果无法预测

## 4、JMM规范下，多线程对变量的读写过程

### 1、读取过程

 由于JVM运行程序的实体是线程，而每个线程创建时JVM都会为其创建一个工作内存(有些地方称为栈空间)，工作内存是每个线程的私有数据区域，而Java内存模型中规定所有变量都存储在主内存，主内存是共享内存区域，所有线程都可以访问，但线程对变量的操作(读取赋值等)必须在工作内存中进行，首先要将变量从主内存拷贝到的线程自己的工作内存空间，然后对变量进行操作，操作完成后再将变量写回主内存，不能直接操作主内存中的变量，各个线程中的工作内存中存储着主内存中的变量副本拷贝，因此不同的线程间无法访问对方的工作内存，线程间的通信(传值)必须通过主内存来完成，其简要访问过程如下图:

![image-20221206203403978](images\image-20221206203403978.png)

JMM定义了线程和主内存之间的抽象关系 1 线程之间的共享变量存储在主内存中(从硬件角度来说就是内存条) 2 每个线程都有一个私有的本地工作内存，本地工作内存中存储了该线程用来读/写共享变量的副本(从硬件角度来说就是CPU的缓存，比如寄存器、L1、L2、L3缓存等

##  5、JMM规范下，多线程先行发生原则之happens-before

在JMM中，如果一个操作执行的结果需要对另一个操作可见性或者 代码重排序，那么这两个操作之间必须存在happens-before关系。

### 1、先行发生原则说明

   如果Java内存模型中所有的有序性都仅靠volatile和synchronized来完成，那么有很多操作都将会变得非常啰嗦， 但是我们在编写Java并发代码的时候并没有察觉到这一点。

​    我们没有时时、处处、次次，添加volatile和synchronized来完成程序，这是因为Java语言中JMM原则下有一个“先行发生”(Happens-Before)的原则限制和规矩

   这个原则非常重要： 它是判断数据是否存在竞争，线程是否安全的非常有用的手段。依赖这个原则，我们可以通过几条简单规则一揽子解决并发环境下两个操 作之间是否可能存在冲突的所有问题，而不需要陷入Java内存模型苦涩难懂的底层编译原理之中。

### 2、happens-before总原则

- 如果一个操作happens-before另一个操作，那么第一个操作的执行结果将对第二个操作可见，而且第一个操作的执行顺序排在第二个操作之前。
- 两个操作之间存在happens-before关系，并不意味着一定要按照happens-before原则制定的顺序来执行。如果重排序之后的执行结果与按照happens-before关系来执行的结果一致，那么这种重排序并不非法。
  - 1+2+3 = 3+2+1
  - 周一张三周二李四，假如有事情调换班可以的

## 6、happens-before之8条

### 1、次序规则

一个线程内，按照代码顺序，写在前面的操作先行发生于写在后面的操作；

前一个操作的结果可以被后续的操作获取。讲白点就是前面一个操作把变量X赋值为1，那后面一个操作肯定能知道X已经变成了1。

### 2、锁定规则

一个unLock操作先行发生于后面((这里的“后面”是指时间上的先后))对同一个锁的lock操作；

```java
public class HappenBeforeDemo
{
    static Object objectLock = new Object();

    public static void main(String[] args) throws InterruptedException
    {
        //对于同一把锁objectLock，threadA一定先unlock同一把锁后B才能获得该锁，   A 先行发生于B
        synchronized (objectLock)
        {

        }
    }
}

```

### 3、volatile变量规则

对一个volatile变量的写操作先行发生于后面对这个变量的读操作，前面的写对后面的读是可见的，这里的“后面”同样是指时间上的先后

### 4、传递规则

如果操作A先行发生于操作B，而操作B又先行发生于操作C，则可以得出操作A先行发生于操作C；

### 5、线程启动规则(Thread Start Rule)

Thread对象的start()方法先行发生于此线程的每一个动作

### 6、线程中断规则(Thread Interruption Rule)

对线程interrupt()方法的调用先行发生于被中断线程的代码检测到中断事件的发生；

可以通过Thread.interrupted()检测到是否发生中断

### 7、线程终止规则(Thread Termination Rule)

线程中的所有操作都先行发生于对此线程的终止检测，我们可以通过Thread::join()方法是否结束、 Thread::isAlive()的返回值等手段检测线程是否已经终止执行。

### 8、对象终结规则(Finalizer Rule)

一个对象的初始化完成（构造函数执行结束）先行发生于它的finalize()方法的开始

对象没有完成初始化之前，是不能调用finalized()方法的

# 十、volatile与Java内存模型

##  1、被volatile修改的变量有2大特

- 可见性
- 有序性

## 2、volatile的内存语义

- 当写一个volatile变量时，JMM会把该线程对应的本地内存中的共享变量值立即刷新回主内存中。
- 当读一个volatile变量时，JMM会把该线程对应的本地内存设置为无效，直接从主内存中读取共享变量
- 所以volatile的写内存语义是直接刷新到主内存中，读的内存语义是直接从主内存中读取。

## 3、内存屏障（重点）

### 内存屏障是什么

 内存屏障（也称内存栅栏，内存栅障，屏障指令等，是一类同步屏障指令，是CPU或编译器在对内存随机访问的操作中的一个同步点，使得此点之前的所有读写操作都执行后才可以开始执行此点之后的操作），避免代码重排序。内存屏障其实就是一种JVM指令，Java内存模型的重排规则会要求Java编译器在生成JVM指令时插入特定的内存屏障指令，通过这些内存屏障指令，volatile实现了Java内存模型中的可见性和有序性，但volatile无法保证原子性。

 内存屏障之前的所有写操作都要回写到主内存，内存屏障之后的所有读操作都能获得内存屏障之前的所有写操作的最新结果(实现了可见性)。

![image-20221206204126157](images\image-20221206204126157.png)

因此重排序时，不允许把内存屏障之后的指令重排序到内存屏障之前。 一句话：对一个 volatile 域的写, happens-before 于任意后续对这个 volatile 域的读，也叫写后读

### volatile凭什么可以保证可见性和有序性

内存屏障 (Memory Barriers / Fences)

### JVM中提供了四类内存屏障指令

Unsafe.class

![image-20221206204247843](images\image-20221206204247843.png)

![image-20221206204308585](images\image-20221206204308585.png)

Unsafe.cpp

![image-20221206204332652](images\image-20221206204332652.png)

OrderAccess.hpp

![image-20221206204358180](images\image-20221206204358180.png)

orderAccess_linux_x86.inline.hpp

![image-20221206204422417](images\image-20221206204422417.png)

### 四大屏障分别是什么意思

![image-20221206204507440](images\image-20221206204507440.png)

orderAccess_linux_x86.inline.hpp

![image-20221206204531723](images\image-20221206204531723.png)

### happens-before 之 volatile 变量规则

![image-20221206204601599](images\image-20221206204601599.png)

当第一个操作为volatile读时，不论第二个操作是什么，都不能重排序。这个操作保证了volatile读之后的操作不会被重排到volatile读之前。

当第二个操作为volatile写时，不论第一个操作是什么，都不能重排序。这个操作保证了volatile写之前的操作不会被重排到volatile写之后。

当第一个操作为volatile写时，第二个操作为volatile读时，不能重排。

### JMM 就将内存屏障插⼊策略分为 4 种

- 写
  - 在每个 volatile 写操作的前⾯插⼊⼀个 StoreStore 屏障
  - 在每个 volatile 写操作的后⾯插⼊⼀个 StoreLoad 屏障
- 读
  - 在每个 volatile 读操作的后⾯插⼊⼀个 LoadLoad 屏障
  - 在每个 volatile 读操作的后⾯插⼊⼀个 LoadStore 屏障

![image-20221206204644100](images\image-20221206204644100.png)

## 4、volatile特性
