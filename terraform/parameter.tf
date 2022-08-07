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

resource "aws_ssm_parameter" "registration_status" {
  name  = "/rightmove/app/registration"
  type  = "String"
  value = "True"
  lifecycle {
    ignore_changes = [
      value,
    ]
  }
}