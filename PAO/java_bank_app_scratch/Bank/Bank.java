package Bank;

import java.util.ArrayList;
import Customer.Customer;

public class Bank {
    ArrayList<Customer> customers = new ArrayList<Customer>();
    private String name = null;
    
    public Bank(String name) { this.name = name; }

    public void addCustomer(Customer customer) {
        customers.add(customer);
    }

    public Customer getCustomer(int account) {
        return customers.get(account);
    }
    
    public ArrayList<Customer> getCustomers(){
        return customers;
    }

    public String basicInfo(){ return name; }



    @Override
    public String toString(){
            return name;}
        
}