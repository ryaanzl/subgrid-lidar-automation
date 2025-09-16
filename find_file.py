import os

def find_geojson(subgrid_name: str, search_path: str) -> str | None:
    """Find a GeoJSON file matching the subgrid name."""
    for root, _, files in os.walk(search_path):
        for f in files:
            if f.lower().endswith(".geojson"):
                prefix = f[:len(subgrid_name)]
                if prefix == subgrid_name or prefix.replace("_", "-") == subgrid_name.replace("_", "-"):
                    return os.path.join(root, f)
    return None
