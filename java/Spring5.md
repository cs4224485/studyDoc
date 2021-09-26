# 一、Spring5框架概述

1、Spring 是轻量级的开源的 JavaEE 框架 

2、Spring 可以解决企业应用开发的复杂性 

3、Spring 有两个核心部分：IOC 和 Aop 

（1）IOC：控制反转，把创建对象过程交给 Spring 进行管理 

（2）Aop：面向切面，不修改源代码进行功能增强 

4、Spring 特点 

（1）方便解耦，简化开发 

（2）Aop 编程支持 

（3）方便程序测试 

（4）方便和其他框架进行整合 

（5）方便进行事务操作 

（6）降低 API 开发难度

## Spring5 入门案例

![image-20210626084250760](\images\image-20210626084250760.png)

### 打开 idea 工具，创建普通 Java 工程

![image-20210626084727763](\images\image-20210626084727763.png)

### 导入 Spring5 相关 jar 包

![image-20210626084812505](\images\image-20210626084812505.png)

![image-20210626084828303](\images\image-20210626084828303.png)

### 创建普通类，在这个类创建普通方法

#### （1）创建实体类

```java
public class User {
    public void add() {
        System.out.println("add......");
    }
}
```

#### （2）Spring 配置文件使用 xml 格式

```xml
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:aop="http://www.springframework.org/schema/aop"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
            http://www.springframework.org/schema/beans/spring-beans.xsd
            http://www.springframework.org/schema/aop
            http://www.springframework.org/schema/aop/spring-aop.xsd
            http://www.springframework.org/schema/context
            http://www.springframework.org/schema/context/spring-context.xsd
http://www.springframework.org/schema/beans ">
	 <!--配置 User 对象创建-->
    <bean id="user" class="com.harry.spring.bean.User"/>
</beans>
```

### 进行测试编写

```java
package com.harry.spring.test;

import com.harry.spring.bean.User;
import org.junit.Test;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class UserTest {
    @Test
    public void testAdd() {
        //1 加载 spring 配置文件
        ApplicationContext context =
                new ClassPathXmlApplicationContext("bean1.xml");
        //2 获取配置创建的对象
        User user = context.getBean("user", User.class);
        System.out.println(user);
        user.add();
    }

}
```

# 二、IOC（概念和原理）

## 1、什么是 IOC 

（1）控制反转，把对象创建和对象之间的调用过程，交给 Spring 进行管理 

（2）使用 IOC 目的：为了耦合度降低 

（3）做入门案例就是 IOC 实现

## 2、IOC 底层原理 

（1）xml 解析、工厂模式、反射

##  3、画图讲解 IOC 底层原理

![image-20210626091242166](\images\image-20210626091242166.png)

## IOC（BeanFactory 接口）

1、IOC 思想基于 IOC 容器完成，IOC 容器底层就是对象工厂 

2、Spring 提供 IOC 容器实现两种方式：（两个接口） 

（1）BeanFactory：IOC 容器基本实现，是 Spring 内部的使用接口，不提供开发人员进行使用 * 加载配置文件时候不会创建对象，在获取对象（使用）才去创建对象 

（2）ApplicationContext：BeanFactory 接口的子接口，提供更多更强大的功能，一般由开发人 员进行使用 * 加载配置文件时候就会把在配置文件对象进行创建 

3、ApplicationContext 接口有实现类

![image-20210626091403251](\images\image-20210626091403251.png)

## IOC 操作 Bean 管理（概念）

### 1、什么是 Bean 管理 

（0）Bean 管理指的是两个操作 

（1）Spring 创建对象 

（2）Spirng 注入属性

### 2、Bean 管理操作有两种方式 

（1）基于 xml 配置文件方式实现 

（2）基于注解方式实现

## IOC 操作 Bean 管理（基于 xml 方式）

### 1、基于 xml 方式创建对象

![image-20210626091649914](\images\image-20210626091649914.png)

（1）在 spring 配置文件中，使用 bean 标签，标签里面添加对应属性，就可以实现对象创建 

（2）在 bean 标签有很多属性，介绍常用的属性 * id 属性：唯一标识 * class 属性：类全路径（包类路径） 

（3）创建对象时候，默认也是执行无参数构造方法完成对象创建

### 2、基于 xml 方式注入属性 

（1）DI：依赖注入，就是注入属性

### 3、第一种注入方式：使用 set 方法进行注入 

（1）创建类，定义属性和对应的 set 方法

```java
/**
 * 演示使用 set 方法进行注入属性
 */
public class Book {
    //创建属性
    private String bname;
    private String bauthor;
    //创建属性对应的 set 方法
    public void setBname(String bname) {
        this.bname = bname;
    }
    public void setBauthor(String bauthor) {
        this.bauthor = bauthor;
    }
}
```

（2）在 spring 配置文件配置对象创建，配置属性注入

```xml
<!--2 set 方法注入属性-->
<bean id="book" class="com.harry.spring.bean.Book">
    <!--使用 property 完成属性注入
    name：类里面属性名称
    value：向属性注入的值
    -->
    <property name="bname" value="易筋经"></property>
    <property name="bauthor" value="达摩老祖"></property>
</bean>
```

### 4、第二种注入方式：使用有参数构造进行注入

（1）创建类，定义属性，创建属性对应有参数构造方法

```java
/**
 * 使用有参数构造注入*/
public class Orders {
    //属性
    private String oname;
    private String address;
    //有参数构造
    public Orders(String oname,String address) {
        this.oname = oname;
        this.address = address;
    }
}
```

（2）在 spring 配置文件中进行配置

```xml
<!--3 有参数构造注入属性-->
<bean id="orders" class="com.harry.spring.bean.Orders">
    <constructor-arg name="oname" value="电脑"></constructor-arg>
    <constructor-arg name="address" value="China"></constructor-arg>
</bean>
```

### 5、p 名称空间注入（了解） 

第一步 添加 p 名称空间在配置文件中

![image-20210626092536817](D:\studyDoc\java\images\image-20210626092536817.png)

第二步 进行属性注入，在 bean 标签里面进行操作

```xml
<!--2 set 方法注入属性-->
<bean id="book" class="com.atguigu.spring5.Book" p:bname="九阳神功"
      p:bauthor="无名氏"></bean
```

## IOC 操作 Bean 管理（xml 注入其他类型属性）

### 1、字面量 

（1）null 值

```xml
<!--null 值-->
<property name="address">
    <null/>
</property>
```

（2）属性值包含特殊符号

```xml
<!--属性值包含特殊符号
 1 把<>进行转义 &lt; &gt;
 2 把带特殊符号内容写到 CDATA
-->
<property name="address">
    <value><![CDATA[<<南京>>]]></value>
</property>
```

### 2、注入属性-外部 bean

（1）创建两个类 service 类和 dao 类 

（2）在 service 调用 dao 里面的方法 

（3）在 spring 配置文件中进行配置

```java
public class UserService {
    //创建 UserDao 类型属性，生成 set 方法
    private UserDao userDao;
    public void setUserDao(UserDao userDao) {
        this.userDao = userDao;
    }
    public void add() {
        System.out.println("service add...............");
        userDao.update();
    }
}
```

```xml
<!--1 service 和 dao 对象创建-->
<bean id="userService" class="com.harry.spring.service.UserService">
    <!--注入 userDao 对象
    name 属性：类里面属性名称
    ref 属性：创建 userDao 对象 bean 标签 id 值
    -->
    <property name="userDao" ref="userDaoImpl"></property>
</bean>
<bean id="userDaoImpl" class="com.harry.spring.Dao.UserDao"></bean>
```

### 3、注入属性-内部 bean

（1）一对多关系：部门和员工 一个部门有多个员工，一个员工属于一个部门 部门是一，员工是多 

（2）在实体类之间表示一对多关系，员工表示所属部门，使用对象类型属性进行表示

```java
//部门类
public class Dept {
    private String dname;
    public void setDname(String dname) {
        this.dname = dname;
    }
}
```

```java
public class Emp {
    private String ename;
    private String gender;
    //员工属于某一个部门，使用对象形式表示
    private Dept dept;
    public void setDept(Dept dept) {
        this.dept = dept;
    }
    public void setEname(String ename) {
        this.ename = ename;
    }
    public void setGender(String gender) {
        this.gender = gender; }
}
```

（3）在 spring 配置文件中进行配置

```xml
<!--内部 bean-->
<bean id="emp" class="com.harry.spring.bean.Emp">
    <!--设置两个普通属性-->
    <property name="ename" value="lucy"></property>
    <property name="gender" value="女"></property>
    <!--设置对象类型属性-->
    <property name="dept">
        <bean id="dept" class="com.harry.spring.bean.Dept">
            <property name="dname" value="安保部"></property>
        </bean>
    </property>
</bean>
```

### 4、注入属性-级联赋值 

### （1）第一种写法

```xml
<!--级联赋值-->
<bean id="emp" class="com.harry.spring.bean.Emp">
    <!--设置两个普通属性-->
    <property name="ename" value="lucy"></property>
    <property name="gender" value="女"></property>
    <!--级联赋值-->
    <property name="dept" ref="dept"></property>
</bean>
<bean id="dept" class="com.harry.spring.bean.Dept">
    <property name="dname" value="财务部"></property>
</bean>
```

### （2）第二种写法

![image-20210626094454812](\images\image-20210626094454812.png)

```xml
<!--级联赋值-->
<bean id="emp" class="com.harry.spring.bean.Emp">
    <!--设置两个普通属性-->
    <property name="ename" value="lucy"></property> <property name="gender" value="女"></property>
    <!--级联赋值-->
    <property name="dept" ref="dept"></property>
    <property name="dept.dname" value="技术部"></property>
</bean>
<bean id="dept" class="com.harry.spring.bean.Dept">
    <property name="dname" value="财务部"></property>
</bean>
```

## IOC 操作 Bean 管理（xml 注入集合属性)

1、注入数组类型属性

 2、注入 List 集合类型属性

 3、注入 Map 集合类型属性 

（1）创建类，定义数组、list、map、set 类型属性，生成对应 set 方法

```java
public class Stu {
    //1 数组类型属性
    private String[] courses;
    //2 list 集合类型属性
    private List<String> list;
    //3 map 集合类型属性
    private Map<String,String> maps;
    //4 set 集合类型属性
    private Set<String> sets;
    public void setSets(Set<String> sets) {
        this.sets = sets;
    }
    public void setCourses(String[] courses) {
        this.courses = courses;
    }
    public void setList(List<String> list) {
        this.list = list;
    }
    public void setMaps(Map<String, String> maps) {
        this.maps = maps;
    }
}
```

（2）在 spring 配置文件进行配置

```xml
<!--1 集合类型属性注入-->
<bean id="stu" class="com.harry.spring.bean.Stu">
    <!--数组类型属性注入-->
    <property name="courses">
        <array>
            <value>java 课程</value>
            <value>数据库课程</value>
        </array>
    </property>
    <!--list 类型属性注入-->
    <property name="list">
        <list> <value>张三</value>
            <value>小三</value>
        </list>
    </property>
    <!--map 类型属性注入-->
    <property name="maps">
        <map>
            <entry key="JAVA" value="java"></entry>
            <entry key="PHP" value="php"></entry>
        </map>
    </property>
    <!--set 类型属性注入-->
    <property name="sets">
        <set>
            <value>MySQL</value>
            <value>Redis</value>
        </set>
    </property>
</bean>
```

在集合里面设置对象类型值

```xml
<!--创建多个 course 对象-->
<bean id="course1" class="com.atguigu.spring5.collectiontype.Course">
    <property name="cname" value="Spring5 框架"></property>
</bean>
<bean id="course2" class="com.atguigu.spring5.collectiontype.Course">
    <property name="cname" value="MyBatis 框架"></property>
</bean>
<!--注入 list 集合类型，值是对象-->
<property name="courseList">
    <list>
        <ref bean="course1"></ref>
        <ref bean="course2"></ref>
    </list>
</property
```

把集合注入部分提取出来

（1）在 spring 配置文件中引入名称空间 util

```xml
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:aop="http://www.springframework.org/schema/aop"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:util="http://www.springframework.org/schema/util"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
            http://www.springframework.org/schema/beans/spring-beans.xsd
            http://www.springframework.org/schema/aop
            http://www.springframework.org/schema/aop/spring-aop.xsd
            http://www.springframework.org/schema/context
            http://www.springframework.org/schema/context/spring-context.xsd
```

（2）使用 util 标签完成 list 集合注入提取

```xml
<!--1 提取 list 集合类型属性注入-->
<util:list id="bookList"> <value>易筋经</value>
    <value>九阴真经</value>
    <value>九阳神功</value>
</util:list>
<!--2 提取 list 集合类型属性注入使用-->
<bean id="book" class="com.harry.spring.bean.Book">
    <property name="list" ref="bookList"></property>
</bean>
```

## IOC 操作 Bean 管理（FactoryBean）

1、Spring 有两种类型 bean，一种普通 bean，另外一种工厂 bean（FactoryBean）

 2、普通 bean：在配置文件中定义 bean 类型就是返回类型 

3、工厂 bean：在配置文件定义 bean 类型可以和返回类型不一样

 第一步 创建类，让这个类作为工厂 bean，实现接口 FactoryBean

 第二步 实现接口里面的方法，在实现的方法中定义返回的 bean 类型

```JAVA
public class MyBean implements FactoryBean<Course> {
    //定义返回 bean
    public Course getObject() throws Exception {
        Course course = new Course();
        course.setCname("abc");
        return course;
    }
    public Class<?> getObjectType() {
        return null;
    }
    public boolean isSingleton() {
        return false;
    }
}
```

```xml
<bean id="myBean" class="com.harry.spring.bean.MyBean"></bean>
```

```java
@Test
public void test3() {
    ApplicationContext context =
            new ClassPathXmlApplicationContext("bean1.xml");
    Course course = context.getBean("myBean", Course.class);
    System.out.println(course);
}
```

# 三、AOP

## 1 什么是AOP

 （1）面向切面编程（方面），利用 AOP 可以对业务逻辑的各个部分进行隔离，从而使得 业务逻辑各部分之间的耦合度降低，提高程序的可重用性，同时提高了开发的效率。

 （2）通俗描述：不通过修改源代码方式，在主干功能里面添加新功能 

 （3）使用登录例子说明 AOP

![image-20210718093437598](\images\image-20210718093437598.png)

### AOP（底层原理）

![image-20210718093602624](\images\image-20210718093602624.png)

### AOP（JDK 动态代理）

1、使用 JDK 动态代理，使用 Proxy 类里面的方法创建代理对象

![image-20210718093812577](\images\image-20210718093812577.png)

2、编写 JDK 动态代理代码

```java
（1）创建接口，定义方法
public interface UserDao {
    public int add(int a,int b);
    public String update(String id);
}
（2）创建接口实现类，实现方法
public class UserDaoImpl implements UserDao {
    @Override
    public int add(int a, int b) {
        return a+b;
    }
    @Override
    public String update(String id) {
        return id;
    }
}
（3）使用 Proxy 类创建接口代理对象
public class JDKProxy {
    public static void main(String[] args) {
        //创建接口实现类代理对象
        Class[] interfaces = {UserDao.class};
// Proxy.newProxyInstance(JDKProxy.class.getClassLoader(), interfaces,
        new InvocationHandler() {
// @Override
// public Object invoke(Object proxy, Method method, Object[] args)
throws Throwable {
// return null;
// }
// });
           UserDaoImpl userDao = new UserDaoImpl();
           UserDao dao =(UserDao)Proxy.newProxyInstance(JDKProxy.class.getClassLoader(), interfaces,
           new UserDaoProxy(userDao)); int result = dao.add(1, 2);
           System.out.println("result:"+result);
    }
 }
//创建代理对象代码
class UserDaoProxy implements InvocationHandler {
    //1 把创建的是谁的代理对象，把谁传递过来
    //有参数构造传递
    private Object obj;
    public UserDaoProxy(Object obj) {
        this.obj = obj;
    }
    //增强的逻辑
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws
            Throwable {
        //方法之前
        System.out.println("方法之前执行...."+method.getName()+" :传递的参
                数..."+ Arrays.toString(args));
        //被增强的方法执行
        Object res = method.invoke(obj, args);
        //方法之后
        System.out.println("方法之后执行...."+obj);
        return res;
    }
```

## 2 AOP（术语）

切面(Aspect): **横切关注点**(跨越应用程序多个模块的功能)被模块化的特殊对象

通知(Advice): **切面必须要完成的工作**

目标(Target): **被通知的对象**

代理(Proxy): **向目标对象应用通知之后创建的对象**

连接点（Joinpoint）：**程序**执行的某个特定位置**：如类某个方法调用前、调用后、方法抛出异常后等。**连接点由两个信息确定：方法表示的程序执行点；相对点表示的方位。例如 ArithmethicCalculator#add() 方法执行前的连接点，执行点为 ArithmethicCalculator#add()； 方位为该方法执行前的位置

切点（pointcut）：**每个**类都拥有多个连接点**：例如 ArithmethicCalculator 的所有方法实际上都是连接点，即**连接点是程序类中客观存在的事务**。**AOP **通过切点定位到特定的连接点**。类比：连接点相当于数据库中的记录，切点相当于查询条件。切点和连接点不是一对一的关系，一个切点匹配多个连接点，切点通过 org.springframework.aop.Pointcut 接口进行描述，它使用类和方法作为连接点的查询条件。

**AspectJ**：Java 社区里最完整最流行的 AOP 框架.

在 Spring2.0 以上版本中, 可以使用基于 AspectJ 注解或基于 XML 配置的 AOP

## 3 AOP 操作（准备工作）

1、Spring 框架一般都是基于 AspectJ 实现 AOP 操作

 （1）AspectJ 不是 Spring 组成部分，独立 AOP 框架，一般把 AspectJ 和 Spirng 框架一起使 用，进行 AOP 操作 2、基于 AspectJ 实现 AOP 操作

 （1）基于 xml 配置文件实现 

 （2）基于注解方式实现（使用）

3、在项目工程里面引入 AOP 相关依

![image-20210718094357626](\images\image-20210718094357626.png)

4、切入点表达式 

（1）切入点表达式作用：知道对哪个类里面的哪个方法进行增强

 （2）语法结构： execution([权限修饰符] [返回类型] [类全路径] [方法名称]([参数列表]) ) 

举例 1：对 com.atguigu.dao.BookDao 类里面的 add 进行增强 execution(* com.atguigu.dao.BookDao.add(..)) 举例 2：对 com.atguigu.dao.BookDao 类里面的所有的方法进行增强 execution(* com.atguigu.dao.BookDao.* (..))

举例 3：对 com.atguigu.dao 包里面所有类，类里面所有方法进行增强 execution(* com.atguigu.dao.*.* (..))

## 4 AOP 操作（AspectJ 注解）

### 1、创建类，在类里面定义方法

```java

public class User {
    public void add() {
        System.out.println("add.......");
    }
}
```

### 2、创建增强类（编写增强逻辑）

```java
//增强的类
public class UserProxy {
    public void before() {//前置通知
        System.out.println("before......");
    }
}
```

### 3、进行通知的配置 

（1）在 spring 配置文件中，开启注解扫描

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:aop="http://www.springframework.org/schema/aop"
       xsi:schemaLocation="http://www.springframework.org/schema/beans 
http://www.springframework.org/schema/beans/spring-beans.xsd 
 http://www.springframework.org/schema/context 
http://www.springframework.org/schema/context/spring-context.xsd 
 http://www.springframework.org/schema/aop 
http://www.springframework.org/schema/aop/spring-aop.xsd">
<!-- 开启注解扫描 -->
<context:component-scan basepackage="com.atguigu.spring5.aopanno"></context:component-scan>
```

（2）使用注解创建 User 和 UserProxy 对象

![image-20210718094828057](\images\image-20210718094828057.png)

（3）在增强类上面添加注解 @Aspect

![image-20210718094909787](\images\image-20210718094909787.png)

（4）在 spring 配置文件中开启生成代理对象

```xml
<!-- 开启 Aspect 生成代理对象-->
<aop:aspectj-autoproxy></aop:aspectj-autoproxy>
```

### 4、配置不同类型的通知

（1）在增强类的里面，在作为通知方法上面添加通知类型注解，使用切入点表达式配置

```java
//增强的类
@Component
@Aspect //生成代理对象
public class UserProxy {
    //前置通知
    //@Before 注解表示作为前置通知
    @Before(value = "execution(* com.atguigu.spring5.aopanno.User.add(..))")
    public void before() {
        System.out.println("before.........");
    }
    //后置通知（返回通知）
    @AfterReturning(value = "execution(* 
            com.atguigu.spring5.aopanno.User.add(..))")
    public void afterReturning() {
        System.out.println("afterReturning.........");
    }
    //最终通知
    @After(value = "execution(* com.atguigu.spring5.aopanno.User.add(..))")
    public void after() {
        System.out.println("after.........");
    }
    //异常通知
    @AfterThrowing(value = "execution(* 
            com.atguigu.spring5.aopanno.User.add(..))")
    public void afterThrowing() {
        System.out.println("afterThrowing.........");
    }
    //环绕通知
    @Around(value = "execution(* com.atguigu.spring5.aopanno.User.add(..))")
    public void around(ProceedingJoinPoint proceedingJoinPoint) throws
            Throwable {
        System.out.println("环绕之前.........");
        //被增强的方法执行
        proceedingJoinPoint.proceed();
        System.out.println("环绕之后.........");
    }
}
```

### 5、相同的切入点抽取

```java
//相同切入点抽取
@Pointcut(value = "execution(* com.atguigu.spring5.aopanno.User.add(..))")public void pointdemo() {
}
//前置通知
//@Before 注解表示作为前置通知
    @Before(value = "pointdemo()")
    public void before() {
        System.out.println("before.........");
    }
```

### 6、有多个增强类多同一个方法进行增强，设置增强类优先

```java
@Component
@Aspect
@Order(1)
public class PersonProxy
```

### 7、完全使用注解开发

```java
@Configuration
@ComponentScan(basePackages = {"com.harry"})
@EnableAspectJAutoProxy(proxyTargetClass = true)
public class ConfigAop {
}
```

## 5 AOP 操作（AspectJ 配置文件）

1、创建两个类，增强类和被增强类，创建方法

2、在 spring 配置文件中创建两个类对象

```xml
<!--创建对象-->
<bean id="book" class="com.atguigu.spring5.aopxml.Book"></bean>
<bean id="bookProxy" class="com.atguigu.spring5.aopxml.BookProxy"></bean>
```

3、在 spring 配置文件中配置切入点

```xml
<!--配置 aop 增强-->
<aop:config>
<!--切入点-->
<aop:pointcut id="p" expression="execution(* 
com.atguigu.spring5.aopxml.Book.buy(..))"/>
<!--配置切面-->
<aop:aspect ref="bookProxy">
    <!--增强作用在具体的方法上-->
    <aop:before method="before" pointcut-ref="p"/>
</aop:aspect>
</aop:config>
```

# 四 、JdbcTemplate

## 1、什么是 JdbcTemplate 

（1）Spring 框架对 JDBC 进行封装，使用 JdbcTemplate 方便实现对数据库操作

## 2、准备工作

![image-20210718095602672](\images\image-20210718095602672.png)

（2）在 spring 配置文件配置数据库连接池

```xml
        <!-- 数据库连接池 -->
<bean id="dataSource" class="com.alibaba.druid.pool.DruidDataSource"
      destroy-method="close">
	<property name="url" value="jdbc:mysql:///user_db" />
	<property name="username" value="root" />
	<property name="password" value="root" />
	<property name="driverClassName" value="com.mysql.jdbc.Driver" />
</bean>
```

（3）配置 JdbcTemplate 对象，注入 DataSource

```xml
<!-- JdbcTemplate 对象 -->
<bean id="jdbcTemplate" class="org.springframework.jdbc.core.JdbcTemplate">
    <!--注入 dataSource-->
    <property name="dataSource" ref="dataSource"></property>
</bean>
```

（4）创建 service 类，创建 dao 类，在 dao 注入 jdbcTemplate 对象

```xml
<!-- 组件扫描 -->
<context:component-scan base-package="com.atguigu"></context:component-scan>
```

```java
@Service
public class BookService {
    //注入 dao
    @Autowired
    private BookDao bookDao;
}
@Repository
public class BookDaoImpl implements BookDao {
    //注入 JdbcTemplate
    @Autowired
    private JdbcTemplate jdbcTemplate;
}
```

## 3、JdbcTemplate 操作数据库（添加）

1、对应数据库创建实体类

![image-20210718100055063](\images\image-20210718100055063.png)

2、编写 service 和 dao 

（1）在 dao 进行数据库添加操作 

（2）调用 JdbcTemplate 对象里面 update 方法实现添加操

 有两个参数 ： 第一个参数：sql 语句   第二个参数：可变参数，设置 sql 语句

```java
@Repository
public class BookDaoImpl implements BookDao {
    //注入 JdbcTemplate
    @Autowired
    private JdbcTemplate jdbcTemplate;
    //添加的方法
    @Override
    public void add(Book book) {
        //1 创建 sql 语句
        String sql = "insert into t_book values(?,?,?)";
        //2 调用方法实现
        Object[] args = {book.getUserId(), book.getUsername(),
                book.getUstatus()};
        int update = jdbcTemplate.update(sql,args); System.out.println(update);
    }
}
```

测试类：

```java
@Test
public void testJdbcTemplate() {
    ApplicationContext context =
            new ClassPathXmlApplicationContext("bean1.xml");
    BookService bookService = context.getBean("bookService",
            BookService.class);
    Book book = new Book();
    book.setUserId("1");
    book.setUsername("java");
    book.setUstatus("a");
    bookService.addBook(book);
}
```

## 4、JdbcTemplate 操作数据库（修改和删除）

```java
1、修改
@Override
public void updateBook(Book book) {
    String sql = "update t_book set username=?,ustatus=? where user_id=?";
    Object[] args = {book.getUsername(), book.getUstatus(),book.getUserId()};
    int update = jdbcTemplate.update(sql, args);
    System.out.println(update);
}   
2、删除
@Override
public void delete(String id) {
   String sql = "delete from t_book where user_id=?";
   int update = jdbcTemplate.update(sql, id);
   System.out.println(update);
}
```

## 5、JdbcTemplate 操作数据库（查询返回某个值）

1、查询表里面有多少条记录，返回是某个值 

2、使用 JdbcTemplate 实现查询返回某个值代码

有两个参数  第一个参数：sql 语句   第二个参数：返回类型 Class

```java
//查询表记录数
@Override
public int selectCount() { String sql = "select count(*) from t_book";
    Integer count = jdbcTemplate.queryForObject(sql, Integer.class);
    return count;
}
```

## 6、JdbcTemplate 操作数据库（查询返回对象）

1、场景：查询图书详情 

2、JdbcTemplate 实现查询返回对象

有三个参数：  

​	第一个参数：sql 语句 

​	第二个参数：RowMapper 是接口，针对返回不同类型数据，使用这个接口里面实现类完成 数据封装 

​	第三个参数：sql 语句

```java
//查询返回对象
@Override
public Book findBookInfo(String id) {
    String sql = "select * from t_book where user_id=?";
    //调用方法
    Book book = jdbcTemplate.queryForObject(sql, new
            BeanPropertyRowMapper<Book>(Book.class), id);
    return book;
}
```

## 7、JdbcTemplate 操作数据库（批量操作）

1、批量操作：操作表里面多条记录 

2、JdbcTemplate 实现批量添加操作

```java
//批量添加
@Override
public void batchAddBook(List<Object[]> batchArgs) {
    String sql = "insert into t_book values(?,?,?)";
    int[] ints = jdbcTemplate.batchUpdate(sql, batchArgs);
    System.out.println(Arrays.toString(ints));
}
//批量添加测试
List<Object[]> batchArgs = new ArrayList<>();
Object[] o1 = {"3","java","a"};
Object[] o2 = {"4","c++","b"};
Object[] o3 = {"5","MySQL","c"};
batchArgs.add(o1);
batchArgs.add(o2);
batchArgs.add(o3);
//调用批量添加
bookService.batchAdd(batchArgs);
```

3、JdbcTemplate 实现批量修改操作

```java
//批量修改
@Override
public void batchUpdateBook(List<Object[]> batchArgs) {
        String sql = "update t_book set username=?,ustatus=? where user_id=?";
        int[] ints = jdbcTemplate.batchUpdate(sql, batchArgs);
        System.out.println(Arrays.toString(ints));
 }
//批量修改
List<Object[]> batchArgs = new ArrayList<>();
Object[] o1 = {"java0909","a3","3"};
Object[] o2 = {"c++1010","b4","4"};
Object[] o3 = {"MySQL1111","c5","5"};
batchArgs.add(o1);
batchArgs.add(o2);
batchArgs.add(o3);
//调用方法实现批量修改
bookService.batchUpdate(batchArgs);
```

4、JdbcTemplate 实现批量删除操作

```java
//批量删除
@Override
public void batchDeleteBook(List<Object[]> batchArgs) {
    String sql = "delete from t_book where user_id=?";
    int[] ints = jdbcTemplate.batchUpdate(sql, batchArgs);
    System.out.println(Arrays.toString(ints));
}
//批量删除
List<Object[]> batchArgs = new ArrayList<>();Object[] o1 = {"3"};
Object[] o2 = {"4"};
batchArgs.add(o1);
batchArgs.add(o2);
//调用方法实现批量删除
bookService.batchDelete(batchArgs);
```

# 五、事务管理

## 1、什么是事务

 （1）事务是数据库操作最基本单元，逻辑上一组操作，要么都成功，如果有一个失败所有操 作都失败

 （2）典型场景：银行转账

​		 * lucy 转账 100 元 给 mary * lucy 少 100，mary 多 100

## 2、事务四个特性（ACID）

 （1）原子性

 （2）一致性 

 （3）隔离性 

 （4）持久性

![image-20210802193412668](\images\image-20210802193412668.png)

创建数据库表，添加记录

![image-20210802193450566](\images\image-20210802193450566.png)

创建 service，搭建 dao，完成对象创建和注入关系

（1）service 注入 dao，在 dao 注入 JdbcTemplate，在 JdbcTemplate 注入 DataSource

```java
@Service
public class UserService {
    //注入 dao
    @Autowired
    private UserDao userDao;
}
@Repository
public class UserDaoImpl implements UserDao {
    @Autowired private JdbcTemplate jdbcTemplate;
}
```

在 dao 创建两个方法：多钱和少钱的方法，在 service 创建方法（转账的方法）

```java
@Repository
public class UserDaoImpl implements UserDao {
    @Autowired
    private JdbcTemplate jdbcTemplate;
    //lucy 转账 100 给 mary
    //少钱
    @Override
    public void reduceMoney() {
        String sql = "update t_account set money=money-? where username=?";
        jdbcTemplate.update(sql,100,"lucy");
    }
    //多钱
    @Override
    public void addMoney() {
        String sql = "update t_account set money=money+? where username=?";
        jdbcTemplate.update(sql,100,"mary");
    }
}
@Service
public class UserService {
    //注入 dao
    @Autowired
    private UserDao userDao;
    //转账的方法
    public void accountMoney() {
        //lucy 少 100
        userDao.reduceMoney();
        //mary 多 100
        userDao.addMoney();
    }
}
```

## 3、Spring 事务管理介绍

1、事务添加到 JavaEE 三层结构里面 Service 层（业务逻辑层） 

2、在 Spring 进行事务管理操作 

（1）有两种方式：编程式事务管理和声明式事务管理（使用）

 3、声明式事务管理 

（1）基于注解方式（使用） 

（2）基于 xml 配置文件方式

 4、在 Spring 进行声明式事务管理，底层使用 AOP 原理

 5、Spring 事务管理 API 

（1）提供一个接口，代表事务管理器，这个接口针对不同的框架提供不同的实现类

![image-20210802193918299](\images\image-20210802193918299.png)

在 spring 配置文件配置事务管理器

![image-20210802194039520](\images\image-20210802194039520.png)

在spring 配置文件，开启事务注解

```xml
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:aop="http://www.springframework.org/schema/aop"
       xmlns:tx="http://www.springframework.org/schema/tx"
       xsi:schemaLocation="http://www.springframework.org/schema/beans 
http://www.springframework.org/schema/beans/spring-beans.xsd 
 http://www.springframework.org/schema/context 
http://www.springframework.org/schema/context/spring-context.xsd 
 http://www.springframework.org/schema/aop 
http://www.springframework.org/schema/aop/spring-aop.xsd  http://www.springframework.org/schema/tx 
http://www.springframework.org/schema/tx/spring-tx.xsd">
```

开启事务注解

```xml
<!--开启事务注解-->
<tx:annotation-driven transaction manager="transactionManager"></tx:annotation-driven>
```

在 service 类上面（或者 service 类里面方法上面）添加事务注解 

（1）@Transactional，这个注解添加到类上面，也可以添加方法上面 

（2）如果把这个注解添加类上面，这个类里面所有的方法都添加事务 

（3）如果把这个注解添加方法上面，为这个方法添加事务

在 service 类上面添加注解@Transactional，在这个注解里面可以配置事务相关参数

![image-20210802194712452](\images\image-20210802194712452.png)

## 4、propagation：事务传播行为

多事务方法直接进行调用，这个过程中事务 是如何进行管理的

![image-20210802194856816](\images\image-20210802194856816.png)

![image-20210802194934325](\images\image-20210802194934325.png)

## 5、ioslation：事务隔离级别

（1）事务有特性成为隔离性，多事务操作之间不会产生影响。不考虑隔离性产生很多问题 

（2）有三个读问题：脏读、不可重复读、虚（幻）读 

（3）脏读：一个未提交事务读取到另一个未提交事务的数据

![image-20210802195412887](\images\image-20210802195412887.png)

（4）不可重复读：一个未提交事务读取到另一提交事务修改数据

![image-20210802195449733](\images\image-20210802195449733.png)

（5）虚读：一个未提交事务读取到另一提交事务添加数据 

（6）解决：通过设置事务隔离级别，解决读问题

![image-20210802195553134](\images\image-20210802195553134.png)

timeout：超时时间

（1）事务需要在一定时间内进行提交，如果不提交进行回滚 

（2）默认值是 -1 ，设置时间以秒单位进行计算

readOnly：是否只读

（1）读：查询操作，写：添加修改删除操作 

（2）readOnly 默认值 false，表示可以查询，可以添加修改删除操作 

（3）设置 readOnly 值是 true，设置成 true 之后，只能查询

rollbackFor：回滚

  设置出现哪些异常进行事务回滚

noRollbackFor：不回滚

  设置出现哪些异常不进行事务回滚

## 6、事务操作（XML 声明式事务管理）

### 在 spring 配置文件中进行配置 

 第一步 配置事务管理器

 第二步 配置通知

 第三步 配置切入点和切面

```xml
<!--1 创建事务管理器-->
<bean id="transactionManager"
      class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
	<!--注入数据源-->
	<property name="dataSource" ref="dataSource"></property>
</bean>

<!--2 配置通知-->
<tx:advice id="txadvice">
<!--配置事务参数-->
<tx:attributes>
    <!--指定哪种规则的方法上面添加事务-->
    <tx:method name="accountMoney" propagation="REQUIRED"/>
    <!--<tx:method name="account*"/>-->
</tx:attributes>
</tx:advice>
 <!--3 配置切入点和切面-->
<aop:config>
	<!--配置切入点-->
	<aop:pointcut id="pt"expression="execution(*com.atguigu.spring5.service.UserService.*(..))"/>
	<!--配置切面-->
	<aop:advisor advice-ref="txadvice" pointcut-ref="pt"/>
</aop:config>
```

### 创建配置类，使用配置类替代 xml 配置文件

```java
@Configuration //配置类
@ComponentScan(basePackages = "com.atguigu") //组件扫描
@EnableTransactionManagement //开启事务
public class TxConfig {
    //创建数据库连接池
    @Bean
    public DruidDataSource getDruidDataSource() {
        DruidDataSource dataSource = new DruidDataSource();
        dataSource.setDriverClassName("com.mysql.jdbc.Driver");
        dataSource.setUrl("jdbc:mysql:///user_db");
        dataSource.setUsername("root");
        dataSource.setPassword("root");
        return dataSource;
    }
    //创建 JdbcTemplate 对象
    @Bean
    public JdbcTemplate getJdbcTemplate(DataSource dataSource) {
        //到 ioc 容器中根据类型找到 dataSource
        JdbcTemplate jdbcTemplate = new JdbcTemplate();
        //注入 dataSource
        jdbcTemplate.setDataSource(dataSource); return jdbcTemplate;
    }
    //创建事务管理器
    @Bean
    public DataSourceTransactionManager
    getDataSourceTransactionManager(DataSource dataSource) {
        DataSourceTransactionManager transactionManager = new
                DataSourceTransactionManager();
        transactionManager.setDataSource(dataSource);
        return transactionManager;
    }
}
```

# 六 、Spring5 框架新功能

## 1、整个 Spring5 框架的代码基于 Java8，运行时兼容 JDK9，许多不建议使用的类和方 法在代码库中删除

## 2、Spring 5.0 框架自带了通用的日志封装  

（1）Spring5 已经移除 Log4jConfigListener，官方建议使用 Log4j2 

（2）Spring5 框架整合 Log4j2

第一步 引入 jar 包

![image-20210802201356285](\images\image-20210802201356285.png)

第二步 创建 log4j2.xml 配置文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--日志级别以及优先级排序: OFF > FATAL > ERROR > WARN > INFO > DEBUG > TRACE > ALL -->
<!--Configuration 后面的 status 用于设置 log4j2 自身内部的信息输出，可以不设置，当设置成 trace 时，可以看到 log4j2 内部各种详细输出-->
<configuration status="INFO">
<!--先定义所有的 appender-->
<appenders>
    <!--输出日志信息到控制台-->
    <console name="Console" target="SYSTEM_OUT">
        <!--控制日志输出的格式-->
        <PatternLayout pattern="%d{yyyy-MM-dd HH:mm:ss.SSS} [%t] %-5level %logger{36} - %msg%n"/>
    </console>
</appenders>
<!--然后定义 logger，只有定义 logger 并引入的 appender，appender 才会生效-->
<!--root：用于指定项目的根日志，如果没有单独指定 Logger，则会使用 root 作为默认的日志输出-->
<loggers>
    <root level="info">
        <appender-ref ref="Console"/>
    </root> </loggers>
</configuration>
```

## 3、Spring5 框架核心容器支持@Nullable 注解

（1）@Nullable 注解可以使用在方法上面，属性上面，参数上面，表示方法返回可以为空，属性值可以 为空，参数值可以为空 

（2）注解用在方法上面，方法返回值可以为空

![image-20210802201643562](\images\image-20210802201643562.png)

（3）注解使用在方法参数里面，方法参数可以为空

![image-20210802201711115](\images\image-20210802201711115.png)

（4）注解使用在属性上面，属性值可以为空

![image-20210802201739869](\images\image-20210802201739869.png)

## 4、Spring5 核心容器支持函数式风格 GenericApplicationContext

```java
//函数式风格创建对象，交给 spring 进行管理
@Test
public void testGenericApplicationContext() {
    //1 创建 GenericApplicationContext 对象
    GenericApplicationContext context = new GenericApplicationContext();
    //2 调用 context 的方法对象注册
    context.refresh();
    context.registerBean("user1",User.class,() -> new User());
    //3 获取在 spring 注册的对象
    // User user = (User)context.getBean("com.atguigu.spring5.test.User");
    User user = (User)context.getBean("user1");
    System.out.println(user);
}
```

## 5、Spring5 支持整合 JUnit5

（1）整合 JUnit4 第一步

第一步 引入 Spring 相关针对测试依赖

![image-20210802202038552](\images\image-20210802202038552.png)

第二步 创建测试类，使用注解方式完成

```java
@RunWith(SpringJUnit4ClassRunner.class) //单元测试框架
@ContextConfiguration("classpath:bean1.xml") //加载配置文件public class JTest4 {
	@Autowired
	private UserService userService;
	@Test
	public void test1() {
		userService.accountMoney();
	}
}
```

（2）Spring5 整合 JUnit5

第一步 引入 JUnit5 的 jar 包

![image-20210802202242181](\images\image-20210802202242181.png)

第二步 创建测试类，使用注解完成

```java
@ExtendWith(SpringExtension.class)
@ContextConfiguration("classpath:bean1.xml")
public class JTest5 {
    @Autowired
    private UserService userService;
    @Test
    public void test1() {
        userService.accountMoney();
    }
}
```

（3）使用一个复合注解替代上面两个注解完成整合

```java
@SpringJUnitConfig(locations = "classpath:bean1.xml")
public class JTest5 {
    @Autowired
    private UserService userService;
    @Test
    public void test1() {
        userService.accountMoney();
    }
}
```

# 七、Spring5 框架新功能（Webflux）