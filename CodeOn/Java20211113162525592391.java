import java.util.Scanner;

public class Java20211113162525592391{
    public static void main(String args[]){
        Scanner myInpt = new Scanner(System.in); 
        int name = myInpt.nextInt();
        int lastname = myInpt.nextInt();
        int result = (name + lastname);
        System.out.println("My name is " + result);
    }
}