# Exercise 1: Docker & Application Packaging

## Table of Contents

* [Introduction](#introduction)
* [Learning Objectives](#learning-objectives)
* [Prerequisites](#prerequisites)
* [Theory Foundation](#theory-foundation)
* [Understanding Production Container Design](#understanding-production-container-design)
* [Building Multi-Stage Container Images](#building-multi-stage-container-images)
* [Implementing Container Security Contexts](#implementing-container-security-contexts)
* [Integrating SRE Observability](#integrating-sre-observability)
* [Testing Container Security and Functionality](#testing-container-security-and-functionality)
* [Final Objective](#final-objective)
* [Verification Questions](#verification-questions)
* [Troubleshooting](#troubleshooting)
* [Next Steps](#next-steps)

---

## Introduction

In this exercise, you will learn to package a production-grade SRE-instrumented application into secure, minimal container artifacts using Docker multi-stage builds. You'll implement container security best practices including non-root execution, minimal base images, and comprehensive health monitoring that forms the foundation for cloud-native deployment.

This approach demonstrates how modern DevOps teams create container artifacts that balance operational observability with security hardening, preparing applications for deployment to orchestrated environments like Amazon EKS while maintaining complete visibility into application behavior.

**What You'll Build:**
* Production-ready Flask application with Prometheus metrics
* Multi-stage Dockerfile optimized for security and size
* Container image under 100MB with non-root execution
* Comprehensive health check endpoints for Kubernetes
* Security-scanned container artifact ready for ECR

---

## Learning Objectives

By completing this exercise, you will understand:

* **Production Container Design**: How to create minimal, secure container images that eliminate unnecessary attack surface
* **Multi-Stage Build Patterns**: How to separate build-time dependencies from runtime environments for optimal image size
* **Container Security Contexts**: How to implement non-root execution and read-only filesystems for defense-in-depth
* **SRE Observability Integration**: How to instrument applications with Prometheus metrics and structured logging from day one
* **Health Check Implementation**: How to provide Kubernetes-compatible health endpoints for automated orchestration

---

## Prerequisites

Before starting this exercise, ensure you have:

* **Docker installed** and daemon running
* **Python 3.11+** for local testing (optional)
* **Git** for version control
* **Text editor** or IDE for code review
* **Command-line proficiency** for build and test operations

**Verify your environment:**
```bash
# Check Docker installation
docker --version

# Verify Docker daemon is running
docker ps

# Check Python availability (optional)
python3 --version

# Confirm current directory
pwd
```

**Expected output:**
```
Docker version 24.0.x
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
Python 3.11.x
/path/to/aws-devops-gitops-platform
```

---

## Theory Foundation

### Container Security and Production Readiness

**Essential Watching** (20 minutes):
- [Docker Security Best Practices](https://www.youtube.com/watch?v=KINjI1tlo2w) by TechWorld with Nana - Comprehensive security overview
- [Multi-Stage Docker Builds Explained](https://www.youtube.com/watch?v=zpkqNPwEzac) by Docker - Official build optimization guide

**Reference Documentation**:
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/) - Official Docker security guidelines
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html) - Comprehensive security checklist
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker) - Industry-standard security framework

### SRE Observability Fundamentals

**Essential Watching** (15 minutes):
- [Prometheus Metrics Best Practices](https://www.youtube.com/watch?v=67Ulrq6DxwA) by Prometheus Monitoring - Official metrics guidelines
- [The Four Golden Signals](https://www.youtube.com/watch?v=tEylFyxbDLE) by Google Cloud - SRE monitoring framework

**Reference Documentation**:
- [Google SRE Book - Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) - Foundational monitoring principles
- [Prometheus Best Practices](https://prometheus.io/docs/practices/naming/) - Metric naming and instrumentation
- [The Twelve-Factor App](https://12factor.net/) - Cloud-native application principles

### Key Concepts You'll Learn

**Multi-Stage Build Benefits** enable separation of build tools from runtime environment, reducing final image size by 60-80% while eliminating build-time security vulnerabilities. This pattern ensures production containers contain only essential runtime dependencies, minimizing attack surface and improving deployment speed.

**Container Security Hardening** requires non-root user execution to limit privilege escalation risks, minimal base images to reduce attack surface and vulnerability exposure, and read-only root filesystems to prevent runtime tampering. These practices implement defense-in-depth security architecture that protects against container escape and privilege escalation attacks.

**SRE Instrumentation from Day One** means applications expose Prometheus-compatible metrics endpoints for automated scraping, implement structured JSON logging for automated parsing and correlation, and provide health check endpoints that Kubernetes orchestration systems require for automated management, self-healing, and traffic routing decisions.

**Why This Matters for Production**: Container security is not optional in production environments. Compromised containers can lead to data breaches, lateral movement attacks, and cluster-wide security incidents. Proper instrumentation enables proactive monitoring, rapid troubleshooting, and data-driven operational decisions that maintain service reliability and availability.

---

## Understanding Production Container Design

Your Flask application has been pre-configured with comprehensive SRE instrumentation including Prometheus metrics collection, structured logging, and health check endpoints. The containerization process must preserve these capabilities while implementing security hardening that meets enterprise standards.

### Application Architecture Review

Navigate to the exercise directory and examine the application structure:
```bash
# Navigate to Exercise 1
cd exercises/exercise1

# Review application structure
tree app/ || ls -la app/
```

**Expected output:**
```
app/
├── __init__.py
├── config.py
└── main.py
```

### Step 1: Examine Application Configuration Management

Review how the application manages configuration across different environments:
```bash
# Review configuration management
cat app/config.py
```

**Configuration design principles:**
* **Environment-based configuration** allows the same code to run in development, staging, and production with different settings
* **Sensible defaults** ensure the application works in local development without configuration
* **Environment variable overrides** enable production configuration without code changes
* **Type safety and validation** prevent configuration errors at runtime

**Why this matters**: Proper configuration management is essential for containerized applications that deploy across multiple environments. Configuration must be externalized from code and injectable at runtime through environment variables or configuration files.

### Step 2: Examine SRE Instrumentation Implementation

Review the comprehensive observability implementation:
```bash
# Review main application code
cat app/main.py
```

**Key instrumentation components:**

**Prometheus Metrics Endpoint** (`/metrics`) exposes request counts, latencies, error rates, and business metrics in Prometheus text format that monitoring systems automatically scrape and store for alerting and dashboarding.

**Structured Logging** uses JSON format with contextual fields including timestamps, request IDs, user agents, and response codes that enable automated log aggregation, parsing, and correlation in centralized logging systems like CloudWatch Logs or ELK stack.

**Health Check Endpoints** provide Kubernetes liveness probes (`/health`) that trigger container restarts on application failure and readiness probes (`/ready`) that control traffic routing to healthy instances only.

**Business Logic Endpoints** demonstrate real-world application patterns including REST API design, error handling, data serialization, and request processing with full observability integration.

### Step 3: Test Application Locally (Optional)

Run the application locally to understand its behavior before containerization:
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python -m app.main
```

**In a new terminal, test the endpoints:**
```bash
# Test home endpoint
curl http://localhost:8080/

# Test health check
curl http://localhost:8080/health

# Test readiness check
curl http://localhost:8080/ready

# Test metrics endpoint
curl http://localhost:8080/metrics | head -30

# Test stores endpoint (business logic)
curl http://localhost:8080/stores
```

**Stop the application** with `Ctrl+C` when testing is complete.

**Understanding application behavior:** Local testing validates that the application functions correctly before containerization. This baseline ensures that any issues discovered during container testing are related to containerization, not application bugs.

---

## Building Multi-Stage Container Images

### Container Requirements Definition

Production containers must satisfy multiple operational requirements that balance security, performance, and maintainability:

**Security Requirements** include:
* Non-root execution context (UID 1000+) to limit privilege escalation
* Minimal base image (<100MB) to reduce attack surface
* No shell access to prevent interactive exploitation
* Read-only root filesystem compatibility
* No hardcoded secrets or credentials

**Operational Requirements** include:
* Preserved Prometheus metrics exposure on `/metrics`
* Continued structured logging output to stdout/stderr
* Functional health check endpoints for orchestration
* Efficient resource utilization with appropriate memory/CPU sizing
* Fast startup time (<10 seconds) for rapid scaling

**Build Efficiency Requirements** include:
* Layer caching optimization for rapid rebuilds during development
* Reproducible builds with pinned dependencies
* Multi-architecture support for diverse deployment targets
* Minimal build context to improve build speed

### Step 4: Examine the Multi-Stage Dockerfile

Review the production-grade Dockerfile implementing security and efficiency best practices:
```bash
# Examine Dockerfile structure
cat Dockerfile
```

**Multi-stage build architecture analysis:**

**Builder Stage** (Lines 1-15):
* Uses full Python image (`python:3.11-slim`) for dependency compilation
* Installs build tools for native extensions (gcc, python3-dev)
* Creates isolated dependency installation with `pip install --user`
* Generates optimized Python bytecode for improved performance
* Includes all build-time dependencies but none reach production

**Production Stage** (Lines 17-40):
* Uses minimal Python slim image (<50MB base)
* Copies only runtime dependencies from builder stage
* Creates non-root user `appuser` (UID 1000) for security
* Implements proper file ownership and permissions
* Exposes only necessary port 8080 with health checks
* Uses ENTRYPOINT for proper signal handling

**Why multi-stage builds matter**: Single-stage builds include all build tools and dependencies in the final image, increasing size from ~100MB to 500MB+ and expanding attack surface with unnecessary packages like gcc, make, and development headers that have no runtime purpose.

### Step 5: Review .dockerignore Configuration

Examine build context optimization:
```bash
# Review Docker ignore patterns
cat .dockerignore
```

**Build context exclusions:**
* **Version control artifacts** (`.git/`, `.gitignore`) prevent 50-100MB of unnecessary data
* **Python cache files** (`__pycache__/`, `*.pyc`) avoid stale bytecode
* **Development tools** (`.venv/`, `venv/`) exclude virtual environments
* **Documentation** (`*.md`, `docs/`) reduces context by 1-5MB
* **Test files** (`tests/`, `*.test`) exclude test infrastructure

**Impact on build performance**: Proper `.dockerignore` reduces build context from 200MB to 10MB, improving build time by 50-70% and preventing accidental inclusion of sensitive development files like `.env` or `.aws/credentials`.

### Step 6: Build the Container Image

Execute multi-stage build with security context:
```bash
# Build container image with appropriate tags
docker build -t devops-demo-app:v1.0.0 -t devops-demo-app:latest .
```

**Expected output:**
```
[+] Building 45.2s (17/17) FINISHED
 => [internal] load build definition from Dockerfile
 => [internal] load .dockerignore
 => [internal] load metadata for docker.io/library/python:3.11-slim
 => [builder 1/4] FROM docker.io/library/python:3.11-slim
 => [builder 2/4] WORKDIR /build
 => [builder 3/4] COPY requirements.txt .
 => [builder 4/4] RUN pip install --user --no-warn-script-location -r requirements.txt
 => [stage-1 1/8] FROM docker.io/library/python:3.11-slim
 => [stage-1 2/8] RUN groupadd -r appuser && useradd -r -g appuser -u 1000 appuser
 => [stage-1 3/8] WORKDIR /app
 => [stage-1 4/8] COPY --from=builder /root/.local /home/appuser/.local
 => [stage-1 5/8] COPY --chown=appuser:appuser app/ /app/
 => [stage-1 6/8] USER appuser
 => [stage-1 7/8] EXPOSE 8080
 => [stage-1 8/8] CMD ["python", "-m", "app.main"]
 => exporting to image
 => => naming to docker.io/library/devops-demo-app:v1.0.0
 => => naming to docker.io/library/devops-demo-app:latest
```

**Build process explanation:**
1. Docker downloads base Python image (cached after first build)
2. Builder stage installs all dependencies with build tools
3. Production stage copies only runtime artifacts
4. Security contexts (non-root user) are applied
5. Health check configuration is embedded
6. Final image is tagged with version and latest

**Monitor build output for:**
- ✅ Layer caching effectiveness (should show `CACHED` for unchanged layers)
- ✅ Final image size (should be <100MB)
- ✅ No security warnings or errors
- ✅ Successful tag creation

### Step 7: Analyze Image Security Profile

Examine the security characteristics of your built image:
```bash
# Inspect image layers and size
docker images devops-demo-app:v1.0.0

# Analyze image configuration
docker inspect devops-demo-app:v1.0.0 | jq '.[0].Config'

# Review security context
docker inspect devops-demo-app:v1.0.0 | jq '.[0].Config.User'

# Check exposed ports
docker inspect devops-demo-app:v1.0.0 | jq '.[0].Config.ExposedPorts'

# Review health check configuration
docker inspect devops-demo-app:v1.0.0 | jq '.[0].Config.Healthcheck'
```

**Expected analysis results:**
```bash
# Image size
REPOSITORY          TAG       IMAGE ID       CREATED          SIZE
devops-demo-app    v1.0.0    abc123def456   2 minutes ago    95.3MB
```

**Security verification checklist:**
- ✅ Non-root user configured (`appuser` UID 1000)
- ✅ Minimal base image (95MB vs 500MB+ for full Python)
- ✅ No shell binaries in production stage
- ✅ Read-only root filesystem compatible
- ✅ Health check configured for orchestration
- ✅ Only necessary port exposed (8080)

### Step 8: Review Image Layer Composition

Understand how layers contribute to final image size:
```bash
# Analyze layer composition
docker history devops-demo-app:v1.0.0 --no-trunc
```

**Layer analysis insights:**
* Base image layers (40-50MB) are shared across images
* Dependency installation (20-30MB) changes only when requirements.txt changes
* Application code (<1MB) changes frequently but has minimal impact
* Total size (90-100MB) is optimal for production deployment

---

## Implementing Container Security Contexts

### Step 9: Test Non-Root Execution

Verify container security contexts function correctly:
```bash
# Run container with security validation
docker run -d --name devops-app-test \
  --read-only \
  --tmpfs /tmp \
  --tmpfs /home/appuser/.local \
  --security-opt=no-new-privileges:true \
  --cap-drop=ALL \
  -p 8080:8080 \
  devops-demo-app:v1.0.0
```

**Security context parameters explained:**

* `--read-only`: Prevents runtime file modification for defense-in-depth
* `--tmpfs /tmp`: Provides ephemeral temporary storage (writable)
* `--tmpfs /home/appuser/.local`: Allows Python cache writes
* `--security-opt=no-new-privileges`: Blocks privilege escalation attacks
* `--cap-drop=ALL`: Removes all Linux capabilities (principle of least privilege)
* `-p 8080:8080`: Exposes only necessary application port

**Why these constraints matter**: Production container platforms like Amazon EKS enforce similar security constraints through Pod Security Standards. Testing locally validates compatibility before deployment.

### Step 10: Verify Security Constraints

Validate security controls are enforced:
```bash
# Verify non-root execution
docker exec devops-app-test whoami

# Check user ID
docker exec devops-app-test id

# Attempt filesystem write (should fail)
docker exec devops-app-test touch /test-file 2>&1 || echo "✅ Write blocked as expected"

# Verify process runs as appuser
docker exec devops-app-test ps aux
```

**Expected behavior:**
```
appuser
uid=1000(appuser) gid=1000(appuser) groups=1000(appuser)
touch: cannot touch '/test-file': Read-only file system
✅ Write blocked as expected
USER       PID  COMMAND
appuser      1  python -m app.main
```

**Security validation confirms:**
- ✅ Container runs as non-root user (appuser)
- ✅ Filesystem writes fail outside /tmp
- ✅ All processes execute with UID 1000
- ✅ No privilege escalation possible

---

## Integrating SRE Observability

### Step 11: Validate Observability Endpoints

Test comprehensive SRE instrumentation in the containerized application:
```bash
# Test health endpoint
curl http://localhost:8080/health

# Test readiness endpoint
curl http://localhost:8080/ready

# Test home endpoint
curl http://localhost:8080/

# Test Prometheus metrics endpoint
curl http://localhost:8080/metrics | head -30

# Test business logic endpoint
curl http://localhost:8080/stores
```

**Expected responses:**

**Health Endpoint:**
```json
{
  "checks": {
    "application": "ok",
    "disk": "ok",
    "memory": "ok"
  },
  "status": "healthy",
  "timestamp": 1735689123.456,
  "version": "1.0.0"
}
```

**Metrics Endpoint:**
```
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 234.0
# HELP http_requests_total Total number of HTTP requests
# TYPE http_requests_total counter
http_requests_total{endpoint="health",method="GET",status_code="200"} 3.0
```

### Step 12: Generate Traffic for Metric Observation

Create realistic traffic patterns to validate metrics collection:
```bash
# Generate diverse application traffic
for i in {1..20}; do
  curl -s http://localhost:8080/ > /dev/null
  curl -s http://localhost:8080/stores > /dev/null
  curl -s http://localhost:8080/health > /dev/null
  sleep 0.5
done

# Observe metric changes
curl -s http://localhost:8080/metrics | grep -E "(http_requests_total|business_operations_total)"
```

**Expected metric output:**
```
http_requests_total{endpoint="home",method="GET",status_code="200"} 20.0
http_requests_total{endpoint="get_stores",method="GET",status_code="200"} 20.0
http_requests_total{endpoint="health",method="GET",status_code="200"} 25.0
business_operations_total{operation="store_fetch",status="success"} 20.0
```

**Observability validation confirms:**
- ✅ Metrics increment correctly with each request
- ✅ Different endpoints tracked separately
- ✅ Business metrics captured alongside technical metrics
- ✅ Status codes properly labeled for error tracking

### Step 13: Analyze Structured Logging

Examine production-ready log output:
```bash
# View structured log output
docker logs devops-app-test

# Filter for specific log levels
docker logs devops-app-test | grep '"level":"INFO"'

# Analyze request patterns
docker logs devops-app-test | grep '"path":"/"'

# Check for errors
docker logs devops-app-test | grep '"level":"ERROR"'
```

**Expected structured log format:**
```json
{
  "event": "request_received",
  "timestamp": "2025-01-01T12:00:00.123Z",
  "level": "INFO",
  "method": "GET",
  "path": "/",
  "remote_addr": "172.17.0.1",
  "user_agent": "curl/7.81.0"
}
{
  "event": "request_completed",
  "timestamp": "2025-01-01T12:00:00.145Z",
  "level": "INFO",
  "method": "GET",
  "path": "/",
  "status_code": 200,
  "duration_ms": 22.3
}
```

**Structured logging benefits:**
* **JSON format** enables automated log parsing in CloudWatch Logs Insights
* **Contextual fields** support correlation analysis across distributed systems
* **Log levels** enable filtering and alerting based on severity
* **Timestamp precision** supports distributed tracing and request correlation

---

## Testing Container Security and Functionality

### Step 14: Execute Comprehensive Container Testing

Run the automated test script that validates all container requirements:
```bash
# Make test script executable
chmod +x scripts/test-container.sh

# Run comprehensive tests
./scripts/test-container.sh
```

**Expected test output:**
```
=== Container Security and Functionality Tests ===

✅ Container is running
✅ Container running as non-root user (appuser)
✅ Health endpoint responding
✅ Readiness endpoint responding
✅ Metrics endpoint responding
✅ Home endpoint responding
✅ Business logic endpoint responding
✅ Structured logging working
✅ Security constraints enforced

=== All Tests Passed ===
```

**What the test script validates:**
* Container startup and runtime health
* Non-root user execution
* All HTTP endpoints functional
* Prometheus metrics exposure
* Structured logging output
* Security constraint enforcement

### Step 15: Execute Container Security Scan

Perform vulnerability analysis using Trivy scanner:
```bash
# Install Trivy scanner (if not already installed)
# Ubuntu/Debian
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy

# Scan container image for vulnerabilities
trivy image devops-demo-app:v1.0.0
```

**Vulnerability assessment goals:**
* **Zero CRITICAL vulnerabilities** in production images
* **Minimal HIGH vulnerabilities** with documented exceptions
* **Current base image** using latest security patches
* **Updated dependencies** with no known exploits

**Expected scan results:**
```
devops-demo-app:v1.0.0 (debian 12.4)

Total: 15 (UNKNOWN: 0, LOW: 10, MEDIUM: 5, HIGH: 0, CRITICAL: 0)
```

**If vulnerabilities found:**
1. Update base image to latest Python 3.11 slim variant
2. Update dependencies in requirements.txt
3. Rebuild image and rescan
4. Document any accepted risks with justification

### Step 16: Validate Resource Efficiency

Measure container resource consumption:
```bash
# Monitor container resource usage
docker stats devops-app-test --no-stream

# Check image size efficiency
docker images | grep devops-demo-app

# Analyze layer composition
docker history devops-demo-app:v1.0.0 --human
```

**Expected resource metrics:**
```
CONTAINER ID   NAME              CPU %   MEM USAGE / LIMIT   MEM %   NET I/O     BLOCK I/O
abc123def456   devops-app-test   0.15%   42.5MiB / 7.77GiB   0.53%   2.5kB/2kB   0B/0B

REPOSITORY          TAG       SIZE
devops-demo-app    v1.0.0    95.3MB
devops-demo-app    latest    95.3MB
```

**Resource efficiency targets:**
- ✅ Image size <100MB (95.3MB actual)
- ✅ Memory baseline <64MB (42.5MB actual)
- ✅ CPU usage <5% at idle (0.15% actual)
- ✅ Fast startup time <10 seconds
- ✅ Layer count <15 for efficient caching

### Step 17: Clean Up Test Container

Remove test container after validation:
```bash
# Stop container
docker stop devops-app-test

# Remove container
docker rm devops-app-test

# Verify removal
docker ps -a | grep devops-app-test
```

---

## Final Objective

By completing this exercise, you should be able to demonstrate:

Your containerized application runs securely with non-root execution context (UID 1000) and read-only filesystem constraints while maintaining complete SRE observability through Prometheus metrics exposure at `/metrics`, structured JSON logging to stdout, and health check endpoints at `/health` and `/ready`.

The multi-stage build produces minimal images under 100MB that eliminate build-time dependencies and reduce attack surface by 70-80% compared to single-stage builds. Container security scanning with Trivy reveals zero CRITICAL vulnerabilities and minimal HIGH vulnerabilities in production images.

Security constraints including `--read-only`, `--security-opt=no-new-privileges`, and `--cap-drop=ALL` are enforced without breaking application functionality. Resource consumption remains under 64MB memory and 5% CPU at idle, enabling efficient cluster utilization.

The container image is production-ready for deployment to Amazon ECR and EKS with proper tagging strategy (version and latest tags) and comprehensive health check configuration for Kubernetes orchestration.

---

## Verification Questions

Test your understanding by answering these questions:

1. **What specific security benefits** does non-root user execution provide, and what attack vectors does it mitigate in containerized environments?

   **Expected understanding**: Non-root execution prevents container escape attacks that exploit kernel vulnerabilities, limits damage from application vulnerabilities by restricting filesystem access, and prevents privilege escalation through setuid binaries. If an attacker compromises the application, they gain only unprivileged user access rather than root.

2. **How does** the multi-stage build pattern reduce final image size, and what categories of files are excluded from production images?

   **Expected understanding**: Multi-stage builds separate builder stage (containing gcc, make, build tools, headers) from production stage (containing only runtime). Excluded categories include compilers, development libraries, build caches, documentation, and intermediate build artifacts. Typical reduction: 500MB single-stage to 95MB multi-stage.

3. **Why is** read-only root filesystem important for production containers, and what directories require write access for the application to function?

   **Expected understanding**: Read-only filesystem prevents malware from modifying binaries, blocks privilege escalation through file substitution, and ensures immutable infrastructure principles. Write access needed only for /tmp (temporary files), /home/appuser/.local (Python cache), and any explicit application data directories.

4. **What information** do the `/health` and `/ready` endpoints provide, and how do Kubernetes orchestration systems use these differently?

   **Expected understanding**: `/health` (liveness) checks if application is alive; Kubernetes restarts container if failing. `/ready` (readiness) checks if application can serve traffic; Kubernetes removes from service load balancer if failing but doesn't restart. Liveness=recovery action, Readiness=traffic routing.

5. **How would** you modify this Dockerfile to support multiple target environments (development, staging, production) with different configurations?

   **Expected understanding**: Use Docker build arguments (ARG) for environment selection, multi-stage builds with environment-specific stages, or external configuration injection via environment variables at runtime. Production approach: single image with runtime configuration through ConfigMaps/Secrets in Kubernetes.

---

## Troubleshooting

### Common Issues

**Build failures with dependency errors:**
```bash
# Clear Docker build cache
docker builder prune -af

# Rebuild without cache
docker build --no-cache -t devops-demo-app:v1.0.0 .
```

Verify `requirements.txt` contains valid package specifications and check network connectivity for PyPI access during build.

**Container exits immediately after start:**
```bash
# Review application logs
docker logs devops-app-test

# Check for Python import errors
docker run --rm devops-demo-app:v1.0.0 python -m app.main
```

Verify that all dependencies are installed and application code has no syntax errors.

**Health checks failing:**

Ensure Flask binds to `0.0.0.0` (not `127.0.0.1`) in `app/main.py`:
```python
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)  # Must bind to 0.0.0.0
```

Verify firewall rules allow port 8080 access and container is running with port mapping (`-p 8080:8080`).

**Permission denied errors:**
```bash
# Verify file ownership in image
docker run --rm devops-demo-app:v1.0.0 ls -la /app

# Check that appuser owns application files
docker run --rm devops-demo-app:v1.0.0 stat -c "%U:%G" /app/app/main.py
```

Confirm non-root user has read access to application files and write access to /tmp for temporary storage.

**Image size excessive (>150MB):**

Review Dockerfile for unnecessary packages:
```bash
# Check layer sizes
docker history devops-demo-app:v1.0.0 --human

# Identify large layers
docker history devops-demo-app:v1.0.0 --human | sort -k2 -h
```

Verify multi-stage build transfers only required artifacts and check .dockerignore excludes development files.

**Port conflict errors:**
```bash
# Check if port 8080 is already in use
sudo lsof -i :8080

# Kill conflicting process
sudo kill $(sudo lsof -t -i :8080)

# Or use a different port
docker run -d -p 8081:8080 devops-demo-app:v1.0.0
```

### Advanced Troubleshooting

**Debugging container internals:**
```bash
# Run container with shell access (if needed)
docker run --rm -it --entrypoint /bin/bash devops-demo-app:v1.0.0

# Check Python imports
docker run --rm devops-demo-app:v1.0.0 python -c "import app; print(app.__file__)"

# Verify dependencies installed
docker run --rm devops-demo-app:v1.0.0 pip list
```

**Analyzing security contexts:**
```bash
# Inspect detailed container configuration
docker inspect devops-app-test | jq '.[0].HostConfig.SecurityOpt'

# Verify user configuration
docker inspect devops-app-test | jq '.[0].Config.User'

# Check capabilities
docker inspect devops-app-test | jq '.[0].HostConfig.CapDrop'
```

**Network connectivity issues:**
```bash
# Test from within container
docker exec devops-app-test curl -I http://localhost:8080/health

# Check container networking
docker network inspect bridge

# Verify port mapping
docker port devops-app-test
```

---

## Next Steps

You have successfully created production-grade container images with comprehensive security hardening and SRE observability instrumentation. You've implemented multi-stage builds that optimize image size by 70-80%, configured non-root execution contexts that limit security risks, integrated Prometheus metrics and structured logging for operational visibility, and validated container security using automated vulnerability scanning with Trivy.

**Key Accomplishments:**
* ✅ Built secure, minimal container image (<100MB)
* ✅ Implemented non-root execution and read-only filesystem
* ✅ Integrated comprehensive SRE observability (metrics, logs, health checks)
* ✅ Validated security with vulnerability scanning
* ✅ Tested container functionality under security constraints

**Proceed to [Exercise 2: Terraform IaC - AWS Networking](../exercise2/)** where you will provision the foundational AWS networking infrastructure using Terraform including:
* VPC isolation with public/private subnet architecture
* Multi-AZ deployment for high availability
* NAT Gateway configuration for private subnet internet access
* Security group controls for defense-in-depth
* Network foundation for EKS cluster deployment

**Key Concepts to Remember**: 
* Container security is multi-layered requiring minimal images, non-root execution, and read-only filesystems
* Multi-stage builds dramatically reduce image size while maintaining build flexibility
* SRE observability must be implemented during containerization, not added later
* Automated security scanning should be integrated into every build pipeline to detect vulnerabilities early
* Production containers must balance security hardening with operational functionality

**Before Moving On**: 
Ensure you can explain:
* Why each security control (non-root, read-only, minimal image) matters for production deployments
* How multi-stage builds balance build convenience with production efficiency
* Why health checks are essential for Kubernetes orchestration
* How Prometheus metrics enable proactive monitoring and alerting

In Exercise 2, you'll provision the AWS networking infrastructure that will host your containerized applications in a production-grade EKS cluster.

---

*Container security and observability are foundational requirements for cloud-native applications, not optional enhancements.*