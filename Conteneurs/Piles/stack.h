/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

#ifndef _STACK_H_
#define _STACK_H_

#include <stdbool.h>

#define SIZE 4

typedef struct {
    int     size;
    void    *data[SIZE];
}           Stack;

void        init(Stack *);
bool        is_empty(Stack *);
void        push(Stack *, void *);
void        *pop(Stack *);

#endif
