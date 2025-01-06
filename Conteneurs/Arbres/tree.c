/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

#include "tree.h"
#include <stdlib.h>


Node    *insert(Node *tree, int elem, predicate p) {
    if (tree == NULL) {
        tree = calloc(1, sizeof(Node));
        tree->data  = elem;
        tree->left  = NULL;
        tree->right = NULL;
    } else if (p(elem, tree->data)) {
        tree->right = insert(tree->right, elem, p);
    } else {
        tree->left = insert(tree->left, elem, p);
    }
    return tree;
}

int     search(Node *tree, int elem, predicate p) {
    if (tree == NULL) {
        return -1;
    } else if (tree->data == elem) {
        return tree->data;
    } else if (p(elem, tree->data)) {
        return search(tree->right, elem, p);
    } else {
        return search(tree->left, elem, p);
    }
}

int     get_depth(Node *tree) {
    if (tree == NULL) {
        return 0;
    } else {
        int left  = get_depth(tree->left);
        int right = get_depth(tree->right);
        return (left > right ?  1 + left : 1 + right);
    }
}
