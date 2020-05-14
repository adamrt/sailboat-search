package main

import (
	"flag"
	"fmt"
	"log"

	"github.com/adamrt/boats/http"
	"github.com/adamrt/boats/importer/bw"
	"github.com/adamrt/boats/importer/yw"
	"github.com/adamrt/boats/postgres"
	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
)

func usage() {
	fmt.Println("boats [serve|import]")
}

func main() {
	flag.Parse()
	if flag.NArg() != 1 {
		usage()
		return
	}

	arg := flag.Args()[0]
	if arg != "serve" && arg != "import" {
		usage()
		return
	}

	db := sqlx.MustConnect("postgres", "postgresql://boats:password@127.0.0.1/boats")
	defer db.Close()
	br := postgres.NewBoatRepo(db)
	lr := postgres.NewListingRepo(db)

	if arg == "serve" {
		s := http.NewServer(br, lr)
		err := s.ListenAndServe(8100)
		if err != nil {
			log.Printf("server crashed %v", err)
		}
		return
	}

	if arg == "import" {
		bImporter := bw.NewBoatImporter(br)
		importedBoats, err := bImporter.Import()
		if err != nil {
			log.Printf("failed to import boats %v", err)
			return
		}

		for _, b := range importedBoats {
			err = br.Create(b)
			if err != nil {
				log.Printf("failed to create %v", err)
				continue
			}
		}

		bb, err := br.List()
		if err != nil {
			log.Printf("failed to list boats %v", err)
			return
		}

		lImporter := yw.NewImporter(lr)
		for _, b := range bb {
			ll, err := lImporter.Import(b)
			if err != nil {
				log.Printf("failed to import %v", err)
				return
			}
			for _, l := range ll {
				err = lr.Create(l)
				if err != nil {
					log.Printf("failed to create %v", err)
					return
				}

			}
		}

		log.Println("finished...")
		return
	}
}
