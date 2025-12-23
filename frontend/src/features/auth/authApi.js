import { http } from "@/shared/api/http";
import { setToken, clearToken } from "./authStorage";


export async function register(payload) {
    const res = await http("/user/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });

    // 201 Created { id, username, email }
    return res.json();
}

export async function login({ username, password }) {
    const res = await http("/user/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });
    const data = await res.json(); // { token: "..." }
    if (!data?.token) throw new Error("No token in response");
    setToken(data.token);
    return data.token;
}

export async function logout() {
    // 서버에 logout endpoint 없으니 일단 로컬 토큰만 제거
    clearToken();
}

export async function getMyProfile() {
    const res = await http("/user/profile/me/");
    return res.json(); // { nickname: "..." }
}

