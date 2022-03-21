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



