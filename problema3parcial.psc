Algoritmo problema3parcial
	Definir diaNac, mesNac, anioNac Como Entero
    Definir diaAct, mesAct, anioAct Como Entero
    Definir edadAnios, edadMeses, edadDias Como Entero
	
    // Leer fecha de nacimiento
    Escribir "Introduce el día de nacimiento: "
    Leer diaNac
    Escribir "Introduce el mes de nacimiento (1-12): "
    Leer mesNac
    Escribir "Introduce el año de nacimiento: "
    Leer anioNac
	
    // Leer fecha actual
    Escribir "Introduce el día actual: "
    Leer diaAct
    Escribir "Introduce el mes actual (1-12): "
    Leer mesAct
    Escribir "Introduce el año actual: "
    Leer anioAct
	
    // Calcular edad inicial
    edadAnios <- anioAct - anioNac
    edadMeses <- mesAct - mesNac
    edadDias <- diaAct - diaNac
	
    // Ajustar días si negativos
    Si edadDias < 0 Entonces
        edadDias <- edadDias + 30
        edadMeses <- edadMeses - 1
    FinSi
	
    // Ajustar meses si negativos
    Si edadMeses < 0 Entonces
        edadMeses <- edadMeses + 12
        edadAnios <- edadAnios - 1
    FinSi
	
    // Mostrar resultado
    Si edadAnios = 0 Entonces
        Escribir "El individuo tiene ", edadMeses, " meses y ", edadDias, " días."
    Sino
        Escribir "El individuo tiene ", edadAnios, " años."
    FinSi

FinAlgoritmo
