library(readr)
library(tidyverse)
library(lubridate)

aeronet_t3_l15 <- read_csv("data/aerosol/aeronet/T3/20140101_20151231_ARM_Manacapuru.lev15", 
                               col_types = cols(`Date(dd:mm:yyyy)` = col_date(format = "%d:%m:%Y"), 
                                                `Time(hh:mm:ss)` = col_time(format = "%H:%M:%S"), 
                                                `Last_Date_Processed` = col_date(format = "%d:%m:%Y")), 
                               skip = 6, na = c("-999.000000", "-999."),
                               name_repair = "minimal")
aeronet_t3_l15 <- aeronet_t3_l15[!duplicated(as.list(aeronet_t3_l15))] %>% 
  mutate(date = ymd_hms(paste(`Date(dd:mm:yyyy)`, `Time(hh:mm:ss)`, sep = " ")))
aeronet_t0e_l15 <- read_csv("data/aerosol/aeronet/T0e/20140101_20151231_Manaus_EMBRAPA.lev15", 
                           col_types = cols(`Date(dd:mm:yyyy)` = col_date(format = "%d:%m:%Y"), 
                                            `Time(hh:mm:ss)` = col_time(format = "%H:%M:%S"), 
                                            `Last_Date_Processed` = col_date(format = "%d:%m:%Y")), 
                           skip = 6, na = c("-999.000000", "-999."),
                           name_repair = "minimal")
aeronet_t0e_l15 <- aeronet_t0e_l15[!duplicated(as.list(aeronet_t0e_l15))] %>% 
  mutate(date = ymd_hms(paste(`Date(dd:mm:yyyy)`, `Time(hh:mm:ss)`, sep = " ")))
aeronet_l15 <- bind_rows(aeronet_t3_l15, aeronet_t0e_l15)
remove(aeronet_t3_l15, aeronet_t0e_l15)

aeronet_t3_l15_tot <- read_csv("data/aerosol/aeronet/T3/20140101_20151231_ARM_Manacapuru.tot_lev15", 
                           col_types = cols(`Date(dd:mm:yyyy)` = col_date(format = "%d:%m:%Y"), 
                                            `Time(hh:mm:ss)` = col_time(format = "%H:%M:%S"), 
                                            `Last_Date_Processed` = col_date(format = "%d:%m:%Y")), 
                           skip = 6, na = c("-999.000000", "-999."),
                           name_repair = "minimal")
aeronet_t3_l15_tot <- aeronet_t3_l15_tot[!duplicated(as.list(aeronet_t3_l15_tot))] %>% 
  # select("Date(dd:mm:yyyy)", "Time(hh:mm:ss)", "Data_Quality_Level", 
  #        "AERONET_Instrument_Number", "AERONET_Site_Name", "Site_Latitude(Degrees)",
  #        "Site_Longitude(Degrees)", "Site_Elevation(m)", "AOD_500nm-Total", "AOD_500nm-AOD",
  #        "AOD_500nm-Rayleigh", "AOD_500nm-O3", "AOD_500nm-NO2", "AOD_500nm-CO2",
  #        "AOD_500nm-CH4", "AOD_500nm-WaterVapor") %>% 
  mutate(date = ymd_hms(paste(`Date(dd:mm:yyyy)`, `Time(hh:mm:ss)`, sep = " ")))
aeronet_t0e_l15_tot <- read_csv("data/aerosol/aeronet/T0e/20140101_20151231_Manaus_EMBRAPA.tot_lev15", 
                               col_types = cols(`Date(dd:mm:yyyy)` = col_date(format = "%d:%m:%Y"), 
                                                `Time(hh:mm:ss)` = col_time(format = "%H:%M:%S"), 
                                                `Last_Date_Processed` = col_date(format = "%d:%m:%Y")), 
                               skip = 6, na = c("-999.000000", "-999."),
                               name_repair = "minimal")
aeronet_t0e_l15_tot <- aeronet_t0e_l15_tot[!duplicated(as.list(aeronet_t0e_l15_tot))] %>% 
  # select("Date(dd:mm:yyyy)", "Time(hh:mm:ss)", "Data_Quality_Level", 
  #        "AERONET_Instrument_Number", "AERONET_Site_Name", "Site_Latitude(Degrees)",
  #        "Site_Longitude(Degrees)", "Site_Elevation(m)", "AOD_500nm-Total", "AOD_500nm-AOD",
  #        "AOD_500nm-Rayleigh", "AOD_500nm-O3", "AOD_500nm-NO2", "AOD_500nm-CO2",
  #        "AOD_500nm-CH4", "AOD_500nm-WaterVapor") %>% 
  mutate(date = ymd_hms(paste(`Date(dd:mm:yyyy)`, `Time(hh:mm:ss)`, sep = " ")))
aeronet_l15_tot <- bind_rows(aeronet_t3_l15_tot, aeronet_t0e_l15_tot)
remove(aeronet_t3_l15_tot, aeronet_t0e_l15_tot)

aeronet_t3_l15_oneill <- read_csv("data/aerosol/aeronet/T3/20140101_20151231_ARM_Manacapuru.ONEILL_lev15", 
                           col_types = cols(`Date_(dd:mm:yyyy)` = col_date(format = "%d:%m:%Y"), 
                                            `Time_(hh:mm:ss)` = col_time(format = "%H:%M:%S"), 
                                            `Last_Processing_Date` = col_date(format = "%d:%m:%Y")), 
                           skip = 6, na = c("-999.000000", "-999."),
                           name_repair = "minimal")
aeronet_t3_l15_oneill <- aeronet_t3_l15_oneill[!duplicated(as.list(aeronet_t3_l15_oneill))] %>% 
  mutate(date = ymd_hms(paste(`Date_(dd:mm:yyyy)`, `Time_(hh:mm:ss)`, sep = " ")))
aeronet_t0e_l15_oneill <- read_csv("data/aerosol/aeronet/T0e/20140101_20151231_Manaus_EMBRAPA.ONEILL_lev15", 
                                   col_types = cols(`Date_(dd:mm:yyyy)` = col_date(format = "%d:%m:%Y"), 
                                                    `Time_(hh:mm:ss)` = col_time(format = "%H:%M:%S"), 
                                                    `Last_Processing_Date` = col_date(format = "%d:%m:%Y")), 
                                   skip = 6, na = c("-999.000000", "-999."),
                                   name_repair = "minimal")
aeronet_t0e_l15_oneill <- aeronet_t0e_l15_oneill[!duplicated(as.list(aeronet_t0e_l15_oneill))] %>% 
  mutate(date = ymd_hms(paste(`Date_(dd:mm:yyyy)`, `Time_(hh:mm:ss)`, sep = " ")))
aeronet_l15_oneill <- bind_rows(aeronet_t3_l15_oneill, aeronet_t0e_l15_oneill)
remove(aeronet_t3_l15_oneill, aeronet_t0e_l15_oneill)

ggplot(aeronet_l15) +
  geom_point(aes(x = date, y = `AOD_500nm`), pch = 1) +
  scale_x_datetime(date_breaks = "3 month", date_minor_breaks = "1 month") +
  facet_grid(rows = "AERONET_Site_Name")
ggsave("met_aerosol_processing/figs/AERONET_AOD_500.png", 
       width = 7, height = 5, dpi = 300)

ggplot(aeronet_l15) +
  geom_point(aes(x = date, y = `500-870_Angstrom_Exponent`), pch = 1) +
  scale_x_datetime(date_breaks = "3 month", date_minor_breaks = "1 month") +
  facet_grid(rows = "AERONET_Site_Name")
ggsave("met_aerosol_processing/figs/AERONET_AE_500-870.png", 
       width = 7, height = 5, dpi = 300)

# ggplot(aeronet_t3_l15) +
#   geom_point(aes(x = date, y = `Precipitable_Water(cm)`), pch = 1)

ggplot(aeronet_l15_tot) +
  geom_point(aes(x = date, y = `AOD_500nm-AOD`), pch = 1) +
  scale_x_datetime(date_breaks = "3 month", date_minor_breaks = "1 month") +
  facet_grid(rows = "AERONET_Site_Name")
ggsave("met_aerosol_processing/figs/AERONET_AOD_500_tot.png", 
       width = 7, height = 5, dpi = 300)

ggplot(aeronet_l15_oneill) +
  geom_point(aes(x = date, y = `Total_AOD_500nm[tau_a]`), pch = 1) +
  geom_point(aes(x = date, y = `Fine_Mode_AOD_500nm[tau_f]`), pch = 1, color = "darkred") +
  geom_point(aes(x = date, y = `Coarse_Mode_AOD_500nm[tau_c]`), pch = 1, color = "darkblue") +
  annotate(geom = "text", x = as_datetime("2014-03-01 12:00:00"), y = 2, 
           label = 'bold("Total")', parse = T) +
  annotate(geom = "text", x = as_datetime("2014-03-01 12:00:00"), y = 1.8, 
           label = 'bold("Fine Mode")', parse = T, color = "darkred") +
  annotate(geom = "text", x = as_datetime("2014-03-01 12:00:00"), y = 1.6, 
           label = 'bold("Coarse Mode")', parse = T, color = "darkblue") +
  scale_x_datetime(date_breaks = "3 month", date_minor_breaks = "1 month") +
  facet_grid(rows = "AERONET_Site_Name")
ggsave("met_aerosol_processing/figs/AERONET_AOD_Fine_Coarse_500.png", 
       width = 7, height = 5, dpi = 300)

ggplot(aeronet_l15_oneill) +
  geom_point(aes(x = date, y = `Angstrom_Exponent(AE)-Total_500nm[alpha]`), pch = 1) +
  geom_point(aes(x = date, y = `AE-Fine_Mode_500nm[alpha_f]`), pch = 1, color = "darkred") +
  annotate(geom = "text", x = as_datetime("2014-03-01 12:00:00"), y = 3.9, 
         label = 'bold("Total")', parse = T) +
  annotate(geom = "text", x = as_datetime("2014-03-01 12:00:00"), y = 3.5, 
           label = 'bold("Fine Mode")', parse = T, color = "darkred") +
  scale_x_datetime(date_breaks = "3 month", date_minor_breaks = "1 month") +
  facet_grid(rows = "AERONET_Site_Name")
ggsave("met_aerosol_processing/figs/AERONET_AE_Tot_Fine_500.png", 
       width = 7, height = 5, dpi = 300)
