import java.util.Scanner;

public class Hi{
	public static void main(String args[]){
		Scanner myInpt = new Scanner(System.in); 
		int a = myInpt.nextInt();
		int b = myInpt.nextInt();
		// int a = 5;
		// int b = 4;
		int result = (a + b);
		System.out.println("My sum is " + result);
	}
}
