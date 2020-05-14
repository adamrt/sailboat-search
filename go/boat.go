package boats

import "time"

type BoatRepo interface {
	Get(id int) (Boat, error)
	List() ([]Boat, error)
	Create(b *Boat) error
}

type BoatImporter interface {
	Import() ([]Boat, error)
}

type Boat struct {
	ID        int       `db:"id"         json:"id"`
	CreatedAt time.Time `db:"created_at" json:"-"`
	UpdatedAt time.Time `db:"updated_at" json:"-"`

	Name        string  `db:"name"         json:"name"`
	Slug        string  `db:"slug"         json:"slug"`
	Length      float64 `db:"length"       json:"length"`
	IsBluewater bool    `db:"is_bluewater" json:"is_bluewater"`
}
