
create table emp (
id int not null unique auto_increment,
name varchar(20) not null,
sex enum('male','female') not null default 'male',
age int(3) unsigned not null,
hire date not null,
post varchar(50),
post_commnet varchar(100),
salary double(15,2),
office int,
depart_id int,
);

insert into emp(name,sex,age,hire,post,salary,office,depart_id) values
('harry','male',24,'20180301','IT',9222.3,401,1),
('sam','male',25,'20180301','IT',4522.3,401,1),
('beal','male',30,'20170301','IT',9832.3,401,1),
('王强','male',40,'20100301','sale',922.3,402,2),
('曹爽','male',34,'20170301','大将军',19222.3,403,3),
('呵呵','female',21,'20180301','ui',9222.3,404,4);

insert into emp(name,sex,age,hire,post,salary,office,depart_id) values('蔡爽','male',25,'20180301','IT',10000.5,401,1);

1 简单查询
	select id,name,sex,age,hire,post,post_commnet from emp;

2 避免重复
	select distinct post from emp;
3 通过四则运算
	select name, salary*12 from emp;
	select name, salary*12 as Annual_salary from emp;
	select name, salary*12 annual_salary from emp;
4 定义显示格式
	CONCAT() 函数用于连接字符串
	select concat('姓名：',name,'年薪：',salary*12) as annual_salary
	from emp;
	
	CONCAT_WS() 第一个参数为分隔符
	select concat_ws(':',name,salary*12) as annual_salary from emp;


WHERE 条件使用

1 单条件查询
	select name from emp where id > 7;	
2 多条件查询
	select name,post,salary from emp where post='IT' and salary > 5000;
3 In关键字
	select name,post,age,salary from emp where age in(25,24,40);
4 like关键字
	通配符'%'
	select * from emp where name like 'ha%';
	select * from emp where name like 'sa_';
5 关键字 between and
	select name,salary from emp where salary between 5000 and 15000;
	select name,salary from emp where salary not between 10000 and 15000;
6 关键字 is null(判断某个字段是否为null不能用等号，需要用is)
	select * from emp where post_commnet is null;
	
练习
1 查看岗位是IT的员工姓名和年龄
	select name,age from emp where post='IT';
2 查看岗位是IT且年龄大于30岁的员工姓名和年龄
	select name,age from emp where post='IT' and age > 30;
3 查看岗位是IT且薪资在9000-10000范围内的员工姓名，年龄和薪资
	select name,age,salary from emp where post='IT' and salary between 9000 and 10000;
4 查看岗位描述不为null的
	select * from emp where post_commnet is not null;
5 查看岗位是IT并且薪资是10000或9000或30000的员工姓名，年龄，薪资
	select * from emp where salary in (10000,9000,30000);
6 查看岗位是IT且薪资不是10000或9000或30000的员工姓名，年龄，薪资
	select * from emp where salary not in (10000,9000,30000);
7 查看岗位是IT并且名字是har开头的员工姓名和年薪
	select name,salary*12 from emp where name like 'har%';
	
	
分组查询 group by
1 分组发生在where之后，即分组是基于where之后得到的记录进行的
2 分组指的是将所有记录按照某个相同字段进行归类，比如真的员工表的职位分组，或者按照请别进行分组
3 取出每个某某进行操作
4 可以按照人一直字段分组，但是分组完毕后，比如group by post只能查看post字段，如果想查看组内信息需要借助聚合函数

ONLY_FULL_GROUP_BY #设置只能去分组的字段
set global sql_mode='only_full_group_by'; 

聚合函数
max
min
avg
sum
count
group_concat

查询每个职位有多少个员工
    select post,count(name) from emp group by post;
查询每个不同岗位的最大工资和最小工资
    select post,max(salary),min(salary) from emp group by post;
查看岗位以及岗位包含的所有员工名字
	select post,group_concat(name) from emp group by post;
查询公司男员工和女员工的个数
	select sex,count(id) from emp group by sex;
查询岗位以及岗位的平均薪资
	select post,avg(salary) from emp group by post;
查询男员工与男员工的平均薪资，女员工与女员工的平均薪资
	select sex,avg(salary) from emp group by sex;
	
having 过滤
1 where 发生在分组group by之前，因而where中可以有任意字段，但是绝对不能使用聚合函数
2 having 发生在分组group by之后， 因而having中可以使用分组的字段，无法直接娶到其他字段，可以使用聚合函数

练习
 查询各岗位包含员工个数小于2的岗位名，岗位包含员工和个数
    select post,name,count(id) from emp group by post having count(id) < 2;
 查询各个岗位平均薪资大于10000的岗位名，平均工资
	select post,avg(salary) from emp group by post having avg(salary) > 10000;
 查询各个岗位平均薪资大于10000且小于20000的岗位名，平均工资
	select post,avg(salary) from emp group by post having avg(salary) between 10000 and 20000;

order by 升序和降序
  先按照age升序排，如果age相同则按照id降序排
   select * from emp order by age asc，id desc；
  
  
  
  
  
  
   