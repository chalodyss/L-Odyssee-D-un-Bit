/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

#include "queue.h"
#include <string.h>


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
