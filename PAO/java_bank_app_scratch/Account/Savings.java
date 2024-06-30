package Account;
public class Savings extends Account{
    private static String accountType = "Savings";
    
    public Savings(double initialDeposit){
        this.setBalance(initialDeposit);
        this.checkInterest(0);
    }
    
    public Savings(int Accno, double balance) {
        super(Accno, balance);
    }
    


    @Override
    public String toString(){
        return "Account Type: " + accountType + " Account\n" +
                "Account Number: " + this.getAccountNumber() + "\n" +
                "Balance: " + this.getBalance() + "\n" + 
                "Interest Rate: " + this.getInterest() + "%\n";
    }
}