public class arthematic {
    int a=20,b=40,c;
     public void add()
    {
        c=a+b;
        System.out.println("addition : "+c);
    }
    public void sub()
    {
        c=a-b;
        System.out.println("subtraction : "+c);
    }
    public void mul()
    {
        c=a*b;
        System.out.println("multiplilcation : "+c);
    }
    public void div()
    {
        c=a/b;
        System.out.println("division :"+c);
    }
    public static void main(String[] args) {
        arthematic k=new arthematic();
        k.add();
        k.sub();
        k.mul();
        k.div();
    }
}
