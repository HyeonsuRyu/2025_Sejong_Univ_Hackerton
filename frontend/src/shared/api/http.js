import { getToken } from "@/features/auth/authStorage";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

export async function http(url, { method = "GET", headers = {}, body } = {}) {
    const token = getToken();

    const res = await fetch(API_BASE + url, {
        method,
        headers: {
            ...(token ? { Authorization: `Token ${token}` } : {}),
            ...headers,
        },
        body,
    });

    if (!res.ok) {
        let detail = "";
        try { detail = await res.text(); } catch { }
        throw new Error(`HTTP ${res.status}: ${detail || res.statusText}`);
    }
    return res;
}
