import { useCallback, useEffect, useState } from "react";
import { getTransactions } from "../api";

export function useTransactions(month, category) {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [tick, setTick] = useState(0);

  useEffect(() => {
    setLoading(true);
    setError(null);
    getTransactions(month, category)
      .then(setTransactions)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [month, category, tick]);

  const refetch = useCallback(() => setTick((t) => t + 1), []);
  return { transactions, loading, error, refetch };
}
