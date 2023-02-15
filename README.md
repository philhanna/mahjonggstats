# mahjonggstats
Go program to display statistics from Gnome mahjongg.

## Unstable
This version is still under active development.
The Python branch is fully functional.

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

The mainline is `cmd/main.go`.

## References
- [Github repository](https://github.com/philhanna/mahjonggstats)
- [Github repository for gnome-mahjongg](https://github.com/GNOME/gnome-mahjongg)
- [Gnome wiki for Mahjongg](https://wiki.gnome.org/Apps/Mahjongg)

[idMVC]: https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller