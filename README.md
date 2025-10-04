# coin-finder

High-throughput Ethereum address scanner that continuously generates random private keys, derives the corresponding public addresses, checks balances via a batch-capable JSON-RPC provider, and records positive-balance hits to CSV. A live terminal dashboard (Rich) surfaces htop-inspired statistics for monitoring throughput, latency, and hit rates.

> ⚠️ **Practicality warning**  
> The probability that a randomly generated key corresponds to a funded address is astronomically low. This project is delivered as an educational exercise on high-concurrency pipelines, async IO, batching, and telemetry—not as an effective method for discovering funded wallets.

---

## Features

- Conda-managed Python 3.11 environment
- SHA3-256 counter-mode RNG seeded by user input plus high-resolution timestamps
- Optimized secp256k1 key generation using `coincurve`
- Ethereum address derivation with EIP-55 checksumming
- JSON-RPC batch requests with retry/backoff logic (aiohttp + backoff)
- Configurable worker count and batch sizes; unlimited runtime until interrupted
- Thread-safe CSV writer for positive balance hits (timestamped, with metadata)
- Rich-powered live dashboard (htop-inspired)
- Extensible architecture for additional chains/providers

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

### 4. Run the scanner

```bash
python -m coin_finder scan --workers 8 --batch-size 1024
```

The process runs until interrupted (Ctrl+C). Hits are appended to `output/eth_hits.csv`.

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
detected_at,address,private_key_hex,public_key_hex,balance_wei,balance_eth,
worker_id,batch_id,batch_index,provider,seed_descriptor
```

Balances are stored **in wei** and **formatted ETH** with 18 decimals.

---

## Architecture overview

```
┌─────────────┐        ┌────────────┐         ┌──────────────┐
│ RNG + Keygen│  batch │ ETH RPC    │ results │ CSV Writer    │
│ (per worker)├───────►│ Batch Client├────────►│ (async locked)│
└───────┬─────┘        └────┬──────┘         └───────┬───────┘
        │ stats update       │ latency metrics        │ hits
        ▼                    ▼                        ▼
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
- Avoid logging beyond hits. DEBUG-level logs can leak timing information—use only for development.
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

MIT License — see [LICENSE](LICENSE).

Happy hacking (responsibly)! 🛠️
