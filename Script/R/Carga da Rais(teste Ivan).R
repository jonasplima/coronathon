#Colocar o caminho onde está a base
setwd("~/Documents/Coronathon/Bases")

#Nome das colunas
nomes <-c("Bairros SP","Bairros Fortaleza",
          "Bairros RJ","Causa Afastamento 1",
          "Causa Afastamento 2","Causa Afastamento 3",
          "Motivo Desligamento","CBO Ocupação 2002",
          "CNAE 2.0 Classe","CNAE 95 Classe",
          "Distritos SP","Vínculo Ativo 31/12",
          "Faixa Etária","Faixa Hora Contrat",
          "Faixa Remun Dezem (SM)","Faixa Remun Média (SM)",
          "Faixa Tempo Emprego","Escolaridade após 2005",
          "Qtd Hora Contr","Idade",
          "Ind CEI Vinculado","Ind Simples",
          "Mês Admissão","Mês Desligamento",
          "Mun Trab","Município",
          "Nacionalidade","Natureza Jurídica",
          "Ind Portador Defic","Qtd Dias Afastamento",
          "Raça Cor","Regiões Adm DF",
          "Vl Remun Dezembro Nom","Vl Remun Dezembro (SM)",
          "Vl Remun Média Nom","Vl Remun Média (SM)",
          "CNAE 2.0 Subclasse","Sexo Trabalhador",
          "Tamanho Estabelecimento","Tempo Emprego",
          "Tipo Admissão","Tipo Estab",
          "Tipo Estab2","Tipo Defic",
          "Tipo Vínculo","IBGE Subsetor",
          "Vl Rem Janeiro CC","Vl Rem Fevereiro CC",
          "Vl Rem Março CC","Vl Rem Abril CC",
          "Vl Rem Maio CC","Vl Rem Junho CC",
          "Vl Rem Julho CC","Vl Rem Agosto CC",
          "Vl Rem Setembro CC","Vl Rem Outubro CC",
          "Vl Rem Novembro CC","Ano Chegada Brasil",
          "Ind Trab Intermitente","Ind Trab Parcial",
          "Tipo Salário","Vl Salário Contratua")

# Limitar a quantidade de linhas para não dar pau
teste<-read.delim2("RAIS_VINC_PUB_SP.txt", sep = ";", nrow = 1000, col.names = nomes)


