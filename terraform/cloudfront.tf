locals {
  domain_name = "rightmove.kieran-smith.com"
  origin_dns  = aws_instance.web_server.public_dns
  origin_id   = "webserver"
}

resource "aws_cloudfront_distribution" "rightmove_distribution" {
  aliases = [local.domain_name]
  default_cache_behavior {
    allowed_methods  = ["HEAD", "DELETE", "POST", "GET", "OPTIONS", "PUT", "PATCH"]
    cached_methods   = ["HEAD", "GET"]
    target_origin_id = local.origin_id

    forwarded_values {
      query_string = true
      cookies {
        forward = "all"
      }
    }
    viewer_protocol_policy = "allow-all"

  }
  enabled = true
  origin {
    domain_name = local.origin_dns
    origin_id   = local.origin_id
    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["SSLv3", "TLSv1", "TLSv1.1", "TLSv1.2"]
    }
  }
  restrictions {
    geo_restriction {
      restriction_type = "whitelist"
      locations        = ["GB"]
    }
  }
  viewer_certificate {
    # cloudfront_default_certificate = true
    acm_certificate_arn      = aws_acm_certificate.rightmove_cert.arn
    minimum_protocol_version = "TLSv1.2_2021"
    ssl_support_method       = "sni-only"
  }
  depends_on = [aws_instance.web_server]
}

resource "aws_acm_certificate" "rightmove_cert" {
  provider          = aws.us_east_1
  domain_name       = "rightmove.kieran-smith.com"
  validation_method = "DNS"
}

data "aws_route53_zone" "kieran-smith" {
  name         = "kieran-smith.com"
  private_zone = false
}

resource "aws_route53_record" "rm_record" {
  for_each = {
    for dvo in aws_acm_certificate.rightmove_cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.kieran-smith.zone_id
}

resource "aws_acm_certificate_validation" "rm_cert_validation" {
  provider                = aws.us_east_1
  certificate_arn         = aws_acm_certificate.rightmove_cert.arn
  validation_record_fqdns = [for record in aws_route53_record.rm_record : record.fqdn]
  depends_on              = [aws_route53_record.rm_record, aws_acm_certificate.rightmove_cert]
  timeouts {
    create = "60m"
  }

}
