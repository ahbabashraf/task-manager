# Task Manager - Cloud & DevOps Project

## Project Overview

Task Manager is a containerized web application built using Flask and MySQL.

The project demonstrates how a web application can be developed locally,
containerized using Docker, and deployed on AWS with a CI/CD pipeline.

The project also includes AWS infrastructure, monitoring, security,
and automated database backups.

## Features

- Add tasks
- View tasks
- Mark tasks as completed or incomplete
- Delete tasks
- Health check endpoint
- MySQL database integration
- Dockerized application
- Automated deployment using GitHub Actions

## Tech Stack

### Application
- Python
- Flask
- Flask-SQLAlchemy
- MySQL

### Containerization
- Docker
- Docker Compose

### CI/CD
- GitHub
- GitHub Actions
- Amazon ECR
- AWS Systems Manager

### AWS
- Amazon EC2
- Application Load Balancer
- Amazon ECR
- Amazon CloudWatch
- Amazon S3
- IAM
- VPC
- Security Groups

## Architecture

```text
Internet / User
       |
       v
Application Load Balancer
       |
       v
EC2 Instance
       |
       v
Docker Compose
   |          |
   v          v
 Flask      MySQL

## CI/CD Deployment Flow

```text
Developer
    |
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    +----> Build Docker Image
    |
    +----> Push Image to Amazon ECR
    |
    v
AWS Systems Manager
    |
    v
EC2 Instance
    |
    v
Pull Image from ECR
    |
    v
Docker Compose
    |
    v
Updated Flask Application

## AWS Infrastructure

### Amazon VPC

The application is deployed inside a custom Amazon VPC.

The VPC contains:

- Public subnets
- Private subnets
- Internet Gateway
- Route tables
- Security Groups

For the current Phase 1 deployment, the EC2 instance and Application Load Balancer use the public subnets.

### Application Load Balancer

The Application Load Balancer acts as the public entry point of the application.

It:

- Accepts HTTP traffic on port 80
- Forwards requests to the EC2 instance
- Performs health checks on the application

### Amazon EC2

The Flask application runs on an Ubuntu EC2 instance.

Docker and Docker Compose are installed on the instance.

The EC2 instance runs:

- Flask application container
- MySQL container

### Amazon ECR

Amazon Elastic Container Registry is used as a private Docker image registry.

GitHub Actions builds the application image and pushes it to ECR.

The EC2 instance then pulls the required image from ECR during deployment.

### AWS Systems Manager

AWS Systems Manager is used to execute deployment commands on the EC2 instance.

This allows GitHub Actions to trigger deployment without directly connecting to EC2 using SSH.

### Amazon CloudWatch

CloudWatch is used for EC2 monitoring.

A CPU utilization alarm is configured to detect high CPU usage.

### Amazon S3

Amazon S3 is used to store compressed MySQL database backups.

The backup process is:

```text
MySQL
  |
  v
mysqldump
  |
  v
gzip compression
  |
  v
Amazon S3

Database backups are automated using a Linux cron job.

## Security

Security Groups are used to control network traffic.

The current setup follows this flow:

```text
Internet
   |
   v
ALB :80
   |
   v
EC2 :80
   |
   v
Flask Container :5000

- ALB allows HTTP traffic from the internet.
- EC2 allows HTTP traffic only from the ALB Security Group.
- SSH access is restricted to the configured administrator IP.
- The application container is not directly exposed to the internet.
- IAM roles are used to provide AWS permissions to EC2.

## AWS Deployment

The application is deployed on AWS using:

- Amazon EC2
- Application Load Balancer
- Amazon ECR
- AWS Systems Manager
- Docker Compose

The EC2 instance runs the Flask application and MySQL using Docker Compose.

The Application Load Balancer provides the public HTTP entry point.

## Database Backup

MySQL database backups are created using `mysqldump`.

The backup process is:

1. Create a MySQL database dump.
2. Compress the dump using gzip.
3. Upload the compressed backup to Amazon S3.
4. Run the backup automatically using a Linux cron job.

## How CI/CD Works

Every push to the `main` branch triggers the GitHub Actions workflow.

The pipeline performs the following steps:

1. Checkout the latest source code.
2. Configure AWS credentials.
3. Login to Amazon ECR.
4. Build the Docker image.
5. Tag the image with the Git commit SHA.
6. Push the image to Amazon ECR.
7. Use AWS Systems Manager to execute deployment commands on EC2.
8. Pull the new image from ECR.
9. Restart the Flask container using Docker Compose.

This allows the application to be updated automatically after a code change.


