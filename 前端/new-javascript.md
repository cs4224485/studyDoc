# 一  javaScript是什么

javaScript是一种web前端的描述语言，也是一种基于对象（object）和事件驱动（Event Driven）的、安全性好的脚本语言。

 

javaScript的特点：

- javaScript主要用来向html页面中添加交互行为
- javaScript是一种脚本语言，语法和c语言系列语言的语法类似，属弱语言类型。
- javaScript一般用来编写客户端脚本，如node.js例外。
- javaScript是一种解释型语言，边执行边解释无需另外编译。

# 二  js中的变量

变量的声明和定义

## 1 先声明后定义

```
var dog;
// alert(dog)   // undefined未定义
// 定义
 dog = '小黄'    
```

## 2 声明立即定义

```
var dog_2 = '小红';
console.log(dog_2);
```

变量命名规范：

- 严格区分大小写
- 命名时名称可以出现字母、数字、下划线、$ ,但是不能数字开头，也不能纯数字，不能包含关键字和保留字。关键字：var number等
- 推荐驼峰命名法：有多个有意义的单词组成名称的时候，第一个单词的首字母小写，其余的单词首字母写
- 匈牙利命名：就是根据数据类型单词的的首字符作为前缀

# 三  js中的数据类型

数据类型决定了一个数据的特征，比如：123和”123”，直观上看这两个 数据都是123，但实际上前者是一个数字，而后者是一个字符串。 

​	• 对于不同的数据类型我们在进行操作时会有很大的不同。

​	• JavaScript中一共有5种基本数据类型：

​		 – 字符串型（String） 

​		 – 数值型（Number）

​		 – 布尔型（Boolean） 

​		 – null型（Null） – undefined型（Undefined） 

   • 这5种之外的类型都称为Object，所以总的来看JavaScript中共有六种数据类型。

## typeof运算符

使用typeof操作符可以用来检查一个变量的数据类型。

 • 使用方式：typeof 数据，例如 typeof 123。

 • 返回结果：

​	 – typeof 数值 number

​     – typeof 字符串 string 

​	 – typeof 布尔型 boolean 

​     – typeof undefined undefined 

​     – typeof null object

## String

• String用于表示一个字符序列，即字符串。 

• 字符串需要使用 ’或“ 括起来。

 • 转义字符：

![image-20210828084303836](img\image-20210828084303836.png)

将其他数值转换为字符串有三种方式：toString()、String()、 拼串。

```javascript
字符串常用方法
    charAt()            返回指定索引的位置字符
    concat()            返回字符串值，表示两个或多个字符串的拼接
    mantch()            返回正则表达式模式对字符串进行匹配到的结果
    replace(a,b)        字符串b替换成了a
    search(stringObj)   返回的第一个匹配结果的索引值
    slice(start,end)    返回start到end-1之间的字符串，索引从0开始
    substr(start,end)   字符串截取，左闭右开
    toUpperCase()       将字符串转成大写
    toLowerCase()       将字符串转成小写
    indexOf()           查找字符的索引位置
    trim()              清楚字符串的前后空格
```

## Number

Number 类型用来表示整数和浮点数，最常用的功能就是用来 表示10进制的整数和浮点数。

 Number表示的数字大小是有限的，范围是： 

​		– ± 1.7976931348623157e+308 

​		– 如果超过了这个范围，则会返回± Infinity。

 NaN，即非数值（Not a Number）是一个特殊的数值，JS中 当对数值进行计算时没有结果返回，则返回NaN。

### 数值的转换

​	有三个函数可以把非数值转换为数值：Number()、parseInt() 和parseFloat()。

​		 • Number()可以用来转换任意类型的数据，而后两者只能用于 转换字符串。 

​		 • parseInt()只会将字符串转换为整数，而parseFloat()可以转换 为浮点数

## Boolean(布尔型)

布尔型也被称为逻辑值类型或者真假值类型。

 • 布尔型只能够取真（true）和假（false）两种数值。除此以外， 其他的值都不被支持。

 • 其他的数据类型也可以通过Boolean()函数转换为布尔类型。

![image-20210828084744139](img\image-20210828084744139.png)

## Undefine

Undefined 类型只有一个值，即特殊的 undefined 。

 • 在使用 var 声明变量但未对其加以初始化时，这个变量的值就 是 undefined。例如： – var message; – message 的值就是 undefined。

 • 需要注意的是typeof对没有初始化和没有声明的变量都会返回 undefined

## Null

Null 类型是第二个只有一个值的数据类型，这个特殊的值是 null 。

 • 从语义上看null表示的是一个空的对象。所以使用typeof检查 null会返回一个Object。

 • undefined值实际上是由null值衍生出来的，所以如果比较 undefined和null是否相等，会返回true；

## 运算符

JS中为我们定义了一套对数据进行运算的 运算符。 这其中包括：算数运算符、位运算符、关系运算符等

### 算数运算符

算数运算符顾名思义就是进行算数操作的运算符。

![image-20210828085028090](img\image-20210828085028090.png)

### 自增和自减

自增 ++ 自减 -- – 自增和自减分为前置运算和后置元素。

 – 所谓的前置元素就是将元素符放到变量的前边，而后置将元素符放到变 量的后边。

 – 例子： 

​	 • 前置自增：++a

​	 • 后置自减：a— 

 – 运算符在前置时，表达式值等于变量原值。

 – 运算符在后置是，表达式值等于变量变更以后的值。

### 逻辑操作符

 一般情况下使用逻辑运算符会返回一个布尔值。

​	 • 逻辑运算符主要有三个：非、与、或。

​	 • 在进行逻辑操作时如果操作数不是布尔类型则会将其转换 布尔类型在进行计算。

​	 • 非使用符号 ! 表示，与使用 && 表示，或使用 || 表示。

![image-20210828085238342](img\image-20210828085238342.png)

# 四 js对象

## Object对象

Object类型，我们也称为一个对象。是JavaScript中的引用数据类型。 

 	• 它是一种复合值，它将很多值聚合到一起，可以通过名字访问这些值。

​	 • 对象也可以看做是属性的无序集合，每个属性都是一个名/值对。

​	 • 对象除了可以创建自有属性，还可以通过从一个名为原型的对象那里 继承属性。 

​	• 除了字符串、数字、true、false、null和undefined之外，JS中的值 都是对象

### 创建对象

创建对象有两种方式： 

– 第一种 

```javascript
var person = new Object(); 
person.name = "孙悟空"; 
person.age = 18;
```

– 第二种

```javascript
var person = { name:"孙悟空", age:18 };
```

### 对象属性的访问

访问属性的两种方式： 

  	– .访问:对象.属性名

​	 – []访问:对象[‘属性名’]

### 引用数据类型

引用类型的值是保存在内存中的对象。

​	 • 当一个变量是一个对象时，实际上变量中保存的并不是 对象本身，而是对象的引用。

​	 • 当从一个变量向另一个变量复制引用类型的值时，会将 对象的引用复制到变量中，并不是创建一个新的对象。 

​	• 这时，两个变量指向的是同一个对象。因此，改变其中 一个变量会影响另一个

### 栈和堆

JavaScript在运行时数据是保存到栈内存和堆内存当中的。

​	• 简单来说栈内存用来保存变量和基本类型。堆内存用来保存对象。

​	• 我们在声明一个变量时实际上就是在栈内存中创建了一个空间 用来保存变量。 

​	• 如果是基本类型则在栈内存中直接保存， 

​	• 如果是引用类型则会在堆内存中保存，变量中保存的实际上对 象在堆内存中的地址。

```javascript
var a = 123;
var b = true;
var c = "hello"; 
var d = {name:'sunwukong',age:18};
```

![image-20210828090419868](img\image-20210828090419868.png)

## 数组

数组也是对象的一种。 

​	• 数组是一种用于表达有顺序关系的值的集 合的语言结构。 

​	• 创建数组：  var array = [1,44,33];

数组内的各个值被称作元素。每一个元素 都可以通过索引（下标）来快速读取。索引是从零开始的整数

```
(1)数组的创建方式
    var colors = ['red','green','yellow']
    使用构造函数创建数组
    var colors2 = new Array()
(2)数组的赋值
    var arr = [];
    arr[0] = 123;
    arr[1] = '哈哈’
(3) 数组的常用方法
    concat()             将几个数组合并为一个数组
    join()               返回字符串，其中包含了连接到一起数组中的所有元素，元素由指定分隔符分割开来
    pop()                移除数组的最后一个元素并返回该元素
    shift()              移除数组的一个元素
    unshift()            移除数组的开头添加一个元素，并返回新的长度
    splice(star,end)     删除元素，或者向数组添加新元素(插入，需添加第三个参赛为想要添加的内容)。
        names.splice(0, 2)             # 删除前两个元素
        names.splice(1,0, "harry")     # 插入新的元素
    slice()                 可从已有的数组中返回选定的元素。
    reverse()             对数组进行反转
    length                 获取数组长度
    toString()             将数组转为字符串
    sort()                 排序,升序或者降序，默认会按照ASSIC码排序
    indexOf()             查找数组元素位置
    lasetIndexOf()        查找数据元素位置从后往前查找
    filter()              过滤数组中某些元素
        var filterResult = numbers.filter(function(item, index, array){
            return item > 10
        })
    map()                 可以操作数组中的每一项元素
        var filterResult = numbers.filter(function(item, index, array){
            return item * 2
        })
```

## 函数

函数是由一连串的子程序（语句的集合）所组成的，可以 被外部程序调用。向函数传递参数之后，函数可以返回一 定的值。

通常情况下，JavaScript 代码是自上而下执行的，不过函 数体内部的代码则不是这样。如果只是对函数进行了声明， 其中的代码并不会执行。只有在调用函数时才会执行函数 体内部的代码。

 这里要注意的是JavaScript中的函数也是一个对象。

### 函数的声明

首先明确一点函数也是一个对象，所以函数也是在 堆内存中保存的。 

函数声明比较特殊，需要使用function关键字声明。 

上边的例子就是创建了一个函数对象，并将函数对 象赋值给了sum这个变量。其中()中的内容表示执 行函数时需要的参数，{}中的内容表示函数的主体。 var sum = function(a,b){return a+b};

可以通过函数声明语句来定义一个函数。函数声明语句以关键字 function 开始，其后跟有函数名、参数列表和函数体。其语法如下所 示：

​	function 函数名(参数,参数,参数...){ 函数体 }

### 函数内部属性

在函数内部，有两个特殊的对象：

​	– arguments 

​		• 该对象实际上是一个数组，用于保存函数的参数。

​	    • 同时该对象还有一个属性callee来表示当前函数。

  – this 

​	   • this 引用的是一个对象。对于最外层代码与函数内部的情况，其 引用目标是不同的。

​       • 此外，即使在函数内部，根据函数调用方式的不同，引用对象也 会有所不同。需要注意的是，this 引用会根据代码的上下文语境 自动改变其引用对象

this 引用的规则

​	 • 在最外层代码中，this 引用的是全局对象。

​	 • 在函数内，this 根据函数调用方式的不同 而有所不同：

![image-20210828091557263](img\image-20210828091557263.png)

### 构造函数

构造函数是用于生成对象的函数，像之前调用的Object()就是一个构 造函数。 

创建一个构造函数：function MyClass(x,y) { this.x = x; this.y = y; }

 调用构造函数： 

​	 – 构造函数本身和普通的函数声明形式相同。

​	 – 构造函数通过 new 关键字来调用，new 关键字会新创建一个对象并返回。

​     – 通过 new关键字调用的构造函数内的 this 引用引用了（被新生成的）对象。 

### new关键字

使用new关键字执行一个构造函数时： 

​	 – 首先，会先创建一个空的对象。

​	 – 然后，会执行相应的构造函数。构造函数中的this将会引用这个新对象。

​	 – 最后，将对象作为执行结果返回。

 构造函数总是由new关键字调用。 

 构造函数和普通函数的区别就在于调用方式的不同。

 任何函数都可以通过new来调用，所以函数都可以是构造函数。 

 在开发中，通常会区分用于执行的函数和构造函数。

 构造函数的首字母要大写

在对象中保存的数据或者说是变量，我们称为是一个对象的属性。

读取对象的属性有两种方式： 

​	– 对象.属性名 

​	– 对象['属性名'] 

 修改属性值也很简单： 

​	– 对象.属性名 = 属性值 

删除属性 

​	– delete 对象.属性名

 constructor

​	 – 每个对象中都有一个constructor属性，它引用了当前对象的构造函数

### 垃圾回收

 不再使用的对象的内存将会自动回收，这 种功能称作垃圾回收。

 所谓不再使用的对象，指的是没有被任何 一个属性（变量）引用的对象。

 垃圾回收的目的是，使开发者不必为对象 的生命周期管理花费太多精力。

### 原型继承

JS是一门面向对象的语言，而且它还是一个基于原型的面向对 象的语言。

所谓的原型实际上指的是，在构造函数中存在着一个名为原型 的(prototype)对象，这个对象中保存着一些属性，凡是通过该 构造函数创建的对象都可以访问存在于原型中的属性。

最典型的原型中的属性就是toString()函数，实际上我们的对象 中并没有定义这个函数，但是却可以调用，那是因为这个函数 存在于Object对应的原型中

### 设置原型

原型就是一个对象，和其他对象没有任何区别，可以通过构造 函数来获取原型对象。

​	 – 构造函数. prototype 

和其他对象一样我们可以添加修改删除原型中的属性，也可以 修改原型对象的引用。

需要注意的是prototype属性只存在于函数对象中，其他对象 是没有prototype属性的。

每一个对象都有原型，包括原型对象也有原型。特殊的是 Object的原型对象没有原型。

获取原型对象的方法

除了可以通过构造函数获取原型对象以外，还可以 通过具体的对象来获取原型对象。

​	 – Object.getPrototypeOf(对象) 

​	 – 对象.\__proto__ 

​	– 对象. constructor.prototype

需要注意的是，我们可以获取到Object的原型对象， 也可以对它的属性进行操作，但是我们不能修改 Object原型对象的引用

### 原型链

基于我们上边所说的，每个对象都有原型对象，原型对象也有原型对象。 

由此，我们的对象，和对象的原型，以及原型的原型，就构成了一个原型链。

比如这么一个对象： 

​	– var mc = new MyClass(123,456); 

​	– 这个对象本身，原型MyClass.proprototype原型对象的原型对象是Object，Object对象还有其原型。这组对象就构成了一个原型链。 

​	– 这个链的次序是：mc对象、mc对象原型、原型的原型（Object）、Object的原型

当从一个对象中获取属性时，会首先从当前对象中查找，如果没有则顺着向 上查找原型对象，直到找到Object对象的原型位置，找到则返回，找不到则 返回undefined

### instanceof

之前学习基本数据类型时我们学习了typeof用来检查一个变量 的类型。

但是typeof对于对象来说却不是那么好用，因为任何对象使用 typeof都会返回Object。而我们想要获取的是对象的具体类型。

这时就需要使用instanceof运算符了，它主要用来检查一个对 象的具体类型。

语法： var result = 变量 instanceof 类型

### 引用类型

上边我们说到JS中除了5种基本数据类型以外其余 的全都是对象，也就是引用数据类型。

但是虽然全都是对象，但是对象的种类却是非常繁 多的。比如我们说过的Array（数组），Function （函数）这些都是不同的类型对象。

实际上在JavaScript中还提供了多种不同类型的对象

## Object

目前为止，我们看到的最多的类型就是Object，它也是我们在JS中使用的最多的对象。 

虽然Object对象中并没有为我们提供太多的功能，但是我们会经常会用途来存储和传 输数据。

创建Object对象有两种方式： – var obj = new Object(); – var obj = {} 

上边的两种方式都可以返回一个Object对象。 

但是第一种我们使用了一个new关键字和一个Object()函数。 

这个函数就是专门用来创建一个Object对象并返回的，像这种函数我们称为构造函数

## Date

Date类型用来表示一个时间。 

Date采取的是时间戳的形式表示时间，所谓的时间戳指的是从 1970年1月1日0时0秒0分开始经过的毫秒数来计算时间。 

直接使用new Date()就可以创建一个Date对象。 

创造对象时不传参数默认创建当前时间。可以传递一个毫秒数 用来创建具体的时间。

也可以传递一个日期的字符串，来创建一个时间。 – 格式为：月份/日/年 时:分:秒    – 例如：06/13/2004 12:12:12

```javascript
创建方法
    var myDate = new Date();
常用方法
    getDate()                根据本地时间返回指定日期对象的月份中的几(1-31)
    Date()                   根据本地时间返回当天的日期和时间
    getMonth()               根据本地时间返回指定日期对象的月份(0-11)
    getFullYear()            根据本地时间返回指定日期对象年份(四位数年份返回四位数字)
    getDay()                 根据本地时间返回指定日期对象的星期中的第几天(0-6)\
    getHours()               根据本地时间返回指定日期对象的小时(0-23)
    getMinutes()             根据本地时间返回指定日期的对象分钟(0-59)
    getSeconds()             根据本地时间返回指定日期对象的秒数(0-59)
日期格式化
    toDateString()            星期 月 日 年
    toTimeString()            时 分 秒 时区
    toLoacleDateSting()
    toLocaleTimeString()
    toLocaleSting()

自定制返回数字时钟格式的时间
function nowNumberTime(){
    var now = new Date();
    var hour = now.getHours();
    var minute = now.getMinutes();
    var second = now.getSeconds();
   
    var temp = ""+(hour>12?hour - 12 : hour)
    if(hour === 0 ){
       temp = '12';
    }
    temp = temp + (minute <10 ? ':0': ":")+minute
    temp = temp + (second <10 ? ':0': ":")+second
    temp = temp + (hour>=12? ' P.M.':" A.M.");
    return temp;
}


```

## Function

Function类型代表一个函数，每一个函数都是一个Function类 型的对象。而且都与其他引用类型一样具有属性和方法。 

由于函数是对象，因此函数名实际上也是一个指向函数对象的 指针，不会与某个函数绑定。 

函数的声明有两种方式：    – function sum(){}            – var sum = function(){};

由于存在函数声明提升的过程，第一种方式在函数声明之前就 可以调用函数，而第二种不行

## 函数对象的方法

每个函数都有两个方法call()和apply()。 

call()和apply()都可以指定一个函数的运行 环境对象，换句话说就是设置函数执行时 的this值。

使用方式： – 函数对象.call(this对象,参数数组) 

​					– 函数对象.apply(this对象,参数1,参数2,参数N)

下面的例子使用 `apply` 与 `call`。通过这两个方法来将一个对象中 `this` 指代的目标进行改变。

```javascript
function Point(x, y) {
  this.x = x;
  this.y = y;
  this.move = function(x, y) {
    this.x += x;
    this.y += y;
  }
}

var point = new Point(0, 0);
point.move(1, 1);

var circle = {x: 0, y: 1, r: 1};

// 改变 point 中 move 方法 this 指代的对象至 circle
point.move.apply(circle, [1, 1]);
// 同样可以用类似的 call 方法，区别为参数需依次传入
point.move.call(circle, 1, 1);
```

## 闭包（closure）

闭包是JS一个非常重要的特性，这意味着 当前作用域总是能够访问外部作用域中的 变量。因为函数是JS中唯一拥有自身作用 域的结构，因此闭包的创建依赖于函数。 

也可以将闭包的特征理解为，其相关的局 部变量在函数调用结束之后将会继续存在。

闭包的应用

保存变量现场

```javascript
/ 错误方法
var addHandlers = function(nodes) {
  for (var i = 0, len = nodes.length; i < len; i++) {
    nodes[i].onclick = function(){
      alert(i);
    }
  }
}

// 正确方法
var addHandlers = function(nodes) {
  var helper = function(i) {
    return function() {
      alert(i);
    }
  }

  var (var i = 0, len = nodes.length; i < len; i++) {
    nodes[i].onclick = helper(i);
  }
}
```

## Math

Math.floor()                 向下取整，称为地板函数
Math.cel()                     向上取整
Math.max(a,b)            求a和b中的最大值
Math.min(a,b)             求a和b中的最小值
Manth.random()         随机数，默认0-1之间的随机数，公式min+Math.random()*(max-min),求min~max之间的数

```javascript
# 获取随机颜色 RGB(0-255, 0-255, 0-255);

function randomColor(){
    var r = random(0, 256),g = random(0, 256),b = random(0, 256);
    var result = 'rgb(${r}, ${g}, ${b})';
    return result;
}
document.body.style.backgroundColor = rc;
```

```javascript
# 随机验证码
function creatCode(){
    // 设置默认的空的字符串
    var code = '';
    // 设置长度
    var codeLength=4
    var rando = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];
    for(var i=0; i<codeLength; i++){
        // 设置随机范围 0~36
        var index = random(0, 36);
        code = randomCode[index]
    }
}
```