# 一、基于注解版的声明式事务

## 导入相关依赖

首先，在项目的pom.xml文件中添加c3p0数据源的依赖，如下所示

```xml
<dependency>
    <groupId>c3p0</groupId>
    <artifactId>c3p0</artifactId>
    <version>0.9.1.2</version>
</dependency>
```

然后，在项目的pom.xml文件中添加MySQL数据库驱动的依赖，如下所示。

```xml
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>5.1.46</version>
</dependency>
```

最后，在项目的pom.xml文件中添加spring-jdbc模块的依赖，如下所示。

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-jdbc</artifactId>
    <version>5.0.4.RELEASE</version>
</dependency>
```

Spring简化了对数据库的操作，只要我们在项目中导入了以上spring-jdbc模块的依赖，那么它就可以简化对数据库的操作以及事务控制。我们在后面就可以用Spring提供的JDBC模板（即JdbcTemplate）来操作数据库。

## 配置数据源以及JdbcTemplate

首先，我们得向IOC容器中注册一个c3p0数据源，先新建一个配置类，例如TxConfig，再使用@Bean注解向IOC容器中注册一个c3p0数据源，如下所示。

```java
@Configuration
public class TxConfig {
    // 注册c3p0数据源
    @Bean
    public DataSource dataSource() throws Exception {
        ComboPooledDataSource dataSource = new ComboPooledDataSource();
        dataSource.setUser("root");
        dataSource.setPassword("123456");
        dataSource.setDriverClass("com.mysql.jdbc.Driver");
        dataSource.setJdbcUrl("jdbc:mysql://192.168.31.70:3306/test");
        return dataSource;
    }

}
```

然后，再向IOC容器中注册一个JdbcTemplate组件，它是Spring提供的一个简化数据库操作的工具，它能简化对数据库的增删改查操作。

```java
@Bean
public JdbcTemplate jdbcTemplate() throws Exception {
    JdbcTemplate jdbcTemplate = new JdbcTemplate(dataSource());
    return jdbcTemplate;
}
```

注意，在创建JdbcTemplate对象的时候，得把数据源传入JdbcTemplate类的有参构造器中，因为需要从数据源里面获取数据库连接。

其实，将数据源传入JdbcTemplate类的有参构造器中，一共有两种方式。第一种方式是将数据源作为一个参数传递到TxConfig配置类的jdbcTemplate()方法中。这样，JdbcTemplate类的有参构造器就可以使用到这个数据源了。

```java
@Bean
public JdbcTemplate jdbcTemplate(DataSource dataSource) throws Exception {
    JdbcTemplate jdbcTemplate = new JdbcTemplate(dataSource);
    return jdbcTemplate;
}
```

因为@Bean注解标注的方法在创建对象的时候，方法参数的值是从IOC容器中获取的，并且标注在这个方法的参数上的@Autowired注解可以省略。

第二种方式就不用那么麻烦了，在JdbcTemplate类的有参构造器中调用一次dataSource()方法即可。可以看到，向IOC容器中注册一个JdbcTemplate组件时，使用的就是这种方式。

**Spring对@Configuration注解标注的类会做特殊处理，多次调用给IOC容器中添加组件的方法，都只是从IOC容器中找组件而已。**

首先在test数据库中临时创建一张表，例如tbl_user，建表语句如下

```sql
CREATE TABLE `tbl_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `age` int(2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```



### 开发dao层

新建一个UserDao类，代码如下所示：

```java
@Repository
public class UserDao {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    public void insert() {
        String sql = "insert into `tbl_user`(username, age) values(?, ?)";
        String username = UUID.randomUUID().toString().substring(0, 5);
        jdbcTemplate.update(sql, username, 19); // 增删改都来调用这个方法
    }

}
```

注意，该类上标注了一个@Repository注解，因为待会我们要用到@ComponentScan注解来配置包扫描。

### 开发service层

```java
@Service
public class UserService {

    @Autowired
    private UserDao userDao;

    public void insertUser() {
        userDao.insert();
        System.out.println("插入完成...");
    }

}
```

可以看到，现在默认insertUser()方法是没有任何事务特性的。如果这个方法上有事务，那么只要这个方法里面有任何一句代码出现了问题，该行代码之前执行的所有操作就都应该回滚。

接下来，我们就要在TxConfig配置类上添加@ComponentScan注解来配置包扫描了，如下所示。

```java
@ComponentScan("com.harry.spring")
@Configuration
public class TxConfig {
    // 注册c3p0数据源
    @Bean
    public DataSource dataSource() throws Exception {
        ComboPooledDataSource dataSource = new ComboPooledDataSource();
        dataSource.setUser("root");
        dataSource.setPassword("123456");
        dataSource.setDriverClass("com.mysql.jdbc.Driver");
        dataSource.setJdbcUrl("jdbc:mysql://192.168.31.70:3306/test");
        return dataSource;
    }

    @Bean
    public JdbcTemplate jdbcTemplate(DataSource dataSource) throws Exception {
        JdbcTemplate jdbcTemplate = new JdbcTemplate(dataSource);
        return jdbcTemplate;
    }

}
```

新建一个单元测试类，例如IOCTest_tx，代码如下所示：

```java
public class IOCTest_tx {

    @Test
    public void test01() {
        AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext(TxConfig.class);

        UserService userService = applicationContext.getBean(UserService.class);

        userService.insertUser();

        applicationContext.close();
    }

}
```

运行以上test01()方法，发现控制台打印出了如下一条信息。

并且，刷新一下tbl_user表，可以看到确实是向该表中插入了一条记录，如下图所示

![image-20210926201754479](images\image-20210926201754479.png)

接下来，我们就为UserService类中的insertUser()方法添加上事务，添加上事务以后，只要这个方法里面有任何一句代码出现了问题，那么该行代码之前执行的所有操作就都应该回滚。

如果要想为该方法添加上事务，那么就得使用@Transactional注解了。我们在该方法上标注这么一个注解，就是为了告诉Spring这个方法它是一个事务方法，这样，Spring在执行这个方法的时候，就会自动地进行事务控制。如果该方法正常执行，没出现任何问题，那么该方法中的所有操作都会生效，最终就会提交；如果该方法运行期间出现异常，那么该方法中的所有操作都会回滚。

```java
@Transactional
public void insertUser() {
    userDao.insert();
    System.out.println("插入完成...");
}
```

为了验证这一点，我们特地在该方法中故意抛出了一个算术异常。

目前tbl_user表中是只有一条记录的，如果insertUser()方法真的变成了一个事务方法，那么执行该方法再向tbl_user表中插入一条记录时，肯定是会出现问题的，既然出现了问题，插入操作势必就会回滚，最终tbl_user表中是不会再插入一条新记录的。

运行完IOCTest_tx类中的test01()方法之后，虽说Eclipse控制台是打印出了`插入完成...`这样的消息，而且也给我们看到了除零的算术异常，但是刷新tbl_user表之后，你会发现仍然会向tbl_user表中插入一条新的记录，如下图所示。

![image-20210926202153095](images\image-20210926202153095.png)

这说明，虽然insertUser()方法是标注了@Transactional注解，但是它并不是一个真正的事务方法。

也就是说，光为insertUser()方法加一个@Transactional注解是不行的，那我们还得做什么呢？还得在TxConfig配置类上标注一个@EnableTransactionManagement注解，来开启基于注解的事务管理功能。

```java
@EnableTransactionManagement
@ComponentScan("com.harry.spring")
@Configuration
public class TxConfig {
    // 注册c3p0数据源
    @Bean
    public DataSource dataSource() throws Exception {
        ComboPooledDataSource dataSource = new ComboPooledDataSource();
        dataSource.setUser("root");
        dataSource.setPassword("123123");
        dataSource.setDriverClass("com.mysql.jdbc.Driver");
        dataSource.setJdbcUrl("jdbc:mysql://192.168.31.70:3306/test");
        return dataSource;
    }

    @Bean
    public JdbcTemplate jdbcTemplate(DataSource dataSource) throws Exception {
        JdbcTemplate jdbcTemplate = new JdbcTemplate(dataSource);
        return jdbcTemplate;
    }

}
```

如果是像以前一样基于配置文件来开发，那么就得在配置文件中添加如下这样一行配置，来开启基于注解的事务管理功能。

```xml
<tx:annotation-driven/>
```

现在我们再来运行一下IOCTest_tx类中的test01()方法，发现控制台并没有打印出`插入完成...`这样的消息，而是抛了一个如下所示的异常，即没有这样一个bean定义的异常。

![image-20210926202533520](images\image-20210926202533520.png)

抛了这样一个异常，自然是不会向tbl_user表中插入一条新的记录的。而且从NoSuchBeanDefinitionException异常的描述信息中我们可以知道，现在是没有org.springframework.transaction.PlatformTransactionManager这种类型的bean的定义的，也就是说我们还没有配置基于平台的事务管理器。


因此，最关键的一步就是配置事务管理器来控制事务。在这之前，我们可以查阅一下源码

![image-20210926202626741](images\image-20210926202626741.png)

发现它是一个接口，然后我们再来看看该接口有些什么实现类，如下图所示，发现该接口有很多实现类，其中有一个实现类是DataSourceTransactionManager，它使用频率很高，在这儿我们也是用它。

像Spring的spring-jdbc模块，以及MyBatis框架等等这些想要进行事务控制，都需要用到这个DataSourceTransactionManager实现类。

接下来，我们就向IOC容器中注册事务管理器，即需要向TxConfig配置类中添加一个如下方法。

```java
// 注册事务管理器在容器中
@Bean
public PlatformTransactionManager platformTransactionManager() throws Exception {
    return new DataSourceTransactionManager(dataSource());
}
```

注意，这个事务管理器有一个特别重要的地方，就是它要管理数据源，也就是说事务管理器一定要把数据源控制住。这样的话，它才会控制住数据源里面的每一个连接，这时该连接上的回滚以及事务的开启等操作，都将会由这个事务管理器来做。

运行IOCTest_tx类中的test01()方法，发现控制台不仅打印出了`插入完成...`这样的消息，而且还抛出了一个除零的算术异常，最重要的是没有向tbl_user表中插入一条新的记录，这说明insertUser()方法现在可真的成了一个事务方法。

## 声明式事务原理的源码分析

### 声明式事务的原理

其实，**要想知道声明式事务的原理，只需要搞清楚@EnableTransactionManagement注解给容器中注册了什么组件，以及这些组件工作时候的功能是什么就行了，一旦把这个研究透了，那么声明式事务的原理我们就清楚了。**

之前研究AOP的原理时，是从@EnableAspectJAutoProxy注解开始入手研究的，研究声明式事务的原理，也是应该从@EnableTransactionManagement注解开始入手研究。

### @EnableTransactionManagement注解利用TransactionManagementConfigurationSelector给容器中导入组件

在配置类上添加@EnableTransactionManagement注解，便能够开启基于注解的事务管理功能。那下面我们就来看一看它的源码，如下图所示。

![image-20210926203004417](images\image-20210926203004417.png)

从源码中可以看出，@EnableTransactionManagement注解使用@Import注解给容器中引入了

TransactionManagementConfigurationSelector组件它其实是一个ImportSelector。

我们可以点到TransactionManagementConfigurationSelector类中一看究竟，如下图所示，发现它继承了一个类，叫AdviceModeImportSelector。

![image-20210926203112065](images\image-20210926203112065.png)

然后再次点到AdviceModeImportSelector类中，如下图所示，发现它实现了一个接口，叫ImportSelector。

![image-20210926203152769](images\image-20210926203152769.png)

其实它是用于给容器中快速导入一些组件的，到底要导入哪些组件，就看它会返回哪些要导入到容器中的组件的全类名。

看一下TransactionManagementConfigurationSelector类的源码，其实在上面我们就看清楚该类的源码了，在它里面会做一个switch判断，如果adviceMode是PROXY，那么就会返回一个String[]，该String数组如下所示：

```java
return new String[]{AutoProxyRegistrar.class.getName(), ProxyTransactionManagementConfiguration.class.getName()};
```

这说明会向容器中导入AutoProxyRegistrar和ProxyTransactionManagementConfiguration这两个组件。

如果adviceMode是ASPECTJ，那么便会返回如下这样一个`String[]`。

```java
return new String[]{"org.springframework.transaction.aspectj.AspectJTransactionManagementConfiguration"}
```

点`TRANSACTION_ASPECT_CONFIGURATION_CLASS_NAME`一下，可以看到，它其实就是AspectJTransactionManagementConfiguration类的全类名，如下图所示。

![image-20210926203508184](images\image-20210926203508184.png)

也就是说，如果adviceMode是ASPECTJ，那么就会向容器中导入一个AspectJTransactionManagementConfiguration组件。只可惜，它和我们研究声明式事务的原理没有半毛钱的关系。

AdviceMode又是个啥呢？点它，发现它是一个枚举，如下图所示

![image-20210926203555826](images\image-20210926203555826.png)

我们可以再来看一下@EnableTransactionManagement注解的源码，发现它里面会定义一个mode属性，且其默认值就是AdviceMode.PROXY。既然如此，那么便会进入到TransactionManagementConfigurationSelector类的switch语句的case PROXY选项中，这时，就会向容器中快速导入两个组件，一个叫AutoProxyRegistrar，一个叫ProxyTransactionManagementConfiguration。

### 导入的第一个组件（即AutoProxyRegistrar）

我们来看导入的第一个组件，即AutoProxyRegistrar，点进去该类里面看一看，发现它实现了一个接口，叫ImportBeanDefinitionRegistrar。

![image-20210926203718557](images\image-20210926203718557.png)

这个AutoProxyRegistrar组件其实就是用来向容器中注册bean的，最终会调用该组件的registerBeanDefinitions()方法来向容器中注册bean。

在该方法中先是通过如下一行代码来获取各种注解类型，这儿需要特别注意的是，这里是拿到所有的注解类型，而不是只拿@EnableAspectJAutoProxy这个类型的。因为mode、proxyTargetClass等属性会直接影响到代理的方式，而拥有这些属性的注解至少有@EnableTransactionManagement、@EnableAsync以及@EnableCaching等等，甚至还有启用AOP的注解，即@EnableAspectJAutoProxy，它也能设置proxyTargetClass这个属性的值，因此也会产生关联影响。

```java
Set<String> annoTypes = importingClassMetadata.getAnnotationTypes();
```

然后是拿到注解里的mode、proxyTargetClass这两个属性的值，如下图所示。

![image-20210927191324948](images\image-20210927191324948.png)

注意，如果这儿的注解是@Configuration或者别的其他注解的话，那么获取到的这俩属性的值就是null了。

接着做一个判断，如果存在mode、proxyTargetClass这两个属性，并且这两个属性的class类型也都是对的，那么便会进入到if判断语句中，这样，其余注解就相当于都被挡在外面了。


要是真进入到了if判断语句中，意味着找到了候选的注解（例如@EnableTransactionManagement）

紧接着会再做一个判断，即判断找到的候选注解中的mode属性的值是否为AdviceMode.PROXY，若是则会调用我们熟悉的AopConfigUtils工具类的registerAutoProxyCreatorIfNecessary方法。它主要是来向容器中注册一个InfrastructureAdvisorAutoProxyCreator组件的。
![image-20210927191521677](images\image-20210927191521677.png)

继续往下看AutoProxyRegistrar类的registerBeanDefinitions()方法。这时，又会做一个判断，要是找到的候选注解设置了proxyTargetClass这个属性的值，并且值为true，那么便会进入到下面的if判断语句中，看要不要强制使用CGLIB的方式。

如果此时找到的候选注解是@EnableTransactionManagement，查看该注解的源码，会发现它里面就拥有一个proxyTargetClass属性，并且其默认值是false。所以此时压根就不会进入到if判断语句中，而只会调用我们熟悉的AopConfigUtils工具类的registerAutoProxyCreatorIfNecessary方法。

点进去registerAutoProxyCreatorIfNecessary方法中，如下图所示，可以看到这个方法又调用了一个同名的重载方法。

![image-20210927191658554](images\image-20210927191658554.png)

然后点进去同名的重载方法中，如下图所示，可以看到这个方法又调用了一个registerOrEscalateApcAsRequired方法，而且还传入了一个参数，即`InfrastructureAdvisorAutoProxyCreator.class`。

现在我们可以得出这样一个结论：**导入的第一个组件（即AutoProxyRegistrar）向容器中注入了一个自动代理创建器，即InfrastructureAdvisorAutoProxyCreator。**

声明式事务的原理跟AOP的原理很相似，只不过对于声明式事务原理而言，它注入的是InfrastructureAdvisorAutoProxyCreator组件而已。，在研究AOP原理时，AnnotationAwareAspectJAutoProxyCreator实质上是一个后置处理器，那么

InfrastructureAdvisorAutoProxyCreator也就是是一个后置处理器，，发现它继承了一个AbstractAdvisorAutoProxyCreator类

![image-20210927192149447](images\image-20210927192149447.png)

然后再点进去AbstractAdvisorAutoProxyCreator类里面去看一看，如下图所示，发现它继承了一个AbstractAutoProxyCreator类。

![image-20210927192219929](images\image-20210927192219929.png)

接着再点进去AbstractAutoProxyCreator类里面去看一看，如下图所示，发现它实现了一个SmartInstantiationAwareBeanPostProcessor接口。

![image-20210927192252215](images\image-20210927192252215.png)

这说明注入的InfrastructureAdvisorAutoProxyCreator组件同样也是一个后置处理器。接下来就来分析一下该组件的功能。

### InfrastructureAdvisorAutoProxyCreator组件的功能

其实，它做的事情也很简单，和之前研究AOP原理时向容器中注入的AnnotationAwareAspectJAutoProxyCreator组件所做的事情基本上没差别，只是利用后置处理器机制在对象创建以后进行包装，然后返回一个代理对象，并且该代理对象里面会存有所有的增强器。最后，代理对象执行目标方法，在此过程中会利用拦截器的链式机制，依次进入每一个拦截器中进行执行。

### 导入的第二个组件（即ProxyTransactionManagementConfiguration）

#### 向容器中注册事务增强器

点进去ProxyTransactionManagementConfiguration类里面去看一看，很快你就会发现它是一个配置类，它会利用@Bean注解向容器中注册各种组件，而且注册的第一个组件就是BeanFactoryTransactionAttributeSourceAdvisor，这个Advisor可是事务的核心内容，可以暂时称之为事务增强器。

![image-20210927192511876](images\image-20210927192511876.png)

#### 在向容器中注册事务增强器时，需要用到事务属性源

从上面的配置类中可以看出，在向容器中注册事务增强器时，它会需要一个TransactionAttributeSource

所需的TransactionAttributeSource又是容器中的一个bean，而且从transactionAttributeSource方法中可以看出，它是new出来了一个AnnotationTransactionAttributeSource对象。这个是重点，它是基于注解驱动的事务管理的事务属性源，和@Transactional注解相关，也是现在使用得最多的方式，其基本作用是遇上比如@Transactional注解标注的方法时，此类会分析此事务注解。

然后，点进AnnotationTransactionAttributeSource类的无参构造方法中去看一看，发现该方法又调用了如下一个this(true)方法，即本类的另一个重载的有参构造方法。

![image-20210927193127787](images\image-20210927193127787.png)

点击一下this(true)方法，这时会跳到如下的一个有参构造方法处。

![image-20210927193555731](images\image-20210927193555731.png)

在该方法中，你会看到一个TransactionAnnotationParser接口，源码如下图所示。

![image-20210927193720427](images\image-20210927193720427.png)

顾名思义，它是解析方法/类上事务注解的，当然了，你也可以称它为事务注解的解析器。

这里我要说明的一点是，Spring支持三个不同的事务注解，它们分别是：

​	Spring事务注解，即org.springframework.transaction.annotation.Transactional（纯正血统，官方推荐）
​	JTA事务注解，即javax.transaction.Transactional
​	EJB 3事务注解，即javax.ejb.TransactionAttribute

因为现在基本上都是Spring的天下了，所以我们一般都会使用Spring事务注解。另外，上面三个注解虽然语义上一样，但是使用方式上不完全一样，若真要使用其它的则请注意各自的使用方式。

上面说到了Spring支持三个不同的事务注解，这里很显然，它们都对应了三个不同的注解解析器，即SpringTransactionAnnotationParser、JtaTransactionAnnotationParser以及Ejb3TransactionAnnotationParser。

也是因为现在基本上都是Spring的天下了，所以只关注SpringTransactionAnnotationParser，其它的雷同。我们可以点进去该类里面看一看，尤其要注意翻阅parseTransactionAnnotation方法，你会发现它就是来解析@Transactional注解里面的每一个信息的，包括它里面的每一个属性，例如rollbackFor、noRollbackFor、···


![image-20210927194003312](images\image-20210927194003312.png)

rollbackFor、noRollbackFor等等这些属性就是我们可以在@Transactional注解里面能写的。

![在这里插入图片描述](images\trancation.jpg)

#### 在向容器中注册事务增强器时，还需要用到事务的拦截器

来看看向容器中注册事务增强器时，还得做些什么。回到ProxyTransactionManagementConfiguration类中，发现在向容器中注册事务增强器时，除了需要事务注解信息，还需要一个事务的拦截器，看到那个transactionInterceptor方法没，它就是表示事务增强器还要用到一个事务的拦截器。
![image-20210927194313514](images\image-20210927194313514.png)

仔细查看上面的transactionInterceptor方法，你会看到在里面创建了一个TransactionInterceptor对象，创建完毕之后，不但会将事务属性源设置进去，而且还会将事务管理器（txManager）设置进去。也就是说，事务拦截器里面不仅保存了事务属性信息，还保存了事务管理器。

我们点进去TransactionInterceptor类里面去看一下，发现该类实现了一个MethodInterceptor接口，如下图所示。

![image-20210927194529368](images\image-20210927194529368.png)

在研究AOP的原理时，就已经认识它了。**切面类里面的通知方法最终都会被整成增强器，而增强器又会被转换成MethodInterceptor**。所以，这样看来，这个事务拦截器实质上还是一个MethodInterceptor（方法拦截器）。

方法拦截器简单来说就是，现在会向容器中放一个代理对象，代理对象要执行目标方法，那么方法拦截器就会进行工作。

跟AOP的原理一模一样，在代理对象执行目标方法的时候，它便会来执行拦截器链，而现在这个拦截器链，只有一个TransactionInterceptor，它正是这个事务拦截器。接下来，我们就来看看这个事务拦截器是怎样工作的，即它的作用是什么。

仔细翻阅TransactionInterceptor类的源码，你会发现它里面有一个invoke方法，而且还会看到在该方法里面又调用了一个invokeWithinTransaction方法，如下图所示。

![image-20210927194749294](images\image-20210927194749294.png)

点进去invokeWithinTransaction方法里面看一下，就能知道这个事务拦截器是怎样工作的了。

##### 先来获取事务相关的一些属性信息

从invokeWithinTransaction方法的第一行代码，即：

```java
TransactionAttributeSource tas = getTransactionAttributeSource();
final TransactionAttribute txAttr = (tas != null ? tas.getTransactionAttribute(method, targetClass) : null);
```

这儿是来获取事务相关的一些属性信息的。

##### 再来获取PlatformTransactionManager

接着往下看invokeWithinTransaction方法，可以看到它的第二行代码是这样写的：

```java
final PlatformTransactionManager tm = determineTransactionManager(txAttr);
```

这就是来获取PlatformTransactionManager的，还记得之前就已经向容器中注册了一个吗，现在就是来获取它的。点进去determineTransactionManager方法里面去看一下。

![image-20210927195038495](images\image-20210927195038495.png)

先来看看下面这几行代码，即：

```java
String qualifier = txAttr.getQualifier();
if (StringUtils.hasText(qualifier)) {
   return determineQualifiedTransactionManager(this.beanFactory, qualifier);
}
```

它是说，如果事务属性里面有Qualifier这个注解，并且这个注解还有值，那么就会直接从容器中按照这个指定的值来获取PlatformTransactionManager。

其实我们在为某个业务方法标注@Transactional注解的时候，是可以明确地指定事务管理器的名字的。

![image-20210927195156438](images\image-20210927195156438.png)

从上图中可以看到，指定事务管理器的名字，其实就等同于Qualifier这个注解。虽说是可以明确指定事务管理器的名字，但我们一般都不这么做，即不指定。

如果真要是指定了的话，那么就应该是到这儿来判断了。

```java
else if (StringUtils.hasText(this.transactionManagerBeanName)) {
    return determineQualifiedTransactionManager(this.transactionManagerBeanName);
}
```

上面这几行代码应该是来判断PlatformTransactionManager是否有名，若有则就应该像上面这么来获取

如果没指定的话，那么就是来获取默认的了，这时很显然会进入到最下面的else判断中。

```java
else {
   PlatformTransactionManager defaultTransactionManager = getTransactionManager();
   if (defaultTransactionManager == null) {
      defaultTransactionManager = this.transactionManagerCache.get(DEFAULT_TRANSACTION_MANAGER_KEY);
      if (defaultTransactionManager == null) {
         defaultTransactionManager = this.beanFactory.getBean(PlatformTransactionManager.class);
         this.transactionManagerCache.putIfAbsent(
               DEFAULT_TRANSACTION_MANAGER_KEY, defaultTransactionManager);
      }
   }
   return defaultTransactionManager;
```

可以看到，会先调用getTransactionManager方法，获取的是默认向容器中自动装配进去的PlatformTransactionManager。

首次获取肯定就为null，但没关系，因为最终会从容器中按照类型来获取，这可以从下面这行代码中看出来。

```java
defaultTransactionManager = this.beanFactory.getBean(PlatformTransactionManager.class);
```

所以，我们只需要给容器中注入一个PlatformTransactionManager，正如我们前面写的这样：

// 注册事务管理器在容器中

```java
@Bean
public PlatformTransactionManager platformTransactionManager() throws Exception {
    return new DataSourceTransactionManager(dataSource());
}
```

然后就能获取到PlatformTransactionManager了。获取到了之后，当然就可以使用它了。

**总结：如果事先没有添加指定任何TransactionManager，那么最终会从容器中按照类型来获取一个PlatformTransactionManager。**

##### 执行目标方法

接下来，继续往下看invokeWithinTransaction方法，来看它接下去又做了些什么。其实，很容易就能看出来，获取到事务管理器之后，然后便要来执行目标方法了，而且如果目标方法执行时一切正常，那么还能拿到一个返回值，如下图所示。

![image-20210927195512948](images\image-20210927195512948.png)

在执行上面这句代码之前，还有这样一句代码：

```java
TransactionInfo txInfo = createTransactionIfNecessary(tm, txAttr, joinpointIdentification);
```

上面这个方法翻译成中文，就是如果是必须的话，那么得先创建一个Transaction。就是如果目标方法是一个事务，那么便开启事务。

如果目标方法执行时一切正常，那么接下来该怎么办呢？这时，会调用一个叫commitTransactionAfterReturning的方法，如下图所示

![image-20210927195615972](images\image-20210927195615972.png)

我们可以点进去commitTransactionAfterReturning方法里面去看一看，发现它是先获取到事务管理器，然后再利用事务管理器提交事务，如下图所示。

![image-20210927195653455](images\image-20210927195653455.png)

如果执行目标方法时出现异常，那么又该怎么办呢？这时，会调用一个叫completeTransactionAfterThrowing的方法，如下图所示。

![image-20210927195810064](images\image-20210927195810064.png)

我们可以点进去completeTransactionAfterThrowing方法里面去看一看，发现它是先获取到事务管理器，然后再利用事务管理器回滚这次操作，如下图所示。

![image-20210927195845554](images\image-20210927195845554.png)

也就是说，真正的回滚与提交事务的操作都是由事务管理器来做的，而TransactionInterceptor只是用来拦截目标方法的。

### 总结

首先，使用AutoProxyRegistrar向Spring容器里面注册一个后置处理器，这个后置处理器会负责给我们包装代理对象。然后，使用ProxyTransactionManagementConfiguration（配置类）再向Spring容器里面注册一个事务增强器，此时，需要用到事务拦截器。最后，代理对象执行目标方法，在这一过程中，便会执行到当前Spring容器里面的拦截器链，而且每次在执行目标方法时，如果出现了异常，那么便会利用事务管理器进行回滚事务，如果执行过程中一切正常，那么则会利用事务管理器提交事务。


# 二、BeanFactoryPostProcessor的原理

## 从源码角度理解BeanFactoryPostProcessor的原理

根据我们在第一讲中的安排，我们接下来要说的Spring里面的一些扩展原理有：

- BeanFactoryPostProcessor
- BeanDefinitionRegistryPostProcessor
- ApplicationListener
- Spring容器创建过程

## BeanFactoryPostProcessor的调用时机

BeanFactoryPostProcessor其实就是BeanFactory（创建bean的工厂）的后置处理器，是不是想起了有一个与BeanFactoryPostProcessor的名字极其相似，它就是BeanPostProcessor。那什么是BeanPostProcessor呢？我们之前早就说过了，它就是bean的后置处理器，并且是在bean创建对象初始化前后进行拦截工作的。

现在要讲解的是BeanFactoryPostProcessor，上面也说过了，它是BeanFactory（创建bean的工厂）的后置处理器。接下来，我们就要搞清楚它的内部原理了，想要搞清楚其内部原理，我们需要从它是什么时候工作这一点开始入手研究，也即搞清楚它的调用时机是什么。

我们点进去BeanFactoryPostProcessor的源码里面去看一看，发现它是一个接口，如下图所示。

![image-20210928192216409](images\image-20210928192216409.png)

仔细看一下其内部postProcessBeanFactory方法上的描述，这很重要，因为从这段描述中我们就可以知道BeanFactoryPostProcessor的调用时机。描述中说，我们可以在IOC容器里面的BeanFactory的标准初始化完成之后，修改IOC容器里面的这个BeanFactory。

也就是说，BeanFactoryPostProcessor的调用时机是在BeanFactory标准初始化之后，这样一来，我们就可以来定制和修改BeanFactory里面的一些内容了。那什么叫标准初始化呢？接着看描述，它说的是所有的bean定义已经被加载了，但是还没有bean被初始化。
就是**BeanFactoryPostProcessor的调用时机是在BeanFactory标准初始化之后，这样一来，我们就可以来定制和修改BeanFactory里面的一些内容了，此时，所有的bean定义已经保存加载到BeanFactory中了，但是bean的实例还未创建。**

## 案例实践

首先，我们来编写一个我们自己的BeanFactoryPostProcessor，例如MyBeanFactoryPostProcessor。要编写这样一个bean工厂的后置处理器，它得需要实现我们上面说的BeanFactoryPostProcessor接口，并且还得添加一个实现方法。由于BeanFactoryPostProcessor接口里面只声明了一个方法，即postProcessBeanFactory，所以咱们自己编写的MyBeanFactoryPostProcessor类中只需要实现其即可。


```JAVA
public class MyBeanFactoryPostProcessor implements BeanFactoryPostProcessor {
    public void postProcessBeanFactory(ConfigurableListableBeanFactory beanFactory) throws BeansException {
        System.out.println("MyBeanFactoryPostProcessor...postProcessBeanFactory..."); // 这个时候我们所有的bean还没被创建
        // 但是我们可以看一下通过Spring给我们传过来的这个beanFactory，我们能拿到什么
        int count = beanFactory.getBeanDefinitionCount(); // 我们能拿到有几个bean定义
        String[] names = beanFactory.getBeanDefinitionNames(); // 除此之外，我们还能拿到每一个bean定义的名字
        System.out.println("当前BeanFactory中有" + count + "个Bean");
        System.out.println(Arrays.asList(names));
    }
}
```

注意，我们自己编写的MyBeanFactoryPostProcessor类要想让Spring知道，并且还要能被使用起来，那么它一定就得被加在容器中，为此，我们可以在其上标注一个@Component注解。

然后，创建一个配置类，例如ExtConfig，记得还要在该配置类上使用@ComponentScan注解来配置包扫描

```java
@ComponentScan("com.harry.spring")
@Configuration
public class ExtConfig {

}
```

当然了，我们也可以使用@Bean注解向容器中注入咱自己写的组件，例如，在这里，我们可以向容器中注入一个Blue组件。

```java
@ComponentScan("com.harry.spring")
@Configuration
public class ExtConfig {

    @Bean
    public Blue blue() {
        return new Blue();
    }


}
```

上面这个Blue组件其实就是一个非常普通的组件，代码如下所示：

```java
public class Blue {
    public Blue() {
        System.out.println("blue...constructor");
    }

    public void init() {
        System.out.println("blue...init...");
    }

    public void destory() {
        System.out.println("blue...destory...");
    }


}
```

可以看到，在创建Blue对象的时候，无参构造器会有相应打印。

接着，编写一个单元测试类，例如IOCTest_Ext，来进行测试。

```java
public class IOCTest_Ext {
    @Test
    public void test01() {
        AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext(ExtConfig.class);

        // 关闭容器
        applicationContext.close();
    }

}
```

实就是来验证一下BeanFactoryPostProcessor的调用时机。说得更具体一点就是，就是看一下咱们自己编写的BeanFactoryPostProcessor究竟是不是在所有的bean定义已经被加载，但是还未创建对象的时候工作

![image-20210928193511246](images\image-20210928193511246.png)

自己编写的BeanFactoryPostProcessor在Blue类的无参构造器创建Blue对象之前就已经工作了。细心一点看的话，从bean的定义信息中还能看到Blue组件注册到容器中的名字，只是此刻还没创建对象。

说明BeanFactoryPostProcessor是在所有的bean定义信息都被加载之后才调用的。

## 源码分析

接下来，我们就以debug的方式来看一下BeanFactoryPostProcessor的调用时机。

首先，在自己编写的MyBeanFactoryPostProcessor类里面的postProcessBeanFactory方法处打上一个断点，如下图所示。

![image-20210928193703406](images\image-20210928193703406.png)

然后，以debug的方式来运行IOCTest_Ext类中的test01方法，如下图所示，程序现在停到了MyBeanFactoryPostProcessor类里面的postProcessBeanFactory方法处。

![image-20210928193845541](images\image-20210928193845541.png)

那么程序是怎么运行到这儿的呢？我们不妨从IOCTest_Ext类中的test01方法开始，来梳理一遍整个流程。

鼠标单击Eclipse左上角方法调用栈中的IOCTest_Ext.test01() line:12，这时程序来到了IOCTest_Ext类的test01方法中，如下图所示
![image-20210928193929296](images\image-20210928193929296.png)

可以看到现在是要来创建IOC容器的。

继续跟进代码，可以看到创建IOC容器时，最后还得刷新容器，如下图所示。

![image-20210928194005555](images\image-20210928194005555.png)

继续跟进代码，可以看到在刷新容器的过程中，还得执行在容器中注册的BeanFactoryPostProcessor（BeanFactory的后置处理器）的方法。

![image-20210928194155927](images\image-20210928194155927.png)

那具体是怎么来执行BeanFactoryPostProcessor的呢？继续跟进代码，发现又调用了一个invokeBeanFactoryPostProcessors方法，如下图所示。

![image-20210928194247846](images\image-20210928194247846.png)

继续跟进代码，可以看到又调用了如下一个invokeBeanFactoryPostProcessors方法。

![image-20210928194347009](images\image-20210928194347009.png)

跟进程序到这里，此时要执行哪些BeanFactoryPostProcessor呢？从以上invokeBeanFactoryPostProcessors方法的参数中，我们可以看到第一个参数代表的是一个List<BeanFactoryPostProcessor>集合，它里面保存的就是那些要执行的BeanFactoryPostProcessor。

也就是说现在要执行的BeanFactoryPostProcessor从名为nonOrderedPostProcessors的`List`集合中拿就可以了。

下面我们来仔细分析一下PostProcessorRegistrationDelegate类中的invokeBeanFactoryPostProcessors方法具体都做了哪些操作。

首先，来看一下如下图所示的这行代码，这行代码说的是拿到所有BeanFactoryPostProcessor组件的名字。

![image-20210928194735376](images\image-20210928194735376.png)

然后，来挨个看相应名字的BeanFactoryPostProcessor组件，哪些是实现了PriorityOrdered接口的，哪些是实现了Ordered接口的，以及哪些是什么接口都没有实现的，说的简单一点就是将不同的BeanFactoryPostProcessor组件给分离出来。

![image-20210928194851873](images\image-20210928194851873.png)

接着，分别按不同的执行顺序来处理三种不同的BeanFactoryPostProcessor组件。

由于咱们自己编写的BeanFactoryPostProcessor既没有实现PriorityOrdered接口，也没有实现Ordered接口，所以就按照最后一种顺序来执行。

![image-20210928195053221](images\image-20210928195053221.png)

以上就是对PostProcessorRegistrationDelegate类中的invokeBeanFactoryPostProcessors方法大致分析。分析完之后，我们继续跟进代码，会发现其遍历了所有的BeanFactoryPostProcessor组件，我们自己编写的实现了BeanFactoryPostProcessor接口的MyBeanFactoryPostProcessor类肯定也属于其中，所以会被遍历到，然后便会执行其postProcessBeanFactory方法。
![image-20210928195140471](images\image-20210928195140471.png)

# 三、BeanDefinitionRegistryPostProcessor

BeanFactoryPostProcessor的调用时机是在BeanFactory标准初始化之后，这样一来，我们就可以来定制和修改BeanFactory里面的一些内容了。

接下来，我们就要学习一下BeanFactoryPostProcessor的一个子接口，即BeanDefinitionRegistryPostProcessor。

![image-20210928200030708](images\image-20210928200030708.png)

从上图中可以看到BeanDefinitionRegistryPostProcessor是BeanFactoryPostProcessor旗下的一个子接口。

## 从源码角度理解BeanDefinitionRegistryPostProcessor的原理

首先，咱们来看一下BeanDefinitionRegistryPostProcessor的源码，如下图所示。

![image-20210928200150929](images\image-20210928200150929.png)

从该接口的名字中，我们大概能知道个一二，说它是bean定义注册中心的后置处理器并不过分。而且，从该接口的源码中我们也可以看出，它是BeanFactoryPostProcessor旗下的一个子接口。

我们还能看到，它里面定义了一个方法，叫postProcessBeanDefinitionRegistry，我们可以看一下它上面的详细描述，说的是在IOC容器标准初始化之后，允许我们来修改IOC容器里面的bean定义注册中心。此时，所有合法的bean定义将要被加载，但是这些bean还没有初始化完成。

postProcessBeanDefinitionRegistry方法的执行时机是在所有bean定义信息将要被加载，但是bean实例还未创建的时候。 BeanDefinitionRegistryPostProcessor是在BeanFactoryPostProcessor前面执行的。

BeanFactoryPostProcessor的执行时机是在所有的bean定义信息已经保存加载到BeanFactory中之后，而BeanDefinitionRegistryPostProcessor却是在所有的bean定义信息将要被加载的时候，所以，BeanDefinitionRegistryPostProcessor就应该要先来执行。

## 案例实践

首先，编写一个类，例如MyBeanDefinitionRegistryPostProcessor，它应要实现BeanDefinitionRegistryPostProcessor这个接口。

```java
@Component
public class MyBeanDefinitionRegistryPostProcessor implements BeanDefinitionRegistryPostProcessor {

    public void postProcessBeanFactory(ConfigurableListableBeanFactory beanFactory) throws BeansException {
        // TODO Auto-generated method stub
        System.out.println("MyBeanDefinitionRegistryPostProcessor...bean的数量：" + beanFactory.getBeanDefinitionCount());
    }

    /**
     * 这个BeanDefinitionRegistry就是Bean定义信息的保存中心，这个注册中心里面存储了所有的bean定义信息，
     * 以后，BeanFactory就是按照BeanDefinitionRegistry里面保存的每一个bean定义信息来创建bean实例的。
     *
     * bean定义信息包括有哪些呢？有这些，这个bean是单例的还是多例的、bean的类型是什么以及bean的id是什么。
     * 也就是说，这些信息都是存在BeanDefinitionRegistry里面的。
     */
   
    public void postProcessBeanDefinitionRegistry(BeanDefinitionRegistry registry) throws BeansException {
        // TODO Auto-generated method stub
        System.out.println("postProcessBeanDefinitionRegistry...bean的数量：" + registry.getBeanDefinitionCount());
        // 除了查看bean的数量之外，我们还可以给容器里面注册一些bean，我们以前也简单地用过
        /*
         * 第一个参数：我们将要给容器中注册的bean的名字
         * 第二个参数：BeanDefinition对象
         */
        // RootBeanDefinition beanDefinition = new RootBeanDefinition(Blue.class); // 现在我准备给容器中添加一个Blue对象
        // 咱们也可以用另外一种办法，即使用BeanDefinitionBuilder这个构建器生成一个BeanDefinition对象，很显然，这两种方法的效果都是一样的
        AbstractBeanDefinition beanDefinition = BeanDefinitionBuilder.rootBeanDefinition(Blue.class).getBeanDefinition();
        registry.registerBeanDefinition("hello", beanDefinition);
    }

}
```

编写的类实现BeanDefinitionRegistryPostProcessor接口之后，还得来实现两个方法，第一个方法，即postProcessBeanFactory，它来源于BeanFactoryPostProcessor接口里面定义的方法；第二个方法，即postProcessBeanDefinitionRegistry，它来源于BeanDefinitionRegistryPostProcessor接口里面定义的方法。

接下来，我们就来测试一下以上类里面的两个方法是什么时候执行的。运行IOCTest_Ext测试类中的test01方法，可以看到控制台打印了如下内容。

![image-20210928201632233](images\image-20210928201632233.png)

可以看到，是我们自己写的MyBeanDefinitionRegistryPostProcessor类里面的postProcessBeanDefinitionRegistry方法先执行，它先是拿到IOC容器中bean的数量，再是向IOC容器中注册一个组件。接着，是我们自己写的MyBeanDefinitionRegistryPostProcessor类里面的postProcessBeanFactory方法再执行，该方法只是打印了一下IOC容器中bean的数量。

现在我们是不是可以得出这样一个结论，**BeanDefinitionRegistryPostProcessor是优先于BeanFactoryPostProcessor执行的，而且我们可以利用它给容器中再额外添加一些组件**。

## 源码分析

为什么BeanDefinitionRegistryPostProcessor是优先于BeanFactoryPostProcessor执行的呢？我们可以从源码的角度来深入分析一下。

首先，在我们自己写的MyBeanDefinitionRegistryPostProcessor类里面的两个方法上都打上一个断点，如下图所示。
![image-20210928202654670](images\image-20210928202654670.png)

然后，以debug的方式运行IOCTest_Ext测试类中的test01方法，如下图所示，程序现在停到了MyBeanDefinitionRegistryPostProcessor类里面的postProcessBeanDefinitionRegistry方法处。

![image-20210928202855953](images\image-20210928202855953.png)

进入调用栈中的`IOCTest_Ext.test01() line:12`，这时程序来到了IOCTest_Ext测试类的test01方法中，如下图所示。

![image-20210928202949710](images\image-20210928202949710.png)

可以看到现在是要来创建IOC容器的。

继续跟进代码，可以看到创建IOC容器时，最后还得刷新容器，如下图所示。

![image-20210928203033850](images\image-20210928203033850.png)

继续跟进代码，如下图所示，可以看到它里面调用了如下一个invokeBeanFactoryPostProcessors方法。

![image-20210928203112104](images\image-20210928203112104.png)

其实这跟我们上一讲中分析BeanFactoryPostProcessor的原理是一模一样的，它也是在IOC容器创建对象的时候，会来调用invokeBeanFactoryPostProcessors这个方法。既然都是调用这个方法，那怎么能说BeanDefinitionRegistryPostProcessor就要优先于BeanFactoryPostProcessor执行呢

继续跟进代码，发现又调用了一个invokeBeanFactoryPostProcessors方法，如下图所示

![image-20210928203221814](images\image-20210928203221814.png)

继续跟进代码，可以看到又调用了如下一个invokeBeanDefinitionRegistryPostProcessors方法。

![image-20211012203842291](images\image-20211012203842291.png)

注意，这个方法的名字叫invokeBeanDefinitionRegistryPostProcessors。此外，还能看到传递进该方法的第一个参数是currentRegistryProcessors，那它又是在哪儿定义的呢？这就不得不好好看看PostProcessorRegistrationDelegate类中的invokeBeanFactoryPostProcessors方法了。

仔细查看该方法，会发现刚进入该方法时，就说明了不管什么时候都会优先调用BeanDefinitionRegistryPostProcessor。由于我们自己写的MyBeanDefinitionRegistryPostProcessor类实现了这个接口，所以它肯定会被先调用。

![image-20211012204307601](images\image-20211012204307601.png)

继续向下看，可以看到会取出所有实现了BeanDefinitionRegistryPostProcessor接口的类，即从容器中获取到所有的BeanDefinitionRegistryPostProcessor组件。然后，优先调用实现了PriorityOrdered接口的BeanDefinitionRegistryPostProcessor组

![image-20211012204632974](images\image-20211012204632974.png)

调用完实现了PriorityOrdered接口的BeanDefinitionRegistryPostProcessor组件之后，接着会再调用实现了Ordered接口的BeanDefinitionRegistryPostProcessor组件。

最后再来调用剩余其他的BeanDefinitionRegistryPostProcessor组件，例如我们自己编写的MyBeanDefinitionRegistryPostProcessor类。

![image-20211012204744729](images\image-20211012204744729.png)

很显然，此时已经从容器中获取到了所有的BeanDefinitionRegistryPostProcessor组件，说是所有，但实际上现在就只获取到了一个，即我们自己编写的MyBeanDefinitionRegistryPostProcessor类。

![image-20211012205232627](images\image-20211012205232627.png)

继续往下跟进代码，可以看到现在所做的事情就是从容器中获取到所有的BeanDefinitionRegistryPostProcessor组件之后，再来依次调用它们的postProcessBeanDefinitionRegistry方法。

![image-20220522230024141](images\image-20220522230024141.png)

所以，BeanDefinitionRegistryPostProcessor组件里面的postProcessBeanDefinitionRegistry方法会最优先被调用。

# 四、ApplicationListener的用法

## ApplicationListener的概述

ApplicationListener按照字面意思，它应该是Spring里面的应用监听器，也就是Spring为我们提供的基于事件驱动开发的功能。

接下来，我们看一下ApplicationListener的源码，如下图所示，可以看到它是一个接口。

![image-20211013192605166](images\image-20211013192605166.png)

也就是说，如果我们要写一个监听器，那么我们要写的监听器就得实现这个接口，而该接口中带的泛型就是我们要监听的事件。也就是说，我们应该要监听ApplicationEvent及其下面的子事件，因此，如果我们要发布事件，那么所发布的事件应该是ApplicationEvent的子类。

## ApplicationListener的作用

它的作用主要是来监听IOC容器中发布的一些事件，只要事件发生便会来触发该监听器的回调，从而来完成事件驱动模型的开发。

## ApplicationListener的用法

首先，编写一个类来实现ApplicationListener接口，例如MyApplicationListener，这实际上就是写了一个监听器。

```java
@Component
public class MyApplicationListener implements ApplicationListener<ApplicationEvent> {

    // 当容器中发布此事件以后，下面这个方法就会被触发
    public void onApplicationEvent(ApplicationEvent event) {
        // TODO Auto-generated method stub
        System.out.println("收到事件：" + event);
    }

}
```

然后，我们就要来测试一下以上监听器的功能了。试着运行IOCTest_Ext测试类中的test01方法，看能不能收到事件

```java
public class IOCTest_Ext {
    @Test
    public void test01() {
        AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext(ExtConfig.class);

        // 关闭容器
        applicationContext.close();
    }

}
```

运行以上test01方法

![image-20211013193144025](images\image-20211013193144025.png)

可以看到我们收到了两个事件，这两个事件分别是org.springframework.context.event.ContextRefreshedEvent和org.springframework.context.event.ContextClosedEvent，其中第一个是容器已经刷新完成事件，第二个是容器关闭事件。
IOC容器在刷新完成之后便会发布ContextRefreshedEvent事件，一旦容器关闭了便会发布ContextClosedEvent事件。

发布自己的事件的步骤：

​	第一步，写一个监听器来监听某个事件。当然了，监听的这个事件必须是ApplicationEvent及其子类。

​	第二步，把监听器加入到容器中，这样Spring才能知道有这样一个监听器。

​	第三步，只要容器中有相关事件发布，那么我们就能监听到这个事件。举个例子，就拿我们上面监听的两个事件来说，你要搞清楚的一个问题是谁发布了这两个事件，猜都能猜得到，这两个事件都是由Spring发布的。

​		ContextRefreshedEvent：容器刷新完成事件。即容器刷新完成（此时，所有bean都已完全创建），便会发布该事件。
​		ContextClosedEvent：容器关闭事件。即容器关闭时，便会发布该事件。

​	第四步，我们自己来发布一个事件。而发布一个事件，我们需要像下面这么来做。

```java
public class IOCTest_Ext {
    @Test
    public void test01() {
        AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext(ExtConfig.class);
        // 发布一个事件
        applicationContext.publishEvent(new ApplicationEvent(new String("自己发布的事件")) {
        });
        // 关闭容器
        applicationContext.close();
    }

}
```

除了能收到容器刷新完成和容器关闭这俩事件之外，还能收到我们调用applicationContext发布出去的事件。只要把这个事件发布出去，那么我们自己编写的监听器就能监听到这个事件。

## 事件监听机制的源码分析

在研究分析事件的整个发布和事件监听机制的内部原理之前，我们先来运行一下如下单元测试类中的test01方法。

运行完毕，控制台打印出了如下三个收到的事件。

- ContextRefreshedEvent事件
- 我们自己发布的一个事件，即`IOCTest_Ext$1[source=我发布的事件]`
- ContextClosedEvent事件

### 创建容器并且刷新

首先，我们在自己编写的监听器（例如MyApplicationListener）内的onApplicationEvent方法处打上一个断点，如下图所示。

![image-20211013193835409](images\image-20211013193835409.png)

然后，以debug的方式运行IOCTest_Ext测试类中的test01方法，如下图所示，程序现在停到了咱们自己编写的监听器的onApplicationEvent方法中。

![image-20211013194410604](images\image-20211013194410604.png)

现在我们看到的是收到的第一个事件，即ContextRefreshedEvent事件

单击方法调用栈中的`IOCTest_Ext.test01() line:13`，这时程序来到了IOCTest_Ext测试类的test01方法中，如下图所示。

![image-20211013194508285](images\image-20211013194508285.png)

可以看到第一步是要来创建IOC容器的。继续跟进代码，可以看到在创建容器的过程中，还会调用一个refresh方法来刷新容器，刷新容器其实就是创建容器里面的所有bean。

![image-20211013194616657](images\image-20211013194616657.png)

继续跟进代码，看这个refresh方法里面具体都做了些啥，如下图所示，可以看到它里面调用了如下一个finishRefresh方法，顾名思义，该方法就是来完成容器的刷新工作的。

![image-20211013194718925](images\image-20211013194718925.png)

对于这个refresh方法而言，再熟悉不过了，它里面做了很多的事情，也就是说，在容器刷新这一步中做了很多的事情，比如执行BeanFactoryPostProcessor组件的方法、给容器中注册后置处理器等等。

### 容器刷新完成，发布ContextRefreshedEvent事件

当容器刷新完成时，就会调用finishRefresh方法，我们继续跟进代码，如下图所示，发现容器刷新完成时调用的finishRefresh方法里面又调用了一个叫publishEvent的方法，而且传递进该方法的参数是new出来的一个ContextRefreshedEvent对象。这一切都在说明着，容器在刷新完成以后，便会发布一个ContextRefreshedEvent事件。

![image-20211013194907369](images\image-20211013194907369.png)

### 事件发布流程

当容器刷新完成时，就会来调用一个叫publishEvent的方法，而且会向该方法中传递一个ContextRefreshedEvent对象。这即是发布了一个事件，这个事件呢，正是我们第一个感知到的事件，即容器刷新完成事件。接下来，我们就来看看这个事件到底是怎么发布的。

继续跟进代码，可以看到程序来到了如下图所示的地方。

![image-20211013195007949](images\image-20211013195007949.png)

我们继续跟进代码，可以看到程序来到了如下图所示的这行代码处。

![image-20211013195040396](images\image-20211013195040396.png)

可以看到先是调用一个getApplicationEventMulticaster方法，从该方法的名字中就可以看出，它是来获取事件多播器的，不过也有人叫事件派发器。接下来，就可以说说ContextRefreshedEvent事件的发布流程了。

首先，调用getApplicationEventMulticaster方法来获取到事件多播器，或者，你叫事件派发器也行。所谓的事件多播器就是指我们要把一个事件发送给多个监听器，让它们同时感知。

然后，调用事件多播器的multicastEvent方法，这个方法就是用来向各个监听器派发事件的。

继续跟进代码，来好好看看multicastEvent方法是怎么写的，如下图所示。

![image-20211013195159948](images\image-20211013195159948.png)

可以看到，一开始就有一个for循环，在这个for循环中，有一个getApplicationListeners方法，它是来拿到所有的ApplicationListener的，拿到之后就会来挨个遍历再来拿到每一个ApplicationListener。

很快，你会看到有一个if判断，它会判断getTaskExecutor方法能不能够返回一个Executor对象，如果能够，那么会利用Executor的异步执行功能来使用多线程的方式异步地派发事件；如果不能够，那么就使用同步的方式直接执行ApplicationListener的方法。

可以点进去Executor里面去看一看，会发现它是一个接口，并且Spring提供了一个叫TaskExecutor的子接口来继承它。在该子接口下，Spring又提供了一个SyncTaskExecutor类来实现它，以及一个AsyncTaskExecutor接口来继承它，如下图所示。
![image-20211013195345079](images\image-20211013195345079.png)

SyncTaskExecutor支持以同步的方式来执行某一任务，AsyncTaskExecutor支持以异步的方式来执行某一任务。也就是说，我们可以在自定义事件派发器的时候，给它传递这两种类型的TaskExecutor，让它支持以同步或者异步的方式来派发事件。

现在程序很显然是进入到了else判断语句中，也就是说，现在是使用同步的方式来直接执行ApplicationListener的方法的，相应地，这时是调用了一个叫invokeListener的方法，而且在该方法中传入了当前遍历出来的ApplicationListener。

我们继续跟进代码，可以看到程序来到了如下图所示的地方。这时，invokeListener方法里面调用了一个叫doInvokeListener的方法。

![image-20211013195704974](images\image-20211013195704974.png)

继续跟进代码，可以看到程序来到了如下图所示的这行代码处。看到这儿，差不多应该知道了这样一个结论，即**遍历拿到每一个ApplicationListener之后，会回调它的onApplicationEvent方法**。

![image-20211013195900357](images\image-20211013195900357.png)

继续跟进代码，这时，程序就会来到我们自己编写的监听器（例如MyApplicationListener）中，继而来回调它其中的onApplicationEvent方法。

![image-20211013200007898](images\image-20211013200007898.png)

以上就是ContextRefreshedEvent事件的发布流程。

总结一下一个事件怎么发布的。首先调用一个publishEvent方法，然后获取到事件多播器，接着为我们派发事件。

## @EventListener这个注解的原理

### @EventListener注解的用法

首先，编写一个普通的业务逻辑组件，例如UserService，并在该组件上标注一个@Service注解。

```java
@Service
public class UserService {

    @Autowired
    private UserDao userDao;
    @Transactional
    public void insertUser() {
        userDao.insert();
        System.out.println("插入完成...");
        int i = 10 / 0;
    }

}
```

在该组件内，我们肯定会写一些很多的方法，但这里就略去了。那么问题来了，如果我们希望该组件能监听到事件，那么该怎么办呢？我们可以在该组件内写一个listen方法，以便让该方法来监听事件。这时，我们只需要简单地给该方法上标注一个@EventListener注解，就可以让它来监听事件了。我们可以通过@EventListener注解中的classes属性来指定，例如，我们可以让listen方法监听ApplicationEvent及其下面的子事件。

```java
@Service
public class UserService {

    @Autowired
    private UserDao userDao;
    @Transactional
    public void insertUser() {
        userDao.insert();
        System.out.println("插入完成...");
        int i = 10 / 0;
    }

    // 一些其他的方法...

    @EventListener(classes= ApplicationEvent.class)
    public void listen() {
        System.out.println("UserService...");
    }
}
```

当然了，我们还可以通过@EventListener注解中的classes属性来指定监听多个事件。

```java
// @EventListener(classes=ApplicationEvent.class)
@EventListener(classes={ApplicationEvent.class})
public void listen() {
    System.out.println("UserService...");
}
```

如果ApplicationEvent及其下面的子事件发生了，我们就要在listen方法的参数位置上写一个ApplicationEvent参数来接收该事件。

```java
// @EventListener(classes=ApplicationEvent.class)
@EventListener(classes={ApplicationEvent.class})
public void listen(ApplicationEvent event) {
    System.out.println("UserService...");
}
```

以上就是我们自己编写的一个普通的业务逻辑组件，该组件就能监听事件，这跟实现ApplicationListener接口的效果是一模一样的。

然后，我们就要来进行测试了，就是运行一下以下IOCTest_Ext测试类中的test01方法。

![image-20211013200759763](images\image-20211013200759763.png)

控制台打印出了如下内容，可以清晰地看到，不仅我们之前编写的监听器（例如MyApplicationListener）收到了事件，而且UserService组件也收到了事件。也就是说，每一个都能正确地收到事件。

### @EventListener注解的原理

们可以点进去@EventListener这个注解里面去看一看，如下图所示，可以看到这个注解上面有一大堆的描述

![image-20211013200841812](images\image-20211013200841812.png)

描述中有一个醒目的字眼，即参考EventListenerMethodProcessor。意思可能是说，如果你想搞清楚@EventListener注解的内部工作原理，那么可以参考EventListenerMethodProcessor这个类。

EventListenerMethodProcessor就是一个处理器，其作用是来解析方法上的@EventListener注解的。Spring会使用EventListenerMethodProcessor这个处理器来解析方法上的@EventListener注解。因此，接下来，我们就要将关注点放在这个处理器上，搞清楚这个处理器是怎样工作的。

我们点进去EventListenerMethodProcessor这个类里面去看一看，如下图所示，发现它实现了一个接口，叫SmartInitializingSingleton。这时，要想搞清楚EventListenerMethodProcessor这个处理器是怎样工作的，那就得先搞清楚SmartInitializingSingleton这个接口的原理了。

![image-20211013201144599](images\image-20211013201144599.png)

点进去SmartInitializingSingleton这个接口里面去看一看，你会发现它里面定义了一个叫afterSingletonsInstantiated的方法，如下图所示。

![image-20211013201221112](images\image-20211013201221112.png)

接下来搞清楚到底是什么时候开始触发执行afterSingletonsInstantiated方法的。

仔细看一下SmartInitializingSingleton接口中afterSingletonsInstantiated方法上面的描述信息，不难看出该方法是在所有的单实例bean已经全部被创建完了以后才会被执行。

其实，在介绍SmartInitializingSingleton接口的时候，我们也能从描述信息中知道，在所有的单实例bean已经全部被创建完成以后才会触发该接口。紧接着下面一段的描述还说了，该接口的调用时机有点类似于ContextRefreshedEvent事件，即在容器刷新完成以后，便会回调该接口。也就是说，这个时候容器已经创建完了。

我们来看看afterSingletonsInstantiated方法的触发时机。首先，我们得在EventListenerMethodProcessor类里面的afterSingletonsInstantiated方法处打上一个断点，如下图所示。

![image-20211013201540074](images\image-20211013201540074.png)

以debug的方式运行IOCTest_Ext测试类中的test01方法，这时程序停留在了EventListenerMethodProcessor类里面的afterSingletonsInstantiated方法中，如下图所示。

![image-20211013201647208](images\image-20211013201647208.png)

鼠标单击方法调用栈中的`IOCTest_Ext.test01() line:13`，这时程序来到了IOCTest_Ext测试类的test01方法中，如下图所示。

![image-20211013201742444](images\image-20211013201742444.png)

可以看到第一步是要来创建IOC容器的。继续跟进代码，可以看到在创建容器的过程中，还会调用一个refresh方法来刷新容器，刷新容器其实就是创建容器里面的所有bean。

继续跟进代码，如下图所示，可以看到它里面调用了如下一个finishBeanFactoryInitialization方法，顾名思义，该方法就是来完成BeanFactory的初始化工作的。

![image-20211013202042116](images\image-20211013202042116.png)

它其实就是来初始化所有剩下的那些单实例bean的。也就是说，如果还有一些单实例bean还没被初始化，即还没创建对象，那么便会在这一步进行（初始化）。

继续跟进代码，如下图所示，可以看到在finishBeanFactoryInitialization方法里面执行了如下一行代码，依旧还是来初始化所有剩下的单实例bean。

![image-20211013202301104](images\image-20211013202301104.png)

继续跟进代码，如下图所示，可以看到现在程序停留在了如下这行代码处。

![image-20211013202338217](images\image-20211013202338217.png)

这不就是我们要讲的afterSingletonsInstantiated方法吗？它原来是在这儿调用的，接下来，就得好好看看在调用该方法之前，具体都做了哪些事。

由于afterSingletonsInstantiated方法位于DefaultListableBeanFactory类的preInstantiateSingletons方法里面，所以我们就得来仔细看看preInstantiateSingletons方法里面具体都做了些啥。

首先是一个for循环，在该for循环里面，beanNames里面存储的都是即将要创建的所有bean的名字，紧接着会做一个判断，即判断bean是不是抽象的，是不是单实例的，等等。最后，不管怎样，都会调用getBean方法来创建对象。

![image-20211013202521889](images\image-20211013202521889.png)

总结一下就是，**先利用一个for循环拿到所有我们要创建的单实例bean，然后挨个调用getBean方法来创建对象。也即，创建所有的单实例bean。

往下翻阅preInstantiateSingletons方法，发现它下面还有一个for循环，在该for循环里面，beanNames里面依旧存储的是即将要创建的所有bean的名字。那么，在该for循环中所做的事情又是什么呢？很显然，在最上面的那个for循环中，所有的单实例bean都已经全部创建完了。因此，在下面这个for循环中，所要做的事就是获取所有创建好的单实例bean，然后判断每一个bean对象是否是SmartInitializingSingleton这个接口类型的，如果是，那么便调用它里面的afterSingletonsInstantiated方法，而该方法就是SmartInitializingSingleton接口中定义的方法。

![image-20220522231529159](images\image-20220522231529159.png)


# 五、Spring IOC容器创建源码解析之BeanFactory的创建以及预准备工作

## BeanFactory的创建以及预准备工作

我们先来看一下如下的一个单元测试类（例如IOCTest_Ext）。

```java
public class IOCTest_Ext {
    @Test
    public void test01() {
        AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext(ExtConfig.class);
        // 发布一个事件
        applicationContext.publishEvent(new ApplicationEvent(new String("自己发布的事件")) {
        });
        // 关闭容器
        applicationContext.close();
    }

}
```

我们知道如下这样一行代码是来new一个IOC容器的，而且还可以看到传入了一个配置类。

```java
AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext(ExtConfig.class);

```

进去AnnotationConfigApplicationContext类的有参构造方法里面去看一看，如下图所示，

![image-20211014193226898](images\image-20211014193226898.png)

由于我们现在是来分析Spring容器的创建以及初始化过程，所以我们将核心的关注点放在refresh方法上，也即刷新容器。该方法运行完以后，容器就创建完成了，包括所有的bean对象也都创建和初始化完成了。

接下来，我们在刷新容器的方法上打上一个断点，如下图所示，重点分析一下刷新容器这个方法里面到底做了些什么事。

![image-20211014193730116](images\image-20211014193730116.png)

我们以debug的方式运行IOCTest_Ext测试类中的test01方法，如下图所示，程序现在停到了标注断点的refresh方法处。

![image-20211014193754952](images\image-20211014193754952.png)

进入refresh方法里面，如下图所示，可以看到映入眼帘的是一个线程安全的锁机制，除此之外，你还能看到第一个方法，即prepareRefresh方法，顾名思义，它是来执行刷新容器前的预处理工作的。

![image-20211014193828110](images\image-20211014193828110.png)

## prepareRefresh()：刷新容器前的预处理工作

让程序往下运行，运行到prepareRefresh方法处时，进入该方法里面，这儿也是来执行刷新容器前的预处理工作的。进入该方法里面，如下图所示，可以看到它里面都做了些什么预处理工作。

![image-20211014194137694](images\image-20211014194137694.png)

现就是先记录下当前时间，然后设置下当前容器是否是关闭、是否是活跃的等状态，除此之外，还会打印当前容器的刷新日志

## initPropertySources()：子类自定义个性化的属性设置的方法

顾名思义，该方法是来初始化一些属性设置的

进入该方法中，如下图所示，发现它是空的，没有做任何事情。

![image-20211014194338399](images\image-20211014194338399.png)

但是，我们要注意该方法是protected类型的，这意味着它是留给子类自定义个性化的属性设置的。例如，我们可以自己来写一个AnnotationConfigApplicationContext的子类，在容器刷新的时候，重写这个方法，这样，我们就可以在子类（也叫子容器）的该方法中自定义一些个性化的属性设置了。

## getEnvironment().validateRequiredProperties()：获取其环境变量，然后校验属性的合法性

让程序往下运行，直至运行到以下这行代码处。

![image-20211014195045485](images\image-20211014195045485.png)

这儿就是来校验这些属性的合法性的。

首先是要来获取其环境变量，进入getEnvironment方法中去看看，如下图所示，可以看到该方法就是用来获取其环境变量的。

![image-20211014195229234](images\image-20211014195229234.png)

快捷键让程序往下运行，让程序再次运行到getEnvironment().validateRequiredProperties()这行代码处。然后，进入validateRequiredProperties方法中去看看，如下图所示，可以看到就是使用属性解析器来进行属性校验的。
![image-20211014195335905](images\image-20211014195335905.png)

只不过，我们现在没有自定义什么属性，所以，此时并没有做任何属性校验工作。

## 保存容器中早期的事件

让程序往下运行，直至运行到以下这行代码处。

![image-20211014195439880](images\image-20211014195439880.png)

这儿是new了一个LinkedHashSet，它主要是来临时保存一些容器中早期的事件的。如果有事件发生，那么就存放在这个LinkedHashSet里面，这样，当事件派发器好了以后，直接用事件派发器把这些事件都派发出去。

总结一下就是一句话，即**允许收集早期的容器事件，等待事件派发器可用之后，即可进行发布**。

至此，我们就分析完了prepareRefresh方法，以上就是该方法所做的事情。我们发现这个方法和BeanFactory并没有太大关系，因此，接下来我们还得来看下一个方法，即obtainFreshBeanFactory方法。

## obtainFreshBeanFactory()：获取BeanFactory对象

让程序往下运行，直至运行至以下这行代码处。

![image-20211014195649279](images\image-20211014195649279.png)

可以看到一个叫obtainFreshBeanFactory的方法，顾名思义，它是来获取BeanFactory的实例的

## refreshBeanFactory()：创建BeanFactory对象，并为其设置一个序列化id

![image-20211014195848421](images\image-20211014195848421.png)

该方法见名思义，应该是来刷新BeanFactory的

键进入该方法中去看看，如下图所示，发现程序来到了GenericApplicationContext类里面。

![image-20211014200006784](images\image-20211014200006784.png)

而且，我们还可以看到在以上refreshBeanFactory方法中，会先判断是不是重复刷新了

程序往下运行，发现程序并没有进入到if判断语句中，而是来到了下面这行代码处。

![image-20211014202122002](images\image-20211014202122002.png)

beanFactory不是还没创建么，怎么在这儿又开始调用方法了呢，难道是已经创建了吗

向上翻阅GenericApplicationContext类的代码，发现原来是在这个类的无参构造方法里面，就已经实例化了beanFactory这个对象。也就是说，在创建GenericApplicationContext对象时，无参构造器里面就new出来了beanFactory这个对象。

现在，我们已经知道了在GenericApplicationContext这个类的无参构造方法里面，就已经实例化了beanFactory这个对象。

究竟是在什么地方调用GenericApplicationContext类的无参构造方法的呢，这时，我们可以去看一下我们的单元测试类（例如IOCTest_Ext），如下图所示

![image-20211014202421880](images\image-20211014202421880.png)

只要点进去AnnotationConfigApplicationContext类里面去看一看，你就知道大概了，如下图所示，原来AnnotationConfigApplicationContext类继承了GenericApplicationContext这个类，所以，当我们实例化AnnotationConfigApplicationContext时就会调用其父类的构造方法，相应地这时就会对我们的BeanFactory进行实例化了。
BeanFactory对象创建好了之后，接下来就是要给其设置一个序列化id，相当于打了一个id标识。我们不妨Inspect一下getId方法的值，发现它是`org.springframework.context.annotation.AnnotationConfigApplicationContext@51e2adc7`这么一长串的字符串

让程序往下运行，直至程序运行到下面这行代码处，refreshBeanFactory方法就执行完了。

![image-20211014203046367](images\image-20211014203046367.png)

该方法所做的事情很简单，无非就是**创建了一个BeanFactory对象（DefaultListableBeanFactory类型的），并为其设置好了一个序列化id**。

## getBeanFactory()：返回设置了序列化id后的BeanFactory对象

接下来，我们就要看看getBeanFactory方法了。进入该方法里面，如下图所示，发现它里面就只是做了一件事，即返回设置了序列化id后的BeanFactory对象。

![image-20211014203155796](images\image-20211014203155796.png)

让程序往下运行，还是运行到下面这行代码处，可以看到这儿是用ConfigurationListableBeanFactory接口去接受我们刚刚实例化的BeanFactory对象（DefaultListableBeanFactory类型的）。

![image-20211014203252073](images\image-20211014203252073.png)

让程序往下运行，一直让程序运行到下面这行代码处。程序运行至此，就返回了我们刚刚创建好的那个BeanFactory对象，只不过这个BeanFactory对象，由于我们刚创建，所以它里面的什么东西都是默认的一些设置。

![image-20211014203411921](images\image-20211014203411921.png)

至此，我们就分析完了obtainFreshBeanFactory方法，以上就是该方法所做的事情，即获取BeanFactory对象。

## prepareBeanFactory(beanFactory)：BeanFactory的预准备工作，即对BeanFactory进性一些预处理

该方法就是对BeanFactory做一些预处理，即BeanFactory的预准备工作。

为什么要在这儿对BeanFactory做一些预处理啊？因为我们前面刚刚创建好的BeanFactory还没有做任何设置呢，所以就得在这儿对BeanFactory做一些设置了。

进入该方法中，如下图所示，我们发现会对BeanFactory进行一系列的赋值（即设置一些属性）。比方说，设置BeanFactory的类加载器，就得像下面这样。

![image-20211014203608363](images\image-20211014203608363.png)

## postProcessBeanFactory(beanFactory)：BeanFactory准备工作完成后进行的后置处理工作

它说的就是在BeanFactory准备工作完成之后进行的后置处理工作。我们不妨点进去该方法里面看看，它究竟做了哪些事，如下图所示，发现它里面是空的。

![image-20211014203901979](images\image-20211014203901979.png)

这不是和刷新容器前的预处理工作中的initPropertySources方法一样吗？方法里面都是空的，默认都是不进行任何处理的，但是方法都是protected类型的，这也就是说子类可以通过重写这个方法，在BeanFactory创建并预处理完成以后做进一步的设置。

这个方法只有在子类重写的时候有用，只不过现在它还是空的，里面啥也没做。

让程序往下运行，一直让程序运行到下面这行代码处。程序运行到这里之后，我们先让它停一停。

![image-20211014204003293](images\image-20211014204003293.png)

至此，BeanFactory的创建以及预准备工作就已经完

# 六、Spring IOC容器创建源码解析之执行BeanFactoryPostProcessor

可以看到这儿会执行一个叫invokeBeanFactoryPostProcessors的方法，这个方法之前也看过，它就是来执行BeanFactoryPostProcessor的。它就是BeanFactory的后置处理器。那么，它是什么时候来执行的呢？不妨看一下它的源码，如下图所示。

![image-20211014204236239](images\image-20211014204236239.png)

从它内部方法的描述上来看，BeanFactoryPostProcessor（也可以说它里面的那个方法）是在BeanFactory标准初始化之后执行的。

我们之前也看过BeanFactoryPostProcessor接口的继承树，可以看到，BeanFactoryPostProcessor接口下还有一个子接口，即BeanDefinitionRegistryPostProcessor。以前，我们还用过BeanDefinitionRegistryPostProcessor这个接口给IOC容器中额外添加过组件

## 先执行BeanDefinitionRegistryPostProcessor的方法

键进入invokeBeanFactoryPostProcessors方法里面去，如下图所示，可以看到现在程序来到了如下这行代码处。

![image-20211014204432369](images\image-20211014204432369.png)

以上这个invokeBeanFactoryPostProcessors方法，看名字就知道了，同样是来执行BeanFactoryPostProcessor的方法的，进入代码看看，此时你会发现进入到了getBeanFactoryPostProcessors方法中，如下图所示，该方法仅仅只是返回了一个空的List<BeanFactoryPostProcessor>集合，该集合是用于存放所有的BeanFactoryPostProcessor的，只不过它现在默认是空的而已，也就是说该集合里面还没存储任何BeanFactoryPostProcessor。

![image-20211014205015294](images\image-20211014205015294.png)

不过，我们可以通过以下addBeanFactoryPostProcessor方法向该集合中添加BeanFactoryPostProcessor。

退出getBeanFactoryPostProcessors方法，返回到调用层，然后进入invokeBeanFactoryPostProcessors方法里面去一探究竟，如下图所示

![image-20211014205240599](images\image-20211014205240599.png)

其中，一开始的注释就告诉了我们，无论什么时候都会先调用实现了BeanDefinitionRegistryPostProcessor接口的类。

紧接着会先来判断我们这个beanFactory是不是BeanDefinitionRegistry。生成的BeanFactory对象是DefaultListableBeanFactory类型的，而且还使用了ConfigurableListableBeanFactory接口进行接收。这里我们就来看下DefaultListableBeanFactory类是不是实现了BeanDefinitionRegistry接口，看下图，很显然是实现了。


![image-20211014205355309](images\image-20211014205355309.png)

自然地，程序就会进入到if判断语句中，进来以后呢，我们来大致地分析一下下面的流程。首先，映入眼帘的是一个for循环，它是来循环遍历invokeBeanFactoryPostProcessors方法中的第二个参数的，即beanFactoryPostProcessors。其实呢，就是拿到所有的BeanFactoryPostProcessor，再挨个遍历出来。然后，再来以遍历出来的每一个BeanFactoryPostProcessor是否实现了BeanDefinitionRegistryPostProcessor接口为依据将其分别存放于以下两个箭头所指向的LinkedList中，其中实现了BeanDefinitionRegistryPostProcessor接口的还会被直接调用。

让程序往下运行，直至运行到下面这行代码处，可以看到现在是会拿到所有BeanDefinitionRegistryPostProcessor的这些bean的名字。

执行实现了PriorityOrdered优先级接口的BeanDefinitionRegistryPostProcessor的postProcessBeanDefinitionRegistry方法

往下运行一步即可，Inspect一下postProcessorNames变量的值，你会发现从IOC容器中拿到的只有一个名字为org.springframework.context.annotation.internalConfigurationAnnotationProcessor的组件，即默认拿到的是ConfigurationClassPostProcessor这样一个BeanDefinitionRegistryPostProcessor。


再往下执行实现了Ordered顺序接口的BeanDefinitionRegistryPostProcessor

最后执行没有实现任何优先级或者顺序接口的BeanDefinitionRegistryPostProcessor

## 执行BeanFactoryPostProcessors

同样先根据优先级判断BeanFactoryPostProcessors

随后获取所有的BeanFactoryPostProcessors

BeanPostProcessor接口旗下确实是有非常多的子接口，而且这些不同接口类型的BeanPostProcessor在bean创建前后的执行时机是不一样的，虽然它们都是后置处理器。

DestructionAwareBeanPostProcessor
InstantiationAwareBeanPostProcessor
SmartInstantiationAwareBeanPostProcessor
MergedBeanDefinitionPostProcessor

# 七、Spring IOC容器创建源码解析之初始化MessageSource组件

顾名思义，该方法是来初始化MessageSource组件的。对于Spring MVC而言，该方法主要是来做国际化功能的，如消息绑定、消息解析等。

![image-20211017092730006](images\image-20211017092730006.png)

## 初始化MessageSource组件

### 获取BeanFactory

进入到initMessageSource方法里面，如下图所示，可以看到一开始是先来获取BeanFactory的。

![image-20211017092834535](images\image-20211017092834535.png)

### 看容器中是否有id为messageSource，类型是MessageSource的组件

程序继续往下运行，会发现有一个判断，即判断BeanFactory中是否有一个id为messageSource的组件。我为什么会这么说呢，你只要看一下常量`MESSAGE_SOURCE_BEAN_NAME`的值就知道了，如下图所示，该常量的值就是messageSource。

![image-20211017092945234](images\image-20211017092945234.png)

如果有的话，那么会从BeanFactory中获取到id为messageSource，类型是MessageSource的组件，并将其赋值给`this.messageSource`。这可以从下面这行代码看出。

![image-20211017093122399](images\image-20211017093122399.png)

很显然，容器刚开始创建的时候，肯定是还没有的，所以程序会来到下面的else语句中。

### 若没有，则创建一个DelegatingMessageSource类型的组件，并把创建好的组件注册在容器中

如果没有的话，那么Spring自己会创建一个DelegatingMessageSource类型的对象，即MessageSource类型的组件。

查看一下MessageSource接口的源码，如下图所示，它里面定义了很多重载的getMessage方法，该方法可以从配置文件（特别是国际化配置文件）中取出某一个key所对应的值。
![image-20211017093226222](images\image-20211017093226222.png)

也就是说，这种MessageSource类型的组件的作用一般是取出国际化配置文件中某个key所对应的值

紧接着，把创建好的MessageSource类型的组件注册到容器中，所执行的是下面这行代码。

![image-20211017093316250](images\image-20211017093316250.png)

# 八、Spring IOC容器创建源码解析之初始化事件派发器

![image-20211017093414159](images\image-20211017093414159.png)

方法是来初始化事件派发器的。

## 初始化事件派发器

进入到initApplicationEventMulticaster方法里面，如下图所示，可以看到一开始是先来获取BeanFactory的。

![image-20211017093515523](images\image-20211017093515523.png)

看容器中是否有id为applicationEventMulticaster，类型是ApplicationEventMulticaster的组件

让程序继续往下运行，会发现有一个判断，即判断BeanFactory中是否有一个id为applicationEventMulticaster的组件。

![image-20211017093619609](images\image-20211017093619609.png)

若有，则赋值给this.applicationEventMulticaster

如果有的话，那么会从BeanFactory中获取到id为applicationEventMulticaster，类型是ApplicationEventMulticaster的组件，并将其赋值给`this.applicationEventMulticaster`

若没有，则创建一个SimpleApplicationEventMulticaster类型的组件，并把创建好的组件注册在容器中

如果没有的话，那么Spring自己会创建一个SimpleApplicationEventMulticaster类型的对象，即一个简单的事件派发器。

然后，把创建好的事件派发器组件注册到容器中，即添加到BeanFactory中，所执行的是下面这行代码。

![image-20211017093733583](images\image-20211017093733583.png)

让程序继续往下运行，直至运行到下面这行代码处。

![image-20211017093821788](images\image-20211017093821788.png)

进入到以上onRefresh方法里面去看一看，如下图所示，发现它里面是空的。

![image-20211017093907856](images\image-20211017093907856.png)

以上onRefresh方法就是留给子类来重写的，这样是为了给我们留下一定的弹性，当子类（也可以说是子容器）重写该方法后，在容器刷新的时候就可以再自定义一些逻辑了，比如给容器中多注册一些组件之类的。

让程序继续往下运行，直至运行到下面这行代码处。

![image-20211017094016597](images\image-20211017094016597.png)

按照registerListeners方法上面的注释来说，该方法是来检查监听器并注册它们的。也就是说，该方法会将我们项目里面的监听器（也即咱们自己编写的ApplicationListener）注册进来。

进入到以上registerListeners方法里面去看一看，如下图所示。

![image-20211017094109276](images\image-20211017094109276.png)

让程序继续往下运行时，来到了下面这行代码处。

![image-20211017094245708](images\image-20211017094245708.png)

这是调用getBeanNamesForType方法从容器中拿到ApplicationListener类型的所有bean的名字的。也就是说，首先会从容器中拿到所有的ApplicationListener组件。

让程序继续往下运行，运行一步即可，这时Inspect一下listenerBeanNames变量的值，就能看到确实是获取到了咱们自己编写的ApplicationListener了，如下图所示。

![image-20211017094526907](images\image-20211017094526907.png)

当早期我们容器中有一些事件时，会将这些事件保存在名为earlyApplicationEvents的Set集合中。这时，会先获取到事件派发器，再利用事件派发器将这些事件派发出去。也就是说，派发之前步骤产生的事件。

程序运行至下面这行代码处时，registerListeners方法就执行完了，它所做的事情很简单，无非就是**从容器中拿到所有的ApplicationListener组件，然后将每一个监听器添加到事件派发器中**。

![image-20211017094643176](images\image-20211017094643176.png)

# 九、Spring IOC容器创建源码解析之初始化所有剩下的单实例bean

## 初始化所有剩下的单实例bean

进入finishBeanFactoryInitialization方法里面，如下图所示

![image-20211017094823916](images\image-20211017094823916.png)

## 获取容器中所有的bean，然后依次进行初始化和创建对象

进入preInstantiateSingletons方法里面，如下图所示，可以看到一开始会先获取容器中所有bean的名字。当程序运行至如下这行代码处时，我们不妨Inspect一下beanNames变量的值，可以看到容器中现在有好多bean，有我们自己编写的组件，有Spring默认内置的一些组件。

![image-20211017095008372](images\image-20211017095008372.png)

对于容器中现在所有的这些bean来说，有些bean可能已经在之前的步骤中创建以及初始化完成了。因此，preInstantiateSingletons方法就是来初始化所有剩下的bean的。你能很明显地看到，这就有一个for循环，该for循环是来遍历容器中所有的bean，然后依次触发它们的整个初始化逻辑的。


## 获取bean的定义注册信息

进入for循环中之后，会获取到每一个遍历出来的bean的定义注册信息。我们要知道bean的定义注册信息是需要用RootBeanDefinition这种类型来进行封装的。

![image-20211017095238644](images\image-20211017095238644.png)

## 根据bean的定义注册信息判断bean是否是抽象的、单实例的、懒加载的

接下来，会根据bean的定义注册信息来判断bean是否是抽象的、单实例的、懒加载的。如果该bean既不是抽象的也不是懒加载的（我们之前就说过懒加载，它就是用到的时候再创建对象，与@Lazy注解有关），并且还是单实例的，那么这个时候程序就会进入到最外面的if判断语句中，如下图所示。


![image-20211017095331162](images\image-20211017095331162.png)

让程序继续往下运行，你会发现还有一个判断，它是来判断当前bean是不是FactoryBean的，若是则进入到if判断语句中，若不是则进入到else分支语句中。

![image-20211017095422770](images\image-20211017095422770.png)

进isFactoryBean方法里面去看一看，如下图所示，可以很清楚地看到该方法就是来判断当前bean是不是属于FactoryBean接口的。

![image-20211017095516030](images\image-20211017095516030.png)

过判断，如果我们的bean确实实现了FactoryBean接口，那么Spring就会调用FactoryBean接口里面的getObject方法来帮我们创建对象，查看FactoryBean接口的源码。

![image-20211017095553524](images\image-20211017095553524.png)

来看看第一个bean究竟是不是属于FactoryBean接口

![image-20211017095704087](images\image-20211017095704087.png)

让程序继续往下运行，此时程序来到了下面的else分支语句中，如下图所示。

![image-20211017095740591](images\image-20211017095740591.png)

为了能够继续跟踪Spring源码的执行过程，我们可以在getBean方法处打上一个断点，如下图所示。

然后，我们就需要给程序不断地放行了，一直放行到我们自己编写的bean中

从该配置类的代码中，我们可以看到还会向容器中注册一个我们自己编写的Blue组件。同样地，为了方便继续跟踪Spring源码的执行过程，我们也可以在下图所示的地方打上一个断点。

![image-20211017100143133](images\image-20211017100143133.png)

让程序运行到下一个断点，可以看到现在是来创建第二个bean的对象。

运行到下一个断点，直至放行到Blue对象的创建为止，如下图所示，在这一过程中，我们可以依次看到每一个bean的创建。

序运行至此，我们可以知道Blue对象是得通过getBean方法来创建的。

进入getBean方法里面去看一看，如下图所示，可以看到它里面又调用了一个叫doGetBean的方法。

![image-20211017101544262](images\image-20211017101544262.png)

进入doGetBean方法里面去看一看，如下图所示，可以看到一开始会拿到我们的bean的名字。

![image-20211017101635918](images\image-20211017101635918.png)

然后，根据我们bean的名字尝试获取缓存中保存的单实例bean。你可以看到这儿调用的是getSingleton方法，而且从缓存中获取到了之后会赋值给一个叫sharedInstance的变量，它翻译过来就是共享的bean。

![image-20211017101737258](images\image-20211017101737258.png)

所有创建过的单实例bean都会被缓存起来，所以这儿会调用getSingleton方法先从缓存中获取。如果能获取到，那么说明这个单实例bean之前已经被创建过了。

进入getSingleton方法里面去看一看，如下图所示，发现它里面是下面这个样子的，好像是又调用了一个重载的getSingleton方法。

进入以上getSingleton方法里面去看一看，如下图所示，可以看到从缓存中获取其实就是从singletonObjects属性里面来获取。

![image-20211017101920934](images\image-20211017101920934.png)

让程序继续往下运行，运行一步即可，此时Inspect一下singletonObject变量的值，发现是null，如下图所示，这说明名字为blue的bean从缓存中是获取不到的。

![image-20211017102115841](images\image-20211017102115841.png)

让程序往下运行，直至运行到下面这行代码处。

![image-20211017102436830](images\image-20211017102436830.png)

让程序往下运行，此时程序并没有进入到以上if判断语句中，而是来到了下面这行代码处。

![image-20211017102521333](images\image-20211017102521333.png)

程序运行至这里，如果从缓存中获取不到我们的bean，那么我们自然就得来创建了，走的便是下面else分支语句里面的逻辑。

现在是该开始创建我们bean的对象了，从上图中可以看到，首先会来获取一个（父）BeanFactory，因为我们后来也是用它来创建对象的。然后，立马会有一个判断，即判断是不是能获取到（父）BeanFactory

让程序继续往下运行，我们会发现程序并没有进入到if判断语句中，而是来到了下面这行代码处，这说明并没有获取到（父）BeanFactory。

![image-20211017102646438](images\image-20211017102646438.png)

可以看到这儿又有一个判断，而且程序能够进入到该if判断语句中

markBeanAsCreated方法它是在我们的bean被创建之前，先来标记其为已创建，相当于做了一个小标记，这主要是为了防止多个线程同时来创建同一个bean，从而保证了bean的单实例特性

让程序继续往下运行，当程序运行至下面这行代码处时，可以看到这是来获取我们bean的定义信息的。

![image-20211017102821973](images\image-20211017102821973.png)

让程序往下运行，直至运行到下面这行代码处。

![image-20211017102855678](images\image-20211017102855678.png)

可以看到这儿调用了bean定义信息对象的一个getDependsOn方法，它是来获取我们当前bean所依赖的其他bean的。

可以看到，depends-on属性也在Spring的源码中得到了体现，这可以参考上图。我们可以看到，会先获取我们当前bean所依赖的其他bean，如果我们要创建的bean确实有依赖其他bean的话，那么还是会调用getBean方法把所依赖的bean都创建出来。

![image-20211017102944977](images\image-20211017102944977.png)

研究到这里，我们又会发现使用它来创建我们的bean之前，它做的一件大事，就是把我们要创建的bean所依赖的bean先创建出来，当然了，前提是我们要创建的bean是确实是真的有依赖其他bean。

让程序往下运行，会发现程序并没有进入到if判断语句中，而是来到了下面这行代码处。

![image-20211017103030335](images\image-20211017103030335.png)

在这会做一个判断，即判断我们的bean是不是单实例的，由于我们的bean就是单实例的，所以程序会进入到if判断语句中，来启动单实例bean的创建流程。

我们可以看到，现在是调用了一个叫getSingleton的方法，而且在调用该方法时，还传入了两个参数，第一个参数是咱们单实例bean的名字，第二个参数是ObjectFactory对象

为了方便继续跟踪Spring源码的执行过程，我们不妨在createBean方法处打上一个断点

![image-20211017103145456](images\image-20211017103145456.png)

让程序直接运行到下一个断点，此时程序来到了createBean方法处

进入到createBean方法里面去看一看，如下图所示。

![image-20211017103246271](images\image-20211017103246271.png)

当程序往下运行时，可以看到会先拿到我们bean的定义信息，然后再来解析我们要创建的bean的类型。

![image-20211017103316371](images\image-20211017103316371.png)

继续让程序往下运行，直至运行到下面这行代码处为止。

![image-20211017103424173](images\image-20211017103424173.png)

可以看到，在创建我们bean的对象之前，会调用了一个resolveBeforeInstantiation方法，看该方法上的注释，它说是给BeanPostProcessor一个机会来提前返回我们bean的代理对象，这主要是为了解决依赖注入问题。也就是说，这是让BeanPostProcessor先拦截并返回代理对象。

一般而言，BeanPostProcessor都是在创建完bean对象初始化前后进行拦截的。而现在我们还没创建对象呢，因为我们是调用createBean方法来创建对象的，这也就是说，我们bean的对象还未创建之前，就已经有了一个BeanPostProcessor

键进入resolveBeforeInstantiation方法里面去看一看，如下图所示，当程序运行到下面这行代码处时，才知道原来是InstantiationAwareBeanPostProcessor这种类型的BeanPostProcessor。

![image-20211017103646711](images\image-20211017103646711.png)

可以看到这儿是来判断是否有InstantiationAwareBeanPostProcessor这种类型的后置处理器的。如果有，那么就会来执行InstantiationAwareBeanPostProcessor这种类型的后置处理器

看到那个applyBeanPostProcessorsBeforeInstantiation方法，点进入看一下

![image-20211017103800061](images\image-20211017103800061.png)

在该方法中，会先判断遍历出的每一个BeanPostProcessor是不是InstantiationAwareBeanPostProcessor这种类型的，如果是，那么便来触发其postProcessBeforeInstantiation方法，该方法定义在InstantiationAwareBeanPostProcessor接口中。

如果applyBeanPostProcessorsBeforeInstantiation方法执行完之后返回了一个对象，并且还不为null，那么紧接着就会来执行后面的applyBeanPstProcessorsAfterInitialization方法。

![image-20211017103946154](images\image-20211017103946154.png)

可以看到它里面是来执行每一个BeanPostProcessor的postProcessAfterInitialization方法的。注意，postProcessAfterInitialization方法是定义在BeanPostProcessor接口中的，只不过是InstantiationAwareBeanPostProcessor接口继承过来了而已。

也就是说，如果有InstantiationAwareBeanPostProcessor这种类型的后置处理器，那么会先执行其postProcessBeforeInstantiation方法，并看该方法有没有返回值（即创建的代理对象），若有则再执行其postProcessAfterInitialization方法

让程序继续往下运行，直至运行到下面这行代码处，看来我们确实是有InstantiationAwareBeanPostProcessor这种类型的后置处理器。

![image-20211017104111533](images\image-20211017104111533.png)

进入applyBeanPostProcessorsBeforeInstantiation方法里面去瞧一瞧，如下图所示，可以看到它里面会遍历获取到的所有的BeanPostProcessor，接着再来判断遍历出的每一个BeanPostProcessor是不是InstantiationAwareBeanPostProcessor这种类型的。很明显，遍历出的第一个BeanPostProcessor并不是InstantiationAwareBeanPostProcessor这种类型的，所以程序并没有进入到最外面的if判断语句中。

![image-20211017104143424](images\image-20211017104143424.png)

继续让程序往下运行，发现这时遍历出的第二个BeanPostProcessor是ConfigurationClassPostProcessor，而且它还是InstantiationAwareBeanPostProcessor这种类型的，于是，程序自然就进入到了最外面的if判断语句中，如下图所示。

![image-20211017104247653](images\image-20211017104247653.png)

ConfigurationClassPostProcessor这种后置处理器是来解析标准了@Configuration注解的配置类的。

紧接着便会来执行ConfigurationClassPostProcessor这种后置处理器的postProcessBeforeInstantiation方法了，但是该方法的返回值为null。于是，我们继续让程序往下运行，直至遍历完所有的BeanPostProcessor。


在创建单实例bean之前，InstantiationAwareBeanPostProcessor这种类型的后置处理器中两个方法的执行时机，即先执行其postProcessBeforeInstantiation方法，并看该方法有没有返回值（即创建的代理对象），若有则再执行其postProcessAfterInitialization方法。


而且，此时程序停留在了下面这行代码处。

![image-20211018200908567](images\image-20211018200908567.png)

让程序往下运行，直至运行到下面这行代码处为止。

![image-20211018201044095](images\image-20211018201044095.png)

这时，resolveBeforeInstantiation方法总算是执行完了，它是在创建我们单实例bean之前，先来给BeanPostProcessor一个返回其代理对象的机会。但是，此刻是没有返回我们单实例bean的代理对象的。

让程序往下运行了，继续执行下面的流程，当程序运行到下面这行代码处时，发现调用了一个叫doCreateBean的方法，顾名思义，该方法就是来创建我们bean的实例的

![image-20211018201209552](images\image-20211018201209552.png)

## 单实例bean的创建流程

进入doCreateBean方法里面去看一下，如下图所示，可以看到会用BeanWrapper接口来接收我们创建的bean

![image-20211018201258678](images\image-20211018201258678.png)

让程序往下运行，直至运行到下面这行代码处为止，可以看到这儿调用的是一个叫createBeanInstance的方法，顾名思义，它是来创建bean实例的。

也就是说，创建bean的流程的第一步就是先来创建bean实例

## 创建bean实例

当执行完createBeanInstance方法之后，我们bean的对象就创建出来了，进入createBeanInstance方法里面去看一下，如下图所示，可以看到一开始就要来解析一下我们要创建的bean的类型。

![image-20211018202120295](images\image-20211018202120295.png)

让程序往下运行，由于解析出来的类型为null，所以程序并不会进入到下面的if判断语句中，而是来到了下面这行代码处。

![image-20211018202207953](images\image-20211018202207953.png)

首先，在if判断语句中的条件表达式中，可以看到调用了bean定义信息对象的一个getFactoryMethodName方法，该方法是来获取工厂方法的名字的。Inspect一下mbd.getFactoryMethodName()表达式的值，发现其值就是blue。

为什么叫工厂方法呢，如下图所示，我们是使用标注了@Bean注解的blue方法来创建Blue对象并将其注册到IOC容器中的。也就是说，blue方法就相当于Blue对象的工厂方法。

![image-20211018202428755](images\image-20211018202428755.png)

现在程序是停留在了if判断语句块内，此时就是来执行Blue对象的工厂方法（即blue方法）来创建Blue对象的。

继续运行代码直至运行到下面这行代码处为止。程序运行至此，咱们这个bean实例（即Blue对象）就创建出来了，只不过该Blue对象刚刚创建出来，空空如也，什么都没有。

![image-20211018202945831](images\image-20211018202945831.png)

这时，以上createBeanInstance方法就算是执行完了，也就是说，创建出了我们的bean实例（即Blue对象）。

后，让程序继续往下运行，直至运行到下面这行代码处为止，从这行代码上面的注释中，我们可以看到这块允许后置处理器来修改咱们这个bean的定义信息。

![image-20211018203041413](images\image-20211018203041413.png)

很明显，我们的bean实例创建完了以后，接下来就得来调用这个applyMergedBeanDefinitionPostProcessors方法了。

让程序继续往下运行，直至运行到下面这行代码处为止，可以看到这儿调用了一个applyMergedBeanDefinitionPostProcessors方法。

直接点击该方法进去它里面看一下，如下图所示，可以看到先是来获取到所有的后置处理器，然后再来遍历它们，如果是MergedBeanDefinitionPostProcessor这种类型的，那么就调用其postProcessMergedBeanDefinition方法。

![image-20211018203219305](images\image-20211018203219305.png)

从这儿也能看到，每一个后置处理器（或者说它里面的方法）的执行时机都是不一样的，比如InstantiationAwareBeanPostProcessor这种类型的后置处理器中的两个方法的执行时机是在创建bean实例之前，而现在MergedBeanDefinitionPostProcessor这种类型的后置处理器，是在创建完bean实例以后，来执行它里面的postProcessMergedBeanDefinition方法的。

接着，让程序继续往下运行，直至运行到下面这行代码处为止，很明显，populateBean方法是来为bean的属性赋值的。

![image-20211018203505394](images\image-20211018203505394.png)

## 为bean实例的属性赋值

在该方法内，首先会创建出我们的bean实例，然后再执行MergedBeanDefinitionPostProcessor这种类型的后置处理器，接着，创建完bean实例之后就得为其属性赋值了。

进入populateBean方法里面去看一下，如下图所示，可以看到一开始会拿到赋给所有属性的属性值。

![image-20211018203734036](images\image-20211018203734036.png)

遍历获取到的所有后置处理器，若是InstantiationAwareBeanPostProcessor这种类型，则调用其postProcessAfterInstantiation方法

## 正式开始为bean的属性赋值

接下来，继续让程序往下运行，此时，populateBean方法就执行完了，也就是说，已经为我们bean的属性赋完值了。接着继续让程序往下运行，运行一步即可，这时程序来到了下面这行代码处。

![image-20211018204230822](images\image-20211018204230822.png)

可以看到，这儿调用了一个initializeBean方法，它就是来初始化bean的

## 初始化bean

总结前面的步骤：

1）在创建bean实例之前，会执行InstantiationAwareBeanPostProcessor这种类型的后置处理器中的两个方法，即postProcessBeforeInstantiation方法和postProcessAfterInitialization方法
2）创建bean实例
3）为bean实例的属性赋值。在赋值的过程中，会依次执行InstantiationAwareBeanPostProcessor这种类型的后置处理器中的两个方法，即postProcessAfterInstantiation方法和postProcessPropertyValues方法
4）初始化bean

进入initializeBean方法中去，如下图所示，进来之后，让程序运行到下面这行代码处。

![image-20211018204432727](images\image-20211018204432727.png)

可以看到，这儿调用了一个invokeAwareMethods方法，顾名思义，它是来执行XxxAware接口中的方法的。

进入该方法里面去看一下，如下图所示。

![image-20211018204522463](images\image-20211018204522463.png)

可以看到，它就是来判断我们的bean是不是实现了BeanNameAware、BeanClassLoaderAware、BeanFactoryAware这些Aware接口的，若是则回调接口中对应的方法。

当然了，现在我们的bean（即Blue对象）是没有实现以上这些Aware接口的，所以，我们直接让程序继续往下运行，直至运行到下面这行代码处为止。

## 执行后置处理器初始化之前的方法

执行完XxxAware接口中的方法之后，可以看到会再来调用一个applyBeanPostProcessorsBeforeInitialization方法，进入该方法里面去看一下，如下图所示。

![image-20211019192314157](images\image-20211019192314157.png)

在applyBeanPostProcessorsBeforeInitialization方法中，会遍历所有的后置处理器，然后依次执行所有后置处理器的postProcessBeforeInitialization方法，一旦后置处理器的postProcessBeforeInitialization方法返回了null以后，则后面的后置处理器便不再执行了，而是直接退出for循环。

然后，我们让程序继续往下运行，一直运行到下面这行代码处为止。

![image-20211019193226113](images\image-20211019193226113.png)

## 执行初始化方法

执行完后置处理器的postProcessBeforeInitialization方法之后，可以看到现在又调用了一个invokeInitMethods方法，其作用就是执行初始化方法。

可以看到，以上Cat组件实现了一个InitializingBean接口，而该接口中定义了一个afterPropertiesSet方法，必然在Cat组件内就会实现该方法，这样，该方法就是Cat组件的初始化方法了。

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

当然了，我们除了通过以上方式来指定初始化方法之外，还可以在@Bean注解中使用initMehod属性来指定初始化方法

来看一下究竟是如何来执行初始化方法的，进入invokeInitMethods方法里面去看一下，如下图所示。

![image-20211019193544819](images\image-20211019193544819.png)

可以看到，一开始就会来判断我们的bean是否是InitializingBean接口的实现，若是则执行该接口中定义的初始化方法。

如果不是的话，可以发现程序并没有进入到下面的if判断语句中，而是来到了下面这行代码处，这是因为我们的bean并没有实现InitializingBean接口。

![image-20211019193729243](images\image-20211019193729243.png)

现在的bean是没有自定义初始化方法的，因此在程序继续往下运行的过程中，程序并不会进入到下面的if判断语句中，而是来到了下面这行代码处。

![image-20211019193911859](images\image-20211019193911859.png)

此时，invokeInitMethods方法便执行完了。这其实就是说，Spring会帮我们把我们bean中的初始化方法回调一下。

## 执行后置处理器初始化之后的方法（即postProcessAfterInitialization方法）

初始化方法执行完了以后，下一步就是来调用applyBeanPostProcessorsAfterInitialization方法

![image-20211019194016209](images\image-20211019194016209.png)

进入该方法里面去看一下，如下图所示。

![image-20211019194045146](images\image-20211019194045146.png)

可以看到，在applyBeanPostProcessorsAfterInitialization方法中，会遍历所有的后置处理器，然后依次执行所有后置处理器的postProcessAfterInitialization方法，一旦后置处理器的postProcessAfterInitialization方法返回了null以后，则后面的后置处理器便不再执行了，而是直接退出for循环。

然后，我们让程序继续往下运行，一直运行到下面这行代码处为止，可以看到我们的bean已经初始化完了。

![image-20211019194200163](images\image-20211019194200163.png)

# 十、Spring IOC容器创建源码解析之完成BeanFactory的初始化创建工作，最终完成容器创建

程序停留在了下面这行代码处，此时，getBean方法就完全是执行完了，这样，我们单实例bean就被创建出来了

![image-20211019194421869](images\image-20211019194421869.png)

我bean创建出来之后，继续让程序往下运行，可以看到接下来就是通过以下for循环来将所有的bean都创建完。

![image-20211019194549329](images\image-20211019194549329.png)

让程序继续往下运行，直至运行到下面这行代码处为止。

![image-20211019194704967](images\image-20211019194704967.png)

可以看到，这儿是来遍历所有的bean，并来判断遍历出来的每一个bean是否实现了SmartInitializingSingleton接口的，所有的bean都利用getBean方法创建完成以后，接下来要做的事情就是检查所有的bean中是否有实现SmartInitializingSingleton接口的，如果有的话，那么便会来执行该接口中的afterSingletonsInstantiated方法

续让程序往下运行，直至执行完整个for循环，。当程序运行至下面这行代码处时，我们发现`finishBeanFactoryInitialization(beanFactory)`这行代码总算是执行完了。

此时，程序来到了Spring IOC容器创建的最后一步了，即完成BeanFactory的初始化创建工作。接下来，我们就看看finishRefresh方法里面都做了些啥事。

## 完成BeanFactory的初始化创建工作

一旦finishRefresh方法执行完，就意味着完成了BeanFactory的初始化创建工作，我们Spring IOC容器就创建完成了。

![image-20211019195630956](images\image-20211019195630956.png)

## 初始化和生命周期有关的后置处理器

从上图中可以知道，在initLifecycleProcessor方法里面一开始就是来获取BeanFactory的，而这个BeanFactory，我们之前早就准备好了

让程序继续往下运行，会发现有一个判断，即判断BeanFactory中是否有一个id为lifecycleProcessor的组件。

若有，则赋值给`this.lifecycleProcessor`

![image-20211019195914505](images\image-20211019195914505.png)

首先默认会从BeanFactory中寻找LifecycleProcessor这种类型的组件，即生命周期组件。

如下图所示，发现它是一个接口

![image-20211019200016993](images\image-20211019200016993.png)

可以看到该接口中还定义了两个方法，一个是onRefresh方法，一个是onClose方法，它俩能够在BeanFactory的生命周期期间进行回调

如此一来，我们就可以自己来编写LifecycleProcessor接口的一个实现类了，该实现类的作用就是可以在BeanFactory的生命周期期间进行拦截，即在BeanFactory刷新完成以及关闭的时候，回调其里面的onRefresh和onClose这俩方法。

当程序继续往下运行时，很显然，它并不会进入到if判断语句中，而是来到了下面的else分支语句中，这是因为容器在刚开始创建的时候，肯定是还没有生命周期组件的。

如果没有的话，那么Spring自己会创建一个DefaultLifecycleProcessor类型的对象，即默认的生命周期组件。

然后，把创建好的DefaultLifecycleProcessor类型的组件注册到容器中，所执行的是下面这行代码。

![image-20211019200152527](images\image-20211019200152527.png)

也就是说，容器中会有一个默认的生命周期组件。这样，我们以后其他组件想要使用生命周期组件，直接自动注入这个生命周期组件即可。

最后，让程序继续往下运行，直至运行到下面这行代码处为止。

![image-20211019200241239](images\image-20211019200241239.png)

可以看到，这儿会拿到生命周期组件，然后再回调其onRefresh方法。

## 回调生命周期处理器的onRefresh方法

当程序运行到`getLifecycleProcessor().onRefresh();`这行代码处时，会先拿到我们前面定义的生命周期处理器（即监听BeanFactory生命周期的处理器），然后再回调其onRefresh方法，也就是容器刷新完成的方法。

# 十一、Spring IOC容器创建源码解析之Spring IOC容器创建源码总结

首先，我们得需要掌握Spring中的一些核心思想，我们所要掌握的第一个核心思想就是，**Spring IOC容器在启动的时候，会先保存所有注册进来的bean的定义信息，将来，BeanFactory就会按照这些bean的定义信息来为我们创建对象**。

可以有如下两种方式来编写这些bean的定义信息：

​	1.使用XML配置文件的方式来注册bean。其实，这种方式说到底无非就是使用<bean>标签来向IOC容器中注册一个bean的定义信息，这种方式我们已经很熟悉了
​	2.使用@Service、@Component、@Bean等等注解来注册bean。其实，这种方式就是使用注解向IOC容器中注册一个bean的定义信息

我们所要掌握的第二个核心思想就是，当IOC容器中有保存一些bean的定义信息的时候，它便会在合适的时机来创建这些bean，而且主要有两个合适的时机，分别如下：

​	1. 就是在用到某个bean的时候。在统一创建所有剩下的单实例bean之前，有一些bean，比如像后置处理器啦等等这些组件，需要用到它的时候，都会利用getBean方法创建出来，创建好以后便会保存在容器中，以后我们就可以直接从容器中获取了

   2.统一创建所有剩下的单实例bean的时候。就是我们在跟踪Spring IOC容器创建过程的源码时所分析的一个步骤，即finishBeanFactoryInitialization(beanFactory)，这一步便是来初始化所有剩下的单实例bean的。
就是说，所有IOC容器中注册的单实例bean，如果还没创建对象，那么就在这个时机创建出来。

我每一个单实例bean在创建完成以后，都会使用各种各样的后置处理器进行处理，以此来增强这个bean的功能。举一个例子，使用@Autowired注解即可完成自动注入，这是因为Spring中有一个专门来处理@Autowired注解的后置处理器，即AutowiredAnnotationBeanPostProcessor。

