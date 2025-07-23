

public class palindrome {
     int neo=111,on,g,r_no;
     public void palindrome()
    
    {
         
        on = neo;
        while(neo!=0)
        {
            g= neo%10;
            r_no=g+(r_no*10);
            neo=neo/10;
        }
        if (r_no==on) 
        {
            System.out.println("you entered palindrome number");    
        }
        else
        {
            System.out.println("you entered number is not palindrome");
        }
    }
    public static void main(String[] args) {
        palindrome p=new palindrome();
        p.palindrome();
    }
}
