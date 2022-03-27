# 一 java基本面试题

## 自增运算

```java
package basic;

public class increment {
    /***
     * 总结， 1. 赋值=，最后计算
     *       2. =右边的从左到右加载值依次压入操作数栈
     *       3. 实际先算哪个看运算符优先级
     *       4. 自增自减操作都是直接修改变量的值，不经过操作数栈
     *       5. 最后赋值之前，临时结果也是存储再操作数栈中
     * @param args
     */
    public static void main(String[] args) {
        int i = 1;
        i = i++; // 先压栈 再++， 第一步先把i的值压入操作数栈，第二部i变量自增1，第三步把操作数栈中(栈中的值此时是1)的值赋值给i 最终i=1
        int j = i++; // 过程同上但是i自增之后赋值给了j 最终结果j=1 i=2(因为i自增了并且没有赋值所以是2)
        // 1. 先把i的值压入操作数栈(数栈i=2),
        // 2. i变量自增1，
        // 3. ++i把i的值压入操作数栈(数栈i=3),
        // 4.i++把i的值压入操作数栈(数栈i=3)
        // 5.i自增1
        // 6.把操作数栈中前两个弹出求乘积结果再压入栈
        // 7.把操作数栈中的值弹出求和再赋值给k
        int k = i + ++i * i++;
        System.out.println("i=" + i);
        System.out.println("j=" + j);
        System.out.println("k=" + k);
    }
}
```

## 单例模式

### 饿汉式

直接创建对象，不存在线程安全问题

​	直接实例化饿汉式（简洁直观）

​	枚举式(最简洁)

 	静态代码块饿汉式(适合复杂实例化)

```java
package basic;

/***
 * 饿汉式：直接创建实例对象，不管你是否需要这个对象
 *    (1) 构造器私有化
 *    (2) 自行创建，并且静态变量保存
 *    (3) 向外提供这个实例
 *    (4) 强调这是一个单例，我们可以用final修饰
 */
public class Singleton1 {
    public static final Singleton1 INSTANCE = new Singleton1();
    private Singleton1(){}

   privie static void main(String[] args) {
        System.out.println(INSTANCE);
    }
}

```

```JAVA

/***
 * 枚举类型，表示该类型的对象是有限的几个
 * 我们可以限定为一个，就成了单例
 */
public enum  Singleton2 {
    INSTANCE
}

```



```java

public class Singleton3 {
    public static Singleton3 instance;
    static {
        instance = new Singleton3();
    }
    private Singleton3(){}
}

```

### 懒汉式

延迟创建对象

​	线程不安全（适用于但线程）

​	线程安全(适用于多线程)

​	静态内部类形式(适用于多线程)

```java
/***
 * 懒汉式：
 *   延迟创建这个实例对象
 *      (1) 构造器私有化
 *      (2) 同一个静态变量保存这个唯一的实例
 *      (3) 提供一个静态方法获取这个实例对象
 */
public class Singleton4{
    private static Singleton4 instance;
    private Singleton4(){}
    public static Singleton4 getInstance(){
        if (instance == null){
            instance = new Singleton4();
        }
        return instance;
    }
}

```

```java
// double-check
public class Singleton5 {
    private static volatile Singleton5 instance;
    private Singleton5(){}
    public static Singleton5 getInstance(){
        if (instance == null){
            synchronized (Singleton5.class){
                if (instance == null){
                    instance = new Singleton5();
                }
            }
        }
        return instance;
    }
    
}

```

```java
/***
 * 在内部类被加载和初始化时才创建INSTANCE实例对象
 * 静态内部类不会自动随外部类的加载和初始化而初始化，它是要单独去加载和初始化的
 * 因为是在内部类加载和初始化创建的，因此线程是安全的
 */
public class Singleton6 {
    private Singleton6(){};
    private static class Inner{
        private static Singleton6 instance = new Singleton6();
    }
    public static Singleton6 getInstance(){
        return Inner.instance;
    }
}

```

## 类初始化过程

1 一个类要创建实例需要先加载并初始化该类

​	main方法所在的类需要先加载和初始化

2 一个子类要初始化需要先初始化父类

3 一个类初始化就是执行\<clinit>()方法

​	\<clinit>()方法由静态类变量显示赋值代码和静态代码块组成

实例初始化

 1. 实例初始化就是执行\<init>()方法

    \<init>()方法可能重载有多个，有几个构造器就有几个\<init>方法

```java
package basic;

public class Father {
    private int i = test();
    private static int j = method();
    static {
        System.out.println("(1)");
    }
    Father(){
        System.out.println("(2)");
    }
    {
        System.out.println("(3)");
    }
    public int test(){
        System.out.println("(4)");
        return 1;
    }
    public static int method(){
        System.out.println("(5)");
        return 1;
    }
}

class Son extends Father{
    private int i = test();
    private static int j = method();
    static {
        System.out.println("(6)");
    }
    Son(){
        System.out.println("(7)");
    }
    {
        System.out.println("(8)");
    }
    public int test(){
        System.out.println("(9)");
        return 1;
    }
    public static int method(){
        System.out.println("(10)");
        return 1;
    }
    public static void main(String[] args){
        Son s1 = new Son();
        System.out.println();
        Son s2 = new Son();
    }
}
```

## 方法的参数传递机制

形参是基本数据类型：传递数据值

引用数据类型：地址值

特殊类型：String 包装类等对象不可变性

![image-20220326201334669](\images\image-20220326201334669.png)

```java
package basic;

import java.util.Arrays;

public class Exam4 {
    public static void main(String[] args) {
        int i = 1;
        String str = "hello";
        Integer num = 200;
        int[] arr = {1,2,3,4,5};
        MyDate my = new MyDate();
        change(i,str,num,arr,my);
        System.out.println("i="  + i);
        System.out.println("str=" + str);
        System.out.println("num=" + num);
        System.out.println("arr=" + Arrays.toString(arr));
        System.out.println("my.a="+ my.a);
    }
    public static void change(int j, String s, Integer n, int[] a, MyDate m){
        j += 1;
        s += "world";
        n += 1;
        a[0] += 1;
        m.a += 1;
    }
}
class MyDate{
    int a = 10;
}

```



## 递归与迭代

```java
public class TestStep {
    public static void main(String[] args) {
        System.out.println(recursion(5));
        System.out.println(loop(40));
    }
    public static int recursion(int n){
        if (n <1){
            return -1;
        }
        if (n == 1 || n == 2){
            return n;
        }
        return recursion(n-2) + (n -1);
    }

    public static int loop(int n){
        if (n <1){
            return -1;
        }
        if (n == 1 || n == 2){
            return n;
        }
        int one = 2; // 初始化走到第二级台阶的走法
        int two = 1; // 初始化走到第一级台阶的走法
        int sum = 0;
        for (int i = 3; i <=n ; i++) {
            sum = one + two;
            two = one;
            one = sum;
        }
        return sum;
    }
}

```

