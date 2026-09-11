# The lab includes the native toolchain; learners only need Docker on the host.
FROM golang:1.27.1-bookworm@sha256:648f440f42a0958804efb24df176f806f9d353b41f1c0627f666428e40310f6b AS toolchain

# gcc enables Go's race detector. Package versions follow Debian's security
# repository; base-image digests are pinned, but apt packages are not frozen.
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 make gcc git \
    && rm -rf /var/lib/apt/lists/*
RUN git config --system --add safe.directory /workspace

ENV GOCACHE=/tmp/go-build \
    GOMODCACHE=/tmp/go-mod \
    GOTOOLCHAIN=local \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /workspace
COPY .go-version /tmp/expected-go-version
RUN test "$(go env GOVERSION)" = "go$(cat /tmp/expected-go-version)"

# Run the checked-in suite or enter a shell. Compose mounts the working tree
# over this copy so edits and reports are visible without rebuilding the image.
FROM toolchain AS lab
COPY --chown=1000:1000 . /workspace
USER 1000:1000
CMD ["make", "verify"]

# Compile a static binary for the minimal, non-root runtime image.
FROM toolchain AS api-build
WORKDIR /src
COPY services/catalog-api/ ./
RUN CGO_ENABLED=0 go build -trimpath -o /out/catalog-api .

FROM alpine:3.23@sha256:fd791d74b68913cbb027c6546007b3f0d3bc45125f797758156952bc2d6daf40 AS api
COPY --from=api-build /out/catalog-api /usr/local/bin/catalog-api
USER 65532:65532
ENV LISTEN_ADDR=0.0.0.0:8080
EXPOSE 8080
HEALTHCHECK --interval=2s --timeout=3s --start-period=3s --retries=15 \
    CMD ["wget", "-q", "-O", "/dev/null", "http://127.0.0.1:8080/health"]
ENTRYPOINT ["/usr/local/bin/catalog-api"]
