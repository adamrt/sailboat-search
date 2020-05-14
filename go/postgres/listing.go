package postgres

import (
	"time"

	"github.com/adamrt/boats"
	"github.com/jmoiron/sqlx"
	"github.com/pkg/errors"
)

func NewListingRepo(db *sqlx.DB) *ListingRepo {
	return &ListingRepo{db: db}
}

type ListingRepo struct {
	db *sqlx.DB
}

// List returns all boats.
func (repo *ListingRepo) List() ([]boats.Listing, error) {
	ll := []boats.Listing{}
	err := repo.db.Select(&ll, "SELECT * FROM listing")
	if err != nil {
		return []boats.Listing{}, errors.Wrapf(err, "ListingRepo.List failed")
	}
	return ll, nil
}

// Get returns a listing by pk.
func (repo *ListingRepo) Get(id int) (boats.Listing, error) {
	l := boats.Listing{}
	err := repo.db.Get(&l, "SELECT * FROM listing WHERE id = $1 LIMIT 1", id)
	if err != nil {
		return boats.Listing{}, errors.Wrapf(err, "ListingRepo.Get failed with %d", id)
	}
	return l, nil
}

// Create listing and update relevant fields on the passed in struct.
func (repo *ListingRepo) Create(l *boats.Listing) error {
	q := `INSERT INTO listing (boat_id, title, slug, price, year, url, location, country)
              VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
              RETURNING id, created_at, updated_at;`

	var id int
	var cAt, uAt time.Time
	err := repo.db.QueryRow(
		q, l.BoatID, l.Title, l.Slug, l.Price, l.Year, l.URL, l.Location, l.Country,
	).Scan(&id, &cAt, &uAt)
	if err != nil {
		return errors.Wrapf(err, "ListingRepo.Create failed for %+v", l)
	}
	l.ID = id
	l.CreatedAt = cAt
	l.UpdatedAt = uAt
	return nil
}
