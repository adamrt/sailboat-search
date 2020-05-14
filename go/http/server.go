package http

import (
	"fmt"
	"net/http"

	"github.com/adamrt/boats"
	"github.com/go-chi/chi"
	"github.com/go-chi/chi/middleware"
	"github.com/go-chi/render"
)

func NewServer(br boats.BoatRepo, lr boats.ListingRepo) *Server {
	r := chi.NewRouter()
	r.Use(
		render.SetContentType(render.ContentTypeJSON),
		middleware.Logger,
		middleware.Recoverer,
		middleware.DefaultCompress,
		middleware.RedirectSlashes,
	)
	s := Server{br, lr, r}
	s.SetupRoutes()
	return &s
}

type Server struct {
	boatRepo    boats.BoatRepo
	listingRepo boats.ListingRepo
	Router      *chi.Mux
}

func (s *Server) ListenAndServe(port int) error {
	ip := "0.0.0.0"
	fmt.Printf("Listening on %s:%d...\n", ip, port)
	return http.ListenAndServe(fmt.Sprintf("%s:%d", ip, port), s.Router)
}
