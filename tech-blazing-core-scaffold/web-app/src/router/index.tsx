import { createBrowserRouter } from "react-router-dom";
import { AppLayout } from "../components/Layout";
import { Home } from "../pages/Home";
import { Features } from "../pages/Features";
import { About } from "../pages/About";
import { Contact } from "../pages/Contact";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    children: [
      { index: true, element: <Home /> },
      { path: "features", element: <Features /> },
      { path: "about", element: <About /> },
      { path: "contact", element: <Contact /> },
    ],
  },
]);
