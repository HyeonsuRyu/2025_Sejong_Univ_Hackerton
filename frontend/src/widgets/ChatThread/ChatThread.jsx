import React from "react";
import styles from "./ChatThread.module.css";

export default function ChatThread({ messages = [] }) {
    return (
        <div className={styles.root}>
            {messages.map((m) => (
                <div
                    key={m.id}
                    className={[
                        styles.bubble,
                        m.role === "user" ? styles.user : styles.assistant,
                    ].join(" ")}
                >
                    <div className={styles.role}>{m.role}</div>
                    <div className={styles.text}>{m.text}</div>

                    {Array.isArray(m.attachments) && m.attachments.length > 0 && (
                        <div className={styles.attachments}>
                            {m.attachments.map((a, idx) => (
                                <div key={idx} className={styles.attachmentItem}>
                                    {a.name || "attachment"}
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
}
