Algoritmo Problema1
	Definir hora24, hora12, min Como Entero
    Definir entrada Como Cadena
    Definir i Como Entero
    Definir horaMin, horaMax Como Cadena
    
    horaMin <- "99:99"
    horaMax <- "00:00"
    
    Para i <- 1 Hasta 3 Hacer
        Escribir "Introduce la hora ", i, " en formato HH:MM (5 caracteres): "
        Leer entrada
        
        // Extraemos hora y minutos
        hora24 <- ConvertirANumero(Subcadena(entrada,0,2))
        min <- ConvertirANumero(Subcadena(entrada,3,2))
        
        // Convertimos a 12 horas
        Si hora24 = 0 Entonces
            hora12 <- 12
            Escribir "Hora ", i, " en formato 12h: ", hora12, ":", min, " AM"
        Sino
            Si hora24 < 12 Entonces
                hora12 <- hora24
                Escribir "Hora ", i, " en formato 12h: ", hora12, ":", min, " AM"
            Sino
                Si hora24 = 12 Entonces
                    hora12 <- 12
                    Escribir "Hora ", i, " en formato 12h: ", hora12, ":", min, " PM"
                Sino
                    hora12 <- hora24 - 12
                    Escribir "Hora ", i, " en formato 12h: ", hora12, ":", min, " PM"
                FinSi
            FinSi
        FinSi
        
        // Comparar para hallar mínimo y máximo
        Si entrada < horaMin Entonces
            horaMin <- entrada
        FinSi
        Si entrada > horaMax Entonces
            horaMax <- entrada
        FinSi
    FinPara
    
    Escribir "La hora más baja ingresada es: ", horaMin
    Escribir "La hora más alta ingresada es: ", horaMax

FinAlgoritmo
