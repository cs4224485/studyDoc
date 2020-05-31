# 一、Spring 是什么

Spring 是一个开源框架.

Spring 为简化企业级应用开发而生. 使用 Spring 可以使简单的 JavaBean 实现以前只有 EJB 才能实现的功能.

Spring 是一个 IOC(DI) 和 AOP 容器框架

### Spring 模块

![image-20200515170159431](\images\image-20200515170159431.png)

### 安装 SPRING TOOL SUITE

SPRING TOOL SUITE 是一个 Eclipse 插件，利用该插件可以更方便的在 Eclipse 平台上开发基于 Spring 的应用。

安装方法说明（springsource-tool-suite-3.4.0.RELEASE-e4.3.1-updatesite.zip）：

​	–**Help** --> **Install New Software...**

​	–Click Add...

​	–In dialog Add Site dialog, click **Archive...** 

​	–Navigate to **springsource-tool-suite-3.4.0.RELEASE-e4.3.1-updatesite.zip** and click  **Open** 

​	–Clicking **OK** in the Add Site dialog will bring you back to the dialog 'Install' 

​	–Select the **xxx/Spring IDE** that has appeared 

​	–Click **Next**  and then **Finish**

​	–**Approve the license** 

​	–Restart eclipse when that is asked

把以下 jar 包加入到工程的 classpath 下:

![image-20200515170327444](\images\image-20200515170327444.png)

Spring 的配置文件: 一个典型的 Spring 项目需要创建一个或多个 Bean 配置文件, 这些配置文件用于在 Spring IOC 容器里配置 Bean. Bean 的配置文件可以**放在** **classpath** **下**, 也可以放在其它目录下.

### 建立 Spring 项目

```java
public class HelloService {
    private String Hello;

    public String getHello() {
        return Hello;
    }

    public void setHello(String hello) {
        Hello = hello;
    }

    public void Hello(){
        System.out.println("Hello World");
    }
}
```

classpath下的：applicationContext.xml

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
            http://www.springframework.org/schema/context/spring-context.xsd">
    <beans>
        <bean class="com.harry.spring.service.HelloService" id="helloService">
            <property name="hello" value="你好"/>
        </bean>
    </beans>

</beans>
```

# 二、Spring 中的 Bean 配置

## 1、IOC 和 DI

IOC(Inversion of Control)：其思想是**反转资源获取的方向**. 传统的资源查找方式要求组件向容器发起请求查找资源. 作为回应, 容器适时的返回资源. 而应用了 IOC 之后, 则是容器主动地将资源推送给它所管理的组件 组件所要做的仅是选择一种合适的方式来接受资源. 这种行为也被称为查找的被动形式

DI(Dependency Injection) — IOC 的另一种表述方式：即组件以一些预先定义好的方式(例如: setter方法)接受来自如容器的资源注入相对于 IOC 而言，这种表述更直接

## 2、在 Spring 的 IOC 容器里配置 Bean

在 xml 文件中通过 bean 节点来配置 bean

```xml
<bean class="com.harry.spring.service.HelloService" id="helloService">
    <property name="hello" value="你好"/>
</bean>
```

id：Bean 的名称。

​	–**在** **IOC** **容器中必须是唯一的**

​	–**若** **id** **没有**指定，Spring **自动将权限定性类名作为** **Bean** **的**名字

​	–id 可以指定多个名字，名字之间可用逗号、分号、或空格分隔

## 3、Spring 容器

在 **Spring IOC** **容器**读取 Bean 配置创建 Bean 实例之前, 必须对它进行实例化. 只有在容器实例化后, 才可以从 IOC 容器里获取 Bean 实例并使用.

Spring 提供了两种类型的 IOC 容器实现.

​	–**BeanFactory**: IOC 容器的基本实现.

​	–**ApplicationContext**: 提供了更多的高级特性. 是 BeanFactory 的子接口.

​	–BeanFactory 是 Spring 框架的基础设施，面向 Spring 本身；ApplicationContext 面向使用 Spring 框架的开发者，**几乎所有的应用场合都直接使用** **ApplicationContext** **而非底层的** **BeanFactory**

​	–无论使用何种方式, 配置文件时相同的.

## 4、ApplicationContext

ApplicationContext 的主要实现类：

​	–**ClassPathXmlApplicationContext**：从 **类路径下**加载配置文件

​	–FileSystemXmlApplicationContext: 从文件系统中加载配置文件

ConfigurableApplicationContext 扩展于 ApplicationContext，新增加两个主要方法：refresh() 和 **close()**， 让 ApplicationContext 具有启动、刷新和关闭上下文的能力

**ApplicationContext** **在初始化上下文时就实例化所有单例的** **Bean**。

WebApplicationContext 是专门为 WEB 应用而准备的，它允许从相对于 WEB 根目录的路径中完成初始化工作

![image-20200515171854315](images\image-20200515171854315.png)

### 从 IOC 容器中获取 Bean

调用 ApplicationContext 的 getBean() 方法

## 5、依赖注入的方式

Spring 支持 3 种依赖注入的方式

​	–属性注入

​	–构造器注入

​	–工厂方法注入（很少使用，不推荐）

### 属性注入

属性注入即通过 **setter** **方法**注入Bean 的属性值或依赖的对象

属性注入使用 <property> 元素, 使用 name 属性指定 Bean 的属性名称，value 属性或 <value> 子节点指定属性值

属性注入是实际应用中最常用的注入方式

```xml
<bean class="com.harry.spring.service.HelloService" id="helloService">
    <property name="hello" value="你好"/>
</bean>
```

### 构造方法注入

通过构造方法注入Bean 的属性值或依赖的对象，它保证了 Bean 实例在实例化后就可以使用。

构造器注入在 <constructor-arg> 元素里声明属性, <constructor-arg>中没有 **name** **属性**

按索引匹配入参：

```xml
<bean class="com.harry.spring.service.bean.Car" id="car">
    <constructor-arg value="奥迪" index="0"></constructor-arg>
    <constructor-arg value="长春一汽" index="1"></constructor-arg>
    <constructor-arg value="500000" index="2"></constructor-arg>
</bean>
```

按类型匹配入参：

```xml
<bean class="com.harry.spring.service.bean.Car" id="car">
    <constructor-arg value="奥迪" type="java.lang.String"></constructor-arg>
    <constructor-arg value="长春一汽" type="java.lang.String"></constructor-arg>
    <constructor-arg value="50000" type="double"></constructor-arg>
</bean>
```

### 字面值

字面值：可用字符串表示的值，可以通过 <value> 元素标签或 value 属性进行注入。

基本数据类型及其封装类、String 等类型都可以采取字面值注入的方式

若字面值中包含特殊字符，可以使用 <![CDATA[]]> 把字面值包裹起来。

```xml
<bean id="car2" class="com.atguigu.spring.helloworld.Car">
	<constructor-arg value="ChangAnMazda"></constructor-arg>
	<!-- 若字面值中包含特殊字符, 则可以使用 DCDATA 来进行赋值. (了解) -->
	<constructor-arg>
		<value><![CDATA[<ATARZA>]]></value>
	</constructor-arg>
	<constructor-arg value="180" type="int"></constructor-arg>
</bean>
```
### 引用其它 Bean

组成应用程序的 Bean 经常需要相互协作以完成应用程序的功能. 要**使** **Bean** **能够相互访问**, 就必须在 Bean 配置文件中指定对 Bean 的引用

在 Bean 的配置文件中, 可以**通过**  **元素或** **ref** **属性**为 Bean 的属性或构造器参数指定对 Bean 的引用.

也可以**在属性或构造器里包含** **Bean** **的声明**, 这样的 Bean 称为**内部** **Bean**

```xml
<bean id="userService" class="com.harry.service.impl.UserServiceImpl" >
	<constructor-arg name="userDao" ref="userDaoId"/>
</bean>
<bean id="userDaoId" class="com.harry.Dao.impl.UserDaoImpl"/>
```
### 内部 Bean

当 Bean 实例**仅仅**给一个特定的属性使用时, 可以将其声明为内部 Bean. 内部 Bean 声明直接包含在 <property> 或 <constructor-arg> 元素里, 不需要设置任何 id 或 name 属性

内部 Bean 不能使用在任何其他地方

### 注入参数详解：null 值和级联属性

可以使用专用的 元素标签为 Bean 的字符串或其它对象类型的属性注入 null 值

和 Struts、Hiberante 等框架一样，**Spring** **支持级联属性的配置**。

### 集合属性

#### List

在 Spring中可以通过一组内置的 xml 标签(例如: <list>, <set> 或 <map>) 来配置集合属性.

配置 java.util.List 类型的属性, 需要指定 **<**list> 标签, 在标签里包含一些元素. 这些标签可以通过  指定简单的常量值, 通过 指定对其他 Bean 的引用 通过 指定内置 Bean 定义. 通过 <null/> 指定空元素. 甚至可以内嵌其他集合.

数组的定义和 List 一样, 都使用 <list>

配置 java.util.Set 需要使用 <set> 标签, 定义元素的方法与 List 一样.

```xml
<bean id="preson" class="com.harry.spring.service.bean.Person">
    <property name="name" value="harry"></property>
    <property name="age" value="21"></property>
    <property name="carList">
        <!-- 使用 list 元素来装配集合属性 -->
        <list>
            <ref bean="car"/>
            <ref bean="car2"/>
        </list>
    </property>
</bean>
```

#### MAP

Java.util.Map 通过 标签定义, <map> 标签里可以使用多个  作为子标签. 每个条目包含一个键和一个值.

必须在  标签里定义键

因为键和值的类型没有限制, 所以可以自由地为它们指定 或元素.

可以将 Map 的键和值作为 <entry> 的属性定义: 简单常量使用 key 和 value 来定义; Bean 引用通过 key-ref 和 value-ref 属性定义

使用定义 java.util.Properties, 该标签使用多个作为子标签. 每个 标签必须定义 **key** 属性.

```xml
<bean id="preson" class="com.harry.spring.service.bean.Person">
    <property name="name" value="harry"></property>
    <property name="age" value="21"></property>
    <property name="carMap">
        <map>
            <entry key="1" value-ref="car"></entry>
            <entry key="2" value-ref="car2"></entry>
        </map>
    </property>
</bean>
```

#### 使用 utility scheme 定义集合

```xml
<!-- 声明集合类型的 bean -->
<util:list id="cars">
	<ref bean="car"/>
	<ref bean="car2"/>
</util:list>

<bean id="user2" class="com.atguigu.spring.helloworld.User">
	<property name="userName" value="Rose"></property>
	<!-- 引用外部声明的 list -->
	<property name="cars" ref="cars"></property>
</bean>
```
#### 配置Properties属性值

```java
public class DataSource {
    private Properties properties;

    public Properties getProperties() {
        return properties;
    }

    public void setProperties(Properties properties) {
        this.properties = properties;
    }
}
```

```xml
<bean id="dataSource" class="com.harry.spring.service.bean.DataSource">
    <property name="properties">
        <props>
            <prop key="user">root</prop>
            <prop key="password">1234</prop>
            <prop key="jdbcUrl">jdbc:mysql://test</prop>
            <prop key="dirverClass">com.mysql.jdbc.Driver</prop>
        </props>
    </property>
</bean>
```

### 使用 p 命名空间

为了简化 XML 文件的配置，越来越多的 XML 文件采用属性而非子元素配置信息。

Spring 从 2.5 版本开始引入了一个新的 p 命名空间，可以通过 <bean> 元素属性的方式配置 Bean 的属性。

使用 p 命名空间后，基于 XML 的配置方式将进一步简化

## 三、Bean的装配

### XML 配置里的 Bean 自动装配

Spring IOC 容器可以自动装配 Bean. 需要做的仅仅是**在** **的** **autowire** **属性里指定自动装配的模式**

**byType**(根据类型自动装配): 若 IOC 容器中有多个与目标 Bean 类型一致的 Bean. 在这种情况下, Spring 将无法判定哪个 Bean 最合适该属性, 所以不能执行自动装配.

**byName**(根据名称自动装配): 必须将目标 Bean 的名称和属性名设置的完全相同.

constructor(通过构造器自动装配): 当 Bean 中存在多个构造器时, 此种自动装配方式将会很复杂. **不推荐**使用

```xml
<!--  
byType: 根据类型进行自动装配. 但要求 IOC 容器中只有一个类型对应的 bean, 若有多个则无法完成自动装配.
byName: 若属性名和某一个 bean 的 id 名一致, 即可完成自动装配. 若没有 id 一致的, 则无法完成自动装配
-->
<!-- 在使用 XML 配置时, 自动转配用的不多. 但在基于 注解 的配置时, 自动装配使用的较多.  -->
<bean id="person2" class="com.harry.spring.service.bean.Person" autowire="byType"/>
```

XML 配置里的 Bean 自动装配的缺点

在 Bean 配置文件里设置 autowire 属性进行自动装配将会装配 Bean 的所有属性. 然而, 若只希望装配个别属性时, autowire 属性就不够灵活了.

autowire 属性要么根据类型自动装配, 要么根据名称自动装配, 不能两者兼而有之.

一般情况下，在实际的项目中很少使用自动装配功能，因为和自动装配功能所带来的好处比起来，明确清晰的配置文档更有说服力一些

### 继承 Bean 配置

**Spring** **允许继承** **bean** **的配置**, 被继承的 bean 称为父 bean. 继承这个父 Bean 的 Bean 称为子 Bean

**子** **Bean** **从父** **Bean** **中继承配置**, **包括** **Bean** 的属性配置

子 Bean 也可以**覆盖**从父 Bean 继承过来的配置

父 Bean 可以作为配置模板, 也可以作为 Bean 实例. **若只想把父** **Bean** **作为模板**, **可以设置** 的abstract **属性为** **true**, 这样 Spring 将不会实例化这个 Bean

**并不是** 元素里的所有属性都会被继承. 比如: autowire, abstract 等.

也**可以忽略父** **Bean** **的** **class** **属性**, 让子 Bean 指定自己的类, 而共享相同的属性配置. 但此时 **abstract** **必须设为** **true**

```xml
<bean id="personParent" abstract="true" class="com.harry.spring.service.bean.Person" >
</bean>
<bean id="person3" parent="personParent">
    <property name="name" value="蔡爽"></property>
    <property name="age" value="24"></property>
</bean>
```

### 依赖 Bean 配置

**Spring** **允许用户通过** **depends-on** **属性设定** **Bean** **前置依赖的**Bean，前置依赖的 Bean 会在本 Bean 实例化之前创建好

**如果前置依赖于多个** **Bean**，则可以通过逗号，空格或的方式配置 **Bean** **的名称**

```xml
<bean id="person3" parent="personParent" depends-on="car2 car">
    <property name="name" value="蔡爽"></property>
    <property name="age" value="24"></property>
</bean>
```

### Bean 的作用域

在 Spring 中, 可以在 <bean> 元素的 **scope** 属性里设置 Bean 的作用域.

**默认**情况下, Spring **只为每个在** **IOC** **容器里声明的** **Bean** **创建唯一一个实例,** **整个** **IOC** **容器范围内都能共享该**实例**：所有后续的 getBean() 调用和 Bean 引用都将返回这个唯一的 Bean 实例.该作用域被称为 **singleton, 它是所有 Bean 的默认作用域.

![image-20200516124212143](\images\image-20200516124212143.png)

```xml
<!-- 默认情况下 bean 是单例的! -->
<!-- 但有的时候, bean 就不能使单例的. 例如: Struts2 的 Action 就不是单例的! 可以通过 scope 属性来指定 bean 的作用域 -->
<!--  
prototype: 原型的. 每次调用 getBean 方法都会返回一个新的 bean. 且在第一次调用 getBean 方法时才创建实例
singleton: 单例的. 每次调用 getBean 方法都会返回同一个 bean. 且在 IOC 容器初始化时即创建 bean 的实例. 默认值 
-->
<bean id="dao2" class="com.atguigu.spring.ref.Dao" scope="prototype"></bean>
<bean id="service" class="com.atguigu.spring.ref.Service" autowire="byName"></bean>
<bean id="action" class="com.atguigu.spring.ref.Action" autowire="byType"></bean>
```
### **使用外部属性文件**

在配置文件里配置 Bean 时, 有时需要在 Bean 的配置里混入**系统部署的细节信息**(例如: 文件路径, 数据源配置信息等). 而这些部署细节实际上需要和 Bean 配置相分离

Spring 提供了一个 PropertyPlaceholderConfigurer 的 **BeanFactory** **后置处理器**, 这个处理器允许用户将 Bean 配置的部分内容外移到**属性文件**中. 可以在 Bean 配置文件里使用形式为 **${var}** 的变量, PropertyPlaceholderConfigurer 从属性文件里加载属性, 并使用这些属性来替换变量.

Spring 还允许在属性文件中使用 ${propName}，以实现属性之间的相互引用。

```xml
<!-- 导入外部的资源文件 -->
<context:property-placeholder location="classpath:db.properties"/>
<!-- 配置数据源 -->
<bean id="dataSource" class="com.mchange.v2.c3p0.ComboPooledDataSource">
	<property name="user" value="${jdbc.user}"></property>
	<property name="password" value="${jdbc.password}"></property>
	<property name="driverClass" value="${jdbc.driverClass}"></property>
	<property name="jdbcUrl" value="${jdbc.jdbcUrl}"></property>
	<property name="initialPoolSize" value="${jdbc.initPoolSize}"></property>
	<property name="maxPoolSize" value="${jdbc.maxPoolSize}"></property>
</bean>
```
```properties
jdbc.user=root
jdbc.password=1230
jdbc.driverClass=com.mysql.jdbc.Driver
jdbc.jdbcUrl=jdbc:mysql:///test
jdbc.initPoolSize=5
jdbc.maxPoolSize=10
```

### Spring表达式语言：SpEL

**Spring** **表达式**语言**（简称**SpEL**）：是一个**支持运行时查询和操作对象图的强大的表达式语言。

**语法类似于** **EL**：**SpEL** **使用** #**{…}** **作为定界符，所有在大框号中的字符都将被认为是** **SpEL**

**SpEL** **为** **bean** **的属性进行动态赋值提供了便利**

通过 SpEL 可以实现：

​	–通过 bean 的 id 对 bean 进行引用

​	–调用方法以及引用对象中的属性

​	–计算表达式的值

​	正则表达式的匹配

#### SpEL：字面量

​	–整数：<property name="count" value="#{5}"/>

​	–小数：<property name="frequency" value="#{89.7}"/>

​	–科学计数法：<property name="capacity" value="#{1e4}"/>

​	–**String**可以使用单引号或者双引号作为字符串的定界符号**：<property name=“name” value="**#			{'Chuck'}**"/> 或 <property name='name' value='**#{"Chuck"}'/>

​	–Boolean：<property name="enabled" value="#{false}"/>

#### SpEL：引用 Bean、属性和方法

**引用其他**对象：

```xml
<!-- 通过Value属性和SpEl配置bean之间的关系 -->
<property name="prefix" value="#{prefixGenerator}"></property>
```

**引用其他对象的**属性

```xml
<!-- 通过value属性和SpEl配置suffix属性为另一个Bean的suffix属性值 -->
<property name="prefix" value="#{prefixGenerator2.suffix}"></property>
```

**调用其他方法，还可以链式操作**

![image-20200516125513925](\images\image-20200516125513925.png)

![image-20200516125533167](\images\image-20200516125533167.png)

**调用静态方法或静态属性**：通过 **T()** 调用一个类的静态方法，它将返回一个 Class Object，然后再调用相应的方法或属性：

![image-20200516130056092](images\image-20200516130056092.png)

#### SpEL支持的运算符号

**算数运算符：+, -, \*, /, %, **^：

![image-20200516125627939](images\image-20200516125627939.png)

**加号**还可以用作字符串连接：

![image-20200516125713695](images\image-20200516125713695.png)

**比较**运算符： **<, >, ==, <=, >=,** lt,gt,eq, le,ge

**逻辑运算符号：** **and, or, not,** 

![image-20200516125821645](images\image-20200516125821645.png)

**if-else** **运算符**：?: (ternary), ?: (Elvis)

![image-20200516125918965](\images\image-20200516125918965.png)

**if-else** 的变体

![image-20200516130001966](images\image-20200516130001966.png)

### IOC 容器中 Bean 的生命周期方法

**Spring IOC** **容器可以管理** **Bean** **的生命周期**, Spring 允许在 Bean 生命周期的特定点执行定制的任务

Spring IOC 容器对 Bean 的生命周期进行管理的过程:

​	–通过构造器或工厂方法创建 Bean 实例

​	–为 Bean 的属性设置值和对其他 Bean 的引用

​	–**调用** **Bean** **的初始化方法**

​	–Bean 可以使用了

​	–**当容器关闭时, **调用**Bean** 的销毁方法

在 Bean 的声明里设置 init-method 和 destroy-method 属性, 为 Bean 指定初始化和销毁方法

```xml
<bean id="person3" parent="personParent" init-method="init" destroy-method="destroy">
    <property name="name" value="蔡爽"></property>
    <property name="age" value="24"></property>
</bean>
```

```java
public class Person {
    private String name;
    private int age;
    private Map<String, Car> carMap;
    public void init(){
        System.out.println("Bean被创建");
    }

    public void destroy(){
        System.out.println("Bean销毁");
    }
}
```

#### 创建 Bean 后置处理器

**Bean** **后置处理器允许在调用初始化方法前后对** **Bean** **进行额外的处理****.**

**Bean** **后置处理器对** **IOC** **容器里的所有** **Bean** **实例逐一处理**, 而非单一实例. 其典型应用是: 检查 Bean 属性的正确性或根据特定的标准更改 Bean 的属性.

对Bean 后置处理器而言, 需要实现 BeanPostProcessor  接口. 在初始化方法被调用前后, Spring 将把每个 Bean 实例分别传递给上述接口的以下两个方法:

public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException 

public Object postProcessAfterInitialization(Object bean, final String beanName) throws BeansException

```xml
<!-- 配置 bean 后置处理器: 不需要配置 id 属性, IOC 容器会识别到他是一个 bean 后置处理器, 并调用其方法 -->
<bean class="com.harry.spring.service.MyBeanPostProcessor"></bean>
```

```java
public class MyBeanPostProcessor implements BeanPostProcessor {
    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
        System.out.println(bean);
        System.out.println(beanName + "初始化前");
        return null;
    }

    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
        System.out.println(bean);
        System.out.println(beanName + "初始化后");
        return null;
    }
}
```

### 通过调用静态工厂方法创建 Bean

调用**静态工厂方法**创建 Bean是将**对象创建的过程封装到静态方法中**. 当客户端需要对象时, 只需要简单地调用静态方法, 而不同关心创建对象的细节.

要声明通过静态方法创建的 Bean, 需要在 Bean 的 **class** 属性里指定拥有该工厂的方法的类, 同时在 **factory-method** 属性里指定工厂方法的名称. 最后, 使用 **<**constrctor-arg> 元素为该方法传递方法参数.

```java
public class PersonBeanFactory {
    // 静态工厂来创建Bean
    public static Person getPerson(String name, int age, Map carMap){
        return new Person(name, age, carMap);
    }
}
```

```xml
<!-- 通过工厂方法的方式来配置 bean -->
<!-- 通过静态工厂方法: 一个类中有一个静态方法, 可以返回一个类的实例(了解) -->
<!-- 在 class 中指定静态工厂方法的全类名, 在 factory-method 中指定静态工厂方法的方法名 -->
<bean id="person4" class="com.harry.spring.service.bean.PersonBeanFactory" factory-method="getPerson">
    <constructor-arg value="蔡爽" type="java.lang.String"></constructor-arg>
    <constructor-arg value="24" type="int"></constructor-arg>
    <constructor-arg name="carMap" type="java.util.Map">
        <map>
            <entry key="1" value-ref="car"></entry>
            <entry key="2" value-ref="car2"></entry>
        </map>
    </constructor-arg>
</bean>
```

### 通过调用实例工厂方法创建 Bean

**实例工厂方法**: **将对象的创建过程封装到另外一个对象实例的方法里**. 当客户端需要请求对象时, 只需要简单的调用该实例方法而不需要关心对象的创建细节.

要声明通过实例工厂方法创建的 Bean

​	–在 bean 的 **factory-bean** 属性里指定拥有该工厂方法的 Bean

​	–在 **factory-method** 属性里指定该工厂方法的名称

​	–使用 **construtor-arg** 元素为工厂方法传递方法参数

```java
// 实例工厂
public class CarBeanFactory {
    
    private Map<String, Car> carMap;

    public CarBeanFactory() {
        carMap = new HashMap<>();
        carMap.put("1", new Car("BMW", "yiiq", 300000));
        carMap.put("2", new Car("大众", "yiiq", 400000));
    }
    
    public Car getCar(){
        return carMap.get("1");
    }
}
```

```xml
<bean id="carFactory" class="com.harry.spring.service.bean.CarBeanFactory"></bean>
<!-- factory-bean 指向工厂 bean, factory-method 指定工厂方法(了解) -->
<bean id="car3" factory-bean="carFactory" factory-method="getCar"></bean>
```

### 实现 FactoryBean 接口在 Spring IOC 容器中配置 Bean

Spring 中有两种类型的 Bean, 一种是普通Bean, 另一种是工厂Bean, 即FactoryBean.

工厂 Bean 跟普通Bean不同, 其返回的对象不是指定类的一个实例, 其返回的是该工厂 Bean 的 getObject 方法所返回的对象

```java
public class CarFactory implements FactoryBean<Car> {
    // 返回bean的对象
    @Override
    public Car getObject() throws Exception {
        return new Car("保时捷", "SA", 500000);
    }
    // 返回bean的类型
    @Override
    public Class<?> getObjectType() {
        return Car.class;
    }
    // 是否是单例
    @Override
    public boolean isSingleton() {
        return true;
    }
}
```

```xml
<bean id="newCar" class="com.harry.spring.service.bean.CarFactory"></bean>
```

# 四、使用注解开发

### 在 classpath 中扫描组件

组件扫描(component scanning): Spring 能够从 classpath 下自动扫描, 侦测和实例化具有特定注解的组件.

特定组件包括:

​	–@Component: 基本注解, 标识了一个受 Spring 管理的组件

​	–@Respository: 标识持久层组件

​	–@Service: 标识服务层(业务层)组件

​	–@Controller: 标识表现层组件

对于扫描到的组件, **Spring** **有默认的命名策略**: 使用非限定类名, 第一个字母小写**.** **也可以**在注解中通过**value** **属性值标识组件的名称**

在组件类上使用了特定的注解之后, 还需要在 Spring 的配置文件中声明 **<**context:component-scan> ：

​	–**base-package** **属性指定一个需要扫描的基类包**，**Spring** 容器将会扫描这个基类包里及其子包中的所有类

​	–当需要扫描多个包时可以使用逗号分隔

​	–如果仅希望扫描特定的类而非基包下的所有类，可使用 resource-pattern 属性过滤特定的类

​	–**<**context:include-filter>子节点表示要包含的目标类

​	–**<**context:exclude-filter> **子节点表示**要排除在外的目标类

​	–<context:component-scan> 下可以拥有若干个 <context:include-filter> 和 <context:exclude-filter> 子节点

<context:include-filter> 和 <context:exclude-filter> 子节点支持多种类型的过滤表达式：

![image-20200516134441369](\images\image-20200516134441369.png)

```xml
<!-- context:exclude-filter 子节点指定排除那些指定表达式的组件 -->
<!-- context:include-filter 子节点包含那些表达式的组件，该子节点需要配合 use-default-filters使用 -->
<context:component-scan base-package="com.harry" use-default-filters="false">
  <context:exclude-filter type="annotation" expression="org.springframework.stereotype.Controller"/>
</context:component-scan>
```

### 组件装配

<context:component-scan> 元素还会自动注册 AutowiredAnnotationBeanPostProcessor 实例, 该实例可以自动装配具有 **@**Autowired **和** **@Resource** 、@Inject注解的属性.

> @Autowired 注解自动装配具有兼容类型的单个 Bean属性
> 构造器, 普通字段(即使是非 public), 一切具有参数的方法都可以应用@Authwired 注解
> 默认情况下, 所有使用 @Authwired 注解的属性都需要被设置. 当 Spring 找不到匹配的 Bean 装配属性时, 会抛出异常, 若某一属性允许不被设置, 可以设置 @Authwired 注解的 required 属性为 false
> 默认情况下, 当 IOC 容器里存在多个类型兼容的 Bean 时, 通过类型的自动装配将无法工作. 此时可以在 @Qualifier 注解里提供 Bean 的名称. Spring 允许对方法的入参标注 @Qualifiter 已指定注入 Bean 的名称 @Authwired 注解也可以应用在数组类型的属性上, 此时 Spring 将会把所有匹配的 Bean 进行自动装配.
> @Authwired 注解也可以应用在集合属性上, 此时 Spring 读取该集合的类型信息, 然后自动装配所有与之兼容的 Bean. 
> @Authwired 注解用在 java.util.Map 上时, 若该 Map 的键值为 String, 那么 Spring 将自动装配与之 Map 值类型兼容的 Bean, 此时 Bean 的名称作为键值

### 泛型依赖注入

Spring 4.x 中可以为子类注入子类对应的泛型类型的成员变量的引用

![image-20200517094604801](\images\image-20200517094604801.png)

 BaseRepository

```java
public class BaseRepository <T>{
}
```

BaseBaseServic

```java
public class BaseService<T> {
    @Autowired
    protected BaseRepository<T> repository;
    public void add(){
        System.out.println("add...");
        System.out.println(repository);
    }
}
```

```java
@Repository
public class UserRepository extends BaseRepository<User> {

}
```

```java
@Service
public class UserService extends BaseService<User> {
}
```

Test

```java
@Test
public void test2(){
    ClassPathXmlApplicationContext applicationContext = new ClassPathXmlApplicationContext("beans-generic-di.xml");
    UserService userService = (UserService)applicationContext.getBean("userService");
    userService.add();
}
```

输出结果：

add...
com.harry.spring.service.UserRepository@534df152

# 五、Spring AOP

代码混乱：越来越多的非业务需求(日志和验证等)加入后, 原有的业务方法急剧膨胀每个方法在处理核心逻辑的同时还必须兼顾其他多个关注点.

代码分散: 以日志需求为例, 只是为了满足这个单一需求, 就不得不在多个模块（方法）里多次重复相同的日志代码. 如果日志需求发生变化, 必须修改所有模块.

## 1、动态代理

代理设计模式的原理: **使用一个代理将对象包装起来**, 然后用该代理对象取代原始对象. 任何对原始对象的调用都要通过代理. 代理对象决定是否以及何时将方法调用转到原始对象上

![image-20200518095801309](\images\image-20200518095801309.png)

实现类：

```java
@Component("arithmeticCalculator")
public class ArithmeticCalculatorImpl implements ArithmeticCalculator {

    @Override
    public int add(int i, int j) {
        int result = i + j;
        return result;
    }

    @Override
    public int sub(int i, int j) {
        int result = i - j;
        return result;
    }

    @Override
    public int mul(int i, int j) {
        int result = i * j;
        return result;
    }

    @Override
    public int div(int i, int j) {
        int result = i / j;
        return result;
    }
}
```

动态代理：

```java
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;
import java.util.Arrays;

public class ArithmeticCalculatorLoggingProxy {
    // 要代理的对象
    private ArithmeticCalculator target;

    public ArithmeticCalculatorLoggingProxy(ArithmeticCalculator target) {
        this.target = target;
    }

    // 返回代理对象
    public ArithmeticCalculator getLoggingProxy() {
        ClassLoader loader = target.getClass().getClassLoader();
        ArithmeticCalculator arithmeticProxy = null;
        Class[] interfaces = new Class[]{ArithmeticCalculator.class};
        InvocationHandler handler = (Object proxy, Method method, Object[] args)->{
            /**
             * proxy: 代理对象。 一般不使用该对象
             * method: 正在被调用的方法
             * args: 调用方法传入的参数
             */
            String methodName = method.getName();
            //打印日志
            System.out.println("[before] The method " + methodName + " begins with " + Arrays.asList(args));
            //调用目标方法
            Object result = null;

            try {
                //前置通知
                result = method.invoke(target, args);
                //返回通知, 可以访问到方法的返回值
            } catch (NullPointerException e) {
                e.printStackTrace();
                //异常通知, 可以访问到方法出现的异常
            }

            //后置通知. 因为方法可以能会出异常, 所以访问不到方法的返回值

            //打印日志
            System.out.println("[after] The method ends with " + result);
            return result;
        };
        /**
         * loader: 代理对象使用的类加载器。
         * interfaces: 指定代理对象的类型. 即代理代理对象中可以有哪些方法.
         * h: 当具体调用代理对象的方法时, 应该如何进行响应, 实际上就是调用 InvocationHandler 的 invoke 方法
         */
        arithmeticProxy = (ArithmeticCalculator) Proxy.newProxyInstance(loader, interfaces, handler);
        return arithmeticProxy;
    }
}
```

测试

```java
public class ProxyTest {
    
    ArithmeticCalculator arithmeticCalculator;
    {
        ClassPathXmlApplicationContext applicationContext = new ClassPathXmlApplicationContext("applicationContext.xml");
        arithmeticCalculator = (ArithmeticCalculator)applicationContext.getBean("arithmeticCalculator");
    }

    @Test
    public void testProxy(){
        System.out.println(arithmeticCalculator);
        ArithmeticCalculator arithmeticCalculator = new ArithmeticCalculatorLoggingProxy(this.arithmeticCalculator).getLoggingProxy();
        arithmeticCalculator.add(1, 10);


    }
}
```

com.harry.spring.proxy.ArithmeticCalculatorImpl@971d0d8
[before] The method add begins with [1, 10]
[after] The method ends with 11

## 2、AOP

AOP(Aspect-Oriented Programming, **面向切面编程**): 是一种新的方法论, 是对传统 OOP(Object-Oriented Programming, 面向对象编程) 的补充

AOP 的主要编程对象是**切面**(aspect), 而**切面模块化横切关注点**.

在应用 AOP 编程时, 仍然需要定义公共功能, 但可以明确的定义这个功能在哪里, 以什么方式应用, **并且不必修改受影响的类**. 这样一来**横切关注点就被模块化到特殊的对象**(切面)里

### AOP 的好处

​	–每个事物逻辑位于一个位置, 代码不分散, 便于维护和升级

​	–业务模块更简洁, 只包含核心业务代码.

![image-20200518112056193](\images\image-20200518112056193.png)

### AOP 术语

切面(Aspect): **横切关注点**(跨越应用程序多个模块的功能)被模块化的特殊对象

通知(Advice): **切面必须要完成的工作**

目标(Target): **被通知的对象**

代理(Proxy): **向目标对象应用通知之后创建的对象**

连接点（Joinpoint）：**程序**执行的某个特定位置**：如类某个方法调用前、调用后、方法抛出异常后等。**连接点由两个信息确定：方法表示的程序执行点；相对点表示的方位。例如 ArithmethicCalculator#add() 方法执行前的连接点，执行点为 ArithmethicCalculator#add()； 方位为该方法执行前的位置

切点（pointcut）：**每个**类都拥有多个连接点**：例如 ArithmethicCalculator 的所有方法实际上都是连接点，即**连接点是程序类中客观存在的事务**。**AOP **通过切点定位到特定的连接点**。类比：连接点相当于数据库中的记录，切点相当于查询条件。切点和连接点不是一对一的关系，一个切点匹配多个连接点，切点通过 org.springframework.aop.Pointcut 接口进行描述，它使用类和方法作为连接点的查询条件。

**AspectJ**：Java 社区里最完整最流行的 AOP 框架.

在 Spring2.0 以上版本中, 可以使用基于 AspectJ 注解或基于 XML 配置的 AOP

### 在 Spring 中启用 AspectJ 注解支持

导入依赖：

```xml
<dependency>
	<groupId>org.aspectj</groupId>
	<artifactId>aspectjweaver</artifactId>
	<version>1.8.13</version>
</dependency>
<dependency>
	<groupId>org.springframework</groupId>
	<artifactId>spring-aspects</artifactId>
	<version>5.0.4.RELEASE</version>
</dependency>
```

将aopSchema添加到根元素中

要在 Spring IOC 容器中启用 AspectJ 注解支持, 只要**在** **Bean** **配置文件中定义一个空的** **XML** **元素** <aop:aspectj-autoproxy>

当 Spring IOC 容器侦测到 Bean 配置文件中的 <aop:aspectj-autoproxy> 元素时, 会自动为与 AspectJ 切面匹配的 Bean 创建代理.

### 用 AspectJ 注解声明切面

**要在** **Spring** **中声明** **AspectJ** **切面**, **只需要在** **IOC** **容器中将切面声明为** **Bean** **实例**. 当在 Spring IOC 容器中初始化 AspectJ 切面之后, Spring IOC 容器就会为那些与 AspectJ 切面相匹配的 Bean 创建代理

**在** **AspectJ** **注解中**, **切面只是一个带有** **@Aspect** **注解的** **Java** **类**

**通知是标注有某种注解的简单的** **Java** **方法**

### AspectJ 的切入点表达式

> AspectJ 除了提供了六种通知外，还定义了专门的表达式用于指定切入点。表达式的原型是：
> 	execution ( 
> 		[modifiers-pattern]  访问权限类型
> 		ret-type-pattern  返回值类型
> 		[declaring-type-pattern]  全限定性类名
> 		name-pattern(param-pattern)  方法名(参数名)
> 		[throws-pattern]  抛出异常类型 
> 	)
> 	
> 切入点表达式要匹配的对象就是目标方法的方法名。所以，execution 表达式中明显就是方法的签名。注意，表达式中加[ ]的部分表示可省略部分，各部分间用空格分开。
>
> execution(public * *(..)) 
> 指定切入点为：任意公共方法。
>
> execution(* set*(..)) 
> 指定切入点为：任何一个以“set”开始的方法。
>
> execution(* com.xyz.service.*.*(..)) 
> 指定切入点为：定义在 service 包里的任意类的任意方法。
>
> execution(* com.xyz.service..*.*(..))
> 指定切入点为：定义在 service 包或者子包里的任意类的任意方法。“..”出现在类名中时，后面必须跟“*”，表示包、子包下的所有类。
>
> execution(* *.service.*.*(..))
> 指定只有一级包下的 serivce 子包下所有类（接口）中所有方法为切入点 
>
> execution(* *..service.*.*(..))
> 指定所有包下的 serivce 子包下所有类（接口）中所有方法为切入点 
>
> execution(* *.ISomeService.*(..))
> 指定只有一级包下的 ISomeSerivce 接口中所有方法为切入点 
>
> execution(* *..ISomeService.*(..))
> 指定所有包下的 ISomeSerivce 接口中所有方法为切入点 
>
> execution(* com.xyz.service.IAccountService.*(..)) 
> 指定切入点为：  IAccountService  接口中的任意方法。 
>
> execution(* com.xyz.service.IAccountService+.*(..)) 
> 指定切入点为：  IAccountService  若为接口，则为接口中的任意方法及其所有实现类中的任意方法；若为类，则为该类及其子类中的任意方法。 
>
> execution(* joke(String,int)))
> 指定切入点为：所有的 joke(String,int)方法，且 joke()方法的第一个参数是 String，第二个参    数是 int。如果方法中的参数类型是 java.lang 包下的类，可以直接使用类名，否则必须使用全限定类名，如 joke( java.util.List, int)。 
>
> execution(* joke(String,*))) 
> 指定切入点为：所有的 joke()方法，该方法第一个参数为 String，第二个参数可以是任意类型，如 joke(String s1,String s2)和 joke(String s1,double d2)都是，但 joke(String s1,double d2,String s3)不是。
>
> execution(* joke(String,..)))   
> 指定切入点为：所有的 joke()方法，该方法第  一个参数为 String，后面可以有任意个参数且参数类型不限，如 joke(String s1)、joke(String s1,String s2)和 joke(Strings1,double d2,String s3)都是。
>
> execution(* joke(Object))
> 指定切入点为：所有的 joke()方法，方法拥有一个参数，且参数是 Object 类型。joke(Object ob)是，但，joke(String s)与 joke(User u)均不是。
>
> execution(* joke(Object+))) 
> 指定切入点为：所有的 joke()方法，方法拥有一个参数，且参数是 Object 类型或该类的子类。不仅 joke(Object ob)是，joke(String s)和 joke(User u)也是。

### 合并切入点表达式

在 AspectJ 中, 切入点表达式可以通过操作符 &&, ||, ! 结合起来

![image-20200518131808759](\images\image-20200518131808759.png)

配置文件

```xml
<context:component-scan base-package="com.harry.spring"/>
<aop:aspectj-autoproxy/>
```

切面

```java
@Aspect
@Component
public class LoggingAspect {

    /**
     * 定义一个方法, 用于声明切入点表达式. 一般地, 该方法中再不需要添入其他的代码.
     * 使用 @Pointcut 来声明切入点表达式.
     * 后面的其他通知直接使用方法名来引用当前的切入点表达式.
     */
    @Pointcut("execution(* com.harry.spring.proxy..*.*(..))")
    public void loginPointcut(){}

    // 前置通知
    @Before("loginPointcut()")
    public void beforeMethod(JoinPoint joinPoint){
        String methodName = joinPoint.getSignature().getName();
        Object [] args = joinPoint.getArgs();

        System.out.println("The method " + methodName + " begins with " + Arrays.asList(args));
    }

    // 后置通知 在方法执行之后执行的代码. 无论该方法是否出现异常
    @After("loginPointcut()")
    public void afterMethod(JoinPoint joinPoint){
        String methodName = joinPoint.getSignature().getName();
        System.out.println("The method " + methodName + " ends");
    }

    /**
     * 在方法法正常结束受执行的代码
     * 返回通知是可以访问到方法的返回值的!
     */
    @AfterReturning(value="loginPointcut()", returning="result")
    public void afterReturning(JoinPoint joinPoint, Object result){
        String methodName = joinPoint.getSignature().getName();
        System.out.println("The method " + methodName + " ends with " + result);
    }

    /**
     * 在目标方法出现异常时会执行的代码.
     * 可以访问到异常对象; 且可以指定在出现特定异常时在执行通知代码
     */
    @AfterThrowing(value="loginPointcut()", throwing="e")
    public void afterThrowing(JoinPoint joinPoint, Exception e){
        String methodName = joinPoint.getSignature().getName();
        System.out.println("The method " + methodName + " occurs excetion:" + e);
    }

    /**
     * 环绕通知需要携带 ProceedingJoinPoint 类型的参数.
     * 环绕通知类似于动态代理的全过程: ProceedingJoinPoint 类型的参数可以决定是否执行目标方法.
     * 且环绕通知必须有返回值, 返回值即为目标方法的返回值
     */

   @Around("loginPointcut()")
   public Object aroundMethod(ProceedingJoinPoint pjd){
      Object result = null;
      String methodName = pjd.getSignature().getName();

      try {
         //前置通知
         System.out.println("The method " + methodName + " begins with " + Arrays.asList(pjd.getArgs()));
         //执行目标方法
         result = pjd.proceed();
         //返回通知
         System.out.println("The method " + methodName + " ends with " + result);
      } catch (Throwable e) {
         //异常通知
         System.out.println("The method " + methodName + " occurs exception:" + e);
         throw new RuntimeException(e);
      }
      //后置通知
      System.out.println("The method " + methodName + " ends");

      return result;
   }
}
```

测试方法

```java
public class AopTest {
    @Test
    public void aopTest(){
        ApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");
        ArithmeticCalculator arithmeticCalculator = (ArithmeticCalculator) ctx.getBean("arithmeticCalculator");

        int result = arithmeticCalculator.add(1, 2);
        System.out.println("result:" + result);

        result = arithmeticCalculator.div(1000, 10);
        System.out.println("result:" + result);
    }
}
```

### 用基于 XML 的配置声明切面

除了使用 AspectJ 注解声明切面, Spring 也支持在 Bean 配置文件中声明切面. 这种声明是通过 aop schema 中的 XML 元素完成的

正常情况下, **基于注解的声明要优先于基于** **XML** 的声明 通过 AspectJ 注解, 切面可以与 AspectJ 兼容, 而基于 XML 的配置则是 Spring 专有的. 由于 AspectJ 得到越来越多的 AOP 框架支持, 所以以注解风格编写的切面将会有更多重用的机会

当使用 XML 声明切面时, 需要在 <beans> 根元素中导入 aop Schema

在 Bean 配置文件中, 所有的 Spring AOP 配置都必须定义在 <aop:config> 元素内部. 对于每个切面而言, 都要创建一个 <aop:aspect>元素来为具体的切面实现引用后端 Bean 实例.

切面 Bean 必须有一个标示符, 供 <aop:aspect> 元素引用

```xml
<!-- 文件扫描器 -->
<context:component-scan base-package="com.harry"/>
<!--注册bean-->
<bean id="userService" class="com.harry.service.impl.UserServiceImpl"/>
<bean id="myAspect" class="com.harry.aspect.MyAspect"/>
<!-- 配置AOP -->
<aop:config>
    <!-- 定义切入点-->
    <aop:pointcut id="addUserPointcut" expression="execution(* com.harry.service.impl.UserServiceImpl.addUser())"/>
    <aop:pointcut id="selectUserPointcut" expression="execution(* com.harry.service.impl.UserServiceImpl.selectUser())"/>
    <aop:pointcut id="selectUserByIdPointcut" expression="execution(* com.harry.service.impl.UserServiceImpl.selectUserByIdU(..))"/>
    <aop:pointcut id="updateUserPointcut" expression="execution(* com.harry.service.impl.UserServiceImpl.updateUser())"/>
    <aop:pointcut id="deleteUserPointcut" expression="execution(* com.harry.service.impl.UserServiceImpl.deleteUser())"/>

    <!-- 定义切面 -->
    <aop:aspect ref="myAspect">
        <!--前置通知-->
        <aop:before method="before" pointcut-ref="addUserPointcut"/>
        <!--返回通知-->
        <aop:after-returning method="afterReturning" pointcut-ref="updateUserPointcut" returning="result"/>
        <!--异常通知-->
        <aop:after-throwing method="afterThrowing" pointcut-ref="selectUserByIdPointcut" throwing="e"/>
        <!--后置通知-->
        <aop:after method="after" pointcut-ref="selectUserPointcut"/>
        <!--环绕通知-->
        <aop:around method="around" pointcut-ref="deleteUserPointcut"/>
    </aop:aspect>
</aop:config>
```

# 六、**Spring** **对** **JDBC** 的支持

## 1、JdbcTemplate 简介

为了使 JDBC 更加易于使用, Spring 在 JDBC API 上定义了一个抽象层, 以此建立一个 JDBC 存取框架.

作为 Spring JDBC 框架的核心, **JDBC** **模板**的设计目的是为不同类型的 JDBC 操作提供**模板方法**. 每个模板方法都能控制整个过程, 并允许覆盖过程中的特定任务. 通过这种方式, 可以在尽可能保留灵活性的情况下, 将数据库存取的工作量降到最低.

依赖导入

```xml
<dependency>
  <groupId>mysql</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>8.0.11</version>
</dependency>

<dependency>
  <groupId>org.springframework</groupId>
  <artifactId>spring-jdbc</artifactId>
  <version>5.2.5.RELEASE</version>
</dependency>

<dependency>
  <groupId>c3p0</groupId>
  <artifactId>c3p0</artifactId>
  <version>0.9.1.2</version>
</dependency>
```

配置文件Application.xml

```xml
<context:component-scan base-package="com.harry.spring"/>
<!-- 导入资源文件 -->
<context:property-placeholder location="classpath:db.properties"/>

<!-- 配置 C3P0 数据源 -->
<bean id="dataSource"
      class="com.mchange.v2.c3p0.ComboPooledDataSource">
    <property name="user" value="${jdbc.user}"></property>
    <property name="password" value="${jdbc.password}"></property>
    <property name="jdbcUrl" value="${jdbc.jdbcUrl}"></property>
    <property name="driverClass" value="${jdbc.driverClass}"></property>

    <property name="initialPoolSize" value="${jdbc.initPoolSize}"></property>
    <property name="maxPoolSize" value="${jdbc.maxPoolSize}"></property>
</bean>
<!-- 配置 Spirng 的 JdbcTemplate -->
<bean id="jdbcTemplate"
      class="org.springframework.jdbc.core.JdbcTemplate">
    <property name="dataSource" ref="dataSource"></property>
</bean>
<!-- 配置 NamedParameterJdbcTemplate, 该对象可以使用具名参数, 其没有无参数的构造器, 所以必须为其构造器指定参数 -->
<bean id="namedJdbcTemplate" class="org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate">
    <constructor-arg name="dataSource" ref="dataSource"></constructor-arg>
</bean>
```

```properties
jdbc.user=root
jdbc.password=123456
jdbc.driverClass=com.mysql.jdbc.Driver
jdbc.jdbcUrl=jdbc:mysql://192.168.0.110:3306/SpringDemo?useUnicode=true&characterEncoding=utf8
jdbc.initPoolSize=5
jdbc.maxPoolSize=10
```

```java
@Repository
public class EmployeeDao {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    public Employee get(Integer id){
        String sql = "SELECT id, lastName lastName, email FROM employees WHERE id = ?";
        RowMapper<Employee> rowMapper = new BeanPropertyRowMapper<>(Employee.class);
        Employee employee = jdbcTemplate.queryForObject(sql, rowMapper, id);
        return employee;
    }
}
```

JdbcTemplate测试

```java
public class JDBCTest {
    private ApplicationContext ctx = null;
    private JdbcTemplate jdbcTemplate;
    private EmployeeDao employeeDao;
    private DepartmentDao departmentDao;
    private NamedParameterJdbcTemplate namedParameterJdbcTemplate;
    {
        ctx = new ClassPathXmlApplicationContext("Application.xml");
        jdbcTemplate = (JdbcTemplate) ctx.getBean("jdbcTemplate");
        employeeDao = ctx.getBean(EmployeeDao.class);
        departmentDao = ctx.getBean(DepartmentDao.class);
        namedParameterJdbcTemplate = ctx.getBean(NamedParameterJdbcTemplate.class);
    }

    /**
     * 执行批量更新: 批量的 INSERT, UPDATE, DELETE
     * 最后一个参数是 Object[] 的 List 类型: 因为修改一条记录需要一个 Object 的数组, 那么多条不就需要多个 Object 的数组吗
     */
    @Test
    public void testBatchUpdate(){
        String sql = "INSERT INTO employees(lastName, email, deptId) VALUES(?,?,?)";

        List<Object[]> batchArgs = new ArrayList<>();
        batchArgs.add(new Object[]{"AA", "aa@harry.com", 1});
        batchArgs.add(new Object[]{"BB", "bb@harry.com", 2});
        batchArgs.add(new Object[]{"CC", "cc@harry.com", 3});
        batchArgs.add(new Object[]{"DD", "dd@harry.com", 3});
        batchArgs.add(new Object[]{"EE", "ee@aharry.com",2});
        jdbcTemplate.batchUpdate(sql,batchArgs);
    }
    /**
     * 插入单条数据
     */
    @Test
    public void testInsertDept(){
        String sql = "INSERT INTO department(name) VALUES(?)";
        jdbcTemplate.update(sql, "财务");
    }

    @Test
    public void testDepartmentDao(){
        Department department = departmentDao.selectById(3);
        System.out.println(department);
    }

    /**
     * 执行 INSERT, UPDATE, DELETE
     */
    @Test
    public void testUpdate(){
        String sql = "UPDATE employees SET last_name = ? WHERE id = ?";
        jdbcTemplate.update(sql, "Jack", 5);
    }

    /**
     * 从数据库中获取一条记录, 实际得到对应的一个对象
     * 注意不是调用 queryForObject(String sql, Class<Employee> requiredType, Object... args) 方法!
     * 而需要调用 queryForObject(String sql, RowMapper<Employee> rowMapper, Object... args)
     * 1. 其中的 RowMapper 指定如何去映射结果集的行, 常用的实现类为 BeanPropertyRowMapper
     * 2. 使用 SQL 中列的别名完成列名和类的属性名的映射. 例如 last_name lastName
     * 3. 不支持级联属性. JdbcTemplate 到底是一个 JDBC 的小工具, 而不是 ORM 框架
     */
    @Test
    public void testQueryForObject(){
        String sql = "SELECT id, lastName, email, deptId as \"department.id\" FROM employees WHERE id = ?";
        RowMapper<Employee> rowMapper = new BeanPropertyRowMapper<>(Employee.class);
        Employee employee = jdbcTemplate.queryForObject(sql, rowMapper, 1);

        System.out.println(employee);
    }

    /**
     * 查到实体类的集合
     * 注意调用的不是 queryForList 方法
     */
    @Test
    public void testQueryForList(){
        String sql = "SELECT id, lastName, email FROM employees WHERE id < ?";
        RowMapper<Employee> rowMapper = new BeanPropertyRowMapper<>(Employee.class);
        List<Employee> employees = jdbcTemplate.query(sql, rowMapper,5);

        System.out.println(employees);
    }

    /**
     * 获取单个列的值, 或做统计查询
     * 使用 queryForObject(String sql, Class<Long> requiredType)
     */
    @Test
    public void testQueryForObject2(){
        String sql = "SELECT count(id) FROM employees";
        long count = jdbcTemplate.queryForObject(sql, Long.class);
        System.out.println(count);
    }
}
```

### 在 JDBC 模板中使用具名参数

```java
/**
 * 使用具名参数时, 可以使用 update(String sql, SqlParameterSource paramSource) 方法进行更新操作
 * 1. SQL 语句中的参数名和类的属性一致!
 * 2. 使用 SqlParameterSource 的 BeanPropertySqlParameterSource 实现类作为参数. 
 */
@Test
public void testNamedParameterJdbcTemplate2(){
	String sql = "INSERT INTO employees(last_name, email, dept_id) "
			+ "VALUES(:lastName,:email,:dpetId)";
	
	Employee employee = new Employee();
	employee.setLastName("XYZ");
	employee.setEmail("xyz@sina.com");
	employee.setDpetId(3);
	
	SqlParameterSource paramSource = new BeanPropertySqlParameterSource(employee);
	namedParameterJdbcTemplate.update(sql, paramSource);
}

/**
 * 可以为参数起名字. 
 * 1. 好处: 若有多个参数, 则不用再去对应位置, 直接对应参数名, 便于维护
 * 2. 缺点: 较为麻烦. 
 */
@Test
public void testNamedParameterJdbcTemplate(){
	String sql = "INSERT INTO employees(last_name, email, dept_id) VALUES(:ln,:email,:deptid)";
	
	Map<String, Object> paramMap = new HashMap<>();
	paramMap.put("ln", "FF");
	paramMap.put("email", "ff@atguigu.com");
	paramMap.put("deptid", 2);
	
	namedParameterJdbcTemplate.update(sql, paramMap);
}
```

## 2、Spring中对事务的支持

作为企业级应用程序框架, **Spring** **在不同的事务管理** **API** **之上定义了一个抽象层**. 而应用程序开发人员不必了解底层的事务管理 API, 就可以使用 Spring 的事务管理机制.

Spring 既支持编程式事务管理, 也支持声明式的事务管理.

编程式事务管理将事务管理代码嵌入到业务方法中来控制事务的提交和回滚 在编程式管理事务时, 必须在每个事务操作中包含额外的事务管理代码.

**声明式事务管理**: 大多数情况下比编程式事务管理更好用. 它**将事务管理代码从业务方法中分离出来**, **以声明的方式来实现事务管理**事务管理作为一种横切关注点, 可以通过 AOP 方法模块化. **Spring** **通过** **Spring AOP** **框架支持声明式事务管理**

Spring 从不同的事务管理 API 中抽象了一整套的事务机制. 开发人员不必了解底层的事务 API, 就可以利用这些事务机制. 有了这些事务机制, **事务管理代码就能独立于特定的事务技术**

Spring 的核心事务管理抽象是Interface Platform  TransactionManager它为事务管理封装了一组独立于技术的方法. 无论使用 Spring 的哪种事务管理策略(编程式或声明式), 事务管理器都是必须的.

### 测试需求

![image-20200518173146090](\images\image-20200518173146090.png)

数据表中的数据

![image-20200518174557146](\images\image-20200518174557146.png)

```java
public interface BookShopDao {

   //根据书号获取书的单价
   public int findBookPriceByIsbn(String isbn);

   //更新数的库存. 使书号对应的库存 - 1
   public void updateBookStock(String isbn);

   //更新用户的账户余额: 使 username 的 balance - price
   public void updateUserAccount(String username, int price);
}
```

```java
@Repository("bookShop")
public class BookShopDaoImpl implements BookShopDao{
    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Override
    public int findBookPriceByIsbn(String isbn) {
        String sql = "SELECT price FROM book WHERE isbn = ?";
        return jdbcTemplate.queryForObject(sql, Integer.class, isbn);
    }

    @Override
    public void updateBookStock(String isbn) {
        //检查书的库存是否足够, 若不够, 则抛出异常
        String sql = "SELECT stock FROM book_stock WHERE isbn= ?";
        Integer stock = jdbcTemplate.queryForObject(sql, Integer.class, isbn);
        if (stock <= 0) {
            throw new BookStockException("库存不足!");
        }
        String sql2 = "UPDATE book_stock SET stock = stock -1 WHERE isbn = ?";
        jdbcTemplate.update(sql2, isbn);
    }

    @Override
    public void updateUserAccount(String username, int price) {
        // 验证余额是否足够, 若不足, 则抛出异常
        String sql2 = "SELECT balance FROM account WHERE username = ?";
        int balance = jdbcTemplate.queryForObject(sql2, Integer.class, username);
        if(balance < price){
            throw new UserAccountException("余额不足!");
        }

        String sql = "UPDATE account SET balance = balance - ? WHERE username = ?";
        jdbcTemplate.update(sql, price, username);
    }
}
```

```java
@Service("bookService")
public class BookShopServiceImpl implements BookShopService{
    @Autowired
    BookShopDao bookShopDao;
    
    // 如果没加事务，那么运行时如果用户余额不足或其他原因导致了异常购买失败，但是库存中的商品仍然会-1。开启事务可解决问题
    @Transactional
    @Override
    public void purchase(String username, String isbn) {
        //1. 获取书的单价
        int price = bookShopDao.findBookPriceByIsbn(isbn);

        //2. 更新数的库存
        bookShopDao.updateBookStock(isbn);

        //3. 更新用户余额
        bookShopDao.updateUserAccount(username, price);
    }
}
```

配置文件

```java
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:aop="http://www.springframework.org/schema/aop"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:tx="http://www.springframework.org/schema/tx"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
            http://www.springframework.org/schema/beans/spring-beans.xsd
            http://www.springframework.org/schema/aop
            http://www.springframework.org/schema/aop/spring-aop.xsd
            http://www.springframework.org/schema/context
            http://www.springframework.org/schema/context/spring-context.xsd
              http://www.springframework.org/schema/tx
              http://www.springframework.org/schema/tx/spring-tx-4.0.xsd">
    <context:component-scan base-package="com.harry.spring"/>
    <!-- 导入资源文件 -->
    <context:property-placeholder location="classpath:db.properties"/>

    <!-- 配置 C3P0 数据源 -->
    <bean id="dataSource"
          class="com.mchange.v2.c3p0.ComboPooledDataSource">
        <property name="user" value="${jdbc.user}"></property>
        <property name="password" value="${jdbc.password}"></property>
        <property name="jdbcUrl" value="${jdbc.jdbcUrl}"></property>
        <property name="driverClass" value="${jdbc.driverClass}"></property>

        <property name="initialPoolSize" value="${jdbc.initPoolSize}"></property>
        <property name="maxPoolSize" value="${jdbc.maxPoolSize}"></property>
    </bean>
    <!-- 配置 Spirng 的 JdbcTemplate -->
    <bean id="jdbcTemplate"
          class="org.springframework.jdbc.core.JdbcTemplate">
        <property name="dataSource" ref="dataSource"></property>
    </bean>

    <bean id="namedJdbcTemplate" class="org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate">
        <constructor-arg name="dataSource" ref="dataSource"></constructor-arg>
    </bean>

    <!-- 配置事务管理器 -->
    <bean id="transactionManager"
          class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
        <property name="dataSource" ref="dataSource"></property>
    </bean>

    <!-- 启用事务注解 -->
    <tx:annotation-driven transaction-manager="transactionManager"/>
</beans>
```

Test

```java
public class SpringTransactionTest {


    private ApplicationContext ctx = null;
    @Autowired
    private BookShopDao bookShopDao;
    @Autowired
    private BookShopService bookShopService;
    @Autowired
    private Cashier cashier;
    {
        ctx = new ClassPathXmlApplicationContext("Application.xml");
        bookShopDao = ctx.getBean(BookShopDao.class);
        bookShopService = ctx.getBean(BookShopService.class);
        cashier = ctx.getBean(Cashier.class);
    }
    @Test
    public void testBookShopService(){
        System.out.println();
        bookShopService.purchase("Tom", "0001");
    }

}
```

### 事务传播属性

当事务方法被另一个事务方法调用时, 必须指定事务应该如何传播. 例如: 方法可能继续在现有事务中运行, 也可能开启一个新事务, 并在自己的事务中运行.

事务的传播行为可以由传播属性指定. Spring 定义了 7  种类传播行为.

![image-20200518212359383](\images\image-20200518212359383.png)

REQUIRED 传播行为

当 bookService 的 purchase() 方法被另一个事务方法 checkout() 调用时, 它默认会在现有的事务内运行. 这个默认的传播行为就是 REQUIRED. 因此在 checkout() 方法的开始和终止边界内只有一个事务. 这个事务只在 checkout() 方法结束的时候被提交, 结果用户一本书都买不了

事务传播属性可以在 @Transactional 注解的 propagation 属性中定义

![image-20200518212643860](\images\image-20200518212643860.png)

REQUIRES_NEW 传播行为

另一种常见的传播行为是 REQUIRES_NEW. 它表示该方法必须启动一个新事务, 并在自己的事务内运行. 如果有事务在运行, 就应该先挂起它.

![image-20200518212757530](\images\image-20200518212757530.png)

```java
@Service("bookShopService")
public class BookShopServiceImpl implements BookShopService {

   @Autowired
   private BookShopDao bookShopDao;

   //添加事务注解
   //1.使用 propagation 指定事务的传播行为, 即当前的事务方法被另外一个事务方法调用时如何使用事务, 默认取值为 REQUIRED, 即使用调用方法的事务
   //REQUIRES_NEW: 事务自己的事务, 调用的事务方法的事务被挂起. 
   //2.使用 isolation 指定事务的隔离级别, 最常用的取值为 READ_COMMITTED
   //3.默认情况下 Spring 的声明式事务对所有的运行时异常进行回滚. 也可以通过对应的属性进行设置. 通常情况下去默认值即可. 
   //4.使用 readOnly 指定事务是否为只读. 表示这个事务只读取数据但不更新数据, 这样可以帮助数据库引擎优化事务. 若真的事一个只读取数据库值的方法, 应设置 readOnly=true
   //5.使用 timeout 指定强制回滚之前事务可以占用的时间.  
// @Transactional(propagation=Propagation.REQUIRES_NEW,
//       isolation=Isolation.READ_COMMITTED,
//       noRollbackFor={UserAccountException.class})
   @Transactional(propagation= Propagation.REQUIRES_NEW,
         isolation= Isolation.READ_COMMITTED,
         readOnly=false,
         timeout=3)
   @Override
   public void purchase(String username, String isbn) {

      try {
         Thread.sleep(5000);
      } catch (InterruptedException e) {}

      //1. 获取书的单价
      int price = bookShopDao.findBookPriceByIsbn(isbn);

      //2. 更新数的库存
      bookShopDao.updateBookStock(isbn);

      //3. 更新用户余额
      bookShopDao.updateUserAccount(username, price);
   }

}
```

### 并发事务所导致的问题

当同一个应用程序或者不同应用程序中的多个事务在同一个数据集上并发执行时, 可能会出现许多意外的问题

并发事务所导致的问题可以分为下面三种类型:

​		–脏读: 对于两个事物 T1, T2, T1 读取了已经被 T2 更新但 还没有被提交的字段. 之后, 若 T2 回滚, T1读取的内容就是临时且无效的.

​		–不可重复读:对于两个事物 T1, T2, T1 读取了一个字段, 然后 T2 更新了该字段. 之后, T1再次读取同一个字段, 值就不同了.

​		–幻读:对于两个事物 T1, T2, T1 从一个表中读取了一个字段, 然后 T2 在该表中插入了一些新的行. 之后, 如果 T1 再次读取同一个表, 就会多出几行.

从理论上来说, 事务应该彼此完全隔离, 以避免并发事务所导致的问题. 然而, 那样会对性能产生极大的影响, 因为事务必须按顺序运行.

在实际开发中, 为了提升性能, 事务会以较低的隔离级别运行.

事务的隔离级别可以通过隔离事务属性指定

![image-20200518213204831](\images\image-20200518213204831.png)

事务的隔离级别要得到底层数据库引擎的支持, 而不是应用程序或者框架的支持.

Oracle 支持的 2 种事务隔离级别：READ_COMMITED , SERIALIZABLE

Mysql 支持 4 中事务隔离级别

### 基于XML配置Spring事务

```xml
<!-- 1. 配置事务管理器 -->
<bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
    <property name="dataSource" ref="dataSource"></property>
</bean>

<!-- 2. 配置事务属性 -->
<tx:advice id="txAdvice" transaction-manager="transactionManager">
    <tx:attributes>
        <!-- 根据方法名指定事务的属性 -->
        <tx:method name="purchase" propagation="REQUIRES_NEW"/>
        <tx:method name="get*" read-only="true"/>
        <tx:method name="find*" read-only="true"/>
        <tx:method name="*"/>
    </tx:attributes>
</tx:advice>

<!-- 3. 配置事务切入点, 以及把事务切入点和事务属性关联起来 -->
<aop:config>
    <aop:pointcut expression="execution(* com.atguigu.spring.tx.xml.service.*.*(..))"
                  id="txPointCut"/>
    <aop:advisor advice-ref="txAdvice" pointcut-ref="txPointCut"/>
</aop:config>
```

# 七、Spring整合 Hibernate

Spring 支持大多数流行的 ORM 框架, 包括 Hibernate JDO, TopLink, Ibatis 和 JPA。

**Spring** **对这些** **ORM** **框架的支持是一致的**, 因此可以把和 Hibernate 整合技术应用到其他 ORM 框架上.

Spring 2.0 同时支持 Hibernate 2.x 和 3.x. 但 Spring 2.5 只支持 Hibernate 3.1 或更高版本

### 在 Spring 中配置 SessionFactory

对于 Hibernate 而言, 必须从原生的 Hibernate API 中构建 SessionFactory. 此外, 应用程序也无法利用 Spring 提供的数据存储机制(例如: Spring 的事务管理机制)

Spring 提供了对应的工厂 Bean, 可以用单实例的形式在 IOC 容器中创建 SessionFactory 实例.

添加依赖

```xml
 <!-- https://mvnrepository.com/artifact/org.hibernate/hibernate-core -->
    <dependency>
      <groupId>org.hibernate</groupId>
      <artifactId>hibernate-core</artifactId>
      <version>5.4.16.Final</version>
    </dependency>


    <!-- 添加Log4J依赖 -->
    <dependency>
      <groupId>log4j</groupId>
      <artifactId>log4j</artifactId>
      <version>1.2.16</version>
    </dependency>

    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-orm</artifactId>
      <version>5.2.5.RELEASE</version>
    </dependency>

    <dependency>
      <groupId>org.slf4j</groupId>
      <artifactId>slf4j-nop</artifactId>
      <version>1.6.4</version>
    </dependency>

    <!-- 添加javassist -->
    <dependency>
      <groupId>javassist</groupId>
      <artifactId>javassist</artifactId>
      <version>3.12.0.GA</version>
     </dependency>
```

Hibernate配置文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE hibernate-configuration PUBLIC
      "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
      "http://hibernate.sourceforge.net/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>

       <!-- 配置 hibernate 的基本属性 -->
       <!-- 1. 数据源需配置到 IOC 容器中, 所以在此处不再需要配置数据源 -->
       <!-- 2. 关联的 .hbm.xml 也在 IOC 容器配置 SessionFactory 实例时在进行配置 -->
       <!-- 3. 配置 hibernate 的基本属性: 方言, SQL 显示及格式化, 生成数据表的策略以及二级缓存等. -->
      <property name="hibernate.dialect">org.hibernate.dialect.MySQL5Dialect</property>

      <property name="hibernate.show_sql">true</property>
      <property name="hibernate.format_sql">true</property>

      <property name="hibernate.hbm2ddl.auto">update</property>

      <!-- 配置 hibernate 二级缓存相关的属性. -->

    </session-factory>
</hibernate-configuration>
```



