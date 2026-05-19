const CATEGORIES = [
  "income", "food", "rent", "transport", "health",
  "entertainment", "shopping", "utilities", "freelance", "savings",
];

export function Filters({ month, category, onMonthChange, onCategoryChange }) {
  return (
    <div className="filters">
      <label>
        Month
        <input
          type="month"
          value={month}
          onChange={(e) => onMonthChange(e.target.value)}
        />
      </label>
      <label>
        Category
        <select value={category} onChange={(e) => onCategoryChange(e.target.value)}>
          <option value="">All</option>
          {CATEGORIES.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </label>
      {(month || category) && (
        <button
          className="btn-ghost"
          onClick={() => { onMonthChange(""); onCategoryChange(""); }}
        >
          Clear filters
        </button>
      )}
    </div>
  );
}
