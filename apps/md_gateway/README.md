# md-gateway

Synthetic market data gateway producing deterministic 1-second and 1-minute bars from simulated ticks.

## Usage

```bash
python -m apps.md_gateway.src.main --mode sim --symbols TCS,INFY --seed 42 --seconds 5
```

Bars are printed as NDJSON and written under `.artifacts/md-gateway/bars.ndjson`.
