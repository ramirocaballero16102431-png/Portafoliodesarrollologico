#include <stdio.h>
int main (){
int a,b;
a=5;
printf("El valor de a es: %d",a);
printf("\nDe un valor para b\n");
scanf("%d",&b);
printf("\nEl valor de b es: %d\n",b);
float c;
printf("\n De un valor para c\n");
scanf("%f",&c);
printf("\nEl valor de c es: %.2f\n",c);
printf("\nEscriba su nombre\n");
char d;
scanf(" %c",&d);
printf("\nSu nombre es:%c\n",d);
return 0;	
}
