# ------------------------------------------------------------------------------
# Loading elevation and shapefile data to create topographic maps
# ------------------------------------------------------------------------------

# Loading library packages -----------------------------------------------------
library(elevatr)
library(tidyverse)
# library(raster)
# library(rasterVis)
# library(rgdal)
library(tabularaster)
library(sf)
library(cptcity)
library(colorspace)
library(ggspatial)
library(ggnewscale)

# Function to draw circle of a given radius ------------------------------------
dfCircle <- function(LonDec, LatDec, Km) {
  # - LatDec = latitude in decimal degrees of the center of the circle
  # - LonDec = longitude in decimal degrees
  # - Km = radius of the circle in kilometers

  # Mean Earth radius in kilometers
  # - Change this to 3959 and you will have your function working in miles
  ER <- 6371
  # Angles in degrees
  AngDeg <- seq(1:360)
  # Latitude of the center of the circle in radians
  Lat1Rad <- LatDec * (pi / 180)
  # Longitude of the center of the circle in radians
  Lon1Rad <- LonDec * (pi / 180)
  # Angles in radians
  AngRad <- AngDeg * (pi / 180)
  # Latitude of each point of the circle rearding to angle in radians
  Lat2Rad <- asin(sin(Lat1Rad) * cos(Km / ER) +
    cos(Lat1Rad) * sin(Km / ER) * cos(AngRad))
  # Longitude of each point of the circle rearding to angle in radians
  Lon2Rad <-
    Lon1Rad + atan2(
      sin(AngRad) * sin(Km / ER) * cos(Lat1Rad),
      cos(Km / ER) - sin(Lat1Rad) * sin(Lat2Rad)
    )
  # Latitude of each point of the circle rearding to angle in radians
  Lat2Deg <- Lat2Rad * (180 / pi)
  # Longitude of each point of the circle rearding to angle in degrees
  # - Conversion of radians to degrees deg = rad*(180/pi)
  Lon2Deg <- Lon2Rad * (180 / pi)
  return(data.frame(lon = Lon2Deg, lat = Lat2Deg))
}

dfLangles <- function(LonDec, LatDec, Km) {
  # - LatDec = latitude in decimal degrees of the center of the circle
  # - LonDec = longitude in decimal degrees
  # - Km = radius of the circle in kilometers
  
  # Mean Earth radius in kilometers
  # - Change this to 3959 and you will have your function working in miles
  ER <- 6371
  # Angles in degrees
  AngDeg <- seq(1,360,90)
  # Latitude of the center of the circle in radians
  Lat1Rad <- LatDec * (pi / 180)
  # Longitude of the center of the circle in radians
  Lon1Rad <- LonDec * (pi / 180)
  # Angles in radians
  AngRad <- AngDeg * (pi / 180)
  # Latitude of each point of the circle rearding to angle in radians
  Lat2Rad <- asin(sin(Lat1Rad) * cos(Km / ER) +
                    cos(Lat1Rad) * sin(Km / ER) * cos(AngRad))
  # Longitude of each point of the circle rearding to angle in radians
  Lon2Rad <-
    Lon1Rad + atan2(
      sin(AngRad) * sin(Km / ER) * cos(Lat1Rad),
      cos(Km / ER) - sin(Lat1Rad) * sin(Lat2Rad)
    )
  # Latitude of each point of the circle rearding to angle in radians
  Lat2Deg <- Lat2Rad * (180 / pi)
  # Longitude of each point of the circle rearding to angle in degrees
  # - Conversion of radians to degrees deg = rad*(180/pi)
  Lon2Deg <- Lon2Rad * (180 / pi)
  return(data.frame(lon = Lon2Deg, lat = Lat2Deg))
}


# Getting data -----------------------------------------------------------------

# Elevation

# Data frame with coordinates
coords <- data.frame(
  lon = seq(-63, -57, 0.1),
  lat = seq(-6, 0, 0.1)
)
# Projection
prj_dd <- "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"

# Downloading data
# elevs <- get_elev_point(coords, prj = prj_dd, src = "aws") %>% data.frame
elevs <- get_elev_raster(coords, prj = prj_dd, z = 6)

# Converting to tibble
elevs_df <- tabularaster::as_tibble(elevs, cell = F, xy = T) %>%
  drop_na() %>%
  filter(x >= -63 & x <= -57, y >= -6 & y <= 0)
# mutate(cellvalue = ifelse(cellvalue <= 25, NA, cellvalue))
rm(elevs)

# Additional points

# GoAmazon sites and labels
goam_sites <-
  read_csv("data/general/goamazon_sites.csv",
    locale = locale(decimal_mark = ",", grouping_mark = ".")
  ) %>%
  gather(has, answer, c(has_aerosol, has_meteo, has_cloud)) #%>%
  #filter(answer == "yes")
goam_has_labels <-
  c(
    `has_aerosol` = "Aerosols",
    `has_cloud` = "Cloud Properties",
    `has_meteo` = "Meteorology"
  )

# Radars location and range
sipam <- tibble("lon" = -59.992, "lat" = -3.1493)
sipam_ring <- dfCircle(sipam$lon, sipam$lat, 250)
sipam_rect <- dfLangles(sipam$lon, sipam$lat, 150)
xpol <- goam_sites %>%
  filter(goamazon_reference == "T3") %>%
  select(longitude, latitude) %>%
  rename(lon = longitude, lat = latitude) %>%
  unique()
xpol_ring <- dfCircle(xpol$lon, xpol$lat, 60) %>%
  mutate(has = "has_cloud")
xpol$has <- "has_cloud"
# Stations ranges
# TOe_ring_100 <- dfCircle(
#   goam_sites %>% 
#     filter(goamazon_reference == "TOe" & has == "has_aerosol") %>% 
#     select(longitude) %>% 
#     deframe,
#   goam_sites %>% 
#     filter(goamazon_reference == "TOe" & has == "has_aerosol") %>% 
#     select(latitude) %>% 
#     deframe,
#   100)
# TOe_ring_50 <- dfCircle(
#   goam_sites %>% 
#     filter(goamazon_reference == "TOe" & has == "has_aerosol") %>% 
#     select(longitude) %>% 
#     deframe,
#   goam_sites %>% 
#     filter(goamazon_reference == "TOe" & has == "has_aerosol") %>% 
#     select(latitude) %>% 
#     deframe,
#   50)
T3_ring_200 <- dfCircle(
  goam_sites %>% 
    filter(goamazon_reference == "T3" & has == "has_aerosol") %>% 
    select(longitude) %>% 
    deframe,
  goam_sites %>% 
    filter(goamazon_reference == "T3" & has == "has_aerosol") %>% 
    select(latitude) %>% 
    deframe, 
  200)
T3_ring_150 <- dfCircle(
  goam_sites %>% 
    filter(goamazon_reference == "T3" & has == "has_aerosol") %>% 
    select(longitude) %>% 
    deframe,
  goam_sites %>% 
    filter(goamazon_reference == "T3" & has == "has_aerosol") %>% 
    select(latitude) %>% 
    deframe, 
  150)
T3_ring_100 <- dfCircle(
  goam_sites %>% 
    filter(goamazon_reference == "T3" & has == "has_aerosol") %>% 
    select(longitude) %>% 
    deframe,
  goam_sites %>% 
    filter(goamazon_reference == "T3" & has == "has_aerosol") %>% 
    select(latitude) %>% 
    deframe, 
  100)
T3_ring_50 <- dfCircle(
  goam_sites %>% 
    filter(goamazon_reference == "T3" & has == "has_aerosol") %>% 
    select(longitude) %>% 
    deframe,
  goam_sites %>% 
    filter(goamazon_reference == "T3" & has == "has_aerosol") %>% 
    select(latitude) %>% 
    deframe, 
  50)
T1_ring <- dfCircle(
  goam_sites %>% 
    filter(goamazon_reference == "Tl" & has == "has_aerosol") %>% 
    select(longitude) %>% 
    deframe,
  goam_sites %>% 
    filter(goamazon_reference == "Tl" & has == "has_aerosol") %>% 
    select(latitude) %>% 
    deframe, 
  30)

# HYSPLIT trajectories
hysplit_fwd_2014 <- read_csv("./data/hysplit_2014_forward_paths.csv")
hysplit_bwd_2014 <- read_csv("./data/hysplit_2014_backward_paths.csv")
hysplit_bwd_2015 <- read_csv("./data/hysplit_2015_backward_paths.csv")

# Shapefiles
cities <- st_read("data/general/shapefiles/AM_Municipios_2019.shp",
  stringsAsFactors = F
)
rivers <-
  st_read("data/general/shapefiles/ne_10m_rivers_lake_centerlines.shp",
    stringsAsFactors = F
  )

# Plotting ---------------------------------------------------------------------
theme_set(theme_bw())
theme_update(plot.title = element_text(hjust = 0.5))

# Elevation + radar range + GoAmazon points ------------------------------------
ggplot() +
  geom_tile(data = elevs_df, aes(x, y, fill = cellvalue)) +
  geom_sf( #- Cities shapefile
    data = cities,
    fill = NA,
    size = 0.25,
    color = "gray60"
  ) +
  geom_sf( #- Rivers shapefile
    data = rivers,
    fill = NA,
    size = 0.25,
    color = "steelblue"
  ) +
  geom_path( #- SIPAM radar range ring
    data = sipam_ring,
    aes(lon, lat),
    size = 0.8,
    color = "darkred",
    linetype="dashed"
  ) +
  geom_point( #- SIPAM radar location
    data = sipam,
    aes(lon, lat, color = "SIPAM"),
    shape = 17,
    size = 4
  ) +
  geom_rect(  #- SIPAM radar range rect
    aes(xmin = sipam_rect$lon[4], xmax = sipam_rect$lon[2], 
        ymin = sipam_rect$lat[3], ymax = sipam_rect$lat[1]),
    alpha = 0,
    color = "darkred",
    size = 1) +
  # geom_path( #- XPOL radar range ring
  #   data = xpol_ring,
  #   aes(lon, lat),
  #   size = 0.8,
  #   color = "purple4"
  # ) +
  # geom_point( #- XPOL radar location
  #   data = xpol,
  #   aes(lon, lat, color = "XPOL"),
  #   shape = 17,
  #   size = 4
  # ) +
  # geom_path( #- TOe radar range ring
  #   data = TOe_ring_100,
  #   aes(lon, lat),
  #   size = 0.5,
  #   color = "black"
  # ) +  
  # geom_path( #- TOe radar range ring
  #   data = TOe_ring_50,
  #   aes(lon, lat),
  #   size = 0.5,
  #   color = "black"
  # ) +
  # geom_path( #- T3 radar range ring
  #   data = T3_ring_200,
  #   aes(lon, lat),
  #   size = 0.5,
  #   color = "black"
  # ) +
  # geom_path( #- T3 radar range ring
  #   data = T3_ring_150,
  #   aes(lon, lat),
  #   size = 0.5,
  #   color = "black"
  # ) +
  # geom_path( #- T3 radar range ring
  #   data = T3_ring_100,
  #   aes(lon, lat),
  #   size = 0.5,
  #   color = "black"
  # ) +
  # geom_path( #- T3 radar range ring
  #   data = T3_ring_50,
  #   aes(lon, lat),
  #   size = 0.5,
  #   color = "black"
  # ) +
  geom_path( #- T1 radar range ring
    data = T1_ring,
    aes(lon, lat),
    size = 0.5,
    color = "black"
  ) +
  geom_point( #- GoAmazon sites locations
    data = goam_sites %>% filter(goamazon_reference %in% c("T3", "Tl", "T2") & has == "has_aerosol"),
    aes(longitude, latitude),
    shape = 16,
    size = 2
  ) +
  geom_text( #- GoAmazon sites labels
    data = goam_sites %>% filter(goamazon_reference %in% c("T3", "Tl", "T2") & has == "has_aerosol"),
    aes(longitude, latitude, label = goamazon_reference),
    position = position_dodge2(0.25, preserve = "single"),
    vjust = -0.5,
    size = 3.5
  ) +
  # annotation_scale(location = "bl", width_hint = 0.4) +
  coord_sf(
    xlim = c(-62.5, -57.5),
    ylim = c(-5.7, -0.6),
    expand = T
  ) +
  scale_color_manual(
    name = NULL,
    values = c("SIPAM" = "darkred")
  ) +
  scale_fill_stepsn(
    name = "Elevation (m)",
    limits = c(-25, 200),
    colours = c(
      "#1B63C9",
      "#00B9A1",
      "#6DE27C",
      "#FEFE98",
      "#B6A272",
      "#93756E",
      "#DBD1CF",
      "#FFFFFF"
    ),
    breaks = seq(-25, 200, 25)
  ) +
  guides(fill = guide_colorbar(barwidth = 16)) +
  theme(
    legend.position = "bottom",
    axis.title = element_blank(),
    panel.background = element_rect(fill = NA),
    panel.grid = element_line(linetype = "dotted", color = gray(0.5, alpha = 0.2)),
    panel.ontop = TRUE,
    plot.background = element_rect(
      fill = "transparent",
      color = "transparent"
    ),
    legend.background = element_rect(fill = "transparent")
  ) # +
  # facet_grid(cols = vars(has), labeller = as_labeller(goam_has_labels))
ggsave(
  "general_processing/figs/sipam_only_aeronet.png",
  width = 6,
  height = 5.5,
  dpi = 300,
  bg = "transparent"
)

# HYSPLIT forward + radar range + GoAmazon points ------------------------------------
hysplit_fwd_2014 <- hysplit_fwd_2014 %>% 
  mutate(date_month = factor(months(date), levels = unique(months(date))))
ggplot(hysplit_fwd_2014) +
  geom_path( 
    aes(x = lon, y = lat, color = date_hours, group = name)
  ) +
  geom_sf( #- Cities shapefile
    data = cities,
    fill = NA,
    size = 0.25,
    color = "gray60"
  ) +
  geom_sf( #- Rivers shapefile
    data = rivers,
    fill = NA,
    size = 0.25,
    color = "steelblue"
  ) +
  geom_path( #- SIPAM radar range ring
    data = sipam_ring,
    aes(lon, lat),
    size = 0.8,
    color = "darkred",
    linetype="dashed"
  ) +
  geom_point( #- SIPAM radar location
    data = sipam,
    aes(lon, lat),
    color = "darkred",
    shape = 17,
    size = 4
  ) +
  geom_rect(  #- SIPAM radar range rect
    aes(xmin = sipam_rect$lon[4], xmax = sipam_rect$lon[2], 
        ymin = sipam_rect$lat[3], ymax = sipam_rect$lat[1]),
    alpha = 0,
    color = "darkred",
    size = 1) +
  geom_path( #- T3 radar range ring
    data = T3_ring_200,
    aes(lon, lat),
    size = 0.5,
    color = "black"
  ) +
  geom_path( #- T3 radar range ring
    data = T3_ring_150,
    aes(lon, lat),
    size = 0.5,
    color = "black"
  ) +
  geom_path( #- T3 radar range ring
    data = T3_ring_100,
    aes(lon, lat),
    size = 0.5,
    color = "black"
  ) +
  geom_path( #- T3 radar range ring
    data = T3_ring_50,
    aes(lon, lat),
    size = 0.5,
    color = "black"
  ) +
  geom_point( #- GoAmazon sites locations
    data = goam_sites %>% filter(goamazon_reference %in% c("T3") & has == "has_aerosol"),
    aes(longitude, latitude),
    shape = 16,
    size = 2
  ) +
  geom_text( #- GoAmazon sites labels
    data = goam_sites %>% filter(goamazon_reference %in% c("T3") & has == "has_aerosol"),
    aes(longitude, latitude, label = goamazon_reference),
    position = position_dodge2(0.25, preserve = "single"),
    vjust = -0.5,
    size = 3.5
  ) +
  # annotation_scale(location = "bl", width_hint = 0.4) +
  coord_sf(
    xlim = c(-62.5, -57.5),
    ylim = c(-5.7, -0.6),
    expand = T
  ) +
  scale_color_continuous_sequential(
    palette = "rocket", rev = T, name = "Hours"
  ) +
  guides(color = guide_colorbar(barwidth = 16)) +
  theme(
    legend.position = "bottom",
    axis.title = element_blank(),
    panel.background = element_rect(fill = NA),
    panel.grid = element_line(linetype = "dotted", color = gray(0.5, alpha = 0.2)),
    panel.ontop = TRUE,
    plot.background = element_rect(
      fill = "transparent",
      color = "transparent"
    ),
    legend.background = element_rect(fill = "transparent")
  ) +
  facet_wrap(vars(date_month), ncol = 3)
ggsave(
  "general_processing/figs/sipam_hysplit_fwd_2014.png",
  width = 6,
  height = 10,
  dpi = 300,
  bg = "transparent"
)
# HYSPLIT backward 2014 + radar range + GoAmazon points ------------------------------------
month_names <- c("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
hysplit_bwd_2014 <- hysplit_bwd_2014 %>% 
  mutate(date_month = factor(months(date), levels = month_names))
ggplot(hysplit_bwd_2014) +
  geom_path( 
    aes(x = lon, y = lat, color = date_hours, group = name)
  ) +
  geom_sf( #- Cities shapefile
    data = cities,
    fill = NA,
    size = 0.25,
    color = "gray60"
  ) +
  geom_sf( #- Rivers shapefile
    data = rivers,
    fill = NA,
    size = 0.25,
    color = "steelblue"
  ) +
  geom_path( #- SIPAM radar range ring
    data = sipam_ring,
    aes(lon, lat),
    size = 0.8,
    color = "darkred",
    linetype="dashed"
  ) +
  geom_point( #- SIPAM radar location
    data = sipam,
    aes(lon, lat),
    color = "darkred",
    shape = 17,
    size = 4
  ) +
  geom_rect(  #- SIPAM radar range rect
    aes(xmin = sipam_rect$lon[4], xmax = sipam_rect$lon[2], 
        ymin = sipam_rect$lat[3], ymax = sipam_rect$lat[1]),
    alpha = 0,
    color = "darkred",
    size = 1) +
  geom_path( #- T3 radar range ring
    data = T3_ring_200,
    aes(lon, lat),
    size = 0.5,
    color = "black"
  ) +
  geom_path( #- T3 radar range ring
    data = T3_ring_150,
    aes(lon, lat),
    size = 0.5,
    color = "black"
  ) +
  geom_path( #- T3 radar range ring
    data = T3_ring_100,
    aes(lon, lat),
    size = 0.5,
    color = "black"
  ) +
  geom_path( #- T3 radar range ring
    data = T3_ring_50,
    aes(lon, lat),
    size = 0.5,
    color = "black"
  ) +
  geom_point( #- GoAmazon sites locations
    data = goam_sites %>% filter(goamazon_reference %in% c("T3") & has == "has_aerosol"),
    aes(longitude, latitude),
    shape = 16,
    size = 2
  ) +
  geom_text( #- GoAmazon sites labels
    data = goam_sites %>% filter(goamazon_reference %in% c("T3") & has == "has_aerosol"),
    aes(longitude, latitude, label = goamazon_reference),
    position = position_dodge2(0.25, preserve = "single"),
    vjust = -0.5,
    size = 3.5
  ) +
  # annotation_scale(location = "bl", width_hint = 0.4) +
  coord_sf(
    xlim = c(-62.5, -57.5),
    ylim = c(-5.7, -0.6),
    expand = T
  ) +
  scale_color_continuous_sequential(
    palette = "rocket", rev = T, name = "Hours"
  ) +
  guides(color = guide_colorbar(barwidth = 16)) +
  theme(
    legend.position = "bottom",
    axis.title = element_blank(),
    panel.background = element_rect(fill = NA),
    panel.grid = element_line(linetype = "dotted", color = gray(0.5, alpha = 0.2)),
    panel.ontop = TRUE,
    plot.background = element_rect(
      fill = "transparent",
      color = "transparent"
    ),
    legend.background = element_rect(fill = "transparent")
  ) +
  facet_wrap(vars(date_month), ncol = 3)
ggsave(
  "general_processing/figs/sipam_hysplit_bwd_2014.png",
  width = 6,
  height = 10,
  dpi = 300,
  bg = "transparent"
)
# HYSPLIT backward 2015 + radar range + GoAmazon points ------------------------------------
hysplit_bwd_2015 <- hysplit_bwd_2015 %>% 
  mutate(date_month = factor(months(date), levels = month_names))
ggplot(hysplit_bwd_2015) +
  geom_path( 
    aes(x = lon, y = lat, color = date_hours, group = name)
  ) +
  geom_sf( #- Cities shapefile
    data = cities,
    fill = NA,
    size = 0.25,
    color = "gray60"
  ) +
  geom_sf( #- Rivers shapefile
    data = rivers,
    fill = NA,
    size = 0.25,
    color = "steelblue"
  ) +
  geom_path( #- SIPAM radar range ring
    data = sipam_ring,
    aes(lon, lat),
    size = 0.8,
    color = "darkred",
    linetype="dashed"
  ) +
  geom_point( #- SIPAM radar location
    data = sipam,
    aes(lon, lat),
    color = "darkred",
    shape = 17,
    size = 4
  ) +
  geom_rect(  #- SIPAM radar range rect
    aes(xmin = sipam_rect$lon[4], xmax = sipam_rect$lon[2], 
        ymin = sipam_rect$lat[3], ymax = sipam_rect$lat[1]),
    alpha = 0,
    color = "darkred",
    size = 1) +
  geom_path( #- T3 radar range ring
    data = T3_ring_200,
    aes(lon, lat),
    size = 0.5,
    color = "black"
  ) +
  geom_path( #- T3 radar range ring
    data = T3_ring_150,
    aes(lon, lat),
    size = 0.5,
    color = "black"
  ) +
  geom_path( #- T3 radar range ring
    data = T3_ring_100,
    aes(lon, lat),
    size = 0.5,
    color = "black"
  ) +
  geom_path( #- T3 radar range ring
    data = T3_ring_50,
    aes(lon, lat),
    size = 0.5,
    color = "black"
  ) +
  geom_point( #- GoAmazon sites locations
    data = goam_sites %>% filter(goamazon_reference %in% c("T3") & has == "has_aerosol"),
    aes(longitude, latitude),
    shape = 16,
    size = 2
  ) +
  geom_text( #- GoAmazon sites labels
    data = goam_sites %>% filter(goamazon_reference %in% c("T3") & has == "has_aerosol"),
    aes(longitude, latitude, label = goamazon_reference),
    position = position_dodge2(0.25, preserve = "single"),
    vjust = -0.5,
    size = 3.5
  ) +
  # annotation_scale(location = "bl", width_hint = 0.4) +
  coord_sf(
    xlim = c(-62.5, -57.5),
    ylim = c(-5.7, -0.6),
    expand = T
  ) +
  scale_color_continuous_sequential(
    palette = "rocket", rev = T, name = "Hours"
  ) +
  guides(color = guide_colorbar(barwidth = 16)) +
  theme(
    legend.position = "bottom",
    axis.title = element_blank(),
    panel.background = element_rect(fill = NA),
    panel.grid = element_line(linetype = "dotted", color = gray(0.5, alpha = 0.2)),
    panel.ontop = TRUE,
    plot.background = element_rect(
      fill = "transparent",
      color = "transparent"
    ),
    legend.background = element_rect(fill = "transparent")
  ) +
  facet_wrap(vars(date_month), ncol = 3)
ggsave(
  "general_processing/figs/sipam_hysplit_bwd_2015.png",
  width = 6,
  height = 10,
  dpi = 300,
  bg = "transparent"
)
