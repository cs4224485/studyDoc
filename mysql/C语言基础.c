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
			