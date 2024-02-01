# Install package to read excel files
# install.packages("readxl")

# Load library
library("readxl")

piracy.df = read_excel("~/Documents/College/NPS/3. Q3/Comp_Methods_2/Final_Project/Data_Files/ListOfIncidents_IMO.xls")
piracy.df$Date = as.Date(piracy.df$Date)         # Casts the dates to date objects
years = as.numeric(format(piracy.df$Date, "%Y")) # Takes only the years from the dates to make the histogram cleaner

par(mfrow=c(1,1))
hist(years, breaks=seq(1994, 2024, 1), 
     xaxp=c(1994,2024,30),  # Adds lines for all years in the data
     las=2,                 # Turns x-labels sideways
     xlab="Incident Year")

summary(piracy.df$Date)
