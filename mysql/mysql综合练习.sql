mysql 综合查询

13 查询全部学生都选修了的课程号和课程名
	select cid,cname 
	from 
	course
	where 
		cid in(
		select
		   course_id
		from
		   score
		group by
			course_id
		having
			count(sid) = (
			   select 
				 count(sid)
			   from
				 student
		)         
		)
17 查询平均成绩大于85的学生姓名和平均成绩
	select 
	   t1.name,t2.avg_num 
	from 
	  student as t1
	 inner join
    (
	select 
		student_id, avg(num) as avg_num
	from 
		score
	group by
		student_id
	having
		avg(num) > 85
	) as t2
	on t1.sid = t2.student_id

19 查看所有选修了李平老师课程的学生中，这些课程(李平老师的课程，不是所有课程) 平均成绩最高的学生姓名
	select
		sname
	from
		student
	where
		sid =(
		
			select
				student_id
			from
				score
			where
				course_id in(
					select 
						cid
					from
						course
					where 
						teacher_id = (
							select
							  tid
							from
							  teacher
							where
							  tname = '李平老师'
						)
				)
			group by
				student_id
			order by
				avg(num) desc
			limit 1
		);