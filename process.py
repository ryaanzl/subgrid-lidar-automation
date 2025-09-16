import os
import shutil
import geopandas as gpd
from shapely.geometry import box
from concurrent.futures import ThreadPoolExecutor, as_completed
from alive_progress import alive_bar

from config import geojson_src, workdir, orange, blue, purple, reset, error_log
from utils import check_local_path, run_pipeline
from find_file import find_geojson
from overlaps import find_overlap_las


def process_subgrid(subgrid: str):
    """Process a single subgrid: crop & merge LAS files."""
    print(f"{orange}▶ Processing Las Data Merge{reset}")

    subdir = os.path.join(workdir, subgrid)
    os.makedirs(subdir, exist_ok=True)

    merged_file = check_local_path(os.path.join(subdir, f"{subgrid}_final.las"))

    # Skip if final LAS already exists
    if any(f.endswith("_final.las") for f in os.listdir(subdir)):
        print(f"Skipping {subgrid}: final LAS already exists{reset}")
        return

    # Locate GeoJSON
    geojson_file = find_geojson(subgrid, geojson_src)
    if not geojson_file:
        print(f"GeoJSON for {subgrid} not found. Skipping.{reset}")
        return

    local_geojson = os.path.join(subdir, os.path.basename(geojson_file))
    if not os.path.exists(local_geojson):
        shutil.copy(geojson_file, local_geojson)

    # Create bounding box once (avoid repeated CRS transform)
    gdf = gpd.read_file(local_geojson).to_crs("EPSG:32748")
    minx, miny, maxx, maxy = gdf.total_bounds
    bbox_poly = box(minx, miny, maxx, maxy)
    wkt_poly = bbox_poly.wkt

    # Find overlapping LAS
    overlap_las = find_overlap_las(bbox_poly)
    if not overlap_las:
        print(f"{blue}No overlapping LAS files found for {subgrid}. Skipping.{reset}")
        return

    local_las = []
    for fname, las in overlap_las.items():
        # Skip LAS files containing '_Convert to las.las'
        fname = fname.lower().replace(" ", "_")
        if "_convert_to_las.las" in fname:
            print(f"{orange}Skipping {fname} (Convert placeholder file){reset}")
            continue

        local_path = os.path.join(subdir, fname)
        if not os.path.exists(local_path):
            shutil.copy(las, local_path)
        local_las.append(local_path)


    cropped_files = []

    # Run cropping in parallel
    def crop_task(las_path):
        cropped = check_local_path(os.path.join(subdir, f"CROP_{os.path.basename(las_path)}"))
        crop_pipeline = {
            "pipeline": [
                las_path,
                {"type": "filters.crop", "polygon": wkt_poly},
                {"type": "writers.las", "filename": cropped, "a_srs": "EPSG:32748"},
            ]
        }
        run_pipeline(crop_pipeline)
        return cropped

    with ThreadPoolExecutor(max_workers=4) as executor:  # parallel workers
        futures = [executor.submit(crop_task, las) for las in local_las]
        for f in as_completed(futures):
            try:
                cropped_files.append(f.result())
            except Exception as e:
                msg = f"Cropping failed for {subgrid}: {e}"
                print(msg)
                error_log.append(msg)

    # Merge using filters.merge (stream mode)
    if cropped_files:
        try:
            merge_pipeline = {
                "pipeline": (
                    [{"type": "readers.las", "filename": f} for f in cropped_files]
                    + [
                        {"type": "filters.merge"},
                        {"type": "writers.las", "filename": merged_file, "a_srs": "EPSG:32748"},
                    ]
                )
            }
            run_pipeline(merge_pipeline)
        except Exception as e:
            msg = f"Merging failed for {subgrid}: {e}"
            print(msg)
            error_log.append(msg)

    # Cleanup temporary files
    for f in os.listdir(subdir):
        path = os.path.join(subdir, f)
        if not (f.endswith("_final.las") or f.lower().endswith(".geojson")):
            try:
                os.remove(path)
            except Exception:
                pass

    print(f"{orange}Final LAS file created: {merged_file}{reset}")


def process_all_subgrids(subgrids: list):
    """Batch process multiple subgrids with global progress bar."""
    with alive_bar(
        len(subgrids),
        bar="filling",
        spinner="waves",
        title=f"{blue}Processing subgrids...{reset}",
        force_tty=True,
        enrich_print=False,
        theme="smooth",
    ) as bar:
        for subgrid in subgrids:
            bar.title = f"{blue}Processing subgrid: {purple}{subgrid}{reset}"
            process_subgrid(subgrid)
            bar()

