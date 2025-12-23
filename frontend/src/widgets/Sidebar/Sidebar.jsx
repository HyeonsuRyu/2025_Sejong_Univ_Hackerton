import React from "react";
import styles from "./Sidebar.module.css";
import { useNavigate } from "react-router-dom";


function IconGrid() {
    return (
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
            <path d="M4 4h7v7H4V4Z" stroke="currentColor" strokeWidth="1.6" />
            <path d="M13 4h7v7h-7V4Z" stroke="currentColor" strokeWidth="1.6" />
            <path d="M4 13h7v7H4v-7Z" stroke="currentColor" strokeWidth="1.6" />
            <path d="M13 13h7v7h-7v-7Z" stroke="currentColor" strokeWidth="1.6" />
        </svg>
    );
}

function IconChat() {
    return (
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
            <path
                d="M20 14c0 1.1-.45 2.1-1.2 2.9C17.5 18.3 15.4 19 13 19H9l-4 3v-5c-.6-.7-1-1.6-1-2.6V7c0-2.2 2.2-4 5-4h4c2.8 0 5 1.8 5 4v7Z"
                stroke="currentColor"
                strokeWidth="1.6"
                strokeLinejoin="round"
            />
        </svg>
    );
}

function isLoggedIn() {
    // 토큰방식으로 바꿔야됨
    return Boolean(localStorage.getItem("ub_token"));
}


function IconUser() {
    return (
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
            <path
                d="M20 21c0-3.314-3.582-6-8-6s-8 2.686-8 6"
                stroke="currentColor"
                strokeWidth="1.6"
                strokeLinecap="round"
            />
            <path
                d="M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z"
                stroke="currentColor"
                strokeWidth="1.6"
            />
        </svg>
    );
}

export default function Sidebar() {
    const navigate = useNavigate();

    const handleProfileClick = () => {
        if (isLoggedIn()) navigate("/profile");
        else navigate("/login");
    };

    return (
        <div className={styles.root}>
            <div className={styles.brand}>UB</div>

            <div className={styles.menu}>
                <button className={styles.iconBtn} type="button" aria-label="Dashboard">
                    <IconGrid />
                </button>
                <button className={styles.iconBtn} type="button" aria-label="Chat">
                    <IconChat />
                </button>

                {/* 아래로 밀어내서 하단 고정 */}
                <div className={styles.spacer} />

                <button
                    className={styles.iconBtn}
                    type="button"
                    aria-label="Profile"
                    onClick={handleProfileClick}
                    title={isLoggedIn() ? "Profile" : "login"}
                >
                    <IconUser />
                </button>
            </div>
        </div>
    );
}
