import React, { useState, useCallback } from "react";
import styles from "./ChatComposer.module.css";

export default function ChatComposer({ onSend }) {
    const [text, setText] = useState("");

    const canSend = text.trim().length > 0;

    const submit = useCallback(() => {
        if (!canSend) return;
        onSend?.({ text, attachments: [] });
        setText("");
    }, [canSend, onSend, text]);

    const onKeyDown = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            submit();
        }
    };

    return (
        <div className={styles.card}>
            <textarea
                className={styles.input}
                placeholder=""
                value={text}
                onChange={(e) => setText(e.target.value)}
                onKeyDown={onKeyDown}
            />

            <button
                type="button"
                className={styles.send}
                onClick={submit}
                disabled={!canSend}
                aria-label="Send"
            >
                ↑
            </button>
        </div>
    );
}