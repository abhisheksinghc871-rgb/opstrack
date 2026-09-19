output "instance_id" {
  value = data.aws_instance.opstrack.id
}

output "instance_type" {
  value = data.aws_instance.opstrack.instance_type
}

output "availability_zone" {
  value = data.aws_instance.opstrack.availability_zone
}

output "private_ip" {
  value = data.aws_instance.opstrack.private_ip
}
