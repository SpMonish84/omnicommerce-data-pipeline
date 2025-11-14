import sqlite3
from rich.console import Console
from rich.table import Table
from pathlib import Path

console = Console()

# Get the project root directory (parent of scripts folder)
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent
SQL_DIR = PROJECT_ROOT / "sql"
DB_PATH = PROJECT_ROOT / "ecommerce.db"


def run_query(query_path: Path, conn: sqlite3.Connection):
    """Read and execute a SQL file."""
    query_name = query_path.stem
    console.rule(f"[bold green]Running Query: {query_name}")

    with open(query_path, "r", encoding='utf-8') as f:
        sql = f.read()

    cursor = conn.execute(sql)
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    if not rows:
        console.print("[yellow]No results returned.[/yellow]")
        return

    # Pretty output with rich table
    table = Table(show_header=True, header_style="bold magenta")
    for col in columns:
        table.add_column(col)

    for row in rows[:20]:  # Show only first 20 rows
        table.add_row(*[str(x) for x in row])

    console.print(table)
    console.print(f"[cyan]Total Rows Returned: {len(rows)}[/cyan]\n")


def main():
    # Check DB exists
    if not DB_PATH.exists():
        console.print(f"[bold red]ERROR:[/] Database {DB_PATH} not found.")
        return

    conn = sqlite3.connect(str(DB_PATH))

    # Loop through all SQL files
    sql_files = sorted(SQL_DIR.glob("*.sql"))

    if not sql_files:
        console.print(f"[bold red]No SQL files found in {SQL_DIR} folder.[/]")
        return

    for sql_file in sql_files:
        run_query(sql_file, conn)

    conn.close()
    console.rule("[bold green]All Queries Executed Successfully[/bold green]")


if __name__ == "__main__":
    main()

