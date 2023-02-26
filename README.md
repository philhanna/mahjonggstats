# mahjonggstats
[![Go Report Card](https://goreportcard.com/badge/github.com/philhanna/mahjonggstats)][idGoReportCard]
[![PkgGoDev](https://pkg.go.dev/badge/github.com/philhanna/mahjonggstats)][idPkgGoDev]

Go program to display statistics from Gnome mahjongg.

## Software architecture
This project uses a [Model-View-Controller][idMVC] approach.
Here are the types associated with each:

### Model
- `History`
- `HistoryLine`
- `LevelHistory`
  
### View
- `View`

### Controller
- `Controller`

The mainline is `cmd/mahjonggstats.go`.

## References
- [Github repository](https://github.com/philhanna/mahjonggstats)
- [Github repository for gnome-mahjongg](https://github.com/GNOME/gnome-mahjongg)
- [Gnome wiki for Mahjongg](https://wiki.gnome.org/Apps/Mahjongg)

[idMVC]: https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller

[idGoReportCard]: https://goreportcard.com/report/github.com/philhanna/mahjonggstats
[idPkgGoDev]: https://pkg.go.dev/github.com/philhanna/mahjonggstats
