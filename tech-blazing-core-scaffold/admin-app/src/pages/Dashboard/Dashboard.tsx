import { Card, Statistic, Grid, Descriptions, Skeleton, Tag } from "@arco-design/web-react";
import { IconUser, IconEye, IconDesktop, IconClockCircle } from "@arco-design/web-react/icon";
import { useRequest } from "../../hooks/useRequest";
import { getHealth } from "../../api/modules/health";

const { Row, Col } = Grid;

const stats = [
  { title: "用户数", value: 128, icon: <IconUser />, suffix: "" },
  { title: "访问量", value: 3842, icon: <IconEye />, suffix: "" },
  { title: "在线数", value: 12, icon: <IconDesktop />, suffix: "" },
  { title: "运行时间", value: 72, icon: <IconClockCircle />, suffix: "h" },
];

export default function Dashboard() {
  const { data, isLoading } = useRequest(getHealth);

  return (
    <div>
      <Row gutter={16} style={{ marginBottom: 16 }}>
        {stats.map((s) => (
          <Col xs={24} sm={12} lg={6} key={s.title}>
            <Card hoverable style={{ marginBottom: 16 }}>
              <Statistic
                title={s.title}
                value={s.value}
                suffix={s.suffix}
                prefix={s.icon}
                styleValue={{ color: "rgb(var(--arcoblue-6))" }}
              />
            </Card>
          </Col>
        ))}
      </Row>

      <Card title="系统状态">
        {isLoading ? (
          <Skeleton animation text={{ rows: 3 }} />
        ) : (
          <Descriptions
            data={[
              { label: "服务状态", value: data ? <Tag color="green">运行中</Tag> : <Tag color="red">离线</Tag> },
              { label: "健康检查", value: data?.status ?? "不可用" },
              { label: "API 版本", value: "v1" },
              { label: "项目名称", value: "Tech Blazing Core Scaffold" },
            ]}
            column={2}
          />
        )}
      </Card>
    </div>
  );
}
