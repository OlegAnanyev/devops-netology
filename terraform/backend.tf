terraform {
  backend "s3" {
    bucket = "netologybucket"
    key    = "terraform/state"
    region = "eu-north-1"
  }
}