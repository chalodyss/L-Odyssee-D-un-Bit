/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

version = "1.0.0"
group   = "abitodyssey.pendu"

plugins {
    application
}

repositories {
    mavenCentral()
}

application {
    mainClass   = "abitodyssey.pendu.Main"
    mainModule  = "pendu"
}

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
}

tasks.named<Delete>("clean") {
    delete("target")
}

tasks.named<Jar>("jar") {
    archiveBaseName = "Pendu"
    destinationDirectory.set(file("target"))

    manifest {
        attributes["Main-Class"] = "abitodyssey.pendu.Main"
    }
}

tasks.named<JavaExec>("run") {
    standardInput = System.`in`
}
