public class Point {
    public int x;
    public int y;

    Point(int x, int y){
        this.x = x;
        this.y = y;
    }

    Point(Point point){
        this.x = point.x;
        this.y = point.y;
    }

    @Override
    public String toString(){
        return "(" + x + ", " + y + ")";
    }

    @Override
    public boolean equals(Object o){
        if(o instanceof Point){
            Point point = (Point)o;
            if(point.x == x && point.y == y) return true;
        }
        return false;
    }
}
