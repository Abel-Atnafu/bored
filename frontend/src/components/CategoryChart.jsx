const ICONS = {
  income: "💰", food: "🍔", rent: "🏠", transport: "🚌",
  health: "💊", entertainment: "🎮", shopping: "🛍️",
  utilities: "💡", freelance: "💼", savings: "🏦",
};

function fmt(amount) {
  const sign = amount >= 0 ? "+" : "-";
  return `${sign}$${Math.abs(amount).toLocaleString("en-US", { minimumFractionDigits: 2 })}`;
}

export function CategoryChart({ byCategory }) {
  if (!byCategory || byCategory.length === 0) {
    return <p className="empty">No data.</p>;
  }
  const maxAbs = Math.max(...byCategory.map((d) => Math.abs(d.total)));

  return (
    <div className="category-chart">
      {byCategory.map(({ category, total }) => {
        const pct = maxAbs ? ((Math.abs(total) / maxAbs) * 100).toFixed(1) : 0;
        const icon = ICONS[category] ?? "📦";
        const isIncome = total >= 0;
        return (
          <div key={category} className="chart-row">
            <span className="chart-label">
              {icon} {category}
            </span>
            <div className="chart-bar-bg">
              <div
                className={`chart-bar ${isIncome ? "income-bar" : "expense-bar"}`}
                style={{ width: `${pct}%` }}
              />
            </div>
            <span className={`chart-amount ${isIncome ? "green" : "red"}`}>{fmt(total)}</span>
          </div>
        );
      })}
    </div>
  );
}
