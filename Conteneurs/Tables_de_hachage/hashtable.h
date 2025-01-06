/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

#ifndef _HASHTABLE_H_
#define _HASHTABLE_H_

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

unsigned int    elf_hash(const char*, unsigned int);
void            init(HashTable *, unsigned int);
void            insert(HashTable *, Player *, hash_f);
int             search(HashTable *, char *, hash_f);

#endif
