# 一、Spring注解开发简介

![在这里插入图片描述](images\spring-annotation.jpg)

根据上面这张脑图，我把整个专栏分成了三个大的部分，分别是：容器、扩展原理以及Web。

## 容器

容器作为整个专栏的第一大部分，内容包括：

AnnotationConfigApplicationContext
组件添加
组件赋值
组件注入
AOP
声明式事务

## 扩展原理

扩展原理作为整个专栏的第二大部分，内容包括：

BeanFactoryPostProcessor
BeanDefinitionRegistryPostProcessor
ApplicationListener
Spring容器创建过程(源码原理重要)

## Web

Web作为整个专栏的第三大部分，内容包括：

servlet3.0
异步请求



# 二、给容器中注册组件

## Spring IOC和DI

在Spring容器的底层，最重要的功能就是IOC和DI，也就是控制反转和依赖注入。

![image-20210831192313370](images\image-20210831192313370.png)

DI和IOC它俩之间的关系是DI不能单独存在，DI需要在IOC的基础上来完成。

在Spring内部，所有的组件都会放到IOC容器中，组件之间的关系通过IOC容器来自动装配，也就是我们所说的依赖注入。接下来，我们就使用注解的方式来完成容器中组件的注册、管理及依赖、注入等功能。

## Configuration和@Bean

添加bean

```java
package com.harry.spring.bean;

public class Person {
    private String name;
    private Integer age;

    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public Integer getAge() {
        return age;
    }
    public void setAge(Integer age) {
        this.age = age;
    }
    public Person(String name, Integer age) {
        super();
        this.name = name;
        this.age = age;
    }
    public Person() {
        super();
        // TODO Auto-generated constructor stub
    }
    @Override
    public String toString() {
        return "Person [name=" + name + ", age=" + age + "]";
    }

}
```

### 通过注解注入JavaBean

通过XML配置文件的方式，我们可以将JavaBean注入到Spring的IOC容器中。那使用注解又该如何实现呢？别急，其实使用注解比使用XML配置文件要简单的多，我们在项目的com.meimeixia.config包下创建一个MainConfig类，并在该类上添加@Configuration注解来标注该类是一个Spring的配置类，也就是告诉Spring它是一个配置类，最后通过@Bean注解将Person类注入到Spring的IOC容器中。

```java
package com.harry.spring.config;

import com.harry.spring.bean.Person;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration // 告诉Spring这是一个配置类
public class MainConfig {
    //@Bean注解是给IOC容器中注册一个bean，类型就是返回值类型，id默认用方法名
    @Bean
    public Person person(){
        return new Person("cs", 18);
    }
}
```

然后，我们修改MainTest类中的main方法，以测试通过注解注入的Person类，如下所示。

```java
import com.harry.spring.bean.Person;
import com.harry.spring.config.MainConfig;
import javafx.application.Application;
import org.junit.Test;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class MainTest {
    @Test
    public void testAnnotation(){
        ApplicationContext applicationContext = new AnnotationConfigApplicationContext(MainConfig.class);
        Person person = applicationContext.getBean(Person.class);
        System.out.println(person);
    }
}
Person [name=cs, age=18]
```

可以看出，通过注解将Person类注入到了Spring的IOC容器中。

到这里，我们已经明确了，通过XML配置文件和注解这两种方式都可以将JavaBean注入到Spring的IOC容器中。那么，使用注解将JavaBean注入到IOC容器中时，使用的bean的名称又是什么呢？我们可以在MainTest类的main方法中添加如下代码来获取Person这个类型的组件在IOC容器中的名字

```java
String[] namesForType = applicationContext.getBeanNamesForType(Person.class);
for (String name : namesForType) {
    System.out.println(name);
}
```

## 使用@ComponentScan

在实际项目中，我们更多的是使用Spring的包扫描功能对项目中的包进行扫描，凡是在指定的包或其子包中的类上标注了@Repository、@Service、@Controller、@Component注解的类都会被扫描到，并将这个类注入到Spring容器中。

Spring包扫描功能可以使用XML配置文件进行配置，也可以直接使用@ComponentScan注解进行设置，使用@ComponentScan注解进行设置比使用XML配置文件来配置要简单的多。


```java
@Configuration // 告诉Spring这是一个配置类
@ComponentScan(value = "com.harry.spring")
public class MainConfig {
    //@Bean注解是给IOC容器中注册一个bean，类型就是返回值类型，id默认用方法名
    @Bean
    public Person person(){
        return new Person("cs",18);
    }
}
```

### 关于@ComponentScan注解

这里，我们着重来看ComponentScan类中的如下两个方法。

![image-20210831195453917](images\image-20210831195453917.png)

includeFilters()方法指定Spring扫描的时候按照什么规则只需要包含哪些组件，而excludeFilters()方法指定Spring扫描的时候按照什么规则排除哪些组件。两个方法的返回值都是Filter[]数组，在ComponentScan注解类的内部存在Filter注解类


### 扫描时排除注解标注的类

现在有这样一个需求，除了@Controller和@Service标注的组件之外，IOC容器中剩下的组件我都要，即相当于是我要排除@Controller和@Service这俩注解标注的组件。要想达到这样一个目的，我们可以在MainConfig类上通过@ComponentScan注解的excludeFilters()方法实现。例如，我们在MainConfig类上添加了如下的注解。

```java
@Configuration // 告诉Spring这是一个配置类
@ComponentScan(value="com.harry.spring", excludeFilters={
        /*
         * type：指定你要排除的规则，是按照注解进行排除，还是按照给定的类型进行排除，还是按照正则表达式进行排除，等等
         * classes：除了@Controller和@Service标注的组件之外，IOC容器中剩下的组件我都要，即相当于是我要排除@Controller和@Service这俩注解标注的组件。
         */
        @ComponentScan.Filter(type= FilterType.ANNOTATION, classes={Controller.class, Service.class})
}) // value指定要扫描的包

public class MainConfig {
    //@Bean注解是给IOC容器中注册一个bean，类型就是返回值类型，id默认用方法名
    @Bean
    public Person person(){
        return new Person("cs",18);
    }
}
```

### 扫描时只包含注解标注的类

我们也可以使用ComponentScan注解类中的includeFilters()方法来指定Spring在进行包扫描时，只包含哪些注解标注的类。

这里需要注意的是，当我们使用includeFilters()方法来指定只包含哪些注解标注的类时，需要禁用掉默认的过滤规则。 还记得我们以前在XML配置文件中配置这个只包含的时候，应该怎么做吗？我们需要在XML配置文件中先配置好use-default-filters="false"，也就是禁用掉默认的过滤规则，因为默认的过滤规则就是扫描所有的，只有我们禁用掉默认的过滤规则之后，只包含才能生效。

```java
@ComponentScan(value="com.harry.spring", includeFilters={
        /*
         * type：指定你要排除的规则，是按照注解进行排除，还是按照给定的类型进行排除，还是按照正则表达式进行排除，等等
         * classes：我们需要Spring在扫描时，只包含@Controller注解标注的类
         */
        @Filter(type=FilterType.ANNOTATION, classes={Controller.class})
}, useDefaultFilters=false) // value指定要扫描的包
```

```java
public class MainTest {
    @Test
    public void testAnnotation(){
        ApplicationContext applicationContext = new AnnotationConfigApplicationContext(MainConfig.class);
        Person person = applicationContext.getBean(Person.class);
        System.out.println(person);

        String[] namesForType = applicationContext.getBeanDefinitionNames();
        for (String name : namesForType) {
            System.out.println(name);
        }

    }
}
// 输出 mainConfig bookController  person
```

## 自定义TypeFilter指定@ComponentScan注解的过滤规则

### FilterType.ANNOTATION：按照注解进行包含或者排除

例如，使用@ComponentScan注解进行包扫描时，如果要想按照注解只包含标注了@Controller注解的组件，那么就需要像下面这样写了。

### FilterType.ASSIGNABLE_TYPE：按照给定的类型进行包含或者排除

例如，使用@ComponentScan注解进行包扫描时，如果要想按照给定的类型只包含BookService类（接口）或其子类（实现类或子接口）的组件，那么就需要像下面这样写了。

### FilterType.ASPECTJ：按照ASPECTJ表达式进行包含或者排除

例如，使用@ComponentScan注解进行包扫描时，按照正则表达式进行过滤，就得像下面这样子写。

### FilterType.REGEX：按照正则表达式进行包含或者排除

例如，使用@ComponentScan注解进行包扫描时，按照正则表达式进行过滤，就得像下面这样子写。

### FilterType.CUSTOM：按照自定义规则进行包含或者排除

如果实现自定义规则进行过滤时，自定义规则的类必须是org.springframework.core.type.filter.TypeFilter接口的实现类。

要想按照自定义规则进行过滤，首先我们得创建org.springframework.core.type.filter.TypeFilter接口的一个实现类，例如MyTypeFilter，该实现类的代码一开始如下所示。

```java
package com.harry.spring.config;

import org.springframework.core.type.classreading.MetadataReader;
import org.springframework.core.type.classreading.MetadataReaderFactory;
import org.springframework.core.type.filter.TypeFilter;

import java.io.IOException;

public class MyTypeFilter implements TypeFilter {
    /**
     * 参数：
     * metadataReader：读取到的当前正在扫描的类的信息
     * metadataReaderFactory：可以获取到其他任何类的信息的（工厂）
     */
    public boolean match(MetadataReader metadataReader, MetadataReaderFactory metadataReaderFactory) throws IOException {
        return false;
    }
}
```

当我们实现TypeFilter接口时，需要实现该接口中的match()方法，match()方法的返回值为boolean类型。当返回true时，表示符合规则，会包含在Spring容器中；当返回false时，表示不符合规则，那就是一个都不匹配，自然就都不会被包含在Spring容器中。另外，在match()方法中存在两个参数，分别为MetadataReader类型的参数和MetadataReaderFactory类型的参数，含义分别如下。

​	metadataReader：读取到的当前正在扫描的类的信息
​	metadataReaderFactory：可以获取到其他任何类的信息的工厂
然后，使用@ComponentScan注解进行如下配置。

```java
@ComponentScan(value="com.harry.spring", includeFilters={
        /*
         * type：指定你要排除的规则，是按照注解进行排除，还是按照给定的类型进行排除，还是按照正则表达式进行排除，等等
         */
        // 指定新的过滤规则，这个过滤规则是我们自个自定义的，过滤规则就是由我们这个自定义的MyTypeFilter类返回true或者false来代表匹配还是没匹配
        @Filter(type= FilterType.CUSTOM, classes={MyTypeFilter.class})
}, useDefaultFilters=false) // value指定要扫描的包
```

## 使用@Scope注解设置组件的作用域

Spring容器中的组件默认是单例的，在Spring启动时就会实例化并初始化这些对象，并将其放到Spring容器中，之后，每次获取对象时，直接从Spring容器中获取，而不再创建对象。如果每次从Spring容器中获取对象时，都要创建一个新的实例对象，那么该如何处理呢？此时就需要使用@Scope注解来设置组件的作用域了。
从@Scope注解类的源码中可以看出，在@Scope注解中可以设置如下值：

​	1 ConfigurableBeanFactory#SCOPE_PROTOTYPE
​	2 ConfigurableBeanFactory#SCOPE_SINGLETON
​	3 org.springframework.web.context.WebApplicationContext#SCOPE_REQUEST
​	4 org.springframework.web.context.WebApplicationContext#SCOPE_SESSION
很明显，在@Scope注解中可以设置的值包括ConfigurableBeanFactory接口中的SCOPE_PROTOTYPE和SCOPE_SINGLETON，以及WebApplicationContext类中的SCOPE_REQUEST和SCOPE_SESSION

SCOPE_SINGLETON就是singleton，而SCOPE_PROTOTYPE就是prototype。

![image-20210831202444985](images\image-20210831202444985.png)

### 单实例bean作用域

首先，我们在com.harry.spring.config包下创建一个配置类，例如MainConfig2，然后在该配置类中实例化一个Person对象，并将其放置在Spring容器中，如下所示。

```java
@Configuration
public class MainConfig2 {
    @Bean("Person2")
    public Person person(){
        return new Person("harry", 25);
    }
}
```

接着，在IOCTest类中创建一个test02()测试方法，在该测试方法中创建一个AnnotationConfigApplicationContext对象，创建完毕后，从Spring容器中按照id获取两个Person对象，并判断这两个对象是否是同一个对象，代码如下所示。

```java
@Test
public void test02(){
    ApplicationContext applicationContext = new AnnotationConfigApplicationContext(MainConfig2.class);
    // 获取到的这个Person对象默认是单实例的，因为在IOC容器中给我们加的这些组件默认都是单实例的，
    // 所以说在这儿我们无论多少次获取，获取到的都是我们之前new的那个实例对象
    Person person = (Person) applicationContext.getBean("Person2");
    Person person2 = (Person) applicationContext.getBean("Person2");
    System.out.println(person == person2);
}
```

由于对象在Spring容器中默认是单实例的，所以，Spring容器在启动时就会将实例对象加载到Spring容器中，之后，每次从Spring容器中获取实例对象，都是直接将对象返回，而不必再创建新的实例对象了。很显然，此时运行test02()方法之后会输出true

### 多实例bean作用域

修改Spring容器中组件的作用域，我们需要借助于@Scope注解。此时，我们将MainConfig2配置类中Person对象的作用域修改成prototype，如下所示。

```java
@Configuration
public class MainConfig2 {
    @Bean("Person2")
    @Scope("prototype") // 通过@Scope注解来指定该bean的作用范围，也可以说成是调整作用域
    public Person person(){
        return new Person("harry", 25);
    }
}
```

### 单实例bean作用域何时创建对象？

接下来，我们验证下在单实例作用域下，Spring是在什么时候创建对象的？

首先，我们将MainConfig2配置类中的Person对象的作用域修改成单实例，并在返回Person对象之前打印相关的信息，如下所示。

```java
@Configuration
public class MainConfig2 {
    @Bean("Person2")
    @Scope("prototype") // 通过@Scope注解来指定该bean的作用范围，也可以说成是调整作用域
    public Person person(){
        System.out.println("给容器中添加咱们这个Person对象...");
        return new Person("harry", 25);
    }
}
```

然后，我们在IOCTest类中再创建一个test03()方法，在该方法中我们只创建Spring容器，如下所示。

```java
@Test
public void test03() {
    AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext(MainConfig2.class);
}
```

此时，我们运行IOCTest类中的test03()方法，输出的结果信息如下所示。

```
// 给容器中添加咱们这个Person对象...
```

从以上输出的结果信息中可以看出，Spring容器在创建的时候，就将@Scope注解标注为singleton的组件进行了实例化，并加载到了Spring容器中。

这说明，Spring容器在启动时，将单实例组件实例化之后，会即刻加载到Spring容器中，以后每次从容器中获取组件实例对象时，都是直接返回相应的对象，而不必再创建新的对象了。

### 单实例bean注意的事项

单实例bean是整个应用所共享的，所以需要考虑到线程安全问题，之前在玩SpringMVC的时候，SpringMVC中的Controller默认是单例的，有些开发者在Controller中创建了一些变量，那么这些变量实际上就变成共享的了，Controller又可能会被很多线程同时访问，这些线程并发去修改Controller中的共享变量，此时很有可能会出现数据错乱的问题，所以使用的时候需要特别注意。

### 多实例bean注意的事项

多实例bean每次获取的时候都会重新创建，如果这个bean比较复杂，创建时间比较长，那么就会影响系统的性能，因此这个地方需要注意点。

## 懒加载

Spring在启动时，默认会将单实例bean进行实例化，并加载到Spring容器中去。也就是说，单实例bean默认是在Spring容器启动的时候创建对象，并且还会将对象加载到Spring容器中。如果我们需要对某个bean进行延迟加载，那么该如何处理呢？此时，就需要使用到@Lazy注解了

### 非懒加载模式

这里我们先来看看非懒加载这种模式。首先，我们将MainConfig2配置类中Person对象的作用域修改成单实例，如下所示。

```java
@Configuration
public class MainConfig2 {
    @Bean("Person2")
    public Person person(){
        System.out.println("给容器中添加咱们这个Person对象...");
        return new Person("harry", 25);
    }
}
```

然后，在IOCTest类中创建一个test05()方法，如下所示。

```java
@Test
public void test05() {
    AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext(MainConfig2.class);
    System.out.println("IOC容器创建完成");
}
```

接着，运行IOCTest类中的test05()方法，输出的结果信息如下所示。

![image-20210831210137492](images\image-20210831210137492.png)

### 懒加载模式

我们再来看看懒加载这种模式。首先，我们在MainConfig2配置类中的person()方法上加上一个@Lazy注解，以此将Person对象设置为懒加载，如下所示。

```java
@Configuration
public class MainConfig2 {
    @Bean("Person2")
    @Lazy
    public Person person(){
        System.out.println("给容器中添加咱们这个Person对象...");
        return new Person("harry", 25);
    }
}
```

然后，我们再次运行IOCTest类中的test05()方法，输出的结果信息如下所示。

![image-20210831210320718](images\image-20210831210320718.png)

可以看到，此时只是打印出了`IOC容器创建完成`这样一条信息，说明此时只创建了IOC容器，而并没有创建bean对象。

那么，加上@Lazy注解后，bean对象是何时被创建的呢？我们可以试着在IOCTest类中的test05()方法中获取一下Person对象，如下所示。

懒加载，也称延时加载，仅针对单实例bean生效。 单实例bean是在Spring容器启动的时候加载的，添加@Lazy注解后就会延迟加载，在Spring容器启动的时候并不会加载，而是在第一次使用此bean的时候才会加载，但当你多次获取bean的时候并不会重复加载，只是在第一次获取的时候才会加载，这不是延迟加载的特性，而是单实例bean的特性

## 按照条件向Spring容器中注册bean

当bean是单实例，并且没有设置懒加载时，Spring容器启动时，就会实例化bean，并将bean注册到IOC容器中，以后每次从IOC容器中获取bean时，直接返回IOC容器中的bean，而不用再创建新的bean了。

若bean是单实例，并且使用@Lazy注解设置了懒加载，则Spring容器启动时，不会立即实例化bean，自然就不会将bean注册到IOC容器中了，只有第一次获取bean的时候，才会实例化bean，并且将bean注册到IOC容器中。

若bean是多实例，则Spring容器启动时，不会实例化bean，也不会将bean注册到IOC容器中，只是在以后每次从IOC容器中获取bean的时候，都会创建一个新的bean返回。

其实，Spring支持按照条件向IOC容器中注册bean，满足条件的bean就会被注册到IOC容器中，不满足条件的bean就不会被注册到IOC容器中。

### @Conditional注解概述

Conditional注解可以按照一定的条件进行判断，满足条件向容器中注册bean，不满足条件就不向容器中注册bean。

@Conditional注解是由Spring Framework提供的一个注解，它位于 org.springframework.context.annotation包内，定义如下。

![image-20210904091058948](images\image-20210904091058948.png)

从@Conditional注解的源码来看，@Conditional注解不仅可以添加到类上，也可以添加到方法上。在@Conditional注解中，还存在着一个Condition类型或者其子类型的Class对象数组

```java
package org.springframework.context.annotation;

import org.springframework.core.type.AnnotatedTypeMetadata;

@FunctionalInterface
public interface Condition {
    boolean matches(ConditionContext var1, AnnotatedTypeMetadata var2);
}
```

可以看到，它是一个接口。所以，我们使用@Conditional注解时，需要写一个类来实现Spring提供的Condition接口，它会匹配@Conditional所符合的方法（这句话怎么说的那么不明白啊！），然后我们就可以使用我们在@Conditional注解中定义的类来检查了。

我们可以在哪些场合使用@Conditional注解呢？@Conditional注解的使用场景如下图所示。
![image-20210904091233885](images\image-20210904091233885.png)

### 向Spring容器注册bean

现在，我们就要提出一个新的需求了，比如，如果当前操作系统是Windows操作系统，那么就向Spring容器中注册名称为bill的Person对象；如果当前操作系统是Linux操作系统，那么就向Spring容器中注册名称为linus的Person对象。要想实现这个需求，我们就得要使用@Conditional注解了。

要想使用@Conditional注解，我们需要实现Condition接口来为@Conditional注解设置条件，所以，这里我们创建了两个实现Condition接口的类，它们分别是LinuxCondition和WindowsCondition，如下所示。

#### LinuxCondition

```java
package com.harry.spring.condition;

import org.springframework.beans.factory.config.ConfigurableListableBeanFactory;
import org.springframework.beans.factory.support.BeanDefinitionRegistry;
import org.springframework.context.annotation.Condition;
import org.springframework.context.annotation.ConditionContext;
import org.springframework.core.env.Environment;
import org.springframework.core.type.AnnotatedTypeMetadata;

public class LinuxCondition implements Condition {
    /**
     * ConditionContext：判断条件能使用的上下文（环境）
     * AnnotatedTypeMetadata：当前标注了@Conditional注解的注释信息
     */
    public boolean matches(ConditionContext context, AnnotatedTypeMetadata annotatedTypeMetadata) {
        // 判断操作系统是否是Linux系统

        // 1. 获取到bean的创建工厂（能获取到IOC容器使用到的BeanFactory，它就是创建对象以及进行装配的工厂）
        ConfigurableListableBeanFactory beanFactory = context.getBeanFactory();
        // 2. 获取到类加载器
        ClassLoader classLoader = context.getClassLoader();
        // 3. 获取当前环境信息，它里面就封装了我们这个当前运行时的一些信息，包括环境变量，以及包括虚拟机的一些变量
        Environment environment = context.getEnvironment();
        // 4. 获取到bean定义的注册类
        BeanDefinitionRegistry registry = context.getRegistry();
	    // 在这儿还可以做更多的判断，比如说我判断一下Spring容器中是不是包含有某一个bean，就像下面这样，如果Spring容器中果真包含有名称为person的bean，那么就做些什么事情...
        boolean definition = registry.containsBeanDefinition("person");
        String property = environment.getProperty("os.name");
        if (property.contains("linux")) {
            return true;
        }

        return false;

    }
}
```

这里通过context的getRegistry()方法获取到的bean定义的注册对象，即BeanDefinitionRegistry对象。它到底是个啥呢？我们可以点进去看一下它的源码，如下所示，可以看到它是一个接口。

![image-20210904091707901](images\image-20210904091707901.png)

在上图中我对BeanDefinitionRegistry接口的源码作了一点简要的说明。知道了，Spring容器中所有的bean都可以通过BeanDefinitionRegistry对象来进行注册，因此我们可以通过它来查看Spring容器中到底注册了哪些bean。而且仔细查看一下BeanDefinitionRegistry接口中声明的各个方法，你就知道我们还可以通过BeanDefinitionRegistry对象向Spring容器中注册一个bean、移除一个bean、查询某一个bean的定义信息或者判断Spring容器中是否包含有某一个bean的定义。

因此，我们可以在这儿做更多的判断，比如说我可以判断一下Spring容器中是不是包含有某一个bean，就像下面这样，如果Spring容器中果真包含有名称为person的bean，那么就做些什么事情，如果没包含，那么我们还可以利用BeanDefinitionRegistry对象向Spring容器中注册一个bean

#### WindowsCondition

```java
public class WindowsCondition implements Condition {
    /**
     * ConditionContext：判断条件能使用的上下文（环境）
     * AnnotatedTypeMetadata：当前标注了@Conditional注解的注释信息
     */
    public boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata) {
        Environment environment = context.getEnvironment();
        String property = environment.getProperty("os.name");
        if (property.contains("Windows")) {
            return true;
        }
        return false;
    }

}
```

然后，我们就需要在MainConfig2配置类中使用@Conditional注解添加条件了。添加该注解后的方法如下所示。

#### Mainconfig

```java
package com.harry.spring.config;

import com.harry.spring.bean.Person;
import com.harry.spring.condition.LinuxCondition;
import com.harry.spring.condition.WindowsCondition;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Conditional;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MainConfig3 {

    @Bean("bill")
    @Conditional({WindowsCondition.class})
    public Person person01(){
        return new Person("Bill Gates", 62);
    }
    @Bean("linus")
    @Conditional(LinuxCondition.class)
    public Person person2(){
        return new Person("Linus", 48);
    }
}
```

#### Test

```java
@Test public void test06(){
    AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext(MainConfig3.class);
    System.out.println("IOC容器创建完成");
    String[] namesForType = applicationContext.getBeanDefinitionNames();
    for (String name : namesForType) {
        System.out.println(name);
    }

}
```

### @Conditional的扩展注解

![在这里插入图片描述](images\condition_all.jpg)

## 使用@Import注解

我们可以将一些bean组件交由Spring来管理，并且Spring还支持单实例bean和多实例bean。我们自己写的类，自然是可以通过包扫描+给组件标注注解（@Controller、@Servcie、@Repository、@Component）的形式将其注册到IOC容器中，但这种方式比较有局限性，局限于我们自己写的类，比方说我们自己写的类，我们当然能把以上这些注解标注上去了。

那么如果不是我们自己写的类，比如说我们在项目中会经常引入一些第三方的类库，我们需要将这些第三方类库中的类注册到Spring容器中，该怎么办呢？此时，我们就可以使用@Bean和@Import注解将这些类快速的导入Spring容器中。

### 注册bean的方式

向Spring容器中注册bean通常有以下几种方式：

​	包扫描+给组件标注注解（@Controller、@Servcie、@Repository、@Component），但这种方式比较有局限性，局限于我们自己写的类
​	@Bean注解，通常用于导入第三方包中的组件
​	@Import注解，快速向Spring容器中导入一个组件

### @Import注解概述

Spring 3.0之前，创建bean可以通过XML配置文件与扫描特定包下面的类来将类注入到Spring IOC容器内。而在Spring 3.0之后提供了JavaConfig的方式，也就是将IOC容器里面bean的元信息以Java代码的方式进行描述，然后我们可以通过@Configuration与@Bean这两个注解配合使用来将原来配置在XML文件里面的bean通过Java代码的方式进行描述。
@Import注解提供了@Bean注解的功能，同时还有XML配置文件里面标签组织多个分散的XML文件的功能，当然在这里是组织多个分散的@Configuration，因为一个配置类就约等于一个XML配置文件。

```JAVA
package org.springframework.context.annotation;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface Import {
    Class<?>[] value();
}
```

从源码里面可以看出@Import可以配合Configuration、ImportSelector以及ImportBeanDefinitionRegistrar来使用，下面的or表示也可以把Import当成普通的bean来使用。

注意：@Import注解只允许放到类上面，不允许放到方法上。@Import注解的使用方式

### @Import注解的三种用法主要包括：

1. 直接填写class数组的方式
2. **ImportSelector接口的方式，即批量导入，这是重点**
3. ImportBeanDefinitionRegistrar接口方式，即手工注册bean到容器中

### @Import导入组件的简单示例

首先，我们在MainConfig2配置类上添加一个@Import注解，并将Color类填写到该注解中，如下所示。

```java
@Configuration
@Import({Color.class}) // 满足当前条件，这个类中配置的所有bean注册才能生效
public class MainConfig2 {
    @Bean("Person2")
    @Lazy
    public Person person(){
        System.out.println("给容器中添加咱们这个Person对象...");
        return new Person("harry", 25);
    }
}
```

@Import注解还支持同时导入多个类，例如，我们再次创建一个Red类，如下所示。

然后，我们也将以上Red类添加到@Import注解中，如下所示。

```java
@Configuration
@Import({Color.class, Red.class}) // 满足当前条件，这个类中配置的所有bean注册才能生效
public class MainConfig2 {
    @Bean("Person2")
    @Lazy
    public Person person(){
        System.out.println("给容器中添加咱们这个Person对象...");
        return new Person("harry", 25);
    }
}
```

### 在@Import注解中使用ImportSelector接口导入bean

#### ImportSelector接口概述

ImportSelector接口是Spring中导入外部配置的核心接口，在Spring Boot的自动化配置和@EnableXXX（功能性注解）都有它的存在。我们先来看一下ImportSelector接口的源码，如下所示。

```java
package org.springframework.context.annotation;

import org.springframework.core.type.AnnotationMetadata;

public interface ImportSelector {
    String[] selectImports(AnnotationMetadata var1);
}
```

该接口文档上说的明明白白，其主要作用是收集需要导入的配置类，selectImports()方法的返回值就是我们向Spring容器中导入的类的全类名。如果该接口的实现类同时实现EnvironmentAware，BeanFactoryAware，BeanClassLoaderAware或者ResourceLoaderAware，那么在调用其selectImports()方法之前先调用上述接口中对应的方法，如果需要在所有的@Configuration处理完再导入时，那么可以实现DeferredImportSelector接口。

在ImportSelector接口的selectImports()方法中，存在一个AnnotationMetadata类型的参数，这个参数能够获取到当前标注@Import注解的类的所有注解信息，也就是说不仅能获取到@Import注解里面的信息，还能获取到其他注解的信息。

#### ImportSelector接口实例

首先，我们创建一个MyImportSelector类实现ImportSelector接口，如下所示，先在selectImports()方法中返回null，后面我们再来改。

```java
public class MyImportSelector implements ImportSelector {
    // 返回值：就是要导入到容器中的组件的全类名
    // AnnotationMetadata：当前标注@Import注解的类的所有注解信息，也就是说不仅能获取到@Import注解里面的信息，还能获取到其他注解的信息
    public String[] selectImports(AnnotationMetadata annotationMetadata) {
        return null;
    }
}
```

然后，在MainConfig2配置类的@Import注解中，导入MyImportSelector类，如下所示。

```JAVA
@Configuration
@Import({Color.class, Red.class, MyImportSelector.class}) // 满足当前条件，这个类中配置的所有bean注册才能生效
public class MainConfig2  {
    @Bean("Person2")
    @Lazy
    public Person person(){
        System.out.println("给容器中添加咱们这个Person对象...");
        return new Person("harry", 25);
    }
}
```

至于使用MyImportSelector类要导入哪些bean，就需要你在MyImportSelector类的selectImports()方法中进行设置了，只须在MyImportSelector类的selectImports()方法中返回要导入的类的全类名（包名+类名）即可。

接着，我们就要运行IOCTest类中的testImport()方法了，在运行该方法之前，咱们先在MyImportSelector类的selectImports()方法处打一个断点，debug调试一下，如下图所示。

![image-20210904100416049](images\image-20210904100416049.png)

打好断点之后，我们再以debug的方式来运行IOCTest类中的testImport()方法。

![image-20210904100956652](images\image-20210904100956652.png)

可以清楚地看到，selectImports()方法中的AnnotationMetadata类型的参数确实获取到了当前标注@Import注解的类的所有注解信息

此时，执行下一步代码控制台打印了一个空指针异常。

为什么会报这样一个空指针异常呢？我们可以再次debug进入到源码中

![image-20210904101156659](images\image-20210904101156659.png)

![image-20210904101335901](images\image-20210904101335901.png)

接着按住F7键进入asSourceClasses()方法中，可以看到该方法中的String[]数组参数是null，当调用null数组的length时，自然而然就会报一个空指针异常了。

![image-20210904101435300](D:\studyDoc\java\images\image-20210904101435300.png)

因此要想不报这样一个空指针异常，咱们MyImportSelector类的selectImports()方法里面就不能返回一个null值了，不妨先返回一个空数组试试，就像下面这样。

```java
public class MyImportSelector implements ImportSelector {
    // 返回值：就是要导入到容器中的组件的全类名
    // AnnotationMetadata：当前标注@Import注解的类的所有注解信息，也就是说不仅能获取到@Import注解里面的信息，还能获取到其他注解的信息
    public String[] selectImports(AnnotationMetadata annotationMetadata) {
        // 方法不要返回null值，否则会报空指针异常
        return new String[]{}; // 可以返回一个空数组
    }
}
```

接下来，我们就来创建两个Java类，它们分别是Bule类和Yellow类，如下所示。

然后，我们将以上两个类的全类名返回到MyImportSelector类的selectImports()方法中，此时，MyImportSelector类的selectImports()方法如下所示。

```java
public class MyImportSelector implements ImportSelector {
    // 返回值：就是要导入到容器中的组件的全类名
    // AnnotationMetadata：当前标注@Import注解的类的所有注解信息，也就是说不仅能获取到@Import注解里面的信息，还能获取到其他注解的信息
    public String[] selectImports(AnnotationMetadata annotationMetadata) {
        // 方法不要返回null值，否则会报空指针异常
        return new String[]{"com.harry.spring.bean.Yellow", "com.harry.spring.bean.Bule"}; // 可以返回一个空数组
    }
}
```

![image-20210904101751135](images\image-20210904101751135.png)

这说明使用ImportSelector接口的方式已经成功将Bule类和Yellow类导入到Spring容器中去了。

### 在@Import注解中使用ImportBeanDefinitionRegistrar向容器中注册bean

#### ImportBeanDefinitionRegistrar接口的简要介绍

我们先来看看ImportBeanDefinitionRegistrar是个什么鬼，点击进入ImportBeanDefinitionRegistrar源码，如下所示。

```java
package org.springframework.context.annotation;

import org.springframework.beans.factory.support.BeanDefinitionRegistry;
import org.springframework.core.type.AnnotationMetadata;

public interface ImportBeanDefinitionRegistrar {
    void registerBeanDefinitions(AnnotationMetadata var1, BeanDefinitionRegistry var2);
}
```

由源码可以看出，ImportBeanDefinitionRegistrar本质上是一个接口。在ImportBeanDefinitionRegistrar接口中，有一个registerBeanDefinitions()方法，通过该方法，我们可以向Spring容器中注册bean实例。

Spring官方在动态注册bean时，大部分套路其实是使用ImportBeanDefinitionRegistrar接口。

所有实现了该接口的类都会被ConfigurationClassPostProcessor处理，ConfigurationClassPostProcessor实现了BeanFactoryPostProcessor接口，所以ImportBeanDefinitionRegistrar中动态注册的bean是优先于依赖其的bean初始化的，也能被aop、validator等机制处理。


#### 使用方法

ImportBeanDefinitionRegistrar需要配合@Configuration和@Import这俩注解，其中，@Configuration注解定义Java格式的Spring配置文件，@Import注解导入实现了ImportBeanDefinitionRegistrar接口的类。

#### ImportBeanDefinitionRegistrar接口实例

既然ImportBeanDefinitionRegistrar是一个接口，那我们就创建一个MyImportBeanDefinitionRegistrar类，去实现ImportBeanDefinitionRegistrar接口，如下所示。

可以看到，这里，我们先创建了MyImportBeanDefinitionRegistrar类的大体框架。然后，我们在MainConfig2配置类上的@Import注解中，添加MyImportBeanDefinitionRegistrar类，如下所示。

```java
@Configuration
@Import({Color.class, Red.class, MyImportSelector.class, MyImportBeanDefinitionRegistrar.class}) // 满足当前条件，这个类中配置的所有bean注册才能生效
public class MainConfig2  {
    @Bean("Person2")
    @Lazy
    public Person person(){
        System.out.println("给容器中添加咱们这个Person对象...");
        return new Person("harry", 25);
    }
}
```

接着，创建一个RainBow类，作为测试ImportBeanDefinitionRegistrar接口的bean来使用

紧接着，我们就要实现MyImportBeanDefinitionRegistrar类中的registerBeanDefinitions()方法里面的逻辑了，添加逻辑后的registerBeanDefinitions()方法如下所示。

```java
public class MyImportBeanDefinitionRegistrar  implements ImportBeanDefinitionRegistrar {
    /**
     * AnnotationMetadata：当前类的注解信息
     * BeanDefinitionRegistry：BeanDefinition注册类
     *
     * 我们可以通过调用BeanDefinitionRegistry接口中的registerBeanDefinition方法，手动注册所有需要添加到容器中的bean
     */
    public void registerBeanDefinitions(AnnotationMetadata annotationMetadata, BeanDefinitionRegistry beanDefinitionRegistry) {
        boolean definition = beanDefinitionRegistry.containsBeanDefinition("com.harry.spring.bean.Red");
        boolean definition2 = beanDefinitionRegistry.containsBeanDefinition("com.harry.spring.bean.Bule");
        if (definition && definition2) {
            // 指定bean的定义信息，包括bean的类型、作用域等等
            // RootBeanDefinition是BeanDefinition接口的一个实现类
            RootBeanDefinition beanDefinition = new RootBeanDefinition(RainBow.class); // bean的定义信息
            // 注册一个bean，并且指定bean的名称
            beanDefinitionRegistry.registerBeanDefinition("rainBow", beanDefinition);
        }

    }
}
```

## 使用FactoryBean向Spring容器中注册bean

### FactoryBean概述

一般情况下，Spring是通过反射机制利用bean的class属性指定实现类来实例化bean的。在某些情况下，实例化bean过程比较复杂，如果按照传统的方式，那么则需要在标签中提供大量的配置信息，配置方式的灵活性是受限的，这时采用编码的方式可以得到一个更加简单的方案。Spring为此提供了一个org.springframework.bean.factory.FactoryBean的工厂类接口，用户可以通过实现该接口定制实例化bean的逻辑。

FactoryBean接口对于Spring框架来说占有非常重要的地位，Spring自身就提供了70多个FactoryBean接口的实现。它们隐藏了实例化一些复杂bean的细节，给上层应用带来了便利。从Spring 3.0开始，FactoryBean开始支持泛型，即接口声明改为FactoryBean的形式


![image-20210905091106603](images\image-20210905091106603.png)

T getObject()：返回由FactoryBean创建的bean实例，如果isSingleton()返回true，那么该实例会放到Spring容器中单实例缓存池中
boolean isSingleton()：返回由FactoryBean创建的bean实例的作用域是singleton还是prototype
Class getObjectType()：返回FactoryBean创建的bean实例的类型

这里，需要注意的是：当配置文件中标签的class属性配置的实现类是FactoryBean时，通过 getBean()方法返回的不是FactoryBean本身，而是FactoryBean#getObject()方法所返回的对象，相当于FactoryBean#getObject()代理了getBean()方法。

### FactoryBean案例

首先，创建一个ColorFactoryBean类，它得实现FactoryBean接口，如下所示。

```java
import org.springframework.beans.factory.FactoryBean;

/**
 * 创建一个Spring定义的FactoryBean
 * T（泛型）：指定我们要创建什么类型的对象
 *
 */
public class ColorFactoryBean implements FactoryBean<Color> {

    // 返回一个Color对象，这个对象会添加到容器中
    public Color getObject() throws Exception {
        // TODO Auto-generated method stub
        System.out.println("ColorFactoryBean...getObject...");
        return new Color();
    }
    
    public Class<?> getObjectType() {
        // TODO Auto-generated method stub
        return Color.class; // 返回这个对象的类型
    }

    // 是单例吗？
    // 如果返回true，那么代表这个bean是单实例，在容器中只会保存一份；
    // 如果返回false，那么代表这个bean是多实例，每次获取都会创建一个新的bean
    public boolean isSingleton() {
        // TODO Auto-generated method stub
        return false;
    }

}
```

然后，我们在MainConfig2配置类中加入ColorFactoryBean的声明，如下所示。

```java
@Configuration
@Import({Color.class, Red.class, MyImportSelector.class, MyImportBeanDefinitionRegistrar.class}) // 满足当前条件，这个类中配置的所有bean注册才能生效
public class MainConfig2  {
    @Bean("Person2")
    @Lazy
    public Person person(){
        System.out.println("给容器中添加咱们这个Person对象...");
        return new Person("harry", 25);
    }
    @Bean
    public ColorFactoryBean colorFactoryBean(){
        return new ColorFactoryBean();
    }
}
```

这里需注意的是：我在这里使用@Bean注解向Spring容器中注册的是ColorFactoryBean对象。

那现在我们就来看看Spring容器中到底都有哪些bean。我们所要做的事情就是，运行IOCTest类中的testImport()方法，此时，输出的结果信息如下所示。

![image-20210905091553301](images\image-20210905091553301.png)

可以看到，结果信息中输出了一个colorFactoryBean，我们看下这个colorFactoryBean到底是个什么鬼！此时，我们对IOCTest类中的testImport()方法稍加改动，添加获取colorFactoryBean的代码，并输出colorFactoryBean实例的类型，如下所示。

再次运行IOCTest类中的testImport()方法，发现输出的结果信息如下所示。

![image-20210905091727548](images\image-20210905091727548.png)

可以看到，虽然我在代码中使用@Bean注解注入的是ColorFactoryBean对象，但是实际上从Spring容器中获取到的bean对象却是调用ColorFactoryBean类中的getObject()方法获取到的Color对象。

# 三、Bean的生命周期

## 使用@Bean注解指定初始化和销毁的方法

### bean的生命周期

通常意义上讲的bean的生命周期，指的是bean从创建到初始化，经过一系列的流程，最终销毁的过程。只不过，在Spring中，bean的生命周期是由Spring容器来管理的。在Spring中，我们可以自己来指定bean的初始化和销毁的方法。我们指定了bean的初始化和销毁方法之后，当容器在bean进行到当前生命周期的阶段时，会自动调用我们自定义的初始化和销毁方法。


我们就介绍第一种定义初始化和销毁方法的方式：**通过@Bean注解指定初始化和销毁方法**。

如果是使用XML配置文件的方式配置bean的话，那么可以在标签中指定bean的初始化和销毁方法，如下所示。

```xml
<bean id="person" class="com.meimeixia.bean.Person" init-method="init" destroy-method="destroy">
    <property name="age" value="18"></property>
    <property name="name" value="liayun"></property>
</bean>
```

这里，需要注意的是，在我们自己写的Person类中，需要存在init()方法和destroy()方法。而且Spring中还规定，这里的init()方法和destroy()方法必须是无参方法，但可以抛出异常。

使用注解的方式，首先，创建一个名称为Car的类，这个类的实现比较简单，如下所示。

```java
public class Car {
    public Car() {
        System.out.println("car constructor...");
    }

    public void init() {
        System.out.println("car ... init...");
    }

    public void destroy() {
        System.out.println("car ... destroy...");
    }

}
```

然后，我们将Car类对象通过注解的方式注册到Spring容器中，具体的做法就是新建一个MainConfigOfLifeCycle类作为Spring的配置类，将Car类对象通过MainConfigOfLifeCycle类注册到Spring容器中，MainConfigOfLifeCycle类的代码如下所示。


```java
@Configuration
public class MainConfigOfLifeCycle {
    @Bean
    public Car car() {
        return new Car();
    }
}
```

接着，我们就新建一个IOCTest_LifeCycle类来测试容器中的Car对象，该测试类的代码如下所示。

```java
@Test
public void test07(){
    AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext(MainConfigOfLifeCycle.class);
    System.out.println("IOC容器创建完成");
    String[] namesForType = applicationContext.getBeanDefinitionNames();
    for (String name : namesForType) {
        System.out.println(name);
    }

}
```

![image-20210905092612633](images\image-20210905092612633.png)

可以看到，在Spring容器创建完成时，会自动调用单实例bean的构造方法，对单实例bean进行了实例化操作。

我们得在MainConfigOfLifeCycle配置类的@Bean注解中指定initMethod属性和destroyMethod属性，如下所示。

```java
@Configuration
public class MainConfigOfLifeCycle {
    @Bean(initMethod="init", destroyMethod="destroy")
    public Car car() {
        return new Car();
    }
}
```

会发现输出的结果信息如下所示。

![image-20210905092828141](images\image-20210905092828141.png)

#### 指定初始化和销毁方法的使用场景

一个典型的使用场景就是对于数据源的管理。例如，在配置数据源时，在初始化的时候，会对很多的数据源的属性进行赋值操作；在销毁的时候，我们需要对数据源的连接等信息进行关闭和清理。这个时候，我们就可以在自定义的初始化和销毁方法中来做这些事情了！

#### 初始化和销毁方法调用的时机

bean对象的初始化方法调用的时机：对象创建完成，如果对象中存在一些属性，并且这些属性也都赋好值之后，那么就会调用bean的初始化方法。对于单实例bean来说，在Spring容器创建完成后，Spring容器会自动调用bean的初始化方法；对于多实例bean来说，在每次获取bean对象的时候，调用bean的初始化方法。

bean对象的销毁方法调用的时机：对于单实例bean来说，在容器关闭的时候，会调用bean的销毁方法；对于多实例bean来说，Spring容器不会管理这个bean，也就不会自动调用这个bean的销毁方法了。不过，小伙伴们可以手动调用多实例bean的销毁方法。


## 使用InitializingBean和DisposableBean来管理bean的生命周期

### InitializingBean接口概述

Spring中提供了一个InitializingBean接口，该接口为bean提供了属性初始化后的处理方法，它只包括afterPropertiesSet方法，凡是继承该接口的类，在bean的属性初始化后都会执行该方法。InitializingBean接口的源码如下所示。

![image-20210905093234839](images\image-20210905093234839.png)

根据InitializingBean接口中提供的afterPropertiesSet()方法的名字不难推断出，afterPropertiesSet()方法是在属性赋好值之后调用的。

### 调用InitializingBean接口

我们定位到Spring中的org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory这个类里面的invokeInitMethods()方法中，来查看Spring加载bean的方法。

我们来到AbstractAutowireCapableBeanFactory类中的invokeInitMethods()方法处，如下所示。

![在这里插入图片描述](images\123213312.jpg)

分析上述代码后，我们可以初步得出如下信息：

1. Spring为bean提供了两种初始化的方式，实现InitializingBean接口（也就是要实现该接口中的afterPropertiesSet方法），或者在配置文件或@Bean注解中通过init-method来指定，两种方式可以同时使用。
2. 实现InitializingBean接口是直接调用afterPropertiesSet()方法，与通过反射调用init-method指定的方法相比，效率相对来说要高点。但是init-method方式消除了对Spring的依赖。
3. 如果调用afterPropertiesSet方法时出错，那么就不会调用init-method指定的方法了。

也就是说Spring为bean提供了两种初始化的方式，第一种方式是实现InitializingBean接口（也就是要实现该接口中的afterPropertiesSet方法），第二种方式是在配置文件或@Bean注解中通过init-method来指定，这两种方式可以同时使用，同时使用先调用afterPropertiesSet方法，后执行init-method指定的方法。

### DisposableBean接口概述

实现org.springframework.beans.factory.DisposableBean接口的bean在销毁前，Spring将会调用DisposableBean接口的destroy()方法。也就是说我们可以实现DisposableBean这个接口来定义咱们这个销毁的逻辑。
![image-20210905093757853](images\image-20210905093757853.png)

可以看到，在DisposableBean接口中只定义了一个destroy()方法。

在bean生命周期结束前调用destroy()方法做一些收尾工作，亦可以使用destroy-method。前者与Spring耦合高，使用类型强转.方法名()，效率高；后者耦合低，使用反射，效率相对来说较低。

### DisposableBean接口注意事项

多实例bean的生命周期不归Spring容器来管理，这里的DisposableBean接口中的方法是由Spring容器来调用的，所以如果一个多实例bean实现了DisposableBean接口是没有啥意义的，因为相应的方法根本不会被调用，当然了，在XML配置文件中指定了destroy方法，也是没有任何意义的。所以，在多实例bean情况下，Spring是不会自动调用bean的销毁方法的。

### 单实例bean案例

首先，创建一个Cat的类来实现InitializingBean和DisposableBean这俩接口，代码如下所示，注意该Cat类上标注了一个@Component注解。

```java
@Component
public class Cat implements InitializingBean, DisposableBean {

    public Cat() {
        System.out.println("cat constructor...");
    }

    /**
     * 会在容器关闭的时候进行调用
     */
    public void destroy() throws Exception {
        // TODO Auto-generated method stub
        System.out.println("cat destroy...");
    }

    /**
     * 会在bean创建完成，并且属性都赋好值以后进行调用
     */
    public void afterPropertiesSet() throws Exception {
        // TODO Auto-generated method stub
        System.out.println("cat afterPropertiesSet...");
    }

}
```

然后，在MainConfigOfLifeCycle配置类中通过包扫描的方式将以上类注入到Spring容器中。

```java
@Configuration
@ComponentScan(value = {"com.harry.spring.bean"})
public class MainConfigOfLifeCycle {
    @Bean(initMethod="init", destroyMethod="destroy")
    public Car car() {
        return new Car();
    }
}
```

![image-20210905094320632](images\image-20210905094320632.png)

从输出的结果信息中可以看出，单实例bean情况下，IOC容器创建完成后，会自动调用bean的初始化方法；而在容器销毁前，会自动调用bean的销毁方法。

### @PostConstruct注解

PostConstruct注解好多人以为是Spring提供的，其实它是Java自己的注解，是JSR-250规范里面定义的一个注解。我们来看下@PostConstruct注解的源码，如下所示。

![image-20210905094627906](images\image-20210905094627906.png)

从源码可以看出，@PostConstruct注解是Java中的注解，并不是Spring提供的注解。

@PostConstruct注解被用来修饰一个非静态的void()方法。被@PostConstruct注解修饰的方法会在服务器加载Servlet的时候运行，并且只会被服务器执行一次。被@PostConstruct注解修饰的方法通常在构造函数之后，init()方法之前执行。

通常我们是会在Spring框架中使用到@PostConstruct注解的，该注解的方法在整个bean初始化中的执行顺序如下：

​	Constructor（构造方法）→@Autowired（依赖注入）→@PostConstruct（注释的方法）


### @PreDestroy注解

@PreDestroy注解同样是Java提供的，它也是JSR-250规范里面定义的一个注解。看下它的源码，如下所示。

![image-20210905094741831](images\image-20210905094741831.png)

被@PreDestroy注解修饰的方法会在服务器卸载Servlet的时候运行，并且只会被服务器调用一次，类似于Servlet的destroy()方法。被@PreDestroy注解修饰的方法会在destroy()方法之后，Servlet被彻底卸载之前执行。执行顺序如下所示：

​	调用destroy()方法→@PreDestroy→destroy()方法→bean销毁

## BeanPostProcessor后置处理器

### BeanPostProcessor后置处理器概述

首先，我们来看下BeanPostProcessor的源码

![image-20210905095105824](images\image-20210905095105824.png)

从源码可以看出，BeanPostProcessor是一个接口，其中有两个方法，即postProcessBeforeInitialization和postProcessAfterInitialization这两个方法，这两个方法分别是在Spring容器中的bean初始化前后执行，所以Spring容器中的每一个bean对象初始化前后，都会执行BeanPostProcessor接口的实现类中的这两个方法。

也就是说，postProcessBeforeInitialization方法会在bean实例化和属性设置之后，自定义初始化方法之前被调用，而postProcessAfterInitialization方法会在自定义初始化方法之后被调用。当容器中存在多个BeanPostProcessor的实现类时，会按照它们在容器中注册的顺序执行。对于自定义的BeanPostProcessor实现类，还可以让其实现Ordered接口自定义排序。


### BeanPostProcessor后置处理器实例

我们创建一个MyBeanPostProcessor类，实现BeanPostProcessor接口，如下所示。

```java
@Component // 将后置处理器加入到容器中，这样的话，Spring就能让它工作了
public class MyBeanPostProcessor implements BeanPostProcessor {

    public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
        // TODO Auto-generated method stub
        System.out.println("postProcessBeforeInitialization..." + beanName + "=>" + bean);
        return bean;
    }


    public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
        // TODO Auto-generated method stub
        System.out.println("postProcessAfterInitialization..." + beanName + "=>" + bean);
        return bean;
    }

}
```

接下来，我们应该是要编写测试用例来进行测试了。不过，在这之前，咱们得做几处改动，第一处改动是将MainConfigOfLifeCycle配置类中的car()方法上的`@Scope("prototype")`注解给注释掉，因为咱们之前做测试的时候，是将Car对象设置成多实例bean了。

此时，运行IOCTest_LifeCycle类中的test01()方法，输出的结果信息如下所示。

![image-20210905100002187](images\image-20210905100002187.png)

可以看到，postProcessBeforeInitialization方法会在bean实例化和属性设置之后，自定义初始化方法之前被调用，而postProcessAfterInitialization方法会在自定义初始化方法之后被调用。

当然了，也可以让我们自己写的MyBeanPostProcessor类来实现Ordered接口自定义排序，如下所示。


```java
@Component // 将后置处理器加入到容器中，这样的话，Spring就能让它工作了
public class MyBeanPostProcessor implements BeanPostProcessor, Order {

    public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
        // TODO Auto-generated method stub
        System.out.println("postProcessBeforeInitialization..." + beanName + "=>" + bean);
        return bean;
    }


    public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
        // TODO Auto-generated method stub
        System.out.println("postProcessAfterInitialization..." + beanName + "=>" + bean);
        return bean;
    }

    public int value() {
        return 3;
    }

    public Class<? extends Annotation> annotationType() {
        return null;
    }
}
```

### BeanPostProcessor后置处理器作用

后置处理器可用于bean对象初始化前后进行逻辑增强。Spring提供了BeanPostProcessor接口的很多实现类，例如AutowiredAnnotationBeanPostProcessor用于@Autowired注解的实现，AnnotationAwareAspectJAutoProxyCreator用于Spring AOP的动态代理等等。


除此之外，我们还可以自定义BeanPostProcessor接口的实现类，在其中写入咱们需要的逻辑。下面会以AnnotationAwareAspectJAutoProxyCreator为例，简单说明一下后置处理器是怎样工作的。

我们都知道spring AOP的实现原理是动态代理，最终放入容器的是代理类的对象，而不是bean本身的对象，那么Spring是什么时候做到这一步的呢？就是在AnnotationAwareAspectJAutoProxyCreator后置处理器的postProcessAfterInitialization方法中，即bean对象初始化完成之后，后置处理器会判断该bean是否注册了切面，若是，则生成代理对象注入到容器中。这一部分的关键代码是在哪儿呢？我们定位到AbstractAutoProxyCreator抽象类中的postProcessAfterInitialization方法处便能看到了，如下所示。


![image-20210905100641162](\images\image-20210905100641162.png)

## BeanPostProcessor的执行流程

们知道BeanPostProcessor的postProcessBeforeInitialization()方法是在bean的初始化之前被调用；而postProcessAfterInitialization()方法是在bean初始化的之后被调用。并且bean的初始化和销毁方法我们可以通过如下方式进行指定。


### （一）通过@Bean指定init-method和destroy-method

```java
@Bean(initMethod="init", destroyMethod="destroy")
public Car car() {
    return new Car();
}
```

### （二）通过让bean实现InitializingBean和DisposableBean这俩接口

```java
@Component
public class Cat implements InitializingBean, DisposableBean {

    public Cat() {
        System.out.println("cat constructor...");
    }

    /**
     * 会在容器关闭的时候进行调用
     */
    public void destroy() throws Exception {
        // TODO Auto-generated method stub
        System.out.println("cat destroy...");
    }

    /**
     * 会在bean创建完成，并且属性都赋好值以后进行调用
     */
    public void afterPropertiesSet() throws Exception {
        // TODO Auto-generated method stub
        System.out.println("cat afterPropertiesSet...");
    }

}
```

### （三）使用JSR-250规范里面定义的@PostConstruct和@PreDestroy这俩注解

- @PostConstruct：在bean创建完成并且属性赋值完成之后，来执行初始化方法
- @PreDestroy：在容器销毁bean之前通知我们进行清理工作

```java
@Component
public class Dog {

    public Dog() {
        System.out.println("dog constructor...");
    }

    // 在对象创建完成并且属性赋值完成之后调用
    @PostConstruct
    public void init() {
        System.out.println("dog...@PostConstruct...");
    }

    // 在容器销毁（移除）对象之前调用
    @PreDestroy
    public void destory() {
        System.out.println("dog...@PreDestroy...");
    }

}
```

### （四）通过让bean实现BeanPostProcessor接口

```java
@Component // 将后置处理器加入到容器中，这样的话，Spring就能让它工作了
public class MyBeanPostProcessor implements BeanPostProcessor, Order {

    public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
        // TODO Auto-generated method stub
        System.out.println("postProcessBeforeInitialization..." + beanName + "=>" + bean);
        return bean;
    }


    public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
        // TODO Auto-generated method stub
        System.out.println("postProcessAfterInitialization..." + beanName + "=>" + bean);
        return bean;
    }

    public int value() {
        return 3;
    }

    public Class<? extends Annotation> annotationType() {
        return null;
    }


}
```

通过以上这四种方式，我们就可以对bean的整个生命周期进行控制：

​	bean的实例化：调用bean的构造方法，我们可以在bean的无参构造方法中执行相应的逻辑。
​	bean的初始化：在初始化时，可以通过BeanPostProcessor的postProcessBeforeInitialization()方法和postProcessAfterInitialization()方法进行拦截，执行自定义的逻辑；通过@PostConstruct注解、InitializingBean和init-method来指定bean初始化前后执行的方法，在该方法中咱们可以执行自定义的逻辑。
​	bean的销毁：可以通过@PreDestroy注解、DisposableBean和destroy-method来指定bean在销毁前执行的方法，在该方法中咱们可以执行自定义的逻辑。

通过上述四种方式，我们可以控制Spring中bean的整个生命周期。


## BeanPostProcessor源码解析

如果想深刻理解BeanPostProcessor的工作原理，那么就不得不看下相关的源码，我们可以在MyBeanPostProcessor类的postProcessBeforeInitialization()方法和postProcessAfterInitialization()方法这两处打上断点来进行调试，如下所示。

![image-20210906192222585](images\image-20210906192222585.png)

随后，我们以Debug的方式来运行IOCTest_LifeCycle类中的test01()方法，运行后的效果如下所示。

![image-20210906193448517](D:\studyDoc\java\images\image-20210906193448517.png)

可以看到，程序已经运行到MyBeanPostProcessor类的postProcessBeforeInitialization()方法中了

通过这个方法调用栈，我们可以详细地分析从运行IOCTest_LifeCycle类中的test01()方法开始，到进入MyBeanPostProcessor类的postProcessBeforeInitialization()方法中的执行流程。

注意：方法调用栈是先进后出的，也就是说，最先调用的方法会最后退出，每调用一个方法，JVM会将当前调用的方法放入栈的栈顶，方法退出时，会将方法从栈顶的位置弹出。

第一步，我们在方法调用栈中，找到IOCTest_LifeCycle类的test08()方法并单击，此时会定位到IOCTest_LifeCycle类的test01()方法中，如下所示。

![image-20210906193717485](images\image-20210906193717485.png)

在IOCTest_LifeCycle类的test08()方法中，首先通过new实例对象的方式创建了一个IOC容器。

第二步，通过Eclipse的方法调用栈继续分析，单击IOCTest_LifeCycle类的test08()方法上面的那个方法，这时会进入AnnotationConfigApplicationContext类的构造方法中。

![image-20210906193859727](images\image-20210906193859727.png)

可以看到，在AnnotationConfigApplicationContext类的构造方法中会调用refresh()方法。

第三步，我们继续跟进方法调用栈，如下所示，可以看到，方法的执行定位到AbstractApplicationContext类的refresh()方法中的如下那行代码处。

![image-20210906194059323](images\image-20210906194059323.png)

上面这行代码的作用就是初始化所有的（非懒加载的）单实例bean对象。

AbstractApplicationContext类中的refresh()方法有点长所以又截了一张图，如下所示，可以清楚地看到refresh()方法里面调用了finishBeanFactoryInitialization()方法。

![image-20210906194315063](images\image-20210906194315063.png)

第四步，我们继续跟进方法调用栈，如下所示，可以看到，方法的执行定位到AbstractApplicationContext类的finishBeanFactoryInitialization()方法中的如下那行代码处

![image-20210906194646969](images\image-20210906194646969.png)

这行代码的作用同样是初始化所有的（非懒加载的）单实例bean。

![image-20210906194742818](\images\image-20210906194742818.png)

第五步，我们继续跟进方法调用栈，如下所示，可以看到，方法的执行定位到DefaultListableBeanFactory类的preInstantiateSingletons()方法的最后一个else分支调用的getBean()方法上。

![image-20210906194818860](images\image-20210906194818860.png)

第六步，继续跟进方法调用栈，如下所示。

![image-20210906194932494](images\image-20210906194932494.png)

此时方法定位到AbstractBeanFactory类的getBean()方法中了，在getBean()方法中，又调用了doGetBean()方法。

第七步，继续跟进方法调用栈，如下所示，此时，方法的执行定位到AbstractBeanFactory类的doGetBean()方法中的如下那行代码处。

![image-20210906195014493](images\image-20210906195014493.png)

可以看到，在Spring内部是通过getSingleton()方法来获取单实例bean的。

第八步，继续跟进方法调用栈，如下所示，此时，方法定位到DefaultSingletonBeanRegistry类的getSingleton()方法中的如下那行代码处。

![image-20210906195105760](images\image-20210906195105760.png)

可以看到，在getSingleton()方法里面又调用了getObject()方法来获取单实例bean。

第九步，继续跟进方法调用栈，如下所示，此时，方法定位到AbstractBeanFactory类的doGetBean()方法中的如下那行代码处。

![image-20210906195241983](images\image-20210906195241983.png)

也就是说，当第一次获取单实例bean时，由于单实例bean还未创建，那么Spring会调用createBean()方法来创建单实例bean。

第十步，继续跟进方法调用栈，如下所示，可以看到，方法的执行定位到AbstractAutowireCapableBeanFactory类的createBean()方法中的如下那行代码处。

![image-20210906195338829](images\image-20210906195338829.png)

可以看到，Spring中创建单实例bean调用的是doCreateBean()方法。

第十一步，继续跟进方法调用栈，如下所示，此时，方法的执行已经定位到AbstractAutowireCapableBeanFactory类的doCreateBean()方法中的如下那行代码处了。

![image-20210906195441413](images\image-20210906195441413.png)

在initializeBean()方法里面会调用一系列的后置处理器。

第十二步，继续跟进方法调用栈，如下所示，此时，方法的执行定位到AbstractAutowireCapableBeanFactory类的initializeBean()方法中的如下那行代码处。

![image-20210906195531525](images\image-20210906195531525.png)

需要重点留意一下这个applyBeanPostProcessorsBeforeInitialization()方法。

回过头来我们再来看看AbstractAutowireCapableBeanFactory类的doCreateBean()方法中的如下这行代码。

![image-20210906195632934](images\image-20210906195632934.png)

没错，在以上initializeBean()方法中调用了后置处理器的逻辑，这我上面已经说到了。需要特别注意一下，在AbstractAutowireCapableBeanFactory类的doCreateBean()方法中，调用initializeBean()方法之前，还调用了一个populateBean()方法，我也在上图中标注出来了。

我们点进去这个populateBean()方法中，看下这个方法到底执行了哪些逻辑，如下所示。

![image-20210906195735069](images\image-20210906195735069.png)

populateBean()方法同样是AbstractAutowireCapableBeanFactory类中的方法，它里面的代码比较多，但是逻辑非常简单，populateBean()方法做的工作就是为bean的属性赋值。也就是说，在Spring中会先调用populateBean()方法为bean的属性赋好值，然后再调用initializeBean()方法。


接下来，我们好好分析下initializeBean()方法，为了方便，我将Spring中AbstractAutowireCapableBeanFactory类的initializeBean()方法的代码特意提取出来了，如下所示。

![image-20210906195901907](images\image-20210906195901907.png)

在initializeBean()方法中，调用了invokeInitMethods()方法，代码行如下所示。

```java
invokeInitMethods(beanName, wrappedBean, mbd);
```

invokeInitMethods()方法的作用就是执行初始化方法，这些初始化方法包括我们之前讲的：在XML配置文件的标签中使用init-method属性指定的初始化方法；在@Bean注解中使用initMehod属性指定的方法；使用@PostConstruct注解标注的方法；实现InitializingBean接口的方法等。

**在调用invokeInitMethods()方法之前，Spring调用了applyBeanPostProcessorsBeforeInitialization()这个方法，代码行如下所示。**

```java
wrappedBean = applyBeanPostProcessorsBeforeInitialization(wrappedBean, beanName);
```

**在调用invokeInitMethods()方法之后，Spring又调用了applyBeanPostProcessorsAfterInitialization()这个方法，如下所示。**

```java
wrappedBean = applyBeanPostProcessorsAfterInitialization(wrappedBean, beanName);
```

这里，我们先来看看applyBeanPostProcessorsBeforeInitialization()方法中具体执行了哪些逻辑，该方法位于AbstractAutowireCapableBeanFactory类中，源码如下所示。

![image-20210906200422724](images\image-20210906200422724.png)

可以看到，在applyBeanPostProcessorsBeforeInitialization()方法中，会遍历所有BeanPostProcessor对象，然后依次执行所有BeanPostProcessor对象的postProcessBeforeInitialization()方法，一旦BeanPostProcessor对象的postProcessBeforeInitialization()方法返回null以后，则后面的BeanPostProcessor对象便不再执行了，而是直接退出for循环。

看Spring源码，我们还看到了一个细节，**在Spring中调用initializeBean()方法之前，还调用了populateBean()方法来为bean的属性赋值，** 这在上面我也已经说过了

经过上面的一系列的跟踪源码分析，我们可以将关键代码的调用过程使用如下伪代码表述出来。

```java
populateBean(beanName, mbd, instanceWrapper); // 给bean进行属性赋值
initializeBean(beanName, exposedObject, mbd)
{
	applyBeanPostProcessorsBeforeInitialization(wrappedBean, beanName);
	invokeInitMethods(beanName, wrappedBean, mbd); // 执行自定义初始化
	applyBeanPostProcessorsAfterInitialization(wrappedBean, beanName);
}

```

也就是说，在Spring中，调用initializeBean()方法之前，调用了populateBean()方法为bean的属性赋值，为bean的属性赋好值之后，再调用initializeBean()方法进行初始化

在initializeBean()中，调用自定义的初始化方法（即invokeInitMethods()）之前，调用了applyBeanPostProcessorsBeforeInitialization()方法，而在调用自定义的初始化方法之后，又调用了applyBeanPostProcessorsAfterInitialization()方法。至此，整个bean的初始化过程就这样结束了。


## BeanPostProcessor在Spring底层使用

### BeanPostProcessor接口

我们先来看下BeanPostProcessor接口的源码，如下所示。

![image-20210906200716559](images\image-20210906200716559.png)

可以看到，在BeanPostProcessor接口中，提供了两个方法：postProcessBeforeInitialization()方法和postProcessAfterInitialization()方法。postProcessBeforeInitialization()方法会在bean初始化之前调用，postProcessAfterInitialization()方法会在bean初始化之后调用。接下来，我们就来分析下BeanPostProcessor接口在Spring中的实现。


**注意：这里，我列举几个BeanPostProcessor接口在Spring中的实现类，来让大家更加清晰的理解BeanPostProcessor接口在Spring底层的应用。**

### ApplicationContextAwareProcessor类

org.springframework.context.support.ApplicationContextAwareProcessor是BeanPostProcessor接口的一个实现类，这个类的作用是可以向组件中注入IOC容器，大致的源码如下所示。

![在这里插入图片描述](D:\studyDoc\java\images\bean1233.jpg)

**注意：我这里的Spring版本为4.3.12.RELEASE。**

要想使用ApplicationContextAwareProcessor类向组件中注入IOC容器，我们就不得不提Spring中的另一个接口了，即ApplicationContextAware。如果需要向组件中注入IOC容器，那么可以让组件实现ApplicationContextAware接口。

例如，我们创建一个Dog类，使其实现ApplicationContextAware接口，此时，我们需要实现ApplicationContextAware接口中的setApplicationContext()方法，在setApplicationContext()方法中有一个ApplicationContext类型的参数，这个就是IOC容器对象，我们可以在Dog类中定义一个ApplicationContext类型的成员变量，然后在setApplicationContext()方法中为这个成员变量赋值，此时就可以在Dog类中的其他方法中使用ApplicationContext对象了，如下所示。

```java
@Component
public class Dog implements ApplicationContextAware {
    private ApplicationContext applicationContext;
    
    public Dog() {
        System.out.println("dog constructor...");
    }

    // 在对象创建完成并且属性赋值完成之后调用
    @PostConstruct
    public void init() {
        System.out.println("dog...@PostConstruct...");
    }

    // 在容器销毁（移除）对象之前调用
    @PreDestroy
    public void destory() {
        System.out.println("dog...@PreDestroy...");
    }

    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        // TODO Auto-generated method stub
        this.applicationContext = applicationContext;
    }
}
```

这就是BeanPostProcessor在Spring底层的一种使用场景。至于上面的案例代码为何会在setApplicationContext()方法中获取到ApplicationContext对象，这就是ApplicationContextAwareProcessor类的功劳了

接下来，我们就深入分析下ApplicationContextAwareProcessor类。

我们先来看下ApplicationContextAwareProcessor类中对于postProcessBeforeInitialization()方法的实现，如下所示

![image-20210906201923358](images\image-20210906201923358.png)

可以看到invokeAwareInterfaces()方法的源码比较简单，就是判断当前bean属于哪种接口类型，然后将bean强转为哪种接口类型的对象，接着调用接口中的方法，将相应的参数传递到接口的方法中。这里，我们在创建Dog类时，实现的是ApplicationContextAware接口，所以，在invokeAwareInterfaces()方法中，会执行如下的逻辑代码。

```java
if (bean instanceof ApplicationContextAware) {   
	((ApplicationContextAware) bean).setApplicationContext(this.applicationContext);
}
```

我们可以看到，此时会将this.applicationContext传递到ApplicationContextAware接口的setApplicationContext()方法中。所以，我们在Dog类的setApplicationContext()方法中就可以直接接收到ApplicationContext对象了。


### BeanValidationPostProcessor类

org.springframework.validation.beanvalidation.BeanValidationPostProcessor类主要是用来为bean进行校验操作的，当我们创建bean，并为bean赋值后，我们可以通过BeanValidationPostProcessor类为bean进行校验操作。BeanValidationPostProcessor类的源码如下所示。


![在这里插入图片描述](images\12231231231.jpg)

这里，我们也来看看postProcessBeforeInitialization()方法和postProcessAfterInitialization()方法的实现，如下所示。

![image-20210906202504047](images\image-20210906202504047.png)

可以看到，在postProcessBeforeInitialization()方法和postProcessAfterInitialization()方法中的主要逻辑都是调用doValidate()方法对bean进行校验，只不过在这两个方法中都会对afterInitialization这个boolean类型的成员变量进行判断，若afterInitialization的值为false，则在postProcessBeforeInitialization()方法中调用doValidate()方法对bean进行校验；若afterInitialization的值为true，则在postProcessAfterInitialization()方法中调用doValidate()方法对bean进行校验。

### InitDestroyAnnotationBeanPostProcessor类

org.springframework.beans.factory.annotation.InitDestroyAnnotationBeanPostProcessor类主要用来处理@PostConstruct注解和@PreDestroy注解。

例如，我们之前创建的Dog类中就使用了@PostConstruct注解和@PreDestroy注解，如下所示。


```java
@Component
public class Dog implements ApplicationContextAware {
    private ApplicationContext applicationContext;

    public Dog() {
        System.out.println("dog constructor...");
    }

    // 在对象创建完成并且属性赋值完成之后调用
    @PostConstruct
    public void init() {
        System.out.println("dog...@PostConstruct...");
    }

    // 在容器销毁（移除）对象之前调用
    @PreDestroy
    public void destory() {
        System.out.println("dog...@PreDestroy...");
    }

    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        // TODO Auto-generated method stub
        this.applicationContext = applicationContext;
    }
}
```

那么，在Dog类中使用了@PostConstruct注解和@PreDestroy注解来标注方法，Spring怎么就知道什么时候执行@PostConstruct注解标注的方法，什么时候执行@PreDestroy注解标注的方法呢？这就要归功于InitDestroyAnnotationBeanPostProcessor类了。


接下来，我们也通过Debug的方式来跟进下代码的执行流程。首先，在Dog类的initt()方法上打上一个断点，如下所示。

![image-20210906202725268](images\image-20210906202725268.png)

我们还是带着问题来分析，通过分析方法的调用栈，我们发现在进入使用@PostConstruct注解标注的方法之前，Spring调用了InitDestroyAnnotationBeanPostProcessor类的postProcessBeforeInitialization()方法，如下所示。

![image-20210906202807364](images\image-20210906202807364.png)

在InitDestroyAnnotationBeanPostProcessor类的postProcessBeforeInitialization()方法中，首先会找到bean中有关生命周期的注解，比如@PostConstruct注解等，找到这些注解之后，则将这些信息赋值给LifecycleMetadata类型的变量metadata，之后调用metadata的invokeInitMethods()方法，通过反射来调用标注了@PostConstruct注解的方法。这就是为什么标注了@PostConstruct注解的方法会被Spring执行的原因。

### AutowiredAnnotationBeanPostProcessor类

org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor类主要是用于处理标注了@Autowired注解的变量或方法。

Spring为何能够自动处理标注了@Autowired注解的变量或方法，就交给小伙伴们自行分析了。大家可以写一个测试方法并通过方法调用堆栈来分析AutowiredAnnotationBeanPostProcessor类的源码，从而找到自己想要的答案。

# 四、属性装配和自动赋值

## @Value注解

Spring中的@Value注解可以为bean中的属性赋值。我们先来看看@Value注解的源码，如下所示。

![image-20210907193102990](images\image-20210907193102990.png)

从@Value注解的源码中我们可以看出，@Value注解可以标注在字段、方法、参数以及注解上，而且在程序运行期间生效。

## @Value注解的用法

### 不通过配置文件注入属性的情况

通过@Value注解将外部的值动态注入到bean的属性中，一般有如下这几种情况：

注入普通字符串

```java
@Value("cs")
private String name;
```

注入操作系统属性

```java
@Value("#{systemProperties['os.name']}")
private String systemPropertiesName; // 注入操作系统属性
```

注入SpEL表达式结果

```java
@Value("#{ T(java.lang.Math).random() * 100.0 }")
private double randomNumber; //注入SpEL表达式结果
```

注入其他bean中属性的值

```java
@Value("#{person.name}") // 注入其他bean中属性的值，即注入person对象的name属性中的值
private String username; 
```

注入文件资源

```java
@Value("classpath:/config.properties")
private Resource resourceFile; // 注入文件资源
```

注入URL资源

```java
@Value("http://www.baidu.com")
private Resource url; // 注入URL资源
```

### 通过配置文件注入属性的情况

首先，我们可以在项目的src/main/resources目录下新建一个属性文件，例如person.properties，其内容如下：

```properties
person.nickName=harry
```

然后，我们新建一个MainConfigOfPropertyValues配置类，并在该类上使用@PropertySource注解读取外部配置文件中的key/value并保存到运行的环境变量中。

```java
@PropertySource(value={"classpath:/person.properties"})
@Configuration
public class MainConfigOfPropertyValues {

    @Bean
    public Person person() {
        return new Person();
    }

}
```

加载完外部的配置文件以后，接着我们就可以使用`${key}`取出配置文件中key所对应的值，并将其注入到bean的属性中了。

```java
@Value("${person.nickName}")
private String nickName; // 昵称
```

### @Value中#{···}和${···}的区别

我们在这里提供一个测试属性文件，例如advance_value_inject.properties，大致的内容如下所示。

```properties
server.name=server1,server2,server3
author.name=caishuang
```

然后，新建一个AdvanceValueInject类，并在该类上使用@PropertySource注解读取外部属性文件中的key/value并保存到运行的环境变量中，即加载外部的advance_value_inject.properties属性文件。

```java
@Component
@PropertySource(value={"classpath:/advance_value_inject.properties"})
public class AdvanceValueInject {

// ···
}
```

#### ${···}的用法

{}里面的内容必须符合SpEL表达式，通过@Value("${spelDefault.value}")我们可以获取属性文件中对应的值，但是如果属性文件中没有这个属性，那么就会报错。不过，我们可以通过赋予默认值来解决这个问题，如下所示

```java
@Value("${author.name:cs}")
private String name;
```

上述代码的含义是表示向bean的属性中注入属性文件中的author.name属性所对应的值，如果属性文件中没有author.name这个属性，那么便向bean的属性中注入默认值cs。

#### #{···}的用法

{}里面的内容同样也是必须符合SpEL表达式。例如，

```java
// SpEL：调用字符串Hello World的concat方法
@Value("#{'Hello World'.concat('!')}")
private String helloWorld;

// SpEL：调用字符串的getBytes方法，然后再调用其length属性
@Value("#{'Hello World'.bytes.length}")
private String helloWorldBytes;
```

#### ${···}和#{···}的混合使用

`${···}`和`#{···}`可以混合使用，例如，

```java
  // SpEL：传入一个字符串，根据","切分后插入列表中， #{}和${}配合使用时，注意不能反过来${}在外面，而#{}在里面
    @Value("#{'${server.name}'.split(',')}")
    private List<String> severs;
}
```

上面片段的代码的执行顺序：通过`${server.name}`从属性文件中获取值并进行替换，然后就变成了执行SpEL表达式`{'server1,server2,server3'.split(',')}`。

## 使用@PropertySource加载配置文件

### @PropertySource注解概述

@PropertySource注解是Spring 3.1开始引入的配置类注解。通过@PropertySource注解可以将properties配置文件中的key/value存储到Spring的Environment中，Environment接口提供了方法去读取配置文件中的值，参数是properties配置文件中定义的key值。当然了，也可以使用@Value注解用${}占位符为bean的属性注入值。
我们来看一下@PropertySource注解的源代码，如下所示。

![image-20210907194537786](images\image-20210907194537786.png)

从@PropertySource的源码中可以看出，我们可以通过@PropertySource注解指定多个properties文件，使用的形式如下所示。

```java
@PropertySource(value={"classpath:/person.properties", "classpath:/car.properties"})
```

### @PropertySources注解概述

首先，我们也来看下@PropertySources注解的源码，如下所示。

![image-20210907195053162](images\image-20210907195053162.png)

@PropertySources注解的源码比较简单，只有一个PropertySource[]数组类型的value属性，那我们如何使用@PropertySources注解指定配置文件呢？其实也很简单，使用如下所示的方式就可以了。

```java
@PropertySources(value={
        @PropertySource(value={"classpath:/person.properties"}),
        @PropertySource(value={"classpath:/car.properties"}),
})
```

## 一个小案例来说明@PropertySource注解的用法

首先，我们在工程的src/main/resources目录下创建一个配置文件，例如person.properties，该文件的内容如下所示。

```properties
person.nickName=harry
```

然后，我们在Person类中新增一个nickName字段，如下所示。

```java
package com.harry.spring.bean;

public class Person {
    private String name;
    private Integer age;

    private String nickName; // 昵称
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public Integer getAge() {
        return age;
    }
    public void setAge(Integer age) {
        this.age = age;
    }
    public Person(String name, Integer age) {
        super();
        this.name = name;
        this.age = age;
    }
    public Person() {
        super();
        // TODO Auto-generated constructor stub
    }

    public String getNickName() {
        return nickName;
    }

    public void setNickName(String nickName) {
        this.nickName = nickName;
    }

    @Override
    public String toString() {
        return "Person{" +
                "name='" + name + '\'' +
                ", age=" + age +
                ", nickName='" + nickName + '\'' +
                '}';
    }
}
```

目前，我们并没有为Person类的nickName字段赋值，所以，此时Person类的nickName字段的值为空。

### 使用注解方式获取值

如果我们使用注解的方式，那么该如何做呢？首先，我们需要在MainConfigOfPropertyValues配置类上添加一个@PropertySource注解，如下所示。

```java
// 使用@PropertySource读取外部配置文件中的key/value保存到运行的环境变量中，加载完外部的配置文件以后，使用${}取出配置文件中的值
@PropertySource(value={"classpath:/person.properties"})
@Configuration
public class MainConfigOfPropertyValues {

    @Bean
    public Person person() {
        return new Person();
    }
}
```

这里使用的@PropertySource(value={"classpath:/person.properties"})注解就相当于XML配置文件中使用的<context:property-placeholder location="classpath:person.properties" />。

然后，我们就可以在Person类的nickName字段上使用@Value注解来获取person.properties文件中的值了，如下所示。

```java
@Value("${person.nickName}")
private String nickName; // 昵称
```

### 使用Environment获取值

上面我已经说过，使用@PropertySource注解读取外部配置文件中的key/value之后，是将其保存到运行的环境变量中了，所以我们也可以通过运行环境来获取外部配置文件中的值。

这里，我们可以稍微修改一下IOCTest_PropertyValue类中的test01()方法，即在其中添加一段使用Environment获取person.properties文件中的值的代码，如下所示。

```java
@Test
public void testAnnotation(){
    ApplicationContext applicationContext = new AnnotationConfigApplicationContext(MainConfigOfPropertyValues.class);
    Person person = applicationContext.getBean(Person.class);
    System.out.println(person);

    ConfigurableEnvironment environment = (ConfigurableEnvironment) applicationContext.getEnvironment();
    String property = environment.getProperty("person.nickName");
    System.out.println(property);

}
```

可以看到，使用Environment确实能够获取到person.properties文件中的值。

## @Autowired、@Qualifier、@Primary三大注解自动装配组件

### @Autowired注解

@Autowired注解可以对类成员变量、方法和构造函数进行标注，完成自动装配的工作。@Autowired注解可以放在类、接口以及方法上。

在使用@Autowired注解之前，我们对一个bean配置属性时，是用如下XML配置文件的形式进行配置的。

```xml
<property name="属性名" value=" 属性值"/>
```

下面我们来看一下@Autowired注解的源码，如下所示。

![image-20210907200310211](images\image-20210907200310211.png)

@Autowired注解默认是优先按照类型去容器中找对应的组件，相当于是调用了如下这个方法：

```
applicationContext.getBean(类名.class);
```

如果找到多个相同类型的组件，那么是将属性名称作为组件的id，到IOC容器中进行查找，这时就相当于是调用了如下这个方法：

```
applicationContext.getBean("组件的id");
```

### @Qualifier注解

@Autowired是根据类型进行自动装配的，如果需要按名称进行装配，那么就需要配合@Qualifier注解来使用了。

![image-20210907200622612](images\image-20210907200622612.png)

### @Primary注解

在Spring中使用注解时，常常会使用到@Autowired这个注解，它默认是根据类型Type来自动注入的。但有些特殊情况，对同一个接口而言，可能会有几种不同的实现类，而在默认只会采取其中一种实现的情况下，就可以使用@Primary注解来标注优先使用哪一个实现类。

下面我们来看一下@Primary注解的源码，如下所示


![image-20210907200748427](images\image-20210907200748427.png)

## 自动装配

在进行项目实战之前，我们先来说说什么是Spring组件的自动装配。Spring组件的自动装配就是**Spring利用依赖注入，也就是我们通常所说的DI，完成对IOC容器中各个组件的依赖关系赋值。**

## 项目实战

### 测试@Autowired注解

这里，我们以之前项目中创建的BookDao、BookService和BookController为例进行说明。BookDao、BookService和BookController的初始代码分别如下所示。

BookDao

```java
import org.springframework.stereotype.Repository;

// 名字默认是类名首字母小写
@Repository
public class BookDao {

}
```

BookService

```java
@Service
public class BookService {

    @Autowired
    private BookDao bookDao;

    public void print() {
        System.out.println(bookDao);
    }

}
```

BookController

```java
@Controller
public class BookController {
    @Autowired
    private BookService bookService;
}
```

可以看到，我们在BookService中使用@Autowired注解注入了BookDao，在BookController中使用@Autowired注解注入了BookService。为了方便测试，我们可以在BookService类中生成一个toString()方法，如下所示。

```java
@Service
public class BookService {

    @Autowired
    private BookDao bookDao;

    public void print() {
        System.out.println(bookDao);
    }
    @Override
    public String toString() {
        return "BookService [bookDao=" + bookDao + "]";
    }

}
```

为了更好的看到演示效果，我们在项目下创建一个配置类，例如MainConfigOfAutowired，如下所示

```java
@Configuration
@ComponentScan({"com.harry.spring.service", "com.harry.spring.dao", "com.harry.spring.controller"})
public class MainConfigOfAutowired {
    
}
```

接下来，我们便来测试一下上面的程序。在项目的src/test/java目录中创建一个单元测试类，例如IOCTest_Autowired，如下所示。

```java
import com.harry.spring.config.MainConfigOfAutowired;
import com.harry.spring.service.BookService;
import org.junit.Test;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class IOCTest_Autowired {
    @Test
    public void test01() {
        AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext(MainConfigOfAutowired.class);

        BookService bookService = applicationContext.getBean(BookService.class);
        System.out.println(bookService);

        applicationContext.close();
    }

}
```

我们运行一下IOCTest_Autowired类中的test01()方法，得出的输出结果信息如下所示。

![image-20210907201559370](images\image-20210907201559370.png)

可以看到，输出了BookDao信息。

那么问题来了，我们在BookService类中使用@Autowired注解注入的BookDao（最后输出了该BookDao的信息），和我们直接在Spring IOC容器中获取的BookDao是不是同一个对象呢？

为了说明这一点，我们可以在IOCTest_Autowired类的test01()方法中添加获取BookDao对象的方法，并输出获取到的BookDao对象，如下所示。


![image-20210907201658292](images\image-20210907201658292.png)

可以看到，我们在BookService类中使用@Autowired注解注入的BookDao对象和直接从IOC容器中获取的BookDao对象是同一个对象

**如果在Spring容器中存在对多个BookDao对象，那么这时又该如何处理呢？**

首先，为了更加直观的看到我们使用@Autowired注解装配的是哪个BookDao对象，我们得对BookDao类进行改造，为其加上一个lable字段，并为其赋一个默认值，如下所示。

```java
// 名字默认是类名首字母小写
@Repository
public class BookDao {
    private String lable = "1";

    public String getLable() {
        return lable;
    }

    public void setLable(String lable) {
        this.lable = lable;
    }

    @Override
    public String toString() {
        return "BookDao [lable=" + lable + "]";
    }

}
```

然后，我们就在MainConfigOfAutowired配置类中注入一个BookDao对象，并且显示指定该对象在IOC容器中的bean的名称为bookDao2，并还为该对象的lable字段赋值为2，如下所示。

```java
@Configuration
@ComponentScan({"com.harry.spring.service", "com.harry.spring.dao", "com.harry.spring.controller"})
public class MainConfigOfAutowired {
    @Bean("bookDao2")
    public BookDao bookDao() {
        BookDao bookDao = new BookDao();
        bookDao.setLable("2");
        return bookDao;
    }
}
```

目前，在我们的IOC容器中就会注入两个BookDao对象。那此时，**@Autowired注解到底装配的是哪个BookDao对象呢？**

接着，我们来运行一下IOCTest_Autowired类中的test01()方法，发现输出的结果信息如下所示。

![image-20210907202019979](images\image-20210907202019979.png)

可以看到，结果信息输出了`lable=1`，这说明，**@Autowired注解默认是优先按照类型去容器中找对应的组件，找到就赋值；如果找到多个相同类型的组件，那么再将属性的名称作为组件的id，到IOC容器中进行查找。**

**那我们如何让@Autowired注解装配bookDao2呢？** 其实很简单，我们只须将BookService类中的bookDao属性的名称全部修改为bookDao2即可，如下所示。

```java
@Service
public class BookService {

    @Autowired
    private BookDao bookDao2;

    public void print() {
        System.out.println(bookDao2);
    }

    @Override
    public String toString() {
        return "BookService [bookDao2=" + bookDao2 + "]";
    }
}
```

### 测试@Qualifier注解

测试@Autowired注解的结果来看，**@Autowired注解默认是优先按照类型去容器中找对应的组件，找到就赋值；如果找到多个相同类型的组件，那么再将属性的名称作为组件的id，到IOC容器中进行查找。**

我们只需要在BookService类里面的bookDao2字段上添加@Qualifier注解，显示指定@Autowired注解装配bookDao即可，如下所示。

```java
@Service
public class BookService {

    @Qualifier("bookDao")
    @Autowired
    private BookDao bookDao2;

    public void print() {
        System.out.println(bookDao2);
    }

    @Override
    public String toString() {
        return "BookService [bookDao2=" + bookDao2 + "]";
    }
}
```

可以看到，此时尽管字段的名称为bookDao2，但是我们使用了@Qualifier注解显示指定了@Autowired注解装配bookDao对象，所以，最终的结果中输出了bookDao对象的信息。

### 测试容器中无组件的情况

如果IOC容器中无相应的组件，那么会发生什么情况呢？这时我们可以做这样一件事情，先注释掉BookDao类上的@Repository注解，

```java
// 名字默认是类名首字母小写
//@Repository
public class BookDao {
    private String lable = "1";

    public String getLable() {
        return lable;
    }

    public void setLable(String lable) {
        this.lable = lable;
    }

    @Override
    public String toString() {
        return "BookDao [lable=" + lable + "]";
    }

}
```

然后再注释掉MainConfigOfAutowired配置类中的bookDao()方法上的@Bean注解，如下所示。

```java
@Configuration
@ComponentScan({"com.harry.spring.service", "com.harry.spring.dao", "com.harry.spring.controller"})
public class MainConfigOfAutowired {
//    @Bean("bookDao2")
    public BookDao bookDao() {
        BookDao bookDao = new BookDao();
        bookDao.setLable("2");
        return bookDao;
    }
}
```

此时IOC容器中不再有任何BookDao对象了。

![image-20210907203136813](images\image-20210907203136813.png)

此时，Spring抛出了异常，未找到相应的bean对象，那我们能不能让Spring不报错呢？抛出的异常信息中都给出了相应的提示。

解决方案就是在BookService类的@Autowired注解里面添加一个属性`required=false`，如下所示。

```java
@Configuration
@ComponentScan({"com.harry.spring.service", "com.harry.spring.dao", "com.harry.spring.controller"})
public class MainConfigOfAutowired {
    @Qualifier("bookDao")
    @Autowired(required=false)
    public BookDao bookDao() {
        BookDao bookDao = new BookDao();
        bookDao.setLable("2");
        return bookDao;
    }
}
```

可以看到，当为@Autowired注解添加属性`required=false`后，即使IOC容器中没有对应的对象，Spring也不会抛出异常了。不过，此时装配的对象就为null了。

## @Resource注解和@Inject注解吗

### @Resource注解

@Resource注解是Java规范里面的，也可以说它是JSR250规范里面定义的一个注解。该注解默认按照名称进行装配，名称可以通过name属性进行指定，如果没有指定name属性，当注解写在字段上时，那么默认取字段名将其作为组件的名称在IOC容器中进行查找，如果注解写在setter方法上，那么默认取属性名进行装配。当找不到与名称匹配的bean时才按照类型进行装配。但是需要注意的一点是，如果name属性一旦指定，那么就只会按照名称进行装配。

我们先看一下@Resource注解的源码，如下所示。


![在这里插入图片描述](D:\studyDoc\java\images\123123123213.jpg)

### @Inject注解

@Inject注解也是Java规范里面的，也可以说它是JSR330规范里面定义的一个注解。该注解默认是根据参数名去寻找bean注入，支持Spring的@Primary注解优先注入，@Inject注解还可以增加@Named注解指定要注入的bean。

我们先看一下@Inject注解的源码，如下所示。

![image-20210908200339892](\images\image-20210908200339892.png)

**温馨提示，要想使用@Inject注解，需要在项目的pom.xml文件中添加如下依赖，即导入javax.inject这个包。**

```xml
<dependency>
    <groupId>javax.inject</groupId>
    <artifactId>javax.inject</artifactId>
    <version>1</version>
</dependency>
```

### @Resource和@Inject这俩注解与@Autowired注解的区别

@Autowired是Spring中的专有注解，而@Resource是Java中JSR250规范里面定义的一个注解，@Inject是Java中JSR330规范里面定义的一个注解
@Autowired支持参数required=false，而@Resource和@Inject都不支持
@Autowired和@Inject支持@Primary注解优先注入，而@Resource不支持
@Autowired通过@Qualifier指定注入特定bean，@Resource可以通过参数name指定注入bean，而@Inject需要通过@Named注解指定注入bean

## 实现方法、构造器位置的自动装配

### 实战案例

首先，我们在项目中新建一个Boss类，在Boss类中有一个Car类的引用，并且我们使用@Component注解将Dog类加载到IOC容器中，如下所示。

```java
// 默认加在IOC容器中的组件，容器启动会调用无参构造器创建对象，然后再进行初始化、赋值等操作
@Component
public class Boss {

    private Car car;

    public Car getCar() {
        return car;
    }

    public void setCar(Car car) {
        this.car = car;
    }

    @Override
    public String toString() {
        return "Boss [car=" + car + "]";
    }

}
```

注意，Car类上也要标注@Component注解，即它也要被加载到IOC容器中。

新建好以上Boss类之后，我们还需要在MainConfigOfAutowired配置类的@ComponentScan注解中进行配置使其能够扫描com.harry.spring包下的类，如下所示

```jade
@Configuration
@ComponentScan({"com.harry.spring.service", "com.harry.spring.dao", "com.harry.spring.controller", "com.harry.spring.bean"})
public class MainConfigOfAutowired {
    @Qualifier("bookDao")
    @Autowired(required=false)
    public BookDao bookDao() {
        BookDao bookDao = new BookDao();
        bookDao.setLable("2");
        return bookDao;
    }
}
```

### 标注在实例方法上

我们可以将@Autowired注解标注在setter方法上，如下所示。

```JAVA
@Autowired
public void setCar(Car car) {
    this.car = car;
}
```

**当@Autowired注解标注在方法上时，Spring容器在创建当前对象的时候，就会调用相应的方法为对象赋值。如果标注的方法存在参数时，那么方法使用的参数和自定义类型的值，需要从IOC容器中获取。**

然后，我们将IOCTest_Autowired类的test01()方法中有关获取和打印BookService信息的代码注释掉，新增获取和打印Boss信息的代码，如下所示。

```java
    @Test
    public void test01() {
        AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext(MainConfigOfAutowired.class);

//        BookService bookService = applicationContext.getBean(BookService.class);
//        System.out.println(bookService);

//        BookDao bookDao = applicationContext.getBean(BookDao.class);
//        System.out.println(bookDao);
        Boss boss = applicationContext.getBean(Boss.class);
        System.out.println(boss);

        applicationContext.close();

    }
```

运行以上test01()方法进行测试，可以看到，结果信息中输出了如下一行信息。

![image-20210908202448762](images\image-20210908202448762.png)

说明已经获取到了car的信息，也就是说可以将@Autowired注解标注在方法上。

为了验证最终的输出结果是否是从IOC容器中获取的，我们可以在IOCTest_Autowired类的test01()方法中直接获取Car对象的信息，如下所示。

```java
    @Test
    public void test01() {
        AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext(MainConfigOfAutowired.class);

//        BookService bookService = applicationContext.getBean(BookService.class);
//        System.out.println(bookService);

//        BookDao bookDao = applicationContext.getBean(BookDao.class);
//        System.out.println(bookDao);
        Boss boss = applicationContext.getBean(Boss.class);
        System.out.println(boss);

        Car car = applicationContext.getBean(Car.class);
        System.out.println(car);

        applicationContext.close();

    }
```

这已然说明在Boss类中通过@Autowired注解获取到的Car对象和直接从IOC容器中获取到Car对象是同一个对象。

![image-20210908202609606](images\image-20210908202609606.png)

### 标注在构造方法上

在上面的案例中，我们在Boss类上使用了@Component注解

接下来，我们为Boss类添加一个有参构造方法，然后去除setCar()方法上的@Autowired注解，将@Autowired注解标注在有参构造方法上，并在构造方法中打印一条信息，如下所示。

```java
// 默认加在IOC容器中的组件，容器启动会调用无参构造器创建对象，然后再进行初始化、赋值等操作
@Component
public class Boss {

    private Car car;

    @Autowired
    public Boss(Car car) {
        this.car = car;
        System.out.println("Boss...有参构造器");
    }

    public void setCar(Car car) {
        this.car = car;
    }


    @Override
    public String toString() {
        return "Boss [car=" + car + "]";
    }

}
```

这里，需要注意的是，使用@Autowired注解标注在构造方法上时，构造方法中的参数对象也是从IOC容器中获取的。

其实，还有一点我得说明一下，使用@Autowired注解标注在构造方法上时，如果组件中只有一个有参构造方法，那么这个有参构造方法上的@Autowired注解可以省略，并且参数位置的组件还是可以自动从IOC容器中获取。

### 标注在方法位置

@Autowired注解可以标注在某个方法的位置上。这里，为了更好的演示效果，我们新建一个Color类，在Color类中有一个Car类型的成员变量，如下所示。

```java
public class Color {
    public Car car;

    public Car getCar() {
        return car;
    }

    public void setCar(Car car) {
        this.car = car;
    }

    @Override
    public String toString() {
        return "Color [car=" + car + "]";
    }

}
```

然后，我们在MainConfigOfAutowired配置类中实例化Color类，如下所示。

```java
@Bean
public Color color() {
    Color color = new Color();
    return color;
}
```

此时，我们可以将Car对象作为一个参数传递到MainConfigOfAutowired配置类的color()方法中，并且将该Car对象设置到Color对象中，如下所示。

```java
@Bean
public Color color(Car car) {
    Color color = new Color();
    color.setCar(car);
    return color;
}
```

当然了，我们也可以使用@Autowired注解来标注color()方法中的car参数，就像下面这样。

```java
@Bean
public Color color(@Autowired Car car) {
    Color color = new Color();
    color.setCar(car);
    return color;
}
```

至此，我们可以得出结论：如果方法只有一个IOC容器中的对象作为参数，当@Autowired注解标注在这个方法的参数上时，我们可以将@Autowired注解省略掉。也就说@Bean注解标注的方法在创建对象的时候，方法参数的值是从IOC容器中获取的，此外，标注在这个方法的参数上的@Autowired注解可以省略。


## 自定义组件中如何注入Spring底层的组件

自定义的组件要想使用Spring容器底层的一些组件，比如ApplicationContext（IOC容器）、底层的BeanFactory等等，那么只需要让自定义组件实现XxxAware接口即可。此时，Spring在创建对象的时候，会调用XxxAware接口中定义的方法注入相关的组件。

### XxxAware接口概览

其实，我们之前使用过XxxAware接口，例如，我们之前创建的Dog类，就实现了ApplicationContextAware接口，Dog类的源码如下所示。

```java
@Component
public class Dog implements ApplicationContextAware {
    private ApplicationContext applicationContext;

    @Value("cs")
    private String name;

    public Dog() {
        System.out.println("dog constructor...");
    }
    @Value("#{systemProperties['os.name']}")
    private String systemPropertiesName; // 注入操作系统属性

    @Value("#{ T(java.lang.Math).random() * 100.0 }")
    private double randomNumber; //注入SpEL表达式结果

    @Value("#{person.name}") // 注入其他bean中属性的值，即注入person对象的name属性中的值
    private String username;


    // 在对象创建完成并且属性赋值完成之后调用
    @PostConstruct
    public void init() {
        System.out.println("dog...@PostConstruct...");
    }

    // 在容器销毁（移除）对象之前调用
    @PreDestroy
    public void destory() {
        System.out.println("dog...@PreDestroy...");
    }

    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        // TODO Auto-generated method stub
        this.applicationContext = applicationContext;
    }
}
```

从以上Dog类的源码中可以看出，实现ApplicationContextAware接口的话，需要实现setApplicationContext()方法。在IOC容器启动并创建Dog对象时，Spring会调用setApplicationContext()方法，并且会将ApplicationContext对象传入到setApplicationContext()方法中，我们只需要在Dog类中定义一个ApplicationContext类型的成员变量来接收setApplicationContext()方法中的参数，那么便可以在Dog类的其他方法中使用ApplicationContext对象了。


其实，在Spring中，类似于ApplicationContextAware接口的设计有很多，本质上，Spring中形如XxxAware这样的接口都继承了Aware接口，我们来看下Aware接口的源码，如下所示。

![image-20210908204317843](images\image-20210908204317843.png)

可以看到，Aware接口是Spring 3.1版本中引入的接口，在Aware接口中，并未定义任何方法。

接下来，我们看看都有哪些接口继承了Aware接口，如下所示。

![image-20210908204341895](images\image-20210908204341895.png)

### XxxAware接口案例

ApplicationContextAware接口使用的比较多，我们先来说说这个接口，通过ApplicationContextAware接口我们可以获取到IOC容器。

首先，我们创建一个Red类，它得实现ApplicationContextAware接口，并在实现的setApplicationContext()方法中将ApplicationContext输出，如下所示。


```java
public class Red implements ApplicationContextAware {
    private ApplicationContext applicationContext;
    
    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        System.out.println("传入的IOC：" + applicationContext);
        this.applicationContext = applicationContext;
    }

}
```

其实，我们也可以让Red类同时实现几个XxxAware接口，例如，使Red类再实现一个BeanNameAware接口，我们可以通过BeanNameAware接口获取到当前bean在Spring容器中的名称，如下所示。

```java
public class Red implements ApplicationContextAware, BeanNameAware {
    private ApplicationContext applicationContext;

    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        System.out.println("传入的IOC：" + applicationContext);
        this.applicationContext = applicationContext;
    }

    /**
     * 参数name：IOC容器创建当前对象时，为这个对象起的名字
     */
    public void setBeanName(String name) {
        System.out.println("当前bean的名字：" + name);
    }

}

```

当然了，我们可以再让Red类实现一个EmbeddedValueResolverAware接口，我们通过EmbeddedValueResolverAware接口能够获取到String值解析器，如下所示。

```java
public class Red implements ApplicationContextAware, BeanNameAware, EmbeddedValueResolverAware {
    private ApplicationContext applicationContext;

    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        System.out.println("传入的IOC：" + applicationContext);
        this.applicationContext = applicationContext;
    }

    /**
     * 参数name：IOC容器创建当前对象时，为这个对象起的名字
     */
    public void setBeanName(String name) {
        System.out.println("当前bean的名字：" + name);
    }

    /**
     * 参数resolver：IOC容器启动时会自动地将这个String值的解析器传递过来给我们
     */
    public void setEmbeddedValueResolver(StringValueResolver resolver) {
        String resolveStringValue = resolver.resolveStringValue("你好，${os.name}，我的年龄是#{20*18}");
        System.out.println("解析的字符串：" + resolveStringValue);
    }


}
```

IOC容器启动时会自动地将String值的解析器（即StringValueResolver）传递过来给我们用，咱们可以用它来解析一些字符串，解析哪些字符串呢？比如包含`#{}`这样的字符串。我们可以看一下StringValueResolver类的源码，如下所示。

![image-20210908204810108](images\image-20210908204810108.png)

从描述中可以看出，它是用来帮我们解析那些String类型的值的，如果这个String类型的值里面有一些占位符，那么也会帮我们把这些占位符给解析出来，最后返回一个解析后的值。

接着，我们需要在Red类上标注@Component注解将该类添加到IOC容器中，如下所示。

```JAVA
@Component
public class Red implements ApplicationContextAware, BeanNameAware, EmbeddedValueResolverAware {
```

最后，运行IOCTest_Autowired类中的test02()方法，输出的结果信息如下所示。

![image-20210908205013473](images\image-20210908205013473.png)

### XxxAware原理

XxxAware接口的底层原理是由XxxAwareProcessor实现类实现的，也就是说每一个XxxAware接口都有它自己对应的XxxAwareProcessor实现类。 例如，我们这里以ApplicationContextAware接口为例，ApplicationContextAware接口的底层原理就是由ApplicationContextAwareProcessor类实现的。从ApplicationContextAwareProcessor类的源码可以看出，其实现了BeanPostProcessor接口，本质上是一个后置处理器。


![image-20210908205917006](images\image-20210908205917006.png)

下来，我们就以分析ApplicationContextAware接口的原理为例，看看Spring是怎么将ApplicationContext对象注入到Red类中的。

首先，我们在Red类的setApplicationContext()方法上打一个断点，如下所示。

![image-20210908210255902](images\image-20210908210255902.png)

然后，我们以debug的方式来运行IOCTest_Autowired类中的test02()方法。

![image-20210908210322474](images\image-20210908210322474.png)

这里，我们可以看到，实际上ApplicationContext对象已经注入到Red类的setApplicationContext()方法中了。

接着，我们在Eclipse的方法调用栈中找到postProcessBeforeInitialization()方法并鼠标单击它，如下所示，此时，自动定位到了postProcessBeforeInitialization()方法中。

![image-20210908210353625](images\image-20210908210353625.png)

其实，postProcessBeforeInitialization()方法所在的类就是ApplicationContextAwareProcessor。postProcessBeforeInitialization()方法的逻辑还算比较简单。

紧接着，我们来看下在postProcessBeforeInitialization()方法中调用的invokeAwareInterfaces()方法，如下所示。


![image-20210908210420010](images\image-20210908210420010.png)

## 使用@Profile注解实现开发、测试和生产环境的配置和切换

### @Profile注解概述

在容器中如果存在同一类型的多个组件，那么可以使用@Profile注解标识要获取的是哪一个bean。也可以说@Profile注解是Spring为我们提供的可以根据当前环境，动态地激活和切换一系列组件的功能。这个功能在不同的环境使用不同的变量的情景下特别有用，例如，开发环境、测试环境、生产环境使用不同的数据源，在不改变代码的情况下，可以使用这个注解来动态地切换要连接的数据库。

接下来，我们来看下@Profile注解的源码，如下所示。


![image-20210911091544193](images\image-20210911091544193.png)

从其源码中我们可以得出如下三点结论：

​	1.@Profile注解不仅可以标注在方法上，也可以标注在配置类上。
​	2.如果@Profile注解标注在配置类上，那么只有是在指定的环境的时候，整个配置类里面的所有配置才会生效。
​	3.如果一个bean上没有使用@Profile注解进行标注，那么这个bean在任何环境下都会被注册到IOC容器中，当然了，前提是在整个配置类生效的情况下。

### 实战案例

我们希望在开发环境中，数据源是连向A数据库的；在测试环境中，数据源是连向B数据库的，而且在这一过程中，测试人员压根就不需要改动任何代码；最终项目上线之后，数据源连向C数据库，而且最重要的一点是在整个过程中，我们不希望改动大量的代码，而实现数据源的切换。

首先，我们需要在pom.xml文件中添加c3p0数据源和MySQL驱动的依赖，如下所示。

```xml
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>5.1.46</version>
</dependency>
<dependency>
    <groupId>c3p0</groupId>
    <artifactId>c3p0</artifactId>
    <version>0.9.1.2</version>
</dependency>
```

```java
import com.mchange.v2.c3p0.ComboPooledDataSource;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import javax.sql.DataSource;

@Configuration
public class MainConfigOfProfile {

    @Bean("testDataSource")
    public DataSource dataSourceTest() throws Exception {
        ComboPooledDataSource dataSource = new ComboPooledDataSource();
        dataSource.setUser("root");
        dataSource.setPassword("liayun");
        dataSource.setJdbcUrl("jdbc:mysql://localhost:3306/test");
        dataSource.setDriverClass("com.mysql.jdbc.Driver");
        return dataSource;
    }

    @Bean("devDataSource")
    public DataSource dataSourceDev() throws Exception {
        ComboPooledDataSource dataSource = new ComboPooledDataSource();
        dataSource.setUser("root");
        dataSource.setPassword("liayun");
        dataSource.setJdbcUrl("jdbc:mysql://localhost:3306/ssm_crud");
        dataSource.setDriverClass("com.mysql.jdbc.Driver");
        return dataSource;
    }

    @Bean("prodDataSource")
    public DataSource dataSourceProd() throws Exception {
        ComboPooledDataSource dataSource = new ComboPooledDataSource();
        dataSource.setUser("root");
        dataSource.setPassword("liayun");
        dataSource.setJdbcUrl("jdbc:mysql://localhost:3306/scw_0515");
        dataSource.setDriverClass("com.mysql.jdbc.Driver");
        return dataSource;
    }

}
```

该配置类这样写，是一点儿问题都没有的，但你有没有想过这一点，在真实项目开发中，那些数据库连接的相关信息，例如用户名、密码以及MySQL数据库驱动类的全名，这些都是要抽取在一个配置文件中的

我们需要在项目的src/main/resources目录下新建一个配置文件，例如dbconfig.properties，在其中写上数据库连接的相关信息，如下所示。

```properties
db.user=root
db.password=liayun
db.driverClass=com.mysql.jdbc.Driver
```

不过，我在这儿还是得说一点，该MainConfigOfProfile配置类实现了一个EmbeddedValueResolverAware接口，我们通过该接口能够获取到String值解析器。也就是说，IOC容器启动时会自动地将String值的解析器（即StringValueResolver）传递过来给我们用，咱们可以用它来解析一些字符串。


```java
@PropertySource("classpath:/dbconfig.properties") // 加载外部的配置文件
@Configuration
public class MainConfigOfProfile {

    @Bean("testDataSource")
    public DataSource dataSourceTest() throws Exception {
        ComboPooledDataSource dataSource = new ComboPooledDataSource();
        dataSource.setUser("root");
        dataSource.setPassword("liayun");
        dataSource.setJdbcUrl("jdbc:mysql://localhost:3306/test");
        dataSource.setDriverClass("com.mysql.jdbc.Driver");
        return dataSource;
    }

    @Bean("devDataSource")
    public DataSource dataSourceDev() throws Exception {
        ComboPooledDataSource dataSource = new ComboPooledDataSource();
        dataSource.setUser("root");
        dataSource.setPassword("liayun");
        dataSource.setJdbcUrl("jdbc:mysql://localhost:3306/ssm_crud");
        dataSource.setDriverClass("com.mysql.jdbc.Driver");
        return dataSource;
    }

    @Bean("prodDataSource")
    public DataSource dataSourceProd() throws Exception {
        ComboPooledDataSource dataSource = new ComboPooledDataSource();
        dataSource.setUser("root");
        dataSource.setPassword("liayun");
        dataSource.setJdbcUrl("jdbc:mysql://localhost:3306/scw_0515");
        dataSource.setDriverClass("com.mysql.jdbc.Driver");
        return dataSource;
    }

}
```

其实，这个配置类相对来说还算是比较简单的，其中使用@Bean("devDataSource")注解标注的是开发环境使用的数据源；使用@Bean("testDataSource")注解标注的是测试环境使用的数据源；使用@Bean("prodDataSource")注解标注的是生产环境使用的数据源。

接着，我们创建一个单元测试类，例如IOCTest_Profile，并在该类中新建一个test01()方法来进行测试，如下所示。


```java
import com.harry.spring.config.MainConfigOfProfile;
import org.junit.Test;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

import javax.sql.DataSource;

public class IOCTest_Profile {

    @Test
    public void test01() {
        AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext(MainConfigOfProfile.class);

        String[] namesForType = applicationContext.getBeanNamesForType(DataSource.class);
        for (String name : namesForType) {
            System.out.println(name);
        }

        // 关闭容器
        applicationContext.close();
    }

}
```

### 根据环境注册bean

我们成功搭建环境之后，接下来，就是要实现根据不同的环境来向IOC容器中注册相应的bean了。也就是说，我们要实现在开发环境注册开发环境下使用的数据源；在测试环境注册测试环境下使用的数据源；在生产环境注册生产环境下使用的数据源。此时，@Profile注解就显示出其强大的特性了。

我们在MainConfigOfProfile配置类中为每个数据源添加@Profile注解标识，如下所示。


```java
@PropertySource("classpath:/dbconfig.properties") // 加载外部的配置文件
@Configuration
public class MainConfigOfProfile implements EmbeddedValueResolverAware {

    @Value("${db.user}")
    private String user;

    private StringValueResolver valueResolver;

    private String dirverClass;

    @Profile("test")
    @Bean("testDataSource")
    public DataSource dataSourceTest(@Value("${db.password}") String pwd) throws Exception {
        ComboPooledDataSource dataSource = new ComboPooledDataSource();
        dataSource.setUser(user);
        dataSource.setPassword(pwd);
        dataSource.setJdbcUrl("jdbc:mysql://localhost:3306/test");
        dataSource.setDriverClass(dirverClass);
        return dataSource;
    }

    @Profile("dev") // 定义了一个环境标识，只有当dev环境被激活以后，我们这个bean才能被注册进来
    @Bean("devDataSource")
    public DataSource dataSourceDev(@Value("${db.password}") String pwd) throws Exception {
        ComboPooledDataSource dataSource = new ComboPooledDataSource();
        dataSource.setUser(user);
        dataSource.setPassword(pwd);
        dataSource.setJdbcUrl("jdbc:mysql://localhost:3306/ssm_crud");
        dataSource.setDriverClass(dirverClass);
        return dataSource;
    }

    @Profile("prod")
    @Bean("prodDataSource")
    public DataSource dataSourceProd(@Value("${db.password}") String pwd) throws Exception {
        ComboPooledDataSource dataSource = new ComboPooledDataSource();
        dataSource.setUser(user);
        dataSource.setPassword(pwd);
        dataSource.setJdbcUrl("jdbc:mysql://localhost:3306/scw_0515");
        dataSource.setDriverClass(dirverClass);
        return dataSource;
    }
    
    public void setEmbeddedValueResolver(StringValueResolver resolver) {
        this.valueResolver = resolver;
        dirverClass = valueResolver.resolveStringValue("${db.driverClass}");
    }

}
```

可以看到，我们使用@Profile("dev")注解来标识在开发环境下注册devDataSource；使用@Profile("test")注解来标识在测试环境下注册testDataSource；使用@Profile("prod")注解来标识在生产环境下注册prodDataDource。


此时，我们运行IOCTest_Profile类中的test01()方法，**发现控制台并未输出任何结果信息。** 说明我们为不同的数据源添加@Profile注解后，默认是不会向IOC容器中注册bean的，需要我们根据环境显示指定向IOC容器中注册相应的bean。

换句话说，通过@Profile注解加了环境标识的bean，只有这个环境被激活的时候，相应的bean才会被注册到IOC容器中。

如果我们需要一个默认的环境，那么该怎么办呢？此时，我们可以通过@Profile("default")注解来标识一个默认的环境，例如，我们将devDataSource环境标识为默认环境，如下所示。


```java
   @Profile("default")
// @Profile("dev") // 定义了一个环境标识，只有当dev环境被激活以后，我们这个bean才能被注册进来
    @Bean("devDataSource")
    public DataSource dataSourceDev(@Value("${db.password}") String pwd) throws Exception {
        ComboPooledDataSource dataSource = new ComboPooledDataSource();
        dataSource.setUser(user);
        dataSource.setPassword(pwd);
        dataSource.setJdbcUrl("jdbc:mysql://localhost:3306/ssm_crud");
        dataSource.setDriverClass(dirverClass);
        return dataSource;
    }
```

此时，我们运行IOCTest_Profile类中的test01()方法，输出的结果信息如下所示。

![image-20210911094231920](images\image-20210911094231920.png)

可以看到，我们在devDataSource数据源上使用`@Profile("default")`注解将其设置为默认的数据源，运行测试方法时Eclipse控制台会输出devDataSource。

接下来，我们将devDataSource数据源上的`@Profile("default")`注解还原成`@Profile("dev")`注解，重新标识它为一个开发环境下注册的数据源，好方便下面的测试。

我们如何根据不同的环境来注册相应的bean呢？例如，我们想在程序运行的时候，将其切换到测试环境下。

通过写代码的方式来激活某种环境

1. 在bean上加@Profile注解，其value属性值为环境标识，可以自定义
2. 使用AnnotationConfigApplicationContext类的无参构造方法创建容器
3. 设置容器环境，其值为第1步设置的环境标识
4. 设置容器的配置类
5. 刷新容器

提示：2、4、5步其实是AnnotationConfigApplicationContext类中带参构造方法的步骤，以上这几个步骤相当于是把其带参构造方法拆开，在其中插入一条语句设置容器环境，这些我们可以在AnnotationConfigApplicationContext类的带参构造方法中看到，如下所示。


![image-20210911094508766](images\image-20210911094508766.png)

我们先在程序中调用AnnotationConfigApplicationContext类的无参构造方法来创建一个IOC容器，然后在容器进行初始化之前，为其设置相应的环境，接着再为容器设置主配置类，最后刷新一下容器。例如，我们将IOC容器设置为测试环境，如下所示。

```java
@Test
public void test02() {
    // 1. 使用无参构造器创建一个IOC容器
    AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext();
    // 2. 在我们容器还没启动创建其他bean之前，先设置需要激活的环境（可以设置激活多个环境哟）
    applicationContext.getEnvironment().setActiveProfiles("test");
    // 3. 注册主配置类
    applicationContext.register(MainConfigOfProfile.class);
    // 4. 启动刷新容器
    applicationContext.refresh();

    String[] namesForType = applicationContext.getBeanNamesForType(DataSource.class);
    for (String name : namesForType) {
        System.out.println(name);
    }

    // 关闭容器
    applicationContext.close();
}
```

此时，我们运行以上test02()方法，输出的结果信息如下所示。

![image-20210911094621417](images\image-20210911094621417.png)

# 五、AOP

## 什么是AOP？

AOP（Aspect Orient Programming），直译过来就是面向切面编程。AOP是一种编程思想，是面向对象编程（OOP）的一种补充。面向对象编程将程序抽象成各个层次的对象，而面向切面编程是将程序抽象成各个切面。

比如，在《Spring实战（第4版）》中有如下一张图描述了AOP的大体模型。


![image-20210912091129885](images\image-20210912091129885.png)

从这张图中，我们可以看出：所谓切面，其实就相当于应用对象间的横切点，我们可以将其单独抽象为单独的模块。

**总之一句话：AOP是指在程序的运行期间动态地将某段代码切入到指定方法、指定位置进行运行的编程方式。AOP的底层是使用动态代理实现的。**

## 实战案例

### （一）导入AOP依赖

要想搭建AOP环境，首先，我们就需要在项目的pom.xml文件中引入AOP的依赖，如下所示。

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-aspects</artifactId>
    <version>5.0.4.RELEASE</version>
</dependency>
```

其实，Spring AOP对面向切面编程做了一些简化操作，我们只需要加上几个核心注解，AOP就能工作起来。

### （二）定义目标类

创建一个业务逻辑类，例如MathCalculator，用于处理数学计算上的一些逻辑。比如，我们在MathCalculator类中定义了一个除法操作，返回两个整数类型值相除之后的结果，如下所示。

```java
public class MathCalculator {

    public int div(int i, int j) {
        System.out.println("MathCalculator...div...");
        return i / j;
    }
}
```

现在，我们希望在以上这个业务逻辑类中的除法运算之前，记录一下日志，例如记录一下哪个方法运行了，用的参数是什么，运行结束之后它的返回值又是什么，顺便可以将其打印出来，还有如果运行出异常了，那么就捕获一下异常信息。

或者，你会有这样一个需求，即希望在业务逻辑运行的时候将日志进行打印，而且是在方法运行之前、方法运行结束、方法出现异常等等位置，都希望会有日志打印出来。


### （三）定义切面类

创建一个切面类，例如LogAspects，在该切面类中定义几个打印日志的方法，以这些方法来动态地感知MathCalculator类中的div()方法的运行情况。如果需要切面类来动态地感知目标类方法的运行情况，那么就需要使用Spring AOP中的一系列通知方法了。

AOP中的通知方法及其对应的注解与含义如下：

​	前置通知（对应的注解是@Before）：在目标方法运行之前运行
​	后置通知（对应的注解是@After）：在目标方法运行结束之后运行，无论目标方法是正常结束还是异常结束都会执行
​	返回通知（对应的注解是@AfterReturning）：在目标方法正常返回之后运行
​	异常通知（对应的注解是@AfterThrowing）：在目标方法运行出现异常之后运行
​	环绕通知（对应的注解是@Around）：动态代理，我们可以直接手动推进目标方法运行（joinPoint.procced()）
这里我不想一下子就把LogAspects类的完整代码贴出来，虽然可以这样做，但没必要。我的初衷是想向大家阐述这个切面类是如何一点一点写出来的，以及都做了哪些优化。试想一下，你一开始是不是这样写的：

```java
/**
 * 切面类
 * @author liayun
 *
 */
public class LogAspects {

    // @Before：在目标方法（即div方法）运行之前切入，public int com.harry.spring.aop.MathCalculator.div(int, int)这一串就是切入点表达式，指定在哪个方法切入
    @Before("public int com.harry.spring.aop.MathCalculator.*(..)")
    public void logStart() {
        System.out.println("除法运行......@Before，参数列表是：{}");
    }

    // 在目标方法（即div方法）结束时被调用
    @After("public int com.harry.spring.aop.MathCalculator.*(..)")
    public void logEnd() {
        System.out.println("除法结束......@After");
    }

    // 在目标方法（即div方法）正常返回了，有返回值，被调用
    @AfterReturning("public int com.harry.spring.aop.MathCalculator.*(..)")
    public void logReturn() {
        System.out.println("除法正常返回......@AfterReturning，运行结果是：{}");
    }

    // 在目标方法（即div方法）出现异常，被调用
    @AfterThrowing("public int com.harry.spring.aop.MathCalculator.*(..)")
    public void logException() {
        System.out.println("除法出现异常......异常信息：{}");
    }

}
```



如果切入点表达式都一样的情况下，那么我们可以抽取出一个公共的切入点表达式，就像下面这样。

```java
public class LogAspects {

    // 如果切入点表达式都一样的情况下，那么我们可以抽取出一个公共的切入点表达式
    @Pointcut("execution(public int com.harry.spring.aop.MathCalculator.*(..))")
    public void pointCut() {}


    // @Before：在目标方法（即div方法）运行之前切入，public int com.harry.spring.aop.MathCalculator.div(int, int)这一串就是切入点表达式，指定在哪个方法切入
    @Before("pointCut()")
    public void logStart() {
        System.out.println("除法运行......@Before，参数列表是：{}");
    }

    // 在目标方法（即div方法）结束时被调用
    @Before("pointCut()")
    public void logEnd() {
        System.out.println("除法结束......@After");
    }
}
```

第二种情况，如果是外部类（即其他的切面类）引用，那么就得在通知注解中写方法的全名了

最后，千万别忘了一点，那就是必须告诉Spring哪个类是切面类，要做到这一点很简单，只需要给切面类上加上一个@Aspect注解即可

```java
@Aspect
public class LogAspects {
```

### （四）将目标类和切面类加入到IOC容器

新建一个配置类，例如MainConfigOfAOP，并使用@Configuration注解标注这是一个Spring的配置类，同时使用@EnableAspectJAutoProxy注解开启基于注解的AOP模式。在MainConfigOfAOP配置类中，使用@Bean注解将业务逻辑类（目标方法所在类）和切面类都加入到IOC容器中，如下所示。


```java
@EnableAspectJAutoProxy
@Configuration
public class MainConfigOfAOP {

    // 将业务逻辑类（目标方法所在类）加入到容器中
    @Bean
    public MathCalculator calculator() {
        return new MathCalculator();
    }

    // 将切面类加入到容器中
    @Bean
    public LogAspects logAspects() {
        return new LogAspects();
    }

}
```

一定不要忘了给MainConfigOfAOP配置类标注@EnableAspectJAutoProxy注解！在Spring中，未来会有很多的@EnableXxx注解，它们的作用都是开启某一项功能，来替换我们以前的那些配置文件。

### （五）测试

创建一个单元测试类，例如IOCTest_AOP，并在该测试类中创建一个test01()方法，如下所示

```java
public class IOCTest_AOP {

    @Test
    public void test01() {
        AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext(MainConfigOfAOP.class);

        // 不要自己创建这个对象
        // MathCalculator mathCalculator = new MathCalculator();
        // mathCalculator.div(1, 1);

        // 我们要使用Spring容器中的组件
        MathCalculator mathCalculator = applicationContext.getBean(MathCalculator.class);
        mathCalculator.div(1, 1);

        // 关闭容器
        applicationContext.close();
    }

}
```

然后，运行以上IOCTest_AOP类中的test01()方法，输出的结果信息如下所示。

![image-20210912093052535](images\image-20210912093052535.png)

可以看到，执行了切面类中的方法，并打印出了相关信息。**但是并没有打印参数列表和运行结果。**

要想打印出参数列表和运行结果，就需要对LogAspects切面类中的方法进行优化，优化后的结果如下所示。

```java
/**
 * 切面类
 * @author liayun
 *
 */
@Aspect
public class LogAspects {

    // 如果切入点表达式都一样的情况下，那么我们可以抽取出一个公共的切入点表达式
    @Pointcut("execution(public int com.harry.spring.aop.MathCalculator.*(..))")
    public void pointCut() {}


    // @Before：在目标方法（即div方法）运行之前切入，public int com.harry.spring.aop.MathCalculator.div(int, int)这一串就是切入点表达式，指定在哪个方法切入
    @Before("pointCut()")
    public void logStart(JoinPoint joinPoint) {
        Object[] args = joinPoint.getArgs(); // 拿到参数列表，即目标方法运行需要的参数列表
        System.out.println(joinPoint.getSignature().getName() + "运行......@Before，参数列表是：{" + Arrays.asList(args) + "}");

    }

    // 在目标方法（即div方法）结束时被调用
    @After("pointCut()")
    public void logEnd(JoinPoint joinPoint) {
        System.out.println(joinPoint.getSignature().getName() + "结束......@After");
    }

    // 在目标方法（即div方法）正常返回了，有返回值，被调用
    @AfterReturning(value="pointCut()", returning="result") // returning来指定我们这个方法的参数谁来封装返回值
    // 一定要注意：JoinPoint这个参数要写，一定不能写到后面，它必须出现在参数列表的第一位，否则Spring也是无法识别的，就会报错
    public void logReturn(JoinPoint joinPoint, Object result) {
        System.out.println(joinPoint.getSignature().getName() + "正常返回......@AfterReturning，运行结果是：{" + result + "}");
    }

    // 在目标方法（即div方法）出现异常，被调用
    @AfterThrowing("pointCut()")
    public void logException() {
        System.out.println("除法出现异常......异常信息：{}");
    }

}
```

**这里，需要注意的是，JoinPoint参数一定要放在参数列表的第一位，否则Spring是无法识别的，那自然就会报错了。**

此时，我们再次运行IOCTest_AOP类中的test01()方法，输出的结果信息如下所示。

![image-20210912094952311](images\image-20210912094952311.png)

如果目标方法运行时出现了异常，而我们又想拿到这个异常信息，那么该怎么办呢？只须对LogAspects切面类中的logException()方法进行优化即可，优化后的结果如下所示。

```java
@AfterThrowing(value="pointCut()", throwing="exception")
public void logException(JoinPoint joinPoint, Exception exception) {
    // System.out.println("除法出现异常......异常信息：{}");

    System.out.println(joinPoint.getSignature().getName() + "出现异常......异常信息：{" + exception + "}");
}
```

可以看到，JoinPoint参数是放在了参数列表的第一位。

接下来，我们就在MathCalculator类的div()方法中模拟抛出一个除零异常，来测试下异常情况，如下所示。

```java
public class IOCTest_AOP {

    @Test
    public void test01() {
        AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext(MainConfigOfAOP.class);

        // 不要自己创建这个对象
        // MathCalculator mathCalculator = new MathCalculator();
        // mathCalculator.div(1, 1);

        // 不要自己创建这个对象
        // MathCalculator mathCalculator = new MathCalculator();
        // mathCalculator.div(1, 1);

        // 我们要使用Spring容器中的组件
        MathCalculator mathCalculator = applicationContext.getBean(MathCalculator.class);
        mathCalculator.div(1, 0);

        // 关闭容器
        applicationContext.close();
    }

}
```

## @EnableAspectJAutoProxy注解

@EnableAspectJAutoProxy注解
在配置类上添加@EnableAspectJAutoProxy注解，便能够开启注解版的AOP功能。也就是说，如果要使注解版的AOP功能起作用的话，那么就得需要在配置类上添加@EnableAspectJAutoProxy注解。我们先来看下@EnableAspectJAutoProxy注解的源码，如下所示
![image-20210912095449576](images\image-20210912095449576.png)

从源码中可以看出，@EnableAspectJAutoProxy注解使用@Import注解给容器中引入了AspectJAutoProxyRegister组件。那么，这个AspectJAutoProxyRegistrar组件又是什么呢？我们继续点进去到AspectJAutoProxyRegistrar类的源码中，如下所示。

![image-20210912095651546](images\image-20210912095651546.png)

可以看到AspectJAutoProxyRegistrar类实现了ImportBeanDefinitionRegistrar接口。我们再点进去到ImportBeanDefinitionRegistrar接口的源码中，如下所示。

![image-20210912095735826](images\image-20210912095735826.png)

也就是说，@EnableAspectJAutoProxy注解使用AspectJAutoProxyRegistrar对象自定义组件，并将相应的组件添加到了IOC容器中。

那么，@EnableAspectJAutoProxy注解使用AspectJAutoProxyRegistrar对象向容器中注册了一个什么bean呢？

### 调试Spring源码

首先，我们需要给这个AspectJAutoProxyRegistrar类打一个断点，断点就打在该类的registerBeanDefinitions()方法处，如下所示。

![image-20210912095957636](images\image-20210912095957636.png)

然后，我们以debug的方式来运行IOCTest_AOP类中的test01()方法。运行后程序进入到断点位置，如下所示。

![image-20210912100355311](images\image-20210912100355311.png)

可以看到，程序已经暂停在断点位置了。

我们还可以看到，在AspectJAutoProxyRegistrar类的registerBeanDefinitions()方法里面，首先调用了AopConfigUtils类的registerAspectJAnnotationAutoProxyCreatorIfNecessary()方法来注册registry，单看registerAspectJAnnotationAutoProxyCreatorIfNecessary()方法也不难理解，字面含义就是：如果需要的话，那么就注册一个AspectJAnnotationAutoProxyCreator组件。

接着，我们进入到AopConfigUtils类的registerAspectJAnnotationAutoProxyCreatorIfNecessary()方法中，如下所示。

![image-20210912100515053](images\image-20210912100515053.png)

在AopConfigUtils类的registerAspectJAnnotationAutoProxyCreatorIfNecessary()方法中，直接调用了重载的registerAspectJAnnotationAutoProxyCreatorIfNecessary()方法。我们继续跟进代码，如下所示。


![image-20210912100609910](images\image-20210912100609910.png)

可以看到在重载的registerAspectJAnnotationAutoProxyCreatorIfNecessary()方法中直接调用了registerOrEscalateApcAsRequired()方法，并且在registerOrEscalateApcAsRequired()方法中，传入了AnnotationAwareAspectJAutoProxyCreator.class对象。


![image-20210912101244583](images\image-20210912101244583.png)

我们可以看到，在registerOrEscalateApcAsRequired()方法中，接收到的Class对象的类型为org.springframework.aop.aspectj.annotation.AnnotationAwareAspectJAutoProxyCreator。

除此之外，我们还可以看到，在registerOrEscalateApcAsRequired()方法中会做一个判断，即首先判断registry（也就是IOC容器）是否包含名称为org.springframework.aop.config.internalAutoProxyCreator的bean，如下所示。


![image-20210912101523348](images\image-20210912101523348.png)

如果registry中包含名称为org.springframework.aop.config.internalAutoProxyCreator的bean，那么就进行相应的处理。从Spring的源码来看，就是将名称为org.springframework.aop.config.internalAutoProxyCreator的bean从容器中取出，并且判断cls对象的name值和apcDefinition的beanClassName值是否相等，若不相等，则获取apcDefinition和cls它俩的优先级，如果apcDefinition的优先级小于cls的优先级，那么将apcDefinition的beanClassName设置为cls的name值。相对来说，理解起来还是比较简单的。

由于我们这里是第一次运行程序，容器中应该还没有包含名称为org.springframework.aop.config.internalAutoProxyCreator的bean，所以此时并不会进入到if判断条件中。我们继续往下看代码，如下所示。

![image-20210912101714285](images\image-20210912101714285.png)

这儿，会使用RootBeanDefinition来创建一个bean的定义信息（即beanDefinition），并且将org.springframework.aop.aspectj.annotation.AnnotationAwareAspectJAutoProxyCreator的Class对象作为参数传递进来。


最终在AopConfigUtils类的registerOrEscalateApcAsRequired()方法中，会通过registry调用registerBeanDefinition()方法注册组件，如下所示。

![image-20210912101942200](images\image-20210912101942200.png)

注册的组件的类型是org.springframework.aop.aspectj.annotation.AnnotationAwareAspectJAutoProxyCreator，组件的名字是org.springframework.aop.config.internalAutoProxyCreator。


我们继续往下看代码，最终会回到AspectJAutoProxyRegistrar类的registerBeanDefinitions()方法中。

![image-20210912102300120](images\image-20210912102300120.png)

接下来，我们继续往下看代码，即查看AspectJAutoProxyRegistrar类中的registerBeanDefinitions()方法的源码，如下所示。

![image-20210912102407275](images\image-20210912102407275.png)

可以看到，通过AnnotationConfigUtils类的attributesFor()方法来获取@EnableAspectJAutoProxy注解的信息。接着，就是判断proxyTargetClass属性的值是否为true，若为true则调用AopConfigUtils类的forceAutoProxyCreatorToUseClassProxying()方法；继续判断exposeProxy属性的值是否为true，若为true则调用AopConfigUtils类的forceAutoProxyCreatorToExposeProxy()方法，其实就是暴露一些什么代理的这些bean，这个以后我们可以再说。

**综上，向Spring的配置类上添加@EnableAspectJAutoProxy注解之后，会向IOC容器中注册AnnotationAwareAspectJAutoProxyCreator，翻译过来就叫注解装配模式的AspectJ切面自动代理创建器。**

这个AnnotationAwareAspectJAutoProxyCreator又是什么呢，在研究它之前，我们来看下AnnotationAwareAspectJAutoProxyCreator类的结构图。

![image-20210912102527812](images\image-20210912102527812.png)

可以看到，它继承了很多东西，我们简单梳理下AnnotationAwareAspectJAutoProxyCreato类的核心继承关系，如下所示。

AnnotationAwareAspectJAutoProxyCreator
    ->AspectJAwareAdvisorAutoProxyCreator（父类）
        ->AbstractAdvisorAutoProxyCreator（父类）
            ->AbstractAutoProxyCreator（父类）
                implements SmartInstantiationAwareBeanPostProcessor, BeanFactoryAware（两个接口）

查看继承关系可以发现，此类实现了Aware与BeanPostProcessor接口，这两个接口都和Spring bean的初始化有关，由此可以推测此类的主要处理方法都来自于这两个接口中的实现方法。

通过以上继承关系，我们也知道了，它最终会实现两个接口，分别是：

- BeanPostProcessor：后置处理器，即在bean初始化完成前后做些事情
- BeanFactoryAware：自动注入BeanFactory

也就是说，AnnotationAwareAspectJAutoProxyCreator不仅是一个后置处理器，还是一个BeanFactoryAware接口的实现类。那么我们就来分析它作为后置处理器，到底做了哪些工作，以及它作为BeanFactoryAware接口的实现类，又做了哪些工作，只要把这个分析清楚，AOP的整个原理就差不多出来了。

### 为AnnotationAwareAspectJAutoProxyCreator组件里面和后置处理器以及Aware接口有关的方法打上断点

接下来，我们就要为AnnotationAwareAspectJAutoProxyCreator这个组件里面和后置处理器以及Aware接口有关的方法都打上断点，看一下它们何时运行，以及都做了些什么事。

在打断点之前，我们还是得小心分析一下，因为AnnotationAwareAspectJAutoProxyCreator这个组件的继承关系还是蛮复杂的。由于是从AbstractAutoProxyCreator这个抽象类开始实现SmartInstantiationAwareBeanPostProcessor以及BeanFactoryAware这俩接口的，如果我们直接来AnnotationAwareAspectJAutoProxyCreator这个类里面找与Aware接口以及BeanPostProcessor接口有关的方法，是极有可能找不到的，所以我们还是得从它的最开始的父类（即AbstractAutoProxyCreator）开始分析。

我们找到该抽象类，并在里面查找与Aware接口以及BeanPostProcessor接口有关的方法，结果都是可以找到的。该抽象类中的setBeanFactory()方法就是与Aware接口有关的方法，因此我们将断点打在该方法上，如下图所示。

![image-20210912103158259](images\image-20210912103158259.png)

此外，我们还得找到该抽象类中与BeanPostProcessor接口有关的方法，即只要发现有与后置处理器相关的逻辑，就给所有与后置处理器有关的逻辑都打上断点。打的断点有两处，一处是在postProcessBeforeInstantiation()方法上，如下图所示。

![image-20210912103259672](images\image-20210912103259672.png)

一处是在postProcessAfterInitialization()方法上，如下图所示。

![image-20210912103551922](images\image-20210912103551922.png)

接下来，我们再来看它的子类（即AbstractAdvisorAutoProxyCreator），从顶层开始一点一点往上分析。

在该抽象类中，我们只能找到一个与Aware接口有关的方法，即setBeanFactory()方法，虽然父类有setBeanFactory()方法，但是在这个子类里面已经把它重写了，因此最终调用的应该就是它。

![image-20210912103701342](images\image-20210912103701342.png)

注意，在重写的时候，在setBeanFactory()方法里面会调用一个initBeanFactory()方法。除此之外，该抽象类中就没有跟后置处理器有关的方法了。

接下来，我们就应该来看AspectJAwareAdvisorAutoProxyCreator这个类了，但由于这个类里面没有跟BeanPostProcessor接口有关的方法，所以我们就不必看这个类了，略过。

接下来，我们就要来看最顶层的类了，即AnnotationAwareAspectJAutoProxyCreator。查看该类时，发现有这样一个initBeanFactory()方法，我们在该方法上打上一个断点就好，如下图所示。


![image-20210912103841654](images\image-20210912103841654.png)

为什么在该类里面会有这个方法呢？因为我们在它的父类里面会调用setBeanFactory()方法，而在该方法里面又会调用initBeanFactory()方法，虽然父类里面有写，但是又被它的子类给重写了，所以说相当于父类中的setBeanFactory()方法还是得调用它。

综上，我们通过简单的人工分析，为这个AnnotationAwareAspectJAutoProxyCreator类中有关后置处理器以及自动装配BeanFactoryAware接口的这些方法都打上了一些断点，接下来，我们就要来进行debug调试分析了。

不过在这之前，我们还得为MainConfigOfAOP配置类中的如下两个方法打上断点。

![image-20210912103957426](images\image-20210912103957426.png)

### 创建和注册AnnotationAwareAspectJAutoProxyCreator的过程

以debug模式来运行IOCTest_AOP测试类之后，会先来到AbstractAdvisorAutoProxyCreator类的setBeanFactory()方法中，如下图所示

![image-20210913191520041](images\image-20210913191520041.png)

们这就来分析一下，在左上角的方法调用栈中，仔细查找，就会在前面找到一个test01()方法，它其实就是IOCTest_AOP测试类中的测试方法，我们就从该方法开始分析，然后详细记录一下方法调用栈中整个的方法调用流程。

鼠标单击方法调用栈中的那个test01()方法，此时，我们会进入到IOCTest_AOP测试类中的test01()方法中，如下图所示。

![image-20210913191629522](images\image-20210913191629522.png)

可以看到这一步是传入主配置类来创建IOC容器，怎么创建的呢？我们点击方法调用栈中test01()方法上面的那个方法，就来到下面这个地方了。

![image-20210913191853493](images\image-20210913191853493.png)

可以看到，传入主配置类来创建IOC容器使用的是AnnotationConfigApplicationContext类的有参构造器，它具体分为下面三步：

1. 首先使用无参构造器创建对象
2. 再来把主配置类注册进来
3. 最后调用refresh()方法刷新容器，刷新容器就是要把容器中的所有bean都创建出来，也就是说这就像初始化容器一样

接下来，我们来看看容器刷新是怎么做的？我们继续跟进方法调用栈，如下图所示，可以看到现在是定位到了AbstractApplicationContext抽象类的refresh()方法中。

![image-20210913192157421](\images\image-20210913192157421.png)

![image-20210913192244077](images\image-20210913192244077.png)

其中，该refresh()方法中有一行非常重要的代码，那就是：

```java
// Register bean processors that intercept bean creation.* 
registerBeanPostProcessors(beanFactory);
```

即注册bean的后置处理器。它的作用是什么呢？我们可以看一下它上面的注释，它就是用来方便拦截bean的创建的，那么这个后置处理器的注册逻辑又是什么样的呢？

我们继续跟进方法调用栈，可以看到现在是定位到了如下图所示的地方。

![image-20210913192500305](images\image-20210913192500305.png)

我们继续跟进方法调用栈，如下图所示，可以看到现在是定位到PostProcessorRegistrationDelegate类的registerBeanPostProcessors()方法中了。

![image-20210913192849852](images\image-20210913192849852.png)

registerBeanPostProcessors()方法中的代码

![在这里插入图片描述](images\ASAD213213.jpg)

分析一下，到底是怎么注册bean的后置处理器的。

1. 先按照类型拿到IOC容器中所有需要创建的后置处理器，即先获取IOC容器中已经定义了的需要创建对象的所有BeanPostProcessor。这可以从如下这行代码中得知：

```java
String[] postProcessorNames = beanFactory.getBeanNamesForType(BeanPostProcessor.class, true, false);
```

为什么IOC容器中会有一些已定义的BeanPostProcessor呢？这是因为在前面创建IOC容器时，需要先传入配置类，而我们在解析配置类的时候，由于这个配置类里面有一个@EnableAspectJAutoProxy注解，对于该注解，我们之前也说过，它会为我们容器中注册一个AnnotationAwareAspectJAutoProxyCreator（后置处理器），这还仅仅是这个@EnableAspectJAutoProxy注解做的事，除此之外，容器中还有一些默认的后置处理器的定义。

所以，程序运行到这，容器中已经有一些我们将要用的后置处理器了，只不过现在还没创建对象，都只是一些定义，也就是说容器中有哪些后置处理器。

2.继续往下看这个registerBeanPostProcessors()方法，可以看到它里面还有其他的逻辑，如下所示：

```java
beanFactory.addBeanPostProcessor(new BeanPostProcessorChecker(beanFactory, beanProcessorTargetCount));
```

说的是给beanFactory中额外还加了一些其他的BeanPostProcessor，也就是说给容器中加别的BeanPostProcessor。

3.继续往下看这个registerBeanPostProcessors()方法，发现它里面还有这样的注释，如下所示：

```java
// Separate between BeanPostProcessors that implement PriorityOrdered,
// Ordered, and the rest.
List<BeanPostProcessor> priorityOrderedPostProcessors = new ArrayList<BeanPostProcessor>();
/************下面是代码，省略************/

```

说的是分离这些BeanPostProcessor，看哪些是实现了PriorityOrdered接口的，哪些又是实现了Ordered接口的，包括哪些是原生的没有实现什么接口的。所以，在这儿，对这些BeanPostProcessor还做了一些处理，所做的处理看以下代码便一目了然

```java
for (String ppName : postProcessorNames) {
    if (beanFactory.isTypeMatch(ppName, PriorityOrdered.class)) {
        BeanPostProcessor pp = beanFactory.getBean(ppName, BeanPostProcessor.class);
        priorityOrderedPostProcessors.add(pp);
        if (pp instanceof MergedBeanDefinitionPostProcessor) {
            internalPostProcessors.add(pp);
        }
    }
    else if (beanFactory.isTypeMatch(ppName, Ordered.class)) {
        orderedPostProcessorNames.add(ppName);
    }
    else {
        nonOrderedPostProcessorNames.add(ppName);
    }
}
```

拿到IOC容器中所有这些BeanPostProcessor之后，是怎么处理的呢？它是来看我们这个BeanPostProcessor是不是实现了PriorityOrdered接口，我们不妨看一下PriorityOrdered接口的源码，如下图所示。

![image-20210913193850416](images\image-20210913193850416.png)

可以看到该接口其实是Ordered接口旗下的，也就是说它继承了Ordered接口。进一步说明，IOC容器中的那些BeanPostProcessor是有优先级排序的。

现在我们知道了这样一个结论，那就是：**IOC容器中的那些BeanPostProcessor可以实现PriorityOrdered以及Ordered这些接口来定义它们工作的优先级，即谁先前谁先后。**

回到代码中，就不难看到，它是在这儿将这些BeanPostProcessor做了一下划分，如果BeanPostProcessor实现了PriorityOrdered接口，那么就将其保存在名为priorityOrderedPostProcessors的List集合中，并且要是该BeanPostProcessor还是MergedBeanDefinitionPostProcessor这种类型的，则还得将其保存在名为internalPostProcessors的List集合中。

4.继续往下看这个registerBeanPostProcessors()方法，主要是看其中的注释，不难发现有以下三步：

1. 优先注册实现了PriorityOrdered接口的BeanPostProcessor
2. 再给容器中注册实现了Ordered接口的BeanPostProcessor
3. 最后再注册没实现优先级接口的BeanPostProcessor

所谓的注册BeanPostProcessor又是什么呢，现在即将要创建的名称为internalAutoProxyCreator的组件（其实它就是我们之前经常讲的AnnotationAwareAspectJAutoProxyCreator）实现了Ordered接口，这只要查看AnnotationAwareAspectJAutoProxyCreator类的源码便知，一级一级地往上查

![image-20210913195023774](images\image-20210913195023774.png)

再次回到程序停留的地方可以看到，是先拿到要注册的BeanPostProcessor的名字，然后再从beanFactory中来获取。

接下来，我们就要获取相应名字的BeanPostProcessor了，继续跟进方法调用栈，如下图所示，可以看到现在是定位到了AbstractBeanFactory抽象类的getBean()方法中。

![image-20210913195336569](images\image-20210913195336569.png)

我们继续跟进方法调用栈，如下图所示，可以看到现在是定位到了AbstractBeanFactory抽象类的doGetBean()方法中。

![image-20210913195432869](images\image-20210913195432869.png)

这个方法特别特别的长，这儿就不再详细分析它了，只须关注程序停留的这行代码即可。这行代码的意思是调用getSingleton()方法来获取单实例的bean，但是呢，IOC容器中第一次并不会有这个bean，所以第一次获取它肯定是会有问题的。

我们继续跟进方法调用栈，如下图所示，可以看到现在是定位到了DefaultSingletonBeanRegistry类的getSingleton()方法中。

![image-20210913195626272](images\image-20210913195626272.png)

也就是说如果从IOC容器中第一次获取单实例的bean出现问题，也即获取不到时，那么就会调用singletonFactory的getObject()方法。

我们继续跟进方法调用栈，如下图所示，可以看到现在又定位到了AbstractBeanFactory抽象类的doGetBean()方法中。
![image-20210913195843816](images\image-20210913195843816.png)

可以发现，现在就是来创建bean的，也就是说如果获取不到那么就创建bean。**咱们现在就是需要注册BeanPostProcessor，说白了，实际上就是创建BeanPostProcessor对象，然后保存在容器中。**

那么接下来，我们就来看看是如何创建出名称为internalAutoProxyCreator的BeanPostProcessor的，它的类型其实就是我们之前经常说的AnnotationAwareAspectJAutoProxyCreator。我们就以它为例，来看看它这个对象是怎么创建出来的。

我们继续跟进方法调用栈，如下图所示，可以看到现在是定位到了AbstractAutowireCapableBeanFactory抽象类的createBean()方法中

![image-20210913200153514](images\image-20210913200153514.png)

接着再跟进方法调用栈，如下图所示，可以看到现在是定位到了AbstractAutowireCapableBeanFactory抽象类的doCreateBean()方法中

![image-20210913200356031](images\image-20210913200356031.png)

程序停留在这儿，就是在初始化bean实例，说明bean实例已经创建好了，如果你要不信的话，那么可以往前翻阅该doCreateBean()方法，这时你应该会看到一个createBeanInstance()方法，说的就是bean实例的创建。创建的是哪个bean实例呢？就是名称为internalAutoProxyCreator的实例，该实例的类型就是我们之前经常说的AnnotationAwareAspectJAutoProxyCreator，即创建这个类型的实例。创建好了之后，就在程序停留的地方进行初始化。
所以，整个的过程就应该是下面这个样子的：

1. 首先创建bean的实例
2. 然后给bean的各种属性赋值（即调用populateBean()方法）
3. 接着初始化bean（即调用initializeBean()方法），这个初始化bean其实特别地重要，因为我们这个后置处理器就是在bean初始化的前后进行工作的。

接下来，我们就来看看这个bean的实例是如何初始化的。继续跟进方法调用栈，如下图所示，可以看到现在是定位到了AbstractAutowireCapableBeanFactory抽象类的initializeBean()方法中。

![image-20210913201142381](images\image-20210913201142381.png)

我就在这儿为大家详细分析一下**初始化bean的流程**。

1. 首先我们进入invokeAwareMethods()这个方法里面看一下，如下图所示。

![image-20210913201242735](images\image-20210913201242735.png)

其实，这个方法是来判断我们这个bean对象是不是Aware接口的，如果是，并且它还是BeanNameAware、BeanClassLoaderAware以及BeanFactoryAware这几个Aware接口中的其中一个，那么就调用相关的Aware接口方法，即处理Aware接口的方法回调。
现在当前的这个bean叫internalAutoProxyCreator，并且这个bean对象已经被创建出来了，创建出来的这个bean对象之前我们也分析过，它是有实现BeanFactoryAware接口的，故而会调用相关的Aware接口方法，这也是程序为什么会停留在invokeAwareMethods()这个方法的原因。

2.还是回到AbstractAutowireCapableBeanFactory抽象类的initializeBean()方法中，即程序停留的地方。如果invokeAwareMethods()这个方法执行完了以后，那么后续又会发生什么呢？

往下翻阅initializeBean()方法，会发现有一个叫applyBeanPostProcessorsBeforeInitialization的方法，如下图所示。

![image-20210913202844400](images\image-20210913202844400.png)



这个方法调用完以后，会返回一个被包装的bean。

该方法的意思其实就是应用后置处理器的postProcessBeforeInitialization()方法。

![image-20210913202629199](images\image-20210913202629199.png)

可以看到，它是拿到所有的后置处理器，然后再调用后置处理器的postProcessBeforeInitialization()方法，也就是说bean初始化之前后置处理器的调用在这儿。

3.还是回到程序停留的地方，继续往下翻阅initializeBean()方法，你会发现还有一个叫invokeInitMethods的方法，即执行自定义的初始化方法。

这个自定义的初始化方法呢，你可以用@bean注解来定义，指定一下初始化方法是什么，销毁方法又是什么.

4.自定义的初始化方法执行完以后，又有一个叫applyBeanPostProcessorsAfterInitialization的方法，该方法的意思其实就是应用后置处理器的postProcessAfterInitialization()方法。

![image-20210913202712577](images\image-20210913202712577.png)

依旧是拿到所有的后置处理器，然后再调用后置处理器的postProcessAfterInitialization()方法。

所以，后置处理器的这两个postProcessBeforeInitialization()与postProcessAfterInitialization()方法前后的执行，就是在这块体现的。


接下来，我们还是回到程序停留的地方，即下面这行代码处。

```java
invokeAwareMethods(beanName, bean);
```

调用initializeBean()方法初始化bean的时候，还得执行那些Aware接口的方，当前的这个bean它确实是实现了BeanFactoryAware接口。因此我们继续跟进方法调用栈，如下图所示，可以看到现在是定位到了AbstractAutowireCapableBeanFactory抽象类的invokeAwareMethods()方法中
![image-20210913203056881](images\image-20210913203056881.png)

再继续跟进方法调用栈，如下图所示，可以看到现在是定位到了AbstractAdvisorAutoProxyCreator抽象类的setBeanFactory()方法中。

![image-20210913203200237](images\image-20210913203200237.png)

可以看到现在调用的是AbstractAdvisorAutoProxyCreator抽象类中的setBeanFactory()方法。我们要创建的是AnnotationAwareAspectJAutoProxyCreator对象，但是调用的却是它父类的setBeanFactory()方法。


接下来，按下`F7`快捷键让程序往下运行，父类的setBeanFactory()方法便会被调用，再按下F7快捷键让程序往下运行，一直让程序运行到如下图所示的这行代码处。

![image-20210913203328473](images\image-20210913203328473.png)

可以看到父类的setBeanFactory()方法被调用完了。然后按下`F7`快捷键继续让程序往下运行，这时会运行到如下这行代码处。

```java
initBeanFactory((ConfigurableListableBeanFactory) beanFactory);
```

该initBeanFactory()方法就是用来初始化BeanFactory的。进入到当前方法内部，如下图所示，可以看到调用到了AnnotationAwareAspectJAutoProxyCreator这个类的initBeanFactory()方法中了，即调到了我们要给容器中创建的AspectJ自动代理创建器的initBeanFactory()方法中。
![image-20210913203549726](images\image-20210913203549726.png)

可以看到这个initBeanFactory()方法创建了两个东西，一个叫ReflectiveAspectJAdvisorFactory，还有一个叫BeanFactoryAspectJAdvisorsBuilderAdapter，它相当于把之前创建的aspectJAdvisorFactory以及beanFactory重新包装了一下，就只是这样。

至此，整个这么一个流程下来以后，咱们的这个BeanPostProcessor，我们是以AnnotationAwareAspectJAutoProxyCreator（就是@EnableAspectJAutoProxy这个注解核心导入的BeanPostProcessor）为例来讲解的，就创建成功了。并且还调用了它的initBeanFactory()方法得到了一些什么aspectJAdvisorFactory和aspectJAdvisorsBuilder，这两个知道一下就行了。至此，整个initBeanFactory()方法我们就说完了，也就是说我们整个的后置处理器的注册以及创建过程就说完了。
我们还是回过头回顾一下，一开始的这行代码是用来注册后置处理器。

```java
// Register bean processors that intercept bean creation.
registerBeanPostProcessors(beanFactory);
```

我们是以AnnotationAwareAspectJAutoProxyCreator为例来讲解的，现在你也应该知道整个后置处理器的创建以及注册流程了。

### 完成BeanFactory的初始化工作

注册完AnnotationAwareAspectJAutoProxyCreator后置处理器之后，接下来就得完成BeanFactory的初始化工作了。
我们还是以debug模式来运行IOCTest_AOP测试类，这时，应该还是会来到AbstractAdvisorAutoProxyCreator类的setBeanFactory()方法中，如下图所示。

![image-20210914194401438](images\image-20210914194401438.png)

我们按下`F9`快捷键直接运行到下一个断点，如下图所示，可以看到现在是定位到了AbstractAutoProxyCreator抽象类的setBeanFactory()方法中。

![image-20210914194515212](images\image-20210914194515212.png)

然后继续按下`F9`快捷键运行直到下一个断点，一直运行到如下图所示的这行代码处。

![image-20210914195128152](images\image-20210914195128152.png)

可以看到程序现在是停留在了AbstractAutoProxyCreator类的postProcessBeforeInstantiation()方法中，不过从方法调用栈中我们可以清楚地看到现在其实调用的是AnnotationAwareAspectJAutoProxyCreator的postProcessBeforeInstantiation()方法。

这个方法一定要引起注意，它跟我们之前经常讲到的后置处理器中的方法是有区别的。看一下BeanPostProcessor接口的源码，如下图所示，它里面有一个postProcessbeforeInitialization()方法。

![image-20210914195404145](\images\image-20210914195404145.png)

而现在这个方法是叫postProcessBeforeInstantiation

AnnotationAwareAspectJAutoProxyCreator它本身就是一个后置处理器，为何其中的方法叫postProcessBeforeInstantiation，而不是叫postProcessbeforeInitialization呢？因为后置处理器跟为后置处理器是不一样的，当前我们要用到的这个后置处理器（即AnnotationAwareAspectJAutoProxyCreator）实现的是一个叫SmartInstantiationAwareBeanPostProcessor的接口，而该接口继承的是InstantiationAwareBeanPostProcessor接口（它又继承了BeanPostProcessor接口），也就是说，AnnotationAwareAspectJAutoProxyCreator虽然是一个BeanPostProcessor，但是它却是InstantiationAwareBeanPostProcessor这种类型的，而InstantiationAwareBeanPostProcessor接口中声明的方法就叫postProcessBeforeInstantiation。

故而程序就停留到了AbstractAutoProxyCreator类的postProcessBeforeInstantiation()方法中。

鼠标单击方法调用栈中的那个test01()方法，此时，我们会进入到IOCTest_AOP测试类中的test01()方法中，如下图所示。

![image-20210914195751649](images\image-20210914195751649.png)

可以看到这一步还是传入主配置类来创建IOC容器，依旧会调用refresh()方法.

我们继续跟进方法调用栈，如下图所示，可以看到现在是定位到了AbstractApplicationContext抽象类的refresh()方法中。

![image-20210914200022022](images\image-20210914200022022.png)

可以看到，在这儿会调用finishBeanFactoryInitialization()方法，这是用来初始化剩下的单实例bean的。而在该方法前面，有一个叫registerBeanPostProcessors的方法，它是用来注册后置处理器的

注册完后置处理器之后，接下来就来到了finishBeanFactoryInitialization()方法处，以完成BeanFactory的初始化工作。所谓的完成BeanFactory的初始化工作，其实就是来创建剩下的单实例bean。为什么叫剩下的呢？因为IOC容器中的这些组件，比如一些BeanPostProcessor，早都已经在注册的时候就被创建了，所以会留一下没被创建的组件，让它们在这儿进行创建。

我们继续跟进方法调用栈，如下图所示，可以看到现在是定位到了AbstractApplicationContext抽象类的finishBeanFactoryInitialization()方法中。

![image-20210914200503264](images\image-20210914200503264.png)

就是说，这儿会继续调用preInstantiateSingletons()方法来创建剩下的单实例bean。

继续跟进方法调用栈，如下图所示，可以看到现在是定位到了DefaultListableBeanFactory类的preInstantiateSingletons()方法中。

![image-20210914200615916](images\image-20210914200615916.png)

在这儿会调用getBean()方法来获取一个bean，获取的是名称为`org.springframework.context.event.internalEventListenerProcessor`的bean，它跟我们目前的研究没什么关系。

既然没有关系，那为何还要获取这个bean呢？往前翻阅preInstantiateSingletons()方法，可以看到有一个for循环，它是来遍历一个beanNames的List集合的，这个beanNames又是什么呢？很明显它是一个List<String>集合，它里面保存的是容器中所有bean定义的名称，如下图所示。

![image-20210914200722894](images\image-20210914200722894.png)

### 完成BeanFactory的初始化工作的第一步

遍历获取容器中所有的bean，并依次创建对象，注意是依次调用getBean()方法来创建对象的。

此刻，咱们是来到了第一个bean的创建，只不过它跟我们目前的研究没什么关系。我们可以以它的创建为例来看一下这个bean到底是怎么来创建的。

我们继续跟进方法调用栈，如下图所示，可以看到现在是定位到了AbstractBeanFactory抽象类的getBean()方法中。

![image-20210914200918696](images\image-20210914200918696.png)

再继续跟进方法调用栈，如下图所示，可以看到现在是定位到了AbstractBeanFactory抽象类的doGetBean()方法中。

![image-20210914200959688](images\image-20210914200959688.png)

可以看到，获取单实例bean调用的是getSingleton()方法，并且会返回一个sharedInstance对象。其实，从该方法上面的注释中也能看出，这儿是来创建bean实例的。

其实呢，在这儿创建之前，sharedInstance变量已经提前声明过了，我们往前翻阅doGetBean()方法，就能看到已声明的sharedInstance变量了。

![image-20210914201105083](images\image-20210914201105083.png)

可以清楚地看到，在如下这行代码处是来第一次获取单实例bean。

```java
// Eagerly check singleton cache for manually registered singletons.
Object sharedInstance = getSingleton(beanName);
```

其实从注释中可以知道，它会提前先检查单实例的缓存中是不是已经人工注册了一些单实例的bean，若是则获取。

### 完成BeanFactory的初始化工作的第二步

也就是说，这个bean的创建不是说一下就创建好了的，它得**先从缓存中获取当前bean，如果能获取到，说明当前bean之前是被创建过的，那么就直接使用，否则的话再创建。**

往上翻阅AbstractBeanFactory抽象类的doGetBean()方法，可以看到有这样的逻辑：

![在这里插入图片描述](images\tttttttt.jgp)

可以看到，单实例bean是能获取就获取，不能获取才创建。**Spring就是利用这个机制来保证我们这些单实例bean只会被创建一次，也就是说只要创建好的bean都会被缓存起来。**

继续跟进方法调用栈，如下图所示，可以看到现在是定位到了DefaultSingletonBeanRegistry类的getSingleton()方法中。

![image-20210914201707920](images\image-20210914201707920.png)

这儿是调用单实例工厂来进行创建单实例bean。

继续跟进方法调用栈，如下图所示，可以看到现在又定位到了AbstractBeanFactory抽象类的doGetBean()方法中。

![image-20210914201813548](images\image-20210914201813548.png)

可以看到又会调用createBean()方法来进行创建单实例bean

继续跟进方法调用栈，如下图所示，可以看到现在是定位到了AbstractAutowireCapableBeanFactory抽象类的createBean()方法中

![image-20210914202021881](images\image-20210914202021881.png)

往上翻阅createBean()方法，发现可以拿到要创建的bean的定义信息，包括要创建的bean的类型是什么，它是否是单实例等等，如下图所示。

![image-20210914202246392](images\image-20210914202246392.png)

我们还是将关注点放在resolveBeforeInstantiation()方法上，当前程序也是停在了这一行，该方法是来解析BeforeInstantiation的，我们可以看一下该方法上的注释，它是说给后置处理器一个机会，来返回一个代理对象，替代我们创建的目标的bean实例。也就是说，我们希望后置处理器在此能返回一个代理对象，如果能返回代理对象那当然就很好了，直接使用就得了，如果不能那么就得调用doCreateBean()方法来创建一个bean实例了。

![image-20210914203631960](images\image-20210914203631960.png)

为什么要说这个方法呢？进入该方法里面看看自然就懂了，点进去之后会发现该方法真的好长好长，为了能够更加清楚地看到这个方法的全貌，就截了如下一张图。

![在这里插入图片描述](images\sdsddfdsfdsf.jpg)

其实，这个doCreateBean()方法我们之前看过很多遍了，所做的事情无非就是：

1. 首先创建bean的实例
2. 然后给bean的各种属性赋值
3. 接着初始化bean
   1）先执行Aware接口的方法
   2）应用后置处理器的postProcessBeforeInitialization()方法
   3）执行自定义的初始化方法
   4）应用后置处理器的postProcessAfterInitialization()方法

调用doCreateBean()方法才是真正的去创建一个bean实例。

我们还是来到程序停留的地方，即AbstractAutowireCapableBeanFactory抽象类。我们希望后置处理器在此能返回一个代理对象，如果能返回代理对象那当然就很好了，直接使用就得了。接下来，我们就要看看resolveBeforeInstantiation()方法里面具体是怎么做的了。

如下图所示，可以看到现在是定位到了AbstractAutowireCapableBeanFactory抽象类的resolveBeforeInstantiation()方法中，既然程序是停留在了此处，那说明并没有走后面调用doCreateBean()方法创建bean实例的流程，而是先来到这儿，希望后置处理器能返回一个代理对象。

![image-20210914204109111](images\image-20210914204109111.png)

可以看到，在该方法中，首先会拿到要创建的bean的定义信息，包括要创建的bean的类型是什么，它是否是单实例等等，然后看它是不是已经提前被解析过了什么什么，这儿都不算太重要，我们主要关注如下这几行代码：

```java
bean = applyBeanPostProcessorsBeforeInstantiation(targetType, beanName);
if (bean != null) {
   bean = applyBeanPostProcessorsAfterInitialization(bean, beanName);
}
```

这一块会调用两个方法，一个叫方法叫applyBeanPostProcessorsBeforeInstantiation，另一个方法叫applyBeanPostProcessorsAfterInitialization。

可以看到，是调用applyBeanPostProcessorsBeforeInstantiation()方法返回一个对象，我们继续跟进方法调用栈，如下图所示，可以看到现在是定位到了AbstractAutowireCapableBeanFactory抽象类的applyBeanPostProcessorsBeforeInstantiation()方法中。

![image-20210914204520581](images\image-20210914204520581.png)

我们发现，它是拿到所有的后置处理器，如果后置处理器是InstantiationAwareBeanPostProcessor这种类型的，那么就执行该后置处理器的postProcessBeforeInstantiation()方法，现在遍历拿到的后置处理器是AnnotationAwareAspectJAutoProxyCreator这种类型的，如下图所示。

![image-20210914204859895](images\image-20210914204859895.png)

并且前面我也说了，它就是InstantiationAwareBeanPostProcessor这种类型的后置处理器，这种类型的后置处理器中声明的方法就叫postProcessBeforeInstantiation，而不是我们以前学的后置处理器中的叫postProcessbeforeInitialization的方法，也就是说后置处理器跟后置处理器是不一样的。

我们以前就知道，BeanPostProcessor是在bean对象创建完成初始化前后调用的。而在这儿我们也看到了，首先是会有一个判断，即判断后置处理器是不是InstantiationAwareBeanPostProcessor这种类型的，然后再尝试用后置处理器返回对象（当然了，是在创建bean实例之前）。

总之，我们可以得出一个结论：**AnnotationAwareAspectJAutoProxyCreator会在任何bean创建之前，先尝试返回bean的实例。**

最后，我们继续跟进方法调用栈，如下图所示，可以看到终于又定位到了AbstractAutoProxyCreator抽象类的postProcessBeforeInstantiation()方法中。

![image-20210914205133006](images\image-20210914205133006.png)

判断后置处理器是不是InstantiationAwareBeanPostProcessor这种类型时，轮到了AnnotationAwareAspectJAutoProxyCreator这个后置处理器，而它正好是InstantiationAwareBeanPostProcessor这种类型的，所以程序自然就会来到它的postProcessBeforeInstantiation()方法中。

呼应前面，我们现在是终于分析到了AnnotationAwareAspectJAutoProxyCreator这个后置处理器的postProcessBeforeInstantiation()方法中，也就是知道了程序是怎么到这儿来的。

最终，我们得出这样一个结论：AnnotationAwareAspectJAutoProxyCreator在所有bean创建之前，会有一个拦截，因为它是InstantiationAwareBeanPostProcessor这种类型的后置处理器，然后会调用它的postProcessBeforeInstantiation()方法。


### AnnotationAwareAspectJAutoProxyCreator作为后置处理器的功能

我们一步一步分析到了AbstractAutoProxyCreator抽象类的postProcessBeforeInstantiation()方法中，其实，我们也知道现在调用的其实是AnnotationAwareAspectJAutoProxyCreator类的postProcessBeforeInstantiation()方法。


我们就来看看AnnotationAwareAspectJAutoProxyCreator作为后置处理器，它的postProcessBeforeInstantiation()方法都做了些什么。

我们还是以debug模式来运行IOCTest_AOP测试类，这时，应该还是会来到AbstractAdvisorAutoProxyCreator类的setBeanFactory()方法中，如下图所示。

![image-20210916194252430](images\image-20210916194252430.png)

这些我们以前说过的方法就不再赘述一遍了。我们就按下`F9`快捷键运行直到下一个断点，一直运行到AnnotationAwareAspectJAutoProxyCreator类的postProcessBeforeInstantiation()方法中，如下图所示。

![image-20210916203037661](images\image-20210916203037661.png)

### 在每一个bean创建之前，调用postProcessBeforeInstantiation()方法

AnnotationAwareAspectJAutoProxyCreator作为后置处理器，它其中的一个作用就是在每一个bean创建之前，调用其postProcessBeforeInstantiation()方法。

接下来，我们来看看这个方法都做了哪些事情。此刻，是来创建容器中的第一个bean的，即EventListenerMethodProcessor，如下所示。

![image-20210916203204689](images\image-20210916203204689.png)

这块是一个循环创建，会循环创建每一个bean。像EventListenerMethodProcessor这样的bean，跟我们要研究的AOP原理没什么关系，所以我们并不关心这个bean的创建。我们主要关心MathCalculator（业务逻辑类）和LogAspects（切面类）这两个bean的创建。


我们要研究的是这两个bean在创建的时候，AnnotationAwareAspectJAutoProxyCreator这个后置处理器都做了些什么

我们按下`F9`快捷键运行到下一个断点，可以看到这是在创建第一个bean，即EventListenerMethodProcessor。

![image-20210916203345853](images\image-20210916203345853.png)

继续按下`F9`快捷键运行到下一个断点，可以看到这是在创建第二个bean，即DefaultEventListenerFactory。

![image-20210916203438469](images\image-20210916203438469.png)

续按下`F9`快捷键运行到下一个断点，又调用到了postProcessAfterInitialization()方法中。

![image-20210916203524684](images\image-20210916203524684.png)

得到一个结论**在每次创建bean的时候，都会先调用postProcessBeforeInstantiation()方法，然后再调用postProcessAfterInitialization()方法**

继续按下`F9`快捷键运行到下一个断点，可以看到这是在创建第三个bean，即MainConfigOfAOP。

![image-20210916203627520](images\image-20210916203627520.png)

也能看到，在创建这个bean时，先是调用了postProcessBeforeInstantiation()方法，继续按下`F9`快捷键运行到下一个断点，可以看到然后是再调用了postProcessAfterInitialization()方法。

![image-20210916203717555](images\image-20210916203717555.png)

要创建的这个bean是我们的主配置类，即MainConfigOfAOP，我们也不需要理它。继续按下`F9`快捷键运行到下一个断点，可以看到这是在创建第四个bean，即MathCalculator，这是我们需要关心的了。

![image-20210916203809771](images\image-20210916203809771.png)

下F7快捷键让程序一步一步往下运行，可以看到先是拿到MathCalculator这个bean的名称（即calculator），然后再来判断名为targetSourcedBeans的Set集合里面是否包含有这个bean的名称，只不过此时该Set集合是一个空集合，接着再来判断名为advisedBeans的Map集合里面是否包含有这个bean的名称。所以，整个的流程应该是下面这样子的。

#### 先来判断当前bean是否在advisedBeans中

首先我得说明一点，这里，我们只关心MathCalculator（业务逻辑类）和LogAspects（切面类）这两个bean的创建。

advisedBeans是个什么东西呢？它是一个Map集合，里面保存了所有需要增强的bean的名称。那什么又叫需要增强的bean呢？就是那些业务逻辑类，例如MathCalculator，因为它里面的那些方法是需要切面来切的，所以我们要执行它里面的方法，不能再像以前那么简单地执行了，得需要增强，这就是所谓的需要增强的bean。

当程序运行到如下这行代码时，我们来看一下，名为advisedBeans的Map集合里面是不包含MathCalculator这个bean的名称的，因为我们是第一次来处理这个bean。

![image-20210916204150843](images\image-20210916204150843.png)

#### 再来判断当前bean是否是基础类型，或者是否是切面（标注了@Aspect注解的）

继续按下`F6`快捷键让程序往下运行，可以看到又会做一个判断，即判断当前bean是否是基础类型，或者是否是标注了@Aspect注解的切面。

![image-20210917191857586](images\image-20210917191857586.png)

所谓的基础类型就是当前bean是否是实现了Advice、Pointcut、Advisor以及AopInfrastructureBean这些接口。我们可以点进去isInfrastructureClass()方法里面大概看一看，如下图所示

![image-20210917192004452](images\image-20210917192004452.png)

其实，除了判断当前bean是否是基础类型之外，还有一个判断，那怎么看到这个判断呢？选中isInfrastructureClass()方法，按入该方法里面，就能看到这个判断了，即判断当前bean是否是标注了@Aspect注解的切面。

![image-20210917192221768](images\image-20210917192221768.png)

从上图中可以清楚地看到，还有一个叫isAspect的方法，它就是来判断当前bean是否是标注了@Aspect注解的切面的。那么它是怎么来判断的呢？我们可以进入该方法里面去看一看如下图所示，可以看到它是用hasAspectAnnotation()方法来判断当前bean有没有标注@Aspect注解的。

![image-20210917192352223](images\image-20210917192352223.png)

很显然，当前的这个bean（即MathCalculator）既不是基础类型，也不是标注了@Aspect注解的切面。所以，让程序继续往下运行，运行回postProcessBeforeInstantiation()方法中之后，isInfrastructureClass(beanClass)表达式的值就是false了。

#### 最后判断是否需要跳过

所谓的跳过，就是说不要再处理这个bean了。那跳过又是怎么判断的呢？我们可以进入shouldSkip()方法里面去看一看，如下图所示。

![image-20210917192804418](images\image-20210917192804418.png)

可以看到，它会在这儿执行一堆的业务逻辑，首先是调用findCandidateAdvisors()方法找到候选的增强器的集合。

继续让程序往下运行，检查candidateAdvisors变量，可以看到现在有4个增强器，什么叫增强器啊？**增强器就是切面里面的那些通知方法。** logStart、logEnd、logReturn、logExecetion如下图所示。

![image-20210917193920726](images\image-20210917193920726.png)

总结：在shouldSkip()方法里面，首先会获取到以上这5个通知方法。也就是说，先来获取候选的增强器。所谓的增强器其实就是切面里面的那些通知方法，只不过，在这儿是把通知方法的详细信息包装成了一个Advisor，并将其存放在了一个List<Advisor>集合中，即增强器的集合，即是说，每一个通知方法都会被认为是一个增强器。


那么，每一个增强器的类型又是什么呢？检查一下candidateAdvisors变量便知，每一个封装通知方法的增强器都是InstantiationModelAwarePointcutAdvisor这种类型的。

![image-20210917194316910](images\image-20210917194316910.png)

获取到5个增强器之后，然后会来判断每一个增强器是不是AspectJPointcutAdvisor这种类型，如果是，那么返回true。很显然，每一个增强器并不是这种类型的，而是InstantiationModelAwarePointcutAdvisor这种类型的，因此程序并不会进入到那个if判断语句中。

继续让程序往下运行，一直运行到shouldSkip()方法中的最后一行代码处，可以看到，在shouldSkip()方法里面，最终会调用父类的shouldSkip()方法，如下图所示。

![image-20210917200757479](images\image-20210917200757479.png)

一直运行回postProcessBeforeInstantiation()方法中，这时，我们可以知道，if判断语句中的第二个表达式的值就是false。

![image-20210917202324087](images\image-20210917202324087.png)

也就是说，shouldSkip()方法的返回值永远是false，而它就是用来判断是否需要跳过的，所以相当于就是说要跳过了。

我们还是能看到当前这个bean的名字是叫calculator，而且还会拿到什么自定义的TargetSource，但这跟我们目前的研究没有关系，程序往下运行，最后将会直接返回null

![image-20210917202619607](images\image-20210917202619607.png)

然后，运行到下一个断点，发现这时会来到主配置类的calculator()方法中。此刻，是要调用calculator()方法来创建MathCalculator对象了。

![image-20210917202717301](images\image-20210917202717301.png)

继续运行到下一个断点，可以发现当我们把MathCalculator对象创建完了以后，在这儿又会调用postProcessAfterInitialization()方法。

![image-20210917202821896](images\image-20210917202821896.png)

**在每次创建bean的时候，都会先调用postProcessBeforeInstantiation()方法，然后再调用postProcessAfterInitialization()方法。**

#### 创建完对象以后，调用postProcessAfterInitialization()方法

AnnotationAwareAspectJAutoProxyCreator作为后置处理器，它的第一个作用。现在，我就来说说它的第二个作用，即在创建完对象以后，会调用其postProcessAfterInitialization()方法。

我们调用刚才的calculator()方法创建完MathCalculator对象以后，发现又会调用AnnotationAwareAspectJAutoProxyCreator（后置处理器）的postProcessAfterInitialization()方法。

继续让程序往下运行，我们可以看到当前创建好的MathCalculator对象，并且这个bean的名字就叫calculator，也可以看到在这儿还做了一个判断，即判断名为earlyProxyReferences的Set集合里面是否包含当前bean，在该Set集合里面我们可以看到之前已经代理过了什么，目前该Set集合是一个空集合。这都不是我们要关注的内容，我们重点要关注的内容其实是那个叫wrapIfNecessary的方法

![image-20210917203208170](images\image-20210917203208170.png)

什么情况是需要包装的呢？我们可以进入该方法里面去看一看，如下图所示

![image-20210917203303091](images\image-20210917203303091.png)

我们继续按下让程序往下运行，可以看到：

​	首先是拿到MathCalculator这个bean的名称（即calculator），然后再来判断名为targetSourcedBeans的Set集合里面是否包含有这个bean的名称，只不过此时该Set集合是一个空集合。

​	接着再来判断名为advisedBeans的Map集合里面是否包含有当前bean的名称。advisedBeans它就是一个Map集合，里面保存了所有需要增强的bean的名称。

​	由于这儿是第一次来处理当前bean，所以名为advisedBeans的Map集合里面是不包含MathCalculator这个bean的名称的。

​	紧接着再来判断当前bean是否是基础类型，或者是否是切面（即标注了@Aspect注解的）。这儿是怎样来判断的，之前我已经详细地讲过了，故略过。

们重点要关注的内容其实是下面这个叫getAdvicesAndAdvisorsForBean的方法。

![image-20210917203511852](images\image-20210917203511852.png)

从该方法上面的注释中可以得知，它是用于创建代理对象的，从该方法的名称上（见名知义），我们也可以知道它是来获取当前bean的通知方法以及那些增强器的。

#### 获取当前bean的所有增强器

调用getAdvicesAndAdvisorsForBean()方法获取当前bean的所有增强器，也就是那些通知方法，最终封装成这样一个`Object[] specificInterceptors`数组。

到底是怎么来获取当前bean的所有增强器的呢？我们可以按进入getAdvicesAndAdvisorsForBean()方法里面去看一看，如下图所示。

![image-20210917203749034](images\image-20210917203749034.png)

可以看到，又会调用findEligibleAdvisors()方法来获取MathCalculator这个类型的所有增强器，也可以说成是可用的增强器。它又是怎么获取的呢？我们可以进入findEligibleAdvisors()方法里面去看一看，如下图所示，可以看到会先调用一个findCandidateAdvisors()方法来获取候选的所有增强器。
![image-20210917203854614](images\image-20210917203854614.png)

候选的所有增强器，前面我也说过了，有5个，就是切面里面定义的那5个通知方法。

让程序往下运行，可以看到会调用一个findAdvisorsThatCanApply()方法，见名知义，该方法是来找到那些可用的增强器的，以便可以应用到目标对象里面的目标方法中。

![image-20210917204001545](images\image-20210917204001545.png)

现在所要做的事情就是，**找到候选的所有增强器，也就是说是来找哪些通知方法是需要切入到当前bean的目标方法中的。**

我们继续按下进入findAdvisorsThatCanApply()方法里面去看一看，如下图所示，可以看到它是用AopUtils工具类来找到所有能用的增强器（通知方法）的。

![image-20210917204228631](images\image-20210917204228631.png)

我们进入AopUtils工具类的findAdvisorsThatCanApply()方法里面去看一看，如下图所示。

![image-20210917204314567](images\image-20210917204314567.png)

让程序往下运行的过程中，我们可以看到，先是定义了一个保存可用增强器的LinkedList集合，即eligibleAdvisors。然后通过下面的一个for循环来遍历每一个增强器，在遍历的过程中，可以看到有两个&&判断条件，前面的那个是来判断每一个增强器是不是IntroductionAdvisor这种类型的，很明显，每一个增强器并不是这种类型的，它是InstantiationModelAwarePointcutAdvisor这种类型的，前面我也说过了。所以，程序压根就不会进入到这个if判断语句中。

程序继续往下运行，这时我们会看到还有一个for循环，它同样是来遍历每一个增强器的，在遍历的过程中，可以看到先是来判断每一个增强器是不是IntroductionAdvisor这种类型的，但很显然，并不是，然后再来利用canApply()方法判断每一个增强器是不是可用的，那什么是叫可用的呢？

我们可以按下进入canApply()方法里面去看一看，如下图所示。

![image-20210917204649039](images\image-20210917204649039.png)

让程序往下运行的过程中，我们可以看到，这一块的逻辑就是用PointcutAdvisor（切入点表达式）开始来算一下每一个通知方法能不能匹配上现在每一个增强器（通知方法）都是能匹配上。

#### 小结

以上这一小节的流程，我们可以归纳为：

1. 找到候选的所有增强器，也就是说是来找哪些通知方法是需要切入到当前bean的目标方法中的
2. 获取到能在当前bean中使用的增强器
3. 给增强器排序

#### 保存当前bean在advisedBeans中，表示这个当前bean已经被增强处理了

接下来，程序往下运行，当程序运行到下面这一行代码时，就会将当前bean添加到名为advisedBeans的Map集合中，表示这个当前bean已经被增强处理了。

![image-20210917204950167](images\image-20210917204950167.png)


当程序继续往下运行时，会发现有一个createProxy()方法，这个方法非常重要，它是来创建代理对象的。

#### 若当前bean需要增强，则创建当前bean的代理对象

当程序运行到createProxy()方法处时，就会创建当前bean的代理对象，那么这个代理对象怎么创建的呢？

当然是进入到该方法中去看一看了，进入这个方法可不简单，进入当前方法中，从当前方法里面退出来，然后再按进入当前方法中，当前方法里面退出来，最后进入当前方法中，就能真正进入到createProxy()方法里面了，如下图所示。

![image-20210917205243559](images\image-20210917205243559.png)

以看到是先拿到所有增强器，然后再把这些增强器保存到代理工厂（即proxyFactory）中。

运行到createProxy()方法的最后一行，如下图所示。

![image-20210917205846134](images\image-20210917205846134.png)

这行代码的意思是说，利用代理工厂帮我们创建一个代理对象，那它是怎么帮我们创建代理对象的呢？这得进入到代理工厂的getProxy()方法里面去看一看了。

![image-20210917205948480](images\image-20210917205948480.png)

可以看到，会先调用createAopProxy()方法来创建AOP代理。进入该方法中去看一看，如下图所示，可以看到是先得到AOP代理的创建工厂，然后再来创建AOP代理的。

![image-20210917210042627](images\image-20210917210042627.png)

进入createAopProxy()方法中去看一看，如下图所示，这时Spring会自动决定，是为组件创建jdk的动态代理呢，还是为组件创建cglib的动态代理

![image-20210917210220296](images\image-20210917210220296.png)


也就是说，会在这儿为组件创建代理对象，并且有两种形式的代理对象，它们分别是：

- 一种是JdkDynamicAopProxy这种形式的，即jdk的动态代理
- 一种是ObjenesisCglibAopProxy这种形式的，即cglib的动态代理

那么Spring是怎么自动决定是要创建jdk的动态代理，还是要创建cglib的动态代理呢？如果当前类是有实现接口的，那么就使用jdk来创建动态代理，如果当前类没有实现接口，例如MathCalculator类，此时jdk是没法创建动态代理的，那么自然就得使用cglib来创建动态代理了
经过上面的分析，我们知道，**wrapIfNecessary()方法调用完之后，最终会给容器中返回当前组件使用cglib增强了的代理对象。**

### 目标方法的拦截逻辑

打开IOCTest_AOP测试类的代码，并在目标方法运行的地方打上一个断点，如下图所示。

![image-20210922192544773](images\image-20210922192544773.png)

然后以debug模式来运行IOCTest_AOP测试类，这时，应该还是会来到AbstractAdvisorAutoProxyCreator抽象类的setBeanFactory()方法中，如下图所示。

![image-20210922192809505](images\image-20210922192809505.png)我们按下`F9`快捷键让程序运行到下一个断点，一直运行到这个即将要执行的目标方法处，也就是说我们以前看过的方法就直接跳过了。

当程序运行到目标方法处之后，我们就得进入该方法中来看一看其执行流程了。不过在此之前，我们来看一下从容器中得到的MathCalculator对象，可以看到它确实是使用cglib增强了的代理对象，它里面还封装了好多的数据，如下图所示。

![image-20210922193112304](images\image-20210922193112304.png)

![在这里插入图片描述](images\data123123.jpg)

就是说**容器中存放的这个增强后的代理对象里面保存了所有通知方法的详细信息，以及还包括要切入的目标对象。**

接下来，我们入目标方法中去看一看，这时，应该是来到了System类的getSecurityManager()方法中，如下图所示。

![image-20210922194823267](images\image-20210922194823267.png)

那接下来该怎么办呢？先按下step into键进入当前方法中，再按下F8快捷键从当前方法里面退出来，然后再按下step into进入当前方法中，再按下F8快捷键从当前方法里面退出来，最后再按下step into键进入当前方法中，这时你会发现程序进入到了CglibAopProxy类的intercept()方法中，如下图所示。


![image-20210922195156557](images\image-20210922195156557.png)

见名知义，这个方法就是来拦截目标方法的执行的。也就是说，在执行目标方法之前，先让这个AOP代理来拦截一下。接下来，我们就来看看它的拦截逻辑。

#### 根据ProxyFactory对象获取将要执行的目标方法的拦截器链

让程序往下运行的过程中，可以看到前面都是一些变量的声明，直至程序运行到下面这行代码处

![image-20210922195329819](images\image-20210922195329819.png)

这时，就拿到了我们要切的目标对象，即MathCalculator对象。接下来，我们就得仔细研究一下getInterceptorsAndDynamicInterceptionAdvice()方法了。

它的意思是说要根据ProxyFactory对象获取将要执行的目标方法的拦截器链（chain，chain翻译过来就是链的意思），其中，advised变量代表的是ProxyFactory对象，method参数代表的是即将要执行的目标方法（即div()方法）。

那么，目标方法的拦截器链到底是怎么获取的呢？这才是我们关注的核心。听起来，它是来拦截目标方法前后进行执行的，而在目标方法前后要执行的，其实就是切面里面的通知方法。所以，我们可以大胆猜测，这个拦截器链应该是来说先是怎么执行通知方法，然后再来怎么执行目标方法的。

回到主题，如果有拦截器链，那么这个拦截器链是怎么获取的呢？我们可以进入getInterceptorsAndDynamicInterceptionAdvice()方法中去看一看，进来以后可以看到有一些缓存，缓存就是要把这些获取到的东西保存起来，方便下一次直接使用

![image-20210922195451657](images\image-20210922195451657.png)

然后让程序往下运行，直至运行到如下图所示的这行代码处。

![image-20210922195531383](images\image-20210922195531383.png)

可以看到，它是利用advisorChainFactory来获取目标方法的拦截器链, 进入getInterceptorsAndDynamicInterceptionAdvice()方法中看一看便知道了。

![image-20210922195850211](images\image-20210922195850211.png)

可以看到，先是在开头创建一个`List interceptorList`集合，然后在后面遍历所有增强器，并为该集合添加值，最后返回该集合。最终，整个拦截器链就会被封装到List集合中.

接下来，来看看getInterceptorsAndDynamicInterceptionAdvice()方法

#### 先创建一个List集合，来保存所有拦截器

注意，在开头创建List集合时，其实已经为该集合赋好了长度，长度到底是多少呢？inspect一下config.getAdvisors()表达式的值便知道了，如下图所示。

![image-20210922200120564](images\image-20210922200120564.png)

很显然，该集合的长度是6，1个默认的ExposeInvocationInterceptor和5个增强器，这个List集合虽然有长度，但是现在是空的。另外，我们也知道，第一个增强器其实是一个异常通知，即AspectJAfterThrowingAdvice。

![image-20210922200301644](images\image-20210922200301644.png)

让程序往下运行，这时会有一个for循环，它是来遍历所有的Advisor的（一共有6个），每遍历出一个Advisor，便来判断它是不是PointcutAdvisor（和切入点有关的Advisor），若是则把这个Advisor传过来，然后包装成一个MethodInterceptor[]类型的interceptors，接着再把它添加到一开始创建的List集合中。


![image-20210922200440906](images\image-20210922200440906.png)

同样是将这个Advisor传过来，然后包装成一个`Interceptor[]`类型的interceptors，最后再把它添加到一开始创建的List集合中。

或者，直接将遍历出的Advisor传进来，然后包装成一个`Interceptor[]`类型的interceptors，最后再把它添加到一开始创建的List集合中

遍历所有的增强器，将其转为Interceptor

让程序往下运行，即进入for循环中去遍历所有的Advisor。此时，inspect一下advisor变量的值，便能知道第一个增强器是ExposeInvocationIntercepto。

然后来判断这个Advisor是不是PointcutAdvisor，让程序继续往下运行，发现能进入到if判读语句中，说明这个Advisor确实是PointcutAdvisor。继续让程序往下运，即：

```
MethodInterceptor[] interceptors = registry.getInterceptors(advisor);
```

#### 转换第一个增强器

进入getInterceptors()方法里面去一探究竟，如下图所示。

![image-20210922200844475](images\image-20210922200844475.png)

该方法的逻辑其实蛮简单的，就是先拿到增强器，然后判断这个增强器是不是MethodInterceptor这种类型的，若是则直接添加进名为interceptors的List集合里面，若不是则使用AdvisorAdapter（增强器的适配器）将这个增强器转为MethodInterceptor这种类型，然后再添加进List集合里面，反正不管如何，最后都会将该List集合转换成MethodInterceptor数组返回出去。

让程序往下运行，发现程序会进入到第一个if判断语句中，说明拿到的第一个增强器（即ExposeInvocationInterceptor）是MethodInterceptor这种类型的，那么自然就会将其添加进List集合中。

当程序运行到while(var4.hasNext())代码处时，inspect一下adapters变量的值，发现它里面有3个增强器的适配器，它们分别是：

​	MethodBeforeAdviceAdapter：专门来转前置通知的
​	AfterReturningAdviceAdapter：专门来返回置通知的
​	ThrowsAdviceAdapter：专门来异常置通知的

![image-20210922201225319](images\image-20210922201225319.png)

此时，会使用到以上这3个增强器的适配器吗？并不会，因为程序继续往下运行的过程中，并不会进入到for循环里面的if判断语句中

接着，让程序继续往下运行，直至getInterceptors()方法执行完毕，并且该方法运行完会返回一个MethodInterceptor数组，该数组只有一个元素，即拿到的第一个增强器（即ExposeInvocationInterceptor）。

让程序继续往下运行，这时程序就运行回getInterceptorsAndDynamicInterceptionAdvice()方法中了

可以点进getInterceptors()方法里面，然后在该方法处打上一个断点，接着便来看其他的增强器是怎么转成Interceptor的。

![image-20210922201732569](images\image-20210922201732569.png)

#### 转换第二个增强器

此时，按下`F9`快捷键让程序运行到下一个断点，可以看到现在传递过来的是第二个Advisor，该Advisor持有的增强器是AspectJAfterThrowingAdvice，即异常通知。

![image-20210922201839565](images\image-20210922201839565.png)

让程序往下运行的过程中，可以看到，先是判断拿到的第二个增强器是不是MethodInterceptor这种类型的。但很显然，它正好就是这种类型，你只要查看一下AspectJAfterThrowingAdvice类的源码便知道了，如下图所示，该类实现了MethodInterceptor接口。
![image-20210922202012196](images\image-20210922202012196.png)

既然是，那么自然就会将其添加进List集合中，如下图所示。

![image-20210922202052033](images\image-20210922202052033.png)

让程序往下运行，此时，会使用到那3个增强器的适配器吗？并不会，因为程序继续往下运行的过程中，并不会进入到for循环里面的if判断语句中。

当程序运行至getInterceptors()方法的最后一行代码时，该方法会返回一个MethodInterceptor数组，并且该数组只有一个元素，即拿到的第二个增强器（即AspectJAfterThrowingAdvice）。

#### 转换第三个增强器

让程序运行到下一个断点，可以看到现在传递过来的是第三个Advisor，该Advisor持有的增强器是AspectJAfterReturningAdvice，即返回通知。

![image-20210922202603001](\images\image-20210922202603001.png)

让程序往下运行，发现程序并不会进入到第一个if判断语句中，说明拿到的第三个增强器（即AspectJAfterReturningAdvice）并不是MethodInterceptor这种类型。也就是说有些通知方法是实现了MethodInterceptor接口的，也有些不是。 如果不是的话，那么该怎么办呢？这时，就要使用到增强器的适配器了。

让程序继续往下运行，可以看到现在使用的增强器的适配器是MethodBeforeAdviceAdapter，如下图所示。

![image-20210922202735441](images\image-20210922202735441.png)

该适配器是专门来转前置通知的，它能不能支持转换这个AspectJAfterReturningAdvice（返回通知）呢？很显然是肯定不支持的。

接着，让程序继续往下运行，可以看到现在使用的增强器的适配器是AfterReturningAdviceAdapter，如下图所示。

![image-20210922202826472](images\image-20210922202826472.png)

该适配器是专门来转返回通知的，很显然它肯定是支持转换这个AspectJAfterReturningAdvice（返回通知）的。那么，问题来了，该适配器是怎么将AspectJAfterReturningAdvice（返回通知）转换为Interceptor的呢？进入getInterceptor()方法里面一看便知，如下图所示，实际上就是拿到Advice（增强器），并将其包装成一个Interceptor而已。

![image-20210922202912870](images\image-20210922202912870.png)

当程序运行至getInterceptors()方法的最后一行代码时，该方法会返回一个MethodInterceptor数组，并且该数组只有一个元素，即拿到的第三个增强器（即AfterReturningAdviceInterceptor）。

#### 转换第四个增强器

让程序运行到下一个断点，可以看到现在传递过来的是第四个Advisor，该Advisor持有的增强器是AspectJAfterAdvice，即后置通知。

![image-20210922203457392](images\image-20210922203457392.png)

让程序往下运行，发现程序会进入到第一个if判断语句中，说明拿到的第四个增强器（即AspectJAfterAdvice）是MethodInterceptor这种类型的，那么自然就会将其添加进List集合中。

![image-20210922203534302](images\image-20210922203534302.png)

让程序往下运行，此时，会使用到那3个增强器的适配器吗？并不会，因为程序继续往下运行的过程中，并不会进入到for循环里面的if判断语句中。

当程序运行至getInterceptors()方法的最后一行代码时，该方法会返回一个MethodInterceptor数组，并且该数组只有一个元素，即拿到的第四个增强器（即AspectJAfterAdvice）。

#### 转换第五个增强器

让程序运行到下一个断点，可以看到现在传递过来的是第五个Advisor，该Advisor持有的增强器是AspectJMethodBeforeAdvice，即前置通知。

![image-20210922203745296](images\image-20210922203745296.png)

快捷键让程序往下运行，发现程序并不会进入到第一个if判断语句中，说明拿到的第五个增强器（即AspectJMethodBeforeAdvice）并不是MethodInterceptor这种类型。如果不是的话，那么该怎么办呢？这时，就要使用到增强器的适配器了。

让程序继续往下运行，可以看到现在使用的增强器的适配器是MethodBeforeAdviceAdapter，如下图所示。

![image-20210922203902479](images\image-20210922203902479.png)

该适配器是专门来转前置通知的，很显然它肯定是支持转换这个AspectJMethodBeforeAdvice（前置通知）的。

当程序运行至getInterceptors()方法的最后一行代码时，该方法会返回一个MethodInterceptor数组，并且该数组只有一个元素，即拿到的第五个增强器（即MethodBeforeAdviceInterceptor）。

接着，让程序继续往下运行，将整个转换流程走完，直至程序运行回getInterceptorsAndDynamicInterceptionAdvice()方法中，如下图所示。

![image-20210922204017226](images\image-20210922204017226.png)

紧接着，继续让程序往下运行，直至走完整个for循环，如下图所示，此时会返回一开始就创建的List集合。

![image-20210922204146452](images\image-20210922204146452.png)

可以看到，该List集合里面有6个拦截器，其中AspectJAfterThrowingAdvice和AspectJAfterAdvice这俩人家本来就是拦截器，而AfterReturningAdviceInterceptor和MethodBeforeAdviceInterceptor这俩是使用适配器重新转换之后的拦截器。

最后，继续让程序往下运行，直至运行回CglibAopProxy类的intercept()方法中，如下图所示。

### ![image-20210922204344350](images\image-20210922204344350.png)

此时，将要执行的目标方法的拦截器链就获取到了，**拦截器链里面保存的其实就是每一个通知方法**。

**什么叫拦截器链呢？所谓的拦截器链其实就是每一个通知方法又被包装为了方法拦截器。** 之后，目标方法的执行，就要使用到这个拦截器链机制。

### 拦截器链的执行过程

我们还是以debug模式来运行IOCTest_AOP测试类，这时，应该还是会来到AbstractAdvisorAutoProxyCreator抽象类的setBeanFactory()方法中，如下图所示。

![image-20210926190220706](images\image-20210926190220706.png)

让程序运行到下一个断点，一直运行到这个即将要执行的目标方法处，也就是说我们以前看过的方法就直接跳过了。

![image-20210926190432901](images\image-20210926190432901.png)

让程序运行到下一个断点，这时程序会运行到DefaultAdvisorAdapterRegistry类的getInterceptors()方法中，如下图所示。

![image-20210926190507125](images\image-20210926190507125.png)

如下图所示，inspect一下config.getAdvisors()表达式的值，便能看到增强器了。

![image-20210926193856254](images\image-20210926193856254.png)

还是回到DefaultAdvisorAdapterRegistry类的getInterceptors()方法中

可以看到现在传递过来的是第五个Advisor，该Advisor持有的增强器是AspectJMethodBeforeAdvice，即前置通知。

让程序往下运行，一直运行到CglibAopProxy类的intercept()方法中



Spring4和Spring5代码后续不太一样

### **AOP原理总结**

最后，我们还需要对AOP原理做一个简单的总结，完美结束对其研究的旅程。

#### 	1.利用@EnableAspectJAutoProxy注解来开启AOP功能

#### 	2.这个AOP功能是怎么开启的呢？主要是通过@EnableAspectJAutoProxy注解向IOC容器中注册一个AnnotationAwareAspectJAutoProxyCreator组件来做到这点的

#### 	3.AnnotationAwareAspectJAutoProxyCreator组件是一个后置处理器

#### 	4.该后置处理器是怎么工作的呢？在IOC容器创建的过程中，我们就能清楚地看到这个后置处理器是如何创建以及注册的，以及它的工作流程。

​		首先，在创建IOC容器的过程中，会调用refresh()方法来刷新容器，而在刷新容器的过程中有一步是来注册后置处理器的，如下所示：

```java
 // 注册后置处理器，在这一步会创建AnnotationAwareAspectJAutoProxyCreator对象
registerBeanPostProcessors(beanFactory);
```

​	在刷新容器的过程中还有一步是来完成BeanFactory的初始化工作的，如下所示：

```java
// 完成BeanFactory的初始化工作。所谓的完成BeanFactory的初始化工作，其实就是来创建剩下的单实例bean的。
finishBeanFactoryInitialization(beanFactory); 
```

很显然，剩下的单实例bean自然就包括MathCalculator（业务逻辑类）和LogAspects（切面类）这两个bean，因此这两个bean就是在这儿被创建的。

​		1.创建业务逻辑组件和切面组件

​		2.在这两个组件创建的过程中，最核心的一点就是AnnotationAwareAspectJAutoProxyCreator（后置处理器）会来拦截这俩组件的创建过程

​		3.怎么拦截呢？主要就是在组件创建完成之后，判断组件是否需要增强。如需要，则会把切面里面的通知方法包装成增强器，然后再为业务逻辑组件创建一个代理对象。我们也认真仔细探究过了，在为业务逻辑组件创建代理对象的时候，使用的是cglib来创建动态代理的。当然了，如果业务逻辑类有实现接口，那么就使用jdk来创建动态代理。一旦这个代理对象创建出来了，那么它里面就会有所有的增强器。

​		这个代理对象创建完以后，IOC容器也就创建完了。接下来，便要来执行目标方法了。

#### 5.执行目标方法

此时，其实是代理对象来执行目标方法

使用CglibAopProxy类的intercept()方法来拦截目标方法的执行，拦截的过程如下：

​	得到目标方法的拦截器链，所谓的拦截器链其实就是每一个通知方法又被包装为了方法拦截器，即MethodInterceptor

​	利用拦截器的链式机制，依次进入每一个拦截器中进行执行

​	最终，整个的执行效果就会有两套：

​		目标方法正常执行：前置通知→目标方法→后置通知→返回通知
​		目标方法出现异常：前置通知→目标方法→后置通知→异常通知

