# Bitcoin Wallet Recovery Tool



## Overview

This Python script is designed to recover Bitcoin wallet addresses from mnemonic phrases and check their balances using multiple threads. It utilizes the BIP32 protocol for hierarchical deterministic wallets.

## Disclaimer
⚠️ Disclaimer ⚠️

This script is developed for educational and research purposes only.

By using this code, you agree to the following:

- You will not use this code, in whole or in part, for malicious intent, including but not limited to unauthorized mining on third-party systems.
- You will seek explicit permission from any and all system owners before running or deploying this code.
- You understand the implications of running mining software on hardware, including the potential for increased wear and power consumption.
- The creator of this script cannot and will not be held responsible for any damages, repercussions, or any negative outcomes that result from using this script.
- If you do not agree to these terms, please do not use or distribute this code.


## Features

- **Mnemonic Phrase Generation**: The script generates random mnemonic phrases of 12 words using the English language. You need to privide the source file of mnemonic words.
- **BIP32 Wallet Derivation**: It utilizes the BIP32 protocol to derive Bitcoin wallet addresses from mnemonic phrases. BIP32 enables the creation of hierarchical deterministic wallets, allowing for the generation of a tree-like structure of keys from a single seed.
- **Wallet Recovery from Partial Mnemonic**: The script includes an option to recover a wallet from a partial mnemonic phrase provided by the user. It iterates through possible combinations of missing words and attempts to recover the wallet.

## Prerequisites

- Python 3.x
- Required Python packages: `mnemonic`, `bip32utils`, `requests`

## Installation

1. Clone the repository or download the source code.
2. Navigate to the project directory.
3. Install the required packages using pip:

```
pip install -r requirements.txt
```


## Usage

1. Run the `BtcRecover.py` script:

```
python BtcRecover.py
```

2. Follow the on-screen prompts to choose between recovering a wallet from a partial mnemonic or checking wallets form the source file of the provided wallet address.
3. If a wallet with a non-zero balance is found, the script will log the mnemonic phrase, wallet address, and balance to the `wallet.txt` file.

