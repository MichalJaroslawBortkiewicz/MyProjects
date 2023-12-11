import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import javafx.scene.shape.Shape;

public class RectangleFigure extends Figure{
    private Rectangle figure;

    RectangleFigure(double x, double y, Color color){
        this(x, y, 0, 0, 0, color);
    }

    RectangleFigure(Rectangle figure, double px, double py){
        super(figure.getX(), figure.getY(), px, py);
        this.figure = figure;
    }

    RectangleFigure(double x, double y, double width, double height, double angle, Color color){
        super(x, y, x, y);
        this.figure = new Rectangle(x0, y0, width, height);
        figure.setRotate(angle);
        figure.setFill(color);
        figure.setStroke(Color.BLACK);
        figure.setStrokeWidth(5);
    }

    @Override
    public void draw(double x1, double y1) {
        figure.setWidth(Math.abs(x0 - x1));
        figure.setHeight(Math.abs(y0 - y1));
        figure.setX(Math.min(x0, x1));
        figure.setY(Math.min(y0, y1));
    }

    @Override
    public void move(double x1, double y1){
        x0 += x1 - px;
        y0 += y1 - py;
        px = x1;
        py = y1;
        figure.setX(x0);
        figure.setY(y0);
    }

    @Override
    public void rotate(double x1, double y1) {
        figure.setRotate(Math.toDegrees(Math.atan2(y1 - y0 - figure.getHeight()/2, x1 - x0 - figure.getWidth()/2)));
    }

    @Override
    public void resize(double scaleX, double scaleY){
        figure.setX(getShiftedX(-figure.getWidth() * scaleX / 2));
        figure.setY(getShiftedY(-figure.getHeight() * scaleY / 2));
        figure.setWidth(figure.getWidth() * (1 + scaleX));
        figure.setHeight(figure.getHeight() * (1 + scaleY));
    }

    @Override
    public void changeColor(Color color){figure.setFill(color);}

    @Override
    public void makePerfect(){
        double avg = (figure.getWidth() + figure.getHeight())/2;
        resize(avg / figure.getWidth() - 1, avg / figure.getHeight() - 1);
    }

    @Override
    public Shape getFigure() {
        return figure;
    }

    @Override
    public String toString(){
        return "Rectangle " + figure.getX() + " " + figure.getY() + " " + figure.getWidth() + " " + figure.getWidth() + " " + figure.getRotate() + " " + figure.getFill();
    }
}
