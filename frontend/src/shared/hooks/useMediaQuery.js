import { useEffect, useState } from "react";

export default function useMediaQuery(query) {
    const getMatch = () => {
        if (typeof window === "undefined") return false;
        return window.matchMedia(query).matches;
    };

    const [matches, setMatches] = useState(getMatch);

    useEffect(() => {
        const mql = window.matchMedia(query);
        const handler = () => setMatches(mql.matches);

        // 초기 동기화
        handler();

        if (mql.addEventListener) mql.addEventListener("change", handler);
        else mql.addListener(handler);

        return () => {
            if (mql.removeEventListener) mql.removeEventListener("change", handler);
            else mql.removeListener(handler);
        };
    }, [query]);

    return matches;
}
