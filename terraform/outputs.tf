//id аккаунта
output "account_id" {
  value = data.aws_caller_identity.current.account_id
}
//id пользователя
output "user_id" {
  value = data.aws_caller_identity.current.user_id
}
//регион
output "region" {
  value = data.aws_region.current.name
}
//приватный ip
output "private_ip" {
  value = aws_instance.netology.private_ip
}
//публичный ip
output "public_ip" {
  value = aws_instance.netology.public_ip
}
//id подсети
output "subnet_id" {
  value = aws_instance.netology.subnet_id
}


//ARN (Amazon Resource Name)
output "caller_arn" {
  value = data.aws_caller_identity.current.arn
}

