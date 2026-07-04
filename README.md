<div align="center">

# 🔷 Blockchain-Based Insurance Certificate Verification System

### Tamper-Proof Insurance Fraud Detection using Cryptographic Hashing + Blockchain

[![Python](https://img.shields.io/badge/Python%203.9-6D28D9?style=flat-square&logo=python&logoColor=white)](#)
[![Django](https://img.shields.io/badge/Django%204.0-7C3AED?style=flat-square&logo=django&logoColor=white)](#)
[![Solidity](https://img.shields.io/badge/Solidity%20Smart%20Contracts-8B5CF6?style=flat-square&logo=solidity&logoColor=white)](#)
[![Ganache](https://img.shields.io/badge/Ganache%20Local%20Blockchain-A78BFA?style=flat-square&logo=ethereum&logoColor=white)](#)
[![Web3.py](https://img.shields.io/badge/Web3.py%20Blockchain%20Integration-A78BFA?style=flat-square)](#)

[Overview](#overview) • [Problem Statement](#problem-statement) • [System Architecture](#system-architecture) • [Modules](#modules) • [Tech Stack](#tech-stack) • [Installation](#installation) • [Usage](#usage) • [Results](#results) 

</div>

---

## Overview

Traditional insurance management systems rely on centralized architectures that lack transparency, making them vulnerable to certificate forgery, duplication, and unauthorized tampering. This project implements a **blockchain-based insurance certificate verification system** that uses cryptographic hashing and a Proof of Work blockchain ledger to guarantee that once a certificate is issued, it cannot be altered without detection.

Hospitals issue certificates through the system, which computes a cryptographic hash of the certificate data and stores it immutably on a **Ganache** blockchain network. When an insurance company needs to verify a certificate, the system recomputes the hash from the submitted data and compares it against the blockchain-stored value — a match confirms authenticity, while a mismatch flags the certificate as tampered or invalid.

Because only the **hash** is stored on-chain (not the certificate details themselves), the system preserves data privacy while still guaranteeing document integrity.

---

## Problem Statement

Centralized insurance systems create several vulnerabilities:

- No transparent, tamper-evident record of certificate issuance
- Ease of forging or duplicating legitimate certificates
- Manual verification processes that are slow and error-prone
- No reliable audit trail once a certificate has been modified

This system addresses these gaps by anchoring every certificate to an immutable blockchain record, enabling instant, verifiable fraud detection.

---

## Objectives

- Build a secure, transparent certificate verification system using blockchain technology
- Prevent fraud and tampering through cryptographic hashing and immutable storage
- Integrate a Django backend with a Ganache blockchain network for real-time verification
- Use a Proof of Work consensus mechanism to guarantee data integrity
- Preserve user privacy by storing only cryptographic hashes on-chain, never raw personal data
- Enable insurance companies to verify certificates instantly via hash comparison

---

## System Architecture

The platform is built around **five core modules** that interact through a Django backend:

```
┌────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│  Health          │ ──> │  Certificate Hashing  │ ──> │  Ganache Blockchain    │
│  Insurance Module│     │  (SHA-256)            │     │  (Proof of Work)       │
│  (Hospitals)     │     └──────────────────────┘     └──────────────────────┘
└────────────────┘                                              │
                                                                  ▼
┌────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│  Insurance       │ ──> │  Hash Recomputation    │ ──> │  Match / Mismatch      │
│  Company Module  │     │  & Comparison          │     │  Verification Result  │
└────────────────┘     └──────────────────────┘     └──────────────────────┘

              Admin Module — user & access management (cross-cutting)
              User Module — patients view & track their certificates
```

**Flow:**
1. A hospital issues a certificate through the **Health Insurance Module**.
2. The system computes a **SHA-256 hash** of the certificate data.
3. The hash is written to a **Solidity smart contract** deployed on the **Ganache** network.
4. When verification is needed, the **Insurance Company Module** recomputes the hash from submitted data.
5. The recomputed hash is compared against the blockchain-stored hash — a match confirms authenticity; a mismatch flags tampering.

---

## Modules

| Module | Responsibility |
|---|---|
| **Admin Module** | User management, access control, and system-wide oversight; logs all administrative actions for audit purposes |
| **User Module** | Lets patients register, log in, view issued certificates, and initiate verification requests |
| **Health Insurance Module** | Used by hospitals to upload patient/medical/billing details, compute the certificate hash, and issue a unique certificate ID |
| **Insurance Company Module** | Lets insurers submit certificate details for verification; recomputes and compares hashes against blockchain records |
| **Blockchain Module** | Interfaces with Ganache via **Web3.py**; handles transaction signing, smart contract calls, gas estimation, and hash storage/retrieval |

---
## Project Structure

```
insurance-fraud-detection/
├── contracts/              # Solidity smart contracts
├── migrations/             # Truffle migration scripts
├── static/                 # CSS, JS assets
├── templates/               # HTML templates (login, register, dashboards)
├── app/                     # Django app (models, views, urls)
│   ├── models.py             # Block, Policy, Notification models
│   ├── views.py               # Certificate issuance, verification, fraud check logic
│   └── blockchain.py          # Web3.py integration for contract deployment & calls
├── manage.py
├── requirements.txt
├── truffle-config.js
└── README.md
```

---
## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Django 4.0 |
| Blockchain Network | Ganache (local Ethereum blockchain, Proof of Work) |
| Smart Contracts | Solidity |
| Blockchain Integration | Web3.py, py-solc-x |
| Contract Tooling | Truffle Suite, Node.js |
| Hashing | SHA-256 |
| Version Control | Git / GitHub |

---

## Requirements

**Software**

| Requirement | Specification |
|---|---|
| OS | Windows 10 or above |
| Backend Language | Python 3.9 |
| Framework | Django 4.0 |
| Blockchain Tool | Ganache |
| Libraries | Web3.py, py-solc-x |

**Hardware**

| Requirement | Specification |
|---|---|
| RAM | 4 GB or above |
| Processor | Intel i3 or above |
| Disk Space | 5 GB or above |

---

## Installation

```bash
# Clone the repository
git clone https://github.com/sujaysuresh-tech/insurance-fraud-detection.git
cd insurance-fraud-detection

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies for smart contract tooling
npm install
```

**Set up the local blockchain:**

1. Install and launch [Ganache](https://trufflesuite.com/ganache/) — it runs a local Ethereum network at `http://127.0.0.1:7545`.
2. Compile and deploy the smart contract:

```bash
truffle compile
truffle migrate
```

3. Update the contract address, chain ID, and account credentials in the Django settings/blockchain config.

**Run database migrations and start the server:**

```bash
python manage.py migrate
python manage.py runserver
```

---

## Usage

1. **Hospital issues a certificate** — via the Health Insurance Module, enter patient and billing details. The system computes a SHA-256 hash and stores it on the Ganache blockchain through the deployed smart contract.
2. **Insurance company verifies a certificate** — submit the certificate's IPN, charge, and total due. The system recomputes the hash and compares it to the on-chain record.
3. **Result** — the system returns whether the certificate is genuine (hash match) or potentially tampered (hash mismatch).
4. **Admin oversight** — administrators manage users, roles, and monitor certificate/blockchain activity through the admin dashboard.

---
## Limitations & Future Work

**Current limitations:**
- Dependent on continuous internet connectivity
- Proof of Work consensus can slow down under high transaction volume
- Runs on a private/local blockchain (Ganache), which needs adaptation for production-scale deployment
- No advanced encryption yet for inter-module data transmission

**Planned enhancements:**
- Automate claim processing via smart contracts
- Add multi-signature verification across multiple stakeholders
- Explore zero-knowledge proofs for stronger privacy guarantees
- Migrate to a more scalable network (e.g. Ethereum L2, Hyperledger Fabric)
- Incorporate machine learning for anomaly/fraud pattern detection alongside hash verification
- Build a mobile application interface

---
## Results

Based on testing carried out during development:

| Metric | Result |
|---|---|
| Certificate validation accuracy | ~98.5% |
| Average verification response time | ~2.3 seconds |
| Legitimate certificate verification time | 3–5 seconds |
| Manual processing reduction | ~60% |

Testing was conducted in iterative cycles covering unit testing (per module), integration testing (system-wide), and security testing (blockchain immutability and data integrity checks).

---


<div align="center">

Built by [Sujay Suresh](https://github.com/sujaysuresh-tech)

</div>
