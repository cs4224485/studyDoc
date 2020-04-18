# include <stdio.h>

int main(void)
{
	float score;
	printf("ÇëÊäÈëÄúµÄ¿¼ÊÔ³É¼¨£º");
	scanf("%f", &score);
	
	if (score > 100)
		printf("×öÃÎ\n");
	else if (score>=90)
		printf("great\n");
	else if (score>=80)
		printf("good\n");
	else if (score>=60)
		printf("ok\n");
	else if (score<60 && score>=0)
		printf("bad\n");
	else
		printf("error\n");
		
	return 0;
}
	