/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

// ################################################################################

#include <stdbool.h>
#include <stdio.h>
#include <string.h>

#define BLUE        "\033[1;34m"
#define RED         "\033[91m"
#define EMPTY       "\033[0m"

#define SIZE_BUFFER 4

typedef struct {
    int     head;
    int     tail;
    int     size;
    void    *data[SIZE_BUFFER];
}           Queue;

// ################################################################################

void        init(Queue *buffer) {
    buffer->head = 0;
    buffer->tail = 0;
    buffer->size = 0;
    memset(buffer->data, 0, sizeof(buffer->data));
}

void        push(Queue *buffer, void *elem) {
    if (buffer->size < SIZE_BUFFER) {
        buffer->data[buffer->head++] = elem;
        buffer->size++;
    }
    if (buffer->head >= SIZE_BUFFER) buffer->head = 0;
}

void        *pop(Queue *buffer) {
    void    *elem = NULL;

    if (buffer->size > 0) {
        elem = buffer->data[buffer->tail++];
        buffer->data[buffer->tail - 1] = NULL;
        buffer->size--;
    }
    if (buffer->tail >= SIZE_BUFFER) buffer->tail = 0;

    return elem;
}

// ################################################################################

bool        compare(void *data[], void *str[]) {
    for (int i = 0; i < SIZE_BUFFER; i++) {
        if (data[i] == 0 && str[i] != 0)                    return false;
        if (data[i] != 0 && strcmp(data[i], str[i]) != 0)   return false;
    }

    return true;
}

void        display(Queue *buffer) {
    for (int i = 0; i < SIZE_BUFFER; i++) {
        if (buffer->data[i] == NULL)    printf("%sX %s", RED, EMPTY);
        else                            printf("%s ", (char *) buffer->data[i]);
    }

    printf(" %d %d", buffer->tail, buffer->head);
}

// ################################################################################

int         main(void) {
    Queue   buffer;

    init(&buffer);

    push(&buffer, "A");
    push(&buffer, "B");
    push(&buffer, "C");
    push(&buffer, "D");
    push(&buffer, "E");
    display(&buffer);
    printf("\t <--- %s ADD A B C D E %s\n", BLUE, EMPTY);

    pop(&buffer);
    display(&buffer);
    printf("\t <--- %s DEL 1 ELEMENT %s\n", BLUE, EMPTY);

    push(&buffer, "F");
    push(&buffer, "G");
    display(&buffer);
    printf("\t <--- %s ADD F G %s\n", BLUE, EMPTY);

    pop(&buffer);
    pop(&buffer);
    display(&buffer);
    printf("\t <--- %s DEL 2 ELEMENTS %s\n", BLUE, EMPTY);

    push(&buffer, "H");
    push(&buffer, "I");
    push(&buffer, "J");
    display(&buffer);
    printf("\t <--- %s ADD H I J %s\n", BLUE, EMPTY);

    pop(&buffer);
    pop(&buffer);
    pop(&buffer);
    pop(&buffer);
    display(&buffer);
    printf("\t <--- %s DEL 4 ELEMENTS %s\n", BLUE, EMPTY);

    push(&buffer, "K");
    display(&buffer);
    printf("\t <--- %s ADD K %s\n", BLUE, EMPTY);

    push(&buffer, "L");
    push(&buffer, "M");
    display(&buffer);
    printf("\t <--- %s ADD L M %s\n", BLUE, EMPTY);

    pop(&buffer);
    pop(&buffer);
    display(&buffer);
    printf("\t <--- %s DEL 2 ELEMENTS %s\n", BLUE, EMPTY);

    push(&buffer, "N");
    push(&buffer, "O");
    push(&buffer, "P");
    display(&buffer);
    printf("\t <--- %s ADD N O P %s\n", BLUE, EMPTY);
}

// ################################################################################
