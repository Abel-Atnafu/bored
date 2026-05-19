import { Link, Route, BrowserRouter as Router, Routes, useLocation } from "react-router-dom";
import { Dashboard } from "./components/Dashboard";
import { TransactionList } from "./components/TransactionList";

function Nav() {
  const { pathname } = useLocation();
  return (
    <nav className="nav">
      <span className="nav-brand">💸 Finance Tracker</span>
      <div className="nav-links">
        <Link className={pathname === "/" ? "active" : ""} to="/">Dashboard</Link>
        <Link className={pathname === "/transactions" ? "active" : ""} to="/transactions">
          Transactions
        </Link>
      </div>
    </nav>
  );
}

export default function App() {
  return (
    <Router>
      <Nav />
      <main className="main">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/transactions" element={<TransactionList />} />
        </Routes>
      </main>
    </Router>
  );
}
