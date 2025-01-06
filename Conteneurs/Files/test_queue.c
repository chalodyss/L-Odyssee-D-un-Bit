/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

#include "queue.h"
#include <criterion/criterion.h>
#include <stdio.h>

#define BLUE    "\033[1;34m"
#define RED     "\033[91m"
#define EMPTY   "\033[0m"


static bool     compare(void *data[], void *str[]) {
    for (int i = 0; i < SIZE_BUFFER; i++) {
        if (data[i] == 0 && str[i] != 0)                    return false;
        if (data[i] != 0 && strcmp(data[i], str[i]) != 0)   return false;
    }

    return true;
}

static void     display(Queue *buffer) {
    for (int i = 0; i < SIZE_BUFFER; i++) {
        if (buffer->data[i] == NULL)    printf("%sX %s", RED, EMPTY);
        else                            printf("%s ", (char *) buffer->data[i]);
    }

    printf(" %d %d", buffer->tail, buffer->head);
}

Test(queue, push_and_pop) {
    Queue   buffer;

    init(&buffer);
    void *cb_1[SIZE_BUFFER] = { 0, 0, 0, 0 };
    cr_assert(compare(buffer.data, cb_1) == true);

    push(&buffer, "A");
    push(&buffer, "B");
    push(&buffer, "C");
    push(&buffer, "D");
    push(&buffer, "E");
    display(&buffer);
    printf("\t <--- %s ADD A B C D E %s\n", BLUE, EMPTY);
    void *cb_2[SIZE_BUFFER] = { "A", "B", "C", "D" };
    cr_assert(compare(buffer.data, cb_2) == true);

    pop(&buffer);
    display(&buffer);
    printf("\t <--- %s DEL 1 ELEMENT %s\n", BLUE, EMPTY);
    void *cb_3[SIZE_BUFFER] = { 0, "B", "C", "D" };
    cr_assert(compare(buffer.data, cb_3) == true);

    push(&buffer, "F");
    push(&buffer, "G");
    display(&buffer);
    printf("\t <--- %s ADD F G %s\n", BLUE, EMPTY);
    void *cb_4[SIZE_BUFFER] = { "F", "B", "C", "D" };
    cr_assert(compare(buffer.data, cb_4) == true);

    pop(&buffer);
    pop(&buffer);
    display(&buffer);
    printf("\t <--- %s DEL 2 ELEMENTS %s\n", BLUE, EMPTY);
    void *cb_5[SIZE_BUFFER] = { "F", 0, 0, "D" };
    cr_assert(compare(buffer.data, cb_5) == true);

    push(&buffer, "H");
    push(&buffer, "I");
    push(&buffer, "J");
    display(&buffer);
    printf("\t <--- %s ADD H I J %s\n", BLUE, EMPTY);
    void *cb_6[SIZE_BUFFER] = { "F", "H", "I", "D" };
    cr_assert(compare(buffer.data, cb_6) == true);

    pop(&buffer);
    pop(&buffer);
    pop(&buffer);
    pop(&buffer);
    display(&buffer);
    printf("\t <--- %s DEL 4 ELEMENTS %s\n", BLUE, EMPTY);
    void *cb_7[SIZE_BUFFER] = { 0, 0, 0, 0 };
    cr_assert(compare(buffer.data, cb_7) == true);

    push(&buffer, "K");
    display(&buffer);
    printf("\t <--- %s ADD K %s\n", BLUE, EMPTY);
    void *cb_8[SIZE_BUFFER] = { 0, 0, 0, "K" };
    cr_assert(compare(buffer.data, cb_8) == true);

    push(&buffer, "L");
    push(&buffer, "M");
    display(&buffer);
    printf("\t <--- %s ADD L M %s\n", BLUE, EMPTY);
    void *cb_9[SIZE_BUFFER] = { "L", "M", 0, "K" };
    cr_assert(compare(buffer.data, cb_9) == true);

    pop(&buffer);
    pop(&buffer);
    display(&buffer);
    printf("\t <--- %s DEL 2 ELEMENTS %s\n", BLUE, EMPTY);
    void *cb_10[SIZE_BUFFER] = { 0, "M", 0, 0 };
    cr_assert(compare(buffer.data, cb_10) == true);

    push(&buffer, "N");
    push(&buffer, "O");
    push(&buffer, "P");
    display(&buffer);
    printf("\t <--- %s ADD N O P %s\n", BLUE, EMPTY);
    void *cb_11[SIZE_BUFFER] = { "P", "M", "N", "O" };
    cr_assert(compare(buffer.data, cb_11) == true);
}
