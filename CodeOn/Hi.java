import java.util.Scanner;

public class Hi{
	public static void main(String args[]){
		Scanner myInpt = new Scanner(System.in); 
		int name = myInpt.nextInt();
		int lastname = myInpt.nextInt();
		int result = (name + lastname);
		System.out.println("My sum is " + result);
	}
}
