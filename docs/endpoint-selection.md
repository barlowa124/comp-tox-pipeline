# Endpoint selection

TODO: pick one endpoint before implementing `data/toxcast.py`. Criteria:

- **Decision relevance**: endpoint maps to a real preclinical safety decision
  (DILI > hERG > ER agonism roughly, for pharma relevance)
- **Label budget**: enough actives for a scaffold split to leave a usable test set
- **Label quality**: prefer endpoints with consistent assay protocols
- **Narrative**: the NAMs framing is strongest when the endpoint is one where
  in-vitro/in-silico methods are actively argued to displace animal studies

## Candidates

| Endpoint | Source | Positives (approx) | Notes |
|---|---|---|---|
| DILI (hepatotox) | literature sets / ChEMBL | TODO | highest relevance, messiest labels |
| hERG inhibition | ChEMBL / ToxCast | TODO | cardiotox, well-studied |
| Tox21 ER/AR agonism | Tox21 | TODO | clean NAMs story, large screen |
| ToxCast assay AC50 | invitrodb | TODO | most labels, assay-specific |

Decision: **TODO**
