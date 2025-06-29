# 一 hibernate简介

## 什么是hibernate

一个框架

一个 Java 领域的**持久化**框架

一个 **ORM** **框架**

### 对象的持久化

狭义的理解，“持久化”仅仅指把对象永久保存到数据库中

广义的理解，“持久化”包括和数据库相关的各种操作：

​	–保存：把对象永久保存到数据库中。

​	–更新：更新数据库中对象(记录)的状态。

​	–删除：从数据库中删除一个对象。

​	–查询：根据特定的查询条件，把符合查询条件的一个或多个对象从数据库加载到内存中。

​	–加载：根据特定的**OID**（为了在系统中能够找到所需对象，需要为每一个对象分配一个唯一的标识号。在关系数据库中称之为主键，而在对象术语中，则叫做对象标识Object identifier-OID，把一个对象从数据库加载到内存中。

### ORM

ORM(Object/Relation **Mapping**): **对象**/关系映射

​	–ORM 主要解决对象-关系的映射

![image-20210515101951262](images\image-20210515101951262.png)

​	–ORM的思想：将关系数据库中表中的记录映射成为对象，以对象的形式展现，**程序员可以把对数据库的操作转化为对对象的操作**。

​	–ORM 采用**元数据**来描述对象-关系映射细节, 元数据通常采用 XML 格式, 并且存放在专门的对象-关系映射文件中.

![image-20210515102041630](images\image-20210515102041630.png)

## 流行的ORM框架

#### **Hibernate:**

​	–非常优秀、成熟的 ORM 框架。

​	–完成对象的持久化操作

​	–Hibernate 允许开发者**采用面向对象的方式**来操作关系数据库。

​	–消除那些针对特定数据库厂商的 SQL 代码

#### myBatis：

​	–相比 Hibernate 灵活高，运行速度快

​	–开发速度慢，不支持纯粹的面向对象操作，需熟悉sql语句，并且熟练使用sql语句优化功能

## Hibernate 与 Jdbc 代码对比

![image-20210515102224887](images\image-20210515102224887.png)

## 准备 Hibernate 环境

![image-20210515102303796](images\image-20210515102303796.png)

# 二 Hibernate开发步骤

![image-20210515102347563](images\image-20210515102347563.png)

## 创建持久化 Java 类

**提供一个无参的构造器**:使Hibernate可以使用Constructor.newInstance() 来实例化持久化类

**提供一个标识属性**(identifier property): 通常映射为数据库表的主键字段. 如果没有该属性，一些功能将不起作用，如：Session.saveOrUpdate()

**为类的持久化类字段声明访问方法**(get/set): Hibernate对JavaBeans 风格的属性实行持久化。

**使用非** **final** **类**: 在运行时生成代理是 Hibernate 的一个重要的功能. 如果持久化类没有实现任何接口, Hibnernate 使用 CGLIB 生成代理. 如果使用的是 final 类, 则无法生成 CGLIB 代理.

**重写** **eqauls** **和** **hashCode** **方法**: 如果需要把持久化类的实例放到 Set 中(当需要进行关联映射时), 则应该重写这两个方法

Hibernate 不要求持久化类继承任何父类或实现接口，这可以保证代码不被污染。这就是Hibernate被称为低侵入式设计的原因



## 创建对象-关系映射文件

#### 创建数据库

```sql
CREATE DATABASE hibernate;
USE hibernate;
CREATE TABLE `user` (
  `id` int(32) PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(20),
  `age` int(4),
  `gender` varchar(4),
)
```

Hibernate 采用 XML 格式的文件来指定对象和关系数据之间的映射. 在运行时 Hibernate 将根据这个映射文件来生成各种 SQL 语句

映射文件的扩展名为 .hbm.xml

实体类 User 目前还不具备持久化操作的能力，为了使该类具备这种能力，需要通知 Hibernate 框架将 User 实体类映射到数据库的某一张表中，以及类中的哪个属性对应数据表的哪个字段，这些都需要在映射文件中配置。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE hibernate-mapping PUBLIC "-//Hibernate/Hibernate Mapping DTD 3.0//EN"
        "http://hibernate.sourceforge.net/hibernate-mapping-3.0.dtd">
<hibernate-mapping>
    <!-- name代表的是类名，table代表的是表名 -->
    <class name="com.harry.bean.User" table="user">
        <!-- name代表的是User类中的id属性，column代表的是user表中的主键id -->
        <id name="id" column="id">
            <!-- 主键生成策略 -->
            <generator class="native" />
        </id>
        <!-- 其他属性使用property标签映射 -->
        <property name="name" column="name" type="java.lang.String" />
        <property name="age" type="integer" column="age" />
        <property name="gender" type="java.lang.String" column="gender" />
    </class>
</hibernate-mapping>
```

## 创建 Hibernate 配置文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://hibernate.sourceforge.net/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>

        <!-- 配置连接数据库的基本信息 -->
        <property name="connection.username">root</property>
        <property name="connection.password">123456</property>
        <property name="connection.driver_class">com.mysql.jdbc.Driver</property>
        <property name="connection.url">jdbc:mysql://192.168.31.70:3306/hibernate</property>

        <!-- 配置 hibernate 的基本信息 -->
        <!-- hibernate 所使用的数据库方言 -->
        <property name="dialect">org.hibernate.dialect.MySQLInnoDBDialect</property>

        <!-- 执行操作时是否在控制台打印 SQL -->
        <property name="show_sql">true</property>

        <!-- 是否对 SQL 进行格式化 -->
        <property name="format_sql">true</property>

        <!-- 指定自动生成数据表的策略 -->
        <property name="hbm2ddl.auto">update</property>

        <!-- 指定关联的 .hbm.xml 文件 -->
        <mapping resource="com/harry/bean/User.hbm.xml"/>

    </session-factory>

</hibernate-configuration>

```

## 通过 Hibernate API 编写访问数据库的代码

```java
public class UserTest {
    @Test
    public void testUserAdd(){
        // 1.创建Configuration对象并加载hibernate.cfg.xml配置文件
        Configuration config = new Configuration().configure();
        // 2.创建sessionFactory
        ServiceRegistry serviceRegistry = new ServiceRegistryBuilder().applySettings(config.getProperties()).buildServiceRegistry();
        SessionFactory sessionFactory = config.buildSessionFactory(serviceRegistry);
        // 4.得到一个Session
        Session session = sessionFactory.openSession();
        // 5.开启事务
        Transaction transaction = session.beginTransaction();
        // 6.执行持久化操作
        User user = new User();
        user.setName("zhangsan");
        user.setAge(21);
        user.setGender("男");
        // 将对象保存到表中
        session.save(user);
        // 7.提交事务
        transaction.commit();
        // 8.关闭资源
        session.close();
        sessionFactory.close();

    }
}
```

# 三 Hibernate组件

主要涉及四个接口的使用，分别为 Configuration 接口、SessionFactory 接口、Session 接口和 Transaction 接口，除了这四个接口以外，其常用接口还有 Query 和 Criteria 等

Hibernate 在运行时的执行流程如图

![Hibernate的执行流程](images\5-1Z624091544327.gif)

## Configuration 类

Configuration 类负责管理 Hibernate 的配置信息。包括如下内容：

​	–Hibernate 运行的底层信息：数据库的URL、用户名、密码、JDBC驱动类，数据库Dialect,数据库连接池等（对应 **hibernate.cfg.xml** 文件）。

​	–持久化类与数据表的映射关系（*.**hbm.xml** 文件）

创建 Configuration 的两种方式

​	–属性文件（hibernate.**properties**）:

​		•**Configuration** **cfg** **= new Configuration();**

​	–Xml文件（hibernate.cfg.**xml**）

​		•**Configuration** **cfg** **= new Configuration().configure();**

​	–Configuration 的 configure 方法还支持带参数的访问：

​		•**File** **file** **= new File(“simpleit.xml”);**

​		•**Configuration** **cfg** **= new Configuration().configure(file);**

## SessionFactory 接口

针对单个数据库映射关系经过编译后的内存镜像，是线程安全的。

SessionFactory 对象一旦构造完毕，即被赋予特定的配置信息

SessionFactory是生成Session的工厂

构造 SessionFactory 很消耗资源，一般情况下一个应用中只初始化一个 SessionFactory 对象。

Hibernate4 新增了一个 ServiceRegistry 接口，所有基于 Hibernate 的配置或者服务都必须统一向这个 ServiceRegistry 注册后才能生效

Hibernate4 中创建 SessionFactory 的步骤

![image-20210515113540252](images\image-20210515113540252.png)

## Session 接口

Session 是应用程序与数据库之间交互操作的一个**单线程对象**，是 Hibernate 运作的中心，所有持久化对象必须在 session 的管理下才可以进行持久化操作。此对象的生命周期很短。Session 对象有一个一级缓存，显式执行 flush 之前，所有的持久层操作的数据都缓存在 session 对象处。**相当于** **JDBC** **中的** **Connection**。

持久化类与 Session 关联起来后就具有了持久化的能力。

Session 类的方法：

​	–取得持久化对象的方法： get() load()

​	–持久化对象都得保存，更新和删除：save(),update(),saveOrUpdate(),delete()

​	–开启事务: beginTransaction().

​	–管理 Session 的方法：isOpen(),flush(), clear(), evict(), close()等

## Transaction(事务)

代表一次原子操作，它具有数据库事务的概念。所有持久层都应该在事务管理下进行，即使是只读操作。

 **Transaction** **tx** **=** **session.beginTransaction**();

常用方法:

​	–commit():提交相关联的session实例

​	–rollback():撤销事务操作

​	–wasCommitted():检查事务是否提交

## Hibernate 配置文件的两个配置项

hbm2ddl.auto*：*该属性可帮助程序员实现正向工程, 即由 java 代码生成数据库脚本, 进而生成具体的表结构. 。取值 create | update | create-drop | validate

​	–create : 会根据 .hbm.xml 文件来生成数据表, 但是每次运行都会删除上一次的表 ,重新生成表, 哪怕二次没有任何改变

​	–create-drop : 会根据 .hbm.xml 文件生成表,但是SessionFactory一关闭, 表就自动删除

​	–update : **最常用的属性值**，也会根据 .hbm.xml 文件生成表, 但若 .hbm.xml 文件和数据库中对应的数据表的表结构不同, Hiberante 将更新数据表结构，但不会删除已有的行和列

​	–validate : 会和数据库中的表进行比较, 若 .hbm.xml 文件中的列在数据表中不存在，则抛出异常

format_sql：是否将 SQL 转化为格式良好的 SQL . 取值 true | false

# 四 通过 Session 操纵对象

## Session 概述

Session 接口是 Hibernate 向应用程序提供的操纵数据库的最主要的接口, 它**提供了基本的保存**,加载**Java** **对象的方法**.

**Session** **具有一个缓存**, **位于缓存中的对象称为持久化对象**,**它和数据库中的相关记录对应**. Session 能够在某些时间点, 按照缓存中对象的变化来执行相关的 SQL 语句, 来同步更新数据库, 这一过程被称为刷新缓存(flush)

**站在持久化的角度**, Hibernate 把对象分为 **4** **种状态**: 持久化状态, 临时状态, 游离状态, 删除状态. Session 的特定方法能使对象从一个状态转换到另一个状态.

## Session 缓存

在 Session 接口的实现中包含一系列的 Java 集合, 这些 Java 集合构成了 Session 缓存. 只要 Session 实例没有结束生命周期, 且没有清理缓存，则存放在它缓存中的对象也不会结束生命周期

Session 缓存可减少 Hibernate 应用程序访问数据库的频率。

![image-20210515114105286](images\image-20210515114105286.png)

![image-20210515114121442](images\image-20210515114121442.png)

### flush 缓存

flush：Session 按照缓存中对象的属性变化来同步更新数据库

默认情况下 Session 在以下时间点刷新缓存：

​	–显式调用 **Session** **的** **flush()** 方法

​	–当应用程序调用 **Transaction** **的** **commit**（）方法的时, 该方法先 flush ，然后在向数据库提交事务

​	–当应用程序执行一些查询(HQL, Criteria)操作时，如果缓存中持久化对象的属性已经发生了变化，会先 flush 缓存，以保证查询结果能够反映持久化对象的最新状态

flush 缓存的例外情况: 如果对象使用 native 生成器生成 OID, 那么当调用 Session 的 save() 方法保存对象时, 会立即执行向数据库插入该实体的 insert 语句.

commit() 和 flush() 方法的区别：flush 执行一系列 sql 语句，但不提交事务；commit 方法先调用flush() 方法，然后提交事务. 意味着提交事务意味着对数据库操作永久保存下来。


```java
/**
 * flush: 使数据表中的记录和 Session 缓存中的对象的状态保持一致. 为了保持一致, 则可能会发送对应的 SQL 语句.
 * 1. 在 Transaction 的 commit() 方法中: 先调用 session 的 flush 方法, 再提交事务
 * 2. flush() 方法会可能会发送 SQL 语句, 但不会提交事务. 
 * 3. 注意: 在未提交事务或显式的调用 session.flush() 方法之前, 也有可能会进行 flush() 操作.
 * 1). 执行 HQL 或 QBC 查询, 会先进行 flush() 操作, 以得到数据表的最新的记录
 * 2). 若记录的 ID 是由底层数据库使用自增的方式生成的, 则在调用 save() 方法时, 就会立即发送 INSERT 语句. 
 * 因为 save 方法后, 必须保证对象的 ID 是存在的!
 */
@Test
public void testSessionFlush2(){
	News news = new News("Java", "SUN", new Date());
	session.save(news);
}
```
## Hibernate 主键生成策略

![image-20210515114532527](images\image-20210515114532527.png)

## 设定刷新缓存的时间点

若希望改变 flush 的默认时间点, 可以通过 Session 的 setFlushMode() 方法显式设定 flush 的时间点

![image-20210515114655933](images\image-20210515114655933.png)

## 数据库的隔离级别

对于同时运行的多个事务, 当这些事务访问数据库中相同的数据时, 如果没有采取必要的隔离机制, 就会导致各种并发问题:

​	–**脏读**: 对于两个事物 T1, T2, T1 读取了已经被 T2 更新但还**没有被提交**的字段. 之后, 若 T2 回滚, T1读取的内容就是临时且无效的.

​	–**不可重复读**: 对于两个事物 T1, T2, T1 读取了一个字段, 然后 T2 **更新**了该字段. 之后, T1再次读取同一个字段, 值就不同了.

​	–**幻读**: 对于两个事物 T1, T2, T1 从一个表中读取了一个字段, 然后 T2 在该表中**插入**了一些新的行. 之后, 如果 T1 再次读取同一个表, 就会多出几行.

数据库事务的隔离性: 数据库系统必须具有隔离并发运行各个事务的能力, 使它们不会相互影响, 避免各种并发问题.

一个事务与其他事务隔离的程度称为隔离级别. 数据库规定了多种事务隔离级别, 不同隔离级别对应不同的干扰程度, 隔离级别越高, 数据一致性就越好, 但并发性越弱

数据库提供的 4 种事务隔离级别:

![image-20210515114758586](images\image-20210515114758586.png)

Oracle 支持的 2 种事务隔离级别：**READ COMMITED**, SERIALIZABLE. Oracle 默认的事务隔离级别为: READ COMMITED 

Mysql 支持 4 中事务隔离级别. Mysql 默认的事务隔离级别为: REPEATABLE READ

### 在 MySql 中设置隔离级别

每启动一个 mysql 程序, 就会获得一个单独的数据库连接. 每个数据库连接都有一个全局变量 @@tx_isolation, 表示当前的事务隔离级别. MySQL 默认的隔离级别为 Repeatable Read

查看当前的隔离级别: SELECT @@tx_isolation;

设置当前 mySQL 连接的隔离级别: 

​	–set transaction isolation level read committed;

设置数据库系统的全局的隔离级别:

​	– set **global** transaction isolation level read committed;

### 在 Hibernate 中设置隔离级别

JDBC 数据库连接使用数据库系统默认的隔离级别. 在 Hibernate 的配置文件中可以显式的设置隔离级别. 每一个隔离级别都对应一个整数:

​	–1. READ UNCOMMITED

​	–2. READ COMMITED

​	–4. REPEATABLE READ

​	–8. SERIALIZEABLE

Hibernate 通过为 Hibernate 映射文件指定 hibernate.connection.isolation 属性来设置事务的隔离级别

## 持久化对象的状态

**站在持久化的角度**, Hibernat **把对象分为** **4** **种状态**: 持久化状态, 临时状态, 游离状态, 删除状态. Session 的特定方法能使对象从一个状态转换到另一个状态.

临时对象（Transient）:

​	–在使用代理主键的情况下, **OID** **通常为** **null**

​	–**不处于** **Session** **的缓存中**

​	–**在数据库中没有对应的记录**

持久化对象(也叫”托管”)（Persist）：

​	–**OID** **不为** **null**

​	–**位于** **Session** **缓存中**

​	–若在数据库中已经有和其对应的记录, **持久化对象和数据库中的相关记录对应**

​	–**Session** **在** **flush** **缓存时**, **会根据持久化对象的属性变化** **来同步更新数据库**

​	–**在同一个** **Session** **实例的缓存中**数据库表中的每条记录只对应唯一的持久化对象

删除对象(Removed)

​	–在数据库中没有和其 OID 对应的记录

​	–不再处于 Session 缓存中

​	–一般情况下, 应用程序不该再使用被删除的对象

游离对象(也叫”脱管”) （Detached）：

​	–**OID** **不为** **null**

​	–**不再处于** **Session** **缓存中**

​	–一般情况需下, 游离对象是由持久化对象转变过来的, 因此在数据库中可能还存在与它对应的记录

### 对象的状态转换图

![image-20210515115218096](images\image-20210515115218096.png)

### Session 的 save() 方法

Session 的 save() 方法使一个临时对象转变为持久化对象

Session 的 save() 方法完成以下操作:

​	–**把** **News** **对象加入到** **Session** **缓存中**使它进入持久化状态

​	–**选用映射文件指定的标识符生成器,**为持久化对象分配唯一的 **OID**. 在 使用代理主键的情况下, setId() 方法为 News 对象设置 OID 是无效的.

​	–**计划执行一条** **insert** **语句：在** **flush** 缓存的时候

Hibernate 通过持久化对象的 OID 来维持它和数据库相关记录的对应关系. 当 News 对象处于持久化状态时, **不允许程序随意修改它的** **ID**

**persist()** **和** **save()** **区别**：

​	–当对一个 OID 不为 Null 的对象执行 save() 方法时, 会把该对象以一个新的 oid 保存到数据库中; 但执行 persist() 方法时会抛出一个异常.

```JAVA
/**
* 1. save() 方法
* 1). 使一个临时对象变为持久化对象
* 2). 为对象分配 ID.
* 3). 在 flush 缓存时会发送一条 INSERT 语句.
* 4). 在 save 方法之前的 id 是无效的
* 5). 持久化对象的 ID 是不能被修改的!
*/
@Test
public void testSave(){
    News news = new News();
    news.setTitle("CC");
    news.setAuthor("cc");
    news.setDate(new Date());
    news.setId(100); 

    System.out.println(news);
    session.save(news);
    System.out.println(news);
    //		news.setId(101); 
}
```

### Session 的 get() 和 load() 方法

都可以根据跟定的 OID 从数据库中加载一个持久化对象

区别:

​	–当数据库中不存在与 OID 对应的记录时, load() 方法抛出 ObjectNotFoundException 异常, 而 get() 方法返回 null

​	–两者采用不同的**延迟检索策略：*load*方法支持延迟加载策略。而** **get** **不支持。**

### Session 的 update() 方法

Session 的 update() 方法使一个游离对象转变为持久化对象, 并且计划执行一条 update 语句.

若希望 Session 仅当修改了 News 对象的属性时, 才执行 update() 语句, 可以把映射文件中 <class> 元素的 **select-before-update** 设为 true. 该属性的默认值为 false

**当** **update()** **方法关联一个游离对象时**, **如果在** **Session** **的缓存中已经存在相同** **OID** **的持久化对象** **会抛出异常**

当 update() 方法关联一个游离对象时, 如果在数据库中不存在相应的记录, 也会抛出异常.

```JAVA

/**
	 * get VS load:
	 * 
	 * 1. 执行 get 方法: 会立即加载对象. 
	 *    执行 load 方法, 若不适用该对象, 则不会立即执行查询操作, 而返回一个代理对象
	 *    
	 *    get 是 立即检索, load 是延迟检索. 
	 * 
	 * 2. load 方法可能会抛出 LazyInitializationException 异常: 在需要初始化
	 * 代理对象之前已经关闭了 Session
	 * 
	 * 3. 若数据表中没有对应的记录, Session 也没有被关闭.  
	 *    get 返回 null
	 *    load 若不使用该对象的任何属性, 没问题; 若需要初始化了, 抛出异常.  
 */
@Test
public void testLoad(){
    News news = (News) session.load(News.class, 10);
    System.out.println(news.getClass().getName()); 
    //		session.close();
    //		System.out.println(news); 
}
```

### Session 的 saveOrUpdate() 方法

Session 的 saveOrUpdate() 方法同时包含了 save() 与 update() 方法的功能

![image-20210515115853846](images\image-20210515115853846.png)

判定对象为临时对象的标准

​	–**Java** **对象的** **OID** **为** **null**

​	–映射文件中为 <id> 设置了 **unsaved-value**  属性, 并且 Java 对象的 OID 取值与这个 unsaved-value 属性值匹配

### Session 的 delete() 方法

Session 的 delete() 方法既可以删除一个游离对象, 也可以删除一个持久化对象

Session 的 delete() 方法处理过程

​	–计划执行一条 delete 语句

​	–把对象从 Session 缓存中删除, 该对象进入删除状态.

Hibernate 的 cfg.xml 配置文件中有一个 

**hibernate.use_identifier_rollback** 属性, 其默认值为 false, 若把它设为 true, 将改变 delete() 方法的运行行为: delete() 方法会把持久化对象或游离对象的 OID 设置为 null, 使它们变为临时对象

## 通过 Hibernate 调用存储过程

Work 接口: 直接通过 JDBC API 来访问数据库的操作

![image-20210515120046909](images\image-20210515120046909.png)

Session 的 doWork(Work) 方法用于执行 Work 对象指定的操作, 即调用 Work 对象的 execute() 方法. Session 会把当前使用的数据库连接传递给 execute() 方法.

![image-20210515120107516](images\image-20210515120107516.png)

# 五 Hibernate 的配置文件

## **Hibernate**配置文件

Hibernate 配置文件主要用于配置数据库连接和 Hibernate 运行时所需的各种属性

每个 Hibernate 配置文件对应一个 Configuration 对象

Hibernate配置文件可以有两种格式:

​	–hibernate.properties

​	–**hibernate.cfg.xml** 

## hibernate.cfg.xml的常用属性

### JDBC 连接属性

​	–connection.url：数据库URL

​	–connection.username：数据库用户名

​	–connection.password：数据库用户密码

​	–connection.driver_class：数据库JDBC驱动

​	–**dialect**：配置数据库的方言，根据底层的数据库不同产生不同的 sql 语句，Hibernate 会针对数据库的特性在访问时进行优化

### C3P0 数据库连接池属性

​	–hibernate.c3p0.max_size: 数据库连接池的最大连接数

​	–hibernate.c3p0.min_size: 数据库连接池的最小连接数

​	–hibernate.c3p0.timeout:  数据库连接池中连接对象在多长时间没有使用过后，就应该被销毁

​	–hibernate.c3p0.max_statements: 缓存 Statement 对象的数量

​	–hibernate.c3p0.idle_test_period: 表示连接池**检测线程**多长时间检测一次池内的所有链接对象是否超时. 连接池本身不会把自己从连接池中移除，而是专门有一个线程按照一定的时间间隔来做这件事，这个线程通过比较连接对象最后一次被使用时间和当前时间的时间差来和 timeout 做对比，进而决定是否销毁这个连接对象。

​	–hibernate.c3p0.acquire_increment: 当数据库连接池中的连接耗尽时, 同一时刻获取多少个数据库连接

```xml
<!-- C3P0连接池设定 -->
<!-- 使用 C3P0连接池配置连接池提供的供应商 -->
<property name="connection.provider_class">
    org.hibernate.connection.c3p0ConnectionProvider
</property>
<!--在连接池中可用的数据库连接的最少数目 -->
<property name="c3p0.min_size">5 </property>
<!--在连接池中所有数据库连接的最大数目 -->
<property name="c3p0.max_sizen">20 </property>
<!--设定数据库连接的过期时间，以ms为单位，如果连接池中的某个数据库连接空闲状态的时间 超过timeout时间，则会从连接池中清除 -->
<property name="c3p0.timeout">120 </property>
<!--每3000s检查所有连接池中的空闲连接以s为单位 -->
<property name="c3p0.idle_test_period">3000 </property>
```

### hibernate.cfg.xml的常用属性

​	–show_sql：是否将运行期生成的SQL输出到日志以供调试。取值 true | false 

​	–format_sql：是否将 SQL 转化为格式良好的 SQL . 取值 true | false

​	–hbm2ddl.auto：在启动和停止时自动地创建，更新或删除数据库模式。取值 create | update | create-drop | validate

​	–hibernate.jdbc.fetch_size

​	–hibernate.jdbc.batch_size

### **jdbc.fetch_size** **和** jdbc.batch_size

hibernate.jdbc.fetch_size：实质是调用 Statement.setFetchSize() 方法**设定** **JDBC** **的** **Statement** **读取数据的时候每次从数据库中取出的记录条数**。

​	–例如一次查询1万条记录，对于Oracle的JDBC驱动来说，是不会 1 次性把1万条取出来的，而只会取出 fetchSize 条数，当结果集遍历完了这些记录以后，再去数据库取 fetchSize 条数据。因此大大节省了无谓的内存消耗。Fetch Size设的越大，读数据库的次数越少，速度越快；Fetch Size越小，读数据库的次数越多，速度越慢。Oracle数据库的JDBC驱动默认的Fetch Size = 10，是一个保守的设定，根据测试，当Fetch Size=50时，性能会提升1倍之多，当 f**etchSize**=100，性能还能继续提升20%，Fetch Size继续增大，性能提升的就不显著了。并不是所有的数据库都支持Fetch Size特性，例如MySQL就不支持

hibernate.jdbc.batch_size：**设定对数据库进行批量删除，批量更新和批量插入的时候的批次大小**，类似于设置缓冲区大小的意思。batchSize 越大，批量操作时向数据库发送sql的次数越少，速度就越快。

​	–测试结果是当Batch Size=0的时候，使用Hibernate对Oracle数据库删除1万条记录需要25秒，Batch Size = 50的时候，删除仅仅需要5秒！Oracle数据库 b**atchSize**=30的时候比较合适。

# 六 对象关系映射文件

## POJO 类和数据库的映射文件*.hbm.xml

POJO 类和关系数据库之间的映射可以用一个XML文档来定义。

通过 POJO 类的数据库映射文件，Hibernate可以理解持久化类和数据表之间的对应关系，也可以理解持久化类属性与数据库表列之间的对应关系

在运行时 Hibernate 将根据这个映射文件来生成各种 SQL 语句

映射文件的扩展名为 .hbm.xml

## 映射文件说明

### hibernate-mapping

​	–类层次：class

​		•主键：id

​		•基本类型:property

​		•实体引用类: many-to-one | one-to-one

​		•集合:set | list | map | array

​			–one-to-many

​			–many-to-many

​		•子类:subclass | joined-subclass

​		•其它:component | any 等

​	–查询语句:query（用来放置查询语句，便于对数据库查询的统一管理和优化）

每个Hibernate-mapping中可以同时定义多个类. 但更推荐为每个类都创建一个单独的映射文件

![image-20210515120840880](images\image-20210515120840880.png)

### class

![image-20210515120928168](images\image-20210515120928168.png)

## 映射对象标识符

Hibernate 使用对象标识符(OID) 来建立内存中的对象和数据库表中记录的对应关系. 对象的 OID 和数据表的主键对应. Hibernate 通过标识符生成器来为主键赋值

Hibernate 推荐在数据表中使用代理主键, 即不具备业务含义的字段. 代理主键通常为整数类型, 因为整数类型比字符串类型要节省更多的数据库空间.

在对象-关系映射文件中, <id> 元素用来设置对象标识符. <generator> 子元素用来设定标识符生成器.

Hibernate 提供了标识符生成器接口: IdentifierGenerator, 并提供了各种内置实现

### id

![image-20210515121059664](images\image-20210515121059664.png)

### Property

![image-20210515121218148](images\image-20210515121218148.png)

![image-20210515121255513](images\image-20210515121255513.png)

## **Java** **类型**, Hibernate映射类型及 **SQL** **类型之间的对应关系**

![image-20210515121351135](images\image-20210515121351135.png)

![image-20210515121424972](images\image-20210515121424972.png)

### Java 时间和日期类型的 Hibernate 映射

在 Java 中, 代表时间和日期的类型包括: java.util.Date 和 java.util.Calendar. 此外, 在 JDBC API 中还提供了 3 个扩展了 java.util.Date 类的子类: java.sql.Date, java.sql.Time 和 java.sql.Timestamp, 这三个类分别和标准 SQL 类型中的 DATE, TIME 和 TIMESTAMP 类型对应

在标准 SQL 中, DATE 类型表示日期, TIME 类型表示时间, TIMESTAMP 类型表示时间戳, 同时包含日期和时间信息.

![image-20210515121510121](images\image-20210515121510121.png)

以下情况下必须显式指定 Hibernate 映射类型

​	–一个 Java 类型可能对应多个 Hibernate 映射类型. 例如: 如果持久化类的属性为 java.util.Date 类型, 对应的 Hibernate 映射类型可以是 date, time 或 timestamp. 此时必须根据对应的数据表的字段的 SQL 类型, 来确定 Hibernate 映射类型. 如果字段为 DATE 类型, 那么 Hibernate 映射类型为 date; 如果字段为 TIME 类型, 那么 Hibernate 映射类型为 time; 如果字段为 TIMESTATMP 类型, 那么 Hibernate 映射类型为 timestamp.

### 映射组成关系

Hibernate 把持久化类的属性分为两种:

​	–值(value)类型: **没有** **OID**, **不能被单独持久化**, **生命周期依赖于所属的持久化类的对象的生命周期**

​	–实体(entity)类型: 有 OID, 可以被单独持久化, 有独立的生命周期

显然无法直接用 property 映射 pay 属性

Hibernate 使用 <component> 元素来映射组成关系, 该元素表名 pay 属性是 Worker 类一个组成部分, 在 Hibernate 中称之为**组件**

![image-20210515134613802](images\image-20210515134613802.png)

# 七 映射一对多关联关系

## 一对多关联关系

在领域模型中, 类与类之间最普遍的关系就是关联关系.

在 UML 中, 关联是有方向的.

​	–以 Customer 和 Order 为例： 一个用户能发出多个订单, 而一个订单只能属于一个客户. 从 Order 到 Customer 的关联是多对一关联; 而从 Customer 到 Order 是一对多关联

​	–单向关联

## 单向 n-1

单向 n-1 关联只需从 n 的一端可以访问 1 的一端

域模型: 从 Order 到 Customer 的多对一单向关联需要在Order 类中定义一个 Customer 属性, 而在 Customer 类中无需定义存放 Order 对象的集合属性

显然无法直接用 property 映射 customer 属性

Hibernate 使用 <many-to-one> 元素来映射多对一关联关系

```xml
<?xml version="1.0"?>
<!DOCTYPE hibernate-mapping PUBLIC "-//Hibernate/Hibernate Mapping DTD 3.0//EN"
        "http://hibernate.sourceforge.net/hibernate-mapping-3.0.dtd">

<hibernate-mapping package="com.harry.one2many">

    <class name="Order" table="ORDERS">

        <id name="orderId" type="java.lang.Integer">
            <column name="ORDER_ID" />
            <generator class="native" />
        </id>

        <property name="orderName" type="java.lang.String">
            <column name="ORDER_NAME" />
        </property>

        <!--
            映射多对一的关联关系。 使用 many-to-one 来映射多对一的关联关系
            name: 多这一端关联的一那一端的属性的名字
            class: 一那一端的属性对应的类名
            column: 一那一端在多的一端对应的数据表中的外键的名字
        -->
        <many-to-one name="customer" class="Customer" column="CUSTOMER_ID"></many-to-one>

    </class>
</hibernate-mapping>
```

## 双向 1-n

双向 1-n 与 双向 n-1 是完全相同的两种情形

双向 1-n 需要在 1 的一端可以访问 n 的一端, 反之依然.

域模型:从 Order 到 Customer 的多对一双向关联需要在Order 类中定义一个 Customer 属性, 而在 Customer 类中需定义存放 Order 对象的集合属性

关系数据模型:ORDERS 表中的 CUSTOMER_ID 参照 CUSTOMER 表的主键

当 Session 从数据库中加载 Java 集合时, 创建的是 Hibernate 内置集合类的实例, 因此**在持久化类中定义集合属性时必须把属性声明为** **Java** **接口类型**

​	–Hibernate 的内置集合类具有集合代理功能, **支持延迟检索策略**

​	–事实上, Hibernate 的内置集合类封装了 JDK 中的集合类, 这使得 Hibernate 能够对缓存中的集合对象进行脏检查, 按照集合对象的状态来同步更新数据库。

在定义集合属性时, 通常把它初始化为集合实现类的一个实例. 这样可以提高程序的健壮性, 避免应用程序访问取值为 null 的集合的方法抛出 NullPointerException

```java
import java.util.Set;

public class Customer {

    private Integer customerId;
    private String customerName;

    /*
     * 1. 声明集合类型时, 需使用接口类型, 因为 hibernate 在获取
     * 集合类型时, 返回的是 Hibernate 内置的集合类型, 而不是 JavaSE 一个标准的
     * 集合实现.
     * 2. 需要把集合进行初始化, 可以防止发生空指针异常
     */
    private Set<Order> orders = new HashSet<>();

    public Integer getCustomerId() {
        return customerId;
    }

    public void setCustomerId(Integer customerId) {
        this.customerId = customerId;
    }

    public String getCustomerName() {
        return customerName;
    }

    public void setCustomerName(String customerName) {
        this.customerName = customerName;
    }

    public Set<Order> getOrders() {
        return orders;
    }

    public void setOrders(Set<Order> orders) {
        this.orders = orders;
    }

}
```

Hibernate 使用 <set> 元素来映射 set 类型的属性

```xml
<?xml version="1.0"?>
<!DOCTYPE hibernate-mapping PUBLIC "-//Hibernate/Hibernate Mapping DTD 3.0//EN"
        "http://hibernate.sourceforge.net/hibernate-mapping-3.0.dtd">

<hibernate-mapping>

    <class name="com.harry.one2many.Customer" table="CUSTOMERS">

        <id name="customerId" type="java.lang.Integer">
            <column name="CUSTOMER_ID" />
            <generator class="native" />
        </id>

        <property name="customerName" type="java.lang.String">
            <column name="CUSTOMER_NAME" />
        </property>
        <!-- 映射 1 对多的那个集合属性 -->
        <!-- set: 映射 set 类型的属性, table: set 中的元素对应的记录放在哪一个数据表中. 该值需要和多对一的多的那个表的名字一致 -->
        <!-- inverse: 指定由哪一方来维护关联关系. 通常设置为 true, 以指定由多的一端来维护关联关系 -->
        <!-- cascade 设定级联操作. 开发时不建议设定该属性. 建议使用手工的方式来处理 -->
        <!-- order-by 在查询时对集合中的元素进行排序, order-by 中使用的是表的字段名, 而不是持久化类的属性名  -->
        <set name="orders" table="ORDERS" inverse="true" order-by="ORDER_NAME DESC">
            <!-- 执行多的表中的外键列的名字 -->
            <key column="CUSTOMER_ID"></key>
            <!-- 指定映射类型 -->
            <one-to-many class="com.harry.one2many.Order"/>
        </set>
    </class>

</hibernate-mapping>
```

![image-20210518194458869](images\image-20210518194458869.png)

### set元素的 inverse 属性

在hibernate中通过对 inverse 属性的来决定是由双向关联的哪一方来维护表和表之间的关系. inverse = false 的为主动方，inverse = true 的为被动方, 由主动方负责维护关联关系

在没有设置 inverse=true 的情况下，父子两边都维护父子 关系 

在 1-n 关系中，将 n 方设为主控方将有助于性能改善(如果要国家元首记住全国人民的名字，不是太可能，但要让全国人民知道国家元首，就容易的多)

在 1-N 关系中，若将 1 方设为主控方

​	–**会额外多出** **update** **语句**。

​	–插入数据时无法同时插入外键列，因而无法为外键列添加非空约束

### cascade 属性

​	在对象 – 关系映射文件中, 用于映射持久化类之间关联关系的元素, <set>, <many-to-one> 和 <one-to-one> 都有一个 cascade 属性, 它用于指定如何操纵与当前对象关联的其他对象.

![image-20210518194710854](images\image-20210518194710854.png)

### 在数据库中对集合排序

<set> 元素有一个 order-by 属性, 如果设置了该属性, 当 Hibernate 通过 select 语句到数据库中检索集合对象时, 利用 order by 子句进行排序

order-by 属性中还可以加入 SQL 函数

```xml
<set name="orders" table="ORDERS" inverse="true" order-by="ORDER_NAME DESC">
    <!-- 执行多的表中的外键列的名字 -->
    <key column="CUSTOMER_ID"></key>
    <!-- 指定映射类型 -->
    <one-to-many class="com.harry.one2many.Order"/>
</set>
```

test

```java
package com.harry.one2many;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import org.hibernate.cfg.Configuration;
import org.hibernate.service.ServiceRegistry;
import org.hibernate.service.ServiceRegistryBuilder;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class HibernateTest {

    private SessionFactory sessionFactory;
    private Session session;
    private Transaction transaction;

    @Before
    public void init(){
        Configuration configuration = new Configuration().configure();
        ServiceRegistry serviceRegistry =
                new ServiceRegistryBuilder().applySettings(configuration.getProperties())
                        .buildServiceRegistry();
        sessionFactory = configuration.buildSessionFactory(serviceRegistry);

        session = sessionFactory.openSession();
        transaction = session.beginTransaction();
    }

    @After
    public void destroy(){
        transaction.commit();
        session.close();
        sessionFactory.close();
    }

    @Test
    public void testCascade(){
        Customer customer = (Customer) session.get(Customer.class, 3);
        customer.getOrders().clear();
    }

    @Test
    public void testDelete(){
        //在不设定级联关系的情况下, 且 1 这一端的对象有 n 的对象在引用, 不能直接删除 1 这一端的对象
        Customer customer = (Customer) session.get(Customer.class, 1);
        session.delete(customer);
    }

    @Test
    public void testUpdat2(){
        Customer customer = (Customer) session.get(Customer.class, 1);
        customer.getOrders().iterator().next().setOrderName("GGG");
    }

    @Test
    public void testUpdate(){
        Order order = (Order) session.get(Order.class, 1);
        order.getCustomer().setCustomerName("AAA");
    }

    @Test
    public void testOne2ManyGet(){
        //1. 对 n 的一端的集合使用延迟加载
        Customer customer = (Customer) session.get(Customer.class, 1);
        System.out.println(customer.getCustomerName());
        //2. 返回的多的一端的集合时 Hibernate 内置的集合类型.
        //该类型具有延迟加载和存放代理对象的功能.
        System.out.println(customer.getOrders().getClass());

        //session.close();
        //3. 可能会抛出 LazyInitializationException 异常

        System.out.println(customer.getOrders().size());

        //4. 再需要使用集合中元素的时候进行初始化.
    }

    @Test
    public void testMany2OneGet(){
        //1. 若查询多的一端的一个对象, 则默认情况下, 只查询了多的一端的对象. 而没有查询关联的
        //1 的那一端的对象!
        Order order = (Order) session.get(Order.class, 1);
        System.out.println(order.getOrderName());

        System.out.println(order.getCustomer().getClass().getName());

        session.close();

        //2. 在需要使用到关联的对象时, 才发送对应的 SQL 语句.
        Customer customer = order.getCustomer();
        System.out.println(customer.getCustomerName());

        //3. 在查询 Customer 对象时, 由多的一端导航到 1 的一端时,
        //若此时 session 已被关闭, 则默认情况下
        //会发生 LazyInitializationException 异常

        //4. 获取 Order 对象时, 默认情况下, 其关联的 Customer 对象是一个代理对象!

    }

    @Test
    public void testMany2OneSave(){
        Customer customer = new Customer();
        customer.setCustomerName("AA");

        Order order1 = new Order();
        order1.setOrderName("ORDER-1");

        Order order2 = new Order();
        order2.setOrderName("ORDER-2");

        //设定关联关系
        order1.setCustomer(customer);
        order2.setCustomer(customer);

        customer.getOrders().add(order1);
        customer.getOrders().add(order2);

        //执行  save 操作: 先插入 Customer, 再插入 Order, 3 条 INSERT, 2 条 UPDATE
        //因为 1 的一端和 n 的一端都维护关联关系. 所以会多出 UPDATE
        //可以在 1 的一端的 set 节点指定 inverse=true, 来使 1 的一端放弃维护关联关系!
        //建议设定 set 的 inverse=true, 建议先插入 1 的一端, 后插入多的一端
        //好处是不会多出 UPDATE 语句
        session.save(customer);

//    session.save(order1);
//    session.save(order2);

        //先插入 Order, 再插入 Cusomer, 3 条 INSERT, 4 条 UPDATE
//    session.save(order1);
//    session.save(order2);
//
//    session.save(customer);
    }
}
```

# 八 映射一对一关联关系

## 基于外键映射的 1-1

对于基于外键的1-1关联，其外键可以存放在任意一边，**在需要存放外键一端，增加**many-to-one**元素**。为many-to-one元素增加unique=“true” 属性来表示为1-1关联

Department

```java
package com.harry.one2one.foreign;

public class Department {

    private Integer deptId;
    private String deptName;

    private Manager mgr;

    public Integer getDeptId() {
        return deptId;
    }

    public void setDeptId(Integer deptId) {
        this.deptId = deptId;
    }

    public String getDeptName() {
        return deptName;
    }

    public void setDeptName(String deptName) {
        this.deptName = deptName;
    }

    public Manager getMgr() {
        return mgr;
    }

    public void setMgr(Manager mgr) {
        this.mgr = mgr;
    }

}
```

Manager

```java
package com.harry.one2one.foreign;

public class Manager {

    private Integer mgrId;
    private String mgrName;

    private Department dept;

    public Integer getMgrId() {
        return mgrId;
    }

    public void setMgrId(Integer mgrId) {
        this.mgrId = mgrId;
    }

    public String getMgrName() {
        return mgrName;
    }

    public void setMgrName(String mgrName) {
        this.mgrName = mgrName;
    }

    public Department getDept() {
        return dept;
    }

    public void setDept(Department dept) {
        this.dept = dept;
    }

}
```

```xml
<?xml version="1.0"?>
<!DOCTYPE hibernate-mapping PUBLIC "-//Hibernate/Hibernate Mapping DTD 3.0//EN"
        "http://hibernate.sourceforge.net/hibernate-mapping-3.0.dtd">
<hibernate-mapping>

    <class name="com.harry.one2one.foreign.Department" table="DEPARTMENTS">

        <id name="deptId" type="java.lang.Integer">
            <column name="DEPT_ID" />
            <generator class="native" />
        </id>

        <property name="deptName" type="java.lang.String">
            <column name="DEPT_NAME" />
        </property>

        <!-- 使用 many-to-one 的方式来映射 1-1 关联关系 -->
        <many-to-one name="mgr" class="com.harry.one2one.foreign.Manager"
                     column="MGR_ID" unique="true"></many-to-one>

    </class>
</hibernate-mapping>
```

另一端需要使用one-to-one元素，该元素使用 **property-ref** 属性指定使用被关联实体主键以外的字段作为关联字段

```xml
<?xml version="1.0"?>
<!DOCTYPE hibernate-mapping PUBLIC "-//Hibernate/Hibernate Mapping DTD 3.0//EN"
        "http://hibernate.sourceforge.net/hibernate-mapping-3.0.dtd">

<hibernate-mapping>

    <class name="com.harry.one2one.foreign.Manager" table="MANAGERS">

        <id name="mgrId" type="java.lang.Integer">
            <column name="MGR_ID" />
            <generator class="native" />
        </id>

        <property name="mgrName" type="java.lang.String">
            <column name="MGR_NAME" />
        </property>

        <!-- 映射 1-1 的关联关系: 在对应的数据表中已经有外键了, 当前持久化类使用 one-to-one 进行映射 -->
        <!--
           没有外键的一端需要使用one-to-one元素，该元素使用 property-ref 属性指定使用被关联实体主键以外的字段作为关联字段
         -->
        <one-to-one name="dept"
                    class="com.harry.one2one.foreign.Department"
                    property-ref="mgr"></one-to-one>
    </class>

</hibernate-mapping>
```

![image-20210519193044178](images\image-20210519193044178.png)

test

```java
public class HibernateTest {

    private SessionFactory sessionFactory;
    private Session session;
    private Transaction transaction;

    @Before
    public void init(){
        Configuration configuration = new Configuration().configure();
        ServiceRegistry serviceRegistry =
                new ServiceRegistryBuilder().applySettings(configuration.getProperties())
                        .buildServiceRegistry();
        sessionFactory = configuration.buildSessionFactory(serviceRegistry);

        session = sessionFactory.openSession();
        transaction = session.beginTransaction();
    }

    @After
    public void destroy(){
        transaction.commit();
        session.close();
        sessionFactory.close();
    }

    @Test
    public void testGet2(){
        //在查询没有外键的实体对象时, 使用的左外连接查询, 一并查询出其关联的对象
        //并已经进行初始化.
        Manager mgr = (Manager) session.get(Manager.class, 1);
        System.out.println(mgr.getMgrName());
        System.out.println(mgr.getDept().getDeptName());
    }

    @Test
    public void testGet(){
        //1. 默认情况下对关联属性使用懒加载
        Department dept = (Department) session.get(Department.class, 1);
        System.out.println(dept.getDeptName());

        //2. 所以会出现懒加载异常的问题.
//    session.close();
//    Manager mgr = dept.getMgr();
//    System.out.println(mgr.getClass());
//    System.out.println(mgr.getMgrName());

        //3. 查询 Manager 对象的连接条件应该是 dept.manager_id = mgr.manager_id
        //而不应该是 dept.dept_id = mgr.manager_id
        Manager mgr = dept.getMgr();
        System.out.println(mgr.getMgrName());


    }

    @Test
    public void testSave(){

        Department department = new Department();
        department.setDeptName("DEPT-BB");

        Manager manager = new Manager();
        manager.setMgrName("MGR-BB");

        //设定关联关系
        department.setMgr(manager);
        manager.setDept(department);

        //保存操作
        //建议先保存没有外键列的那个对象. 这样会减少 UPDATE 语句
        session.save(department);
        session.save(manager);

    }



}
```

## 基于主键映射的 1-1

基于主键的映射策略:指一端的主键生成器使用 foreign 策略,表明根据**”对方”**的主键来生成自己的主键，自己并不能独立生成主键<param> 子元素指定使用当前持久化类的哪个属性作为 “对方”

```xml
<class name="Department" table="DEPARTMENTS">

    <id name="deptId" type="java.lang.Integer">
        <column name="DEPT_ID" />
        <!-- 使用外键的方式来生成当前的主键 -->
        <generator class="foreign">
        	<!-- property 属性指定使用当前持久化类的哪一个属性的主键作为外键 -->
        	<param name="property">mgr</param>
        </generator>
    </id>
```



```xml
<!--  
采用 foreign 主键生成器策略的一端增加 one-to-one 元素映射关联属性,
其 one-to-one 节点还应增加 constrained=true 属性, 以使当前的主键上添加外键约束
-->
<one-to-one name="mgr" class="Manager" constrained="true"></one-to-one>
```

采用foreign主键生成器策略的一端增加 one-to-one 元素映射关联属性，其one-to-one属性还应增加 constrained=“true” 属性；另一端增加one-to-one元素映射关联属性。

**constrained**(约束):指定为当前持久化类对应的数据库表的主键添加一个外键约束，引用被关联的对象(对方)所对应的数据库表主键

# 九 映射多对多关联关系

## 单向 n-n

**n-n** **的关联必须使用连接表**

与 1-n 映射类似，**必须为** **set** **集合元素添加** **key** **子元素，指定** **CATEGORIES_ITEMS** **表中参照** **CATEGORIES** **表的外键为** **CATEGORIY_ID**. 与 1-n 关联映射不同的是，建立 n-n 关联时, 集合中的元素使用 **many-to-many**. many-to-many 子元素的 class 属性指定 items 集合中存放的是 Item 对象, **column** **属性指定** **CATEGORIES_ITEMS** **表中参照** **ITEMS** **表的外键为** **ITEM_ID**

![image-20210519194605466](images\image-20210519194605466.png)

## 双向 n-n

双向 n-n 关联需要**两端都使用集合属性**

双向n-n关联**必须使用连接表**

集合属性应增加 key 子元素用以映射外键列, 集合元素里还应增加many-to-many子元素关联实体类

**在双向** **n-n** **关联的两边都需指定连接表的表名及外键列的列名**. **两个集合元素** **set** **的** **table** **元素的值必须指定，而且必须相同。set元素的两个子元素：key**和**many-to-many** **都必须指定** **column** **属性**，其中，key和 **many-to-many** **分别指定本持久化类和关联类在连接表中的外键列名，因此两边的** **key** **与** **many-to-many** **的column属性交叉相同**。也就是说，一边的set元素的key的 cloumn值为a,many-to-many 的 column 为b；则另一边的 set 元素的 key 的 column 值 b,many-to-many的 column 值为 a. 

**对于双向** **n-n** **关联** 必须把其中一端的 **inverse** **设置为** **true**, 否则两端都维护关联关系可能会造成主键冲突.

![image-20210519195257369](images\image-20210519195257369.png)

category

```java
public class Category {

    private Integer id;
    private String name;

    private Set<Item> items = new HashSet<Item>();

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Set<Item> getItems() {
        return items;
    }

    public void setItems(Set<Item> items) {
        this.items = items;
    }

}
```

Item

```java
public class Item {

    private Integer id;
    private String name;

    private Set<Category> categories = new HashSet<Category>();

    public Integer getId() {
        return id;
    }
    public void setId(Integer id) {
        this.id = id;
    }
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public Set<Category> getCategories() {
        return categories;
    }
    public void setCategories(Set<Category> categories) {
        this.categories = categories;
    }

}
```

```xml
<hibernate-mapping package="com.harry.n2n">

    <class name="Category" table="CATEGORIES">

        <id name="id" type="java.lang.Integer">
            <column name="ID" />
            <generator class="native" />
        </id>

        <property name="name" type="java.lang.String">
            <column name="NAME" />
        </property>

        <!-- table: 指定中间表 -->
        <set name="items" table="CATEGORIES_ITEMS">
            <key>
                <column name="C_ID" />
            </key>
            <!-- 使用 many-to-many 指定多对多的关联关系. column 执行 Set 集合中的持久化类在中间表的外键列的名称  -->
            <many-to-many class="Item" column="I_ID"></many-to-many>
        </set>

    </class>
</hibernate-mapping>
```

```xml
<hibernate-mapping>

    <class name="com.harry.n2n.Item" table="ITEMS">

        <id name="id" type="java.lang.Integer">
            <column name="ID" />
            <generator class="native" />
        </id>

        <property name="name" type="java.lang.String">
            <column name="NAME" />
        </property>

        <set name="categories" table="CATEGORIES_ITEMS" inverse="true">
            <key column="I_ID"></key>
            <many-to-many class="com.harry.n2n.Category" column="C_ID"></many-to-many>
        </set>

    </class>
</hibernate-mapping>
```

test

```java
public class HibernateTest {

    private SessionFactory sessionFactory;
    private Session session;
    private Transaction transaction;

    @Before
    public void init(){
        Configuration configuration = new Configuration().configure();
        ServiceRegistry serviceRegistry =
                new ServiceRegistryBuilder().applySettings(configuration.getProperties())
                        .buildServiceRegistry();
        sessionFactory = configuration.buildSessionFactory(serviceRegistry);

        session = sessionFactory.openSession();
        transaction = session.beginTransaction();
    }

    @After
    public void destroy(){
        transaction.commit();
        session.close();
        sessionFactory.close();
    }

    @Test
    public void testGet(){
        Category category = (Category) session.get(Category.class, 1);
        System.out.println(category.getName());

        //需要连接中间表
        Set<Item> items = category.getItems();
        System.out.println(items.size());
    }

    @Test
    public void testSave(){
        Category category1 = new Category();
        category1.setName("C-AA");

        Category category2 = new Category();
        category2.setName("C-BB");

        Item item1 = new Item();
        item1.setName("I-AA");

        Item item2 = new Item();
        item2.setName("I-BB");

        //设定关联关系
        category1.getItems().add(item1);
        category1.getItems().add(item2);

        category2.getItems().add(item1);
        category2.getItems().add(item2);

        item1.getCategories().add(category1);
        item1.getCategories().add(category2);

        item2.getCategories().add(category1);
        item2.getCategories().add(category2);

        //执行保存操作
        session.save(category1);
        session.save(category2);

        session.save(item1);
        session.save(item2);
    }

}
```

# 十 Hibernate 检索策略

检索数据时的 2 个问题：

​	–不浪费内存：当 Hibernate 从数据库中加载 Customer 对象时, 如果同时加载所有关联的 Order 对象, 而程序实际上仅仅需要访问 Customer 对象, 那么这些关联的 Order 对象就白白浪费了许多内存.

​	–更高的查询效率：发送尽可能少的 SQL 语句

## 类级别的检索策略

类级别可选的检索策略包括立即检索和延迟检索, 默认为延迟检索

​	–**立即检索**：立即加载检索方法指定的对象

​	–**延迟检索： **延迟加载检索方法指定的对象。在使用具体的属性时，再进行加载

**类级别的检索策略可以通过** **元素的** **lazy** **属性进行设置**

如果程序加载一个对象的目的是为了访问它的属性, 可以采取立即检索.

如果程序加载一个持久化对象的目的是仅仅为了获得它的引用, 可以采用延迟检索。注意出现懒加载异常！

**无论元素的 **lazy **属性是** **true** **还是** **false, Session** **的** **get()** **方法及** **Query** **的** **list()** 方法在类级别总是使用立即检索策略

若 <class> 元素的 lazy 属性为 true 或取默认值, Session 的 **load()** 方法不会执行查询数据表的 SELECT 语句, 仅返回代理类对象的实例, 该代理类实例有如下特征:

​	–由 Hibernate 在运行时采用 CGLIB 工具动态生成

​	–Hibernate 创建代理类实例时, **仅初始化其** **OID** **属性**

​	–在应用程序第一次访问代理类实例的非 OID 属性时, Hibernate 会初始化代理类实例

## 一对多和多对多的检索策略

在映射文件中, 用 <set> 元素来配置一对多关联及多对多关联关系. <set> 元素有 lazy 和 fetch 属性

​	–**lazy**: **主要决定** **orders** **集合被初始化的时机**. 即到底是在加载 Customer 对象时就被初始化, 还是在程序访问 orders 集合时被初始化

​	–**fetch**: **取值为 “**select” **或 “**subselect” **时, **决定初始化 **orders** **的查询语句的形式; **若取值为”join”, **则决定** **orders** **集合被初始化的时机**

​	–**若把** **fetch** **设置为 “join”, lazy 属性将被忽略**

​	–<set> 元素的 batch-size 属性：用来为延迟检索策略或立即检索策略设定批量检索的数量. 批量检索能减少 SELECT 语句的数目, 提高延迟检索或立即检索的运行性能.

### set元素的 lazy 和 fetch 属性

![image-20210519200820154](images\image-20210519200820154.png)

## 延迟检索和增强延迟检索

在延迟检索(lazy 属性值为 true) 集合属性时, Hibernate 在以下情况下初始化集合代理类实例 

​	–应用程序第一次访问集合属性: iterator(), size(), isEmpty(), contains() 等方法

​	–通过 Hibernate.initialize() 静态方法显式初始化

增强延迟检索(lazy 属性为 extra): 与 lazy=“true” 类似. 主要区别是**增强延迟检索策略能进一步延迟** **Customer** **对象的** **orders** **集合代理实例的初始化时机**：

​	–当程序第一次访问 orders 属性的 iterator() 方法时, 会导致 orders 集合代理类实例的初始化

​	–当程序第一次访问 order 属性的 size(), contains() 和 isEmpty() 方法时, Hibernate 不会初始化 orders 集合类的实例, 仅通过特定的 select 语句查询必要的信息, 不会检索所有的 Order 对象

## 多对一和一对一关联的检索策略

和 <set> 一样, <many-to-one> 元素也有一个 lazy 属性和 fetch 属性.

![image-20210519201320001](images\image-20210519201320001.png)

–**若** **fetch** **属性设为** **join,** **那么** **lazy** **属性被忽略**

–迫切左外连接检索策略的优点在于比立即检索策略使用的 SELECT 语句更少.

–无代理延迟检索需要增强持久化类的字节码才能实现

**Query** **的** **list** **方法会忽略映射文件配置的迫切左外连接检索策略**, **而采用延迟检索策略**

如果在关联级别使用了延迟加载或立即加载检索策略, 可以**设定批量检索的大小**, 以帮助提高延迟检索或立即检索的运行性能.

Hibernate 允许在应用程序中覆盖映射文件中设定的检索策略

## 检索策略小结

类级别和关联级别可选的检索策略及默认的检索策略

![image-20210519201427125](images\image-20210519201427125.png)

3 种检索策略的运行机制

![image-20210519201452933](images\image-20210519201452933.png)

映射文件中用于设定检索策略的几个属性

![image-20210519201528156](images\image-20210519201528156.png)

比较 Hibernate 的三种检索策略

![image-20210519201647476](images\image-20210519201647476.png)

# 十一 Hibernate 检索方式

Hibernate 提供了以下几种检索对象的方式

​	–**导航对象图检索方式**: 根据已经加载的对象导航到其他对象

​	–**OID** **检索方式**: 按照对象的 OID 来检索对象

​	–**HQL** **检索方式**: 使用面向对象的 HQL 查询语言

​	–**QBC** **检索方式**:使用 QBC(Query By Criteria) API 来检索对象. 这种 API 封装了基于字符串形式的查询语句, 提供了更加面向对象的查询接口.

​	–**本地** **SQL** **检索方式**: 使用本地数据库的 SQL 查询语句

## HQL 检索方式

HQL(Hibernate Query Language) 是面向对象的查询语言, 它和 SQL 查询语言有些相似. 在 Hibernate 提供的各种检索方式中, HQL 是使用最广的一种检索方式. 它有如下功能:

​	–在查询语句中设定各种查询条件

​	–支持投影查询, 即仅检索出对象的部分属性

​	–支持分页查询

​	–支持连接查询

​	–支持分组查询, 允许使用 HAVING 和 GROUP BY 关键字

​	–提供内置聚集函数, 如 sum(), min() 和 max()

​	–支持子查询

​	–支持动态绑定参数

​	–能够调用 用户定义的 SQL 函数或标准的 SQL 函数

HQL 检索方式包括以下步骤:

​	–通过 Session 的 createQuery() 方法创建一个 Query 对象, 它包括一个 HQL 查询语句. HQL 查询语句中可以包含命名参数

​	–动态绑定参数

​	–调用 Query 相关方法执行查询语句.

**Qurey** **接口支持方法链编程风格**, 它的 setXxx() 方法返回自身实例, 而不是 void 类型

HQL vs SQL:

​	–**HQL** **查询语句是面向对象的**, Hibernate **负责解析** **HQL** **查询语句**, 然后根据对象-关系映射文件中的映射信息, 把 HQL 查询语句翻译成相应的 SQL 语句. HQL 查询语句中的主体是域模型中的类及类的属性

​	–SQL 查询语句是与关系数据库绑定在一起的. SQL 查询语句中的主体是数据库表及表的字段

绑定参数:

​	–Hibernate 的参数绑定机制依赖于 JDBC API 中的 PreparedStatement 的预定义 SQL 语句功能.

​	–HQL 的参数绑定由两种形式:

​		按参数名字绑定: 在 HQL 查询语句中定义命名参数, 命名参数以 “**:**” 开头.

​		按参数位置绑定: 在 HQL 查询语句中用 “?” 来定义参数位置

​	–相关方法:

​		setEntity(): 把参数与一个持久化类绑定

​		setParameter(): 绑定任意类型的参数. 该方法的第三个参数显式指定 Hibernate 映射类型

HQL 采用 **ORDER BY** 关键字对查询结果**排序**

分页查询:

​	–**setFirstResult**(int firstResult): 设定从哪一个对象开始检索, 参数 firstResult 表示这个对象在查询结果中的索引位置, 索引位置的起始值为 0. 默认情况下, Query 从查询结果中的第一个对象开始检索

​	–**setMaxResults**(int maxResults): 设定一次最多检索出的对象的数目. 在默认情况下, Query 和 Criteria 接口检索出查询结果中所有的对象

在映射文件中定义命名查询语句

​	–Hibernate 允许在映射文件中定义字符串形式的查询语句.

​	–<query> 元素用于定义一个 HQL 查询语句, 它和 <class> 元素并列

![image-20210523101019133](images\image-20210523101019133.png)

  –在程序中通过 Session 的 getNamedQuery() 方法获取查询语句对应的 Query 对象.

## 投影查询

投影查询: **查询结果仅包含实体的部分属性**. 通过 SELECT 关键字实现.

**Query** **的** **list()** **方法返回的集合中包含的是数组类型的元素**, **每个对象数组代表查询结果的一条记录**

**可以在持久化类中定义一个对象的构造器来包装投影查询返回的记录**, 使程序代码能完全运用面向对象的语义来访问查询结果集.

可以通过 DISTINCT 关键字来保证查询结果不会返回重复元素

## 报表查询

报表查询用于对数据分组和统计, 与 SQL 一样, HQL 利用 **GROUP BY** 关键字对数据分组, 用 **HAVING** 关键字对分组数据设定约束条件.

在 HQL 查询语句中可以调用以下聚集函数

​	–count()

​	–min()

​	–max()

​	–sum()

​	avg()

## HQL (迫切)左外连接

**迫切左外连接**:

​	–**LEFT JOIN** **FETCH** 关键字表示迫切左外连接检索策略.

​	–list() 方法**返回的集合中存放实体对象的引用**, 每个 Department 对象关联的 Employee 集合都被初始化, 存放所有关联的 Employee 的实体对象.

​	–查询结果中可能会包含重复元素, 可以通过一个 HashSet 来过滤重复元素

左外连接:

​	–**LEFT JOIN** 关键字表示左外连接查询.

​	–**list()** **方法返回的集合中存放的是对象数组类型**

​	–**根据配置文件来决定** **Employee** **集合的检索策略**.

​	–如果希望 list() 方法返回的集合中仅包含 Department 对象, 可以在HQL 查询语句中使用 SELECT 关键字

## HQL (迫切)内连接

**迫切内连接**:

​	–**INNER JOIN FETCH** 关键字表示迫切内连接, 也可以省略 INNER 关键字

​	–list() 方法返回的集合中存放 Department 对象的引用, 每个 Department 对象的 Employee 集合都被初始化, 存放所有关联的 Employee 对象

内连接:

​	–INNER JOIN 关键字表示内连接, 也可以省略 INNER 关键字

​	–list() 方法的集合中存放的每个元素对应查询结果的一条记录, 每个元素都是对象数组类型

​	–如果希望 list() 方法的返回的集合仅包含 Department 对象, 可以在 HQL 查询语句中使用 SELECT 关键字

关联级别运行时的检索策略

​	如果在 HQL 中没有显式指定检索策略, 将使用映射文件配置的检索策略.

​	HQL 会忽略映射文件中设置的迫切左外连接检索策略, **如果希望** **HQL** **采用迫切左外连接策略****,** **就必须在** **HQL** **查询语句中显式的指定它**

​	若在 HQL 代码中显式指定了检索策略, 就会覆盖映射文件中配置的检索策略

# 十二 Hibernate 二级缓存

## Hibernate 缓存

​	缓存(Cache): 计算机领域非常通用的概念。它介于应用程序和永久性数据存储源(如硬盘上的文件或者数据库)之间，其作用是降低应用程序直接读写永久性数据存储源的频率，从而提高应用的运行性能**。缓存中的数据是数据存储源中数据的拷贝。**缓存的物理介质通常是内存

Hibernate中提供了两个级别的缓存

 	–第一级别的缓存是 Session 级别的缓存，它是属于事务范围的缓存。这一级别的缓存由 hibernate 管理的

​	–第二级别的缓存是 SessionFactory 级别的缓存，它是属于进程范围的缓存

## SessionFactory 级别的缓存

SessionFactory 的缓存可以分为两类:

​	–内置缓存: **Hibernate** **自带的**, **不可卸载**. 通常在 Hibernate 的初始化阶段, Hibernate 会把映射元数据和预定义的 SQL 语句放到 SessionFactory 的缓存中, 映射元数据是映射文件中数据（.hbm.xml 文件中的数据）的复制. 该内置缓存是只读的.

​	–**外置缓存**(二级缓存)**: **一个可配置的缓存插件. 在默认情况下, SessionFactory 不会启用这个缓存插件. 外置缓存中的数据是数据库数据的复制, 外置缓存的物理介质可以是内存或硬盘

## 使用 Hibernate 的二级缓存

适合放入二级缓存中的数据:

​	–很少被修改

​	–不是很重要的数据, 允许出现偶尔的并发问题

不适合放入二级缓存中的数据:

​	–经常被修改

​	–财务数据, 绝对不允许出现并发问题

​	–与其他应用程序共享的数据

![image-20210523101651891](images\image-20210523101651891.png)

### 二级缓存的并发访问策略

两个并发的事务同时访问持久层的缓存的相同数据时, 也有可能出现各类并发问题.

二级缓存可以设定以下 4 种类型的并发访问策略, 每一种访问策略对应一种事务隔离级别

​	–非严格读写(Nonstrict-read-write): 不保证缓存与数据库中数据的一致性**.** 提供 **Read** **Uncommited** **事务隔离级别**, 对于极少被修改, 而且允许脏读的数据, 可以采用这种策略

​	读写型(Read-write):提供 **Read** **Commited** **数据隔离级别**.对于经常读但是很少被修改的数据, 可以采用这种隔离类型, 因为它可以防止脏读

​	–事务型(Transactional): 仅在受管理环境下适用. **它提供了** **Repeatable Read** **事务隔离级别**. 对于经常读但是很少被修改的数据, 可以采用这种隔离类型, 因为它可以防止脏读和不可重复读

​	–只读型(Read-Only):**提供** **Serializable** **数据隔离级别**, 对于从来不会被修改的数据, 可以采用这种访问策略

### 管理 Hibernate 的二级缓存

Hibernate 的二级缓存是进程或集群范围内的缓存

二级缓存是可配置的的插件, Hibernate 允许选用以下类型的缓存插件:

​	–**EHCache**: 可作为进程范围内的缓存, 存放数据的物理介质可以使内存或硬盘, 对 Hibernate 的查询缓存提供了支持

​	–OpenSymphony OSCache:可作为进程范围内的缓存, 存放数据的物理介质可以使内存或硬盘, 提供了丰富的缓存数据过期策略, 对 Hibernate 的查询缓存提供了支持

​	–SwarmCache: 可作为集群范围内的缓存, 但不支持 Hibernate 的查询缓存

​	–JBossCache:可作为集群范围内的缓存, 支持 Hibernate 的查询缓存

4 种缓存插件支持的并发访问策略(x 代表支持, 空白代表不支持)

![image-20210523101929636](images\image-20210523101929636.png)

### 配置进程范围内的二级缓存

配置进程范围内的二级缓存的步骤:

​	–选择合适的缓存插件: EHCache(jar 包和 配置文件), 并编译器配置文件

​	–在 Hibernate 的配置文件中启用二级缓存并指定和 EHCache 对应的缓存适配器

​	–选择需要使用二级缓存的持久化类, 设置它的二级缓存的并发访问策略

​	 	<class> 元素的 cache 子元素表明 Hibernate 会缓存对象的简单属性, 但不会缓存集合属性, 若希望缓存集合属性中的元素, 必须在 <set> 元素中加入 <cache> 子元素

​		在 hibernate 配置文件中通过 <class-cache/> 节点配置使用缓存

### ehcache.xml

<diskStore>: 指定一个目录：当 EHCache 把数据写到硬盘上时, 将把数据写到这个目录下.

<defaultCache>: 设置缓存的默认数据过期策略

<cache> 设定具体的命名缓存的数据过期策略。**每个命名缓存代表一个缓存区域**

缓存区域(region)：一个具有名称的缓存块，可以给每一个缓存块设置不同的缓存策略。如果没有设置任何的缓存区域，则所有被缓存的对象，都将使用默认的缓存策略。即：<defaultCache.../>

Hibernate在不同的缓存区域保存不同的类/集合。

​	–对于类而言，区域的名称是类名。如:com.atguigu.domain.Customer

​	–对于集合而言，区域的名称是类名加属性名。如com.atguigu.domain.Customer.orders

#### cache 元素的属性 

​	–name:设置缓存的名字,它的取值为类的全限定名或类的集合的名字

​	–maxInMemory:设置基于内存的缓存中可存放的对象最大数目

​	–eternal:设置对象是否为永久的,true表示永不过期,此时将忽略timeToIdleSeconds 和 timeToLiveSeconds属性; 默认值是false

​	–timeToIdleSeconds:设置对象空闲最长时间,以秒为单位, 超过这个时间,对象过期。当对象过期时,EHCache会把它从缓存中清除。如果此值为0,表示对象可以无限期地处于空闲状态。

​	–timeToLiveSeconds:设置对象生存最长时间,超过这个时间,对象过期。
 如果此值为0,表示对象可以无限期地存在于缓存中. 该属性值必须大于或等于 timeToIdleSeconds 属性值

​	–overflowToDisk:设置基于内存的缓存中的对象数目达到上限后,是否把溢出的对象写到基于硬盘的缓存中

#### 查询缓存

对于经常使用的**查询语句**, 如果启用了查询缓存, 当第一次执行查询语句时, Hibernate 会把查询结果存放在查询缓存中. 以后再次执行该查询语句时, 只需从缓存中获得查询结果, 从而提高查询性能

查询缓存使用于如下场合:

​	–应用程序运行时经常使用查询语句

​	–很少对与查询语句检索到的数据进行插入, 删除和更新操作

启用查询缓存的步骤

​	–配置二级缓存, 因为查询缓存依赖于二级缓存

​	–在 hibernate 配置文件中启用查询缓存

​	–对于希望启用查询缓存的查询语句, 调用 Query 的 setCacheable() 方法

```java
public class HibernateUtils {
	

	private HibernateUtils(){}
	
	private static HibernateUtils instance = new HibernateUtils();
	
	public static HibernateUtils getInstance() {
		return instance;
	}
	
	private SessionFactory sessionFactory;
	
	public SessionFactory getSessionFactory() {
		if (sessionFactory == null) {
			Configuration configuration = new Configuration().configure();
			ServiceRegistry serviceRegistry = new ServiceRegistryBuilder()
					.applySettings(configuration.getProperties())
					.buildServiceRegistry();
			sessionFactory = configuration.buildSessionFactory(serviceRegistry);
		}
		return sessionFactory;
	}
	
	public Session getSession(){
		return getSessionFactory().getCurrentSession();
	}

}
```

ecach配置文件

```xml
<ehcache>

    <!-- Sets the path to the directory where cache .data files are created.

         If the path is a Java System Property it is replaced by
         its value in the running VM.

         The following properties are translated:
         user.home - User's home directory
         user.dir - User's current working directory
         java.io.tmpdir - Default temp file path -->
    <!--  
       指定一个目录：当 EHCache 把数据写到硬盘上时, 将把数据写到这个目录下.
    -->
    <diskStore path="d:\\tempDirectory"/>


    <!--Default Cache configuration. These will applied to caches programmatically created through
        the CacheManager.

        The following attributes are required for defaultCache:

        maxInMemory       - Sets the maximum number of objects that will be created in memory
        eternal           - Sets whether elements are eternal. If eternal,  timeouts are ignored and the element
                            is never expired.
        timeToIdleSeconds - Sets the time to idle for an element before it expires. Is only used
                            if the element is not eternal. Idle time is now - last accessed time
        timeToLiveSeconds - Sets the time to live for an element before it expires. Is only used
                            if the element is not eternal. TTL is now - creation time
        overflowToDisk    - Sets whether elements can overflow to disk when the in-memory cache
                            has reached the maxInMemory limit.

        -->
    <!--  
       设置缓存的默认数据过期策略 
    -->
    <defaultCache
            maxElementsInMemory="10000"
            eternal="false"
            timeToIdleSeconds="120"
            timeToLiveSeconds="120"
            overflowToDisk="true"
    />

    <!--  
        设定具体的命名缓存的数据过期策略。每个命名缓存代表一个缓存区域
        缓存区域(region)：一个具有名称的缓存块，可以给每一个缓存块设置不同的缓存策略。
        如果没有设置任何的缓存区域，则所有被缓存的对象，都将使用默认的缓存策略。即：<defaultCache.../>
        Hibernate 在不同的缓存区域保存不同的类/集合。
         对于类而言，区域的名称是类名。如:com.atguigu.domain.Customer
         对于集合而言，区域的名称是类名加属性名。如com.atguigu.domain.Customer.orders
    -->
    <!--  
        name: 设置缓存的名字,它的取值为类的全限定名或类的集合的名字 
     maxElementsInMemory: 设置基于内存的缓存中可存放的对象最大数目 
     
     eternal: 设置对象是否为永久的, true表示永不过期,
     此时将忽略timeToIdleSeconds 和 timeToLiveSeconds属性; 默认值是false 
     timeToIdleSeconds:设置对象空闲最长时间,以秒为单位, 超过这个时间,对象过期。
     当对象过期时,EHCache会把它从缓存中清除。如果此值为0,表示对象可以无限期地处于空闲状态。 
     timeToLiveSeconds:设置对象生存最长时间,超过这个时间,对象过期。
     如果此值为0,表示对象可以无限期地存在于缓存中. 该属性值必须大于或等于 timeToIdleSeconds 属性值 
     
     overflowToDisk:设置基于内存的缓存中的对象数目达到上限后,是否把溢出的对象写到基于硬盘的缓存中 
    -->
    <cache name="com.atguigu.hibernate.entities.Employee"
           maxElementsInMemory="1"
           eternal="false"
           timeToIdleSeconds="300"
           timeToLiveSeconds="600"
           overflowToDisk="true"
    />

    <cache name="com.atguigu.hibernate.entities.Department.emps"
           maxElementsInMemory="1000"
           eternal="true"
           timeToIdleSeconds="0"
           timeToLiveSeconds="0"
           overflowToDisk="false"
    />

</ehcache>
```

hibernate配置文件


```xml
	<!-- 启用二级缓存 -->
	<property name="cache.use_second_level_cache">true</property>
	
	<!-- 配置使用的二级缓存的产品 -->
	<property name="hibernate.cache.region.factory_class">org.hibernate.cache.ehcache.EhCacheRegionFactory</property>
	
	<!-- 配置启用查询缓存 -->
	<property name="cache.use_query_cache">true</property>
	
	<!-- 配置管理 Session 的方式 -->
	<property name="current_session_context_class">thread</property>
	
	<!-- 需要关联的 hibernate 映射文件 .hbm.xml -->
	<mapping resource="com/atguigu/hibernate/entities/Department.hbm.xml"/>
	<mapping resource="com/atguigu/hibernate/entities/Employee.hbm.xml"/>
	
	<class-cache usage="read-write" class="com.atguigu.hibernate.entities.Employee"/>
	<class-cache usage="read-write" class="com.atguigu.hibernate.entities.Department"/>
	<collection-cache usage="read-write" collection="com.atguigu.hibernate.entities.Department.emps"/>

```
