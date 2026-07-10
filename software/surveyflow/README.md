# surveyflow

**Status:** public scope / early release planning  
**Author:** Nichodemus Amollo  
**Intent:** Practical helpers for survey and research data operations in low-connectivity health and development studies.

## Problem

Field teams repeatedly rebuild the same pieces:

- XLSForm / ODK naming conventions  
- High-frequency check (HFC) templates  
- Completeness and constraint-failure summaries  
- Enumerator performance extracts for supervisors  

`surveyflow` is meant to package patterns that already show up in real programmes (including diaries-style streaming quality work), not to replace ODK, Kobo, or REDCap.

## Planned first public surface

| Module | Purpose |
|---|---|
| `hfc_checks` | Starter rules: duplicates, range, requiredness, date order |
| `completeness` | Module- and enumerator-level completion summaries |
| `id_audit` | Stable ID validation and collision reports |
| `export_tidy` | Opinionated tidy extracts from common CAPI exports |

## Non-goals (v0)

- Full CAPI server  
- Auto-magic multi-language UI builder  
- Claims of one-click offline sync (that is server/platform territory)

## Roadmap

1. Document the HFC recipe used on real studies (public-safe)  
2. Ship a minimal R package skeleton with one vignette  
3. Add example synthetic data only (no real household microdata)

## Related portfolio work

- [Health financial diaries systems](../../projects/health-financial-diaries/)  
- [Mobile data collection note](../../posts/24-mobile-data-collection/)

## License

MIT (planned for first code release).
