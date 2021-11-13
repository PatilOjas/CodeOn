import java.util.Scanner;

class Hi{
    public static void main(String args[]){
        Scanner myInpt = new Scanner(System.in); 
        int name = myInpt.nextInt();
        int lastname = myInpt.nextInt();
        int result = (name + lastname);
        System.out.println("My name is " + result);
    }
}