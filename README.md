# Project INTERLOPER

A systematic search of pre-Rubin sky survey archives for interstellar objects
that were recorded but never recognized.

I'm Marshall Fanaeian, a high school student in Wisconsin. This repository is my
research project for the 2027 science fair season: the Capital Science &
Engineering Fair and the Badger State Science & Engineering Fair, aiming for
Regeneron ISEF in Los Angeles in May 2027.

## The idea

Only three interstellar objects have ever been confirmed: 1I/'Oumuamua (2017),
2I/Borisov (2019), and 3I/ATLAS (2025). All three turned out to have "precovery"
detections sitting in archives before anyone noticed them. 3I/ATLAS shows up in
TESS images almost two months before its discovery.

Every one of those searches was done after the orbit was already known. Nobody
has run the blind version: searching the archives for hyperbolic objects that
nobody ever flagged.

The plan in short. Search the Minor Planet Center's Isolated Tracklet File, the
pile of observations that were never matched to any known object, for linkages
that only fit unbound orbits. Train a classifier on synthetic interstellar
objects injected through real survey pointing histories to vet the candidates.
Then measure my own detection efficiency, so that even finding nothing produces
a real upper limit on how many interstellar objects are passing through the
solar system. A discovery is the upside case, not the requirement for success.

## What I've measured so far

Two findings from my own census that update the published literature:

**The archive is smaller than the papers say, and it is shrinking.** Work from
2017 to 2021 describes the Isolated Tracklet File as holding 14 to 17 million
observations. I measured 9,354,883 lines on 16 July 2026 and 9,173,323 lines on
7 September, a drop of 1.94% in seven and a half weeks. Other groups are
actively linking tracklets out of it. The material I am searching is a
shrinking resource, and I have a rate for how fast it is going.

**The list of contributing surveys has changed.** Older papers describe
Pan-STARRS and Mt. Lemmon as the two dominant sources. In the current file,
DECam at Cerro Tololo (W84, 1,197,169 observations) has overtaken Mt. Lemmon
(G96, 1,085,281) for second place. Pan-STARRS 1 and 2 together supply about 40%.

The file holds 2,593,332 distinct object designations, averaging 3.58
observations each with a median of 3, and spans observations from 1858 to 2026.
Structurally it is a pile of two and a half million fragments. Orbits are only
possible by linking them across nights, which is what this project is built to
do.

## Status

Done:

- [x] Repository, environment, and lab notebook set up
- [x] Parsed the full public astrometry for all three known interstellar
      objects and reproduced their orbits independently (my e values: 1.2009,
      3.3566, 6.1368, against JPL's 1.2011, 3.3565, 6.1414)
- [x] Derived v-infinity by hand from vis-viva for all three
- [x] Found 3I/ATLAS's TESS precovery detections in my own dataset, plus
      observations taken from four spacecraft including one during its Mars
      close approach (found through a parsing bug, story in the lab notebook)
- [x] Full census of the Isolated Tracklet File
- [x] Converted the entire archive from text into numbers and stored it in a
      form that loads in seconds

Next:

- [ ] Tracklet kinematics: time spans and sky-plane rates
- [ ] Synthetic interstellar object injection engine
- [ ] Detection efficiency curves and a population upper limit
- [ ] Hyperbolic linking pipeline over the full archive
- [ ] Machine learning candidate vetting

## What's where

`notebooks/`: analysis notebooks, numbered in order (01 is 3I parsing and plots)

`docs/notebook/`: my lab notebook, dated entries written as I work, plus
`attachments/` for hand calculations, screenshots, and reference images

`docs/literature/`: one note file per paper, in my own words

`docs/ISO_comparison.md`: side by side table of my derived orbits for all three
known interstellar objects against JPL's values

`results/`: saved orbit fit outputs, including the full residual listings, so
every number in the comparison table traces back to a file

`src/`: the parsing and conversion code, with tests in `tests/`

`figures/`: generated plots, versioned rather than overwritten

`data/`: not tracked in git. Sources and download instructions are documented in
`DATA_SOURCES.md` so everything can be re-fetched.

## Tools

Python (astropy, pandas, matplotlib), Find_Orb for orbit fitting, git for
provenance.

AI (Claude) is used as a tutor: explanations, debugging help, and background
reading. Every session that uses it is logged in the lab notebook. The code is
written and understood by me.

## License

None yet, and that is deliberate. All rights reserved while the project is in
progress. I expect to release it under MIT when the research freezes ahead of
competition season.