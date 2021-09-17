# ---------------------------------------------------------------------
# Calculate and plot radar strategies
# ---------------------------------------------------------------------

# Loading necessary scripts and packages
library(ggalt)
library(tidyverse)
library(grid)
library(reshape2)
library(directlabels)
library(scales)
library(colorspace)
library(patchwork)
source("general_processing/generate_colorpals.R")

#-- Constantes
a <- 6378 #-- km
ke <- 4 / 3
r <- seq(0, 240, 2) #-- km
h_grid <- seq(0, 20, 0.5)

sipam_elevs <- c(0.9, 1.5, 2, 3, 4, 5, 6, 7, 8, 9, 10.5, 12, 13.5)

sipam_scan <- merge(r, sipam_elevs) %>%
  rename(r = x, elev = y) %>%
  mutate(
    h = sqrt(r^2 + (ke * a)^2 + 2 * r * ke * a * sin(elev * pi / 180)) - ke * a,
    h_up = sqrt(r^2 + (ke * a)^2 + 2 * r * ke * a * sin((elev + 0.99) * pi / 180)) - ke * a,
    h_down = sqrt(r^2 + (ke * a)^2 + 2 * r * ke * a * sin((elev - 0.99) * pi / 180)) - ke * a,
    elev = as.factor(elev),
    cut_r = cut(r, breaks = seq(0, 240, by = 2), include.lowest = T),
    cut_h_up = cut(h_up, breaks = seq(0.5, 20, by = 0.5), include.lowest = T),
    cut_h_down = cut(h_down, breaks = seq(0.5, 20, by = 0.5), include.lowest = T)
  ) %>% 
  group_by(elev, cut_r, cut_h_up, cut_h_down) %>% 
  mutate(n_bin = n()) %>% 
  ungroup() %>% 
  group_by(elev) %>% 
  mutate(p_bin = n_bin/n())

# Plotting
theme_set(theme_bw())

ggplot(sipam_scan, aes(x = r)) +
  # geom_vline(aes(y = h), xintercept = c(61.4, 221), linetype = "dashed") +
  geom_ribbon(aes(ymax = h_up, ymin = h_down, fill = elev, color = elev),
              alpha = 0.6, size = 0.1
  ) +
  geom_line(aes(y = h, color = elev), size = 1, linetype = "dotted") +
  labs(
    title = "SIPAM", x = "Range (km)", y = "Height (km)",
    fill = expression("Elevation (" * degree * ")"),
    color = expression("Elevation (" * degree * ")")
  ) +
  # labs(
  #   title = "Estratégia de Varredura - SIPAM", x = "Alcance (km)", y = "Altura (km)",
  #   fill = expression("Elevação ("*degree*")"),
  #   color = expression("Elevação ("*degree*")")
  # ) +  # pt-br
  scale_fill_manual(values = pal_scan(length(sipam_elevs))) +
  scale_color_manual(values = pal_scan(length(sipam_elevs))) +
  coord_cartesian(ylim = c(0, 20), xlim = c(0, 250)) +
  theme(
    plot.title = element_text(hjust = 0.5),
    plot.background = element_rect(fill = "transparent", color = "transparent"),
    legend.background = element_rect(fill = "transparent")
  )
ggsave("radar_processing/figs/sipam_scan_strategy_R.png", 
       width = 8, height = 4, dpi = 300, bg = "transparent")

ggplot(sipam_scan) +
  geom_tile(aes(x = cut_r, y = cut_h_up, fill = n_bin)) +
  geom_tile(aes(x = cut_r, y = cut_h_down, fill = n_bin))

# plt_sipam + plt_sr + plt_xpol +
#   plot_layout(ncol = 1) +
#   plot_annotation(tag_levels = "a") &
#   theme(
#     plot.background = element_rect(
#       fill = "transparent",
#       color = "transparent"
#     ),
#     legend.background = element_rect(fill = "transparent")
#   )
# ggsave("General_Processing/figures/scan_strategy_full.png",
#        width = 6, height = 7.5, dpi = 300, bg = "transparent"
# )
