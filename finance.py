#!/usr/bin/env python3
import json
import uuid
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Optional

import typer
from rich import print as rprint
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table

DATA_FILE = Path.home() / ".finance_tracker.json"
console = Console()

CATEGORY_ICONS = {
    "income": "💰",
    "food": "🍔",
    "rent": "🏠",
    "transport": "🚌",
    "health": "💊",
    "entertainment": "🎮",
    "shopping": "🛍️",
    "utilities": "💡",
    "freelance": "💼",
    "savings": "🏦",
}
DEFAULT_ICON = "📦"

app = typer.Typer(name="finance", help="Personal finance tracker — CLI edition.", add_completion=False)


def load_data() -> dict:
    if not DATA_FILE.exists():
        return {"version": 1, "transactions": []}
    return json.loads(DATA_FILE.read_text())


def save_data(data: dict) -> None:
    tmp = DATA_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2))
    tmp.replace(DATA_FILE)


def fmt_amount(amount: float) -> str:
    sign = "+" if amount >= 0 else "-"
    color = "green" if amount >= 0 else "red"
    return f"[{color}]{sign}${abs(amount):,.2f}[/{color}]"


def icon_for(category: str) -> str:
    return CATEGORY_ICONS.get(category.lower(), DEFAULT_ICON)


def resolve_date(date_str: Optional[str]) -> str:
    if date_str:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            console.print(f"[red]Invalid date '{date_str}'. Use YYYY-MM-DD.[/red]")
            raise typer.Exit(1)
    return date.today().isoformat()


@app.command()
def add(
    amount: str = typer.Argument(..., help="Amount (positive=income, negative=expense). E.g. 2500 or -45.50"),
    category: str = typer.Argument(..., help="Category (e.g. food, rent, income)"),
    description: str = typer.Argument(..., help="Short description"),
    date_str: Optional[str] = typer.Option(None, "--date", help="Date in YYYY-MM-DD (default: today)"),
):
    """Add a transaction."""
    try:
        amt = float(amount)
    except ValueError:
        console.print(f"[red]'{amount}' is not a valid number.[/red]")
        raise typer.Exit(1)

    txn_date = resolve_date(date_str)
    txn = {
        "id": str(uuid.uuid4()),
        "amount": amt,
        "category": category.lower(),
        "description": description,
        "date": txn_date,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    data = load_data()
    data["transactions"].append(txn)
    save_data(data)

    icon = icon_for(category)
    direction = "income" if amt >= 0 else "expense"
    console.print(Rule(f"[bold]Transaction Added[/bold]"))
    console.print(
        f"  {icon} [bold]{category.lower()}[/bold]  {fmt_amount(amt)}  "
        f"[dim]{description}[/dim]  [cyan]{txn_date}[/cyan]  "
        f"[dim]id: {txn['id'][:8]}[/dim]"
    )


@app.command(name="list")
def list_transactions(
    month: Optional[str] = typer.Option(None, "--month", help="Filter by month, e.g. 2026-05"),
    category: Optional[str] = typer.Option(None, "--category", help="Filter by category"),
):
    """List transactions."""
    data = load_data()
    txns = data["transactions"]

    if month:
        txns = [t for t in txns if t["date"].startswith(month)]
    if category:
        txns = [t for t in txns if t["category"] == category.lower()]

    txns = sorted(txns, key=lambda t: (t["date"], t["created_at"]), reverse=True)

    console.print(Rule("[bold]Transactions[/bold]"))

    if not txns:
        console.print(Panel("[yellow]No transactions found.[/yellow]", expand=False))
        return

    table = Table(show_header=True, header_style="bold cyan", box=None, pad_edge=False, row_styles=["", "dim"])
    table.add_column("Date", style="cyan", no_wrap=True)
    table.add_column("ID", style="dim", no_wrap=True)
    table.add_column("Category", no_wrap=True)
    table.add_column("Description")
    table.add_column("Amount", justify="right", no_wrap=True)

    for t in txns:
        icon = icon_for(t["category"])
        amt_str = fmt_amount(t["amount"])
        table.add_row(
            t["date"],
            t["id"][:8],
            f"{icon} {t['category']}",
            t["description"],
            amt_str,
        )

    console.print(table)
    console.print(f"\n[dim]{len(txns)} transaction(s)[/dim]")


@app.command()
def summary(
    month: Optional[str] = typer.Option(None, "--month", help="Filter by month, e.g. 2026-05"),
):
    """Show income/expense summary with category breakdown."""
    data = load_data()
    txns = data["transactions"]

    if month:
        txns = [t for t in txns if t["date"].startswith(month)]

    console.print(Rule("[bold]Summary[/bold]" + (f" — {month}" if month else "")))

    if not txns:
        console.print(Panel("[yellow]No transactions found.[/yellow]", expand=False))
        return

    income = sum(t["amount"] for t in txns if t["amount"] > 0)
    expenses = sum(abs(t["amount"]) for t in txns if t["amount"] < 0)
    balance = income - expenses

    # Totals panel
    totals_table = Table(show_header=False, box=None, pad_edge=True)
    totals_table.add_column("Label", style="bold")
    totals_table.add_column("Value", justify="right")
    totals_table.add_row("Income", f"[green]+${income:,.2f}[/green]")
    totals_table.add_row("Expenses", f"[red]-${expenses:,.2f}[/red]")
    totals_table.add_row("─" * 10, "─" * 10)
    balance_color = "green" if balance >= 0 else "red"
    balance_sign = "+" if balance >= 0 else "-"
    totals_table.add_row("Balance", f"[{balance_color}]{balance_sign}${abs(balance):,.2f}[/{balance_color}]")
    totals_panel = Panel(totals_table, title="[bold]Totals[/bold]", expand=False)

    # Category breakdown
    cat_totals: dict[str, float] = defaultdict(float)
    for t in txns:
        cat_totals[t["category"]] += t["amount"]

    sorted_cats = sorted(cat_totals.items(), key=lambda x: abs(x[1]), reverse=True)
    max_abs = max(abs(v) for _, v in sorted_cats) if sorted_cats else 1

    breakdown_table = Table(show_header=False, box=None, pad_edge=True)
    breakdown_table.add_column("Icon+Cat", no_wrap=True)
    breakdown_table.add_column("Bar")
    breakdown_table.add_column("Amount", justify="right", no_wrap=True)

    bar_width = 20
    for cat, total in sorted_cats:
        icon = icon_for(cat)
        filled = int(abs(total) / max_abs * bar_width) if max_abs else 0
        bar_char = "█" * filled + "░" * (bar_width - filled)
        color = "green" if total >= 0 else "red"
        breakdown_table.add_row(
            f"{icon} {cat}",
            f"[{color}]{bar_char}[/{color}]",
            fmt_amount(total),
        )

    breakdown_panel = Panel(breakdown_table, title="[bold]By Category[/bold]", expand=False)

    console.print(Columns([totals_panel, breakdown_panel], equal=False, expand=False))


@app.command()
def delete(
    id_prefix: str = typer.Argument(..., help="ID prefix to delete (first 8 chars shown in list)"),
):
    """Delete a transaction by ID prefix."""
    data = load_data()
    matches = [t for t in data["transactions"] if t["id"].startswith(id_prefix)]

    if not matches:
        console.print(f"[red]No transaction found with ID starting with '{id_prefix}'.[/red]")
        raise typer.Exit(1)

    if len(matches) > 1:
        console.print(f"[red]Ambiguous prefix '{id_prefix}' matches {len(matches)} transactions:[/red]")
        for m in matches:
            console.print(f"  [dim]{m['id'][:8]}[/dim]  {m['date']}  {m['description']}")
        raise typer.Exit(1)

    txn = matches[0]
    icon = icon_for(txn["category"])
    console.print(
        f"  {icon} {txn['category']}  {fmt_amount(txn['amount'])}  "
        f"[dim]{txn['description']}[/dim]  [cyan]{txn['date']}[/cyan]"
    )
    confirmed = typer.confirm("Delete this transaction?")
    if not confirmed:
        console.print("[yellow]Cancelled.[/yellow]")
        return

    data["transactions"] = [t for t in data["transactions"] if t["id"] != txn["id"]]
    save_data(data)
    console.print("[green]Deleted.[/green]")


@app.command()
def undo():
    """Remove the most recently added transaction."""
    data = load_data()
    if not data["transactions"]:
        console.print("[yellow]No transactions to undo.[/yellow]")
        return

    txns_sorted = sorted(data["transactions"], key=lambda t: t["created_at"], reverse=True)
    last = txns_sorted[0]

    icon = icon_for(last["category"])
    console.print(Rule("[bold]Undo[/bold]"))
    console.print(
        f"  Removed: {icon} {last['category']}  {fmt_amount(last['amount'])}  "
        f"[dim]{last['description']}[/dim]  [cyan]{last['date']}[/cyan]"
    )

    data["transactions"] = [t for t in data["transactions"] if t["id"] != last["id"]]
    save_data(data)


if __name__ == "__main__":
    app()
