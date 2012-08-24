import os

def dump_cache_dir(cache_directory):
    ws = os.getenv("WORKSPACE")
    if ws:
        f = open(os.path.join(ws, "current_cache_dir.txt"), "w")
        f.write(cache_directory)
        f.close()
