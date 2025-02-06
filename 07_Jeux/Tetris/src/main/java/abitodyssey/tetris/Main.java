/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

package abitodyssey.tetris;


import javafx.animation.AnimationTimer;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.beans.property.*;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.BorderPane;
import javafx.scene.paint.Color;
import javafx.scene.text.Text;
import javafx.stage.Stage;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.function.IntPredicate;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import static abitodyssey.tetris.Collisions.*;
import static abitodyssey.tetris.Tetros.*;
import static abitodyssey.tetris.Renderer.*;


class Tetros {

    static final List<Tetromino> TETROMINOS = List.of(new Tetromino(Color.YELLOW, new Square(4, 2), new Square(5, 2), new Square(4, 3), new Square(5, 3)),
                                                      new Tetromino(Color.CYAN, new Square(4, 2), new Square(4, 0), new Square(4, 1), new Square(4, 3)),
                                                      new Tetromino(Color.VIOLET, new Square(4, 2), new Square(3, 2), new Square(5, 2), new Square(4, 3)),
                                                      new Tetromino(Color.ORANGE, new Square(4, 1), new Square(5, 1), new Square(4, 2), new Square(4, 3)),
                                                      new Tetromino(Color.BLUE, new Square(4, 1), new Square(3, 1), new Square(4, 2), new Square(4, 3)),
                                                      new Tetromino(Color.RED, new Square(4, 2), new Square(3, 2), new Square(4, 3), new Square(5, 3)),
                                                      new Tetromino(Color.LAWNGREEN, new Square(4, 2), new Square(5, 2), new Square(4, 3), new Square(3, 3)));

}

class Square {

    int x;
    int y;


    public Square(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public Square(Square s) {
        x = s.x;
        y = s.y;
    }

}

class Tetromino {

    Color        color;
    List<Square> squares;


    public Tetromino(Color color, Square... squares) {
        this.color   = color;
        this.squares = Arrays.asList(squares);
    }

    public Tetromino(Tetromino tetromino) {
        color   = tetromino.color;
        squares = tetromino.squares.stream().map(Square::new).collect(Collectors.toList());
    }

    void move(int dx, int dy) {
        squares.forEach(s -> {
            s.x += dx;
            s.y += dy;
        });
    }

    void rotate() {
        var origin = squares.getFirst();

        for (var i = 1; i <= 3; i++) {
            var s = squares.get(i);
            var x = s.x;
            s.x = origin.x + origin.y - s.y;
            s.y = origin.y - origin.x + x;
        }
    }

}

class Collisions {

    private Collisions() {}

    static boolean isNotBottomCollided(Tetromino tetro, int[][] board) {
        return tetro.squares.stream().allMatch(s -> s.y < 23 && board[s.y + 1][s.x] == 0);
    }

    static boolean isNotLeftCollided(Tetromino tetro, int[][] board) {
        IntPredicate p = x -> x > 0;

        return tetro.squares.stream().allMatch(s -> p.test(s.x) && board[s.y][s.x - 1] == 0);
    }

    static boolean isNotRightCollided(Tetromino tetro, int[][] board) {
        IntPredicate p = x -> x < 9;

        return tetro.squares.stream().allMatch(s -> p.test(s.x) && board[s.y][s.x + 1] == 0);
    }

    static boolean isNotTetroCollided(Tetromino tetro, int[][] board) {
        var copy = new Tetromino(tetro);

        copy.rotate();

        for (Square s : copy.squares) {
            if (s.x < 0 || s.x > 9 || s.y < 0 || s.y > 23)  return false;
            if (board[s.y][s.x] == 1)                       return false;
        }

        return true;
    }

}

class Game {

    static BooleanProperty end;
    static IntegerProperty level;
    static IntegerProperty score;
    static LongProperty    time;

    static Random          rand;
    static int             scoreLimit;
    static int[][]         grid;
    static List<Tetromino> tetrominos;
    static Tetromino       curTetro;
    static int             nbRows;

    static {
        reset();
    }


    private Game() {}

    static void reset() {
        end        = new SimpleBooleanProperty(false);
        level      = new SimpleIntegerProperty(1);
        score      = new SimpleIntegerProperty(0);
        time       = new SimpleLongProperty(1_000_000_000L);
        rand       = new Random();
        scoreLimit = 400;
        grid       = new int[24][10];
        tetrominos = new ArrayList<>();
        curTetro   = new Tetromino(TETROMINOS.get(rand.nextInt(7)));
        nbRows     = 0;

        tetrominos.add(curTetro);
    }

    static void update() {
        if (isNotBottomCollided(curTetro, grid)) {
            curTetro.squares.forEach(s -> s.y++);
        } else {
            curTetro.squares.forEach(s -> grid[s.y][s.x] = 1);
            nbRows = updateRows();
            if (nbRows > 0) {
                updateScore();
                updateLevel();
                nbRows = 0;
            }
            curTetro = new Tetromino(TETROMINOS.get(rand.nextInt(7)));
            tetrominos.add(curTetro);
        }
    }

    static void resetGrid() {
        for (int[] line : grid) {
            Arrays.fill(line, 0);
        }
    }

    static void updateLevel() {
        if (score.get() >= scoreLimit) {
            if (level.get() < 10) {
                level.set(level.get() + 1);
                time.set(time.get() - 100_000_000L);
                scoreLimit = 100 * 4 * level.get() * 2;
            }
        }
    }

    static void updateScore() {
        score.set(score.get() + 100 * nbRows * level.get());
    }

    static int updateRows() {
        var rows = 0;
        var i    = 23;

        while (i > 0) {
            if (Arrays.stream(grid[i]).filter(e -> e == 1).count() == 10) {
                rows++;
                resetGrid();
                var lim = i;
                tetrominos.forEach(t -> t.squares.removeIf(s -> s.y == lim));
                tetrominos.removeIf(t -> t.squares.isEmpty());
                tetrominos.forEach(t -> t.squares.forEach(s -> s.y += (s.y < lim) ? 1 : 0));
                tetrominos.forEach(t -> t.squares.forEach(s -> grid[s.y][s.x] = 1));
            } else {
                i--;
            }
        }

        return rows;
    }

}

class Renderer {

    private Renderer() {}

    static void render(GraphicsContext gc, List<Tetromino> tetrominos) {
        gc.setFill(Color.BLACK);
        gc.fillRect(0, 0, 350, 700);
        gc.setStroke(Color.WHITE);
        IntStream.range(1, 10).forEach(i -> gc.strokeLine(i * 350.0 / 10, 0, i * 350.0 / 10, 700));
        IntStream.range(1, 10 * 2).forEach(j -> gc.strokeLine(0, j * 0.5 * 700.0 / 10, 350, j * 0.5 * 700.0 / 10));

        tetrominos.forEach(t -> {
            gc.setFill(t.color);
            t.squares.forEach(s -> gc.fillRect(s.x * 35 + 1, (s.y - 4) * 35 + 1, 33, 33));
        });
    }

}

class Controller {

    @FXML
    Text            score;
    @FXML
    Text            level;
    @FXML
    Canvas          canvas;

    LongProperty    timeInterval;
    AnimationTimer  loop;


    Controller() {
        loop = new AnimationTimer() {
            long lastTime;

            @Override
            public void handle(long now) {
                long time = now - lastTime;
                if (time >= timeInterval.get()) {
                    Game.update();
                    lastTime = now;
                }
                render(canvas.getGraphicsContext2D(), Game.tetrominos);
            }
        };
    }

    @FXML
    void initialize() {
        level.textProperty().bind(Game.level.asString());
        score.textProperty().bind(Game.score.asString());
        render(canvas.getGraphicsContext2D(), Game.tetrominos);
    }

    @FXML
    void start() {
        if (loop != null) loop.stop();
        Game.reset();
        canvas.getGraphicsContext2D().clearRect(0, 0, 350, 700);
        timeInterval = new SimpleLongProperty(1_000_000_000L);
        timeInterval.bind(Game.time);
        if (loop != null) loop.start();
    }

    void move(KeyEvent e) {
        switch (e.getCode()) {
            case LEFT   -> { if (isNotLeftCollided(Game.curTetro, Game.grid))   Game.curTetro.move(-1, 0); }
            case DOWN   -> { if (isNotBottomCollided(Game.curTetro, Game.grid)) Game.curTetro.move(0, 1); }
            case RIGHT  -> { if (isNotRightCollided(Game.curTetro, Game.grid))  Game.curTetro.move(1, 0); }
            case UP     -> { if (isNotTetroCollided(Game.curTetro, Game.grid))  Game.curTetro.rotate(); }
        }
    }

}

public class Main extends Application {

    @Override
    public void start(Stage primaryStage) {
        try {
            FXMLLoader loader       = new FXMLLoader(getClass().getResource("/views/View.fxml"));
            Controller controller   = new Controller();

            loader.setController(controller);

            BorderPane root         = loader.load();
            Scene      scene        = new Scene(root);

            scene.setOnKeyPressed(controller::move);

            primaryStage.setTitle("Tetris");
            primaryStage.setResizable(false);
            primaryStage.setScene(scene);
            primaryStage.show();
        } catch (Exception e) {
            Platform.exit();
            System.exit(-1);
        }
    }

    public static void main(String[] args) {
        launch(args);
    }

}
