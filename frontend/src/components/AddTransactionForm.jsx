import { useState } from "react";
import { addTransaction } from "../api";

const CATEGORIES = [
  "income", "food", "rent", "transport", "health",
  "entertainment", "shopping", "utilities", "freelance", "savings",
];

function today() {
  return new Date().toISOString().slice(0, 10);
}

export function AddTransactionForm({ onAdd }) {
  const [amount, setAmount] = useState("");
  const [category, setCategory] = useState("food");
  const [description, setDescription] = useState("");
  const [date, setDate] = useState(today());
  const [type, setType] = useState("expense");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    const raw = parseFloat(amount);
    if (isNaN(raw) || raw <= 0) {
      setError("Enter a positive number for amount.");
      return;
    }
    const signedAmount = type === "expense" ? -raw : raw;
    setSubmitting(true);
    setError(null);
    try {
      await addTransaction({ amount: signedAmount, category, description, date });
      setAmount("");
      setDescription("");
      setDate(today());
      onAdd();
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form className="add-form card" onSubmit={handleSubmit}>
      <h3>Add Transaction</h3>
      {error && <p className="error">{error}</p>}
      <div className="form-row">
        <label>
          Type
          <select value={type} onChange={(e) => setType(e.target.value)}>
            <option value="expense">Expense (−)</option>
            <option value="income">Income (+)</option>
          </select>
        </label>
        <label>
          Amount ($)
          <input
            type="number"
            min="0.01"
            step="0.01"
            placeholder="0.00"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            required
          />
        </label>
        <label>
          Category
          <select value={category} onChange={(e) => setCategory(e.target.value)}>
            {CATEGORIES.map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
        </label>
        <label>
          Description
          <input
            type="text"
            placeholder="e.g. Grocery run"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </label>
        <label>
          Date
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            required
          />
        </label>
        <button type="submit" className="btn-primary" disabled={submitting}>
          {submitting ? "Adding…" : "Add"}
        </button>
      </div>
    </form>
  );
}
