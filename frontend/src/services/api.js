/**
 * API service — connects frontend to FastAPI backend.
 * VITE_API_URL must be set in frontend/.env
 * e.g.  VITE_API_URL=http://localhost:8000
 */

const API_BASE = import.meta.env.VITE_API_URL
  ? import.meta.env.VITE_API_URL.replace(/\/$/, '')   // trim trailing slash
  : 'http://localhost:8000';                           // fallback default

/**
 * Send a message and get the full AI response.
 */
export async function sendMessage(message, previousInteractionId = null) {
  let res;
  try {
    res = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        previous_interaction_id: previousInteractionId,
      }),
    });
  } catch (networkErr) {
    // fetch() itself threw — backend is down or CORS blocked
    throw new Error(
      `Cannot reach backend at ${API_BASE}. ` +
      `Make sure uvicorn is running: uvicorn main:app --reload`
    );
  }

  if (!res.ok) {
    let detail = `HTTP ${res.status}`;
    try {
      const body = await res.json();
      detail = body.detail || JSON.stringify(body);
    } catch (_) {}
    throw new Error(detail);
  }

  return res.json();
}

/**
 * Check if the backend is reachable.
 */
export async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE}/health`, { method: 'GET' });
    return res.ok;
  } catch {
    return false;
  }
}
