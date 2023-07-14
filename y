version = 0.1
[y.deploy.parameters]
stack_name = "student-api"
resolve_s3 = true
s3_prefix = "student-api"
region = "ap-south-1"
confirm_changeset = true
capabilities = "CAPABILITY_IAM"
image_repositories = []
