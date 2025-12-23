import { useState,useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { register } from "@/features/auth/authApi";
import styles from "./RegisterPage.module.css";

const KEY_STORAGE = "openrouter_api_key";

export default function RegisterPage() {
    const nav = useNavigate();

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [nickname, setNickname] = useState("");
    const [password, setPassword] = useState("");
    const [password2, setPassword2] = useState("");

    const [apiKey, setApiKey] = useState(""); 
    const [err, setErr] = useState("");
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const saved = sessionStorage.getItem(KEY_STORAGE) || "";
        setApiKey(saved);
    }, []);

    async function onSubmit(e) {
        e.preventDefault();
        setErr("");

        if (password !== password2) {
            setErr("비밀번호가 일치하지 않습니다.");
            return;
        }

        // 키는 옵션: 있으면 sessionStorage에 저장
        if (apiKey.trim()) {
            sessionStorage.setItem(KEY_STORAGE, apiKey.trim());
        }

        setLoading(true);
        try {
            await register({ username, email, nickname, password, password2 });
            nav("/login", { replace: true });
        } catch (e2) {
            setErr(e2?.message || "Register failed");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className={styles.page}>
            <div className={styles.stack}>
                <h1 className={styles.brandTop}>Uni_Brain</h1>

                <div className={styles.card}>
                    <h2 className={styles.title}>Register</h2>

                    <form className={styles.form} onSubmit={onSubmit}>
                        <input
                            className={styles.input}
                            placeholder="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            autoComplete="username"
                        />

                        <input
                            className={styles.input}
                            placeholder="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            autoComplete="email"
                        />

                        <input
                            className={styles.input}
                            placeholder="nickname"
                            value={nickname}
                            onChange={(e) => setNickname(e.target.value)}
                            autoComplete="nickname"
                        />

                        {/* OpenRouter 키(옵션) */}
                        <input
                            className={styles.input}
                            placeholder="OpenRouter API Key (optional)"
                            value={apiKey}
                            onChange={(e) => setApiKey(e.target.value)}
                            type="password"
                        />

                        <input
                            className={styles.input}
                            placeholder="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            autoComplete="new-password"
                        />

                        <input
                            className={styles.input}
                            placeholder="password confirm"
                            type="password"
                            value={password2}
                            onChange={(e) => setPassword2(e.target.value)}
                            autoComplete="new-password"
                        />

                        {err && <p className={styles.error}>{err}</p>}

                        <button className={styles.button} disabled={loading}>
                            {loading ? "Creating..." : "Create account"}
                        </button>

                        <div className={styles.hintRow}>
                            <span>이미 계정이 있나요?</span>
                            <Link className={styles.link} to="/login">
                                로그인
                            </Link>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}
