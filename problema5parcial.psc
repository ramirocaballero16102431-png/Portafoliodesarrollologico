Algoritmo problema5parcial
	Definir horas, tarifa, salarioBruto, salarioNeto, impuesto, horasExtras Como Real
    Definir mostrarBruto, mostrarImpuesto, mostrarNeto Como Real
	
    Escribir "Introduce las horas trabajadas en la semana: "
    Leer horas
    Escribir "Introduce la tarifa por hora: "
    Leer tarifa
	
    Si horas <= 40 Entonces
        salarioBruto <- horas * tarifa
    Sino
        horasExtras <- horas - 40
        salarioBruto <- 40 * tarifa + horasExtras * tarifa * 1.5
    FinSi
	
    // Calcular impuesto
    Si salarioBruto <= 750 Entonces
        impuesto <- 0
    Sino
        impuesto <- salarioBruto * 0.10
    FinSi
	
    salarioNeto <- salarioBruto - impuesto
	
    // Simular 2 decimales
    mostrarBruto <- Trunc(salarioBruto * 100 + 0.5) / 100
    mostrarImpuesto <- Trunc(impuesto * 100 + 0.5) / 100
    mostrarNeto <- Trunc(salarioNeto * 100 + 0.5) / 100
	
    Escribir "Salario bruto: ", mostrarBruto, " Balboas"
    Escribir "Impuesto: ", mostrarImpuesto, " Balboas"
    Escribir "Salario neto: ", mostrarNeto, " Balboas"

FinAlgoritmo
