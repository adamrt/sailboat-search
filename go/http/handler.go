package http

import (
	"log"
	"net/http"

	"github.com/go-chi/render"
)

func (s *Server) handleListBoats() http.HandlerFunc {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		boats, err := s.boatRepo.List()
		if err != nil {
			log.Printf("failed boatRepo.List: %v", err)
			w.WriteHeader(http.StatusInternalServerError)
			render.JSON(w, r, nil)
			return
		}
		render.JSON(w, r, map[string]interface{}{"boats": boats})
	})
}

func (s *Server) handleListListings() http.HandlerFunc {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		listings, err := s.listingRepo.List()
		if err != nil {
			log.Printf("failed listingRepo.List: %v", err)
			w.WriteHeader(http.StatusInternalServerError)
			render.JSON(w, r, nil)
			return
		}
		render.JSON(w, r, map[string]interface{}{"listings": listings})
	})
}
