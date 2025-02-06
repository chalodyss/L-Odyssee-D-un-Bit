/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

// ################################################################################

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BLUE        "\033[1;34m"
#define RED         "\033[91m"
#define EMPTY       "\033[0m"

#define NAME_SIZE   30

typedef struct      PL {
    int             elo;
    char            name[NAME_SIZE];
    struct PL       *next;
}                   Player;

typedef struct {
    unsigned int    size;
    Player          **items;
}                   HashTable;

typedef unsigned int (*hash_f) (const char *, unsigned int);

// ################################################################################

unsigned int    elf_hash(const char* str, unsigned int length) {
    unsigned int    hash   = 0;
    unsigned int    x      = 0;

    for (unsigned int i = 0; i < length; ++str, ++i) {
        hash = (hash << 4) + (*str);
        if ((x = hash & 0xF0000000L) != 0) {
            hash ^= (x >> 24);
        }
        hash &= ~x;
    }

    return hash;
}

// ################################################################################

void            init(HashTable *ht, unsigned int size) {
    ht->size    = size;
    ht->items   = calloc(size, sizeof(Player *));
}

void            insert(HashTable *ht, Player *player, hash_f hash) {
    Player          *tmp    = NULL;
    unsigned int    code    = hash(player->name, strlen(player->name)) % ht->size;

    tmp = ht->items[code];

    if (tmp == NULL) {
        ht->items[code] = player;
    } else {
        player->next    = tmp;
        ht->items[code] = player;
    }
}

int             search(HashTable *ht, char *key, hash_f hash) {
    int             elo     = -1;
    unsigned int    code    = hash(key, strlen(key)) % ht->size;
    Player          *player = ht->items[code];

    while (player != NULL) {
        if (strncmp(player->name, key, strlen(key)) == 0) {
            elo = player->elo;
            break;
        }
        player = player->next;
    }

    return elo;
}

// ################################################################################

void            display(HashTable *ht, int size) {
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

// ################################################################################

int             main(void) {
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

    printf("ELO Carlsen         : %d\n", search(&ht, "Carlsen", elf_hash));
    printf("ELO Ding            : %d\n", search(&ht, "Ding", elf_hash));
    printf("ELO Anand           : %d\n", search(&ht, "Anand", elf_hash));
    printf("ELO Abdusattorov    : %d\n", search(&ht, "Abdusattorov", elf_hash));
    printf("ELO Nakamura        : %d\n", search(&ht, "Nakamura", elf_hash));
    printf("ELO Caruana         : %d\n", search(&ht, "Caruana", elf_hash));
    printf("ELO Nepomniachtchi  : %d\n", search(&ht, "Nepomniachtchi", elf_hash));
}

// ################################################################################
