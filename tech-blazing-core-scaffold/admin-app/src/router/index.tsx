import { createBrowserRouter, Navigate } from "react-router-dom";
import { AdminLayout } from "../components/Layout";
import { Login } from "../pages/Login";
import { Dashboard } from "../pages/Dashboard";
import { System } from "../pages/System";
import { Users } from "../pages/Users";
import { getAccessToken } from "../api/client";

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  if (!getAccessToken()) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
}

export const router = createBrowserRouter([
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/admin",
    element: (
      <ProtectedRoute>
        <AdminLayout />
      </ProtectedRoute>
    ),
    children: [
      { index: true, element: <Navigate to="/admin/dashboard" replace /> },
      { path: "dashboard", element: <Dashboard /> },
      { path: "system", element: <System /> },
      { path: "users", element: <Users /> },
    ],
  },
  {
    path: "/",
    element: <Navigate to="/admin/dashboard" replace />,
  },
]);
