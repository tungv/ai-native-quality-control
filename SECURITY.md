# Security policy

This is an educational playground. Test only local fixtures, your own isolated deployments, or systems for which you have explicit authorization. Use synthetic identities, products, orders, credentials, and documents.

The default reference baseline must pass its security assertions. Deliberately vulnerable scenarios must require explicit selection, contain no real credentials, and remain local. A passing deterministic prompt-injection exercise is not evidence that a real model is resistant to injection.

Do not publish private data or usable secrets in an issue or pull request. For a vulnerability affecting the repository tooling, use the repository's **Security → Report a vulnerability** feature if enabled. If unavailable, open an issue requesting a private reporting channel without exploit details or sensitive data. Maintainers should enable private vulnerability reporting before public launch.

See [security testing](docs/security-testing.md) for the threat model, permitted lab targets, and evidence requirements. Educational vulnerabilities in opt-in scenarios should be reported as lab defects unless they escape the documented isolation boundary.
