import { Card, Skeleton, Result, Empty, Typography, Grid, Tag } from "@arco-design/web-react";
import { IconCheckCircle } from "@arco-design/web-react/icon";
import { useRequest } from "../../hooks/useRequest";
import { getHealth } from "../../api/modules/health";

const { Row, Col } = Grid;
const { Title, Paragraph } = Typography;

const features = [
  { title: "高性能 API", desc: "基于 FastAPI 构建的高性能后端服务，支持多进程部署" },
  { title: "现代化前端", desc: "React + TypeScript + Arco Design 企业级组件库" },
  { title: "安全加固", desc: "JWT 认证、API 限流、安全响应头、CORS 保护" },
  { title: "容器化部署", desc: "Docker Compose 一键部署，Nginx 静态资源托管" },
];

export default function Home() {
  const { data, isLoading, error, refetch } = useRequest(getHealth);

  return (
    <div>
      <div
        style={{
          background: "linear-gradient(135deg, rgb(var(--arcoblue-6)), rgb(var(--arcoblue-5)))",
          borderRadius: 8,
          padding: "48px 32px",
          marginBottom: 24,
          color: "#fff",
        }}
      >
        <Title heading={2} style={{ color: "#fff", marginTop: 0 }}>
          Tech Blazing Core Scaffold
        </Title>
        <Paragraph style={{ color: "rgba(255,255,255,0.85)", fontSize: 16, marginBottom: 16 }}>
          全栈项目脚手架模板 — FastAPI + React + Arco Design
        </Paragraph>
        {isLoading && <Skeleton animation text={{ rows: 1 }} style={{ background: "rgba(255,255,255,0.2)" }} />}
        {error && (
          <Tag color="red" style={{ marginTop: 8 }}>
            服务连接失败
          </Tag>
        )}
        {data && (
          <Tag icon={<IconCheckCircle />} color="green" style={{ marginTop: 8 }}>
            服务状态: {data.status}
          </Tag>
        )}
      </div>

      <Title heading={4}>核心特性</Title>
      <Row gutter={16}>
        {features.map((f) => (
          <Col xs={24} sm={12} lg={6} key={f.title} style={{ marginBottom: 16 }}>
            <Card hoverable title={f.title} style={{ height: "100%" }}>
              {f.desc}
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
}
