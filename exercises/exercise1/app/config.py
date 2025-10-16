"""
Configuration Management for SRE Application

Provides environment-based configuration with sensible defaults for local development
and environment variable overrides for production deployment.
"""

import os


class Config:
    """
    Application configuration with environment variable support.
    
    Configuration follows 12-factor app principles with all configuration
    externalized through environment variables and sensible defaults.
    """
    
    # Application Metadata
    APP_NAME = os.getenv("APP_NAME", "devops-demo-app")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")  # Must bind to 0.0.0.0 for container access
    PORT = int(os.getenv("PORT", "8080"))
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = os.getenv("LOG_FORMAT", "json")  # json or text
    
    # Observability Configuration
    METRICS_ENABLED = os.getenv("METRICS_ENABLED", "True").lower() in ("true", "1", "yes")
    HEALTH_CHECK_ENABLED = os.getenv("HEALTH_CHECK_ENABLED", "True").lower() in ("true", "1", "yes")
    
    # Business Logic Configuration (Demo)
    ENABLE_RANDOM_FAILURES = os.getenv("ENABLE_RANDOM_FAILURES", "True").lower() in ("true", "1", "yes")
    FAILURE_RATE = float(os.getenv("FAILURE_RATE", "0.1"))  # 10% failure rate for demo
    
    # Resource Limits (for health checks)
    MAX_MEMORY_MB = int(os.getenv("MAX_MEMORY_MB", "512"))
    MAX_CPU_PERCENT = int(os.getenv("MAX_CPU_PERCENT", "80"))
    
    @classmethod
    def validate(cls):
        """
        Validate configuration values are within acceptable ranges.
        
        Raises:
            ValueError: If configuration values are invalid
        """
        if not 1 <= cls.PORT <= 65535:
            raise ValueError(f"PORT must be between 1 and 65535, got {cls.PORT}")
        
        if not 0.0 <= cls.FAILURE_RATE <= 1.0:
            raise ValueError(f"FAILURE_RATE must be between 0.0 and 1.0, got {cls.FAILURE_RATE}")
        
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if cls.LOG_LEVEL.upper() not in valid_log_levels:
            raise ValueError(f"LOG_LEVEL must be one of {valid_log_levels}, got {cls.LOG_LEVEL}")
        
        valid_environments = ["development", "staging", "production"]
        if cls.ENVIRONMENT.lower() not in valid_environments:
            raise ValueError(f"ENVIRONMENT must be one of {valid_environments}, got {cls.ENVIRONMENT}")
    
    @classmethod
    def display(cls):
        """Display current configuration (safe for logging - no secrets)."""
        return {
            "app_name": cls.APP_NAME,
            "app_version": cls.APP_VERSION,
            "environment": cls.ENVIRONMENT,
            "host": cls.HOST,
            "port": cls.PORT,
            "debug": cls.DEBUG,
            "log_level": cls.LOG_LEVEL,
            "log_format": cls.LOG_FORMAT,
            "metrics_enabled": cls.METRICS_ENABLED,
            "health_check_enabled": cls.HEALTH_CHECK_ENABLED,
        }