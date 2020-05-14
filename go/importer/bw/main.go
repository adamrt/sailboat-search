package bw

import (
	"log"
	"net/http"
	"regexp"
	"strconv"
	"strings"
	"time"

	"github.com/adamrt/boats"
	"github.com/gocolly/colly/v2"
)

// 2279=sail, 2285=used, ps=results per page

const BaseURL = "http://bluewaterboats.org/about/index/"

var re = regexp.MustCompile("[^a-z0-9]+")

func slugify(s string) string {
	return strings.Trim(re.ReplaceAllString(strings.ToLower(s), "-"), "-")
}

func NewBoatImporter(br boats.BoatRepo) *BoatImporter {
	return &BoatImporter{
		boatRepo: br,
		http:     &http.Client{Timeout: time.Second * 10},
	}
}

type BoatImporter struct {
	boatRepo boats.BoatRepo
	http     *http.Client
}

func (i BoatImporter) Import() ([]*boats.Boat, error) {
	url := BaseURL
	bb := make([]*boats.Boat, 0)

	c := colly.NewCollector()
	c.OnHTML(".boatname", func(e *colly.HTMLElement) {
		b := &boats.Boat{}
		b.Name = e.ChildText("a")
		b.Slug = slugify(b.Name)
		z := strings.Split(b.Name, " ")
		l := z[len(z)-1]
		length, err := strconv.ParseFloat(l, 64)
		if err != nil {
			log.Printf("length is bad %s", l)
		}
		b.Length = length
		bb = append(bb, b)
	})
	c.Visit(url)

	return bb, nil
}
