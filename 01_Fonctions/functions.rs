/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

use regex::Regex;


fn hello() {
    println!("Hello");
}

fn print_numbers(n: u32) {
    for i in 0..=n {
        print!("{} ", i);
    }
}

fn print_alphabet() {
    for c in 'a'..='z' {
        print!("{} ", c);
    }
}

fn count_vowels(str: &str) -> u32 {
    let mut count = 0;

    for c in str.chars() {
        if  c == 'a' || c == 'e' || c == 'i' ||
            c == 'o' || c == 'u' || c == 'y' {
            count += 1;
        }
    }

    return count;
}

fn count_consonants(str: &str) -> u32 {
    let re      = Regex::new(r"[^aeiou]").unwrap();
    let mut nb  = 0;

    for c in str.chars() {
        if re.is_match(&c.to_string()) {
            nb += 1;
        }
    }

    return nb;
}

fn is_palindrome(word: &str) -> bool {
    let mut i       = 0;
    let mut j       = word.len() - 1;
    let lower_word  = word.to_lowercase();

    while i < j {
        if lower_word.chars().nth(i) != lower_word.chars().nth(j) {
            return false;
        }
        i += 1;
        j -= 1;
    }

    return true;
}

fn nb_abs(nb : i64) -> i64 {
    return if nb < 0 {-nb} else {nb};
}

fn is_prime(nb : u64) -> bool {
    if nb < 2     { return false };
    if nb == 2    { return true };

    let sqrt_nb = (nb as f64).sqrt() as u64;
    for i in (3..=sqrt_nb + 1).step_by(2) {
        if nb % i == 0 { return false };
    }

    return true;
}

fn is_perfect(nb : u64) -> bool {
    if nb <= 1 { return false };

    let mut sum = 1;

    let sqrt_nb = (nb as f64).sqrt() as u64;
    for i in 2..=sqrt_nb + 1 {
        if nb % i == 0 {
            sum += i;
            if i != nb / i { sum += nb / i };
        }
    }

    return sum == nb;
}

fn binary_conv(nb : u64) -> String {
    if nb == 0 { return "0".to_string() };
    
    let mut binary = String::new();
    let mut op     = nb;

    while op > 0 {
        binary.push_str(&(op % 2).to_string());
        op /= 2;
    }

    return binary.chars().rev().collect::<String>();
}

fn base_conv(nb : u64, base : u64) -> String {
    if nb == 0 { return "0".to_string() };

    let digits      = "0123456789ABCDEF";
    let mut result  = String::new();
    let mut op      = nb;

    while op > 0 {
        result.push(digits.chars().nth((op % base) as usize).unwrap());
        op =  op / base;
    }

    return result.chars().rev().collect::<String>();
}

fn cesar_cipher(plain_text : &str, key : u8) -> String {
    let mut cipher = String::new();

    for c in plain_text.chars() {
        let ascii   = ((c as u8) - ('a' as u8) + key) % 26 + ('a' as u8);
        cipher.push(ascii as char);
    }

    return cipher;
}

fn bubble_sort(array: &mut[i32]) -> &[i32] {
    for i in 0..array.len() {
        for j in 0..array.len() - 1 - i {
            if array[j] > array[j + 1] {
                let temp        = array[j];
                array[j]        = array[j + 1];
                array[j + 1]    = temp;
            }
        }
    }

    return array;
}

fn nb_occurrences(array: &[i32], limit : usize) {
    let mut count = vec![0; limit];

    for &num in array {
        count[num as usize] += 1;
    }

    for i in 0..count.len() {
        if count[i] > 0 {
            println!("[ {} ] -> {}", i, count[i]);
        }
    }
}

fn postfix(expr : &str) -> i32 {
    let mut stack           = Vec::new();
    let tokens: Vec<&str>   = expr.split(" ").collect();
    let operators           = Regex::new(r"[\+\-\*\/]").unwrap();

    for token in tokens {
        if operators.is_match(token) {
            let b : i32 = stack.pop().unwrap();
            let a : i32 = stack.pop().unwrap();

            match token {
                "+" => stack.push(a + b),
                "-" => stack.push(a - b),
                "*" => stack.push(a * b),
                "/" => stack.push(a / b),
                _   => println!("")
            }
        } else {
            stack.push(token.parse::<i32>().unwrap());
        }
    }

    return stack.pop().unwrap();
}

fn main() {
    hello();
    print_numbers(10);
    println!();
    print_alphabet();
    println!();
    println!("Nombre de voyelles dans charles                           : {}", count_vowels("charles"));
    println!("Nombre de consonnes dans charles                          : {}", count_consonants("charles"));
    println!("Palindromes : Maeva - Radar                               : {} {}", is_palindrome("Maeva"), is_palindrome("Radar"));
    println!("Valeur absolue de -7                                      : {}", nb_abs(-7));
    println!("Le nombre 101 est premier                                 : {}", is_prime(101));
    println!("Le nombre 496 est parfait                                 : {}", is_perfect(496));
    println!("Représentation binaire de 27                              : {}", binary_conv(27));
    println!("Représentation binaire de 2500                            : {}", base_conv(2500, 2));
    println!("Représentation octale de 2500                             : {}", base_conv(2500, 8));
    println!("Représentation hexadécimale de 2500                       : {}", base_conv(2500, 16));
    println!("Cipher                                                    : {}", cesar_cipher("abcdefghijklmnopqrstuvwxyz", 4));
    let mut bubble  = [ 3, 6, 8, 10, 1, 2, 1 ];
    println!("Tableau trié                                              : {}", format!("{:?}", bubble_sort(&mut bubble)));
    let array   = [ 1, 2, 2, 3, 3, 3, 4, 7, 7, 7, 7, 7 ];
    println!("Occurrences [1, 2, 2, 3, 3, 3, 4, 7, 7, 7, 7, 7]          :");
    nb_occurrences(&array, 10);
    println!("Résultat de l'expression postfixée [3 2 * 6 + 3 - 3 /]    : {}", postfix("3 2 * 6 + 3 - 3 /"));
}
