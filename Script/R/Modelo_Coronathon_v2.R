## Instala o pacote do Tidyverse
install.packages("tidyverse")

# Carrega as variáveis
library(tidyverse)
library(readxl)

# Define a workspace
setwd("/Users/jonasplima/Desktop/Coronathon/coronathon/")

# Carrega base do caged utilizando as seguites segmentações
# TOP 30 CBOs que foram ADMITIDOS em 2019 em SP
caged <- read.csv("Dados/CAGED/CAGED.csv", sep = ";",encoding='cp1252')  

attach(caged)

# Corrige o formato das colunas
caged$GRAU_INSTRUCAO <- as.factor(GRAU_INSTRUCAO)
caged$CBO <- as.character(CBO) 
caged$SALARIO <- as.integer(SALARIO)
caged$PORTADOR_DEFICIENCIA <- as.character(PORTADOR_DEFICIENCIA)

attach(caged)

### Cria dimensão de CBOs únicos
cbos <- unique(caged$CBO)

# Gera tabela auxiliar do caged com nome de colunas para cruzamento
caged_col <- matrix(ncol = length(cbos), nrow = length(caged$CBO))
caged_col <- as.data.frame(caged_col)
colnames(caged_col) <- paste("a",cbos, sep = "")
 
# gera tabela inicial para comparativos
for (i in 1:length(cbos)) {
  caged_col[,i] <- ifelse(caged$CBO == cbos[i],1,0)
}

### Separa base de treino e base de teste
bases_treino <- list(0)
bases_teste <- list(0)

set.seed(0)

base_total <- cbind(caged, caged_col)

j <- sample(0.7*nrow(base_total))

bases_treino <- base_total[j,]
bases_teste <- base_total[-j,]
 
#### Remove coluna de município, pois só está sendo usado SP para criação do Modelo
bases_treino <- bases_treino %>% select(-MUNICIPIO)
bases_teste <- bases_teste %>% select(-MUNICIPIO)
base_total <- base_total %>% select(-MUNICIPIO)

###### STEP de criação do modelo

## lista auxiliar
reg_log <- list(0)
 
# Execução do modelo de regressão logística
for (t in 1:length(cbos)) {
  
  reg_log[[t]] <- bases_treino %>% 
    
    glm(as.formula(paste(colnames(bases_teste[t+4]),"~ GRAU_INSTRUCAO+SALARIO+PORTADOR_DEFICIENCIA", sep="")), 
        family = binomial(link="logit"), 
        data = .)
}
 
# Gerando o summary do modelo
modelo_reg_log <- list(0)
for (o in 1:length(cbos)) {
  
  modelo_reg_log[[o]] <- summary(reg_log[[o]])
  
}

# Puxando os parâmetros do modelo
tabela_parametros <- list(0)
for (y in 1:length(cbos)) {
  
  tabela_parametros[[y]] <- as.data.frame(modelo_reg_log[[y]]$coefficients)
  tabela_parametros[[y]]$Estimate <- exp(tabela_parametros[[y]]$Estimate)
}

# Gera tabela auxiliar
predicoes <- matrix(ncol = length(cbos), nrow = length(bases_teste$CBO))
predicoes <- as.data.frame(predicoes)
colnames(predicoes) <- cbos

## Gera tabela de predições 
for (x in 1:length(cbos)) { 
  predicoes[,x] <- as.data.frame(bases_teste %>%  
                                    predict(reg_log[[x]], newdata = ., type = "response")) 
}

# Gera tabela auxiliar
resultado <- matrix(ncol = length(cbos), nrow = length(bases_teste$CBO))
resultado <- as.data.frame(resultado)
colnames(resultado) <- paste("aa",cbos, sep="")
 
# Atribui o resultado da predição 
for (i in 1:cbos) { 
  resultado[,i] <- ifelse(predicoes[,i] > 0.01,1,0) 
}

# Tabela auxiliar
comparacao <- list(0)
tabela_teste <- list(0)

# Cria tabela para análise de acurácia do modelo
for (x in 1:length(predicoes)) {
  comparacao[[x]] <- cbind(bases_teste[,x+4], resultado[,x])
  tabela_teste[[x]] <- table(comparacao[[x]][,1],comparacao[[x]][,2])
}


acuracia <- rep(0,length(tabela_teste))

# Resultado da acurácia
for (y in 1:length(tabela_teste)) { 
  acuracia[y] <- sum(diag(tabela_teste[[y]]))/sum(tabela_teste[[y]])
  }

# Cria variável de análise para ponderação da acurácia do modelo
proporcoes_cbo <- caged %>% 
                   count(CBO) %>% 
                   summarize(prop = n / sum(n))

# cria tabela de proporção vs acurácia por cbo
concat_prop_acu <- cbind(acuracia, proporcoes_cbo)

# cria coluna de soma produto
concat_prop_acu <- concat_prop_acu %>% mutate (somaprod = acuracia * prop)

# junta com informações de CBO 
resultado_final <- cbind(concat_prop_acu, cbos)

# Gera base de saída da tabela
write_csv2(resultado_final, "Dados/CAGED/CAGED.csv") 