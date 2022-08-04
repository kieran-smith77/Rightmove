resource "aws_route53_record" "www" {
  zone_id = "Z3E90BKB7SO4HQ"
  name    = "rightmove.kieran-smith.com"
  type    = "A"
  alias {
    name                   = aws_cloudfront_distribution.rightmove_distribution.domain_name
    zone_id                = aws_cloudfront_distribution.rightmove_distribution.hosted_zone_id
    evaluate_target_health = false
  }
}