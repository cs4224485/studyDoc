一、Spring Boot与缓存

## 1 JSR107

Java Caching定义了5个核心接口，分别是**CachingProvider**, **CacheManager**, **Cache**, **Entry** 和 **Expiry**。

•**CachingProvider**定义了创建、配置、获取、管理和控制多个**CacheManager**。一个应用可以在运行期访问多个CachingProvider。

•**CacheManager**定义了创建、配置、获取、管理和控制多个唯一命名的**Cache**，这些Cache存在于CacheManager的上下文中。一个CacheManager仅被一个CachingProvider所拥有。

•**Cache**是一个类似Map的数据结构并临时存储以Key为索引的值。一个Cache仅被一个CacheManager所拥有。

•**Entry**是一个存储在Cache中的key-value对。

•**Expiry** 每一个存储在Cache中的条目有一个定义的有效期。一旦超过这个时间，条目为过期的状态。一旦过期，条目将不可访问、更新和删除。缓存有效期可以通过ExpiryPolicy设置。



![image-20200510110437065](images\image-20200510110437065.png)

## 2 Spring缓存抽象

Spring从3.1开始定义了org.springframework.cache.Cache

和org.springframework.cache.CacheManager接口来统一不同的缓存技术；

并支持使用JCache（JSR-107）注解简化我们开发；

Cache接口为缓存的组件规范定义，包含缓存的各种操作集合；

Cache接口下Spring提供了各种xxxCache的实现；如RedisCache，EhCacheCache , ConcurrentMapCache等；

每次调用需要缓存功能的方法时，Spring会检查检查指定参数的指定的目标方法是否已经被调用过；如果有就直接从缓存中获取方法调用后的结果，如果没有就调用方法并缓存结果后返回给用户。下次调用直接从缓存中获取。

使用Spring缓存抽象时我们需要关注以下两点；

​	1、确定方法需要被缓存以及他们的缓存策略

​	2、从缓存中读取之前缓存存储的数据

![image-20200510110720572](\images\image-20200510110720572.png)

几个重要概念&缓存注解

| **Cache**          | 缓存接口，定义缓存操作。实现有：RedisCache、EhCacheCache、ConcurrentMapCache等 |
| ------------------ | ------------------------------------------------------------ |
| **CacheManager**   | **缓存管理器，管理各种缓存（Cache）组件**                    |
| **@Cacheable**     | **主要针对方法配置，能够根据方法的请求参数对其结果进行缓存** |
| **@CacheEvict**    | **清空缓存**                                                 |
| **@CachePut**      | **保证方法被调用，又希望结果被缓存。**                       |
| **@EnableCaching** | **开启基于注解的缓存**                                       |
| **keyGenerator**   | **缓存数据时**key生成策略                                    |
| **serialize**      | **缓存数据时**value序列化策略                                |

![image-20200510110720572](\images\capture_20200510111050851.bmp)

**Cache** **SpEL** **available metadata**

| **名字**        | **位置**           | **描述**                                                     | **示例**             |
| --------------- | ------------------ | ------------------------------------------------------------ | -------------------- |
| methodName      | root object        | 当前被调用的方法名                                           | #root.methodName     |
| method          | root object        | 当前被调用的方法                                             | #root.method.name    |
| target          | root object        | 当前被调用的目标对象                                         | #root.target         |
| targetClass     | root object        | 当前被调用的目标对象类                                       | #root.targetClass    |
| args            | root object        | 当前被调用的方法的参数列表                                   | #root.args[0]        |
| caches          | root object        | 当前方法调用使用的缓存列表（如@Cacheable(value={"cache1",  "cache2"})），则有两个cache | #root.caches[0].name |
| *argument name* | evaluation context | 方法参数的名字. 可以直接 #参数名 ，也可以使用 #p0或#a0 的形式，0代表参数的索引； | #iban 、 #a0 、 #p0  |
| result          | evaluation context | 方法执行后的返回值（仅当方法执行之后的判断有效，如‘unless’，’cache put’的表达式 ’cache evict’的表达式beforeInvocation=false） | #result              |

## 3 搭建缓存环境

Controller：

```java
@Controller
public class DeptController {

    @Autowired
    DeptService deptService;

    @GetMapping("/dept/{id}")
    public Department getDept(@PathVariable("id") Integer id){
        return deptService.getDeptById(id);
    }
}
```

```java
public class EmployeeController {

    @Autowired
    EmployeeService employeeService;

    @GetMapping("/emp/{id}")
    public Employee getEmployee(@PathVariable("id") Integer id){
        Employee employee = employeeService.getEmp(id);
        return employee;
    }

    @GetMapping("/emp")
    public Employee update(Employee employee){
        Employee emp = employeeService.updateEmp(employee);

        return emp;
    }

    @GetMapping("/delemp")
    public String deleteEmp(Integer id){
        employeeService.deleteEmp(id);
        return "success";
    }

    @GetMapping("/emp/lastname/{lastName}")
    public Employee getEmpByLastName(@PathVariable("lastName") String lastName){
        return employeeService.getEmpByLastName(lastName);
}
```

Mapper：

```java
@Mapper
public interface DepartmentMapper {
    @Select("SELECT * FROM department WHERE id = #{id} ")
    Department getDeptById(Integer id);
}
```

```java
public interface EmployeeMapper {
    @Select("SELECT * FROM employee WHERE id = #{id}")
    public Employee getEmpById(Integer id);

    @Update("UPDATE employee SET lastName=#{lastName},email=#{email},gender=#{gender},d_id=#{dId} WHERE id=#{id}")
    public void updateEmp(Employee employee);

    @Delete("DELETE FROM employee WHERE id=#{id}")
    public void deleteEmpById(Integer id);

    @Insert("INSERT INTO employee(lastName,email,gender,d_id) VALUES(#{lastName},#{email},#{gender},#{dId})")
    public void insertEmployee(Employee employee);

    @Select("SELECT * FROM employee WHERE lastName = #{lastName}")
    Employee getEmpByLastName(String lastName);
}
```

Service:

```java
@Service
public class EmployeeService {
    @Autowired
    EmployeeMapper employeeMapper;

    public Employee getEmp(Integer id){
        System.out.println("查询"+id+"号员工");
        Employee emp = employeeMapper.getEmpById(id);
        return emp;
    }

    public Employee updateEmp(Employee employee){
        System.out.println("updateEmp:"+employee);
        employeeMapper.updateEmp(employee);
        return employee;
    }
    
    public void deleteEmp(Integer id){
        System.out.println("deleteEmp:"+id);
        //employeeMapper.deleteEmpById(id);
        int i = 10/0;
    }

    public Employee getEmpByLastName(String lastName){
        return employeeMapper.getEmpByLastName(lastName);
    }


}
```

```java
@SpringBootApplication
@EnableCaching
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

}
```

## 4 @Cacheable注解

### (1) 使用方式

cacheNames/value：指定缓存组件的名字;将方法的返回结果放在哪个缓存中，是数组的方式，可以指定多个缓存；

key：缓存数据使用的key；可以用它来指定。默认是使用方法参数的值  1-方法的返回值
                   编写SpEL； #i d;参数id的值   #a0  #p0  #root.args[0]
                   getEmp[2]

keyGenerator：key的生成器；可以自己指定key的生成器的组件id
key/keyGenerator：二选一使用;
cacheManager：指定缓存管理器；或者cacheResolver指定获取解析器
condition：指定符合条件的情况下才缓存；
     condition = "#id>0"
     condition = "#a0>1"：第一个参数的值》1的时候才进行缓存

unless:否定缓存；当unless指定的条件为true，方法的返回值就不会被缓存；可以获取到结果进行判断

​    unless = "#result == null"

​    unless = "#a0==2":如果第一个参数的值是2，结果不缓存；

sync：是否使用异步模式

```java
@Cacheable(value = {"emp"}, key = "#id")
public Employee getEmp(Integer id){
    System.out.println("查询"+id+"号员工");
    Employee emp = employeeMapper.getEmpById(id);
    return emp;
}
```

使用自定义KeyGenerator

```java
@Configuration
public class MyCacheConfig {
    @Bean("myKeyGenerator")
    public KeyGenerator keyGenerator(){
        return new KeyGenerator() {
            @Override
            public Object generate(Object o, Method method, Object... objects) {
                return method.getName() + "[" + Arrays.asList(objects).toString()+"]";
            }
        };
    }
}
```

```java
@Cacheable(value = {"emp"}, key = "myKeyGenerator")
public Employee getEmp(Integer id){
    System.out.println("查询"+id+"号员工");
    Employee emp = employeeMapper.getEmpById(id);
    return emp;
}
```

### (2)原理

将方法的运行结果进行缓存；以后再要相同的数据，直接从缓存中获取，不用调用方法；

CacheManager管理多个Cache组件的，对缓存的真正CRUD操作在Cache组件中，每一个缓存组件有自己唯一一个名字；

1、自动配置类；CacheAutoConfiguration

2、缓存的配置类

```java
 *   org.springframework.boot.autoconfigure.cache.GenericCacheConfiguration
 *   org.springframework.boot.autoconfigure.cache.JCacheCacheConfiguration
 *   org.springframework.boot.autoconfigure.cache.EhCacheCacheConfiguration
 *   org.springframework.boot.autoconfigure.cache.HazelcastCacheConfiguration
 *   org.springframework.boot.autoconfigure.cache.InfinispanCacheConfiguration
 *   org.springframework.boot.autoconfigure.cache.CouchbaseCacheConfiguration
 *   org.springframework.boot.autoconfigure.cache.RedisCacheConfiguration
 *   org.springframework.boot.autoconfigure.cache.CaffeineCacheConfiguration
 *   org.springframework.boot.autoconfigure.cache.GuavaCacheConfiguration
 *   org.springframework.boot.autoconfigure.cache.SimpleCacheConfiguration【默认】
 *   org.springframework.boot.autoconfigure.cache.NoOpCacheConfiguration
```
3、哪个配置类默认生效：SimpleCacheConfiguration；

4、给容器中注册了一个CacheManager：ConcurrentMapCacheManager

5、可以获取和创建ConcurrentMapCache类型的缓存组件；他的作用将数据保存在ConcurrentMap中；

运行流程：

    1、方法运行之前，先去查询Cache（缓存组件），按照cacheNames指定的名字获取；
      （CacheManager先获取相应的缓存），第一次获取缓存如果没有Cache组件会自动创建。
    2、去Cache中查找缓存的内容，使用一个key，默认就是方法的参数；
       key是按照某种策略生成的；默认是使用keyGenerator生成的，默认使用SimpleKeyGenerator生成key；
               SimpleKeyGenerator生成key的默认策略；
                      如果没有参数；  key=new SimpleKey()；
                      如果有一个参数：key=参数的值
                      如果有多个参数：key=new SimpleKey(params)；
    3、没有查到缓存就调用目标方法；
    4、将目标方法返回的结果，放进缓存中
     
    @Cacheable标注的方法执行之前先来检查缓存中有没有这个数据，默认按照参数的值作为key
    如果没有就运行方法并将结果放入缓存；以后再来调用就可以直接使用缓存中的数据

核心

 1）、使用CacheManager【ConcurrentMapCacheManager】按照名字得到Cache【ConcurrentMapCache】组件
 2）、key使用keyGenerator生成的，默认是SimpleKeyGenerator

## 5 @CachePut

@CachePut：既调用方法，又更新缓存数据；同步更新缓存
     修改了数据库的某个数据，同时更新缓存；
     运行时机：
       1、先调用目标方法
       2、将目标方法的结果缓存起来
      测试步骤：
       1、查询1号员工；查到的结果会放在缓存中；
               key：1  value：lastName：张三
       2、以后查询还是之前的结果
       3、更新1号员工；【lastName:zhangsan；gender:0】
               将方法的返回值也放进缓存了；
               key：传入的employee对象  值：返回的employee对象；
       4、查询1号员工？
           应该是更新后的员工；
               key = "#employee.id":使用传入的参数的员工id；
               key = "#result.id"：使用返回后的id
               @Cacheable的key是不能用#result
           为什么是没更新前的？【1号员工没有在缓存中更新】

```java
@CachePut(/*value = "emp",*/key = "#result.id")
public Employee updateEmp(Employee employee){
    System.out.println("updateEmp:"+employee);
    employeeMapper.updateEmp(employee);
    return employee;
}
```
## 6 @CacheEvict：缓存清除

key：指定要清除的数据
       allEntries = true：指定清除这个缓存中所有的数据
       beforeInvocation = false：缓存的清除是否在方法之前执行
           默认代表缓存清除操作是在方法执行之后执行;如果出现异常缓存就不会清除
       beforeInvocation = true：
           代表清除缓存操作是在方法运行之前执行，无论方法是否出现异常，缓存都清除

```java
@CacheEvict(value="emp",beforeInvocation = true/*key = "#id",*/)
public void deleteEmp(Integer id){
    System.out.println("deleteEmp:"+id);
    //employeeMapper.deleteEmpById(id);
    int i = 10/0;
}
```
@Caching 定义复杂的缓存规则

```java
@Caching(
     cacheable = {
         @Cacheable(/*value="emp",*/key = "#lastName")
     },
     put = {
         @CachePut(/*value="emp",*/key = "#result.id"),
         @CachePut(/*value="emp",*/key = "#result.email")
     }
)
public Employee getEmpByLastName(String lastName){
    return employeeMapper.getEmpByLastName(lastName);
}
```
```java
@CacheConfig(cacheNames="emp"/*,cacheManager = "employeeCacheManager"*/) //抽取缓存的公共配置
```

## 7 使用Redis作为缓存

引入redis启动配置

```xml
	<dependency>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-data-redis</artifactId>
	</dependency>
```
Redis配置

```properties
spring.redis.host=192.168.0.208
```

使用RedisTemplate

```java
@Autowired
RedisTemplate redisTemplate; //操作k-v都是字符串的

@Autowired
StringRedisTemplate stringRedisTemplate; //k-v都是对象的

/**
 *Reis常见的五大数据类型
 * String(字符串),List(列表),Set(集合),Hash(散列),ZSet(有序集合)
 * stringRedisTemplate.opsForValue()[String（字符串）]
 * StringRedisTemplate.opsForList()[List]
 * StringRedisTemplate.opsForSet()[Set]
 * StringRedisTemplate.opsForHash()[Hash]
 * StringRedisTemplate.opsForZSet()[ZSet]
 */
```

配置自定义的RedisTemplate

```java
@Configuration
public class MyRedisConfig {
    @Bean
    public RedisTemplate<Object, Employee> empRedisTemplate(RedisConnectionFactory redisConnectionFactory){
        RedisTemplate<Object, Employee> redisTemplate = new RedisTemplate<>();
        redisTemplate.setConnectionFactory(redisConnectionFactory);
        // 序列化成jason数据
        Jackson2JsonRedisSerializer<Employee> ser = new Jackson2JsonRedisSerializer<Employee>(Employee.class);
        redisTemplate.setDefaultSerializer(ser);
        return redisTemplate;
    }

    @Bean
    public RedisTemplate<Object, Department> deptRedisTemplate(
            RedisConnectionFactory redisConnectionFactory)
            throws UnknownHostException {
        RedisTemplate<Object, Department> template = new RedisTemplate<Object, Department>();
        template.setConnectionFactory(redisConnectionFactory);
        Jackson2JsonRedisSerializer<Department> ser = new Jackson2JsonRedisSerializer<Department>(Department.class);
        template.setDefaultSerializer(ser);
        return template;
    }
}
```

自定义CacheManager

springboot2.x的cacheManager

```java
//CacheManagerCustomizers可以来定制缓存的一些规则
@Primary  //将某个缓存管理器作为默认的
@Bean
public RedisCacheManager myCacheManager(RedisConnectionFactory redisConnectionFactory) {
    RedisCacheWriter redisCacheWriter = RedisCacheWriter.nonLockingRedisCacheWriter(redisConnectionFactory);
    RedisSerializer<String> redisSerializer = new StringRedisSerializer();
    Jackson2JsonRedisSerializer jackson2JsonRedisSerializer = new Jackson2JsonRedisSerializer(Object.class);

    //解决查询缓存转换异常的问题
    ObjectMapper om = new ObjectMapper();
    om.setVisibility(PropertyAccessor.ALL, JsonAutoDetect.Visibility.ANY);
    om.enableDefaultTyping(ObjectMapper.DefaultTyping.NON_FINAL);
    jackson2JsonRedisSerializer.setObjectMapper(om);

    // 默认配置，过期时间指定是30分钟
    RedisCacheConfiguration defaultCacheConfig = RedisCacheConfiguration.defaultCacheConfig();
    defaultCacheConfig.entryTtl(Duration.ofMinutes(30));


    // 配置序列化（解决乱码的问题）
    RedisCacheConfiguration config = RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofHours(1))
            .serializeKeysWith(RedisSerializationContext.SerializationPair.fromSerializer(redisSerializer))
            .serializeValuesWith(RedisSerializationContext.SerializationPair.fromSerializer(jackson2JsonRedisSerializer));
    Map<String, RedisCacheConfiguration> redisCacheConfigurationMap = new HashMap<>();
    RedisCacheManager cacheManager = RedisCacheManager.builder(redisConnectionFactory)
            .cacheDefaults(config)
            .build();

    return cacheManager;
}
```

springboot1.x版本

```java
@Bean
public RedisCacheManager deptCacheManager(RedisTemplate<Object, Department> deptRedisTemplate){
    RedisCacheManager cacheManager = new RedisCacheManager(deptRedisTemplate);
    //key多了一个前缀

    //使用前缀，默认会将CacheName作为key的前缀
    cacheManager.setUsePrefix(true);

    return cacheManager;
}
```
使用制定CacheManager

```java
@Service
public class DeptService {
    @Autowired
    DepartmentMapper departmentMapper;


    /**
     *  缓存的数据能存入redis；
     *  第二次从缓存中查询就不能反序列化回来；
     *  存的是dept的json数据;CacheManager默认使用RedisTemplate<Object, Employee>操作Redis
     *
     *
     * @param id
     * @return
     */
    @Cacheable(cacheNames = "dept",cacheManager = "deptCacheManager")
    public Department getDeptById(Integer id){
        System.out.println("查询部门"+id);
        Department department = departmentMapper.getDeptById(id);
        return department;
    }
```

使用缓存管理器得到缓存，进行api调用

```java
public Department getDeptById(Integer id){
    System.out.println("查询部门"+id);
    Department department = departmentMapper.getDeptById(id);

    //获取某个缓存
    Cache dept = deptCacheManager.getCache("dept");
    dept.put("dept:1",department);

    return department;
}
```

# 二、Spring Boot与消息队列

## 1、概述

大多应用中，可通过消息服务中间件来提升系统异步通信、扩展解耦能力

消息服务中两个重要概念：

​    消息代理（message broker）和目的地（destination）

当消息发送者发送消息以后，将由消息代理接管，消息代理保证消息传递到指定目的地。

消息队列主要有两种形式的目的地

​	队列（queue）：点对点消息通信（point-to-point）

​	主题（topic）：发布（publish）/订阅（subscribe）消息通信

**异步处理**

![image-20200512105219224](\images\image-20200512105219224.png)

**应用解耦**

![image-20200512105324541](images\image-20200512105324541.png)

**流量削峰**

![image-20200512105410270](images\image-20200512105410270.png)

### 点对点式

​		– 消息发送者发送消息，消息代理将其放入一个队列中，消息接收者从队列中获取消息内容，消息读取后被移出队列

​		– 消息只有唯一的发送者和接受者，但并不是说只能有一个接收者

### 发布订阅式

​		– 发送者（发布者）发送消息到主题，多个接收者（订阅者）监听（订阅）这个主题，那么就会在消息到达时同时收到消息

### JMS（Java Message Service）JAVA消息服务

​		– 基于JVM消息代理的规范。ActiveMQ、HornetMQ是JMS实现

### AMQP（Advanced Message Queuing Protocol）

​		– 高级消息队列协议，也是一个消息代理的规范，兼容JMS

​		– RabbitMQ是AMQP的实现

### Spring支持

​		–spring-jms提供了对JMS的支持

​		–spring-rabbit提供了对AMQP的支持

​		–需要ConnectionFactory的实现来连接消息代理

​		–提供JmsTemplate、RabbitTemplate来发送消息

​		–@JmsListener（JMS）、@RabbitListener（AMQP）注解在方法上监听消息代理发布的消息

​		–@EnableJms、@EnableRabbit开启支持

### Spring Boot自动配置

​		– JmsAutoConfiguration

​		– RabbitAutoConfiguration

## 2、RabbitMQ简介

RabbitMQ是一个由erlang开发的AMQP(Advanved Message Queue Protocol)的开源实现。

### 核心概念

**Message**

消息，消息是不具名的，它由消息头和消息体组成。消息体是不透明的，而消息头则由一系列的可选属性组成，这些属性包括routing-key（路由键）、priority（相对于其他消息的优先权）、delivery-mode（指出该消息可能需要持久性存储）等。

**Publisher**

消息的生产者，也是一个向交换器发布消息的客户端应用程序。

**Exchange**

交换器，用来接收生产者发送的消息并将这些消息路由给服务器中的队列。

Exchange有4种类型：direct(默认)，fanout, topic, 和headers，不同类型的Exchange转发消息的策略有所区别

**Queue**

消息队列，用来保存消息直到发送给消费者。它是消息的容器，也是消息的终点。一个消息可投入一个或多个队列。消息一直在队列里面，等待消费者连接到这个队列将其取走。

**Binding**

绑定，用于消息队列和交换器之间的关联。一个绑定就是基于路由键将交换器和消息队列连接起来的路由规则，所以可以将交换器理解成一个由绑定构成的路由表。

Exchange 和Queue的绑定可以是多对多的关系。

**Connection**

网络连接，比如一个TCP连接。

**Channel**

信道，多路复用连接中的一条独立的双向数据流通道。信道是建立在真实的TCP连接内的虚拟连接，AMQP 命令都是通过信道发出去的，不管是发布消息、订阅队列还是接收消息，这些动作都是通过信道完成。因为对于操作系统来说建立和销毁 TCP 都是非常昂贵的开销，所以引入了信道的概念，以复用一条 TCP 连接。

**Consumer**

消息的消费者，表示一个从消息队列中取得消息的客户端应用程序。

**Virtual Host**

虚拟主机，表示一批交换器、消息队列和相关对象。虚拟主机是共享相同的身份认证和加密环境的独立服务器域。每个 vhost 本质上就是一个 mini 版的 RabbitMQ 服务器，拥有自己的队列、交换器、绑定和权限机制。vhost 是 AMQP 概念的基础，必须在连接时指定，RabbitMQ 默认的 vhost 是 / 。

**Broker**

表示消息队列服务器实体

![image-20200512141502272](\images\image-20200512141502272.png)

## 3、RabbitMQ运行机制

### AMQP 中的消息路由

AMQP 中消息的路由过程和 Java 开发者熟悉的 JMS 存在一些差别，AMQP 中增加了 **Exchange** 和 **Binding** 的角色。生产者把消息发布到 Exchange 上，消息最终到达队列并被消费者接收，而 Binding 决定交换器的消息应该发送到那个队列。

### Exchange 类型

Exchange分发消息时根据类型的不同分发策略有区别，目前共四种类型：direct、fanout、topic、headers 。headers 匹配 AMQP 消息的 header 而不是路由键， headers 交换器和 direct 交换器完全一致，但性能差很多，目前几乎用不到了，所以直接看另外三种类型：

> 消息中的路由键（routing key）如果和 Binding 中的 binding key 一致， 交换器就将消息发到对应的队列中。路由键与队列名完全匹配，如果一个队列绑定到交换机要求路由键为“dog”，则只转发 routing key 标记为“dog”的消息，不会转发“dog.puppy”，也不会转发“dog.guard”等等。它是完全匹配、单播的模式。

> 每个发到 fanout 类型交换器的消息都会分到所有绑定的队列上去。fanout 交换器不处理路由键，只是简单的将队列绑定到交换器上，每个发送到交换器的消息都会被转发到与该交换器绑定的所有队列上。很像子网广播，每台子网内的主机都获得了一份复制的消息。fanout 类型转发消息是最快的。

> topic 交换器通过模式匹配分配消息的路由键属性，将路由键和某个模式进行匹配，此时队列需要绑定到一个模式上。它将路由键和绑定键的字符串切分成单词，这些**单词之间用点隔开**。它同样也会识别两个通配符：符号“#”和符号“**”**。**#**匹配**0**个或多个单词**，****匹配一个单词

## 4、RabbitMQ测试

从docker中拉取RabbitMQ的镜像并运行镜像

```shell
[root@localhost docker]# docker pull rabbitmq:management
```

```shell
[root@localhost docker]# docker run -d -p 5672:5672 -p 15672:15672 --name myrabb  
```

创建队列

![image-20200512145557292](images\image-20200512145557292.png)

创建Exchange

![image-20200512145753723](images\image-20200512145753723.png)

将Exchange与队列进行绑定

![image-20200512150137876](images\image-20200512150137876.png)

在Exchange中发送消息

![image-20200512150531375](images\image-20200512150531375.png)

队列中获取消息

![image-20200512150625500](\images\image-20200512150625500.png)

类型为fandout类型的Exchange发现消息所以的队列都能够收到

![image-20200512150804614](\images\image-20200512150804614.png)

## 5、SpringBoot整合RabbitMQ

引入RabbitMQ

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-amqp</artifactId>
</dependency>
```

Rabbit自动配置类

```java
@Configuration
@ConditionalOnClass({RabbitTemplate.class, Channel.class})
@EnableConfigurationProperties({RabbitProperties.class})
@Import({RabbitAnnotationDrivenConfiguration.class})
public class RabbitAutoConfiguration {
    public RabbitAutoConfiguration() {
    }
```

自动配置工厂ConnectionFactory

```java
@Configuration
@Import({RabbitAutoConfiguration.RabbitConnectionFactoryCreator.class})
protected static class RabbitTemplateConfiguration {
    private final ObjectProvider<MessageConverter> messageConverter;
    private final RabbitProperties properties;

    public RabbitTemplateConfiguration(ObjectProvider<MessageConverter> messageConverter, RabbitProperties properties) {
        this.messageConverter = messageConverter;
        this.properties = properties;
    }
```

RabbitProperties封装了 RabbitMQ的配置

配置Rabbit

```properties
spring.rabbitmq.host=192.168.0.128
spring.rabbitmq.username=guest
spring.activemq.password=guest
```

RabbitTemlate:给RabbitMQ发送和接受消息

```java
@Bean
@ConditionalOnSingleCandidate(RabbitTemplate.class)
public RabbitMessagingTemplate rabbitMessagingTemplate(RabbitTemplate rabbitTemplate) {
    return new RabbitMessagingTemplate(rabbitTemplate);
}
```

测试点对点消息的发送

```java
@SpringBootTest
class ApplicationTests {

    @Autowired
    RabbitTemplate rabbitTemplate;

    @Test
    void contextLoads() {
        // 单播(点对点)
        //Message需要自己构造一个；定义消息体内容和消息头
        //rabbitTemplate.send(exchange, routeKey, message)

        //object默认当成消息体只需传入要发送的对象，自动序列化发送给rabbitmq
        //rabbitTemplate.convertAndSend(exchange, routeKey,object)
         Map<String,Object> map = new HashMap<>();
         map.put("msg", "这是第一个消息");
         map.put("data", Arrays.asList("helloworld", 123, true));
         rabbitTemplate.convertAndSend("harry.dircect", "harry.news", map);

    }

}
```

接收数据

```java
@Test
public void receive(){
    // 接受数据
    Object o = rabbitTemplate.receiveAndConvert("harry.news");
    System.out.println(o.getClass());
    System.out.println(o);
}
```

自定消息的转换器，实现转换成Jason格式

```java
import org.springframework.context.annotation.Configuration;

@Configuration
public class MyAMQPConfig {
    @Bean
    public MessageConverter messageConverter(){
        return new Jackson2JsonMessageConverter();
    }
}
```

广播发送一个对象

```java
/**
 * 广播
 */
@Test
public void sendMsg(){
	rabbitTemplate.convertAndSend("exchange.fanout","",new Book("红楼梦","曹雪芹"));
}
```
使用@RabbitListener来监听消息，当监听到消息注解的方法会执行

```java
@Service
public class BookService {
    @RabbitListener(queues = "harry.news")
    public void receive(Book book){
        System.out.println("收到消息"+ book);

    }
    @RabbitListener(queues = "harry")
    public void receive02(Message message){
        System.out.println(message.getBody());
        System.out.println(message.getMessageProperties());

    }
}
```

注意使用监听需要在启动配置中添加@EnableRabbit

```java
@SpringBootApplication
@EnableRabbit
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

amqpAdmin创建Exchange或队列等等

```java
@Test
public void createExchange(){

    amqpAdmin.declareExchange(new DirectExchange("amqpadmin.exchange"));
    System.out.println("创建完成");

    amqpAdmin.declareQueue(new Queue("amqpadmin.queue",true));
    //创建绑定规则

    amqpAdmin.declareBinding(new Binding("amqpadmin.queue",      	 Binding.DestinationType.QUEUE,"amqpadmin.exchange","amqp.haha",null));

}
```

# 三、Spring Boot与检索

Elasticsearch是一个分布式搜索服务，提供Restful API，底层基于Lucene，采用多shard（分片）的方式保证数据安全，并且提供自动resharding的功能，github等大型的站点也是采用了ElasticSearch作为其搜索服务，docker 运行Elasticsearch

```shell
[root@localhost docker]# docker pull  elasticsearch
[root@localhost docker]# docker run -e ES_JAVA_OPS="-Xms256m -Xmx256m" -d -p 9200:9200 -p 9300:9300 --name ES01 5acf0e8da90b
```

## 1、概念

以 员工文档的形式存储为例：一个文档代表一个员工数据。存储数据到 ElasticSearch 的行为叫做 *索引* ，但在索引一个文档之前，需要确定将文档存储在哪里。

一个 ElasticSearch 集群可以 包含多个 *索引* ，相应的每个索引可以包含多个 *类型* 。 这些不同的类型存储着多个 *文档* ，每个文档又有 多个 *属性* 。

类似关系：

​	–索引-数据库

​	–类型-表

​	–文档-表中的记录

​	–属性-列

![image-20200513100956764](\images\image-20200513100956764.png)

## 2、ElasticSearch的一些常用操作

### 新建和删除Index

新建 Index，可以直接向 Elastic 服务器发出 PUT 请求。下面的例子是新建一个名叫harry.cai的 Index。

![image-20200513160209532](\images\image-20200513160209532.png)

服务器返回一个 JSON 对象，里面的`acknowledged`字段表示操作成功。

```json
{
    "acknowledged": true,
    "shards_acknowledged": true,
    "index": "harry.cai"
}
```

删除只需要使用delete方式的请求即可

### 数据操作

向指定的 /Index/Type 发送 PUT 请求，就可以在 Index 里面新增一条记录。比如，向`/accounts/person`发送请求，就可以新增一条人员记录。

![image-20200513160658514](images\image-20200513160658514.png)

服务器返回的 JSON 对象，会给出 Index、Type、Id、Version 等信息。

```json
{
    "_index": "accounts",
    "_type": "person",
    "_id": "1",
    "_version": 1,
    "result": "created",
    "_shards": {
        "total": 2,
        "successful": 1,
        "failed": 0
    },
    "created": true
}
```

如果你仔细看，会发现请求路径是`/accounts/person/1`，最后的`1`是该条记录的 Id。它不一定是数字，任意字符串（比如`abc`）都可以。

新增记录的时候，也可以不指定 Id，这时要改成 POST 请求。

```bash
$ curl -X POST 'localhost:9200/accounts/person' -d '
{
  "user": "李四",
  "title": "工程师",
  "desc": "系统管理"
}'
```

上面代码中，向`/accounts/person`发出一个 POST 请求，添加一个记录。这时，服务器返回的 JSON 对象里面，`_id`字段就是一个随机字符串。

```json
{
  "_index":"accounts",
  "_type":"person",
  "_id":"AV3qGfrC6jMbsbXb6k1p",
  "_version":1,
  "result":"created",
  "_shards":{"total":2,"successful":1,"failed":0},
  "created":true
}
```

### 查看记录

向`/Index/Type/Id`发出 GET 请求，就可以查看这条记录。

```bash
[root@localhost ~]# curl '192.168.0.128:9200/accounts/person/1?pretty=true'
```

上面代码请求查看`/accounts/person/1`这条记录，URL 的参数`pretty=true`表示以易读的格式返回。

返回的数据中，`found`字段表示查询成功，`_source`字段返回原始记录。

```json
{
  "_index" : "accounts",
  "_type" : "person",
  "_id" : "1",
  "_version" : 1,
  "found" : true,
  "_source" : {
    "user" : "张三",
    "title" : "工程师",
    "desc" : "数据库管理"
  }
}

```

### 更新记录

更新记录就是使用 PUT 请求，重新发送一次数据。

```bash
$ curl -X PUT 'localhost:9200/accounts/person/1' -d '
{
    "user" : "张三",
    "title" : "工程师",
    "desc" : "数据库管理，软件开发"
}' 

{
  "_index":"accounts",
  "_type":"person",
  "_id":"1",
  "_version":2,
  "result":"updated",
  "_shards":{"total":2,"successful":1,"failed":0},
  "created":false
}
```

更多参考官方文档：https://www.elastic.co/guide/cn/elasticsearch/guide/current/foreword_id.html

## 3、整合ElasticSearch测试 

SpringBoot默认支持两种技术来和ES交互；

### (1) 使用Jest（默认不生效）

​	需要导入jest的工具包（io.searchbox.client.JestClient）

```xml
	<dependency>
		<groupId>io.searchbox</groupId>
		<artifactId>jest</artifactId>
		<version>5.3.3</version>
	</dependency>
```
配置

```properties
spring.elasticsearch.jest.uris=http://192.168.0.128:9200
```

在实体类的Id字段注解标注ES的ID值

```java
public class Article {

    @JestId
    private Integer id;
```

向Elasticsearch中添加值

```java
@SpringBootTest
class ApplicationTests {

    @Autowired
    JestClient jestClient;

    @Test
    void contextLoads() {
        // 1. 给Es索引中(保存)一个文档
        Article article = new Article();
        article.setId(2);
        article.setTitle("好消息2");
        article.setAuthor("王二");
        article.setContent("JAVA");
        // 构建一个索引功能
        Index index = new Index.Builder(article).index("harry").type("news").build();
        try {
            jestClient.execute(index);
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

}
```

测试搜索值

```java
// 测试搜索
@Test
public void search(){
    // 查询表达式
    String json ="{\n" +
            "    \"query\" : {\n" +
            "        \"match\" : {\n" +
            "            \"content\" : \"hello\"\n" +
            "        }\n" +
            "    }\n" +
            "}";
    //更多操作：https://github.com/searchbox-io/Jest/tree/master/jest
    //构建搜索功能
    Search search = new Search.Builder(json).addIndex("harry").addType("news").build();
    //执行
    try {
        SearchResult result = jestClient.execute(search);
        System.out.println(result.getJsonString());
        List<SearchResult.Hit<Article, Void>> hits = result.getHits(Article.class);
        for (SearchResult.Hit<Article, Void> hit : hits) {
            System.out.println(hit.source);
            System.out.println(hit.source.getAuthor());
        }
    } catch (IOException e) {
        e.printStackTrace();
    }
}
```

### (2)SpringData ElasticSearch【ES版本有可能不合适】

版本适配说明：https://github.com/spring-projects/spring-data-elasticsearch

如果版本不适配：2.4.6

​		1）、升级SpringBoot版本

​		2）、安装对应版本的ES

1）、Client 节点信息clusterNodes；clusterName

2）、ElasticsearchTemplate 操作es

3）、编写一个 ElasticsearchRepository 的子接口来操作ES；

两种用法：https://github.com/spring-projects/spring-data-elasticsearch

引入依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-elasticsearch</artifactId>
</dependency>
```

```properties
spring.data.elasticsearch.cluster-name=docker-cluster
spring.data.elasticsearch.cluster-nodes=192.168.0.128:9300
spring.data.elasticsearch.client.reactive.use-ssl=true
```

注意cluster-name要与es配置文件的cluster.name命名一致

```bash
[root@localhost ~]# cat elasticsearch.yml
cluster.name: "docker-cluster"
network.host: 0.0.0.0
```

写一个Repository接口

```java
import com.harry.springboot.bean.Book;
import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;

import java.util.List;

public interface BookRepository extends ElasticsearchRepository<Book,Integer> {
    //参照
    // https://docs.spring.io/spring-data/elasticsearch/docs/3.0.6.RELEASE/reference/html/
    public List<Book> findByBookNameLike(String bookName);
    
}
```

在实体类添加注解标清楚Index

```java
@Document(indexName = "harry",type = "book")
public class Book {
    private Integer id;
    private String bookName;
    private String author;
```

添加操作

```java
  @Test
  public void dataAdd(){
      Book book = new Book();
	  book.setId(1);
	  book.setBookName("西游记");
	  book.setAuthor("吴承恩");
	  bookRepository.index(book);

  }
```

测试搜索

```java
// 测试搜索
@Test
public void search(){
    for (Book book : bookRepository.findByBookNameLike("游")) {
        System.out.println(book);
    }
}
```

# 四、Spring Boot与任务2

## 1、异步任务

在Java应用中，绝大多数情况下都是通过同步的方式来实现交互处理的；但是在处理与第三方系统交互的时候，容易造成响应迟缓的情况，之前大部分都是使用多线程来完成此类任务，其实，在Spring 3.x之后，就已经内置了@Async来完美解决这个问题。

两个注解：

@EnableAysnc、@Aysnc

```java
@SpringBootApplication
@EnableAsync
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

}
```

在Service中定义一个异步方法

```java
@Service
public class AsyncService {
    //告诉Spring这是一个异步方法
    @Async
    public void hello(){
        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("处理数据中...");
    }
}
```

```java
@Controller
public class AsyncController {
    @Autowired
    AsyncService asyncService;

    @GetMapping("/hello")
    @ResponseBody
    public String hello(){
        asyncService.hello();
        return "success";
    }
}
```

## 2、定时任务 

项目开发中经常需要执行一些定时任务，比如需要在每天凌晨时候，分析一次前一天的日志信息。Spring为我们提供了异步执行任务调度的方式，提供TaskExecutor 、TaskScheduler 接口。

**两个注解：**@EnableScheduling、@Scheduled

**cron**表达式：

| **字段** | **允许值**             | **允许的特殊字符** |
| -------- | ---------------------- | ------------------ |
| 秒       | 0-59                   | , -  * /           |
| 分       | 0-59                   | , -  * /           |
| 小时     | 0-23                   | , -  * /           |
| 日期     | 1-31                   | , -  * ? / L W C   |
| 月份     | 1-12                   | , -  * /           |
| 星期     | 0-7或SUN-SAT  0,7是SUN | , -  * ? / L C #   |

| **特殊字符** | **代表含义**               |
| ------------ | -------------------------- |
| ,            | 枚举                       |
| -            | 区间                       |
| *            | 任意                       |
| /            | 步长                       |
| ?            | 日/星期冲突匹配            |
| L            | 最后                       |
| W            | 工作日                     |
| C            | 和calendar联系后计算过的值 |
| #            | 星期，4#2，第2个星期四     |

```java
@Service
public class ScheduledService {
    /**
     * second(秒), minute（分）, hour（时）, day of month（日）, month（月）, day of week（周几）.
     * 0 * * * * MON-FRI
     *  【0 0/5 14,18 * * ?】 每天14点整，和18点整，每隔5分钟执行一次
     *  【0 15 10 ? * 1-6】 每个月的周一至周六10:15分执行一次
     *  【0 0 2 ? * 6L】每个月的最后一个周六凌晨2点执行一次
     *  【0 0 2 LW * ?】每个月的最后一个工作日凌晨2点执行一次
     *  【0 0 2-4 ? * 1#1】每个月的第一个周一凌晨2点到4点期间，每个整点都执行一次；
     */
    // @Scheduled(cron = "0 * * * * MON-SAT")
    // @Scheduled(cron = "0,1,2,3,4 * * * * MON-SAT")
    // @Scheduled(cron = "0-4 * * * * MON-SAT")
    @Scheduled(cron = "0/4 * * * * MON-SAT") // 每4秒执行一次
    public void hello(){
        System.out.println("hello ......");
    }
}
```

## 3、邮件任务 

邮件发送需要引入spring-boot-starter-mail

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-mail</artifactId>
</dependency>
```

```java
public class Springboot04TaskApplicationTests {

    @Autowired
    JavaMailSenderImpl mailSender;

    @Test
    void contextLoads() {
        SimpleMailMessage message = new SimpleMailMessage();
        // 邮件设置
        message.setSubject("通知-今晚开会");
        message.setText("今晚7:30开会");

        message.setTo("caishuang1993@126.com");
        message.setFrom("414804000@qq.com");

        mailSender.send(message);
    }

    @Test
    public void test02() throws  Exception{
        //1、创建一个复杂的消息邮件
        MimeMessage mimeMessage = mailSender.createMimeMessage();
        MimeMessageHelper helper = new MimeMessageHelper(mimeMessage, true);

        //邮件设置
        helper.setSubject("通知-今晚开会");
        helper.setText("<b style='color:red'>今天 7:30 开会</b>",true);

        helper.setTo("17512080612@163.com");
        helper.setFrom("534096094@qq.com");

        //上传文件
        helper.addAttachment("1.jpg",new File("C:\\Users\\lfy\\Pictures\\Saved Pictures\\1.jpg"));
        helper.addAttachment("2.jpg",new File("C:\\Users\\lfy\\Pictures\\Saved Pictures\\2.jpg"));

        mailSender.send(mimeMessage);

    }

}
```

```properties
spring.mail.username=414804000@qq.com
spring.mail.password=ucxslfakpmlxcacg
spring.mail.host=smtp.qq.com
spring.mail.properties.mail.smtp.ssl.enable=true
```

# 五、Spring Boot与安全

## 1、SpringSecurity简介

Spring Security是针对Spring项目的安全框架，也是Spring Boot底层安全模块默认的技术选型。他可以实现强大的web安全控制。对于安全控制，我们仅需引入spring-boot-starter-security模块，进行少量的配置，即可实现强大的安全管理。

几个类：

WebSecurityConfigurerAdapter：自定义Security策略

AuthenticationManagerBuilder：自定义认证策略

@EnableWebSecurity：开启WebSecurity模式

应用程序的两个主要区域是“认证”和“授权”（或者访问控制）。这两个主要区域是Spring Security 的两个目标。

“认证”（Authentication），是建立一个他声明的主体的过程（一个“主体”一般是指用户，设备或一些可以在你的应用程序中执行动作的其他系统）。

“授权”（Authorization）指确定一个主体是否允许在你的应用程序执行一个动作的过程。为了抵达需要授权的店，主体的身份已经有认证过程建立。

这个概念是通用的而不只在Spring Security中。

## 2、SpringBoot整合SpringSecurity

导入依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
```

```xml
	<dependency>
		<groupId>org.thymeleaf.extras</groupId>
		<artifactId>thymeleaf-extras-springsecurity5</artifactId>
	</dependency>
```
```xml
<properties>
    <java.version>1.8</java.version>
    <thymeleaf.version>3.0.9.RELEASE</thymeleaf.version>
    <thymeleaf-layout-dialect.version>2.2.2</thymeleaf-layout-dialect.version>
    <thymeleaf-extras-springsecurity4.version>3.0.2.RELEASE</thymeleaf-extras-springsecurity4.version>
</properties>
```

### 登陆/注销

```java
@EnableWebSecurity
public class MySecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        //super.configure(http);
        //定制请求的授权规则
        http.authorizeRequests().antMatchers("/").permitAll()
                .antMatchers("/level1/**").hasRole("VIP1")
                .antMatchers("/level2/**").hasRole("VIP2")
                .antMatchers("/level3/**").hasRole("VIP3");

        //开启自动配置的登陆功能，效果，如果没有登陆，没有权限就会来到登陆页面
        http.formLogin().usernameParameter("user").passwordParameter("pwd")
                .loginPage("/userlogin");
        // 1. /login来登录页面
        // 2. 冲定向到/login?error表示登录失败
        // 3. 更多详细规定
        // 4. 默认post形式的/login代表处理登录
        // 5. 一旦定制loginPage，那么loginPage的post请求就是登录

        // 开启自动配置的注销功能
        http.logout().logoutSuccessUrl("/"); // 注销成功以后来到首页
        // 1. 访问 /logout 表示用户注销，清空session
        // 2. 注销成功会返回 /login?logout页面

        // 开启记住我功能
        http.rememberMe().rememberMeParameter("remember");
        //登陆成功以后，将cookie发给浏览器保存，以后访问页面带上这个cookie，只要通过检查就可以免登录
        //点击注销会删除cookie
    }
```

### 登录授权功能

使用springboot，权限管理使用spring security，使用内存用户验证，但无响应报错：

java.lang.IllegalArgumentException: There is no PasswordEncoder mapped for the id "null"

解决方法：
这是因为Spring boot 2.0.3引用的security 依赖是 spring security 5.X版本，此版本需要提供一个PasswordEncorder的实例，否则后台汇报错误：
java.lang.IllegalArgumentException: There is no PasswordEncoder mapped for the id "null"
并且页面毫无响应。
因此，需要创建PasswordEncorder的实现类。
MyPasswordEncoder.class:

```java
public class MyPasswordEncoder implements PasswordEncoder {
    @Override
    public String encode(CharSequence charSequence) {
        return charSequence.toString();
    }

    @Override
    public boolean matches(CharSequence charSequence, String s) {
        return s.equals(charSequence.toString());
    }
}
```

```java
//定义认证规则
@Override
protected void configure(AuthenticationManagerBuilder auth) throws Exception {
    //super.configure(auth);
    //这样，页面提交时候，密码以明文的方式进行匹配。
    auth.inMemoryAuthentication().passwordEncoder(new MyPasswordEncoder())
            .withUser("zhangsan").password("123456").roles("VIP1", "VIP2")
            .and()
            .withUser("lisi").password("123456").roles("VIP2", "VIP3")
            .and()
            .withUser("wangwu").password("123456").roles("VIP1", "VIP3");

}
```

### Thymeleaf提供的SpringSecurity标签支持

需要引入thymeleaf-extras-springsecurity4(SpringBoot2.x引入5)

sec:authentication=“name”获得当前用户的用户名

sec:authorize=“hasRole(‘ADMIN’)”当前用户必须拥有ADMIN权限时才会显示标签内容

```html
<h1 align="center">欢迎光临武林秘籍管理系统</h1>
<div sec:authorize="!isAuthenticated()">
   <h2 align="center">游客您好，如果想查看武林秘籍 <a th:href="@{/userlogin}">请登录</a></h2>
</div>
<div sec:authorize="isAuthenticated()">
   <h2><span sec:authentication="name"></span>，您好,您的角色有：
      <span sec:authentication="principal.authorities"></span></h2>
   <form th:action="@{/logout}" method="post">
      <input type="submit" value="注销"/>
   </form>
</div>

<hr>

<div sec:authorize="hasRole('VIP1')">
   <h3>普通武功秘籍</h3>
   <ul>
      <li><a th:href="@{/level1/1}">罗汉拳</a></li>
      <li><a th:href="@{/level1/2}">武当长拳</a></li>
      <li><a th:href="@{/level1/3}">全真剑法</a></li>
   </ul>

</div>

<div sec:authorize="hasRole('VIP2')">
   <h3>高级武功秘籍</h3>
   <ul>
      <li><a th:href="@{/level2/1}">太极拳</a></li>
      <li><a th:href="@{/level2/2}">七伤拳</a></li>
      <li><a th:href="@{/level2/3}">梯云纵</a></li>
   </ul>

</div>

<div sec:authorize="hasRole('VIP3')">
   <h3>绝世武功秘籍</h3>
   <ul>
      <li><a th:href="@{/level3/1}">葵花宝典</a></li>
      <li><a th:href="@{/level3/2}">龟派气功</a></li>
      <li><a th:href="@{/level3/3}">独孤九剑</a></li>
   </ul>
</div>
```

### remember me

表单添加remember-me的checkbox

配置启用remember-me功能

```html
<h1 align="center">欢迎登陆武林秘籍管理系统</h1>
<hr>
<div align="center">
   <form th:action="@{/userlogin}" method="post">
      用户名:<input name="user"/><br>
      密码:<input name="pwd"><br/>
      <input type="checkbox" name="remeber"> 记住我<br/>
      <input type="submit" value="登陆">
   </form>
</div>
```

```java
    // 开启记住我功能
    http.rememberMe().rememberMeParameter("remember");
```
# 六、Spring Boot与分布式

## 1、Zookeeper和Dubbo

**ZooKeeper**

ZooKeeper 是一个分布式的，开放源码的分布式应用程序协调服务。它是一个为分布式应用提供一致性服务的软件，提供的功能包括：配置维护、域名服务、分布式同步、组服务等。

**Dubbo**

Dubbo是Alibaba开源的分布式服务框架，它最大的特点是按照分层的方式来架构，使用这种方式可以使各个层之间解耦合（或者最大限度地松耦合）。从服务模型的角度来看，Dubbo采用的是一种非常简单的模型，要么是提供方提供服务，要么是消费方消费服务，所以基于这一点可以抽象出服务提供方（Provider）和服务消费方（Consumer）两个角色

Docker下载Zookeepr镜像

```bash
[root@localhost ~]# docker pull registry.docker-cn.com/library/zookeeper
```

运行zookeepr

```bash
[root@localhost ~]# docker run --name zk02 -p 2181:2181  --restart always -d zookeeper:latest
```

创建一个Provider整合Dubbo

```xml
<dependency>
    <groupId>org.apache.dubbo</groupId>
    <artifactId>dubbo-spring-boot-starter</artifactId>
    <version>2.7.6</version>
</dependency>
```

如果启动报这个异常：java.lang.NoClassDefFoundError: org/apache/curator/RetryPolicy

还需引入以下依赖

```xml
<dependency>
    <groupId>org.apache.curator</groupId>
    <artifactId>curator-framework</artifactId>
    <version>2.8.0</version>
</dependency>
<dependency>
    <groupId>org.apache.curator</groupId>
    <artifactId>curator-recipes</artifactId>
    <version>2.8.0</version>
</dependency>
```

Dubbo Provider的相关配置

```properties
# dubbo中的服务名称
dubbo.application.name=provider-ticket
# zookeeper注册中心的地址
dubbo.registry.address=zookeeper://192.168.0.129:2181
# dubbo的通讯协议名称
dubbo.protocol.name=dubbo
# dubbo的服务的扫描路径
dubbo.scan.base-packages=com.harry.springboot.service
# 消费端超时时间
dubbo.consumer.timeout=600000
dubbo.consumer.check=false
```

service

```java
public interface TicketService {
    public String getTicket();
}
```

```java
@Component
@Service
public class TicketServiceImpl implements TicketService{
    @Override
    public String getTicket() {
        return "《厉害了，我的国》";
    }
}
```

消费者端：

```properties
server.port=8081
dubbo.application.name=consumer-user
dubbo.registry.address=zookeeper://192.168.0.128:2181
```

```java
@Service
public class UserService {

    @Reference
    TicketService ticketService;

    public void hello(){
        String ticket = ticketService.getTicket();
        System.out.println("买到票了："+ticket);
    }

}
```

```java
class ApplicationTests {
    @Autowired
    UserService userService;

    @Test
    void contextLoads() {
        userService.hello();
    }

}
```

注意一点：消费端要调用服务端Service也需要创建一个Service接口，注意包路径要保证是dubbo的服务的扫描路径。在实际项目中可以抽取一个公共API模块创建Service接口

## 2、Spring Boot和Spring Cloud

Spring Cloud是一个分布式的整体解决方案。Spring Cloud 为开发者提供了在分布式系统（配置管理，服务发现，熔断，路由，微代理，控制总线，一次性token，全局琐，leader选举，分布式session，集群状态）中快速构建的工具，使用Spring Cloud的开发者可以快速的启动服务或构建应用、同时能够快速和云平台资源进行对接。

Provider：

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter</artifactId>
</dependency>

<dependency>
     <groupId>org.springframework.cloud</groupId>
     <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>

<dependencyManagement>
    <dependencies>
       <dependency>
           <groupId>org.springframework.cloud</groupId>
           <artifactId>spring-cloud-dependencies</artifactId>
           <version>${spring-cloud.version}</version>
           <type>pom</type>
           <scope>import</scope>
        </dependency>
     </dependencies>
</dependencyManagement>
```

```java
@Service //将服务发布出去
public class TicketServiceImpl implements TicketService {
    @Override
    public String getTicket() {
        System.out.println("8002");
        return "《厉害了，我的国》";
    }
}
```

```java
@RestController
public class TicketController {
    @Autowired
    TicketService ticketService;

    @GetMapping("/ticket")
    public String getTicket(){
        return ticketService.getTicket();
    }
}
```

```yml
server:
  port: 8002
spring:
  application:
    name: provider-ticket
eureka:
  instance:
    instance-id:  provider-ticket8002  #自定义服务名称信息
    prefer-ip-address: true # 注册服务的时候使用服务的ip地址
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/

```

EurecaServer

```java
@SpringBootApplication
@EnableEurekaServer
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

```yml
server:
  port: 8761
eureka:
  instance:
    hostname: eureka-server  # eureka实例的主机名
  client:
    register-with-eureka: false #不把自己注册到eureka上
    fetch-registry: false #不从eureka上来获取服务的注册信息
    service-url:
      defaultZone: http://localhost:8761/eureka/
```

Consumer

```yml
spring:
  application:
    name: consumer-user
server:
  port: 8200

eureka:
  instance:
    prefer-ip-address: true # 注册服务的时候使用服务的ip地址
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
```

1) 使用Ribbon+RestTemplate调用

```java
@SpringBootApplication
@EnableDiscoveryClient
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @LoadBalanced //使用负载均衡机制
    @Bean
    public RestTemplate restTemplate(){
        return new RestTemplate();
    }
}
```

```java
@RestController
public class UserController {
    @Autowired
    RestTemplate restTemplate;

    @RequestMapping("/getTicket")
    public String getTicker(){
        String forObject = restTemplate.getForObject("http://PROVIDER-TICKET/ticket", String.class);
        return forObject;
    }
}
```

2) 使用Feign调用

```   xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```
```java
@SpringBootApplication
@EnableDiscoveryClient
@EnableFeignClients
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
```

创建一个Client

```java
@FeignClient(value = "provider-ticket")
@Component
public interface TicketClient {
    @RequestMapping(path = "/ticket", method = RequestMethod.GET)
    String getTicket();
}
```

```java
@Service
public class TicketService {
    @Autowired
    TicketClient ticketClient;

    public String getTicket(){
        return ticketClient.getTicket();
    }
}
```

# 七、SpringBoot热部署

在开发中我们修改一个Java文件后想看到效果不得不重启应用，这导致大量时间花费，我们希望不重启应用的情况下，程序可以自动部署（热部署）。有以下四种情况，如何能实现热部署。



–引入依赖

```xml
 <!--开发热部署-->
<dependency>
   <groupId>org.springframework.boot</groupId>
   <artifactId>spring-boot-devtools</artifactId>
   <optional>true</optional>
</dependency>
```

IDEA使用ctrl+F9
–或做一些小调整
Intellij IEDA和Eclipse不同，Eclipse设置了自动编译之后，修改类它会自动编译，而IDEA在非RUN或DEBUG情况下才会自动编译（前提是你已经设置了Auto-Compile）。
设置自动编译（settings-compiler-make project automatically）
ctrl+shift+alt+/（maintenance）
勾选compiler.automake.allow.when.app.running

# 八、Spring Boot与监控管理

通过引入spring-boot-starter-actuator，可以使用Spring Boot为我们提供的准生产环境下的应用监控和管理功能。我们可以通过HTTP，JMX，SSH协议来进行操作，自动得到审计、健康及指标信息等

步骤：

​	–引入spring-boot-starter-actuator

​	–通过http方式访问监控端点

​	–可进行shutdown（POST 提交，此端点默认关闭）

### 监控和管理端点 

| **端点名**   | **描述**                    |
| ------------ | --------------------------- |
| *autoconfig* | 所有自动配置信息            |
| auditevents  | 审计事件                    |
| beans        | 所有Bean的信息              |
| configprops  | 所有配置属性                |
| dump         | 线程状态信息                |
| env          | 当前环境信息                |
| health       | 应用健康状况                |
| info         | 当前应用信息                |
| metrics      | 应用的各项指标              |
| mappings     | 应用@RequestMapping映射路径 |
| shutdown     | 关闭当前应用（默认关闭）    |
| trace        | 追踪信息（最新的http请求）  |

spring boot为actuator提供了起步依赖starter，我们需要在pom中添加下面starter：

```xml
		<!--web依赖-->
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-web</artifactId>
		</dependency>
		<!--添加actuator依赖-->
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-actuator</artifactId>
		</dependency>
		<!--spring boot admin依赖-->
		<dependency>
			<groupId>de.codecentric</groupId>
			<artifactId>spring-boot-admin-starter-client</artifactId>
		</dependency>
```
在配置文件中添加下面配置

```properties
# 设置actuator监控端口
management.server.port=8082
# 开启所有监控端点(endpoint), 默认值开启了health和info
management.endpoints.web.exposure.include=*

# 添加info信息
info.author=harry
info.url=www.harry.com
# 自定义endpoint的id和路径已经开关
#endpoints.beans.id=mybean
#endpoints.beans.path=/bean
#endpoints.beans.enabled=false
#
#endpoints.dump.path=/du

# \u5173\u95ED\u6240\u6709\u7AEF\u70B9\u8BBF\u95EE
#endpoints.enabled=false
#endpoints.beans.enabled=true
```
​	启动spring boot程序，在浏览器中输入：http://localhost:8082/actuator/info

自定义健康信息检测

```java
@Component
public class MyAppHealthIndicator implements HealthIndicator {

    @Override
    public Health health() {

        //自定义的检查方法
        //Health.up().build()代表健康
        return Health.down().withDetail("msg","服务异常").build();
    }
}
```

### spring boot admin图形化界面

上面通过actuator提供的rest接口，返回的数据都是json格式，这个对于不懂json格式的人来说不太方便，因此就产生了spring boot admin，它提供了图形化界面，通过界面来展示这些数据。

创建新的模块，加入相关依赖

```xml
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-web</artifactId>
</dependency>
<!--spring boot admin相关依赖-->
<dependency>
	<groupId>de.codecentric</groupId>
	<artifactId>spring-boot-admin-starter-server</artifactId>
</dependency>
```

在spring boot的启动类上添加下面注解，开启admin

```java
@SpringBootApplication
@EnableAdminServer // 开启SBA server
public class ApplicationServer {
	public static void main(String[] args) {
		SpringApplication.run(ApplicationServer.class, args);
	}

}
```

在配置文件中设置下端口号：
			server.port=8085

上面的项目是作为server端，将之前的spring boot项目作为client端，由server端统一监控client端。

client的模块中，在配置文件里面添加下面内容：

```properties
# 配置SBA server端的地址和端口号
spring.boot.admin.client.url=http://localhost:8085
# 开启所有监控端点(endpoint), 默认值开启了health和info
management.endpoints.web.exposure.include=*
			
```

启动server和client，访问server端，http://localhost:8085 就可以看到spring boot admin的页面了
