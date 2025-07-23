import java.util.Scanner;

class TEJA
{
    int a=10,b=60,c,j,d=70,k=1,g,r_no=0,on,x[]={1,2,3,4,5,6,7,8,9,10},y[]={2,5,6,4,7,8,9,3,10,1},z[]=new int[10],key=10;
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
    public void num()
    {
       if(a>b)
       {
        if(a>d)
        {
            System.out.println("Biggest Of Three Numbers");
            System.out.println("a is biggest");
        }
        else
        {
            System.out.println("Biggest Of Three Numbers");
            System.out.println("c is biigest");
        }
       } 
       else
       {
            if(b>d)
            {
                System.out.println("Biggest Of Three Numbers");
                System.out.println("b is biggest");
            }
            else
            {
                System.out.println("Biggest Of Three Numbers");
                System.out.println("c is biggest");
            }
       }
    }
     public void num2()
    {
       if(a>b)
       { 
        System.out.println("Biggest Of Two Numbers");
        System.out.println("a is biggest");      
       } 
       else
       {
            System.out.println("Biggest Of Two Numbers");
            System.out.println("b is biggest");

       }
    }
    public void for_l()
    {
        System.out.println("Printing numbers from 1 to 100 using for loop");
        for(int i=1;i<10;i++)
        { 
            System.out.println(i);
        }
    }
     public void while_1()
    {
        System.out.println("Printing numbers from 1 to 100 using while loop");
        while(j<101)
        { 
            System.out.println(j);
            j++;
        }
    }
    public void arr_2()
    {
        System.out.print("printing the array values : ");
        for (int i = 0; i < 10; i++) 
        {
            System.out.println(z[i]);
        }
    }
    public void do_while()
    {
        do
        {
            System.out.println(k);
            k++;
        }while(k<100);
    }
    public void arm_strong()
    {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter a number : ");
        int neo = sc.nextInt();
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
    public void arr_3()
    {
        System.out.println("Addition Of Two Arrays Is :");

        for (int j = 0; j < 10; j++) 
        {
            
            System.out.println(z[j] = x[j] + y[j]);
        }
    }
    public void forlin()
    {
        for(int i=0;i<10;i++)
        {
            if(x[i]==key)
            {
                System.out.println("the key element found");
                break;
            }
            else
            {
                System.out.println("the key element not found");
            }
        }
    }
     public static void printStars(int rows) {
        for (int i = 1; i <= rows; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print("*");
            }
            System.out.println();
        }
    }

    public static void printIncreasingNumbers(int rows) {
        for (int i = 1; i <= rows; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print(j);
            }
            System.out.println();
        }
    }

    public static void printRepeatedNumbers(int rows) {
        for (int i = 1; i <= rows; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print(i);
            }
            System.out.println();
        }
    }
    public void multi()
    {
        System.out.println("Multiplication Table of 4:");

      for(int var1 = 1; var1 <= 10; ++var1) {
         System.out.println("4 x " + var1 + " = " + 4 * var1);
      }
    }
    public static void switchu()
    {
      byte var1 = 1;
      switch (var1) {
         case 1:
            System.err.println("sunday");
            break;
         case 2:
            System.out.println("monday");
            break;
         case 3:
            System.out.println("tuesday");
            break;
         case 4:
            System.out.println("wednesday");
            break;
         case 5:
            System.out.println("thursday");
            break;
         case 6:
            System.out.println("friday");
            break;
         case 7:
            System.out.println("saturday");
            break;
         default:
            System.out.println("You Entered wrong Option Please Try Again");
      }

   }
    public static void main(String args[])
    {
        TEJA k=new TEJA();
        System.out.println("1 . addition");  
        System.out.println("2 . subtraction");  
        System.out.println("3 . multiplication");  
        System.out.println("4 . division");  
        System.out.println("5 . even numbers");  
        System.out.println("6 . odd numbers");  
        System.out.println("7 . biigest of three numbers");   
        System.out.println("8 . biggest of two numbers");
        System.out.println("9 . for loop");
        System.out.println("10. while loop");
        System.out.println("11. do while");
        System.out.println("12. palindrome number");
        System.out.println("13. printing array elements");
        System.out.println("14. Addition Of Two Arrays ");
        System.out.println("15. Searching a key element in an array");
        System.out.println("16. printing stars");
        System.out.println("17. printing by increasing numbers");
        System.out.println("18. printing repeated numbers");
        System.out.println("19. 4th table program");
        System.out.println("20. fiding the day by using switch class");
        Scanner inputScanner = new Scanner(System.in);
        System.out.println("Enter a number : ");
        String number = inputScanner.nextLine();
        switch(number)
        {
            case "1":
                k.add();
                break;
            case "2":
                k.sub();
                break;
            case "3":
                k.mul();
                break;
            case "4":
                k.div();
                break;
            case "5":
                k.for_demo();
                break;
            case "6":
                k.for_dem();
                break;
            case "7":
                k.num();
                break;
            case "8":
                k.num2();
                break;
            case "9":
                 k.for_l();
                break;
            case "10":
                k.while_1();
                break;
            case "11":
                k.do_while();
                break;
            case"12":
                k.arm_strong();
                break;
            case "13":
                k.arr_2();
                break;
            case "14":
                k.arr_3();
                break;   
            case "15":
                k.forlin();
                break; 
            case "16":
                k.printStars(5);
                break;
            case "17":
                k.printIncreasingNumbers(5);
                break;
            case "18":
                k.printRepeatedNumbers(5);
                break;
            case "19":
                k.multi();
                break;

            default:
            System.out.println("You Entered wrong Option Please Try Again");
            break;
        }
    }
}