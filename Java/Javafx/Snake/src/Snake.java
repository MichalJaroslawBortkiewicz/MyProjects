import java.util.ArrayList;

public class Snake {
    private Point apple;
    private ArrayList<Point> snake;
    private int width;
    private int height;

    Snake(int width, int height){
        this.width = width;
        this.height = height;

        snake = new ArrayList<Point>();
        snake.add(0, new Point(0,0));
        snake.add(0, new Point(1,0));
        snake.add(0, new Point(2,0));
        snake.add(0, new Point(3,0));
        snake.add(0, new Point(4,0));
        genNewApple();
    }

    public void move(DirectionEnum direction) throws GameOverException{
        Point newHead = new Point(snake.get(0));
        switch(direction){
            case UP:
                newHead.y--;
                break;
            case DOWN:
                newHead.y++;
                break;
            case LEFT:
                newHead.x--;
                break;
            case RIGHT:
                newHead.x++;
                break;
        }

        if((snake.contains(newHead) && newHead != snake.get(snake.size() - 1))|| newHead.y == -1 || newHead.y == height || newHead.x == -1 || newHead.x == width){
            throw new GameOverException();
        }

        snake.add(0, newHead);
        if(apple.equals(newHead)) genNewApple();
        else snake.remove(snake.size() - 1);
    }

    private void genNewApple(){
        while(true){
            apple = new Point((int)Math.round(Math.random() * (width - 1)), (int)Math.round(Math.random() * (height - 1)));
            if(!snake.contains(apple)) break;
        }
    }

    public ArrayList<Point> getPoints(){
        return snake;
    }

    public int getLength(){
        return snake.size();
    }

    public Point getApple(){
        return apple;
    }
}
