(declare (uses tcp))
(define-values (i o) (tcp-connect "localhost" 4242))
(write-line "/home/mateus/dev/projeto/server\tteste.c\t-g -pthread -pg" o)
(print (read-line i))