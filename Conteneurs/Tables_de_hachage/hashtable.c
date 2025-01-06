/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

#include "hashtable.h"
#include <stdlib.h>
#include <string.h>


unsigned int        elf_hash(const char* str, unsigned int length) {
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

void                init(HashTable *ht, unsigned int size) {
    ht->size    = size;
    ht->items   = calloc(size, sizeof(Player *));
}

void                insert(HashTable *ht, Player *player, hash_f hash) {
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

int                 search(HashTable *ht, char *key, hash_f hash) {
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
