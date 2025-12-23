import React, { useEffect, useCallback, useState } from "react";
import { Outlet } from "react-router-dom";

import Sidebar from "@/widgets/Sidebar/Sidebar";
import useMediaQuery from "@/shared/hooks/useMediaQuery";
import useSidebar from "@/shared/hooks/useSidebar";

import styles from "@/layouts/AppShell/AppShell.module.css";

export default function AppShell() {
    return (
        <div className={styles.shell}>
            <aside className={styles.sidebar}>
                <Sidebar />
            </aside>

            <main className={styles.main}>
                <Outlet />
            </main>
        </div>
    );
}