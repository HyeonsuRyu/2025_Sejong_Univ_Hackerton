import { useCallback, useEffect, useState } from "react";

const KEY = "sidebarCollapsed";

export default function useSidebar() {
    const [collapsed, setCollapsed] = useState(() => {
        try {
            return localStorage.getItem(KEY) === "1";
        } catch {
            return false;
        }
    });

    useEffect(() => {
        try {
            localStorage.setItem(KEY, collapsed ? "1" : "0");
        } catch {
            // ignore
        }
    }, [collapsed]);

    const toggleCollapsed = useCallback(() => {
        setCollapsed((v) => !v);
    }, []);

    return { collapsed, setCollapsed, toggleCollapsed };
}
