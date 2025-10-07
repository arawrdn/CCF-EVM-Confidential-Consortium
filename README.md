# CCF-EVM-Confidential-Consortium

This project implements a confidential ledger service using the **Confidential Consortium Framework (CCF)**. It enables mutually distrusting parties (a consortium) to compute and share data confidentially, leveraging **Trusted Execution Environments (TEEs)** for strong security guarantees.

A key innovation is the integration of an **EVM address** for enhanced member governance and identity binding.

## 🌟 Features

* **Hardware-Backed Confidentiality:** All application logic and data processing occurs within a TEE (e.g., Intel SGX), ensuring **data privacy** from node operators, cloud providers, and the underlying OS.
* **Auditable & Immutable Ledger:** All transactions and state changes are recorded in an append-only ledger, providing universal **verifiability and auditability**.
* **EVM Identity Binding (Admin):** The core administrative role is bound to a specific Ethereum Virtual Machine (EVM) address, adding an extra layer of non-repudiable identity proof for critical governance actions.
    * **Bound Admin EVM Address:** `0x2A6b5204B83C7619c90c4EB6b5365AA0b7d912F7`
* **High Performance:** Achieves database-like throughput via efficient consensus and the TEE architecture.
* **Programmable Governance:** Network changes (e.g., adding a member, updating the application) are managed through transparent, on-ledger proposal and voting by the consortium.

## 💻 Getting Started: Installation

### Prerequisites

* Linux operating system (Ubuntu 20.04/22.04 recommended)
* CCF build dependencies (Refer to the official CCF documentation for the complete list: `git`, `cmake`, `clang`, etc.)

### Steps

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/arawrdn/CCF-EVM-Confidential-Consortium.git](https://github.com/arawrdn/CCF-EVM-Confidential-Consortium.git)
    cd CCF-EVM-Confidential-Consortium
    ```

2.  **Install CCF Dependencies:**
    Ensure your environment is set up for CCF development (e.g., sourcing the relevant CCF environment script).

3.  **Build the Application:**
    The following command compiles the application logic and packages it for deployment.
    ```bash
    make build-app
    ```

## 🚀 Usage Guide

### 1. Starting the Local Network

This script starts a three-node CCF network locally, generating initial keys and certificates required for communication.

```bash
./infra/start_network.sh

Note: The script outputs the necessary files for client interaction, including the service certificate (service_cert.pem) and the initial member keys (member0_privk.pem, member0_cert.pem).

2. Member Governance (Using the Admin Key)
The initial consortium member (member0) holds the administrative power and is conceptually linked to the 0x2A6b5204B83C7619c90c4EB6b5365AA0b7d912F7 EVM address.

1. Activate the Service:
The service starts in a pending state and must be explicitly activated by the consortium (in this case, member0). This is the first official governance action.

./clients/client.py --action activate

2. Propose a Governance Change (e.g., Add a New Member):
This step requires the admin member to submit a proposal. In a real-world scenario with EVM binding, this transaction would require an extra parameter: a signature from the private key of the EVM admin address, verified inside the TEE.

# Step 2a: Propose adding a new member (requires new_member_cert.pem)
./clients/client.py --action propose_add_member --new_member_cert ./new_member_cert.pem

# Step 2b: Member0 votes to approve the proposal (assuming proposal ID 1)
./clients/client.py --action vote --proposal_id 1 --approve true

3. Governance Flow Notes (Advanced):
For critical actions, the CCF application logic (app/src/main.ts) checks the transaction's metadata. If the transaction relates to "admin" roles (like changing governance rules), the TEE logic requires proof: a cryptographic signature that verifies ownership of the bound EVM address (0x2A6b5204B83C7619c90c4EB6b5365AA0b7d912F7). This ensures strong accountability beyond the CCF keys alone.

## Confidential Data Transaction
Use the client script to send and retrieve data securely, utilizing the application logic running inside the TEE.

1. Submit Confidential Data:

# Data is encrypted on the wire and processed securely inside the TEE
./clients/client.py --action submit_data --data '{"price": 100, "volume": 500}'

2 Retrieve Aggregate Result:

# Retrieves a calculated (non-confidential) aggregate from the TEE
./clients/client.py --action get_aggregate
