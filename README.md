# <img src="https://www.svgrepo.com/show/182472/location-maps-and-location.svg" width="35" style="vertical-align:middle"/> LAS Cropping & Merging Pipeline
<p align="justify"> A Python-based pipeline for <b>cropping and merging LiDAR LAS tiles</b> using <b>GeoJSON subgrids</b> as spatial boundaries. The workflow ensures efficient processing by <b>detecting overlaps, cropping with bounding polygons, merging in stream mode,</b> and skipping redundant operations. Original LAS and GeoJSON sources remain untouched in the database. </p>

---

## <img src="https://www.svgrepo.com/show/181070/route-gps.svg" width="24" style="vertical-align:middle"/> Features

1. Automatic subgrid processing with GeoJSON boundaries.  
2. Skip mechanism: if `_final.las` already exists, the subgrid is skipped.  
3. Safe operations: no destructive changes on source **Z:** database.  
4. Optimized performance:  
   - Parallel cropping with `ThreadPoolExecutor`  
   - Avoid repeated CRS transformation  
   - Stream merging with `filters.merge`  
   - Batch subgrid processing with progress bar  
5. Validation: skip placeholder LAS files (`_Convert to las.las`).  
6. Colored progress logs with ANSI codes and `alive-progress` bars.  
---
## <img src="https://www.svgrepo.com/show/181175/folder-folder.svg" width="24" style="vertical-align:middle"/> Repository Layout
```
├── main_las.py                      # Main entry point: orchestrates LAS pipeline
├── config.py                        # Global configuration: paths, colors, error logs
├── utils.py                         # Helpers: check paths, run PDAL pipelines
├── find_file.py                     # Locate GeoJSON subgrids in source folder
├── overlaps.py                      # Detect overlapping LAS tiles with subgrid
├── readme.md                        # Project documentation
├── requirements.txt                 # Library requirements
│
├── Z:/                              # Source database (read-only, untouched)
│   ├── 01 DKI JAKARTA 2025/
│   │   ├── 01 DATA LIDAR/           # Original LAS dataset
│   │   └── 02 DIGITASI/             # Subgrid GeoJSONs
│
└── C:/3D_RYAN/03_PROJECT/04_LAS_MERGING/   # Working directory for outputs
    ├── AB_10_A/                     # Example subgrid folder
    │   ├── AB_10_A_final.las        # Final merged LAS
    │   └── *.geojson                # Copied subgrid GeoJSON
    └── ...
```
## <img src="https://www.svgrepo.com/show/182434/levels-controls.svg" width="24" style="vertical-align:middle"/> Installation
### 1. Clone this repository:
```bash
git clone https://github.com/ryaanzl/las-merging-pipeline.git
cd las-merging-pipeline
```

### 2. Create a virtual environment with mamba:
```bash
mamba create -n lasenv python=3.11 -y
mamba activate lasenv
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Dependencies

The pipeline requires the following Python packages (already listed in requirements.txt):

`geopandas`, `shapely`, `pdal`, `fiona`, `pyogrio`, `proj`, `alive-progress`, `python-pdal`

## <img src="https://www.svgrepo.com/show/180902/location-location.svg" width="24" style="vertical-align:middle"/> Usage

### 1. Prepare your working directory
Make sure you have:
1. **Source LAS** in `Z:\01 DKI JAKARTA 2025\01 DATA LIDAR`
2. **Subgrid GeoJSON** in `Z:\01 DKI JAKARTA 2025\02 DIGITASI\02 DATA FIX PEMODELAN 3D`
3. **Local working dir** in `C:\3D_RYAN\03_PROJECT\04_LAS_MERGING`

### 2. Configure base directory and mode in main.py

```bash
geojson_src = r"Z:\01 DKI JAKARTA 2025\02 DIGITASI\02 DATA FIX PEMODELAN 3D"
```
```bash
las_src     = r"Z:\01 DKI JAKARTA 2025\01 DATA LIDAR"
```
```bash
workdir     = r"C:\3D_RYAN\03_PROJECT\04_LAS_MERGING"
```
### 3. Run the pipeline:
````bash
python main_las.py
````

### 4. List of Subgrids to Process
The list of subgrids to process is defined manually in the `config.py` file:
```python
subgrid_list = [
    "AU_12_C",
    "BE_15_D"
    # ...
]
```

### 5. Processing finished:
When processing is complete, the pipeline prints a final confirmation message with colors applied in the terminal:
```python
▶ Processing Las Data Merge
Skipping AU_12_C: final LAS already exists
▶ Processing Las Data Merge
Skipping BE_15_D: final LAS already exists
Processing subgrid: BE_15_D |████████████████████████████████████████| 2/2 [100%] in 0.0s (404.23/s)
```
### 6. Results will be saved automatically in dated output folders:
````
AU_12_C
├── AU_12_C_RO.geojson
├── AU_12_C.final.las
BE_15_D
├── BE_15_D_RO.geojson
├── BE_15_D.final.las
````

## <img src="https://www.svgrepo.com/show/180846/briefcase-travel.svg" width="24" style="vertical-align:middle"/> Workflow Summary

The pipeline (main.py) runs sequentially through these stages:
### [1] Subgrid detection
Match subgrid name with GeoJSON in source folder.

### [2] Overlap detection
Find all LAS tiles intersecting with the subgrid bounding box.

### [3] Cropping (parallel)
Run PDAL filters.crop per LAS tile.

### [4] Merge (stream mode)
Use filters.merge + writers.las to produce a single _final.las.

### [5] Cleanup
Remove temporary cropped LAS files, keep only final LAS + GeoJSON.

---

### <img src="https://www.svgrepo.com/show/181069/user-social.svg" width="14" style="vertical-align:middle"/> Author
Developed and maintained by Github [@ryaanzl](https://github.com/ryaanzl)  
<img src="https://www.svgrepo.com/show/180848/attach-tool.svg" width="14" style="vertical-align:middle"/> [ryanzulqifli@gmail.com](mailto:ryanzulqifli@gmail.com)