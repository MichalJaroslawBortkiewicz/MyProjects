import java.util.ArrayList;

import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import javafx.stage.Stage;
import javafx.util.Duration;

public class Main extends Application{
    double SQUARE_SIDE = 30;

    int HEIGHT = 20;
    int WIDTH = 30;

    double WINDOW_WIDTH = WIDTH * SQUARE_SIDE;
    double WINDOW_HEIGHT = HEIGHT * SQUARE_SIDE;

    DirectionEnum direction = DirectionEnum.RIGHT;


    public static void main(String[] args){
        launch(args);
    }

    @Override
    public void start(Stage stage) {
        Rectangle win = new Rectangle(WINDOW_WIDTH + 2, WINDOW_HEIGHT + 2, Color.TRANSPARENT);
        win.setLayoutX(SQUARE_SIDE - 1);
        win.setLayoutY(SQUARE_SIDE - 1);
        win.setStroke(Color.WHITE);
        win.setStrokeWidth(2);

        Pane plane = new Pane();
        Group root = new Group(plane, win);
        Scene scene = new Scene(root, WINDOW_WIDTH + 2 * SQUARE_SIDE, WINDOW_HEIGHT + 2 * SQUARE_SIDE, Color.BLACK);

        Snake snake = new Snake(WIDTH, HEIGHT);
        
        scene.setOnKeyPressed(event ->{
            switch(event.getCode()){
                case W:
                    direction = DirectionEnum.UP;
                    break;
                case S:
                    direction = DirectionEnum.DOWN;
                    break;
                case A:
                    direction = DirectionEnum.LEFT;
                    break;
                case D:
                    direction = DirectionEnum.RIGHT;
                    break;
                default:
            }
        });

        Timeline snakeMove = new Timeline(
            new KeyFrame(Duration.seconds(0.2), 
            new EventHandler<ActionEvent>() {
                @Override
                public void handle(ActionEvent event){
                    try{
                        snake.move(direction);
                        if(snake.getLength() == WIDTH * HEIGHT){
                            System.out.println("YOU WON!!! SENSATIONAL!!!");
                            Platform.exit();
                        }
                        display(plane, snake);
                    }
                    catch(GameOverException ex){
                        System.out.println("You lost!");
                        Platform.exit();
                    }
                }
            }
        ));

        snakeMove.setCycleCount(Timeline.INDEFINITE);
        snakeMove.play();

        stage.setTitle("Snake");
        stage.setScene(scene);
        stage.show();
    }
    
    private void display(Pane plane, Snake snake){
        ArrayList<Point> snakePoints = snake.getPoints();
        plane.getChildren().clear();
        
        for(int i = 0; i < snakePoints.size(); i++){
            Point point = snakePoints.get(i);

            Rectangle snakeBody = new Rectangle(SQUARE_SIDE * (point.x + 1) + 1, SQUARE_SIDE * (point.y + 1) + 1, SQUARE_SIDE - 2, SQUARE_SIDE - 2);
            snakeBody.setFill((i == 0) ? Color.YELLOW : Color.GREEN);
            plane.getChildren().add(snakeBody);
        }

        Point point = snake.getApple();
        Rectangle apple = new Rectangle(SQUARE_SIDE * (point.x + 1) + 1, SQUARE_SIDE * (point.y + 1) + 1, SQUARE_SIDE, SQUARE_SIDE);
        apple.setFill(Color.RED);
        plane.getChildren().add(apple);
    }
}
