/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

module spaceinvaders {
    requires javafx.controls;
    requires javafx.fxml;

    exports abitodyssey.spaceinvaders;

    opens abitodyssey.spaceinvaders to javafx.fxml;
}
