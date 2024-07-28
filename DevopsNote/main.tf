provider "aws" {
  region = "us-west-2"
  access_key ="xxxxx"
  secret_key ="xxxxx"
}


resource "aws_vpc" "new_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "new_vpc" #保留key
    mykey = "myvalue" #自定义key
  }
}

resource "aws_subnet" "new_subnet" {
  vpc_id = aws_vpc.new_vpc.id
  cidr_block = "10.0.10.0/24"
    tags = {
    Name = "new_vpc_subnet" #保留key
  }
}

