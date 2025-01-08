/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

#include <ctype.h>
#include <math.h>
#include <regex.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


static void         hello() {
    printf("hello\n");
}

static void         print_numbers(int n) {
    for (int i = 0; i <= n; i++) {
        printf("%d ", i);
    }
}

static void         print_alphabet() {
    for (char c = 'a'; c <= 'z'; c++) {
        printf("%c ", c);
    }
}

static int          count_vowels(const char *str) {
    int count = 0;

    while (*str) {
        char c = tolower(*str);
        if (c == 'a' || c == 'e' || c == 'i' ||
            c == 'o' || c == 'u' || c == 'y') {
            count++;
        }
        str++;
    }

    return count;
}

static int          count_consonants(const char *str) {
    regex_t regex;
    int     reti;
    int     count = 0;

    reti = regcomp(&regex, "[bcdfghjklmnpqrstvwxyz]", REG_EXTENDED);

    while (*str) {
        reti = regexec(&regex, str, 0, NULL, 0);
        if (!reti) {
            count++;
        }
        str++;
    }

    regfree(&regex);

    return count;
}

static bool         is_palindrome(char *word) {
    int i   = 0;
    int j   = strlen(word) - 1;

    while (i < j) {
        if (word[i] != word[j])
            return false;
        i += 1;
        j -= 1;
    }
    
    return true;
}

static int          nb_abs(int nb) {
    return nb < 0 ? -nb : nb;
}

static bool         is_prime(int nb) {
    if (nb < 2)     return false;
    if (nb == 2)    return true;

    for (int i = 3; i <= sqrt(nb); i += 2) {
        if (nb % i == 0) return false;
    }

    return true;
}

static bool         is_perfect(int nb) {
    if (nb <= 1) return false;

    int sum = 1;

    for (int i = 2; i <= sqrt(nb); i++) {
        if (nb % i == 0) {
            sum += i;
            if (i != nb / i) sum += nb / i;
        }
    }

    return sum == nb;
}

static char*        binary_conv(int n) {
    char *binary = (char *) malloc(33);

    binary[32] = '\0';

    for (int i = 31; i >= 0; i--) {
        binary[i] = (n & 1) ? '1' : '0';
        n >>= 1;
    }

    return binary;
}

static char*        base_conv(int n, int base) {
    char    *result     = (char *) malloc(33);
    char    digits[]    = "0123456789ABCDEF";
    int     index       = 31;

    result[32] = '\0';

    do {
        result[index--] = digits[n % base];
        n /= base;
    } while (n > 0);

    return &result[index + 1];
}

static char*        cesar_cipher(char *plainText, int key) {
    int length = strlen(plainText);

    for (int i = 0; i < length; i++) {
        char c = plainText[i];

        if (isalpha(c)) {
            char base = islower(c) ? 'a' : 'A';
            plainText[i] = (c - base + key) % 26 + base;
        }
    }

    return plainText;
}

static void         bubble_sort(int *array, int size) {
    for (int i = 0; i < size - 1; i++) {
        for (int j = 0; j < size - 1 - i; j++) {
            if (array[j] > array[j + 1]) {
                int temp = array[j];
                array[j] = array[j + 1];
                array[j + 1] = temp;
            }
        }
    }
}

static void         nb_occurrences(int *array, int size, int limit) {
    int *count = (int *) calloc(limit, sizeof(int));

    for (int i = 0; i < size; i++) {
        if (array[i] < limit) count[array[i]]++;
    }

    for (int i = 0; i < limit; i++) {
        if (count[i] > 0)
            printf("[ %d ] -> %d\n", i, count[i]);
    }

    free(count);
}

static int          postfix(const char *expression) {
    Stack   stack;
    int     result;

    init(&stack);

    for (int i = 0; i < strlen(expression); i++) {
        char c = expression[i];

        if (isdigit(c)) push(&stack, c - '0');
        else if (c == ' ') continue;
        else {
            int val2 = pop(&stack);
            int val1 = pop(&stack);

            switch (c) {
                case '+': push(&stack, val1 + val2); break;
                case '-': push(&stack, val1 - val2); break;
                case '*': push(&stack, val1 * val2); break;
                case '/': push(&stack, val1 / val2); break;
                default: 
                    fprintf(stderr, "Invalid operator: %c\n", c);
                    exit(1);
            }
        }
    }

    return pop(&stack);
}


int                 main(void) {
    hello();
    print_numbers(10);
    putchar('\n');
    print_alphabet();
    putchar('\n');
    printf("Nombre de voyelles dans charles                         : %d\n", count_vowels("charles"));
    printf("Nombre de consonnes dans charles                        : %d\n", count_consonants("charles"));
    printf("Palindromes : Maeva - Radar                             : %d %d\n", is_palindrome("maeva"), is_palindrome("radar"));
    printf("Valeur absolue de -7                                    : %d\n", nb_abs(-7));
    printf("Le nombre 101 est premier                               : %s\n", is_prime(101) ? "Yes" : "No");
    printf("Le nombre 496 est parfait                               : %s\n", is_perfect(496) ? "Yes" : "No");
    printf("Représentation binaire de 27                            : %s\n", binary_conv(27));
    printf("Représentation binaire de 2500                          : %s\n", base_conv(2500, 2));
    printf("Représentation octale de 2500                           : %s\n", base_conv(2500, 8));
    printf("Représentation hexadécimale de 2500                     : %s\n", base_conv(2500, 16));
    printf("Cipher                                                  : %s\n", cesar_cipher(strdup("abcedfghijklmnopqrstuvwxyz"), 4));

    int array_1[] = { 3, 6, 8, 10, 1, 2, 1 };
    bubble_sort(array_1, 7);
    printf("Tableau trié                                            : ");
    for (int i = 0; i < 7; i++) printf("%d ", array_1[i]);
    putchar('\n');

    int array_2[] = { 1, 2, 2, 3, 3, 3, 4, 7, 7, 7, 7, 7 };
    printf("Occurrences [1, 2, 2, 3, 3, 3, 4, 7, 7, 7, 7, 7]        :\n");    
    nb_occurrences(array_2, 12, 10);

    printf("Résultat de l'expression postfixée [3 2 * 6 + 3 - 3 /]  : %d\n", postfix("3 2 * 6 + 3 - 3 /"));

    return 0;
}
