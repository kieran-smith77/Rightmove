output "instance_addr" {
  value = aws_instance.web_server.public_dns
}

