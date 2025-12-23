import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { getToken, clearToken } from "@/features/auth/authStorage";
import { getMyProfile, logout as apiLogout } from "@/features/auth/authApi";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [token, setTokenState] = useState(getToken());
    const [me, setMe] = useState(null);
    const [isBooting, setIsBooting] = useState(true);

    useEffect(() => {
        let alive = true;

        async function boot() {
            if (!token) {
                if (alive) { setMe(null); setIsBooting(false); }
                return;
            }
            try {
                const profile = await getMyProfile();
                if (alive) setMe(profile);
            } catch {
                // 토큰이 무효면 정리
                clearToken();
                if (alive) { setTokenState(null); setMe(null); }
            } finally {
                if (alive) setIsBooting(false);
            }
        }

        boot();
        return () => { alive = false; };
    }, [token]);

    const value = useMemo(() => ({
        token,
        me,
        isAuthenticated: !!token,
        isBooting,
        setToken: (t) => setTokenState(t),
        logout: async () => {
            await apiLogout();
            setTokenState(null);
            setMe(null);
        },
    }), [token, me, isBooting]);

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export const useAuth = () => useContext(AuthContext);
