# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

CC	=	gcc

PROG	=	test_tree

CFLAGS	=	-Wextra  -Wall

LDFLAGS	=	-lcriterion -lm

SRCS	=	tree.c \
		test_tree.c

OBJS	=	$(SRCS:.c=.o)

all:		$(PROG)

$(PROG):	$(OBJS)
		$(CC) $(CFLAGS) $(OBJS) -o $(PROG) $(LDFLAGS) 

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(PROG)

re: fclean all

.PHONY: fclean clean re
