import { Layout, Menu, Typography, Button } from "@arco-design/web-react";
import { IconHome, IconApps, IconInfoCircle, IconPhone } from "@arco-design/web-react/icon";
import { useNavigate, useLocation, Outlet } from "react-router-dom";

const { Header, Content, Footer } = Layout;
const { Title } = Typography;

const menuItems = [
  { key: "/", label: "首页", icon: <IconHome /> },
  { key: "/features", label: "功能", icon: <IconApps /> },
  { key: "/about", label: "关于", icon: <IconInfoCircle /> },
  { key: "/contact", label: "联系我们", icon: <IconPhone /> },
];

export default function AppLayout() {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Header
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "0 24px",
          borderBottom: "1px solid var(--color-border)",
          background: "var(--color-bg-1)",
        }}
      >
        <Title heading={5} style={{ margin: 0, color: "rgb(var(--arcoblue-6))" }}>
          Tech Blazing
        </Title>
        <Menu
          mode="horizontal"
          selectedKeys={[location.pathname]}
          onClickMenuItem={(key) => navigate(key)}
          style={{ background: "transparent" }}
        >
          {menuItems.map((item) => (
            <Menu.Item key={item.key}>
              {item.icon}
              {item.label}
            </Menu.Item>
          ))}
        </Menu>
      </Header>
      <Content style={{ padding: "24px", background: "var(--color-bg-2)" }}>
        <Outlet />
      </Content>
      <Footer
        style={{
          textAlign: "center",
          padding: "16px 24px",
          background: "var(--color-bg-1)",
          borderTop: "1px solid var(--color-border)",
        }}
      >
        Tech Blazing Core Scaffold ©{new Date().getFullYear()}
      </Footer>
    </Layout>
  );
}
