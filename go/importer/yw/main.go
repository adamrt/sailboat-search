package yw

import (
	"fmt"
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
const BaseURL = "http://www.yachtworld.com"
const URLTemplate = BaseURL + "/boats-for-sale/condition-used/type-sail/?keyword=%s"

var re = regexp.MustCompile("[^a-z0-9]+")

func slugify(s string) string {
	return strings.Trim(re.ReplaceAllString(strings.ToLower(s), "-"), "-")
}

func NewImporter(lr boats.ListingRepo) *Importer {
	return &Importer{
		listingRepo: lr,
		http:        &http.Client{Timeout: time.Second * 10},
	}
}

type Importer struct {
	listingRepo boats.ListingRepo
	http        *http.Client
}

func (i Importer) Import(b boats.Boat) ([]*boats.Listing, error) {
	term := strings.ToLower(strings.ReplaceAll(b.Name, " ", "%20"))
	url := fmt.Sprintf(URLTemplate, term)
	ll := make([]*boats.Listing, 0)

	c := colly.NewCollector()
	c.OnHTML("a[data-reporting-click-listing-type='standard listing']", func(e *colly.HTMLElement) {
		l := &boats.Listing{BoatID: b.ID}
		ps := e.ChildAttr("meta[property=price]", "content")
		if ps == "" {
			//log.Println("price is empty, skipping...")
			return
		}
		price, err := strconv.ParseFloat(ps, 64)
		if err != nil {
			log.Printf("invalid price %s, skipping. %v", e.ChildAttr("meta[property=price]", "content"), err)
			return
		}
		l.Location = e.ChildText(".listing-card-location")
		l.URL = e.ChildAttr("meta[property=url]", "content")
		l.Price = price
		title := e.ChildText(".listing-card-title")
		l.Title = title
		l.Slug = slugify(title)
		lengthYear := strings.Split(e.ChildText(".listing-card-length-year.regular"), " / ")
		length, err := strconv.Atoi(strings.ReplaceAll(lengthYear[0], " ft", ""))
		if err != nil {
			log.Printf("invalid length %s, skipping", lengthYear[1])
			return
		}
		if float64(length) != b.Length {
			log.Printf("length %v doesn't match boat length %v - %s - %s", length, b.Length, b.Name, title)
			return
		}

		// year, err := strconv.Atoi(lengthYear[1])
		// if err != nil {
		// 	log.Printf("invalid year %s, skipping", lengthYear[1])
		// 	return
		// }
		// log.Printf("imported %s", l.Title)
		// l.Year = year
		// ll = append(ll, l)
	})
	log.Println(url)
	c.Visit("https://www.yachtworld.com/boats-for-sale/type-sail/make-cal/region-northamerica/?length=33-33")

	return ll, nil
}
