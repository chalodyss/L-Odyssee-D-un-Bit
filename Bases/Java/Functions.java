/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.regex.Pattern;


public class Functions {

    static void hello() {
        System.out.println("hello");
    }

    static void printNumbers(int n) {
        for (var i = 0; i <= n; i++) {
            System.out.print(i + " ");
        }
    }

    static void printAlphabet() {
        for (var c = 'a'; c <= 'z'; c++) {
            System.out.print(c + " ");
        }
    }

    static int countVowels(String str) {
        var len = str.length();
        var nb  = 0;

        for (var i = 0; i < len; i++) {
            if ("aeiouyAEIOUY".contains(Character.toString(str.charAt(i)))) {
                nb += 1;
            }
        }

        return nb;
    }

    static int countConsonants(String str) {
        var len = str.length();
        var nb  = 0;

        for (var i = 0; i < len; i++) {
            var c = str.charAt(i);
    
            if (Pattern.matches("^[^AEIOUYaeiouy0-9\\s]*$", Character.toString(c))) {
                nb += 1;
            }
        }

        return nb;
    }

    static boolean isPalindrome(String word) {
        word    = word.toLowerCase();
        var i   = 0;
        var j   = word.length() - 1;

        while (i < j) {
            if (word.charAt(i) != word.charAt(j))
                return false;
            i += 1;
            j -= 1;
        }
    
        return true;
    }

    static int nbAbs(int nb) {
        return nb < 0 ? -nb : nb;
    }

    static boolean isPrime(int nb) {
        if (nb < 2)     return false;
        if (nb == 2)    return true;

        for (var i = 3; i <= Math.sqrt(nb); i += 2) {
            if (nb % i == 0) return false;
        }

        return true;
    }

    static boolean isPerfect(int nb) {
        if (nb <= 1) return false;

        var sum = 1;

        for (var i = 2; i <= Math.sqrt(nb); i++) {
            if (nb % i == 0) {
                sum += i;
                if (i != nb / i) sum += nb / i;
            }
        }

        return sum == nb;
    }

    public static String binaryConv(int nb) {
        if (nb == 0) return "0";
        
        var binary = new StringBuilder();

        while (nb > 0) {
            binary.insert(0, nb % 2);
            nb = nb / 2;
        }
        
        return binary.toString();
    }

    public static String baseConv(int nb, int base) {
        if (nb == 0) return "0";

        var digits = "0123456789ABCDEF";
        var result = new StringBuilder();

        while (nb > 0) {
            result.insert(0, digits.charAt(nb % base));
            nb = nb / base;
        }

        return result.toString();
    }

    public static String cesarCipher(String plainText, int key) {
        var cipher  = new StringBuilder();

        for (var i = 0; i < plainText.length(); i++) {
            var c = plainText.charAt(i);
            cipher.append((char) ((c - 'a' + key) % 26 + 'a'));
        }

        return cipher.toString();
    }

    public static <T extends Comparable<T>> T[] bubbleSort(T[] array) {
        for (var i = 0; i < array.length - 1; i++) {
            for (var j = 0; j < array.length - 1 - i; j++) {
                if (array[j].compareTo(array[j + 1]) > 0) {
                    T temp          = array[j];
                    array[j]        = array[j + 1];
                    array[j + 1]    = temp;
                }
            }
        }

        return array;
    }

    public static void nbOccurrences(int[] array, int limit) {
        var count = new int[limit];

        for (var num : array) count[num]++;

        for (var i = 0; i < count.length; i++) {
            if (count[i] > 0) {
                System.out.println("[ " + i + " ] -> " + count[i]);
            }
        }
    }

    public static int postfix(String expr) {
        var stack       = new ArrayDeque<Integer>();
        var tokens      = expr.split("\\s+");
        var operators   = Pattern.compile("[+\\-*/]");

        for (var token : tokens) {
            if (operators.matcher(token).matches()) {
                var b = stack.pop();
                var a = stack.pop();
    
                switch (token) {
                    case "+" -> stack.push(a + b);
                    case "-" -> stack.push(a - b);
                    case "*" -> stack.push(a * b);
                    case "/" -> stack.push(a / b);
                }
            } else {
                stack.push(Integer.parseInt(token));
            }
        }

        return stack.pop();
    }

    public static void main(String[] args) {
        hello();
        printNumbers(10);
        System.out.println();
        printAlphabet();
        System.out.println();
        System.out.println("Nombre de voyelles dans [charles]                           : " + countVowels("chArles"));
        System.out.println("Nombre de consonnes dans [charles]                          : " + countConsonants("chArles"));
        System.out.println("Palindromes : Maeva - Radar                                 : " + isPalindrome("Maeva") + " " + isPalindrome("Radar"));
        System.out.println("Valeur absolue de -7                                        : " + nbAbs(-7));
        System.out.println("Le nombre 101 est premier                                   : " + isPrime(101));
        System.out.println("Le nombre 496 est parfait                                   : " + isPerfect(496));
        System.out.println("Représentation binaire de 27                                : " + binaryConv(27));
        System.out.println("Représentation binaire de 2500                              : " + baseConv(2500, 2));
        System.out.println("Représentation octale de 2500                               : " + baseConv(2500, 8));
        System.out.println("Représentation hexadécimale de 2500                         : " + baseConv(2500, 16));
        System.out.println("Cipher                                                      : " + cesarCipher("abcdefghijklmnopqrstuvwxyz", 4));
        System.out.println("Tableau trié                                                : " + Arrays.toString(bubbleSort(new Integer[]{ 3, 6, 8, 10, 1, 2, 1 })));    
        System.out.println("Occurrences [1, 2, 2, 3, 3, 3, 4, 7, 7, 7, 7, 7]            : ");    
        nbOccurrences(new int[]{1, 2, 2, 3, 3, 3, 4, 7, 7, 7, 7, 7}, 10);
        System.out.println("Résultat de l'expression postfixée [3 2 * 6 + 3 - 3 /]      : " + postfix("3 2 * 6 + 3 - 3 /"));
    }
    
}
