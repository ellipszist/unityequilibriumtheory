import {
  Body,
  Container,
  Head,
  Heading,
  Html,
  Link,
  Preview,
  Text,
} from "@react-email/components";
import * as React from "react";

interface WelcomeEmailProps {
  name: string;
}

export const WelcomeEmail = ({ name }: WelcomeEmailProps) => (
  <Html>
    <Head />
    <Preview>Welcome to UET Platform!</Preview>
    <Body style={main}>
      <Container style={container}>
        <Heading style={h1}>Welcome, {name}!</Heading>
        <Text style={text}>
          Thank you for joining the UET Platform. We're excited to have you on board.
        </Text>
        <Text style={text}>
          You can now start exploring the Unity Equilibrium Theory knowledge base, integrating with our MCP endpoints, and diving into the scientific grid.
        </Text>
        <Link href="https://uet-platform.com/docs" style={button}>
          Get Started with Docs
        </Link>
        <Text style={footer}>
          If you have any questions, reply to this email. We're here to help.
        </Text>
      </Container>
    </Body>
  </Html>
);

export default WelcomeEmail;

const main = {
  backgroundColor: "#f5f7f5",
  fontFamily:
    '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen-Sans,Ubuntu,Cantarell,"Helvetica Neue",sans-serif',
};

const container = {
  margin: "0 auto",
  padding: "20px 0 48px",
  width: "580px",
  backgroundColor: "#ffffff",
  borderRadius: "8px",
  border: "1px solid #eaeaea",
  marginTop: "40px",
  paddingLeft: "40px",
  paddingRight: "40px",
};

const h1 = {
  color: "#111",
  fontSize: "24px",
  fontWeight: "bold",
  margin: "40px 0",
  padding: "0",
};

const text = {
  color: "#444",
  fontSize: "14px",
  lineHeight: "24px",
};

const button = {
  backgroundColor: "#0d7a5f",
  borderRadius: "6px",
  color: "#fff",
  fontSize: "14px",
  fontWeight: "bold",
  textDecoration: "none",
  textAlign: "center" as const,
  display: "block",
  width: "100%",
  padding: "12px",
  marginTop: "24px",
  marginBottom: "24px",
};

const footer = {
  color: "#888",
  fontSize: "12px",
  lineHeight: "22px",
  marginTop: "24px",
};
