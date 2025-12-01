FROM --platform=${BUILDPLATFORM} node:20 AS build

WORKDIR /opt/node_app

COPY . .

# do not ignore optional dependencies:
# Error: Cannot find module @rollup/rollup-linux-x64-gnu
RUN --mount=type=cache,target=/root/.cache/yarn \
    npm_config_target_arch=${TARGETARCH} yarn --network-timeout 600000

ARG NODE_ENV=production

RUN cd excalidraw-app && VITE_APP_DISABLE_SENTRY=true VITE_APP_ENABLE_PWA="" yarn vite build

FROM --platform=${TARGETPLATFORM} nginx:1.27-alpine

COPY --from=build /opt/node_app/excalidraw-app/build /usr/share/nginx/html

# Copy nginx configuration
COPY excalidraw-app/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 8765

HEALTHCHECK CMD wget -q -O /dev/null http://localhost:8765 || exit 1
