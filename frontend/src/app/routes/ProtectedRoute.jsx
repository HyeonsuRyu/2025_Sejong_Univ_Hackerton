import { Navigate } from "react-router-dom";
import { useAuth } from "@/app/providers/AuthProvider";

export default function ProtectedRoute({ children }) {
    const { isAuthenticated, isBooting } = useAuth();

    if (isBooting) return null; // 또는 로딩 컴포넌트
    if (!isAuthenticated) return <Navigate to="/login" replace />;

    return children;
}