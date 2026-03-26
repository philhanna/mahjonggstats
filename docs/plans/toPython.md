## Plan: Go to Python Full Replacement

Replace the Go implementation with a Python 3.12+ implementation that preserves current behavior (features and semantics) while allowing minor output formatting differences. Use a src-layout Python package with argparse for CLI and pytest for test coverage, and migrate behavior from existing Go tests plus new CLI output tests to reduce regression risk.

**Steps**
1. Phase 1 - Baseline and behavior lock
2. Inventory behavior from current test suite and command paths in [history_line_test.go](history_line_test.go), [history_test.go](history_test.go), [level_history_test.go](level_history_test.go), [cmd/mahjonggstats_test.go](cmd/mahjonggstats_test.go), and runtime wiring in [cmd/mahjonggstats.go](cmd/mahjonggstats.go).
3. Add missing baseline tests before rewrite: controller routing and rendered-output checks currently not covered (summary, verbose, level-names-only, filtered level). Use existing Go app output as temporary golden behavior reference. Depends on step 2.
4. Phase 2 - Python project scaffolding
5. Create Python package structure under src layout and pytest test package under tests layout, with CLI entrypoint and test runner configuration. Parallel with step 3 once behavior inventory is complete.
6. Define Python module boundaries mirroring current architecture: history line parsing, history aggregation, level statistics, view rendering, controller orchestration, and CLI argument validation. Depends on step 5.
7. Phase 3 - Feature migration
8. Port parsing and formatting behavior from [history_line.go](history_line.go): datetime parse with timezone, date extraction, time formatting MM:SS and HH:MM:SS thresholds, debug string behavior. Depends on step 6.
9. Port level statistics from [level_history.go](level_history.go): count, min, mean, sample standard deviation, 95% confidence interval with non-negative lower bound. Depends on step 6.
10. Port history model and loading flow from [history.go](history.go): file loading, level grouping, earliest/latest date, and level ordering by mean time. Depends on steps 8 and 9.
11. Port view rendering and sorting from [view.go](view.go): summary sorting by GA/NA/AA/MA with direction, verbose per-level report, top shortest scores, level names view. Depends on step 10.
12. Port controller and CLI from [controller.go](controller.go) and [cmd/mahjonggstats.go](cmd/mahjonggstats.go): flag compatibility for name, level-names-only, sort, verbose, plus sort-option validation rules. Depends on step 11.
13. Phase 4 - Test migration and parity hardening
14. Convert Go unit tests to pytest equivalents and preserve assertions from [history_line_test.go](history_line_test.go), [history_test.go](history_test.go), [level_history_test.go](level_history_test.go), and [cmd/mahjonggstats_test.go](cmd/mahjonggstats_test.go). Depends on steps 8-12.
15. Add new pytest coverage for controller dispatch and full CLI output modes (currently weak in Go tests), including malformed lines and empty-history behavior decisions. Depends on step 14.
16. Phase 5 - Replacement and cleanup
17. Switch default runnable command/docs to Python entrypoint, update README usage/examples from [README.md](README.md), and adjust changelog entry in [CHANGELOG.md](CHANGELOG.md). Depends on step 15.
18. Remove or archive Go-specific runtime code and obsolete tests after Python parity is validated; keep fixture data such as [testdata23.txt](testdata23.txt) as regression fixtures if useful. Depends on step 17.

**Relevant files**
- /home/saspeh/dev/python/mahjonggstats/cmd/mahjonggstats.go - Current CLI parsing and ValidateSortOption behavior to mirror.
- /home/saspeh/dev/python/mahjonggstats/controller.go - Dispatch logic and mode sequencing to mirror.
- /home/saspeh/dev/python/mahjonggstats/view.go - Summary/verbose rendering and sorting behavior.
- /home/saspeh/dev/python/mahjonggstats/history.go - Loading and aggregation model.
- /home/saspeh/dev/python/mahjonggstats/history_line.go - Input line parsing and time/date formatting behavior.
- /home/saspeh/dev/python/mahjonggstats/level_history.go - Statistical formulas and confidence interval logic.
- /home/saspeh/dev/python/mahjonggstats/history_line_test.go - Parsing/formatting behavioral requirements.
- /home/saspeh/dev/python/mahjonggstats/history_test.go - Aggregation/date-level requirements.
- /home/saspeh/dev/python/mahjonggstats/level_history_test.go - Statistics parity requirements.
- /home/saspeh/dev/python/mahjonggstats/cmd/mahjonggstats_test.go - CLI sort validation parity.
- /home/saspeh/dev/python/mahjonggstats/README.md - Usage documentation update during cutover.
- /home/saspeh/dev/python/mahjonggstats/CHANGELOG.md - Migration release notes.

**Verification**
1. Run existing Go tests as a baseline snapshot before migration and record current pass/fail and known gaps (controller/output coverage).
2. Run pytest suite for migrated Python modules and ensure parity for parser, stats, history aggregation, and sort-option validation.
3. Add CLI behavior tests that execute Python entrypoint for: default summary, verbose all-levels, level filter, and level-names-only.
4. Run fixture-based regression tests using existing history samples (including [testdata23.txt](testdata23.txt)) to ensure stable results across representative datasets.
5. Manually spot-check output readability and sort ordering in behavioral parity mode, allowing minor formatting differences only.

**Decisions**
- Included scope: full replacement to Python as primary implementation.
- Included scope: behavioral parity (semantics and options) rather than byte-for-byte output matching.
- Included scope: argparse, pytest, src layout, Python 3.12+.
- Excluded scope: major UX redesign, alternate CLI frameworks, or feature expansion beyond current Go behavior unless needed for safety/error handling.

**Further Considerations**
1. Empty-history behavior should be explicitly defined during migration (graceful message vs failure) because current Go path can panic and is not well-tested.
2. Malformed line handling policy should be standardized (skip with warning vs fail-fast) to avoid silent data loss ambiguity from current implementation.
3. Decide whether to preserve mean-time level ordering in names output or switch to alphabetical; current tests imply mean-time order for level list semantics.
