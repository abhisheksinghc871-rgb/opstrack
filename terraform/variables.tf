variable "aws_region" {
  description = "AWS region for OpsTrack infrastructure"
  type        = string
  default     = "us-east-1"
}

variable "instance_id" {
  description = "Existing OpsTrack EC2 instance ID"
  type        = string
  default     = "i-07082b61094629d1c"
}
