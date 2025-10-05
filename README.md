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

Ethereum uses 256-bit private keys, giving us a search space of:

$$2^{256} \approx 1.16 \times 10^{77} \text{ possible keys}$$

To put this in perspective, this number is larger than the estimated number of atoms in the observable universe ($10^{80}$... wait, actually it's close, but still mind-bogglingly huge).

### The Target

Let's be extremely generous and assume there are $10^9$ (1 billion) Ethereum addresses with positive balances. The probability of randomly generating one of these addresses is:

$$P(\text{hit}) = \frac{10^9}{10^{77}} = 10^{-68}$$

### Time to Success

Now let's imagine we somehow commandeer **all computational power on Earth**. As of 2025, estimates put total global computing power at roughly $10^{21}$ FLOPS. Let's generously assume we can check $10^{18}$ keys per second (unrealistic, but let's dream big).

The expected time to find a single match is:

$$t = \frac{\text{keyspace}}{2 \times \text{rate}} = \frac{10^{77}}{2 \times 10^{18}} = 5 \times 10^{58} \text{ seconds}$$

Converting to years ($3.15 \times 10^7$ seconds per year):

$$t \approx 1.6 \times 10^{51} \text{ years}$$

**Translation:** The universe is approximately $1.4 \times 10^{10}$ years old. You'd need to run this program for about $10^{41}$ consecutive universe lifetimes. To put this in cosmic perspective:

- **Proton decay** (if it happens): $10^{34}$ to $10^{40}$ years (lower bound) - the very atoms making up your computer would decay into radiation, yet your program would still have $10^{11}$ years left to run
- **All stars burn out**: Around $10^{14}$ years - the last stars would fade to black while you're still only $0.000001\%$ of the way there
- **Stellar-mass black holes evaporate**: Around $10^{67}$ years - you'd actually finish BEFORE this happens, but the universe would be a cold, lightless void for the last $10^{16}$ years of your search
- **Supermassive black holes evaporate**: Around $10^{85}$ years - if you could somehow keep running until then, you'd expect to find about $6 \times 10^{33}$ funded addresses. Not bad! Except there's no universe left, no Ethereum network, and you're a disembodied search algorithm floating in an infinite void of darkness.

Even in a dead, dark universe with no stars, no planets, no atoms - just you, somehow, checking keys - you'd finish your search and find nothing long before the final supermassive black holes evaporated into Hawking radiation. The universe would literally rather become an endless void of scattered photons than let you randomly guess someone's private key.

You might ask the universe's last superintelligent computer: *"How can the net amount of entropy of the universe be massively decreased?"* hoping to somehow reverse time and continue your search. But even Multivac's distant descendant would simply respond: *INSUFFICIENT DATA FOR A MEANINGFUL ANSWER.*

### Birthday Paradox Disclaimer

"But wait," you might say, "what about the birthday paradox? If I check billions of addresses, don't my odds improve?" 

Not meaningfully. Even if you check $10^{12}$ keys, your success probability only becomes:

$$P \approx 1 - e^{-\frac{n^2}{2 \times 10^{77}}} \approx 0$$

Still effectively zero. The birthday paradox only helps when the keyspace is much smaller.

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
