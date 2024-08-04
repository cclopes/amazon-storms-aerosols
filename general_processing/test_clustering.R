library(readr)
library(dplyr)
library(tidyr)
library(FactoMineR)
library(Factoshiny)
library(ggplot2)
library(stringr)
library(cowplot)

# Data with categorical vars
systems_25km <- read_csv("/home/camilacl/git/amazon-storms-aerosols/data/general/systems_filtered_25km.csv",
                         col_types = cols(date_init = col_datetime(format = "%Y-%m-%d %H:%M:%S")),
                         ) %>% drop_na()
systems_10km <- read_csv("/home/camilacl/git/amazon-storms-aerosols/data/general/systems_filtered_10km.csv", 
                                  col_types = cols(date_init = col_datetime(format = "%Y-%m-%d %H:%M:%S")))

# Analyzing systems_25km
systems_25km$area <- as.factor(systems_25km$area)
systems_25km$reflectivity <- as.factor(systems_25km$reflectivity)
systems_25km$lifespan <- as.factor(systems_25km$lifespan)
systems_25km$`sys duration` <- as.factor(systems_25km$`sys duration`)
systems_25km$season <- as.factor(systems_25km$season)
systems_25km$`time of day` <- as.factor(systems_25km$`time of day`)
systems_25km$`electrical activity` <- as.factor(systems_25km$`electrical activity`)

Factoshiny::MFAshiny(systems_25km)
# Results for above line
newDF <- systems_25km[,c("sys duration","time of day","season","area","lifespan","max reflectivity","max echotop 0 dBZ","max echotop 20 dBZ","max echotop 40 dBZ","max VIL","max VII","max VIWL","GLD strokes","CAPE","CIN","bl relative humidity","v-wind shear","warm cloud depth","total aerosols","ultrafine aerosols","total CCNs","reflectivity","electrical activity")]
res.MFA<-MFA(newDF,group=c(3,2,8,5,3,2), type=c("n","n","s","s","s","n"),ncp=3,name.group=c("convection_time","convection_geom","convection_int","initiation_thermo","initiation_aero","supplement_conv"),num.group.sup=c(6),graph=FALSE)
plot.MFA(res.MFA, choix="ind",lab.par=FALSE,title="Individual factor map")
plot.MFA(res.MFA, choix="var",habillage='group',title="Correlation circle")
plot.MFA(res.MFA, choix="group")
plot.MFA(res.MFA, choix="axes",habillage='group')
res.HCPC<-HCPC(res.MFA,nb.clust=6,consol=TRUE,graph=FALSE,description=TRUE,order=FALSE)
plot.HCPC(res.HCPC,choice='tree',title='Hierarchical tree')
plot.HCPC(res.HCPC,choice='map',draw.tree=FALSE,title='Factor map')
plot.HCPC(res.HCPC,choice='3D.map',ind.names=FALSE,centers.plot=FALSE,angle=60,title='Hierarchical tree on the factor map')

# Reproducing apps
Factoshiny::MFAshiny(res.MFA)
Factoshiny::HCPCshiny(res.MFA)

# Extracting clusters and saving to file
clusters_systems_25km <- res.HCPC$data.clust
clusters_systems_25km$name <- systems_25km$name
clusters_systems_25km$`max area` <- systems_25km$`max area`
clusters_systems_25km %>% 
  filter(clust %in% c(1,2,4,5)) %>% 
  relocate(clust) %>% 
  relocate(name) %>% 
  write.csv(
    "/home/camilacl/git/amazon-storms-aerosols/data/general/clusters_aero_systems_25km.csv", 
    row.names = FALSE)

