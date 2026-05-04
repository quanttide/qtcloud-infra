FROM node:20-alpine

ENV OPENCODE_VERSION=v1.2.27

RUN apk add --no-cache curl \
    && curl -fsSL -o /tmp/opencode-linux-x64-musl.tar.gz https://github.com/anomalyco/opencode/releases/download/${OPENCODE_VERSION}/opencode-linux-x64-musl.tar.gz \
    && tar -xzf /tmp/opencode-linux-x64-musl.tar.gz -C /usr/local/bin/ \
    && rm /tmp/opencode-linux-x64-musl.tar.gz \
    && chmod +x /usr/local/bin/opencode \
    && mkdir -p /root/.local/share/opencode

WORKDIR /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 9000

ENTRYPOINT ["/entrypoint.sh"]
