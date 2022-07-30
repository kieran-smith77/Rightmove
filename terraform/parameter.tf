# Parameter store for Webhook
resource "aws_ssm_parameter" "webhooks" {
  name  = "/rightmove/scraper/webhooks"
  type  = "StringList"
  value = " "
  lifecycle {
    ignore_changes = [
      value,
    ]
  }
}
# Parameter store for search term
resource "aws_ssm_parameter" "searches" {
  name  = "/rightmove/scraper/searches"
  type  = "StringList"
  value = " "
  lifecycle {
    ignore_changes = [
      value,
    ]
  }
}

resource "aws_ssm_parameter" "secretkey" {
  name  = "/rightmove/app/secretkey"
  type  = "String"
  value = " "
  lifecycle {
    ignore_changes = [
      value,
    ]
  }
}