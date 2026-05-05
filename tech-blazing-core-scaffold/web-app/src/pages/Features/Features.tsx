import { Card, Typography, Grid, Descriptions } from "@arco-design/web-react";

const { Row, Col } = Grid;
const { Title } = Typography;

const features = [
  {
    title: "API 系统",
    details: [
      { label: "框架", value: "FastAPI 0.115+" },
      { label: "运行时", value: "Python 3.11+" },
      { label: "多进程", value: "Gunicorn + Uvicorn Workers" },
      { label: "配置管理", value: "application.yml + 环境覆盖" },
    ],
  },
  {
    title: "前台页面",
    details: [
      { label: "框架", value: "React 18 + TypeScript" },
      { label: "UI 组件", value: "Arco Design" },
      { label: "构建工具", value: "Vite 8" },
      { label: "路由", value: "React Router 7" },
    ],
  },
  {
    title: "后台管理",
    details: [
      { label: "认证", value: "JWT (HS256)" },
      { label: "密码哈希", value: "bcrypt" },
      { label: "限流", value: "slowapi 内存存储" },
      { label: "安全", value: "CORS + 安全头 + 输入校验" },
    ],
  },
  {
    title: "部署运维",
    details: [
      { label: "容器化", value: "Docker Compose" },
      { label: "前端托管", value: "Nginx" },
      { label: "API 代理", value: "Nginx reverse proxy" },
      { label: "Monorepo", value: "pnpm workspace" },
    ],
  },
];

export default function Features() {
  return (
    <div>
      <Title heading={3}>平台功能</Title>
      <Row gutter={16}>
        {features.map((f) => (
          <Col xs={24} sm={12} lg={12} key={f.title} style={{ marginBottom: 16 }}>
            <Card title={f.title}>
              <Descriptions
                data={f.details.map((d) => ({ label: d.label, value: d.value }))}
                column={1}
                style={{ marginBottom: 0 }}
              />
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
}
