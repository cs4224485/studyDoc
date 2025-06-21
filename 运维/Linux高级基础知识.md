# 一、Vim的命令与使用

### 基本模式：

​                    编辑模式，命令模式

​                    输入模式

​                    末行模式

### 打开文件： vim [options] [file ..]

​                     +：直接打开文件最后一行

​                   +#：打开文件后，直接让光标处于第#行的行首

​                   +/PATTERN:打开文件后直接让光标定位于处于第一个被PATTERN匹配到的行行首

###  模式转换：

​         编辑模式-->输入模式“

​                                 i：insert 在光标所在位置输入

​                                a：append 在光标所在处后方输入

​                                o：在光标所在处下方新建一行

​                                 I：在光标所在行的行首插入

​                                A：在光标所在处的行尾插入

​                                O：在光标所在处的上方打开一个新行

​         输入模式 -->编辑模式

​                 ESC

​          编辑模式-->末行模式

​                    ：

​          末行模式-->编辑模式

​                ESC

关闭文件：

​         ZZ:保存并退出

​         ：q 退出

​         ：q！强制退出

​         ：x 保存并退出

光标跳转：

​       字符间跳转

​            h，向右

​             l，向左

​             j，向下

​             k，向上

   单词间调整

​           w：下一个单词的词首

​           b：当前或前一个单词的词首

​           e：当前或后一个单词的词尾

   行首行尾跳转：

​          ^:跳转至行首的第一个非空白字符

​         0：直接跳转到行首

​         $：跳转至行尾

  行间跳转：

​         \#G:跳转至#指定的行

​         1G:第一行

​          G:最后一行

翻屏：

​       ctrl+f：向文件尾部翻一屏

​       ctrl+b：向文件顶部翻一屏

​       ctrl+d：向文件尾部翻半屏

​       ctrl+u：向文件首部翻半屏

### VIM末行模式：

> （1）地址定界
>
> ​                .:当前行
>
> ​               $:最后一行
>
> ​              %:全文
>
> ​               \#：start_pos[,end_pos  #：特定的第#行，列入第5行
>
> ​             \#,#: 指定行范围，左侧起始行，右侧为结束行
>
> ​            \#,+#： 指定行范围，左侧为起始行绝对编号，右侧为相对左侧行号的偏移量； 例如：3+7
>
> ​            /pattern/：从光标所在处开始第一次被模式所匹配到的行
>
> ​     可用编辑命令一同使用，实现编辑操作：d y c
>
> ​            w /PATH/TO/SOMEFILE: 将范围内的文本保存至指定的文件中
>
> ​            r  /PATH/TO/SOMEFILE: 将指定的文件中的文本读取并插入至指定位置
>
>   （2）查找功能
>
> ​       /PATTERN: 从当前光标所在处向文件尾部查找能够被当前模式匹配到的所有字符串
>
> ​     ？PATTERN: 从当前光标所在处向文件首部查找能够被当前模式匹配到的所有字符串 
>
> ​                     n：下一个
>
> ​                    N：上一个                  
>
> （3）查找并替换
>
> ​           s：末行模式的命令
>
> ​               s/要查找的内容/替换为的内容/修饰符
>
> ​                        要查找的内容：可使用正则表达式
>
> ​                        替换的内容：不能使用正则表达式，但可以引用
>
> ​                             如果“要查找的内容”部分在模式只用分组符号：在“替换为的内容”中使用后向引用
>
> ​                             直接引用查找模式匹配到的全部文本；
>
> ​         修饰符：
>
> ​                 i：忽略大小写
>
> ​                g：全局替换，意味着一行只能怪匹配到多次，则均替换
>
> 示例: %s@\<s\([[:alpha:]]\)\+\>@S\1@g
>
> ​         %s@\<t[[:alpha:]]\+\>@&er@g

### VIM多文件功能

>  vim   FILE1 FILE2
>
> ​            大文件间切换
>
> ​                      ：next  下一个
>
> ​                      ：prev  上一个
>
> ​                      ：first   第一个
>
> ​                      ：last  最后一个
>
> ​            退出所有文件：wqall
>
> ​             多窗口：
>
> ​                 -o  水平窗口
>
> ​                 -O 垂直窗口
>
> ​              在窗口间切换：Ctrl+w， ARROW
>
> ​              单个文件也可以分割为多个窗口进行查看 
>
> ​                  ctrl+w,s:水平分割窗口
>
> ​                  ctrl+w,v:垂直分割窗口

### 定制vim的工作特性

> ​      永久生效：全局 /etc/vimrc   用户个人：~/.vimrc
>
> ​             1. 行号  ：set number | se nu  显示行号
>
> ​                             set nonumber | se nonu 取消显示
>
> ​             2. 括号匹配高亮显示
>
> ​                      匹配：set showmatch, set nonu
>
> ​                      取消：set nosm
>
> ​             3. 自动缩进功能
>
> ​                       启用：se ai 
>
> ​                       禁用：set noai
>
> ​            4. 高领搜索
>
> ​                      启用：set  hlsearch
>
> ​                      禁用：set  nohlserch
>
> ​            5. 语法高亮
>
> ​                      启用：syntax on
>
> ​                      禁用：syntax off
>
> ​           6. 忽略字符大小写
>
> ​                     启用：set ic
>
> ​                     禁用：set noic
>
> ​           获取帮助：
>
> ​                    ：help or ：help subject



# 二、Find命令的使用

find工作方式：实时查找工具，通过遍历指定起始路径下文件系统层级结构完成查找

find    find [OPTIONS] [查找起始路径] [查找条件] [处理动作]

​          查找起始路径：指定具体搜索目标起始路径；默认为当前目录

​          查找条件：指定的查找的标准，可根据文件名，大小 类型， 从属关系，权限等标准进行，默认找出指定目录的所有文件

​          处理动作：对符合条件查找的文件做出动作，如删除复制等操作。默认为显示

查找条件：选项和测试

### 根据文件名查找：

​										 -name PATTERN                    	 支持global通配符

​                                         -iname PATTERN 不区分大小    支持global通配符

​                                         -regex  PATTERN: 基于正则表达式，但匹配整个路径不是基于基名

### 根据文件从属关系查找：

​										-user USERNAME           查找属猪指定的用户所有文件

​                                        -group GROUPNAME      查找属组指定组的所有文件

​                                        -uid   UID         查找属主指定UID的所有文件      

​                                        -gid   GID         查找属组指定GID的所有文件             

​                                        -nouser  查找没有属主的文件

​                                        -nogroup 查找没有属组的文件



### 据文件的类型查找：

​		 -type  TYPE (b c d f s p l)

###  组合测试：

​            -a ：与逻辑，默认的组合逻辑为与 

​            -o ：或逻辑，

​          -not：非逻辑 

​		 ！A -a !B 交集 = !(A -o b)并集

  		! A -o  !B 并集= !(A -a B)j交集

### 根据文件大小查找：

​                 -size [+|-]#UNIT  常用单位：k,M,G           

​                               \#UNIT: 精品匹配                     

​                              -#UNIT: 小于  [0,至#-1]                       

​                             +#UNIT: 大于#

### 根据时间戳查找

​                以“天为单位：

​                        -atime [+|-]#

​                               \#:[#,#-1]

​                              -#: #天访问的区间[#，0]

​                             +#：#天之前访问的

​                        -mtime

​                        -ctime

​                以”分钟“单位：

​                         -amin

​                        -mmin

​                        -cmin

​               根据权限查找

​                   -prem [/] | - mode

​                   mode:精确权限匹配

​                  /mode:任何一类用户中的权限中的任何一位符合条件即满足。 9位权限之间存在“或”关系    

​                 -mode：每一类用户的权限中的每一位同时符合条件 9位权限之间存在“与”关系    

​             处理动作：

​                   -print： 输出至标准输出，默认的动作

​                   -ls：类似于对查找到的文件执行“ls -“ 命令

​                  -delete：删除查找到的文件

​                  -fls /PATH/TO/SOMEFILE:把查找到的所有文件的长格式信息保存至指定文件

​                  -ok COMMAND {} \; ：对查找到的每个文件执行由此处COMMAND表示的命令，需确认

​                  -exec  COMMAND {} \; :对查找到的每个文件执行由此处COMMAND表示的命令,不确认

 	注意：find传递查找到的文件路径至后面的命令时，是先查找出所有符合条件的文件路径，并一次性传递给后面的命令；但是有些命令不能接受过长的参数，此时执行会失败，另一种方式可规避问题：find | xargs

# 三、定时任务

Linux任务计划及周期性任务执行

未来的某时间执行一次

某任务：at，batch

周期性运行某任务：crontab

### 1、at命令

 at  [option].... TIME

​          TIME:

​             HH:MM[YYYY-MM-DD]

​             noon, midnight,teatime

​             tomorrow 

​             now+#  UNIT:minutes hours days OR weeks

​           at的作业有队列，用单个字母表示，默认都使用a队列

​           常用选项：

​                 -l：查看作业队列，相当于atq

​                 -f /PATH/FROM/SOMEFILE：从某一文件读取作业任务

​                 -d：删除指定的作业，相当atrm

​                 -c：查看指定作业的具体内容

​                 -q：指明队列

### 2、周期性任务计划

需要一个服务监控：cronle(centos7&6) 提供了crond守护进程及相关辅助工具

需确保crond守护进程（daemon）处于运行状态

​                  Centos7：systemctl status crond.service

​                  Ctentos6：service crond statu

向crond提交作业的方式不同于at，它需要使用专用的配置文件，此文件有固定格式，不建议使用文本编辑器；要使用crontab

 cron任务分为两类：

​             系统cron任务：主要用于实现系统自身的维护 手动编辑:/etc/corntab文件

​             用户cron任务：crontab 命令

cron命令的语法：

```bash
SHELL=/bin/bash

PATH=/sbin:/bin:/usr/sbin:/usr/bin

MAILTO=root

 .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name  command to be execute
```

### （1） 每一行定义一个周期性任务：

​			   \* * * * * ：定义周期性时间

​               user-name：运行任务的用户身份

​               commandi to be excuted：任务

### （2）此处的环境变量不同于用户登陆获得的环境，因此，建议使用绝对路径，或自定义PATH

### （3）执行结果发送给MAILTO指定的用户

用户cron的配置文件：/var/spool/corn/USERNAME; 与系统cron不同是无需定义user-name

### 3、时间表示法

   （1）特定值

​               给定时间点有效取值范围内的值（day of week和day of month一般不同时使用）

​     （2）*

​               给定时间点上有效取值范围内的所有值           

​      （3）离散取值 ，

​             在给定时间点上只用逗号分隔多个值

​                    \#，#，#，

​      （4）连续取值  -

​                   在时间上使用- 连接开头和结束

​      （5）在指定时间点上，定义步长：

​                   /#： #为步长

​                注意：

​                        1 制定的时间布恩那个被步长整除时，其意义将不不负存在

​                        2 最小时间为分钟,想完成秒级任务，需要在脚本中实现在每分钟内循环执行多次

​            示例：  3 * * * * ：每小时执行一次；每小时第三分钟执行

​                         3 4 * * * ：每周执行一次；每周 5的4点3分执行

​                         5  6 7 * * ： 每月执行一次；每月的7号的6点5分

​                         7 8 9 10 *：每年执行一次；每年的10月9号8点7分

​                         9 8 * * 3,7： 每周三和周日8点9分执行一次

​                         0 8,20 * * 3,7: 每周三和周日 8点和20点执行一次

​                         0  9-18 * * 1-5：工作时间每小时执行一次

​                         */5 * * * * ：每5分钟执行一次

### 4、crontab命令

crontab [-u user] [-l | -r | -e] [-i] [-s]

​             -e 编辑任务

​             -l  列出所有任务

​             -r  移除所有任务；即表示删除/var/spool/cron/USERNAME文件

​             -i  在使用-r选项移除任务时提示用户确认

​             -u  user：root 用户可为指定用户定义任务

如果期望某时间因故未能按时执行，下次开机后无论是否到了相应时间点都要执行一次，可使用anacron实现

# 四、用户和权限管理

用户类别：

​        管理

​        普通用户

​                系统用户

​                登录用户

  用户标识：UserID, UID

​          16bits二进制数：0-65535

​                管理员：0

​                普通用户：1-65535

​                系统用户：1-499（CentOS6） 1-999（CentOS7)

​                登录用户：500-60000 （CentOS6） 1000-60000 （CentOS7)

  组类别：

​          管理员组

​          普通用户组

​                 系统组

​                 登录组              

组类别2：

​      用户的基本组

​      用户的附加组

组类别3：

​      私有组：组名同用户名，且只包含一个用户

​      公共组：组内包含了多个用户

加密算法：

​       对称加密：加密解密使用同一个密码

​       非对称加密：加密和解密使用一对儿秘钥

单向加密：只能加密不能解密：提取数据特征码

​      定长输出

​      雪崩效应

​      常见算法;

​              md5: message digest  128bits

​              sha: secure hash algorithm  128bits



## 1、Linux用户和组管理命令

安全上下文：

​        进程以其发起者的身份用行

​                 进程对文件的访问权限，取决于发起此进程的用户的权

系统用户： 为了能够让后台进程或服务类进程以非管理员的身份运行，通常需要为此创建多个普通用户；这类用户从不登录系统

groupadd命令：  groupadd [options] group  创建一个组

​         -g GID:指定GID: 默认是上一个组的GID

​         -r  创建系统组：

groupmod命令： group - user group file

​         -g GID:指定GID

useradd命令：   useradd [options] LOGIN 创建一个用户

​         -u 指定UID

​         -g GROUP  指定基本组，此组需要事先存在

​         -G GROUP1[,GROUP2,...[,GROUPN]]]  指定附加组

​         -c 用户注释信息

​         -d 以指定的路径为用户的家目录：通过复制/etc/skel此目录并重新命名实现，指定的家目录路径如果事先存在，则不会为用户复制环境配置文件

​         -s 指定用户的默认shell，可用的所有shell列表为/etc/shells 文件、

​         -M 不为用户创建家目录

​         -D 显示创建用户的默认配置

创建用户时的诸多默认配置文件/etc/login.defs



usermod命令：修改用户属性  usermod [options] LOGIN

​          -u 修改用户UID 

​          -g GROUP  修改用户的基本组

​          -G 修改用户所属的附加组，原来的附加组会被覆盖

​          -a 于-G一同使用，为用户追加新的附加组

​          -c  修改注释信息

​          -d 修改用户的家目录 

​          -m 只能与-d选项一同使用将原来家目录的文件一同复制到新的家目录

​          -l   修改用户名

​          -s 修改用户的默认shell

​          -L 锁定用户密码

​          -U 解锁用户的密码

userdel命令：用户删除

​         -r 删除用户一并删除家目录

passwd命令： passwd [-k] [-l] [-u [-f]] [-d] [-e] [-n mindays] [-x maxdays]  [-S] [--stdin] [username]

​       （1） passwd：修改用户自己的密码

​       （2）passwd username： 修改指定用户密码

​            -l，-u：锁定和解锁用户

​                 -d ：删除一个用户的密码

​                 -e date：过期期限，日期

​                 -i  days：非活动期限

​                 -n DAYS:密码使用的最短使用期限

​                 -x DAYS:密码的最长使用期限

​                 -w DAYS:密码警告时间

gpasswd命令：给组定义密码，也能实现向组添加删除用户 

newgrp:登录到一个新组 

chage：修改密码过期信息

id命令：显示用户的真实和有效ID信息

​             -u：仅显示有效的UID

​             -g：仅显示用户的基本组ID

​             -G:  仅显示用户所属的所有组ID

​             -n：显示名字而非ID

su命令:切换用户

​       登录式切换：会通过重新读取用户的配置文件来重新初始化

​           su - USERNAME

​           su -l USERNAME

​      非登录式切换：不会读取目标用户的配置文件进行初始化

​          su  -c  ‘COMAND’:仅以指定用户的身份运行此处的命令



## 2、权限管理

 注意：仅管理员可修改文件的属主属组，用户仅能修改属主为自己的文件权限

​        进程安全上下文：

​               进程对文件的访问权限应用模型

​                      进程的属主与文件的属主是否相同； 如果相同，则应用属主权限

​                      否则，则坚持进程的属主是否与文件的属组；如果是，则应用属组权限

​                      否则，就只能用other权限

文件：

​     r:可获取文件的数据

​    w：可对文件进行编辑修改添加内容

​    x：可将此文件运行为进程

目录：

​    r：可使用ls命令获取其下的文件列表

   w：可修改此目录下的文件列表

   x：可cd至此目录，且可以使用ls -l 获取所有文件详细属性信息



权限管理命令：

​        chmod命令：  chmod [OPTION]... MODE[,MODE]... FILE...       

​                                chmod [OPTION]... OCTAL-MODE FILE...

​                                chmod [OPTION]... --reference=RFILE FILE..

MODE表示法：

​       赋权表示法     u= | g= | o= | a=

​       授权表示法     u+，u- | g+，g- | o+, o-

chmod --reference=/etc/fstab /var/tmp/harry.cai/test  根据其他文件的权限修改

选项:

​    -R 递归修改

​    

从属关系选项管理命令：

​       chown命令：     chown [OPTION]... [OWNER][:[GROUP]] FILE...

​                                 chown [OPTION]... --reference=RFILE FILE...



umask：文件权限反向掩码，遮罩码

​         文件：666 - umask 

​         目录：777 - umask

之所以文件用6666去减，表示文件默认不能拥有执行权限，如果减得的结果中有执行权限，则需要将其加1

install命令： 复制文件并设置属性

​                     install [OPTION]... [-T] SOURCE DEST            

​                     install [OPTION]... SOURCE... DIRECTORY

​                     install [OPTION]... -t DIRECTORY SOURCE...

​                     install [OPTION]... -d DIRECTORY...

  常用选项：

​          -m， 设定文件的权限，默认为755

​          -o，  设定目标文件属主

​          -g，  设定目标文件属组

mktemp命令：创建一个临时的文件或目录

​                       mktemp [OPTION]... [TEMPLATE]

​       -d  创建临时目录

​       -u  

注意：mktemp会将创建的临时文件名直接返回，因此可直接通过命令引用保存起来



## 3、sudo的使用 

su -与su 的区别

su -是su命令的一个参数表示切换用户的时候 更新用户的一些环境变量。

```bash
   ###不使用 su -
[root@oldboyedu-39-nb ~]# su oldboy
[oldboy@oldboyedu-39-nb root]$ pwd
/root
[oldboy@oldboyedu-39-nb root]$ env |grep -i root
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin
MAIL=/var/spool/mail/root
PWD=/root
[oldboy@oldboyedu-39-nb root]$ exit
   ###使用su -
[root@oldboyedu-39-nb ~]# su - oldboy
[oldboy@oldboyedu-39-nb ~]$ pwd
/home/oldboy
[oldboy@oldboyedu-39-nb ~]$ env |grep -i root
[oldboy@oldboyedu-39-nb ~]$ env |grep -i oldboy
HOSTNAME=oldboyedu-39-nb
USER=oldboy
MAIL=/var/spool/mail/oldboy
PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/home/oldboy/bin
PWD=/home/oldboy
HOME=/home/oldboy
LOGNAME=oldboy
```

sudo -l 查看当前用户可以使用的sudo命令

visudo 给用户授予尚方宝剑
	crontab -e (root) ==== vi /var/spool/cron/root
		语法检查
	visudo ==== vim /etc/sudoers

授权多个命令
	oldboy  ALL=(ALL)       /bin/ls, /bin/rm, /usr/sbin/useradd

​	oldboy  ALL=(ALL)       /bin/ls, /bin/touch

```bash
[oldboy@oldboyedu-39-nb ~]$ sudo -l
[sudo] password for oldboy:
Matching Defaults entries for oldboy on this host:
    !visiblepw, always_set_home, env_reset, env_keep="COLORS DISPLAY HOSTNAME HISTSIZE
    INPUTRC KDEDIR LS_COLORS", env_keep+="MAIL PS1 PS2 QTDIR USERNAME LANG LC_ADDRESS
    LC_CTYPE", env_keep+="LC_COLLATE LC_IDENTIFICATION LC_MEASUREMENT LC_MESSAGES",
    env_keep+="LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE", env_keep+="LC_TIME
    LC_ALL LANGUAGE LINGUAS _XKB_CHARSET XAUTHORITY",
    secure_path=/sbin\:/bin\:/usr/sbin\:/usr/bin

User oldboy may run the following commands on this host:
    (ALL) /bin/ls, (ALL) /bin/touch
[oldboy@oldboyedu-39-nb ~]$ ls -l /root/
ls: cannot open directory /root/: Permission denied
[oldboy@oldboyedu-39-nb ~]$ sudo ls -l /root/
total 7728
-rw-r--r--  1 root root       0 Aug  3 13:10 access-2017-05-20.log
-rw-r--r--  1 root root       0 Aug  3 13:10 access-2017-05-21.log
-rw-r--r--  1 root root       0 Aug  3 13:10 access-2017-05-22.log
-rw-r--r--  1 root root       0 Aug  3 13:12 access-2017-08-03.log
```

### sudo的使用过程

1.给某一个用户授予 sudo
  root用户下 使用
  visudo 命令
  crontab -e =====  vim /var/spool/cron/root
  visudo  ========  vim /etc/sudoers
  授予oldboy用户 可以以root的身份运行ls, touch mkdir
  oldboy ALL=(ALL)  /bin/ls, /bin/touch, /bin/mkdir
2.使用
sudo  ls /root

  授权所有命令
  oldboy  ALL=(ALL)       ALL

  授权所有命令并且不用密码
  	oldboy ALL=(ALL) NOPASSWD: ALL
  	###oldboy是运维人员的用户 就是你在使用
  	###自己用的时候 我不想输入密码（sudo)



# 五、磁盘管理和文件系统

Linux磁盘及文件系统管理

   I/O设备：Disks， Ethercard

   Disks接口类型：

​               IDE(ata）：并口， 133MB/s

​               SCSI: 并口 Ultrascsi320，320MB/s，UltraSCSI640，640MB/s

​               SATA：串口, 6Gbps/s  

​               SAS：串口 , 6Gbps/s  

​               USB:串口 3.1 480MB/s

 机械硬盘：

​      track：磁道

​     sector： 扇区  512bytes

​     cylinder：柱面

​           分区划分基于柱面

设备类型：

​       块：随机访问，数据交换单位是“块”

​     字符：线性访问，数据交换单位是”字符“

设备文件：

​        /dev

​           设置文件：关联至设备的驱动程序，用于识别设备访问入口

​           设备号：

​                major：主设备号，区别设备类型，用于标明设备所需的驱动程序

​                minor：次设备号，区分同种类型下的不同设备，是特定设备的访问入口

​           设备文件名:

​                   IDE：/dev/hd[a-z]

​           SCSI,SATA,USB,SAS: /dev/sa[a-z]

​           并口：同一线缆可以接多块设备

​                IDE:两个，主，从

​                SCIS:宽带 16-1  窄带：8-1

​            串口：同一线缆可以接一个设备      

磁盘分区：MBR, GPT

   MBR0 sector分为三部分：

​                       前446bytes：BootLoader程序，引导启启动操作系统的程序

​                       后64bytes：分区表，16bytes标识一个分区，一共只能有4个分区

​                      最后2bytes：MBR区域的有效性标识；55AA有效

## 1、创建分区

 fdisk /dev/sa#

​           -l    列出指定磁盘设备的分区情况

注意：已经分区并且已经挂载其中某个分区的设备上创建的新分区，内核可能在创建后无法直接识别

查看：cat /proc/partition

通知内核强制重读磁盘分区表：

​                 centos 5：partprobe [device]

​                 centos 6 7：partx  kpartx

​                          partx -a /dev/sda

创建文件系统：

​     格式化：低级格式化 （分区之前进行，划分磁道）。高级格式化（分区之后对分区进行，创建文件系统）                          

​          元数据区和数据区

​                 文件元数据区：大小，权限，属主属组，时间戳 ， 数据块指针 （index node）

​          链接文件：存储数据指针的空间当中存储的是真实文件的访问路径

​          设备文件：存储数据指针的空间当中存储的是设备号

 bitmap index：位图索引

删除文件：1 将删除文件指向的date block标记为未使用状态

​                  2 将此文件的inode标记为未使用

 复制文件：新建文件并将源文件的数据流导入至新建文件

 移动文件：如果在同一文件系统改变仅是其路径，在不同文件系统复制数据至目标，并删除原文件            

VFS:Virtual File System

​         Linux的文件系统：ext2  ext3  ext4 xfs  reiserfs   btrfs  ISO9660

​         网络文件系统：NFS CIFS

​         集群文件系统：gfs2 ocfs2

​         内核级分布文件系统：ceph

​        Windows文件系统：vfat  ntfs

​         伪文件系统：proc   sysfs  tmpfs  hugepagefs

​         unix的文件系统：UFS FFS JFS

​         交换分区文件系统：swap

​         用户空间的分布文件系统：mogilefs  moosefs  glusterfs

文件系统管理工具：

​         创建文件系统工具

​                   mkfs | mkfs.ext2   mkfs.ext3 .....

​         检测及修复文件系统的工具

​                    fsck: fsck.ext2     fsck.ext3   

​         查看其属性的工具

​                   dumpe2fs, tune2fs

​         调整文件系统特性：

​                    tune2fs

## 2、硬链接和软链接

链接文件：访问同一个文件的不同路径

​     硬链接：指向同一iNode的多个文件路径

​                特性：1目录不支持硬链接

​                           2硬链接不能跨越文件系统

​                           3创建硬链接会增加iNode引路计数

​                    创建：in     src     link_file

​     软链接：指向一个文件路径的另一个文件路径

​                特性：1 符号链接与元文件是两个各自独立的文件，各自有自己的inode

​                           2 支持目录创建符号链接，可以跨文件系统

​                           3 删除符号链接对源文件不影响，但删除原文件，符号指定的路径即不存在 

​                           4 符号链接文件的大小是其指定的文件的路径字符串的字节数

​                  创建：in -s  src  link_file

## 3、格式化文件系统

内核级文件系统的组成部分：

​             文件系统驱动：由内核提供

​             文件系统管理工具：由用户空间的应用程序提供

ext系列文件系统的管理工具：

​            mkfs.ext2  mkfs.ext3   mkfs.ext4

  ext系列文件系统专用管理工具   mke2fs

  ext系列文件系统专用管理工具   mke2fs

​                         mke2fs   [options]   device

​                              -t {ext2|ext3|ext4}:指明创建文件系统选项

​                              -b{1024|2048|4096}:指定文件系统的块大小

​                              -l LABEL:指明卷标 

​                              -j 创建有日志功能的文件系统ext3

​                              -i#: bytes-per-inode 指明inod与字节的比例：即多少字节创建一个inode

​                             -N#:直接指明要给此文件系统创建的inode的数量

​                             -O[^]FEATURE:以指定的特性创建文件系统； 

​                             -m#: 指定预留空间，百分比

​            查看修改和设定文件系统卷标：e2label

​                                    查看：e2label device

​                                    设定：e2label device LABEL

​            查看或修改ext系列文件系统的某些属： tune2fs

​                 tune2fs - adjust tunable filesystem parameters on ext2/ext3/ext4 filesystems

​                    tune2fs   [options]   device

​                              -l：查看超级快的内容 

​                              -j：将ext2升级至ext3

​                              -L LABEL:修改卷标

​                              -m#：调整预留空间百分比

​                            -O[^]FEATURE:调整或关闭某种特性

​                            -o[^]mount_options:开启或关闭某种默认挂载选项

   显示ext系列文件系统的属性信息：dumpe2fs

​                            dumpe2fs -h devic 只显示超级块信息

​           用于实现文件系统检测工具：e2fsck

​                 因进程意外终止或系统崩溃等原因导致写入操作非正常终止时，可能会造成文件损坏，此时应该检测并修复文件系统；建议离线进行（非挂载状态）

​                e2fsck:  ext系统专用修复工具 e2fsck - check a Linux ext2/ext3/ext4 file system

​                            -y：对所有问题自动回答为yes

​                             -f：即使文件系统处于clean状态，也要强制修复    

​                  fack：通用文件系统修复工具

​                             -t fstype：指明文件系统类型

​                             -a：无需交互自动修复所有错误

​                  bikid命令：

​                          blkid  device

​                          blkid    -L  LABEL:根据LABEL定位设备

​                          blkid    -U UUID：根据UUID定位设备

​             cetnos 6 安装xfs文件系统: yum -y intall xfsprogs

## 4、swap文件系统

 Linux上的交换分区必须使用独立的文件系统, 且文件系统system ID必须为82

  创建swap设备：mkswap 命令

​         mkswap [OPTIONS] device

​                 -L LABEL: 指明卷标

创建交换分区：

​       启用使用：swapon

​               swapon [option] [DEVICE]

​                     -a：定义在/etc/fstab文件中的所有swap设备

​       禁用：swapoff

​              swapoff [option] [DEVICE]

## 5、挂载文件系统

根文件系统除外的其他文件系统想要被访问，都必须通过关联至根系统上的某个目录来实现，此关联操作即为挂载，此目录即为挂载点：

挂载点 mount_point, 用于作为另一个文件系统入口

​	1 挂载点必须事先存在

​	2 挂载点应该使用未被或不会被其它进程使用到的目录

​	3 挂载点下原有的文件会被隐藏

mount 命令：

​         mount [-fnrsvw] [-t vfstype] [-o options] device dir

​              命令选项：

​                      -r ： readonly， 只读挂载

​                      -w： read and wirte 读写挂载

​                      -n： 默认情况下，设备挂载或卸载的操作会同步更新至/etc/mtab文件中，-n用于禁用

​                      -t vfstype：指明要挂载的设备上的文件系统的类型，多数情况下可省略，此时mount会通过blkid来判断要挂载的设备的文件系统类型 

​                      -L LABEL：挂载时以卷标方式指明设备

​                      -U UUID：挂载时以UUID方式指明设备

​                      -o options : 挂载选项

​                             sync/async：同步/异步操作

​                             atime/noatime：文件或目录被访问是否更新访问时间戳

​                           diratime/nodiratime：目录被访问是否更新访问时间戳

​                           remount：重新挂载

​                           acl：支持使用FACL功能

​                           ro : 只读

​                           rw：读写

​                           dev/nodev:此设备上是否允许创建设备文件

​                          exec/noexec：是否允许运行此设备上的程序文件

​                          auto/noauto ：是否支持自动挂载

​                          user/nouser ：是否允许普通用户挂载文件系统

​                          suid/nosuid   ：是否允许程序文件上的suid或sgid生效

​                          default：  Use default options: rw, suid, dev, exec, auto, nouser, and async.

可以实现将目录绑定至另一个目录上，作为其临时访问入口：mount  --bind SDIR DESDIR

​                         挂载光盘： mount  -r  /dev/cdrom  mount_point

​                         光盘设备文件：/dev/cdrom /dev/dvd

​              注意：正在被进程访问到的挂载点无法被卸载

​                         查看被哪个或哪些进程所占用

​                             lsot        MOUNT_POINT

​                             fuser  -v MOUNT_POINT

​                        终止所有正在访问某挂载点的进程：

​                          fuser  -km MOUNT_POIN

​                         挂载本地回环设备

​                         mount    -o  loop  /PATH/TO/SOME_LOOP_FILE  MOUNT_POINT

设定除根文件系统以为的其他文件系统能够开机时自动挂载需要修改：etc/fstab

​         每行定义一个要挂载的文件系统相关属性：

   要挂载的设备（设备文件,UUID,LABEL)   挂载点    文件系统类型    挂载选项   转储频率   自检次序

   查看文件系统以及文件大小命令：df   dumingl

​                 df命令：

​                         df [OPTION]... [FILE]...

​                            -I:仅显示本地文件的相关信息

​                            -h:human-reable

​                            -i:x显示inode的使用状态而非block

​                 du命令：

​                        du [OPTION]... [FILE]...

​                           -s： sumary

​                           -h：human-reable

## 6、RAID

RAID：Redunant Arrays of Inexpensive  Disk

​                                           Independent

​      提供IO能力，提高其耐用性

​      RAID级别：多块磁盘组织在一起的工作方式有所不同

​      RIAD实现方式：

​              外接磁盘阵列：通穿过扩展卡提供适配能力

​              外接式RAID：主板集成RAID控制器

​              Software RAID:

  级别：level

​       RAID-0: 0级别称之为条带卷，strip 提升了IO能力，没提供冗余能力，至少两块硬盘。可用空间：N*min

​       RAID-1: 1级别称之为镜像卷，mirror，读性能提升，写性能略有下降，有冗余能力. 可用空间：1*min

​       RAID-4: 4级别为校验码 

​       RAID-5：5级别相比4会轮流做校验盘。读写性能提升，可用空间：（N-1）*min，只能容错一块磁盘。至少三块磁盘

​      RAID-6：相比5，校验磁盘为两块 读写性能提升，可用空间：（N-2）*min       

​      RAID10: 读写性能提升，可用空间：N*min/2，有容错能力最多能同组能坏1块盘  

​      JBOD:将多块磁盘空间合并为一个大的连续空间

  

软RAID的实现： 结合内核中的md（multi devices）

​      mdadm：模式化的工具

​            命令格式：mdadm  [mode] <raiddevice> [options] <componet-devices>

​                支持RAID级别：JBOD,RAID0,RAID1，RAID4，RAID5，RAID6，RAID10 

​     device:/dev/md#

​     模式：

​        创建模式：-C

​             -n #：使用#个块设备来创建次RAID

​             -l  #：指明要创建的RAID的级别

​            -a {yes|no}：自动创建目标RAID设备的设备文件

​            -c CHUNK_SIZE: 指明块大小

​            -x  #： 指明空闲盘的个数

​        装配：-A

​        监控：-F

​        管理：-f  -r，-a

​           -D /dev/md#:查看raid信息

​           -f  /dev/md#  /dev/sda#:将一块盘模拟成坏盘

​           \- r /dev/md#  /dev/sa#:移除一块磁盘

​           -a /dev/md#  /dev/sda#： 装载一块盘

观察md同步：cat  /proc/mdstat



# 六、Linux三剑客

## 1、grep

grep作用：文本搜索工具，根据用户指定的“模式（过滤条件”对目标文本逐行进行匹配检查,打印匹配到的行

​         模式：由正则表达式的元字符及文本字符所编写出的过滤条件

grep  [option] PATTERN  FILE          

grep [OPTIONS] [-e PATTERN | -f FILE] [FILE...]

​          --colour=auto:对匹配到的文本着色

​          -i：ignorecase 忽略字符大小写

​          -o：仅显示匹配到的字符串本身

​          -v：反向显示

​          -E：支持扩展的正则表达式

​          -q：静默模式 不输出任何信息

​          -A#：after 后#行

​          -B#：before 前#行

​          -C#：context 前后#行

基本正则表达式的元字符：

​                字符匹配：

​                         . :任意单个字符

​                        []：匹配指定范围内的任意单个字符

​                        [^]：匹配指定范围外的任意单个字符

​                匹配次数：用在要指定其出现的次数的字符的后面，用于限制其前面字符出现的次数

​                        *：匹配其前面的字符任意此；0,1，多次

​                       .*：匹配任意长度的任意字符           

​                       \?: 匹配前面的字符0次或1次，即其前面的字符可有可无

​                       \+: 匹配前面的字符1次或多次，即前面的字符至少出现1次

​                      \{m\}:匹配前面的字符m次

​                      \{m,n\}匹配前面的字符至少m次，最多n次

​                            \{0,n}:最多n次

​                            \{m,\}:至少m次

​                位置锚定

​                        ^:行首锚定：用于模式的最左侧

​                       $：行尾锚定；用于模式最右侧

​                       ^PATTERN$:用于PATTERN来匹配整行

​                       ^$:空白行

​                       ^[[:space:]]*$:空白行货包含空白字符的行

​                      单词：非特殊字符组成的连续字符串都称为单词

​                       \< 或\b:词首锚定 用于单词模式的左侧 

​                       \>或\b:词尾锚定，用于单词模式的右侧

​                       \<PATTERN\>：匹配完整单词

​                分组及引用

​                       \(\):将一个或多个字符捆绑在一起，当作一个整体处理

​                                 例如：\(xy\)*ab

​              分组括号中的模式匹配到的内容会被正则表达式引擎自动记录于内部的变量中，这些变量为

​                   \1:模式从左侧起，第一个左括号以及与之匹配的右括号之前的模式所匹配到的字符

​                   \2:模式从左侧起，第二个左括号以及与之匹配的右括号之前的模式所匹配到的字符

​                   \3:

​           后项引用：应用前面的分组括号中的模式所匹配到的字符

扩展正则表达式

​            字符匹配

​                  .:匹配任意单个字符

​                  []:指定范围内的任意单个字符 

​               [^]：匹配指定范围外的任意单个字符

​            次数匹配

​                    *:任意次，0,1或多次

​                   ？：0次或1次，其前字符可有可无

​                    +：其前字符至少1次

​                  {m}：其前字符至少m次

​                  {m,n}:其前的字符m次

​            位置锚定

​                   ^:行首锚定

​                   $:词尾锚定

​                   \< 或\b:词首锚定 用于单词模式的左侧 

​                   \>或\b:词尾锚定，用于单词模式的右侧

​                   \<PATTERN\>：匹配完整单词  

​            分组及引用：

​                 ():分组，括号内的模式匹配到的字符会被记录于正则表达式引擎的内部变量中

​                  后向引用：\1, \2

​            或： a|b: a或者b

### 练习：

```bash
1 取出ifconfig命令中的ip地址
[root@Linuxprobe ~]# ifconfig | egrep  -o "([1-9]|[1-9][0-9]|1[0-9]{2}|2[0-9][0-4]|25[0-5])\.(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-9][0-5]|25[0-5])\.){2}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-9][0-5]|25[0-5])"
10.127.69.19
255.255.255.0
10.127.69.255
127.0.0.1
255.0.0.0
192.168.122.1
255.255.255.0
192.168.122.255
[root@Linuxprobe ~]# ifconfig | egrep -o "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" 稍微简洁写的写法
10.127.69.19
255.255.255.0
10.127.69.255
127.0.0.1
255.0.0.0
192.168.122.1
255.255.255.0
192.168.122.255
[root@Linuxprobe ~]# ifconfig | egrep -o "(([0-9]{1,3})\.){3}[0-9]{1,3}"再次进行精简
10.127.69.19
255.255.255.0
10.127.69.255
127.0.0.1
255.0.0.0
192.168.122.1
255.255.255.0
192.168.122.255

2 找出/etc/passwd中用户名与默认shell同名的的行  
 [root@Linuxprobe ~]# cat /etc/passwd | grep -E "^([[:alnum:]]+\>).*\1$"
 sync:x:5:0:sync:/sbin:/bin/sync
 shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
 halt:x:7:0:halt:/sbin:/sbin/halt
 bash:x:1002:1002::/home/bash:/bin/bash
 nologin:x:1003:1003::/home/nologin:/bin/nologin

3 取出一个文件的基名和路径名
[root@Linuxprobe ~]# echo /etc/sysconfig/network-scripts/ifcfg-ens33 | egrep -o "[^/]+$" 取一个文件的基本
ifcfg-ens33
[root@Linuxprobe ~]# echo /etc/sysconfig/network-scripts/ifcfg-ens33 | egrep  "^/.*/" -o 取出路径名
/etc/sysconfig/network-scripts/

4 取出/etc/rc.d/functions文件某个单词后面跟一个小括号的行
 [root@Linuxprobe ~]# egrep "[[:alnum:]]+\>\(\)+" /etc/rc.d/init.d/functions -o
checkpid()
checkpids()
kill()
.....

5 用两种方法显示/proc/meminfoz中大写或小写S开头的行
[root@Linuxprobe backups]# grep "^[sS].*" /proc/meminfo 
SwapCached:87404 kB
SwapTotal:   2097148 kB
SwapFree:1929492 kB
Shmem:  8332 kB
Slab: 189808 kB
SReclaimable: 118840 kB
SUnreclaim:70968 kB
[root@Linuxprobe backups]# grep -E "^(s|S).*" /proc/meminfo 
SwapCached:87400 kB
SwapTotal:   2097148 kB
SwapFree:1929496 kB
Shmem:  8336 kB
Slab: 189808 kB
SReclaimable: 118840 kB
SUnreclaim:70968 kB

6 取出/etc/paswwd文件中默认shell为非/sbin/nogloin
[root@Linuxprobe backups]# grep -v "nologin\>$" /etc/passwd
root:x:0:0:root:/root:/bin/bash
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
harrycai:x:1000:1000:harry.cai:/home/harrycai:/bin/bash
.............................................
7 取出/etc/paswwd文件中默认shell为/bin/bash的用户
[root@Linuxprobe backups]# grep  "bash\>$" /etc/passwd
root:x:0:0:root:/root:/bin/bash
harrycai:x:1000:1000:harry.cai:/home/harrycai:/bin/bash
student:x:1001:1001::/home/student:/bin/bash
bash:x:1002:1002::/home/bash:/bin/bash
user1:x:1004:1004::/home/user1:/bin/bash
.............................................

8 找出/etc/passwd 文件中的一位数或两位数
[root@Linuxprobe backups]# grep -E  "\<[0-9]{1,2}\>" /etc/passwd
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
.............................................

9 显示/boot/grub/grub.conf中至少一个空白字符开头的行
[root@Linuxprobe backups]# grep -E "^[[:space:]]+" /boot/grub2/grub.cfg 
10 显示/etc/rc.d/network文件中以#开头局，后面至少一个空白字符，而后又至少一个非空白字符行
[root@Linuxprobe backups]# grep -E "^#[[:space:]]+[^[:space:]]+" /etc/rc.d/init.d/network 
# network   Bring up/down networking
# chkconfig: 2345 10 90
# description: Activates/Deactivates all network interfaces configured to \
.......................

11 打出netstat -tan命令执行结果以“LISTEN”，后面跟空白字符的行
[root@Linuxprobe backups]# netstat -tan | grep -E "LISTEN\>[[:space:]]+"
tcp0  0 0.0.0.0:111 0.0.0.0:*   LISTEN 
tcp0  0 192.168.122.1:530.0.0.0:*   LISTEN   
............................................

12 匹配出所有的邮件地址
[root@Linuxprobe ~]# cat mailtest | grep -E "\<[[:alnum:]]*@[[:alnum:]]*[[:punct:]]*[[:alnum:]]*\.[a-z]+\>" 
noc@google.com
noc@telstra-pbs.cn
noc@pacnet.com.cn
414804000@qq.com
jzssysjzzyxgs@3158.com 
sales@wiremesh-machine.cn 
1305480186@qq.com 
.............
```

## 2、SED命令使用

字符流编辑器 Stream Editor 

​      sed [OPTION]... {script-only-if-no-other-script} [input-file]...

​       常用选项

​               -n：不输出模式空间中内容

​               -e script，--expression==script：多点编辑

​               -f /PATH/TO/SED_SCRIPT_FILE ：从文件总读取编辑命令脚本

​               -r：支持使用扩展正则表达式

​               -i：直接编辑源文件

​         地址定界：

​                （1）不给定地址，对全文进行处理

​                （2）单地址：

​                          \#：制定行

​                        /pattern/：被此模式所匹配到的每一行

​                （3）地址范围

​                         \#，#：#其实至#结束

​                         \#，+#：#向下#行

​                         \#，/pat1/：指定行到第一次模式匹配到的行

​                         /pat1/,/pat2/

​                  （4）步进：~

​                         1~2：所有基数行

​                          2~2：所有偶数行

​         script：地址定界编辑命令

​                     d: 删除

​                     p: 显示模式空间的内容

​                     a \text: 在行后面追加文本“text”，支持使用\n实现多行插入

​                     i \text：在行前面插入文本“text”，支持使用\n实现多行插入

​                    c \test：把匹配到的行替换为此处指定的文本“text”

​                    w /PATH/TO/SOMEFILE：保存模式空间匹配到的行至指定文件

​                    r  /PATH/TO/SOMEFILE：读取指定的文件的内容至当前文件被模式匹配到的行处

​                    =：为模式匹配到的行打印行号

​                    ！: 条件取反 地址定界!编辑命令

​                    s///：查找替换，其分隔符可自行指定，常用有s@@@，s###等

​                            g：全局提供

​                            w /PATH/TO/SOMEFILE：将替换成功的结果保存至指定文件

​                            p：显示替换成功的行

​       高级编辑命令:

​                  h: 把模式空间中的内容覆盖至保持空间中

​                  H: 把模式空间中的内容追加至保持空间中

​                  g:把保持空间中的内容覆盖至，模式空间中

​                 G:把保持空间中的内容追加至，模式空间中

​                  x:把模式空间内容与保持空间内容互换

​                  n:覆盖匹配到的行的下一行至模式空间

​                  N:追加匹配到的行的下一行至模式空间

​                  d:删除模式空间的行

​                 D:删除多行模式空间的所有行

​        示例： sed -n ‘n；p’ FILE:显示偶数行

​                   sed ‘1！G;h;$!d' FILE逆序显示文件内容

​                   sed ’$!N; $!D' FILE: 取出文件后两行

​                   sed ‘$!d' FILE :取出最后一行

​                   sed ’/^$/d;G' FILE:删除原有的空白行，而后为所有的非空白行后添加一个空白行

​                   sed ‘G’ FILE: 在原有的每行后方添加一个空白行

## 3、awk的使用

基本用法：gawk [option] 'program' FILE

​    program:PATTERN{ACTION STATEMENTS}

​                   语句之间用分号分割

   选项：

​        -F：指明输入时用到的字段分隔符

​        -v： var=value:自定义变量

1. print

​    print  item, item2....

​    要点：

​    （1）逗号分隔符

​    （2）输出的各item可以是字符串，也可以是数值；当前记录的字段，还可以是变量或awk的表达式   

​    （3）如省略item，相当于print $0;

2 变量

   内建变量    

​       FS:输入字段分隔符，默认为空白字符

​       awk -v FS=':' '{print $1}' /etc/passwd

​       OFS:输出字段分割符，默认为空白字符 

​       awk -v FS=':' -v OFS=':' '{print $1,$3}' /etc/passwd

​       RS:输入的换行符

​      ORS:输出时的换行符

​       NF: 每一行的字段数量

​       awk '{print NF}' /etc/fstab

​       NR:文件中的行数

​       FNR:各文件分别计数；行数

​       FILENAME:当前文件名

​       ARGC: 命令行参数的个数

​       ARGV: 数组，保存的是命令行所给定的各参数

​       awk 'BEGIN{print ARGV[1]}' /etc/fstab 

   自定义变量     

​    （ 1）    -v   var=value

​           变量名区分字符大小写

​    （2）  在program中直接定义

​           awk 'BEGIN{test="hellow awk";print test}'

3 printf命令

​         格式化输出：printf  FORMAT, item1，item2.....

​         (1) FORMAT必须给出

​         (2)不会自动换行，需要显式给出换控制符，\n

​         (3)FORMAT中需要分别为后面的每个item指定一个格式化符号

​         格式符：awk -F: '{printf "username:%s,UID:%d\n",$1,$3}' /etc/passwd

​                 %c：显示字符ASCII码

​                %d,%i:显示十进制整数

​                %e,%E:科学计数法数值显示；

​                %f:显示浮点数

​                %g,%G:以科学计数法或浮点形式显示数值

​                %s：显示字符串

​                %u：无符号整数

​                 %%：显示%自身

​        修饰符：

​                \#[.#]：第一个数字控制显示的宽度；第二个#表示小数点的精度

​                       %3.1f

​                  awk -F: '{printf "username:%15s,UID:%d\n",$1,$3}' /etc/passwd

​                 -：左对齐

​                 +：显示数字符号

4 操作符

​     算术操作符

​         x+y，x-y，x*y，x/y，x^y, x%y

​     字符串操作符:没有符号的操作符，字符串连接

​     赋值操作符：

​         =，+=，-+，*=

​      模式匹配符：

​          ~：是否匹配

​         ！~：是否不匹配

​      逻辑操作符

​          &&

​           ||

​      函数调用

​          function_name(argu1,argu2,...)

​       条件表达式

​        selecto？  if-true-expression：if-false-expression

awk -F: '{$3>=1000?usertype="Common User":usertype="Sysadmin or SysUser";printf"%15s:%-s\n",$1,usertype}' /etc/passwd

5 PATTERN

   (1) empty：空模式，匹配每一行

   (2) /regular expression :仅处理模式匹配到的行

~]# awk '/^\//{print $1}' /etc/fstab

   (3) relation expression:关系表达式，结果有“真”有“假”.结果为真才会处理

​          真：结果为非0值，非空字符串

​          awk -F: '$3<=1000{print $1,$3}' /etc/passw

​          ~]# awk -F: '$NF=="/bin/bash"{print $1,$NF}' /etc/passwd

​            ]# awk -F: '$NF~/bash$/{print $1,$NF}' /etc/passwd

  (4) line range :行范围 /part1/ /part2/

​      不支持直接给出数字的格式，示例：

​      awk '(NR>=5&&NR<=10){print $1}' /etc/passwd

  (5) BEGIN/END模式

​       BEGIN{}:仅在开始处理文件中的文本之前执行一次

awk -F: BEGIN'{print "username              uid  \n---------------------------"}''{printf"%-13s %10d\n",$1,$3}' /etc/passwd

​       END{}: 仅在文本处理完成之后执行一次

6 常用action

​    (1) Expressions

​    (2) control statements: if, while等

​    (3)Compound statements:组合语句

​    (4) input and output statements

7 控制语句

​      if（condition）{statement}

​      if（condition）{statement} else {statement}

​     while(condition) {statments}

​     do {statements} while(condition)

​      for (expr1;expr2;expr3) {statement}

​      break

​      continue

​      delete  array[index]

​      delete  array

​      exit

7.1  if-else

​    语法：if（condition)statement[else statement]

awk -F: '{if($3>=1000) {printf "Common user:%s\n",$1} else {printf "root or Sysuser:%s\n",$1}}' /etc/passwd

~]# awk -F: '{if($3>=1000)printf "username:%s,uid:%d\n",$1,$3}' /etc/passwd

 awk -F: '{if($NF=="/bin/bash")print $1,$7}' /etc/passwd

 awk '{if(NF>5) print $0}' /etc/fstab

 df -h | awk -F [%] '/^\/dev/{print $1}' | awk '{if($NF>=20) print $1}'

 使用场景：对awk取得的整行或某个字段做条件判断

7.2 while 

   语法：while(condition) statement

   条件为真进入循环，条件为假退出

   使用场景：对一行内的多个字段逐一处理时使用

awk '/^[[:space:]]*linux16/ {i=1;while(i<=NF) {print $i,length($i); i++}}' /etc/grub2.cfg 

awk '/^[[:space:]]*linux16/ {i=1;while(i<=NF) {if(length($i)>=7) print $i,length($i); i++}}' /etc/grub2.cfg 

7.3 do while

   语法：do statement while（condition） 至少执行一次循环体

7.4 for 循环

   语法：for（expr1 ;expr2；expr3)statement

   awk '/^[[:space:]]*linux16/{for(i=1;i<=NF;i++) {print $i,length($i)}}' /etc/grub2.cfg

7.5 switch

   语法：switch（expression）{case VALUE1 or /REGEXP/: statement; case VALUE2 or /REGEXP2/： statement; ....; default: statement}

7.6 break和continue

​     break[n[

​     continue

7.7 next

​       提前结束对本行的处理直接进入下一行；

​      awk -F: '{if($3%2!=0) next; print $1,$3}' /etc/passwd

\8. array

  关联数组： array[index-expression]

​       index-expression:

​             (1) 可使用任意字符串，字符串要使用双引号

​             (2)如果某数组元素事先不存在，在引用时，awk会自动创建此元素，并将其值初始化为空

​           awk 'BEGIN{weekdays["mon"]="Monday";weekdays["tue"]="Tuesday";print weekdays["mon"]}'

​           若要判断数组中是否存在某元素，要使用“index in array”格式进行

​           若要遍历数组中的每个元素，要使用for循环

​          awk 'BEGIN{weekdays["mon"]="Monday";weekdays["tue"]="Tuesday";for(i in weekdays) {print weekdays[i]}}'

​         netstat -tan | awk '/^tcp\>/{state[$NF]++}END{for(i in state) {print i,state[i]}}'

​         awk '/^(UUID|\/dev)/{fs[$3]++}END{for(i in fs){print i,fs[i]}}' /etc/fstab 

​         awk '{for(i=1;i<=NF;i++){count[$i]++}}END{for(i in count){print i,count[i]}}' /etc/fstab 

9 内置函数

​       数值处理：

​             rand():返回0和1之间一个随机数

​        字符串处理

​             length([s]): 返回指定字符串的长度

​             sub（r,s,[t]): 以r表示的模式模式来查找t所表示的字符中的匹配内容，并将其第一次出现替换

为s所表示的内容

​             gsub（r,s,[t])表示全部替换

​             split（s,a.[r]): 以r为分隔符切割字符s，并将切割后的结果保存至a所表示的属组中

​             切割后数组索引安装 1 2 3 4 保存

​           netstat -tan | awk '/^tcp\>/{split($5,ip,":");count[ip[1]]++}END{for(i in count) {print i,count[i]}}'