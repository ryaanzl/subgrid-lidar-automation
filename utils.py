import os
import json
import pdal

def check_local_path(path: str) -> str:
    """Prevent writing directly to network drive Z:"""
    if path.upper().startswith("Z:"):
        raise PermissionError("Writing to Z: drive is not allowed. Use a local drive instead.")
    return path


def run_pipeline(pipeline_json: dict):
    """Run a PDAL pipeline from JSON."""
    pipeline = pdal.Pipeline(json.dumps(pipeline_json))
    pipeline.execute()