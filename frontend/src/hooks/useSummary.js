import { useEffect, useState } from "react";
import { getSummary } from "../api";

export function useSummary(month) {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    getSummary(month)
      .then(setSummary)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [month]);

  return { summary, loading, error };
}
