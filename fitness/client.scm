(declare (uses tcp))
(define-values (i o) (tcp-connect "localhost" 4242))
(write-line "./\tteste.c\t-g -pthread -pg" o)
(print (read-line i))