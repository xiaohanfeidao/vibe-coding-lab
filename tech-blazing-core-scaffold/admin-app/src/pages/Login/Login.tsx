import { Card, Form, Input, Button, Typography, Message } from "@arco-design/web-react";
import { useNavigate } from "react-router-dom";
import { login } from "../../api/auth";

const { Title } = Typography;
const { Item: FormItem } = Form;

export default function Login() {
  const [form] = Form.useForm();
  const navigate = useNavigate();

  const handleSubmit = async () => {
    try {
      const values = await form.validate();
      const resp = await login(values);
      if (resp.code === 0) {
        Message.success("登录成功");
        navigate("/admin/dashboard");
      }
    } catch {
      Message.error("登录失败，请检查用户名和密码");
    }
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        background: "var(--color-bg-2)",
      }}
    >
      <Card style={{ width: 400 }}>
        <Title heading={4} style={{ textAlign: "center", marginTop: 0 }}>
          后台管理系统
        </Title>
        <Form form={form} layout="vertical">
          <FormItem label="用户名" field="username" rules={[{ required: true, message: "请输入用户名" }]}>
            <Input placeholder="请输入用户名" />
          </FormItem>
          <FormItem label="密码" field="password" rules={[{ required: true, message: "请输入密码" }]}>
            <Input.Password placeholder="请输入密码" />
          </FormItem>
          <FormItem>
            <Button type="primary" long onClick={handleSubmit}>
              登录
            </Button>
          </FormItem>
        </Form>
      </Card>
    </div>
  );
}
