/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

#include "stack.h"
#include <string.h>


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
