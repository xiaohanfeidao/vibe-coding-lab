import { Card, Form, Input, Button, Typography, Message } from "@arco-design/web-react";

const { Title } = Typography;
const { Item: FormItem } = Form;

export default function Contact() {
  const [form] = Form.useForm();

  const handleSubmit = () => {
    Message.info("此功能为演示占位，暂不实际发送消息");
  };

  return (
    <div>
      <Title heading={3}>联系我们</Title>
      <Card style={{ maxWidth: 600 }}>
        <Form form={form} layout="vertical" onSubmit={handleSubmit}>
          <FormItem label="姓名" field="name" rules={[{ required: true, message: "请输入姓名" }]}>
            <Input placeholder="请输入姓名" />
          </FormItem>
          <FormItem label="邮箱" field="email" rules={[{ required: true, message: "请输入邮箱" }, { type: "email", message: "邮箱格式不正确" }]}>
            <Input placeholder="请输入邮箱" />
          </FormItem>
          <FormItem label="消息" field="message" rules={[{ required: true, message: "请输入消息" }]}>
            <Input.TextArea placeholder="请输入消息" autoSize={{ minRows: 4 }} />
          </FormItem>
          <FormItem>
            <Button type="primary" htmlType="submit">提交</Button>
          </FormItem>
        </Form>
      </Card>
    </div>
  );
}
