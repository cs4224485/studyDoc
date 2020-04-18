1 视图

create view course2teacher as select * from course inner join teacher on course.teacher_id = teacher.id 

2 触发器

	# 插入前
	create trigger tri_before_insert_tb1 before insert  on tb1 for each row
	BEGIN
	......
	END

	# 插入后
	crate trigger tri_after_insert_tb1 after insert on tb1 for each row
	BEGIN
	.....
	END
	1
	# 删除前
	create trigger tri_before_delete_tb1 before delete on tb1 for each row
	BEGIN
	......
	END
	
	# 删除后
	crate trigger tri_after_delete_tb1 after delete on tb1 for each row
	BEGIN
	.....
	END

	# 更新前
	create trigger tri_before_update_tb1 before update on tb1 for each row
	BEGIN
	......
	END
	
	# 跟新后
	create trigger tri_after_update_tb1 after update on tb1 for each row
	BEGIN
	......
	END
触发器示例：
			#准备表
		CREATE TABLE cmd (
			id INT PRIMARY KEY auto_increment,
			USER CHAR (32),
			priv CHAR (10),
			cmd CHAR (64),
			sub_time datetime, #提交时间
			success enum ('yes', 'no') #0代表执行失败
		);

		CREATE TABLE errlog (
			id INT PRIMARY KEY auto_increment,
			err_cmd CHAR (64),
			err_time datetime
		);

		#创建触发器
		delimiter //
		CREATE TRIGGER tri_after_insert_cmd AFTER INSERT ON cmd FOR EACH ROW
		BEGIN
			IF NEW.success = 'no' THEN #等值判断只有一个等号
					INSERT INTO errlog(err_cmd, err_time) VALUES(NEW.cmd, NEW.sub_time) ; #必须加分号
			  END IF ; #必须加分号
		END//
		delimiter ;


		#往表cmd中插入记录，触发触发器，根据IF的条件决定是否插入错误日志
		INSERT INTO cmd (
			USER,
			priv,
			cmd,
			sub_time,
			success
		)
		VALUES
			('egon','0755','ls -l /etc',NOW(),'yes'),
			('egon','0755','cat /etc/passwd',NOW(),'no'),
			('egon','0755','useradd xxx',NOW(),'no'),
			('egon','0755','ps aux',NOW(),'yes');


		#查询错误日志，发现有两条
		mysql> select * from errlog;
		+----+-----------------+---------------------+
		| id | err_cmd         | err_time            |
		+----+-----------------+---------------------+
		|  1 | cat /etc/passwd | 2017-09-14 22:18:48 |
		|  2 | useradd xxx     | 2017-09-14 22:18:48 |
		+----+-----------------+---------------------+
		rows in set (0.00 sec)

3 存储过程
	无参数创建方式：
		delimiter //
		create procedure p1()
		BEGIN
			select * from testdb.employee;
		END //
		delimiter;
	
	在mysql中的调用方式
	     call p1();
	在Python中的调用
		 cursor.callproc('p1')
	
    有参数创建方式：	
		delimiter //
		create procedure p2(in n1 int,in n2 int,out res int)
		BEGIN
			select * from testdb.employee where age > n1 and id < n2;
			set res = 1;
			
		END //
		delimiter;
		
		在mysql中的调用方式
		 set @x = 0 
	     call p2(20,2,@x);
		
		在Python中的调用
			 cursor.callproc('p2',(2,4,0)

