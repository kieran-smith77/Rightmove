resource "aws_route53_record" "www" {
  zone_id = "Z3E90BKB7SO4HQ"
  name    = "rightmove.kieran-smith.com"
  type    = "A"
  ttl     = "300"
  records = [aws_instance.web_server.public_ip]
}