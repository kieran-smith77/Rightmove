# DDB to replace TinyDB
resource "aws_dynamodb_table" "storage_table" {
    name = "rightmove_table"
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "id"
    attribute {
        name = "id"
        type = "N"
    }
}