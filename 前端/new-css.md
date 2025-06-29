# 一 CSS介绍

层叠样式表
实际上是一个多层的结构，通过CSS可以分别为网页的每一个层来设置样式
而最终我们能看到只是网页的最上边一层

总之一句话，CSS用来设置网页中元素的样式    

## 使用CSS来修改元素的样式

### 第一种方式(内联样式，行内样式)：

```html
<p style="background-color:red">hello world</p>
```

​	在标签内部通过style属性来设置元素的样式 使用内联样式，样式只能对一个标签生效，
​    如果希望影响到多个元素必须在每一个元素中都复制一遍并且当样式发生变化时，我们必须要一个一个的修改，非常的不方便

   注意：开发时绝对不要使用内联样

# 第二种方式（内部样式表）

```html
<head>
    <meta charset="utf-8">
    <title>title</title>
    <style>
        div{
            background-color:red;
        }
    </style>
</head>
```

将样式编写到head中的style标签里然后通过CSS的选择器来选中元素并为其设置各种样式可以同时为多个标签设置样式，并且修改时只需要修改一处即可全部应用

内部样式表更加方便对样式进行复用

问题：我们的内部样式表只能对一个网页起作用，它里边的样式不能跨页面进行复用

### 第三种方式 （外部样式表） 最佳实践

```html
<link href="mystyle.css" rel="stylesheet" type="text/css"/>
```

可以将CSS样式编写到一个外部的CSS文件中,然后通过link标签来引入外部的CSS文件

外部样式表需要通过link标签进行引入，意味着只要想使用这些样式的网页都可以对其进行引用使样式可以在不同页面之间进行复用

将样式编写到外部的CSS文件中，可以使用到浏览器的缓存机制，从而加快网页的加载速度，提高用户的体验。

# 二 CSS选择器

### 1 基本选择器

```
*:  通用元素选择器，匹配任何元素 * { margin 0; padding 0;}
E:  便签选择器，匹配所有使用E标签的元素 p{color：green；}
.info和E.info: class选择器，匹配所有class属性中包含info的元素
#info和E#info: id选择器， 匹配所有id属性等于info的元素
```

### 2 组合选择器

```
E,F     多元素选择器(群组选择器)，同时匹配所有E元素或F元素，E和F直接用逗号分隔          div,p { color:red; }
E F     后代元素选择器，匹配所有属于E元素后代的F元素，E和F之间用空格分隔                li a { font-weight:bodf; }
E > F   子元素选择器，匹配所有E元素的子元素F,与后代选择器的区别是不会选中孙子辈元素      div > p { color：green; }
E + F   毗邻选择器,匹配所有紧随E元素之后的同级元素F
```

### 3 属性选择器

```
E[att] 匹配所有具有att属性的E元素，不考虑他的值                           p[title]    { color:red; }
E[att=val] 匹配所有att属性等于"val"的E元素
E[att~=val] 匹配所有att属性具有多个空格分隔的值，其中一个值属于val的E元素    td[class~="name"]  {color:#f00;}
E[att^=val] 匹配属性值以指定开头的每个元素                               div[class^="test"] { background:red; }
E[att$=val] 匹配属性值以指定结尾的每个元素
E[att*=val] 匹配属性值中包含指定值的每个元素
p：before   在每个<p>元素的内容之前插入内容                              p:before{ content:"hello";color:red;}
p：after    在每个<p>元素的内容之后插入内容 
```

### 嵌套注意规则

- 1 块及元素可以包含内联元素或某些块级元素，但内联元素不能包含块级元素，它只能包含其他内联元素
- 2 块级元素不能放在p里面
- 3 有几个特殊的块级元素只能包含内联元素，不能包含块级元素。 如h1，h2,h3,h4,p,dt
- 4 li内可以包含div
- 5 块级元素与块级元素并列内联元素与内联元素并列

### CSS选择权重总结

先看有没有选中,如果选中了就数数(id,class,标签的数量)谁的权重大就显示谁的属性

- 内联选择器权重：1000
- ID选择器：100
- 类选择器：10
- 元素选择器权重：1
- 如果没有被选中，权重为0
- 如果属性都是被继承下来的权重都是0"就近原则":即谁描述的近就显示谁的属性
- 注意：继承来的属性的权重非常低W

比较优先级时，需要将所有的选择器的优先级进行相加计算，最后优先级越高，则越优先显示（分组选择器是单独计算的）,选择器的累加不会超过其最大的数量级，类选择器在高也不会超过id选择器如果优先级计算后相同，此时则优先使用靠下的样式

可以在某一个样式的后边添加 !important ，则此时该样式会获取到最高的优先级，甚至超过内联样式，
注意：在开发中这个玩意一定要慎用！

# 三 CSS伪类以及伪元素

```
a:link              未单击访问时的超链接样式
a:visited           单击访问后超链接样式
a:hover             鼠标悬浮其上的超链接样式
a:active            鼠标单机未释放的超链接样式
input：focus        当专注到输入框的样式
div ul li:first-child       选中li标签的第一个元素
div ul li：nth-child(3)     选中当前指定的元素 数值从1开始
div ul li：nth-child(n)     n表示选中索引从0开始 0的时候表示没有选中
div ul li：nth-child(2n)    所有偶数
div ul li：nth-child(2n-1)  所有基数      
```

### css伪元素选择器

```
 first-lette       用于为文本首字母设置特殊样式
 before            用于在元素内容前面插入新内容
 after             用于在元素内容后面插入新内容，在布局时可以用来清除浮动
```

# 四 CSS样式处理

### 1 字体样式

- font-family 设置字体类型
- font-size 设置字体大小
- font-style 设置字体风格
- font-weight 设置字体粗细
- font 在一个声明中设置所有字体属性

### 2 文本样式

- color 设置文本颜色
- text-align 设置元素水平对齐方式
- text-indent 设置首行文本的缩进
- line-height 设置文本的行高事项单行垂直居中
- text-decoration 设置文本的装饰
- letter-spacing 文字与文字之间的距离
- word-spacing 英文单词之间的距离
-  vertical-align 设置元素垂直对齐的方式

### 3 背景样式

- background-color  设置背景颜色
- background-image 设置背景图像路径
- backgroup-repeat  设置背景重复方式
- backgroup-position 设置背景定位

### 4 单位

- px：绝对单位。一旦设置了值，不够网页如何编号始终如一
- em：相对单位。 当前某块区域的字体大小，比如给P标签设置了字体大小20px, 那么1em=20px
- rem：相对单位。主要应用于移动端

### 5 图标字体

在网页中经常需要使用一些图标，可以通过图片来引入图标 但是图片大小本身比较大，并且非常的不灵活

所以在使用图标时，我们还可以将图标直接设置为字体，然后通过font-face的形式来对字体进行引入，这样我们就可以通过使用字体的形式来使用图标

​    fontawesome 使用步骤
​        1.下载 https://fontawesome.com/
​        2.解压
​        3.将css和webfonts移动到项目中
​        4.将all.css引入到网页中
​        5.使用图标字体

​	直接通过类名来使用图标字体
​	class="fas fa-bell"
​	class="fab fa-accessible-icon"

```html
<i class="fas fa-bell" style="font-size:80px; color:red;"></i>
<i class="fas fa-bell-slash"></i>
<i class="fab fa-accessible-icon"></i>
<i class="fas fa-otter" style="font-size: 160px; color:green;"></i>
```
### 6 行高

```html
<style>
div{
    font-size: 50px;

    /* 可以将行高设置为和高度一样的值，使单行文字在一个元素中垂直居中 */
    line-height: 200px;

    /*
    行高（line height）
  	  - 行高指的是文字占有的实际高度
   	  - 可以通过line-height来设置行高
   	    行高可以直接指定一个大小（px em）
        也可以直接为行高设置一个整数
        如果是一个整数的话，行高将会是字体的指定的倍数
    - 行高经常还用来设置文字的行间距
    行间距 = 行高 - 字体大小
    字体框
    - 字体框就是字体存在的格子，设置font-size实际上就是在设置字体框的高度
    行高会在字体框的上下平均分配
    */

    border: 1px red solid;

    /* line-height: 1.33; */
    /* line-height: 1; */
    /* line-height: 10 */
   }
</style>
```

# 五 CSS盒子模型

盒模型：在网页中基本都会显示一些方方正正的盒子，这种盒子被称为盒子模型。
重要属性：width height padding border margin
weight,height: 指的是内容宽高 而不是整个盒子真实的宽高
盒子模型的计算: 如果想保证盒子的真实宽度， 加width应该减少padding， 减width应该加padding

### 1 边框 boder

- border-top-style 上边框样式
- border-right-style 右边框样式
- border-bottom-style 下边框样式
- border-left-style 左边框样式
- border-style 设置四个边框样式

 border-width可以用来指定四个方向的边框的宽度
       值的情况
               四个值：上 右 下 左
                三个值：上 左右 下
                两个值：上下 左右
                一个值：上下左右

    边框（border），边框属于盒子边缘，边框里边属于盒子内部，出了边框都是盒子的外部
        边框的大小会影响到整个盒子的大小
    要设置边框，需要至少设置三个样式：
        边框的宽度 border-width
        边框的颜色 border-color
        边框的样式 border-style
### 2 内边距padding

padding控制的是盒子内容到盒子border之间的距离，设置了padding值是额外加载原来大小之上的width+padding，如果不想给不实现大小，那么就在width减去padding方向对应的值

 一个盒子的可见框的大小，由内容区内边距和边框共同决定，所以在计算盒子大小时，需要将这三个区域加到一起计算

### 3 外边距margin

外边距控制的是元素与元素之间的距离，margin也有四个方向，会改变实际大小背景色不会渲染到marigin区域，但是这个区域也属于盒子一部分

元素在页面中是按照自左向右的顺序排列的， 所以默认情况下如果我们设置的左和上外边距则会移动元素自身，而设置下和右外边距会移动其他元素

margin垂直方向上会出现外边距合并
使用margin: 0 auto 水平居中盒子。使用条件：

​	   1 必须有width,要明确width,文字水平居中使用text-align:center

​       2 只有标准流下的盒子才能使用margin:0 auto, 当一个盒子浮动了，固定定位或绝对定位了就无法使用margin: 0 auto

​      3 margin:0 auto居中盒子而不是居中文本

一个元素在其父元素中，水平布局必须要满足以下的等式：

margin-left+border-left+padding-left+width+padding-right+border-right+margin-right = 其父元素内容区的宽度 （必须满足）

以上等式必须满足，如果相加结果使等式不成立，则称为过度约束，则等式会自动调整

调整的情况：

​	如果这七个值中没有为 auto 的情况，则浏览器会自动调整margin-right值以使等式满足

​	这七个值中有三个值和设置为auto
​	width
​	margin-left
​	maring-right

如果某个值为auto，则会自动调整为auto的那个值以使等式成立

```
0 + 0 + 0 + auto + 0 + 0 + 0 = 800  auto = 800
0 + 0 + 0 + auto + 0 + 0 + 200 = 800  auto = 600
200 + 0 + 0 + auto + 0 + 0 + 200 = 800  auto = 400
auto + 0 + 0 + 200 + 0 + 0 + 200 = 800  auto = 400
auto + 0 + 0 + 200 + 0 + 0 + auto = 800  auto = 300
```

如果将一个宽度和一个外边距设置为auto，则宽度会调整到最大，设置为auto的外边距会自动为0，则外边距都是0，宽度最大

如果将两个外边距设置为auto，宽度固定值，则会将外边距设置为相同的值所以我们经常利用这个特点来使一个元素在其父元素中水平居中
示例：
    width:xxxpx;
    margin:0 auto;

### 4 垂直方向的布局

子元素是在父元素的内容区中排列的，如果子元素的大小超过了父元素，则子元素会从父元素中溢出，使用 overflow 属性来设置父元素如何处理溢出的子元素

可选值：

  	visible，默认值 子元素会从父元素中溢出，在父元素外部的位置显示
      hidden 溢出内容将会被裁剪不会显示
      scroll 生成两个滚动条，通过滚动条来查看完整的内容
      auto 根据需要生成滚动条

### 5 圆角

```
border-radius: 50% 圆形
```

### 6 阴影效果

```
box-shadow： 0 0 15px  // 阴影效果x y 阴影模糊程度 阴影颜色
第一个值 水平偏移量 设置阴影的水平位置 正值向右移动 负值向左移动
第二个值 垂直偏移量 设置阴影的水平位置 正值向下移动 负值向上移动
第三个值 阴影的模糊半径
第四个值 阴影的颜色
```

### 7 设置行内元素的水平垂直居中

```
display: table-cell;
vertical-align: middls;
```

### 8 块级元素水平居中

(1) 方式一

```css
.box{
    width:200px;
    height：200px;
    position:relative;
    background-color:red;
}
.child{
    width：100px;
    height：100px;
    background-color:green;
    position:absolute
    margin: auto;
    left:0;
    right:0;
    top:0;
    bottom:0;
}
```

(2) 方式二

```css
.box{
    width:200px;
    height：200px;
    background-color:red;
    display:table-cell;
    vertical-align: middle
    text-align:center
}

.child{
    width：100px;
    height：100px;
    background-color:green;
    display:inline-block;
    line-height:100px
}
```

(3) 方式三

```css
.box{
    width:200px;
    height：200px;
    background-color:red;
    position:relative;
}

.child{
    width：100px;
    height：100px;
    background-color:green;
    position:absolute;
    top:50%
    left:50%
    margin-left:-50px
    margin-top:-50px
}
```

### 9 行内元素的盒模型

行内元素的盒模型
       行内元素不支持设置宽度和高度
       行内元素可以设置padding，但是垂直方向padding不会影响页面的布局
       行内元素可以设置border，垂直方向的border不会影响页面的布局
       行内元素可以设置margin，垂直方向的margin不会影响布局

 display 用来设置元素显示的类型
     可选值：
                inline 将元素设置为行内元素
                block 将元素设置为块元素
                inline-block 将元素设置为行内块元素 行内块，既可以设置宽度和高度又不会独占一行
                table 将元素设置为一个表格
                none 元素不在页面中显示

 visibility 用来设置元素的显示状态
     可选值：
                visible 默认值，元素在页面中正常显示
                hidden 元素在页面中隐藏 不显示，但是依然占据页面的位置

### 10 盒子的尺寸

默认情况下，盒子可见框的大小由内容区、内边距和边框共同决定

box-sizing 用来设置盒子尺寸的计算方式（设置width和height的作用）

可选值:

​	content-box 默认值，宽度和高度用来设置内容区的大小

​    border-box 宽度和高度用来设置整个盒子可见框的大小

​               width 和 height 指的是内容区 和 内边距 和 边框的总大小

# 六 CSS页面浮动

文档流：可见元素在文档中显示位置

### 浮动产生的效果：

- 浮动可以使元素按指定位置排列，直到遇到父元素的边界或另一个元素的边界停止
- 如果父元素没有足够的空间那么第三个盒子紧贴着第二个盒子，第二个盒子紧贴第一个盒子， 第一个贴着边
- 如果没有足够的空间那么会靠着第一个盒子，如果没有足够的空间靠着第一个盒子，自己会往边贴

### 浮动效果

- 1 浮动可以使元素脱离文档流，不占位置
- 2 浮动会使元素提升层级
- 3 浮动可以使块元素在一行内排列 不设置宽高时可以使元素适应内容
- 4 浮动可以使行内元素支持宽高 所有便签一旦设置浮动都不区分行内和块状元素

### 浮动的特点

​     1、浮动元素会完全脱离文档流，不再占据文档流中的位置
​     2、设置浮动以后元素会向父元素的左侧或右侧移动，
​     3、浮动元素默认不会从父元素中移出
​     4、浮动元素向左或向右移动时，不会超过它前边的其他浮动元素
​     5、如果浮动元素的上边是一个没有浮动的块元素，则浮动元素无法上移
​     6、浮动元素不会超过它上边的浮动的兄弟元素，最多最多就是和它一样高

注意，元素设置浮动以后，水平布局的等式便不需要强制成立
       元素设置浮动以后，会完全从文档流中脱离，不再占用文档流的位置，
       所以元素下边的还在文档流中的元素会自动向上移动

### 浮动产生的问题

   父元素不设置高度，子元素设置浮动之后，不会撑开父元素的高度,那么此时父盒子没有高度了。如果在次父盒子下面还有一个标准流的盒子，那么就会影响页面的布局。
所以我们要解决浮动带来的页面布局错乱问题------清除浮动。

### 高度塌陷的问题

BFC(Block Formatting Context) 块级格式化环境
   - BFC是一个CSS中的一个隐含的属性，可以为一个元素开启BFC
        BFC该元素会变成一个独立的布局区域
   - 元素开启BFC后的特点：
        1.开启BFC的元素不会被浮动元素所覆盖
        2.开启BFC的元素子元素和父元素外边距不会重叠
        3.开启BFC的元素可以包含浮动的子元素

高度塌陷的问题：

​	 在浮动布局中，父元素的高度默认是被子元素撑开的，当子元素浮动后，其会完全脱离文档流，子元素从文档流中脱离 将会无法撑起父元素的高度，导致父元素的高度丢失 父元素高度丢失以后，其下的元素会自动上移，导致页面的布局混乱

### 清除浮动的方法

​	1 父元素设置高度是，子元素设置了浮动不会撑开父元素的高度，子元素不占位置

​	2 给浮动元素最后一个加一个空的块级元素，且改元素不浮动，设置clear:both

​	3 给最后一个盒子添加 visibility: hidden; clear:both; display: block; content:"" height:0; 官方推荐

​	4 给父元素添加overflow:hidden

### 浮动：float

```
left     元素向左浮动       /*左浮动 左侧为起始，从左往右依次排列*/
right    元素向右浮动       /*右浮动 右侧为起始，从左往右依次排列*/
```

### 高度塌陷的最终解决方案

```html
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <style>
        .box1{
        border: 10px red solid;

        /* overflow: hidden; */
        }

        .box2{
            width: 100px;
            height: 100px;
            background-color: #bfa;
            float: left;
        }

        .box3{
            clear: both;
        }

        .box1::after{
           content: '';
           display: block;
           clear: both;
        }

    </style>
</head>
<body>

    <div class="box1">
        <div class="box2"></div>
        <!-- <div class="box3"></div> -->
    </div>
</body>
</html>
```

# 七 CSS页面布局相关属性

### 1 Overflow属性

- visible 默认值，内容不会被修剪,会呈现在盒子之外
- hidden 内容会被修剪，并其余内容不可见
- scroll 内容会被修剪，但是浏览器会显示滚动条以便查看其余内容
- auto 如果内容被修剪，则浏览器会显示滚动以便查看其余内容

### 2 display属性

控制元素的显示和隐藏
块级元素与行内元素的转变

- none 设置元素不会被显示
- inline 元素会被显示为内联元素
- block 元素会被显示为块级元素
- inline-block 行内块元素
- visibility：hidden 隐藏标签但是仍然占用位置

### 3 position属性

static    默认值,没有定位

relative   相对定位

> 特点：1 不脱标准文档流 2 形影分离 3 老家流坑  4 相对定位会提升元素的层级 5 相对定位不会改变元素的性质块还是块，行内还是行内
>
> 用处：1微调页面信息 2 做绝对定位的参考位置
> 相对自身原来位置进行偏移，设置相对定位的盒子会相对它原来的位置，通过指定偏移到达新的位置
> 设置了相对定位的网页元素，无论是在标准流还是在浮动流中，都不会对它的父级元素和相邻元素有任何影响，它只只对自身原来的位置进行偏移

absolute   绝对定位 

> 1.开启绝对定位后，如果不设置偏移量元素的位置不会发生变化
> 2.开启绝对定位后，元素会从文档流中脱离
> 3.绝对定位会改变元素的性质，行内变成块，块的宽高被内容撑开
> 4.绝对定位会使元素提升一个层级
> 5.绝对定位元素是相对于其包含块进行定位的
>
> 在没有父级元素定位时，以浏览器的左上角为基准，有父级的情况下，父级设置相对定位，子级设置绝对定位，是以父盒子为基准进行定位
> 可以提升层级关系
> 脱离文档流

fixed 固定定位 

> 特性：1 脱离标准流 2 提升层级 3 固定不变 不会随着页面滚动而滚动
>
> 将元素的position属性设置为fixed则开启了元素的固定定位
>
> 固定定位也是一种绝对定位，所以固定定位的大部分特点都和绝对定位一样，唯一不同的是固定定位永远参照于浏览器的视口进行定位
> 固定定位的元素不会随网页的滚动条滚动
>
> *参考点： 设置固定定位用top描述，那么是以浏览器左上角为参考点， 如果用bottom描述那么是以浏览器的左下角为参考点
> 绝对定位居中的办法: 设置子元素的绝对定位,left：50%， margin-left等于元素宽度的一半实现绝对定位盒子居中*

### 4 绝对定位元素的布局

水平布局
left + margin-left + border-left + padding-left + width + padding-right + border-right + margin-right + right = 包含块的内容区的宽度

当我们开启了绝对定位后:水平方向的布局等式就需要添加left 和 right 两个值
此时规则和之前一样只是多添加了两个值：

 当发生过度约束：
                如果9个值中没有 auto 则自动调整right值以使等式满足
                如果有auto，则自动调整auto的值以使等式满足

可设置auto的值：margin width left right

    - 因为left 和 right的值默认是auto，所以如果不指定left和right
则等式不满足时，会自动调整这两个值

垂直方向布局的等式的也必须要满足：top + margin-top/bottom + padding-top/bottom + border-top/bottom + height = 包含块的高

### 5 z-index 

​	(1) z-index值表示谁压着谁，数值大的亚盖住数值小的，

​	(2) 只有定位了的元素才能有z-index， 也就是说不管相对定位，绝对定位，固定定位，都可以使用z-index，而浮动元素不能使用。

​	(3) z-index值没有单位就是一个正整数

​	(4) 如果大家都没有z-index值或者z-index值一样那么谁写在html的后面谁在上面压着谁，定位了的元素永远压住没有定位的元素

​	(5) 从父现象

