建表

create table department(
id int primary key auto_increment,
name varchar(20)
);

create table employee(
id int primary key auto_increment,
name varchar(20),
sex enum('male','female') not null default 'male',
age int，
dep_id int
);

插入数据

insert into department values
(200,'技术'),
(201,'人力资源'),
(202,'销售'),
(203,'运营');

insert into employee(name,sex,age,dep_id) values
('harry','male',24,200),
('alex','female',49,201),
('jerry','male',25,200),
('吴佩','female',20,202),
('jingliyang','female',24,203),
('liwenzhou','male',18,204);


连表方式

1 内连接：只取两张表的共同部分
select * from employee inner join department on employee.dep_id = department.id;

2 左连接：在内连接的基础上保留左表的记录
select * from employee left join department on employee.dep_id = department.id;

3 右连接：在内连接的基础上保留右表的记录
select * from employee right join department on employee.dep_id = department.id;

4 全外连接：在内连接的基础上保留左右两表没有对象关系的记录
select * from employee left join department on employee.dep_id = department.id
union
select * from employee right join department on employee.dep_id = department.id;

查询平均年龄大于30岁的部门
select department.name,avg(age) from employee inner join department on employee.dep_id = department.id
	group by department.name
	having avg(age) > 30;
	
select 语句的执行顺序
1 执行from语句
  通过from语句找到两张表后先做一个笛卡尔积将两张表拼在一起
2 执行on过滤
  通过on a.stuendt_id = b.id 条件过滤，根据on中指定条件去掉不符合条件的数据
3 添加外部行
  通过join语句连接两张表
4 执行where过滤
  通过where语句匹配条件进行过滤
5 执行group by
  对where过滤后的数据进行分组
6 执行having过滤
  分组后对表进行条件过滤
7 select 列表
  执行select语句
8 distinct语句
  执行distinct语句对表进行去重
9 order by语句
  对表进行排序
10 limit语句
   最后将表限制输出
   
子查询
1 查询平均年龄在25岁以上的部门名
select name from department where id in
(select dep_id from employee
	group by employee.dep_id
	having avg(age) > 25);
2 查询技术部员工姓名
select * from employee where dep_id =(
  select id from department 
	where name = '技术');
3 查看不足1人的部门名
 select name from department where id not in(
	select distinct dep_id from employee);
4 查询大于所有人平均年龄的员工名与年龄
  select name,age from employee where age >
    (select avg(age) from employee);
5 查询每个部门最新入职的那名员工
	select * from emp as t1 inner join
	(select max(hire) as max_hire,post from emp
	group by post) as t2
	on t1.post = t2.post
	where t1.hire = t2.max_hire;
