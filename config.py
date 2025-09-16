import warnings

# ================== CONFIGURATION ==================
geojson_src = r"Z:\01 DKI JAKARTA 2025\02 DIGITASI\02 DATA FIX PEMODELAN 3D"
las_src     = r"Z:\01 DKI JAKARTA 2025\01 DATA LIDAR"
workdir     = r"C:\3D_RYAN\03_PROJECT\04_LAS_MERGING"

# List of subgrids to process (manual input)
subgrid_list = [
    "AU_12_C",
    "BE_15_D"
]

# Error log
error_log = []

# ================== WARNINGS & COLORS ==================
warnings.filterwarnings("ignore", "Several features with id", RuntimeWarning)
warnings.filterwarnings("ignore", "GeoSeries.notna", UserWarning)

orange       = "\033[38;5;173m"
blue      = "\033[38;5;75m"
purple = "\033[38;5;141m"
reset     = "\033[0m"

# peru        = "\033[38;5;173m"   # orange-brown
# blue_symbol = "\033[38;5;75m"    # cyan-blue
# purple_code = "\033[38;5;141m"   # blue-purple
# reset       = "\033[0m"