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
        enabled        = false
    }
    lifecycle {
        prevent_destroy = true
    }

}
