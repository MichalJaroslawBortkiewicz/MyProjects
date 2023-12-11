import java.util.HashSet;
import java.util.Set;

import javafx.application.Application;
import javafx.collections.ObservableList;
import javafx.event.EventTarget;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.geometry.Rectangle2D;
import javafx.scene.Group;
import javafx.scene.Node;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.ColorPicker;
import javafx.scene.control.Menu;
import javafx.scene.control.MenuBar;
import javafx.scene.control.MenuItem;
import javafx.scene.control.TextArea;
import javafx.scene.control.Tooltip;
import javafx.scene.input.KeyCode;
import javafx.scene.input.MouseButton;
import javafx.scene.layout.Background;
import javafx.scene.layout.BackgroundFill;
import javafx.scene.layout.CornerRadii;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Pane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.ClosePath;
import javafx.scene.shape.Ellipse;
import javafx.scene.shape.LineTo;
import javafx.scene.shape.MoveTo;
import javafx.scene.shape.Path;
import javafx.scene.shape.Polygon;
import javafx.scene.shape.Rectangle;
import javafx.scene.text.Font;
import javafx.scene.text.Text;
import javafx.stage.Modality;
import javafx.stage.Screen;
import javafx.stage.Stage;
 
public class Main extends Application {
    enum Tool{
        CURSOR,
        RECTANGLE,
        ELLIPSE,
        POLYGON
    }

    double WIDTH = 800;
    double HEIGHT = 800;
    double SCALE = 0.05;

    private final Set<KeyCode> pressedKeys = new HashSet<>();
    Figure figure;
    Tool selectedTool;
    double mx, my;
    Color color = Color.TRANSPARENT;
    

    public static void main(String[] args) {
        launch(args);
    }
    

    @Override
    public void start(Stage stage) {
        Pane GUI = new Pane();
        Pane plane = new Pane();
        Group root = new Group(plane, GUI);
        Scene scene = new Scene(root, WIDTH, HEIGHT);

        HBox buttonBar = createButtonBar(plane);
        MenuBar menuBar = createMenu();
        
        GUI.getChildren().addAll(buttonBar, menuBar);

        stage.widthProperty().addListener((obs, oldVal, newVal) -> {
            buttonBar.setMinWidth((double)newVal);
            buttonBar.setMaxWidth((double)newVal);
            plane.setMinWidth((double)newVal);
            plane.setMaxWidth((double)newVal);
        });
       
        stage.heightProperty().addListener((obs, oldVal, newVal) -> {
            plane.setMinHeight((double)newVal);
            plane.setMaxWidth((double)newVal);
        });

        scene.setOnKeyPressed(event -> pressedKeys.add(event.getCode()));
        
        scene.setOnKeyReleased(event ->  {
            pressedKeys.remove(event.getCode());
            if(event.getCode() == KeyCode.CONTROL && selectedTool == Tool.CURSOR && figure != null) figure.setPivot(mx, my);
        });

        plane.setOnMouseMoved(event -> {
            mx = event.getX();
            my = event.getY();
        });

        stage.setTitle("Paint");
        stage.setScene(scene);
        stage.show();
    }


    private HBox createButtonBar(Pane plane){
        /*
        Path cursorIcon = new Path(
            new MoveTo(0, 0),
            new LineTo(0, 16),
            new LineTo(4, 12),
            new LineTo(6.625, 17.5),
            new LineTo(9.125, 17.5),
            new LineTo(6.25, 12),
            new LineTo(6.25 + 4 * Math.sqrt(2), 12),
            new ClosePath()
        );
        cursorIcon.setStrokeWidth(2);*/

        Path cursorIcon = new Path(
            new MoveTo(0, 0),
            new LineTo(0, 14),
            new LineTo(3, 11),
            //new LineTo(6.75, 15),
            new LineTo(5.25, 15),
            new LineTo(8.03125, 15),
            new LineTo(5.5, 10.5),
            new LineTo(10, 10.5),
            new ClosePath()
        );
        cursorIcon.setStrokeWidth(1.5);

        Rectangle squareIcon = new Rectangle(15, 15, Color.TRANSPARENT);
        squareIcon.setStroke(Color.BLACK);
        squareIcon.setStrokeWidth(1.5);

        Circle circleIcon = new Circle(7.5, Color.TRANSPARENT);
        circleIcon.setStroke(Color.BLACK);
        circleIcon.setStrokeWidth(1.5);

        Path pentagonIcon = new Path(
            new MoveTo(0, 0),
            new LineTo(0, 15),
            new LineTo(15, 15),
            new LineTo(10, 10),
            new LineTo(5, 10),
            new LineTo(5, 5),
            new ClosePath()
        );
        pentagonIcon.setStrokeWidth(1.5);

        double side = 5 * Math.sqrt(3);
        Path regularNGonIcon = new Path(
            new MoveTo(0, 7.5),
            new LineTo(side / 2, 15),
            new LineTo(1.5 * side, 15),
            new LineTo(2 * side, 7.5),
            new LineTo(1.5 * side, 0),
            new LineTo(side / 2, 0),
            new ClosePath()
        );
        regularNGonIcon.setStrokeWidth(1.5);

        Button cursorButton = new Button("", cursorIcon);
        Button rectangleButton = new Button("", squareIcon);
        Button circleButton = new Button("", circleIcon);
        Button polygonButton = new Button ("", pentagonIcon);
        Button regularNGonButton = new Button("", regularNGonIcon);
        final ColorPicker colorButton = new ColorPicker();

        cursorButton.setMinSize(30, 30);
        cursorButton.setMaxSize(30, 30);
        rectangleButton.setMinSize(30, 30);
        rectangleButton.setMaxSize(30, 30);
        circleButton.setMinSize(30, 30);
        circleButton.setMaxSize(30, 30);
        polygonButton.setMinSize(30, 30);
        polygonButton.setMaxSize(30, 30);
        regularNGonButton.setMinSize(30, 30);
        regularNGonButton.setMaxSize(30, 30);
        colorButton.setMinSize(30, 30);
        colorButton.setMaxSize(30, 30);

        cursorButton.setTooltip(new Tooltip("Cursor"));
        rectangleButton.setTooltip(new Tooltip("Rectangle"));
        circleButton.setTooltip(new Tooltip("Circle"));
        polygonButton.setTooltip(new Tooltip("Polygon"));
        regularNGonButton.setTooltip(new Tooltip("Regular n-gon"));
        colorButton.setTooltip(new Tooltip("Color"));


        cursorButton.setOnAction(event -> {
            selectedTool = Tool.CURSOR;
            setCursorActions(plane);
        });
        rectangleButton.setOnAction(event -> {
            selectedTool = Tool.RECTANGLE;
            setRectangleActions(plane);
        });
        circleButton.setOnAction(event -> {
            selectedTool = Tool.ELLIPSE;
            setCircleActions(plane);
        });
        polygonButton.setOnAction(event -> {
            selectedTool = Tool.POLYGON;
            setPolygonActions(plane);
        });
        colorButton.setOnAction(event -> {
            color = colorButton.getValue();
            cursorButton.fire();
        });

        cursorButton.fire();

        HBox functions = new HBox(5, cursorButton, rectangleButton, circleButton, polygonButton, regularNGonButton, colorButton);
        functions.setBackground(new Background(new BackgroundFill(Color.LIGHTGREY, CornerRadii.EMPTY, Insets.EMPTY)));
        functions.setAlignment(Pos.CENTER);
        functions.setPrefSize(WIDTH, 40);
        return functions;
    }


    private void setCursorActions(Pane plane){
        plane.setOnMousePressed(event -> {
            EventTarget et  = event.getTarget();
            switch (et.getClass().getSimpleName()){
                case "Rectangle":
                    figure = new RectangleFigure((Rectangle)et, event.getX(), event.getY());
                    break;
                case "Ellipse":
                    figure = new EllipseFigure((Ellipse)et, event.getX(), event.getY());
                    break;
                case "Polygon":
                    figure = new PolygonFigure((Polygon)et, event.getX(), event.getY());
                    break;
                default:
                    figure = null;
                    return;
            }
            if(event.isShiftDown()) figure.makePerfect();
            if(event.isAltDown()) figure.changeColor(color);
        });

        plane.setOnMouseDragged(event -> {
            mx = event.getX();
            my = event.getY();
            if(figure == null) return;
            if(!event.isControlDown()) figure.move(event.getX(), event.getY());
            else figure.rotate(event.getX(), event.getY());
        });

        plane.setOnMouseReleased(event -> {if(event.getButton() == MouseButton.PRIMARY) figure = null;});

        plane.setOnScroll(event ->{
            double sDY = event.getDeltaY();
            if(sDY == 0) return;
            double scaleX = event.isAltDown() ? 0 : SCALE * Math.abs(sDY) / sDY;
            double scaleY = event.isControlDown() ? 0 : SCALE * Math.abs(sDY) / sDY;

            EventTarget et  = event.getTarget();
            switch (et.getClass().getSimpleName()){
                case "Rectangle":
                    figure = new RectangleFigure((Rectangle)et, event.getX(), event.getY());
                    break;
                case "Ellipse":
                    figure = new EllipseFigure((Ellipse)et, event.getX(), event.getY());
                    break;
                case "Polygon":
                    figure = new PolygonFigure((Polygon)et, event.getX(), event.getY());
                    break;
                default:
                    figure = null;
                    return;
            }

            figure.resize(scaleX, scaleY);
        });
    }

    private void setRectangleActions(Pane plane){
        plane.setOnMousePressed(event -> {
            figure = new RectangleFigure(event.getX(), event.getY(), color);
            plane.getChildren().add(figure.getFigure());
        });
        plane.setOnMouseDragged(event -> {
            if(!event.isShiftDown()) figure.draw(event.getX(), event.getY());
            else{
                double dx = figure.x0 - event.getX();
                double dy = figure.y0 - event.getY();
                double side = Math.min(Math.abs(dx), Math.abs(dy));
                if(dx != 0 && dy != 0){
                    figure.draw(figure.getShiftedX(-side * dx / Math.abs(dx)), figure.getShiftedY(-side * dy / Math.abs(dy)));
                }
            }
        });
    }

    private void setCircleActions(Pane plane){
        plane.setOnMousePressed(event -> {
            figure = new EllipseFigure(event.getX(), event.getY(), color);
            plane.getChildren().add(figure.getFigure());
        });

        plane.setOnMouseDragged(event -> {
            if(!event.isShiftDown()) figure.draw(event.getX(), event.getY());
            else{
                double radius = Math.sqrt(Math.pow(figure.getDX(event.getX()), 2) + Math.pow(figure.getDY(event.getY()), 2));
                figure.draw(figure.getShiftedX(radius), figure.getShiftedY(radius));
            }
        });
    }

    private void setPolygonActions(Pane plane){

        //plane.setOnMouseDragExited(null);
        figure = new PolygonFigure();
        plane.getChildren().add(figure.getFigure());
        plane.setOnMousePressed(event -> {
            figure.draw(event.getX(), event.getY());
        });
        plane.setOnMouseDragged(null);
        plane.setOnMouseReleased(null);

        
    }
    
    private MenuBar createMenu(){
        MenuItem saveButton = new MenuItem("Save");
        MenuItem openButton = new MenuItem("Open");
        MenuItem helpButton = new MenuItem("Help");
        MenuItem docsButton = new MenuItem("Docs");
        MenuItem infoButton = new MenuItem("Info");
        
        //saveButton.setOnAction(event -> save(plane));
        helpButton.setOnAction(event -> displayHelp());

        infoButton.setOnAction(event -> displayInfo());

        Menu fileMenu = new Menu("File");
        fileMenu.getItems().addAll(saveButton, openButton, helpButton, docsButton, infoButton);
        

        MenuBar mainMenu = new MenuBar(fileMenu);
        mainMenu.setMinHeight(30);
        mainMenu.setLayoutX(5);
        mainMenu.setLayoutY(5);

        return mainMenu;
    }

    private void save(Pane plane){
        ObservableList<Node> figures = plane.getChildren();
        for(int i = 0; i < figures.size(); i++){
            //figures.get(i).toString()
        }
    }
    
    private void displayHelp(){
        VBox dialogVbox = new VBox(50);
        Scene dialogScene = new Scene(dialogVbox, dialogVbox.getWidth(), dialogVbox.getHeight());
        final Stage dialog = new Stage();

        dialog.initModality(Modality.APPLICATION_MODAL);
        dialogVbox.setAlignment(Pos.CENTER);

        TextArea text = new TextArea("""
        \"Cursor\" - Przesuwanie figur
        \"Cursor\" + CTRL - Obracanie
        \"Cursor\" + ALT  - Wypełnienie kolorem

        \"Prostokąt\"         - Tworzenie prostokąta
        \"Prostokąt\" + SHIFT - Tworzenie kwadratu

        \"Elipsa\"            - Tworzenie elipsy
        \"Elipsa\"    + SHIFT - Tworzenie koła

        \"Scroll\"            - Powiększanie/Zmniejszanie
        \"Scroll\"    + CTRL  - Powiększanie po X
        \"Scroll\"    + ALT   - Powiększanie po Y
        """);

        text.setFont(new Font("Monospaced", 12));
        //text.setFont(Font.font("Consolas", FontWeight.THIN, 12));

        dialogVbox.getChildren().add(text);
            
        dialog.setTitle("Info");
        dialog.setScene(dialogScene);
        dialog.show();

        Rectangle2D screenBounds = Screen.getPrimary().getBounds();
        dialog.setX((screenBounds.getWidth() - dialogVbox.getWidth())/2);
        dialog.setY((screenBounds.getHeight() - dialogVbox.getHeight())/2);
    }


    private void displayInfo(){
        VBox dialogVbox = new VBox(50);
        Scene dialogScene = new Scene(dialogVbox, dialogVbox.getWidth(), dialogVbox.getHeight());
        final Stage dialog = new Stage();

        dialog.initModality(Modality.APPLICATION_MODAL);
        dialogVbox.setAlignment(Pos.CENTER);
        dialogVbox.getChildren().add(new Text("""
        Autor: Michał Bortkiewicz
        Przeznaczenie: Program do malowania figur
        Nazwa: Paint V0.5
        """));
            
        dialog.setTitle("Info");
        dialog.setScene(dialogScene);
        dialog.show();

        Rectangle2D screenBounds = Screen.getPrimary().getBounds();
        dialog.setX((screenBounds.getWidth() - dialogVbox.getWidth())/2);
        dialog.setY((screenBounds.getHeight() - dialogVbox.getHeight())/2);
    }
}