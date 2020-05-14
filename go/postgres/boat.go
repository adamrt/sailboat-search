package postgres

import (
	"time"

	"github.com/adamrt/boats"
	"github.com/jmoiron/sqlx"
	"github.com/pkg/errors"
)

func NewBoatRepo(db *sqlx.DB) *BoatRepo {
	return &BoatRepo{db: db}
}

type BoatRepo struct {
	db *sqlx.DB
}

// List returns all boats.
func (repo *BoatRepo) List() ([]boats.Boat, error) {
	bb := []boats.Boat{}
	err := repo.db.Select(&bb, "SELECT * FROM boat")
	if err != nil {
		return []boats.Boat{}, errors.Wrapf(err, "BoatRepo.List failed")
	}
	return bb, nil
}

// Get returns a boat by pk.
func (repo *BoatRepo) Get(id int) (boats.Boat, error) {
	b := boats.Boat{}
	err := repo.db.Get(&b, "SELECT * FROM boat WHERE id = $1 LIMIT 1", id)
	if err != nil {
		return boats.Boat{}, errors.Wrapf(err, "BoatRepo.Get failed with %d", id)
	}
	return b, nil
}

// Create boat and update relevant fields on the passed in struct.
func (repo *BoatRepo) Create(b *boats.Boat) error {
	q := `INSERT INTO boat (name, slug, length, is_bluewater)
              VALUES ($1, $2, $3, $4)
              RETURNING id, created_at, updated_at;`
	var id int
	var cAt, uAt time.Time
	err := repo.db.QueryRow(q, b.Name, b.Slug, b.Length, b.IsBluewater).Scan(&id, &cAt, &uAt)
	if err != nil {
		return errors.Wrapf(err, "BoatRepo.Create failed for %+v", b)
	}
	b.ID = id
	b.CreatedAt = cAt
	b.UpdatedAt = uAt
	return nil
}
