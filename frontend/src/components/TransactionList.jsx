import { useState } from "react";
import { deleteTransaction } from "../api";
import { useTransactions } from "../hooks/useTransactions";
import { AddTransactionForm } from "./AddTransactionForm";
import { ConfirmModal } from "./ConfirmModal";
import { Filters } from "./Filters";

const ICONS = {
  income: "💰", food: "🍔", rent: "🏠", transport: "🚌",
  health: "💊", entertainment: "🎮", shopping: "🛍️",
  utilities: "💡", freelance: "💼", savings: "🏦",
};

function fmtAmount(amount) {
  const sign = amount >= 0 ? "+" : "-";
  return `${sign}$${Math.abs(amount).toLocaleString("en-US", { minimumFractionDigits: 2 })}`;
}

export function TransactionList() {
  const [month, setMonth] = useState("");
  const [category, setCategory] = useState("");
  const [selectedTxn, setSelectedTxn] = useState(null);
  const [deleteError, setDeleteError] = useState(null);

  const { transactions, loading, error, refetch } = useTransactions(
    month || null,
    category || null
  );

  async function handleDelete() {
    try {
      await deleteTransaction(selectedTxn.id);
      setSelectedTxn(null);
      refetch();
    } catch (e) {
      setDeleteError(e.message);
      setSelectedTxn(null);
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <h2>Transactions</h2>
        <Filters
          month={month}
          category={category}
          onMonthChange={setMonth}
          onCategoryChange={setCategory}
        />
      </div>

      <AddTransactionForm onAdd={refetch} />

      {(error || deleteError) && <p className="error">{error || deleteError}</p>}
      {loading && <p className="loading">Loading…</p>}

      {!loading && transactions.length === 0 && (
        <p className="empty">No transactions found.</p>
      )}

      {transactions.length > 0 && (
        <div className="card table-card">
          <table className="txn-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Category</th>
                <th>Description</th>
                <th className="right">Amount</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {transactions.map((txn) => {
                const icon = ICONS[txn.category] ?? "📦";
                const isIncome = txn.amount >= 0;
                return (
                  <tr key={txn.id}>
                    <td className="date-cell">{txn.date}</td>
                    <td>
                      {icon} {txn.category}
                    </td>
                    <td className="desc-cell">{txn.description}</td>
                    <td className={`right ${isIncome ? "green" : "red"}`}>
                      {fmtAmount(txn.amount)}
                    </td>
                    <td>
                      <button
                        className="btn-icon"
                        title="Delete"
                        onClick={() => setSelectedTxn(txn)}
                      >
                        ✕
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          <p className="table-count">{transactions.length} transaction(s)</p>
        </div>
      )}

      <ConfirmModal
        txn={selectedTxn}
        onConfirm={handleDelete}
        onCancel={() => setSelectedTxn(null)}
      />
    </div>
  );
}
