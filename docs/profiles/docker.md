# Docker profile

- Use multi-stage builds.
- Pin base images by digest for release builds.
- Run as a non-root user.
- Keep build secrets out of layers and logs.
- Include health checks appropriate to orchestration.
- Use `.dockerignore`.
- Separate build-time and runtime dependencies.
- Scan images and generate an SBOM.
- Support graceful shutdown and fast startup.
- Never bake environment-specific configuration into the image.
