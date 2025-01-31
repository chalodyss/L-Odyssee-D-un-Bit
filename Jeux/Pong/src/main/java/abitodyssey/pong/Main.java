/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

package abitodyssey.pong;


import javafx.animation.AnimationTimer;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.beans.binding.Bindings;
import javafx.beans.property.IntegerProperty;
import javafx.beans.property.SimpleIntegerProperty;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Rectangle;
import javafx.stage.Stage;

import static java.lang.Math.*;


class Game {

    static IntegerProperty score  = new SimpleIntegerProperty(0);
    //
    static Rectangle       player = new Rectangle(30, 150, Color.WHITE);
    static Rectangle       cpu    = new Rectangle(30, 150, Color.WHITE);
    static Circle          ball   = new Circle(450, 350, 15, Color.WHITE);
    //
    static double          vel    = 0;
    static double          angle  = atan2(1.0, 5.0);
    static double          mag    = sqrt(26);
    static double          dX     = mag * cos(angle);
    static double          dY     = mag * sin(angle);

    static {
        player.setX(0);
        player.setY(150);
        cpu.setX(1170);
        cpu.setY(450);
    }


    private Game() {}

    static void update() {
        if (ball.getCenterX() > 15) {
            updatePlayer();
            updateBall();
            updateCpu();
        }
    }

    static void updatePlayer() {
        if ((vel > 0 && player.getY() <= 590) || (vel < 0 && player.getY() >= 10)) {
            player.setY(player.getY() + vel);
        }
    }

    static void updateCpu() {
        cpu.setY(ball.getCenterY() - 75);
    }

    static void updateBall() {
        var newX = ball.getCenterX() + dX;
        var newY = ball.getCenterY() + dY;

        ball.setCenterX(newX);
        ball.setCenterY(newY);

        if (newY > 735 || newY < 15) dY = -dY;

        if (player.getBoundsInParent().intersects(ball.getBoundsInParent())) {
            mag     *= (mag < 25) ? 1.1 : 1;
            angle   = Math.abs((Math.PI / 4.0) * (player.getY() + 75 - newY - 15) / 75);
            dX      = mag * Math.cos(angle);
            dY      = dY < 0 ? -mag * Math.sin(angle) : mag * Math.sin(angle);
            score.set(score.get() + 1);
        } else if (newX > 1150 && cpu.getBoundsInParent().intersects(ball.getBoundsInParent())) {
            dX = -dX;
        }
    }

    static void reset() {
        angle = atan2(1.0, 5.0);
        mag   = sqrt(26);
        dX    = mag * cos(angle);
        dY    = mag * sin(angle);

        ball.setCenterX(450);
        ball.setCenterY(350);
        player.setY(150);
        cpu.setY(450);
        score.set(0);
    }

}

class Controller {

    @FXML
    Pane            board;
    @FXML
    Label           score;

    AnimationTimer  loop;


    Controller() {
        loop = new AnimationTimer() {
            @Override
            public void handle(long l) {
                Game.update();
            }
        };
    }

    @FXML
    void initialize() {
        score.textProperty().bind(Bindings.convert(Game.score));

        board.getChildren().add(Game.player);
        board.getChildren().add(Game.cpu);
        board.getChildren().add(Game.ball);
    }

    @FXML
    void start() {
        loop.start();
    }

    @FXML
    void reset() {
        loop.stop();
        Game.reset();
    }

    void move(KeyEvent e) {
        switch (e.getCode()) {
            case UP     -> Game.vel = -10;
            case DOWN   -> Game.vel = 10;
        }
    }

    void halt(KeyEvent e) {
        Game.vel = 0;
    }

}

public class Main extends Application {

    public void start(Stage stage) {
        try {
            FXMLLoader loader       = new FXMLLoader(getClass().getResource("/views/View.fxml"));
            Controller controller   = new Controller();

            loader.setController(controller);

            BorderPane root         = loader.load();
            Scene      scene        = new Scene(root);

            scene.setOnKeyPressed(controller::move);
            scene.setOnKeyReleased(controller::halt);

            stage.setResizable(false);
            stage.setTitle("Pong");
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
