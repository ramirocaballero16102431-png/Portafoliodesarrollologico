#include <stdio.h>

int main() {
    int diaNac, mesNac, anioNac;
    int diaAct, mesAct, anioAct;
    int edadAnios, edadMeses, edadDias;

    // Leer fecha de nacimiento
    printf("Introduce el día de nacimiento: ");
    scanf("%d", &diaNac);
    printf("Introduce el mes de nacimiento (1-12): ");
    scanf("%d", &mesNac);
    printf("Introduce el año de nacimiento: ");
    scanf("%d", &anioNac);

    // Leer fecha actual
    printf("Introduce el día actual: ");
    scanf("%d", &diaAct);
    printf("Introduce el mes actual (1-12): ");
    scanf("%d", &mesAct);
    printf("Introduce el año actual: ");
    scanf("%d", &anioAct);

    // Calcular edad inicial
    edadAnios = anioAct - anioNac;
    edadMeses = mesAct - mesNac;
    edadDias = diaAct - diaNac;

    // Ajustar días si negativos
    if (edadDias < 0) {
        edadDias += 30;  // aproximación de mes
        edadMeses -= 1;
    }

    // Ajustar meses si negativos
    if (edadMeses < 0) {
        edadMeses += 12;
        edadAnios -= 1;
    }

    // Mostrar resultado
    if (edadAnios == 0) {
        printf("El individuo tiene %d meses y %d días.\n", edadMeses, edadDias);
    } else {
        printf("El individuo tiene %d años.\n", edadAnios);
    }

    return 0;
}

