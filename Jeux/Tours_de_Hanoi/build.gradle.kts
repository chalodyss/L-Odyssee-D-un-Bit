/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

group   = "abitodyssey.hanoitowers"
version = "1.0.0"

plugins {
    application
    id("org.openjfx.javafxplugin") version "0.1.0"
}

repositories {
    mavenCentral()
}

application {
    mainClass   = "abitodyssey.hanoitowers.Main"
    mainModule  = "hanoitowers"
}

javafx {
    modules("javafx.graphics", "javafx.controls", "javafx.fxml")
}

tasks.withType<Jar> {
    archiveBaseName = "HanoiTowers"

    manifest {
        attributes["Main-Class"] = "abitodyssey.hanoitowers.Main"
    }
}
