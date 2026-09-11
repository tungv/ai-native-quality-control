# Public launch

The source tree is ready to place in a public GitHub repository. No remote URL or maintainer identity is assumed, and local initialization does not publish anything.

1. Create a public repository named `ai-native-quality-control` in the intended personal account or organization. Use the repository description: “Hands-on AI-native quality engineering: agents, tests, evaluation, retrieval, CI/CD, and security labs.” Do not add a second generated README or license.
2. Commit this source tree and push `main` to that remote. Inspect the staged files first; `reports`, local environment files, toolchains, and learner scratch work are ignored.
3. Verify both jobs in `.github/workflows/ci.yml` on GitHub. The workflow uses read-only repository permissions, SHA-pinned actions, hosted runners, and no model or cloud secrets. The database image is pinned by digest. Configure fork-workflow approval for first-time contributors in repository settings.
4. Enable private vulnerability reporting, dependency alerts, and discussions if maintainers can support them. Add real maintainers to `CODEOWNERS` once ownership is known. Protect `main` with review and the two passing CI job checks after their first run.
5. Add repository topics such as `quality-engineering`, `sdet`, `ai-testing`, `test-automation`, `prompt-injection`, and `learning`. Link the curriculum from the repository description or About section where useful.
6. Have a newcomer reproduce lab 00 from a clean checkout with only Docker and Compose installed, including image builds, baseline success, intended fault failures, host-visible reports, API health, and database teardown. Run `docker compose run --rm --build lab make verify`; no host Go, Python, or Make should be required. Record the tested revision and platform before calling a release stable.

The MIT license covers original repository material. Keep upstream licenses with any future dependencies, borrowed content, or datasets. Repository visibility does not require hosting the vulnerable lab services on the public internet.

For contributor workflows, avoid running untrusted fork code in a privileged `pull_request_target` job or adding deployment credentials to ordinary PR checks. The later delivery lab should use a separate trusted deployment lane with short-lived credentials, an isolated target, and verified cleanup. [GitHub Actions secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use)
