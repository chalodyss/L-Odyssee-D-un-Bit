/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

group   = "abitodyssey.morpion"
version = "1.0.0"

plugins {
    application
    id("org.openjfx.javafxplugin") version "0.1.0"
}

repositories {
    mavenCentral()
}

application {
    mainClass   = "abitodyssey.morpion.Main"
    mainModule  = "morpion"
}

javafx {
    modules("javafx.graphics", "javafx.controls", "javafx.fxml")
}

sourceSets {
    main {
        resources.srcDir("src/main/resources/images/")
    }
}

tasks.withType<Jar> {
    archiveBaseName = "Morpion"

    manifest {
        attributes["Main-Class"] = "abitodyssey.morpion.Main"
    }
}
