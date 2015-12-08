checkSimple(C) :- integer(C).

%integrals
	%x^n
	integral(X, X, IY) :- integral(X^1,X, IY).
	integral(X^N, X, X^(N+1)/(N+1)) :- checkSimple(N), N =\= -1.

	integral(X^(-1), X, ln(abs(x))).

	%a^x
	integral(A^X, X, A^X/ln(A)) :- checkSimple(A).
	integral(A^(-X), X, ln(A)/A^X) :- checkSimple(A).

	integral(A^(C*X), X, (A^C)^IY) :- checkSimple(C), integral(A^X, X, IY).
	integral(A^(X*C), X, IY) :- checkSimple(C), integral(A^(C*X), X, IY).
	%integral(A^(-X*C), X, IY) :- checkSimple(C), integral(A^(X*-C), X, IY).


	integral(A^(B-C), X, IY) :- checkSimple(B), integral(A^(-C+B), X, IY).
	integral(A^(B+C), X, A^B*IY) :- checkSimple(B), integral(A^C, X, IY).
	integral(A^(B+C), X, IY) :- checkSimple(C), integral(A^(C+B), X, IY).
	
%properties
integral(C, X, C*X) :- checkSimple(C). 

integral(Z+Y, X, IZ+IY) :- integral(Z, X, IZ), integral(Y, X, IY).
integral(Z-Y, X, IZ-IY) :- integral(Z, X, IZ), integral(Y, X, IY).

integral(C*Y, X, C*IY) :- checkSimple(C), integral(Y, X, IY).
integral(Y*C, X, IY) :- checkSimple(C), integral(C*Y, X, IY).


%integral(3^(2*x),x,X).