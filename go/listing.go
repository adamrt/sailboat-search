package boats

import (
	"time"
)

type ListingRepo interface {
	List() ([]Listing, error)
	Get(id int) (Listing, error)
	Create(l *Listing) error
}

type ListingImporter interface {
	Import(b Boat) ([]Listing, error)
}

type Listing struct {
	ID        int       `db:"id"         json:"id"`
	CreatedAt time.Time `db:"created_at" json:"-"`
	UpdatedAt time.Time `db:"updated_at" json:"-"`

	Title    string  `db:"title"    json:"title"`
	Slug     string  `db:"slug"     json:"slug"`
	Price    float64 `db:"price"    json:"price"`
	Year     int     `db:"year"     json:"year"`
	URL      string  `db:"url"      json:"url"`
	Location string  `db:"location" json:"location"`
	Country  string  `db:"country"  json:"country"`

	BoatID int `db:"boat_id" json:"-"`
}
