# Interstellar Object Archival Search

I'm Marshall Fanaeian, a high school student in Middleton, Wisconsin. This repository
is my research project for the 2027 science fair season (Capital Science &
Engineering Fair and Badger State Science & Engineering Fair, aiming for
Regeneron ISEF): a systematic search of pre-Rubin sky survey archives for
interstellar objects that were recorded but never recognized.

## The idea

Only three interstellar objects have ever been confirmed, 1I/'Oumuamua (2017),
2I/Borisov (2019), and 3I/ATLAS (2025). All three turned out to have "precovery"
detections sitting in archives before anyone noticed them: 3I/ATLAS shows up in
TESS images almost two months before its discovery. Those searches were done
after the orbits were known. Nobody has run the blind version, searching the
2010–2024 archives for hyperbolic objects nobody ever flagged.

The plan, in one paragraph: search the Minor Planet Center's Isolated Tracklet
File (~4 million unlinked tracklets) for linkages that only fit unbound (e > 1)
orbits, use ML trained on synthetic interstellar objects injected through real
survey pointing histories to vet candidates, and measure my own detection
efficiency so that even a null result becomes a real upper limit on the local
interstellar object density. A discovery would be an upside case, not the requirement for success.

## Status

Early days — currently in the learning/foundations phase:

- [x] Repo + environment setup
- [x] Parsed 3I/ATLAS's full astrometry from the MPC (8,433 observations,
      including the TESS precovery points — found those via a parsing bug,
      story in the lab notebook)
- [ ] Reproduce 3I/ATLAS's orbit fit (target: recover e ≈ 6.14 myself)
- [ ] First look at the Isolated Tracklet File
- [ ] Synthetic ISO injection engine
- [ ] Hyperbolic linking pipeline

## What's where

- `notebooks/` — analysis notebooks, numbered in order
- `docs/notebook/` — my lab notebook, dated entries, kept as I work
- `docs/` — literature notes, data source records, planning docs
- `data/` — not tracked in github; sources and download instructions are
  documented so everything can be re-fetched

## Tools

Python (astropy, pandas, matplotlib so far), find_orb for orbit fitting,
git for provenance. AI (Claude) is used as a tutor, explanations, debugging
help, background, as is logged in the lab notebook; the code is written and
understood by me.

## License

None yet, intentionally — all rights reserved while the project is in progress.
I expect to open-source it (MIT) when the research freezes before my competitions.
