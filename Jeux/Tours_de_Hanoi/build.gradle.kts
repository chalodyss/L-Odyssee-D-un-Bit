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

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
}

javafx {
    version = "21"
    modules("javafx.graphics", "javafx.controls", "javafx.fxml")
}

tasks.named<Delete>("clean") {
    delete("target")
}

tasks.named<Jar>("jar") {
    archiveBaseName = "HanoiTowers"
    destinationDirectory.set(file("target"))

    manifest {
        attributes["Main-Class"] = "abitodyssey.hanoitowers.Main"
    }
}
