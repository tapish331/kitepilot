# Risk Matrix

| Rule | Config Key | Default |
|------|------------|---------|
| Kill switch | `toggles.kill_switch` | `false` |
| Instrument banlist | `lists.instrument_banlist` | `[]` |
| Opening minutes block | `toggles.opening_minutes_block` | `null` |
| Max daily loss | `limits.max_daily_loss` | `null` |
| Max open positions | `limits.max_open_positions` | `null` |
| Max qty per order | `limits.max_qty_per_order` | `null` |
| Max qty per symbol day | `limits.max_qty_per_symbol_day` | `null` |
| Max turnover day | `limits.max_turnover_day` | `null` |
| Throttle per symbol | `throttle.min_seconds_between_orders` | `null` |

Reason codes: `KILL_SWITCH`, `INSTRUMENT_BANNED`, `OPENING_BLOCK`,
`MAX_DAILY_LOSS`, `MAX_OPEN_POS`, `MAX_QTY_ORDER`, `MAX_QTY_DAY`,
`MAX_TURNOVER_DAY`, `THROTTLED`.
