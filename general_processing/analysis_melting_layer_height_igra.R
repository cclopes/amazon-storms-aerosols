# ------------------------------------------------------------------------------
# Defining melting layer height in Campina from IGRA dataset
# ------------------------------------------------------------------------------

# Loading necessary packages ---------------------------------------------------
library(tidyverse)
library(lubridate)

# Loading data -----------------------------------------------------------------

# Station info - print
# BRM00082332  -3.1500  -59.9833   84.0    MANAUS (AERO)        1967 2021  22432

# First try
# igra2_derived <- read_table2("data/soundings/IGRA2/BRM00082332-drvd.txt", 
#                              col_names = c("PRESS", "REPGPH", "CALCGPH", "TEMP", 
#                                            "TEMPGRAD", "PTEMP", "PTEMPGRAD", 
#                                            "VTEMP", "VPTEMP", "VAPPRESS", 
#                                            "SATVAP", "REPRH", "CALCRH", "RHGRAD",
#                                            "UWND", "UWDGRAD", "VWND", "VWNDGRAD",
#                                            "N"), 
#                              comment = "#")

# Second try
igra2_header <- read_csv("data/soundings/IGRA2/BRM00082332-drvd.txt", 
                         col_names = "header") %>%
  # mutate(row_id = row_number()) %>% 
  filter(substr(header, 1, 1) == "#") %>% 
  # column_to_rownames("row_id") %>% 
  separate(header, 
           sep = c(1, 12, 17, 20, 23, 26, 31, 36, 43, 49, 55, 61, 67, 73, 79, 
                   85, 91, 97, 103, 109, 115, 121, 127, 133, 139, 145, 151, 157),
           into = c("HEADREC", "ID", "YEAR", "MONTH", "DAY", "HOUR", "RELTIME",
                    "NUMLEV", "PW", "INVPRESS", "INVHGT", "INVTEMPDIF", 
                    "MIXPRESS", "MIXHGT", "FRZPRESS", "FRZHGT", "LCLPRESS", 
                    "LCLHGT", "LFCPRESS", "LFCHGT", "LNBPRESS", "LNBHGT", "LI",
                    "SI", "KI", "TTI", "CAPE", "CIN"),
           convert = T)

# Extracting freezing height ---------------------------------------------------
frz_hgt <- igra2_header %>% 
  mutate(HOUR = na_if(HOUR, 99),
         date = ymd_hms(paste(YEAR, MONTH, DAY, HOUR, "00", "00")),
         FRZHGT = na_if(FRZHGT, -99999)) %>% 
  select(date, YEAR, MONTH, HOUR, FRZHGT, NUMLEV) %>% 
  mutate(HOUR = as.character(HOUR),
         clm = ifelse(YEAR <= 1990, "1961-1990", 
                      ifelse(YEAR == 2021, NA, "1991-2020")))

# Plots ------------------------------------------------------------------------
theme_set(theme_bw())
theme_update(plot.title = element_text(hjust = 0.5))

# Data availability ------------------------------------------------------------
ggplot(frz_hgt) +
  geom_histogram(aes(x = date), bins = 648) +
  geom_hline(yintercept = c(30, 60), color = "red") +
  scale_x_datetime(date_labels = "%Y", date_breaks = "5 year",
                   expand = c(0.01, 0.01)) +
  labs(title = "Data Availability per Month (1967 - 2021) - Manaus (AERO)",
       x = "Date", y = "Counts")
ggsave("general_processing/figs/igra2_data_availability.png",
       dpi = 300, width = 7, height = 3)

# Levels per sounding ----------------------------------------------------------
ggplot(frz_hgt) +
  geom_point(aes(x = date, y = NUMLEV), size = 0.1) +
  scale_x_datetime(date_labels = "%Y", date_breaks = "5 year",
                   expand = c(0.01, 0.01)) +
  labs(title = "Levels per Sounding (1967 - 2021) - Manaus (AERO)",
       x = "Date", y = "Number of Levels")
ggsave("general_processing/figs/igra2_levels_availability.png",
       dpi = 300, width = 7, height = 3)

# Boxplot of full dataset per month --------------------------------------------
ggplot(frz_hgt %>% group_by(MONTH)) +
  geom_boxplot(aes(x = month(date, label = T), y = FRZHGT)) +
  stat_summary(aes(x = month(date), y = FRZHGT), 
               fun = mean, geom = "path", color = "red") +
  scale_y_continuous(limits = c(NA, 6000)) +
  labs(title = "Full Dataset (1967 - 2021) by Month - Manaus (AERO)", 
       x = "Month", y = "Freezing Level Height (m)")
ggsave("general_processing/figs/igra2_full_dataset.png", 
       dpi = 300, width = 6, height = 4)

# Boxplot of climatologies per month -------------------------------------------
ggplot(frz_hgt %>% group_by(MONTH) %>% filter(!is.na(clm))) +
  geom_boxplot(aes(x = month(date, label = T), y = FRZHGT, color = clm)) +
  stat_summary(aes(x = month(date), y = FRZHGT, color = clm), 
               fun = mean, geom = "path") +
  scale_y_continuous(limits = c(NA, 6000)) +
  labs(title = "Climatologies by Month - Manaus (AERO)", 
       x = "Month", y = "Freezing Level Height (m)", color = "Climatology") +
  theme(legend.position = "bottom")
ggsave("general_processing/figs/igra2_climatologies.png", 
       dpi = 300, width = 6, height = 4.5)

# Boxplot of full dataset by month/hour ----------------------------------------
ggplot(frz_hgt %>% filter(HOUR %in% c(0, 11, 12)) %>% group_by(MONTH)) +
  geom_boxplot(aes(x = month(date, label = T), y = FRZHGT, color = HOUR)) +
  stat_summary(aes(x = month(date), y = FRZHGT, color = HOUR),
               fun = mean, geom = "path") +
  scale_y_continuous(limits = c(NA, 6000)) +
  scale_color_manual(values = c("blue", "darkgoldenrod", "darkred"), 
                     labels = c("0000 (6642 values)", "1100 (1122 values)", "1200 (13224 values)")) +
  labs(title = "Full Dataset (1967 - 2021) by Month/Hour - Manaus (AERO)", 
       x = "Month", y = "Freezing Level Height (m)", color = "Hour (UTC)") +
  theme(legend.position = "bottom")
ggsave("general_processing/figs/igra2_full_dataset_byhour.png", 
       dpi = 300, width = 6, height = 4.5)

# Calculating means ------------------------------------------------------------
frz_means <- frz_hgt %>% 
  filter(HOUR %in% c("0", "11", "12")) %>% 
  mutate(HOUR = ifelse(HOUR == "11", "12", HOUR)) %>% 
  mutate(mean_total = mean(FRZHGT, na.rm = T)) %>% 
  group_by(MONTH) %>% 
  mutate(mean_month = mean(FRZHGT, na.rm = T)) %>% 
  ungroup() %>% 
  group_by(HOUR) %>% 
  mutate(mean_hour = mean(FRZHGT, na.rm = T)) %>% 
  ungroup() %>% 
  group_by(MONTH, HOUR) %>% 
  mutate(mean_month_hour = mean(FRZHGT, na.rm = T)) %>% 
  ungroup()
summary(frz_means)

# Plotting means ---------------------------------------------------------------
ggplot(frz_means) +
  geom_density(aes(x = (mean_total - FRZHGT))) +
  geom_density(aes(x = (mean_month - FRZHGT)), color = "red") +
  geom_density(aes(x = (mean_hour - FRZHGT)), color = "blue") +
  geom_density(aes(x = (mean_month_hour - FRZHGT)), color = "forestgreen") +
  annotate("text", x = 700, y = c(0.0020, 0.0019, 0.0018, 0.0017),
           label = c("Média total", "Média mensal", "Média horária", "Média mensal/horária"),
           color = c("black", "red", "blue", "forestgreen")) +
  scale_x_continuous(limits = c(-1000, 1000)) +
  labs(title = "Error of Full Dataset (1967 - 2021) - Manaus (AERO)",
       x = "Mean - Freezing Level Height (m)", y = "Density")
ggsave("general_processing/figs/igra2_density_error.png", dpi = 300,
       width = 6, height = 5)

# ggplot(
#   frz_means %>% 
#     group_by(MONTH) %>% 
#     mutate(ymin = min(FRZHGT, na.rm = T), ymax = max(FRZHGT, na.rm = T))
#   ) +
#   geom_line(aes(x = month(date), y = mean_total)) +
#   geom_errorbar(aes(x = month(date), y = mean_total, ymin = ymin, ymax = ymax))
# 
# ggplot(
#   frz_means %>% 
#     group_by(MONTH) %>% 
#     mutate(ymin = min(FRZHGT, na.rm = T), ymax = max(FRZHGT, na.rm = T))
#   ) +
#   geom_line(aes(x = month(date), y = mean_month)) +
#   geom_errorbar(aes(x = month(date), y = mean_month, ymin = ymin, ymax = ymax))

# Generating freezing height profile -------------------------------------------
frz_hour <- frz_means %>% 
  group_by(HOUR) %>% 
  select(mean_hour) %>% 
  unique()

frz_hour <- tibble(
  hour = 0:23,
  frz_height = c(
    head(seq(frz_hour$mean_hour[2], frz_hour$mean_hour[1], length.out = 13), -1),
    head(seq(frz_hour$mean_hour[1], frz_hour$mean_hour[2], length.out = 13), -1)
  )
)

# Plotting freezing height profile, saving file --------------------------------
ggplot(frz_hour, aes(hour, frz_height)) +
  geom_point() +
  geom_path() +
  labs(title = "Freezing Height Profile by Hour - Manaus (AERO)", x = "Hour", 
       y = "Freezing Height (m)")
ggsave("general_processing/figs/frz_hgt_profile.png", dpi = 300, 
       width = 5, height = 4)
write_csv(frz_hour, "general_processing/frz_hgt_profile.csv")
