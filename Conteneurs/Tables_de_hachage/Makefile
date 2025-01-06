# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

CC	=	gcc

PROG	=	test_hashtable

CFLAGS	=	-Wextra  -Wall

LDFLAGS	=	-lcriterion

SRCS	=	hashtable.c \
		test_hashtable.c

OBJS	=	$(SRCS:.c=.o)

all:		$(PROG)

$(PROG):	$(OBJS)
		$(CC) $(CFLAGS) $(LDFLAGS) $(OBJS) -o $(PROG)

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(PROG)

re: fclean all

.PHONY: fclean clean re
