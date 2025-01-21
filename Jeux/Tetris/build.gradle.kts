/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

group   = "abitodyssey.tetris"
version = "1.0.0"

plugins {
    application
    id("org.openjfx.javafxplugin") version "0.1.0"
}

repositories {
    mavenCentral()
}

application {
    mainClass   = "abitodyssey.tetris.Main"
    mainModule  = "tetris"
}

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
}

javafx {
    version = "21"
    modules("javafx.controls", "javafx.graphics", "javafx.fxml")
}

tasks.named<Delete>("clean") {
    delete("target")
}

tasks.named<Jar>("jar") {
    archiveBaseName = "Tetris"
    destinationDirectory.set(file("target"))

    manifest {
        attributes["Main-Class"] = "abitodyssey.tetris.Main"
    }
}
