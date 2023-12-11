import javafx.scene.paint.Color;
import javafx.scene.shape.Ellipse;
import javafx.scene.shape.Shape;

public class EllipseFigure extends Figure {
    private Ellipse figure;


    EllipseFigure(double x, double y, Color color){
        this(x, y, 0, 0, 0, color);
    }

    EllipseFigure(Ellipse figure, double px, double py){
        super(figure.getCenterX(), figure.getCenterY(), px, py);
        this.figure = figure;
    }

    EllipseFigure(double x, double y, double radiusX, double radiusY, double angle, Color color){
        super(x, y, x, y);
        this.figure = new Ellipse(x0, y0, radiusX, radiusY);
        figure.setRotate(angle);
        figure.setFill(color);
        figure.setStroke(Color.BLACK);
        figure.setStrokeWidth(5);
    }


    @Override
    public void draw(double x1, double y1) {
        figure.setRadiusX(Math.abs(x0 - x1));
        figure.setRadiusY(Math.abs(y0 - y1));
    }

    @Override
    public void move(double x1, double y1){
        x0 += x1 - px;
        y0 += y1 - py;
        px = x1;
        py = y1;
        figure.setCenterX(x0);
        figure.setCenterY(y0);
    }

    @Override
    public void rotate(double x1, double y1) {
        figure.setRotate(Math.toDegrees(Math.atan2(y1 - figure.getCenterY(), x1 - figure.getCenterX())));
    }

    @Override
    public void resize(double scaleX, double scaleY){
        figure.setRadiusX(figure.getRadiusX() * (1 + scaleX));
        figure.setRadiusY(figure.getRadiusY() * (1 + scaleY));
    }

    @Override
    public void changeColor(Color color){figure.setFill(color);}

    @Override
    public void makePerfect(){
        double avg = (figure.getRadiusX() + figure.getRadiusY())/2;
        figure.setRadiusX(avg);
        figure.setRadiusY(avg);
    }

    @Override
    public Shape getFigure() {
        return figure;
    }

    @Override
    public String toString(){
        return "Ellipse " + figure.getCenterX() + " " + figure.getCenterY() + figure.getRadiusX() + " " + figure.getCenterY() + " " + figure.getRotate() + " " + figure.getFill();
    }

}
