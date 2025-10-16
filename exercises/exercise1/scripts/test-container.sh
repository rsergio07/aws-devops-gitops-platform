#!/bin/bash

# =============================================================================
# Container Security and Functionality Test Script
# =============================================================================
# This script validates that the containerized application meets all
# production requirements including security, functionality, and observability.
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test configuration
CONTAINER_NAME="devops-app-test"
IMAGE_NAME="devops-demo-app:v1.0.0"
HOST_PORT="8080"
CONTAINER_PORT="8080"

# =============================================================================
# Helper Functions
# =============================================================================

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

cleanup() {
    print_info "Cleaning up test container..."
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
}

# =============================================================================
# Pre-Test Setup
# =============================================================================

echo "=== Container Security and Functionality Tests ==="
echo ""

# Cleanup any existing test container
cleanup

# =============================================================================
# Test 1: Image Exists
# =============================================================================

print_info "Test 1: Checking if image exists..."
if docker images "$IMAGE_NAME" | grep -q "devops-demo-app"; then
    print_success "Image exists"
else
    print_error "Image not found. Run 'docker build -t $IMAGE_NAME .' first"
    exit 1
fi

# =============================================================================
# Test 2: Container Starts Successfully
# =============================================================================

print_info "Test 2: Starting container with security constraints..."
docker run -d \
    --name "$CONTAINER_NAME" \
    --read-only \
    --tmpfs /tmp \
    --tmpfs /home/appuser/.local \
    --security-opt=no-new-privileges:true \
    --cap-drop=ALL \
    -p "$HOST_PORT:$CONTAINER_PORT" \
    "$IMAGE_NAME"

sleep 5  # Wait for application startup

if docker ps | grep -q "$CONTAINER_NAME"; then
    print_success "Container is running"
else
    print_error "Container failed to start"
    docker logs "$CONTAINER_NAME"
    cleanup
    exit 1
fi

# =============================================================================
# Test 3: Non-Root User Execution
# =============================================================================

print_info "Test 3: Verifying non-root execution..."
USER=$(docker exec "$CONTAINER_NAME" whoami)
if [ "$USER" = "appuser" ]; then
    print_success "Container running as non-root user (appuser)"
else
    print_error "Container running as $USER (should be appuser)"
    cleanup
    exit 1
fi

# =============================================================================
# Test 4: Health Endpoint
# =============================================================================

print_info "Test 4: Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" http://localhost:"$HOST_PORT"/health)
HTTP_CODE=$(echo "$HEALTH_RESPONSE" | tail -n 1)
BODY=$(echo "$HEALTH_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "200" ]; then
    if echo "$BODY" | grep -q '"status":"healthy"'; then
        print_success "Health endpoint responding correctly"
    else
        print_error "Health endpoint response unexpected: $BODY"
        cleanup
        exit 1
    fi
else
    print_error "Health endpoint returned HTTP $HTTP_CODE"
    cleanup
    exit 1
fi

# =============================================================================
# Test 5: Readiness Endpoint
# =============================================================================

print_info "Test 5: Testing readiness endpoint..."
READY_RESPONSE=$(curl -s -w "\n%{http_code}" http://localhost:"$HOST_PORT"/ready)
HTTP_CODE=$(echo "$READY_RESPONSE" | tail -n 1)
BODY=$(echo "$READY_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "503" ]; then
    if echo "$BODY" | grep -q '"status"'; then
        print_success "Readiness endpoint responding"
    else
        print_error "Readiness endpoint response unexpected: $BODY"
        cleanup
        exit 1
    fi
else
    print_error "Readiness endpoint returned unexpected HTTP $HTTP_CODE"
    cleanup
    exit 1
fi

# =============================================================================
# Test 6: Metrics Endpoint
# =============================================================================

print_info "Test 6: Testing metrics endpoint..."
METRICS_RESPONSE=$(curl -s http://localhost:"$HOST_PORT"/metrics)

if echo "$METRICS_RESPONSE" | grep -q "http_requests_total"; then
    print_success "Metrics endpoint responding with Prometheus format"
else
    print_error "Metrics endpoint not returning expected data"
    cleanup
    exit 1
fi

# =============================================================================
# Test 7: Home Endpoint
# =============================================================================

print_info "Test 7: Testing home endpoint..."
HOME_RESPONSE=$(curl -s -w "\n%{http_code}" http://localhost:"$HOST_PORT"/)
HTTP_CODE=$(echo "$HOME_RESPONSE" | tail -n 1)
BODY=$(echo "$HOME_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "200" ]; then
    if echo "$BODY" | grep -q '"message"'; then
        print_success "Home endpoint responding"
    else
        print_error "Home endpoint response unexpected"
        cleanup
        exit 1
    fi
else
    print_error "Home endpoint returned HTTP $HTTP_CODE"
    cleanup
    exit 1
fi

# =============================================================================
# Test 8: Business Logic Endpoint
# =============================================================================

print_info "Test 8: Testing business logic endpoint..."
STORES_RESPONSE=$(curl -s -w "\n%{http_code}" http://localhost:"$HOST_PORT"/stores)
HTTP_CODE=$(echo "$STORES_RESPONSE" | tail -n 1)
BODY=$(echo "$STORES_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "503" ]; then
    if echo "$BODY" | grep -q '"stores"' || echo "$BODY" | grep -q '"error"'; then
        print_success "Business logic endpoint responding"
    else
        print_error "Business logic endpoint response unexpected"
        cleanup
        exit 1
    fi
else
    print_error "Business logic endpoint returned unexpected HTTP $HTTP_CODE"
    cleanup
    exit 1
fi

# =============================================================================
# Test 9: Structured Logging
# =============================================================================

print_info "Test 9: Verifying structured logging..."
LOGS=$(docker logs "$CONTAINER_NAME" 2>&1)

if echo "$LOGS" | grep -q '"event"'; then
    if echo "$LOGS" | grep -q '"timestamp"'; then
        print_success "Structured logging working"
    else
        print_error "Logs missing timestamp field"
        cleanup
        exit 1
    fi
else
    print_error "Logs not in JSON format"
    cleanup
    exit 1
fi

# =============================================================================
# Test 10: Security Constraints
# =============================================================================

print_info "Test 10: Testing security constraints..."

# Test read-only filesystem
docker exec "$CONTAINER_NAME" touch /test-file 2>&1 | grep -q "Read-only file system"
if [ $? -eq 0 ]; then
    print_success "Read-only filesystem enforced"
else
    print_error "Read-only filesystem not enforced"
    cleanup
    exit 1
fi

# Test user ID
UID=$(docker exec "$CONTAINER_NAME" id -u)
if [ "$UID" = "1000" ]; then
    print_success "Running with correct UID (1000)"
else
    print_error "Running with incorrect UID ($UID, expected 1000)"
    cleanup
    exit 1
fi

# =============================================================================
# Test Summary
# =============================================================================

echo ""
echo "=== All Tests Passed ==="
echo ""
print_info "Container security and functionality validated successfully"
print_info "Container meets production requirements:"
print_success "  • Runs as non-root user"
print_success "  • Read-only filesystem enforced"
print_success "  • All HTTP endpoints functional"
print_success "  • Prometheus metrics exposed"
print_success "  • Structured logging enabled"
print_success "  • Health checks working"
echo ""

# =============================================================================
# Cleanup
# =============================================================================

print_info "Cleaning up test container..."
cleanup
print_success "Cleanup complete"

echo ""
echo "=== Test Suite Complete ===" 
echo ""
print_info "Image is ready for deployment to container registry"