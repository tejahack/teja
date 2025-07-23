public class obj 
{
    String name;
    String village;
    String mandal;
    String district;

    public obj(String name,String village,String mandal,String district)
    {
        this.name = name;
        this.village = village;
        this.mandal= mandal;
        this.district=district;
    }
    public void print()
    {
        System.out.println("name : " +this.name);
        System.out.println("village : " +this.village);
        System.out.println("mandal : " +this.mandal);
        System.out.println("district : " +this.district);
    }

    public static void main(String[] args) {
        obj  adress = new obj("teja","srirangapatnam","korukonda","east godavari");
        adress.print();
    }
}
