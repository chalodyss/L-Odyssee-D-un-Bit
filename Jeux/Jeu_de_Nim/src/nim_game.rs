/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

use rand::Rng;
use std::io::*;


pub const RESET:    &str = "\u{001B}[0m";
pub const RED:      &str = "\u{001B}[31m";
pub const GREEN:    &str = "\u{001B}[32m";
pub const CYAN:     &str = "\u{001B}[36m";
pub const SMILE:    &str = "\u{1F642}";
pub const LAPTOP:   &str = "\u{1F4BB}";


struct AppNim {
    matches: i32,
    packets: Vec<i32>,
}

impl AppNim {

    fn new() -> Self {
        Self {
            matches: 0,
            packets: Vec::new(),
        }
    }

    fn display_packets(&mut self) {
        for (i, &packet_count) in self.packets.iter().enumerate() {
            print!("{} - [", i);
            for _ in 0..packet_count {
                print!("{}", GREEN);
                print!("|");
            }
            for _ in packet_count..5 {
                print!(" ");
            }
            print!("{}", RESET);
            print!("]");
            for _ in 0..=5 {
                print!(" ");
            }
        }
    }

    fn init(&mut self) {
        let mut input   = String::new();
        let mut rng     = rand::thread_rng();

        loop {
            print!("Enter the number of packets [1 - 7] : ");
            stdout().flush().unwrap();
            stdin().read_line(&mut input).unwrap();

            let nb_packets = match input.trim().parse() {
                Ok(n) => n,
                Err(_) => {
                    println!("Invalid input. Please try again.");
                    continue;
                }
            };

            if nb_packets >= 1 && nb_packets <= 7 {
                self.packets = (0..nb_packets).map(|_| rng.gen_range(1..=5)).collect();
                self.matches = self.packets.iter().sum();
                break;
            } else {
                println!("Number of packets must be between 1 and 7. Please try again.");
            }
        }
    }

    fn move_hal(&mut self) -> i32 {
        for i in 0..self.packets.len() {
            for j in 1..=self.packets[i] {
                self.packets[i] -= j;
                if self.packets.iter().filter(|&x| *x >= 0).fold(0, |x, y| x ^ y) == 0 {
                    return j;
                }
                self.packets[i] += j;
            }
        }

        return 0;
    }

    fn move_you(&mut self) -> i32 {
        let mut remove  = -1;
        let mut input   = false;

        while !input {
            print!("{}{}{}: ", CYAN, "Choose your packet                     ", RESET);
            stdout().flush().unwrap();
            let mut buffer      = String::new();
            stdin().read_line(&mut buffer).unwrap();
            let indice: usize   = buffer.trim().parse().unwrap();

            if indice < self.packets.len() && self.packets[indice as usize] != 0 {
                while !input {
                    print!("{}{}{}: ", CYAN, "Choose the number of matches to remove ", RESET);
                    stdout().flush().unwrap();
                    buffer.clear();
                    stdin().read_line(&mut buffer).unwrap();
                    remove = buffer.trim().parse().unwrap();

                    if remove > 0 && remove <= self.packets[indice as usize] {
                        self.packets[indice as usize]   -= remove;
                        input                           = true;
                    }
                }
            }
        }

        return remove;
    }

    fn start(&mut self) {
        let mut move_val = match self.packets.iter().fold(0, |x, y| x ^ y) {
            0 => 1,
            _ => 0,
        };

        self.display_packets();
        println!();

        while self.matches >= 1 {
            if move_val == 1 {
                self.matches -= self.move_you();
            } else {
                self.matches -= self.move_hal();
            }

            self.display_packets();
            print!("{}{}{}{}",
                    if move_val == 1 { SMILE } else { LAPTOP },
                    if move_val == 1 { CYAN } else { RED },
                    if move_val == 1 { " YOU PLAYED\n" } else { " HAL PLAYED\n" }, RESET);

            move_val ^= 1;
        }

        println!("{}{}{}", RED, if move_val == 1 { "Hal wins." } else { "Hal loses." }, RESET);
    }

}


fn main() {
    loop {
        let mut app_nim = AppNim::new();

        app_nim.init();
        app_nim.start();

        println!("Another game? y / n : ");

        let mut input   = String::new();

        stdin().read_line(&mut input).expect("Failed to read line");
        let c           = input.chars().next();

        if c != Some('y') { break };
    }
}
