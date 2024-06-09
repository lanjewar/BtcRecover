import mnemonic
import bip32utils
import requests
import logging
import time
import multiprocessing
from pybloom_live import BloomFilter

def generate_mnemonic():
    mnemo = mnemonic.Mnemonic("english")
    return mnemo.generate(strength=128)

def recover_wallet_from_mnemonic(mnemonic_phrase, rich_bloom):
    seed = mnemonic.Mnemonic.to_seed(mnemonic_phrase)
    root_key = bip32utils.BIP32Key.fromEntropy(seed)
    child_key = root_key.ChildKey(44 | bip32utils.BIP32_HARDEN).ChildKey(0 | bip32utils.BIP32_HARDEN).ChildKey(0 | bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0)
    address = child_key.Address()
    if address in rich_bloom:
        balance = check_BTC_balance(address)
        return mnemonic_phrase, balance, address
    return mnemonic_phrase, 0, address

def check_BTC_balance(address, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = requests.get(f"https://blockchain.info/balance?active={address}", timeout=10)
            response.raise_for_status()
            data = response.json()
            balance = data[address]["final_balance"]
            return balance / 100000000
        except requests.RequestException as e:
            if attempt < retries - 1:
                logging.error(f"Error checking balance, retrying in {delay} seconds: {str(e)}")
                time.sleep(delay)
            else:
                logging.error("Error checking balance: %s", str(e))
    return 0

def read_rich_addresses(filename):
    # Significantly increase capacity to handle much larger number of addresses
    rich_bloom = BloomFilter(capacity=50000000, error_rate=0.001)
    with open(filename, 'r') as file:
        for line in file:
            rich_bloom.add(line.strip())
    return rich_bloom

def check_mnemonic(rich_bloom, total_checked, found_count):
    while True:
        mnemonic_phrase = generate_mnemonic()
        total_checked.value += 1
        full_mnemonic, balance, address = recover_wallet_from_mnemonic(mnemonic_phrase, rich_bloom)
        if balance > 0:
            with total_checked.get_lock():
                found_count.value += 1
            with open("wallet.txt", "a") as f:
                f.write(f"Mnemonic Phrase: {full_mnemonic}\n")
                f.write(f"Wallet Address: {address}\n")
                f.write(f"Balance: {balance} BTC\n\n")

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    rich_bloom = read_rich_addresses("rich2.txt")

    # Use 80% of the available CPU cores
    num_cores = multiprocessing.cpu_count()
    num_processes = max(1, int(num_cores * 0.8))

    # Shared counters
    manager = multiprocessing.Manager()
    total_checked = manager.Value('i', 0)
    found_count = manager.Value('i', 0)

    # Create a pool of processes
    pool = multiprocessing.Pool(processes=num_processes)
    
    try:
        # Start the processes
        for _ in range(num_processes):
            pool.apply_async(check_mnemonic, args=(rich_bloom, total_checked, found_count))
        
        # Monitor progress
        while True:
            time.sleep(10)
            logging.info(f"Total checked: {total_checked.value}, Matches found: {found_count.value}")
    except KeyboardInterrupt:
        logging.info("Interrupted by user")
    finally:
        pool.terminate()
        pool.join()

if __name__ == "__main__":
    main()
