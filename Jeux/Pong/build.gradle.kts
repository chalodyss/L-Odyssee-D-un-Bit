/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

group   = "abitodyssey.pong"
version = "1.0.0"

plugins {
    application
    id("org.openjfx.javafxplugin") version "0.1.0"
}

repositories {
    mavenCentral()
}

application {
    mainClass   = "abitodyssey.pong.Main"
    mainModule  = "pong"
}

javafx {
    modules("javafx.graphics", "javafx.controls", "javafx.fxml", "javafx.media")
}

tasks.withType<Jar> {
    archiveBaseName = "Pong"

    manifest {
        attributes["Main-Class"] = "abitodyssey.pong.Main"
    }
}
