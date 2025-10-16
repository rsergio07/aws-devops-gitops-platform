# Installation and Prerequisites (SRE Toolkit)

To successfully complete this hands-on curriculum, you must prepare your local machine with the standard SRE toolkit required for cloud-native development and operations on AWS.

## Required Software

Ensure the following tools are installed and configured:

1.  **AWS Account and Credentials:**
    * An active AWS Account with Administrator-level access.
    * **AWS CLI:** Installed and configured with programmatic access keys.
    * **Note:** All exercises will assume the AWS CLI is configured and authenticated in the terminal environment.

2.  **Infrastructure as Code (IaC):**
    * **Terraform CLI:** Version 1.5.0 or later. Required for provisioning VPC, EKS, and ArgoCD.

3.  **Containerization:**
    * **Docker Engine:** Installed and running. Required for Exercise 1 builds.

4.  **Kubernetes Management:**
    * **kubectl:** The Kubernetes command-line tool. Required for interacting with the EKS cluster.
    * **aws-iam-authenticator (or aws-cli integration):** Ensure your AWS CLI is up-to-date, as modern versions handle the EKS authentication automatically via `aws eks update-kubeconfig`.

## Environment Setup Verification

Run the following commands to confirm your environment is correctly set up:

```bash
aws sts get-caller-identity
terraform version
docker --version
kubectl version --client