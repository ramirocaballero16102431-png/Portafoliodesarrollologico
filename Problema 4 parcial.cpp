#include <stdio.h>

int main() {
    int anio;

    printf("Introduce el año: ");
    scanf("%d", &anio);

    if (anio % 4 == 0) {
        if (anio % 100 == 0) {
            if (anio % 400 == 0) {
                printf("%d es un año bisiesto.\n", anio);
            } else {
                printf("%d NO es un año bisiesto.\n", anio);
            }
        } else {
            printf("%d es un año bisiesto.\n", anio);
        }
    } else {
        printf("%d NO es un año bisiesto.\n", anio);
    }

    return 0;
}

