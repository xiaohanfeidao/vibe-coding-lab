import { Card, Typography, Descriptions } from "@arco-design/web-react";

const { Title } = Typography;

export default function About() {
  return (
    <div>
      <Title heading={3}>关于项目</Title>
      <Card>
        <Descriptions
          column={1}
          data={[
            { label: "项目名称", value: "Tech Blazing Core Scaffold" },
            { label: "版本", value: "0.1.0" },
            { label: "描述", value: "全栈项目脚手架模板" },
            { label: "后端技术", value: "Python FastAPI + Gunicorn + PyJWT" },
            { label: "前端技术", value: "React 18 + TypeScript + Arco Design" },
            { label: "部署方案", value: "Docker Compose + Nginx" },
          ]}
          style={{ marginBottom: 0 }}
        />
      </Card>
    </div>
  );
}
