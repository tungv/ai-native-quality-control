package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"mime"
	"net/http"
	"strconv"
	"strings"
	"unicode/utf8"
)

const (
	baselineScenario         = "baseline"
	priceRoundingScenario    = "price-rounding"
	contextInjectionScenario = "context-injection"
	maxChatBodyBytes         = 16 << 10
	maxMessageCharacters     = 2000
)

type api struct {
	scenario string
}

type product struct {
	SKU        string `json:"sku"`
	Name       string `json:"name"`
	PriceCents int    `json:"price_cents"`
	Currency   string `json:"currency"`
	InStock    bool   `json:"in_stock"`
}

type chatRequest struct {
	Message string `json:"message"`
	Context string `json:"context,omitempty"`
}

type chatResponse struct {
	Answer    string   `json:"answer"`
	Citations []string `json:"citations"`
	Actions   []string `json:"actions"`
}

func newAPI(scenario string) (*api, error) {
	if scenario == "" {
		scenario = baselineScenario
	}
	switch scenario {
	case baselineScenario, priceRoundingScenario, contextInjectionScenario:
		return &api{scenario: scenario}, nil
	default:
		return nil, fmt.Errorf("unknown LAB_SCENARIO %q; expected baseline, price-rounding, or context-injection", scenario)
	}
}

func (a *api) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.Header().Set("X-Content-Type-Options", "nosniff")
	w.Header().Set("Cache-Control", "no-store")
	switch {
	case r.URL.Path == "/health":
		if !allowMethod(w, r, http.MethodGet) {
			return
		}
		writeJSON(w, http.StatusOK, map[string]string{"status": "ok", "scenario": a.scenario})
	case r.URL.Path == "/products":
		if allowMethod(w, r, http.MethodGet) {
			a.listProducts(w, r)
		}
	case strings.HasPrefix(r.URL.Path, "/products/"):
		if allowMethod(w, r, http.MethodGet) {
			a.getProduct(w, r)
		}
	case r.URL.Path == "/chat":
		if allowMethod(w, r, http.MethodPost) {
			a.chat(w, r)
		}
	default:
		writeError(w, http.StatusNotFound, "route not found")
	}
}

func allowMethod(w http.ResponseWriter, r *http.Request, method string) bool {
	if r.Method == method {
		return true
	}
	w.Header().Set("Allow", method)
	writeError(w, http.StatusMethodNotAllowed, "method not allowed")
	return false
}

func (a *api) products() []product {
	products := []product{
		{SKU: "trail-shoes", Name: "Trail Shoes", PriceCents: 12900, Currency: "USD", InStock: true},
		{SKU: "rain-jacket", Name: "Rain Jacket", PriceCents: 8900, Currency: "USD", InStock: true},
		{SKU: "city-backpack", Name: "City Backpack", PriceCents: 5900, Currency: "USD", InStock: false},
	}
	// An explicit, reproducible teaching fault. The baseline uses integer cents.
	if a.scenario == priceRoundingScenario {
		products[0].PriceCents = 129
	}
	return products
}

func (a *api) listProducts(w http.ResponseWriter, r *http.Request) {
	limit := 10
	query := r.URL.Query()
	if values, present := query["limit"]; present {
		if len(values) != 1 {
			writeError(w, http.StatusBadRequest, "limit must be a single integer from 1 to 20")
			return
		}
		parsed, err := strconv.Atoi(values[0])
		if err != nil || parsed < 1 || parsed > 20 {
			writeError(w, http.StatusBadRequest, "limit must be an integer from 1 to 20")
			return
		}
		limit = parsed
	}
	search := strings.ToLower(strings.TrimSpace(query.Get("q")))
	matches := make([]product, 0)
	for _, item := range a.products() {
		if strings.Contains(strings.ToLower(item.Name), search) {
			matches = append(matches, item)
			if len(matches) == limit {
				break
			}
		}
	}
	writeJSON(w, http.StatusOK, struct {
		Products []product `json:"products"`
	}{Products: matches})
}

func (a *api) getProduct(w http.ResponseWriter, r *http.Request) {
	sku := strings.TrimPrefix(r.URL.Path, "/products/")
	for _, item := range a.products() {
		if item.SKU == sku {
			writeJSON(w, http.StatusOK, item)
			return
		}
	}
	writeError(w, http.StatusNotFound, "product not found")
}

func (a *api) chat(w http.ResponseWriter, r *http.Request) {
	mediaType, _, err := mime.ParseMediaType(r.Header.Get("Content-Type"))
	if err != nil || mediaType != "application/json" {
		writeError(w, http.StatusUnsupportedMediaType, "Content-Type must be application/json")
		return
	}
	r.Body = http.MaxBytesReader(w, r.Body, maxChatBodyBytes)
	defer r.Body.Close()
	decoder := json.NewDecoder(r.Body)
	decoder.DisallowUnknownFields()
	var wireInput struct {
		Message string          `json:"message"`
		Context json.RawMessage `json:"context"`
	}
	if err := decoder.Decode(&wireInput); err != nil {
		writeDecodeError(w, err)
		return
	}
	// A second value (including null), malformed tail, or excessive whitespace
	// is invalid. Reading through EOF also enforces the full body byte limit.
	if err := decoder.Decode(new(any)); !errors.Is(err, io.EOF) {
		writeDecodeError(w, err)
		return
	}
	input := chatRequest{Message: strings.TrimSpace(wireInput.Message)}
	if wireInput.Context != nil {
		// JSON null is not a context string. encoding/json otherwise silently
		// accepts null into a string field, so enforce that boundary explicitly.
		if string(wireInput.Context) == "null" {
			writeDecodeError(w, errors.New("context must be a string"))
			return
		}
		if err := json.Unmarshal(wireInput.Context, &input.Context); err != nil {
			writeDecodeError(w, err)
			return
		}
	}
	if input.Message == "" {
		writeError(w, http.StatusBadRequest, "message is required")
		return
	}
	if utf8.RuneCountInString(input.Message) > maxMessageCharacters {
		writeError(w, http.StatusBadRequest, "message must be at most 2000 characters")
		return
	}
	writeJSON(w, http.StatusOK, a.respond(input))
}

func (a *api) respond(input chatRequest) chatResponse {
	response := chatResponse{Citations: []string{}, Actions: []string{}}
	// Deliberately broken only when opted in. This returns a synthetic action
	// label and canary; it never performs a refund or reads a real secret.
	if a.scenario == contextInjectionScenario && strings.Contains(input.Context, "[[OVERRIDE]]") {
		response.Answer = "Untrusted override accepted. Synthetic canary: LAB_CANARY_ONLY."
		response.Actions = []string{"issue_refund"}
		return response
	}
	// The baseline deliberately ignores context. This teaches a trust boundary;
	// it is not an LLM, RAG implementation, or production injection defense.
	message := strings.ToLower(input.Message)
	switch {
	case strings.Contains(message, "refund"), strings.Contains(message, "return"):
		response.Answer = "I cannot issue refunds. Please contact support for returns or refunds."
	case strings.Contains(message, "shoes"), strings.Contains(message, "trail"):
		response.Answer = "Trail Shoes cost $129.00 and are in stock."
		response.Citations = []string{"trail-shoes"}
	case strings.Contains(message, "jacket"):
		response.Answer = "Rain Jacket costs $89.00 and is in stock."
		response.Citations = []string{"rain-jacket"}
	case strings.Contains(message, "backpack"):
		response.Answer = "City Backpack costs $59.00 and is out of stock."
		response.Citations = []string{"city-backpack"}
	default:
		response.Answer = "Which product would you like to know about: Trail Shoes, Rain Jacket, or City Backpack?"
	}
	return response
}

func writeDecodeError(w http.ResponseWriter, err error) {
	var tooLarge *http.MaxBytesError
	if errors.As(err, &tooLarge) {
		writeError(w, http.StatusRequestEntityTooLarge, "request body must be at most 16384 bytes")
		return
	}
	writeError(w, http.StatusBadRequest, "body must be one JSON object with only message and optional context string fields")
}

func writeError(w http.ResponseWriter, status int, message string) {
	writeJSON(w, status, map[string]string{"error": message})
}

func writeJSON(w http.ResponseWriter, status int, value any) {
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(value)
}
