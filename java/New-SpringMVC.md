# 一、SpringMVC 概述

Spring 为展现层提供的基于 MVC 设计理念的优秀的 Web 框架，是目前最主流的 MVC 框架之一 

• Spring3.0 后全面超越 Struts2，成为最优秀的 MVC 框架 

• Spring MVC 通过一套 MVC 注解，让 POJO 成为处理请 求的控制器，而无须实现任何接口。

• 支持 REST 风格的 URL 请求 • 采用了松散耦合可插拔组件结构，比其他 MVC 框架更具 扩展性和灵活性

## Hello World Demo

### 引入依赖

```xml
<dependency>
  <groupId>javax.servlet</groupId>
  <artifactId>javax.servlet-api</artifactId>
  <version>3.1.0</version>
</dependency>

<dependency>
  <groupId>org.springframework</groupId>
  <artifactId>spring-webmvc</artifactId>
  <version>5.0.4.RELEASE</version>
</dependency>
```

### 配置WEB.xml

配置 DispatcherServlet ：DispatcherServlet 默认加载 /WEBINF/.xml 的 Spring 配置文件, 启动 WEB 层 的 Spring 容器。可以通过 contextConfigLocation 初始化参数自定 义配置文件的位置和名称

```xml
<!--字符编码过滤器-->
<filter>
    <filter-name>characterEncodingFilter</filter-name>
    <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>

    <!--指定字符编码-->
    <init-param>
        <param-name>encoding</param-name>
        <param-value>utf-8</param-value>
    </init-param>

    <!--强制指定字符编码，即如果在request中指定了字符编码，那么也会为其强制指定当前设置的字符编码-->
    <init-param>
        <param-name>forceEncoding</param-name>
        <param-value>true</param-value>
    </init-param>
</filter>
<filter-mapping>
    <filter-name>characterEncodingFilter</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>

<!-- 注册spring MVC中央控制器 -->
<servlet>
    <servlet-name>springMVC</servlet-name>
    <!-- spring MVC中的核心控制器 -->
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    <init-param>
        <param-name>contextConfigLocation</param-name>
        <param-value>classpath:springmvc.xml</param-value>
    </init-param>
    <load-on-startup>1</load-on-startup>
</servlet>

<servlet-mapping>
    <servlet-name>springMVC</servlet-name>
    <url-pattern>/</url-pattern>
</servlet-mapping>
```

### 创建 Spring MVC 配置文件

```xml
<!-- 视图解释类 -->
<bean class="org.springframework.web.servlet.view.InternalResourceViewResolver">
    <property name="prefix" value="/jsp/"/>
    <property name="suffix" value=".jsp"/>
</bean>

<!--解决返回json数据乱码问题-->
<bean id="stringHttpMessageConverter"
      class="org.springframework.http.converter.StringHttpMessageConverter">
    <property name="supportedMediaTypes">
        <list>
            <value>text/plain;charset=UTF-8</value>
            <value>application/json;charset=UTF-8</value>
        </list>
    </property>
</bean>
<mvc:annotation-driven>
    <mvc:message-converters>
        <ref bean="stringHttpMessageConverter" />
    </mvc:message-converters>
</mvc:annotation-driven>


<!-- 注册组件扫描器 -->
<context:component-scan base-package="com.harry.*"/>
<mvc:default-servlet-handler/>

<!--静态资源-->
<mvc:resources mapping="/images/**" location="/images/" />
<mvc:resources mapping="/js/**" location="/js/" />
<mvc:resources mapping="/css/**" location="/css/" />
<mvc:resources mapping="/html/**" location="/html/" />
```

### 创建请求处理器类

```java
@Controller
public class HelloController {

    @RequestMapping("/hello")
    public String helloWorld(ModelMap modelMap){
        modelMap.addAttribute("hello", "hello world CaiShuang");
        return "success";
    }
}
```

### 视图

```jsp
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
    <h1>${hello}</h1>
</body>
</html>
```

## 使用 @RequestMapping 映射请求

Spring MVC 使用 @RequestMapping 注解为控制器指定可 以处理哪些 URL 请求 

• 在控制器的类定义及方法定义处都可标注

 @RequestMapping 

​	– 类定义处：提供初步的请求映射信息。相对于 WEB 应用的根目录 

​	– 方法处：提供进一步的细分映射信息。相对于类定义处的 URL。若 类定义处未标注 @RequestMapping，则方法处标记的 URL 相对于 WEB 应用的根目录 

• DispatcherServlet 截获请求后，就通过控制器上 @RequestMapping 提供的映射信息确定请求所对应的处理 方法。

### 映射请求参数、请求方法或请求头

标准的 HTTP 请求报头

![image-20200523155803766](images\image-20200523155803766.png)

@RequestMapping 除了可以使用请求 URL 映射请求外， 还可以使用请求方法、请求参数及请求头映射请求 

@RequestMapping 的 value、method、params 及 heads 分别表示请求 URL、请求方法、请求参数及请求头的映射条 件，他们之间是与的关系，联合使用多个条件可让请求映射 更加精确化。

params 和 headers支持简单的表达式： 

 	– param1: 表示请求必须包含名为 param1 的请求参数

​	 – !param1: 表示请求不能包含名为 param1 的请求参数 

​	 – param1 != value1: 表示请求包含名为 param1 的请求参数，但其值 不能为 value1

​	 – {“param1=value1”, “param2”}: 请求必须包含名为 param1 和param2 的两个请求参数，且 param1 参数的值必须为 value1

### 使用 @RequestMapping 映射请求

Ant 风格资源地址支持 3 种匹配符：

 	– ?：匹配文件名中的一个字符 

​	– *：匹配文件名中的任意字符 *

​	– \**：** 匹配多层路径

## @PathVariable 映射 URL 绑定的占位符

带占位符的 URL 是 Spring3.0 新增的功能，该功能在 SpringMVC 向 REST 目标挺进发展过程中具有里程碑的 意义

通过 @PathVariable 可以将 URL 中占位符参数绑定到控 制器处理方法的入参中：URL 中的 {xxx} 占位符可以通过 @PathVariable("xxx") 绑定到操作方法的入参中。

```java
   @RequestMapping("/test/{num}")
    public String testPathVariable(@PathVariable(value = "num") String num, Map<String, Object> map){
        System.out.println(num);
        map.put("num", num);
        return "success";
    }
```

## 使用 @RequestParam 绑定请求参数值

在处理方法入参处使用 @RequestParam 可以把请求参 数传递给请求方法 

 	– value：参数名

​	 – required：是否必须。默认为 true, 表示请求参数中必须包含对应 的参数，若不存在，将抛出异常

```java
/**
 * @RequestParam 来映射请求参数. value 值即请求参数的参数名 required 该参数是否必须. 默认为 true
 *               defaultValue 请求参数的默认值
 */
@RequestMapping(value = "/testRequestParam")
public String testRequestParam(
		@RequestParam(value = "username") String un,
		@RequestParam(value = "age", required = false, defaultValue = "0") int age) {
	System.out.println("testRequestParam, username: " + un + ", age: "+ age);
	return SUCCESS;
}
```
## 使用 @CookieValue 绑定请求中的 Cookie 值

@CookieValue 可让处理方法入参绑定某个 Cookie 值

```java
@RequestMapping("/testCookieValue")
public String testCookieValue(@CookieValue("JSESSIONID") String sessionId) {
	System.out.println("testCookieValue: sessionId: " + sessionId);
	return SUCCESS;
}
```
## 使用 POJO 对象绑定请求参数值

Spring MVC 会按请求参数名和 POJO 属性名进行自动匹 配，自动为该对象填充属性值。支持级联属性。 如：dept.deptId、dept.address.tel 等

```java
/**
 * Spring MVC 会按请求参数名和 POJO 属性名进行自动匹配， 自动为该对象填充属性值。支持级联属性。
 * 如：dept.deptId、dept.address.tel 等
 */
@RequestMapping("/testPojo")
public String testPojo(User user) {
	System.out.println("testPojo: " + user);
	return SUCCESS;
}
```
## 使用 Servlet API 作为入参

```java
/**
 * 可以使用 Serlvet 原生的 API 作为目标方法的参数 具体支持以下类型
 *
 * HttpServletRequest 
 * HttpServletResponse 
 * HttpSession
 * java.security.Principal 
 * Locale InputStream 
 * OutputStream 
 * Reader 
 * Writer
 * @throws IOException
 */
@RequestMapping("/testServletAPI")
public void testServletAPI(HttpServletRequest request,
                           HttpServletResponse response, Writer out) throws IOException {
    System.out.println("testServletAPI, " + request + ", " + response);
    out.write("hello springmvc");
//		return SUCCESS;
}
```

# 二、SpringMVC处理数据模型

Spring MVC 提供了以下几种途径输出模型数据：

​	 – ModelAndView: 处理方法返回值类型为 ModelAndView 时, 方法体即可通过该对象添加模型数据

​	– Map 及 Model: 入参为 org.springframework.ui.Model、org.springframework.ui. ModelMap 或 java.uti.Map 时，处理方法返回时，Map 中的数据会自动添加到模型中。

​	– @SessionAttributes: 将模型中的某个属性暂存到 HttpSession 中，以便多个请求之间可以共享这个属性	

​	– @ModelAttribute: 方法入参标注该注解后, 入参的对象 就会放到数据模型中

## ModelAndView

控制器处理方法的返回值如果为 ModelAndView, 则其既 包含视图信息，也包含模型数据信息。

添加模型数据: 

​	– MoelAndView addObject(String attributeName, Object attributeValue) 

​	– ModelAndView addAllObject(Map modelMap)

设置视图:

​	– void setView(View view) 

​	– void setViewName(String viewN

```java
/**
 * 重定向返回ModelAndView对象
 * @return
 * @throws Exception
 */
@RequestMapping("/redirectMAV.do")
public ModelAndView redirectMAV(School school,String name)throws Exception {

    ModelAndView mv = new ModelAndView();

    //在重定向中可以使用ModelAndView传递数据，但是只能传递基本数据类型和String类型
    mv.addObject("school", school);
    mv.addObject("name", name);

    //使用重定向，此时springmvc.xml配置文件中的视图解析器将会失效
    mv.setViewName("redirect:/jsp/result.jsp");
    return mv;
}
```

## Map 及 Model

Spring MVC 在内部使用了一个 org.springframework.ui.Model 接口存 储模型数据

具体步骤

 	– Spring MVC 在调用方法前会创建一个隐 含的模型对象作为模型数据的存储容器。

​	 – 如果方法的入参为 Map 或 Model 类 型，Spring MVC 会将隐含模型的引用传 递给这些入参。在方法体内，开发者可以 通过这个入参对象访问到模型中的所有数 据，也可以向模型中添加新的属性数据

![image-20200523164713573](images\image-20200523164713573.png)

## @SessionAttributes

若希望在多个请求之间共用某个模型属性数据，则可以在 控制器类上标注一个 @SessionAttributes, Spring MVC 将在模型中对应的属性暂存到 HttpSession 中。

@SessionAttributes 除了可以通过属性名指定需要放到会 话中的属性外，还可以通过模型属性的对象类型指定哪些 模型属性需要放到会话中

​	– @SessionAttributes(types=User.class) 会将隐含模型中所有类型 为 User.class 的属性添加到会话中

​	– @SessionAttributes(value={“user1”, “user2”}) 

​	– @SessionAttributes(types={User.class, Dept.class})

​	– @SessionAttributes(value={“user1”, “user2”}, types={Dept.class})

```java
@Controller
@SessionAttributes(value={"user"}, types={String.class})
public class HelloController {
    @RequestMapping("/testSA")
    public String testSessionAttributes(Map<String, Object> map){
        map.put("user", "Caishuang");
        return "success";
    }
}
```

## @ModelAttribute

在方法定义上使用 @ModelAttribute 注解：Spring MVC 在调用目标处理方法前，会先逐个调用在方法级上标注了 @ModelAttribute 的方法。

在方法的入参前使用 @ModelAttribute 注解：

​	 – 可以从隐含对象中获取隐含的模型数据中获取对象，再将请求参数 绑定到对象中，再传入入参 

​	 – 将方法入参对象添加到模型中

```java
/**
 * 1. 有 @ModelAttribute 标记的方法, 会在每个目标方法执行之前被 SpringMVC 调用!
 * 2. @ModelAttribute 注解也可以来修饰目标方法 POJO 类型的入参, 其 value 属性值有如下的作用:
 *   1). SpringMVC 会使用 value 属性值在 implicitModel 中查找对应的对象, 若存在则会直接传入到目标方法的入参中.
 *   2). SpringMVC 会一 value 为 key, POJO 类型的对象为 value, 存入到 request 中.
 */
@ModelAttribute
public void getUser(@RequestParam(value="id",required=false) Integer id,
                    Map<String, Object> map) {
    System.out.println("modelAttribute method");
    if (id != null) {
        //模拟从数据库中获取对象
        User user = new User(1, "Tom", "123456", "tom@atguigu.com", 12);
        System.out.println("从数据库中获取一个对象: " + user);

        map.put("user", user);
    }
}
```

```java
@RequestMapping("/testModelAttribute")
public String testModelAttribute(User user){
	System.out.println("修改: " + user);
	return SUCCESS;
}
```
运行流程:

​	1.执行 @ModelAttribute 注解修饰的方法: 从数据库中取出对象, 把对象放入到了 Map 中. 键为: user

​	2.SpringMVC 从 Map 中取出 User 对象, 并把表单的请求参数赋给该 User 对象的对应属性.

​	3.SpringMVC 把上述对象传入目标方法的参数. 

注意: 在 @ModelAttribute 修饰的方法中, 放入到 Map 时的键需要和目标方法入参类型的第一个字母小写的字符串一致!

SpringMVC 确定目标方法 POJO 类型入参的过程:

1. 确定一个 key:

   1. 若目标方法的 POJO 类型的参数木有使用 @ModelAttribute 作为修饰, 则 key 为 POJO 类名第一个字母的小写

   2. 若使用了  @ModelAttribute 来修饰, 则 key 为 @ModelAttribute 注解的 value 属性值. 

2. 在 implicitModel 中查找 key 对应的对象, 若存在, 则作为入参传入
   1. 若在 @ModelAttribute 标记的方法中在 Map 中保存过, 且 key 和 1 确定的 key 一致, 则会获取到

3. 若 implicitModel 中不存在 key 对应的对象, 则检查当前的 Handler 是否使用 @SessionAttributes 注解修饰, 若使用了该注解, 且 @SessionAttributes 注解的 value 属性值中包含了 key, 则会从 HttpSession 中来获取 key 所对应的 value 值, 若存在则直接传入到目标方法的入参中. 若不存在则将抛出异常. 

  4. 若 Handler 没有标识 @SessionAttributes 注解或 @SessionAttributes 注解的 value 值中不包含 key, 则会通过反射来创建 POJO 类型的参数, 传入为目标方法的参数

5. SpringMVC 会把 key 和 POJO 类型的对象保存到 implicitModel 中, 进而会保存到 request 中. 

源代码分析的流程:

 1. 调用 @ModelAttribute 注解修饰的方法. 实际上把 @ModelAttribute 方法中 Map 中的数据放在了 implicitModel 中.

 2. 解析请求处理器的目标参数, 实际上该目标参数来自于 WebDataBinder 对象的 target 属性

    1). 创建 WebDataBinder 对象:

    ​	①. 确定 objectName 属性: 若传入的 attrName 属性值为 "", 则 objectName 为类名第一个字母小写. 

    ​	注意: attrName. 若目标方法的 POJO 属性使用了 @ModelAttribute 来修饰, 则 attrName 值即为 @ModelAttribute  的 value 属性值 

    ​	②. 确定 target 属性:

    ​		* 在 implicitModel 中查找 attrName 对应的属性值. 若存在, ok

    ​		* 若不存在: 则验证当前 Handler 是否使用了 @SessionAttributes 进行修饰, 若使用了, 则尝试从 Session 中获取 attrName 所对应的属性值. 若 session 中没有对应的属性值, 则抛出了异常. 

    ​		* 若 Handler 没有使用 @SessionAttributes 进行修饰, 或 @SessionAttributes 中没有使用 value 值指定的 key 和 attrName 相匹配, 则通过反射创建了 POJO 对象

    2). SpringMVC 把表单的请求参数赋给了 WebDataBinder 的 target 对应的属性. 

    3). SpringMVC 会把 WebDataBinder 的 attrName 和 target 给到 implicitModel,近而传到 request 域对象中. 

    4). 把 WebDataBinder 的 target 作为参数传递给目标方法的入参. 

# 三、Spring MVC解析视图

![image-20200524145432273](images\image-20200524145432273.png)

## 视图和视图解析器

​	请求处理方法执行完成后，最终返回一个 ModelAndView 对象。对于那些返回 String，View 或 ModeMap 等类型的 处理方法，Spring MVC 也会在内部将它们装配成一个 ModelAndView 对象，它包含了逻辑名和模型对象的视图

​	Spring MVC 借助视图解析器（ViewResolver）得到最终 的视图对象（View），最终的视图可以是 JSP ，也可能是 Excel、JFreeChart 等各种表现形式的视图

​	对于最终究竟采取何种视图对象对模型数据进行渲染，处理器并不关心，处理器工作重点聚焦在生产模型数据的工作上，从而实现 MVC 的充分解耦

## 视图

​	视图的作用是渲染模型数据，将模型里的数据以某种形式呈现给客户。

​	为了实现视图模型和具体实现技术的解耦，Spring 在 org.springframework.web.servlet 包中定义了一个高度抽象的 View 接口

​	视图对象由视图解析器负责实例化。由于视图是无状态的，所以他们不会有线程安全的问题

常用的视图实现类：

![image-20200524150323433](images\image-20200524150323433.png)

## 使用视图解析器

​	SpringMVC 为逻辑视图名的解析提供了不同的策略，可 以在 Spring WEB 上下文中配置一种或多种解析策略，并 指定他们之间的先后顺序。每一种映射策略对应一个具体的视图解析器实现类

​	视图解析器的作用比较单一：将逻辑视图解析为一个具体的视图对象。

​	所有的视图解析器都必须实现ViewResolver 接口

```java
@Component
public class HelloView implements View {

    @Override
    public String getContentType() {
        return "text/html";
    }

    @Override
    public void render(Map<String, ?> model, HttpServletRequest request,
                       HttpServletResponse response) throws Exception {
        response.getWriter().print("hello view, time: " + new Date());
    }

}
```

​	SpringMVC 为逻辑视图名的解析提供了不同的策略，可 以在 Spring WEB 上下文中配置一种或多种解析策略，并 指定他们之间的先后顺序。每一种映射策略对应一个具体 的视图解析器实现类。

​	视图解析器的作用比较单一：将逻辑视图解析为一个具体的视图对象。

​	所有的视图解析器都必须实现 ViewResolver 接口

常用的视图解析器实现类

![image-20200524152712449](images\image-20200524152712449.png)

程序员可以选择一种视图解析器或混用多种视图解析器

每个视图解析器都实现了 Ordered 接口并开放出一个 order 属性，可 以通过 order 属性指定解析器的优先顺序，order 越小优先级越高。

SpringMVC 会按视图解析器顺序的优先顺序对逻辑视图名进行解 析，直到解析成功并返回视图对象，否则将抛出 ServletException 异 常

```xml
<!-- 配置视图  BeanNameViewResolver 解析器: 使用视图的名字来解析视图 -->
<!-- 通过 order 属性来定义视图解析器的优先级, order 值越小优先级越高 -->
<bean class="org.springframework.web.servlet.view.BeanNameViewResolver">
	<property name="order" value="100"></property>
</bean>
```
```xml
<!-- 视图解释类 -->
<bean class="org.springframework.web.servlet.view.InternalResourceViewResolver">
    <property name="prefix" value="/jsp/"/>
    <property name="suffix" value=".jsp"/>
</bean>
```

```java
@RequestMapping("/testView")
public String testView(){
	System.out.println("testView");
	return "helloView";
}
```

# 四、RESTful SpringMVC CRUD

### 显示所有员工信息

 – URI：emps 

– 请求方式：GET

 – 显示效果

![image-20200527195356460](images\image-20200527195356460.png)

```java
@RequestMapping("/emps")
public String list(Map<String, Object> map){
    System.out.println("list");
    map.put("employees", employeeDao.getAll());
    return "list";
}
```

```jsp
</script>
<html>
<head>

</head>
<body>
<form action="" method="POST">
    <input type="hidden" name="_method" value="DELETE"/>
</form>

<c:if test="${empty requestScope.employees}">
    没有任何员工信息
</c:if>
<c:if test="${!empty requestScope.employees}">
    <table border="1" cellpadding="10" cellspacing="0">
        <tr>
            <th>ID</th>
            <th>LastName</th>
            <th>Email</th>
            <th>Gender</th>
            <th>Department</th>
            <th>Edit</th>
            <th>Delete</th>
        </tr>
        <c:forEach items="${requestScope.employees}" var="emp">
            <tr>
                <td>${emp.id }</td>
                <td>${emp.lastName }</td>
                <td>${emp.email }</td>
                <td>${emp.gender == 0 ? 'Female' : 'Male' }</td>
                <td>${emp.department.departmentName }</td>
                <td><a href="emp/${emp.id}">Edit</a></td>
                <td><a class="delete" href="emp/${emp.id}">Delete</a></td>
            </tr>
        </c:forEach>
    </table>
</c:if>


<br><br>

<a href="emp">Add New Employee</a>
</body>
</html>
```

### 添加所有员工信息

```java
@RequestMapping(value = "/emp", method = RequestMethod.POST)
public String add(Employee employee, Errors result, Map<String, Object> map){
    if(result.getErrorCount() > 0){
        System.out.println("出错了!");

        for(FieldError error:result.getFieldErrors()){
            System.out.println(error.getField() + ":" + error.getDefaultMessage());
        }
        //若验证出错, 则转向定制的页面
        map.put("departments", departmentDao.getDepartments());
        return "input";
    }
    employeeDao.save(employee);
    return "redirect:/emps";
}
```

#### 使用 Spring 的表单标签

​	通过 SpringMVC 的表单标签可以实现将模型数据 中的属性和 HTML 表单元素相绑定，以实现表单数据更便捷编辑和表单值的回显

#### form 标签

​	一般情况下，通过 GET 请求获取表单页面，而通过 POST 请求提交表单页面，因此获取表单页面和提交表单 页面的 URL 是相同的。只要满足该最佳条件的契 约， 标签就无需通过 action 属性指定表单 提交的 URL 

​	可以通过 modelAttribute 属性指定绑定的模型属性，若没有指定该属性，则默认从 request 域对象中读取 command 的表单 bean，如果该属性值也不存在，则会发生错误。

​	form:input、form:password、form:hidden、form:textarea ：对应 HTML 表单的 text、password、hidden、textarea 标签

用以绑定表单字段的 属性值，它们的共有属性如下：

- path：表单字段，对应 html 元素的 name 属性，支持级联属性 

- htmlEscape：是否对表单值的 HTML 特殊字符进行转换，默认值 为 true 

- cssClass：表单组件对应的 CSS 样式类名

- cssErrorClass：表单组件的数据存在错误时，采取的 CSS 样式

form:radiobutton：单选框组件标签，当表单 bean 对应的 属性值和 value 值相等时，单选框被选中 form:radiobuttons：单选框组标签，用于构造多个单选框

​	items：可以是一个 List、String[] 或 Map 

​	itemValue：指定 radio 的 value 值。可以是集合中 bean 的一个 属性值

​	itemLabel：指定 radio 的 label 值

​	delimiter：多个单选框可以通过 delimiter 指定分隔符

form:checkbox：复选框组件。用于构造单个复选框 •

form:checkboxs：用于构造多个复选框。使用方式同 form:radiobuttons 标签 

form:select：用于构造下拉框组件。使用方式同 form:radiobuttons 标签 

form:option：下拉框选项组件标签。使用方式同 form:radiobuttons 标签 

 form:errors：显示表单组件或数据校验所对应的错误 

​	– 显示表单所有的错误 

​	– 显示所有以 user 为前缀的属性对应 的错误 

​	– 显示特定表单对象属性的错误

```jsp
<%@ page import="java.util.HashMap" %>
<%@ page import="java.util.Map" %><%--
  Created by IntelliJ IDEA.
  User: harry.cai
  Date: 2020/5/25
  Time: 21:11
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
<br><br>

<!--
    1. WHY 使用 form 标签呢 ?
    可以更快速的开发出表单页面, 而且可以更方便的进行表单值的回显
    2. 注意:
    可以通过 modelAttribute 属性指定绑定的模型属性,
    若没有指定该属性，则默认从 request 域对象中读取 command 的表单 bean
    如果该属性值也不存在，则会发生错误。
-->
<form:form action="${pageContext.request.contextPath}/emp" method="post" modelAttribute="employee">
    <form:errors path="*"></form:errors>
    <c:if test="${employee.id == null }">
        <!-- path 属性对应 html 表单标签的 name 属性值 -->
        LastName: <form:input path="lastName"/>
        <form:errors path="lastName"></form:errors>
    </c:if>
    <c:if test="${employee.id != null }">
        <form:hidden path="id"/>
        <input type="hidden" name="_method" value="PUT"/>
        <%-- 对于 _method 不能使用 form:hidden 标签, 因为 modelAttribute 对应的 bean 中没有 _method 这个属性 --%>
        <%--
        <form:hidden path="_method" value="PUT"/>
        --%>
    </c:if>
    <br>
    Email: <form:input path="email"/>
    <form:errors path="email"></form:errors>
    <br>
    <%
        Map<String, String> genders = new HashMap();
        genders.put("1", "Male");
        genders.put("0", "Female");

        request.setAttribute("genders", genders);
    %>
    Gender:
    <br>
    <form:radiobuttons path="gender" items="${genders }" delimiter="<br>"/>
    <br>
    Department: <form:select path="department.id"
                             items="${departments }" itemLabel="departmentName" itemValue="id"></form:select>
    <br>
    <!--
    1. 数据类型转换
    2. 数据类型格式化
    3. 数据校验.
    1). 如何校验 ? 注解 ?
    ①. 使用 JSR 303 验证标准
    ②. 加入 hibernate validator 验证框架的 jar 包
    ③. 在 SpringMVC 配置文件中添加 <mvc:annotation-driven />
    ④. 需要在 bean 的属性上添加对应的注解
    ⑤. 在目标方法 bean 类型的前面添加 @Valid 注解
    2). 验证出错转向到哪一个页面 ?
    注意: 需校验的 Bean 对象和其绑定结果对象或错误对象时成对出现的，它们之间不允许声明其他的入参
    3). 错误消息 ? 如何显示, 如何把错误消息进行国际化
    -->
    Birth: <form:input path="birth"/>
    <form:errors path="birth"></form:errors>
    <br>
    Salary: <form:input path="salary"/>
    <br>
    <input type="submit" value="Submit"/>
</form:form>

</body>
</html>
```

### 删除操作

```java
@RequestMapping(value="/emp/{id}", method=RequestMethod.DELETE)
public String delete(@PathVariable("id") Integer id){
    employeeDao.delete(id);
    return "redirect:/emps";
}
```

### 修改操作：lastName 不可修改！

```java
@RequestMapping(value="/emp/{id}", method=RequestMethod.GET)
public String delete(@PathVariable(value = "id", required = true) Integer id, Map<String, Object> map){
    map.put("employee", employeeDao.get(id));
    map.put("departments", departmentDao.getDepartments());
    return "input";
}

@RequestMapping(value="/emp", method=RequestMethod.PUT)
public String update(Employee employee){

    employeeDao.save(employee);
    return "redirect:/emps";
}
```

### 处理静态资源

​	若将 DispatcherServlet 请求映射配置为 /，则 Spring MVC 将捕获 WEB 容器的所有请求，包括静态资源的请求， SpringMVC 会将他们当成一个普通请求处理，因找不到对应处理器将导致错误。

可以在 SpringMVC 的配置文件中配置  的方式解决静态资源的问题： 

​	 \<mvc:default-servlet-handler/>将在 SpringMVC 上下文中定义一个 DefaultServletHttpRequestHandler，它会对进入 DispatcherServlet 的 请求进行筛查，如果发现是没有经过映射的请求，就将该请求交由 WEB 应用服务器默认的 Servlet 处理，如果不是静态资源的请求，才由 DispatcherServlet 继续处理 – 一般 WEB 应用服务器默认的 Servlet 的名称都是 default。若所使用的 WEB 服务器的默认 Servlet 名称不是 default，则通过defaultservlet-name 属性显式指定

​	一般 WEB 应用服务器默认的 Servlet 的名称都是 default。若所使用的 WEB 服务器的默认 Servlet 名称不是 default，则需要通过 defaultservlet-name 属性显式指定

```xml
<mvc:default-servlet-handler/>
```

### 数据绑定流程

​	1.  Spring MVC 主框架将 ServletRequest 对象及目标方法的入参实例传递给WebDataBinderFactory实例，以创建DataBinder实例对象

 	2. DataBinder 调用装配在 Spring MVC 上下文中的 ConversionService 组件进行数据类型转换、数据格式化工作。将 Servlet 中的请求信息填充到入参对象中

 	3. 调用 Validator 组件对已经绑定了请求消息的入参对象 进行数据合法性校验，并最终生成数据绑定结果 BindingData 对象

​	4. Spring MVC 抽取 BindingResult 中的入参对象和校验错误对象，将它们赋给处理方法的响应入参

Spring MVC 通过反射机制对目标处理方法进行解析，将请求消息绑定到处理方法的入参中。数据绑定的核心部件是 DataBinder，运行机制如下：

![image-20200527204002093](\images\image-20200527204002093.png)

![image-20200527204325130](images\image-20200527204325130.png)

![image-20200527204405046](\images\image-20200527204405046.png)

### 自定义类型转换器

​	以利用 ConversionServiceFactoryBean 在 Spring 的 IOC 容器中定义一个 ConversionService. Spring 将自动识别出 IOC 容器中的 ConversionService，并在 Bean 属性配置及Spring MVC处理方法入参绑定等场合使用它进行数据的转换

​	可通过 ConversionServiceFactoryBean 的 converters 属性注册自定义的类型转换器

```xml
<!--注解驱动-->
<mvc:annotation-driven conversion-service="conversionService"/>
<!-- 注册类型转换器 -->
<bean id="dateConverter" class="com.harry.converter.DateConverter"/>
<!-- 注册类型转换服务的bean -->
<bean id="conversionService" class="org.springframework.context.support.ConversionServiceFactoryBean">
	<property name="converters" ref="dateConverter"/>
</bean>
```

Spring 定义了 3 种类型的转换器接口，实现任意一个转换器接口都可以作为自定义转换器注册到 ConversionServiceFactroyBean 中：

​	 Converter<S,T>：将 S 类型对象转为 T 类型对象 

​	 ConverterFactory：将相同系列多个 “同质” Converter 封装在一 起。如果希望将一种类型的对象转换为另一种类型及其子类的对 象（例如将 String 转换为 Number 及 Number 子类 （Integer、Long、Double 等）对象）可使用该转换器工厂类 

​	GenericConverter：会根据源类对象及目标类对象所在的宿主类 中的上下文信息进行类型转换

```java
//创建一个类实现Converter接口，该接口中的泛型，前面的类是待转换的类型，后面的是转换之后的类型。
/**
 * 日期转换器
 */
public class DateConverter implements Converter<String, Date> {
   @Override
   public Date convert(String s) {
      if(s != null && !"".equals(s)){
         SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
         try {
            return sdf.parse(s);
         } catch (ParseException e) {
            e.printStackTrace();
         }
      }

      return null;
   }
}
```

```java
@Controller
@RequestMapping("/user")
public class UserController extends BaseExceptionController {
   @RequestMapping("/addUser.do")
   public ModelAndView addUser(String name, int age, Date birthday) throws Exception {
      ModelAndView mv = new ModelAndView();
      mv.addObject("name", name);
      mv.addObject("age", age);
      mv.addObject("birthady", birthday);
      mv.setViewName("result");
      return mv;
   }
}
```

### 关于 mvc:annotation-driven

<mvc:annotation-driven /> 会自动注 册RequestMappingHandlerMapping 、  RequestMappingHandlerAdapter 与 ExceptionHandlerExceptionResolver 三个bean。

还将提供以下支持：

​	 支持使用 ConversionService 实例对表单参数进行类型转换 

​	 支持使用 @NumberFormat annotation、@DateTimeFormat 注解完成数据类型的格式化 

​	 支持使用 @Valid 注解对 JavaBean 实例进行 JSR 303 验证 

​	 支持使用 @RequestBody 和 @ResponseBody 注解

### @InitBinde

由 @InitBinder 标识的方法，可以对 WebDataBinder 对 象进行初始化。WebDataBinder是DataBinder 的子类，用于完成由表单字段到 JavaBean 属性的绑定

@InitBinder方法不能有返回值，它必须声明为void

@InitBinder方法的参数通常是是 WebDataBinder

```java
@InitBinder
public void initBinder(WebDataBinder binder){
  // 不对lastName属性进行赋值
   binder.setDisallowedFields("lastName");
}
```

### 数据格式化

对属性对象的输入/输出进行格式化，从其本质上讲依然 属于 “类型转换” 的范畴。

Spring 在格式化模块中定义了一个实现ConversionService接口的 FormattingConversionService 实现类，该实现类扩展 了 GenericConversionService，因此它既具有类型转换的功能，又具有格式化的功能

FormattingConversionService 拥有一个 FormattingConversionServiceFactroyBean 工厂类， 后者用于在 Spring 上下文中构造前者

FormattingConversionServiceFactroyBean 内部已经注册了 :

​	– NumberFormatAnnotationFormatterFactroy：支持对数字类型的属性 使用 @NumberFormat 注解

​	– JodaDateTimeFormatAnnotationFormatterFactroy：支持对日期类型 的属性使用 @DateTimeFormat 注解

装配了FormattingConversionServiceFactroyBean 后，就可以在 Spring MVC入参绑定及模型数据输出时使用注解驱动了。

```java
private Integer id;
@NotEmpty
private String lastName;

@Email
private String email;
//1 male, 0 female
private Integer gender;

private Department department;

@Past
@DateTimeFormat(pattern="yyyy-MM-dd")
private Date birth;

@NumberFormat(pattern="#,###,###.#")
private Float salary;

```
#### 日期格式化

@DateTimeFormat 注解可对 java.util.Date、java.util.Calendar、java.long.Long 时间 类型进行标注：

​	pattern 属性：类型为字符串。指定解析/格式化字段数据的模式， 如：”yyyy-MM-dd hh:mm:ss”

​	iso 属性：类型为 DateTimeFormat.ISO。指定解析/格式化字段数据 的ISO模式，包括四种：ISO.NONE（不使用） -- 默 认、ISO.DATE(yyyy-MM-dd) 、ISO.TIME(hh:mm:ss.SSSZ)、 ISO.DATE_TIME(yyyy-MM-dd hh:mm:ss.SSSZ)

​	style 属性：字符串类型。通过样式指定日期时间的格式，由两位字 符组成，第一位表示日期的格式，第二位表示时间的格式：S：短日 期/时间格式、M：中日期/时间格式、L：长日期/时间格式、F：完整日期/时间格式、-：忽略日期或时间格式

#### 数值格式化

@NumberFormat 可对类似数字类型的属性进行标 注，它拥有两个互斥的属性：

​	style：类型为 NumberFormat.Style。用于指定样式类型，包括三种：Style.NUMBER（正常数字类型）、 Style.CURRENCY（货币类型）、 Style.PERCENT（ 百分数类型）

​	pattern：类型为 String，自定义样式， 如patter="#,###"；

# 五、Spring MVC 数据校验

### JSR 303

JSR 303是 Java为Bean数据合法性校验提供的标准框架， 它已经包含在 JavaEE 6.0中 

JSR 303通过在 Bean属性上标注类似于@NotNull、@Max 等标准的注解指定校验规则，并通过标准的验证接口对 Bean进行验证

![image-20200528205233654](\images\image-20200528205233654.png)

### Hibernate Validator 扩展注解

Hibernate Validator是 JSR 303 的一个参考实现，除支持所有标准的校验注解外，它还支持以下的扩展注解

![image-20200528205416559](images\image-20200528205416559.png)

 	\<mvc:annotation-driven> 会默认装配好一个 LocalValidatorFactoryBean，通过在处理方法的入参上标 注 @valid 注解即可让 Spring MVC 在完成数据绑定后执行 数据校验的工作

​	在已经标注了 JSR303 注解的表单/命令对象前标注一个 @Valid，Spring MVC 框架在将请求参数绑定到该入参对象 后，就会调用校验框架根据注解声明的校验规则实施校验

​	Spring MVC是通过对处理方法签名的规约来保存校验结果的：前一个表单/命令对象的校验结果保存到随后的入参 中，这个保存校验结果的入参必须是 BindingResult 或 Errors 类型，这两个类都位于org.springframework.validation 包中

需校验的 Bean 对象和其绑定结果对象或错误对象时成对出现的，它们 之间不允许声明其他的入参

Errors 接口提供了获取错误信息的方法，如 getErrorCount() 或 getFieldErrors(String field) 

BindingResult 扩展了 Errors 接口

![image-20200528210400036](\images\image-20200528210400036.png)

### 在目标方法中获取校验结果

​	在表单/命令对象类的属性中标注校验注解，在处理方法对应的入参前添加 @Valid，Spring MVC 就会实施校验并将校 验结果保存在被校验入参对象之后的 BindingResult 或 Errors 入参中。

常用方法：

​	 FieldError getFieldError(String field) 

​	 List getFieldErrors() 

​	 Object getFieldValue(String field) 

​	 Int getErrorCount()

### 在页面上显示错误

​	Spring MVC 除了会将表单/命令对象的校验结果保存到对 应的 BindingResult 或 Errors 对象中外，还会将所有校验 结果保存到 “隐含模型”

​	即使处理方法的签名中没有对应于表单/命令对象的结果入参，校验结果也会保存在 “隐含对象” 中。

​	隐含模型中的所有数据最终将通过HttpServletRequest的属性列表暴露给 JSP视图对象，因此在 JSP中可以获取错误信息

​	在 JSP 页面上可通过  \<form:errors path=“userName”> 显示错误消息

![image-20200528211048261](\images\image-20200528211048261.png)

### 提示消息的国际化

​	每个属性在数据绑定和数据校验发生错误时，都会生成一 个对应的FieldError 对象。

​	当一个属性校验失败后，校验框架会为该属性生成 4个消息代码，这些代码以校验注解类名为前缀，结合 modleAttribute、属性名及属性类型名生成多个对应的消息代码：例如 User 类中的 password 属性标准了一个 @Pattern注解，当该属性值不满足 @Pattern 所定义的规则时, 就会产生以下 4 个错误代码：

 	– Pattern.user.password

​	 – Pattern.password

​	 – Pattern.java.lang.String

​	 – Pattern

​	当使用 Spring MVC 标签显示错误消息时，Spring MVC会查看 WEB 上下文是否装配了对应的国际化消息，如果没有，则显示默认的错误消息，否则使用国际化消息

​	若数据类型转换或数据格式转换时发生错误，或该有的参数不存在，或调用处理方法时发生错误，都会在隐含模型中创建错误消息。其错误代码前缀说明如下：

​	required：必要的参数不存在。如 @RequiredParam(“param1”) 标注了一个入参，但是该参数不存在 

​	typeMismatch：在数据绑定时，发生数据类型不匹配的问题 

​	methodInvocation：Spring MVC 在调用处理方法时发生了错误

注册国际化资源文件

```xml
<!-- 配置国际化资源文件 -->
<bean id="messageSource"
	class="org.springframework.context.support.ResourceBundleMessageSource">
	<property name="basename" value="i18n"></property>
</bean>
```
# 六、HttpMessageConverter

​	HttpMessageConverter 是 Spring3.0 新添加的一个接 口，负责将请求信息转换为一个对象（类型为 T），将对象（ 类型为 T）输出为响应信息

HttpMessageConverter接口定义的方法：

​	Boolean canRead(Class clazz,MediaType mediaType): 指定转换器 可以读取的对象类型，即转换器是否可将请求信息转换为 clazz 类型的对 象，同时指定支持 MIME 类型(text/html,applaiction/json等)

​	Boolean canWrite(Class clazz,MediaType mediaType):指定转换器 是否可将 clazz 类型的对象写到响应流中，响应流支持的媒体类型 在MediaType 中定义。

​	LIst getSupportMediaTypes()：该转换器支持的媒体类 型。

​	T read(Class clazz,HttpInputMessage inputMessage)： 将请求信息流转换为 T 类型的对象。

​	void write(T t,MediaType contnetType,HttpOutputMessgae outputMessage):将T类型的对象写到响应流中，同时指定相应的媒体类 型为 contentType。

![image-20200528221612625](images\image-20200528221612625.png)

HttpMessageConverter 的实现类

![image-20200528221654264](images\image-20200528221654264.png)

DispatcherServlet 默认装配RequestMappingHandlerAdapter ，而 RequestMappingHandlerAdapter 默认装配如下 HttpMessageConverter：

![image-20200528221815700](images\image-20200528221815700.png)

加入jackson jar 包后， RequestMappingHandlerAdapter装配的HttpMessageConverter 如下：

![image-20200528221853897](images\image-20200528221853897.png)

使用 HttpMessageConverter 将请求信息转化并绑定到处理方法的入 参中或将响应结果转为对应类型的响应信息，Spring提供了两种途径：

​	使用 @RequestBody / @ResponseBody 对处理方法进行标注 

​	使用 HttpEntity / ResponseEntity 作为处理方法的入参或返回值

@RequestBody、@ResponseBody 示例

```java
@ResponseBody
@RequestMapping("/testHttpMessageConverter")
public String testHttpMessageConverter(@RequestBody String body){
	System.out.println(body);
	return "helloworld! " + new Date();
}

@ResponseBody
@RequestMapping("/testJson")
public Collection<Employee> testJson(){
	return employeeDao.getAll();
}
```
HttpEntity、ResponseEntity 示例

```java
@RequestMapping("/testResponseEntity")
public ResponseEntity<byte[]> testResponseEntity(HttpSession session) throws IOException {
    byte [] body = null;
    ServletContext servletContext = session.getServletContext();
    InputStream in = servletContext.getResourceAsStream("/files/abc.txt");
    body = new byte[in.available()];
    in.read(body);

    HttpHeaders headers = new HttpHeaders();
    headers.add("Content-Disposition", "attachment;filename=abc.txt");

    HttpStatus statusCode = HttpStatus.OK;

    ResponseEntity<byte[]> response = new ResponseEntity<byte[]>(body, headers, statusCode);
    return response;
}
```

# 七、国际化概述

默认情况下，SpringMVC根据 Accept-Language参数判断客户端的本地化类型。

当接受到请求时, SpringMVC 会在上下文中查找一个本地化解析器(LocalResolver)，找到后使用它获取请求所对应的本地化类型信息。

SpringMVC 还允许装配一个动态更改本地化类型的拦截器，这样通过指定一个请求参数就可以控制单个请求的本 地化类型。

SessionLocaleResolver & LocaleChangeInterceptor 工作原理

![image-20200529205949580](\images\image-20200529205949580.png)

### 本地化解析器和本地化拦截器

AcceptHeaderLocaleResolver：根据 HTTP 请求头的 Accept-Language 参数确定本地化类型，如果没有显式定义 本地化解析器，SpringMVC使用该解析器。

CookieLocaleResolver：根据指定的 Cookie 值确定本地化类型

SessionLocaleResolver：根据 Session中特定的属性确定本地化类型

LocaleChangeInterceptor：从请求参数中获取本次请求对应的本地化类型。

关于国际化:

​	1.在页面上能够根据浏览器语言设置的情况对文本(不是内容), 时间, 数值进行本地化处理

​	2.可以在 bean 中获取国际化资源文件 Locale 对应的消息

​	3.可以通过超链接切换 Locale, 而不再依赖于浏览器的语言设置情况

解决:

1. 使用 JSTL 的 fmt 标签

 	2. 在 bean 中注入 ResourceBundleMessageSource 的示例, 使用其对应的 getMessage 方法即可
 	3. 配置 LocalResolver 和 LocaleChangeInterceptor

```xml
<!-- 配置国际化资源文件 -->
<bean id="messageSource"
		class="org.springframework.context.support.ResourceBundleMessageSource">
	<property name="basename" value="i18n"></property>
</bean>
	
<!-- 配置 SessionLocalResolver -->
<bean id="localeResolver"
	class="org.springframework.web.servlet.i18n.SessionLocaleResolver"></bean>

<mvc:interceptors>
	<!-- 配置 LocaleChanceInterceptor -->
	<bean class="org.springframework.web.servlet.i18n.LocaleChangeInterceptor"></bean>
</mvc:interceptors>
```

# 八、文件上传

​	Spring MVC 为文件上传提供了直接的支持，这种支持是通 过即插即用的 MultipartResolver 实现的。Spring 用 Jakarta Commons FileUpload 技术实现了一个 MultipartResolver 实现类：CommonsMultipartResovler

​	Spring MVC 上下文中默认没有装配 MultipartResovler，因此默认情况下不能处理文件的上传工作，如果想使用 Spring 的文件上传功能，需现在上下文中配置 MultipartResolver

### 配置 MultipartResolver

defaultEncoding: 必须和用户 JSP 的 pageEncoding 属性 一致，以便正确解析表单的内容

为了让 CommonsMultipartResovler 正确工作，必须先 将 Jakarta Commons FileUpload 及 Jakarta Commons io 的类包添加到类路径下。

在spring mvc中支持两种上传文件的方式：

> ​		使用apache的commons-io和commons-fileupload实现文件上传
> ​		使用servlet3.0实现文件上传

使用commons组件实现文件上传

```xml
<dependency>
	<groupId>commons-io</groupId>
	<artifactId>commons-io</artifactId>
	<version>2.5</version>
</dependency>

<dependency>
	<groupId>commons-fileupload</groupId>
	<artifactId>commons-fileupload</artifactId>
	<version>1.4</version>
</dependency>
```

编写文件上传的jsp中的表单：

```jsp
<form enctype="multipart/form-data" method="post" action="/upload.do">
        图片:<input type="file" name="photo"><br>
<input type="submit" value="上传">
</form>
```

编写处理文件上传的controller，在处理文件上传的方法中需要添加MultipartFile类型的参数，MultipartFile本身是一个接口，里面提供了一些文件上传的操作的方法：

> ​		getOriginalFilename()
> ​		获得文件名
> ​		isEmpty()
> ​		判断是否上传了文件，如果没有选择文件上传的话，此时结果为true
> ​		getContentType()
> ​		获得上传文件的文件类型
> ​		transferTo(File file)
> ​		将文件上传至指定目录中
> ​		getName()
> ​		获取表单中input的name值
> ​		getBytes()
> ​		获取上传文件的byte数组
> ​		getInputStream()
> ​		获取上传文件的InputStream对象

方法中的另外一个参数HttpSession的主要作用就是获取服务器中用来存放上传文件的路径。

```java
/**
 * 文件上传
 */
@Controller
public class UploadController  {
    @RequestMapping("/upload")
    public ModelAndView upload1(MultipartFile photo, HttpSession session) throws Exception{
        ModelAndView mv = new ModelAndView();
        // 判断用户是否上传了文件
        if(!photo.isEmpty()){
            // 获取服务器中文件上传的路径
            String path = session.getServletContext().getRealPath("/upload");
            // 获取文件上传的名称
            String fileName = photo.getOriginalFilename();
            // 限制文件上传的类型
            if("image/png".equals(photo.getContentType())){
                File file = new File(path, fileName);
                // 完成文件上传
                photo.transferTo(file);
            }else {
                mv.addObject("msg", "请选择PNG格式的图片上传");
                mv.setViewName("upload_fail");
                return mv;
            }
        }else {
            mv.addObject("msg", "请上传一张png格式的图片");
            mv.setViewName("upload_fail");
            return mv;
        }
        // 跳转到成功页面
        mv.setViewName("upload_success");
        return mv;
    }
}
```

在springmvc.xml配置文件中添加multipartResolver，这里的id必须要写成multipartResolver，会有DispatcherServlet来调用，我们可以在这里设置上传文件大小、字符编码等内容：

```xml
<!-- 注册一个multipartResolver  由DispatcherServlet来调用 -->
<bean id="multipartResolver" class="org.springframework.web.multipart.commons.CommonsMultipartResolver">
	<!--设置字符编码防止文件名乱码-->
	<property name="defaultEncoding" value="utf-8"/>
	<!--设置上传文件的总大小，单位是字节b-->
	<property name="maxUploadSize" value="1048576"/>
	<!--设置单个上传文件的大小，单位是字节b-->
	<property name="maxUploadSizePerFile" value="1048576"/>
	<!--设置内存缓冲区的大小，当超过该值的时候会写入到临时目录-->
	<property name="maxInMemorySize" value="1048576"/>
	<!--设置临时目录-->
	<property name="uploadTempDir" value="tempupload"/>
	<!--默认是false，如果设置为true的话，不会将文件路径去除，在IE浏览器下上传时会将路径名也作为文件名上传：D:\image\monkey.png-->
	<property name="preserveFilename" value="false"/>
	<!--是否使用懒加载，默认是false-->
	<property name="resolveLazily" value="true"/>
</bean>
```

设置临时上传文件目录的作用：

提高安全性
	客户端上传的文件直接传到临时目录，这样子对于客户端来说隐藏了真实的文件存放目录
便于管理
	当用户取消上传或上传失败的话，直接操作临时目录即可，无需再去修改真实目录中的文件

### 使用servlet3.0实现文件上传

在web.xml中的中央控制器的servlet配置里面添加下面内容，location的标签需要写在multipart-config中的第一行：

```xml
<!-- 使用servlet3.0实现文件上传-->
<multipart-config>
	<!--临时文件路径-->
	<location>/temp</location>
	<!--单个上传文件的最大值，单位是byte-->
	<max-file-size>104876</max-file-size>
	<!--总上传文件的最大值-->
	<max-request-size>52428800</max-request-size>
	<!--内存缓冲区的大小,当超过该值时，会写入到临时文件中，单位是byte-->
	<file-size-threshold>1024</file-size-threshold>
</multipart-config>
```

然后需要在springmvc.xml文件中配置multipartResolver

```xml
<!-- 注册使用servlet3.0实现文件上传的bean -->
<bean id="multipartResolver" class="org.springframework.web.multipart.support.StandardServletMultipartResolver"/>
```

上传文件超出设定大小的异常处理

当上传文件超出指定大小时，会抛出 MaxUploadSizeExceededException 异常。通过spring mvc异常处理方式来进行处理，给用户一个友好的提示信息。

### 上传多个文件		

修改jsp，多个input的name相同：

```jsp
<form enctype="multipart/form-data" method="post" action="/upload.do">
	图片1:<input type="file" name="photos"><br>
	图片2:<input type="file" name="photos"><br>
	图片3:<input type="file" name="photos"><br>
	<input type="submit" value="上传">
</form>
```

在controller中添加方法，方法参数中需要添加MultipartFile[]，并且要在其前面加上@RequestParam注解：

```java
@Controller
public class UploadController  {
    /**
     * 处理多个文件上传
     * @param photos
     * @param session
     * @return
     * @throws Exception
     */
    @RequestMapping("/upload")
    public ModelAndView upload1(@RequestParam MultipartFile[] photos, HttpSession session) throws Exception{
        ModelAndView mv = new ModelAndView();
        // 获取服务器中文件上传的路径
        String path = session.getServletContext().getRealPath("/upload");
        for(MultipartFile photo:photos){
            // 判断用户是否上传了文件
            if(!photo.isEmpty()){
                // 获取文件上传的名称
                String fileName = photo.getOriginalFilename();
                // 限制文件上传的类型
                if("image/png".equals(photo.getContentType())){
                    File file = new File(path, fileName);
                    // 完成文件上传
                    photo.transferTo(file);
                }else {
                    mv.addObject("msg", "请选择PNG格式的图片上传");
                    mv.setViewName("upload_fail");
                    return mv;
                }
            }else {
                mv.addObject("msg", "请上传一张png格式的图片");
                mv.setViewName("upload_fail");
                return mv;
            }
        }

        // 跳转到成功页面
        mv.addObject("msg", "上传成功");
        mv.setViewName("upload_success");
        return mv;
    }
}
```

# 九、自定义拦截器

Spring MVC也可以使用拦截器对请求进行拦截处理，用户 可以自定义拦截器来实现特定的功能，自定义的拦截器必 须实现HandlerInterceptor接口

​	preHandle()：这个方法在业务处理器处理请求之前被调用，在该方法中对用户请求request 进行处理。如果程序员决定该拦截器对请求进行拦截处理后还要调用其他的拦截器，或者是业务处理器去进行处理，则返回true；如果程序员决定不需要再调用其他的组件去处理请求，则返回false

​	postHandle()：这个方法在业务处理器处理完请求后，但是DispatcherServlet向客户端返回响应前被调用，在该方法中对用户请求request进行处理。

​	afterCompletion()：这个方法在 DispatcherServlet 完全处理完请求后被调用，可以在该方法中进行一些资源清理的操作。

### 拦截器方法执行顺序

![image-20200531103736683](images\image-20200531103736683.png)

### 配置自定义拦截器

```java
/**
 * 拦截器
 * 只拦截controller的请求
 */
public class MyInterceptor implements HandlerInterceptor {
   @Override
   public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
      System.out.println("拦截器中preHandle方法");
      return true;
   }

   @Override
   public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
      System.out.println("拦截器中的postHandle");
   }

   @Override
   public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
      System.out.println("拦截器中的afterCompletion方法");
   }
}
```

在springmvc.xml文件中注册拦截器，/** 表示对所有controller拦截：

```xml
<!-- 注册拦截器 -->
<mvc:interceptors>
	<mvc:interceptor>
		<mvc:mapping path="/**"/>
		<bean class="com.harry.intercepetor.MyInterceptor"/>
	</mvc:interceptor>
</mvc:interceptors>
```

创建一个controller：

```java
@Controller
public class TestController03 {
	@RequestMapping("/test3.do")
	public ModelAndView test() throws Exception{
		ModelAndView mv = new ModelAndView();
		System.out.println("test方法");
		mv.setViewName("result");
		return mv;
	}
}
```

当有请求被该方法处理的时候，可以看到控制台中打印下面内容：

> ​		过滤器
> ​		拦截器中的preHandle方法
> ​		test方法
> ​		拦截器中的postHandle方法
> ​		拦截器中的afterCompletion方法

### 多拦截器的执行流程

![image-20200531104528641](images\image-20200531104528641.png)

### 拦截器的使用案例：权限控制

在实际应用中，我们可以使用拦截器来控制权限，比如，这里做一个这样的小功能，判断用户名是否登录

```java
@Controller
public class LoginController {
	@RequestMapping("/welcome")
	public ModelAndView welcome() throws Exception{
		ModelAndView mv = new ModelAndView();
		mv.addObject("welcome", "欢迎登录本系统");
		mv.setViewName("/welcome");
		return mv;
	}
}
```

welcome.jsp:

```jsp
<body>
	${welcome}<br>
</body>
```

定义PermissionInterceptor拦截器：

```java
/**
 * 权限拦截器
 */
public class PermissionInterceptor implements HandlerInterceptor {
   @Override
   public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
      Object user = (String)request.getSession().getAttribute("user");
      // 判断用户名为harry的用户是否已经登录
      if(!"harry".equals(user)){
         request.getRequestDispatcher("/jsp/fail.jsp").forward(request, response);
         // 不进行后续的处理
         return false;
      }
      return true;
   }

   @Override
   public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {

   }

   @Override
   public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {

   }
}
      
```

fail.jsp:

```jsp
<body>
	请先登录系统，否则无权访问该系统
</body>
```

login.jsp

```jsp
<body>
	<!--当访问该页面的时候，就表示用户已登录-->
	<%
		request.getSession().setAttribute("user", "monkey1024");
	%>
</body>

```

# 十、异常处理

Spring MVC通过HandlerExceptionResolver处理程序的异常，包括 Handler 映射、数据绑定以及目标方法执行 时发生的异常。

SpringMVC 提供的 HandlerExceptionResolver 的实现类

![image-20200531105412107](images\image-20200531105412107.png)

### HandlerExceptionResolver

使用了  \<mvc:annotation-driven/> 配置：

![image-20200531105640993](images\image-20200531105640993.png)

### ExceptionHandlerExceptionResolver

主要处理 Handler 中用 @ExceptionHandler 注解定义的 方法

@ExceptionHandler 注解定义的方法优先级问题：例如发生的是NullPointerException，但是声明的异常有 RuntimeException和 exception，此候会根据异常的最近继承关系找到继承深度最浅的那个@ExceptionHandler 注解方法，即标记了 RuntimeException 的方法

ExceptionHandlerMethodResolver内部若找不到@ExceptionHandler 注解的话，会找@ControllerAdvice中的@ExceptionHandler 注解方法

```java
@ControllerAdvice
public class SpringMVCTestExceptionHandler {

   @ExceptionHandler({ArithmeticException.class})
   public ModelAndView handleArithmeticException(Exception ex){
      System.out.println("----> 出异常了: " + ex);
      ModelAndView mv = new ModelAndView("error");
      mv.addObject("exception", ex);
      return mv;
   }
}
```

### ResponseStatusExceptionResolver

在异常及异常父类中找到@ResponseStatus 注解，然后使用这个注解的属性进行处理

定义一个@ResponseStatus注解修饰的异常类

```java
@ResponseStatus(value= HttpStatus.FORBIDDEN, reason="用户名和密码不匹配!")
public class UserNameNotMatchPasswordException extends RuntimeException{
   /**
    *
    */
   private static final long serialVersionUID = 1L;

}
```

若在处理器方法中抛出了上述异常：

​	若ExceptionHandlerExceptionResolver不解析述异常。由于触发的异常UnauthorizedException带有@ResponseStatus 注解。因此会被ResponseStatusExceptionResolver 解析 到。最后响应 HttpStatus.UNAUTHORIZED 代码给客户 端。HttpStatus.UNAUTHORIZED代表响应码401，无权限。关于其他的响应码请参考 HttpStatus 枚举类型源码。

### DefaultHandlerExceptionResolver

> 对一些特殊的异常进行处理，比 如NoSuchRequestHandlingMethodException、HttpReques tMethodNotSupportedException、HttpMediaTypeNotSuppo rtedException、HttpMediaTypeNotAcceptableException 等。

# 十一、SpingMVC的执行流程

> ​	1）用户发送请求至前端控制器 DispatcherServlet。 
> ​	2）DispatcherServlet 收到请求调用 HandlerMapping 处理器映射器。
> ​	3）处理器映射器找到具体的处理器(可以根据 xml 配置、注解进行查找)，生成处理器对象及处理器拦截器(如果有则生成)一并返回给 DispatcherServlet。
> ​	4）DispatcherServlet 调用 HandlerAdapter 处理器适配器。
> ​	5）HandlerAdapter 经过适配调用具体的处理器(Controller，也叫后端控制器)。
> ​	6）Controller 执行完成返回 ModelAndView。
> ​	7）HandlerAdapter 将 controller 执行结果 ModelAndView 返回给 DispatcherServlet。
> ​	8）DispatcherServlet 将 ModelAndView 传给 ViewReslover 视图解析器。
> ​	9）ViewReslover 解析后返回具体 View。
> ​	10）DispatcherServlet 根据 View 进行渲染视图（即将模型数据填充至视图中）。
> ​	11）DispatcherServlet 响应用户

![image-20200531110743497](images\image-20200531110743497.png)

