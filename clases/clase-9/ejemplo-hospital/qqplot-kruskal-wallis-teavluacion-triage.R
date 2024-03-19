hosp <- datos.hospital.descriptiva
View(hosp)
t_ev = hosp$Tiempo.Evaluacion...minutos.
triage = hosp$TriageNum
boxplot(t_ev ~ triage, data=hosp)
kruskal.test(t_ev ~ triage, data=hosp)
