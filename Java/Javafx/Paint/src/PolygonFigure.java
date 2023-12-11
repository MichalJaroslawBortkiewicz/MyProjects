import javafx.collections.ObservableList;
import javafx.scene.paint.Color;
import javafx.scene.shape.Polygon;
import javafx.scene.shape.Shape;

public class PolygonFigure extends Figure {
    private Polygon figure;

    PolygonFigure(){
        super(0,0,0,0);
        this.figure = new Polygon();
        figure.setFill(Color.TRANSPARENT);
        figure.setStroke(Color.BLACK);
        figure.setStrokeWidth(5); 
    }

    PolygonFigure(Polygon figure, double px, double py){
        super(figure.getLayoutX(), figure.getLayoutY(), px, py);
        this.figure = figure;
        findCenter();
    }

    private void findCenter(){
        ObservableList<Double> points = figure.getPoints();
        for(int i = 0; i < points.size(); i += 2){
            x0 = (x0 * i / 2 + points.get(i)) / (i / 2 + 1);
            y0 = (y0 * i / 2 + points.get(i + 1)) / (i / 2 + 1);
        }
    }

    @Override
    public void draw(double x1, double y1) {
        int nop = figure.getPoints().size()/2;
        x0 = (x0 * nop + x1) / (nop + 1);
        y0 = (y0 * nop + y1) / (nop + 1);
        figure.getPoints().addAll(new Double[]{x1, y1});
    }

    @Override
    public void move(double x1, double y1) {
        x0 += x1 - px;
        y0 += y1 - py;
        px = x1;
        py = y1;
        figure.setLayoutX(x0);
        figure.setLayoutY(y0);
    }

    @Override
    public void rotate(double x1, double y1) {
        figure.setRotate(Math.toDegrees(Math.atan2(y1 - y0, x1 - x0)));
    }

    @Override
    public Shape getFigure() {
        return figure;
    }

    @Override
    public void resize(double scaleX, double scaleY) {
        ObservableList<Double> points = figure.getPoints();
        for(int i = 0; i < points.size(); i += 2){
            double x = points.get(i);
            double y = points.get(i + 1);

            figure.getPoints().set(i, x - scaleX * (x - x0));
            figure.getPoints().set(i + 1, y - scaleY * (y - y0));
        }
    }

    @Override
    public void changeColor(Color color) {
        figure.setFill(color);
    }

    @Override
    public void makePerfect() {}

    @Override
    public String toString(){
        return "Polygon " + figure.getLayoutX() + " " + figure.getLayoutY() + " " + figure.getPoints() + " " + figure.getRotate() + " " + figure.getFill();
    }
}