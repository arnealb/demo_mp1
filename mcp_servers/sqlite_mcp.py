from mcp.server.fastmcp import FastMCP
import aiosqlite
import logging


logging.basicConfig(level=logging.INFO)
logging.info("Starting sqlite MCP Server...")


mcp = FastMCP("sqlite_mcp")
DB_FILE = "db/example.db"

@mcp.tool()
async def list_all_entries() -> list[str]:
    """List all saved entries."""
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute("SELECT * FROM records")
        rows = await cursor.fetchall()
    return [
        f"id={row[0]}, name={row[1]}, details={row[2]}"
        for row in rows
    ]


@mcp.tool()
async def list_all_entries_with_id(entry_id: int) -> list[str]:
    """List all entries with a certain id"""
    async with aiosqlite.connect(DB_FILE) as db: 
        cursor = await db.execute(
            "SELECT id, name, details FROM records WHERE id = ?",
            (entry_id,)
        )
        rows = await cursor.fetchall()
    return [
        f"id={row[0]}, name={row[1]}, details={row[2]}"
        for row in rows
    ]

def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
