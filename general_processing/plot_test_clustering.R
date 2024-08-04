library(readr)
library(dplyr)
library(tidyr)
library(ggplot2)
library(stringr)
library(cowplot)

# Analyzing files
clusters_aero_systems_25km <- read_csv("/home/camilacl/git/amazon-storms-aerosols/data/general/clusters_aero_systems_25km.csv")
clusters_aero_systems_25km$clust <- as.factor(clusters_aero_systems_25km$clust)
clusters_aero_systems_25km$area <- as.factor(clusters_aero_systems_25km$area)
clusters_aero_systems_25km$reflectivity <- as.factor(clusters_aero_systems_25km$reflectivity)
clusters_aero_systems_25km$lifespan <- as.factor(clusters_aero_systems_25km$lifespan)
clusters_aero_systems_25km$`sys duration` <- as.factor(clusters_aero_systems_25km$`sys duration`)
clusters_aero_systems_25km$season <- as.factor(clusters_aero_systems_25km$season)
clusters_aero_systems_25km$`time of day` <- as.factor(clusters_aero_systems_25km$`time of day`)
clusters_aero_systems_25km$`electrical activity` <- as.factor(clusters_aero_systems_25km$`electrical activity`)

clusters_all_25km <- read_csv("data/general/clusters_all_25km.csv")
clusters_all_25km$clust <- as.factor(clusters_all_25km$clust)

tapply(clusters_aero_systems_25km %>% select(!clust), clusters_aero_systems_25km$clust, summary)

clust_df <- clusters_aero_systems_25km %>% 
  group_by(clust) %>% 
  count() %>% 
  unite("c", clust, n, sep = " - ", remove = F) %>% 
  select(clust, c) %>% 
  mutate(clust = as.character(clust))
clust_n <- clust_df$c
names(clust_n) <- clust_df$clust
clusters_aero_systems_25km$clust_c <- clust_n[as.character(clusters_aero_systems_25km$clust)]

clust_df <- clusters_all_25km %>% 
  group_by(clust) %>% 
  count() %>% 
  unite("c", clust, n, sep = " - ", remove = F) %>% 
  select(clust, c) %>% 
  mutate(clust = as.character(clust))
clust_n <- clust_df$c
names(clust_n) <- clust_df$clust
clusters_all_25km$clust_c <- clust_n[as.character(clusters_all_25km$clust)]

clust_nas <- clusters_all_25km %>% 
  mutate(clust_c = clust_n[as.character(clusters_all_25km$clust)]) %>% 
  group_by(clust_c) %>% 
  summarise(
    `0 dBZ` = sum(is.na(echotop0)),
    `20 dBZ` = sum(is.na(echotop20)),
    `40 dBZ` = sum(is.na(echotop40))
    ) %>% 
  mutate(clust_c = paste("Cluster", clust_c, "cases")) %>% 
  gather('echotop', 'value', -clust_c) %>% 
  filter(value > 0) %>% 
  mutate(value = paste("NAs =", value))


# Plotting
theme_set(theme_bw())
theme_update(plot.title = element_text(hjust = 0.5))

c1 <- clusters_aero_systems_25km %>% 
  filter(clust == 1) %>% 
  select(c(`sys duration`, `time of day`, season, area, lifespan, reflectivity, `electrical activity`)) %>% 
  gather('category', 'value') %>% 
  group_by(category, value) %>% 
  count() %>% 
  mutate(
    category = factor(category, levels = c('electrical activity', 'reflectivity', 'lifespan', 'area', 'season', 'time of day', 'sys duration')),
    value = str_replace_all(value, "_", " "),
    value = factor(value, levels = c('with lightning', 'without lightning', 'intense', 'no intense', 'no splitmerge', 'with splitmerge', 'small', 'large', 'dry', 'dry-to-wet', 'wet', 'diurnal', 'nocturnal', 'short span', 'medium_span'))
  ) %>% 
  ggplot(aes(x = n, y = category, fill = value, group = value)) +
  geom_col(alpha = 0.7, color = 'black') +
  geom_label(aes(label = value), position = position_stack(vjust = .5), fill = 'white', size = 2.5) +
  scale_fill_manual(
    values = c('gold', 'gray', 'azure3', 'azure', 'azure', 'azure', 'red', 'yellowgreen', 'yellow', 'midnightblue', 'azure'),
    guide = "none")+
  labs(x = '', y = '', title = paste0('Cluster 1 - ', clusters_aero_systems_25km %>% filter(clust == 1) %>% nrow(), ' cases'))
# ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/cats_cluster_1_25km.png')

c2 <- clusters_aero_systems_25km %>% 
  filter(clust == 2) %>% 
  select(c(`sys duration`, `time of day`, season, area, lifespan, reflectivity, `electrical activity`)) %>% 
  gather('category', 'value') %>% 
  group_by(category, value) %>% 
  count() %>% 
  mutate(
    category = factor(category, levels = c('electrical activity', 'reflectivity', 'lifespan', 'area', 'season', 'time of day', 'sys duration')),
    value = str_replace_all(value, "_", " "),
    value = factor(value, levels = c('with lightning', 'without lightning', 'intense', 'no intense', 'no splitmerge', 'with splitmerge', 'small', 'large', 'dry', 'dry-to-wet', 'wet', 'diurnal', 'nocturnal', 'short span', 'medium span'))
  ) %>% 
  ggplot(aes(x = n, y = category, fill = value, group = value)) +
  geom_col(alpha = 0.7, color = 'black') +
  geom_label(aes(label = value), position = position_stack(vjust = .5), fill = 'white', size = 2.5) +
  scale_fill_manual(
    values = c('gold', 'gray', 'azure3', 'azure', 'azure3', 'azure', 'azure', 'azure3', 'red', 'dodgerblue', 'yellow', 'midnightblue', 'azure', 'azure3'),
    guide = "none") +
  scale_y_discrete(labels = NULL) +
  labs(x = '', y = '', title = paste0('Cluster 2 - ', clusters_aero_systems_25km %>% filter(clust == 2) %>% nrow(), ' cases'))
# ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/cats_cluster_2_25km.png')

c4 <- clusters_aero_systems_25km %>% 
  filter(clust == 4) %>% 
  select(c(`sys duration`, `time of day`, season, area, lifespan, reflectivity, `electrical activity`)) %>% 
  gather('category', 'value') %>% 
  group_by(category, value) %>% 
  count() %>% 
  mutate(
    category = factor(category, levels = c('electrical activity', 'reflectivity', 'lifespan', 'area', 'season', 'time of day', 'sys duration')),
    value = str_replace_all(value, "_", " "),
    value = factor(value, levels = c('with lightning', 'without lightning', 'intense', 'no intense', 'no splitmerge', 'with splitmerge', 'small', 'large', 'dry', 'dry-to-wet', 'wet', 'diurnal', 'nocturnal', 'short span', 'medium span'))
  ) %>% 
  ggplot(aes(x = n, y = category, fill = value, group = value)) +
  geom_col(alpha = 0.7, color = 'black') +
  geom_label(aes(label = value), position = position_stack(vjust = .5), fill = 'white', size = 2.5) +
  scale_fill_manual(
    values = c('gold', 'gray', 'azure3', 'azure', 'azure3', 'azure', 'azure', 'azure3', 'yellowgreen', 'dodgerblue', 'yellow', 'midnightblue', 'azure', 'azure3'),
    guide = "none") +
  labs(x = 'Number of cases', y = '', title = paste0('Cluster 4 - ', clusters_aero_systems_25km %>% filter(clust == 4) %>% nrow(), ' cases'))
# ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/cats_cluster_4_25km.png')

c5 <- clusters_aero_systems_25km %>% 
  filter(clust == 5) %>% 
  select(c(`sys duration`, `time of day`, season, area, lifespan, reflectivity, `electrical activity`)) %>% 
  gather('category', 'value') %>% 
  group_by(category, value) %>% 
  count() %>% 
  mutate(
    category = factor(category, levels = c('electrical activity', 'reflectivity', 'lifespan', 'area', 'season', 'time of day', 'sys duration')),
    value = str_replace_all(value, "_", " "),
    value = factor(value, levels = c('with lightning', 'without lightning', 'intense', 'no intense', 'no splitmerge', 'with splitmerge', 'small', 'large', 'dry', 'dry-to-wet', 'wet', 'diurnal', 'nocturnal', 'short span', 'medium span'))
  ) %>% 
  ggplot(aes(x = n, y = category, fill = value, group = value)) +
  geom_col(alpha = 0.7, color = 'black') +
  geom_label(aes(label = value), position = position_stack(vjust = .5), fill = 'white', size = 2.5) +
  scale_fill_manual(
    values = c('gold', 'gray', 'azure3', 'azure', 'azure3', 'azure', 'azure', 'azure3', 'yellowgreen', 'dodgerblue', 'yellow', 'midnightblue', 'azure', 'azure3'),
    guide = "none") +
  scale_y_discrete(labels = NULL) +
  labs(x = 'Number of cases', y = '', title = paste0('Cluster 5 - ', clusters_aero_systems_25km %>% filter(clust == 5) %>% nrow(), ' cases'))
# ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/cats_cluster_5_25km.png')

cowplot::plot_grid(c1, c2, c4, c5, rel_widths = c(1.3,1,1.3,1))
ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/categories_clusters_25km.png', height = 8)

echotop <- clusters_aero_systems_25km %>%
  select(c(clust_c, `max echotop 0 dBZ`, `max echotop 20 dBZ`, `max echotop 40 dBZ`)) %>% 
  gather('max echotop', 'value', -clust_c) %>% 
  mutate(
    `max echotop` = str_replace_all(`max echotop`, "max echotop ", ""),
    clust_c = paste("Cluster", clust_c, "cases")) %>% 
  ggplot() +
  geom_violin(aes(x = `max echotop`, y = value), draw_quantiles = c(0.25, 0.5, 0.75), scale = "count", trim = F, fill = "NA") +
  # geom_count(aes(x = `max echotop`, y = value), shape = 1) +
  # scale_size_continuous(breaks = c(2, 4, 6, 8, 10)) +
  scale_y_continuous(limits = c(2, 16), breaks = c(2, 6, 10, 14)) +
  theme(legend.position='bottom', legend.box.spacing = unit(0, "pt")) +
  facet_grid(~clust_c) +
  labs(x = 'Max echotop', y = 'Height (km)', size = "Cases")
# ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/max_echotop_clusters_25km.png', height = 5)

echotop_all <- clusters_all_25km %>%
  select(c(clust_c, echotop20, echotop0, echotop40)) %>% 
  gather('echotop', 'value', -clust_c) %>% 
  mutate(
    echotop = paste(str_replace_all(echotop, "echotop", ""), 'dBZ'),
    clust_c = paste("Cluster", clust_c, "cases")) %>% 
  ggplot() +
  geom_violin(aes(x = echotop, y = value), draw_quantiles = c(0.25, 0.5, 0.75), scale = "count", trim = F, fill = "NA") +
  geom_text(data = clust_nas, aes(x = echotop, y = 16, label = value), size = 2.5) +
  # geom_count(aes(x = echotop, y = value), shape = 1) +
  # scale_size_continuous(breaks = c(5, 10, 15, 20, 25, 30)) +
  scale_y_continuous(limits = c(2, 16), breaks = c(2, 6, 10, 14)) +
  theme(legend.position='bottom', legend.box.spacing = unit(0, "pt")) +
  guides(size = guide_legend(nrow = 1)) +
  facet_grid(~clust_c) +
  labs(x = 'Echotop', y = 'Height (km)', size = "Cases")
# ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/gld_strmin_clusters_25km.png', height = 3)

vi <- clusters_aero_systems_25km %>%
  select(c(clust_c, `max VIL`, `max VII`, `max VIWL`)) %>% 
  gather('max_vi', 'value', -clust_c) %>% 
  mutate(
    clust_c = paste("Cluster", clust_c, "cases"),# ) %>%
    max_vi = factor(max_vi, levels = c("max VIWL", "max VII", "max VIL"))) %>%
  ggplot() +
  geom_boxplot(aes(x = max_vi, y = value)) +
  # geom_violin(aes(x = max_vi, y = value), draw_quantiles = c(0.25, 0.5, 0.75)) +
  geom_jitter(aes(x = max_vi, y = value), shape = 1, size = 1) +
  scale_x_discrete() +
  theme(axis.title.x=element_blank()) +
  facet_grid(~clust_c) + 
  labs(y = 'kg/m²')
# ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/max_vi_clusters_25km.png', height = 5)

vi_all <- clusters_all_25km %>%
  select(c(clust_c, vil, vii, viwl)) %>% 
  gather('vi', 'value', -clust_c) %>% 
  mutate(
    clust_c = paste("Cluster", clust_c, "cases"),# ) %>%
    vi = toupper(vi),
    vi = factor(vi, levels = c("VIWL", "VII", "VIL"))) %>%
  ggplot() +
  # geom_boxplot(aes(x = vi, y = value)) +
  # geom_jitter(aes(x = vi, y = value), shape = 1, size = 1) +
  geom_violin(aes(x = vi, y = value), draw_quantiles = c(0.25, 0.5, 0.75), scale = "count", trim = F, fill = "NA") +
  scale_x_discrete() +
  scale_y_continuous(limits = c(0,NA)) +
  theme(axis.title.x=element_blank()) +
  facet_grid(~clust_c) + 
  labs(y = 'kg/m²')

area <- clusters_aero_systems_25km %>%
  select(c(clust_c, `max area`)) %>% 
  mutate(
    clust_c = paste("Cluster", clust_c, "cases")) %>% 
  ggplot() +
  geom_boxplot(aes(x = '', y = `max area`)) +
  geom_jitter(aes(x = '', y = `max area`), shape = 1, size = 1) +
  scale_x_discrete(drop = T) +
  scale_y_log10() +
  theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank()) +
  facet_grid(~clust_c) +
  labs(y = 'Max area (km²)')
# ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/gld_clusters_25km.png', height = 5)

gld <- clusters_aero_systems_25km %>%
  select(c(clust_c, `GLD strokes`)) %>% 
  mutate(
    clust_c = paste("Cluster", clust_c, "cases")) %>% 
  ggplot() +
  geom_boxplot(aes(x = '', y = `GLD strokes`)) +
  geom_jitter(aes(x = '', y = `GLD strokes`), shape = 1, size = 1) +
  scale_x_discrete(drop = T) +
  # scale_y_log10() +
  theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank()) +
  scale_y_continuous(trans=scales::pseudo_log_trans(base = 2), breaks=c(0, 1, 10, 100, 1000)) +
  facet_grid(~clust_c) +
  labs(y = 'GLD strokes')
# ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/gld_clusters_25km.png', height = 5)

gld_all <- clusters_all_25km %>%
  select(c(clust_c, gld_strmin)) %>% 
  mutate(
    clust_c = paste("Cluster", clust_c, "cases")) %>% 
  ggplot() +
  geom_boxplot(aes(x = '', y = gld_strmin)) +
  geom_jitter(aes(x = '', y = gld_strmin), shape = 1, size = 1) +
  scale_x_discrete(drop = T) +
  # scale_y_log10() +
  theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank()) +
  scale_y_continuous(trans=scales::pseudo_log_trans(sigma = 10e-2, base = 10), breaks=c(-10, -1, 0, 1, 10)) +
  facet_grid(~clust_c) +
  labs(y = 'strokes/min')
# ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/gld_strmin_clusters_25km.png', height = 5)

cape <- clusters_aero_systems_25km %>%
  select(c(clust_c, CAPE)) %>% 
  mutate(
    clust_c = paste("Cluster", clust_c, "cases")) %>% 
  ggplot() +
  geom_boxplot(aes(x = '', y = CAPE)) +
  geom_jitter(aes(x = '', y = CAPE), shape = 1, size = 1) +
  scale_x_discrete(drop = T) +
  # scale_y_log10() +
  theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank()) +
  facet_grid(~clust_c) +
  labs(y = 'CAPE (J/kg)')
# ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/cape_clusters_25km.png', height = 5)

cin <- clusters_aero_systems_25km %>%
  select(c(clust_c, CIN)) %>% 
  mutate(
    clust_c = paste("Cluster", clust_c, "cases")) %>% 
  ggplot() +
  geom_boxplot(aes(x = '', y = CIN)) +
  geom_jitter(aes(x = '', y = CIN), shape = 1, size = 1) +
  scale_x_discrete(drop = T) +
  # scale_y_log10() +
  theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank()) +
  facet_grid(~clust_c) +
  labs(y = 'CIN (J/kg)')
# ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/cin_clusters_25km.png', height = 5)

reflec <- clusters_aero_systems_25km %>%
  select(c(clust_c, `max reflectivity`)) %>% 
  mutate(
    clust_c = paste("Cluster", clust_c, "cases")) %>% 
  ggplot() +
  geom_boxplot(aes(x = '', y = `max reflectivity`)) +
  geom_jitter(aes(x = '', y = `max reflectivity`), shape = 1, size = 1) +
  scale_x_discrete(drop = T) +
  # scale_y_log10() +
  theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank()) +
  facet_grid(~clust_c) +
  labs(y = 'Max reflectivity (dBZ)')
# ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/reflectivity_clusters_25km.png', height = 5)

blrh <- clusters_aero_systems_25km %>%
  select(c(clust_c, `bl relative humidity`)) %>% 
  mutate(
    clust_c = paste("Cluster", clust_c, "cases")) %>% 
  ggplot() +
  geom_boxplot(aes(x = '', y = `bl relative humidity`)) +
  geom_jitter(aes(x = '', y = `bl relative humidity`), shape = 1, size = 1) +
  scale_x_discrete(drop = T) +
  # scale_y_log10() +
  theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank()) +
  facet_grid(~clust_c) +
  labs(y = 'BL relative humidity (%)')
# ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/reflectivity_clusters_25km.png', height = 5)

lvws <- clusters_aero_systems_25km %>%
  select(c(clust_c, `v-wind shear`)) %>% 
  mutate(
    clust_c = paste("Cluster", clust_c, "cases")) %>% 
  ggplot() +
  geom_boxplot(aes(x = '', y = `v-wind shear`)) +
  geom_jitter(aes(x = '', y = `v-wind shear`), shape = 1, size = 1) +
  scale_x_discrete(drop = T) +
  # scale_y_log10() +
  theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank()) +
  facet_grid(~clust_c) +
  labs(y = 'LL v-wind shear (m/s)')
# ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/reflectivity_clusters_25km.png', height = 5)

wcd <- clusters_aero_systems_25km %>%
  select(c(clust_c, `warm cloud depth`)) %>% 
  mutate(
    clust_c = paste("Cluster", clust_c, "cases")) %>% 
  ggplot() +
  geom_boxplot(aes(x = '', y = `warm cloud depth`)) +
  geom_jitter(aes(x = '', y = `warm cloud depth`), shape = 1, size = 1) +
  scale_x_discrete(drop = T) +
  # scale_y_log10() +
  theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank()) +
  facet_grid(~clust_c) +
  labs(y = 'Warm cloud depth (km)')
# ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/reflectivity_clusters_25km.png', height = 5)

aerosols <- clusters_aero_systems_25km %>%
  select(c(clust_c, `total aerosols`, `ultrafine aerosols`, `total CCNs`)) %>% 
  gather('aerosols', 'value', -clust_c) %>% 
  mutate(
    aerosols = str_replace_all(aerosols, "ultrafine", "sub-50nm"),
    aerosols = factor(aerosols, levels = c('total aerosols', 'sub-50nm aerosols', 'total CCNs')),
    clust_c = paste("Cluster", clust_c, "cases")) %>% 
  ggplot() +
  geom_boxplot(aes(x = aerosols, y = value)) +
  geom_jitter(aes(x = aerosols, y = value), shape = 1, size = 1) +
  scale_x_discrete(guide = guide_axis(angle = 90)) +
  # scale_y_continuous(trans=scales::pseudo_log_trans(base = 10)) +
  scale_y_log10() +
  theme(axis.title.x=element_blank()) +
  facet_grid(~clust_c) +
  labs(y = expression(~cm^{-3}))
ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/aerosols_clusters_25km.png', height = 3)

cowplot::plot_grid(area, reflec, echotop, vi, gld, labels = 'auto', ncol = 1, rel_heights = c(1,1,1.1,1.04,1), axis = 'l', align = 'v')
ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/convection_clusters_25km.png', height = 11)

cowplot::plot_grid(area, reflec, echotop_all, vi_all, gld, labels = 'auto', ncol = 1, rel_heights = c(1,1,1.1,1.04,1), axis = 'l', align = 'v')
ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/convection_clusters_withall_25km.png', height = 11)

cowplot::plot_grid(cape, cin, blrh, lvws, wcd, labels = 'auto', ncol = 1, axis = 'l', align = 'v')
ggsave('/home/camilacl/git/amazon-storms-aerosols/general_processing/figs/initiation_clusters_25km.png', height = 10)

