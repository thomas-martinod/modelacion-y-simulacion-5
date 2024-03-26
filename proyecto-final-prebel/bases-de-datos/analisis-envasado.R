library(readxl)
paros_envasado_gran_volumen_2023 <- read_excel("C:\\Users\\thomm\\Documents\\GitHub\\modelacion-y-simulacion-5\\proyecto-final-prebel\\bases-de-datos\\paros-envasado-gran-volumen-2023.xlsx", 
                                               col_types = c("text", "numeric", "date", 
                                                             "numeric", "text", "numeric", "numeric", 
                                                             "numeric", "text", "text", "text", 
                                                             "text"))

# Contar la frecuencia de los elementos en la columna 'Tipo Intervalo'
frecuencia_tipo_intervalo <- sort(table(paros_envasado_gran_volumen$`Tipo Intervalo`),decreasing = TRUE)

# Mostrar la frecuencia
print(frecuencia_tipo_intervalo)


# Sumar los tiempos de paro para cada 'Tipo Intervalo'
suma_tiempo_paro <- aggregate(paros_envasado_gran_volumen$`Tiempo del Paro (Minutos)`, 
                              by = list(paros_envasado_gran_volumen$`Tipo Intervalo`), 
                              FUN = mean)

# Renombrar las columnas
colnames(suma_tiempo_paro) <- c("Tipo Intervalo", "Tiempo Paro Total")

# Ordenar los resultados por el tiempo total de paro en orden descendente
suma_tiempo_paro_ordenada <- suma_tiempo_paro[order(-suma_tiempo_paro$`Tiempo Paro Total`),]

# Mostrar el resultado ordenado
print(suma_tiempo_paro_ordenada)
