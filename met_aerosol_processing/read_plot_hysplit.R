library(readr)
library(tidyverse)
library(lubridate)
library(sf)
library(colorspace)
library(purrr)

# Getting files
data_path <- "/data2/camilacl/git/amazon-storms-aerosols/data/aerosol/hysplit/gdas0p5/forward/T3/"
data_files <- paste0(data_path, list.files(data_path))
data_names <- list.files(data_path) %>% str_remove(pattern = "_forward.dat.T3")

# Since files line distribution changes, defining the line to cut from
limit <- "     8 PRESSURE THETA    AIR_TEMP RAINFALL MIXDEPTH RELHUMID TERR_MSL SUN_FLUX"

# Function to read a single file
read_hysplit <- function(data_file, data_name, max_hours){
  lines <- readLines(data_file)
  print(paste("doing", data_name))
  
  return(
    read_table(data_file, col_names = FALSE, skip = grep(limit, lines), col_types = cols()) %>% 
      select(c("X3", "X4", "X5", "X6", "X7", "X10", "X11")) %>% 
      mutate(date = as_datetime(paste0("20", X3, "-", X4, "-", X5, "-", X6, "-", X7), format = "%Y-%m-%d-%H-%M")) %>% 
      rename(lat = X10, lon = X11) %>% 
      select(date, lon, lat) %>% 
      mutate(date_hours = interval(date[1], date)/hours(1), name = data_name) %>% 
      filter(if(max_hours > 0) date_hours <= max_hours else date_hours >= max_hours)
  )

}

# Applying read function to all files (takes a long time)
hysplit_fwd <- map2_dfr(data_files, data_names, ~read_hysplit(.x, .y, 12))

# Saving to a csv file
write_csv(hysplit_fwd, "./data/hysplit_2014_forward_paths.csv")

# Getting files - bwd 2014
data_path <- "/data2/camilacl/git/amazon-storms-aerosols/data/aerosol/hysplit/hysplit_goam0p5_12min_backward_T3_2014/T3/"
data_files <- paste0(data_path, list.files(data_path))
data_names <- list.files(data_path) %>% str_remove(pattern = "_backward.dat.T3")

# Applying read function to all files (takes a long time)
hysplit_bwd_2014 <- map2_dfr(data_files, data_names, ~read_hysplit(.x, .y, -12))

# Saving to a csv file
write_csv(hysplit_bwd_2014, "./data/hysplit_2014_backward_paths.csv")

# Getting files - bwd 2015
data_path <- "/data2/camilacl/git/amazon-storms-aerosols/data/aerosol/hysplit/hysplit_goam0p5_12min_backward_T3_2015/T3/"
data_files <- paste0(data_path, list.files(data_path))
data_names <- list.files(data_path) %>% str_remove(pattern = "_backward.dat.T3")

# Applying read function to all files (takes a long time)
hysplit_bwd_2015 <- map2_dfr(data_files, data_names, ~read_hysplit(.x, .y, -12))

# Saving to a csv file
write_csv(hysplit_bwd_2015, "./data/hysplit_2015_backward_paths.csv")

# Example plot (takes some time)
ggplot(hysplit_fwd) +
  geom_path(aes(x = lon, y = lat, color = date_hours, group = name)) + 
  coord_sf(
    xlim = c(-62.5, -57.5),
    ylim = c(-5.7, -0.6),
    expand = T
  ) +
  scale_color_continuous_sequential(
    palette = "rocket", rev = T
  ) 
