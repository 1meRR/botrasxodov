from db import add_expense, get_stats, get_today


def parse_expense(text):
    parts = text.strip().split()
    if len(parts) < 2:
        return None, None
    try:
        amount = int(parts[-1])
    except ValueError:
        return None, None
    title = " ".join(parts[:-1])
    return title, amount


def format_today():
    rows = get_today()
    if not rows:
        return "Сегодня пока ничего"
    items = []
    total = 0
    for row in rows:
        items.append(f"{row['title']} - {row['amount']}")
        total += row["amount"]
    items.append(f"Всего: {total}")
    return "\n".join(items)


def format_stats():
    rows = get_stats()
    if not rows:
        return "Нет данных"
    lines = []
    for row in rows:
        lines.append(f"{row['title']}: {row['total']}")
    return "\n".join(lines)


def save_expense(text):
    title, amount = parse_expense(text)
    if not title or not amount:
        return False
    add_expense(title, amount)
    return True
