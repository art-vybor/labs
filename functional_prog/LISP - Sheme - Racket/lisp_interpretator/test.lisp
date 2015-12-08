(define f 42)

(define (b x y) (< x y))

(define (sqr_max x y) (
		; define in definw
		(define (max x y) (
			if (< x y) y x ))
		(define (sqr x) (* x x))
		(* (sqr (max x y)))
	)
)

( define (g x y) ( + x y))

(define (fact x)
  (if (< x 3)
      x
      (* (fact (- x 1)) x)))

; (define z <)
; (z 1 2)
; (f (lambda (x) (* x 2)) 10) 

; (compare lesser 1 2)

(fact (+ 2 2))
(sqr_max 2 3)
(max 1 2)