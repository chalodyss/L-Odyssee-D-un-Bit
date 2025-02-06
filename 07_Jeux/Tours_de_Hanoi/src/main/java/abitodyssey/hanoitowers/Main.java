/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

package abitodyssey.hanoitowers;


import javafx.animation.AnimationTimer;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.beans.property.IntegerProperty;
import javafx.beans.property.SimpleIntegerProperty;
import javafx.collections.FXCollections;
import javafx.concurrent.Task;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.control.ComboBox;
import javafx.scene.layout.Pane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import javafx.scene.text.Text;
import javafx.stage.Stage;

import java.math.BigInteger;
import java.time.Duration;
import java.time.Instant;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;


class Disk extends Rectangle {

    double[] xPos;


    Disk(double x, double y, double width, double height) {
        super(width, height, Color.WHITE);

        setStrokeWidth(2);
        setxPos(width);
        move(x, y);
    }

    Disk(Disk disk) {
        setWidth(disk.getWidth());
        setHeight(disk.getHeight());
        setX(disk.getX());
        setY(disk.getY());
        setxPos(disk.getWidth());
        setFill(disk.getFill());
        setStrokeWidth(2);
        setStroke(Color.BLACK);
    }

    void move(double x, double y) {
        setX(x);
        setY(y);
    }

    void setxPos(double w) {
        xPos    = new double[3];
        xPos[0] = 300 - w / 2;
        xPos[1] = 600 - w / 2;
        xPos[2] = 900 - w / 2;
    }

}

class HanoiTask extends Task<Void> {

    volatile boolean cancelled = false;

    List<List<Disk>> rods;
    List<List<Disk>> snapShot;
    BigInteger       nbMoves;
    int              nbDisks;
    Instant          startTime;


    HanoiTask(int nb) {
        rods      = Arrays.asList(new CopyOnWriteArrayList<>(),
                                  new CopyOnWriteArrayList<>(),
                                  new CopyOnWriteArrayList<>());
        snapShot  = Arrays.asList(new CopyOnWriteArrayList<>(),
                                  new CopyOnWriteArrayList<>(),
                                  new CopyOnWriteArrayList<>());
        nbDisks   = nb;
        nbMoves   = new BigInteger("2").pow(nbDisks).subtract(BigInteger.ONE);
        startTime = Instant.now();
    }

    void hanoi(int nbDisks, int start, int end, int tmp) {
        if (cancelled) return;
        if (nbDisks > 0) {
            nbMoves = nbMoves.subtract(BigInteger.ONE);
            hanoi(nbDisks - 1, start, tmp, end);
            moveDisk(start, end);
            hanoi(nbDisks - 1, tmp, end, start);
        } else if (rods.get(2).size() == this.nbDisks) {
            takeSnapShot();
            cancelled = true;
        }
    }

    void moveDisk(int start, int end) {
        var disk = rods.get(start - 1).removeLast();

        disk.move(disk.xPos[end - 1], 750 - ((rods.get(end - 1).size() + 1) * disk.getHeight()));
        rods.get(end - 1).add(disk);

        if (Duration.between(startTime, Instant.now()).toMillis() >= 10L) {
            takeSnapShot();
            startTime = Instant.now();
        }
    }

    void takeSnapShot() {
        snapShot.forEach(List::clear);

        for (int i = 0; i < rods.size(); i++) {
            for (var disk : rods.get(i)) {
                snapShot.get(i).add(new Disk(disk));
            }
        }
    }

    @Override
    protected Void call() {
        hanoi(nbDisks, 1, 3, 2);
        return null;
    }

}

class Renderer {

    static void renderDisks(Pane board, List<List<Disk>> rods) {
        board.getChildren().removeIf(e -> e.getClass() == Disk.class);

        for (var rod : rods) {
            for (var disk : rod) {
                board.getChildren().add(new Disk(disk));
            }
        }
    }

}

class Controller {

    @FXML
    Pane                board;
    @FXML
    Text                nbMoves;
    @FXML
    ComboBox<Integer>   disks;

    HanoiTask           task;
    IntegerProperty     nbDisks;

    AnimationTimer      timer;


    Controller() {
        timer = new AnimationTimer() {
            @Override
            public void handle(long now) {
                nbMoves.setText(task.nbMoves.toString());
                Renderer.renderDisks(board, task.snapShot);
            }
        };
    }

    @FXML
    void initialize() {
        var obListDisks = FXCollections.observableList(Arrays.asList(1, 2, 4, 8, 16, 32, 64, 128));

        disks.setItems(obListDisks);
        disks.getSelectionModel().select(0);

        nbDisks = new SimpleIntegerProperty();
        nbDisks.bind(disks.valueProperty());

        reset();
    }

    @FXML
    void reset() {
        timer.stop();

        if (task != null) {
            task.cancelled = true;
            task.cancel();
        }

        var diskW = 200.0;
        var diskH = nbDisks.get() > 8 ? 512.0 / nbDisks.get() : 256.0 / (nbDisks.get() * (8.0 / nbDisks.get()));
        var x     = 200.0;
        var y     = 750.0 - diskH;

        task = new HanoiTask(nbDisks.get());

        for (var i = 0; i < nbDisks.get(); i++) {
            task.rods.getFirst().add(new Disk(x, y, diskW, diskH));
            x += ((diskW / nbDisks.doubleValue()) / 2);
            y -= diskH;
            diskW -= diskW / nbDisks.doubleValue();
        }

        task.takeSnapShot();
        nbMoves.setText(task.nbMoves.toString());
        Renderer.renderDisks(board, task.snapShot);
    }

    @FXML
    void solve() {
        timer.start();

        var t = new Thread(task);

        t.setDaemon(true);
        t.start();
    }

}

public class Main extends Application {

    public void start(Stage stage) {
        try {
            FXMLLoader loader       = new FXMLLoader(getClass().getResource("/views/View.fxml"));
            Controller controller   = new Controller();

            loader.setController(controller);

            VBox  root              = loader.load();
            Scene scene             = new Scene(root);

            stage.setResizable(false);
            stage.setTitle("Hanoi Towers");
            stage.setScene(scene);
            stage.show();
        } catch (Exception e) {
            Platform.exit();
            System.exit(-1);
        }
    }

    public static void main(String[] args) {
        launch(args);
    }

}
