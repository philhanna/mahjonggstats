# Call tree — mahjonggstats invocation

Traces a single call from the command line to stdout across every layer.
Three output paths branch inside `TextPresenter.render`; each is shown separately.

```
main()                                          cli.py:12
├── build_parser()                              cli.py:54
├── validate_sort_option(ns.sort)               cli.py:89
├── StatsQueryPort(...)                         ports/stats_query_port.py:8
├── StatsService(                               application/stats_service.py:13
│     loader=FileHistoryLoader(),               adapters/file_history_loader.py:13
│     presenter=TextPresenter()                 adapters/text_presenter.py:25
│   )
├── StatsService.run(query)                     application/stats_service.py:39
│   ├── FileHistoryLoader.load()                adapters/file_history_loader.py:32
│   │   └── HistoryLine.parse(line)  [×N]       domain/history_line.py:30
│   ├── History.from_records(records)           domain/history.py:31
│   │   └── LevelHistory(...)        [×level]   domain/level_history.py:11
│   └── TextPresenter.render(history, query)    adapters/text_presenter.py:45
│       ├── _resolve_levels(history, query)     adapters/text_presenter.py:76
│       │   └── History.level_names()           domain/history.py:80
│       │       └── LevelHistory.mean()  [×N]   domain/level_history.py:45
│       │
│       ├── [if level_names_only]
│       │   └── _show_level_names(...)          adapters/text_presenter.py:124
│       │
│       ├── [if verbose]
│       │   ├── _show_heading(history)          adapters/text_presenter.py:108
│       │   │   ├── History.earliest_date()     domain/history.py:54
│       │   │   └── History.latest_date()       domain/history.py:67
│       │   └── _show_all_levels(history, query) adapters/text_presenter.py:183
│       │       └── [per level]
│       │           ├── LevelHistory.mean()     domain/level_history.py:45
│       │           ├── LevelHistory.standard_deviation()  domain/level_history.py:56
│       │           ├── LevelHistory.confidence()          domain/level_history.py:74
│       │           ├── LevelHistory.count()    domain/level_history.py:26
│       │           └── HistoryLine.time_date() domain/history_line.py:53
│       │               └── format_time()       domain/history_line.py:93
│       │
│       └── [default — summary]
│           └── _show_summary(history, query)   adapters/text_presenter.py:141
│               └── [per level]
│                   ├── LevelHistory.count()    domain/level_history.py:26
│                   ├── LevelHistory.mean()     domain/level_history.py:45
│                   ├── LevelHistory.min()      domain/level_history.py:34
│                   └── format_time()           domain/history_line.py:93
│
└── sys.stdout.write(result)                    cli.py:48
```

## File index

| Layer | File |
|---|---|
| CLI adapter | [src/mahjonggstats/cli.py](../src/mahjonggstats/cli.py) |
| Application service (use case) | [src/mahjonggstats/application/stats_service.py](../src/mahjonggstats/application/stats_service.py) |
| Driven adapter — loader | [src/mahjonggstats/adapters/file_history_loader.py](../src/mahjonggstats/adapters/file_history_loader.py) |
| Driven adapter — presenter | [src/mahjonggstats/adapters/text_presenter.py](../src/mahjonggstats/adapters/text_presenter.py) |
| Domain — aggregate | [src/mahjonggstats/domain/history.py](../src/mahjonggstats/domain/history.py) |
| Domain — value object | [src/mahjonggstats/domain/history_line.py](../src/mahjonggstats/domain/history_line.py) |
| Domain — level statistics | [src/mahjonggstats/domain/level_history.py](../src/mahjonggstats/domain/level_history.py) |
| Port — outbound loader | [src/mahjonggstats/ports/history_loader_port.py](../src/mahjonggstats/ports/history_loader_port.py) |
| Port — outbound presenter | [src/mahjonggstats/ports/presenter_port.py](../src/mahjonggstats/ports/presenter_port.py) |
| Port — inbound query | [src/mahjonggstats/ports/stats_query_port.py](../src/mahjonggstats/ports/stats_query_port.py) |
