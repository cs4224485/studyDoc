# 一 JVM概述

## 什么是JVM

JVM 是 java[虚拟机](https://so.csdn.net/so/search?q=虚拟机&spm=1001.2101.3001.7020)，是用来执行java字节码(二进制的形式)的虚拟计算机

jvm是运行在操作系统之上的，与硬件没有任何关系



![image-20220731095615776](images\image-20220731095615776.png)

## Java的跨平台及原理

跨平台：由Java编写的程序可以在不同的操作系统上运行：一次编写，多处运行

原理：编译之后的字节码文件和平台无关，需要在不同的操作系统上安装一个对应版本的虚拟机(JVM)
(Java虚拟机不和包括java在内的任何语言绑定，它只与class文件这种二进制文件格式所关联。无论使用何种语言进行软件开发，只要将源文件编译为正确的Class文件，那么这种语言就可以在Java虚拟机上执行，可以说，统一而强大的Class文件结构，就是Java虚拟机的基石、桥梁)

![image-20220731095838923](images\image-20220731095838923.png)

## JVM的分类

- 类加载子系统
- 运行时数据区(我们核心关注这里 的栈、堆、方法区)
- 执行引擎(一般都是JIT编译器和解释器共存

1. JIT编译器(主要影响性能)：编译执行;一般热点数据会进行二次编译，将字节码指令变成机器指令。将机器指令放在方法区缓存
2. 解释器(负责响应时间)：逐行解释字节码

![image-20220731095925411](images\image-20220731095925411.png)

![image-20220731100043968](images\image-20220731100043968.png)

![image-20220731100130812](images\image-20220731100130812.png)

## 三大商业虚拟机

### Sun HotSpot

1. 提起HotSpot VM，相信所有Java程序员都知道，它是Sun JDK和OpenJDK中所带的虚拟机，也是目前使用范围最广的Java虚拟
2. 在2006年的JavaOne大会上，Sun公司宣布最终会把Java开源，并在随后的一年，陆续将JDK的各个部分（其中当然也包括了HotSpot VM）在GPL协议下公开了源码， 并在此基础上建立了OpenJDK。这样，HotSpot VM便成为了Sun JDK和OpenJDK两个实现极度接近的JDK项目的共同虚拟机。
3. 在2008年和2009年，Oracle公司分别收购了BEA公司和Sun公司，这样Oracle就同时拥有了两款优秀的Java虚拟机：JRockit VM和HotSpot VM。 Oracle公司宣布在不久的将来（大约应在发布JDK 8的时候）会完成这两款虚拟机的整合工作，使之优势互补。 整合的方式大致上是在HotSpot的基础上，移植JRockit的优秀特性，譬如使用JRockit的垃圾回收器与MissionControl服务， 使用HotSpot的JIT编译器与混合的运行时系统

### BEA JRocket

1. 专注于服务端应用(JRockit内部不包含解释器实现，全部代码都靠即时编译器编译后执行)
2. Jrockit JVM 是世界上最快的jvm3. 2008年被oracle收购

###  iBM J9

1. 市场定位与hotspot接近，服务器端，桌面应用，嵌入式等
2. 目前，是影响力的三大商业虚拟机之一



# 二 类加载器

## 类加载过程

1. 第一过程的加载(loading)也称为装载
2. 验证、准备、解析3个部分统称为链接(Linking)
3. 在Java中数据类型分为基本数据类型和引用数据类型。基本数据类型由虚拟机预先定义,引用数据类型则需要进行类的加载

![image-20220731100627521](images\image-20220731100627521.png)

当程序要使用某个类时,如果该类还未被加载到内存中,则系统会通过类的加载、类的链接、类的初始化这三个步骤来对类进行初始化。如果不出现意外,JVM将会连续完成这三个步骤,所以有时也把这三个步骤统称为类加载或者初始化

从程序中类的使用过程看:

![image-20220731100737505](images\image-20220731100737505.png)

### 过程一:类的加载(Loading)

类的加载指的是将类的.class文件中的二进制数据读取到内存中,存放在运行时数据区的方法区中,并创建一个大的Java.lang.Class对象,用来封装方法区内的数据结构 在加载类时,Java虚拟机必须完成以下3件事情:

1. 通过类的全名,获取类的二进制数据流
2. 解析类的二进制数据流为方法区内的数据结构(Java类模型)
3. 创建java.lang.Class类的实例,表示该类型。作为方法区这个类的各种数据的访问入口

![image-20220731101001555](images\image-20220731101001555.png)

我们也可以这样去理解:所谓装载(加载),简而言之就是将Java类的字节码文件加载到机器内存中,并在内存中构建出Java类的原型——类模板对象(所谓类模板对象,其实就是Java类在JVM内存中的一个快照,JVM将从字节码文件中解析出的常量池、类字段、类方法等信息存储到类模板中,这样JVM在运行期便能通过类模板而获取Java类中的任意信息,能够对Java类的成员变量进行遍历,也能进行Java方法的调用)

对于类的二进制数据流,[虚拟机](https://so.csdn.net/so/search?q=虚拟机&spm=1001.2101.3001.7020)可以通过多种途径产生或获得(只要所读取的字节码符合JVM：

1. 虚拟机可能通过文件系统读入一个class后缀的文件(最常见)
2. 读入jar、zip等归档数据包,提取类文件。
3. 事先存放在数据库中的类的二进制数据
4. 使用类似于HTTP之类的协议通过网络进行加载
5. 在运行时生成一段Class的二进制信息等

Class实例的位置：(类将.class文件加载至元空间后,会在堆中创建一个Java.lang.Class对象,用来封装类位于方法区内的数据结构,该Class对象是在加载类的过程中创建的,每个类都对应有一个Class类型的对象)

### 过程二:链接(Linking)

1. 验证:确保Class文件的字节流中包含信息符合当前虚拟机要求,保证被加载类的正确性

- ​	目的是确保Class文件的字节流中包含信息符合当前虚拟机要求,保证被加载类的正确性,不会危害虚拟机自身安全
- ​	主要包括四种验证:文件格式验证,元数据验证,字节码验证,符号引用验证
- ​	格式检查:是否以魔术oxCAFEBABE开头,主版本和副版本是否在当前Java虚拟机的支持范围内,数据中每一项是否都拥有正确的长度等

![image-20220731101255220](images\image-20220731101255220.png)

2. 准备(静态变量,不能是常量)

- 为类变量分配内存并且设置该类变量的默认初始化值
- 这里不包含用final修饰的static,因为final在编译的时候就会分配了,准备阶段会显式赋值
- 这里不会为实例变量分配初始化,类变量会分配在方法区中,而实例变量会随着对象一起分配到Java堆中
- 注意:Java并不支持boolean类型,对于boolean类型,内部实现是int,由于int的默认值是0,故对应的,boolean的默认值就是false

![image-20220731101544309](images\image-20220731101544309.png)

3. 解析:将常量池中的符号引号转换为直接引用的过程(简言之,将类、接口、字段和方法的符号引用转为直接引用)

虚拟机在加载Class文件时才会进行动态链接,也就是说,Class文件中不会保存各个方法和字段的最终内存布局信息,因此,这些字段和方法的符号引用不经过转换是无法直接被虚拟机使用的。当虚拟机运行起来时,需要从常量池中获得对应的符号引用,再在类加载过程中(初始化阶段)将其替换直接引用,并翻译到具体的内存地址中

符号引用:符号引用以一组符号来描述所引用的目标,符号可以是任何形式的字面量,只要使用时能无歧义地定位到目标即可。符号引用与虚拟机实现的内存布局无关,引用的目标并不一定已经加载到了内存中

直接引用:直接引用可以是直接指向目标的指针、相对偏移量或是一个能间接定位到目标的句柄。直接引用是与虚拟机实现的内存布局相关的,同一个符号引用在不同虚拟机实例上翻译出来的直接引用一般不会相同。如果有了直接引用,那说明引用的目标必定已经存在于内存之中了。

不过Java虚拟机规范并没有明确要求解析阶段一定要按照顺序执行。在HotSpot VM中,加载、验证、准备和初始化会按照顺序有条不紊地执行,但链接阶段中的解析操作往往会伴随着JVM在执行完初始化之后再执行

符号引号有:类和接口的权限定名、字段的名称和描述符、方法的名称和描述符

### 初始化(Initialization)

为类变量赋予正确的初始化值

初始化阶段就是执行类构造器方法< clinit >()的过程。此方法不需要定义,是javac编译器自动收集类中的所有类变量的赋值动作和静态代码快中的语句合并而来

```java
public class ClassInitTest {
    private  static int num=1; //类变量的赋值动作
    //静态代码快中的语句
    static{
        num=2;
        number=20;
        System.out.println(num);
        //System.out.println(number); 报错:非法的前向引用
    }
    //Linking之prepare: number=0 -->initial:20-->10
    private static int number=10;

    public static void main(String[] args) {
        System.out.println(ClassInitTest.num);
        System.out.println(ClassInitTest.number);
    }
}

```

![image-20220731101939856](images\image-20220731101939856.png)

若该类具有父类,Jvm会保证子类的< clinit >() 执行前,父类的< clinit >() 已经执行完成。clinit 不同于类的构造方法(init) (由父及子,静态先行)

```java
public class ClinitTest1 {
    static class Father{
        public static int A=1;
        static{
            A=2;
        }
    }
    static class Son extends Father{
        public static int B=A;
    }

    public static void main(String[] args) {
        //这个输出2,则说明父类已经全部加载完毕
        System.out.println(Son.B);
    }
}

```

Java编译器并不会为所有的类都产生`<clinit>()`初始化方法。哪些类在编译为字节码后,字节码文件中将不会包含`<clinit>()`方法？

- 一个类中并没有声明任何的类变量,也没有静态代码块时
- 一个类中声明类变量,但是没有明确使用类变量的初始化语句以及静态代码块来执行初始化操作时
- 一个类中包含static final修饰的基本数据类型的字段,这些类字段初始化语句采用编译时常量表达式 (如果这个static final 不是通过方法或者构造器,则在链接阶段)

```java
public class InitializationTest1 {
    //场景1:对应非静态的字段,不管是否进行了显式赋值,都不会生成<clinit>()方法
    public int num = 1;
    //场景2:静态的字段,没有显式的赋值,不会生成<clinit>()方法
    public static int num1;
    //场景3:比如对于声明为static final的基本数据类型的字段,不管是否进行了显式赋值,都不会生成<clinit>()方法
    public static final int num2 = 1;
}
```

static与final的搭配问题

(使用static + final修饰,且显示赋值中不涉及到方法或构造器调用的基本数据类型或String类型的显式赋值,是在链接阶段的准备环节进行)

```java

/**
 * 说明:使用static + final修饰的字段的显式赋值的操作,到底是在哪个阶段进行的赋值？
 * 情况1:在链接阶段的准备环节赋值
 * 情况2:在初始化阶段<clinit>()中赋值
 * 结论:
 * 在链接阶段的准备环节赋值的情况:
 * 1. 对于基本数据类型的字段来说,如果使用static final修饰,则显式赋值(直接赋值常量,而非调用方法)通常是在链接阶段的准备环节进行
 * 2. 对于String来说,如果使用字面量的方式赋值,使用static final修饰的话,则显式赋值通常是在链接阶段的准备环节进行
 *
 * 在初始化阶段<clinit>()中赋值的情况:
 * 排除上述的在准备环节赋值的情况之外的情况。
 * 最终结论:使用static + final修饰,且显示赋值中不涉及到方法或构造器调用的基本数据类型或String类型的显式赋值,是在链接阶段的准备环节进行。
 */
public class InitializationTest2 {
    public static int a = 1;//在初始化阶段<clinit>()中赋值
    public static final int INT_CONSTANT = 10;//在链接阶段的准备环节赋值

    public static final Integer INTEGER_CONSTANT1 = Integer.valueOf(100);//在初始化阶段<clinit>()中赋值
    public static Integer INTEGER_CONSTANT2 = Integer.valueOf(1000);//在初始化阶段<clinit>()中赋值

    public static final String s0 = "helloworld0";//在链接阶段的准备环节赋值
    public static final String s1 = new String("helloworld1");//在初始化阶段<clinit>()中赋值

    public static String s2 = "helloworld2";
    public static final int NUM1 = new Random().nextInt(10);//在初始化阶段<clinit>()中赋值
}

```

clinit()的调用会死锁吗?

1. 虚拟机会保证一个类的`<clinit>()`方法在多线程环境中被正确地加锁、同步,如果多个线程同时去初始化一个类,那么只会有一个线程去执行这个类的()方法,其他线程都需要阻塞等待,直到活动线程执行`<clinit>()`方法完毕
2. 正是因为函数`<clinit>()`带锁线程安全的,因此,如果在一个类的`<clinit>()`方法中有耗时很长的操作,就可能造成多个线程阻塞,引发死锁。并且这种死锁是很难发现的,因为看起来它们并没有可用的锁信息

```java

class StaticA {
    static {
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
        }
        try {
            Class.forName("com.xiaozhi.StaticB");
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
        System.out.println("StaticA init OK");
    }
}

class StaticB {
    static {
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
        }
        try {
            Class.forName("com.xiaozhi.StaticA");
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
        System.out.println("StaticB init OK");
    }
}

public class StaticDeadLockMain extends Thread {
    private char flag;

    public StaticDeadLockMain(char flag) {
        this.flag = flag;
        this.setName("Thread" + flag);
    }

    @Override
    public void run() {
        try {
            Class.forName("com.xiaozhi.Static" + flag);
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
        System.out.println(getName() + " over");
    }

    public static void main(String[] args) throws InterruptedException {
        StaticDeadLockMain loadA = new StaticDeadLockMain('A');
        loadA.start();
        StaticDeadLockMain loadB = new StaticDeadLockMain('B');
        loadB.start();
    }
}

```

### 主动引用(触发在初始化阶段的Clinit方法)

①. 当创建一个类的实例时,比如使用new关键字,或者通过反射、克隆、反序列化

②. 访问某个类或接口的静态变量,或者对该静态变量赋值

③. 调用类的静态方法

④. 反射(比如:Class.forName(“com.xiaozhi.Test”))

⑤. 初始化一个子类(当初始化子类时,如果发现其父类还没有进行过初始化,则需要先触发其父类的初始化)

⑥. 当虚拟机启动时,用户需要指定一个要执行的主类(包含main()方法的那个类),虚拟机会先初始化这个主类

⑦. JDK7开始提供的动态语言支持(涉及解析REF_getStatic、REF_putStatic、REF_invokeStatic方法句柄对应的类)

⑧. 如果一个接口定义了default方法,那么直接实现或者间接实现该接口的类的初始化,该接口要在其之前被初始化

### 被动使用

①. 除了以上的情况属于主动使用,其他的情况均属于被动使用。被动使用不会引起类的初始化。意味着没有\<clinit>()的调用。

②. 调用ClassLoader类的loadClass()方法加载一个类,并不是对类的主动使用,不会导致类的初始化

③. 当访问一个静态字段时,只有真正声明这个字段的类才会被初始化。当通过子类引用父类的静态变量,不会导致子类初始化

④. 引用常量不会触发此类或接口的初始化。因为常量在链接阶段就已经被显式赋值了

⑤. 通过数组定义类引用,不会触发此类的初始化


### 类的Using(使用)

①. 任何一个类型在使用之前都必须经历过完整的加载、链接和初始化3个类加载步骤。一旦一个类型成功经历过这3个步骤之后,便"万事俱备,只欠东风"就等着开发者使用了

②. 开发人员可以在程序中访问和调用它的静态类成员信息(比如:静态字段、静态方法)或者使用new关键字为其创建对象实例


### 类的Unloading(卸载)

类、类的加载器、类的实例之间的引用关系

1. 在类加载器的内部实现中,用一个Java集合来存放所加载类的引用。另一方面,一个Class对象总是会引用它的类加载器,调用Class对象的getClassLoader()方法,就能获得它的类加载器。由此可见,代表某个类的Class实例与其类的加载器之间为双向关联关系
2. 一个类的实例总是引用代表这个类的Class对象。在Object类中定义了getClass()方法,这个方法返回代表对象所属类的Class对象的引用。此外,所有的Java类都有一个静态属性class,它引用代表这个类的Class对象

![image-20220731103527100](images\image-20220731103527100.png)

方法区的垃圾回收

1. 方法区的垃圾收集主要回收两部分内容:常量池中废弃的常量和不再使用的类型。
2. HotSpot虚拟机对常量池的回收策略是很明确的,只要常量池中的常量没有被任何地方引用,就可以被回收
3. 判定一个常量是否"废弃”还是相对简单,而要判定一个类型是否属于"不再被使用的类”的条件就比较苛刻了。需要同时满足下面三个条件
   

![image-20220731104320397](images\image-20220731104320397.png)

1. 启动类加载器加载的类型在整个运行期间是不可能被卸载的(jvm和jls规范)
2. 被系统类加载器和扩展类加载器加载的类型在运行期间不太可能被卸载,因为系统类加载器实例或者扩展类的实例基本上在整个运行期间总能直接或者间接的访问的到,其达到unreachable的可能性极小
3. 开发者自定义的类加载器实例加载的类型只有在很简单的上下文环境中才能被卸载,而且一般还要借助于强制调用虚拟机的垃圾收集功能才可以做到。可以预想,稍微复杂点的应用场景中(比如:很多时候用户在开发自定义类加载器实例的时候采用缓存的策略以提高系统性能),被加载的类型在运行期间也是几乎不太可能被卸载的(至少卸载的时间是不确定的)。

## 类的加载器介绍

ClassLoader的作用：ClassLoader是Java的核心组件,所有的Class都是由ClassLoader进行加载的,ClassLoader负责通过各种方式将Class信息的二进制数据流读入JVM内部,转换为一个与目标类对应的java.lang.Class对象实例。然后交给Java虚拟机进行链接、初始化等操作、因此,ClassLoader在整个装载(加载)阶段,只能影响到类的加载,而无法通过ClassLoader去改变类的链接和初始化行为。至于它是否可以运行,则由Execution Engine决定

类加载器最早出现在Java1.0版本中,那个时候只是单纯地为了满足Java Applet应用而研发出来。但如今类加载器却在OSGI(热部署)、字节码加密解密领域大放异彩。这主要归功于Java虚拟机的设计者当初在设计类加载器的时候,并没有考虑将它绑定在Jvm内部,这样做的好处就是能够更加灵活和动态地执行类加载操作

![image-20220731110215927](images\image-20220731110215927.png)

class文件的显式加载与隐式加载的方式是指JVM加载class文件到内存的方式(在日常开发以上两种方式一般会混合使用)

1. 显式加载:指的是在代码中通过调用ClassLoader加载class对象,如直接使用Class.forName(name)或this.getClass().getClassLoader().loadClass()加载class对象
2. 隐式加载:则是不直接在代码中调用ClassLoader的方法加载class对象,而是通过虚拟机自动加载到内存中,如在加载某个类的class文件时,该类的class文件中引用了另外一个类的对象,此时额外引用的类将通过JVM自动加载到内存中。比如 new User()

### 类的加载器分类与测试

①. JVM支持两种类型的类加载器,分别为引导类加载器(Bootstrap ClassLoader)和自定义类加载器(User-Defined ClassLoader)

②. 从概念上来讲,自定义类加载器一般指的是程序中由开发人员自定义的一类类加载器,但是Java虚拟机规范并没有这么定义,而是将所有派生于抽象类ClassLoader的类加载器都划分为自定义类加载器

③. 无论类加载器的类型如何划分,在程序中我们常见的类加载器如下所示: 除了顶层的启动类加载器外,其余的类加载器都应当有自己的"父类"加载器


![image-20220731110413159](images\image-20220731110413159.png)

![image-20220731110435411](images\image-20220731110435411.png)

![image-20220731110515417](images\image-20220731110515417.png)

### 启动(引导)类加载器 Bootstrap

①. 这个类加载使用C/C++语言实现的,嵌套在JVM内部

②. 它用来加载Java的核心类库(JAVA_HOME/jre/lib/rt.jar、resource.jar或sum.boot.class.path路径下的内容),用于提供JVM自身需要的类(String类就是使用的这个类加载器)

③. 由于安全考虑,Bootstrap启动类加载器只加载包名为java、javax、sun等开头的类

④. 并不继承自java.lang.ClassLoader,没有父加载器

⑤. 加载扩展类和应用程序类加载器,并指定为他们的父类加载器

### 扩展类加载器 Extension

①. Java语言编写,由sum.music.Launcher$ExtClassLoader实现

②. 派生于ClassLoader类,父类加载器为启动类加载器

③. 从java.ext.dirs系统属性所指定的目录中加载类库,或从JDK的安装目录的jre/lib/ext子目录(扩展目录)下加载类库。如果用户创建的JAR放在此目录下,也会自动由扩展类加载器加载


![image-20220731110639291](images\image-20220731110639291.png)

### 应用程序(系统)类加载器 AppClassLoader

①. java语言编写,由sum.misc.Launcher$AppClassLoader实现

②. 派生于ClassLoader类,父类加载器为扩展类加载器

③. 它负责加载环境变量classpath或系统属性java.class.path指定路径下的类库

④. 该类加载是程序中默认的类加载器,一般来说,Java应用的类都是由它来完成加载

⑤. 通过ClassLoader的getSystemClassLoader()方法可以获取到该类加载器

### 用户自定义类加载器

①. 在Java的日常应用程序开发中,类的加载几乎是由上述3种类加载器相互配合执行的,在必要时,我们换可以自定义类加载器,来定制类的加载方式(自定义类加载器通常需要继承于 ClassLoader)

②. 体现Java语言强大生命力和巨大魅力的关键因素之一便是,Java 开发者可以自定义类加载器来实现类库的动态加载,加载源可以是本地的JAR包,也可以是网络上的远程资源

③. 自定义 ClassLoader 的子类时候,我们常见的会有两种做法:
             1.  重写loadClass()方法(不推荐,这个方法会保证类的双亲委派机制)
             2.  重写findClass()方法 -->推荐
             3.  这两种方法本质上差不多,毕竟loadClass()也会调用findClass(),但是从逻辑上讲我们最好不要直接修改loadClass()的内部逻辑。建议的做法是只在findClass()里重写自定义类的加载方法,根据参数指定类的名字,返回对应的Class对象的引用。

手写一个简单的自定义加载器



```java
package com.harry.jvm.classLoader;

import java.io.ByteArrayOutputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

public class UserClassLoader extends ClassLoader{
    private String rootDir;

    public UserClassLoader(ClassLoader parent, String rootDir) {
        this.rootDir = rootDir;
    }

    @Override
    protected Class<?> findClass(String name) throws ClassNotFoundException {
        // 获取类的class文件字节码数组

        byte[] classData = new byte[0];
        try {
            classData = getClassDate(name);
            if (classData == null) {
                throw new ClassNotFoundException();
            } else {
                //直接生成class对象
                return defineClass(name, classData, 0, classData.length);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        return null;

    }
    private byte[] getClassDate(String className) throws IOException {
        // 读取类文件的字节
        String path = classNameToPath(className);
        FileInputStream ins = new FileInputStream(path);
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        byte[] buffer = new byte[1024];
        int len = 0;
        // 读取类文件的字节码
        while ((len = ins.read(buffer)) != -1) {
            baos.write(buffer, 0, len);
        }
        return baos.toByteArray();

    }

    /**
     * 类文件的完全路径
     */
    private String classNameToPath(String className) {
        return rootDir + "\\" + className.replace('.', '\\') + ".class";
    }

}

```

### 测试不同的类加载器

每个Class对象都会包含一个定义它的ClassLoader的一个引用

获取ClassLoader的途径

```
(1). 获得当前类的ClassLoader
clazz.getClassLoader()
(2). 获得当前线程上下文的ClassLoader(系统类加载器)
Thread.currentThread().getContextClassLoader()
(3). 获得系统的ClassLoader
ClassLoader.getSystemClassLoader()

```

站在程序的角度看,引导类加载器与另外两种类加载器(系统类加载器和扩展类加载器)并不是同一个层次意义上的加载器,引导类加载器是使用C++语言编写而成的,而另外两种类加载器则是使用Java语言编写而成的。由于引导类加载器压根儿就不是一个Java类,因此在Java程序中只能打印出空值

数组类的Class对象,不是由类加载器去加载的,而是在Java运行期JVM根据需要自动创建的。对于数组的类加载器来说,是通过Class.getClassLoader()返回的,与数组中元素类型的类加载器是一样的;如果数组当中的元素类型是基本数据类型,数组类是没有类加载器的(基本数据类型由虚拟机预先定义)

```java
public class ClassLoaderDemo {
    public static void main(String[] args) {
        ClassLoader classloader1 = ClassLoader.getSystemClassLoader();
        //sun.misc.Launcher$AppClassLoader@18b4aac2
        System.out.println(classloader1);
        //获取到扩展类加载器
        //sun.misc.Launcher$ExtClassLoader@424c0bc4
        System.out.println(classloader1.getParent());
        //获取到引导类加载器 null
        System.out.println(classloader1.getParent().getParent());
        //获取系统的ClassLoader
        ClassLoader classloader2 = Thread.currentThread().getContextClassLoader();
        //sun.misc.Launcher$AppClassLoader@18b4aac2
        System.out.println(classloader2);
        String[]strArr=new String[10];
        ClassLoader classLoader3 = strArr.getClass().getClassLoader();
        //null,表示使用的是引导类加载器
        System.out.println(classLoader3);
        ClassLoaderDemo[]refArr=new ClassLoaderDemo[10];
        //sun.misc.Launcher$AppClassLoader@18b4aac2
        System.out.println(refArr.getClass().getClassLoader());
        int[]intArr=new int[10];
        //null,如果数组的元素类型是基本数据类型,数组类是没有类加载器的
        System.out.println(intArr.getClass().getClassLoader());
    }
}

```

###  ClassLoader源码剖析

#### ClassLoader与现有类加载器的关系

- ClassLoader是一个抽象类。如果我们给定了一个类的二进制名称,类加载器应尝试去定位或生成构成定义类的数据。一种典型的策略是将给定的二进制名称转换为文件名,然后去文件系统中读取这个文件名所对应的class文件
- ClassLoader与现有类加载器的关系

![image-20220731112646279](images\image-20220731112646279.png)

- ExtClassLoader并没有重写loadClass()方法,这足矣说明其遵循双亲委派模式
-  AppClassLoader重载了loadClass()方法,但最终调用的还是父类loadClass()方法,因此依然遵守双亲委派模式。

#### 抽象类ClassLoader的主要方法(内部没有抽象方法)

①. public final ClassLoader getParent():返回该类加载器的超类加载器

②. public Class<?> loadClass(String name) throws ClassNotFoundException
(加载名称为name的类,返回结果为java.lang.Class类的实例。如果找不到类,则返回ClassNot FoundException 异常。该方法中的逻辑就是双亲委派模式的实现)

③. protected Class<?> findClass (String name) throws ClassNotFoundException
查找二进制名称为name的类,返回结果为java.lang.Class类的实例。这是一个受保护的方法,JVM鼓励我们重写此方法,需要自定义加载器遵循双亲委托机制,该方法会在检查完父类加载器之后被loadClass()方法调用。

④. protected final Class<?> defineClass(String name, byte[] b, int off, int len)
根据给定的字节数组b转换为Class的实例,off和len参数表示实际Class信息在byte数组中的位置和长度,其中byte数组b是ClassLoader从外部获取的。这是受保护的方法,只有在自定义ClassLoader子类中可以使用。

⑤. protected final void resolveClass(Class<?> c)
链接指定的一个Java类。使用该方法可以使用类的Class对象创建完成的同时也被解析。前面我们说链接阶段主要是对字节码进行验证,为类变量分配内存并设置初始值同时将字节码文件中的符号引用转换为直接引用

源码解析Classloader方法

```java
 测试代码:
 ClassLoader.getSystemClassLoader().loadClass("com.xiaozhi.java.User");
 //resolve==true,加载class的同时需要进行解析操作
 protected Class<?> loadClass(String name, boolean resolve) 
        throws ClassNotFoundException
    {
		//同步操作,保证只能加载一次
        synchronized (getClassLoadingLock(name)) {
            // 在缓存中判断是否已经加载同名的类
            Class<?> c = findLoadedClass(name);
            if (c == null) {
                long t0 = System.nanoTime();
                try {
					//获取当前类的父类加载器
                    if (parent != null) {
						//如果存在父类加载器,则调用父类加载器进行类的加载(双亲委派机制)
                        c = parent.loadClass(name, false);
                    } else {
						//parent==null 父类加载器是引导类加载器
                        c = findBootstrapClassOrNull(name);
                    }
                } catch (ClassNotFoundException e) {
                    // ClassNotFoundException thrown if class not found
                    // from the non-null parent class loader
                }
				// 当前类的加载器的父类加载器未加载此类 or 当前类的加载器未加载此类
                if (c == null) {
                    // 调用当前classloader的findClass
                    long t1 = System.nanoTime();
                    c = findClass(name);

                    // this is the defining class loader; record the stats
                    sun.misc.PerfCounter.getParentDelegationTime().addTime(t1 - t0);
                    sun.misc.PerfCounter.getFindClassTime().addElapsedTimeFrom(t1);
                    sun.misc.PerfCounter.getFindClasses().increment();
                }
            }
			//是否进行解析操作
            if (resolve) {
                resolveClass(c);
            }
            return c;
        }
    }

```

#### Class.forName()与ClassLoader.loadClass()对比

①. Class.forName():是一个静态方法,最常用的是Class.forName(String className);根据传入的类的全限定名返回一个 Class 对象。该方法在将 Class 文件加载到内存的同时,会执行类的初始化。如:Class.forName(“com.atguigu.java.HelloWorld”);

②. ClassLoader.loadClass():这是一个实例方法,需要一个 ClassLoader 对象来调用该方法。该方法将 Class 文件加载到内存时,并不会执行类的初始化,直到这个类第一次使用时才进行初始化。该方法因为需要得到一个 ClassLoader 对象,所以可以根据需要指定使用哪个类加载器。

### 双亲委派机制

1. 如果一个类加载收到了类加载请求,它并不会自己先去加载,而是把这个请求委托给父类加载器去执行
2. 如果父类加载器还存在其父类加载器,则进一步向上委托,依次递归,请求最终将到达顶层的启动类加载器
3. 如果父类的加载器可以完成类的加载任务,就成功返回,倘若父类加载器无法完成此加载任务,子加载器才会尝试自己去加载,这就是双亲委派模式

![image-20220731113028290](images\image-20220731113028290.png)

本质(规定了类加载的顺序是:引导类加载器先加载,若加载不到,由扩展类加载器加载,若还加载不到,才会由系统类加载器或自定义的类加载器进行加载)

![image-20220731113105368](images\image-20220731113105368.png)

源码分析(双亲委派机制在java.lang.ClassLoader.loadClass(String,boolean)接口中体现。该接口的逻辑如下)

1. 先在当前加载器的缓存中查找有无目标类,如果有,直接返回。
2. 判断当前加载器的父加载器是否为空,如果不为空,则调用parent.loadClass(name, false)接口进行加载
3. 反之,如果当前加载器的父类加载器为空,则调用findBootstrapClassOrNull(name)接口,让引导类加载器进行加载
4. 如果通过以上3条路径都没能成功加载,则调用findClass(name)接口进行加载。该接口最终会调用java.lan g.ClassLoader接口的defineClass系列的native接口加载目标Java类。
5. 双亲委派的模型就隐藏在这第2和第3步中

#### 双亲委派机制优势

1. 避免类的重复加载,确保一个类的全局唯一性(当父ClassLoader已经加载了该类的时候,就没有必要子ClassLoader再加载一次)
2. 保护程序安全,防止核心API被随意篡改  (自定义类:java.lang.String | java.lang.ShkStart)

#### 双亲委托模式的弊端

检查类是否加载的委托过程是单向的,这个方式虽然从结构上说比较清晰,使各个ClassLoader的职责非常明确,但是同时会带来一个问题,即顶层的ClassLoader无法访问底层的ClassLoader所加载的类)

### 沙箱安全机制

 如图,虽然我们自定义了一个java.lang包下的String尝试覆盖核心类库中的String,但是由于双亲委派机制,启动加载器会加载java核心类库的String类(BootStrap启动类加载器只加载包名为java、javax、sun等开头的类),而核心类库中的String并没有main方法
![image-20220731113345898](images\image-20220731113345898.png)

自定义String类,但是在加载自定义String类的时候先使用引导类加载器加载,而引导类加载器在加载过程中会先加载jdk自带的文件(rt.jar包中的java\lang\String.class),报错信息说没有main方法就是因为加载的是rt.jar包中的String类。这样可以保证对java核心源代码的保护,这就是沙箱安全机制

# 三 运行时数据区

## 程序计数器

①. 作用 (是用来存储指向下一条指令的地址,也即将要执行的指令代码。由执行引擎读取下一条指令)

②. 特点(是线程私有的 、不会存在内存溢出)

③. 注意:在物理上实现程序计数器是在寄存器实现的,整个cpu中最快的一个执行单元

④. 它是唯一一个在java虚拟机规范中没有OOM的区域

解释:
(1). 每个线程都有一个程序计数器,是线程私有的,就是一个指针,指向方法区中的方法字节码(用来存储指向下一条指令的地址,也即将要执行的指令代码),由执行引擎读取下一条指令,是一个非常小的内存空间,几乎可以忽略不记
(2). 这块内存区域很小,它是当前线程所执行的字节码的行号指示器,字节码解释器通过改变这个计数器的值来选取下一条需要执行的字节码指令
(3). 如果执行的是一个Native方法,那这个计数器是undefined

![image-20220731113735843](images\image-20220731113735843.png)

![image-20220731113757564](images\image-20220731113757564.png)

使用PC寄存器存储字节码指令地址有什么用呢?
为什么使用PC寄存器记录当前线程的执行地址呢?

1. 因为CPU需要不停的切换各个线程,这时候切换回来以后,就得知道接着从哪开始继续执行
2. JVM的字节码解释器就需要通过改变PC寄存器的值来明确下一条应该执行什么样的字节码指令

 关于线程在JVM中的说明:

1. 在Hotspot JVM里,每个线程都与操作系统的本地线程直接映射
   (解释:当一个Java线程准备好执行以后,此时一个操作系统的本地线程也同时创建.Java线程执行终止后,本地线程也会被回收)
2. 操作系统负责所有线程的安排调度到任何一个可用的CPU上。一旦本地线程初始化完毕,它就会调用Java线程中的run方法

## 本地方法栈

本地接口的作用是融合不同的编程语言为Java所用,它的初衷是融合C/C++程序,Java诞生的时候是C/C++横行的时候,要想立足,必须由调用C/C++程序,于是就在内存中专门开辟了一块区域处理标记为native的代码,它的具体做法是Native Method Stack中登记native方法,在Execution Engine执行时加载native libraies

目前该方法的使用的越来越少了,除非是与硬件有关的应用,比如通过Java程序驱动打印机或者Java系统管理生产设备,在企业级应用中已经比较少见。因为现在的异构领域间的通信很发达,比如可以使用Socket通信,也可以使用Web Service等等,不多做介绍

本地方法栈(Native Method Stack) (它的具体做法是Native Method Stack中登记native方法,在Execution Engine 执行时加载本地方法库)

 native方法的举例: Object类中的clone wait notify hashCode 等 Unsafe类都是native方法

## 虚拟机栈

每创建一个线程就会创建一个Java栈,每一个Java栈中都会有很多栈帧(局部变量表 | 操作数栈 | 动态链接 | 方法返回地址 | 一些附加信息)
注意:虚拟机栈中不存在GC,但是存在StackOverflowError和OOM

解释:
(1). 虚拟机栈(Java Virtual Machine Stacks)和线程是紧密联系的,每创建一个线程时就会对应创建一个Java栈,所以Java栈也是"线程私有"的内存区域,这个栈中又会对应包含多个栈帧,每调用一个方法时就会往栈中创建并压入一个栈帧,栈帧是用来存储方法数据和部分过程结果的数据结构,每一个方法从调用到最终返回结果的过程,就对应一个栈帧从入栈到出栈的过程(先进后出)
(2). 栈帧中有如下部分组成:
![image-20220801203928210](images\image-20220801203928210.png)

存放于栈中的东西如下
(8种基本类型的变量+对象的引用变量+实例方法都是在函数的栈内存中分配[局部变量])

栈内存溢出(StackOverflowError) `-Xss`参数

1. 栈帧过多导致栈内存溢出(方法的递归调用,没设置正确停止条件)
2. 局部数组过大。当函数内部的数组过大时,有可能导致堆栈溢出

Java虚拟机规范允许Java栈的大小是动态的或者是固定不变的 掌握

1. 如果采用固定大小的Java虚拟机栈,那每一个线程的Java虚拟机栈容量可以在线程创建的时候独立选定。
2. 如果线程请求分配的栈容量超过Java虚拟机栈允许的最大容量,Java虚拟机将会抛出一个StackoverflowError异常
3. 如果Java虚拟机栈可以动态扩展,并且在尝试扩展的时候无法申请到足够的内存,或者是在创建新的线程时就没有足够的内存区创建对应的虚拟机栈,那Java虚拟机将会抛出一个OutOfMemoryError异常

如何设置栈内存的大小？ -Xss size (即:-XX:ThreadStackSize)

一般默认为512k-1024k,取决于操作系统(jdk5之前,默认栈大小是256k;jdk5之后,默认栈大小是1024k)
栈的大小直接决定了函数调用的最大可达深度

![image-20220801204119613](images\image-20220801204119613.png)

栈和堆的区别是什么?

1. 从GC、OOM、StackOverflowError的角度。
   (栈中不存在GC,当固定大小的栈会发生StackOverflowError,动态的会发生OOM。堆中GC、OOM、StackOverflowError都存在)
2. 从堆栈的执行效率
   (栈的效率高于堆)
3. 内存大小,数据结构
   (堆的空间比栈的大一般,栈是一种FIFO先进后出的模型。堆中结构复杂,可以有链表、数组等)
4. 栈管运行,堆管存储
   

### 局部变量表(LocalVariables)

①. 定义为一个数字数组,主要用于存储方法参数和定义在方法体内的局部变量(这些数据类型包括各种基本数据类型、对象引用(reference)以及return Address类型)

②. 由于局部变量是建立在线程的栈上,是线程私有数据,因此不存在数据安全问题

③. 局部变量表所需容量大小是在编译期确定下来的。(并保存在方法Code属性的maximum local variables数据项中,在方法运行期间不会改变局部变量表的大小的)

```java
//使用javap -v 类.class 或者使用jclasslib
public class LocalVariableTest {
    public static void main(String[] args) {
        LocalVariableTest test=new LocalVariableTest();
        int num=10;
        test.test1();
    }
    public static void test1(){
        Date date=new Date();
        String name="xiaozhi";
    }
}

```

### 关于slot的理解(引用数据类型(方法的返回地址)占用1个slot)

1. 局部变量表,是基本的存储单元是slot(变量槽)
2. 在局部变量表中,32位以内的类型只占有一个slot(包括引用数据类型),64位的类型(long和double)占有两个slot
3. byte、short、char在存储前被转换为int,boolean也被转换为int(0表示fasle,非0表示true)。long和double则占据两个slot

Jvm会为局部变量表中的每一个slot都分配一个访问索引,通过这个索引即可成功访问到局部变量表中指定的局部变量值

如果需要访问局部变量表中一个64bit的局部变量值时,只需要使用前一个索引即可(比如:访问long或double类型变量)

![image-20220801204535840](images\image-20220801204535840.png)

如果当前帧是由构造方法或者实例方法创建,那么该对象引用this将会放在index为0的slot处

![image-20220801204628180](images\image-20220801204628180.png)

栈帧中的局部变量表中的槽位是可以复用的,如果一个局部变量过了其作用域,那么在其作用域之后申请的新的局部变量就很可能会复用过期局部变量的槽位,从而节省资源的目的

与GC Roots的关系
局部变量表中的变量也是重要的垃圾回收根节点,只要被局部变量表中直接或间接引用的对象都不会被回收

### 操作数栈(operand stack)

1. 我们说Java虚拟机的解释引擎是基于栈的执行引擎,其中的栈指的就是操作数栈。
2. 每一个独立的栈帧中除了包含局部变量表以外,还包含了一个后进先出的操作数栈,也可以称之为表达式栈
3.  操作数栈,在方法执行过程中,根据字节码指令,往栈中写入数据或提取数据,即入栈或出栈
4. 每一个操作数栈都会拥有一个明确的栈深度用于存储数值,其所需的最大深度在编译期就定义好了,保存在方法的Code属性中,为max_stack的值
5. 栈中的任何一个元素都是可以任意的Java数据类型：2bit的类型占用一个栈单位深度   64bit的类型占用两个栈单位深度
6. 如果被调用的方法带有返回值的话,其返回值将会被压入当前栈帧的操作数栈中,并更新PC寄存器中下一条需要执行的字节码指令
7. 操作数栈,主要用于保存计算机过程的中间结果,同时作为计算过程中变量临时的存储空间 掌握

操作数栈的具体说明(一)

这里的代码中操作数栈的长度最大是2,在iload_1、iload_2的时候

```java
	public void testAddOperation(){
	    byte i = 15;
	    int j = 8;
	    int k = i + j;
	}

```

![image-20220801205104283](images\image-20220801205104283.png)

![image-20220801205130671](images\image-20220801205130671.png)

![image-20220801205202307](images\image-20220801205202307.png)

![image-20220801205233715](images\image-20220801205233715.png)

![image-20220801205352905](images\image-20220801205352905.png)

![image-20220801205504015](images\image-20220801205504015.png)

![image-20220801205610549](images\image-20220801205610549.png)

![image-20220801205638328](images\image-20220801205638328.png)

![image-20220801205653708](images\image-20220801205653708.png)

### 操作数栈的具体说明(二)

1. 局部变量有多少个?
2. 操作数栈的最大深度是多少?

![image-20220807095159792](images\image-20220807095159792.png)

```java
public class OperandStackTest {
    public void testAddOperation(){
        //byte、short、char、boolean:都以int型保存
        byte i=15;
        short j=8;
        int k=i+j;

        long m=12L;
        int n=800;
        //存在宽化类型转换
        m=m*n;
    }
}

```

![image-20220807095444934](images\image-20220807095444934.png)

### 操作数栈的具体说明(三)

操作数栈的最大深度是2,这个2是在(new #2 、dup的时候)

```java
public class OperandStackTest {
    public static void main(String[] args) {
        OperandStackTest test=new OperandStackTest();
        int num=10;
        test.testAddOperation();
    }
    public void testAddOperation(){
        //byte、short、char、boolean:都以int型保存
        byte i=15;
        short j=8;
        int k=i+j;

        long m=12L;
        int n=800;
        //存在宽化类型转换
        m=m*n;
    }

```

```
0 new #2 <com/xiaozhi/jvm/OperandStackTest> 将new的对象放入操作数栈中
 3 dup 复制一份出来,在操作数栈中,这时操作数栈的长度为2
 下面用了dup出来的对象
 4 invokespecial #3 <com/xiaozhi/jvm/OperandStackTest.<init>>
 7 astore_1 将new出来的放入了局部变量表为1的位置,0的位置放的是arg
 8 bipush 10 将10放入操作数栈
10 istore_2  将操作数栈中的10放入局部变量表为2的位置
11 aload_1   将巨变变量表1的位置放入操作数栈中
下面调用了方法,也就意味着操作数栈1的位置出栈了
12 invokevirtual #4 <com/xiaozhi/jvm/OperandStackTest.testAddOperation>
15 return

```

![image-20220807100744407](images\image-20220807100744407.png)

### 动态链接(Dynamic Linking)

运行时常量池位于方法区,字节码中的常量池结构如下:

![image-20220807101413225](images\image-20220807101413225.png)

为什么需要常量池呢？

(常量池的作用,就是为了提供一些符号和常量,便于指令的识别。下面提供一张测试类的运行时字节码文件格式)

![image-20220807101526125](images\image-20220807101526125.png)

![image-20220807101554707](images\image-20220807101554707.png)

每一个栈帧内部都包含一个指向运行时常量池Constant pool或该栈帧所属方法的引用。包含这个引用的目的就是为了支持当前方法的代码能够实现动态链接。比如invokedynamic指令

在Java源文件被编译成字节码文件中时,所有的变量和方法引用都作为符号引用(symbolic Refenrence)保存在class字节码文件(javap反编译查看)的常量池里。比如:描述一个方法调用了另外的其他方法时,就是通过常量池中指向方法的符号引用来表示的,那么动态链接的作用就是为了将这些符号引用(#)最终转换为调用方法的直接引用

#### 方法的调用:(小插曲)难点

①. 静态链接(早期绑定):当一个 字节码文件被装载进JVM内部时,如果被调用的目标方法在编译期可知,且运行期保持不变时。这种情况下将调用方法的符号引用转换为直接引用的过程称之为静态链接
(invokestatic | invokespecial)

②. 动态链接(晚期绑定):如果被调用的方法在编译期无法被确定下来,也就是说,只能够在程序运行期将调用方法的符号引用转换为直接引用,由于这种引用转换过程具备动态性,因此也就被称之为动态链接。体现了多态
(invokevirtual | invokeinterface)

③. 非虚方法: 如果方法在编译器就确定了具体的调用版本,这个版本在运行时是不可变的。这样的方法称为非虚方法
(静态方法、私有方法、final方法、实例构造器(实例已经确定,this()表示本类的构造器)、父类方法(super调用)都是非虚方法)

④. 其他所有体现多态特性的方法称为虚方法

⑤. 如下指令要重点掌握

```
	普通调用指令:
	1.invokestatic:调用静态方法,解析阶段确定唯一方法版本；
	2.invokespecial:调用<init>方法、私有及父类方法,解析阶段确定唯一方法版本；
	3.invokevirtual:调用所有虚方法；
	4.invokeinterface:调用接口方法；
	动态调用指令(Java7新增):
	5.invokedynamic:动态解析出需要调用的方法,然后执行 .
	前四条指令固化在虚拟机内部,方法的调用执行不可人为干预,而invokedynamic指令则支持由用户确定方法版本。
    其中invokestatic指令和invokespecial指令调用的方法称为非虚方法

    其中invokevirtual(final修饰的除外,JVM会把final方法调用也归为invokevirtual指令,但要注意final方法调用不是虚方法)、invokeinterface指令调用的方法称称为虚方法。

```

```java
/**
 * 解析调用中非虚方法、虚方法的测试
 */
class Father {
    public Father(){
        System.out.println("Father默认构造器");
    }

    public static void showStatic(String s){
        System.out.println("Father show static"+s);
    }

    public final void showFinal(){
        System.out.println("Father show final");
    }

    public void showCommon(){
        System.out.println("Father show common");
    }

}

public class Son extends Father{
    public Son(){
        super();
    }

    public Son(int age){
        this();
    }

    public static void main(String[] args) {
        Son son = new Son();
        son.show();
    }

    //不是重写的父类方法,因为静态方法不能被重写
    public static void showStatic(String s){
        System.out.println("Son show static"+s);
    }

    private void showPrivate(String s){
        System.out.println("Son show private"+s);
    }

    public void show(){
        //invokestatic
        showStatic(" 大头儿子");
        //invokestatic
        super.showStatic(" 大头儿子");
        //invokespecial
        showPrivate(" hello!");
        //invokespecial
        super.showCommon();
        //invokevirtual 因为此方法声明有final 不能被子类重写,所以也认为该方法是非虚方法
        showFinal();
        //虚方法如下
        //invokevirtual
        showCommon();//没有显式加super,被认为是虚方法,因为子类可能重写showCommon
        info();

        MethodInterface in = null;
        //invokeinterface  不确定接口实现类是哪一个 需要重写
        in.methodA();

    }

    public void info(){

    }

}

interface MethodInterface {
    void methodA();
}

```

#### 关于invokedynamic指令

①. JVM字节码指令集一直比较稳定,一直到java7才增加了一个invokedynamic指令,这是Java为了实现【动态类型语言】支持而做的一种改进

②. 动态类型语言和静态类型语言两者的却别就在于对类型的检查是在编译期还是在运行期,满足前者就是静态类型语言,反之则是动态类型语言。

③. Java是静态类型语言(尽管lambda表达式为其增加了动态特性),js,python是动态类型语言

#### 方法返回地址(Return Address)

理解如下话:
(pc寄存器每执行一条指令都会被改变
而返回地址在调用call之前一直是上一条call后面的地址,不改变)

①. 存放调用该方法的PC[寄存器](https://so.csdn.net/so/search?q=寄存器&spm=1001.2101.3001.7020)的值

②. 执行引擎遇到任意一个方法返回的字节码指令(return),会有返回值传递给上层的方法调用者,简称正常完成出口



1. 一个方法在正常调用完成之后究竟需要使用哪一个返回指令还需要根据方法返回值的实际数据类型而定
2. 在字节码指令中,返回指令包含ireturn(当返回值是boolena、byte、char、short和int类型时使用)、lreturn、freturn、dreturn以及areturn(引用类型的)
3. 另外还有一个return指令供声明为void的方法、实例初始化方法、类和接口的初始化方法使用

![image-20220807112642076](images\image-20220807112642076.png)

在方法执行的过程中遇到了异常(Exception),并且这个异常没有在方法内进行处理,也就是只要在本方法的异常表中没有搜素到匹配的异常处理器,就会导致方法退出,简称异常完成出口

#### 问题小结与扩展

①. 栈溢出的情况?栈溢出:StackOverflowError
栈中是不存在GC的,存在OOM和StackOverflowError
举个简单的例子:在main方法中调用main方法,就会不断压栈执行,直到栈溢出;
栈的大小可以是固定大小的,也可以是动态变化(动态扩展)的
如果是固定的,那么会抛出StackOverflowError
如果是动态扩展的,那么会抛出OOM异常(java.lang.OutOfMemoryError)
②. 调整栈大小,就能保证不出现溢出吗?
不能。因为调整栈大小,只会减少出现溢出的可能,栈大小不是可以无限扩大的,所以不能保证不出现溢出

③. 分配的栈内存越大越好吗?
不是,因为增加栈大小,会造成每个线程的栈都变的很大,使得一定的栈空间下,能创建的线程数量会变小

④. 垃圾回收是否会涉及到虚拟机栈?
不会;垃圾回收只会涉及到方法区和堆中,方法区和堆也会存在溢出的可能
程序计数器,只记录运行下一行的地址,不存在溢出和垃圾回收
虚拟机栈和本地方法栈,都是只涉及压栈和出栈,可能存在栈溢出,不存在垃圾回收

⑤. 方法中定义的局部变量是否线程安全?

```java
/**方法中定义的局部变量是否线程安全?   具体问题具体分析
 * @author shkstart
 * @create 15:53
 */
public class LocalVariableThreadSafe {
    //s1的声明方式是线程安全的,因为线程私有,在线程内创建的s1 ,不会被其它线程调用
    public static void method1() {
        //StringBuilder:线程不安全
        StringBuilder s1 = new StringBuilder();
        s1.append("a");
        s1.append("b");
        //...
    }
    
    //stringBuilder的操作过程:是线程不安全的,
    // 因为stringBuilder是外面传进来的,有可能被多个线程调用
    public static void method2(StringBuilder stringBuilder) {
        stringBuilder.append("a");
        stringBuilder.append("b");
        //...
    }

    //stringBuilder的操作:是线程不安全的；因为返回了一个stringBuilder,
    // stringBuilder有可能被其他线程共享
    public static StringBuilder method3() {
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append("a");
        stringBuilder.append("b");
        return stringBuilder;
    }

    //stringBuilder的操作:是线程安全的；因为返回了一个stringBuilder.toString()相当于new了一个String,
    // 所以stringBuilder没有被其他线程共享的可能
    public static String method4() {
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append("a");
        stringBuilder.append("b");
        return stringBuilder.toString();

        /**
         * 结论:如果局部变量在内部产生并在内部消亡的,那就是线程安全的
         */
    }
}

```

## 堆空间

### 堆的概述(共享|垃圾回收)

①. 一个JVM实例只存在一个堆内存,堆也是Java内存管理的核心区域

②. 堆可以在物理上不连续的内存空间中,但在逻辑上是连续的

③. Java堆区在JVM启动的时候即被创建,其空间大小也是确定的。是Jvm管理最大的一块内存空间

④. 所有的线程共享Java堆,在这里还可以划分线程私有的缓冲区(Thread Local Allocation Buffer,TLAB)

⑤. 在方法结束后,堆中的对象不会马上被移除,仅仅在垃圾收集的时候才有被移除
(注意:一个进程就是一个JVM实例,一个进程中包含多个线程)

```java
public class SimpleHeap {
    private int id;

    public SimpleHeap(int id) {
        this.id = id;
    }

    public void show() {
        System.out.println("My ID is " + id);
    }

    public static void main(String[] args) {
        SimpleHeap sl = new SimpleHeap(1);
        SimpleHeap s2 = new SimpleHeap(2);
    }
}

```

![image-20220807113531197](images\image-20220807113531197.png)

### 堆的内存结构

①. 现在垃圾收集器大部分都基于分带收集理论设计的,堆空间细分为:

![image-20220807113608564](images\image-20220807113608564.png)

②. jdk1.7 堆中的结构

![image-20220807113711671](images\image-20220807113711671.png)

![image-20220807113743921](images\image-20220807113743921.png)

### 堆空间大小的设置 -Xms -Xmx

①. Java堆区用于存储Java对象实例,那么堆的大小在JVM启动时就已经设定好了,大家可以通过选项"-Xmx 和 -Xms"来设置

②. -Xms(物理内存的1/64):表示堆区的起始内存,等价于-XX:InitialHeapSize

③. -Xmx(物理内存的1/4):则用于表示堆区的最大内存,等价于-XX:MaxHeapSize

④. 通常会将-Xms和-Xmx两个参数配置相同的值,其目的是为了能够在java垃圾回收机制清理完堆区后不需要重新分隔计算堆区的大小,从而提升性能

```java
/**
 * -Xms:600m
 * -Xmx:600m
 * 查看设置的参数:
 * 方式一(cmd中):jps  / jstat -gc 进程id
 * 方式二(XX:+PrintGCDetails)
 */
public class HeapDemo1 {
    public static void main(String[] args)throws Exception {
        //返回Java虚拟机中的堆内存总量
        long initialMemory = Runtime.getRuntime().totalMemory()/1024/1024;
        //返回Java虚拟机试图使用的最大堆内存量
        long maxMemory = Runtime.getRuntime().maxMemory()/1024/1024;
        System.out.println("-Xms:"+initialMemory+"M");
        System.out.println("-Xmx:"+maxMemory+"M");
        //TimeUnit.SECONDS.sleep(1000000);
    }
}

```


![image-20220807114247327](images\image-20220807114247327.png)

### 新生代与老年代参数设置 NewRation SurvivorRatio

①. 配置新生代与老年代在堆结构占比
默认:-XX:NewRatio=2,表示新生代占1,老年代占2,新生代占整个堆的1/3
可以修改-XX:NewRatio=4,表示新生代占1,老年代占4,新生代占整个堆的1/5

![image-20220807114331111](images\image-20220807114331111.png)

②. -XX:SurvivorRatio调整这个空间比例(Eden空间和另外两个Survivor空间缺省所占的比例是8:1:1)

③. -Xmn:设置新生代最大内存大小,一般使用默认值就可以了

④. 几乎所有的Java对象都是在Eden区被new出来的,觉大部分的Java对象的销毁都在新生代进行的
 复制算法

###  复制算法

①. 一般过程(图解)

![image-20220807114439864](images\image-20220807114439864.png)

![image-20220807114619673](images\image-20220807114619673.png)

### 复制算法详解

(伊甸园满了,就会触发gc(minor gc),而gc就会把标识为垃圾的对象干掉,不是垃圾的对象就要转移到幸存区,把伊甸园让出来给新的对象用)

![image-20220807114953601](images\image-20220807114953601.png)

### Minor GC | Major GC | Full GC

①. YONG GC(minor GC):发生在新生代

1. 只针对新生代区域的GC,指发生在新生代的垃圾收集动作,因为大多数Java对象存活率都不高,所以Minor GC非常频繁,一般回收速度也比较快
2. 当Eden代满,会触发minor GC ,Survivor 满不会引发GC
3. minor gc 会引发STW,暂停其他用户线程,等垃圾回收结束,用户线程才能恢复

②. Major GC:发生在老年代
major GC 是回收老年代的垃圾；major gc 的速度一般比Minor gc 慢10倍以上,STW时间更长

③. Full GC:发生在新生代和老年代

1. full GC 就会出现所谓的STW(stop the world)现象,即所有的进程都挂起等待清理垃圾
2. full GC是回收老年代和年轻代的垃圾
3. full gc 是开发调优中尽量避免的,这样暂时时间会短一些

```
(1). 调用System.gc()时,系统建议执行Full GC,但是不必然执行
(2). 老年代空间不足
(3). 方法区空间不足
(4). 通过Minor GC后进入老年代的平均大小大于老年代的可用内存(空间分配担保)
(5). 由Eden区、survivor space0(From Space)区向survivor space1(To Space)区复制时,对象大小大于To Space可用内存,则把该对象转存到老年代,且老年代的可用内存小于该对象大小
```

④. 全局GC(major GC or Full GC):

(指发生在老年代的垃圾收集动作,出现了Major GC,经常会伴随至少一次的Minor GC(但并不是绝对的)。Major GC的速度一般要比Minor GC慢上10倍以上)

### 针对不同年龄阶段的对象分配原则

①. 优先分配到Eden

②. 大对象直接分配到老年(尽量避免程序中出现过多的大对象)

③. 长期存活的对象分配到老年代

④. 动态对象年龄判断
(如果Survivor 区中相同年龄的所有对象大小的总和大于Survivor空间的一半,年龄大于或等于该年龄对象可以直接进入老年代,无须等到MaxTenurningThreshold中要求的年龄)

⑤. 空间分配担保 -XX:HandlePromotionFailure
(JDK6之后,只要老年代的连续空间大于新生代对象总大小或者历次晋升的平均大小就会进行Minor GC,否则将进行Full GC)

### TLAB(Thread Local Allocation Buffer)

①. 从内存模型而不是垃圾收集的角度,对Eden区域继续进行划分,JVM为每个线程分配了一个私有缓存区域,它包含在Eden空间内

②. 尽管不是所有的对象实例都能够在TLAB中成功分配内存,但JVM确实是将TLAB作为内存分配的首选

③. 默认情况下,TLAB空间的内存非常小,仅占有整个Eden空间的1%,当然可通过选项"-XX:TLABWasteTargePercent"设置TLAB空间所占用Eden空间的百分比大小

④. 一旦对象在TLAB空间分配内存失败时,JVM就会尝试着通过使用加锁机制确保数据操作的原子性,从而直接在Eden空间中分配内存

⑤. 图解:

![image-20220807115930729](images\image-20220807115930729.png)

![image-20220807115952130](images\image-20220807115952130.png)

### 堆空间参数总结

①. -XX:+PrintFlagsInitial : 查看所有的参数的默认初始值

②. -XX:+PrintFlagsFinal : 查看所有的参数的最终值(可能会存在修改(:表示修改了),不再是初始值)

③. 具体查看某个参数的指令:
(jps:查看当前运行中的进程
jinfo -flag SurvivorRatio 进程id)

④. -Xms:初始堆空间内存 (默认为物理内存的1/64)

⑤. -Xmx:最大堆空间内存(默认为物理内存的1/4)

⑥. -Xmn:设置新生代的大小。(初始值及最大值)

⑦. -XX:NewRatio:配置新生代与老年代在堆结构的占比
(默认:-XX:NewRatio=2,表示新生代占1,老年代占2,新生代占整个堆的1/3
可以修改-XX:NewRatio=4,表示新生代占1,老年代占4,新生代占整个堆的1/5)

⑧. -XX:SurvivorRatio:设置新生代中Eden和S0/S1空间的比例
(Eden空间和另外两个Survivor空间缺省所占的比例是8:1:1)

⑨. -XX:MaxTenuringThreshold:设置新生代垃圾的最大年龄

⑩. -XX:+PrintGCDetails:输出详细的GC处理日志
(如下这两种方式是简单的打印
打印gc简要信息:① -XX:+PrintGC ② -verbose:gc)

⑩①. -XX:HandlePromotionFailure:是否设置空间分配担保
(JDK6之后,只要老年代的连续空间大于新生代对象总大小或者历次晋升的平均大小就会进行Minor GC,否则将进行Full GC)

> 内存分配策略(或对象提升(Promotion)规则)
> (1). 在繁盛Minor GC之前,虚拟机会检查老年代最大可用的连续空间是否大于新生代所有对象的总空间
> ====如果大于,则此次Minor GC是安全的
> ====如果小于,则虚拟机会检查查看-XX:HandlePromotionFailure设置值是否允许担保失败
> =====如果 HandlePromotionFailure=true,那么会继续检查老年代最大可用连续空间是否大于历次晋级到老年代的对象的平均大小
> ========如果大于,则尝试进行一次Minor GC,但是这次Minor GC依然是有风险的
> ========如果小于,则改为一次Full GC
> =====如果HandlePromotionFailure=false,则改为进行一次Full GC
> (2). 在JDK6 Update24之后,HandlePromotionFailure参数不会再影响虚拟机的空间分配担保策略,观察OpenJDK中源码变化,虽然源码中还定义了HandlePromotionFailure参数,但是在代码中已经不会再使用它
> (3). JDK6 Update24之后规则变为只有老年代的连续空间大于新生代对象总大小或者历次晋身的平均大小就会进行Minor GC,否则将进行Full GC

### 逃逸分析

①. 如何将堆上的对象分配到栈,需要使用逃逸分析手段

1. 当一个对象在方法中被定义后,对象只在方法内部使用(这里关注的是这个对象的实体),则认为没有发生逃逸。
2. 当一个对象在方法中被定义后,它被外部方法所引用,则认为发生逃逸。例如作为调用参数传递到其他地方中

②. 代码演示

```java
//(1). 没有发生逃逸的对象,则可以分配到栈上,随着方法执行的结束,栈空间就被移除
public void my_method() {
    V v = new V();
    // use v
    // ....
    v = null;
}
//(2). 下面代码中的 StringBuffer sb 发生了逃逸
public static StringBuffer createStringBuffer(String s1, String s2) {
    StringBuffer sb = new StringBuffer();
    sb.append(s1);
    sb.append(s2);
    return sb;
}
//如果想要StringBuffer sb不发生逃逸,可以这样写
public static String createStringBuffer(String s1, String s2) {
    StringBuffer sb = new StringBuffer();
    sb.append(s1);
    sb.append(s2);
    return sb.toString();
}

```

③. 逃逸分析的举例

```java
/**
 * 逃逸分析
 *
 * 如何快速的判断是否发生了逃逸分析,大家就看new的对象实体是否有可能在方法外被调用。
 */
public class EscapeAnalysis {

    public EscapeAnalysis obj;

    /*
    方法返回EscapeAnalysis对象,发生逃逸
     */
    public EscapeAnalysis getInstance(){
        return obj == null? new EscapeAnalysis() : obj;
    }

    /*
    为成员属性赋值,发生逃逸
     */
    public void setObj(){
        this.obj = new EscapeAnalysis();
    }
    //思考:如果当前的obj引用声明为static的？ 仍然会发生逃逸。

    /*
    对象的作用域仅在当前方法中有效,没有发生逃逸
     */
    public void useEscapeAnalysis(){
        EscapeAnalysis e = new EscapeAnalysis();
    }

    /*
    引用成员变量的值,发生逃逸
    
     */
    public void useEscapeAnalysis1(){
        EscapeAnalysis e = getInstance(); //这个e对象,本身就是从外面的方法逃逸进来的
        //getInstance().xxx()同样会发生逃逸
    }
}

```

④. 在JDK1.7版本之后,HotSpot中默认就已经开启了逃逸分析

如果使用的是较早的版本,开发人员则可以通过:
选项“-XX:+DoEscapeAnalysis"显式开启逃逸分析
通过选项“-XX:+PrintEscapeAnalysis"查看逃逸分析的筛选结果

结论: ⑤. 开发中能使用局部变量的,就不要使用在方法外定义

⑥. 使用逃逸分析,编译器可以对代码做如下优化:

1. 栈上分配:将堆分配转化为栈分配。如果一个对象在子程序中被分配,要使指向该对象的指针永远不会发生逃逸,对象可能是栈上分配的候选,而不是堆上分配
2. 同步省略:如果一个对象被发现只有一个线程被访问到,那么对于这个对象的操作可以不考虑同步。
3. 分离对象或标量替换:有的对象可能不需要作为一个连续的内存结构存在也可以被访问到,那么对象的部分(或全部)可以不存储在内存,而是存储在CPU寄存器中
   

#### 栈上分配

①. JIT编译器在编译期间根据逃逸分析的结果,发现如果一个对象并没有逃逸出方法的话,就可能被优化成栈上分配

②.代码举例

```java
/**
 * 栈上分配测试
 * -Xmx256m -Xms256m -XX:-DoEscapeAnalysis -XX:+PrintGCDetails
 */
public class StackAllocation {
    public static void main(String[] args) {
        long start = System.currentTimeMillis();

        for (int i = 0; i < 10000000; i++) {
            alloc();
        }
        // 查看执行时间
        long end = System.currentTimeMillis();
        System.out.println("花费的时间为: " + (end - start) + " ms");
        // 为了方便查看堆内存中对象个数,线程sleep
        try {
            Thread.sleep(1000000);
        } catch (InterruptedException e1) {
            e1.printStackTrace();
        }
    }

    private static void alloc() {
        User user = new User(); //未发生逃逸
    }

    static class User {

    }
}

```

③. 未开启逃逸分析的情况
-Xmx256m -Xms256m -XX:-DoEscapeAnalysis -XX:+PrintGCDetails

```
日志打印发生了GC
[GC (Allocation Failure) [PSYoungGen: 65536K->560K(76288K)] 65536K->568K(251392K), 0.0017179 secs] [Times: user=0.01 sys=0.00, real=0.00 secs] 
[GC (Allocation Failure) [PSYoungGen: 66096K->464K(76288K)] 66104K->480K(251392K), 0.0017602 secs] [Times: user=0.00 sys=0.00, real=0.01 secs] 
花费的时间为: 74 ms

```

④. 开启逃逸分析的情况
-Xmx256m -Xms256m -XX:+DoEscapeAnalysis -XX:+PrintGCDetails

```
日志打印:并没有发生 GC,耗时 3ms ,栈上分配是真的快啊
花费的时间为: 4 ms
```

####  同步替换 锁消除

①. 从JIT角度看相当于无视它了,这个锁对象没有被共享给其他线程

②. 例如下面的智障代码,根本起不到锁的作用
代码中对hellis这个对象加锁(每个线程都有一个hellis对象的锁),但是hellis对象的生命周期只在f( )方法中,并不会被其他线程所访问到,所以在JIT编译阶段就会被优化掉,优化成:

```java
public void f() {
    Object hellis = new Object();
    synchronized(hellis) {
        System.out.println(hellis);
    }
}
// JIT会将它变成这样
public void f() {
  	Object hellis = new Object();
		System.out.println(hellis);
}

```

③. 注意:字节码文件中并没有进行优化,可以看到加锁和释放锁的操作依然存在,同步省略操作是在解释运行时发生的

#### 分离对象或标量替换

①. 标量(scalar)是指一个无法再分解成更小的数据的数据。Java中的原始数据类型就是标量

②. 相对的,那些还可以分解的数据叫做聚合量(Aggregate),Java中的对象就是聚合量,因为他可以分解成其他聚合量和标量

③. 在JIT阶段,如果经过逃逸分析,发现一个对象不会被外界访问的话,那么经过JIT优化,就会把这个对象拆解成若干个其中包含的若干个成员变量来代替。这个过程就是标量替换

④. 举列子

```java
public static void main(String args[]) {
    alloc();
}
class Point {
    private int x;
    private int y;
}
private static void alloc() {
    Point point = new Point(1,2);
    System.out.println("point.x" + point.x + ";point.y" + point.y);
}
//以上代码,经过标量替换后,就会变成
private static void alloc() {
    int x = 1;
    int y = 2;
    System.out.println("point.x = " + x + "; point.y=" + y);
}

```

## 方法区的概述

方法区在JVM启动的时候被创建,并且它的实际的物理内存空间和Java堆区一样都可以是不连续的 | 关闭Jvm就会释放这个区域的内存

方法区时逻辑上是堆的一个组成部分,但是在不同虚拟机里头实现是不一样的，最典型的就是永久代(PermGen space)和元空间(Metaspace)

方法区的大小决定了系统可以保存多少个类,如果系统定义了太多的类,导致方法区溢出,虚拟机同样会抛出内存溢出错误：(java.lang.OutOfMemoryError:PermGen space、java.lang.OutOfMemoryError:Metaspace)

1. 加载大量的第三方的jar包
2. tomcat部署的工程过多(30-50个)
3. 大量动态的生成反射类

 对于HotspotJVM而言,方法区还有一个别名叫非堆(Non-heap),目的就是要和堆分开,方法区可以看成一块独立于Java堆的内存空间

### 方法区的内部结构

深入理解Java虚拟机》书中对方法区存储内容描述如下：它用于存储已被虚拟机加载的类型信息、常量、静态变量、即时编译器编译后的代码缓存等

![image-20220813085631559](images\image-20220813085631559.png)

类型信息(对每个加载的类型(类class、接口interface、枚举enum、注解annotation),JVM必 .须在方法区中存储以下类型信息：

1. 这个类型的完整有效名称（全名=包名.类名）
2. 这个类型直接父类的完整有效名（对于interface或是java. lang.Object，都没有父类）
3. 这个类型的修饰符（public， abstract， final的某个子集）
4. 这个类型直接接口的一个有序列表

域信息（成员变量）

1. JVM必须在方法区中保存类型的所有域的相关信息以及域的声明顺序。
2. 域的相关信息包括：域名称、 域类型、域修饰符（public， private， protected， static， final， volatile， transient的某个子集）

方法信息：JVM必须保存所有方法的以下信息，同域信息一样包括声明顺序

​	方法名称
​	方法的返回类型（或void）
​	方法参数的数量和类型（按顺序）
​	方法的修饰符（public， private， protected， static， final，synchronized， native ， abstract的一个子集）
​	方法的字节码（bytecodes）、操作数栈、局部变量表及大小（ abstract和native 方法除外）
​	异常表（ abstract和native方法除外）
​	每个异常处理的开始位置、结束位置、代码处理在程序计数器中的偏移地址、被捕获的异常类的常量池索引
**non-final的类变量**

(Order.class字节码文件，右键Open in Teminal打开控制台，使用javap -v -p Order.class > tst.txt 将字节码文件反编译并输出为txt文件,可以看到被声明为static final的常量number在编译的时候就被赋值了，这不同于没有被final修饰的static变量count是在类加载的准备阶段被赋值为默认的初始化值,在初始化的时候赋予正确的初始化值

```
 public static int count;
    descriptor: I
    flags: ACC_PUBLIC, ACC_STATIC

  public static final int number;
    descriptor: I
    flags: ACC_PUBLIC, ACC_STATIC, ACC_FINAL
    ConstantValue: int 2

```

**`以下代码不会报空指针异常`**

```java
public class MethodAreaTest {
    public static void main(String[] args) {
        Order order = null;
        order.hello();
        System.out.println(order.count);
    }
}

class Order {
    public static int count = 1;
    public static final int number = 2;


    public static void hello() {
        System.out.println("hello!");
    }
}

```

### 方法区的演进细节

①. Jdk 1.6 及之前：有永久代，静态变量、字符串常量池1.6在方法区

②. Jdk 1.7 ：有永久代，但已经逐步 " 去永久代 "，字符串常量池、静态变量移除,保存在堆中

③. jdk 1.8 及之后： 无永久代，常量池1.8在元空间。但静态变量、字符串常量池仍在堆中


![image-20220813090024197](images\image-20220813090024197.png)

为什么要用元空间取代永久代

1. 为永久代设置空间大小是很难确定的

​	①. 永久代参数设置过小,在某些场景下,如果动态加载的类过多,容易产生Perm区的OOM,比如某个实际Web工程中,因为功能点比较多,在运行过程中,要不断动态加载很多类,经常出现致命错误
​	②. 永久代参数设置过大,导致空间浪费
​	③. 默认情况下,元空间的大小受本地内存限制)

2. 对永久代进行调优是很困难的

​	(方法区的垃圾收集主要回收两部分：常量池中废弃的常量和不再使用的类型,而不再使用的类或类的加载器回收比较复杂,full gc 的时间长)

 StringTable为什么要调整

1. jdk7中将StringTable放到了堆空间中。因为永久代的回收效率很低,在full gc的时候才能触发。而full gc是老年代的空间不足、永久代不足才会触发
2. 这就导致StringTable回收效率不高,而我们开发中会有大量的字符串被创建,回收效率低,导致永久代内存不足,放到堆里,能及时回收内存
   

### 设置方法区大小

 jdk7及以前:

1. -XX:PermSize=100m(默认值是20.75M)
2. -XX:MaxPermSize=100m(32位机器默认是64M,64位机器模式是82M)
3. 图解：

![image-20220813090244157](images\image-20220813090244157.png)

 jdk1.8及以后

1. -XX:MetaspaceSize=100m(windows下,默认约等于21M)
2. -XX:MaxMetaspaceSize=100m(默认是-1,即没有限制)

### 常量池的理解

常量池，可以看做是一张表，虚拟机指令根据这张常量表找到要执行的类名，方法名，参数类型、字面量等信息

```
Constant pool:
   #1 = Methodref          #7.#23         // java/lang/Object."<init>":()V
   #2 = Methodref          #24.#25        // com/xiaozhi/heap/Order.hello:()V
   #3 = Fieldref           #26.#27        // java/lang/System.out:Ljava/io/PrintStream;
   #4 = Fieldref           #24.#28        // com/xiaozhi/heap/Order.count:I
   #5 = Methodref          #29.#30        // java/io/PrintStream.println:(I)V

```

一个有效的字节码文件中除了包含类的版本信息、字段、方法以及接口等描述信息外，还包含一项信息那就是常量池表（Constant Poo1 Table），包括各种字面量和对类型域和方法的符号引用。

一个 java 源文件中的类、接口，编译后产生一个字节码文件。而 Java 中的字节码需要数据支持，通常这种数据会很大以至于不能直接存到字节码里，换另一种方式，可以存到常量池这个字节码包含了指向常量池的引用。在动态链接的时候会用到运行时常量池

比如如下代码，虽然只有 194 字节，但是里面却使用了 string、System、Printstream 及 Object 等结构。这里代码量其实已经很小了。如果代码多，引用到的结构会更多！

```java
	Public class Simpleclass {
	public void sayhelloo() {
	    System.out.Println (hello) }
	}

```

### 运行时常量池

1. 运行时常量池，常量池是 `*.class` 文件中的，当该类被加载，它的常量池信息就会放入运行时常量池，并把里面的符号地址变为真实地址
2. 运行时常量池（ Runtime Constant Pool）是方法区的一部分。
3. 常量池表（Constant Pool Table）是Class文件的一部分，用于存放编译期生成的各种字面量与符号引用，这部分内容将在类加载后存放到方法区的运行时常量池中。
4. 运行时常量池中包含多种不同的常量,包括编译期就已经明确的数值字面量，也包括到运行期解析后才能够获得的方法或者字段引用此时不再是常量池中的符号地址了，这里换为真实地址。

(方法区内常量池之中主要存放的两大类常量：字面量和符号引用。
字面量比较接近Java语言层次的常量概念，如文本字符串、被声明为final的常量值等。
而符号引用则属于编译原理方面的概念，包括下面三类常量：
	1、类和接口的全限定名
	2、字段的名称和描述符
	3、方法的名称和描述符)

### 如何证明静态变量存在哪

```java
/**
 * 《深入理解Java虚拟机》中的案例：
 * staticObj、instanceObj、localObj存放在哪里？
 */
public class StaticObjTest {
    static class Test {
        static ObjectHolder staticObj = new ObjectHolder();
        ObjectHolder instanceObj = new ObjectHolder();

        void foo() {
            ObjectHolder localObj = new ObjectHolder();
            System.out.println("done");
        }
    }

    private static class ObjectHolder {
    }

    public static void main(String[] args) {
        Test test = new StaticObjTest.Test();
        test.foo();
    }
}

```

staticObj随着Test的类型信息存放在方法区，instance0bj 随着Test的对象实例存放在Java堆，localobject则是存放在foo（）方法栈帧的局部变量表中

```
hsdb>scanoops 0x00007f32c7800000 0x00007f32c7b50000 JHSDB_ _TestCase$Obj ectHolder
0x00007f32c7a7c458 JHSDB_ TestCase$Obj ectHolder
0x00007f32c7a7c480 JHSDB_ TestCase$Obj ectHolder
0x00007f32c7a7c490 JHSDB_ TestCase$Obj ectHolder
```

测试发现：三个对象的数据在内存中的地址都落在Eden区范围内，所以结论：只要是对象实例必然会在Java堆中分配

接着，找到了一个引用该staticObj对象的地方，是在一个java. lang . Class的实例里，并且给出了这个实例的地址，通过Inspector查看该对象实例，可以清楚看到这确实是一个
java.lang.Class类型的对象实例，里面有一个名为staticObj的实例字段：
![image-20220813091003977](images\image-20220813091003977.png)

从《Java 虛拟机规范》所定义的概念模型来看，所有 C1ass 相关的信息都应该存放在方法区之中，但方法区该如何实现，《Java 虚拟机规范》并未做出规定，这就成了一件允许不同虚拟机自己灵活把握的事情。JDK7 及其以后版本的 Hotspot 虚拟机选择把静态变量与类型在 Java 语言一端的映射 C1ass 对象存放在一起，存储于】ava 堆之中，从我们的实验中也明确验证了这一点.


### 方法区的垃圾回收

> 前言：
> (1).有些人认为方法区（如Hotspot，虚拟机中的元空间或者永久代）是没有垃圾收集行为的，其实不然。《Java 虚拟机规范》对方法区的约束是非常宽松的，提到过可以不要求虚拟机在方法区中实现垃圾收集。事实上也确实有未实现或未能完整实现方法区类型卸载的收集器存在（如 JDK11 时期的 ZGC 收集器就不支持类卸载）
> (2). 一般来说这个区域的回收效果比较难令人满意，尤其是类型的卸载，条件相当苛刻。但是这部分区域的回收有时又确实是必要的。以前 Sun 公司的 Bug 列表中，曾出现过的若干个严重的 Bug 就是由于低版本的 Hotspot 虚拟机对此区域未完全回收而导致内存泄漏

①. 方法区的垃圾收集主要回收两部分内容：常量池中废奔的常量和不再使用的类型

②. 先来说说方法区内常量池之中主要存放的两大类常量：字面量和符号引用。 字面量比较接近Java语言层次的常量概念，如文本字符串、被声明为final的常量值等。而符号引用则属于编译原理方面的概念，包括下面三类常量

1. 类和接口的全限定名
2. 字段的名称和描述符
3. 方法的名称和描述符

③. HotSpot虚拟机对常量池的回收策略是很明确的，只要常量池中的常量没有被任何地方引用，就可以被回收。回收废弃常量与回收Java堆中的对象非常类似。

④. 判定一个常量是否“废弃”还是相对简单，而要判定一个类型是否属于“不再被使用的类”的条件就比较苛刻了。需要同时满足下面三个条件：

1. 该类所有的实例都已经被回收，也就是Java堆中不存在该类及其任何派生子类的实例。
2. 加载该类的类加载器已经被回收，这个条件除非是经过精心设计的可替换类加载器的场景，如OSGi、JSP的重加载等，否则通常是很难达成的
3. 该类对应的java.lang.Class对象没有在任何地方被引用，无法在任何地方通过反射访问该类的方法

Java虛拟机被允许对满足上述三个条件的无用类进行回收，这里说的仅仅是“被允许”，而并不是和对象一样，没有引用了就必然会回收。关于是否要对类型进行回收，HotSpot虚拟机提供了一Xnoclassgc 参数进行控制，还可以使用一verbose：class以及一XX： +TraceClass一Loading、一XX：+TraceClassUnLoading查 看类加载和卸载信息

在大量使用反射、动态代理、CGLib等字节码框架，动态生成JSP以及oSGi这类频繁自定义类加载器的场景中，通常都需要Java虚拟机具备类型卸载的能力，以保证不会对方法区造成过大的内存压力

### 字符串常量池基本特性

①. String：字符串，使用一对""引起来表示。

```
String sl = “hello”；//字面量的定义方式
String s2 = new String（“hello”）
```

②. String声明为final的,不可被继承

③. String实现了Serializable接口：表示字符串是支持序列化的。 实现了Comparable接口：表示String可以比较大小

④. String在jdk8及以前内部定义了final char[ ],value用于存储字符串数据。jdk9时改为byte[ ]

```java
	public final class String implements 
	java.io.Serializable， Comparable<String>,CharSequence {
	@Stable
	private final byte[] value；
	}

```

⑤. String：代表不可变的字符序列。简称：不可变性。

⑥. 通过字面量的方式（区别于new）给一个字符串赋值，此时的字符串值声明在字符串常量池中

⑦. 字符串常量池中是不会存储相同内容的字符串的

#### String的内存分配

①. 常量池就类似一个Java系统级别提供的缓存。8种基本数据类型的常量池都是系统协调的，String类型的常量池比较特殊。它的主要使用方法有两种：

	1. 直接使用双引号声明出来的String对象会直接存储在常量池中(比如： String info = “abc” )
	1. 如果不是用双引号声明的String对象，可以使用String提供的intern（）方法

②.String的基本操作

![image-20220813094726531](images\image-20220813094726531.png)

```java
	class Memory {
	    public static void main(String[] args) {//line 1
	        int i = 1;//line 2
	        Object obj = new Object();//line 3
	        Memory mem = new Memory();//line 4
	        mem.foo(obj);//line 5
	    }//line 9
	
	    private void foo(Object param) {//line 6
	        String str = param.toString();//line 7
	        System.out.println(str);
	    }//line 8
	}

```

![image-20220813094801704](images\image-20220813094801704.png)



####  字符串拼接操作

①. 常量与常量的拼接结果在常量池，原理是编译期优化

②. 常量池中不会存在相同内容的常量。

③. 只要其中有一个是变量，结果就在堆中

只有有一个是变量,那么它会在堆中创建一个StringBuilder，调用append( )方法进行添加操作，调用toString( )方法转换为字符串【toString( )方法其实就是:new String( )】)

④. 如果拼接的结果调用intern（）方法分为两种情况：

1. JDK1.6，将这个字符串对象尝试放入串池 ①. 如果字符串常量池中有，则并不会放入。返回已有的串池中的对象的地址②. 如果没有,它会在常量池中创建一个对象放入串池中，并返回串池中的对象地址
2. JDK1.7，将这个字符串对象尝试放入串池 ①. 如果字符串常量池中有，则并不会放入。返回已有的串池中的对象的地址②. 如果没有，它不会创建一个对象，如果堆中已经有这个字符串，那么会将堆中的引用地址赋给它

```java
    @Test
    public void test1(){
        String s1 = "a" + "b" + "c";//编译期优化：等同于"abc" 在字节码文件中,s1="abc"
        String s2 = "abc"; //"abc"一定是放在字符串常量池中，将此地址赋给s2
        /*
         * 最终.java编译成.class,再执行.class
         * String s1 = "abc";
         * String s2 = "abc"
         */
        System.out.println(s1 == s2); //true
        System.out.println(s1.equals(s2)); //true
    }

    @Test
    public void test2(){
        String s1 = "javaEE";
        String s2 = "hadoop";

        String s3 = "javaEEhadoop";
        String s4 = "javaEE" + "hadoop";//编译期优化
        //如果拼接符号的前后出现了变量，则相当于在堆空间中new String()，具体的内容为拼接的结果：javaEEhadoop
        String s5 = s1 + "hadoop";
        String s6 = "javaEE" + s2;
        String s7 = s1 + s2;

        System.out.println(s3 == s4);//true
        System.out.println(s3 == s5);//false
        System.out.println(s3 == s6);//false
        System.out.println(s3 == s7);//false
        System.out.println(s5 == s6);//false
        System.out.println(s5 == s7);//false
        System.out.println(s6 == s7);//false
        //intern():判断字符串常量池中是否存在javaEEhadoop值，如果存在，则返回常量池中javaEEhadoop的地址；
        //如果字符串常量池中不存在javaEEhadoop，则在常量池中加载一份javaEEhadoop，并返回次对象的地址。
        String s8 = s6.intern();
        System.out.println(s3 == s8);//true
    }


```

```java
    @Test
    public void test3(){
        String s1 = "a";
        String s2 = "b";
        String s3 = "ab";
        /*
        如下的s1 + s2 的执行细节：(变量s是我临时定义的）
        ① StringBuilder s = new StringBuilder();
        ② s.append("a")
        ③ s.append("b")
        ④ s.toString()  --> 约等于 new String("ab")

        补充：在jdk5.0之后使用的是StringBuilder,
        在jdk5.0之前使用的是StringBuffer
         */
        String s4 = s1 + s2;//
        System.out.println(s3 == s4);//false
    }

    /*
    1. 字符串拼接操作不一定使用的是StringBuilder!
       如果拼接符号左右两边都是字符串常量或常量引用，则仍然使用编译期优化，即非StringBuilder的方式。
    2. 针对于final修饰类、方法、基本数据类型、引用数据类型的量的结构时，能使用上final的时候建议使用上。
     */
    @Test
    public void test4(){
        final String s1 = "a";
        final String s2 = "b";
        String s3 = "ab";
        String s4 = s1 + s2;
        System.out.println(s3 == s4);//true
    }

    //练习：
    @Test
    public void test5(){
        String s1 = "javaEEhadoop";
        String s2 = "javaEE";
        String s3 = s2 + "hadoop";
        System.out.println(s1 == s3);//false

        final String s4 = "javaEE";//s4:常量
        String s5 = s4 + "hadoop";
        System.out.println(s1 == s5);//true

    }

```

#### 拼接操作与append的效率对比

append效率要比字符串拼接高很多

```java
/*
    体会执行效率：通过StringBuilder的append()的方式添加字符串的效率要远高于使用String的字符串
 拼接方式！
    详情：① StringBuilder的append()的方式：自始至终中只创建过一个StringBuilder的对象
           使用String的字符串拼接方式：创建过多个StringBuilder和String的对象
         ② 使用String的字符串拼接方式：内存中由于创建了较多的StringBuilder和String的对象，
           内存占用更大；如果进行GC，需要花费额外的时间。

     改进的空间：在实际开发中，如果基本确定要前前后后添加的字符串长度不高于某个限定值highLevel
     的情况下,建议使用构造器实例化：
     StringBuilder s = new StringBuilder(highLevel);//new char[highLevel]
     */
    @Test
    public void test6(){

        long start = System.currentTimeMillis();

//        method1(100000);//4014
        method2(100000);//7

        long end = System.currentTimeMillis();

        System.out.println("花费的时间为：" + (end - start));
    }

    public void method1(int highLevel){
        String src = "";
        for(int i = 0;i < highLevel;i++){
            src = src + "a";//每次循环都会创建一个StringBuilder、String
        }
//        System.out.println(src);

    }

    public void method2(int highLevel){
        //只需要创建一个StringBuilder
        StringBuilder src = new StringBuilder();
        for (int i = 0; i < highLevel; i++) {
            src.append("a");
        }
//        System.out.println(src);
    }

```

####  intern()的使用

> 前言：
> (1). 如果不是用双引号声明的String对象，可以使用String提供的intern方法： intern方法会从字符串常量池中查询当前字符串是否存在，若不存在就会将当前字符串放入常量池中
> (2). 比如： String myInfo = new String(“I love u”).intern()；
> 也就是说，如果在任意字符串上调用String. intern方法，那么其返回结果所指向的那个类实例，必须和直接以常量形式出现的字符串实例完全相同。因此，下 列表达式的值必定是true：
> （“a” + “b” + “c”）.intern（）== “abc”;
> (3). 通俗点讲，Interned String就是确保字符串在内存里只有一份拷贝，这样可以节约内存空间，加快字符串操作任务的执行速度。注意，这个值会被存放在字符串内部池（String Intern Pool）

##### new String(“ab”)会创建几个对象

1. 一个对象是：new关键字在堆空间创建的
2. 另一个对象是：字符串常量池中的对象"ab"。 字节码指令：ldc
3. 如下图：(常量池中已经有了该对象)

![image-20220813095538754](images\image-20220813095538754.png)



##### new String(“a”) + new String(“b”)创建几个对象呢？

1. 对象1：new StringBuilder()
2. 对象2： new String(“a”)
3. 对象3： 常量池中的"a"
4. 对象4： new String(“b”)
5. 对象5： 常量池中的"b"

![image-20220813095655012](images\image-20220813095655012.png)

深入剖析： StringBuilder的toString(): 对象6 ：new String(“ab”)

注意：强调一下，toString()的调用，在字符串常量池中，没有生成"ab" 没有ldc指令

![image-20220813095755429](images\image-20220813095755429.png)

#### 关于String.intern( )的面试题

```java
/**
 * 如何保证变量s指向的是字符串常量池中的数据呢？
 * 有两种方式：
 * 方式一： String s = "shkstart";//字面量定义的方式
 * 方式二： 调用intern()
 *         String s = new String("shkstart").intern();
 *         String s = new StringBuilder("shkstart").toString().intern();
 *  */
public class StringIntern {
    public static void main(String[] args) {
        String s = new String("1");
        String s1 = s.intern();//调用此方法之前，字符串常量池中已经存在了"1"
        String s2 = "1";
        //s  指向堆空间"1"的内存地址
        //s1 指向字符串常量池中"1"的内存地址
        //s2 指向字符串常量池已存在的"1"的内存地址  所以 s1==s2
        System.out.println(s == s2);//jdk6：false   jdk7/8：false
        System.out.println(s1 == s2);//jdk6: true   jdk7/8：true
        System.out.println(System.identityHashCode(s));//491044090
        System.out.println(System.identityHashCode(s1));//644117698
        System.out.println(System.identityHashCode(s2));//644117698

        //s3变量记录的地址为：new String("11")
        String s3 = new String("1") + new String("1");
        //执行完上一行代码以后，字符串常量池中，是否存在"11"呢？答案：不存在！！

        //在字符串常量池中生成"11"。如何理解：jdk6:创建了一个新的对象"11",也就有新的地址。
        //jdk7:此时常量中并没有创建"11",而是创建一个指向堆空间中new String("11")的地址
        s3.intern();
        //s4变量记录的地址：使用的是上一行代码代码执行时，在常量池中生成的"11"的地址
        String s4 = "11";
        System.out.println(s3 == s4);//jdk6：false  jdk7/8：true
    }
}

```

![image-20220813100004484](images\image-20220813100004484.png)

![image-20220813100023480](images\image-20220813100023480.png)

```java
public class StringIntern1 {
    public static void main(String[] args) {
        //StringIntern.java中练习的拓展：
        String s3 = new String("1") + new String("1");//new String("11")
        //执行完上一行代码以后，字符串常量池中，是否存在"11"呢？答案：不存在！！
        String s4 = "11";//在字符串常量池中生成对象"11"
        String s5 = s3.intern();
        System.out.println(s3 == s4);//false
        System.out.println(s5 == s4);//true
    }
}

```

#### 总结String的intern（）的使用

如果拼接的结果调用intern（）方法分为两种情况：

1. JDK1.6，将这个字符串对象尝试放入串池 ①. 如果字符串常量池中有，则并不会放入。返回已有的串池中的对象的地址②. 如果没有,它会在常量池中创建一个对象放入串池中，并返回串池中的对象地址

2. JDK1.7，将这个字符串对象尝试放入串池 ①. 如果字符串常量池中有，则并不会放入。返回已有的串池中的对象的地址②. 如果没有，它不会创建一个对象，如果堆中已经这个字符串，那么会将堆中的引用地址赋给它

   ```java
   public class StringExer1 {
       public static void main(String[] args) {
           //String x = "ab";
           String s = new String("a") + new String("b");//new String("ab")
           //在上一行代码执行完以后，字符串常量池中并没有"ab"
   
           String s2 = s.intern();//jdk6中：在串池中创建一个字符串"ab"
                                  //jdk8中：串池中没有创建字符串"ab",而是创建一个引用，指向new String("ab")，将此引用返回
   
           System.out.println(s2 == "ab");//jdk6:true  jdk8:true
           System.out.println(s == "ab");//jdk6:false  jdk8:true
       }
   }
   
   ```

   

# 四 对象实例化

![image-20220813091920184](images\image-20220813091920184.png)

##  从字节码角度看待对象的创建过程

从最简单的Object ref = new Object()

![image-20220813092023330](images\image-20220813092023330.png)

 new:如果找不到Class对象,则进行类加载。加载成功后,则在堆中分配内存,从Object 开始到本类路径上的所有属性值都要分配内存。分配完毕之后,进行零值初始化。在分配过程中,注意引用是占据存储空间的,它是一个变量,占用4个字节。这个指令完毕后,将指向实例对象的引用变量压入虚拟机栈顶。

dup:在栈顶复制该引用变量,这时的栈顶有两个指向堆内实例对象的引用变量。如果 方法有参数,还需要把参数压人操作栈中。两个引用变量的目的不同,其中压至底下的引用用于赋值,或者保存到局部变量表,另一个栈顶的引用变量作为句柄调用相关方法。

invokespecial:调用对象实例方法,通过栈顶的引用变量调用init方法。
补充:clinit是类初始化时执行的方法, 而init 是对象初始化时执行的方法。

## 对象的实例化(六个步骤)

①. 判断对象对应的类是否加载、链接、初始化
(虚拟机遇到一条new指令,首先去检查这个指令的参数能否在Metaspace的常量池中定位到一个类的符号引用,并且检查这个符号引用代表的类是否已经被加载、解析和初始化。( 即判断类元信息是否存在)。如果没有,那么在双亲委派模式下,使用当前类加载器以ClassLoader+包名+类名为Key进行查找对应的.class文件。如果没有找到文件,则抛出ClassNotFoundException异常,如果找到,则进行类加载,并生成对应的Class类对象)

②. 为对象分配内存：首先计算对象占用空间大小,接着在堆中划分一块内存给新对象。 如果实例成员变量是引用变量,仅分配引用变量空间即可,即4个字节大小
(byte、int、float、引用数据类型4个字节大小 | double、long 占八个字节)

1. 如果内存规整,使用指针碰撞
   如果内存是规整的,那么虚拟机将采用的是指针碰撞法(BumpThePointer)来为对象分配内存。意思是所有用过的内存在一边,空闲的内存在另外一边,中间放着一个指针作为分界点的指示器,分配内存就仅仅是把指针向空闲那边挪动一段与对象大小相等的距离罢了。如果垃圾收集器选择的是Serial、ParNew这种基于压缩算法的,虚拟机采用这种分配方式。一般使用带有compact (整理)过程的收集器时,使用指针碰撞。
2. 如果内存不规整,虚拟机需要维护一个列表,使用空闲列表分配(CMS)
   如果内存不是规整的,已使用的内存和未使用的内存相互交错,那么虛拟机将采用的是空闲列表法来为对象分配内存。意思是虚拟机维护了一个列表,记录上哪些内存块是可用的,再分配的时候从列表中找到一块足够大的空间划分给对象实例,并更新列表上的内容。这种分配方式成为“空闲列表(Free List)
3. 说明：选择哪种分配方式由Java堆是否规整决定,而Java堆是否规整又由所采用的垃圾收集器是否带有压缩整理功能决定。

![image-20220813092546933](images\image-20220813092546933.png)

![image-20220813092615552](images\image-20220813092615552.png)

③. 处理并发安全问题
(在分配内存空间时,另外一个问题是及时保证new对象时候的线程安全性：创建对象是非常频繁的操作,虚拟机需要解决并发问题。虚拟机采用 了两种方式解决并发问题：)

1. CAS ( Compare And Swap )失败重试、区域加锁：保证指针更新操作的原子性
2. TLAB把内存分配的动作按照线程划分在不同的空间之中进行,即每个线程在Java堆中预先分配一小块内存,称为本地线程分配缓冲区,(TLAB ,Thread Local Allocation Buffer) 虚拟机是否使用TLAB,可以通过一XX：+/一UseTLAB参数来 设定

④. 初始化分配到的空间:赋予默认的初始化值；比如int=0| boolean=false(默认的值)

⑤. 设置对象的对象头：将对象的所属类(即类的元数据信息)、对象的HashCode和对象的GC信息、锁信息等数据存储在对象的对象头中。这个过程的具体设置方式取决于JVM实现。

⑥. 执行init方法进行初始化(进行赋值的处理)
(在Java程序的视角看来,初始化才正式开始。初始化成员变量,执行实例化代码块,调用类的构造方法,并把堆内对象的首地址赋值给引用变量。因此一般来说(由字节码中是否跟随有invokespecial指令所决定),new指令之 后会接着就是执行方法,把对象按照程序员的意愿进行初始化,这样一个真正可用的对象才算完全创建出来。)

```java
/**
 * 测试对象实例化的过程
 *  ① 加载类元信息 - ② 为对象分配内存 - ③ 处理并发问题  - ④ 属性的默认初始化（零值初始化）
 *  - ⑤ 设置对象头的信息 - ⑥ 属性的显式初始化、代码块中初始化、构造器中初始化
 *
 *  给对象的属性赋值的操作：
 *  ① 属性的默认初始化 - ② 显式初始化 / ③ 代码块中初始化 - ④ 构造器中初始化
 * 
 */
public class Customer{
    int id = 1001;
    String name;
    Account acct;

    {
        name = "匿名客户";
    }
    public Customer(){
        acct = new Account();
    }

}

class Account{

}

```

## 对象的内存布局

①. 对象内部结构分为：对象头、实例数据、对齐填充(保证8个字节的倍数)

②. 对象头分为对象标记(markOop)和类元信息(klassOop),类元信息存储的是指向该对象类元数据(klass)的首地址

![image-20220813092914552](images\image-20220813092914552.png)

##  对象头(Header)

①. 对象标记Mark Word 默认存储 (哈希值(HashCode )、GC分代年龄、锁状态标志、线程持有的锁、偏向线程ID、偏向时间戳)等信息

1. 这些信息都是与对象自身定义无关的数据，所以MarkWord被设计成一个非固定的数据结构以便在极小的空间内存存储尽量多的数据。
2. 它会根据对象的状态复用自己的存储空间，也就是说在运行期间MarkWord里存储的数据会随着锁标志位的变化而变化。

![image-20220813092957851](images\image-20220813092957851.png)

②. 对象头多大 在64位系统中,Mark Word占了8个字节,类型指针占了8个字节,一共是16个字节

![image-20220813093032285](images\image-20220813093032285.png)

③. 类元信息(又叫类型指针) 对象指向它的类元数据的指针，虚拟机通过这个指针来确定这个对象是哪个类的实例

## 实例数据（Instance Data）

 说明:它是对象真正存储的有效信息,包括程序代码中定义的各种类型的字段(包括从父类继承下来的和本身拥有的字段) 规则:

1. 相同宽度的字段总被分配在一起
2. 父类中定义的变量会出现在子类之前
3. 如果CompactFields参数为true(默认为true),子类的窄变量可能插入到父类变量的空隙

## 对齐填充（Padding）

①. 不是必须的，也没特别含义，仅仅起到占位符作用

②. 解释如下图：

![image-20220813093152144](images\image-20220813093152144.png)

## 总结

```java
public class CustomerTest {
    public static void main(String[] args) {
        Customer cust = new Customer();
    }
}

```

图解代码

![image-20220813093258298](images\image-20220813093258298.png)

### 对象的访问定位

![image-20220813093512016](images\image-20220813093512016.png)

①. 句柄访问

![image-20220813093727594](images\image-20220813093727594.png)

## 直接内存(Direct Memory)

①. 不是虚拟机运行时数据区的一部分，也不是《Java虚拟机规范》中定义的内存区域

②. 直接内存是Java堆外的、直接向系统申请的内存区间

③. 代码演示：

```java
/**
 *  IO                  NIO (New IO / Non-Blocking IO)
 *  byte[] / char[]     Buffer
 *  Stream              Channel
 *
 * 查看直接内存的占用与释放
 */
public class BufferTest {
    private static final int BUFFER = 1024 * 1024 * 1024;//1GB

    public static void main(String[] args){
        //直接分配本地内存空间
        ByteBuffer byteBuffer = ByteBuffer.allocateDirect(BUFFER);
        System.out.println("直接内存分配完毕，请求指示！");

        Scanner scanner = new Scanner(System.in);
        scanner.next();

        System.out.println("直接内存开始释放！");
        byteBuffer = null;
        System.gc();
        scanner.next();
    }
}

```

④. 来源于NIO，通过存在堆中的DirectByteBuffer操作Native内存

![image-20220813093935425](images\image-20220813093935425.png)

![image-20220813094025685](images\image-20220813094025685.png)

⑤. 通常，访问直接内存的速度会优于Java堆。即读写性能高

⑥. 直接内存大小可以通过MaxDirectMemorySize设置，如果不指定，默认与堆的最大值一Xmx参数值一致

⑦. 简单理解： java process memory = java heap + native memory

![image-20220813094100065](images\image-20220813094100065.png)

# 五 执行引擎概述、机器码

为什么有了AOT静态提前编译,我们没用？而是用的JLT编译器？
(1). 使用JLT编译器,针对的是字节码文件,可以跨平台
(2). 可以在动态期间对齐进行优化,比如:逃逸分析优化(逃逸分析优化可以有如下几种:栈上分配、标量替换、同步消除)

![image-20220813110627635](images\image-20220813110627635.png)

## 执行引擎概述

①. 执行引擎是Java虚拟机的核心组成部分之一

②. JVM的主要任务是负责装载字节码到其内部,但字节码并不能够直接运行在操作系统之上,因为字节码指令并非等价于本地机器指令,它内部包含的仅仅只是一些能够被JVM锁识别的字节码指令、符号表和其他辅助信息

③. 那么,如果想让一个Java程序运行起来、执行引擎的任务就是将字节码指令解释/编译为对应平台上的本地机器指令才可以。简单来说,JVM中的执行引擎充当了将高级语言翻译为机器语言的译者

④. 执行引擎的工作过程 (从外观上来看,所有的Java虚拟机的执行引擎输入、输出都是一致的：输入的是字节码二进制流,处理过程是字节码解析执行的等效过程,输出的是执行结果)


1. 执行引擎在执行的过程中究竟需要执行什么样的字节码指令完全依赖于PC寄存器
2. 每当执行完一项指令操作后,PC寄存器就会更新下一条需要被执行的指令地址
3. 当然方法在执行的过程中,执行引擎有可能会通过存储在局部变量表中的对象引用准确定位到存储在Java堆区中的对象实例信息,以及通过对象头中的元数据指针定位到目标对象的类型信息。
   

![image-20220813110949936](images\image-20220813110949936.png)

##  Java代码编译和执行过程

①. 大部分的程序代码转换成物理机的目标代码或虚拟机能执行的指令集之前，都需要经过下面图中的各个步骤：

![image-20220813111245247](images\image-20220813111245247.png)

②. 什么是解释器( Interpreter),什么是JIT编译器？

1. 解释器:当Java虚拟机启动时会根据预定义的规范对字节码采用逐行解释的方式执行,将每条字节码文件中的内容“翻译”为对应平台的本地机器指令执行
2. JIT (Just In Time Compiler)编译器(即时编译器):就是虚拟机将源代码直接编译成和本地机器平台相关的机器语言

③. 为什么说Java是半编译半解释型语言?如下图要记住

1. JDK1.0时代,将Java语言定位为“解释执行”还是比较准确的。再后来,Java也发展出可以直接生成本地代码的编译器
2. 现在JVM在执行Java代码的时候,通常都会将解释执行与编译执行二者结合起来进行。

![image-20220813110627635](images\image-20220813110627635.png)

## 机器码、指令、汇编语言

①. 机器码：各种用二进制编码方式表示的指令，叫做机器指令码。开始，人们就用它采编写程序，这就是机器语言(0 | 1 组成的)

1. 机器语言虽然能够被计算机理解和接受，但和人们的语言差别太大，不易被人们理解和记忆，并且用它编程容易出差错
2. 用它编写的程序一经输入计算机，CPU直接读取运行，因此和其他语言编的程序相比，执行速度最快
3. 机器指令与CPU紧密相关，所以不同种类的CPU所对应的机器指令也就不同。

②. 指令就是把机器码中特定的0和1序列，简化成对应的指令（一般为英文简写，如mov，inc等），可读性稍好
(由于不同的硬件平台，执行同一个操作，对应的机器码可能不同，所以不同的硬件平台的同一种指令（比如mov），对应的机器码也可能不同)

③. 指令集

1. 不同的硬件平台，各自支持的指令，是有差别的。因此每个平台所支持的指令，称之为对应平台的指令集
2. 如常见的 (x86指令集，对应的是x86架构的平台 | ARM指令集，对应的是ARM架构的平台 )

④. 汇编语言

1. 在汇编语言中，用助记符（Mnemonics）代替机器指令的操作码，用地址符号（Symbol）或标号（Label）代替指令或操作数的地址
2. 在不同的硬件平台，汇编语言对应着不同的机器语言指令集，通过汇编过程转换成机器指令
   (由于计算机只认识指令码，所以用汇编语言编写的程序还必须翻译成机器指令码，计算机才能识别和执行)

⑤. 高级语言(如下图需要记住)

1. 为了使计算机用户编程序更容易些，后来就出现了各种高级计算机语言。高级语言比机器语言、汇编语言更接近人的语言
2. 当计算机执行高级语言编写的程序时，仍然需要把程序解释和编译成机器的指令码。完成这个过程的程序就叫做解释程序或编译程序

![image-20220813111905385](C:\Users\cs1\AppData\Roaming\Typora\typora-user-images\image-20220813111905385.png)

## 解释器 -负责响应时间

①.JVM设计者们的初衷仅仅只是单纯地为了满足Java程序实现跨平台特性,因此避免采用静态编译的方式直接生成本地机器指令,从而诞生了实现解释器在运行时采用逐行解释字节码执行程序的想法。

![image-20220813112250358](images\image-20220813112250358.png)



②. 解释器真正意义上所承担的角色就是`一个运行时“翻译者”`,将字节码文件中的内容“翻译”为对应平台的本地机器指令执行

③. 当一条字节码指令被解释执行完成后,接着再根据PC寄存器中记录的下一条需要被执行的字节码指令执行解释操作

④. 在Java的发展历史里，一共有两套解释执行器,即古老的字节码解释器、现在普遍使用的模板解释器(了解)

![image-20220813112401890](images\image-20220813112401890.png)

##  JIT编译器 -主要影响性能

HostSpot JVM的执行方式：当虛拟机启动的时候，解释器可以首先发挥作用，而不必等待即时编译器全部编译完成再执行，这样可以省去许多不必要的编译时间。并且随着程序运行时间的推移，即时编译器逐渐发挥作用，根据热点探测功能，将有价值的字节码编译为本地机器指令，以换取更高的程序执行效率。

 目前HotSpot VM所采用的热点探测方式是基于计数器的热点探测(采用基于计数器的热点探测,HotSpot VM将会为每一个 方法都建立2个不同类型的计数器,分别为方法调用计数器(Invocation Counter) 和回边计数器(BackEdge Counter) )

1. 方法调用计数器用于统计方法的调用次数
2. 回边计数器则用于统计循环体执行的循环次数

 方法调用计数器

1. 这个计数器就用于统计方法被调用的次数,它的默认阈值在Client模式下是1500次,在Server模式下是10000次。超过这个阈值,就会触发JIT编译
2. 这个阈值可以通过虚拟机参数-XX:CompileThreshold来人为设定
3. 当一个方法被调用时,会先检查该方法是否存在被JIT编译过的版本,如果存在,则优先使用编译后的本地代码来执行。如果不存在已被编译过的版本,则将此方法的调用计数器值加1,然后判断方法调用计数器与回边计数器值之和是否超过方法调用计数器的阈值。如果已超过阈值,那么将会向即时编译器提交一个该方法的代码编译请求

回边计数器

它的作用是统计一个方法中循环体代码执行的次数,在字节码中遇到控制流向后跳转的指令称为"边"(Back Edge)。显然,建立回边计数器统计的目的就是为了触发OSR编译(n-Stack Replacem ent)

热度衰减

缺省情况下HotSpot VM是采用解释器与即时编译器并存的架构,当然开发人员可以根据具体的应用场景,通过命令显式地为Java虚拟机指定在运行时到底是完全采用解释器执行,还是完全采用即时编译器执行。如下所示：

![image-20220813112948482](images\image-20220813112948482.png)

.-Xint:完全采用解释器模式执行程序；

.-Xcomp:完全采用即时编译器模式执行程序。如果即时编译出现问题,解释器会介入执行

.-Xmixed:采用解释器+即时编译器的混合模式共同执行程序。

①. 在HotSpot VM中内嵌有两个JIT编译器，分别为Client Compiler和Server
Compiler，但大多数情况下我们简称为C1编译器和C2编译器。开发人员可以通过如下命.令显式指定Java虚拟机在运行时到底使用哪一种即时编译器，如下所示：

![image-20220813113129380](images\image-20220813113129380.png)

C1和C2编译器不同的优化策略：

![image-20220813113207548](images\image-20220813113207548.png)

1. 一般来讲,JIT编译出来的机器码性能比解释器高。
2. C2编译器启动时长比C1编译器慢,系统稳定执行以后,C2编译器执行速度远远快于C1编译器。

# 六 垃圾回收算法整理

## 引用计数法

①. 原理:假设有一个对象A,任何一个对象对A的引用,那么对象A的引用计数器+1,当引用失败时,对象A的引用计数器就-1,如果对象A的计数器的值为0,就说明对象A没有引用了,可以被回收

②. 最大的缺陷:无法解决循环引用的问题,gc永远都清除不了(这也是引用计数法被淘汰的原因)

③. 代码展示:

```java
/**
 * -XX:+PrintGCDetails
 * 证明:java使用的不是引用计数算法
 */
public class RefCountGC {
    //这个成员属性唯一的作用就是占用一点内存
    private byte[] bigSize = new byte[5 * 1024 * 1024];//5MB

    Object reference = null;

    public static void main(String[] args) {
        RefCountGC obj1 = new RefCountGC();
        RefCountGC obj2 = new RefCountGC();

        obj1.reference = obj2;
        obj2.reference = obj1;

        obj1 = null;
        obj2 = null;
        //显式的执行垃圾回收行为
        //这里发生GC,obj1和obj2能否被回收？
        System.gc();

        try {
            Thread.sleep(1000000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}

```

![image-20220828103352486](images\image-20220828103352486.png)

④. 注意:Java使用的不是引用计数法(Java之所以没有使用引用计数法,是由于不能解决循环引用问题) | (Python使用了是引用

## 枚举根节点做可达性分析

①. 基本思路是通过一系列名为"GC Roots"的对象(集合)作为起点,从这个被称为GC ROOTs 的对象开始向下搜索,如果一个对象到GC Roots没有任何引用链相连时,则说明此对象是不可达对象(被回收),否则就是可达对象

![image-20220828103736480](images\image-20220828103736480.png)

②. 在java中,可作为GC Roots的对象有

> 	(1).虚拟机栈(栈帧中的局部变量表)中的引用对象(比如各个线程被调用的方法中使用到的参数、局部变量等)
> 	(2).本地方法栈中JNI(即一般来说native方法)中引用的对象[ 线程中的start方法 ]
> 	(3).静态属性引用的对象(比如:Java类的引用类型静态变量)
> 	(4).方法区中常量引用的对象(比如:字符串常量池(String Table)里的引用)
> 	(5).所有被synchronized持有的对象
> 	(6).Java虚拟机内部的引用(基本数据类型对应的Class对象,一些常驻的异常对象
> 	[如NullPointerException、OutofMemoryError],系统类加载器)
> 	(7).反映java虚拟机内部情况的JMXBean、JVMTI中注册的回调、本地代码缓存等
> 	(8).注意:除了这些固定的GC Roots集合之外,根据用户所选用的垃圾收集器以及当前回收的内存区域
> 不同,还可以有其他对象临时加入,共同构架完成整GC Roots集合。比如:分代收集和局部回收(面试加分项)

③. 关于GCroot对象集合 注意事项:

注意:除了这些固定的GC Roots集合之外,根据用户所选用的垃圾收集器以及当前回收的内存区域不同,还可以有其他对象临时加入,共同构架完成整GC Roots 集合。比如: 分代收集和局部回收

解释:如果只针对java堆中的某一区域进行垃圾回收(比如: 典型的只针对新生代),必须考虑到内存区域是虚拟机自己的实现细节,更不是孤立封闭的,这个区域的对象完全有可能被其他区域的对象所引用时候就需要一并将关联的区域对象也加入到GC Roots 集合中考虑,才能保证可达性分析的准确性
④. 小技巧:由于Root采用栈方式存放变量和指针,所以如果一个指针,它保存了堆内存里面的对象,但是自己又不存放在堆内存里面,那它就是一个Root

⑤. 优势:

1. 相对于引用计数法而言,可达性分析算法不仅同样具备实现简单和执行高效 等特点,更重要的是该算法可以有效解决在引用计数算法中循环引用的问题,防止内存泄漏的发生
2. 相较于引用计数算法,这里的可达性分析就是Java、C#选择的。这种类型的垃圾收集通常也叫做追踪性垃圾收集

## finalization机制

①. finalize( ) 方法允许在子类中被重写,用于对象被回收时进行资源释放。通常在这个方法中进行一些资源释放和清理的工作,比如关闭文件、套接字和数据库连接等

②. 当垃圾回收器发现没有引用指向一个对象,即:垃圾收集此对象之前,总会先调用这个对象的finalize( )方法

③. Java语言提提供了对象终止(finalization)机制来允许开发人员提供对象被销毁之前的自定义逻辑


### 不主动调用某个对象的finalize( ) 方法,应该交给垃圾回收机制调用,理由包括下面三点

①. 在finalize( )时可能会导致对象复活

②. finalize( )方法执行时间是没有保障的,它完全由GC线程决定,极端情况下,若不发生GC,则finalize( ) 方法将没有执行机会

③. 一个糟糕的finalize( )会严重影响GC的性能

④. 由于finalize( )方法的存在,虚拟机中的对象一般处于三种可能的状态

###  finalize( )方法中虚拟机的状态

如果从所有的根节点都无法访问到某个对象,说明对象已经不再使用了。一般来说,此对象需要被回收,但事实上,也并非是"非死不可"的,这时候它们暂时处于"缓刑"阶段。一个无法触及的对象肯能在某一个条件下"复活"自己,如果这样,那么对它的回收就是不合理的。为此,定义虚拟机中的对象可能有三种状态。如下:(掌握)

1. 可触及的:从根节点开始,可以到达这个对象
2. 可复活的:对象的所有引用都被释放,但是对象有可能在finalize( )中复活
3. 不可触及的: 对象的finalize( )被调用,并且没有复活,那么就会进入不可触及状态。不可触及的对象不可能被复活,因为finalize( )只会被调用一次

以上3种状态中,是由于finalize( )方法的存在,进行的区分。只有对象不可触及才可以被回收

### 判断一个对象是否可以进行回收

以上3种状态中,是由于finalize()方法的存在,进行的区分。只有在对象不可触及时才可以被回收。 判定是否可以回收具体过程 判定一个对象objA是否可回收,至少要经历两次标记过程:

![image-20220828105508029](images\image-20220828105508029.png)

```java
/**
 * 测试Object类中finalize()方法,即对象的finalization机制。
 *
 */
public class CanReliveObj {
    public static CanReliveObj obj;//类变量,属于 GC Root


    //此方法只能被调用一次
    @Override
    protected void finalize() throws Throwable {
        super.finalize();
        System.out.println("调用当前类重写的finalize()方法");
        obj = this;//当前待回收的对象在finalize()方法中与引用链上的一个对象obj建立了联系
    }


    public static void main(String[] args) {
        try {
            obj = new CanReliveObj();
            // 对象第一次成功拯救自己
            obj = null;
            System.gc();//调用垃圾回收器
            System.out.println("第1次 gc");
            // 因为Finalizer线程优先级很低,暂停2秒,以等待它
            Thread.sleep(2000);
            if (obj == null) {
                System.out.println("obj is dead");
            } else {
                System.out.println("obj is still alive");
            }
            System.out.println("第2次 gc");
            // 下面这段代码与上面的完全相同,但是这次自救却失败了
            obj = null;
            System.gc();
            // 因为Finalizer线程优先级很低,暂停2秒,以等待它
            Thread.sleep(2000);
            if (obj == null) {
                System.out.println("obj is dead");
            } else {
                System.out.println("obj is still alive");
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}

```

## 复制算法(Copying)

核心思想:将活着的内存空间分为两块,每次只使用其中一块,在垃圾回收时将正在.使用的内存中的存活对象复制到未被使用的内存块中,之后清除正在使用的内存块中的所有对象,交换两个内存的角色,最后完成垃圾回收。

![image-20220828105644763](images\image-20220828105644763.png)

一般过程(图解)

![image-20220828105804380](images\image-20220828105804380.png)

优点：没有标记和清除过程,实现简单,运行高效   不会产生内存碎片,且对象完整不丢

缺点:①. 浪费了10%的空间 ②. 对于G1这种分拆成为大量region的GC,复制而不是移动,意味着GC需要维护region之间对象引用关系,不管是内存占用或者时间开销也不小。

注意:复制算法需要复制的存活对象数量并不会太大,或者说非常低才行。因为新生代中的对象一般都是朝生夕死的,在新生代中使用复制算法是非常好的

注意:是当伊甸园区满后,会触发minjor gc,进行垃圾的回收

在新生代，对常规应用的垃圾回收,一次通常可以回收70%-99%的内存空间。回收性价比很高。所以现在的商业虚拟机都是用这种收集算法回收新生代

## 标记清除算法(Mark一Sweep)

- 标记一清除算法(Mark一Sweep)是一种非常基础和常见的垃圾收集算法,该算法被J . McCarthy等人在1960年提出并并应用于Lisp语言
- 标记:Collector(垃圾回收器)从引用根节点开始遍历,标记所有被引用的对象。一般是在对象的Header中记录为可达对象
- 清除: Collector(垃圾回收器)对堆内存从头到尾进行线性的遍历,如果发现某个对象在其Header中没有标记为可达对象,则将其回收
- 图解: CMS使用这种方式

![image-20220828110251073](images\image-20220828110251073.png)

优点：不需要额外的空间

缺点：.两次扫描,耗时严重 ②.清理出来的空闲内存不连续,会产生内存碎片,需要维护一个空闲列表 ③.效率比较低:递归与全堆对象遍历两次(经历了两次遍历)

注意:这里所谓的清除并不是真的置空,而是把需要清除的对象地址保存在空闲的地址列表里。下次有新对象需要加载时,判断垃圾的位置空间是否够,如果够,就存放

## 标记整理(压缩)算法(Mark-Compact)

1. 复制算法的高效性是建立在存活对象少、垃圾对象多的前提下的。这种情况在新生代经常发生,但是在老年代,更常见的情况是大部分对象都是存活对象。如果依然使用复制算法,由于存活对象较多,复制的成本也将很高。因此,基于老年代垃圾回收的特性,需要使用其他的算法。
2. 标记一清除算法的确可以应用在老年代中,但是该算法不仅执行效率低下,而且在执行完内存回收后还会产生内存碎片,所以JVM的设计者需要在此基础之上进行改进。标记一压缩(Mark一Compact) 算法由此诞生
3. 1970年前后,G. L. Steele 、C. J. Chene和D.S. Wise 等研究者发布标记一压缩算法。在许多现代的垃圾收集器中,人们都使用了标记一压缩算法或其改进版本。

执行过程:

1. 第一阶段和标记一清除算法一样,从根节点开始标记所有被引用对象.
2. 第二阶段将所有的存活对象压缩到内存的一端,按顺序排放。
3. 最后,清理边界外所有的空间。
4. 可以看到,标记的存活对象将会被整理,按照内存地址依次排列,而未被标记的内存会被清理掉。如此一来,当我们需要给新对象分配内存时,JVM只需要持有一个内存的起始地址即可,这比维护一个空闲列表显然少了许多开销

![image-20220828110713213](images\image-20220828110713213.png)

优点:①. 消除了标记一清除算法当中,内存区域分散的缺点,我们需要给新对象分配内存时,JVM只需要持有一个内存的起始地址即可②. 消除了复制算法当中,内存减半的高额代价

缺点:①. 从效率.上来说,标记一整理算法要低于复制算法。②. 移动对象的同时,如果对象被其他对象引用,则还需要调整引用的地址。移动过程中,需要全程暂停用户应用程序。即: STW

## 分代收集

分代算法是针对对象的不同特征,而使用合适的算法,这里面并没有实际上的新算法产生。与其说分代搜集算法是第五个算法,不如说它是对前三个算法的实际应用,在新生代使用复制算法eden在8分空间,survivor在两个1分,只浪费10%的空闲空间。老年代使用标记清除/标记压缩算法清除

### 新生代(Young Gen)

1. 新生代特点:区域相对老年代较小,对象生命周期短、存活率低,回收频繁。
2. 这种情况复制算法的回收整理,速度是最快的。复制算法的效率只和当前存活对象大小有关,因此很适用于年轻代的回收。而复制算法内存利用率不高的问题,通过hotspot中的两个survivor的设计得到缓解

### 老年代(Tenured Gen)

1. 老年代特点:区域较大,对象生命周期长、存活率高,回收不及年轻代频繁。
2. 这种情况存在大量存活率高的对象,复制算法明显变得不合适。一般是由标记一清除或者是标记一清除与标记一整理的混合实现。
   Mark阶段的开销与存活对象的数量成正比
   Sweep阶段的开销与所管理区域的大小成正相关
   Compact阶段的开销与存活对象的数据成正比

# 七 垃圾回收相关概念

## System.gc()的理解

在默认情况下,通过System.gc( )或者Runtime.getRuntime( ).gc( )的调用,会显式触发Full GC,同时对老年代和新生代进行回收,尝试释放被丢弃对象占用的内存。

然而System.gc()调用附带一个免责声明,无法保证对垃圾收集器的调用(无法保证马上触发GC)。(不保证一定会发生垃圾收集,只是给[jvm](https://so.csdn.net/so/search?q=jvm&spm=1001.2101.3001.7020)发出提示)

JVM实现者可以通过system.gc( )调用来决定JVM的GC行为。而一般情况下,垃圾回收应该是自动进行的,无须手动触发,否则就太过于麻烦了。在一些特殊情况下,如我们正在编写一个性能基准,我们可以在运行之间调用System.gc( )

以下代码,如果注掉System.runFinalization( ); 那么控制台不保证一定打印,证明了System.gc( )无法保证GC一定执行

```java
public class SystemGCTest {
    public static void main(String[] args) {
        new SystemGCTest();
        System.gc();//提醒jvm的垃圾回收器执行gc,但是不确定是否马上执行gc
        //与Runtime.getRuntime().gc();的作用一样。
        System.runFinalization();//强制调用使用引用的对象的finalize()方法
    }

    @Override
    protected void finalize() throws Throwable {
        super.finalize();
        System.out.println("SystemGCTest 重写了finalize()");
    }
}

```

手动gc理解不可达对象的回收行为

```java
public class LocalVarGC {
    public void localvarGC1() {
        byte[] buffer = new byte[10 * 1024 * 1024];//10MB
        System.gc();
        //输出: 不会被回收, FullGC时被放入老年代
        //[GC (System.gc()) [PSYoungGen: 14174K->10736K(76288K)] 14174K->10788K(251392K), 0.0089741 secs] [Times: user=0.01 sys=0.00, real=0.01 secs]
        //[Full GC (System.gc()) [PSYoungGen: 10736K->0K(76288K)] [ParOldGen: 52K->10649K(175104K)] 10788K->10649K(251392K), [Metaspace: 3253K->3253K(1056768K)], 0.0074098 secs] [Times: user=0.01 sys=0.02, real=0.01 secs]
    }

    public void localvarGC2() {
        byte[] buffer = new byte[10 * 1024 * 1024];
        buffer = null;
        System.gc();
        //输出: 正常被回收
        //[GC (System.gc()) [PSYoungGen: 14174K->544K(76288K)] 14174K->552K(251392K), 0.0011742 secs] [Times: user=0.00 sys=0.00, real=0.00 secs]
        //[Full GC (System.gc()) [PSYoungGen: 544K->0K(76288K)] [ParOldGen: 8K->410K(175104K)] 552K->410K(251392K), [Metaspace: 3277K->3277K(1056768K)], 0.0054702 secs] [Times: user=0.01 sys=0.00, real=0.01 secs]

    }

    public void localvarGC3() {
        {
            byte[] buffer = new byte[10 * 1024 * 1024];
        }
        System.gc();
        //输出: 不会被回收, FullGC时被放入老年代
        //[GC (System.gc()) [PSYoungGen: 14174K->10736K(76288K)] 14174K->10784K(251392K), 0.0076032 secs] [Times: user=0.02 sys=0.00, real=0.01 secs]
        //[Full GC (System.gc()) [PSYoungGen: 10736K->0K(76288K)] [ParOldGen: 48K->10649K(175104K)] 10784K->10649K(251392K), [Metaspace: 3252K->3252K(1056768K)], 0.0096328 secs] [Times: user=0.01 sys=0.01, real=0.01 secs]
    }

    public void localvarGC4() {
        {
            byte[] buffer = new byte[10 * 1024 * 1024];
        }
        int value = 10;
        System.gc();
        //输出: 正常被回收
        //[GC (System.gc()) [PSYoungGen: 14174K->496K(76288K)] 14174K->504K(251392K), 0.0016517 secs] [Times: user=0.01 sys=0.00, real=0.00 secs]
        //[Full GC (System.gc()) [PSYoungGen: 496K->0K(76288K)] [ParOldGen: 8K->410K(175104K)] 504K->410K(251392K), [Metaspace: 3279K->3279K(1056768K)], 0.0055183 secs] [Times: user=0.00 sys=0.00, real=0.01 secs]
    }

    public void localvarGC5() {
        localvarGC1();
        System.gc();
        //输出: 正常被回收
        //[GC (System.gc()) [PSYoungGen: 14174K->10720K(76288K)] 14174K->10744K(251392K), 0.0121568 secs] [Times: user=0.02 sys=0.00, real=0.02 secs]
        //[Full GC (System.gc()) [PSYoungGen: 10720K->0K(76288K)] [ParOldGen: 24K->10650K(175104K)] 10744K->10650K(251392K), [Metaspace: 3279K->3279K(1056768K)], 0.0101068 secs] [Times: user=0.01 sys=0.02, real=0.01 secs]
        //[GC (System.gc()) [PSYoungGen: 0K->0K(76288K)] 10650K->10650K(251392K), 0.0005717 secs] [Times: user=0.00 sys=0.00, real=0.00 secs]
        //[Full GC (System.gc()) [PSYoungGen: 0K->0K(76288K)] [ParOldGen: 10650K->410K(175104K)] 10650K->410K(251392K), [Metaspace: 3279K->3279K(1056768K)], 0.0045963 secs] [Times: user=0.01 sys=0.00, real=0.00 secs]
    }

    public static void main(String[] args) {
        LocalVarGC local = new LocalVarGC();
        local.localvarGC5();
    }
}

```

## 内存溢出(out of Memory)

javadoc中对OutOfMemoryError的解释是,没有空闲内存,并且垃圾收集器也无法提供更多内存

说明Java虚拟机的堆内存不够。原因有二

1. Java虚拟机的堆内存设置不够(比如:可能存在内存泄漏问题；也很有可能就是堆的大小不合理,比如我们要处理比较可观的数据量,但是没有显式指定JVM堆大小或者指定数值偏小。我们可以通过参数一Xms、一Xmx来调整)
2. 代码中创建了大量大对象,并且长时间不能被垃圾收集器收集(存在被引用)

这里面隐含着一层意思是,在抛出0utOfMemoryError之前,通常垃圾收集器会被触发,尽其所能去清理出空间。

1. 例如:在引用机制分析中,涉及到JVM会去尝试回收软引用指向的对象等。
2. 在java.nio.BIts.reserveMemory()方法中,我们能清楚的看到,System.gc()会被调用,以清理空间。

当然,也不是在任何情况下垃圾收集器都会被触发的(OOM之前会触发GC吗?)

(比如,我们去分配一一个超大对象,类似一个超大数组超过堆的最大值,JVM可以判断出垃圾收集并不能解决这个问题,所以直接拋出OutOfMemoryError)

## 内存泄漏(Memory Leak)

①. 也称作“存储渗漏”。严格来说,只有对象不会再被程序用到了,但是GC又不能回收他们的情况,才叫内存泄漏

②. 但实际情况很多时候一些不太好的实践(或疏忽)会导致对象的生命周期变得很长甚至导致OOM,也可以叫做宽泛意义上的“内存泄漏

③. 尽管内存泄漏并不会立刻引起程序崩溃,但是一旦发生内存泄漏,程序中的可用内存就会被逐步蚕食,直至耗尽所有内存,最终出现0utOfMemory异常,导致程序崩溃。

### Java中内存泄漏的8种情况

1. 单例模式(单例的生命周期和应用程序是一样长的,所以单例程序中,如果持有对外部对象的引用的话,那么这个外部对象是不能被回收的,则会导致内存泄漏的产生。)
2. 一些提供close的资源未关闭导致内存泄漏数据库连接( dataSourse. getConnection()),网络连接(socket)和io连接必须手动close,否则是不能被回收的。
3. 静态集合类(如HashMap、LinkedList等等。如果这些容器为静态的,那么它们的生命周期与JVM程序一致,则容器中的对象在程序结束之前将不能被释放,从而造成内存泄漏。简单而言,长生命周期的对象持有短生命周期对象的引用,尽管短生命周期的对象不再使用,但是因为长生命周期对象持有它的引用而导致不能被回收)
4. 内部类持有外部类(内部类持有外部类,如果一个外部类的实例对象的方法返回了一个内部类的实例对象。这个内部类对象被长期引用了,即使那个外部类实例对象不再被使用,但由于内部类持有外部类的实例对象,这个外部类对象将不会被垃圾回收,这也会造成内存泄漏。)
5. 变量不合理的作用域(一般而言,一个变量的定义的作用范围大于其使用范围,很有可能会造成内存泄漏。另一方面,如果没有及时地把对象设置为null,很有可能导致内存泄漏的发生)
6. 改变哈希值
7. 缓存泄漏(内存泄漏的另一个常见来源是缓存,一旦你把对象引用放入到缓存中,他就很容易遗忘。比如:之前项目在一次上线的时候,应用启动奇慢直到夯死,就是因为代码中会加载一个表中的数据到缓存(内存)中,测试环境只有几百条数据,但是生产环境有几百万的数据)
8. 监听器和回调(内存泄漏另一个常见来源是监听器和其他回调,如果客户端在你实现的API中注册回调,却没有显式的取消,那么就会积聚

```java
//静态集合类
public class MemoryLeak {
    static List list = new ArrayList();

    public void oomTests() {
        Object obj = new Object();//局部变量
        list.add(obj);
    }
}
//变量不合理的作用域
public class UsingRandom {
     private String msg;
     public void receiveMsg(){
        //private String msg;
        readFromNet();// 从网络中接受数据保存到msg中
        saveDB();// 把msg保存到数据库中
        //msg = null;
     }
}
//改变哈希值
public class ChangeHashCode {
    public static void main(String[] args) {
        HashSet set = new HashSet();
        Person p1 = new Person(1001, "AA");
        Person p2 = new Person(1002, "BB");

        set.add(p1);
        set.add(p2);
        p1.name = "CC";
        set.remove(p1);
        System.out.println(set);//2个对象！
        
//        set.add(new Person(1001, "CC"));
//        System.out.println(set);
//        set.add(new Person(1001, "AA"));
//        System.out.println(set);

    }
}

```

## Stop The World

Stop一the一World,简称STW,指的是GC事件发生过程中,会产生应用程序的停顿。停顿产生时整个应用程序线程都会被暂停,没有任何响应,有点像卡死的感觉,这个停顿称为STW

STW事件和采用哪款GC无关,所有的GC都有这个事件。

哪怕是G1也不能完全避免Stop一the一world情况发生,只能说垃圾回收器越来越优秀,回收效率越来越高,尽可能地缩短了暂停时间。

STW是JVM在后台自动发起和自动完成的。在用户不可见的情况下,把用户正常的工作线程全部停掉

开发中不要用System.gc(),会导致full gc,会导致Stop一the一world的发生

什么情况下会导致stop the world 记住：



1. 可达性分析算法中枚举根节点(GC Roots)会导致所有Java执行线程停顿
2. 进行gc的时候会发生STW现象(调用finalize()方法的时候会暂停用户线程
3. System.gc( ) | 调用finalize( )方法

## 多线程中的并行与并发

### 并发(Concurrent)

1. 在操作系统中,是指一个时间段中有几个程序都处于己启动运行到运行完毕之间,且这几个程序都是在同一个处理器_上运行
2. 并发不是真正意义上的“同时进行”,只是CPU把一个时间段划分成几个时间片段(时间区间),然后在这几个时间区间之间来回切换,由于CPU处理的速度非常快,只要时间间隔处理得当,即可让用户感觉是多个应用程序同时在进行

![image-20220828112246200](images\image-20220828112246200.png)

### 并行(Parallel)

1. 当系统有一个以上CPU时,当一个CPU执行一个进程时,另一个CPU可以执行另一个进程,两个进程互不抢占CPU资源,可以同时进行,我们称之为并行(Parallel)
2. 其实决定并行的因素不是CPU的数量,而是CPU的核心数量,比如一个CPU多个核也可以 并行
3. 图解:

![image-20220828112332837](images\image-20220828112332837.png)

### 垃圾回收的并行、串行、并发

①. 并行(Parallel) :指多条垃圾收集线程并行工作,但此时用户线程仍处于等待状态。如ParNew、 Parallel Scavenge、 Parallel 0ld；

②. 串行(Serial)

1. 相较于并行的概念,单线程执行。
2. 如果内存不够,则程序暂停,启动JVM垃圾回收器进行垃圾回收。回收完,再启动程序的线程。
3. 图解

![image-20220828112511943](images\image-20220828112511943.png)③. 并发

1. 指用户线程与垃圾收集线程同时执行(但不一定是并行的,可能会交替执行),垃圾回收线程在执行时不会停顿用户程序的运行
2. 在同一个时间段,用户线程和垃圾回收线程同时执行
3. 图解

![image-20220828112556477](images\image-20220828112556477.png)

###  安全点(Safepoint)

①. 程序执行时并非在所有地方都能停顿下来开始GC,只有在特定的位置才能停顿下来开始GC,这些位置称为"安全点(Safepoint)"

②. Safe Point的选择很重要,如果太少可能导致GC等待的时间太长,如果太频繁可能导致运行时的性能问题。大部分指令的执行时间都非常短暂,通常会根据“是否具有让程序长时间执行的特征”为标准。比如:选择些执行时间较长的指令作为Safe Point, 如方法调用、循环跳转和异常跳转等。
③. 如何在GC发生时,检查所有线程都跑到最近的安全点停顿下来呢？

1. 抢先式中断: (目前没有虚拟机采用了) 首先中断所有线程。如果还有线程不在安全点,就恢复线程,让线程跑到安全点。
2. 主动式中断: 设置一个中断标志,各个线程运行到Safe Point的时候主动轮询这个标志,如果中断标志为真,则将自己进行中断挂起。

## 引用

我们希望能描述这样一类对象: 当内存空间还足够时,则能保留在内存中；如果内存空间在进行垃圾收集后还是很紧张,则可以抛弃这些对象

在JDK 1.2版之后,Java对引用的概念进行了扩充,将引用分为强引用(StrongReference)、软引用(Soft Reference) 、弱引用(Weak Reference) 和虚引用(Phantom Reference) 4种,这4种引用强度依次逐渐减弱

除强引用外,其他3种引用均可以在java.lang.ref包中找到它们的身影。如下图,显示了这3种引用类型对应的类,开发人员可以在应用程序中直接使用它们。

Reference子类中只有终结器引用是包内可见的,其他3种引用类型均为public,可以在应用程序中直接使用

简单介绍下强软弱虚引用：

1. 强引用(StrongReference)I :最传统的“引用”的定义,是指在程序代码之中普遍存在的引用赋值,即类似“0bject obj=new object( )”这种引用关系。 无论任何情况下,只要强引用关系还存在,垃圾收集器就永远不会回收掉被引用的对象
2. 软引用(SoftReference) :在系统将要发生内存溢出之前,将会把这些对象列入回收范围之中进行第二次回收。如果这次回收后还没有足够的内存,才会抛出内存溢出异常 内存不足即回收
3. 弱引用(WeakReference) :被弱引用关联的对象只能生存到下一次垃圾收集之前。当垃圾收集器工作时,无论内存空间是否足够,都会回收掉被弱引用关联的对象。 发现即回收
4. 虚引用(PhantomReference) :一个对象是否有虛引用的存在,完全不会对其生存时 间构成影响,也无法通过虚引用来获得一个对象的实例。 为一个对象设置虛引用关联的唯一目的就是能在这个对象被收集器回收时收到一个系统通知(回收跟踪)

### 强引用:不回收

在Java程序中,最常见的引用类型是强引用(普通系统99%以上都是强引用),也就是我们最常见的普通对象引用,也是默认的引用类型。

当在Java语言中使用new操作符创建一个新的对象, 并将其赋值给一个变量的时候,这个变量就成为指向该对象的一个强引用。

强引用的对象是可触及的,垃圾收集器就永远不会回收掉被引用的对象。

对于一个普通的对象,如果没有其他的引用关系,只要超过了引用的作用域或者显式地将相应(强)引用赋值为null,就是可以当做垃圾被收集了,当然具体回收时机还是要看垃圾收集策略。

相对的,软引用、 弱引用和虚引用的对象是软可触及、弱可触及和虛可触及的,在一定条件下,都是可以被回收的。所以,强引用是造成Java内存泄漏的主要原因之一。

### 软引用: 内存不足即回收

软引用是用来描述一 些还有用,但非必需的对象。只被软引用关联着的对象,在系统将要发生内存溢出异常前,会把这些对象列进回收范围之中进行第二次回收,如果这次回收还没有足够的内存,才会抛出内存溢出异常。
注意:一次回收是回收强引用中没有引用的对象

软引用通常用来实现内存敏感的缓存。比如:高速缓存就有用到软引用。如果还有空闲内存,就可以暂时保留缓存,当内存不足时清理掉,这样就保证了使用缓存的同时,不会耗尽内存

类似弱引用,只不过Java虚拟机会尽量让软引用的存活时间长一些,迫不得.已才清理

1. 当内存足够: 不会回收软用的可达对象
2. 当内存不够时: 会回收软引用的可达对象

在JDK 1. 2版之后提供了java.lang.ref.SoftReference类来实现软引用。

```java
	Object obj = new object()； //声明强引用
	SoftReference<0bject> sf = new SoftReference<0bject>(obj)；
	obj = null； //销毁强引用
```

```java
/**
 * 软引用的测试:内存不足即回收
 * -Xms10m -Xmx10m -XX:+PrintGCDetails
 */
public class SoftReferenceTest {
    public static class User {
        public User(int id, String name) {
            this.id = id;
            this.name = name;
        }

        public int id;
        public String name;

        @Override
        public String toString() {
            return "[id=" + id + ", name=" + name + "] ";
        }
    }

    public static void main(String[] args) {
        //创建对象,建立软引用
//        SoftReference<User> userSoftRef = new SoftReference<User>(new User(1, "songhk"));
        //上面的一行代码,等价于如下的三行代码
        User u1 = new User(1,"songhk");
        SoftReference<User> userSoftRef = new SoftReference<User>(u1);
        u1 = null;//取消强引用


        //从软引用中重新获得强引用对象
        System.out.println(userSoftRef.get());

        System.gc();
        System.out.println("After GC:");
//        //垃圾回收之后获得软引用中的对象
        System.out.println(userSoftRef.get());//由于堆空间内存足够,所有不会回收软引用的可达对象。
//
        try {
            //让系统认为内存资源紧张、不够
//            byte[] b = new byte[1024 * 1024 * 7];
            byte[] b = new byte[1024 * 7168 - 399 * 1024];//恰好能放下数组又放不下u1的内存分配大小 不会报OOM
        } catch (Throwable e) {
            e.printStackTrace();
        } finally {
            //再次从软引用中获取数据
            System.out.println(userSoftRef.get());//在报OOM之前,垃圾回收器会回收软引用的可达对象。
        }
    }
}

```

###  弱引用: 发现即回收

​     弱引用也是用来描述那些非必需对象,被弱引用关联的对象只能生存到下一次垃圾收集发生为止。在系统GC时,只要发现弱引用,不管系统堆空间使用是否充足,都会回收掉只被弱引用关联的对象

​    但是,由于垃圾回收器的线程通常优先级很低,因此,并不一 定能很快地发现持有弱引用的对象。在这种情况下,弱引用对象可以存在较长的时间。

​    弱引用和软引用一样,在构造弱引用时,也可以指定一个引用队列,当弱引用对象被回收时,就会加入指定的引用队列,通过这个队列可以跟踪对象的回收情况。

​     软引用、弱引用都非常适合来保存那些可有可无的缓存数据。如果这么做,当系统内存不足时,这些缓存数据会被回收,不会导致内存溢出。而当内存资源充足时,这些缓存数据又可以存在相当长的时间,从而起到加速系统的作用

面试题:你开发中使用过WeakHashMap吗？

1. 通过查看WeakHashMap源码,可以看到其内部类Entry使用的就是弱引用
2. line 702 -> private static class Entry<K,V> extends WeakReference implements Map.Entry<K,V> {…}

```java
	public class WeakReferenceTest {
	    public static class User {
	        public User(int id, String name) {
	            this.id = id;
	            this.name = name;
	        }
	
	        public int id;
	        public String name;
	
	        @Override
	        public String toString() {
	            return "[id=" + id + ", name=" + name + "] ";
	        }
	    }
	
	    public static void main(String[] args) {
	        //构造了弱引用
	        WeakReference<User> userWeakRef = new WeakReference<User>(new User(1, "songhk"));
	        //从弱引用中重新获取对象
	        System.out.println(userWeakRef.get());
	
	        System.gc();
	        // 不管当前内存空间足够与否,都会回收它的内存
	        System.out.println("After GC:");
	        //重新尝试从弱引用中获取对象
	        System.out.println(userWeakRef.get());
	    }
	}

```

### 虚引用: 对象回收跟踪

虚引用(Phantom Reference),也称为“幽灵引用”或者“幻影引用”,是所有引用类型中最弱的一个。

为一个对象设置虚引用关联的唯一目的在于跟踪垃圾回收过程。比如:能在这个对象被收集器回收时收到一个系统通知。

引用必须和引用队列一起使用。虚引用在创建时必须提供一个引用队列作为参数。当垃圾回收器准备回收一个对象时,如果发现它还有虛引用,就会在回收对象后,将这个虚引用加入引用队列,以通知应用程序对象的回收情况。虚引用的get方法总是返回给null,因此无法访问对应的引用对象理解

由于虚引用可以跟踪对象的回收时间,因此,也可以将一些资源释放操作放置在虛引用中执行和记录

```java
/***
 * -xms10m -xmx10m
 */
public class MyObject {
    public static void main(String[] args) {

        ReferenceQueue<MyObject> referenceQueue = new ReferenceQueue();
        PhantomReference<MyObject> phantomReference = new PhantomReference<>(new MyObject(),referenceQueue);
        //System.out.println(phantomReference.get());

        List<byte[]> list = new ArrayList<>();

        new Thread(() -> {
            while (true)
            {
                list.add(new byte[1 * 1024 * 1024]);
                try { TimeUnit.MILLISECONDS.sleep(500); } catch (InterruptedException e) { e.printStackTrace(); }
                System.out.println(phantomReference.get());
            }
        },"t1").start();

        new Thread(() -> {
            while (true)
            {
                Reference<? extends MyObject> reference = referenceQueue.poll();
                if (reference != null) {
                    //下面这句话被打印出说明进行了gc,然后将对象放在了引用队列中,我们可以使用poll方法获取
                    System.out.println("***********有虚对象加入队列了"+reference);
                }
            }
        },"t2").start();

        //暂停几秒钟线程
        try { TimeUnit.SECONDS.sleep(5); } catch (InterruptedException e) { e.printStackTrace(); }

    }

    @Override
    protected void finalize() throws Throwable {
        // gc finalize method over 这句话被打印出来,说明进行了gc
        System.out.println("gc finalize method over");
    }
}

```

# 八 垃圾回收算法

截止JDK 1.8,一共有7款不同的垃圾收集器。每一款不同的垃圾收集器都有不同的特点,在具体使用的时候,需要根据具体的情况选用不同的垃圾收集器

![image-20220904115635269](images\image-20220904115635269.png)

不同厂商、不同版本的虚拟机实现差别很大。HotSpot 虚拟机在JDK7/8后所有收集器及组合(连线),如下图:

![image-20220904105957572](images\image-20220904105957572.png)

![image-20220904110028731](images\image-20220904110028731.png)

## 评估GC的性能指标

吞吐量:运行用户代码的时间占总运行时间的比例
	吞吐量 = 运行用户代码时间 /(运行用户代码时间 + 垃圾收集时间)
	比如:虚拟机总共运行了100分钟,其中垃圾收集花掉1分钟,那吞吐量就是99%
	吞吐量优先,意味着在单位时间内,STW的时间最短:0.2 + 0.2 = 0.4

![image-20220904110153323](images\image-20220904110153323.png)

暂停时间:执行垃圾收集时,程序的工作线程被暂停的时间
暂停时间优先,意味着尽可能让单次STW的时间最短:0.1 + 0.1 + 0.1 + 0.1 + 0.1 = 0.5

![image-20220904110224400](images\image-20220904110224400.png)

内存占用: Java堆区所占的内存大小

垃圾收集开销:吞吐量的补数,垃圾收集所用时间与总运行时间的比例

收集频率:相对于应用程序的执行,收集操作发生的频率

### 评估GC的性能指标:吞吐量vs暂停时间

1. 这三者共同构成一个“不可能三角”。三者总体的表现会随着技术进步而越来越好。一款优秀的收集器通常最多同时满足其中的两项。
2. 这三项里,暂停时间的重要性日益凸显。因为随着硬件发展,内存占用 多些越来越能容忍,硬件性能的提升也有助于降低收集器运行时对应用程序的影响,即提高了吞吐量。而内存的扩大,对延迟反而带来负面效果。‘
3. 简单来说,主要抓住两点:吞吐量、暂停时间
4. 现在JVM调优标准:在最大吞吐量优先的情况下,降低停顿时间

## 不同的垃圾回收器概述

7款经典的垃圾收集器
	串行回收器:Serial、Serial Old
	并行回收器:ParNew、Parallel Scavenge、Parallel Old
	并发回收器:CMS、G1

![image-20220904110641705](images\image-20220904110641705.png)

### 查看默认的垃圾收集器

1. -xx:+PrintCommandLineFlags: 查看命令行相关参数(包含使用的垃圾收集器)

```java
/**
 *  -XX:+PrintCommandLineFlags
 *  -XX:+UseSerialGC:表明新生代使用Serial GC ,同时老年代使用Serial Old GC
 *  -XX:+UseParNewGC:标明新生代使用ParNew GC
 *  -XX:+UseParallelGC:表明新生代使用Parallel GC
 *  -XX:+UseParallelOldGC : 表明老年代使用 Parallel Old GC
 *  说明:二者可以相互激活
 *  -XX:+UseConcMarkSweepGC:表明老年代使用CMS GC。同时,年轻代会触发对ParNew 的使用
 */
public class GCUseTest {
    public static void main(String[] args) {
        ArrayList<byte[]> list = new ArrayList<>();

        while(true){
            byte[] arr = new byte[100];
            list.add(arr);
            try {
                Thread.sleep(10);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
输出:
(-XX:InitialHeapSize=268435456 -XX:MaxHeapSize=4294967296 
-XX:+PrintCommandLineFlags -XX:+UseCompressedClassPointers 
-XX:+UseCompressedOops -XX:+UseParallelGC)

```

使用命令行指令: jinfo 一flag 相关垃圾回收器参数进程ID

( jinfo -flag UseParallelGC 进程id
jinfo -flag UseParallelOldGC 进程id )

![image-20220904111813264](images\image-20220904111813264.png)

## Serial、SerialOld 回收器:串行回收

①. Serial收集器采用复制算法、串行回收和"Stop一 the一World"机制的方式执行内存回收

②. Serial 0ld收集器同样也采用了串行回收 和"Stop the World"机制,只不过内存回收算法使用的是标记一压缩算法

③. 单线程回收:使用一个cpu或一条线程去完成垃圾收集工作 | 必须暂停其他所有的工作线程

④. 使用 -XX: +UseSerialGC 参数可以指定年轻代和老年代都使用串行收集器等价于新生代用Serial GC,且老年代用Serial 0ld GC

控制台输出:
 -XX:InitialHeapSize=268435456

 -XX:MaxHeapSize=4294967296

 -XX:+PrintCommandLineFlags

 -XX:+UseCompressedClassPointers -XX:+UseCompressedOops -XX:+UseSerialGC
![image-20220904112001539](images\image-20220904112001539.png)

## ParNew回收器:并行回收

①. 如果说Serial GC是年轻代中的单线程垃圾收集器,那么ParNew收集器则是Serial收集器的多线程版本

②. ParNew收集器除了采用并行回收的方式执行内存回收外,两款垃圾收集器之间几乎没有任何区别。ParNew收集器在年轻代中同样也是采用复制算法、"Stop一 the一World"机制

③. 因为除Serial外,目前只有ParNew GC能与CMS收集器配合工作

④. 在程序中,开发人员可以通过选项"-XX:+UseParNewGC"手动指定使用.ParNew收集器执行内存回收任务。它表示年轻代使用并行收集器, 不影响老年代

⑤. -XX:ParallelGCThreads 限制线程数量,默认开启和CPU数据相同的线程数。

![image-20220904112444193](images\image-20220904112444193.png)

SerialGC 和 ParNewGC哪个更好?

1. ParNew 收集器运行在多CPU的环境下,由于可以充分利用多CPU、多核心等物理硬件资源优势,可以更快速地完成垃圾收集,提升程序的吞吐量
2. 但是在单个CPU的环境下,ParNew收集器不比Serial 收集器更高效。虽然Serial收集器是基于串行回收,但是由于CPU不需要频繁地做任务切换,因此可以有效避免多线程交互过程中产生的一些额外开销

## Parallel、ParallelOld:吞吐量优先

①. HotSpot的年轻代中除了拥有ParNew收集器是基于并行回收的以外, Parallel Scav enge收集器同样也采用了复制算法、并行回收和"Stop the World"机制。在Java8中,默认是此垃圾收集器

②. 那么Parallel收集器的出现是否多此一举？

1. 和ParNew收集器不同,Parallel Scavenge收集器的目标则是达到一个可控制的吞吐量(Throughp ut),它也被称为吞吐量优先的垃圾收集器。
2. 自适应调节策略也是Parallel Scavenge与ParNew一个重要区别

③. 高吞吐量则可以高效率地利用CPU时间,尽快完成程序的运算任务,主要适合在后台运算而不需要太多交互的任务。因此,常见在服务器环境中使用。例如,那些执行批量处理、订单处理、工资支付、科学计算的应用程序。

④. Parallel收集器在JDK1.6时提供了用于执行老年代垃圾收集的 Parallel 0ld收集器,用来代替老年代的Serial 0ld收集器

⑤. Parallel 0ld收集器采用了标记一压缩算法,但同样也是基于并行回收和”Stop一the一World"机制

![image-20220904114111634](images\image-20220904114111634.png)

⑥. 在程序吞吐量优先的应用场景中,Parallel 收集器和Parallel 0ld收集器的组合,在Server模式下的内存回收性能很不错

⑦. 参数配置
-XX:+UseParallelGC手动指定年轻代使用Parallel并行收集器执行内存回收任务

-XX:+UseParallelOldGC手动指定老年代都是使用并行回收收集器。(分别适用于新生代和老年代。默认jdk8是开启的。上面两个参数,默认开启一个,另一个也会被开启。(互相激活))

-XX:ParallelGCThreads设置年轻代并行收集器的线程数。一般地,最好与CPU数量相等,以避免过多的线程数影响垃圾收集性能
(在默认情况下,当CPU 数量小于8个, ParallelGCThreads 的值等于CPU 数量。当CPU数量大于8个,ParallelGCThreads 的值等于3+[5*CPU_Count]/8] )

-XX:MaxGCPauseMillis:设置垃圾收集器最大停顿时间(即STW的时间)。单位是毫秒(为了尽可能地把停顿时间控制在MaxGCPauseMills以内,收集器在工作时会调整Java堆大小或者其他一些参数对于用户来讲,停顿时间越短体验越好。但是在服务器端,我们注重高并发,整体的吞吐量。所以服务器端适合Parallel,进行控制该参数使用需谨慎)

-XX:+UseAdaptiveSizePolicy 设置Parallel Scavenge收集器具有自适应调节策略(在这种模式下,年轻代的大小、Eden和Survivor的比例、晋升老年代的对象年龄等参数会被自动调整,已达到在堆大小、吞吐量和停顿时间之间的平衡点在手动调优比较困难的场合,可以直接使用这种自适应的方式,仅指定虚拟机的最大堆、目标的吞吐量(GCTimeRatio)和停顿时间(MaxGCPauseMills),让虚拟机自己完成调优工作)

## CMS垃圾回收器，低延迟

在JDK1.5时期, HotSpot推出了一款在强交互应用中几乎可认为有划时代意义的垃圾收集器: CMS (Concurrent 一Mark 一 Sweep)收集器,这款收集器是HotSpot虚拟机中第一款真正意义上的并发收集器,它第一次实现了让垃圾收集线程与用户线程同时工作

CMS收集器的关注点是尽可能缩短垃圾收集时用户线程的停顿时间。停顿时间越短(低延迟)就越适合与用户交互的程序,良好的响应速度能提升用户体验。

CMS的垃圾收集算法采用标记一清除算法,并且也会" stop一the一world"

不幸的是,CMS 作为老年代的收集器,却无法与JDK 1.4.0 中已经存在的新生代收集器Parallel Scavenge配合工作,所以在JDK 1. 5中使用CMS来收集老年代的时候,新生代只能选择ParNew或者Serial收集器中的一个

在G1出现之前,CMS使用还是非常广泛的。一直到今天,仍然有很多系统使用CMS GC

![image-20220904114724642](images\image-20220904114724642.png)

### CMS过程(原理)

①. 初始标记(Initial一Mark)仅仅只是标记出和GCRoots能直接关联到的对象,有STW现象、暂时时间非常短

②. 并发标记(Concurrent一Mark)阶段:从GC Roots的直接关联对象开始遍历整个对象图的过程,这个过程耗时较长但是不需要停顿用户线程,可以与垃圾收集线程一起并发运行(并发标记阶段有三色标记,下文有记录)

③. 重新标记(Remark) 阶段:有些对象可能开始是垃圾,在并发标记阶段,由于用户线程的影响,导致不是垃圾了,这里需要重新标记的是这部分对象,这个阶段的停顿时间通常会比初始标记阶段稍长一些,但也远比并发标记阶段的时间短

④. 并发清除:此阶段清理删除掉标记阶段判断的已经死亡的对象,释放内存空间。由于不需要移动存活对象,所以这个阶段也是可以与用户线程同时并发的

⑤. 补充说明:

​	在CMS回收过程中,还应该确保应用程序用户线程有足够的内存可用。因此,CMS收集器不能像其他收集器那样等到老年代几乎完全被填满了再进行收集,而是当堆内存使用率达到某一阈值时,便开始进行回收,以确保应用程序在CMS工作过程中依然有足够的空间支持应用程序运行。要是CMS运行期间预留的内存无法满足程序需要,就会出现一次“Concurrent Mode Failure”失败,这时虚拟机将启动后备预案:临时启用Serial 0ld收集器来重新进行老年代的垃圾收集,这样停顿时间就很长了。

​	CMS收集器的垃圾收集算法采用的是标记一清除算法,这意味着每次执行完内存回收后,由于被执行内存回收的无用对象所占用的内存空间极有可能是不连续的一些内存块,不可避免地将会产生一些内存碎片。 那么CMS在为新对象分配内存空间时,将无法使用指针碰撞(Bump the Pointer) 技术,而只能够选择空闲列表(Free List) 执行内存分配。
(在并发标记阶段一开始不是垃圾,最后变成了垃圾)

### CMS优缺点

①. 优点:并发收集、低延迟

②. CMS的弊端:

1. 会产生内存碎片
2. CMS收集器对CPU资源非常敏感
   (在并发阶段,它虽然不会导致用户停顿,但是会因为占用了一部分线程而导致应用程序变慢,总吞吐量会降低)
3. CMS收集器无法处理浮动垃圾。可能出现"Concurrent Mode Failure" 失败而导致另一次Full GC的产生。在并发标记阶段由于程序的工作线程和垃圾收集线程是同时运行或者交叉运行的,那么在并发标记阶段如果产生新的垃圾对象,CMS将无法对这些垃圾对象进行标记,最终会导致这些新产生的垃圾对象没有被及时回收,从而只能在下一次执行GC时释放这些之前未被回收的内存空间

③.区分两个注意事项

1. 并发标记阶段,在遍历GCRoots,用户线程也在执行,若此时遍历过一个对象发现没有引用,但由于用户线程并发执行,这期间可能导致遍历过的这个对象又被其他对象引用,所以才需要重新标记阶段再遍历一次看又没有漏标记的,否则就会导致被重新引用的对象被清理掉
2. 浮动垃圾:在并发标记阶段一开始不是垃圾,最后变成了垃圾(属于多标的情况)

###  CMS参数设置

①. -XX:+UseConcMarkSweepGc:手动指定使用CMS收集器执行内存回收任务
(开启该参数后会自动将一XX: +UseParNewGc打开。即: ParNew (Young区用) +CMS (0ld区用) +Serial 0ld的组合)

②. -XX:CMSlnitiatingOccupanyFraction:设置堆内存使用率的阈值,一旦达到该阈值,便开始进行回收

1. JDK5及以前版本的默认值为68,即当老年代的空间使用率达到68%时,会执行一次CMS 回收。JDK6及以上版本默认值为92%
2. 如果内存增长缓慢,则可以设置一个稍大的值,大的阈值可以有效降低CMS的触发频率,减少老年代回收的次数可以较为明显地改善应用程序性能。反之,如果应用程序内存使用率增长很快,则应该降低这个阈值,以避免频繁触发老年代串行收集器。因此通过该选项便可以有效降低Full GC的执行次数

③. -XX:+UseCMSCompactAtFullCollection:用于指定在执行完Full GC后对内存空间进行压缩整理,以此避免内存碎片的产生。不过由于内存压缩整理过程无法并发执行,所带来的问题就是停顿时间变得更长了

④. -XX:CMSFullGCsBeforeCompaction:设置在执行多少次Full GC后对内存空间进行压缩整理

⑤. -XX:ParallelCMSThreads:设置CMS的线程数量

(CMS 默认启动的线程数是(ParallelGCThreads+3)/4,ParallelGCThreads 是年轻代并行收集器的线程数。当CPU 资源比较紧张时,受到CMS收集器线程的影响,应用程序的性能在垃圾回收阶段可能会非常糟糕)

## G1垃圾收集器

### 什么是G1垃圾收集器

①. G1(Garbage-First)是一款面向服务端应用的垃圾收集器,主要针对配备多核CPU及大容量内存的机器,以及高概率满足GC停顿时间的同时,还兼具高吞吐量的性能特征

②. 在JDK1.7版本正式启用,是JDK 9以后的默认垃圾收集器,取代了CMS 回收器。

![image-20220904115910615](images\image-20220904115910615.png)

### 为什么名字叫Garbage First

①. G1是一个并行回收器,它把堆内存分割为很多不相关的区域(region物理上不连续),把堆分为2048个区域,每一个region的大小是1 - 32M不等,必须是2的整数次幂。使用不同的region可以来表示Eden、幸存者0区、幸存者1区、老年代等

②. 每次根据允许的收集时间,优先回收价值最大的Region
(每次回收完以后都有一个空闲的region,在后台维护一个优先列表

③. 由于这种方式的侧重点在于回收垃圾最大量的区间(Region),所以我们给G1一个名字:垃圾优先(Garbage First)

④. 下面说一个问题:既然我们已经有了前面几个强大的GC,为什么还要发布Garbage First(G1)GC？官方给G1设定的目标是在延迟可控的情况下获得尽可能高的吞吐量,所以才担当起"全功能收集器"的重任与期望。

### G1垃圾收集器的特点、缺点

①. 并行和并发

1. 并行性: G1在回收期间,可以有多个Gc线程同时工作,有效利用多核计算能力。此时用户线程STW
2. 并发性: G1拥有与应用程序交替执行的能力,部分工作可以和应用程序同时执行,因此,一般来说,不会在整个回收阶段发生完全阻塞应用程序的情况

②. 分代收集

1. 从分代上看,G1依然属于分代型垃圾回收器,它会区分年轻代和老年代,年轻代依然有Eden区和Survivor区。但从堆的结构上看,它不要求整个Eden区、年轻代或者老年代都是连续的,也不再坚持固定大小和固定数量。
2. 将堆空间分为若干个区域(Region),这些区域中包含了逻辑上的年轻代和老年代。
3. 和之前的各类回收器不同,它同时兼顾年轻代和老年代。对比其他回收器,或者工作在年轻代,或者工作在老年代

③. 空间整合

​	G1将内存划分为一个个的region。 内存的回收是以region作为基本单位的。Region之间是复制算法,但整体上实际可看作是标记一压缩(Mark一Compact)算法,两种算法都可以避免内存碎片。这种特性有利于程序长时间运行,分配大对象时不会因为无法找到连续内存空间而提前触发下一次GC。尤其是当Java堆非常大的时候,G1的优势更加明显)

④. 可预测的停顿时间模型(即:软实时soft real一time)

​	(这是 G1 相对于 CMS 的另一大优势,G1除了追求低停顿外,还能建立可预测的停顿时间模型,能让使用者明确指定在一个长度为 M 毫秒的时间片段内,消耗在垃圾收集上的时间不得超过 N 毫秒、可以通过参数-XX:MaxGCPauseMillis进行设置)

1. 由于分区的原因,G1可以只选取部分区域进行内存回收,这样缩小了回收的范围,因此对于全局停顿情况的发生也能得到较好的控制
2. G1 跟踪各个 Region 里面的垃圾堆积的价值大小(回收所获得的空间大小以及回收所需时间的经验值),在后台维护一个优先列表,每次根据允许的收集时间,优先回收价值最大的Region。保证了G1收集器在有限的时间内可以获取尽可能高的收集效率
3. 相比于CMS GC,G1未必能做到CMS在最好情况下的延时停顿,但是最差情况要好很多。(CMS的最好的情况G1不一定比的上,但是CMS最差的部分,G1可以比上)

⑤. 缺点:

1. 相较于CMS,G1还不具备全方位、压倒性优势。比如在用户程序运行过程中,G1无论是为了垃圾收集产生的内存占用(Footprint)还是程序运行时的额外执行负载(Overload)都要比CMS要高。
2. 从经验上来说,在小内存应用上CMS的表现大概率会优于G1,而G1在大内存应用上则发挥其优势。平衡点在6-8GB之间

### 参数设置

①. -XX:+UseG1GC:手动指定使用G1收集器执行内存回收任务

②. -XX:G1HeapRegionSize:设置每个Region的大小。值是2的幂,范围是1MB到32MB之间,目标是根据最小的Java堆大小划分出约2048个区域。默认是堆内存的1/2000

③. -XX:MaxGCPauseMillis:设置期望达到的最大Gc停顿时间指标(JVM会尽力实现,但不保证达到)。默认值是200ms
(如果这个值设置很小,如20ms,那么它收集的region会少,这样长时间后,堆内存会满。产生FullGC,FullGC会出现STW,反而影响用户体验)

④. -XX:ParallelGCThread:设置stw时GC线程数的值。最多设置为8(垃圾回收线程)

⑤. -XX:ConcGCThreads:设置并发标记的线程数。将n设置为并行垃圾回收线程数(ParallelGCThreads)的1/4左右

⑥. -XX:Ini tiatingHeapOccupancyPercent:设置触发并发GC周期的Java堆占用率阈值。超过此值,就触发GC。默认值是45

### 调优操作步骤

①. G1的设计原则就是简化JVM性能调优,开发人员只需要简单的三步即可完成调优：

1. 开启G1垃圾收集器
2. 设置堆的最大内存
3. 设置最大的停顿时间

②. G1中提供了三种垃圾回收模式：YoungGC、Mixed GC和Full GC,在不同的条件下被触发

### Region详解

①. 使用G1收集器时,它将整个Java堆划分成约2048个大小相同的独立Region块,每个Region块大小根据堆空间的实际大小而定,整体被控制在1MB到32MB之间,且为2的N次幂,即1MB, 2MB, 4MB, 8MB, 1 6MB, 32MB。可以通过-XX:G1Hea pRegionSize设定。所有的Region大小相同,且在JVM生命周期内不会被改变

②. 一个region 有可能属于Eden, Survivor 或者0ld/Tenured 内存区域。但是一个region只可能属于一个角色。图中的E表示该region属于Eden内存区域,s表示属于Survivor内存区域,0表示属于0ld内存区域。图中空白的表示未使用的内存空间

③. 垃圾收集器还增加了一种新的内存区域,叫做Humongous内存区域,如图中的H块。主要用于存储大对象,如果超过1. 5个region,就放到H

对于堆中的大对象,默认直接会被分配到老年代,但是如果它是一个短期存在的大对象,就会对垃圾收集器造成负面影响。为了解决这个问题,G1划分了一个Humongous区,它用来专门存放大对象。如果一个H区装不下一个大对象,那么G1会寻找连续的H区来存储。为了能找到连续的H区,有时候不得不启动Full GC。G1的大多数行为都把H区作为老年代的一部分来看待)
![image-20220904121030682](images\image-20220904121030682.png)

### 记忆集与写屏障

①. 问题:一个Region不可能是孤立的,一个Region中的对象可能被其他对象引用,如新生代中引用了老年代,这个时候垃圾回收时,会去扫描老年代,会出现STW

②. 解决:无论是G1还是分带收集器,JVM都是使用Remembered Set来避免全局扫描。每个Region都有一个对应的Remembered Set；[下面过程需要掌握]

1. 每次Reference类型数据写操作时,都会产生一个Write Barrier暂时
2. 然后检查将要写入的引用指向的对象是否和该Reference类型数据在不同的Region (其他收集器:检查老年代对象是否引用了新生代对象)
3. 如果不同,通过CardTable把相关引用信息记录到引用指向对象的所在Region对应的Remembered Set中；
4. 当进行垃圾收集时,在GC根节点的枚举范围加入Remembered Set；就可以保证不进行全局扫描,也不会有遗漏

![image-20220904121220733](images\image-20220904121220733.png)



### G1回收器垃圾回收过程

①. G1 GC的垃圾回收过程主要包括如下三个环节：

1. 年轻代GC (Young GC)
2. 老年代并发标记过程 (Concurrent Marking)
3. 混合回收(Mixed GC)
4. 顺时针,young gc -> young gc + concurrent mark-> Mixed GC顺序,进行垃圾回收。

![image-20220904121340546](images\image-20220904121340546.png)

②. 应用程序分配内存,当年轻代的Eden区用尽时开始年轻代回收过程；G1的年轻代收集阶段是一个并行(多个垃圾线程)的独占式收集器。在年轻代回收期,G1 GC暂停所有应用程序线程,启动多线程执行年轻代回收。然后从年轻代区间移动存活对象到Survivor区间或者老年区间,也有可能是两个区间都会涉及

③. 当堆内存使用达到一定值(默认45%)时,开始老年代并发标记过程

④. 标记完成马上开始混合回收过程。对于一个混合回收期,G1 GC从老年区间移动存活对象到空闲区间,这些空闲区间也就成为了老年代的一部分。和年轻代不同,老年代的G1回收器和其他GC不同,G1的老年代回收器不需要整个老年代被回收,一次只需要扫描/回收一小部分老年代的Region就可以了。同时,这个老年代Region是和年轻代一起被回收的。

⑤. 举个例子：一个Web服务器,Java进程最大堆内存为4G,每分钟响应1500个请求,每45秒钟会新分配大约2G的内存。G1会每45秒钟进行一次年轻代回收,每31个小时整个堆的使用率会达到45%,会开始老年代并发标记过程,标记完成后开始四到五次的混合回收

#### 年轻代GC

回收时机
(1). 当Eden空间耗尽时,G1会启动一次年轻代垃圾回收过程
(2). 年轻代垃圾回收只会回收Eden区和Survivor区
(3). 回收前:

![image-20220904121718436](images\image-20220904121718436.png)

①. 根扫描: 一定要考虑remembered Set,看是否有老年代中的对象引用了新生代对象
(根是指static变量指向的对象,正在执行的方法调用链条上的局部变量等。根引用连同RSet记录的外部引用作为扫描存活对象的入口)

②.更新RSet:处理dirty card queue(见备注)中的card,更新RSet。 此阶段完成后,RSet可以准确的反映老年代对所在的内存分段中对象的引用(dirty card queue: 对于应用程序的引用赋值语句object.field=object,JVM会在之前和之后执行特殊的操作以在dirty card queue中入队一个保存了对象引用信息的card。在年轻代回收的时候,G1会对Dirty CardQueue中所有的card进行处理,以更新RSet,保证RSet实时准确的反映引用关系。那为什么不在引用赋值语句处直接更新RSet呢？这是为了性能的需要,RSet的处理需要线程同步,开销会很大,使用队列性能会好很多)

③. 处理RSet:识别被老年代对象指向的Eden中的对象,这些被指向的Eden中的对象被认为是存活的对象

④. 复制对象:复制算法
(此阶段,对象树被遍历,Eden区 内存段中存活的对象会被复制到Survivor区中空的内存分段,Survivor区内存段中存活的对象如果年龄未达阈值,年龄会加1,达到阀值会被会被复制到01d区中空的内存分段。如果Survivor空间不够,Eden空间的 部分数据会直接晋升到老年代空间)

⑤. 处理引用:处理Soft,Weak, Phantom, Final, JNI Weak等引用。最终Eden空间的数据为空,GC停止工作,而目标内存中的对象都是连续存储的,没有碎片,所以复制过程可以达到内存整理的效果,减少碎片

#### 并发标记过程

①. 初始标记阶段:标记从根节点直接可达的对象。这个阶段是STW的,并且会触发一次年轻代GC

②. 根区域扫描(Root Region Scanning):G1 GC扫描Survivor区直接可达的老年代区域对象,并标记被引用的对象。这一过程必须在young GC之前完成(YoungGC时,会动Survivor区,所以这一过程必须在young GC之前完成)

③. 并发标记(Concurrent Marking): 在整个堆中进行并发标记(和应用程序并发执行),此过程可能被young GC中断。在并发标记阶段,若发现区域对象中的所有对象都是垃圾,那这个区域会被立即回收。同时,并发标记过程中,会计算每个区域的对象活性(区域中存活对象的比例)。

④. 再次标记(Remark):由于应用程序持续进行,需要修正上一次的标记结果。是STW的。G1中采用了比CMS更快的初始快照算法:snapshot一at一the一beginning (SATB)

⑤. 独占清理(cleanup,STW):计算各个区域的存活对象和GC回收比例,并进行排序,识别可以混合回收的区域。为下阶段做铺垫。是STW的。(这个阶段并不会实际上去做垃圾的收集)

⑥. 并发清理阶段:识别并清理完全空闲的区域

#### 混合回收 Mixed GC

Mixed GC并不是FullGC,老年代的堆占有率达到参数(-XX:InitiatingHeapOccupancyPercent)设定的值则触发,回收所有的Young和部分Old(根据期望的GC停顿时间确定old区垃圾收集的优先顺序)以及大对象区,正常情况G1的垃圾收集是先做MixedGC,主要使用复制算法,需要把各个region中存活的对象拷贝到别的region里去,拷贝过程中如果发现没有足够的空region能够承载拷贝对象就会触发一次Full GC

![image-20220904122244665](images\image-20220904122244665.png)

#### Full GC

①. 堆内存过小,当G1在复制存活对象的时候没有空的内存分段可用,则会回退到full gc,这种情况可以通过增大内存解决

②. 暂停时间-XX:MaxGCPauseMillis设置短,回收频繁。由于用户线程和GC线程一起执行,可能用户线程产生的垃圾大于GC线程回收的垃圾,会导致内存不足,触发Full gc

#### 优化建议

①. 年轻代发送GC频率高,避免使用-Xmn或-XX:NewRatio,让JVM自己设置

②. 暂停时间目标不要太过严苛

![image-20220904122444466](images\image-20220904122444466.png)

## GC日志分析

![image-20220904122530837](images\image-20220904122530837.png)

打开GC日志

-verbose:GC

这个只会显示堆中的GC变化如下：

![image-20220904122704718](images\image-20220904122704718.png)

参数解析

![image-20220904122723966](images\image-20220904122723966.png)

-verbose:GC -xx:PrintGCDetails

输出内容如下

![image-20220904122905118](images\image-20220904122905118.png)

参数解析

![image-20220904122939069](images\image-20220904122939069.png)

如果把GC输出到日志

![image-20220904123042117](images\image-20220904123042117.png)

日志说明补充

![image-20220904123130912](images\image-20220904123130912.png)

![image-20220904123157592](images\image-20220904123157592.png)

![image-20220904123250542](images\image-20220904123250542.png)

![image-20220904123316796](images\image-20220904123316796.png)

![image-20220904123342748](images\image-20220904123342748.png)
