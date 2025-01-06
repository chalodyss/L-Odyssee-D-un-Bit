/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

#ifndef _TREE_H_
#define _TREE_H_

#include <stdbool.h>

typedef struct Node {
    int         data;
    struct Node *left;
    struct Node *right;
}               Node;

typedef bool (*predicate) (int, int);

Node    *insert(Node *, int, predicate);
int     search(Node *, int, predicate);
int     get_depth(Node *);

#endif
