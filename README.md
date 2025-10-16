# AWS DevOps with GitOps Platform

**Production-Grade Cloud-Native Platform Engineering with AWS, Terraform, and ArgoCD**

A comprehensive, hands-on curriculum that transforms developers into production-ready DevOps engineers through systematic implementation of enterprise-grade GitOps platforms on AWS. This course eliminates local environment complexity by using cloud-based development and deployment, making advanced DevOps practices accessible to students regardless of hardware limitations while teaching modern enterprise workflows used by leading technology companies.

---

## Table of Contents

* [Introduction](#introduction)
* [Learning Objectives](#learning-objectives)
* [Prerequisites](#prerequisites)
* [Getting Started](#getting-started)
* [Course Structure](#course-structure)
* [Learning Path](#learning-path)
* [Key Technologies](#key-technologies)
* [Success Metrics](#success-metrics)
* [Community and Contributions](#community-and-contributions)
* [License](#license)

---

## Introduction

This curriculum teaches modern DevOps practices through the comprehensive lens of **GitOps methodology**, using AWS cloud services and infrastructure-as-code to build production-ready systems. Students develop a complete understanding of modern operational practices while constructing an **enterprise-grade, declaratively-managed platform** that demonstrates industry-standard reliability engineering principles.

### What You'll Build: A Complete GitOps Platform

Your journey culminates in a comprehensive, production-ready platform that includes:

**Foundation and Infrastructure:**
* **Secure, multi-tier AWS networking** with VPC isolation, public/private subnet segregation, and high-availability NAT gateways that provide defense-in-depth architecture and scalable network foundation
* **Production-grade EKS cluster** with managed node groups, auto-scaling capabilities, and proper IAM role separation that enables secure, multi-tenant workload execution
* **Infrastructure-as-Code foundation** using Terraform with state management, modular design, and idempotent operations that ensure reproducible, auditable infrastructure provisioning

**Containerization and Artifact Management:**
* **SRE-instrumented container application** with Prometheus metrics, structured logging, and comprehensive health monitoring that provides complete visibility into application behavior
* **Secure container registry** in Amazon ECR with vulnerability scanning, image signing, and lifecycle policies that protect the software supply chain
* **Multi-stage Docker builds** that optimize image size, minimize attack surface, and separate build-time from runtime dependencies

**Continuous Integration and Deployment:**
* **OIDC-authenticated GitHub Actions pipelines** that eliminate long-lived credentials, enforce least-privilege access, and provide secure CI/CD automation
* **Automated testing and security scanning** with container vulnerability analysis, code quality gates, and compliance validation integrated into every build
* **Initial imperative deployment** that establishes baseline cluster state and validates application functionality before transitioning to declarative management

**GitOps Automation and Reliability:**
* **ArgoCD GitOps engine** providing declarative continuous delivery, automated synchronization, and complete audit trails for all configuration changes
* **Git-based single source of truth** where all infrastructure and application state is version-controlled, peer-reviewed, and automatically reconciled
* **Configuration drift prevention** with automated detection and remediation that maintains desired state without manual intervention
* **Declarative rollback capabilities** enabling rapid recovery from failed deployments while maintaining complete change history

### Why This Approach Matters

**Industry Relevance**: This curriculum teaches the same tools, practices, and operational patterns used by leading technology companies to manage production systems at scale. Students graduate with immediately applicable skills that align with current industry expectations for DevOps and Platform Engineering roles.

**Production Focus**: Rather than simplified tutorial examples, every component is designed for actual production deployment with proper security controls, high availability, and operational procedures that scale with business growth and regulatory requirements.

**Cloud-Native Excellence**: By using cloud-based development and AWS cloud services from day one, students learn modern operational practices without the complexity and inconsistency of local development environments while gaining experience with enterprise-grade cloud platforms.

**GitOps Philosophy**: The curriculum emphasizes the fundamental shift from imperative (command-based) to declarative (desired-state) infrastructure management, teaching students why GitOps represents the future of platform operations and how it improves reliability, security, and developer productivity.

---

## Learning Objectives

By completing this comprehensive curriculum, you will demonstrate the ability to:

**Foundation DevOps Capabilities:**
1. **Package applications into production-grade containers** with proper security contexts, minimal attack surfaces, and comprehensive observability instrumentation that supports operational excellence
2. **Provision AWS infrastructure using Terraform** with modular design, state management, and idempotent operations that enable reproducible, version-controlled infrastructure
3. **Deploy and operate production EKS clusters** with proper IAM configuration, network isolation, and auto-scaling capabilities that maintain availability and performance under varying conditions

**Advanced GitOps Implementation:**
4. **Implement secure CI/CD pipelines** using OIDC authentication, automated testing, and container scanning that eliminate credential management risks while ensuring software quality
5. **Deploy and configure ArgoCD GitOps engines** that continuously synchronize Git-defined desired state with actual cluster state, providing automated reconciliation and drift prevention
6. **Establish declarative deployment workflows** through Git-based change management that provides complete audit trails, peer review processes, and automated rollback capabilities

**Production Operations Excellence:**
7. **Troubleshoot complex infrastructure issues** using systematic debugging approaches, log analysis, and AWS service integration that minimize mean time to resolution
8. **Implement security best practices** including IAM least-privilege access, network segmentation, and container security scanning that meet enterprise compliance requirements
9. **Design and operate GitOps workflows** that balance deployment velocity with operational stability through automated validation, progressive rollouts, and instant rollback capabilities

---

## Prerequisites

### Required Knowledge Foundation

**Technical Prerequisites:**
* **Cloud computing fundamentals** including understanding of virtualization, networking concepts, and basic AWS service awareness
* **Command-line proficiency** with Linux/Unix terminal navigation, text processing, and shell scripting that supports hands-on exercises
* **Version control experience** with Git including branching strategies, merge workflows, and collaborative development practices
* **Container fundamentals** including basic Docker concepts, containerization benefits, and container orchestration awareness

**DevOps Conceptual Understanding:**
* **Infrastructure-as-Code principles** including declarative configuration, idempotency, and version-controlled infrastructure management
* **CI/CD pipeline concepts** including build automation, testing stages, and deployment strategies
* **GitOps philosophy** including Git as single source of truth, desired state management, and reconciliation loops

### Required Accounts and Access

**Cloud Platform Access:**
* **AWS account** with billing enabled (free tier sufficient for initial exercises, ~$50-100 for complete curriculum)
* **GitHub account** with access to Actions (free tier sufficient for curriculum completion)
* **AWS CLI configured** with appropriate IAM credentials and default region settings

**Optional but Recommended:**
* **Terraform Cloud account** for remote state management (free tier available)
* **Docker Hub account** for container image distribution during development
* **Basic Kubernetes knowledge** helpful but not required, as concepts are introduced progressively

---

## Getting Started

This curriculum uses **GitHub Codespaces** for cloud-based development, providing a consistent, fully-configured environment that eliminates local setup complexity and ensures all students work with identical tooling and configurations.

### Quick Start Process

**Step 1: Environment Preparation**
1. **Create an AWS account** and configure billing alerts at $25, $50, and $75 thresholds
2. **Fork this repository** to your GitHub account to track personal progress and enable GitOps workflows
3. **Configure AWS credentials** using IAM user with programmatic access and appropriate permissions

**Step 2: Launch Cloud Development Environment**
1. **Open your forked repository** in GitHub and navigate to the Code tab
2. **Click "Create codespace on main"** to launch your cloud development environment
3. **Wait 2-3 minutes** for environment initialization including Terraform, Docker, AWS CLI, and kubectl tools

**Step 3: Configure AWS Integration**
1. **Set up AWS credentials** in your Codespace environment using environment variables or AWS configuration files
2. **Verify AWS access** with `aws sts get-caller-identity` to confirm authentication
3. **Begin learning journey** with Exercise 1 directly within your Codespace environment

The cloud environment comes pre-configured with all necessary tools including Terraform, Docker, AWS CLI, kubectl, and ArgoCD CLI, enabling immediate focus on learning DevOps concepts rather than environment configuration.

Detailed setup instructions with troubleshooting guidance are available in the [installation guide](installation.md).

---

## Course Structure

| Exercise | Title | Duration | Focus Area | Key Learning Outcomes |
|----------|-------|----------|------------|----------------------|
| [Exercise&nbsp;1](exercises/exercise1/) | Docker & Application Packaging | 2 hours | Container Security, Multi-Stage Builds, Observability | Master production container builds, implement SRE instrumentation, understand container security contexts |
| [Exercise&nbsp;2](exercises/exercise2/) | Terraform IaC: AWS Networking | 3 hours | VPC Design, Subnet Strategy, NAT Gateways, Terraform Modules | Provision secure AWS networks, implement high-availability design, establish IaC foundations |
| [Exercise&nbsp;3](exercises/exercise3/) | Terraform IaC: EKS Cluster | 3 hours | EKS Provisioning, IAM Configuration, Node Groups, RBAC | Deploy production EKS clusters, configure IAM roles, implement cluster security |
| [Exercise&nbsp;4](exercises/exercise4/) | CI/CD with OIDC & Imperative Deploy | 2.5 hours | GitHub Actions, ECR Integration, OIDC Auth, Kubectl Deploy | Implement secure CI/CD, eliminate long-lived credentials, perform initial cluster deployment |
| [Exercise&nbsp;5](exercises/exercise5/) | GitOps Engine: ArgoCD Installation | 2 hours | ArgoCD Deployment, Terraform Integration, GitOps Principles | Install GitOps controller, configure repository access, establish automation foundation |
| [Exercise&nbsp;6](exercises/exercise6/) | Full GitOps Workflow Implementation | 3 hours | Declarative Delivery, Drift Prevention, Rollback Procedures | Master GitOps workflows, implement automated reconciliation, demonstrate operational benefits |

**Total Investment**: ~15.5 hours of intensive, hands-on learning with immediate practical application

### Progressive Complexity Design

**Infrastructure Foundation (Exercises 1-3)**: Establishes containerization practices, network architecture, and cluster provisioning that form the basis for all subsequent work

**CI/CD Integration (Exercise 4)**: Implements secure automation pipelines and performs initial imperative deployment that demonstrates traditional approaches and their limitations

**GitOps Transformation (Exercises 5-6)**: Deploys declarative continuous delivery engine and implements complete GitOps workflows that represent modern platform operations excellence

---

## Learning Path

### Flexible Scheduling Options

**Intensive Learning Track (2 weeks)**:
* **Week 1**: Exercises 1-3 (Containers, Networking, EKS Cluster)
* **Week 2**: Exercises 4-6 (CI/CD, ArgoCD, GitOps Workflows)

**Standard Learning Track (4 weeks)**:
* **Week 1**: Exercise 1 (Container packaging and security)
* **Week 2**: Exercises 2-3 (Infrastructure provisioning with Terraform)
* **Week 3**: Exercise 4 (CI/CD implementation and imperative deployment)
* **Week 4**: Exercises 5-6 (GitOps engine installation and workflow implementation)

**Extended Learning Track (8 weeks)**:
* **Weeks 1-2**: Exercise 1 with deep-dive into container security and observability patterns
* **Weeks 3-4**: Exercises 2-3 with comprehensive Terraform module development and AWS networking exploration
* **Weeks 5-6**: Exercise 4 with advanced CI/CD patterns and security scanning integration
* **Weeks 7-8**: Exercises 5-6 with extensive GitOps workflow experimentation and production readiness implementation

### Self-Paced Learning Support

Each exercise includes comprehensive verification questions, troubleshooting guidance, and extension activities that support different learning speeds and depths of exploration while maintaining consistent learning outcomes across all tracks.

---

## Key Technologies

### Development Environment
**Cloud-Native Development Platform**:
* **GitHub Codespaces** - Complete cloud-based VS Code environment with pre-configured tools and extensions
* **AWS CloudShell** - Browser-based terminal with integrated AWS tools and temporary credential management
* **Git and GitHub** - Version control and collaboration platform with CI/CD integration and OIDC authentication

### Infrastructure and Orchestration
**AWS Cloud Services**:
* **Amazon VPC** - Isolated virtual network with complete control over network configuration
* **Amazon EKS** - Managed Kubernetes service with automated control plane operations
* **Amazon ECR** - Private container registry with vulnerability scanning and lifecycle policies
* **AWS IAM** - Identity and access management with OIDC federation and fine-grained permissions
* **Amazon EC2** - Compute instances for EKS node groups with auto-scaling capabilities

### Infrastructure-as-Code Platform
**Terraform Ecosystem**:
* **Terraform Core** - Infrastructure provisioning with declarative HCL syntax
* **AWS Provider** - Comprehensive AWS service integration with 900+ resources
* **Terraform State** - Persistent state storage with locking and remote backend support
* **Terraform Modules** - Reusable infrastructure components with versioning and composition

### Application and Runtime Stack
**Production-Ready Application Framework**:
* **Python 3.11 + Flask** - Modern web framework with extensive ecosystem support
* **Prometheus client libraries** - Industry-standard metrics collection and exposition
* **Structured JSON logging** - Production-grade logging with automated parsing capabilities
* **Container health endpoints** - Kubernetes-native liveness and readiness probes

### CI/CD and GitOps Platform
**Continuous Delivery Automation**:
* **GitHub Actions** - Cloud-native CI/CD with matrix builds and OIDC authentication
* **ArgoCD** - Declarative GitOps continuous delivery with automated synchronization
* **Kustomize** - Kubernetes configuration management with overlay-based customization
* **Helm** (optional) - Kubernetes package management with templating and versioning

### Observability and Operations
**Enterprise-Grade Monitoring Stack**:
* **Prometheus** - Open-source metrics collection and time-series database
* **Amazon CloudWatch** - AWS-native monitoring with metrics, logs, and alarms
* **AWS CloudTrail** - API activity logging for security analysis and compliance
* **Container Insights** - Deep container and EKS cluster monitoring integration

---

## Success Metrics

By successfully completing this curriculum, you will have demonstrated the following measurable capabilities:

### Technical Implementation Skills
**Infrastructure Provisioning Mastery**:
* Provision production-ready AWS networking with proper subnet isolation, NAT gateway high-availability, and security group controls
* Deploy and configure EKS clusters with appropriate node sizing, IAM role separation, and RBAC configuration
* Implement infrastructure-as-code using Terraform with modular design, state management, and idempotent operations

### GitOps Workflow Expertise
**Declarative Platform Operations**:
* Deploy and configure ArgoCD for continuous delivery automation with repository synchronization and health monitoring
* Implement Git-based deployment workflows that provide complete audit trails, peer review processes, and automated rollback capabilities
* Demonstrate configuration drift prevention through automated reconciliation loops that maintain desired state

### Security and Compliance Implementation
**Enterprise Security Practices**:
* Implement OIDC authentication for CI/CD pipelines that eliminate long-lived credential management risks
* Configure IAM roles with least-privilege access following AWS security best practices
* Integrate container vulnerability scanning and compliance validation into automated pipelines

### Operational Excellence Capabilities
**Production Platform Management**:
* Troubleshoot complex infrastructure issues using AWS service logs, kubectl debugging, and Terraform state analysis
* Implement systematic rollback procedures that minimize downtime and maintain service availability
* Establish operational practices that balance deployment velocity with reliability through automated validation gates

### Portfolio and Career Advancement
**Demonstrable Professional Value**:
* **Complete GitHub repository** showcasing production-ready GitOps platform with comprehensive infrastructure-as-code
* **Practical experience** with enterprise-grade tools and practices aligned with current industry DevOps job requirements
* **Systematic approach** to platform engineering demonstrating both technical implementation and operational thinking

### Verification and Assessment
**Comprehensive Skill Validation**:
Each exercise includes detailed verification questions that test synthesis and application rather than rote memorization, ensuring students can adapt their knowledge to new scenarios and business requirements while maintaining the operational excellence principles learned throughout the curriculum.

---

## Community and Contributions

### Open Source Educational Excellence

This curriculum represents a **community-driven initiative** to democratize access to enterprise-grade DevOps education. We welcome contributions that enhance learning outcomes and expand accessibility:

**Curriculum Content Enhancement**:
* **Clarity improvements** for exercise instructions, troubleshooting guides, and conceptual explanations
* **Additional scenarios** demonstrating DevOps practices in different industry contexts
* **Advanced extensions** exploring specialized topics like service mesh, observability, or security hardening
* **Accessibility improvements** including alternative learning formats and multilingual support

**Community Learning Support**:
* **Translation efforts** making content accessible to global learners
* **Video walkthroughs** and supplementary content supporting different learning preferences
* **Discussion facilitation** and peer support programs enhancing collaborative learning
* **Industry perspective sharing** from practicing DevOps engineers providing real-world context

### Contribution Guidelines

**Getting Started with Contributions**:
* Review [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines and standards
* Start with **documentation improvements** or **issue reporting** to familiarize yourself with project structure
* **Join discussions** on proposed enhancements to understand community priorities
* **Test thoroughly** any suggested changes to ensure they enhance learning experience

**Areas of Particular Need**:
* **AWS service integration examples** demonstrating additional managed services
* **Advanced GitOps patterns** including multi-environment strategies and progressive delivery
* **Security hardening guides** with compliance framework alignment
* **Cost optimization techniques** for AWS resource management

### Community Recognition

Contributors making significant improvements to curriculum content, learning accessibility, or community support will be recognized in course materials and project documentation, helping build professional portfolios while supporting educational excellence.

---

## License

This educational project is licensed under the **MIT License**, promoting open access to high-quality DevOps education while enabling adaptation and improvement by the global learning community.

See [LICENSE.md](LICENSE.md) for complete licensing terms supporting both individual learning and organizational training requirements.

---

## Ready to Transform Your Career?

**Begin your journey to DevOps excellence** with [Exercise 1: Docker & Application Packaging](exercises/exercise1/).

**Transform from developer to Platform Engineer** through systematic implementation of production-ready GitOps platforms that demonstrate enterprise-grade operational capabilities and advance your professional career in cloud-native infrastructure and platform engineering.

---

*Master the art and science of declarative platform operations through GitOps methodologies that improve deployment reliability, accelerate delivery velocity, and reduce operational overhead while maintaining comprehensive audit trails and instant rollback capabilities.*

![AWS DevOps GitOps](https://img.shields.io/badge/AWS-DevOps%20GitOps-orange)