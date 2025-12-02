#include <stdio.h>

int main() {
    double horas, tarifa, salarioBruto, salarioNeto, impuesto, horasExtras;

    printf("Introduce las horas trabajadas en la semana: ");
    scanf("%lf", &horas);
    printf("Introduce la tarifa por hora: ");
    scanf("%lf", &tarifa);

    if (horas <= 40) {
        salarioBruto = horas * tarifa;
    } else {
        horasExtras = horas - 40;
        salarioBruto = 40 * tarifa + horasExtras * tarifa * 1.5;
    }

    if (salarioBruto <= 750) {
        impuesto = 0;
    } else {
        impuesto = salarioBruto * 0.10;
    }

    salarioNeto = salarioBruto - impuesto;

    printf("Salario bruto: %.2lf Balboas\n", salarioBruto);
    printf("Impuesto: %.2lf Balboas\n", impuesto);
    printf("Salario neto: %.2lf Balboas\n", salarioNeto);

    return 0;
}

