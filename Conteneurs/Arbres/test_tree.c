/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

#include "tree.h"
#include <criterion/criterion.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define FGWHITE_BGBLUE  "\033[38;5;255;48;5;27m"
#define BGCYAN          "\033[48;5;50m"
#define EMPTY           "\033[0m"

#define OFFSET          2

int     row             = 0;


static bool compare(int a, int b) {
    return a > b;
}

static void display_tree(Node *root, int level, int **array) {
    if (root == NULL) return;

    int spaces = level * OFFSET;

    display_tree(root->right, level + 1, array);

    int i;

    for (i = 0; i < spaces; i++) {
        array[row][i] = 0;
    }

    array[row][i]   = root->data;
    row             += 1;

    display_tree(root->left, level + 1, array);
}

Test(tree, primitives) {
    Node        tree;
    predicate   p = compare;

    tree.data   = 7;
    tree.left   = NULL;
    tree.right  = NULL;

    printf("Init\n----------\n");

    cr_assert(get_depth(&tree) == 1);

    printf("Insert\n----------\n");

    insert(&tree, 2, p);
    cr_assert(get_depth(&tree) == 2);
    insert(&tree, 8, p);
    cr_assert(get_depth(&tree) == 2);
    insert(&tree, 5, p);
    cr_assert(get_depth(&tree) == 3);
    insert(&tree, 3, p);
    cr_assert(get_depth(&tree) == 4);
    insert(&tree, 9, p);
    cr_assert(get_depth(&tree) == 4);
    insert(&tree, 10, p);
    cr_assert(get_depth(&tree) == 4);
    insert(&tree, 6, p);
    cr_assert(get_depth(&tree) == 4);
    insert(&tree, 1, p);
    cr_assert(get_depth(&tree) == 4);

    printf("Search\n----------\n");

    cr_assert(search(&tree, 1, p) == 1);
    cr_assert(search(&tree, 2, p) == 2);
    cr_assert(search(&tree, 3, p) == 3);
    cr_assert(search(&tree, 4, p) == -1);
    cr_assert(search(&tree, 5, p) == 5);
    cr_assert(search(&tree, 6, p) == 6);
    cr_assert(search(&tree, 7, p) == 7);
    cr_assert(search(&tree, 8, p) == 8);
    cr_assert(search(&tree, 9, p) == 9);
    cr_assert(search(&tree, 10, p) == 10);
    cr_assert(search(&tree, -8, p) == -1);

    printf("Display\n----------\n");

    int size    = pow(2, get_depth(&tree)) * 2;
    int **array = calloc(size, sizeof(int *));

    for (int i = 0; i < size; i++) {
        array[i] = calloc(size / 2, sizeof(int));
    }

    display_tree(&tree, 0, array);

    for (int j = 0; j <= (get_depth(&tree) - 1) * OFFSET; j++) {
        for (int i = row - 1; i >= 0; i--) {
            if (array[i][j] == 0)   printf(" ");
            else                    printf("%s %d %s", FGWHITE_BGBLUE, array[i][j], EMPTY);
        }
        printf("\n");
    }

    printf("\n");
}
