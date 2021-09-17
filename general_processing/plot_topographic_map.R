# Loading library packages -----------------------------------------------

library(elevatr)
library(tidyverse)
# library(raster)
# library(rasterVis)
# library(rgdal)
library(tabularaster)
library(sf)
# library(cptcity)
library(colorspace)
library(ggspatial)
library(ggnewscale)


# Function definition -----------------------------------------------------

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
    Lon1Rad + atan2(sin(AngRad) * sin(Km / ER) * cos(Lat1Rad),
                    cos(Km / ER) - sin(Lat1Rad) * sin(Lat2Rad))
  # Latitude of each point of the circle rearding to angle in radians
  Lat2Deg <- Lat2Rad * (180 / pi)
  # Longitude of each point of the circle rearding to angle in degrees
  # - Conversion of radians to degrees deg = rad*(180/pi)
  Lon2Deg <- Lon2Rad * (180 / pi)
  return(data.frame(lon = Lon2Deg, lat = Lat2Deg))
}


# Getting data ------------------------------------------------------------

# Elevations

# Data frame with coordinates
coords <- data.frame(lon = seq(-63, -57, 0.1),
                     lat = seq(-6, 0, 0.1))
# Projection
prj_dd <- "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"

# Getting data
# elevs <- get_elev_point(coords, prj = prj_dd, src = "aws") %>% data.frame
elevs <- get_elev_raster(coords, prj = prj_dd, z = 6)

# Converting to tibble
elevs_df <- tabularaster::as_tibble(elevs, cell = F, xy = T) %>%
  drop_na %>%
  filter(x >= -63 & x <= -57, y >= -6 & y <= 0) %>%
  mutate(cellvalue = ifelse(cellvalue < 0, NA, cellvalue))
rm(elevs)

# Radar, stations position
goam_sites <-
  read_csv("data/general/goamazon_sites.csv",
           locale = locale(decimal_mark = ",", grouping_mark = ".")) %>%
  gather(has, answer, c(has_aerosol, has_meteo, has_cloud)) %>%
  filter(answer == "yes")
goam_has_labels <-
  c(
    `has_aerosol` = "Aerosols",
    `has_cloud` = "Cloud Properties",
    `has_meteo` = "Meteorology"
  )
sipam <- tibble("lon" = -59.992, "lat" = -3.1493)
sipam_ring <- dfCircle(sipam$lon, sipam$lat, 150)

# Shapefiles
cities <- st_read("data/general/shapefiles/AM_Municipios_2019.shp",
                  stringsAsFactors = F)
rivers <-
  st_read("data/general/shapefiles/ne_10m_rivers_lake_centerlines.shp",
          stringsAsFactors = F)

# Plotting ----------------------------------------------------------------

theme_set(theme_bw())
theme_update(plot.title = element_text(hjust = 0.5))

# Elevation + radar range + GoAmazon points
ggplot() +
  geom_tile(data = elevs_df, aes(x, y, fill = cellvalue)) +
  geom_sf(
    data = cities,
    fill = NA,
    size = 0.25,
    color = "gray"
  ) +
  geom_sf(
    data = rivers,
    fill = NA,
    size = 0.4,
    color = "lightblue"
  ) +
  geom_path(data = sipam_ring,
            aes(lon, lat),
            size = 1,
            color = "darkred") +
  geom_point(
    data = sipam,
    aes(lon, lat),
    color = "darkred",
    shape = 17,
    size = 4
  ) +
  geom_point(
    data = goam_sites,
    aes(longitude, latitude),
    shape = 16,
    size = 2
  ) +
  geom_text(
    data = goam_sites,
    aes(longitude, latitude, label = goamazon_reference),
    position = position_dodge2(0.25, preserve = "single"),
    vjust = -0.5,
    size = 3.5
  ) +
  # annotation_scale(location = "bl", width_hint = 0.4) +
  coord_sf(
    xlim = c(-61.343496, -58.640505),
    ylim = c(-4.505793, -1.792021),
    expand = F
  ) +
  scale_fill_continuous_sequential(
    name = "Elevation (m)",
    limits = c(0, 500),
    palette = "terrain2",
    rev = F,
    na.value = "mediumaquamarine"
  ) +
  guides(fill = guide_colorbar(barwidth = 10)) +
  theme(
    legend.position = "bottom",
    axis.title = element_blank(),
    panel.background = element_rect(fill = NA),
    panel.grid = element_line(linetype = "dotted", color = gray(0.5, alpha = 0.2)),
    panel.ontop = TRUE,
    plot.background = element_rect(fill = "transparent",
                                   color = "transparent"),
    legend.background = element_rect(fill = "transparent")
  ) +
  facet_grid(cols = vars(has), labeller = as_labeller(goam_has_labels))
ggsave(
  "general_processing/figs/sipam_data_points.png",
  width = 7.5,
  height = 3.5,
  dpi = 300,
  bg = "transparent"
)
