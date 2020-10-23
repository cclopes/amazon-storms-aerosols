# Loading required packages -----------------------------------------------

require(elevatr)
require(tidyverse)
# require(raster)
# require(rasterVis)
# require(rgdal)
require(tabularaster)
require(sf)
# require(cptcity)
require(colorspace)
require(ggspatial)
require(ggnewscale)


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
  Lat1Rad <- LatDec * (pi/180)
  # Longitude of the center of the circle in radians
  Lon1Rad <- LonDec * (pi/180)
  # Angles in radians
  AngRad <- AngDeg * (pi/180)
  # Latitude of each point of the circle rearding to angle in radians
  Lat2Rad <-asin(sin(Lat1Rad) * cos(Km/ER) +
                   cos(Lat1Rad) * sin(Km/ER) * cos(AngRad))
  # Longitude of each point of the circle rearding to angle in radians
  Lon2Rad <- Lon1Rad + atan2(sin(AngRad) * sin(Km/ER) * cos(Lat1Rad),
                             cos(Km/ER) - sin(Lat1Rad) * sin(Lat2Rad))
  # Latitude of each point of the circle rearding to angle in radians
  Lat2Deg <- Lat2Rad * (180/pi)
  # Longitude of each point of the circle rearding to angle in degrees
  # - Conversion of radians to degrees deg = rad*(180/pi)
  Lon2Deg <- Lon2Rad * (180/pi)
  return(data.frame(lon = Lon2Deg, lat = Lat2Deg))
}


# Getting data ------------------------------------------------------------

# Elevations

# Data frame with coordinates
coords <- data.frame(lon = seq(-65, -55, 0.1), 
                     lat = seq(-7, 3, 0.1))
# Projection
prj_dd <- "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"

# Getting data
# elevs <- get_elev_point(coords, prj = prj_dd, src = "aws") %>% data.frame
elevs <- get_elev_raster(coords, prj = prj_dd, z = 5)

# Converting to tibble
elevs_df <- tabularaster::as_tibble(elevs, cell = F, xy = T) %>% 
  drop_na %>% 
  filter(x >= -65 & x <= -55, y >= -7 & y <= 3) %>%
  mutate(cellvalue = ifelse(cellvalue < 0, NA, cellvalue))
rm(elevs)

# Radars, hailpads position

# st_layers("Data/GENERAL/radar_coverages.kml")
# radars <- st_read("Data/GENERAL/radars_pos.kml", stringsAsFactors = F)
# radars <- cbind(radars$Name, st_coordinates(radars)[,-3]) %>% 
#   data.frame %>% 
#   mutate(X = as.numeric(as.character(X)), Y = as.numeric(as.character(Y)))
# radars_circles <- rbind(
#   radars %>% 
#     filter(V1 != "XPOL") %>% 
#     group_by(V1) %>% nest %>% 
#     mutate(circle_250 = map(data, ~dfCircle(.x$X, .x$Y, 250)),
#            circle_100 = map(data, ~dfCircle(.x$X, .x$Y, 100)),
#            circle_80 = map(data, ~dfCircle(factor(.x$X), factor(.x$Y), 80)),
#            circle_60 = map(data, ~dfCircle(factor(.x$X), factor(.x$Y), 60))) %>% 
#     unnest(cols = c(data, circle_250, circle_100, circle_80, circle_60), 
#            names_sep = "_") %>% 
#     ungroup,
#   radars %>% 
#     filter(V1 == "XPOL") %>% 
#     group_by(V1) %>% nest %>% 
#     mutate(circle_250 = map(data, ~dfCircle(factor(.x$X), factor(.x$Y), 250)),
#            circle_100 = map(data, ~dfCircle(factor(.x$X), factor(.x$Y), 100)),
#            circle_80 = map(data, ~dfCircle(.x$X, .x$Y, 80)),
#            circle_60 = map(data, ~dfCircle(.x$X, .x$Y, 60))) %>% 
#     unnest(cols = c(data, circle_250, circle_100, circle_80, circle_60), 
#            names_sep = "_") %>% 
#     ungroup
# ) %>% 
#   rename(radar = V1, lon = data_X, lat = data_Y)
# select(V1, data_X, data_Y, circle_100_lat, circle_100_lon) %>% 
# pivot_longer(cols = ends_with("lon"), 
#              names_to = "var_lon", values_to = "lon") %>% 
# pivot_longer(cols = ends_with("lat"), 
#              names_to = "var_lat", values_to = "lat") %>% 
# mutate_at(vars(matches("var_l\\w\\w")), 
#           funs(str_remove(., "_l\\w\\w")))

# Shapefiles

states <- st_read("data/general/shapefiles/ne_10m_admin_1_states_provinces.shp",
                  stringsAsFactors = F)
st_crs(states) <- 4326


# Plotting ----------------------------------------------------------------

theme_set(theme_bw())
theme_update(plot.title = element_text(hjust = 0.5))

# Radar ranges
ggplot() +
  geom_tile(data = elevs_df, aes(x, y, fill = cellvalue)) +
  geom_sf(data = states, fill = NA, size = 0.25) +
  # geom_path(data = radars_circles, size = 1,
  #           aes(circle_250_lon, circle_250_lat, color = radar, linetype = "250")) +
  # geom_path(data = radars_circles, size = 1,
  #           aes(circle_100_lon, circle_100_lat, color = radar, linetype = "100")) +
  # geom_path(data = radars_circles, size = 1,
  #           aes(circle_80_lon, circle_80_lat, color = radar, linetype = "80")) +
  # geom_path(data = radars_circles, size = 1,
  #           aes(circle_60_lon, circle_60_lat, color = radar, linetype = "60")) +
  # geom_point(data = radars_circles, aes(lon, lat, color = radar), 
  #            shape = 17, size = 2) +
  # annotation_scale(location = "bl", width_hint = 0.4) +
  # annotation_north_arrow(location = "bl", which_north = "true", 
  #                        pad_x = unit(0.2, "in"), pad_y = unit(0.2, "in"),
  #                        style = north_arrow_fancy_orienteering) +
			

  coord_sf(xlim = c(-62.1561, -57.8267), ylim = c(-5.30485, -0.991217), expand = F) +
  scale_fill_continuous_sequential(name = "Elevation (m)",
                                   palette = "terrain2", rev = F,
                                   na.value = "mediumaquamarine") +
  # scale_color_manual(name = "Radar",
  #                    values = c("#e41a1c", "#3D3308", "#352C51")) +
  # scale_linetype_manual(name = "Radius (km)",
  #                       breaks = c("250", "100", "80", "60"),
  #                       values = c(41, 11, "solid", 3111)) +
  guides(fill = guide_colorbar(reverse = T, order = 1)) +# ,
         # color = guide_legend(order = 2),
         # size = guide_legend(order = 3)) +
  theme(axis.title = element_blank(),
        legend.spacing.y = unit(0.075, "cm"),
        panel.background = element_rect(fill = NA), 
        panel.grid = element_line(
          linetype = "dotted", color = gray(0.5, alpha = 0.2)), 
        panel.ontop = TRUE,
        plot.background = element_rect(fill = "transparent", 
                                       color = "transparent"),
        legend.background = element_rect(fill = "transparent"))
ggsave("radar_coverages.png",
       width = 6, height = 4, dpi = 300, bg = "transparent")
