function StatCard({ label, amount, color }) {
  const sign = amount >= 0 ? "+" : "-";
  return (
    <div className={`stat-card ${color}`}>
      <div className="stat-label">{label}</div>
      <div className="stat-value">
        {sign}${Math.abs(amount).toLocaleString("en-US", { minimumFractionDigits: 2 })}
      </div>
    </div>
  );
}

export function SummaryCards({ income, expenses, balance }) {
  return (
    <div className="summary-cards">
      <StatCard label="Income" amount={income} color="green" />
      <StatCard label="Expenses" amount={-expenses} color="red" />
      <StatCard label="Balance" amount={balance} color={balance >= 0 ? "green" : "red"} />
    </div>
  );
}
