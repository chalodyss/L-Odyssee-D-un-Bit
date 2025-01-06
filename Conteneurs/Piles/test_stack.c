/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

#include "stack.h"
#include <criterion/criterion.h>
#include <stdio.h>


static void display(Stack *stack) {
    for (int i = stack->size - 1; i >= 0; i--) {
        printf("%s\n", (char *) stack->data[i]);
    }

    puts("----------");
}

Test(stack, primitives) {
    Stack s;

    init(&s);
    printf("Init\n----------\n");
    cr_assert(is_empty(&s) == true);

    push(&s, "A");
    display(&s);
    cr_assert(strcmp(s.data[s.size - 1], "A") == 0);
    cr_assert(s.size == 1);

    push(&s, "B");
    display(&s);
    cr_assert(strcmp(s.data[s.size - 1], "B") == 0);
    cr_assert(s.size == 2);

    push(&s, "C");
    display(&s);
    cr_assert(strcmp(s.data[s.size - 1], "C") == 0);
    cr_assert(s.size == 3);

    pop(&s);
    display(&s);
    cr_assert(s.data[s.size] == 0);
    cr_assert(s.size == 2);

    pop(&s);
    display(&s);
    cr_assert(s.data[s.size] == 0);
    cr_assert(s.size == 1);

    pop(&s);
    display(&s);
    cr_assert(is_empty(&s) == true);
}
