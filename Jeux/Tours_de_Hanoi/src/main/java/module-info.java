/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

module hanoitowers {
    requires transitive javafx.graphics;
    requires javafx.controls;
    requires javafx.fxml;

    exports abitodyssey.hanoitowers;

    opens abitodyssey.hanoitowers to javafx.fxml;
}
