export function ConfirmModal({ txn, onConfirm, onCancel }) {
  if (!txn) return null;

  const sign = txn.amount >= 0 ? "+" : "-";
  const color = txn.amount >= 0 ? "green" : "red";

  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <h3>Delete transaction?</h3>
        <p>
          <span className={color}>
            {sign}${Math.abs(txn.amount).toFixed(2)}
          </span>{" "}
          · {txn.category} · {txn.description || "—"} · {txn.date}
        </p>
        <div className="modal-actions">
          <button className="btn-ghost" onClick={onCancel}>Cancel</button>
          <button className="btn-danger" onClick={onConfirm}>Delete</button>
        </div>
      </div>
    </div>
  );
}
