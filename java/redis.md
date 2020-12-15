# 一 Redis简介

## 1、什么是redis

​    Redis是一个开源（BSD许可），**内存存储的数据结构服务器，可用作数据库，高速缓存和消息队列代理。它支持字符串、哈希表、列表、集合、有序集合，位图，hyperloglogs等数据类型**。内置复制、Lua脚本、LRU收回、事务以及不同级别磁盘持久化功能，同时通过Redis
Sentinel提供高可用，通过Redis Cluster提供自动分区。

   Redis属于**NoSQL**类型数据，即非关系型数据库。

## 2、什么是NoSQL

NoSQL，**泛指非关系型的数据库**。随着互联网web2.0网站的兴起，传统的关系数据库在处理web2.0网站，特别是超大规模和高并发的SNS类型的web2.0纯动态网站已经显得力不从心，出现了很多难以克服的问题，而非关系型的数据库则由于其本身的特点得到了非常迅速的发展。NoSQL数据库的产生就是为了解决大规模数据集合多重数据种类带来的挑战，尤其是大数据应用难题。

NoSQL，即：**not only sql**

RDBMS VS NoSQL

RDBMS：  	

	1. 高度组织化结构化数据  	
 	2. 结构化查询语言(SQL)  	
 	3. 数据和关系都存储在单独的表中  	
 	4. 数据操纵语言，数据定义语言  	
 	5. 严格的一致性  	6. 基础事务(ACDI属性)  

NoSQL：

	1. 代表着不仅仅是SQL  	
 	2.  没有声明性查询语言  	
 	3. 没有预定义的模式  	
 	4. 键-值对存储，列存储，文档存储，图形数据库  	
 	5.  最终一致性，而非ACID属性

## 3、为什么使用NoSQL

   随着互联网飞速发展，数据访问量和存储量高速扩大，传统的架构APP访问DAL层，DAL层再查询直接通过关系型数据库(比如MYSQL数据库)获取数据返回给用用户已然出现了性能问题。为了解决这个问题，需要对数据库和数据库表的水平拆分和垂直拆分

![image-20201129113730065](\images\image-20201129113730065.png)

### 分布式缓存+MySQL+垂直拆分

![image-20201129113806498](\images\image-20201129113806498.png)

​    后来，随着访问量的上升，几乎大部分使用MySQL架构的网站在数据库上都开始出现了性能问题，web程序不再仅仅专注在功能上，同时也在追求性能。程序员们开始大量的使用缓存技术来缓解数据库的压力，优化数据库的结构和索引。开始比较流行的是通过文件缓存来缓解数据库压力，但是当访问量继续增大的时候，多台web机器通过文件缓存不能共享，大量的小文件缓存也带了了比较高的IO压力。在这个时候，分布式缓存就自然的成为一个非常时尚的技术产品。

​    数据库拆分之后就会出现多了多个数据库，多个数据库有分别部署在了不同的服务器，这时就需要对数据库进行集群，为了保证多台机器的缓存一致性、可用性和分区容错性，分布式缓存(比如Redis)的诞生正好解决了这个痛点。

​    分布式缓存为多个web服务器提供了一个共享的高性能缓存服务。

### Mysql主从读写分离

​    由于数据库的写入压力增加，分布式缓存只能缓解数据库的读取压力。读写集中在一个数据库上让数据库不堪重负，大部分网站开始使用主从复制技术来达到读写分离，以提高读写性能和读库的可扩展性。Mysql的master-slave模式成为这个时候的网站标配了。

### 分库分表+水平拆分+mysql集群

![image-20201129114032267](\images\image-20201129114032267.png)

```
在分布式的高速缓存，MySQL的主从复制，读写分离的基础之上，这时MySQL主库的写压力开始出现瓶颈，而数据量的持续猛增，由于MyISAM在写数据的时候会使用表锁，在高并发写数据的情况下会出现严重的锁问题，大量的高并发MySQL应用开始使用InnoDB引擎代替MyISAM。
同时，开始流行使用分表分库来缓解写压力和数据增长的扩展问题。这个时候，分表分库成了以一个热门技术， 也是面试的热门问题也是业界讨论的热门技术问题。也就在这个时候，MySQL推出了还不太稳定的表分区，这也 给技术实力一般的公司带来 了希望。虽然MySQL推出了MySQL Cluster集群，但性能也不能很好满足互联网 的要求，只是在高可靠性上提供了非常大的保证。
```

## 4、NoSQL分类

1. 键值(Key-Value)存储数据库
   这一类数据库主要会使用到一个哈希表，这个表中有一个特定的键和一个指针指向特定的数据。Key/value模型对于IT系统来说的优势在于简单、易部署。但是如果数据库管理员(DBA)只对部分值进行查询或更新的时候，Key/value就显得效率低下了。举例如：Tokyo Cabinet/Tyrant， Redis， Voldemort， Oracle BDB。
2. 列存储数据库
   这部分数据库通常是用来应对分布式存储的海量数据。键仍然存在，但是它们的特点是指向了多个列。这些列是由列家族来安排的。如：Cassandra， HBase， Riak.
3. 文档型数据库
   文档型数据库的灵感是来自于Lotus Notes办公软件的，而且它同第一种键值存储相类似。该类型的数据模型是版本化的文档，半结构化的文档以特定的格式存储，比如JSON。文档型数据库可以看作是键值数据库的升级版，允许之间嵌套键值，在处理网页等复杂数据时，文档型数据库比传统键值数据库的查询效率更高。如：CouchDB， MongoDb. 国内也有文档型数据库SequoiaDB，已经开源。
4. 图形(Graph)数据库
   图形结构的数据库同其他行列以及刚性结构的SQL数据库不同，它是使用灵活的图形模型，并且能够扩展到多个服务器上。NoSQL数据库没有标准的查询语言(SQL)，因此进行数据库查询需要制定数据模型。许多NoSQL数据库都有REST式的数据接口或者查询API。如：Neo4J， InfoGrid， Infinite Graph。



## 5、NoSQL特性

- C：consistency，数据在多个副本中能保持一致的状态。
- A：Availability，整个系统在任何时刻都能提供可用的服务，通常达到99.99%四个九可以称为高可用
- P：Partition tolerance，分区容错性，在分布式中，由于网络的原因无法避免有时候出现数据不一致的情况，系统如果不能在时限内达成数据一致性，就意味着发生了分区的情况，必须就当前操作在C和A之间做出选择，换句话说，系统可以跨网络分区线性的伸缩和扩展。

CAP理论的核心：一个分布式系统不可能同时很好的满足一致性，可用性和分区容错性这三个需求，最多只能同时较好的满足两个。

CA：单点集群，满足一致性，可用性的系统，通常在可扩展上不太强大。应用：传统的Oracle数据库
CP：满足一致性，分区容错性的系统，通常性能不是特别高。应用：Redis，MongoDB，银行
AP：满足可用性，分区容错性，通常可能对一致性要求低一些。应用：大多数网站架构的选择

![image-20201129114438987](\images\image-20201129114438987.png)

- CAP理论就是说在分布式存储系统中，最多只能实现上面的两个。而由于当前的网络硬件肯定会出现延迟丢包等问题，所以分区容忍性（P）是我们必须需要实现的。所以在分布式系统中，根据不同的情况选择使用AP或者CP模式。

- 分布式和集群
  `分布式：不同的多台服务器上面部署不同的服务模块（工程）`
  `集群：不同的多台服务器上面部署相同的服务模块。通过分布式调度软件进行统一的调度，对外提供服务和访问`

- 为何CAP三者不可兼得?

  假设有两台服务器，一台放着应用A和数据库DB0，一台放着应用B和数据库DBI，他们之间的网络可以互通，也就相当于分布式系统的两个部分。

  在满足一致性(C)的时候，一开始两台服务器的数据是一样的，DB0=DBI。在满足可用性(A)的时候，用户不管是请求服务器1还是服务器2，都会得到立即响应。在满足分区容错性(P)的情况下，两台有任何一方宕机，或者网络不通的时候，都不会影响彼此之间的正常运作。

![image-20201129114629431](\images\image-20201129114629431.png)

​    在两台服务器正常通讯的情况下，当服务器1通过应用A请求更新数据库DB0的时候，通过分布式系统系统的同步更新操作，服务器2的数据也由DBI更新到了DBII，此时DB1=DBII，这时用户通过服务器2向数据库发起请求得到的数据就是最新的数据

​    上面是正常运作的情况，但分布式系统中，最大的问题就是网络传输问题，现在假设一种极端情况，服务器1和服务器2之间的网络断开了，但我们仍要支持这种网络异常，也就是满足分区容错性(P)，那么这样能不能同时满足一致性(C)和可用性(A)呢？

![image-20201129114818233](\images\image-20201129114818233.png)

​    假设服务器1和服务器2之间通信的时候网络突然出现故障，有用户向服务器1发送数据更新请求，那服务器1中的数据DB0将被更新为DB1，由于网络是断开的，服务器2中的数据库仍旧是DBI，这时DB1 != DBI。

​    如果这个时候，有用户向服务器2发送数据读取请求，由于数据还没有进行同步，应用程序没办法立即给用户返回最新的数据DBII，怎么办呢？有二种选择，第一，牺牲数据一致性(C)，响应旧的数据DBI给用户；第二，牺牲可用性(A)，阻塞等待，直到网络连接恢复，数据更新操作完成之后，再给用户响应最新的数据DBII。

   上面的过程比较简单，但也说明了要满足分区容错性的分布式系统，只能在一致性(C)和可用性(A)两者中，选择其中一个。也就是说分布式系统不可能同时满足三个特性。这就需要我们在搭建系统时进行取舍了。

# 二 redis的安装

## 1、redis相对其他k-v缓存技术的特点：

1. 支持数据的持久化，可以将内存中的数据保持在磁盘中，重启的时候可以再次加载进行使用。
2. 不仅仅支持简单的k-v键值对，同时还提供list、hash、set和zset等数据结构的存储。
3. 支持数据的备份，即master-slave模式的数据备份。

## 2、redis能干吗？

1. redis支持异步将内存中的数据写到磁盘上，同时不影响继续服务。
2. 取N个最新数据的操作，如：可以将最新的10条评论的ID放在redis的list集合中。
3. 模拟类似HttpSession这种需要设定过期时间的功能。
4. 发布订阅消息系统。
5. 定时器、计数器。

## 3、redis安装

```
$ wget https://download.redis.io/releases/redis-6.0.9.tar.gz
$ tar xzf redis-6.0.9.tar.gz
$ cd redis-6.0.9
$ make
```

假设一切环境准备就绪的情况下，将下载好的后缀名为`tar.gz`的redis安装包(如)拷贝到linux系统中，放入我们自定义的目录，比如：`/usr/src`，运行解压命令`tar -xvf redis-6.0.9.tar.gz`，解压成功后将生成`redis-6.0.69目录。

gcc编译器低于5.0执行make命令时将会报如下错误：

![image-20201207193933847](D:\studyDoc\java\images\image-20201207193933847.png)

执行`gcc -v`，查看当前虚拟机gcc版本。

![image-20201207194201716](\images\image-20201207194201716.png)

如果需要，升级gcc版本如下：
yum -y install centos-release-scl
yum -y install devtoolset-9-gcc devtoolset-9-gcc-c++ devtoolset-9-binutils

`scl enable devtoolset-9 bash`设置gcc新版本生效（临时）。

在设置临时生效的基础上，执行`echo "source /opt/rh/devtoolset-9/enable" >>/etc/profile` 写入配置文件设置gcc新版本永久生效。

虚拟机上没安装gcc编译器可以执行以下命令安装gcc编译器：

```bash
yum install cpp
yum install binutils
yum install glibc
yum install glibc-kernheaders
yum install glibc-common
yum install glibc-devel
yum install gcc
yum install make
```

解决了gcc版本过低的问题，先执行`make`命令进行编译，后执行`make install`安装redis， 两条命令可以合并为一条命令`make && make install`编译并安装。

redis安装成功后将在`/usr/local/bin`目录下多出如下几个文件：

![image-20201207194521980](\images\image-20201207194521980.png)

## 4、启动redis

修改redis.conf文件将里面的daemonize no改成yes，让服务在后台启动。

![image-20201207194835526](\images\image-20201207194835526.png)

进入`/usr/`执行`redis-server /myredis/redis.conf`读取拷贝的redis.conf配置文件来启动redis服务，`ps -ef | grep redis`查看redis服务是否成功启动，默认端口号为6379。

![image-20201207194904355](\images\image-20201207194904355.png)

## 5、连通测试

执行`redis-cli -p 6379`命令使用redis客户端连接端口号为6379的redis服务，并输入`ping`来测试是否连接成功。

![image-20201207194943927](\images\image-20201207194943927.png)

# 三 redis数据类型和常用命令

## 1、redis数据类型介绍

你也许已经知道Redis并不是简单的key-value存储，实际上他是一个数据结构服务器，支持不同类型的值。也就是说，你不必仅仅把字符串当作键所指向的值。下列这些数据类型都可作为值类型：

​     Strings(字符串)：**二进制安全的字符串**，意味着redis的string可以包含任何数据。比如jpg图片或者序列化的对象。一个键最多能存储512MB。二进制安全是指，在传输数据的时候，能保证二进制数据的信息安全，也就是不会被篡改、破译；如果被攻击，能够及时检测出来。

​     Lists(列表)：**按插入顺序排序的字符串元素的集合**。他们基本上就是**链表**（linked lists）。你可以一个元素到列表的头部（左边），或者添加一个元素到尾部（右边）。

​     Sets(无序集合)：**不重复且无序的字符串元素的集合**

​     Sorted sets(有序集合)：**不重复且有序的字符串元素的集合**。类似Sets，但是每个字符串元素都关联到一个叫score浮动数值（floating number value）。里面的元素总是通过score进行着排序，所以不同的是，它是可以检索的一系列元素。**Sorted sets的元素是唯一的，但是score是可以重复的**。

​     Hashes(哈希)：**由field和关联的value组成的map，field和value都是字符串的。是一个键值对集合，特别适用于存储对象。**
Redis key值是二进制安全的，这意味着可以用任何二进制序列作为key值，从形如”foo”的简单字符串到一个JPEG文件的内容都可以。空字符串也是有效key值。

## 2、redis数据类型常见的操作命令

注：在redis里，执行指令返回结果中，0表示否，1表示是。

### Redis 键(key)

- keys *
- exists key的名字，判断某个key是否存在
- move key db   --->当前库就没有了，被移除了
- expire key 秒钟：为给定的key设置过期时间
-  ttl key 查看还有多少秒过期，-1表示永不过期，-2表示已过期
- type key 查看你的key是什么类型

### Strings常用命令

- **set** key value：设置指定key的值，示例：`set key1 value1`
- **setex** key seconds value：给指定的key设置value，并设置key的过期时间，单位秒，（set with expire）示例：`setex name 5 zhagnsan`
- **setnx** key value：当key不存在时设置key的值。（set if not exists），分布式锁的问题，示例：`setnx key2 helloworld`
- **append** key value：追加指定key的值，示例：`append key1 hello`
- **get** key：获取指定key的值，示例：`get key1`
- **getrange** key start end：获取key中指定范围的value值，end为-1时，表示从start位置到value值的最后一个字符串，示例：`getrange key1 0 3`
- **setrange** key offset value：替换key中指定offset偏移量的值，示例：`setrange key1 5 kitty`
- **strlen** key：返回key所存储的字符串值的长度，示例：`strlen key1`
- **del** key：删除指定的key，示例：`del key1`
- **incr** key：如果key指定的值是integer类型，则值自增1，示例：`incr key1`
- **decr** key：如果key指定的值是integer类型，则值自减1，示例：`decr key1`
- **incrby** key number：如果key指定的值是integer类型，则值自增number个数值，示例：`incrby key1 5`
- **decrby** key number：如果key指定的值是integer类型，则值自减number个数值，示例：`incrby key1 5`
- **mset** key value [key value …]：批量设置多个key和值，示例：`mset a1 b1 a2 b2`
- **mget** key value [key value …]：批量获取多个key的值，示例：`mget a1 a2`
- **getset** key value：先get再set，示例：`getset name lisi`

### Lists常用命令

- **lpush** key element [element …] ：给列表指定的key在头部（左边）设置多个元素，示例：`lpush numbers 1 2 3 4 5`
- **rpush** key element [element …] ：给列表指定的key在尾部（右边）设置多个元素，示例：`rpush numbers1 a b c d e`
- **lrange** key start stop：获取key指定范围内的元素，stop为-1时，表示从start位置开始一直到list的最后一个元素，示例：`lrange numbers 1 3`
- **lpop** key：弹出指定key头元素，即左边第一个元素，示例：`lpop numbers`
- **rpop** key：弹出指定key：尾元素，即右边第一个元素，示例：`rpop numbers`
- **lindex** key index：根据索引下标获得指定key的元素，示例：`lindex numbers 1`
- **llen** key：获取指定key元素的个数，示例：`llen numbers`
- **lrem** key count element：

#### 案例

 lpop/rpop

![image-20201208200125558](\images\image-20201208200125558.png)

lindex，按照索引下标获得元素(从上到下)

![image-20201208200149233](\images\image-20201208200149233.png)

 lrem key 删N个value

 从left往right删除2个值等于v1的元素，返回的值为实际删除的数量

 LREM list3 0 值，表示删除全部给定的值。零个就是全部值

![image-20201208200240964](\images\image-20201208200240964.png)

 ltrim key 开始index 结束index，截取指定范围的值后再赋值给key

 ltrim：截取指定索引区间的元素，格式是ltrim list的key 起始索引 结束索引

![image-20201208200316741](\images\image-20201208200316741.png)

rpoplpush 源列表 目的列表

移除列表的最后一个元素，并将该元素添加到另一个列表并返回

![image-20201208200348428](\images\image-20201208200348428.png)

lset key index value

![image-20201208200415937](\images\image-20201208200415937.png)

linsert key  before/after 值1 值2 在list某个已有值的前后再添加具体值

![image-20201208200516381](\images\image-20201208200516381.png)

### Sets常用命令

- **sadd** key member [member …]：给指定的key添加多个不重复的元素，示例：`sadd set1 1 2 3 4`
- **smembers** key：查看指定key元素，示例：`smembers set1`
- **sismember** key member：判断指定的key是否存在指定的值，示例：`sismember set1 2`
- **scard** key：获取集合指定key元素的个数，示例：`scard set1`
- **srem** key member [member …]：删除集合中指定key的元素，示例：`srem set1 1 2`
- **srandmember** key [count]：随机获取集合中指定key的count个值，count默认为：1，示例：`srandmember set1 2`
- **spop** key [count]：出栈count个指定key的值，示例：`spop set1 2`
- **smove** source destination member：将source的member元素移动到destination去，示例：`smove set1 set2 3`
- **sdiff** key [key …]：返回指定key的元素与其他多个key的差集，示例：`sdiff set1 set2`
- **sinter** key [key …]：返回指定key的元素与其他多个key的交集，示例：`sinter set1 set2`
- **sunion** key [key …]：返回指定key的元素与其他多个key的并集，示例：`sunion set1 set2`

#### 案例

sadd/smembers/sismember

![image-20201208202932685](\images\image-20201208202932685.png)

scard，获取集合里面的元素个数

![image-20201208202953367](\images\image-20201208202953367.png)

 srem key value 删除集合中元素

![image-20201208203016861](\images\image-20201208203016861.png)

srandmember key 某个整数(随机出几个数)


 *   从set集合里面随机取出2个
 *   如果超过最大数量就全部取出，
 *   如果写的值是负数，比如-3 ，表示需要取出3个，但是可能会有重复值。

![image-20201208203055330](\images\image-20201208203055330.png)

spop key 随机出栈

![image-20201208203121308](\images\image-20201208203121308.png)

smove key1 key2 在key1里某个值      作用是将key1里的某个值赋给key2

![image-20201208203150612](\images\image-20201208203150612.png)

数学集合类

差集：sdiff

![image-20201208203224176](\images\image-20201208203224176.png)

交集：sinter

![image-20201208203256170](\images\image-20201208203256170.png)

并集：sunion

![image-20201208203323207](\images\image-20201208203323207.png)

### Sort Sets常用命令

- zadd key score member [score member …] ：给指定的key添加多个不重复的元素，score用于元素的排序，示例：`zadd zset1 10 b 20 a 30 e 40 c 50 d`
- **zrange** key start stop [WITHSCORES]：查询从start到stop区间指定key的元素（顺序），stop为-1时，表示从start开始到最后一个元素，可选参数WITHSCORES表示带score显示，示例：`zrange zset1 0 -1 withscores`
- **zrevrange** key start stop [WITHSCORES]：查询从start到stop区间指定key的元素（逆序），stop为-1时，表示从start开始到最后一个元素，可选参数WITHSCORES表示带score显示，示例：`zrevrange zset1 0 -1 withscores`
- **zrangebyscore** key min max [WITHSCORES] [LIMIT offset count]：查询从min到max区间的score值的指定key的元素（顺序），可选参数WITHSCORES表示带score显示，可选参数LIMIT offset count用于分页显示，示例：`zrangebyscore zset1 21 50 withscores`
- **zrevrangebyscore** key min max [WITHSCORES] [LIMIT offset count]：查询从min到max区间的score值的指定key的元素（逆序），可选参数WITHSCORES表示带score显示，可选参数LIMIT offset count用于分页显示，示例：`zrangebyscore zset1 21 50 withscores`
- **zrem** key member [member …]：移除集合指定key的一个或者多个元素，示例：`zrem zset1 e a`
- **zcard** key：返回集合指定key元素的个数，示例：`zcard zset1`
- **zcount** key min max：返回集合指定key元素在min和max的score区间的个数，示例：`zcount zset1 31 50`
- **zrank** key member：返回集合指定key的member元素的下标（通过score顺序排序），示例：`zrank zset1 d`
- **zrevrank** key member：返回集合指定key的member元素的下标（通过score逆序排序），示例：`zrevrank zset1 d`

#### 案例

zadd/zrange

![image-20201208203525389](\images\image-20201208203525389.png)

zrangebyscore key 开始score 结束score

![image-20201208203549588](\images\image-20201208203549588.png)

zrem key 某score下对应的value值，作用是删除元素

删除元素，格式是zrem zset的key 项的值，项的值可以是多个

zrem key score某个对应值，可以是多个值

![image-20201208203852360](\images\image-20201208203852360.png)

 zcard/zcount key score区间/zrank key values值，作用是获得下标值/zscore key 对应值,获得分数

![image-20201208203925978](\images\image-20201208203925978.png)

 zrevrank key values值，作用是逆序获得下标值

![image-20201208204029174](\images\image-20201208204029174.png)

zrevrange

![image-20201208204056505](\images\image-20201208204056505.png)

zrevrangebyscore  key 结束score 开始score

zrevrangebyscore zset1 90 60 withscores    分数是反着来的

![image-20201208204130281](\images\image-20201208204130281.png)

### Hashes常用命令

- **hset** key field value [field value …]：给指定的key设置一个或多个K-V键值对，示例：`hset user name zhangsan age 30 hight 170`
- **hsetnx** key field value：如果指定的field还没存在，则给指定的key设置一个K-V键值对，示例：`hsetnx user weight 110`
- **hget** key field：获取指定key的field字段的值，示例：`hget user name`
- **hmset** key field value [field value …]：等价于hset，给指定的key设置一个或多个K-V键值对，示例：`hmset user name zhangsan age 30 hight 170`
- **hmget** key field [field …]：获取指定key的一个或多个field指定的值，示例：`hmget user name age hight`
- **hgetall** key：返回指定key的所有K-V键值对，示例：`hgetall user`
- **hdel** key field [field …]：删除指定key的一个或者多个K-V键值对，示例：`hdel user name age`
- **hlen** key：返回指定key的K-V键值对的个数，示例：`hlen user`
- **hexists** key field：判断指定key的field是否存在，示例：`hexists user hight`
- **hkeys** key：返回key指定的所有field，示例：`hkeys user`
- **hvals** key：返回key指定的所有field对应的值，示例：`hvals user`
- **hincrby** key field increment：给指定的key的field的值进行自增increment数量，前提是field指定的值是integer类型的，示例：`hincrby user age 5`
- hincrbyfloat key field increment：给指定的key的field的值进行自增increment数量，示例：`hincrbyfloat user money 11.11`

#### 案例

hset/hget/hmset/hmget/hgetall/hdel

![image-20201208204838929](\images\image-20201208204838929.png)

hexists key 在key里面的某个值的key

hkeys/hvals

![image-20201208204926115](\images\image-20201208204926115.png)

hincrby/hincrbyfloat

![image-20201208204958225](\images\image-20201208204958225.png)

hsetnx不存在赋值，存在了无效。

![image-20201208205049111](\images\image-20201208205049111.png)

# 四 redis配置文件

## 1. UNITS（单位）

![image-20201208205533993](\images\image-20201208205533993.png)

## 2. INCLUDES （包含）

![image-20201208205829669](\images\image-20201208205829669.png)

## 3. GENERAL（通用）

```bash
# By default Redis does not run as a daemon. Use 'yes' if you need it.
# Note that Redis will write a pid file in /var/run/redis.pid when daemonized.
#daemonize no
#是否在后台运行；no：不是后台运行，而是在控制台打印出启动信息
daemonize yes

# If you run Redis from upstart or systemd, Redis can interact with your
# supervision tree. Options:
#   supervised no      - no supervision interaction
#   supervised upstart - signal upstart by putting Redis into SIGSTOP mode
#   supervised systemd - signal systemd by writing READY=1 to $NOTIFY_SOCKET
#   supervised auto    - detect upstart or systemd method based on
#                        UPSTART_JOB or NOTIFY_SOCKET environment variables
# Note: these supervision methods only signal "process is ready."
#       They do not enable continuous liveness pings back to your supervisor.
supervised no

# If a pid file is specified, Redis writes it where specified at startup
# and removes it at exit.
#
# When the server runs non daemonized, no pid file is created if none is
# specified in the configuration. When the server is daemonized, the pid file
# is used even if not specified, defaulting to "/var/run/redis.pid".
#
# Creating a pid file is best effort: if Redis is not able to create it
# nothing bad happens, the server will start and run normally.

#redis的进程文件
pidfile /var/run/redis_6379.pid

# Specify the server verbosity level.
# This can be one of:
# debug (a lot of information, useful for development/testing)
# verbose (many rarely useful info, but not a mess like the debug level)
# notice (moderately verbose, what you want in production probably)
# warning (only very important / critical messages are logged)

#指定了服务端日志的级别。级别包括：
#debug（很多信息，方便开发、测试）
#verbose（许多有用的信息，但是没有debug级别信息多）
#notice（适当的日志级别，适合生产环境）
#warn（只有非常重要的信息）
loglevel notice

# Specify the log file name. Also the empty string can be used to force
# Redis to log on the standard output. Note that if you use standard
# output for logging but daemonize, logs will be sent to /dev/null

#保存日志的文件。空字符串时，日志会打印到标准输出设备。后台运行的redis标准输出是/dev/null
logfile ""

# To enable logging to the system logger, just set 'syslog-enabled' to yes,
# and optionally update the other syslog parameters to suit your needs.

#是否把日志输出到syslog中
syslog-enabled no

# Specify the syslog identity.
#指定syslog里的日志标志
# syslog-ident redis
# Specify the syslog facility. Must be USER or between LOCAL0-LOCAL7.
#指定syslog设备，值可以是USER或LOCALO-LOCAL7
# syslog-facility local0
# Set the number of databases. The default database is DB 0, you can select
# a different one on a per-connection basis using SELECT <dbid> where
# dbid is a number between 0 and 'databases'-1

#数据库的数量，默认16个，数据库下标索引从0开始，可通过命令select + 下标切换数据库
databases 16

# By default Redis shows an ASCII art logo only when started to log to the
# standard output and if the standard output is a TTY. Basically this means
# that normally a logo is displayed only in interactive sessions.
#
# However it is possible to force the pre-4.0 behavior and always show a
# ASCII art logo in startup logs by setting the following option to yes.

always-show-logo yes
```

## 4. MODULES（模块）

```bash
# Load modules at startup. If the server is not able to load modules
# it will abort. It is possible to use multiple loadmodule directives.
#
# loadmodule /path/to/my_module.so
# loadmodule /path/to/other_module.so
```

## 5.NETWORK(网络连接)

```bash
# By default, if no "bind" configuration directive is specified, Redis listens
# for connections from all the network interfaces available on the server.
# It is possible to listen to just one or multiple selected interfaces using
# the "bind" configuration directive, followed by one or more IP addresses.
#
# Examples:
#

# bind 192.168.1.100 10.0.0.1
# bind 127.0.0.1 ::1

#
# ~~~ WARNING ~~~ If the computer running Redis is directly exposed to the
# internet, binding to all the interfaces is dangerous and will expose the
# instance to everybody on the internet. So by default we uncomment the
# following bind directive, that will force Redis to listen only into
# the IPv4 loopback interface address (this means Redis will be able to
# accept connections only from clients running into the same computer it
# is running).
#

# IF YOU ARE SURE YOU WANT YOUR INSTANCE TO LISTEN TO ALL THE INTERFACES

# JUST COMMENT THE FOLLOWING LINE.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#指定redis只接收来自于该IP地址的请求，如果不进行设置，那么将处理所有请求，在生产环境中最好设置该项
bind 127.0.0.1

# Protected mode is a layer of security protection, in order to avoid that
# Redis instances left open on the internet are accessed and exploited.
#
# When protected mode is on and if:
#
# 1) The server is not binding explicitly to a set of addresses using the
#    "bind" directive.
# 2) No password is configured.
#

# The server only accepts connections from clients connecting from the
# IPv4 and IPv6 loopback addresses 127.0.0.1 and ::1, and from Unix domain
# sockets.

#
# By default protected mode is enabled. You should disable it only if
# you are sure you want clients from other hosts to connect to Redis
# even if no authentication is configured, nor a specific set of interfaces
# are explicitly listed using the "bind" directive.

#是否启动redis保护模式，默认开启，启动之后远程服务需要密码才能连接，如果没有设置密码又需要远程连接，则需要把保护模式关闭
protected-mode yes

# Accept connections on the specified port, default is 6379 (IANA #815344).
# If port 0 is specified Redis will not listen on a TCP socket.
#redis启动端口
port 6379

# TCP listen() backlog.
#
# In high requests-per-second environments you need an high backlog in order
# to avoid slow clients connections issues. Note that the Linux kernel
# will silently truncate it to the value of /proc/sys/net/core/somaxconn so
# make sure to raise both the value of somaxconn and tcp_max_syn_backlog
# in order to get the desired effect.
#设置tcp的backlog，backlog 其实是- - .个连接队列，backlog队列总 和=未完成三次握手队列+已经完成三次握手队列。
#在高并发环境下你需要--个高backlog值来避免慢客户端连接问题。注意Linux内核会将这个值减小到/proc/sys/net/core/somaxconn的值，所以需要确认增大somaxconn和tcp_max_syn_backlog两个值来达到想要的效果
tcp-backlog 511

# Unix socket.
#
# Specify the path for the Unix socket that will be used to listen for
# incoming connections. There is no default, so Redis will not listen
# on a unix socket when not specified.
#

# unixsocket /tmp/redis.sock
# unixsocketperm 700
# Close the connection after a client is idle for N seconds (0 to disable)

#设置客户端连接时的超时时间，单位为秒。当客户端在这段时间内没有发出任何指令，那么关闭该连接，0是关闭此设置
timeout 0
#TCP keepalive.
#
# If non-zero, use SO_KEEPALIVE to send TCP ACKs to clients in absence
# of communication. This is useful for two reasons:
#

# 1) Detect dead peers.
# 2) Take the connection alive from the point of view of network
#    equipment in the middle.
#

# On Linux, the specified value (in seconds) is the period used to send ACKs.
# Note that to close the connection the double of the time is needed.
# On other kernels the period depends on the kernel configuration.
#
# A reasonable value for this option is 300 seconds, which is the new
# Redis default starting with Redis 3.2.1.
#单位为秒，如果设置为0，则不会进行Keepalive检测，建议设置成60
tcp-keepalive 300
```

## 6. TLS/SSL

```bash
# By default, TLS/SSL is disabled. To enable it, the "tls-port" configuration
# directive can be used to define TLS-listening ports. To enable TLS on the
# default port, use:
#

# port 0
# tls-port 6379
# Configure a X.509 certificate and private key to use for authenticating the
# server to connected clients, masters or cluster peers.  These files should be
# PEM formatted.

#
# tls-cert-file redis.crt 
# tls-key-file redis.key
# Configure a DH parameters file to enable Diffie-Hellman (DH) key exchange:
#
# tls-dh-params-file redis.dh
# Configure a CA certificate(s) bundle or directory to authenticate TLS/SSL
# clients and peers.  Redis requires an explicit configuration of at least one
# of these, and will not implicitly use the system wide configuration.

#
# tls-ca-cert-file ca.crt
# tls-ca-cert-dir /etc/ssl/certs
# By default, clients (including replica servers) on a TLS port are required
# to authenticate using valid client side certificates.
#

# It is possible to disable authentication using this directive.
#

# tls-auth-clients no
# By default, a Redis replica does not attempt to establish a TLS connection
# with its master.
#

# Use the following directive to enable TLS on replication links.
#
# tls-replication yes
# By default, the Redis Cluster bus uses a plain TCP connection. To enable
# TLS for the bus protocol, use the following directive:
#

# tls-cluster yes
# Explicitly specify TLS versions to support. Allowed values are case insensitive
# and include "TLSv1", "TLSv1.1", "TLSv1.2", "TLSv1.3" (OpenSSL >= 1.1.1) or
# any combination. To enable only TLSv1.2 and TLSv1.3, use:
#

# tls-protocols "TLSv1.2 TLSv1.3"
# Configure allowed ciphers.  See the ciphers(1ssl) manpage for more information
# about the syntax of this string.
#

# Note: this configuration applies only to <= TLSv1.2.
#

# tls-ciphers DEFAULT:!MEDIUM
# Configure allowed TLSv1.3 ciphersuites.  See the ciphers(1ssl) manpage for more
# information about the syntax of this string, and specifically for TLSv1.3
# ciphersuites.

#
# tls-ciphersuites TLS_CHACHA20_POLY1305_SHA256
# When choosing a cipher, use the server's preference instead of the client
# preference. By default, the server follows the client's preference.
#

# tls-prefer-server-ciphers yes
# By default, TLS session caching is enabled to allow faster and less expensive
# reconnections by clients that support it. Use the following directive to disable
# caching.

#

# tls-session-caching no
# Change the default number of TLS sessions cached. A zero value sets the cache
# to unlimited size. The default size is 20480.

#
# tls-session-cache-size 5000
# Change the default timeout of cached TLS sessions. The default timeout is 300
# seconds.

#
# tls-session-cache-timeout 60
```

## 7. SNAPSHOTTING（快照）

```bash
#
# Save the DB on disk:
#
#   save <seconds> <changes>
#
#   Will save the DB if both the given number of seconds and the given
#   number of write operations against the DB occurred.
#

#   In the example below the behaviour will be to save:
#   after 900 sec (15 min) if at least 1 key changed
#   after 300 sec (5 min) if at least 10 keys changed
#   after 60 sec if at least 10000 keys changed
#
#   Note: you can disable saving completely by commenting out all "save" lines.
#
#   It is also possible to remove all the previously configured save
#   points by adding a save directive with a single empty string argument
#   like in the following example:
#

#持久化save格式：save <seconds> <changes>，表示在seconds秒内有changes次修改（增删改），则触发数据持久化
#禁用RDB持久化策略
save ""
#在900内有1次修改，则触发数据持久化
save 900 1
#在300内有10次修改，则触发数据持久化
save 300 10
#在60内有10000次修改，则触发数据持久化
save 60 10000

# By default Redis will stop accepting writes if RDB snapshots are enabled
# (at least one save point) and the latest background save failed.
# This will make the user aware (in a hard way) that data is not persisting
# on disk properly, otherwise chances are that no one will notice and some
# disaster will happen.
#

# If the background saving process will start working again Redis will
# automatically allow writes again.
#
# However if you have setup your proper monitoring of the Redis server
# and persistence, you may want to disable this feature so that Redis will
# continue to work as usual even if there are problems with disk,
# permissions, and so forth.

#如果后台持久化发生错误，是否停止前台数据写操作，默认开启
#如果配置成no，表示你不在乎数据不一致或者有其他的手段发现和控制
stop-writes-on-bgsave-error yes
# Compress string objects using LZF when dump .rdb databases?
# For default that's set to 'yes' as it's almost always a win.
# If you want to save some CPU in the saving child set it to 'no' but
# the dataset will likely be bigger if you have compressible values or keys.
#是否开启使用LZF算法压缩RDB文件，默认开启，开启则会增加CPU开销，但会减小持久化文件大小
rdbcompression yes
# Since version 5 of RDB a CRC64 checksum is placed at the end of the file.
# This makes the format more resistant to corruption but there is a performance
# hit to pay (around 10%) when saving and loading RDB files, so you can disable it
# for maximum performances.
#

# RDB files created with checksum disabled have a checksum of zero that will
# tell the loading code to skip the check.

#在存储RDB文件后，还可以让redis使用CRC64算法来进行数据校验，但是这样做会增加大约10%的性能消耗，如果希望获取到最大的性能提升，可以关闭此功能
rdbchecksum yes
# The filename where to dump the DB
#RDB文件的名称，默认：dump.rdb
dbfilename dump.rdb
# Remove RDB files used by replication in instances without persistence
# enabled. By default this option is disabled, however there are environments
# where for regulations or other security concerns, RDB files persisted on
# disk by masters in order to feed replicas, or stored on disk by replicas
# in order to load them for the initial synchronization, should be deleted
# ASAP. Note that this option ONLY WORKS in instances that have both AOF
# and RDB persistence disabled, otherwise is completely ignored.

#

# An alternative (and sometimes better) way to obtain the same effect is
# to use diskless replication on both master and replicas instances. However
# in the case of replicas, diskless is not always an option.
#是否删除在没有持久性的实例中复制使用的RDB文件，此选项仅在同时具有AOF的实例中有效（此配置我也不是很熟悉，注释说明来源于官网）
rdb-del-sync-files no

# The working directory.
#

# The DB will be written inside this directory, with the filename specified
# above using the 'dbfilename' configuration directive.
#
# The Append Only File will also be created inside this directory.
#
# Note that you must specify a directory here, not a file name.
#redis工作目录，默认为当前开启redis服务所在的目录
#RDB和AOF文件将再次目录生成，同时也是数据库恢复的目录
#注意，这里必须指定目录，而不是文件名
dir ./
```

## 8. Security安全

![image-20201210201131149](\images\image-20201210201131149.png)

## 9.LIMITS限制

### Maxclients

设置redis同时可以与多少个客户端进行连接。默认情况下为10000个客户端。当你
无法设置进程文件句柄限制时，redis会设置为当前的文件句柄限制值减去32，因为redis会为自
身内部处理逻辑留一些句柄出来。如果达到了此限制，redis则会拒绝新的连接请求，并且向这
些连接请求方发出“max number of clients reached”以作回应。

### Maxmemory

设置redis可以使用的内存量。一旦到达内存使用上限，redis将会试图移除内部数据，移除规则可以通过maxmemory-policy来指定。如果redis无法根据移除规则来移除内存中的数据，或者设置了“不允许移除”，
那么redis则会针对那些需要申请内存的指令返回错误信息，比如SET、LPUSH等。

但是对于无内存申请的指令，仍然会正常响应，比如GET等。如果你的redis是主redis（说明你的redis有从redis），那么在设置内存使用上限时，需要在系统中留出一些内存空间给同步队列缓存，只有在你设置的是“不移除”的情况下，才不用考虑这个因素

### Maxmemory-policy

（1）volatile-lru：使用LRU算法移除key，只对设置了过期时间的键
（2）allkeys-lru：使用LRU算法移除key
（3）volatile-random：在过期集合中移除随机的key，只对设置了过期时间的键
（4）allkeys-random：移除随机的key
（5）volatile-ttl：移除那些TTL值最小的key，即那些最近要过期的key
（6）noeviction：不进行移除。针对写操作，只是返回错误信息

### Maxmemory-samples

设置样本数量，LRU算法和最小TTL算法都并非是精确的算法，而是估算值，所以你可以设置样本的大小，
redis默认会检查这么多个key并选择其中LRU的那个

## 10. APPEND ONLY MODE追加

```bash
# By default Redis asynchronously dumps the dataset on disk. This mode is
# good enough in many applications, but an issue with the Redis process or
# a power outage may result into a few minutes of writes lost (depending on
# the configured save points).
#
# The Append Only File is an alternative persistence mode that provides
# much better durability. For instance using the default data fsync policy
# (see later in the config file) Redis can lose just one second of writes in a
# dramatic event like a server power outage, or a single write if something
# wrong with the Redis process itself happens, but the operating system is
# still running correctly.
#

# AOF and RDB persistence can be enabled at the same time without problems.
# If the AOF is enabled on startup Redis will load the AOF, that is the file
# with the better durability guarantees.

#

# Please check http://redis.io/topics/persistence for more information.
#是否开启AOF持久化，默认关闭
appendonly no
# The name of the append only file (default: "appendonly.aof")
#配置AOF文件名称，默认名称为appendonly.aof
appendfilename "appendonly.aof"
# The fsync() call tells the Operating System to actually write data on disk
# instead of waiting for more data in the output buffer. Some OS will really flush
# data on disk, some other OS will just try to do it ASAP.
#

# Redis supports three different modes:
#

# no: don't fsync, just let the OS flush the data when it wants. Faster.
# always: fsync after every write to the append only log. Slow, Safest.
# everysec: fsync only one time every second. Compromise.
#

# The default is "everysec", as that's usually the right compromise between
# speed and data safety. It's up to you to understand if you can relax this to
# "no" that will let the operating system flush the output buffer when
# it wants, for better performances (but if you can live with the idea of
# some data loss consider the default persistence mode that's snapshotting),
# or on the contrary, use "always" that's very slow but a bit safer than
# everysec.
#
# More details please check the following article:
# http://antirez.com/post/redis-persistence-demystified.html

#

# If unsure, use "everysec".

#持久化策略always模式，总是写入aof文件，并完成磁盘同步，性能较差但数据完整性比较好
appendfsync always
#持久化策略everysec模式，每一秒写入aof文件，并完成磁盘同步，如果1秒内宕机，会丢失最后一秒的数据，是相对于always和no模式的这种办法
appendfsync everysec
#持久化策略no模式，写入aof文件，不等待磁盘同步，速度最快
appendfsync no

# When the AOF fsync policy is set to always or everysec, and a background
# saving process (a background save or AOF log background rewriting) is
# performing a lot of I/O against the disk, in some Linux configurations
# Redis may block too long on the fsync() call. Note that there is no fix for
# this currently, as even performing fsync in a different thread will block
# our synchronous write(2) call.
#

# In order to mitigate this problem it's possible to use the following option
# that will prevent fsync() from being called in the main process while a
# BGSAVE or BGREWRITEAOF is in progress.
#

# This means that while another child is saving, the durability of Redis is
# the same as "appendfsync none". In practical terms, this means that it is
# possible to lose up to 30 seconds of log in the worst scenario (with the
# default Linux settings).

#

# If you have latency problems turn this to "yes". Otherwise leave it as
# "no" that is the safest pick from the point of view of durability.

#持久化策略no模式，写入aof文件，不等待磁盘同步，速度最快
# appendfsync no
#重写aof文件时，是否可以运用appendfsync配置，用默认no即可，保证数据的安全性
no-appendfsync-on-rewrite no
# Automatic rewrite of the append only file.
# Redis is able to automatically rewrite the log file implicitly calling
# BGREWRITEAOF when the AOF log size grows by the specified percentage.
#

# This is how it works: Redis remembers the size of the AOF file after the
# latest rewrite (if no rewrite has happened since the restart, the size of
# the AOF at startup is used).
#

# This base size is compared to the current size. If the current size is
# bigger than the specified percentage, the rewrite is triggered. Also
# you need to specify a minimal size for the AOF file to be rewritten, this
# is useful to avoid rewriting the AOF file even if the percentage increase
# is reached but it is still pretty small.

#

# Specify a percentage of zero in order to disable the automatic AOF
# rewrite feature.

#当aof文件大小超过上一次重写的aof文件大小的指定百分比时进行重写，即当aof文件增长到一定大小的时候Redis能够调用bgrewriteaof对日志文件进行重写。
auto-aof-rewrite-percentage 100
#允许重写的最小aof文件大小
auto-aof-rewrite-min-size 64mb

# An AOF file may be found to be truncated at the end during the Redis
# startup process, when the AOF data gets loaded back into memory.
# This may happen when the system where Redis is running
# crashes, especially when an ext4 filesystem is mounted without the
# data=ordered option (however this can't happen when Redis itself
# crashes or aborts but the operating system still works correctly).

# Redis can either exit with an error when this happens, or load as much
# data as possible (the default now) and start if the AOF file is found
# to be truncated at the end. The following option controls this behavior.

#

# If aof-load-truncated is set to yes, a truncated AOF file is loaded and
# the Redis server starts emitting a log to inform the user of the event.
# Otherwise if the option is set to no, the server aborts with an error
# and refuses to start. When the option is set to no, the user requires
# to fix the AOF file using the "redis-check-aof" utility before to restart
# the server.

#
# Note that if the AOF file will be found to be corrupted in the middle
# the server will still exit with an error. This option only applies when
# Redis will try to read more data from the AOF file but not enough bytes
# will be found.

aof-load-truncated yes

# When rewriting the AOF file, Redis is able to use an RDB preamble in the
# AOF file for faster rewrites and recoveries. When this option is turned
# on the rewritten AOF file is composed of two different stanzas:

#   [RDB file][AOF tail]
# When loading Redis recognizes that the AOF file starts with the "REDIS"
# string and loads the prefixed RDB file, and continues loading the AOF
# tail.

aof-use-rdb-preamble yes
```

## 11、常见配置redis.conf介绍

参数说明
redis.conf 配置项说明如下：
1. Redis默认不是以守护进程的方式运行，可以通过该配置项修改，使用yes启用守护进程
    daemonize no
2. 当Redis以守护进程方式运行时，Redis默认会把pid写入/var/run/redis.pid文件，可以通过pidfile指定
    pidfile /var/run/redis.pid
3. 指定Redis监听端口，默认端口为6379，作者在自己的一篇博文中解释了为什么选用6379作为默认端口，因为6379在手机按键上MERZ对应的号码，而MERZ取自意大利歌女Alessia Merz的名字
    port 6379
4. 绑定的主机地址
    bind 127.0.0.1
5.当 客户端闲置多长时间后关闭连接，如果指定为0，表示关闭该功能
    timeout 300
6. 指定日志记录级别，Redis总共支持四个级别：debug、verbose、notice、warning，默认为verbose
    loglevel verbose
7. 日志记录方式，默认为标准输出，如果配置Redis为守护进程方式运行，而这里又配置为日志记录方式为标准输出，则日志将会发送给/dev/null
    logfile stdout
8. 设置数据库的数量，默认数据库为0，可以使用SELECT <dbid>命令在连接上指定数据库id
    databases 16
9. 指定在多长时间内，有多少次更新操作，就将数据同步到数据文件，可以多个条件配合
    save <seconds> <changes>
    Redis默认配置文件中提供了三个条件：
    save 900 1
    save 300 10

# 五、Redis的持久化

## RBD

  &nbsp;     在指定的时间间隔内生成内存中整个数据集的持久化快照。快照文件默认被存储在当前文件夹中，名称为`dump.rdb`，可以通过dir和dbfilename参数来修改默认值。

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Redis会单独创建（fork）一个子进程来进行持久化，会先将数据写入到一个临时文件中，待持久化过程都结束了，再用这个临时文件替换上次持久化好的文件。&nbsp;&nbsp;整个过程中，主进程是不进行任何的IO操作的，这就确保了极高的性能。

### 配置文件

```bash
# redis是基于内存的数据库，可以通过设置该值定期写入磁盘。
# 注释掉“save”这一行配置项就可以让保存数据库功能失效
# 900秒（15分钟）内至少1个key值改变（则进行数据库保存--持久化） 
# 300秒（5分钟）内至少10个key值改变（则进行数据库保存--持久化） 
# 60秒（1分钟）内至少10000个key值改变（则进行数据库保存--持久化）

save 900 1
save 300 10
save 60 10000

#当RDB持久化出现错误后，是否依然进行继续进行工作，yes：不能进行工作，no：可以继续进行工作，可以通过info中的rdb_last_bgsave_status了解RDB持久化是否有错误
stop-writes-on-bgsave-error yes

#使用压缩rdb文件，rdb文件压缩使用LZF压缩算法，yes：压缩，但是需要一些cpu的消耗。no：不压缩，需要更多的磁盘空间
rdbcompression yes

#是否校验rdb文件。从rdb格式的第五个版本开始，在rdb文件的末尾会带上CRC64的校验和。这跟有利于文件的容错性，但是在保存rdb文件的时候，会有大概10%的性能损耗，所以如果你追求高性能，可以关闭该配置。
rdbchecksum yes
#rdb文件的名称
dbfilename dump.rdb
#数据目录，数据库的写入会在这个目录。rdb、aof文件也会写在这个目录
dir /data
```

### Fork

&nbsp;fork的作用相当于复制一个与当前进程一样的进程。但是是一个全新的进程，并作为原进程的子进程。

### 触发条件

1.通过配制文件中的save条件（可自己配置）

```shell
save 900 1
save 300 10
save 60 10000
```

2.手动通过save和bgsave命令

- save：save时只管保存，其他不管，全部阻塞
- bgsave：redis会在后台异步的进行快照操作，同时还可以响应客户端请求。可以通过lastsave命令获取最后一次成功执行快照的事件

3. 通过flushall命令，也会产生dump.rdb文件，但是里面是空的，无意义。
4. 通过shutdown命令，安全退出，也会生成快照文件（和异常退出形成对比，比如：kill杀死进程的方式）

### 如何恢复

```shell
appendonly no
dbfilename dump.rdb
dir /var/lib/redis  #可以自行指定
```

`appendonly 设置成no`，redis启动时会把/var/lib/redis 目录下的dump.rdb 中的数据恢复。dir 和dbfilename 都可以设置。我测试时`appendonly 设置成yes 时候不会将dump.rdb文件中的数据恢复`。

### 优势

1. 恢复数据的速度很快，适合大规模的数据恢复，而又对部分数据不敏感的情况
2. dump.db文件是一个压缩的二进制文件，文件暂用空间小

### 劣势

1. 当出现异常退出时，会丢失最后一次快照后的数据
2. 当fork的时候，内存的中的数据会被克隆一份，大致两倍的膨胀需要考虑。而且，当数据过大时，fork操作占用过多的系统资源，造成主服务器进程假死。

### 使用场景

1. 数据备份 
2. 可容忍部分数据丢失 
3. 跨数据中心的容灾备份

## AOF

### 介绍

以日志的形式来记录每个写操作，将Redis执行过的所有写指令记录下来（读操作补不可记录），只许追加文件但不可以改写文件，redis启动之初会读取改文件重新构建数据。保存的是appendonly.aof文件

aof机制默认关闭，可以通过`appendonly = yes`参数开启aof机制，通过`appendfilename = myaoffile.aof`指定aof文件名称。

aof持久化的一些策略配置

```shell
#aof持久化策略的配置
#no表示不执行fsync，由操作系统保证数据同步到磁盘，速度最快。
#always表示每次写入都执行fsync，以保证数据同步到磁盘。
#everysec表示每秒执行一次fsync，可能会导致丢失这1s数据。
appendfsync everysec
```

对于触发aof重写机制也可以通过配置文件来进行设置：

```bash
# aof自动重写配置。当目前aof文件大小超过上一次重写的aof文件大小的百分之多少进行重写，即当aof文件增长到一定大小的时候Redis能够调用bgrewriteaof对日志文件进行重写。当前AOF文件大小是上次日志重写得到AOF文件大小的二倍（设置为100）时，自动启动新的日志重写过程。
auto-aof-rewrite-percentage 100
# 设置允许重写的最小aof文件大小，避免了达到约定百分比但尺寸仍然很小的情况还要重写
auto-aof-rewrite-min-size 64mb
```

当aop重写时会引发重写和持久化追加同时发生的问题，可以通过`no-appendfsync-on-rewrite no`进行配置

```bash
# 在aof重写或者写入rdb文件的时候，会执行大量IO，此时对于everysec和always的aof模式来说，执行fsync会造成阻塞过长时间，no-appendfsync-on-rewrite字段设置为默认设置为no，是最安全的方式，不会丢失数据，但是要忍受阻塞的问题。如果对延迟要求很高的应用，这个字段可以设置为yes，，设置为yes表示rewrite期间对新写操作不fsync,暂时存在内存中,不会造成阻塞的问题（因为没有磁盘竞争），等rewrite完成后再写入，这个时候redis会丢失数据。Linux的默认fsync策略是30秒。可能丢失30秒数据。因此，如果应用系统无法忍受延迟，而可以容忍少量的数据丢失，则设置为yes。如果应用系统无法忍受数据丢失，则设置为no。

no-appendfsync-on-rewrite no
```

### 如何恢复

##### 正常恢复

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;将文件放到dir指定的文件夹下，当redis启动的时候会自动加载数据，注意：`aof文件的优先级比dump大`。

##### 异常恢复

- 有些操作可以直接到appendonly.aof文件里去修改。

  eg：使用了flushall这个命令，此刻持久化文件中就会有这么一条命令记录，把它删掉就可以了

- 写坏的文件可以通过 `redis-check-aof --fix`进行修复

#### 优势

1. 根据不同的策略，可以实现每秒，每一次修改操作的同步持久化，就算在最恶劣的情况下只会丢失不会超过两秒数据。

2. 当文件太大时，会触发重写机制，确保文件不会太大。
3. 文件可以简单的读懂

#### 劣势

1. aof文件的大小太大，就算有重写机制，但重写所造成的阻塞问题是不可避免的
2. aof文件恢复速度慢



### 总结

1. 如果你只希望你的数据在服务器运行的时候存在，可以不使用任何的持久化方式

2. 一般建议同时开启两种持久化方式。AOF进行数据的持久化，确保数据不会丢失太多，而RDB更适合用于备份数据库，留着一个做万一的手段。

3. 性能建议：

   因为RDB文件只用做后备用途，建议只在slave上持久化RDB文件，而且只要在15分钟备份一次就够了，只保留900 1这条规则。

   如果Enalbe AOF,好处是在最恶劣情况下也只会丢失不超过两秒数据，启动脚本较简单只load自己的AOF文件就可以了。代价：1、带来了持续的IO；2、AOF rewrite的最后将rewrite过程中产生的新数据写到新文件造成的阻塞几乎是不可避免的。只要硬盘许可，应该尽量减少AOF rewrite的频率，AOF重写的基础大小默认值64M太小了，可以设到5G以上。默认超过原大小100%大小时重写可以改到适当的数值。

   如果不Enable AOF,仅靠Master-Slave Replication 实现高可用性也可以。能省掉一大笔IO也减少了rewrite时带来的系统波动。代价是如果Master/Slave同时宕掉，会丢失10几分钟的数据，启动脚本也要比较两个Master/Slave中的RDB文件，载入较新的那个。新浪微博就选用了这种架构。

# 六、Redis的事务

### 是什么？

可以一次执行多个命令，本质是一组命令的集合。一个事物中的所有命令都会被序列化，按顺序的串行执行而不会被其他命令插入，不许加塞。

### 能干嘛？

一个队列中，一次性的，顺序的，排他的执行一系列命令。

### 常用命令

| 命令            | 描述                                                         |
| --------------- | ------------------------------------------------------------ |
| multi           | 标记一个事务的开始                                           |
| exec            | 执行所有事务块内的命令                                       |
| discard         | 取消事务，放弃执行事务块内的所有命令                         |
| watch key [key] | 监视一个(或多个) key ，如果在事务执行之前这个(或这些) key 被其他命令所改动，那么事务将被打断。 |
| unwatch         | 取消watch命令对所有 key 的监视。                             |

### 这么玩？

1. **正常执行**

   ![](\images\watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ0NzY2ODgz,size_16,color_FFFFFF,t_70)

2. 放弃事务

   

![image-20201215193424423](\images\image-20201215193424423.png)

3. 全体连坐

![image-20201215193638193](\images\image-20201215193638193.png)

4. 冤头债主

![image-20201215193734074](\images\image-20201215193734074.png)

### 乐观锁和悲观锁

#### 悲观锁

悲观锁(Pessimistic Lock), 顾名思义，就是很悲观，每次去拿数据的时候都认为别人会修改，所以每次在拿数据的时候都会上锁，这样别人想拿这个数据就会block直到它拿到锁。传统的关系型数据库里边就用到了很多这种锁机制，比如行锁，表锁等，读锁，写锁等，都是在做操作之前先上锁

#### 乐观锁

 乐观锁(Optimistic Lock), 顾名思义，就是很乐观，每次去拿数据的时候都认为别人不会修改，所以不会上锁，但是在更新的时候会判断一下在此期间别人有没有去更新这个数据，可以使用版本号等机制。乐观锁适用于多读的应用类型，这样可以提高吞吐量。

乐观锁策略:提交版本必须大于记录当前版本才能执行更新

### Watch监控

watch指令，`类似乐观锁`，如果key的值已经被修改了，那么**整个事务队列都不会被执行**,同时返回一个Nullmulti-bulk应答以通知调用者事务执行失败。

注意：**一旦执行了exec或者discard，之前加的所有监控锁都会被取消掉了。**

例子：

初始化信用卡的可用余额和欠额

![image-20201215200248403](\images\image-20201215200248403.png)

无加塞篡改

![image-20201215200341648](\images\image-20201215200341648.png)

有加塞篡改，当watch的key被修改，后面的那个事务全部执行失败

![image-20201215200428487](\images\image-20201215200428487.png)

unwatch

![image-20201215200600009](\images\image-20201215200600009.png)

#### 小结

​    Watch指令，类似乐观锁，事务提交时，如果Key的值已被别的客户端改变，比如某个list已被别的客户端push/pop过了，整个事务队列都不会被执行

​    通过WATCH命令在事务执行之前监控了多个Keys，倘若在WATCH之后有任何Key的值发生了变化，

​    EXEC命令执行的事务都将被放弃，同时返回Nullmulti-bulk应答以通知调用者事务执行失败

### 3阶段

开启:以multi开启事务

入队:将多个命令入队到事务中,接到这些命令不会立刻执行,而是放到等待执行的事务队列里面

执行：有exec命令触发事务

![image-20201215202452329](\images\image-20201215202452329.png)

### 3特性

单独的隔离操作：事务中的所有命令都会序列化，按顺序的执行。事务在等待执行的时候，不会被其他客户端发送来的米命令请求打断

没有隔离级别的概念：队列中的所有命令没有提交exec之前都是不会被执行的

不保证原子性：redis中如果一条命令执行失败，其后的命令仍然会被执行，没有回滚，参考冤头债主

# 七、Redis的复制（Master/Slave）

### 是什么？

​	就是我们常说的主从复制，主机数据更新后根据配置和策略，自动同步到备机的master/slaver机制，Master以写为主，Slave以读为主

### 能干嘛？

​	`读写分离`

​    `容灾恢复`

### 怎么玩？

配从(库)不配主(库)

从库配置

```shell
#配置从库
slaveof 主库ip 主库端口
#查看主从信息
info replication
```

每次与master断开后，都需要重新连接，除非你配置进redis.conf文件

### 常用的主从方式

#### 一主二仆

含义：就是一个Master两个Slave

![image-20201215202902880](\images\image-20201215202902880.png)

通过`info replication`查看主从信息

```shell
# Replication
role:master
connected_slaves:0
master_replid:f6baff9abfda12ca58048cfce4b0e2c1f4683da1
master_replid2:e8fe596d47d9d1d923d56d884b28128b78d2c1e0
master_repl_offset:0
second_repl_offset:1
repl_backlog_active:0
repl_backlog_size:1048576
repl_backlog_first_byte_offset:0
repl_backlog_histlen:0
```

```shell
# Replication
role:slave
master_host:127.0.0.1
master_port:6379
master_link_status:down
master_last_io_seconds_ago:-1
master_sync_in_progress:0
slave_repl_offset:0
master_link_down_since_seconds:1585217521
slave_priority:100
slave_read_only:1
connected_slaves:0
master_replid:adbec19afa734e84a333b07ea2f33c43c73fe743
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:0
second_repl_offset:-1
repl_backlog_active:0
repl_backlog_size:1048576
repl_backlog_first_byte_offset:0
repl_backlog_histlen:0
```

注意：

1. 第一次slave1 和slave2切入点，是全量复制，之后是增量复制

2. 主机可以写，但是从机不可以写，从机只能读
3. 主机shutdowm后从机待机状态，等主机回来后，主机新增记录从机可以顺利复制 
4. 从机shutdowm后，每次与master断开之后，都需要重新连接，除非你配置进redis.conf文件
5. 从机复制到的数据，会被本机持久化。就算shutdown断开连接依然会有数据。
6. 重新连接或者变更master，会清除之前的数据，重新建立拷贝最新的数据

#### 薪火相传

含义:就是上一个Slave可以是下一个slave的Master，Slave同样可以接收其他slaves的连接和同步请求，那么该slave作为了链条中下一个的master,可以有效减轻master的写压力。

![image-20201215203025426](\images\image-20201215203025426.png)

`注意事项和一主二仆差不多,但注意虽然有slave是相对master，但是依然是slave`

#### 反客为主

```shell    
SLAVEOF no one
```

 使当前数据库停止与其他数据库的同步，转成主数据库

#### 哨兵模式（sentinel）

反客为主的自动版，能够后台监控Master库是否故障，如果故障了根据投票数自动将slave库转换为主库。一组sentinel能

同时监控多个Master。

使用步骤：

1. 在Master对应redis.conf同目录下新建sentinel.conf文件，名字绝对不能错；

2. 配置哨兵，在sentinel.conf文件中填入内容(可以配置多个)：

   ```shell
   #说明：最后一个数字1，表示主机挂掉后slave投票看让谁接替成为主机，得票数多少后成为主机。
   sentinel monitor 被监控数据库名字（自己起名字） ip port 1
   ```

3. 启动哨兵模式(路径按照自己的需求进行配置)：

   ```shell
   redis-sentinel  /myredis/sentinel.conf
   ```

注意：

1. 当master挂掉后，会通过选票进行选出下一个master。而且只有使用了sentinel.conf启动的才能开启选票

2. 当原来的master后来后，很不幸变成了slave。

#### 复制原理

1. Slave启动成功连接到master后会发送一个sync命令；

2. Master接到命令启动后的存盘进程，同时收集所有接收到的用于修改数据集命令，在后台进程执行完毕之后，master

   将传送整个数据文件到slave，以完成一次完全同步；

3. `全量复制`：而slave服务在数据库文件数据后，将其存盘并加载到内存中；

4. `增量复制`：Master继续将新的所有收集到的修改命令依次传给slave，完成同步；

5. 但是只要是重新连接master，一次完全同步（全量复制）将被自动执行。

### 复制的缺点

​       延时，由于所有的写操作都是在Master上操作，然后同步更新到Slave上，所以从Master同步到Slave机器有一定的延迟，当系统很繁忙的时候，延迟问题会更加严重，Slave机器数量的增加也会使得这个问题更加严重。


### 命令

| 命令                                                         | 作用                                             |
| ------------------------------------------------------------ | ------------------------------------------------ |
| slaveof 主库ip  主库端口                                     | 配置从库                                         |
| info replication                                             | 查看redis主从复制的情况                          |
| slaveof  no one                                              | 使当前数据库停止与其他数据库的同步，转成主数据库 |
| sentinel monitor 被监控数据库名字(自己起名字) 127.0.0.1 6379 1 | 配置哨兵，监视master                             |
| redis-sentinel /myredis/sentinel.conf                        | 以哨兵模式启动redis                              |

# 八、Redis集群

### 什么是Redis集群？

Redis集群实现了对Redis的水平扩容，即启动N个redis节点，将整个数据库分布存储在这N个节点中，每个节点存储总数据的1/N

Redis集群通过分区（partition）来提供一定程度的可用性（availability）：即使集群中有一部分节点失效或者无法进行通讯，集群也可以继续处理命令请求。

### 集群搭建

[搭建看这篇文章,有效](http://codekiller.top/2020/03/30/redis-cluster/)

```mermaid
graph LR
yi((导入安装包))-->er((修改配置文件))
er((修改配置文件))-->san((创建基本镜像))
san-->si((创建节点镜像))
si-->|启动6个容器|wu((进入一个redis-cli))
wu-->|cluster meet|liu((集群添加节点))
liu-->qi((配置槽点))
qi-->ba((配置主从高可用))
```

### 集群命令



```bash
CLUSTER INFO 打印集群的信息 
CLUSTER NODES 列出集群当前已知的所有节点（node），以及这些节点的相关信息。  

//节点(node) 
CLUSTER MEET <ip> <port> 将 ip 和 port 所指定的节点添加到集群当中，让它成为集群的一份子。 
CLUSTER FORGET <node_id> 从集群中移除 node_id 指定的节点。 
CLUSTER REPLICATE <node_id> 将当前节点设置为 node_id 指定的节点的从节点。 
CLUSTER SAVECONFIG 将节点的配置文件保存到硬盘里面。  

//槽(slot) 
CLUSTER ADDSLOTS <slot> [slot ...] 将一个或多个槽（slot）指派（assign）给当前节点。 
CLUSTER DELSLOTS <slot> [slot ...] 移除一个或多个槽对当前节点的指派。 
CLUSTER FLUSHSLOTS 移除指派给当前节点的所有槽，让当前节点变成一个没有指派任何槽的节点。 
CLUSTER SETSLOT <slot> NODE <node_id> 将槽 slot 指派给 node_id 指定的节点，如果槽已经指派给另一个节点，那么先让另一个节点删除该槽>，然后再进行指派。 
CLUSTER SETSLOT <slot> MIGRATING <node_id> 将本节点的槽 slot 迁移到 node_id 指定的节点中。 
CLUSTER SETSLOT <slot> IMPORTING <node_id> 从 node_id 指定的节点中导入槽 slot 到本节点。 
CLUSTER SETSLOT <slot> STABLE 取消对槽 slot 的导入（import）或者迁移（migrate）。  

//键 (key) 
CLUSTER KEYSLOT <key> 计算键 key 应该被放置在哪个槽上。 
CLUSTER COUNTKEYSINSLOT <slot> 返回槽 slot 目前包含的键值对数量。 
CLUSTER GETKEYSINSLOT <slot> <count> 返回 count 个 slot 槽中的键。
```

### 节点

1. 一个集群至少要有三个主节点，即要有六个节点。

2. 分配原则尽量保证每个主数据库运行在不同的ip地址，每个从库和主库不在一个ip地址。

3. 当主节点崩了，从节点能自动升为主节点；当主节点再次恢复时，主节点变为slave。参考哨兵模式。

4. redis.conf有个参数cluster-require-full-coverage

   ```shell
   #默认情况下，集群全部的slot有节点负责，集群状态才为ok，才能提供服务。设置为no，可以在slot没有全部分配的时候提供服务。不建议打开该配置。
   # cluster-require-full-coverage yes
   ```


### SLOTS

- 一个Redis 集群包含16384个插槽(hash slot)， 数据库中的每个键都属于这16384个插槽的其中一个，集群使用公式CRC1 6(key)% 16384来计算键key属于哪个槽(如果有组的话就只算组的部分)，其中`CRC16(key)`语句用于计算键key的CRC16校验和。

- 集群中的每个节点负责处理一部分插槽。 举个例子， 如果一个集群可以有主节点。其中:
  - 节点A负责处理0号至5500号插槽
  - 节点B负责处理5501号至11000号插槽
  - 节点C负责处理11001号至16383号插槽

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(注意：每个节点分配的插槽具体数字可能不同，当然可以通过一个小脚本来指定)

**一个疑问：为什么是16384(2^14)，而不是65535(2^16)呢？**

在redis节点发送心跳包时需要把所有的槽放到这个心跳包里，以便让节点知道当前集群信息，16384=16k，在发送心跳包时使用char进行bitmap压缩后是2kb（16384÷8÷1024=2kb），也就是说使用2k的空间创建了16k的槽数65535=65k，压缩后就是8kb（65536÷8÷1024=8kb），也就是说需要需要8k的心跳包。

### Redis Cluster原理

1. node1和node2首先进行握手meet，知道彼此的存在
2. 握手成功后，两个节点会定期发送ping/pong消息，交换数据信息(消息头，消息体)
3. 消息头里面有个字段：unsigned char myslots[CLUSTER_SLOTS/8]，每一位代表一个槽，如果该位是1，代表该槽属于这个节点
4. 消息体中会携带一定数量的其他节点的信息，大约占集群节点总数量的十分之一，至少是3个节点的信息。节点数量越多，消息体内容越大。
5. 每秒都在发送ping消息。每秒随机选取5个节点，找出最久没有通信的节点发送ping消息。
6. 每100毫秒都会扫描本地节点列表，如果发现节点最近一次接受pong消息的时间大于cluster-node-timeout/2,则立即发送ping消息

redis集群的主节点数量基本不可能超过1000个，超过的话可能会导致网络拥堵。

### 在集群中录入值(组的概念)

redis-cli客户端提供-c参数实现自动重定向

```shell
redis-cli -c -p 6379
```

不在一个slot下的键值，是不能使用mget，mset等多键操作

可以通过{}来定义`组的概念`，从而使key中{}内相同内容的键值对放到一个slot中去。

```shell
set user:{info}:name xxx
set age{info} 12
set {info}email 12345@qq.com
hset user{info} name jiang
hset user{info} age 19
hset user{info} eamil 12345@qq.com

#结果
172.17.0.3:6379> keys *
1) "user{info}"
2) "{info}email"
3) "user:{info}:name"
4) "age{info}"
------------------------------------------------------
172.17.0.3:6379> hkeys user{info}
1) "name"
2) "age"
3) "eamil"
```

# 九、Redis的Java客户端Jedis

### Jedis所需要的jar包

Commons-pool-1.6.jar

Jedis-2.1.0.jar

### Jedis常用操作

#### 测试连通性

```java
public class Demo01 {
  public static void main(String[] args) {
    //连接本地的 Redis 服务
    Jedis jedis = new Jedis("127.0.0.1",6379);
    //查看服务是否运行，打出pong表示OK
    System.out.println("connection is OK==========>: "+jedis.ping());
  }
}
```

#### 5+1

```java
public class Test02
{
    public static void main(String[] args) {
        Jedis jedis = new Jedis("127.0.0.1",6379);
        //key
        Set<String> keys = jedis.keys("*");
        for (Iterator iterator = keys.iterator(); iterator.hasNext();) {
            String key = (String) iterator.next();
            System.out.println(key);
        }
        System.out.println("jedis.exists====>"+jedis.exists("k2"));
        System.out.println(jedis.ttl("k1"));
        //String
        //jedis.append("k1","myreids");
        System.out.println(jedis.get("k1"));
        jedis.set("k4","k4_redis");
        System.out.println("----------------------------------------");
        jedis.mset("str1","v1","str2","v2","str3","v3");
        System.out.println(jedis.mget("str1","str2","str3"));
        //list
        System.out.println("----------------------------------------");
        //jedis.lpush("mylist","v1","v2","v3","v4","v5");
        List<String> list = jedis.lrange("mylist",0,-1);
        for (String element : list) {
            System.out.println(element);
        }
        //set
        jedis.sadd("orders","jd001");
        jedis.sadd("orders","jd002");
        jedis.sadd("orders","jd003");
        Set<String> set1 = jedis.smembers("orders");
        for (Iterator iterator = set1.iterator(); iterator.hasNext();) {
            String string = (String) iterator.next();
            System.out.println(string);
        }
        jedis.srem("orders","jd002");
        System.out.println(jedis.smembers("orders").size());
        //hash
        jedis.hset("hash1","userName","lisi");
        System.out.println(jedis.hget("hash1","userName"));
        Map<String,String> map = new HashMap<String,String>();
        map.put("telphone","13811814763");
        map.put("address","atguigu");
        map.put("email","abc@163.com");
        jedis.hmset("hash2",map);
        List<String> result = jedis.hmget("hash2", "telphone","email");
        for (String element : result) {
            System.out.println(element);
        }
        //zset
        jedis.zadd("zset01",60d,"v1");
        jedis.zadd("zset01",70d,"v2");
        jedis.zadd("zset01",80d,"v3");
        jedis.zadd("zset01",90d,"v4");

        Set<String> s1 = jedis.zrange("zset01",0,-1);
        for (Iterator iterator = s1.iterator(); iterator.hasNext();) {
            String string = (String) iterator.next();
            System.out.println(string);
        }
    }
}
```

#### 事务提交

日常

```java
import redis.clients.jedis.Jedis;
import redis.clients.jedis.Response;
import redis.clients.jedis.Transaction;

public class Test03 {
    public static void main(String[] args) {
        Jedis jedis = new Jedis("127.0.0.1",6379);

        //监控key，如果该动了事务就被放弃
     /*3
     jedis.watch("serialNum");
     jedis.set("serialNum","s#####################");
     jedis.unwatch();*/

        Transaction transaction = jedis.multi();//被当作一个命令进行执行
        Response<String> response = transaction.get("serialNum");
        transaction.set("serialNum","s002");
        response = transaction.get("serialNum");
        transaction.lpush("list3","a");
        transaction.lpush("list3","b");
        transaction.lpush("list3","c");

        transaction.exec();
        //2 transaction.discard();
        System.out.println("serialNum***********"+response.get());
    }
}
 
```

加锁

```java
public class TestTransaction {
    public boolean transMethod() {
        Jedis jedis = new Jedis("127.0.0.1", 6379);
        int balance;// 可用余额
        int debt;// 欠额
        int amtToSubtract = 10;// 实刷额度

        jedis.watch("balance");
        //jedis.set("balance","5");//此句不该出现，讲课方便。模拟其他程序已经修改了该条目
        balance = Integer.parseInt(jedis.get("balance"));
        if (balance < amtToSubtract) {
            jedis.unwatch();
            System.out.println("modify");
            return false;
        } else {
            System.out.println("***********transaction");
            Transaction transaction = jedis.multi();
            transaction.decrBy("balance", amtToSubtract);
            transaction.incrBy("debt", amtToSubtract);
            transaction.exec();
            balance = Integer.parseInt(jedis.get("balance"));
            debt = Integer.parseInt(jedis.get("debt"));
            System.out.println("*******" + balance);
            System.out.println("*******" + debt);
            return true;
        }
    }
    /**
     * 通俗点讲，watch命令就是标记一个键，如果标记了一个键， 在提交事务前如果该键被别人修改过，那事务就会失败，这种情况通常可以在程序中
     * 重新再尝试一次。
     * 首先标记了键balance，然后检查余额是否足够，不足就取消标记，并不做扣减； 足够的话，就启动事务进行更新操作，
     * 如果在此期间键balance被其它人修改， 那在提交事务（执行exec）时就会报错， 程序中通常可以捕获这类错误再重新执行一次，直到成功。
     */
    public static void main(String[] args) {
        TestTransaction test = new TestTransaction();
        boolean retValue = test.transMethod();
        System.out.println("main retValue-------: " + retValue);
    }
}
 
```

#### 主从复制

```java
public static void main(String[] args) throws InterruptedException
    {
        Jedis jedis_M = new Jedis("127.0.0.1",6379);
        Jedis jedis_S = new Jedis("127.0.0.1",6380);

        jedis_S.slaveof("127.0.0.1",6379);

        jedis_M.set("k6","v6");
        Thread.sleep(500);
        System.out.println(jedis_S.get("k6"));
   }
          
```

### JedisPool

获取Jedis实例需要从JedisPool中获取

用完Jedis实例需要返还给JedisPool

如果Jedis在使用过程中出错，则也需要还给JedisPool

#### 案例见代码

JedisPoolUtil

```java
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

public class JedisPoolUtil {
    private static volatile JedisPool jedisPool = null;//被volatile修饰的变量不会被本地线程缓存，对该变量的读写都是直接操作共享内存。
    private JedisPoolUtil() {}
    
    public static JedisPool getJedisPoolInstance() {
        if(null == jedisPool) {
            synchronized (JedisPoolUtil.class) {
                if(null == jedisPool) {
                    JedisPoolConfig poolConfig = new JedisPoolConfig();
                    poolConfig.setMaxActive(1000);
                    poolConfig.setMaxIdle(32);
                    poolConfig.setMaxWait(100*1000);
                    poolConfig.setTestOnBorrow(true);
                    jedisPool = new JedisPool(poolConfig,"127.0.0.1");
                }
            }
        }
        return jedisPool;
    }

    public static void release(JedisPool jedisPool,Jedis jedis) {
        if(null != jedis) {
            jedisPool.returnResourceObject(jedis);
        }
    }
}
```

Demo5

```java
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

public class Test01 {
    public static void main(String[] args) {
        JedisPool jedisPool = JedisPoolUtil.getJedisPoolInstance();
        Jedis jedis = null;
        try {
            jedis = jedisPool.getResource();
            jedis.set("k18","v183");

        } catch (Exception e) {
            e.printStackTrace();
        }finally{
            JedisPoolUtil.release(jedisPool, jedis);
        }
    }
}
```

#### 配置总结all

```
edisPool的配置参数大部分是由JedisPoolConfig的对应项来赋值的。

maxActive：控制一个pool可分配多少个jedis实例，通过pool.getResource()来获取；如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted。

maxIdle：控制一个pool最多有多少个状态为idle(空闲)的jedis实例；
 whenExhaustedAction：表示当pool中的jedis实例都被allocated完时，pool要采取的操作；默认有三种。
 WHEN_EXHAUSTED_FAIL --> 表示无jedis实例时，直接抛出NoSuchElementException；
 WHEN_EXHAUSTED_BLOCK --> 则表示阻塞住，或者达到maxWait时抛出JedisConnectionException；
 WHEN_EXHAUSTED_GROW --> 则表示新建一个jedis实例，也就说设置的maxActive无用；
 
maxWait：表示当borrow一个jedis实例时，最大的等待时间，如果超过等待时间，则直接抛JedisConnectionException；

testOnBorrow：获得一个jedis实例的时候是否检查连接可用性（ping()）；如果为true，则得到的jedis实例均是可用的；

testOnReturn：return 一个jedis实例给pool时，是否检查连接可用性（ping()）；

testWhileIdle：如果为true，表示有一个idle object evitor线程对idle object进行扫描，如果validate失败，此object会被从pool中drop掉；这一项只有在timeBetweenEvictionRunsMillis大于0时才有意义；

timeBetweenEvictionRunsMillis：表示idle object evitor两次扫描之间要sleep的毫秒数；

numTestsPerEvictionRun：表示idle object evitor每次扫描的最多的对象数；

minEvictableIdleTimeMillis：表示一个对象至少停留在idle状态的最短时间，然后才能被idle object evitor扫描并驱逐；这一项只有在timeBetweenEvictionRunsMillis大于0时才有意义；

softMinEvictableIdleTimeMillis：在minEvictableIdleTimeMillis基础上，加入了至少minIdle个对象已经在pool里面了。如果为-1，evicted不会根据idle time驱逐任何对象。如果minEvictableIdleTimeMillis>0，则此项设置无意义，且只有在timeBetweenEvictionRunsMillis大于0时才有意义；

lifo：borrowObject返回对象时，是采用DEFAULT_LIFO（last in first out，即类似cache的最频繁使用队列），如果为False，则表示FIFO队列；

==================================================================================================================
其中JedisPoolConfig对一些参数的默认设置如下：
testWhileIdle=true
minEvictableIdleTimeMills=60000
timeBetweenEvictionRunsMillis=30000
numTestsPerEvictionRun=-1
```

