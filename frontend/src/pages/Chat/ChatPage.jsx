import { useEffect, useMemo, useState } from "react";
import { openRouterRequest } from "@/features/chat/openRouterApi";
import {
    getOpenRouterKey,
    setOpenRouterKey,
    clearOpenRouterKey,
} from "@/features/chat/openRouterKeyStorage";
import Sidebar from "@/widgets/Sidebar/Sidebar";
import styles from "./ChatPage.module.css";

export default function ChatPage() {
    const [apiKey, setApiKey] = useState("");
    const [text, setText] = useState("");
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [err, setErr] = useState("");

    useEffect(() => {
        setApiKey(getOpenRouterKey());
    }, []);

    const canSend = useMemo(
        () => apiKey.trim() && text.trim() && !loading,
        [apiKey, text, loading]
    );

    function onSaveKey() {
        setOpenRouterKey(apiKey.trim());
    }

    function onClearKey() {
        clearOpenRouterKey();
        setApiKey("");
    }

    async function onSend(e) {
        e.preventDefault();
        if (!canSend) return;

        const prompt = text.trim();
        setText("");
        setErr("");

        setMessages((p) => [
            ...p,
            { id: crypto.randomUUID(), role: "user", content: prompt },
        ]);

        const tempId = crypto.randomUUID();
        setMessages((p) => [
            ...p,
            { id: tempId, role: "assistant", content: "..." },
        ]);

        setLoading(true);
        try {
            setOpenRouterKey(apiKey.trim());

            const data = await openRouterRequest({ text: prompt, apiKey: apiKey.trim() });

            const answer =
                data?.response ??
                data?.result ??
                data?.text ??
                data?.message ??
                JSON.stringify(data);

            setMessages((p) =>
                p.map((m) => (m.id === tempId ? { ...m, content: String(answer) } : m))
            );
        } catch (e2) {
            setErr(e2?.message || "Request failed");
            setMessages((p) => p.filter((m) => m.id !== tempId));
        } finally {
            setLoading(false);
        }
    }

    const isEmpty = messages.length === 0;

    return (
        <div className={styles.page}>
            {/* Left Sidebar */}
            <Sidebar/>

            {/* Main */}
            <main className={styles.main}>
                <div className={styles.centerWrap}>
                    <div className={`${styles.card} ${isEmpty ? styles.cardCompact : styles.cardExpanded}`}>
                        {/* Title */}
                        <div className={styles.cardHeader}>
                            <h1 className={styles.cardTitle}>Uni_Brain</h1>
                        </div>

                        {/* Optional: key input (prototype) */}
                        <div className={styles.keyRow}>
                            <input
                                className={styles.keyInput}
                                value={apiKey}
                                onChange={(e) => setApiKey(e.target.value)}
                                placeholder="OpenRouter API Key"
                                type="text"
                            />
                        </div>

                        {/* Thread: only show after first message */}
                        {!isEmpty && (
                            <div className={styles.thread}>
                                {messages.map((m) => {
                                    const isUser = m.role === "user";
                                    return (
                                        <div
                                            key={m.id}
                                            className={`${styles.msgRow} ${isUser ? styles.msgUser : styles.msgAI}`}
                                        >
                                            <div className={`${styles.bubble} ${isUser ? styles.bubbleUser : ""}`}>
                                                {m.content}
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        )}

                        {err && <div className={styles.error}>{err}</div>}

                        {/* Composer (always visible) */}
                        <form className={styles.composer} onSubmit={onSend}>
                            <input
                                className={styles.input}
                                value={text}
                                onChange={(e) => setText(e.target.value)}
                                placeholder="메시지 입력..."
                            />
                            <button className={styles.sendBtn} disabled={!canSend}>
                                {loading ? "..." : "Send"}
                            </button>
                        </form>
                    </div>
                </div>
            </main>
        </div>
    );
}
