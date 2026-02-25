#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
input_path <- if (length(args) >= 1) args[[1]] else "/Users/yoavram/Downloads/life_table_data/malddaba_life_table.Rdata"
output_dir <- if (length(args) >= 2) args[[2]] else "data"
species_name <- if (length(args) >= 3) args[[3]] else "Orcinus_orca"

if (!file.exists(input_path)) {
  stop(sprintf("Input file not found: %s", input_path))
}

load(input_path)

if (!exists("result_list")) {
  stop("Expected object `result_list` in input Rdata")
}

species_values <- vapply(
  result_list,
  function(x) as.character(x$species$Species)[1],
  character(1)
)

idx <- which(species_values == species_name)
if (length(idx) == 0) {
  stop(sprintf("Species `%s` not found in result_list", species_name))
}

orca <- result_list[[idx[[1]]]]

required_tables <- c("life_table", "demographic_metric", "data_used")
missing_tables <- setdiff(required_tables, names(orca))
if (length(missing_tables) > 0) {
  stop(sprintf("Missing required table(s): %s", paste(missing_tables, collapse = ", ")))
}

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

write.csv(orca$life_table, file.path(output_dir, "orca_life_table.csv"), row.names = FALSE)
write.csv(orca$demographic_metric, file.path(output_dir, "orca_demographic_metric.csv"), row.names = FALSE)
write.csv(orca$data_used, file.path(output_dir, "orca_data_used.csv"), row.names = FALSE)

message("Wrote Orca CSV snapshots to ", normalizePath(output_dir))
