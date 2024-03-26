library(readxl)

# Read the Excel file
paros_manofactura <- read_excel("C:\\Users\\thomm\\Documents\\GitHub\\modelacion-y-simulacion-5\\proyecto-final-prebel\\bases-de-datos\\paros-manofactura-2023.xlsx", 
                                sheet = "Resumen Paros", 
                                col_types = c("text", "text", "text", "numeric", "date", "text", "text"))

# Generate the subbase of data with rows where the value in the 'ÁREA' column is 'Gran Volumen'
paros_manufactura_gran_volumen <- subset(paros_manofactura, AREA == "Gran Volumen")

# Count the frequency of elements in the 'tipo de paro' column
frecuencia_tipo_paro <- sort(table(paros_manufactura_gran_volumen$`tipo de paro`), decreasing = TRUE)

# Show the frequency
print(frecuencia_tipo_paro)

# Sum the stop times for each 'Tipo Intervalo'
suma_tiempo_paro <- aggregate(paros_manufactura_gran_volumen$`T. Paro`, 
                              by = list(paros_manufactura_gran_volumen$`tipo de paro`), 
                              FUN = mean)

# Rename the columns
colnames(suma_tiempo_paro) <- c("Tipo Intervalo", "Tiempo Paro Media")

# Order the results by the total stop time in descending order
suma_tiempo_paro_ordenada <- suma_tiempo_paro[order(-suma_tiempo_paro$`Tiempo Paro Media`), ]

# Show the ordered result
print(suma_tiempo_paro_ordenada)
