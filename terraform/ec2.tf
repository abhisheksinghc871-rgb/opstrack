resource "aws_instance" "opstrack" {
  ami           = "ami-0b6d9d3d33ba97d99"
  instance_type = "m7i-flex.large"

  subnet_id = "subnet-0c59de9a2a3dc446f"

  vpc_security_group_ids = [
    "sg-033db216f332af3db"
  ]

  key_name = "orbitdesk-devops-key"

  iam_instance_profile = "OpsTrack-Terraform-Role"

  tags = {
    Name = "Devops_Projects"
  }
}
