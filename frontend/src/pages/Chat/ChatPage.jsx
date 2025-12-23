import React, { useState, useCallback } from "react";

import ChatThread from "@/widgets/ChatThread/ChatThread";
import ChatComposer from "@/widgets/ChatComposer/ChatComposer";

import styles from "./ChatPage.module.css";

export default function ChatPage() {
    return (
        <div className={styles.wrap}>
            <div className={styles.title}>Uni_Brain</div>
            <ChatComposer onSend={(payload) => console.log(payload)} />
        </div>
    );
}
