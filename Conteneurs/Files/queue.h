/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

#ifndef _QUEUE_H_
#define _QUEUE_H_

#define SIZE_BUFFER 4

typedef struct {
    int     head;
    int     tail;
    int     size;
    void    *data[SIZE_BUFFER];
}           Queue;

void        init(Queue *);
void        push(Queue *, void *);
void        *pop(Queue *);

#endif
