import { useState } from "react";
import { health } from "./api";

export default function App() {
  const [data, setData] = useState<any>(null);
  return (
    <div style={{ fontFamily: "sans-serif", padding: 24 }}>
      <h1>WatchTower AI</h1>
      <button
        onClick={async () => {
          setData(await health());
        }}
      >
        Testar API
      </button>
      <pre>{data ? JSON.stringify(data, null, 2) : "Clique para testar /api/health"}</pre>
    </div>
  );
}
