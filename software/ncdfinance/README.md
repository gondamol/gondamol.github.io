# ncdfinance

**Status:** public scope / early release planning  
**Author:** Nichodemus Amollo  
**Intent:** Analysis and presentation helpers for facility-level NCD financing and decision-space work in devolved health systems (Kenya-first, methods transferable).

## Problem

Facility financing studies mix:

- structured facility questionnaires  
- financial process timelines (approvals, reimbursement lag)  
- qualitative notes from in-charges  
- simple scenario levers for operations audiences  

`ncdfinance` will package the **public-safe analysis patterns** from the Kisumu NCD financing research (not confidential microdata).

## Planned first public surface

| Module | Purpose |
|---|---|
| `facility_indicators` | Standard tables for funding streams, autonomy, stockouts |
| `decision_space` | Simple summaries of planning vs spending authority |
| `scenarios` | Transparent lever calculations for ops/policy briefs |
| `report_blocks` | Quarto-ready table/figure blocks for manuscripts and briefs |

## Related research

- [Thesis / NCD financing study](../../research/thesis.html)  
- [Public essay on facility decision space](../../posts/47-facility-decision-space-chronic-care/)  
- [Operations case study framing](../../projects/case-studies/ncd-financing-impact/)

## Non-goals (v0)

- Claiming national representativeness from a sub-county sample  
- Shipping any facility-identifying raw data  
- Full micro-simulation of county budgets

## Roadmap

1. Freeze indicator dictionary from the public manuscript results  
2. Ship synthetic example facility table + vignette  
3. Align scenario helpers with the existing case-study R script

## License

MIT (planned for first code release).
