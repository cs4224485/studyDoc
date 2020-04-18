c语言基础

基本输入输出函数
	printf() -- 将变量的内容输出到屏幕
	四种用法
		1. printf("字符串")
		2. printf("输出控制符",输出参数);
		3. printf("输出控制符1 输出控制符2...", 输出参数1，输出参数2)
		4. printf("输出控制符 非输出控制符", 输出参数);
			输出控制符包含如下
				%d			--  int
				%ld			--  long int
				%c			--  char
				%f			--  float
				%lf			--  double
				%x			--  16进制数
				%s          --  字符串
				
	sacnf() --  通过键盘将数据输入到变量中
		三种用法
			1、 scanf("输入控制符", 输入参数) 功能：将从键盘输入的字符转化为输入控制符所规定格式的数据，然后存入输入参数的值为地址的变量中
			代码：
			# include <stdio.h>
			
			int main(voide)
			{	
				int i;
				scanf("%d", &i);  // $i 表示i的地址 $s 是一个取地址符
				printf("i = %d\n", i); 
				return 0
			}
			
			2. sacnf("非输入控制符 输入控制符", 输入参数);  注意非输入控制符必须原样输入
			# include <stdio.h>
			int main(void)
			{
				int i;
				scanf("m%d", &i);
				printf("i = %d\n", i);
				return;
			}
			
			3.sacnf("输入控制符 输入控制符 输入控制符", 输入参数)
			# include <stdio.h>
			
			int main(void)
			{	
				int i,j;
				scanf("%d %d", &i,&j);
				printf("i = %d, j = %d", i,j);
				return 0;
			}
			
		使用scanf编写高质量代码
			1. 使用scanf之前最好先用printf提示用户以什么样的方式输入
			2. scanf中尽量不要使用非输入控制符，尤其是不要用\n
			
			# include <stdio.h>
	
			int main(void)
			{
				int i;
				printf("请输入i的值:");
				sacnf("%d", &i);
				printf ("i = %d\n",i);
			}
			
C语言的流程控制
	if 语句
		1. 
			if  (表达式）
				语句A；
				语句B;
		2.
			if  (表达式）
			{
				语句A；
				语句B;
			}
		3   if (表达式1)
				A;
			else if (表达式2)
				B;
			else if (表达式3）
				C;
			else
				D;
			
	if 语句的常见错误
		1 空语句的问题
			if (3 > 2 );
			等价于
			if （3 > 2)
				   ;   // 这是一个空语句
					
		2 多分支if语句
		    if (表达式1)
				A;
			else if (表达式2)
				B;
			else if (表达式3）
				C;
			else
				D;
	
	
	C语言的for循环语句
		# include <stdio.h>
		int main(void){
			
			int i;
			int sum = 0;
			for (i=1; i<=100; ++i)
				sum+=i;
			printf("sum = %d\n", sum);
			return 0;
			}
			
	
	for和if语句的嵌套使用	
	// 求出1到100之间所有的能被3整除的数字之和
		# include <stdio.h>
		int main(void){
			int i；
			int sum；
			for (i=3; i<=100;++i){
				if (i%3 == 0) {   // 如果i能被3整除
					sum+=i
				}
			}
			printf("sum = %d\n", sum);
		}
	// 1 + 1/2 + 1/3 + ..... + 1/100 的和
	/*
	强制类型转化
		格式：
			(数据类型)(表达式)
		功能：
			把表达式的值强制转化为前面所执行的数据类型
		例子：
			(int)(4.5+2.2) 最终值是6
			(float)(5) 最终值是5.00000
	*/
		# include <stdio.h>
		int main(void){
			int i;
			float sum = 0;
			
			for (i=1; i<=100; ++i){
				sum += 1 / (float)(i);  // 将i强制将数据类型转换为浮点数
			} 
		
			printf("sum = %f\n", sum);
		}
	