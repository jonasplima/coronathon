install.packages("tidyverse")

library(tidyverse)
library(readxl)

setwd("/Users/jonasplima/Desktop/Coronathon/coronathon/")

caged <- read.csv("Dados/CAGED/CAGED.csv", sep = ";",encoding='cp1252')  

str(caged)

attach(caged)

caged$GRAU_INSTRUCAO <- as.factor(GRAU_INSTRUCAO)
caged$CBO <- as.character(CBO)
caged$MUNICIPIO <- as.character(MUNICIPIO)
caged$SALARIO <- as.integer(CBO)
caged$PORTADOR_DEFICIENCIA <- as.character(PORTADOR_DEFICIENCIA)

length(caged)

attach(caged)
#### segmentando por cbo
base_cbo <- list(0)

for (i in 1:length(caged$CBO)) {

  base_cbo[[i]] <-  as.data.frame(rep(caged,i))

}


#### tratando a variavel cbo

for (l in 1:length(cbos)) {
  
  base_cbo[[l]]$CBO.2002.Ocupa??o <- ifelse(
    
    base_cbo[[l]]$CBO.2002.Ocupa??o == cbos[l], 1, 0)

}


#### separando base de treino e base de teste
bases_treino <- list(0)
bases_teste <- list(0)

set.seed(0)

for (k in 1:length(cbos)) {

  j <- sample(0.7*nrow(caged))
  bases_treino[[k]] <- as.data.frame(base_cbo[[k]][j,])
  bases_teste[[k]] <- as.data.frame(base_cbo[[k]][-j,])
    
}



reg_log <- list(0)

for (t in 1:length(cbos)) {

  reg_log[[t]] <- bases_treino[[t]] %>% 
    
    glm(CBO.2002.Ocupa??o ~ Grau.Instru??o + Qtd.Hora.Contrat, family = binomial(link="logit"), data = .)
}


#reg_log <- bases_treino[[1]] %>% 
#  glm(CBO.2002.Ocupa??o~Grau.Instru??o, family = binomial(link="logit"), data = .)

modelo_reg_log <- list(0)
for (o in 1:length(cbos)) {

  modelo_reg_log[[o]] <- summary(reg_log[[o]])
  
}
#modelo_reg_log <- summary(reg_log)

tabela_parametros <- list(0)
for (y in 1:length(cbos)) {

  tabela_parametros[[y]] <- as.data.frame(modelo_reg_log[[y]]$coefficients)
  
}

predicoes <- list(0)
for (x in 1:length(cbos)) {
  
  predicoes[[x]] <- as.data.frame(bases_teste[[x]] %>% 
  
  predict(reg_log[[x]], newdata = ., type = "response"))
  
  colnames(predicoes[[x]]) <- cbos[x]
  
}


for (i in 1:cbos) {
  
  predicoes[[i]]$`622020` <- ifelse(predicoes[[i]]$`622020` > 0.1,1,0)
  
}


comparacao <- list(0)

for (c in 1:length(cbos)) {
  
  comparacao[[c]] <- cbind(bases_teste[[c]]$CBO.2002.Ocupa??o, predicoes[[c]]$`622020`)

  }

