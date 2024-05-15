library(readxl)
library(FrF2)

datos_thomas_sara_manu <- read_excel("C:\\Users\\thomm\\Documents\\GitHub\\modelacion-y-simulacion-5\\parciales\\p3\\datos-thomas-sara-manu.xlsx")
df = as.data.frame(t(datos_thomas_sara_manu))

colnames(df) <- df[1, ]  # Set column names to the values in the first row
df <- df[-1, ]  # Remove the first row since it's now the column names
str(df) # All strings
df[] <- lapply(df, as.numeric)
str(df)

factorial_design = FrF2(nruns = 64, nfactors = 6, 
                        factor.names = list(OI = c(2,4), OE = c(2,4), RLED = c(1,2),
                                            RSTV = c(1,2), R4K = c(1,2), RI = c(1,2)),randomize = F,
                        replications = 1)


tsis = df$`Productos terminados.Average Time in System`
factorial_tsis <- add.response(design = factorial_design, response = tsis)
summary(factorial_tsis)

OE = factor(df$`Op_Ensamble.Max Available`)
OI = factor(df$`Op_Inspección.Max Available`)
R4K = factor(df$`Ensamblaje 4K.Replication`)
RLED = factor(df$`Ensamblaje LED.Replication`)
RSTV = factor(df$`Ensamblaje Smart TV.Replication`)
RI = factor(df$`Inspección.Replication`)

Model = lm(df$`Productos terminados.Average Time in System`~(OE+OI+R4K+RLED+RSTV+RI)^3)
ANOVA = aov(Model)
summary(ANOVA)

#Prueba de comparaciones multiples
Tukey_result <- TukeyHSD(ANOVA)
Tukey_result


datensambladores2 <- factorial_tsis[factorial_tsis$'OE' == 2, ]
datensambladores4 <- factorial_tsis[factorial_tsis$'OE' == 4, ]
boxplot(df$`Productos terminados.Average Time in System` ~ OE, 
        data = rbind(datensambladores2, datensambladores4),
        names = c(paste("OE = ", 2), paste("OE =", 4)),
        main = "Boxplots para OE",
        xlab = "Número de ensambladores", ylab = "Tiempo promedio en el sistema")


datsmartv1 <- factorial_tsis[factorial_tsis$'RSTV' == 1, ]
datsmartv2 <- factorial_tsis[factorial_tsis$'RSTV' == 2, ]
boxplot(df$`Productos terminados.Average Time in System` ~ RSTV, 
        data = rbind(datensambladores2, datensambladores4),
        names = c(paste("RSTV = ", 1), paste("RSTV =", 2)),
        main = "Boxplots para RSTV",
        xlab = "Número de réplicas para producción de SmartTV", ylab = "Tiempo promedio en el sistema")


qqnorm(rstandard(Model))
qqline(rstandard(Model))
shapiro.test(rstandard(Model))

# Grafica de efectos principales
MEPlot(factorial_tsis, lwd = 2)
abline(h=0, col="red")

# Grafica de Interacciones
IAPlot(factorial_tsis, lwd = 2)

# Grafica de Interacción Triple
resp = df$`Productos terminados.Average Time in System`
cubePlot(obj = resp, eff1 = OE, eff2 = OI, eff3 = RI, main = "Cubo")

