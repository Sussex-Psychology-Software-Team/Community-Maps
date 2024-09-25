library(readxl)
library(rworldmap)
library(dplyr)

## https://cran.r-project.org/web/packages/rworldmap/vignettes/rworldmapFAQ.pdf

folder <- "C:/Users/Jamie/Documents/R"
coauthor_data <- read_xlsx(file.path(folder,"international data from Darya.xlsx"))

## BY NUMBER OF OUTPUTS

## add up the number of outputs per country

coauthor_data <- coauthor_data[,c(2,3)]
outputs <- summarise_all(group_by(coauthor_data, Country_by_institution), sum)

sPDF <- joinCountryData2Map( outputs
                             ,joinCode = "NAME"
                             ,nameJoinColumn = "Country_by_institution")

mapDevice() #create world map shaped window
mapCountryData(sPDF,nameColumnToPlot='Outputs', catMethod = "pretty", colourPalette = "terrain")


mapCountryData(sPDF,nameColumnToPlot='Outputs', 
               catMethod = "pretty", 
               oceanCol = "lightblue",
               missingCountryCol = "white",
               mapRegion = "Europe",  # "Eurasia"
               colourPalette = "terrain") #"heat"

mapBubbles( dF=sPDF,  #getMap() 
            nameZSize="Outputs", 
            nameZColour="continent", 
            colourPalette='rainbow', 
            oceanCol='lightblue', 
            landCol='wheat') 

## BY NUMBER OF INSTITUTIONS
institutions <- data.frame(table(coauthor_data$Country_by_institution))

sPDF <- joinCountryData2Map( institutions
                             ,joinCode = "NAME"
                             ,nameJoinColumn = "Var1")

mapDevice() #create world map shaped window
mapCountryData(sPDF,nameColumnToPlot='Freq', catMethod = "pretty", colourPalette = "heat")

mapCountryData(sPDF,nameColumnToPlot='Freq', 
               catMethod = "pretty", 
               oceanCol = "lightblue",
               missingCountryCol = "white",
               mapRegion = "Eurasia",
               colourPalette = "heat")

mapBubbles( dF=sPDF,  #getMap() 
            nameZSize="Freq", 
            nameZColour="continent", 
            colourPalette='rainbow', 
            oceanCol='lightblue', 
            landCol='wheat') 