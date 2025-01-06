/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

package abitodyssey.pendu;


import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Random;
import java.util.Scanner;
import java.util.stream.IntStream;

import static abitodyssey.pendu.Constants.MAN;


class Main {

    static Scanner sc   = new Scanner(System.in);
    static String  word = "";


    static String buildWord(String str, char c) {
        var sb = new StringBuilder(str);

        if (!str.contains(Character.toString(c))) {
            IntStream.range(0, word.length())
                     .filter(i -> word.charAt(i) == c)
                     .forEach(i -> sb.setCharAt(i, c));
        }

        return sb.toString();
    }

    static void start() {
        var trials = 0;
        var str    = "_".repeat(word.length());

        str.chars().forEach(c -> System.out.print((char) c + " "));
        System.out.println("\n");

        while (trials < 7 && !str.equals(word)) {
            System.out.println("Choose a letter:");
            var c = sc.next().charAt(0);
            if (word.contains(Character.toString(c))) str = buildWord(str, c);
            else System.out.println(MAN[trials++] + "\n");
            str.chars().forEach(letter -> System.out.print((char) letter + " "));
            System.out.println("\n");
        }

        System.out.println(((trials < 7) ? "You win." : "You lose."));
    }

    public static void main(String[] args) throws IOException {
        var resp = 0;
        var rand = new Random();
        var dico = Files.readAllLines(Paths.get(args[0]));

        do {
            word = dico.get(rand.nextInt(dico.size()));
            start();
            System.out.println("Another game? y / n");
            resp = sc.next().charAt(0);
        } while (resp == 'y');
    }

}
