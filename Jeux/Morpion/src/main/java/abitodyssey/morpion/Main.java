/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

package abitodyssey.morpion;


import javafx.application.Application;
import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.image.Image;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.HBox;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;
import java.util.stream.IntStream;


class Game {

    static Random  rand;
    static int     move;
    static int     nbMoves;
    static boolean end;
    static int[]   grid;
    static int[]   rows;
    static int[]   cols;
    static int     lDiag;
    static int     rDiag;


    private Game() { }

    static void init(int start) {
        rand    = new Random();
        move    = start;
        nbMoves = 9;
        end     = false;
        grid    = new int[9];
        rows    = new int[3];
        cols    = new int[3];
        lDiag   = 0;
        rDiag   = 0;
    }

    static void checkEnd() {
        end = isAligned() || nbMoves == 0;
    }

    static int o_play() {
        var cells = new ArrayList<>();
        var cell  = -1;

        for (var i = 0; i < 9; i++) if (grid[i] == 0) cells.add(i);
        cell       = (int) cells.get(rand.nextInt(cells.size()));
        grid[cell] = -1;
        move       = 1;
        update(cell, -1);

        return cell;
    }

    static void x_play(int row, int col) {
        grid[row * 3 + col] = 1;
        move                = 0;

        update(row * 3 + col, 1);
    }

    static void update(int num, int state) {
        int c = num % 3;
        int r = num / 3;

        rows[r] += state;
        cols[c] += state;
        lDiag   += (r == c) ? state : 0;
        rDiag   += (r + c == 2) ? state : 0;
    }

    static boolean isAligned() {
        return (Arrays.stream(rows).filter(v -> Math.abs(v) == 3).count() == 1)
                || (Arrays.stream(cols).filter(v -> Math.abs(v) == 3).count() == 1)
                || (Math.abs(lDiag) == 3) || (Math.abs(rDiag) == 3);
    }

}

class Controller {

    Image           cross  = new Image("/cross.png", 240, 240, false, false);
    Image           circle = new Image("/circle.png", 240, 240, false, false);

    @FXML
    Canvas          board;

    int             start;


    Controller() { }

    @FXML
    void initialize() {
        board.setOnMouseClicked(this::play);
        start();
    }

    @FXML
    void start() {
        start = start == 0 ? 1 : 0;
        drawBoard(board.getGraphicsContext2D());
        Game.init(start);

        if (Game.move == 0) {
            var num = Game.o_play();
            var x   = num % 3;
            var y   = num / 3;

            drawMove(circle, x, y);
        }
    }

    void play(MouseEvent e) {
        int row = (e.getY() < 250) ? 0 : (e.getY() < 500) ? 1 : 2;
        int col = (e.getX() < 250) ? 0 : (e.getX() < 500) ? 1 : 2;

        if (!Game.end && Game.move == 1 && Game.grid[row * 3 + col] == 0) {
            Game.x_play(row, col);
            drawMove(cross, col, row);
            Game.checkEnd();
            if (!Game.end) {
                var num = Game.o_play();
                var x   = num % 3;
                var y   = num / 3;
                drawMove(circle, x, y);
                Game.checkEnd();
            }
        }
    }

    void drawBoard(GraphicsContext gc) {
        gc.clearRect(0, 0, 750, 750);
        gc.fillRect(0, 0, 750, 750);
        gc.setLineWidth(1);
        gc.setStroke(Color.WHITE);
        IntStream.range(1, 3).forEach(i -> {
            gc.strokeLine(i * 250, 0, i * 250, 750);
            gc.strokeLine(0, i * 250, 750, i * 250);
        });
    }

    void drawMove(Image img, int x, int y) {
        board.getGraphicsContext2D().drawImage(img, x * 250 + 5, y * 250 + 5);
    }

}

public class Main extends Application {

    public void start(Stage stage) {
        try {
            Controller controller = new Controller();

            FXMLLoader loader = new FXMLLoader(getClass().getResource("/views/View.fxml"));
            loader.setController(controller);

            HBox  root  = loader.load();
            Scene scene = new Scene(root);

            stage.setResizable(false);
            stage.setTitle("Morpion");
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
