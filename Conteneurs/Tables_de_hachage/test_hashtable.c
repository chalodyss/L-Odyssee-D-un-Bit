/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

#include "hashtable.h"
#include <criterion/criterion.h>
#include <stdio.h>

#define BLUE    "\033[1;34m"
#define RED     "\033[91m"
#define EMPTY   "\033[0m"


static void     display(HashTable *ht, int size) {
    Player      *player = NULL;

    for (int i = 0; i < size; i++) {
        player = ht->items[i];

        printf("%s[[%-3d]]%s", RED, i, EMPTY);

        while (player != NULL) {
            printf("%s -> ", BLUE);
            printf("(%s, %d)%s", player->name, player->elo, EMPTY);
            player = player->next;
        }

        putchar('\n');
    }
}

Test(hashtable, insert_and_search) {
    HashTable   ht  = { 0 };
    Player      p1  = { 2830, "Carlsen", NULL };
    Player      p2  = { 2762, "Ding", NULL };
    Player      p3  = { 2751, "Anand", NULL };
    Player      p4  = { 2765, "Abdusattorov", NULL };
    Player      p5  = { 2794, "Nakamura", NULL };
    Player      p6  = { 2805, "Caruana", NULL };
    Player      p7  = { 2770, "Nepomniachtchi", NULL };


    init(&ht, 5);
    printf("--------------------\n");
    display(&ht, 5);
    printf("--------------------\n");

    insert(&ht, &p1, elf_hash);
    insert(&ht, &p2, elf_hash);
    insert(&ht, &p3, elf_hash);
    insert(&ht, &p4, elf_hash);
    insert(&ht, &p5, elf_hash);
    insert(&ht, &p6, elf_hash);
    insert(&ht, &p7, elf_hash);
    display(&ht, 5);
    printf("--------------------\n");

    cr_assert(search(&ht, "Carlsen", elf_hash) == 2830);
    cr_assert(search(&ht, "Ding", elf_hash) == 2762);
    cr_assert(search(&ht, "Anand", elf_hash) == 2751);
    cr_assert(search(&ht, "Abdusattorov", elf_hash) == 2765);
    cr_assert(search(&ht, "Nakamura", elf_hash) == 2794);
    cr_assert(search(&ht, "Caruana", elf_hash) == 2805);
    cr_assert(search(&ht, "Nepomniachtchi", elf_hash) == 2770);
}
