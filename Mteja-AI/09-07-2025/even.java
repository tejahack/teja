public class even {
     public void for_demo()
    {
        for(int i=1;i<100;i++)
        {
            if(i%2==0)
            {
                System.out.println("even numbers : "+i);               
            }
        }
    }
    public void for_dem()
    {
        for(int i=1;i<100;i++)
        {
            if(i%2!=0)
            {   
                System.out.println("odd numbers : "+i);
            }
        }
    } 
    public static void main(String[] args) {
        even t=new even();
        t.for_demo();
        t.for_dem();
    }   
}
