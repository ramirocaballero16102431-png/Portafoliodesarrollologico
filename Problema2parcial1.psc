Algoritmo Problema2parcial
	Definir dia, anio, mesNumero, i Como Entero
    Definir mesTexto, fechaMin, fechaMax, fecha, fechaMinMostrar, fechaMaxMostrar Como Cadena
	
    fechaMin <- "99991231"
    fechaMax <- "00000101"
    fechaMinMostrar <- ""
    fechaMaxMostrar <- ""
	
    Para i <- 1 Hasta 3 Hacer
        Escribir "Introduce el día de la fecha ", i, ": "
        Leer dia
        Escribir "Introduce el mes de la fecha ", i, " (en texto, ej: febrero): "
        Leer mesTexto
        Escribir "Introduce el año de la fecha ", i, ": "
        Leer anio
		
        // Convertir mes de texto a número
        Segun mesTexto Hacer
            "enero": mesNumero <- 1
            "febrero": mesNumero <- 2
            "marzo": mesNumero <- 3
            "abril": mesNumero <- 4
            "mayo": mesNumero <- 5
            "junio": mesNumero <- 6
            "julio": mesNumero <- 7
            "agosto": mesNumero <- 8
            "septiembre": mesNumero <- 9
            "octubre": mesNumero <- 10
            "noviembre": mesNumero <- 11
            "diciembre": mesNumero <- 12
            De Otro Modo:
                mesNumero <- 0
        FinSegun
		
        Escribir "Fecha ", i, " en números: ", dia, " ", mesNumero, " ", anio
		
        // Formato AAAAMMDD para comparar
        fecha <- ConvertirATexto(anio*10000 + mesNumero*100 + dia)
		
        // Guardar la fecha completa para mostrar
        fechaCompleta <- ConvertirATexto(dia) + " " + ConvertirATexto(mesNumero) + " " + ConvertirATexto(anio)
		
        // Comparar fechas
        Si fecha < fechaMin Entonces
            fechaMin <- fecha
            fechaMinMostrar <- fechaCompleta
        FinSi
        Si fecha > fechaMax Entonces
            fechaMax <- fecha
            fechaMaxMostrar <- fechaCompleta
        FinSi
    FinPara
	
    Escribir "La fecha más baja es: ", fechaMinMostrar
    Escribir "La fecha más alta es: ", fechaMaxMostrar

FinAlgoritmo
