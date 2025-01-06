# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

CC	=	gcc

PROG	=	test_queue

CFLAGS	=	-Wextra -Wall

LDFLAGS	=	-lcriterion

SRCS	=	queue.c \
		test_queue.c

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
