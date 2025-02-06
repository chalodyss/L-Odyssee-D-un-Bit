/*
 * Copyright © 2025 Charles Theetten
 * Tous droits réservés.
 * Ce programme est distribué sous licence CC BY-NC-ND 4.0.
 */

package abitodyssey.spaceinvaders;


import javafx.animation.AnimationTimer;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.beans.binding.Bindings;
import javafx.beans.property.BooleanProperty;
import javafx.beans.property.IntegerProperty;
import javafx.beans.property.SimpleBooleanProperty;
import javafx.beans.property.SimpleIntegerProperty;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.Pane;
import javafx.scene.layout.VBox;
import javafx.scene.text.Text;
import javafx.stage.Stage;

import java.util.*;

import static abitodyssey.spaceinvaders.Collisions.*;
import static abitodyssey.spaceinvaders.EState.*;
import static abitodyssey.spaceinvaders.Images.*;


class Images {

    static Image PLAYER       = new Image("/player.png", 50, 40, false, false);
    static Image CRAB         = new Image("/crab.png", 50, 40, false, false);
    static Image OCTOPUS      = new Image("/octopus.png", 50, 40, false, false);
    static Image SQUID        = new Image("/squid.png", 50, 40, false, false);
    static Image BEAM_PLAYER  = new Image("/beam_player.png", 5, 25, false, false);
    static Image BEAM_INVADER = new Image("/beam_invader.png", 5, 25, false, false);
    static Image WALL         = new Image("/wall.png", 40, 30, false, false);

}

enum EState {
    ALIVE, DEAD;
}

class Entity extends ImageView {

    EState state;


    public Entity(double x, double y, Image img) {
        setX(x);
        setY(y);
        state = ALIVE;
        setImage(img);
    }

    void move(double velX, double velY) {
        setX(getX() + velX);
        setY(getY() + velY);
    }

    boolean isDead() {
        return state == DEAD;
    }

}

class Player extends Entity {

    Entity  beam;
    int     velX;
    boolean canShoot;


    public Player(double x, double y, Image img) {
        super(x, y, img);

        beam     = new Entity(-20, 0, BEAM_PLAYER);
        canShoot = true;
    }

    void move() {
        if ((getX() >= 10 && velX < 0) || (getX() < 945 && velX > 0)) {
            setX(getX() + velX);
        }
    }

    void shoot() {
        if (canShoot) {
            beam.setX(getX() + 23);
            beam.setY(getY());
        }

        canShoot = false;
    }

}

class Collisions {

    private Collisions() {}

    static boolean collide(Entity e1, Entity e2) {
        return e1.getBoundsInParent().intersects(e2.getBoundsInParent());
    }

    static void collideBeamInvadersPlayer(List<Entity> beams, Player player, BooleanProperty end) {
        if (beams.stream().anyMatch(b -> collide(b, player))) {
            player.state = DEAD;
            end.set(true);
        }
    }

    static void collideBeamInvadersWalls(List<Entity> beams, List<Entity> walls) {
        walls.removeIf(w -> {
            var op = beams.stream().filter(b -> collide(b, w)).findFirst();

            if (op.isPresent()) {
                Entity e = op.get();
                e.state = DEAD;
                w.state = DEAD;
                return true;
            }
            
            return false;
        });
    }

    static void collideBeamPlayerInvaders(Entity beam, List<Entity> invaders, IntegerProperty score) {
        if (beam.getY() > 0) {
            var op = invaders.stream().filter(i -> collide(i, beam)).findFirst();

            if (op.isPresent()) {
                Entity e = op.get();
                e.state = DEAD;
                beam.setY(-25);
                score.set(score.get() + 20);
                invaders.remove(e);
            }
        }
    }

    static void collideBeamPlayerWalls(Entity beam, List<Entity> walls) {
        if (beam.getY() > 0) {
            var op = walls.stream().filter(w -> collide(w, beam)).findFirst();

            if (op.isPresent()) {
                Entity e = op.get();
                e.state = DEAD;
                beam.setY(-25);
                walls.remove(e);
            }
        }
    }

    static void collideInvadersPlayer(Entity player, List<Entity> invaders, BooleanProperty end) {
        var op = invaders.stream().filter(i -> (i.getY() >= 435 && collide(i, player))).findFirst();

        if (op.isPresent()) {
            player.state = DEAD;
            end.set(true);
        }
    }

}

class Game {

    static BooleanProperty end;
    static IntegerProperty score;
    //
    static Random          rand;
    static int             direction;
    static double          deltaX;
    //
    static Player          player;
    static List<Entity>    invaders;
    static List<Entity>    walls;
    static List<Entity>    beams;

    static {
        reset();
    }


    private Game() {}

    static void reset() {
        end       = new SimpleBooleanProperty(false);
        score     = new SimpleIntegerProperty(0);
        rand      = new Random();
        direction = 0;
        deltaX    = 1;

        end.set(false);
        score.set(0);

        setPlayer();
        setInvaders();
        setWalls();
        setBeams();
    }

    static void update() {
        updatePlayer();
        updateInvaders();
        updateBeams();
        updateCollisions();
    }

    static void updatePlayer() {
        player.move();
    }

    static void updateInvaders() {
        invadersMove();
        invadersShoot();
    }

    static void invadersMove() {
        if ((direction & 1) == 0) {
            invaders.forEach(invader -> invader.move(deltaX, 0));
        } else {
            invaders.forEach(invader -> invader.move(0, 15));
            deltaX = -deltaX;
        }

        for (var invader : invaders) {
            if (invader.getX() <= 50 || invader.getX() >= 900) {
                direction ^= 1;
                break;
            }
        }

        if (invaders.size() > 33)       deltaX = (deltaX < 0) ? -1 : 1;
        else if (invaders.size() > 11)  deltaX = (deltaX < 0) ? -2 : 2;
        else if (invaders.size() > 5)   deltaX = (deltaX < 0) ? -5 : 5;
        else if (invaders.size() > 1)   deltaX = (deltaX < 0) ? -10 : 10;
        else                            deltaX = (deltaX < 0) ? -25 : 25;
    }

    static void invadersShoot() {
        invaders.forEach(i -> {
            if (beams.size() < 5 && rand.nextInt(55) == 0) {
                var beam = new Entity(i.getX() + 23, i.getY() + 40, BEAM_INVADER);
                beams.add(beam);
            }
        });
    }

    static void updateBeams() {
        updateBeamPlayer();
        updateBeamsInvaders();
    }

    static void updateBeamsInvaders() {
        beams.forEach(beam -> {
            if (beam.getY() > 700) beam.state = DEAD;
            else beam.setY(beam.getY() + 5);
        });
        beams.removeIf(Entity::isDead);
    }

    static void updateBeamPlayer() {
        if (player.beam.getY() < 0) {
            player.beam.move(-20, 0);
            player.canShoot = true;
        } else if (player.beam.getY() >= 0) {
            player.beam.move(0, -30);
        }
    }

    static void updateCollisions() {
        collideBeamInvadersWalls(beams, walls);
        collideBeamPlayerWalls(player.beam, walls);
        collideBeamInvadersPlayer(beams, player, end);
        collideBeamPlayerInvaders(player.beam, invaders, score);
        collideInvadersPlayer(player, invaders, end);
    }

    static void setBeams() {
        beams = new LinkedList<>();
    }

    static void setPlayer() {
        player = new Player(475, 660, PLAYER);
    }

    static void setInvaders() {
        var x = 60;
        var y = 60;

        invaders = new LinkedList<>();

        for (var i = 1; i <= 60; i++) {
            if (i <= 12)        invaders.add(new Entity(x, y, SQUID));
            else if (i <= 36)   invaders.add(new Entity(x, y, CRAB));
            else                invaders.add(new Entity(x, y, OCTOPUS));

            x = (i % 12 == 0) ? 60 : x + 60;
            y = (i % 12 == 0) ? y + 60 : y;
        }
    }

    static void setWalls() {
        var x = 100;
        var y = 500;

        walls = new LinkedList<>();

        for (var i = 0; i < 4; i++) {
            for (var j = 1; j <= 15; j++) {
                if (x == 300) x = 400;
                else if (x == 600) x = 700;
                walls.add(new Entity(x, y, WALL));
                x += 40;
            }

            x = 100;
            y += 30 - 1;
        }
    }

}

class Renderer {

    private Renderer() {}

    static void renderBeams(Pane board) {
        for (var e : Game.beams) {
            if (!board.getChildren().contains(e)) {
                board.getChildren().add(e);
            }
        }
    }

    static void removeEntities(Pane board) {
        board.getChildren().removeIf(e -> {
            var entity = (Entity) e;
            return entity.state == DEAD;
        });
    }

    static void render(Pane board) {
        renderBeams(board);
        removeEntities(board);
    }

}

class Controller {

    @FXML
    Pane            board;
    @FXML
    Text            score;

    AnimationTimer  loop;
    Set<KeyCode>    activeKeys;


    Controller() {
        activeKeys = EnumSet.noneOf(KeyCode.class);
        loop       = new AnimationTimer() {
            @Override
            public void handle(long now) {
                if (!Game.end.get()) {
                    inputs();
                    Game.update();
                    Renderer.render(board);
                } else {
                    stop();
                }
            }
        };
    }

    @FXML
    void initialize() {
        resetBoard();
    }

    @FXML
    void reset() {
        resetGame();
        resetBoard();
    }

    @FXML
    void start() {
        loop.start();
    }

    void inputs() {
        for (var code : activeKeys) {
            switch (code) {
                case LEFT   -> Game.player.velX = -10;
                case RIGHT  -> Game.player.velX = 10;
                case SPACE  -> Game.player.shoot();
            }
        }
    }

    void move(KeyEvent e) {
        switch (e.getCode()) {
            case LEFT   -> { if (!activeKeys.contains(KeyCode.RIGHT)) activeKeys.add(e.getCode()); }
            case RIGHT  -> { if (!activeKeys.contains(KeyCode.LEFT)) activeKeys.add(e.getCode()); }
            case SPACE  -> activeKeys.add(e.getCode());
        }
    }


    void halt(KeyEvent e) {
        switch (e.getCode()) {
            case LEFT -> {
                activeKeys.remove(KeyCode.LEFT);
                Game.player.velX = 0;
            }
            case RIGHT -> {
                activeKeys.remove(KeyCode.RIGHT);
                Game.player.velX = 0;
            }
            case SPACE -> activeKeys.remove(KeyCode.SPACE);
        }
    }

    void resetBoard() {
        loop.stop();

        board.getChildren().clear();
        board.getChildren().add(Game.player);
        board.getChildren().add(Game.player.beam);
        board.getChildren().addAll(Game.invaders);
        board.getChildren().addAll(Game.walls);

        score.textProperty().bind(Bindings.convert(Game.score));
    }

    void resetGame() {
        Game.reset();
    }

}

public class Main extends Application {

    @Override
    public void start(Stage primaryStage) {
        try {
            FXMLLoader loader       = new FXMLLoader(getClass().getResource("/views/View.fxml"));
            Controller controller   = new Controller();

            loader.setController(controller);

            VBox  root              = loader.load();
            Scene scene             = new Scene(root);

            scene.setOnKeyPressed(controller::move);
            scene.setOnKeyReleased(controller::halt);

            primaryStage.setTitle("Space Invaders");
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
