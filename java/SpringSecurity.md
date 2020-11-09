# 一 基本概念

## 1 什么是认证

   进入移动互联网时代，大家每天都在刷手机，常用的软件有微信、支付宝、头条等，下边拿微信来举例子说明认证 相关的基本概念，在初次使用微信前需要注册成为微信用户，然后输入账号和密码即可登录微信，输入账号和密码 登录微信的过程就是认证。

系统为什么要认证？
认证是为了保护系统的隐私数据与资源，用户的身份合法方可访问该系统的资源。

认证 ：用户认证就是判断一个用户的身份是否合法的过程，用户去访问系统资源时系统要求验证用户的身份信 息，身份合法方可继续访问，不合法则拒绝访问。常见的用户身份认证方式有：用户名密码登录，二维码登录，手 机短信登录，指纹认证等方式。 

## 2 什么是会话

​    用户认证通过后，为了避免用户的每次操作都进行认证可将用户的信息保证在会话中。会话就是系统为了保持当前 用户的登录状态所提供的机制，常见的有基于session方式、基于token方式等。
  基于session的认证方式如下图：

   它的交互流程是，用户认证成功后，在服务端生成用户相关的数据保存在session(当前会话)中，发给客户端的 sesssion_id 存放到 cookie 中，这样用户客户端请求时带上 session_id 就可以验证服务器端是否存在 session 数 据，以此完成用户的合法校验，当用户退出系统或session过期销毁时,客户端的session_id也就无效了。

![image-20200907193450657](images\image-20200907193450657.png)

  基于token方式如下图：

  它的交互流程是，用户认证成功后，服务端生成一个token发给客户端，客户端可以放到 cookie 或 localStorage 等存储中，每次请求时带上 token，服务端收到token通过验证后即可确认用户身份。

![image-20200907193549232](images\image-20200907193549232.png)

  基于session的认证方式由Servlet规范定制，服务端要存储session信息需要占用内存资源，客户端需要支持 cookie；基于token的方式则一般不需要服务端存储token，并且不限制客户端的存储方式。如今移动互联网时代 更多类型的客户端需要接入系统，系统多是采用前后端分离的架构进行实现，所以基于token的方式更适合

## 3 什么是授权 

   还拿微信来举例子，微信登录成功后用户即可使用微信的功能，比如，发红包、发朋友圈、添加好友等，没有绑定 银行卡的用户是无法发送红包的，绑定银行卡的用户才可以发红包，发红包功能、发朋友圈功能都是微信的资源即 功能资源，用户拥有发红包功能的权限才可以正常使用发送红包功能，拥有发朋友圈功能的权限才可以使用发朋友 圈功能，这个根据用户的权限来控制用户使用资源的过程就是授权。

### 授权的数据模型 


授权可简单理解为Who对What(which)进行How操作，包括如下：

   Who，即主体（Subject），主体一般是指用户，也可以是程序，需要访问系统中的资源。   What，即资源 （Resource），如系统菜单、页面、按钮、代码方法、系统商品信息、系统订单信息等。系统菜单、页面、按 钮、代码方法都属于系统功能资源，对于web系统每个功能资源通常对应一个URL；系统商品信息、系统订单信息 都属于实体资源（数据资源），实体资源由资源类型和资源实例组成，比如商品信息为资源类型，商品编号 为001 的商品为资源实例。   How，权限/许可（Permission），规定了用户对资源的操作许可，权限离开资源没有意义， 如用户查询权限、用户添加权限、某个代码方法的调用权限、编号为001的用户的修改权限等，通过权限可知用户 对哪些资源都有哪些操作许可。
主体、资源、权限关系如下图：

​	

![image-20200907193951682](images\image-20200907193951682.png)

## 4 基于Session的认证方式

  基于Session认证方式的流程是，用户认证成功后，在服务端生成用户相关的数据保存在session(当前会话)，而发 给客户端的 sesssion_id 存放到 cookie 中，这样用客户端请求时带上 session_id 就可以验证服务器端是否存在 session 数据，以此完成用户的合法校验。当用户退出系统或session过期销毁时,客户端的session_id也就无效了。 下图是session认证方式的流程图：

![image-20200907194255577](images\image-20200907194255577.png)

  基于Session的认证机制由Servlet规范定制，Servlet容器已实现，用户通过HttpSession的操作方法即可实现，如 下是HttpSession相关的操作API

![image-20200907194344551](images\image-20200907194344551.png)

### 1、 Spring 容器配置 

```java
@Configuration
@ComponentScan(basePackages = "com.harry.security", excludeFilters = {@ComponentScan.Filter(type = FilterType.ANNOTATION, value = Controller.class)})
public class ApplicationConfig {
    //在此配置除了Controller的其它bean，比如：数据库链接池、事务管理器、业务bean
}
```

### 2、 servletContext配置 

本案例采用Servlet3.0无web.xml方式，的conﬁg包下定义WebConﬁg.java，它对应s对应于DispatcherServlet配 置。

```java
@Configuration
@EnableWebMvc
@ComponentScan(basePackages = "com.harry.security",includeFilters = {@ComponentScan.Filter(type = FilterType.ANNOTATION,value = Controller.class)})
public class WebConfig extends WebMvcConfigurerAdapter {

    //视频解析器
    @Bean
    public InternalResourceViewResolver viewResolver(){
        InternalResourceViewResolver viewResolver = new InternalResourceViewResolver();
        viewResolver.setPrefix("/WEB-INF/view/");
        viewResolver.setSuffix(".jsp");
        return viewResolver;
    }

    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        registry.addViewController("/").setViewName("redirect:/login");
    }
}
```

### 3、 加载 Spring容器 

在init包下定义Spring容器初始化类SpringApplicationInitializer，此类实现WebApplicationInitializer接口， Spring容器启动时加载WebApplicationInitializer接口的所有实现类。

```java
public class SpringApplicationInitializer extends AbstractAnnotationConfigDispatcherServletInitializer {
    @Override
    protected Class<?>[] getRootConfigClasses() {
        return new Class[] { ApplicationConfig.class}; // 指定rootContext的配置类
    }

    @Override
    protected Class<?>[] getServletConfigClasses() {
        return new Class[] {WebConfig.class}; // 指定servletContext的配置类
    }

    @Override
    protected String[] getServletMappings() {
        return new String[] {"/"};
    }
}
```

### 4、 认证页面

  在webapp/WEB-INF/views下定义认证页面login.jsp，本案例只是测试认证流程，页面没有添加css样式，页面实 现可填入用户名，密码，触发登录将提交表单信息至/login，内容如下：

```jsp
<%@ page contentType="text/html;charset=UTF-8" pageEncoding="utf-8" %>
<html>
<head>
    <title>用户登录</title>
</head>
<body>
<form action="login" method="post">
    用户名：<input type="text" name="username"><br>
    密&nbsp;&nbsp;&nbsp;码:
    <input type="password" name="password"><br>
    <input type="submit" value="登录">
</form>
</body>
</html>
```

在WebConﬁg中新增如下配置，将/直接导向login.jsp页面：

```java
@Override
public void addViewControllers(ViewControllerRegistry registry) {
    registry.addViewController("/").setViewName("redirect:/login");
}
```

### 5、认证接口

用户进入认证页面，输入账号和密码，点击登录，请求/login进行身份认证。 

（1）定义认证接口，此接口用于对传来的用户名、密码校验，若成功则返回该用户的详细信息，否则抛出错误异 常：

```java
public interface AuthenticationService {
    /**
     * 用户认证
     * @param authenticationRequest 用户认证请求，账号和密码
     * @return 认证成功的用户信息
     */
    UserDto authentication(AuthenticationRequest authenticationRequest);

}
```

```java
@Service
public class AuthenticationServiceImpl implements  AuthenticationService{
    /**
     * 用户认证，校验用户身份信息是否合法
     *
     * @param authenticationRequest 用户认证请求，账号和密码
     * @return 认证成功的用户信息
     */
    @Override
    public UserDto authentication(AuthenticationRequest authenticationRequest) {
        //校验参数是否为空
        if(authenticationRequest == null
            || StringUtils.isEmpty(authenticationRequest.getUsername())
            || StringUtils.isEmpty(authenticationRequest.getPassword())){
            throw new RuntimeException("账号和密码为空");
        }
        //根据账号去查询数据库,这里测试程序采用模拟方法
        UserDto user = getUserDto(authenticationRequest.getUsername());
        //判断用户是否为空
        if(user == null){
            throw new RuntimeException("查询不到该用户");
        }
        //校验密码
        if(!authenticationRequest.getPassword().equals(user.getPassword())){
            throw new RuntimeException("账号或密码错误");
        }
        //认证通过，返回用户身份信息
        return user;
    }
    //根据账号查询用户信息
    private UserDto getUserDto(String userName){
        return userMap.get(userName);
    }
    //用户信息
    private Map<String,UserDto> userMap = new HashMap<>();
    {
        Set<String> authorities1 = new HashSet<>();
        authorities1.add("p1");//这个p1我们人为让它和/r/r1对应
        Set<String> authorities2 = new HashSet<>();
        authorities2.add("p2");//这个p2我们人为让它和/r/r2对应
        userMap.put("zhangsan",new UserDto("1010","zhangsan","123","张三","133443",authorities1));
        userMap.put("lisi",new UserDto("1011","lisi","456","李四","144553",authorities2));
    }
}
```

（2）登录Controller，对/login请求处理，它调用AuthenticationService完成认证并返回登录结果提示信息：

```java
@RestController
public class LoginController {

    @Autowired
    AuthenticationService authenticationService;

    @RequestMapping(value = "/login",produces = "text/plain;charset=utf-8")
    public String login(AuthenticationRequest authenticationRequest, HttpSession session){
        UserDto userDto = authenticationService.authentication(authenticationRequest);
        //存入session
        session.setAttribute(UserDto.SESSION_USER_KEY,userDto);
        return userDto.getUsername() +"登录成功";
    }

    @GetMapping(value = "/logout",produces = {"text/plain;charset=UTF-8"})
    public String logout(HttpSession session){
        session.invalidate();
        return "退出成功";
    }

    @GetMapping(value = "/r/r1",produces = {"text/plain;charset=UTF-8"})
    public String r1(HttpSession session){
        String fullname = null;
        Object object = session.getAttribute(UserDto.SESSION_USER_KEY);
        if(object == null){
            fullname = "匿名";
        }else{
            UserDto userDto = (UserDto) object;
            fullname = userDto.getFullname();
        }
        return fullname+"访问资源r1";
    }
    @GetMapping(value = "/r/r2",produces = {"text/plain;charset=UTF-8"})
    public String r2(HttpSession session){
        String fullname = null;
        Object userObj = session.getAttribute(UserDto.SESSION_USER_KEY);
        if(userObj != null){
            fullname = ((UserDto)userObj).getFullname();
        }else{
            fullname = "匿名";
        }
        return fullname + " 访问资源2";
    }
}
```

# 二 Spring Security快速上手 

## 1、Spring Security介绍

   Spring Security是一个能够为基于Spring的企业应用系统提供声明式的安全访问控制解决方案的安全框架。由于它 是Spring生态系统中的一员，因此它伴随着整个Spring生态系统不断修正、升级，在spring boot项目中加入spring security更是十分简单，使用Spring Security 减少了为企业系统安全控制编写大量重复代码的工作

依赖引入：

```xml
    <dependency>
        <groupId>org.springframework.security</groupId>
        <artifactId>spring-security-web</artifactId>
        <version>5.1.4.RELEASE</version>
    </dependency>

    <dependency>
        <groupId>org.springframework.security</groupId>
        <artifactId>spring-security-config</artifactId>
        <version>5.1.4.RELEASE</version>
    </dependency>
```
## 2、认证

springSecurity默认提供认证页面，不需要额外开发。

### 安全配置

  spring security提供了用户名密码登录、退出、会话管理等认证功能，只需要配置即可使用。
  1) 在conﬁg包下定义WebSecurityConﬁg，安全配置的内容包括：用户信息、密码编码器、安全拦截机制

```java
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {

    // 配置用户信息服务
    @Bean
    public UserDetailsService userDetailsService() {
        InMemoryUserDetailsManager manager = new InMemoryUserDetailsManager();
        manager.createUser(User.withUsername("zhangsan").password("123").authorities("p1").build());
        manager.createUser(User.withUsername("lisi").password("456").authorities("p2").build());
        return manager;
    }

    @Bean
    public PasswordEncoder passwordEncoder(){
        return NoOpPasswordEncoder.getInstance();
    }
    
    // 配置安全拦截机制
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests().
                antMatchers("/r/**").authenticated()
                .anyRequest().permitAll()
                .and()
                .formLogin().successForwardUrl("/login-success");
    }
}
```

在userDetailsService()方法中，我们返回了一个UserDetailsService给spring容器，Spring Security会使用它来 获取用户信息。我们暂时使用InMemoryUserDetailsManager实现类，并在其中分别创建了zhangsan、lisi两个用 户，并设置密码和权限。

 而在conﬁgure()中，我们通过HttpSecurity设置了安全拦截规则，其中包含了以下内容：
  （1）url匹配/r/**的资源，经过认证后才能访问。
  （2）其他url完全开放。

  （3）支持form表单认证，认证成功后转向/login-success。 

### Spring Security初始化

Spring Security初始化，这里有两种情况 若当前环境没有使用Spring或Spring MVC，则需要将 WebSecurityConﬁg(Spring Security配置类) 传入超 类，以确保获取配置，并创建spring context。

相反，若当前环境已经使用spring，我们应该在现有的springContext中注册Spring Security(上一步已经做将 WebSecurityConﬁg加载至rootcontext)，此方法可以什么都不做。 

在init包下定义SpringSecurityApplicationInitializer：

```java
public class SpringSecurityApplicationInitializer extends AbstractSecurityWebApplicationInitializer {
    public SpringSecurityApplicationInitializer() {
        //super(WebSecurityConfig.class);
    }     
}
```

## 3、测试

（1）启动项目，访问http://localhost:8080/security-spring-security/路径地址

  页面会根据WebConﬁg中addViewControllers配置规则，跳转至/login，/login是pring Security提供的登录页面

（2）登录 

  输入错误的用户名、密码

## 4、授权

实现授权需要对用户的访问进行拦截校验，校验用户的权限是否可以操作指定的资源，Spring Security默认提供授 权实现方法。
在LoginController添加/r/r1或/r/r2

在安全配置类WebSecurityConﬁg.java中配置授权规则：

```java
//安全拦截机制（最重要）
@Override
protected void configure(HttpSecurity http) throws Exception {
    http.authorizeRequests()
            .antMatchers("/r/r1").hasAuthority("p1")
            .antMatchers("/r/r2").hasAuthority("p2")
            .antMatchers("/r/**").authenticated()//所有/r/**的请求必须认证通过
            .anyRequest().permitAll()//除了/r/**，其它的请求可以访问
            .and()
            .formLogin()//允许表单登录
            .successForwardUrl("/login-success");//自定义登录成功的页面地址

}
```

# 三 Spring Security 应用详解

## 1、集成SpringBoot 

  Spring Boot是一套Spring的快速开发框架，基于Spring 4.0设计，使用Spring Boot开发可以避免一些繁琐的工程 搭建和配置，同时它集成了大量的常用框架，快速导入依赖包，避免依赖包的冲突。基本上常用的开发框架都支持 Spring Boot开发，例如：MyBatis、Dubbo等，Spring 家族更是如此，例如：Spring cloud、Spring mvc、 Spring security等，使用Spring Boot开发可以大大得高生产率，所以Spring Boot的使用率非常高。
本章节讲解如何通过Spring Boot开发Spring Security应用，Spring Boot提供spring-boot-starter-security用于开 发Spring Security应用。

### 引入依赖

```xml
    <dependencies>
        <!-- 以下是>spring boot依赖-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <!-- 以下是>spring security依赖-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>


        <!-- 以下是jsp依赖-->
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
            <scope>provided</scope>
        </dependency>
        <!--jsp页面使用jstl标签 -->
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>jstl</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-tomcat</artifactId>
            <scope>provided</scope>
        </dependency>
        <!--用于编译jsp -->
        <dependency>
            <groupId>org.apache.tomcat.embed</groupId>
            <artifactId>tomcat-embed-jasper</artifactId>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>1.18.0</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-jdbc</artifactId>
        </dependency>

        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>5.1.47</version>
        </dependency>
    </dependencies>
```

### application.properity

```properties
server.port=8080
server.servlet.context-path=/security-springboot
spring.application.name = security-springboot
spring.mvc.view.suffix=.jsp 
spring.mvc.view.prefix=/WEB‐INF/views
```

###  Servlet Context配置 

```java
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        registry.addViewController("/").setViewName("redirect:/login-view");
        registry.addViewController("/login-view").setViewName("login");
    }
}
```

### 安全配置

由于Spring boot starter自动装配机制，这里无需使用@EnableWebSecurity，WebSecurityConﬁg内容如下

```java
@EnableWebSecurity
@Configuration
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {

    //定义用户信息服务（查询用户信息）
    @Bean
    public UserDetailsService userDetailsService(){
        InMemoryUserDetailsManager manager = new InMemoryUserDetailsManager();
        manager.createUser(User.withUsername("zhangsan").password("123").authorities("p1").build());
        manager.createUser(User.withUsername("lisi").password("456").authorities("p2").build());
        return manager;
    }

    //密码编码器
    @Bean
    public PasswordEncoder passwordEncoder(){
        return NoOpPasswordEncoder.getInstance();
    }

    //安全拦截机制（最重要）
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests()
                .antMatchers("/r/r1").hasAuthority("p1")
                .antMatchers("/r/r2").hasAuthority("p2")
                .antMatchers("/r/**").authenticated()//所有/r/**的请求必须认证通过
                .anyRequest().permitAll()//除了/r/**，其它的请求可以访问
                .and()
                .formLogin()//允许表单登录
                .successForwardUrl("/login-success");//自定义登录成功的页面地址

    }
}
```

## 2、工作原理

​    Spring Security所解决的问题就是安全访问控制，而安全访问控制功能其实就是对所有进入系统的请求进行拦截， 校验每个请求是否能够访问它所期望的资源。根据前边知识的学习，可以通过Filter或AOP等技术来实现，Spring Security对Web资源的保护是靠Filter实现的，所以从这个Filter来入手，逐步深入Spring Security原理。

​    当初始化Spring Security时，会创建一个名为 SpringSecurityFilterChain 的Servlet过滤器，类型为 org.springframework.security.web.FilterChainProxy，它实现了javax.servlet.Filter，因此外部的请求会经过此 类，下图是Spring Security过虑器链结构图：

![image-20200910201253426](images\image-20200910201253426.png)

​    FilterChainProxy是一个代理，真正起作用的是FilterChainProxy中SecurityFilterChain所包含的各个Filter，同时 这些Filter作为Bean被Spring管理，它们是Spring Security核心，各有各的职责，但他们并不直接处理用户的认 证，也不直接处理用户的授权，而是把它们交给了认证管理器（AuthenticationManager）和决策管理器 （AccessDecisionManager）进行处理，下图是FilterChainProxy相关类的UML图示。

![image-20200910201420060](images\image-20200910201420060.png)

spring Security功能的实现主要是由一系列过滤器链相互配合完成

![image-20200910201458190](images\image-20200910201458190.png)

下面介绍过滤器链中主要的几个过滤器及其作用：

​    **SecurityContextPersistenceFilte**r： 这个Filter是整个拦截过程的入口和出口（也就是第一个和后一个拦截 器），会在请求开始时从配置好的 SecurityContextRepository 中获取 SecurityContext，然后把它设置给 SecurityContextHolder。在请求完成后将 SecurityContextHolder 持有的 SecurityContext 再保存到配置好 的 SecurityContextRepository，同时清除 securityContextHolder 所持有的 SecurityContext； 

​    **UsernamePasswordAuthenticationFilter**： 用于处理来自表单提交的认证。该表单必须提供对应的用户名和密 码，其内部还有登录成功或失败后进行处理的 AuthenticationSuccessHandler 和 AuthenticationFailureHandler，这些都可以根据需求做相关改变；

​    **FilterSecurityInterceptor** ：是用于保护web资源的，使用AccessDecisionManager对当前用户进行授权访问，前面已经详细介绍过了；

​    **ExceptionTranslationFilter** ：能够捕获来自 FilterChain 所有的异常，并进行处理。但是它只会处理两类异常： AuthenticationException 和 AccessDeniedException，其它的异常它会继续抛出。

### 认证流程

![image-20200910201813648](images\image-20200910201813648.png)

1. 用户提交用户名、密码被SecurityFilterChain中的 UsernamePasswordAuthenticationFilter 过滤器获取到， 封装为请求Authentication，通常情况下是UsernamePasswordAuthenticationToken这个实现类。

2. 然后过滤器将Authentication提交至认证管理器（AuthenticationManager）进行认证

3. 认证成功后， AuthenticationManager 身份管理器返回一个被填充满了信息的（包括上面提到的权限信息， 身份信息，细节信息，但密码通常会被移除） Authentication 实例。

4. SecurityContextHolder 安全上下文容器将第3步填充了信息的 Authentication ，通过SecurityContextHolder.getContext().setAuthentication(…)方法，设置到其中。

认证核心组件的大体关系如下：

![image-20200910202601691](images\image-20200910202601691.png)

### AuthenticationProvide

AuthenticationProvider是一个接口，定义如下：

```java
public interface AuthenticationProvider { 
        Authentication authenticate(Authentication authentication) throws AuthenticationException;    
        boolean supports(Class<?> var1);
}
```

authenticate()方法定义了认证的实现过程，它的参数是一个Authentication，里面包含了登录用户所提交的用 户、密码等。而返回值也是一个Authentication，这个Authentication则是在认证成功后，将用户的权限及其他信 息重新组装后生成。

  Spring Security中维护着一个 List<AuthenticationProvider> 列表，存放多种认证方式，不同的认证方式使用不 同的AuthenticationProvider。如使用用户名密码登录时，使用AuthenticationProvider1，短信登录时使用 AuthenticationProvider2等等这样的例子很多。 

  每个AuthenticationProvider需要实现supports（）方法来表明自己支持的认证方式，如我们使用表单方式认证， 在提交请求时Spring Security会生成UsernamePasswordAuthenticationToken，它是一个Authentication，里面 封装着用户提交的用户名、密码信息。

我们在DaoAuthenticationProvider的基类AbstractUserDetailsAuthenticationProvider发现以下代码：

```java
public boolean supports(Class<?> authentication) {
    return UsernamePasswordAuthenticationToken.class.isAssignableFrom(authentication);
}
```

也就是说当web表单提交用户名密码时，Spring Security由DaoAuthenticationProvider处理

最后，我们来看一下Authentication(认证信息)的结构，它是一个接口，我们之前提到的 UsernamePasswordAuthenticationToken就是它的实现之一：

```java
public interface Authentication extends Principal, Serializable {
    Collection<? extends GrantedAuthority> getAuthorities();

    Object getCredentials();

    Object getDetails();

    Object getPrincipal();

    boolean isAuthenticated();

    void setAuthenticated(boolean var1) throws IllegalArgumentException;
}
```

（1）Authentication是spring security包中的接口，直接继承自Principal类，而Principal是位于 java.security 包中的。它是表示着一个抽象主体身份，任何主体都有一个名称，因此包含一个getName()方法。
（2）getAuthorities()，权限信息列表，默认是GrantedAuthority接口的一些实现类，通常是代表权限信息的一系 列字符串。
（3）getCredentials()，凭证信息，用户输入的密码字符串，在认证过后通常会被移除，用于保障安全。 

（4）getDetails()，细节信息，web应用中的实现接口通常为 WebAuthenticationDetails，它记录了访问者的ip地 址和sessionId的值。
（5）getPrincipal()，身份信息，大部分情况下返回的是UserDetails接口的实现类，UserDetails代表用户的详细 信息，那从Authentication中取出来的UserDetails就是当前登录用户信息，它也是框架中的常用接口之一。 

### UserDetailsService

现在咱们现在知道DaoAuthenticationProvider处理了web表单的认证逻辑，认证成功后既得到一个 Authentication(UsernamePasswordAuthenticationToken实现)，里面包含了身份信息（Principal）。这个身份 信息就是一个 Object ，大多数情况下它可以被强转为UserDetails对象。 

DaoAuthenticationProvider中包含了一个UserDetailsService实例，它负责根据用户名提取用户信息 UserDetails(包含密码)，而后DaoAuthenticationProvider会去对比UserDetailsService提取的用户密码与用户提交 的密码是否匹配作为认证成功的关键依据，因此可以通过将自定义的 UserDetailsService 公开为spring bean来定 义自定义身份验证。

```java
public interface UserDetailsService {
    UserDetails loadUserByUsername(String var1) throws UsernameNotFoundException;
}
```

很多人把DaoAuthenticationProvider和UserDetailsService的职责搞混淆，其实UserDetailsService只负责从特定 的地方（通常是数据库）加载用户信息，仅此而已。而DaoAuthenticationProvider的职责更大，它完成完整的认 证流程，同时会把UserDetails填充至Authentication。

#### 自定义UserDetailsService

```java
public class SpringDataUserDetailsService implements UserDetailsService {

    @Autowired
    UserDao userDao;

    // 根据账号查询用户信息
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        UserDto userDto = userDao.getUserByUsername(username);
        if (userDto == null){
            //如果用户查不到，返回null，由provider来抛出异常
            return null;
        }
        //根据用户的id查询用户的权限
        List<String> permissions = userDao.findPermissionsByUserId(userDto.getId());
        //将permissions转成数组
        String[] permissionArray = new String[permissions.size()];
        permissions.toArray(permissionArray);
        UserDetails userDetails = User.withUsername(userDto.getUsername()).password(userDto.getPassword()).authorities(permissionArray).build();
        return userDetails;
    }
}
```

### PasswordEncoder

  DaoAuthenticationProvider认证处理器通过UserDetailsService获取到UserDetails后，它是如何与请求 Authentication中的密码做对比呢？
  在这里Spring Security为了适应多种多样的加密类型，又做了抽象，DaoAuthenticationProvider通过 PasswordEncoder接口的matches方法进行密码的对比，而具体的密码对比细节取决于实现：

```java
public interface PasswordEncoder {
    String encode(CharSequence var1);

    boolean matches(CharSequence var1, String var2);

    default boolean upgradeEncoding(String encodedPassword) {
        return false;
    }
}
```

而Spring Security提供很多内置的PasswordEncoder，能够开箱即用，使用某种PasswordEncoder只需要进行如 下声明即可，如下

```java
@Bean
public PasswordEncoder passwordEncoder(){
    return NoOpPasswordEncoder.getInstance();
}
```

NoOpPasswordEncoder采用字符串匹配方法，不对密码进行加密比较处理，密码比较流程如下：
1、用户输入密码（明文 ）

2、DaoAuthenticationProvider获取UserDetails（其中存储了用户的正确密码）

3、DaoAuthenticationProvider使用PasswordEncoder对输入的密码和正确的密码进行校验，密码一致则校验通 过，否则校验失败。

实际项目中推荐使用BCryptPasswordEncoder, Pbkdf2PasswordEncoder, SCryptPasswordEncoder等

```java
@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder();
}
```

生成方法

```java
@RunWith(SpringRunner.class)
public class TestBCrypt {
    public void test1(){
    //对原始密码加密          
    String hashpw = BCrypt.hashpw("123",BCrypt.gensalt());
     System.out.println(hashpw);
     //校验原始密码和BCrypt密码是否一致         
     boolean checkpw = BCrypt.checkpw("123", "$2a$10$NlBC84MVb7F95EXYTXwLneXgCca6/GipyWR5NHm8K0203bSQMLpvm"); 
     System.out.println(checkpw);
    }}
    
```

## 3、授权流程

Spring Security的授权流程如下：

![image-20200915212058262](images\image-20200915212058262.png)

1. 拦截请求，已认证用户访问受保护的web资源将被SecurityFilterChain中的 FilterSecurityInterceptor 的子类拦截。

2. 获取资源访问策略，FilterSecurityInterceptor会从 SecurityMetadataSource 的子类 DefaultFilterInvocationSecurityMetadataSource 获取要访问当前资源所需要的权限 Collection\<ConfigAttribute\> 

3. FilterSecurityInterceptor会调用 AccessDecisionManager 进行授权决策，若决策通过，则允许访问资 源，否则将禁止访问。

### 授权决策

AccessDecisionManager采用投票的方式来确定是否能够访问受保护资源。

![image-20200915212820184](images\image-20200915212820184.png)

通过上图可以看出，AccessDecisionManager中包含的一系列AccessDecisionVoter将会被用来对Authentication 是否有权访问受保护对象进行投票，AccessDecisionManager根据投票结果，做出终决策。

AccessDecisionVoter是一个接口，其中定义有三个方法，具体结构如下所示。

```java
public interface AccessDecisionVoter<S> {
    int ACCESS_GRANTED = 1;
    int ACCESS_ABSTAIN = 0;
    int ACCESS_DENIED = -1;

    boolean supports(ConfigAttribute var1);

    boolean supports(Class<?> var1);

    int vote(Authentication var1, S var2, Collection<ConfigAttribute> var3);
}
```

  vote()方法的返回结果会是AccessDecisionVoter中定义的三个常量之一。ACCESS_GRANTED表示同意， ACCESS_DENIED表示拒绝，ACCESS_ABSTAIN表示弃权。如果一个AccessDecisionVoter不能判定当前 Authentication是否拥有访问对应受保护对象的权限，则其vote()方法的返回值应当为弃权ACCESS_ABSTAIN。 

Spring Security内置了三个基于投票的AccessDecisionManager实现类如下，它们分别是 AﬃrmativeBased、ConsensusBased和UnanimousBased。

   AﬃrmativeBased的逻辑是：        

​    （1）只要有AccessDecisionVoter的投票为ACCESS_GRANTED则同意用户进行访问；
​    （2）如果全部弃权也表示通过；

​    （3）如果没有一个人投赞成票，但是有人投反对票，则将抛出AccessDeniedException。 Spring security默认使用的是AﬃrmativeBased。

  ConsensusBased的逻辑是：

​       （1）如果赞成票多于反对票则表示通过。
​       （2）反过来，如果反对票多于赞成票则将抛出AccessDeniedException。       

​       （3）如果赞成票与反对票相同且不等于0，并且属性allowIfEqualGrantedDeniedDecisions的值为true，则表 示通过，否则将抛出异常AccessDeniedException。参数allowIfEqualGrantedDeniedDecisions的值默认为true。
​       （4）如果所有的AccessDecisionVoter都弃权了，则将视参数allowIfAllAbstainDecisions的值而定，如果该值 为true则表示通过，否则将抛出异常AccessDeniedException。参数allowIfAllAbstainDecisions的值默认为false

   UnanimousBased的逻辑与另外两种实现有点不一样，另外两种会一次性把受保护对象的配置属性全部传递给AccessDecisionVoter进行投票，而UnanimousBased会一次只传递一个ConﬁgAttribute给 AccessDecisionVoter进行投票。这也就意味着如果我们的AccessDecisionVoter的逻辑是只要传递进来的 ConﬁgAttribute中有一个能够匹配则投赞成票，但是放到UnanimousBased中其投票结果就不一定是赞成了。 UnanimousBased的逻辑具体来说是这样的：
       （1）如果受保护对象配置的某一个ConﬁgAttribute被任意的AccessDecisionVoter反对了，则将抛出 AccessDeniedException。        

​       （2）如果没有反对票，但是有赞成票，则表示通过。
​       （3）如果全部弃权了，则将视参数allowIfAllAbstainDecisions的值而定，true则通过，false则抛出 AccessDeniedException。 

## 4、自定义认证

  Spring Security提供了非常好的认证扩展方法，比如：快速上手中将用户信息存储到内存中，实际开发中用户信息 通常在数据库，Spring security可以实现从数据库读取用户信息，Spring security还支持多种授权方法。

### 自定义登录页面

在WebConﬁg.java中配置认证页面地址：

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        registry.addViewController("/").setViewName("redirect:/login-view");
        registry.addViewController("/login-view").setViewName("login");
    }
}
```

在WebSecurityConﬁg中配置表章登录信息：

```java
    //安全拦截机制（最重要）
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.csrf().disable()
                .authorizeRequests()
//                .antMatchers("/r/r1").hasAuthority("p2")
//                .antMatchers("/r/r2").hasAuthority("p2")
                .antMatchers("/r/**").authenticated()//所有/r/**的请求必须认证通过
                .anyRequest().permitAll()//除了/r/**，其它的请求可以访问
                .and()
                .formLogin()//允许表单登录
                .loginPage("/login-view")//登录页面
                .loginProcessingUrl("/login")
                .successForwardUrl("/login-success")//自定义登录成功的页面地址
                .and()
                .sessionManagement()
                .sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED)
                .and()
                .logout()
                .logoutUrl("/logout")
                .logoutSuccessUrl("/login-view?logout");


    }
```

## 5、连接数据库认证

#### 创建数据库

创建user_db数据

```sql
CREATE DATABASE `user_db` CHARACTER SET 'utf8' COLLATE 'utf8_general_ci'; 
```

创建t_user表

```sql
CREATE TABLE `t_user` (    
    `id` bigint(20) NOT NULL COMMENT '用户id',    
    `username` varchar(64) NOT NULL,  
    `password` varchar(64) NOT NULL,    
    `fullname` varchar(255) NOT NULL COMMENT '用户姓名',    
    `mobile` varchar(11) DEFAULT NULL COMMENT '手机号',   
    PRIMARY KEY (`id`) USING BTREE  ) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC
```

#### 代码实现

1）定义dataSource 在application.properties配置

```properties
spring.datasource.url=jdbc:mysql://192.168.30.129:3306/user_db
spring.datasource.username=root
spring.datasource.password=123456
spring.datasource.driver-class-name=com.mysql.jdbc.Driver
```

2）添加依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jdbc</artifactId>
</dependency>

<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>5.1.47</version>
</dependency>
```

3）定义Dao

定义模型类型，在model包定义UserDto

```java
package com.harry.security.model;

import lombok.Data;

/**
 * @author Administrator
 * @version 1.0
 **/
@Data
public class UserDto {
    private String id;
    private String username;
    private String password;
    private String fullname;
    private String mobile;
}
```

在Dao包定义UserDao：

```java
@Repository
public class UserDao {

    @Autowired
    JdbcTemplate jdbcTemplate;

    //根据账号查询用户信息
    public UserDto getUserByUsername(String username){
        String sql = "select id,username,password,fullname,mobile from t_user where username = ?";
        //连接数据库查询用户
        List<UserDto> list = jdbcTemplate.query(sql, new Object[]{username}, new BeanPropertyRowMapper<>(UserDto.class));
        if(list !=null && list.size()==1){
            return list.get(0);
        }
        return null;
    }

}
```

#### 定义UserDetailService 

在service包下定义SpringDataUserDetailsService：

```java
public class SpringDataUserDetailsService implements UserDetailsService {

    @Autowired
    UserDao userDao;

    // 根据账号查询用户信息
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        UserDto userDto = userDao.getUserByUsername(username);
        if (userDto == null){
            //如果用户查不到，返回null，由provider来抛出异常
            return null;
        }
        //根据用户的id查询用户的权限
        List<String> permissions = userDao.findPermissionsByUserId(userDto.getId());
        //将permissions转成数组
        String[] permissionArray = new String[permissions.size()];
        permissions.toArray(permissionArray);
        UserDetails userDetails = User.withUsername(userDto.getUsername()).password(userDto.getPassword()).authorities(permissionArray).build();
        return userDetails;
    }
}
```

## 6、会话

  用户认证通过后，为了避免用户的每次操作都进行认证可将用户的信息保存在会话中。spring security提供会话管 理，认证通过后将身份信息放入SecurityContextHolder上下文，SecurityContext与当前线程进行绑定，方便获取 用户身份。 

#### 获取用户身份

  编写LoginController，实现/r/r1、/r/r2的测试资源，并修改loginSuccess方法，注意getUsername方法，Spring Security获取当前登录用户信息的方法为SecurityContextHolder.getContext().getAuthentication()

```java
@RestController
public class LoginController {
    @RequestMapping(value = "/login-success")
    public String loginSuccess(){
        String username = getUsername();
        return username+"登录成功";
    }

    public String getUsername(){
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if(!authentication.isAuthenticated()){
            return null;
        }
        Object principal = authentication.getPrincipal();
        String username = null;
        if(principal instanceof UserDetails){
            username = ((UserDetails)principal).getUsername();
        }else {
            username = principal.toString();
        }
        return username;
    }
    
    @GetMapping(value = "/r/r1")
    public String r1(){
        String username = getUsername();
        return username + "访问资源1";
    }
    
    @GetMapping(value = "r1/r2")
    public String r2(){
        String username = getUsername();
        return username + "访问资源2";
    }
}
```

#### 会话控制

我们可以通过以下选项准确控制会话何时创建以及Spring Security如何与之交互：

![image-20200918201714093](images\image-20200918201714093.png)

通过以下配置方式对该选项进行配置：

```java
@Override
protected void configure(HttpSecurity http) throws Exception {

    http.sessionManagement().sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED);
}
```

   默认情况下，Spring Security会为每个登录成功的用户会新建一个Session，就是ifRequired 。
  若选用never，则指示Spring Security对登录成功的用户不创建Session了，但若你的应用程序在某地方新建了 session，那么Spring Security会用它的。

   若使用stateless，则说明Spring Security对登录成功的用户不会创建Session了，你的应用程序也不会允许新建 session。并且它会暗示不使用cookie，所以每个请求都需要重新进行身份验证。这种无状态架构适用于REST API 及其无状态认证机制。

#### 会话超时

可以再sevlet容器中设置Session的超时时间，如下设置Session有效期为3600s；
spring boot 配置文件：

```properties
server.servlet.session.timeout=3600s
```

session超时之后，可以通过Spring Security 设置跳转的路径。

```java
http.sessionManagement().invalidSessionUrl("/login‐view?error=INVALID_SESSION");
```

## 7、授权

  授权的方式包括 web授权和方法授权，web授权是通过 url拦截进行授权，方法授权是通过 方法拦截进行授权。他 们都会调用accessDecisionManager进行授权决策，若为web授权则拦截器为FilterSecurityInterceptor；若为方法授权则拦截器为MethodSecurityInterceptor。如果同时通过web授权和方法授权则先执行web授权，再执行方法授权，后决策通过，则允许访问资源，否则将禁止访问。

![image-20200918202350782](images\image-20200918202350782.png)

#### 数据库环境

在t_user数据库创建如下表：

角色表:

```sql
CREATE TABLE `t_role` (  
     `id` varchar(32) NOT NULL,   
     `role_name` varchar(255) DEFAULT NULL, 
     `description` varchar(255) DEFAULT NULL,  
     `create_time` datetime DEFAULT NULL,  
     `update_time` datetime DEFAULT NULL,    
     `status` char(1) NOT NULL,    PRIMARY KEY (`id`),    
     UNIQUE KEY `unique_role_name` (`role_name`)  ) ENGINE=InnoDB DEFAULT CHARSET=utf8 
 insert  into `t_role`(`id`,`role_name`,`description`,`create_time`,`update_time`,`status`) values  ('1','管理员',NULL,NULL,NULL,'');
```

用户角色关系表：

```sql
CREATE TABLE `t_user_role` (    
    `user_id` varchar(32) NOT NULL, 
    `role_id` varchar(32) NOT NULL,  
    `create_time` datetime DEFAULT NULL,  
    `creator` varchar(255) DEFAULT NULL,    PRIMARY KEY (`user_id`,`role_id`)  ) ENGINE=InnoDB DEFAULT CHARSET=utf8 
 insert  into `t_user_role`(`user_id`,`role_id`,`create_time`,`creator`) values  ('1','1',NULL,NULL)
```

权限表：

```sql
CREATE TABLE `t_permission` (   
     `id` varchar(32) NOT NULL,  
     `code` varchar(32) NOT NULL COMMENT '权限标识符',   
     `description` varchar(64) DEFAULT NULL COMMENT '描述',   
     `url` varchar(128) DEFAULT NULL COMMENT '请求地址',
      PRIMARY KEY (`id`)  ) ENGINE=InnoDB DEFAULT CHARSET=utf8  
insert  into `t_permission`(`id`,`code`,`description`,`url`) values ('1','p1','测试资源 1','/r/r1'),('2','p3','测试资源2','/r/r2'); 
```

角色权限关系表:

```sql
CREATE TABLE `t_role_permission` (  
    `role_id` varchar(32) NOT NULL,   
    `permission_id` varchar(32) NOT NULL,    
    PRIMARY KEY (`role_id`,`permission_id`)  ) ENGINE=InnoDB DEFAULT CHARSET=utf8  
insert  into `t_role_permission`(`role_id`,`permission_id`) values ('1','1'),('1','2'); 
```

#### 修改UserDetailService

修改dao接口

```java
public List<String> findPermissionsByUserId(String userId){
    String sql = "SELECT * FROM t_permission WHERE id IN(\n" +
            "\n" +
            "SELECT permission_id FROM t_role_permission WHERE role_id IN(\n" +
            "  SELECT role_id FROM t_user_role WHERE user_id = ? \n" +
            ")\n" +
            ")\n";

    List<PermissionDto> list = jdbcTemplate.query(sql, new Object[]{userId}, new BeanPropertyRowMapper<>(PermissionDto.class));
    List<String> permissions = new ArrayList<>();
    list.forEach(c -> permissions.add(c.getCode()));
    return permissions;
}
```

#### web授权 

  在上面例子中我们完成了认证拦截，并对/r/**下的某些资源进行简单的授权保护，但是我们想进行灵活的授权控 制该怎么做呢？通过给 http.authorizeRequests() 添加多个子节点来定制需求到我们的URL，如下代码：

```java
http.csrf().disable()
        .authorizeRequests()//  http.authorizeRequests() 方法有多个子节点，每个macher按照他们的声明顺序执行。
        .antMatchers("/r/r1").hasAuthority("p2")// 指定"/r/r1"URL，拥有p1权限能够访问
        .antMatchers("/r/r2").hasAuthority("p2")// 指定"/r/r2"URL，拥有p2权限能够访问
        .antMatchers("/r/**").authenticated()//所有/r/**的请求必须认证通过
        .anyRequest().permitAll()//除了/r/**，其它的请求可以访问
```

规则的顺序是重要的,更具体的规则应该先写.现在以/ admin开始的所有内容都需要具有ADMIN角色的身份验证用 户,即使是/ admin / login路径(因为/ admin / login已经被/ admin / **规则匹配,因此第二个规则被忽略).

保护URL常用的方法有： 

authenticated() 保护URL，需要用户登录

 permitAll() 指定URL无需保护，一般应用与静态资源文件

 hasRole(String role) 限制单个角色访问，角色将被增加 “ROLE_” .所以”ADMIN” 将和 “ROLE_ADMIN”进行比较.

hasAuthority(String authority) 限制单个权限访问 

hasAnyRole(String… roles)允许多个角色访问. 

hasAnyAuthority(String… authorities) 允许多个权限访问

access(String attribute) 该方法使用 SpEL表达式, 所以可以创建复杂的限制. 

hasIpAddress(String ipaddressExpression) 限制IP地址或子网 

#### 方法授权 

我们可以在任何 @Configuration 实例上使用 @EnableGlobalMethodSecurity 注释来启用基于注解的安全性。 以下内容将启用Spring Security的 @Secured 注释。

```java
public interface BankService {
    @PreAuthorize("isAnonymous()")
    public UserDto redUser(Long id);

    @PreAuthorize("hasAuthority('p_transfer') and hasAuthority('p_read_account')")
    public UserDto post(Long id);
}
```

以上配置标明redUser方法可匿名访问，post方法需要同时拥有p_transfer和p_read_account 权限才能访问，底层使用WebExpressionVoter投票器，可从AﬃrmativeBased第23行代码跟踪。

# 四、分布式系统认证

## 1、什么是分布式系统

  随着软件环境和需求的变化 ，软件的架构由单体结构演变为分布式架构，具有分布式架构的系统叫分布式系统，分 布式系统的运行通常依赖网络，它将单体结构的系统分为若干服务，服务之间通过网络交互来完成用户的业务处 理，当前流行的微服务架构就是分布式系统架构，如下图

![image-20200918204037081](images\image-20200918204037081.png)

分布式系统具体如下基本特点：
1、分布性：每个部分都可以独立部署，服务之间交互通过网络进行通信，比如：订单服务、商品服务。

2、伸缩性：每个部分都可以集群方式部署，并可针对部分结点进行硬件及软件扩容，具有一定的伸缩能力。

3、共享性：每个部分都可以作为共享资源对外提供服务，多个部分可能有操作共享资源的情况。

4、开放性：每个部分根据需求都可以对外发布共享资源的访问接口，并可允许第三方系统访问。 

## 2、分布式认证需求

分布式系统的每个服务都会有认证、授权的需求，如果每个服务都实现一套认证授权逻辑会非常冗余，考虑分布式 系统共享性的特点，需要由独立的认证服务处理系统认证授权的请求；考虑分布式系统开放性的特点，不仅对系统 内部服务提供认证，对第三方系统也要提供认证。分布式认证的需求总结如下：

#### 统一认证授权

提供独立的认证服务，统一处理认证授权。
无论是不同类型的用户，还是不同种类的客户端(web端，H5、APP)，均采用一致的认证、权限、会话机制，实现 统一认证授权。

要实现统一则认证方式必须可扩展，支持各种认证需求，比如：用户名密码认证、短信验证码、二维码、人脸识别 等认证方式，并可以非常灵活的切换。

## 3、分布式认证方案

#### 选项分析

##### 基于session的认证方式 

在分布式的环境下，基于session的认证会出现一个问题，每个应用服务都需要在session中存储用户身份信息，通 过负载均衡将本地的请求分配到另一个应用服务需要将session信息带过去，否则会重新认证。

![image-20200920101327531](images\image-20200920101327531.png)

这个时候，通常的做法有下面几种：
Session复制：多台应用服务器之间同步session，使session保持一致，对外透明。

Session黏贴：当用户访问集群中某台服务器后，强制指定后续所有请求均落到此机器上。

Session集中存储：将Session存入分布式缓存中，所有服务器应用实例统一从分布式缓存中存取Session。

总体来讲，基于session认证的认证方式，可以更好的在服务端对会话进行控制，且安全性较高。但是，session机 制方式基于cookie，在复杂多样的移动客户端上不能有效的使用，并且无法跨域，另外随着系统的扩展需提高 session的复制、黏贴及存储的容错性。

##### 基于token的认证方式

基于token的认证方式，服务端不用存储认证数据，易维护扩展性强， 客户端可以把token 存在任意地方，并且可 以实现web和app统一认证机制。其缺点也很明显，token由于自包含信息，因此一般数据量较大，而且每次请求 都需要传递，因此比较占带宽。另外，token的签名验签操作也会给cpu带来额外的处理负担。



![image-20200920101840767](images\image-20200920101840767.png)

#### 技术方案

根据 选型的分析，决定采用基于token的认证方式，它的优点是：

1、适合统一认证的机制，客户端、一方应用、三方应用都遵循一致的认证机制。

2、token认证方式对第三方应用接入更适合，因为它更开放，可使用当前有流行的开放协议Oauth2.0、JWT等。

3、一般情况服务端无需存储会话信息，减轻了服务端的压力。

分布式系统认证技术方案见下图：



![image-20200920101944282](images\image-20200920101944282.png)

流程描述：

（1）用户通过接入方（应用）登录，接入方采取OAuth2.0方式在统一认证服务(UAA)中认证。

（2）认证服务(UAA)调用验证该用户的身份是否合法，并获取用户权限信息。

（3）认证服务(UAA)获取接入方权限信息，并验证接入方是否合法。

（4）若登录用户以及接入方都合法，认证服务生成jwt令牌返回给接入方，其中jwt中包含了用户权限及接入方权 限。

（5）后续，接入方携带jwt令牌对API网关内的微服务资源进行访问。

（6）API网关对令牌解析、并验证接入方的权限是否能够访问本次请求的微服务。

（7）如果接入方的权限没问题，API网关将原请求header中附加解析后的明文Token，并将请求转发至微服务。

（8）微服务收到请求，明文token中包含登录用户的身份和权限信息。因此后续微服务自己可以干两件事：1，用 户授权拦截（看当前用户是否有权访问该资源）2，将用户信息存储进当前线程上下文（有利于后续业务逻辑随时 获取当前用户信息）

## 4、OAuth2.0

OAuth（开放授权）是一个开放标准，允许用户授权第三方应用访问他们存储在另外的服务提供者上的信息，而不 需要将用户名和密码提供给第三方应用或分享他们数据的所有内容。OAuth2.0是OAuth协议的延续版本，但不向 后兼容OAuth 1.0即完全废止了OAuth1.0。很多大公司如Google，Yahoo，Microsoft等都提供了OAUTH认证服 务，这些都足以说明OAUTH标准逐渐成为开放资源授权的标准。

Oauth协议目前发展到2.0版本，1.0版本过于复杂，2.0版本已得到广泛应用。
参考：https://baike.baidu.com/item/oAuth/7153134?fr=aladdin 

Oauth协议：https://tools.ietf.org/html/rfc6749



1、客户端请求第三方授权

用户进入登录页面，点击微信的图标以微信账号登录系统，用户是自己在微信里信息的资源拥有者。

![image-20200920102759341](images\image-20200920102759341.png)

点击“微信”出现一个二维码，此时用户扫描二维码

![image-20200920102824281](images\image-20200920102824281.png)

2、资源拥有者同意给客户端授权

资源拥有者扫描二维码表示资源拥有者同意给客户端授权，微信会对资源拥有者的身份进行验证， 验证通过后，微 信会询问用户是否给授权问自己的微信数据，用户点击“确认登录”表示同意授权，微信认证服务器会 颁发一个授权码

3、客户端获取到授权码，请求认证服务器申请令牌

此过程用户看不到，客户端应用程序请求认证服务器，请求携带授权码。

4、认证服务器向客户端响应令牌

微信认证服务器验证了客户端请求的授权码，如果合法则给客户端颁发令牌，令牌是客户端访问资源的通行证。
此交互过程用户看不到，当客户端拿到令牌后，用户看到已经登录成功。

5、客户端请求资源服务器的资源

客户端携带令牌访问资源服务器的资源。
网站携带令牌请求访问微信服务器获取用户的基本信息。

6、资源服务器返回受保护资源

资源服务器校验令牌的合法性，如果合法则向用户响应资源信息内容。



![image-20200920103426284](images\image-20200920103426284.png)

通过上边的例子我们大概了解了OAauth2.0的认证过程，下边我们看OAuth2.0认证流程：

![image-20200920103458660](images\image-20200920103458660.png)

1、客户端

本身不存储资源，需要通过资源拥有者的授权去请求资源服务器的资源，比如：Android客户端、Web客户端（浏 览器端）、微信客户端等。

2、资源拥有者

通常为用户，也可以是应用程序，即该资源的拥有者

3、授权服务器（也称认证服务器）

用于服务提供商对资源拥有的身份进行认证、对访问资源进行授权，认证成功后会给客户端发放令牌 （access_token），作为客户端访问资源服务器的凭据。本例为微信的认证服务器。 

4、资源服务器

存储资源的服务器，本例子为微信存储的用户信息。
现在还有一个问题，服务提供商能允许随便一个客户端就接入到它的授权服务器吗？答案是否定的，服务提供商会 给准入的接入方一个身份，用于接入时的凭据:
client_id：客户端标识 client_secret：客户端秘钥 因此，准确来说，授权服务器对两种OAuth2.0中的两个角色进行认证授权，分别是资源拥有者、客户端。 

# 五、 Spring Cloud Security OAuth2 

## 1、环境介绍

Spring-Security-OAuth2是对OAuth2的一种实现，并且跟我们之前学习的Spring Security相辅相成，与Spring Cloud体系的集成也非常便利，接下来，我们需要对它进行学习，终使用它来实现我们设计的分布式认证授权解 决方案。

OAuth2.0的服务提供方涵盖两个服务，即授权服务 (Authorization Server，也叫认证服务) 和资源服务 (Resource Server)，使用 Spring Security OAuth2 的时候你可以选择把它们在同一个应用程序中实现，也可以选择建立使用 同一个授权服务的多个资源服务。

授权服务 (Authorization Server）应包含对接入端以及登入用户的合法性进行验证并颁发token等功能，对令牌 的请求端点由 Spring MVC 控制器进行实现，下面是配置一个认证服务必须要实现的endpoints：

​	AuthorizationEndpoint 服务于认证请求。默认 URL： /oauth/authorize 。

​	TokenEndpoint 服务于访问令牌的请求。默认 URL： /oauth/token 。 

​	资源服务 (Resource Server)，应包含对资源的保护功能，对非法请求进行拦截，对请求中token进行解析鉴 权等，下面的过滤器用于实现 OAuth 2.0 资源服务： 

​	OAuth2AuthenticationProcessingFilter用来对请求给出的身份令牌解析鉴权

![image-20200920103953894](images\image-20200920103953894.png)

认证流程如下：
 1、客户端请求UAA授权服务进行认证。

 2、认证通过后由UAA颁发令牌。

 3、客户端携带令牌Token请求资源服务。

 4、资源服务校验令牌的合法性，合法即返回资源信息。

## 2、环境搭建

### 父工程

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.3.5.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.harry.security</groupId>
    <artifactId>demo</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>demo</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>1.8</java.version>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-starter</artifactId>
            </dependency>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>Greenwich.RELEASE</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>

            <dependency>
                <groupId>javax.servlet</groupId>
                <artifactId>javax.servlet-api</artifactId>
                <version>3.1.0</version>
                <scope>provided</scope>
            </dependency>

            <dependency>
                <groupId>javax.interceptor</groupId>
                <artifactId>javax.interceptor-api</artifactId>
                <version>1.2</version>
            </dependency>

            <dependency>
                <groupId>com.alibaba</groupId>
                <artifactId>fastjson</artifactId>
                <version>1.2.47</version>
            </dependency>

            <dependency>
                <groupId>org.projectlombok</groupId>
                <artifactId>lombok</artifactId>
                <version>1.18.0</version>
            </dependency>

            <dependency>
                <groupId>mysql</groupId>
                <artifactId>mysql-connector-java</artifactId>
                <version>5.1.47</version>
            </dependency>


            <dependency>
                <groupId>org.springframework.security</groupId>
                <artifactId>spring-security-jwt</artifactId>
                <version>1.0.10.RELEASE</version>
            </dependency>


            <dependency>
                <groupId>org.springframework.security.oauth.boot</groupId>
                <artifactId>spring-security-oauth2-autoconfigure</artifactId>
                <version>2.1.3.RELEASE</version>
            </dependency>


            <dependency>

                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-starter-test</artifactId>
                <scope>test</scope>
                <exclusions>
                    <exclusion>
                        <groupId>org.junit.vintage</groupId>
                        <artifactId>junit-vintage-engine</artifactId>
                    </exclusion>
                </exclusions>
            </dependency>
        </dependencies>
    </dependencyManagement>



    <build>
        <finalName>${project.name}</finalName>
        <resources>
            <resource>
                <directory>src/main/resources</directory>
                <filtering>true</filtering>
                <includes>
                    <include>**/*</include>
                </includes>
            </resource>
            <resource>
                <directory>src/main/java</directory>
                <includes>
                    <include>**/*.xml</include>
                </includes>
            </resource>
        </resources>
        <plugins>
            <!--<plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>-->

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <source>1.8</source>
                    <target>1.8</target>
                </configuration>
            </plugin>

            <plugin>
                <artifactId>maven-resources-plugin</artifactId>
                <configuration>
                    <encoding>utf-8</encoding>
                    <useDefaultDelimiters>true</useDefaultDelimiters>
                </configuration>
            </plugin>
        </plugins>
    </build>

</project>
```

### 创建UAA授权服务工程 

创建distributed-security-uaa作为授权服务工程，依赖如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <parent>
        <artifactId>distributed-security</artifactId>
        <groupId>com.harry.security</groupId>
        <version>1.0-SNAPSHOT</version>
    </parent>
    <modelVersion>4.0.0</modelVersion>

    <artifactId>distributed-security-uaa</artifactId>

    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-ribbon</artifactId>

        </dependency>

        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-openfeign</artifactId>

        </dependency>

        <dependency>
            <groupId>com.netflix.hystrix</groupId>
            <artifactId>hystrix-javanica</artifactId>

        </dependency>

        <dependency>
            <groupId>org.springframework.retry</groupId>
            <artifactId>spring-retry</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-freemarker</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.data</groupId>
            <artifactId>spring-data-commons</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-security</artifactId>

        </dependency>

        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-oauth2</artifactId>
        </dependency>

        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-jdbc</artifactId>
        </dependency>
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>fastjson</artifactId>
        </dependency>

        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
        </dependency>
    </dependencies>

</project>
```

启动类

```java
package com.harry.security.auth2.uaa;

import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.netflix.hystrix.EnableHystrix;
import org.springframework.cloud.openfeign.EnableFeignClients;

@SpringBootApplication
@EnableDiscoveryClient
@EnableHystrix
@EnableFeignClients(basePackages = {"com.harry.security.auth2.uaa"})
public class UaaServer {
}
```

在resources下创建application.properties

```properties
spring.application.name=uaa-service
server.port=53020
spring.main.allow-bean-definition-overriding = true

logging.level.root = debug
logging.level.org.springframework.web = info

spring.http.encoding.enabled = true
spring.http.encoding.charset = UTF-8
spring.http.encoding.force = true
server.tomcat.remote_ip_header = x-forwarded-for
server.tomcat.protocol_header = x-forwarded-proto
server.use-forward-headers = true
server.servlet.context-path = /uaa

spring.freemarker.enabled = true
spring.freemarker.suffix = .html
spring.freemarker.request-context-attribute = rc
spring.freemarker.content-type = text/html
spring.freemarker.charset = UTF-8
spring.mvc.throw-exception-if-no-handler-found = true
spring.resources.add-mappings = false

spring.datasource.url = jdbc:mysql://localhost:3306/user_db?useUnicode=true
spring.datasource.username = root
spring.datasource.password = mysql
spring.datasource.driver-class-name = com.mysql.jdbc.Driver

eureka.client.serviceUrl.defaultZone = http://localhost:53000/eureka/
eureka.instance.preferIpAddress = true
eureka.instance.instance-id = ${spring.application.name}:${spring.cloud.client.ip-address}:${spring.application.instance_id:${server.port}}
management.endpoints.web.exposure.include = refresh,health,info,env

feign.hystrix.enabled = true
feign.compression.request.enabled = true
feign.compression.request.mime-types[0] = text/xml
feign.compression.request.mime-types[1] = application/xml
feign.compression.request.mime-types[2] = application/json
feign.compression.request.min-request-size = 2048
feign.compression.response.enabled = true
```

### 创建Order资源服务工程 

本工程为Order订单服务工程，访问本工程的资源需要认证通过

创建Order工程

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <parent>
        <artifactId>distributed-security</artifactId>
        <groupId>com.harry.security</groupId>
        <version>1.0-SNAPSHOT</version>
    </parent>
    <modelVersion>4.0.0</modelVersion>

    <artifactId>distributed-security-order</artifactId>

    <dependencies>

        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-security</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-oauth2</artifactId>
        </dependency>
        <dependency>
            <groupId>javax.interceptor</groupId>
            <artifactId>javax.interceptor-api</artifactId>
        </dependency>

        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>fastjson</artifactId>
        </dependency>

        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
        </dependency>


    </dependencies>

</project>
```

启动类

```java
@SpringBootApplication
@EnableDiscoveryClient
@EnableHystrix
public class OrderServer {
    public static void main(String[] args) {
        SpringApplication.run(OrderServer.class, args);
    }
}
```

配置文件

```properties
spring.application.name=order-service
server.port=53021
spring.main.allow-bean-definition-overriding = true

logging.level.root = debug
logging.level.org.springframework.web = info
spring.http.encoding.enabled = true
spring.http.encoding.charset = UTF-8
spring.http.encoding.force = true
server.tomcat.remote_ip_header = x-forwarded-for
server.tomcat.protocol_header = x-forwarded-proto
server.use-forward-headers = true
server.servlet.context-path = /order


spring.freemarker.enabled = true
spring.freemarker.suffix = .html
spring.freemarker.request-context-attribute = rc
spring.freemarker.content-type = text/html
spring.freemarker.charset = UTF-8
spring.mvc.throw-exception-if-no-handler-found = true
spring.resources.add-mappings = false


eureka.client.serviceUrl.defaultZone = http://localhost:53000/eureka/
eureka.instance.preferIpAddress = true
eureka.instance.instance-id = ${spring.application.name}:${spring.cloud.client.ip-address}:${spring.application.instance_id:${server.port}}
management.endpoints.web.exposure.include = refresh,health,info,env

feign.hystrix.enabled = true
feign.compression.request.enabled = true
feign.compression.request.mime-types[0] = text/xml
feign.compression.request.mime-types[1] = application/xml
feign.compression.request.mime-types[2] = application/json
feign.compression.request.min-request-size = 2048
feign.compression.response.enabled = true
```

## 3、授权服务器配

###  EnableAuthorizationServer 

可以用 @EnableAuthorizationServer 注解并继承AuthorizationServerConﬁgurerAdapter来配置OAuth2.0 授权 服务器

```java
@Configuration
@EnableAuthorizationServer
public class AuthorizationServer extends AuthorizationServerConfigurerAdapter {
    
}
```

AuthorizationServerConﬁgurerAdapter要求配置以下几个类，这几个类是由Spring创建的独立的配置对象，它们 会被Spring传入AuthorizationServerConﬁgurer中进行配置。

```java
public class AuthorizationServerConfigurerAdapter implements AuthorizationServerConfigurer {
    public AuthorizationServerConfigurerAdapter() {
    }

    public void configure(AuthorizationServerSecurityConfigurer security) throws Exception {
    }

    public void configure(ClientDetailsServiceConfigurer clients) throws Exception {
    }

    public void configure(AuthorizationServerEndpointsConfigurer endpoints) throws Exception {
    }
}
```

ClientDetailsServiceConﬁgurer：用来配置客户端详情服务（ClientDetailsService），客户端详情信息在 这里进行初始化，你能够把客户端详情信息写死在这里或者是通过数据库来存储调取详情信息。 AuthorizationServerEndpointsConﬁgurer：用来配置令牌（token）的访问端点和令牌服务(token services)。 AuthorizationServerSecurityConﬁgurer：用来配置令牌端点的安全约束.

### 配置客户端详细信息 

ClientDetailsServiceConﬁgurer 能够使用内存或者JDBC来实现客户端详情服务（ClientDetailsService）， ClientDetailsService负责查找ClientDetails，而ClientDetails有几个重要的属性如下列表： 

​	clientId：（必须的）用来标识客户的Id。

​	 secret：（需要值得信任的客户端）客户端安全码，如果有的话。

​	scope：用来限制客户端的访问范围，如果为空（默认）的话，那么客户端拥有全部的访问范围。 		

​	authorizedGrantTypes：此客户端可以使用的授权类型，默认为空。

​	authorities：此客户端可以使用的权限（基于Spring Security authorities）。

客户端详情（Client Details）能够在应用程序运行的时候进行更新，可以通过访问底层的存储服务（例如将客户 端详情存储在一个关系数据库的表中，就可以使用 JdbcClientDetailsService）或者通过自己实现 ClientRegistrationService接口（同时你也可以实现 ClientDetailsService 接口）来进行管理。

我们暂时使用内存方式存储客户端详情信息，配置如下:

```java
@Configuration
@EnableAuthorizationServer
public class AuthorizationServer extends AuthorizationServerConfigurerAdapter {

    //客户端详情服务
    @Override
    public void configure(ClientDetailsServiceConfigurer clients)
            throws Exception {
//        clients.withClientDetails(clientDetailsService);
        clients.inMemory()// 使用in-memory存储
                .withClient("c1")// client_id
                .secret(new BCryptPasswordEncoder().encode("secret"))//客户端密钥
                .resourceIds("res1")//资源列表
                .authorizedGrantTypes("authorization_code", "password","client_credentials","implicit","refresh_token")// 该client允许的授权类型authorization_code,password,refresh_token,implicit,client_credentials
                .scopes("all")// 允许的授权范围
                .autoApprove(false)//false跳转到授权页面
                //加上验证回调地址
                .redirectUris("http://www.baidu.com");
    }

}
```

### 管理令牌

AuthorizationServerTokenServices 接口定义了一些操作使得你可以对令牌进行一些必要的管理，令牌可以被用来 加载身份信息，里面包含了这个令牌的相关权限。

自己可以创建 AuthorizationServerTokenServices 这个接口的实现，则需要继承 DefaultTokenServices 这个类， 里面包含了一些有用实现，你可以使用它来修改令牌的格式和令牌的存储。默认的，当它尝试创建一个令牌的时 候，是使用随机值来进行填充的，除了持久化令牌是委托一个 TokenStore 接口来实现以外，这个类几乎帮你做了 所有的事情。并且 TokenStore 这个接口有一个默认的实现，它就是 InMemoryTokenStore ，如其命名，所有的 令牌是被保存在了内存中。除了使用这个类以外，你还可以使用一些其他的预定义实现，下面有几个版本，它们都 实现了TokenStore接口：

- InMemoryTokenStore：这个版本的实现是被默认采用的，它可以完美的工作在单服务器上（即访问并发量 压力不大的情况下，并且它在失败的时候不会进行备份），大多数的项目都可以使用这个版本的实现来进行 尝试，你可以在开发的时候使用它来进行管理，因为不会被保存到磁盘中，所以更易于调试。 
- JdbcTokenStore：这是一个基于JDBC的实现版本，令牌会被保存进关系型数据库。使用这个版本的实现时， 你可以在不同的服务器之间共享令牌信息，使用这个版本的时候请注意把"spring-jdbc"这个依赖加入到你的 classpath当中。
- JwtTokenStore：这个版本的全称是 JSON Web Token（JWT），它可以把令牌相关的数据进行编码（因此对 于后端服务来说，它不需要进行存储，这将是一个重大优势），但是它有一个缺点，那就是撤销一个已经授 权令牌将会非常困难，所以它通常用来处理一个生命周期较短的令牌以及撤销刷新令牌（refresh_token）。 另外一个缺点就是这个令牌占用的空间会比较大，如果你加入了比较多用户凭证信息。JwtTokenStore 不会保存任何数据，但是它在转换令牌值以及授权信息方面与 DefaultTokenServices 所扮演的角色是一样的。

#### 1、定义TokenConﬁg 

在conﬁg包下定义TokenConﬁg，我们暂时先使用InMemoryTokenStore，生成一个普通的令牌。

```java
package com.harry.security.auth2.uaa.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.oauth2.provider.token.TokenStore;
import org.springframework.security.oauth2.provider.token.store.InMemoryTokenStore;

@Configuration
public class TokenConfig {
    @Bean
    public TokenStore tokenStore(){
        return new InMemoryTokenStore();
    }
}
```

#### 2、定义AuthorizationServerTokenServices 

在AuthorizationServer中定义AuthorizationServerTokenServices

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.oauth2.config.annotation.configurers.ClientDetailsServiceConfigurer;
import org.springframework.security.oauth2.config.annotation.web.configuration.AuthorizationServerConfigurerAdapter;
import org.springframework.security.oauth2.config.annotation.web.configuration.EnableAuthorizationServer;
import org.springframework.security.oauth2.provider.ClientDetailsService;
import org.springframework.security.oauth2.provider.token.AuthorizationServerTokenServices;
import org.springframework.security.oauth2.provider.token.DefaultTokenServices;
import org.springframework.security.oauth2.provider.token.TokenStore;

@Configuration
@EnableAuthorizationServer
public class AuthorizationServer extends AuthorizationServerConfigurerAdapter {

    @Autowired
    private TokenStore tokenStore;
    @Autowired
    private ClientDetailsService clientDetailsService;

    @Bean
    public AuthorizationServerTokenServices tokenService(){
        DefaultTokenServices service = new DefaultTokenServices();
        service.setClientDetailsService(clientDetailsService);
        service.setTokenStore(tokenStore);
        service.setSupportRefreshToken(true);
        service.setAccessTokenValiditySeconds(7200); // 令牌有限期2小时
        service.setRefreshTokenValiditySeconds(2529200); // 刷新令牌默认有效期3天
        return service;
    }
```

### 令牌访问端点配置 

AuthorizationServerEndpointsConﬁgurer 这个对象的实例可以完成令牌服务以及令牌endpoint配置

#### 配置授权类型（Grant Types）

AuthorizationServerEndpointsConﬁgurer 通过设定以下属性决定支持的授权类型（Grant Types）: 

- authenticationManager：认证管理器，当你选择了资源所有者密码（password）授权类型的时候，请设置 这个属性注入一个 AuthenticationManager 对象。
- userDetailsService：如果你设置了这个属性的话，那说明你有一个自己的 UserDetailsService 接口的实现， 或者你可以把这个东西设置到全局域上面去（例如 GlobalAuthenticationManagerConﬁgurer 这个配置对 象），当你设置了这个之后，那么 "refresh_token" 即刷新令牌授权类型模式的流程中就会包含一个检查，用 来确保这个账号是否仍然有效，假如说你禁用了这个账户的话。
- authorizationCodeServices：这个属性是用来设置授权码服务的（即 AuthorizationCodeServices 的实例对 象），主要用于 "authorization_code" 授权码类型模式。
- implicitGrantService：这个属性用于设置隐式授权模式，用来管理隐式授权模式的状态。 
- tokenGranter：当你设置了这个东西（即 TokenGranter 接口实现），那么授权将会交由你来完全掌控，并 且会忽略掉上面的这几个属性，这个属性一般是用作拓展用途的，即标准的四种授权模式已经满足不了你的 需求的时候，才会考虑使用这个

#### 配置授权端点的URL（Endpoint URLs）：

AuthorizationServerEndpointsConﬁgurer 这个配置对象有一个叫做 pathMapping() 的方法用来配置端点URL链 接，它有两个参数：

​	第一个参数：String 类型的，这个端点URL的默认链接。 

​	第二个参数：String 类型的，你要进行替代的URL链接

以上的参数都将以 "/" 字符为开始的字符串，框架的默认URL链接如下列表，可以作为这个 pathMapping() 方法的 第一个参数

- /oauth/authorize：授权端点。 

-  /oauth/token：令牌端点。 
- /oauth/conﬁrm_access：用户确认授权提交端点
-  /oauth/error：授权服务错误信息端点。
-  /oauth/check_token：用于资源服务访问的令牌解析端点。
-  /oauth/token_key：提供公有密匙的端点，如果你使用JWT令牌的话

需要注意的是授权端点这个URL应该被Spring Security保护起来只供授权用户访问.

在AuthorizationServer配置令牌访问端点

```java
@Autowired
private AuthorizationCodeServices authorizationCodeServices;

@Autowired
private AuthenticationManager authenticationManager;

@Override
public void configure(AuthorizationServerEndpointsConfigurer endpoints){
    endpoints.authenticationManager(authenticationManager)
            .authorizationCodeServices(authorizationCodeServices)
            .tokenServices(tokenService())
            .allowedTokenEndpointRequestMethods(HttpMethod.POST);
}

@Bean
public AuthorizationCodeServices getAuthorizationCodeServices(){
    //设置授权码模式的授权码如何存取，暂时采用内存方式
    return new InMemoryAuthorizationCodeServices();
}
```

### authenticationManager 无法注入解决办法

在使用 Spring Security 做权限管理的时候，不知道为什么突然无法注入 authenticationManager 了，而之前一个项目可以使用的，切换了不同版本的 Spring Security 未解，一直报错。 Consider defining a bean of type 'org.springframework.security.authentication.AuthenticationManager' in your configuration.  最终还是找到了解决方案。  解决方案 在WebSecurityConfigurerAdapter的实现类当中，重写authenticationManagerBean方法：

```java
@Bean(name = BeanIds.AUTHENTICATION_MANAGER)
@Override
public AuthenticationManager authenticationManagerBean() throws Exception {
    return super.authenticationManagerBean();
}
```

### 令牌端点的安全约束 

AuthorizationServerSecurityConﬁgurer：用来配置令牌端点(Token Endpoint)的安全约束，在 AuthorizationServer中配置如下.

```java
@Override
public void configure(AuthorizationServerSecurityConfigurer security){
    security
            .tokenKeyAccess("permitAll()")
            .checkTokenAccess("permitAll()")
            .allowFormAuthenticationForClients();
}
```

（1）tokenkey这个endpoint当使用JwtToken且使用非对称加密时，资源服务用于获取公钥而开放的，这里指这个 endpoint完全公开。

（2）checkToken这个endpoint完全公开 

（3） 允许表单认证 

### 授权服务配置总结

授权服务配置分成三大块，可以关联记忆。

 既然要完成认证，它首先得知道客户端信息从哪儿读取，因此要进行客户端详情配置。

 既然要颁发token，那必须得定义token的相关endpoint，以及token如何存取，以及客户端支持哪些类型的 token。

 既然暴露除了一些endpoint，那对这些endpoint可以定义一些安全上的约束等

## 4、 web安全配置 

将Spring-Boot工程中的WebSecurityConﬁg拷贝到UAA工程中

```java
package com.harry.security.auth2.uaa.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.access.AccessDecisionVoter;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCrypt;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

@Configuration
@EnableGlobalMethodSecurity(securedEnabled = true,prePostEnabled = true)
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    //安全拦截机制（最重要）
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.csrf().disable()
                .authorizeRequests()//  http.authorizeRequests() 方法有多个子节点，每个macher按照他们的声明顺序执行。
                .antMatchers("/r/r1").hasAuthority("p1")// 指定"/r/r1"URL，拥有p1权限能够访问
                .antMatchers("/r/r2").hasAuthority("p2")// 指定"/r/r2"URL，拥有p2权限能够访问
                .antMatchers("/r/**").authenticated()//所有/r/**的请求必须认证通过
                .antMatchers("/login*").permitAll()
                .anyRequest().permitAll()//除了/r/**，其它的请求可以访问
                .and()
                .formLogin();//允许表单登录

    }

}
```

## 5、授权码模式 

下图是授权码模式交互图

![image-20201108114349147](images\image-20201108114349147.png)

（1）资源拥有者打开客户端，客户端要求资源拥有者给予授权，它将浏览器被重定向到授权服务器，重定向时会 附加客户端的身份信息。如：

```
/uaa/oauth/authorize?client_id=c1&response_type=code&scope=all&redirect_uri=http://www.baidu.com 
```

参数列表如下:

-  client_id：客户端准入标识。
-  response_type：授权码模式固定为code。 
-  scope：客户端权限。
-  redirect_uri：跳转uri，当授权码申请成功后会跳转到此地址，并在后边带上code参数（授权码）。

（2）浏览器出现向授权服务器授权页面，之后将用户同意授权

（3）授权服务器将授权码（AuthorizationCode）转经浏览器发送给client(通过redirect_uri)。

（4）客户端拿着授权码向授权服务器索要访问access_token，请求如下：

```
/uaa/oauth/token? client_id=c1&client_secret=secret&grant_type=authorization_code&code=5PgfcD&redirect_uri=http://www.baidu.com  
```

参数列表如下

-  client_id：客户端准入标识。
-  client_secret：客户端秘钥。 
-   grant_type：授权类型，填写authorization_code，表示授权码模式
-   code：授权码，就是刚刚获取的授权码，注意：授权码只使用一次就无效了，需要重新申请。 
-   redirect_uri：申请授权码时的跳转url，一定和申请授权码时用的redirect_uri一致

（5）授权服务器返回令牌(access_token) 

这种模式是四种模式中安全的一种模式。一般用于client是Web服务器端应用或第三方的原生App调用资源服务 的时候。因为在这种模式中access_token不会经过浏览器或移动端的App，而是直接从服务端去交换，这样就大限度的减小了令牌泄漏的风险。

### 测试

浏览器访问认证页面：

```
http://localhost:53020/uaa/oauth/authorize? client_id=c1&response_type=code&scope=all&redirect_uri=http://www.baidu.com
```

如出现保存java.lang.NoSuchMethodError: javax.servlet.http.HttpServletRequest.getHttpServletMapping()Ljavax/servlet/http/HttpServletMapping;

SpringBoot2.x内置的tomcat9，tomcat9使用的是servletAPI v4

但是SpringBoot 2.x还包含着 servletAPI v3.1

解决方法：将tomcat版本改为8.5.37即可

父工程

```xml
<properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
    <java.version>1.8</java.version>
    <tomcat.version>8.5.37</tomcat.version>
</properties>
```

![image-20201108130408994](images\image-20201108130408994)

然后输入模拟的账号和密码点登陆之后进入授权页面：

![image-20201108130432145](images\image-20201108130432145.png)

 确认授权后，浏览器会重定向到指定路径（oauth_client_details表中的web_server_redirect_uri）并附加验证码? code=DB2mFj（每次不一样），后使用该验证码获取token。

url需要传递redirect_uri，另外AuthorizationServerConfigurerAdapter的配置需要一致

```
POST http://localhost:53020/uaa/oauth/token 
```

![image-20201108132528769](images\image-20201108132528769.png)

## 6、简化模式

![image-20201108132825366](images\image-20201108132825366.png)

（1）资源拥有者打开客户端，客户端要求资源拥有者给予授权，它将浏览器被重定向到授权服务器，重定向时会 附加客户端的身份信息。如：

```
/uaa/oauth/authorize?client_id=c1&response_type=token&scope=all&redirect_uri=http://www.baidu.com  
```

参数描述同授权码模式 ，注意response_type=token，说明是简化模式。 

（2）浏览器出现向授权服务器授权页面，之后将用户同意授权。

（3）授权服务器将授权码将令牌（access_token）以Hash的形式存放在重定向uri的fargment中发送给浏览 器。

注：fragment 主要是用来标识 URI 所标识资源里的某个资源，在 URI 的末尾通过 （#）作为 fragment 的开头， 其中 # 不属于 fragment 的值。如https://domain/index#L18这个 URI 中 L18 就是 fragment 的值。大家只需要 知道js通过响应浏览器地址栏变化的方式能获取到fragment 就行了。

## 7、密码模式

![image-20201108132942762](images\image-20201108132942762.png)

（1）资源拥有者将用户名、密码发送给客户端

（2）客户端拿着资源拥有者的用户名、密码向授权服务器请求令牌（access_token），请求如下：

```
/uaa/oauth/token? client_id=c1&client_secret=secret&grant_type=password&username=cs&password=123  
```

参数列表如下：

- client_id：客户端准入标识。
-  client_secret：客户端秘钥。
-  grant_type：授权类型，填写password表示密码模式 
- username：资源拥有者用户名。
-  password：资源拥有者密码。

## 8、资源服务测试

###  资源服务器配置

@EnableResourceServer 注解到一个 @Conﬁguration 配置类上，并且必须使用 ResourceServerConﬁgurer 这个 配置对象来进行配置（可以选择继承自 ResourceServerConﬁgurerAdapter 然后覆写其中的方法，参数就是这个 对象的实例），下面是一些可以配置的属性：

- ResourceServerSecurityConﬁgurer中主要包括：
- tokenServices：ResourceServerTokenServices 类的实例，用来实现令牌服务。
- tokenStore：TokenStore类的实例，指定令牌如何访问，与tokenServices配置可选
- resourceId：这个资源服务的ID，这个属性是可选的，但是推荐设置并在授权服务中进行验证。 
- 其他的拓展属性例如 tokenExtractor 令牌提取器用来提取请求中的令牌。

HttpSecurity配置这个与Spring Security类似：

- 请求匹配器，用来设置需要进行保护的资源路径，默认的情况下是保护资源服务的全部路径。
- 通过http.authorizeRequests()来设置受保护资源的访问规则 
- 其他的自定义权限保护规则通过 HttpSecurity 来进行配置。 

@EnableResourceServer 注解自动增加了一个类型为 OAuth2AuthenticationProcessingFilter 的过滤器链 

编写ResouceServerConﬁg

```java
@Configuration
@EnableResourceServer
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class ResouceServerConfig extends ResourceServerConfigurerAdapter {
    public static final String RESOURCE_ID = "res1";


    @Override
    public void configure(ResourceServerSecurityConfigurer resources) {
        resources.resourceId(RESOURCE_ID)//资源 id
                .tokenServices(tokenService())//验证令牌的服务
                .stateless(true);
    }

    @Override
    public void configure(HttpSecurity http) throws Exception {

        http
                .authorizeRequests()
                .antMatchers("/**").access("#oauth2.hasScope('ROLE_ADMIN')")
                .and().csrf().disable()
                .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS);
    }


    //资源服务令牌解析服务
   @Bean
    public ResourceServerTokenServices tokenService() {
        //使用远程服务请求授权服务器校验token,必须指定校验token 的url、client_id，client_secret
        RemoteTokenServices service=new RemoteTokenServices();
        service.setCheckTokenEndpointUrl("http://localhost:53020/uaa/oauth/check_token");
        service.setClientId("c1");
        service.setClientSecret("secret");
        return service;
    }
}
```

###  验证token 

ResourceServerTokenServices 是组成授权服务的另一半，如果你的授权服务和资源服务在同一个应用程序上的 话，你可以使用 DefaultTokenServices ，这样的话，你就不用考虑关于实现所有必要的接口的一致性问题。如果 你的资源服务器是分离开的，那么你就必须要确保能够有匹配授权服务提供的 ResourceServerTokenServices，它 知道如何对令牌进行解码。

令牌解析方法： 使用 DefaultTokenServices 在资源服务器本地配置令牌存储、解码、解析方式 使用 RemoteTokenServices 资源服务器通过 HTTP 请求来解码令牌，每次都请求授权服务器端点 /oauth/check_token 

使用授权服务的 /oauth/check_token 端点你需要在授权服务将这个端点暴露出去，以便资源服务可以进行访问， 这在咱们授权服务配置中已经提到了，下面是一个例子,在这个例子中，我们在授权服务中配置了 /oauth/check_token 和 /oauth/token_key 这两个端点：

```java
@Override
public void configure(AuthorizationServerSecurityConfigurer security){
    security
            .tokenKeyAccess("permitAll()")   // /oauth/token_key 安全配置
            .checkTokenAccess("primitAll()") // /oauth/check_token 安全配置
            .allowFormAuthenticationForClients();
}
```

在资源服务配置RemoteTokenServices ，在ResouceServerConﬁg中配置：

```java
 //资源服务令牌解析服务
@Bean
 public ResourceServerTokenServices tokenService() {
     //使用远程服务请求授权服务器校验token,必须指定校验token 的url、client_id，client_secret
     RemoteTokenServices service=new RemoteTokenServices();
     service.setCheckTokenEndpointUrl("http://localhost:53020/uaa/oauth/check_token");
     service.setClientId("c1");
     service.setClientSecret("secret");
     return service;
 }
 
     @Override
    public void configure(ResourceServerSecurityConfigurer resources) {
        resources.resourceId(RESOURCE_ID)//资源 id
                .tokenServices(tokenService())//验证令牌的服务
                .stateless(true);
    }

```

### 编写资源

在controller包下编写OrderController，此controller表示订单资源的访问类

```java
@RestController
public class OrderController {
    
    @GetMapping(value = "/r1")
    @PreAuthorize("hasAnyAuthority('p1')")
    public String r1(){
        return "访问资源1";
    }
}
```

###  添加安全访问控制 

```java
package com.harry.security.oauth2.order.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;

@Configuration
@EnableGlobalMethodSecurity(securedEnabled = true, prePostEnabled = true)
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception{
        http.csrf().disable()
                .authorizeRequests()
                .antMatchers("/r/**").authenticated() //所有/r/**的请求必须认证通过
                .anyRequest().permitAll(); // 除了/r/** 其他请求可以访问
    }
}
```

### 测试

申请令牌使用密码模式

![image-20201108135414104](images\image-20201108135414104.png)

```json
{
    "access_token": "04ce60e8-1099-4eeb-a7d4-3b29ef0b89d8",
    "token_type": "bearer",
    "refresh_token": "a41149e4-0606-4671-9197-4d6e82e5ca46",
    "expires_in": 5471,
    "scope": "all"
}
```

请求资源

按照oauth2.0协议要求，请求资源需要携带token，如下： 

token的参数名称为：Authorization，值为：Bearer token值

# 六、JWT令牌

## 1、JWT介绍 

通过上边的测试我们发现，当资源服务和授权服务不在一起时资源服务使用RemoteTokenServices 远程请求授权 服务验证token，如果访问量较大将会影响系统的性能 。

解决上边问题：

令牌采用JWT格式即可解决上边的问题，用户认证通过会得到一个JWT令牌，JWT令牌中已经包括了用户相关的信 息，客户端只需要携带JWT访问资源服务，资源服务根据事先约定的算法自行完成令牌校验，无需每次都请求认证 服务完成授权。

JSON Web Token（JWT）是一个开放的行业标准（RFC 7519），它定义了一种简介的、自包含的协议格式，用于 在通信双方传递json对象，传递的信息经过数字签名可以被验证和信任。JWT可以使用HMAC算法或使用RSA的公 钥/私钥对来签名，防止被篡改

JWT令牌的优点： 

1）jwt基于json，非常方便解析。

2）可以在令牌中自定义丰富的内容，易扩展。 

3）通过非对称加密算法及数字签名技术，JWT防止篡改，安全性高。

4）资源服务使用JWT可不依赖认证服务即可完成授权。

缺点：

１）JWT令牌较长，占存储空间比较大

## 2、JWT令牌结构

通过学习JWT令牌结构为自定义jwt令牌打好基础。 

JWT令牌由三部分组成，每部分中间使用点（.）分隔，比如：xxxxx.yyyyy.zzzzz 

### Header

头部包括令牌的类型（即JWT）及使用的哈希算法（如HMAC SHA256或RSA） 

一个例子如下： 

下边是Header部分的内容

```json
{  
   "alg": "HS256",  
   "typ": "JWT"
 }  
```

将上边的内容使用Base64Url编码，得到一个字符串就是JWT令牌的第一部分。

### Payload

第二部分是负载，内容也是一个json对象，它是存放有效信息的地方，它可以存放jwt提供的现成字段，比 如：iss（签发者）,exp（过期时间戳）, sub（面向的用户）等，也可自定义字段。 

此部分不建议存放敏感信息，因为此部分可以解码还原原始内容

后将第二部分负载使用Base64Url编码，得到一个字符串就是JWT令牌的第二部分。

一个例子

```json
{    
  "sub": "1234567890", 
  "name": "456",   
  "admin": true  
} 
```

### Signature

第三部分是签名，此部分用于防止jwt内容被篡改

这个部分使用base64url将前两部分进行编码，编码后使用点（.）连接组成字符串，后使用header中声明 签名算法进行签名。 

一个例子：

```java
HMACSHA256(   
	 base64UrlEncode(header) + "." +   
	 base64UrlEncode(payload),   
	 secret)  
```

 base64UrlEncode(header)：jwt令牌的第一部分。

 base64UrlEncode(payload)：jwt令牌的第二部分。
 secret：签名所使用的密钥。

## 3、配置JWT令牌服务 

在uaa中配置jwt令牌服务，即可实现生成jwt格式的令牌

### 1、TokenConﬁg

```java
@Configuration
public class TokenConfig {
    private   String SIGNING_KEY = "uaa123";

    @Bean
    public TokenStore tokenStore(){
       return new JwtTokenStore(accessTokenConverter());

    }

    @Bean
    public JwtAccessTokenConverter accessTokenConverter(){
        JwtAccessTokenConverter converter = new JwtAccessTokenConverter();
        converter.setSigningKey(SIGNING_KEY); //对称秘钥，资源服务器使用该秘钥来验证
        return converter;
    }
}
```

### 2、定义JWT令牌服务

```java
@Configuration
@EnableAuthorizationServer
public class AuthorizationServer extends AuthorizationServerConfigurerAdapter {
	@Autowired
    private JwtAccessTokenConverter accessTokenConverter;
    
    @Bean
    public AuthorizationServerTokenServices tokenService(){
        DefaultTokenServices service = new DefaultTokenServices();
        service.setClientDetailsService(clientDetailsService);
        service.setTokenStore(tokenStore);
        service.setSupportRefreshToken(true);
        //令牌增强
        TokenEnhancerChain tokenEnhancerChain = new TokenEnhancerChain();
        tokenEnhancerChain.setTokenEnhancers(Arrays.asList(accessTokenConverter));
        service.setTokenEnhancer(tokenEnhancerChain);
        service.setAccessTokenValiditySeconds(7200); // 令牌有限期2小时
        service.setRefreshTokenValiditySeconds(2529200); // 刷新令牌默认有效期3天
        return service;
    }
```

### 3、生成jwt令牌 

![image-20201108150014523](images\image-20201108150014523.png)

### 4、校验jwt令牌 

资源服务需要和授权服务拥有一致的签字、令牌服务等：

1、将授权服务中的TokenConﬁg类拷贝到资源 服务中 

2、屏蔽资源 服务原来的令牌服务类

```java
@Configuration
@EnableResourceServer
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class ResouceServerConfig extends ResourceServerConfigurerAdapter {
    public static final String RESOURCE_ID = "res1";
    
    @Autowired
    TokenStore tokenStore;

    @Override
    public void configure(ResourceServerSecurityConfigurer resources) {
        resources.resourceId(RESOURCE_ID)//资源 id
                .tokenServices(tokenStore)//验证令牌的服务
                .stateless(true);
    }

    @Override
    public void configure(HttpSecurity http) throws Exception {

        http
                .authorizeRequests()
                .antMatchers("/**").access("#oauth2.hasScope('all')")
                .and().csrf().disable()
                .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS);
    }


    //资源服务令牌解析服务
//   @Bean
//    public ResourceServerTokenServices tokenService() {
//        //使用远程服务请求授权服务器校验token,必须指定校验token 的url、client_id，client_secret
//        RemoteTokenServices service=new RemoteTokenServices();
//        service.setCheckTokenEndpointUrl("http://localhost:53020/uaa/oauth/check_token");
//        service.setClientId("c1");
//        service.setClientSecret("secret");
//        return service;
//    }

}
```

### 5、测试

1）申请jwt令牌
2）使用令牌请求资源

![image-20201108150429613](images\image-20201108150429613.png)

小技巧：
令牌申请成功可以使用/uaa/oauth/check_token校验令牌的有效性，并查询令牌的内容，例子如下：

![image-20201108150508512](images\image-20201108150508512.png)

## 4、完善环境配置

截止目前客户端信息和授权码仍然存储在内存中，生产环境中通过会存储在数据库中，下边完善环境的配置： 

### 创建表

在user_db中创建如下表：

```sql
DROP TABLE
IF EXISTS `oauth_client_details`;
CREATE TABLE `oauth_client_details` (
	`client_id` VARCHAR (255) CHARACTER
	SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '客户端标识',
	resource_ids VARCHAR (255) CHARACTER
    SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '接入资源列表',
     client_secret VARCHAR (255) CHARACTER
    SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '客户端秘钥',
     scope VARCHAR (255) CHARACTER
    SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
     authorized_grant_types VARCHAR (255) CHARACTER
    SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
     web_server_redirect_uri VARCHAR (255) CHARACTER
    SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
     authorities VARCHAR (255) CHARACTER
    SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
     access_token_validity INT (11) NULL DEFAULT NULL,
     refresh_token_validity INT (11) NULL DEFAULT NULL,
     additional_information LONGTEXT CHARACTER
    SET utf8 COLLATE utf8_general_ci NULL,
    create_time TIMESTAMP (0) NOT NULL DEFAULT CURRENT_TIMESTAMP (0) ON UPDATE CURRENT_TIMESTAMP (0),
     archived TINYINT (4) NULL DEFAULT NULL,
     trusted TINYINT (4) NULL DEFAULT NULL,
     autoapprove VARCHAR (255) CHARACTER
    SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
     PRIMARY KEY (client_id) USING BTREE
) ENGINE = INNODB CHARACTER
```

```sql
INSERT INTO `oauth_client_details`
VALUES
	(
		'c1',
		'res1',
		'$2a$10$NlBC84MVb7F95EXYTXwLneXgCca6/GipyWR5NHm8K0203bSQMLpvm',
		'ROLE_ADMIN,ROLE_USER,ROLE_API',
		'client_credentials,password,authorization_code,implicit,refresh_token',
		'http://www.baidu.com',
		NULL,
		7200,
		259200,
		NULL,
		'2019-09-09 16:04:28',
		0,
		0,
		'false'
	);
```

```sql
INSERT INTO `oauth_client_details`
VALUES
	(
		'c2',
		'res2',
		'$2a$10$NlBC84MVb7F95EXYTXwLneXgCca6/GipyWR5NHm8K0203bSQMLpvm',
		'ROLE_API',
		'client_credentials,password,authorization_code,implicit,refresh_token',
		'http://www.baidu.com',
		NULL,
		31536000,
		2592000,
		NULL,
		'2019-09-09 21:48:51',
		0,
		0,
		'false'
	);
```

oauth_code表，Spring Security OAuth2使用，用来存储授权码：

```sql
DROP TABLE IF EXISTS oauth_code;
CREATE TABLE `oauth_code` (
 `create_time` TIMESTAMP (0) NOT NULL DEFAULT CURRENT_TIMESTAMP,
 `code` VARCHAR (255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
 `authentication` BLOB NULL,
 INDEX `code_index`(`code`) USING BTREE
) ENGINE = INNODB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact
```

