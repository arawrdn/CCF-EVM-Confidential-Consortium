# Contributing to CCF-EVM-Confidential-Consortium

We welcome contributions! By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How Can I Contribute?

There are several ways to contribute, beyond just writing code:

1.  **Reporting Bugs:** If you find a bug, please create an issue with clear steps to reproduce the problem and the observed behavior.
2.  **Suggesting Enhancements:** Propose new features or improvements by creating an issue. Clearly articulate the problem you are solving and why the enhancement is needed.
3.  **Writing Documentation:** Improving the documentation (in the `README.md` or dedicated `docs/` folder) is always appreciated.
4.  **Submitting Pull Requests (PRs):** Follow the guidelines below for code contributions.

## Pull Request Guidelines

Before submitting a Pull Request, please ensure the following:

1.  **Fork the repository** and clone it locally.
2.  **Create a new branch** from `main` for your changes (e.g., `feature/add-evm-check` or `bugfix/fix-client-bug`).
3.  **Follow Coding Standards:** Ensure your TypeScript/JavaScript code adheres to the existing style.
4.  **Test Your Changes:**
    * Ensure all existing tests pass.
    * Write new unit tests for any new features or bug fixes.
    * Verify the CCF network runs correctly (`./infra/start_network.sh`).
5.  **Commit Messages:** Use clear and descriptive commit messages (e.g., "FEAT: Implement EVM signature verification in governance").
6.  **Submit the PR:** Target the `main` branch. In the PR description, clearly reference any related issues and explain the motivation for the change.

## Code Structure Notes (CCF Specific)

* **Application Logic:** Changes to the core functionality must reside in the `app/src/` directory (TypeScript/JavaScript). This code runs inside the **TEE** and must be rigorously tested for security and correctness.
* **Client Interactions:** Client examples and wrappers should be updated in the `clients/` directory.
* **Governance:** Any changes to the governance logic (member roles, voting quorum) must be formally documented, as they affect the core trust model of the consortium.

Thank you for helping make this a robust and secure framework!
