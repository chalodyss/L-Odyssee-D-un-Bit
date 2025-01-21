/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

module tetris {
    requires javafx.controls;
    requires javafx.fxml;

    exports abitodyssey.tetris;

    opens abitodyssey.tetris to javafx.fxml;
}
