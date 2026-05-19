import { useState } from "react";
import { useSummary } from "../hooks/useSummary";
import { CategoryChart } from "./CategoryChart";
import { SummaryCards } from "./SummaryCards";

export function Dashboard() {
  const [month, setMonth] = useState("");
  const { summary, loading, error } = useSummary(month || null);

  return (
    <div className="page">
      <div className="page-header">
        <h2>Dashboard</h2>
        <div className="filters">
          <label>
            Month
            <input
              type="month"
              value={month}
              onChange={(e) => setMonth(e.target.value)}
            />
          </label>
          {month && (
            <button className="btn-ghost" onClick={() => setMonth("")}>
              Clear
            </button>
          )}
        </div>
      </div>

      {error && <p className="error">{error}</p>}
      {loading && <p className="loading">Loading…</p>}

      {summary && (
        <>
          <SummaryCards
            income={summary.income}
            expenses={summary.expenses}
            balance={summary.balance}
          />
          <div className="card">
            <h3>By Category</h3>
            <CategoryChart byCategory={summary.by_category} />
          </div>
        </>
      )}
    </div>
  );
}
