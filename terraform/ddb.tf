# DDB to replace TinyDB
resource "aws_dynamodb_table" "storage_table" {
    name = "rightmove_table"
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "id"
    attribute {
        name = "id"
        type = "N"
    }
    attribute {
        name = "review"
        type = "S"
    }
    global_secondary_index {
        hash_key = "review"
        name = "review"
        projection_type = "ALL"
    }
    ttl {
        attribute_name = "TimeToLive"
        enabled        = true
    }
    lifecycle {
        prevent_destroy = true
    }

}

resource "aws_dynamodb_table" "user_table" {
    name = "rightmove_users"
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "userID"
    attribute {
        name = "username"
        type = "S"
    }
    attribute {
        name = "userID"
        type = "N"
    }
    global_secondary_index {
        hash_key = "username"
        name = "username"
        projection_type = "ALL"
    }
    lifecycle {
        prevent_destroy = true
    }
}
