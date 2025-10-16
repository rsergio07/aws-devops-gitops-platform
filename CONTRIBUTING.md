# Contributing to the AWS DevOps with GitOps Platform

This repository is built on the principle of **operational excellence** and **continuous improvement**. Contributions are highly welcome, particularly those that enhance the reliability, security, or educational clarity of the curriculum.

## SRE Contribution Philosophy

All contributions must adhere to the following SRE standards:

1.  **Prioritize Clarity:** Documentation and instructions must be clear, concise, and maintain the **Expert SRE Mentor** tone.
2.  **Verify Reliability:** All Infrastructure as Code (Terraform) and Kubernetes manifests must be validated and tested before submission. Changes should aim to **reduce toil** or improve platform resilience.
3.  **Maintain Consistency:** New exercises or examples must seamlessly integrate into the progressive learning path and adhere to the established folder structure.
4.  **Security First:** Any change touching IAM, networking, or application code must be reviewed for security best practices (e.g., Least Privilege, OIDC).

## How to Contribute

1.  **Fork** this repository.
2.  **Clone** your fork and create a new branch: `git checkout -b feature/your-contribution-name`.
3.  Make your changes. If modifying an exercise, explain the improvement in the commit message.
4.  **Test Locally:** Run the modified exercise steps on your local machine to confirm the expected outcome.
5.  Submit a **Pull Request (PR)** to the `main` branch of this repository.

## Contribution Standards

* All Terraform files must be `terraform fmt` compliant.
* All Kubernetes manifests must be `kubectl apply --validate` compliant.
* All documentation must use standard Markdown formatting.