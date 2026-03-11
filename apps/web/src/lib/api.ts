const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';

let authToken: string | null = null;

export function setAuthToken(token: string) {
  authToken = token;
  if (typeof window !== 'undefined') {
    localStorage.setItem('auth_token', token);
  }
}

export function getAuthToken(): string | null {
  if (authToken) return authToken;
  if (typeof window !== 'undefined') {
    return localStorage.getItem('auth_token');
  }
  return null;
}

async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getAuthToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const response = await fetch(`${API_URL}${path}`, { ...options, headers });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: response.statusText }));
    throw new Error(error.message || 'API error');
  }

  return response.json();
}

export const api = {
  auth: {
    login: (email: string, password: string) =>
      apiFetch<{ accessToken: string; user: object }>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      }),
    register: (email: string, password: string, name?: string) =>
      apiFetch<{ accessToken: string; user: object }>('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ email, password, name }),
      }),
  },
  stocks: {
    get: (symbol: string) => apiFetch(`/stocks/${symbol}`),
    history: (symbol: string, days?: number) =>
      apiFetch(`/stocks/${symbol}/history${days ? `?days=${days}` : ''}`),
    marketOverview: () => apiFetch('/stocks/market/overview'),
  },
  portfolio: {
    get: () => apiFetch('/portfolio'),
    trade: (data: { symbol: string; action: string; shares: number; price: number }) =>
      apiFetch('/portfolio/trade', { method: 'POST', body: JSON.stringify(data) }),
    performance: () => apiFetch('/portfolio/performance'),
  },
  agents: {
    decisions: (limit?: number) => apiFetch(`/agents/decisions${limit ? `?limit=${limit}` : ''}`),
    decisionsBySymbol: (symbol: string) => apiFetch(`/agents/decisions/${symbol}`),
    run: (symbol: string) =>
      apiFetch('/agents/run', { method: 'POST', body: JSON.stringify({ symbol }) }),
  },
};
