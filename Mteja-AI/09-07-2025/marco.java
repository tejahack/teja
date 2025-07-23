public class marco
{

    public static void main(String[] args) {
        int marks = 65;  // Change this value to test different results

        if (marks >= 70 && marks <= 80) {
            System.out.println("Excellent");
        } else if (marks >= 60 && marks < 70) {
            System.out.println("Very Good");
        } else if (marks >= 50 && marks < 60) {
            System.out.println("Good");
        } else if (marks >= 35 && marks < 50) {
            System.out.println("Pass");
        } else if (marks >= 0 && marks < 35) {
            System.out.println("Fail");
        } else {
            System.out.println("Invalid marks");
        }
    }
}
