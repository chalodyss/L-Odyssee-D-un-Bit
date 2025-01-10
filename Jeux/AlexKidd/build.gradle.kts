/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

group   = "abitodyssey.alexkidd"
version = "1.0.0"

plugins {
    application
    id("org.openjfx.javafxplugin") version "0.1.0"
}

repositories {
    mavenCentral()
}

application {
    mainClass   = "abitodyssey.alexkidd.Main"
    mainModule  = "alexkidd"
}

javafx {
    modules("javafx.graphics", "javafx.controls", "javafx.fxml")
}

sourceSets {
    main {
        resources.srcDir("src/main/resources/levels")
        resources.srcDir("src/main/resources/sprites")
        resources.srcDir("src/main/resources/views")
    }
}
