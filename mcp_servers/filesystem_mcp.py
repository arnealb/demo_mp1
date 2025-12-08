from mcp.server.fastmcp import FastMCP
import logging
import os 

logging.basicConfig(level = logging.INFO)
logging.info("Starting file system MCP server")

mcp = FastMCP("filesystem")
ROOT = "data"

def resolve_path(path: str) -> str:
    full = os.path.abspath(os.path.join(ROOT, path))
    if not full.startswith(os.path.abspath(ROOT)):
        raise ValueError("Access outside root is not allowed")
    return full

@mcp.tool()
def list_all_files() -> list[str]:
    paths = []
    for root, dirs, files in os.walk(ROOT):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), ROOT)
            paths.append(rel)
    return paths


@mcp.tool()
def read_files(path: str) -> str:
    full = resolve_path(path)
    if not os.path.isfile(full):
        raise ValueError("Not a file")
    with open(full, "r", encoding="utf-8") as f:
        return f.read()

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
