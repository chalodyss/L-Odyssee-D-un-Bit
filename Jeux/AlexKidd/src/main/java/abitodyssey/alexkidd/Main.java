/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

package abitodyssey.alexkidd;


import javafx.animation.AnimationTimer;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.beans.property.BooleanProperty;
import javafx.beans.property.SimpleBooleanProperty;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.image.WritableImage;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Pane;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.scene.text.Text;
import javafx.stage.Stage;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.EnumSet;
import java.util.List;
import java.util.Set;

import static abitodyssey.alexkidd.Collisions.*;


class Images {

    static Image GRASS       = new Image("grass.png", 50, 50, true, true);
    static Image WALL        = new Image("wall.png", 50, 50, true, true);
    //
    static Image SHEET       = new Image("sheet.png", 462, 1194, true, true);
    static Image ALEX_WALK_1 = new WritableImage(SHEET.getPixelReader(), 4, 4, 42, 70);
    static Image ALEX_WALK_2 = new WritableImage(SHEET.getPixelReader(), 55, 4, 42, 70);
    static Image ALEX_WALK_3 = new WritableImage(SHEET.getPixelReader(), 106, 4, 42, 70);
    //
    static Image ALEX        = new WritableImage(SHEET.getPixelReader(), 4, 85, 45, 70);
    static Image ALEX_PUNCH  = new WritableImage(SHEET.getPixelReader(), 58, 85, 66, 70);
    static Image ALEX_JUMP   = new WritableImage(SHEET.getPixelReader(), 133, 85, 45, 70);
    static Image ALEX_SQUAT  = new WritableImage(SHEET.getPixelReader(), 187, 85, 45, 70);

}

class Levels {

    private Levels() {}

    static List<Entity> load_level(String file) throws IOException {

        List<Entity> level = new ArrayList<>();
        var          x     = 0;
        var          y     = 0;

        try (InputStream is = Levels.class.getClassLoader().getResourceAsStream(file)) {
            if (is == null) {
                throw new FileNotFoundException("Resource not found: " + file);
            }

            try (BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(is))) {
                String line;

                while ((line = bufferedReader.readLine()) != null) {
                    for (int j = 0; j < line.length(); j++) {
                        switch (line.charAt(j)) {
                            case '1' -> level.add(new Entity(x, y, Images.GRASS));
                            case '2' -> level.add(new Entity(x, y, Images.WALL));
                            default -> {
                            }
                        }
                        x += 50;
                    }
                    x = 0;
                    y += 50;
                }
            }
        }

        return level;
    }

}

class Collisions {

    private Collisions() {}

    static boolean collide(Entity e1, Entity e2) {
        return e1.getBoundsInParent().intersects(e2.getBoundsInParent());
    }

    static void collidePlayerWalls(Player player, List<Entity> walls, char direction) {
        var entities = walls.stream().filter(w -> collide(player, w)).toList();

        if (!entities.isEmpty()) {
            var wall = entities.getFirst();

            if (direction == 'v') {
                player.velY = 0;
                if (player.getY() < wall.getY()) {
                    player.setY(wall.getY() - 71);
                    player.canJump = true;
                } else if (player.getY() > wall.getY()) {
                    player.setY(wall.getY() + 51);
                }
            } else if (direction == 'h') {
                if (player.getX() < wall.getX()) {
                    player.setX(wall.getX() - 46);
                } else if (player.getX() > wall.getX()) {
                    player.setX(wall.getX() + 51);
                }
            }
        }
    }

}

class Entity extends ImageView {

    Entity(double x, double y, Image img) {
        setX(x);
        setY(y);
        setImage(img);
    }

}

abstract class AnimatedEntity extends Entity {

    Image[] images;
    int     index;
    int     frame;


    AnimatedEntity(double x, double y, Image img) {
        super(x, y, img);
    }

    abstract void update(int n);

}

class Player extends AnimatedEntity {

    float   velX;
    float   velY;
    float   gravity;
    boolean canJump;


    Player(double x, double y, Image img) {
        super(x, y, img);
        gravity = 0.4f;
        canJump = true;
        images  = new Image[] { Images.ALEX_WALK_1, Images.ALEX_WALK_2, Images.ALEX_WALK_3,
                                Images.ALEX_PUNCH, Images.ALEX_JUMP, Images.ALEX_SQUAT };
    }

    void move(List<Entity> walls) {
        if (velY <= 9.8) {
            velY += gravity;
        }

        setY(getY() + velY);
        collidePlayerWalls(this, walls, 'v');

        setX(getX() + velX);
        collidePlayerWalls(this, walls, 'h');
    }

    @Override
    void update(int n) {
        if (getX() < 0) setX(0);
        if (getX() > 2650) setX(2650);

        switch (n) {
            case 0 -> {
                velX  = 0;
                index = 0;
                frame = 0;
                if (canJump) setImage(Images.ALEX);
            }
            case 1 -> {
                velX = -10;
                if (frame++ % 4 == 0) index = (index == 2) ? 0 : ++index;
                if (canJump) setImage((images[index]));
                setRotate(-180);
                setScaleY(-1);
            }
            case 2 -> {
                velX = 10;
                if (frame++ % 4 == 0) index = (index == 2) ? 0 : ++index;
                if (canJump) setImage((images[index]));
                if (getRotate() == -180) setRotate(0);
                if (getScaleY() == -1) setScaleY(1);
            }
            case 3 -> {
                if (canJump) {
                    setImage((images[4]));
                    velY -= 15;
                    canJump = false;
                }
            }
        }
    }

}

class Game {

    static BooleanProperty end;
    //
    static List<Entity>    level;
    static Player          player;

    static {
        reset();
    }


    private Game() {}

    static void reset() {
        end = new SimpleBooleanProperty(false);

        setLevel(1);
        setPlayer();
    }

    static void update() {
        updatePlayer();
        updateCollisions();
        updateImage();
    }

    static void updateCollisions() {

    }

    static void updateImage() {
        if (player.canJump && player.velX == 0) {
            player.setImage(Images.ALEX);
        }
    }

    static void updatePlayer() {
        player.move(level);
    }

    static void setPlayer() {
        player = new Player(50, 750, Images.ALEX);
    }

    static void setLevel(int n) {
        try {
            switch (n) {
                case 1  -> level = Levels.load_level("level_1.txt");
                case 2  -> level = Levels.load_level("level_2.txt");
                default -> {
                }
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

}

class Controller {

    Pane           board;
    //
    AnimationTimer loop;
    //
    Set<KeyCode>   activeKeys;
    boolean        jumpRelease;
    boolean        pause;


    Controller(Pane pane) {
        board       = pane;
        activeKeys  = EnumSet.noneOf(KeyCode.class);
        jumpRelease = true;
        loop        = new AnimationTimer() {
            @Override
            public void handle(long now) {
                if (!pause) {
                    if (!Game.end.get()) {
                        inputs();
                        Game.update();
                    } else {
                        stop();
                    }
                }
            }
        };
    }

    void scrolling() {
        Game.player.xProperty().addListener((obs, old, newValue) -> {
            var offset = newValue.intValue();

            if (offset > 900 && offset < 1800) {
                board.setTranslateX(900 - offset);
            }
        });
    }

    void pause(boolean b) {
        pause = b;
    }

    void reset() {
        pause(false);
        resetGame();
        resetBoard();
    }

    void start() {
        board.requestFocus();
        loop.start();
    }

    void inputs() {
        for (var code : activeKeys) {
            switch (code) {
                case LEFT   -> Game.player.update(1);
                case RIGHT  -> Game.player.update(2);
                case C      -> { if (jumpRelease) {
                                    Game.player.update(3);
                                    jumpRelease = false; }
                }
            }
        }
    }

    void onKeyPressed(KeyEvent e) {
        switch (e.getCode()) {
            case LEFT   -> { if (!activeKeys.contains(KeyCode.RIGHT)) activeKeys.add(KeyCode.LEFT); }
            case RIGHT  -> { if (!activeKeys.contains(KeyCode.LEFT)) activeKeys.add(KeyCode.RIGHT); }
            case C      -> { if (!activeKeys.contains(KeyCode.DOWN)) activeKeys.add(KeyCode.C); }
        }
    }

    void onKeyReleased(KeyEvent e) {
        switch (e.getCode()) {
            case LEFT -> {
                activeKeys.remove(KeyCode.LEFT);
                Game.player.update(0);
            }
            case RIGHT -> {
                activeKeys.remove(KeyCode.RIGHT);
                Game.player.update(0);
            }
            case C -> {
                activeKeys.remove(KeyCode.C);
                jumpRelease = true;
            }
        }
    }

    void resetBoard() {
        loop.stop();

        board.getChildren().clear();
        board.setTranslateX(0);
        board.getChildren().add(Game.player);
        board.getChildren().addAll(Game.level);
        board.setOnKeyPressed(this::onKeyPressed);
        board.setOnKeyReleased(this::onKeyReleased);
    }

    void resetGame() {
        Game.reset();
    }

}

class Home {

    Pane  home;
    Text  title;
    VBox  menu;
    int   currentItem;
    //
    App   app;
    Stage stage;
    Scene sceneHome;


    Home() {
        home = new Pane();
        home.setId("home");
        home.setPrefSize(1800, 1000);

        title = new Text("Alex Kidd");
        title.setId("title");
        title.setTranslateX(600);
        title.setTranslateY(250);

        menu = new VBox(new MenuItem("R E S E T"), new MenuItem("P A U S E"), new MenuItem("E X I T"));
        menu.setId("menu");
        menu.setTranslateX(600);
        menu.setTranslateY(350);
        getMenuItem(currentItem).setActive(true);

        home.getChildren().addAll(title, menu);
        home.getStylesheets().add("/Home.css");

        sceneHome = new Scene(home);
    }

    void action() {
        switch (currentItem % 3) {
            case 0 -> {
                stage.setScene(app.sceneApp);
                app.controller.reset();
                app.controller.scrolling();
                app.controller.start();
            }
            case 1 -> {
                stage.setScene(app.sceneApp);
                app.controller.pause(false);
            }
            case 2 -> {
                Platform.exit();
                System.exit(0);
            }
        }
    }

    void setOnKeyPressed() {
        sceneHome.setOnKeyPressed(e -> {
            switch (e.getCode()) {
                case DOWN -> {
                    getMenuItem(currentItem % 3).setActive(false);
                    getMenuItem(++currentItem % 3).setActive(true);
                }
                case ENTER -> action();
            }
        });
    }

    MenuItem getMenuItem(int index) {
        return (MenuItem) menu.getChildren().get(index);
    }

    static class MenuItem extends StackPane {

        Rectangle bg;
        Text      text;


        MenuItem(String name) {
            bg = new Rectangle(600, 100);

            text = new Text(name);
            text.setFill(Color.BLUE);
            text.setFont(Font.font("Consolas", FontWeight.SEMI_BOLD, 50));

            setActive(false);
            getChildren().addAll(bg, text);
        }

        void setActive(boolean b) {
            bg.setFill(b ? Color.AQUA : Color.BLACK);
        }

    }

}

class App {

    VBox       root;
    HBox       footer;
    Controller controller;
    //
    Stage      stage;
    Scene      sceneApp;
    Home       home;


    App() {
        root = new VBox();
        root.setPrefWidth(1800);
        root.setPrefHeight(1000);

        footer = new HBox();
        footer.setPrefWidth(1800);
        footer.setPrefHeight(100);
        footer.setStyle("-fx-background-color : black");

        Pane board = new Pane();
        board.setPrefWidth(2700);
        board.setPrefHeight(900);

        root.getChildren().addAll(board, footer);

        controller = new Controller(board);

        sceneApp = new Scene(root);
        sceneApp.setFill(Color.BLUE);
    }


    void setOnKeyPressed() {
        sceneApp.setOnKeyPressed(e -> {
            if (e.getCode() == KeyCode.ENTER) {
                controller.pause(true);
                stage.setScene(home.sceneHome);
            }
        });
    }

}

public class Main extends Application {

    @Override
    public void start(Stage primaryStage) {
        try {
            var home    = new Home();
            var app     = new App();

            app.stage   = primaryStage;
            home.stage  = primaryStage;

            app.home    = home;
            home.app    = app;

            app.setOnKeyPressed();
            home.setOnKeyPressed();

            primaryStage.setTitle("Alex Kidd");
            primaryStage.setResizable(false);
            primaryStage.setScene(home.sceneHome);
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
