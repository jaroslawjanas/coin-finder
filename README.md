<p align="center">
  <img src="https://i.imgur.com/SvxWJIh.png" alt="CoinFinder">
</p>

## What Is This Madness?

This is a cryptographic experiment- or perhaps a cosmic joke - that attempts to find Ethereum private keys with positive balances through pure brute-force random generation. The goal? To randomly stumble upon someone's wallet by generating private keys, deriving their addresses, and checking if they hold any ETH.

Spoiler alert: you won't find anything. But that's exactly the point.

## The Real Purpose: Demonstrating Cryptographic Security

This project serves as a practical demonstration of why blockchain cryptography works. Ethereum (and similar blockchains) rely on the mathematical near-impossibility of finding a valid private key through random guessing. When people say "your crypto wallet is secure," this is what they mean - not that it's theoretically impossible to guess, but that the probability is so astronomically small that it might as well be impossible.

Unlike real-world attacks that exploit:
- Weak random number generators
- Brain wallets (human-chosen phrases like "password123")
- Implementation bugs or protocol vulnerabilities
- Reused nonces or signature flaws

...this project uses pure, unbiased random generation against properly implemented cryptography. It's the digital equivalent of trying to find a specific grain of sand on all the beaches in the universe, while blindfolded, in the dark.

### ⚠️ Important: Cryptography ≠ Complete Security

While this project demonstrates that the *cryptography* itself is secure, it's crucial to understand that **your wallet's security depends entirely on keeping your private keys secret**. 

The math proves that guessing your private key is impossible. But:

- **Phishing attacks** can trick you into revealing your seed phrase
- **Malware** can steal keys from compromised devices
- **Hot wallet vulnerabilities** can expose keys stored on internet-connected systems
- **Exchange hacks** have resulted in billions of dollars stolen - not by breaking cryptography, but by exploiting security flaws in key storage and management
- **Social engineering** can manipulate you into handing over access

Major incidents that have resulted in billions of dollars in losses all share one thing in common: none of them broke the underlying cryptography. Instead, they exploited weaknesses in implementation, human behavior, and operational security:

- **Mt. Gox (2014, ~$450M)**: The largest Bitcoin exchange at the time collapsed after years of poor security practices and missing funds. Private keys were stored insecurely, enabling systematic theft.

- **The DAO (2016, ~$60M)**: A smart contract reentrancy vulnerability allowed an attacker to drain funds. Led to Ethereum's controversial hard fork. The cryptography was fine - the code logic wasn't.

- **Parity Wallet (2017, ~$280M)**: A bug in the multi-signature wallet code allowed someone to accidentally become the owner and then "kill" the contract, freezing funds permanently. Again, not a crypto break - just more bad code.

- **Coincheck (2018, ~$530M)**: Hot wallet private keys were stored on internet-connected systems without proper security measures. Attackers simply broke in and stole the keys.

- **Poly Network (2021, ~$611M)**: Cross-chain bridge exploit where the attacker found a way to forge transactions between blockchains. Interestingly, the hacker later returned most funds, claiming it was a "white hat" test. We bow our heads to you anonymous hero.

- **Ronin Network (2022, ~$625M)**: Social engineering and compromised private keys of validator nodes. Attackers gained control of enough validators to approve fraudulent withdrawals.

- **Wormhole Bridge (2022, ~$325M)**: Smart contract vulnerability in a cross-chain bridge allowed minting of fake tokens. Cryptographic signatures worked perfectly - the validation logic didn't.

**Bottom line:** The cryptography protecting your wallet is virtually unbreakable. You, however, might not be. Guard your private keys like they're the combination to a vault containing all your wealth - because that's exactly what they are.

## The Math: A Journey Through Cosmic Impossibility

Let's quantify exactly how hopeless this endeavor is.

### The Keyspace

Here's a crucial distinction: Ethereum uses **256-bit private keys**, but these are hashed down to **160-bit addresses** using the Keccak-256 algorithm. When we're searching for funded wallets, what matters is the **address space**, not the private key space.

**Private key space:** $2^{256} \approx 1.16 \times 10^{77}$ possible private keys

**Address space:** $2^{160} \approx 1.46 \times 10^{48}$ possible addresses

Why does this matter? Because multiple private keys can theoretically map to the same address (though finding such a collision is still astronomically unlikely). When searching for a match, we're looking for any private key that produces a funded address - so the **address space** is our relevant search domain.

To put $2^{160}$ in perspective: this is still about 100 billion times larger than the estimated number of atoms in the observable universe.

### The Target

Current estimates suggest there are approximately $1.1 \times 10^8$ (110 million) Ethereum addresses with positive balances. However, for the sake of this thought experiment, let's be extremely generous and assume there are $10^9$ (1 billion) funded addresses. The probability of randomly generating a private key that maps to one of these addresses is:

$$P(\text{hit}) = \frac{10^9}{1.46 \times 10^{48}} \approx 6.8 \times 10^{-40}$$

### Time to Success

Now let's imagine we somehow commandeer **all computational power on Earth**. As of 2025, estimates put total global computing power at roughly $10^{21}$ FLOPS. Let's generously assume we can check $10^{18}$ keys per second (unrealistic, but let's dream big).

Since there are $10^9$ funded addresses in an address space of $1.46 \times 10^{48}$, the expected number of attempts to find one is:

$$\text{Expected attempts} = \frac{1.46 \times 10^{48}}{10^9} = 1.46 \times 10^{39}$$

The expected time to find a single match is:

$$t = \frac{1.46 \times 10^{39}}{10^{18}} = 1.46 \times 10^{21} \text{ seconds}$$

Converting to years ($3.15 \times 10^7$ seconds per year):

$$t \approx 4.6 \times 10^{13} \text{ years}$$

**Translation:** The universe is approximately $1.4 \times 10^{10}$ years old. You'd need to run this program for about **3,300 consecutive universe lifetimes**. To put this in cosmic perspective:

- **All stars burn out**: Around $10^{14}$ years - you'd actually finish your search BEFORE the last stars die! Though you'd still be searching in darkness for the last third of your quest as stars progressively burn out.
- **Proton decay** (if it happens): $10^{34}$ to $10^{40}$ years (lower bound) - you'd finish searching long, long before even the lower estimates of proton decay. The atoms making up your computer would remain intact throughout your entire futile search.
- **Stellar-mass black holes evaporate**: Around $10^{67}$ years - you'd finish your search about $10^{53}$ years before these even start evaporating. 
- **Supermassive black holes evaporate**: Around $10^{85}$ years - if you could somehow keep running until then, you'd complete your entire search about $10^{71}$ times over. You'd find approximately $10^{80}$ funded addresses - which ironically is close to the number of atoms in the observable universe. Too bad none of it exists anymore.

In a dead, dark universe with no stars, no planets, no atoms - just you, somehow, checking keys - you'd finish your search long before the final supermassive black holes evaporated into Hawking radiation.

You might ask the universe's last superintelligent computer: *"How can the net amount of entropy of the universe be massively decreased?"* hoping to somehow reverse time and continue your search. But even Multivac's distant descendant would simply respond: *INSUFFICIENT DATA FOR A MEANINGFUL ANSWER.*

### Birthday Paradox Disclaimer

"But wait," you might say, "what about the birthday paradox? If I check billions of addresses, don't my odds improve?" 

Not meaningfully. When searching for any of the $10^9$ funded addresses by checking $n$ random keys in an address space of $1.46 \times 10^{48}$, your success probability is:

$$P \approx 1 - e^{-\frac{n \times 10^9}{1.46 \times 10^{48}}} = 1 - e^{-n \times 6.8 \times 10^{-40}}$$

Even if you check $10^{12}$ keys (a trillion attempts), this becomes:

$$P \approx 1 - e^{-10^{12} \times 6.8 \times 10^{-40}} = 1 - e^{-6.8 \times 10^{-28}} \approx 6.8 \times 10^{-28}$$

Still effectively zero. You'd need to check an incomprehensible number of keys before the birthday paradox provides any meaningful advantage.

## What If You Actually Win This Cosmic Lottery?

In the incomprehensibly unlikely event that this tool finds a funded address:

1. **Don't steal the funds.** Seriously. That's theft, and also you'd be the luckiest person in human history - maybe use that luck for good?
2. **Document everything.** This would be a cryptographically significant event worthy of academic papers.
3. **Responsible disclosure.** Contact the address owner if possible, or Ethereum security researchers.
4. **Buy a lottery ticket.** Your odds of winning those are *much* better (typically around $10^{-7}$ to $10^{-9}$), so if you can beat $10^{-69}$, you can definitely beat those.

> ⚠️ **Warning**  
> Treat coin-finder as an educational tool. Any improbable successes must be handled responsibly and ethically.

## But Hey, You Never Know...

Improbable is not impossible. Every private key is technically valid. Somewhere in that $10^{77}$ keyspace are all the funded wallets, waiting to be found. The math says you won't find them, but mathematics deals in probabilities, not certainties.

Maybe the universe's random number generator will smile upon you. Maybe you'll be the one person in all of history to crack this cosmic safe with a lucky guess. Maybe pigs will fly and hell will freeze over simultaneously.

Or, more likely, this tool will serve its intended purpose: demonstrating through direct experience why cryptography works and why your crypto wallet is actually secure.

Happy hunting! 🔍

---

## Quick start

### 1. Clone & enter the repo

```bash
git clone https://github.com/jaroslawjanas/coin-finder.git
cd coin-finder
```

### 2. Create the Conda environment

```bash
conda env create -f environment.yml
conda activate coin-finder
```

> Windows users: consider `conda init powershell` if PowerShell doesn’t auto-activate.

### 3. Provide configuration

Copy `.env.example` to `.env` and set values as needed:

```bash
cp .env.example .env
```

At minimum define:

```
ETH_RPC_URL=https://your-provider.example/v2/your-key
```

The RPC endpoint **must support JSON-RPC POST batching** (`eth_getBalance`).

> **Recommendation:** For quick testing without API keys, we recommend using the free public node at `https://ethereum-rpc.publicnode.com/` with a batch size of 100. Example:
> ```
> ETH_RPC_URL=https://ethereum-rpc.publicnode.com/
> ```
> Then run with: `python -m coin_finder scan --workers 4 --batch-size 100`

### 4. Run the scanner

```bash
python -m coin_finder scan --workers 6 --batch-size 100
```

The process runs until interrupted (Ctrl+C). Hits are appended to `output/eth_hits.csv`. The dashboard renders three stacked panels - the main summary, *Throughput Rates* (requests/sec and keys/sec), and *Lifetime Stats* (runtime, totals, and hit chance). Lifetime counters persist between runs via `output/stats.json`.

![Dashboard Preview](https://i.imgur.com/aTvXDOb.png)

---

## CLI reference

`python -m coin_finder scan [OPTIONS]`

| Option | Description | Default / ENV |
|--------|-------------|---------------|
| `--eth-rpc-url TEXT` | Ethereum JSON-RPC endpoint (batch capable). **Required**. | `ETH_RPC_URL` |
| `--provider-name TEXT` | Label stored in CSV for the provider. | `ethereum` / `PROVIDER_NAME` |
| `-w, --workers INTEGER` | Number of concurrent workers. | `4` / `WORKERS` |
| `-b, --batch-size INTEGER` | Keys generated per worker per batch. | `512` / `BATCH_SIZE` |
| `--rpc-timeout FLOAT` | HTTP timeout (seconds). | `30` / `RPC_TIMEOUT` |
| `--rpc-max-outstanding INTEGER` | Max simultaneous RPC requests. | `8` / `RPC_MAX_OUTSTANDING` |
| `--stats-refresh-interval FLOAT` | Dashboard refresh cadence (seconds). | `0.25` / `STATS_REFRESH_INTERVAL` |
| `--output-dir PATH` | Directory for CSV hits. | `output/` / `OUTPUT_DIR` |
| `--hits-filename TEXT` | CSV filename under `output_dir`. | `eth_hits.csv` / `HITS_FILENAME` |
| `--seed TEXT` | Optional base seed for RNG reproducibility. | `SEED` |
| `--log-level TEXT` | Logging level. | `INFO` / `LOG_LEVEL` |

All options have matching environment variables. CLI flags override env values.

---

## Output data

Hits are appended to `output/<hits_filename>` with headers:

```
private_key_hex,public_key_hex,address,balance_wei,balance_eth,detected_at
```

Each successful hit is recorded with:
- **private_key_hex**: The private key in hexadecimal format
- **public_key_hex**: The public key in hexadecimal format  
- **address**: The Ethereum address
- **balance_wei**: Balance in wei (smallest ETH unit)
- **balance_eth**: Balance formatted in ETH with 18 decimal precision
- **detected_at**: ISO 8601 timestamp (UTC) when the hit was detected

---

## Architecture overview

```
┌─────────────┐        ┌─────────────┐         ┌───────────────┐
│ RNG + Keygen│  batch │ ETH RPC     │ results │ CSV Writer    │
│ (per worker)├───────►│ Batch Client├────────►│ (async locked)│
└──────┬──────┘        └──────┬──────┘         └───────┬───────┘
       │ stats update         │ latency metrics        │ hits
       ▼                      ▼                        ▼
┌─────────────────────────────────────────────────────────────┐
│                      Statistics Registry                    │
│              (rates, totals, last hit, errors)              │
└───────────────┬──────────────────────┬──────────────────────┘
                │                      │
                ▼                      ▼
        Rich Dashboard        Structured logging (stdout)
```

- `HashStreamRNG` blends user seed, worker/batch IDs, nanosecond timestamps, and OS entropy.
- `JsonRpcHttpClient` manages batching, rate limiting (capacity limiter), and exponential backoff.
- `EthBalanceClient` converts batched responses into typed results.
- `Statistics` offers snapshots for the dashboard and metrics updates.
- `dashboard_loop` renders a live terminal UI with throughput metrics.
- `run_worker` loops until stop, generating keys → requesting balances → recording hits.
- `runner.py` orchestrates workers, dashboard, and graceful shutdown.

---

## Extending to new chains

1. Implement `<chain>/keygen.py` (keypair + address derivation).
2. Implement `<chain>/rpc.py` for batch balance checks.
3. Wire into the pipeline (chain-specific client; extend `AppConfig`).
4. Update CSV headers and CLI flags as needed.

The current design isolates chain-specific logic from the pipeline.

---

## Testing / benchmarking guidance

| Goal | Suggestion |
|------|------------|
| Smoke test | Run with a local mock RPC server or set `--batch-size 5` and intercept requests (e.g., mitmproxy). |
| Throughput benchmark | Configure a fast provider (low latency). Run `python -m coin_finder scan --workers 16 --batch-size 2048 --stats-refresh-interval 0.5` and observe the dashboard rates. |
| Retry logic | Intentionally return HTTP 429/500 from a mock server to ensure exponential backoff kicks in (log level DEBUG). |
| Deterministic behavior | Supply `--seed foo` and capture addresses generated in first batch to verify reproducibility. |

> Since live providers charge per request, benchmarking against production endpoints can be expensive. Use low batch sizes for validation.

---

## Security considerations

- Private keys are only written when a positive balance is detected. Secure the `output/` directory accordingly.
- Avoid logging beyond hits. DEBUG-level logs can leak timing information - use only for development.
- Store API keys in `.env`. The `.gitignore` already excludes `.env` and `output/`.

---

## Roadmap ideas

- Add graceful shutdown on SIGTERM/SIGINT with progress reporting.
- Support Ethereum Etherscan REST `balancemulti` as a fallback.
- Add Electrum and Esplora clients for Bitcoin, or Solana RPC integration.
- Emit Prometheus metrics or OpenTelemetry traces.
- Plugin system for pluggable providers/chains.

---

## License

GNU AFFERO GENERAL PUBLIC LICENSE - see [LICENSE](LICENSE).

Happy hacking (responsibly)! 🛠️
