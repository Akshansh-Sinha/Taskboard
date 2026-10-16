variable "aws_region" {
  type        = string
  description = "AWS region for resources"
  default     = "ap-south-1"
}

variable "cluster_name" {
  type        = string
  description = "EKS cluster name"
  default     = "taskboard-eks"
}

variable "environment" {
  type        = string
  description = "Deployment environment"
  default     = "dev"
}
