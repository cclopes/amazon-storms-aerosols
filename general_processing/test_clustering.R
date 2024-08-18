library(readr)
library(dplyr)
library(tidyr)
library(FactoMineR)
library(Factoshiny)
library(ggplot2)
library(stringr)
library(gridGraphics)
library(cowplot)

# Data with categorical vars
systems_25km <- read_csv("/home/camilacl/git/amazon-storms-aerosols/data/general/systems_filtered_25km.csv",
                         col_types = cols(date_init = col_datetime(format = "%Y-%m-%d %H:%M:%S")),
                         ) %>% drop_na()
systems_10km <- read_csv("/home/camilacl/git/amazon-storms-aerosols/data/general/systems_filtered_10km.csv", 
                         col_types = cols(date_init = col_datetime(format = "%Y-%m-%d %H:%M:%S")),
                         ) %>% drop_na()

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
newDF <- systems_25km[,c("sys duration","time of day","season","area","lifespan","max reflectivity","max echotop 0 dBZ","max echotop 20 dBZ","max echotop 40 dBZ","max VIL","max VII","max VIWL","GLD strokes","CAPE","CIN","bl relative humidity","v-wind shear","warm cloud depth","total aerosols","sub-50nm aerosols","total CCNs","reflectivity","electrical activity")]
res.MFA<-MFA(newDF,group=c(3,2,8,5,3,2), type=c("n","n","s","s","s","n"),ncp=3,name.group=c("convection_time","convection_geom","convection_int","initiation_thermo","initiation_aero","supplement_conv"),num.group.sup=c(6),graph=FALSE)
res.HCPC<-HCPC(res.MFA,nb.clust=6,consol=TRUE,graph=FALSE,description=TRUE,order=FALSE)

# Reproducing apps
Factoshiny::MFAshiny(res.MFA)
Factoshiny::HCPCshiny(res.MFA)

# Saving plots
theme_set(theme_bw())
theme_update(plot.title = element_text(hjust = 0.5))

plt1 <- plot.MFA(res.MFA, choix="ind",lab.par=FALSE,title="Individual factor map",graph.type='ggplot')
plt2 <- plot.MFA(res.MFA, choix="var",habillage='group', title="Correlation circle - quantitative variables")
plt3 <- plot.MFA(res.MFA, choix="group")
plt4 <- plot.MFA(res.MFA, choix="axes",habillage='group')
cowplot::plot_grid(plt1, plt2, plt3, plt4, rel_widths = c(1,1.3,1,1.2), labels = "auto")
ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/mfa_25km.png', height = 10, width = 12)

plt1 <- ~ plot.HCPC(res.HCPC,choice='bar',title='Inertia gain')
plt2 <- ~ plot.HCPC(res.HCPC,choice='map',draw.tree=FALSE,title='Factor map')
plt3 <- ~ plot.HCPC(res.HCPC,choice='3D.map',ind.names=FALSE,centers.plot=TRUE,angle=60,title='Hierarchical tree on the factor map')
cplt <- cowplot::plot_grid(plot_grid(plt1, plt2, labels = c('a', 'b'), rel_widths = c(1.2,1)), rel_heights = c(1.2,1), plt3, labels = c('', 'c'), nrow = 2)
# ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/hcpc_25km.png', height = 10, width = 12)
cowplot::save_plot('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/hcpc_25km.png', cplt, base_height = 12, base_width = 14)

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

# Analyzing systems_10km
systems_10km$area <- as.factor(systems_10km$area)
systems_10km$reflectivity <- as.factor(systems_10km$reflectivity)
systems_10km$lifespan <- as.factor(systems_10km$lifespan)
systems_10km$`sys duration` <- as.factor(systems_10km$`sys duration`)
systems_10km$season <- as.factor(systems_10km$season)
systems_10km$`time of day` <- as.factor(systems_10km$`time of day`)
systems_10km$`electrical activity` <- as.factor(systems_10km$`electrical activity`)

Factoshiny::MFAshiny(systems_10km)
# Results for above line
newDF <- systems_10km[,c("sys duration","time of day","season","area","lifespan","max reflectivity","max echotop 0 dBZ","max echotop 20 dBZ","max echotop 40 dBZ","max VIL","max VII","max VIWL","GLD strokes","CAPE","CIN","bl relative humidity","v-wind shear","warm cloud depth","total aerosols","sub-50nm aerosols","total CCNs","reflectivity","electrical activity")]
res.MFA<-MFA(newDF,group=c(3,2,8,5,3,2), type=c("n","n","s","s","s","n"),ncp=3,name.group=c("convection_time","convection_geom","convection_int","initiation_thermo","initiation_aero","supplement_conv"),num.group.sup=c(6),graph=FALSE)
res.HCPC<-HCPC(res.MFA,nb.clust=5,consol=TRUE,graph=FALSE,description=TRUE,order=FALSE)

# Reproducing apps
Factoshiny::MFAshiny(res.MFA)
Factoshiny::HCPCshiny(res.MFA)

# Saving plots
theme_set(theme_bw())
theme_update(plot.title = element_text(hjust = 0.5))

plt1 <- plot.MFA(res.MFA, choix="ind",lab.par=FALSE,title="Individual factor map",graph.type='ggplot')
plt2 <- plot.MFA(res.MFA, choix="var",habillage='group', title="Correlation circle - quantitative variables")
plt3 <- plot.MFA(res.MFA, choix="group")
plt4 <- plot.MFA(res.MFA, choix="axes",habillage='group')
cowplot::plot_grid(plt1, plt2, plt3, plt4, rel_widths = c(1,1.3,1,1.2), labels = "auto")
ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/mfa_10km.png', height = 10, width = 12)

plt1 <- ~ plot.HCPC(res.HCPC,choice='bar',title='Inertia gain')
plt2 <- ~ plot.HCPC(res.HCPC,choice='map',draw.tree=FALSE,title='Factor map')
plt3 <- ~ plot.HCPC(res.HCPC,choice='3D.map',ind.names=FALSE,centers.plot=TRUE,angle=60,title='Hierarchical tree on the factor map')
cplt <- cowplot::plot_grid(plot_grid(plt1, plt2, labels = c('a', 'b'), rel_widths = c(1.2,1)), rel_heights = c(1.2,1), plt3, labels = c('', 'c'), nrow = 2)
# ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/hcpc_10km.png', height = 10, width = 12)
cowplot::save_plot('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/hcpc_10km.png', cplt, base_height = 12, base_width = 14)

# Extracting clusters and saving to file
clusters_systems_10km <- res.HCPC$data.clust
clusters_systems_10km$name <- systems_10km$name
clusters_systems_10km$`max area` <- systems_10km$`max area`
clusters_systems_10km %>% 
  filter(clust %in% c(2,3,4,5)) %>% 
  relocate(clust) %>% 
  relocate(name) %>% 
  write.csv(
    "/home/camilacl/git/amazon-storms-aerosols/data/general/clusters_aero_systems_10km.csv", 
    row.names = FALSE)
