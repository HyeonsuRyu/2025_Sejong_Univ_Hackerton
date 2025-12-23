import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./ProfilePage.module.css";
import { getOpenRouterKey, setOpenRouterKey, clearOpenRouterKey } from "../../features/chat/openRouterKeyStorage";

function maskKey(key) {
    if (!key) return "";
    if (key.length <= 10) return "********";
    return `${key.slice(0, 6)}...${key.slice(-4)}`;
}

export default function ProfilePage() {
    const navigate = useNavigate();
    const [apiKey, setApiKey] = useState("");
    const [toast, setToast] = useState("");

    useEffect(() => {
        setApiKey(getOpenRouterKey());
    }, []);

    const save = () => {
        setOpenRouterKey(apiKey.trim());
        setToast("저장 완료");
        setTimeout(() => setToast(""), 1200);
    };

    const remove = () => {
        clearOpenRouterKey();
        setApiKey("");
        setToast("삭제 완료");
        setTimeout(() => setToast(""), 1200);
    };

    const saved = getOpenRouterKey();

    return (
        <div className={styles.page}>
            <div className={styles.header}>
                <div>
                    <h1 className={styles.title}>프로필</h1>
                    <p className={styles.subtitle}>OpenRouter API Key를 관리합니다. (sessionStorage)</p>
                </div>

                <button className={styles.backBtn} onClick={() => navigate("/")} type="button">
                    채팅으로
                </button>
            </div>

            <div className={styles.card}>
                <div className={styles.row}>
                    <span className={styles.label}>현재 저장된 키</span>
                    <span className={styles.value}>{saved ? maskKey(saved) : "없음"}</span>
                </div>

                <div className={styles.field}>
                    <label className={styles.fieldLabel}>OpenRouter API Key</label>
                    <input
                        className={styles.input}
                        value={apiKey}
                        onChange={(e) => setApiKey(e.target.value)}
                        placeholder="sk-or-v1-..."
                        autoComplete="off"
                    />
                </div>

                <div className={styles.actions}>
                    <button className={styles.primary} onClick={save} type="button">저장</button>
                    <button className={styles.ghost} onClick={remove} type="button">삭제</button>
                    {toast && <span className={styles.toast}>{toast}</span>}
                </div>
            </div>
        </div>
    );
}
