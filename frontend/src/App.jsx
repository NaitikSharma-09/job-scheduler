import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import { io } from "socket.io-client";

const api = axios.create({
  baseURL: "/",
  withCredentials: true,
});

function App() {
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("123456");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [result, setResult] = useState("");
  const [live, setLive] = useState([]);
  const [executionTime, setExecutionTime] = useState(6);
  const [memory, setMemory] = useState(3);
  const [prediction, setPrediction] = useState("");
  const [error, setError] = useState("");

  const socket = useMemo(() => io(), []);

  useEffect(() => {
    socket.on("update_graph", (data) => {
      setLive((prev) => {
        const next = [...prev, `Generation ${data.generation}: fitness ${data.fitness}`];
        return next.slice(-20);
      });
    });
    return () => {
      socket.disconnect();
    };
  }, [socket]);

  const login = async () => {
    setError("");
    try {
      await api.post("/api/login", {
        username: username.trim(),
        password: password.trim(),
      });
      setIsLoggedIn(true);
    } catch (err) {
      setError(
        err.response?.data?.error ||
          "Login failed. Ensure backend is running on port 5000.",
      );
    }
  };

  const logout = async () => {
    await api.post("/api/logout");
    setIsLoggedIn(false);
    setResult("");
  };

  const runScheduler = async () => {
    try {
      const res = await api.get("/api/run");
      setResult(res.data.result);
    } catch {
      setError("Run failed. Login first.");
    }
  };

  const predictPriority = async () => {
    try {
      const res = await api.post("/api/predict-priority", {
        execution_time: Number(executionTime),
        memory: Number(memory),
      });
      setPrediction(res.data.predicted_priority);
    } catch {
      setError("Prediction failed. Login first.");
    }
  };

  return (
    <div className="container">
      <h1>Genetic Scheduler Dashboard</h1>

      {!isLoggedIn ? (
        <div className="card">
          <h2>Login</h2>
          <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" />
          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="password"
            placeholder="Password"
          />
          <button onClick={login}>Login</button>
        </div>
      ) : (
        <>
          <div className="card">
            <button onClick={runScheduler}>Run Scheduler</button>
            <button onClick={logout}>Logout</button>
            <pre>{result}</pre>
          </div>
          <div className="card">
            <h2>Live Genetic Updates</h2>
            <pre>{live.join("\n") || "Waiting..."}</pre>
          </div>
          <div className="card">
            <h2>AI Job Priority Prediction</h2>
            <input
              type="number"
              value={executionTime}
              onChange={(e) => setExecutionTime(e.target.value)}
              placeholder="Execution time"
            />
            <input
              type="number"
              value={memory}
              onChange={(e) => setMemory(e.target.value)}
              placeholder="Memory"
            />
            <button onClick={predictPriority}>Predict</button>
            <p>Predicted Priority: {prediction || "-"}</p>
          </div>
        </>
      )}

      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default App;
