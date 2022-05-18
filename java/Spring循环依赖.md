# spring循环依赖题目说明

解释下spring中的三级缓存？
三级缓存分别是什么？三个Map有什么异同？
什么是循环依赖？请你谈谈？看过spring源码吗？
如何检测是否存在循环依赖？实际开发中见过循环依赖的异常吗？
多例的情况下，循环依赖问题为什么无法解决？
什么是循环依赖？

多个bean之间相互依赖，形成了一个闭环。比如：A依赖于B、B依赖于C、C依赖于A。

通常来说，如果问Spring容器内部如何解决循环依赖，一定是指默认的单例Bean中，属性互相引用的场景。


![image-20220517213520682](images\image-20220517213520682.png)

两种注入方式对循环依赖的影响

循环依赖官网说明

> Circular dependencies
>
> If you use predominantly constructor injection, it is possible to create an unresolvable circular dependency scenario.
>
> For example: Class A requires an instance of class B through constructor injection, and class B requires an instance of class A through constructor injection. If you configure beans for classes A and B to be injected into each other, the Spring IoC container detects this circular reference at runtime, and throws a BeanCurrentlyInCreationException.
>
> One possible solution is to edit the source code of some classes to be configured by setters rather than constructors. Alternatively, avoid constructor injection and use setter injection only. In other words, although it is not recommended, you can configure circular dependencies with setter injection.
>
> Unlike the typical case (with no circular dependencies), a circular dependency between bean A and bean B forces one of the beans to be injected into the other prior to being fully initialized itself (a classic chicken-and-egg scenario).link
> 
>

结论

我们AB循环依赖问题只要A的注入方式是setter且singleton ，就不会有循环依赖问题。

# spring循环依赖纯java代码验证案例

Spring容器循环依赖报错演示BeanCurrentlylnCreationException

循环依赖现象在spring容器中注入依赖的对象，有2种情况

- 构造器方式注入依赖（不可行）
- 以set方式注入依赖（可行）

构造器方式注入依赖（不可行）

```java
@Component
public class ServiceA {
    private ServiceB serviceB;

    public ServiceA(ServiceB serviceB){
        this.serviceB = serviceB;
    }
}

```

```java
@Component
public class ServiceB {
    private ServiceA serviceA;

    public ServiceB(ServiceA serviceA){
        this.serviceA = serviceA;
    }
}
```

```java
public class ClientConstructor {
    public static void main(String[] args){
        //这会抛出编译异常
        new ServiceA(new ServiceB(new ServiceA()));
    }
}
```

以set方式注入依赖（可行）

```java
@Component
public class ServiceA {
    private ServiceB serviceB;

    public ServiceB getServiceB() {
        return serviceB;
    }

    public void setServiceB(ServiceB serviceB) {
        this.serviceB = serviceB;
    }
}

```

```java

@Component
public class ServiceB {
    private ServiceA serviceA;

    public ServiceA getServiceA() {
        return serviceA;
    }

    public void setServiceA(ServiceA serviceA) {
        this.serviceA = serviceA;
    }
}

```

```java
public class ClientConstructor {
    public static void main(String[] args){
            //创建serviceAA
            ServiceA a = new ServiceA();
            //创建serviceBB
            ServiceB b = new ServiceB();
            //将serviceA入到serviceB中
            b.setServiceA(a);
            //将serviceB法入到serviceA中
            a.setServiceB(b);
    }
}
```

输出结果：

B里面设置了A
A里面设置了B

## spring循环依赖bug演示

beans：A，B

```java

public class A {

    private B b;

    public B getB() {
        return b;
    }

    public void setB(B b) {
        this.b = b;
        System.out.println("A call setB.");
    }
}

```

```java
public class B {
    private A a;

    public A getA() {
        return a;
    }

    public void setA(A a) {
        this.a = a;
        System.out.println("B call setA.");
    }
}

```

运行类

```java
package com.harry.spring.serivce;

import org.springframework.context.support.ClassPathXmlApplicationContext;

public class ClientSpringContainer {
    public static void main(String[] args) {
        ClassPathXmlApplicationContext applicationContext = new ClassPathXmlApplicationContext("beans.xml");
        applicationContext.getBean("a", A.class);
        applicationContext.getBean("b", B.class);
    }
}

```

默认的单例(Singleton)的场景是**支持**循环依赖的，不报错

pom

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>SpringCircleDependency</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>8</maven.compiler.source>
        <maven.compiler.target>8</maven.compiler.target>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-context</artifactId>
            <version>5.2.8.RELEASE</version>
            <scope>compile</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-tx</artifactId>
            <version>5.3.0</version>
        </dependency>
        <dependency>
            <groupId>ch.qos.logback</groupId>
            <artifactId>logback-core</artifactId>
            <version>1.1.3</version>
        </dependency>

        <dependency>
            <groupId>ch.qos.logback</groupId>
            <artifactId>logback-access</artifactId>
            <version>1.1.3</version>
        </dependency>

        <dependency>
            <groupId>ch.qos.logback</groupId>
            <artifactId>logback-classic</artifactId>
            <version>1.1.3</version>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-aop</artifactId>
            <version>5.3.0</version>
        </dependency>
    </dependencies>
</project>
```

beans.xml

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:p="http://www.springframework.org/schema/p"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:aop="http://www.springframework.org/schema/aop" xmlns:tx="http://www.springframework.org/schema/tx"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans-4.0.xsd
       http://www.springframework.org/schema/context
       http://www.springframework.org/schema/context/spring-context-4.0.xsd
       http://www.springframework.org/schema/tx
       http://www.springframework.org/schema/tx/spring-tx-4.0.xsd
       http://www.springframework.org/schema/aop
       http://www.springframework.org/schema/aop/spring-aop-4.0.xsd">

    <bean id="a" class="com.harry.spring.serivce.A">
        <property name="b" ref="b"></property>
    </bean>
    <bean id="b" class="com.harry.spring.serivce.B">
        <property name="a" ref="a"></property>
    </bean>

</beans>
```

输出结果

![image-20220517222047206](images\image-20220517222047206.png)



beans.xml

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:p="http://www.springframework.org/schema/p"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:aop="http://www.springframework.org/schema/aop" xmlns:tx="http://www.springframework.org/schema/tx"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans-4.0.xsd
       http://www.springframework.org/schema/context
       http://www.springframework.org/schema/context/spring-context-4.0.xsd
       http://www.springframework.org/schema/tx
       http://www.springframework.org/schema/tx/spring-tx-4.0.xsd
       http://www.springframework.org/schema/aop
       http://www.springframework.org/schema/aop/spring-aop-4.0.xsd">

    <bean id="a" class="com.harry.spring.serivce.A" scope="prototype">
        <property name="b" ref="b" ></property>
    </bean>
    <bean id="b" class="com.harry.spring.serivce.B" scope="prototype">
        <property name="a" ref="a"></property>
    </bean>

</beans>
```

输出结果

![image-20220517222557825](images\image-20220517222557825.png)

重要结论(spring内部通过3级缓存来解决循环依赖) - DefaultSingletonBeanRegistry

只有单例的bean会通过三级缓存提前暴露来解决循环依赖的问题，而非单例的bean，每次从容器中获取都是一个新的对象，都会重新创建，所以非单例的bean是没有缓存的，不会将其放到三级缓存中。

第一级缓存（也叫单例池）singletonObjects：存放已经经历了完整生命周期的Bean对象。

第二级缓存：earlySingletonObjects，存放早期暴露出来的Bean对象，Bean的生命周期未结束（属性还未填充完。

第三级缓存：Map<String, ObjectFactory<?>> singletonFactories，存放可以生成Bean的工厂
![image-20220517222750114](images\image-20220517222750114.png)

## spring循环依赖debug前置知识

实例化 - 内存中申请一块内存空间，如同租赁好房子，自己的家当还未搬来。

初始化属性填充 - 完成属性的各种赋值，如同装修，家具，家电进场。

3个Map和四大方法，总体相关对象

![image-20220517222913311](images\image-20220517222913311.png)

第一层singletonObjects存放的是已经初始化好了的Bean,

第二层earlySingletonObjects存放的是实例化了，但是未初始化的Bean,

第三层singletonFactories存放的是FactoryBean。假如A类实现了FactoryBean,那么依赖注入的时候不是A类，而是A类产生的Bean


```java
package org.springframework.beans.factory.support;

...

public class DefaultSingletonBeanRegistry extends SimpleAliasRegistry implements SingletonBeanRegistry {

	...

	/** 
	单例对象的缓存:bean名称—bean实例，即:所谓的单例池。
	表示已经经历了完整生命周期的Bean对象
	第一级缓存
	*/
	private final Map<String, Object> singletonObjects = new ConcurrentHashMap<>(256);

	/**
	早期的单例对象的高速缓存: bean名称—bean实例。
	表示 Bean的生命周期还没走完（Bean的属性还未填充）就把这个 Bean存入该缓存中也就是实例化但未初始化的 bean放入该缓存里
	第二级缓存
	*/
	private final Map<String, Object> earlySingletonObjects = new HashMap<>(16);

	/**
	单例工厂的高速缓存:bean名称—ObjectFactory
	表示存放生成 bean的工厂
	第三级缓存
	*/
	private final Map<String, ObjectFactory<?>> singletonFactories = new HashMap<>(16);
 
    ...
    
}

```

A / B两对象在三级缓存中的迁移说明

A创建过程中需要B，于是A将自己放到三级缓里面，去实例化B。

B实例化的时候发现需要A，于是B先查一级缓存，没有，再查二级缓存，还是没有，再查三级缓存，找到了A然后把三级缓存里面的这个A放到二级缓存里面，并删除三级缓存里面的A。

B顺利初始化完毕，将自己放到一级缓存里面（此时B里面的A依然是创建中状态)，然后回来接着创建A，此时B已经创建结束，直接从一级缓存里面拿到B，然后完成创建，并将A自己放到一级缓存里面。


```java
@FunctionalInterface
public interface ObjectFactory<T> {

	T getObject() throws BeansException;

}

```

## 循环依赖debug源码01

DEBUG一步一步来，scope默认为singleton

从运行类启航

在new ClassPathXmlApplicationContext带上一个断点

![image-20220517223453973](images\image-20220517223453973.png)

进入refresh方法 这是spring中的核心方法

![image-20220517223717124](images\image-20220517223717124.png)

![image-20220517223828314](images\image-20220517223828314.png)

进入到this.finishBeanFactoryInitialization(beanFactory); 这个方法 会实例化单例的bean

![image-20220517224024930](images\image-20220517224024930.png)

走到 beanFactory.preInstantiateSingletons()

![image-20220517224301603](images\image-20220517224301603.png)



## spring循环依赖debug源码02

beanFactory是ConfigurableListableBeanFactory

DefaultListableBeanFactory实现了ConfigurableListableBeanFactory接口

![image-20220517224437757](images\image-20220517224437757.png)

*点关注点是这里*    源于AbstractAutowireCapableBeanFactory---->AbstractBeanFactory的getBean()

当前的beanname 是a

![image-20220517224841731](images\image-20220517224841731.png)

进入dogetbean， 在spring中前面带do的方法说明就要进入实际干活的方法

![image-20220517225009876](images\image-20220517225009876.png)

源于FactoryBeanRegistrySupport  ----> DefaultSingletonBeanRegistry的getSingleton()---->  DefaultSingletonBeanRegistry也就是上文谈论的三级缓存所在类

getsingleton() 会先尝试从一级缓存获取当前的bean a 当然目前肯定是获取不到的

![image-20220517225351653](images\image-20220517225351653.png)

![image-20220517225417820](images\image-20220517225417820.png)

RootBeanDefinition相当于是bean定义信息保存在这个里面

![image-20220517225644532](images\image-20220517225644532.png)

mbd.isSingleton()返回true，执行下面if语块， 重点关注， 

```java
sharedInstance = getSingleton(beanName, () -> {
						try {
--------------------------->//<---------------------重点关注点是这里
							return createBean(beanName, mbd, args);
						}

```

![image-20220517231058613](images\image-20220517231058613.png)

这里有调用一次getsingleton(beanName，lambda函数）

这里还是尝试先从一级缓存获取bean 结果是null

![image-20220517231526104](images\image-20220517231526104.png)

执行到 singeltonFactory.getObject()方法会执行之前穿进来的lamba表达式 里面方法会执行createBean

![image-20220518001136465](images\image-20220518001136465.png)

![image-20220518001208604](images\image-20220518001208604.png)

进入createBean之后又调用了doCreateBean

![image-20220517232537953](images\image-20220517232537953.png)



doCreateBean中创建Bean对象实例

![image-20220518000056497](images\image-20220518000056497.png)

createBeanInstance里面利用反射将Bean a实例化出来

![image-20220518000257648](images\image-20220518000257648.png)

继续走doCreateBean这里会将 lamba表达式放到三级缓存里面

![image-20220518000550411](images\image-20220518000550411.png)

![image-20220518000641388](images\image-20220518000641388.png)

![image-20220518000743480](images\image-20220518000743480.png)



在doCeateBean里面有一个populateBean方法 ，这个方法会给当前bean a进行属性赋值

![image-20220517232720023](C:\Users\cs1\AppData\Roaming\Typora\typora-user-images\image-20220517232720023.png)

在poplulateBean方法里面最下面代码里面有个是需要对b bean进行赋值

![image-20220517232942846](images\image-20220517232942846.png)

进入applyPropertyValues 方法 后找到resolveValues方法

![image-20220517233843841](C:\Users\cs1\AppData\Roaming\Typora\typora-user-images\image-20220517233843841.png)

之后进入到这段代码

![image-20220517234034740](images\image-20220517234034740.png)

在这个方法里面发现因为a对象里面有一个b的属性 所以这里又调用了doGetBean尝试获取B对象

![image-20220517234141066](images\image-20220517234141066.png)

这里调用doGetBean尝试获取B对象

![image-20220517231748232](images\image-20220517231748232.png)

调用getsiongleton 主要这里再次调用beanName是b

![image-20220517231831201](images\image-20220517231831201.png)

后面的过程基本与创建a 相同

这里在装配b对象属性的时候 发现有属性是依赖于a的

![image-20220517234620243](images\image-20220517234620243.png)

注意这里又调用了getBean 但是这时的beanName又变成了a

![image-20220518210542146](images\image-20220518210542146.png)

![image-20220517234812881](images\image-20220517234812881.png)

![image-20220517234836212](images\image-20220517234836212.png)

这时候有一次走到DefaultSingletonBeanRegistry的getSingleton方法，因为之前a第一次进来时会将lamba的创建a对象的工厂放到三级缓存所以这里会从三级缓存获取到这个lamba表达式并执行后将创建好的对象放到二级缓存（这时候a还是半成品） 并从三级缓存中移除a

![image-20220517235251142](images\image-20220517235251142.png)

beanB获取beanA

![image-20220518211424986](images\image-20220518211424986.png)

由于a对象第一次已经添加了缓存，所以这里不为空并将三级缓存移动到二级

![image-20220518211123290](C:\Users\cs1\AppData\Roaming\Typora\typora-user-images\image-20220518211123290.png)

这里就或取到了bean a对象， 但是这个的a应该这是被实例化了 并没有进行属性赋值后面还会走到populateBean（beanA）

![image-20220518211542215](images\image-20220518211542215.png)

又回到了populateBean来装配bean

![image-20220518211854366](images\image-20220518211854366.png)



这里应该是从二级缓存获取b对象（没太看懂猜的）

![image-20220518213243242](C:\Users\cs1\AppData\Roaming\Typora\typora-user-images\image-20220518213243242.png)

这里走到b对象创建流程的addSingleton（beanB， singletonObject）

![image-20220518213438138](C:\Users\cs1\AppData\Roaming\Typora\typora-user-images\image-20220518213438138.png)

这里把b对象从二级缓存移除并放入了一级缓存

![image-20220518213655756](C:\Users\cs1\AppData\Roaming\Typora\typora-user-images\image-20220518213655756.png)

这里有走到getObjectForBeanInstance(.... beanB)  最终返回了对象b

![image-20220518214325884](images\image-20220518214325884.png)

![image-20220518214426022](images\image-20220518214426022.png)

![image-20220518214525357](images\image-20220518214525357.png)

这里返回到了a对象的populateBean

![image-20220518214738180](images\image-20220518214738180.png)

这里对a对象进行了初始化

![image-20220518214823433](images\image-20220518214823433.png)

进入addSingleton（beanA， singletonObject）

![image-20220518215250052](images\image-20220518215250052.png)

![image-20220518215356276](images\image-20220518215356276.png)

这里获取getSingleton返回获取到了a对象， 然后进入getObjectForBeanInstance（... beanA）

![image-20220518215543835](images\image-20220518215543835.png)

![image-20220518215701838](images\image-20220518215701838.png)

到此a和b对象就全部创建完成了



## 总结

![image-20220518220002423](images\image-20220518220002423.png)

1 调用doGetBean()方法，想要获取beanA，于是调用getSingleton()方法从缓存中查找beanA

2 在getSingleton()方法中，从一级缓存中查找，没有，返回null

3 doGetBean()方法中获取到的beanA为null，于是走对应的处理逻辑，调用getSingleton()的重载方法（参数为ObjectFactory的)

4 在getSingleton()方法中，先将beanA_name添加到一个集合中，用于标记该bean正在创建中。然后回调匿名内部类的creatBean方法

5 进入AbstractAutowireCapableBeanFactory#doCreateBean，先反射调用构造器创建出beanA的实例，然后判断。是否为单例、是否允许提前暴露引用(对于单例一般为true)、是否正在创建中〈即是否在第四步的集合中)。判断为true则将beanA添加到【三级缓存】中

6 对beanA进行属性填充，此时检测到beanA依赖于beanB，于是开始查找beanB

7 调用doGetBean()方法，和上面beanA的过程一样，到缓存中查找beanB，没有则创建，然后给beanB填充属性

8 此时beanB依赖于beanA，调用getsingleton()获取beanA，依次从一级、二级、三级缓存中找，此时从三级缓存中获取到beanA的创建工厂，通过创建工厂获取到singletonObject，此时这个singletonObject指向的就是上面在doCreateBean()方法中实例化的beanA

9 这样beanB就获取到了beanA的依赖，于是beanB顺利完成实例化，并将beanA从三级缓存移动到二级缓存中

10 随后beanA继续他的属性填充工作，此时也获取到了beanB，beanA也随之完成了创建，回到getsingleton()方法中继续向下执行，将beanA从二级缓存移动到一级缓存中