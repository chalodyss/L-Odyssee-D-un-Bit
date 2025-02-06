/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

// ################################################################################

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define FGWHITE_BGBLUE  "\033[38;5;255;48;5;27m"
#define BGCYAN          "\033[48;5;50m"
#define EMPTY           "\033[0m"

#define OFFSET          2

typedef struct          Node {
    int                 data;
    struct Node         *left;
    struct Node         *right;
}                       Node;

typedef bool            (*predicate) (int, int);

// ################################################################################

int                     row = 0;

// ################################################################################

Node        *insert(Node *tree, int elem, predicate p) {
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

int         search(Node *tree, int elem, predicate p) {
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

int         get_depth(Node *tree) {
    if (tree == NULL) {
        return 0;
    } else {
        int left  = get_depth(tree->left);
        int right = get_depth(tree->right);
        return (left > right ?  1 + left : 1 + right);
    }
}

void        display_tree(Node *root, int level, int **array) {
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

// ################################################################################

bool        compare(int a, int b) {
    return a > b;
}

// ################################################################################

int         main(void) {
    Node        tree;
    predicate   p = compare;

    tree.data   = 7;
    tree.left   = NULL;
    tree.right  = NULL;

    printf("\n----------\nInsert\n----------\n\n");

    insert(&tree, 2, p);
    insert(&tree, 8, p);
    insert(&tree, 5, p);
    insert(&tree, 3, p);
    insert(&tree, 9, p);
    insert(&tree, 10, p);
    insert(&tree, 6, p);
    insert(&tree, 1, p);

    printf("\n----------\nSearch\n----------\n\n");

    printf("search(&tree, 1, p)  : %d\n", search(&tree, 1, p));
    printf("search(&tree, 2, p)  : %d\n", search(&tree, 2, p));
    printf("search(&tree, 3, p)  : %d\n", search(&tree, 3, p));
    printf("search(&tree, 4, p)  : %d\n", search(&tree, 4, p));
    printf("search(&tree, 5, p)  : %d\n", search(&tree, 5, p));
    printf("search(&tree, 6, p)  : %d\n", search(&tree, 6, p));
    printf("search(&tree, 7, p)  : %d\n", search(&tree, 7, p));
    printf("search(&tree, 8, p)  : %d\n", search(&tree, 8, p));
    printf("search(&tree, 9, p)  : %d\n", search(&tree, 9, p));
    printf("search(&tree, 10, p) : %d\n", search(&tree, 10, p));
    printf("search(&tree, -8, p) : %d\n", search(&tree, -8, p));

    printf("\n----------\nDisplay\n----------\n\n");

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

// ################################################################################
