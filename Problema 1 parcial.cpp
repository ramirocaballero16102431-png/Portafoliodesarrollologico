#include <stdio.h>
#include <string.h>

int main() {
    char entrada[6];
    int hora24, minuto, hora12;
    char horaMin[6] = "99:99";
    char horaMax[6] = "00:00";

    for (int i = 1; i <= 3; i++) {
        printf("Introduce la hora %d en formato HH:MM (5 caracteres): ", i);
        scanf("%s", entrada);

        // Extraer hora y minutos
        sscanf(entrada, "%d:%d", &hora24, &minuto);

        // Convertir a 12 horas
        if (hora24 == 0) {
            hora12 = 12;
            printf("Hora %d en formato 12h: %d:%02d AM\n", i, hora12, minuto);
        } else if (hora24 < 12) {
            hora12 = hora24;
            printf("Hora %d en formato 12h: %d:%02d AM\n", i, hora12, minuto);
        } else if (hora24 == 12) {
            hora12 = 12;
            printf("Hora %d en formato 12h: %d:%02d PM\n", i, hora12, minuto);
        } else {
            hora12 = hora24 - 12;
            printf("Hora %d en formato 12h: %d:%02d PM\n", i, hora12, minuto);
        }

        // Comparar para mínimo y máximo
        if (strcmp(entrada, horaMin) < 0) {
            strcpy(horaMin, entrada);
        }
        if (strcmp(entrada, horaMax) > 0) {
            strcpy(horaMax, entrada);
        }
    }

    printf("La hora más baja ingresada es: %s\n", horaMin);
    printf("La hora más alta ingresada es: %s\n", horaMax);

    return 0;
}

