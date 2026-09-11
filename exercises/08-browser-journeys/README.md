# Lab 08 — Extend the playground with browser journeys

**Status:** Extension assignment. A Next.js storefront must be implemented or connected before browser testing can be claimed. **Prerequisites:** Lab 02, basic TypeScript/HTML, and the Go service contract. **Outcome:** A small browser surface with meaningful journey and accessibility evidence.

## Brief

Build or connect a minimal storefront that lists and searches the existing products, shows a product's price and stock state, and offers the assistant. Keep the product small enough that a QC engineer can inspect the full request path.

## Tasks

1. Write acceptance criteria before asking an agent to build or test the UI. Include USD price formatting from cents, empty results, invalid product navigation, failed requests, loading, keyboard operation, and the assistant's citation/action presentation.
2. Implement or connect the browser app in a reviewed change. Document setup, ports, API configuration, reset, shutdown, and test commands. Keep the Docker-first workflow: provide any Node/browser runtime in a separate container image. The existing lab container has external networking disabled and is not a browser-extension runner. Start the API from a host terminal with `docker compose up --build -d --wait api`; define networking explicitly if adding a frontend container. Do not assume authentication, cart, checkout, or real payments exist; those require separate contracts and implementation.
3. Add one real browser journey against the running API and a small set of isolated UI checks for edge states. State which requests are real and which are mocked.
4. Prefer user-visible roles and labels for interaction. Use deliberate test identifiers when needed; avoid sleeps or selectors tied unnecessarily to layout internals.
5. Test a narrow viewport and keyboard-only traversal. Combine automated accessibility checks with manual inspection of focus order, visible focus, and understandable errors. Record the scope; an automated pass alone is not a complete accessibility review.
6. Show that the price-rounding defect is visible or detected at the browser boundary. Use a controlled local fault and restore the baseline.
7. Add useful browser failure evidence to CI in your fork. Ensure screenshots, traces, and logs contain only synthetic data.

## Evidence and completion

Submit the app/test diff, documented commands, one recorded real-API journey, edge-state assertions, accessibility findings, and fault/restored evidence. A test running solely against mocks cannot demonstrate integration with the Go service.

**Cleanup:** Stop the UI using its documented command, stop the starter API with host-side `docker compose down`, restore faults, and remove generated artifacts that should not be committed.

**Stretch:** Add a documented order-creation mock with an idempotency rule and test a double-submit journey across browser and API. Keep it disconnected from real commerce systems.
