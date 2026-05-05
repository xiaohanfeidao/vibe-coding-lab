import { useState, useEffect } from "react";
import { Layout, Menu, Skeleton, Button, Typography, Dropdown } from "@arco-design/web-react";
import {
  IconDashboard,
  IconSettings,
  IconUserGroup,
  IconMenuFold,
  IconMenuUnfold,
  IconExport,
} from "@arco-design/web-react/icon";
import { useNavigate, useLocation, Outlet } from "react-router-dom";
import { useRequest } from "../../hooks/useRequest";
import { getAdminMenus } from "../../api/modules/menu";
import { logout } from "../../api/auth";
import type { MenuItem } from "../../api/modules/menu";

const { Sider, Header, Content } = Layout;
const { Title } = Typography;

const iconMap: Record<string, React.ReactNode> = {
  "icon-dashboard": <IconDashboard />,
  "icon-settings": <IconSettings />,
  "icon-user-group": <IconUserGroup />,
};

function buildMenuItems(menus: MenuItem[]) {
  return menus.map((m) => ({
    key: m.path || m.key,
    label: m.title,
    icon: iconMap[m.icon || ""],
    children: m.children ? buildMenuItems(m.children) : undefined,
  }));
}

function flattenMenuPaths(menus: MenuItem[]): Record<string, string> {
  const map: Record<string, string> = {};
  for (const m of menus) {
    if (m.path) map[m.path] = m.key;
    if (m.children) Object.assign(map, flattenMenuPaths(m.children));
  }
  return map;
}

export default function AdminLayout() {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { data: menus, isLoading } = useRequest(getAdminMenus);

  const menuItems = menus ? buildMenuItems(menus) : [];
  const pathToKey = menus ? flattenMenuPaths(menus) : {};
  const selectedKeys = [pathToKey[location.pathname] || location.pathname];

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Sider
        collapsed={collapsed}
        collapsible
        trigger={null}
        width={220}
        style={{ borderRight: "1px solid var(--color-border)" }}
      >
        <div style={{ padding: "16px", textAlign: "center" }}>
          <Title heading={5} style={{ margin: 0, color: "rgb(var(--arcoblue-6))" }}>
            {collapsed ? "TB" : "Tech Blazing"}
          </Title>
        </div>
        {isLoading ? (
          <div style={{ padding: "8px 16px" }}>
            <Skeleton animation text={{ rows: 5 }} />
          </div>
        ) : (
          <Menu
            selectedKeys={selectedKeys}
            onClickMenuItem={(key) => navigate(key)}
            style={{ background: "transparent" }}
          >
            {menuItems.map((item) =>
              item.children ? (
                <Menu.SubMenu key={item.key} title={item.label} icon={item.icon}>
                  {item.children.map((child) => (
                    <Menu.Item key={child.key}>{child.label}</Menu.Item>
                  ))}
                </Menu.SubMenu>
              ) : (
                <Menu.Item key={item.key} icon={item.icon}>
                  {item.label}
                </Menu.Item>
              ),
            )}
          </Menu>
        )}
      </Sider>
      <Layout>
        <Header
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "0 16px",
            borderBottom: "1px solid var(--color-border)",
            background: "var(--color-bg-1)",
          }}
        >
          <Button
            type="text"
            icon={collapsed ? <IconMenuUnfold /> : <IconMenuFold />}
            onClick={() => setCollapsed(!collapsed)}
          />
          <Dropdown
            droplist={
              <Menu>
                <Menu.Item key="logout" onClick={handleLogout}>
                  <IconExport /> 退出登录
                </Menu.Item>
              </Menu>
            }
          >
            <Button type="text">管理员</Button>
          </Dropdown>
        </Header>
        <Content style={{ padding: "16px", background: "var(--color-bg-2)" }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
}
