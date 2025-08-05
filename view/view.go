package view

// ---------------------------------------------------------------------
// Type definitions
// ---------------------------------------------------------------------
type View interface {
	ShowLevelNames()
}

type DefaultView struct {

}

func NewDefaultView() *DefaultView {
	p := new(DefaultView)
	return p
}

// ---------------------------------------------------------------------
// Methods
// ---------------------------------------------------------------------
