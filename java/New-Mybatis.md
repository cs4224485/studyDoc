# 一、MyBatis简介

MyBatis 是支持定制化 SQL、存储过程以及高级 映射的优秀的持久层框架。

MyBatis 避免了几乎所有的 JDBC 代码和手动设 置参数以及获取结果集。 

 MyBatis可以使用简单的XML或注解用于配置和原 始映射，将接口和Java的POJO（Plain Old Java Objects，普通的Java对象）映射成数据库中的记录.

## 1、引入依赖

```xml
<dependency>
	<groupId>junit</groupId>
	<artifactId>junit</artifactId>
	<version>4.11</version>
</dependency>
<dependency>
	<groupId>org.mybatis</groupId>
	<artifactId>mybatis</artifactId>
	<version>3.5.2</version>
</dependency>
<dependency>
	<groupId>mysql</groupId>
	<artifactId>mysql-connector-java</artifactId>
	<version>8.0.17</version>
</dependency>
<dependency>
	<groupId>log4j</groupId>
	<artifactId>log4j</artifactId>
	<version>1.2.17</version>
</dependency>
```

除了mybatis的jar包之外，为了方便调试，这里要使用junit，其相关依赖jar包在你使用骨架创建maven项目的时候会自动加入的。
另外还需要在pom.xml文件中的build标签下添加：

```xml
<resources>
	<resource>
		<directory>src/main/java</directory>
		<includes>
			<include>**/*.xml</include>
		</includes>
	</resource>
</resources>
```

## 2、创建一张表

```sql
CREATE TABLE tbl_employee(
id INT(11) PRIMARY KEY AUTO_INCREMENT,
last_name VARCHAR(2555),
gender CHAR(1),
email VARCHAR(255)
)
```

## 3、Java Bean

```java
public class Employee {

    private Integer id;
    private String lastName;
    private String email;
    private String gender;

    public Integer getId() {
        return id;
    }
```

## 4、添加mybatis的主配置文件

主配置文件的名称同样也是可以随意命名的，这里就将其命名为mybatis.xml，将这个配置文件放到maven项目中的resources目录下

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://192.168.0.110:3306/TestMyBatis?useSSL=false"/>
                <property name="username" value="root"/>
                <property name="password" value="123456"/>
            </dataSource>
        </environment>
    </environments>
    <mappers>
        <!--注册映射文件-->
        <mapper resource="com\harry\mybatis\Bean\Dao\mapper\EmployeeMapper.xml"/>
    </mappers>
</configuration>
```

## 5、定义一个dao的接口：

```java
public interface EmployeeDao {
    List<Employee> selectEmployees();

    Employee selectEmployeeById(int id);
}
```

## 6、添加Mapping映射文件

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.harry.mybatis.Bean.Dao.EmployeeDao">
    <!--parameterType可省略-->
    <select id="selectEmployees"  resultType="com.harry.mybatis.Bean.Employee">
        SELECT * FROM tbl_employee
    </select>

    <select id="selectEmployeeById" resultType="com.harry.mybatis.Bean.Employee">
        SELECT * FROM tbl_employee WHERE id = #{id}
    </select>
</mapper>
```

## 7、Test

```java
public class MyBatisTest {
    public static void main(String[] args) {
        String resource = "mybatis.xml";
        //读取主配置文件
        InputStream stream = null;
        SqlSession sqlSession = null;
        try {
            stream = Resources.getResourceAsStream(resource);
            //创建SqlSessionFactory对象
            SqlSessionFactory sessionFactory = new SqlSessionFactoryBuilder().build(stream);
            //创建SqlSession对象
            sqlSession = sessionFactory.openSession();
            Employee employee = sqlSession.selectOne("selectEmployeeById", 1);
            System.out.println(employee);
            List<Employee> employees = sqlSession.selectList("selectEmployees");
            for (int i = 0; i < employees.size(); i++) {
                System.out.println(employees.get(i));
            }

        } catch (IOException e) {
            e.printStackTrace();
        }finally {
            sqlSession.close();
        }

    }
}
```

测试2 使用接口式编程

```java
public class MyBatisTest {
    public static void main(String[] args) {
        String resource = "mybatis.xml";
        //读取主配置文件
        InputStream stream = null;
        SqlSession sqlSession = null;
        try {
            stream = Resources.getResourceAsStream(resource);
            //创建SqlSessionFactory对象
            SqlSessionFactory sessionFactory = new SqlSessionFactoryBuilder().build(stream);
            //创建SqlSession对象
            sqlSession = sessionFactory.openSession();
            EmployeeDao employeeDao = sqlSession.getMapper(EmployeeDao.class);
            Employee employee = employeeDao.selectEmployeeById(2);
            System.out.println(employee);
            List<Employee> employees = employeeDao.selectEmployees();
            for (int i = 0; i < employees.size(); i++) {
                System.out.println(employees.get(i));
            }

        } catch (IOException e) {
            e.printStackTrace();
        }finally {
            sqlSession.close();
        }

    }
}
```

8、小结

>   1、接口式编程
>   	原生：		Dao		====>  DaoImpl
>   	mybatis：	Mapper	====>  xxMapper.xml
>   2、SqlSession代表和数据库的一次会话；用完必须关闭；
>   3、SqlSession和connection一样她都是非线程安全。每次使用都应该去获取新的对象。
>   4、mapper接口没有实现类，但是mybatis会为这个接口生成一个代理对象。
>   		（将接口和xml进行绑定）
>   		EmployeeMapper empMapper =	sqlSession.getMapper(EmployeeMapper.class);
>   5、两个重要的配置文件：
>   		mybatis的全局配置文件：包含数据库连接池信息，事务管理器信息等...系统运行环境信息
>   		sql映射文件：保存了每一个sql语句的映射信息：将sql抽取出来。	

# 二、MyBatis-全局配置文件

MyBatis 的配置文件包含了影响 MyBatis 行为甚深的 设置（settings）和属性（properties）信息。

## 1、properties属性

如果属性在不只一个地方进行了配置，那么 MyBatis 将按 照下面的顺序来加载：

​	在 properties 元素体内指定的属性首先被读取。 

​	然后根据 properties 元素中的 resource 属性读取类路径下属性文件或根 据 url 属性指定的路径读取属性文件，并覆盖已读取的同名属性。

   最后读取作为方法参数传递的属性，并覆盖已读取的同名属性。

```xml
<!--
	1、mybatis可以使用properties来引入外部properties配置文件的内容；
	resource：引入类路径下的资源
	url：引入网络路径或者磁盘路径下的资源
  -->
<properties resource="dbconfig.properties"></properties>

<environments default="dev_mysql">
	<environment id="dev_mysql">
		<transactionManager type="JDBC"></transactionManager>
		<dataSource type="POOLED">
			<property name="driver" value="${jdbc.driver}" />
			<property name="url" value="${jdbc.url}" />
			<property name="username" value="${jdbc.username}" />
			<property name="password" value="${jdbc.password}" />
		</dataSource>
	</environment>

	<environment id="dev_oracle">
		<transactionManager type="JDBC" />
		<dataSource type="POOLED">
			<property name="driver" value="${orcl.driver}" />
			<property name="url" value="${orcl.url}" />
			<property name="username" value="${orcl.username}" />
			<property name="password" value="${orcl.password}" />
		</dataSource>
	</environment>
</environments>

```
## 2、settings设置

这是 MyBatis 中极为重要的调整设置，它们会改变 MyBatis 的运行时行为。

![image-20200621101616348](\images\image-20200621101616348.png)

```xml
<settings>
	<setting name="mapUnderscoreToCamelCase" value="true"/>
</settings>
```

## 3、typeAliases别名处理器

类型别名是为 Java 类型设置一个短的名字，可以方便我们 引用某个类。

类很多的情况下，可以批量设置别名这个包下的每一个类 创建一个默认的别名，就是简单类名小写。

```xml
<typeAliases>
	<!-- 1、typeAlias:为某个java类型起别名
			type:指定要起别名的类型全类名;默认别名就是类名小写；employee
			alias:指定新的别名
	 -->
	<!-- <typeAlias type="com.harry.mybatis.bean.Employee" alias="emp"/> -->
	
	<!-- 2、package:为某个包下的所有类批量起别名 
			name：指定包名（为当前包以及下面所有的后代包的每一个类都起一个默认别名（类名小写），）
	-->
	<package name="com.harry.mybatis.bean"/>
	
	<!-- 3、批量起别名的情况下，使用@Alias注解为某个类型指定新的别名 -->
</typeAliases>
```
值得注意的是，MyBatis已经为许多常见的 Java 类型内建 了相应的类型别名。它们都是大小写不敏感的，我们在起 别名的时候千万不要占用已有的别名。

![image-20200621102039441](\images\image-20200621102039441.png)

## 4、typeHandlers类型处理器

无论是 MyBatis 在预处理语句（PreparedStatement）中 设置一个参数时，还是从结果集中取出一个值时， 都会 用类型处理器将获取的值以合适的方式转换成 Java 类型。

![image-20200621102139771](\images\image-20200621102139771.png)

## 5、plugins插件

插件是MyBatis提供的一个非常强大的机制，我们可以通过插件来修改MyBatis的一些核心行为。插件通过动态代理机制，可以介入四大对象的任何 一个方法的执行。

Executor (update, query, flushStatements, commit, rollback, getTransaction, close, isClosed)

ParameterHandler (getParameterObject, setParameters) 

ResultSetHandler (handleResultSets, handleOutputParameters) 

StatementHandler (prepare, parameterize, batch, update, query) 

## 6、environments环境

MyBatis可以配置多种环境，比如开发、测试和生 产环境需要有不同的配置。

每种环境使用一个environment标签进行配置并指 定唯一标识符

可以通过environments标签中的default属性指定 一个环境的标识符来快速的切换环境

```xml
<!-- 
environment：配置一个具体的环境信息；必须有两个标签；id代表当前环境的唯一标识
	transactionManager：事务管理器；
		type：事务管理器的型;JDBC(JdbcTransactionFactory)|MANAGED(ManagedTransactionFactory)
			自定义事务管理器：实现TransactionFactory接口.type指定为全类名
	dataSource：数据源;
		type:数据源类型;UNPOOLED(UnpooledDataSourceFactory)
					|POOLED(PooledDataSourceFactory)
					|JNDI(JndiDataSourceFactory)
		自定义数据源：实现DataSourceFactory接口，type是全类名
-->
<environments default="dev_mysql">
	<environment id="dev_mysql">
		<transactionManager type="JDBC"></transactionManager>
		<dataSource type="POOLED">
			<property name="driver" value="${jdbc.driver}" />
			<property name="url" value="${jdbc.url}" />
			<property name="username" value="${jdbc.username}" />
			<property name="password" value="${jdbc.password}" />
		</dataSource>
	</environment>

	<environment id="dev_oracle">
		<transactionManager type="JDBC" />
		<dataSource type="POOLED">
			<property name="driver" value="${orcl.driver}" />
			<property name="url" value="${orcl.url}" />
			<property name="username" value="${orcl.username}" />
			<property name="password" value="${orcl.password}" />
		</dataSource>
	</environment>
</environments>
```
## 7、databaseIdProvider环境

MyBatis 可以根据不同的数据库厂商执行不同的语句。

```xml
<databaseIdProvider type="DB_VENDOR">
	<!-- 为不同的数据库厂商起别名 -->
	<property name="MySQL" value="mysql"/>
	<property name="Oracle" value="oracle"/>
	<property name="SQL Server" value="sqlserver"/>
</databaseIdProvider>
```

```xml
<select id="selectEmployeeById" resultType="com.harry.mybatis.Bean.Employee" databaseId="mysql">
    SELECT * FROM tbl_employee WHERE id = #{id}
</select>
```

MyBatis匹配规则如下：

1、如果没有配置databaseIdProvider标签，那么databaseId=null

2、如果配置了databaseIdProvider标签，使用标签配置的name去匹配数据库信息，匹配上设置databaseId=配置指定的值，否则依旧为 null

3、如果databaseId不为null，他只会找到配置databaseId的sql语句

4、MyBatis 会加载不带 databaseId 属性和带有匹配当前数据库 databaseId 属性的所有语句。如果同时找到带有 databaseId和不带 databaseId 的相同语句，则后者会被舍弃

## 8、mapper映射

mapper逐个注册SQL映射文件

```xml
<mappers>
	<!-- 
		mapper:注册一个sql映射 
			注册配置文件
			resource：引用类路径下的sql映射文件
				mybatis/mapper/EmployeeMapper.xml
			url：引用网路路径或者磁盘路径下的sql映射文件
				file:///var/mappers/AuthorMapper.xml
				
			注册接口
			class：引用（注册）接口，
				1、有sql映射文件，映射文件名必须和接口同名，并且放在与接口同一目录下；
				2、没有sql映射文件，所有的sql都是利用注解写在接口上;
				推荐：
					比较重要的，复杂的Dao接口我们来写sql映射文件
					不重要，简单的Dao接口为了开发快速可以使用注解；
	-->
	<!-- <mapper resource="mybatis/mapper/EmployeeMapper.xml"/> -->
	<!-- <mapper class="com.atguigu.mybatis.dao.EmployeeMapperAnnotation"/> -->
	
	<!-- 批量注册： -->
	<package name="com.atguigu.mybatis.dao"/>
</mappers>
```
# 三、MyBatis-映射文件

映射文件指导着MyBatis如何进行数据库增删改查， 有着非常重要的意义；

cache –命名空间的二级缓存配置 

cache-ref – 其他命名空间缓存配置的引用。 

resultMap – 自定义结果集映射 

parameterMap – 已废弃！老式风格的参数映射 

sql –抽取可重用语句块。

insert – 映射插入语句 

update – 映射更新语句 

delete – 映射删除语句 

select – 映射查询语句

## 1、insert、update、delete元素

![image-20200621115504779](\images\image-20200621115504779.png)

### 插入语句

```xml
<!-- public void insertEmployee(Employee employee); -->
<!-- parameterType：参数类型，可以省略，
获取自增主键的值：
    mysql支持自增主键，自增主键值的获取，mybatis也是利用statement.getGenreatedKeys()；
    useGeneratedKeys="true"；使用自增主键获取主键值策略
    keyProperty；指定对应的主键属性，也就是mybatis获取到主键值以后，将这个值封装给javaBean的哪个属性
-->
<insert id="insertEmployee"  useGeneratedKeys="true" keyProperty="id">
    INSERT INTO tbl_employee(last_name,email,gender)  values (#{lastName},#{email},#{gender})
</insert>
```

```java
@Test
public void testInsert(){
    String resource = "mybatis.xml";
    InputStream stream = null;
    SqlSession sqlSession = null;
    try {
        stream = Resources.getResourceAsStream(resource);
        //创建SqlSessionFactory对象
        SqlSessionFactory sessionFactory = new SqlSessionFactoryBuilder().build(stream);
        //创建SqlSession对象
        sqlSession = sessionFactory.openSession();
        EmployeeDao employeeDao = sqlSession.getMapper(EmployeeDao.class);
        Employee entity = new Employee("harry1", "414804000@qq.com", "0");
        employeeDao.insertEmployee(entity);
        System.out.println(entity.getId()+":获取插入后的ID");
        sqlSession.commit();
    } catch (IOException e) {
        e.printStackTrace();
    }


}
```

若使用的数据库为Oracle不支持自增

```xml
 <!--
获取非自增主键的值：
   Oracle不支持自增；Oracle使用序列来模拟自增；
   每次插入的数据的主键是从序列中拿到的值；如何获取到这个值；
 -->
   <insert id="addEmp" databaseId="oracle">
       <!--
       keyProperty:查出的主键值封装给javaBean的哪个属性
       order="BEFORE":当前sql在插入sql之前运行
              AFTER：当前sql在插入sql之后运行
       resultType:查出的数据的返回值类型

       BEFORE运行顺序：
           先运行selectKey查询id的sql；查出id值封装给javaBean的id属性
           在运行插入的sql；就可以取出id属性对应的值
       AFTER运行顺序：
           先运行插入的sql（从序列中取出新值作为id）；
           再运行selectKey查询id的sql；
        -->
       <selectKey keyProperty="id" order="BEFORE" resultType="Integer">
           <!-- 编写查询主键的sql语句 -->
           <!-- BEFORE-->
           select EMPLOYEES_SEQ.nextval from dual
           <!-- AFTER：
            select EMPLOYEES_SEQ.currval from dual -->
       </selectKey>

       <!-- 插入时的主键是从序列中拿到的 -->
       <!-- BEFORE:-->
       insert into employees(EMPLOYEE_ID,LAST_NAME,EMAIL)
       values(#{id},#{lastName},#{email<!-- ,jdbcType=NULL -->})
       <!-- AFTER：
       insert into employees(EMPLOYEE_ID,LAST_NAME,EMAIL)
       values(employees_seq.nextval,#{lastName},#{email}) -->
   </insert>
```

单个参数：mybatis不会做特殊处理，
	#{参数名/任意名}：取出参数值。
	
多个参数：mybatis会做特殊处理。
	多个参数会被封装成 一个map，
		key：param1...paramN,或者参数的索引也可以
		value：传入的参数值
	#{}就是从map中获取指定的key的值；	

异常：
org.apache.ibatis.binding.BindingException: 
Parameter 'id' not found. 
Available parameters are [1, 0, param1, param2]
操作：
	方法：public Employee getEmpByIdAndLastName(Integer id,String lastName);
	取值：#{id},#{lastName}

【命名参数】：明确指定封装参数时map的key；@Param("id")
	多个参数会被封装成 一个map，
		key：使用@Param注解指定的值
		value：参数值
	#{指定的key}取出对应的参数值

POJO：
如果多个参数正好是我们业务逻辑的数据模型，我们就可以直接传入pojo；
	#{属性名}：取出传入的pojo的属性值	

Map：
如果多个参数不是业务模型中的数据，没有对应的pojo，不经常使用，为了方便，我们也可以传入map
	#{key}：取出map中对应的值

TO：
如果多个参数不是业务模型中的数据，但是经常要使用，推荐来编写一个TO（Transfer Object）数据传输对象
Page{
	int index;
	int size;
}

```java
public Employee getEmp(@Param("id")Integer id,String lastName);
	取值：id==>#{id/param1}   lastName==>#{param2}

public Employee getEmp(Integer id,@Param("e")Employee emp);
	取值：id==>#{param1}    lastName===>#{param2.lastName/e.lastName}

/***     特别注意：如果是Collection（List、Set）类型或者是数组，
		 也会特殊处理。也是把传入的list或者数组封装在map中。
			key：Collection（collection）,如果是List还可以使用这个key(list)
				数组(array)
***/
public Employee getEmpById(List<Integer> ids);
	取值：取出第一个id的值：   #{list[0]}
```

### 删除语句

```xml
<!--    int deleteEmployee(@Param("last_name") String lastName, @Param("gender") String gender);-->

<delete id="deleteEmployee">
  DELETE FROM tbl_employee WHERE last_name=#{last_name} AND gender=#{gender}
</delete>
```

### 更新语句

```xml
<!--    int updateEmployee(@Param("last_name") String lastName, @Param("update_name") String updateName);-->
<update id="updateEmployee">
	UPDATE tbl_employee SET last_name=#{update_name} WHERE last_name=#{last_name}
</update>
```

## 2、参数值的获取

#{}：可以获取map中的值或者pojo对象属性的值；
${}：可以获取map中的值或者pojo对象属性的值；

select * from tbl_employee where id=${id} and last_name=#{lastName}
Preparing: select * from tbl_employee where id=2 and last_name=?
	区别：
		#{}:是以预编译的形式，将参数设置到sql语句中；PreparedStatement；防止sql注入
		${}:取出的值直接拼装在sql语句中；会有安全问题；
		大多情况下，我们去参数的值都应该去使用#{}；

​	原生jdbc不支持占位符的地方我们就可以使用${}进行取值
​	比如分表、排序。。。；按照年份分表拆分
​		select * from ${year}_salary where xxx;
​		select * from tbl_employee order by ${f_name} ${order}

#{}:更丰富的用法：

> 规定参数的一些规则：
> 	javaType、 jdbcType、 mode（存储过程）、 numericScale、
> 	resultMap、 typeHandler、 jdbcTypeName、 expression（未来准备支持的功能）；
>
> jdbcType通常需要在某种特定的条件下被设置：
> 	在我们数据为null的时候，有些数据库可能不能识别mybatis对null的默认处理。比如Oracle（报错）；
> 	
> 	JdbcType OTHER：无效的类型；因为mybatis对所有的null都映射的是原生Jdbc的OTHER类型，oracle不能正确处理;
> 	
> 	由于全局配置中：jdbcTypeForNull=OTHER；oracle不支持；两种办法
> 	1、#{email,jdbcType=OTHER};
> 	2、jdbcTypeForNull=NULL
> 		<setting name="jdbcTypeForNull" value="NULL"/>

## 3、select元素

Id：唯一标识符用来引用这条语句，需要和接口的方法名一致

parameterType：参数类型,可以不传，MyBatis会根据TypeHandler自动推断

resultType：返回值类型，别名或者全类名，如果返回的是集合，定义集合中元 素的类型。不能和resultMap同时使用

![image-20200623200732639](\images\image-20200623200732639.png)

## 4、resultMap

constructor ：类在实例化时, 用来注入结果到构造方法中 

​	– idArg ID 参数; 标记结果作为 ID 可以帮助提高整体效能 

​	– arg   注入到构造方法的一个普通结果

id ：一个 ID 结果; 标记结果作为 ID 可以帮助提高整体效能  

result ：注入到字段或 JavaBean 属性的普通结果

association ：一个复杂的类型关联;许多结果将包成这种类型

​	 – 嵌入结果映射 

​	– 结果映射自身的关联,或者参考一个

collection ： 复杂类型的集，嵌入结果映射， 结果映射自身的集,或者参考一个

discriminator ：使用结果值来决定使用哪个结果映射

### result的基本使用

```xml
<!--自定义某个javaBean的封装规则
    type：自定义规则的Java类型
    id:唯一id方便引用
-->
<resultMap id="employeeMap" type="com.harry.mybatis.Bean.Employee">
    <!--指定主键列的封装规则
     id定义主键会底层有优化；
     column：指定哪一列
     property：指定对应的javaBean属性
    -->
    <id column="eid" property="id"/>
    <!-- 定义普通列封装规则 -->
    <result column="lastName" property="lastName"/>
    <!-- 其他不指定的列会自动封装：我们只要写resultMap就把全部的映射规则都写上。 -->
    <result column="gender" property="gender"/>
    <result column="email" property="email"/>

</resultMap>

<!-- resultMap:自定义结果集映射规则；  -->
<select id="getEmployeeById" resultMap="employeeMap">
    select id eid, last_name lastName, gender, email from tbl_employee where id=#{id}
</select>
```

```java
@Test
public void testMap(){
    String resource = "mybatis.xml";
    InputStream stream = null;
    SqlSession sqlSession = null;
    try {
        stream = Resources.getResourceAsStream(resource);
        //创建SqlSessionFactory对象
        SqlSessionFactory sessionFactory = new SqlSessionFactoryBuilder().build(stream);
        //创建SqlSession对象
        sqlSession = sessionFactory.openSession();
        EmployeeDao employeeDao = sqlSession.getMapper(EmployeeDao.class);
        Employee employeeById = employeeDao.getEmployeeById(3);
        System.out.println(employeeById);
    }catch (IOException e) {
        e.printStackTrace();
    }
}
```

### association的使用

```xml
   <!--
       联合查询：级联属性封装结果集
     -->
   <resultMap type="com.harry.mybatis.Bean.Employee" id="MyDifEmp">
       <id column="id" property="id"/>
       <result column="last_name" property="lastName"/>
       <result column="gender" property="gender"/>
       <!--  association可以指定联合的javaBean对象
           property="dept"：指定哪个属性是联合的对象
           javaType:指定这个属性对象的类型[不能省略]
           -->
       <association property="dept" javaType="com.harry.mybatis.Bean.Department">
           <id column="did" property="id"/>
           <result column="dept_name" property="departmentName"/>
       </association>
   </resultMap>
<!--  public Employee getEmpAndDept(Integer id);-->
<select id="getEmpAndDept" resultMap="MyDifEmp">
   SELECT e.id id,e.last_name last_name,e.gender gender,e.d_id d_id,
   d.id did,d.dept_name dept_name FROM tbl_employee e,departement d
   WHERE e.d_id=d.id AND e.id=#{id}
</select>
```

```java
@Test
public void testMap(){
    String resource = "mybatis.xml";
    InputStream stream = null;
    SqlSession sqlSession = null;
    try {
        stream = Resources.getResourceAsStream(resource);
        //创建SqlSessionFactory对象
        SqlSessionFactory sessionFactory = new SqlSessionFactoryBuilder().build(stream);
        //创建SqlSession对象
        sqlSession = sessionFactory.openSession();
        EmployeeDao employeeDao = sqlSession.getMapper(EmployeeDao.class);
        Employee employeeById = employeeDao.getEmployeeById(1);
        Employee empAndDept = employeeDao.getEmpAndDept(1);
        System.out.println(empAndDept);
        System.out.println(employeeById);
    }catch (IOException e) {
        e.printStackTrace();
    }
}
```

### association的阶段查询

```xml
<!-- 使用association进行分步查询：
1、先按照员工id查询员工信息
2、根据查询员工信息中的d_id值去部门表查出部门信息
3、部门设置到员工中；
-->

<!--  id  last_name  email   gender    d_id   -->
<resultMap type="com.harry.mybatis.Bean.Employee" id="MyEmpByStep">
    <id column="id" property="id"/>
    <result column="last_name" property="lastName"/>
    <result column="email" property="email"/>
    <result column="gender" property="gender"/>
    <!-- association定义关联对象的封装规则
        select:表明当前属性是调用select指定的方法查出的结果
        column:指定将哪一列的值传给这个方法

        流程：使用select指定的方法（传入column指定的这列参数的值）查出对象，并封装给property指定的属性
     -->
    <association property="dept"
                 select="getDeptById"
                 column="d_id">
    </association>
</resultMap>

<!--  public Employee getEmpByIdStep(Integer id);-->
<select id="getEmpByIdStep" resultMap="MyEmpByStep">
    select * from tbl_employee where id=#{id}
    <if test="_parameter!=null">
        and 1=1
    </if>
</select>
```

DepartmentMapper

```xml
<mapper namespace="com.harry.mybatis.Bean.Dao.EmployeeDao">
    <select id="getDeptById" resultType="com.harry.mybatis.Bean.Department">
      select id,dept_name departmentName from departement where id=#{id}
   </select>
</mapper>
```

### collection的使用

```xml
<resultMap id="myDept" type="com.harry.mybatis.Bean.Department">
   <id column="did" property="id"/>
   <result column="dept_name" property="departmentName"/>
   <!--
      collection定义关联集合类型的属性的封装规则
      ofType:指定集合里面元素的类型
   -->
   <collection property="emps" ofType="com.harry.mybatis.Bean.Employee">
      <!-- 定义这个集合中元素的封装规则 -->
      <id column="eid" property="id"/>
      <result column="last_name" property="lastName"/>
      <result column="email" property="email"/>
      <result column="gender" property="gender"/>
   </collection>
</resultMap>
<select id="getDeptByIdPlus" resultMap="myDept">
   SELECT d.id did,d.dept_name dept_name,
         e.id eid,e.last_name last_name,e.email email,e.gender gender
   FROM tbl_dept d
   LEFT JOIN tbl_employee e
   ON d.id=e.d_id
   WHERE d.id=#{id}
</select>
```

### collection的分段查询

```xml
<!-- collection：分段查询 -->
<resultMap type="com.harry.mybatis.Bean.Department" id="MyDeptStep">
   <id column="id" property="id"/>
   <id column="dept_name" property="departmentName"/>
   <collection property="emps"
            select="getEmpByIdStep"
            column="{deptId=id}" fetchType="lazy"></collection>
</resultMap>
<!-- public Department getDeptByIdStep(Integer id); -->
<select id="getDeptByIdStep" resultMap="MyDeptStep">
   select id,dept_name from tbl_dept where id=#{id}
</select>

<!-- 扩展：多列的值传递过去：
       将多列的值封装map传递；
       column="{key1=column1,key2=column2}"
   fetchType="lazy"：表示使用延迟加载；
           - lazy：延迟
           - eager：立即
 -->
```

# 四、MyBatis-动态SQL

动态 SQL是MyBatis强大特性之一。极大的简化我们拼装 SQL的操作。 

动态 SQL 元素和使用 JSTL 或其他类似基于 XML 的文本处 理器相似。 

 MyBatis 采用功能强大的基于 OGNL 的表达式来简化操作。

​	 – if 

​	– choose (when, otherwise) 

​	– trim (where, set) 

​	– foreach

### if标签

这里的if标签主要是用来判断用户是否输入了某个条件，如果输入了再将该条件拼接到sql语句中，如下示例表示用户可以输入两个查询条件，name和age：

```xml
<select id="selectIf" resultType="student">
    SELECT id,name,age,score
    FROM t_student
    WHERE 1=1
    <if test="name != null and name != ''">
        AND name LIKE '%' #{name} '%'
    </if>
    <if test="age>=0">
        AND age > #{age}
    </if>
</select>
```

​	在上面的语句中，我们在where后面添加了一个1=1的条件，这样就不至于两个条件均未设定而出现只剩下一个where，这样sql语句就不正确了，所以在后面添加了1=1这个为true的条件。

在dao中添加方法

```java
List<Student> selectIf(Student student);
```

在测试类中进行测试：

```java
@Test
public void selectIf(){
	Student student = new Student("富", 0, 0.0);
	List<Student> students = studentDao.selectIf(student);
	students.forEach((s)-> {
		System.out.println(s);
	});
}
```

### where标签

在上面的if语句中，为了防止用户未设置条件而导致sql语句出现一个where，我们添加了1=1这个条件，但是这个条件没有什么意义，所以可以使用where标签来解决这个问题。

在mapper中添加下面sql：

```XML
<select id="selectWhere" resultType="student">
    SELECT id,name,age,score
    FROM t_student
    <where>
        <if test="name != null and name != ''">
            name LIKE '%' #{name} '%'
        </if>
        <if test="age>=0">
            AND age > #{age}
        </if>
    </where>
</select>
```

使用where标签后，就无需再写1=1了，注意在第一个if标签中的sql可以不加and，但是其后面的if标签中必须要加and。

### choose标签

通过choose标签实现下面功能若姓名不空，则按照姓名查询；若姓名为空，则按照年龄查询；若没有查询条件，则没有查询结果。

在mapper中添加下面sql：

```xml
<select id="selectChoose" resultType="student">
    SELECT id,name,age,score
    FROM t_student
    <where>
        <choose>
            <when test="name != null and name != ''">
                name like '%' #{name} '%'
            </when>
            <when test="age>0">
                age>#{age}
            </when>
            <otherwise>
                1 != 1
            </otherwise>
        </choose>
    </where>
</select>
```

在choose标签中可以有多个when，但是只能有一个otherwise，这个有点类似java中的switch语句

在dao接口中添加下面方法：

```java
List<Student> selectChoose(Student student);
```

在测试类中添加测试方法

```java
@Test
public void selectChoose(){
	Student student = new Student("harry", 30, 0.0);
	List<Student> students = studentDao.selectChoose(student);
	students.forEach(s -> {
		System.out.println(s);
	});
}
```

### Foreach标签

有时候会有这样的操作，用户需要查询Student的id是5,6,10,15的数据，这些数据可能会被放到数组里面作为参数进行传递，以前我们可以在sql语句中使用in来实现，在mybatis中就可以使用foreach标签。

foreach标签的属性中
			collection 表示要遍历的集合类型，这里是数组，即 array。
			open、close、separator 为对遍历内容的 SQL 拼接。

在dao中添加方法：

```java
List<Student> selectForeachArray(Object[] ids);
```

```xml
<select id="selectForeachArray" resultType="student">
    <!--
        collection：指定要遍历的集合：
            list类型的参数会特殊处理封装在map中，map的key就叫list
        item：将当前遍历出的元素赋值给指定的变量
        separator:每个元素之间的分隔符
        open：遍历出所有结果拼接一个开始的字符
        close:遍历出所有结果拼接一个结束的字符
        index:索引。遍历list的时候是index就是索引，item就是当前值
                      遍历map的时候index表示的就是map的key，item就是map的值
        
        #{变量名}就能取出变量的值也就是当前遍历出的元素
    -->
    SELECT id,name,age,score
    FROM t_student
    <if test="array != null and array.length>0">
        WHERE id IN
        <foreach collection="array" open="(" close=")" item="id" separator=",">
            #{id}
        </foreach>
    </if>
</select>
```

在测试类中添加测试方法：

```java
@Test
public void selectForeachArray(){
   Object[] ids = new Object[]{5,6,10,15};

   List<Student> students = studentDao.selectForeachArray(ids);
   students.forEach((s)-> {
      System.out.println(s);
   });
}
```

foreach标签遍历基本数据类型的集合

遍历集合的方式跟数组差不多，只不过有些地方需要稍作修改

```xml
<select id="selectForeachList" resultType="student">
    select id,name,age,score
    from t_student
    <if test="list != null and list.size>0" >
        where id in
        <foreach collection="list" open="(" close=")" item="id" separator=",">
            #{id}
        </foreach>
    </if>
</select>
```

在测试类中添加测试方法

```java
@Test
public void selectForeachList(){
   List<Integer> list = new ArrayList<>();
   list.add(5);
   list.add(6);
   list.add(10);
   list.add(15);

   List<Student> students = studentDao.selectForeachList(list);
   students.forEach((s)-> {
      System.out.println(s);
   });
}
```

foreach标签遍历自定义数据类型的集合

```xml
<select id="selectForeachListStudent" resultType="student">
    SELECT id,name,age,score
    FROM t_student
    <if test="list != null and list.size>0">
        WHERE id IN
        <foreach collection="list" open="(" close=")" item="stu" separator=",">
            #{stu.id}
        </foreach>
    </if>
</select>
```

在dao中添加方法：

```java
List<Student> selectForeachListStudent(List<Student> students);
```

在测试类中添加方法：

```java
@Test
public void selectForeachListStudent(){
   List<Student> stuList = new ArrayList<>();
   Student s1 = new Student();
   Student s2 = new Student();
   s1.setId(1);
   s2.setId(5);
   stuList.add(s1);
   stuList.add(s2);
   List<Student> students = studentDao.selectForeachListStudent(stuList);
   students.forEach(student -> {
      System.out.println(student);
   });
}
```

批量保存

```xml
<!--public void addEmps(@Param("emps")List<Employee> emps);  -->
<!--MySQL下批量保存：可以foreach遍历   mysql支持values(),(),()语法-->
<insert id="addEmps">
    insert into tbl_employee(
    <include refid="insertColumn"></include>
    )
    values
    <foreach collection="emps" item="emp" separator=",">
        (#{emp.lastName},#{emp.email},#{emp.gender},#{emp.dept.id})
    </foreach>
</insert><!--   -->

<!-- 这种方式需要数据库连接属性allowMultiQueries=true；
    这种分号分隔多个sql可以用于其他的批量操作（删除，修改） -->
<!-- <insert id="addEmps">
    <foreach collection="emps" item="emp" separator=";">
        insert into tbl_employee(last_name,email,gender,d_id)
        values(#{emp.lastName},#{emp.email},#{emp.gender},#{emp.dept.id})
    </foreach>
</insert> -->
```

Oracle数据库批量保存

```xml
<!-- Oracle数据库批量保存： 
        Oracle不支持values(),(),()
        Oracle支持的批量方式
        1、多个insert放在begin - end里面
            begin
               insert into employees(employee_id,last_name,email) 
               values(employees_seq.nextval,'test_001','test_001@atguigu.com');
               insert into employees(employee_id,last_name,email) 
               values(employees_seq.nextval,'test_002','test_002@atguigu.com');
           end;
       2、利用中间表：
           insert into employees(employee_id,last_name,email)
              select employees_seq.nextval,lastName,email from(
                     select 'test_a_01' lastName,'test_a_e01' email from dual
                     union
                     select 'test_a_02' lastName,'test_a_e02' email from dual
                     union
                     select 'test_a_03' lastName,'test_a_e03' email from dual
              )    
    -->
<insert id="addEmps" databaseId="oracle">
    <!-- oracle第一种批量方式 -->
    <!-- <foreach collection="emps" item="emp" open="begin" close="end;">
        insert into employees(employee_id,last_name,email) 
           values(employees_seq.nextval,#{emp.lastName},#{emp.email});
    </foreach> -->

    <!-- oracle第二种批量方式  -->
    insert into employees(
    <!-- 引用外部定义的sql -->
    <include refid="insertColumn">
        <property name="testColomn" value="abc"/>
    </include>
    )
    <foreach collection="emps" item="emp" separator="union"
             open="select employees_seq.nextval,lastName,email from("
             close=")">
        select #{emp.lastName} lastName,#{emp.email} email from dual
    </foreach>
</insert>
```

```xml
  <sql id="insertColumn">
  		<if test="_databaseId=='oracle'">
  			employee_id,last_name,email
  		</if>
  		<if test="_databaseId=='mysql'">
  			last_name,email,gender,d_id
  		</if>
  </sql>
```

# 五、MyBatis-缓存机制

MyBatis 包含一个非常强大的查询缓存特性,它可以非 常方便地配置和定制。缓存可以极大的提升查询效率

MyBatis系统中默认定义了两级缓存。 

一级缓存和二级缓存

​	1、默认情况下，只有一级缓存（SqlSession级别的缓存， 也称为本地缓存）开启。 

​	2、二级缓存需要手动开启和配置，他是基于namespace级 别的缓存。

​	3、为了提高扩展性。MyBatis定义了缓存接口Cache。我们 可以通过实现Cache接口来自定义二级缓存

## 一级缓存

 一级缓存(local cache), 即本地缓存, 作用域默认 为sqlSession。当 Session flush 或 close 后, 该 Session 中的所有 Cache 将被清空。 

本地缓存不能被关闭, 但可以调用 clearCache() 来清空本地缓存, 或者改变缓存的作用域. 

在mybatis3.1之后, 可以配置本地缓存的作用域. 在 mybatis.xml 中配置

### 一级缓存演示&失效情况

同一次会话期间只要查询过的数据都会保存在当 前SqlSession的一个Map中

​	 key:hashCode+查询的SqlId+编写的sql查询语句+参数

一级缓存失效的四种情况 

​    1、不同的SqlSession对应不同的一级缓存 

​	2、同一个SqlSession但是查询条件不同 

​	3、同一个SqlSession两次查询期间执行了任何一次增 删改操作 

​	4、同一个SqlSession两次查询期间手动清空了缓存

## 二级缓存

 二级缓存(second level cache)，全局作用域缓存 

 二级缓存默认不开启，需要手动配置 

MyBatis提供二级缓存的接口以及实现，缓存实现要求 POJO实现Serializable接口 

二级缓存在 SqlSession 关闭或提交之后才会生

使用步骤 

​	1、全局配置文件中开启二级缓存 \<setting name= "cacheEnabled" value="true"/> 

​    2、需要使用二级缓存的映射文件处使用cache配置缓存 \<cache /> 

​    3、注意：POJO需要实现Serializable接口

## 缓存相关属性

```xml
<cache type="org.mybatis.caches.ehcache.EhcacheCache"></cache>
<!--  
eviction:缓存的回收策略：
	• LRU – 最近最少使用的：移除最长时间不被使用的对象。
	• FIFO – 先进先出：按对象进入缓存的顺序来移除它们。
	• SOFT – 软引用：移除基于垃圾回收器状态和软引用规则的对象。
	• WEAK – 弱引用：更积极地移除基于垃圾收集器状态和弱引用规则的对象。
	• 默认的是 LRU。
flushInterval：缓存刷新间隔
	缓存多长时间清空一次，默认不清空，设置一个毫秒值
readOnly:是否只读：
	true：只读；mybatis认为所有从缓存中获取数据的操作都是只读操作，不会修改数据。
			 mybatis为了加快获取速度，直接就会将数据在缓存中的引用交给用户。不安全，速度快
	false：非只读：mybatis觉得获取的数据可能会被修改。
			mybatis会利用序列化&反序列的技术克隆一份新的数据给你。安全，速度慢
size：缓存存放多少元素；
type=""：指定自定义缓存的全类名；
		实现Cache接口即可；
-->
```
## 缓存有关设置

1、全局setting的cacheEnable： 

​	– 配置二级缓存的开关。一级缓存一直是打开的。 

2、select标签的useCache属性：

​	 – 配置这个select是否使用二级缓存。一级缓存一直是使用的 

 3、sql标签的flushCache属性： 

​	– 增删改默认flushCache=true。sql执行以后，会同时清空一级和二级缓存。 查询默认flushCache=false。 

4、sqlSession.clearCache()： 

​	– 只是用来清除一级缓存。 

 5、当在某一个作用域 (一级缓存Session/二级缓存 Namespaces) 进行了 C/U/D 操作后，默认该作用域下所有 select 中的缓存将被clear

## 第三方缓存整合 

EhCache 是一个纯Java的进程内缓存框架，具有快速、精 干等特点，是Hibernate中默认的CacheProvider。 

MyBatis定义了Cache接口方便我们进行自定义扩展。 

步骤： 

1、导入ehcache包，以及整合包，日志包 ehcache-core-2.6.8.jar、mybatis-ehcache-1.0.3.jar slf4j-api-1.6.1.jar、slf4j-log4j12-1.6.2.jar 

2、编写ehcache.xml配置文件 

3、配置cache标签 \<cache type= "org.mybatis.caches.ehcache.EhcacheCache">\</cache> 

参照缓存：若想在命名空间中共享相同的缓存配置和实例。 可以使用 cache-ref 元素来引用另外一个缓存。

![image-20200819202557585](images\image-20200819202557585.png)

# 六、MyBatis-逆向工程

简称MBG，是一个专门为MyBatis框架使用者定 制的代码生成器，可以快速的根据表生成对应的 映射文件，接口，以及bean类。支持基本的增删 改查，以及QBC风格的条件查询。但是表连接、 存储过程等这些复杂sql的定义需要我们手工编写 

## 使用步骤： 

1、编写MBG的配置文件（重要几处配置）

​	 1）jdbcConnection配置数据库连接信息

​	 2）javaModelGenerator配置javaBean的生成策略 

​	 3）sqlMapGenerator 配置sql映射文件生成策略

​     4）javaClientGenerator配置Mapper接口的生成策略

​     5）table 配置要逆向解析的数据表 tableName：表名 domainObjectName：对应的javaBean名 

–2、运行代码生成器生成代码

注意： 

Context标签

 targetRuntime=“MyBatis3“可以生成带条件的增删改查 

targetRuntime=“MyBatis3Simple“可以生成基本的增删改查 如果再次生成，建议将之前生成的数据删除，避免xml向后追加内容出现的问题。

## MBG配置文件

```xml
<generatorConfiguration>
<context id="DB2Tables" targetRuntime="MyBatis3 ">
<!--数据库连接信息配置 -->
    <jdbcConnection driverClass="com.mysql.jdbc.Driver" connectionURL="jdbc:mysql://localhost:3306/bookstore0629" userId=" root" password="123456"></jdbcConnection> //javaBean
<!--javaBean 的生成策-->
    <javaModelGenerator targetPackage="com.atguigu.bean" targetProject=".\src">
        <property name="enableSubPackages" value="true"/>
        <property name="trimStrings" value="true"/>
    </javaModelGenerator>
<!--    映射文件的生成策略-->
    <sqlMapGenerator targetPackage="mybatis.mapper" targetProject=".\conf">
        <property name="enableSubPackages" value="true"/>
    </sqlMapGenerator>
<!--    dao 接口 java 文件的生成策略-->
    <javaClientGenerator type="XMLMAPPER" targetPackage="com.atguigu.dao" targetProject=".\src">
        <property name="enableSubPackages" value="true"/>
    </javaClientGenerator>
<!--    数据表与 javaBean 的映射 -->
    <table tableName="books" domainObjectName="Book"></ table>
</context>
</generatorConfiguration>
```

## 生成器代码

```java
public static void main(String[] args) throws Exception {
    List<String> warnings = new ArrayList<String>();
    boolean overwrite = true;
    File configFile = new File("mbg.xml");
    ConfigurationParser cp = new ConfigurationParser(warnings);
    Configuration config = cp.parseConfiguration(configFile);
    DefaultShellCallback callback = new DefaultShellCallback(overwrite);
    MyBatisGenerator myBatisGenerator = new MyBatisGenerator(config, callback, warnings);
    myBatisGenerator.generate(null);
}
```

测试查询： QBC风格的带条件查询

```java
    @Test
    public void test01() {
        SqlSession openSession = build.openSession();
        DeptMapper mapper = openSession.getMapper(DeptMapper.class);
        DeptExample example = new DeptExample();
        //所有的条件都在example中封装 
        Criteria criteria = example.createCriteria(); 
        //select id, deptName, locAdd from tbl_dept WHERE 
        // ( deptName like ? and id > ? ) criteria.andDeptnameLike("%部%"); 
        criteria.andIdGreaterThan(2);
        List<Dept> list = mapper.selectByExample(example); 
        for (Dept dept : list) { 
            System. out .println(dept); 
        } 
}
```

# 七 MyBatis-工作原理和流程

![image-20200819203744136](images\image-20200819203744136.png)

![image-20200819203809696](images\image-20200819203809696.png)

[^一个MappedStatement代表一个增删改查标签的详细信息]: 

![image-20200819203856342](\images\image-20200819203856342.png)

Configuration对象保存了所有配置文件的详细信息

![image-20200819204008063](images\image-20200819204008063.png)

全局Configuration中的一个重要属性

![image-20200819204034010](images\image-20200819204034010)

![image-20200819204050638](images\image-20200819204050638.png)

## **1**、根据配置文件创建SQLSessionFactory

Configuration封装了所有配置文件的详细信息

![image-20200819204144233](images\image-20200819204144233.png)

**总结：把配置文件的信息解析并保存在**Configuration对象中，返回包含了Configuration的DefaultSqlSession对象。

## 2、返回SqlSession的实现类DefaultSqlSession对象。他里面包含了Executor和Configuration；Executor会在这一步被创建

![image-20200819204254930](C:\Users\harry.cai\AppData\Roaming\Typora\typora-user-images\image-20200819204254930.png)

## 3、getMapper返回接口的代理对象包含了SqlSession对象

![image-20200819204337600](images\image-20200819204337600.png)

## 4、查询流程

![image-20200819204411391](images\image-20200819204411391.png)

## 5、查询流程总结

![image-20200819204511508](images\image-20200819204511508.png)

# 八、MyBatis-插件开发

MyBatis在四大对象的创建过程中，都会有插件进行介入。插件可以利用动态代理机制一层层的包装目标对象，而实现在目标对象执行目标方法之前进行拦截的效果。

MyBatis允许在已映射语句执行过程中的某一点进行拦截调用。 

默认情况下，MyBatis允许使用插件来拦截的方法调用包括：

​    Executor (update, query, flushStatements, commit, rollback, getTransaction, close, isClosed) 	

​	ParameterHandler (getParameterObject, setParameters) 

​	ResultSetHandler (handleResultSets, handleOutputParameters) 

​	StatementHandler (prepare, parameterize, batch, update, query) 

## 插件开发

### 插件开发步骤 

1）、编写插件实现Interceptor接口，并使用 @Intercepts注解完成插件签名

![image-20200820193642470](images\image-20200820193642470.png)

2）、在全局配置文件中注册插件

![image-20200820193708153](images\image-20200820193708153.png)

## 插件原理

1）、按照插件注解声明，按照插件配置顺序调用插件plugin方 法，生成被拦截对象的动态代理 

2）、多个插件依次生成目标对象的代理对象，层层包裹，先声 明的先包裹；形成代理链 

 3）、目标方法执行时依次从外到内执行插件的intercept方法。

4）、多个插件情况下，我们往往需要在某个插件中分离出目标 对象。可以借助MyBatis提供的SystemMetaObject类来进行获 取最后一层的h以及target属性的值

## Interceptor接口

Intercept：拦截目标方法执行 

plugin：生成动态代理对象，可以使用MyBatis提 供的Plugin类的wrap方法 

setProperties：注入插件配置时设置的属性