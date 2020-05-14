package http

import "github.com/go-chi/chi"

func (s *Server) SetupRoutes() {
	s.Router.Route("/v1", func(r chi.Router) {
		r.Get("/boats", s.handleListBoats())
		r.Get("/listings", s.handleListListings())
	})
}
