/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

module pong {
    requires transitive javafx.graphics;
    requires javafx.controls;
    requires javafx.fxml;

    exports abitodyssey.pong;

    opens abitodyssey.pong to javafx.fxml;
}
