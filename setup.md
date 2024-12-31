# Project setup details

## Steps to create infrastructure and set up project (I used a Linux VM running on EC2)

1. Clone this git repo.

2. Build a docker container named stock-screener, tag it and push to ECR.
  - Navigate to the scripts folder to locate the python scripts and docker container definition file (Dockerfile)
  - Install docker on the VM using the follow commands if not already installed:
  '''
  sudo yum update -y
  sudo amazon-linux-extras install docker
  sudo service docker start
  sudo usermod -a -G docker ec2-user
  '''
  - Build the docker container using '''docker build -t stock-screener'''.
  - Create a new repository on AWS ECR. I named my repository as '''finance/stock-screener'''.
  - Tag the docker container using '''docker tag stock-screener:<ECR Repository URI>'''.
  - Authenticate AWS ECR '''aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <ECR Repository URI>'''
  - Push the tagged image to the ECR repository '''docker push <ECR Repository URI>:latest'''



After setup, deploy the pipeline using steps on the [deploy](deploy.md) file.