/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

// ################################################################################

#include <stdbool.h>
#include <stdio.h>
#include <string.h>

#define SIZE 4

typedef struct {
    int     size;
    void    *data[SIZE];
}           Stack;

// ################################################################################

void        init(Stack *stack) {
    stack->size = 0;
    memset(stack->data, 0, sizeof(stack->data));
}

bool        is_empty(Stack *stack) {
    return stack->size == 0;
}

void        push(Stack *stack, void *elem) {
    stack->data[stack->size++] = elem;
}

void        *pop(Stack *stack) {
    void    *elem = NULL;

    stack->size--;
    elem = stack->data[stack->size];
    stack->data[stack->size] = 0;

    return elem;
}

// ################################################################################

void        display(Stack *stack) {
    for (int i = stack->size - 1; i >= 0; i--) {
        printf("%s\n", (char *) stack->data[i]);
    }

    puts("----------");
}

// ################################################################################

int         main(void) {
    Stack s;

    init(&s);
    printf("Init\n----------\n");

    push(&s, "A");
    display(&s);

    push(&s, "B");
    display(&s);

    push(&s, "C");
    display(&s);

    pop(&s);
    display(&s);

    pop(&s);
    display(&s);

    pop(&s);
    display(&s);
}

// ################################################################################
