#include <stdio.h>
#include <string.h>

int mesATexto(char mes[]) {
    if (strcmp(mes, "enero") == 0) return 1;
    if (strcmp(mes, "febrero") == 0) return 2;
    if (strcmp(mes, "marzo") == 0) return 3;
    if (strcmp(mes, "abril") == 0) return 4;
    if (strcmp(mes, "mayo") == 0) return 5;
    if (strcmp(mes, "junio") == 0) return 6;
    if (strcmp(mes, "julio") == 0) return 7;
    if (strcmp(mes, "agosto") == 0) return 8;
    if (strcmp(mes, "septiembre") == 0) return 9;
    if (strcmp(mes, "octubre") == 0) return 10;
    if (strcmp(mes, "noviembre") == 0) return 11;
    if (strcmp(mes, "diciembre") == 0) return 12;
    return 0;
}

int main() {
    int dia, anio, mesNum;
    char mes[20];
    char fechaMin[11] = "9999-99-99";
    char fechaMax[11] = "0000-00-00";
    char fecha[11];

    for (int i = 1; i <= 3; i++) {
        printf("Introduce la fecha %d (ejemplo: 15 febrero 1989): ", i);
        scanf("%d %s %d", &dia, mes, &anio);

        mesNum = mesATexto(mes);

        printf("Fecha %d en numeros: %d %d %d\n", i, dia, mesNum, anio);

        // Crear formato AAAA-MM-DD
        sprintf(fecha, "%04d-%02d-%02d", anio, mesNum, dia);

        // Comparar
        if (strcmp(fecha, fechaMin) < 0) {
            strcpy(fechaMin, fecha);
        }
        if (strcmp(fecha, fechaMax) > 0) {
            strcpy(fechaMax, fecha);
        }
    }

    printf("La fecha más baja es: %s\n", fechaMin);
    printf("La fecha más alta es: %s\n", fechaMax);

    return 0;
}

