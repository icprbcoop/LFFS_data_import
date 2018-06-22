location <- "D://shiny/"
archive_directory1 <- paste0(location, "FEWS_outputs/archive/")
gdrive_folder <- "lffs_demand_archives"
link <- "https://icprbcoop.org/drupal4/products/coop_pot_withdrawals.csv"
demand_filename <- paste0(archive_directory1, "demand", format(Sys.time(), "_%Y%m%d_%H"), ".csv")

X <- read.csv(url(link), skip=10, sep=",")
write.csv(X, file=demand_filename)

demand_filename1 <- "wma_demand.csv"
write.csv(X, file=demand_filename1)
a <- drive_upload(demand_filename1, gdrive_folder, demand_filename1)
