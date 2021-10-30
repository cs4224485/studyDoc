# 一 Serverlet3.0简介

现在咱们是来到了Spring注解驱动开发的最后一部分了，即与web相关的部分。在这一部分，我们将学会注解版的web开发，如果是以前的话，编写好web开发的三大组件（即Servlet、Filter以及Listener）之后，那么还得需要在web.xml配置文件中进行注册。不仅如此，包括Spring MVC的前端控制器（即DispatcherServlet）如果要使用，它也得在web.xml配置文件中进行注册，因为它依然是一个Servlet。


而在Servlet 3.0标准以后，它给我们提供了一些非常方便的方式，即使用注解，来完成这些组件的注册以及添加，它也会给我们提供了一些运行时的可插拔的插件功能。

Servlet 3.0标准是需要`Tomcat 7.0.x`及以上版本的服务器来支持的，而且Servlet 3.0是属于JSR 315系列中的规范。大家可以去jcp的官网，即https://www.jcp.org/en/home/index，亲自去搜索一下Servlet 3.0标准。

然后，在页面右上角的搜索框中输入`Servlet 3.0`进行搜索，搜索结果如下。

![image-20211025195336719](\images\image-20211025195336719.png)

只有`Tomcat 7.0.x`及以上版本的服务器才支持Servlet 3.0标准。所以，将来我们在运行项目的时候，一定要下载`Tomcat 7.0.x`及其以上版本的Tomcat服务器才行。

接下来，。首先，按照如下步骤来创建一个动态web工程

 pom.xml的内容如下：
    

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>serverlet3.0</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>war</packaging>
    <dependencies>

        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
            <version>4.0.0</version>
            <scope>provided</scope>
        </dependency>

        <dependency>
            <groupId>javax.servlet.jsp</groupId>
            <artifactId>jsp-api</artifactId>
            <version>2.2</version>
            <scope>provided</scope>
        </dependency>

    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.eclipse.jetty</groupId>
                <artifactId>jetty-maven-plugin</artifactId>
                <version>9.4.8.v20171121</version>
            </plugin>

            <plugin>
                <groupId>org.apache.tomcat.maven</groupId>
                <artifactId>tomcat7-maven-plugin</artifactId>
                <version>2.2</version>
            </plugin>

            <plugin>
                <artifactId>maven-war-plugin</artifactId>
                <version>3.0.0</version>
            </plugin>

        </plugins>
    </build>
</project>
```
然后，我们新建一个Servlet，例如HelloServlet，来处理以上get请求，即使用response来给我们浏览器写出一个字符串。

需求是这样的，我们希望发出一个get请求，然后给我们客户端响应一串字符串。这个需求说得应该是非常明朗了，为了解决这个需求，首先，我们在工程下创建一个首页，例如index.jsp，其内容如下。

```jsp
<%--
  Created by IntelliJ IDEA.
  User: harry.cai
  Date: 2021/10/25
  Time: 20:36
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Insert title here</title>
</head>
<body>
<a href="hello">hello</a>
</body>
</html>
```

如果是以前的话，那么我们需要将以上编写好的Servlet配置在web.xml文中，例如配置一下其拦截路径等等。而现在我们只需要使用一个简单的注解就行了，即@WebServlet。并且，我们还可以在该注解中配置要拦截哪些路径，例如@WebServlet("/hello")，这样就会拦截一个hello请求了。


```java
@WebServlet("/hello")
public class HelloServlet extends HttpServlet {

    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        // TODO Auto-generated method stub
        // super.doGet(req, resp);
        resp.getWriter().write("hello ...");
    }

}
```

![image-20211025204748050](\images\image-20211025204748050.png)

