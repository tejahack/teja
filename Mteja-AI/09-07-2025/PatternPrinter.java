public class PatternPrinter {

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

    public static void main(String[] args) {
        int rows = 5;

        printStars(rows);
        System.out.println();

        printIncreasingNumbers(rows);
        System.out.println();

        printRepeatedNumbers(rows);
    }
}
