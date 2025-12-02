Algoritmo problema4parcial
	Definir anio Como Entero
	
    Escribir "Introduce el año: "
    Leer anio
	
    // Verificar si es bisiesto
    Si (anio MOD 4 = 0) Entonces
        Si (anio MOD 100 = 0) Entonces
            Si (anio MOD 400 = 0) Entonces
                Escribir anio, " es un año bisiesto."
            Sino
                Escribir anio, " NO es un año bisiesto."
            FinSi
        Sino
            Escribir anio, " es un año bisiesto."
        FinSi
    Sino
        Escribir anio, " NO es un año bisiesto."
    FinSi

FinAlgoritmo
