// Adiciona tipagem para import.meta.env
interface ImportMetaEnv {
  VITE_API_URL?: string;
}

// Adiciona a tipagem para import.meta
interface ImportMeta {
  env: ImportMetaEnv;
}

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export interface HealthResponse {
  status: string;
}

export async function health(): Promise<HealthResponse> {
  try {
    const res = await fetch(`${API_URL}/api/health/`);
    if (!res.ok) {
      throw new Error(`Erro na requisição: ${res.status} ${res.statusText}`);
    }
    return await res.json();
  } catch (error) {
    console.error('Erro ao verificar saúde da API:', error);
    throw new Error('Não foi possível conectar ao servidor. Verifique sua conexão e tente novamente.');
  }
}
