import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "@/features/auth/authApi";
import { useAuth } from "@/app/providers/AuthProvider";
import styles from "./LoginPage.module.css";
import { Link } from "react-router-dom";



export default function LoginPage() {
    const nav = useNavigate();
    const { setToken } = useAuth();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [err, setErr] = useState("");
    const [loading, setLoading] = useState(false);

    async function onSubmit(e) {
        e.preventDefault();
        setErr("");
        setLoading(true);
        try {
            const token = await login({ username, password });
            setToken(token);
            nav("/", { replace: true });
        } catch (e2) {
            setErr(e2?.message || "Login failed");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className={styles.page}>
            <div className={styles.stack}>
                <h1 className={styles.brandTop}>Uni_Brain</h1>

                <div className={styles.card}>
                    <div className={styles.headerRow}>
                        <h2 className={styles.title}>Login</h2>
                        <Link className={styles.registerLink} to="/register">
                            Register
                        </Link>
                    </div>

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
                            placeholder="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            autoComplete="current-password"
                        />

                        {err && <p className={styles.error}>{err}</p>}

                        <button className={styles.button} disabled={loading}>
                            {loading ? "Logging in..." : "Login"}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}
