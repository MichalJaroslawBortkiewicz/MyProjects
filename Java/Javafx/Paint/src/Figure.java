import javafx.scene.paint.Color;
import javafx.scene.shape.Shape;

abstract public class Figure {
    public double x0, y0;
    public double px, py;

    Figure(double x0, double y0, double px, double py){
        this.x0 = x0;
        this.y0 = y0;
        this.px = px;
        this.py = py;
    }

    public void setPivot(double px, double py){
        this.px = px;
        this.py = py;
    }

    public void printData(){
        System.out.println("x0 = " + x0 + ", y0 = " + y0 + ", px = " + px + ", py = " + py + "");
    }

    public double getDX(double x){return x - x0;}
    public double getDY(double y){return y - y0;}
    public double getShiftedX(double shiftX){return x0 + shiftX;}
    public double getShiftedY(double shiftY){return y0 + shiftY;}

    public abstract void draw(double x1, double y1);
    public abstract void move(double x1, double y1);
    public abstract void rotate(double x1, double y1);
    public abstract void resize(double scaleX, double scaleY);
    public abstract void changeColor(Color color);
    public abstract void makePerfect();
    public abstract Shape getFigure();

    @Override
    public abstract String toString();
}
