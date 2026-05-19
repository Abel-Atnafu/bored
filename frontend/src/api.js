const BASE = "";

export async function getSummary(month) {
  const params = month ? `?month=${month}` : "";
  const res = await fetch(`${BASE}/api/summary${params}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getTransactions(month, category) {
  const p = new URLSearchParams();
  if (month) p.set("month", month);
  if (category) p.set("category", category);
  const qs = p.toString() ? `?${p}` : "";
  const res = await fetch(`${BASE}/api/transactions${qs}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function addTransaction(txn) {
  const res = await fetch(`${BASE}/api/transactions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(txn),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function deleteTransaction(id) {
  const res = await fetch(`${BASE}/api/transactions/${id}`, { method: "DELETE" });
  if (res.status !== 204) throw new Error(await res.text());
}
