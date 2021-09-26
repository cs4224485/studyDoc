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

![image-20210926201637604](C:\Users\harry.cai\AppData\Roaming\Typora\typora-user-images\image-20210926201637604.png)

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

