import os
import laspy
from shapely.geometry import box
from collections import OrderedDict
from config import las_src

def find_overlap_las(subgrid_box) -> OrderedDict:
    """Find LAS files overlapping a given bounding box."""
    overlap_las = OrderedDict()
    for root, _, files in os.walk(las_src):
        for f in files:
            if f.lower().endswith(".las"):
                if f in overlap_las:  # Skip duplicates
                    continue
                las_path = os.path.join(root, f)
                try:
                    with laspy.open(las_path) as l:
                        xmin, ymin, _ = l.header.mins
                        xmax, ymax, _ = l.header.maxs
                        las_box = box(xmin, ymin, xmax, ymax)
                        if las_box.intersects(subgrid_box):
                            overlap_las[f] = las_path
                except Exception as e:
                    print(f"Failed to read {las_path}: {e}")
    return overlap_las
