# Call tree — mahjonggstats invocation

Traces a single call from the command line to stdout across every layer.
Three output paths branch inside `TextPresenter.render`; each is shown separately.

```
main()                                          cli.py:53
├── build_parser()                              cli.py:31
├── validate_sort_option(ns.sort)               cli.py:12
├── StatsQuery(...)                             ports/stats_query.py:9
├── StatsService(                               application/stats_service.py:13
│     loader=FileHistoryLoader(),               adapters/file_history_loader.py:13
│     presenter=TextPresenter()                 adapters/text_presenter.py:16
│   )
├── StatsService.run(query)                     application/stats_service.py:17
│   ├── FileHistoryLoader.load()                adapters/file_history_loader.py:16
│   │   └── HistoryLine.parse(line)  [×N]       domain/history_line.py:17
│   ├── History.from_records(records)           domain/history.py:18
│   │   └── LevelHistory(...)        [×level]   domain/level_history.py:11
│   └── TextPresenter.render(history, query)    adapters/text_presenter.py:17
│       ├── _resolve_levels(history, query)     adapters/text_presenter.py:30
│       │   └── History.level_names()           domain/history.py:38
│       │       └── LevelHistory.mean()  [×N]   domain/level_history.py:23
│       │
│       ├── [if level_names_only]
│       │   └── _show_level_names(...)          adapters/text_presenter.py:49
│       │
│       ├── [if verbose]
│       │   ├── _show_heading(history)          adapters/text_presenter.py:43
│       │   │   ├── History.earliest_date()     domain/history.py:28
│       │   │   └── History.latest_date()       domain/history.py:33
│       │   └── _show_all_levels(history, query) adapters/text_presenter.py:82
│       │       └── [per level]
│       │           ├── LevelHistory.mean()     domain/level_history.py:23
│       │           ├── LevelHistory.standard_deviation()  domain/level_history.py:29
│       │           ├── LevelHistory.confidence()          domain/level_history.py:38
│       │           ├── LevelHistory.count()    domain/level_history.py:15
│       │           └── HistoryLine.time_date() domain/history_line.py:26
│       │               └── format_time()       domain/history_line.py:42
│       │
│       └── [default — summary]
│           └── _show_summary(history, query)   adapters/text_presenter.py:54
│               └── [per level]
│                   ├── LevelHistory.count()    domain/level_history.py:15
│                   ├── LevelHistory.mean()     domain/level_history.py:23
│                   ├── LevelHistory.min()      domain/level_history.py:18
│                   └── format_time()           domain/history_line.py:42
│
└── sys.stdout.write(result)                    cli.py:70
```

## File index

| Layer | File |
|---|---|
| CLI adapter | [src/mahjonggstats/cli.py](../src/mahjonggstats/cli.py) |
| Application service | [src/mahjonggstats/application/stats_service.py](../src/mahjonggstats/application/stats_service.py) |
| Driven adapter — loader | [src/mahjonggstats/adapters/file_history_loader.py](../src/mahjonggstats/adapters/file_history_loader.py) |
| Driven adapter — presenter | [src/mahjonggstats/adapters/text_presenter.py](../src/mahjonggstats/adapters/text_presenter.py) |
| Domain — aggregate | [src/mahjonggstats/domain/history.py](../src/mahjonggstats/domain/history.py) |
| Domain — value object | [src/mahjonggstats/domain/history_line.py](../src/mahjonggstats/domain/history_line.py) |
| Domain — level statistics | [src/mahjonggstats/domain/level_history.py](../src/mahjonggstats/domain/level_history.py) |
| Port — outbound loader | [src/mahjonggstats/ports/history_loader.py](../src/mahjonggstats/ports/history_loader.py) |
| Port — outbound presenter | [src/mahjonggstats/ports/presenter.py](../src/mahjonggstats/ports/presenter.py) |
| Port — inbound query | [src/mahjonggstats/ports/stats_query.py](../src/mahjonggstats/ports/stats_query.py) |
