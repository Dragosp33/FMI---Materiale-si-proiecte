import Account.Account;
import Account.Savings;
import Account.Checking;

import java.sql.*;
import Actiuni.InvalidAccountTypeException;
import sql.*;
import Actiuni.*;

import Bank.Bank;
import Customer.Customer;

/*  In pachetul account sunt fisierele care tin de un cont bancar, indiferent de tipul lui */
// In Actiuni avem erorile in cazul unui tip de date invalid 
// iar pachetele Bank si Customer contin fiecare un singur fisier, cel care reprezinta clasa

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

import java.io.*;
import java.util.stream.Collectors;


import java.text.SimpleDateFormat;  
import java.util.Date;  


public class Menu {
    
    ArrayList<Savings> saves = new ArrayList<Savings>();
    ArrayList<Checking> checks = new ArrayList<Checking>();
    ArrayList<Customer> customers = new ArrayList<Customer>();
    FileWriter x;
    

    // Atributele de mai sus sunt de la etapa a 2a, nu au mai fost folosite in etapa 3,
    // dar le-am pastrat ca sa pot pastra si metodele de la etapa a 2a, sa para un proiect mai mare :))



    //Instance Variables
    ArrayList<Bank> banci = new ArrayList<Bank>();
    boolean exit, exit2;
    MysqlCon m = new MysqlCon();
    //initializare obiect nou mysqlcon;

    public  Menu() throws IOException{
    this.banci = new ArrayList<Bank>();
    this.saves = new ArrayList<Savings>();
    this.checks = new ArrayList<Checking>();
    this.customers = new ArrayList<Customer>();
    this.x = new FileWriter("data/report.csv");}
   
    

    public static void main(String[] args) {

        Menu menu;
        try {
            menu = new Menu();
            menu.runMenu();
        } catch (IOException e) {
            // TODO Auto-generated catch block

            e.printStackTrace();
        }
        
        
       
    }

    public void runMenu() {
        printHeader();
        

        while (!exit) {
            printMenu();
            int choice = getMenuChoice1();
            performAction1(choice);
        }
    }

    public void runMenu2(Bank bank) {
        System.out.println("you're working on bank: " + bank.basicInfo());
        while(!exit2) {
            printMenu2();
            int choice = getMenuChoice();
            performAction(choice, bank);
        }
    }

    private void printHeader() {
        System.out.println("+-----------------------------------+");
        System.out.println("|     Polifronie Dragos-Constantin  |");
        System.out.println("|              Bank App             |");
        System.out.println("+-----------------------------------+");
    }

    private void printMenu() {
        displayHeader("Please make a selection");
     
        System.out.println("1) Add banks");
        System.out.println("2) Choose/Switch banks");
        System.out.println("3) File Reading");
        System.out.println("4) Introdu locatia fisierului destinat raporturilor (actiuni,timestamp)");
        System.out.println("5) JDBC connect");
        System.out.println("0) Exit");
    }

    private void printMenu2() {
        displayHeader("Please make a selection");
         System.out.println("1) Create a new Account");
         System.out.println("2) Make a deposit");
         System.out.println("3) Make a withdrawal");
         System.out.println("4) List account balance");
        
         System.out.println("5) Read information from file");
         System.out.println("6) Delete account");
    }

    private int getMenuChoice() {
        Scanner keyboard = new Scanner(System.in);
        int choice = -1;
        do {
            System.out.print("Enter your choice: ");
            try {
                choice = Integer.parseInt(keyboard.nextLine());
            } catch (NumberFormatException e) {
                System.out.println("Invalid selection. Numbers only please.");
            }
            if (choice < 0 || choice > 6) {
                System.out.println("Choice outside of range. Please chose again.");
            }
        } while (choice < 0 || choice > 6);
        return choice;
    }


    private int getMenuChoice1() {
        Scanner keyboard = new Scanner(System.in);
        int choice = -1;
        do {
            System.out.print("Enter your choice: ");
            try {
                choice = Integer.parseInt(keyboard.nextLine());
            } catch (NumberFormatException e) {
                System.out.println("Invalid selection. Numbers only please.");
            }
            if (choice < 0 || choice > 5) {
                System.out.println("Choice outside of range. Please chose again.");
            }
        } while (choice < 0 || choice > 5);
        return choice;
    }

    private void performAction1(int choice) {
        switch (choice) {
            case 0:
                System.out.println("Thank you for using our application.");
                if (this.m.getConnection() != null) {
                    this.m.close_con();

                    //Inchidere conexiune;
                } 
                
                System.exit(0);
                break;
            case 1: {
                try {
                    addBank();
                } catch ( Exception e) {
                    System.out.println(e);
                }
            }
            break;
            case 2:
                int banca = switchBanks(banci);
                if(banca != -1){
                runMenu2(banci.get(banca));
                break;}
                break;
            case 3:
                System.out.println("Intrare in mod citire:");
                Scanner keyboard = new Scanner(System.in);
                int choice3 = 1;
                while(choice3 > 0){
                        System.out.println("1) Citire fisier banci");
                        System.out.println("2) Citire fisier conturi savings");
                        System.out.println("3) Citire fisier conturi check");
                        System.out.println("4) Citire fisier clienti");
                        choice3 = Integer.parseInt(keyboard.nextLine());
                            switch(choice3){
                            case 1:
                                citireBanci();
                                break;
                            case 2:
                                citireConturi("savings");
                                break;
                            case 3:
                                citireConturi("checkings");
                                break;
                            case 4:
                                CitireCustomers();
                                break;
                            default:
                                System.out.println("Going back to main menu");
                                break;
                            
                        }
                
                }
                break;
            case 4:
                System.out.println("First of all, insert the name for the report file: (unde vor fi scrise actiunile+timestamp)");
                Scanner keyboard2 = new Scanner(System.in);
                String llsd = keyboard2.nextLine();
                System.out.println("esti sigur ca in " + llsd );
                try{InitFile(llsd);}
                catch(Exception e){System.out.println("Se pare ca fisierul " + llsd + "nu poate fi deschis.\n");}
                break;
            
            case 5:

                //aici se incarca toate datele din baza de date, mai intai cele din tabela banks, 
                // urmand ca pentru fiecare banca sa se citeasca si sa se introduca in obiectul meniu
                // datele corespunzatoare (clienti, conturi);

                System.out.println("Se incearca conectarea la bd");
                try{this.m.connection(); System.out.println("conectare reusita, se vor incarca datele!");
                    ResultSet rs = this.m.selectAllBanks();
                    if (rs != null){
                        while(rs.next()){
                            this.banci.add(new Bank(rs.getString(1)));
                        }
                    }
                    System.out.println("Bancile au fost incarcate!");

                    if(this.banci.size() > 0){

                        for(int i=0; i<this.banci.size(); i++){
                        rs = this.m.join_Customers_Accounts_Banks(banci.get(i).basicInfo());
                        if (rs != null){
                        while(rs.next()){ 
                            int acc_number = rs.getInt(1);
                            int balance = rs.getInt(2);
                            String acctype = rs.getString(4);
                            String ssid = rs.getString(6);
                            String firstName = rs.getString(7);
                            String lastName = rs.getString(8);
                            Account account;

                            if (acctype.toUpperCase().equals("SAVINGS")) {
                            account = new Savings(acc_number, balance);
                            
                            }else{
                                account = new Checking(acc_number, balance);
                            }
                            Customer c= new Customer(firstName, lastName, ssid, account);
                            this.banci.get(i).addCustomer(c);
                            

                        }

                        }
                  


                    }
                }
                Account.set_accNo(this.m.getMaxRecords());
                // Iau maximul din tabela conturi pentru a pastra acelasi acc_number la crearea unui
                // nou cont, deoarece am pus ca acc_number (in clasa account ) un integer static care se va autoincrementa
                // la crearea unui nou obiect ce deriva din clasa account;

                }
                catch(Exception e){System.out.println("Nu s-a reusit conectarea la bd");}
                
                
                break;
            
            default:
                System.out.println("Unknown error has occured.");
        } 
    }

    

    private void performAction(int choice, Bank bank) {
        switch (choice) {
            case 0:
                exit2 = true;
                break;
            case 1: {
                try {
                    createAnAccount(bank);
                } catch (InvalidAccountTypeException ex) {
                    System.out.println("Account was not created successfully.");
                }
            }
            break;
            case 2:
                makeADeposit(bank);
                break;
            case 3:
                makeAWithdrawal(bank);
                break;
            case 4:
                listBalances(bank);
                break;
            case 5:
                Scanner keyboard = new Scanner(System.in);
                
                String s = askQuestion("Please enter an account type: ", Arrays.asList("checking", "savings"));
                citireConturi(s);
                break;
            case 6:
                DeleteAccount(bank);
                break;
            default:
                System.out.println("Unknown error has occured.");
        }
    }

    private String askQuestion(String question, List<String> answers) {
        String response = "";
        Scanner keyboard = new Scanner(System.in);
        boolean choices = ((answers == null) || answers.size() == 0) ? false : true;
        boolean firstRun = true;
        do {
            if (!firstRun) {
                System.out.println("Invalid selection. Please try again.");
            }
            System.out.print(question);
            if (choices) {
                System.out.print("(");
                for (int i = 0; i < answers.size() - 1; ++i) {
                    System.out.print(answers.get(i) + "/");
                }
                System.out.print(answers.get(answers.size() - 1));
                System.out.print("): ");
            }
            response = keyboard.nextLine();
            firstRun = false;
            if (!choices) {
                break;
            }
        } while (!answers.contains(response));
        return response;
    }

    private double getDeposit(String accountType) {
        Scanner keyboard = new Scanner(System.in);
        double initialDeposit = 0;
        Boolean valid = false;
        while (!valid) {
            System.out.print("Please enter an initial deposit: ");
            try {
                initialDeposit = Double.parseDouble(keyboard.nextLine());
            } catch (NumberFormatException e) {
                System.out.println("Deposit must be a number.");
            }
            if (accountType.equalsIgnoreCase("checking")) {
                if (initialDeposit < 100) {
                    System.out.println("Checking accounts require a minimum of $100 dollars to open.");
                } else {
                    valid = true;
                }
            } else if (accountType.equalsIgnoreCase("savings")) {
                if (initialDeposit < 50) {
                    System.out.println("Savings accounts require a minimum of $50 dollars to open.");
                } else {
                    valid = true;
                }
            }
        }
        return initialDeposit;
    }

    private void createAnAccount(Bank bank) throws InvalidAccountTypeException {
        displayHeader("Create an Account");
        //Get account information
        String accountType = askQuestion("Please enter an account type: ", Arrays.asList("checking", "savings"));
        String firstName = askQuestion("Please enter your first name: ", null);
        String lastName = askQuestion("Please enter your last name: ", null);
        String ssn = askQuestion("Please enter your social security number: ", null);
        double initialDeposit = getDeposit(accountType);
        //We can create an account now;
        Account account;
        if (accountType.equalsIgnoreCase("checking")) {
            account = new Checking(initialDeposit);

            try {
                WriteFile("S-a creat contul de checking " + account.getAccountNumber());
            } catch (IOException e) {
               
                System.out.println("se pare ca nu s-a putut deschide fisierul!");
               
            }



        } else if (accountType.equalsIgnoreCase("savings")) {
            account = new Savings(initialDeposit);

            try {
                WriteFile("S-a creat contul de checking " + account.getAccountNumber());
            } catch (IOException e) {
               
                System.out.println("se pare ca nu s-a putut deschide fisierul!");
               
            }


        } else {
            throw new InvalidAccountTypeException();
        }
        Customer customer = new Customer(firstName, lastName, ssn, account);


        this.m.insert_account(account.getBalance(), accountType, bank.basicInfo());
        this.m.insert_customer(ssn, firstName, lastName, account.getAccountNumber());

        bank.addCustomer(customer);
    }

    private double getDollarAmount(String question) {
        Scanner keyboard = new Scanner(System.in);
        System.out.print(question);
        double amount = 0;
        try {
            amount = Double.parseDouble(keyboard.nextLine());
        } catch (NumberFormatException e) {
            amount = 0;
        }
        return amount;
    }

    private void makeADeposit(Bank bank) {
        displayHeader("Make a Deposit");
        int account = selectAccount(bank);
        if (account >= 0) {
            double amount = getDollarAmount("How much would you like to deposit?: ");
            bank.getCustomer(account).getAccount().deposit(amount);
            int accno = bank.getCustomer(account).getAccount().getAccountNumber();
            double balance = bank.getCustomer(account).getAccount().getBalance();
            this.m.update_balance(accno, balance);

            try {
                WriteFile("S-a facut o depunere de  " + amount + "din contul" + bank.getCustomer(account).getAccount().getAccountNumber());
            } catch (IOException e) {
               
                System.out.println("se pare ca nu s-a putut deschide fisierul!");
               
            }


        }
    }

    private void makeAWithdrawal(Bank bank) {
        displayHeader("Make a Withdrawal");
        int account = selectAccount(bank);
        if (account >= 0) {
            double amount = getDollarAmount("How much would you like to withdraw?: ");
            bank.getCustomer(account).getAccount().withdraw(amount);
            int accno = bank.getCustomer(account).getAccount().getAccountNumber();
            double balance = bank.getCustomer(account).getAccount().getBalance();
            this.m.update_balance(accno, balance);

            try {
                WriteFile("S-a facut o retragere de  " + amount + "din contul" + bank.getCustomer(account).getAccount().getAccountNumber());
            } catch (IOException e) {
               
                System.out.println("se pare ca nu s-a putut deschide fisierul!");
               
            }


        }
        
    }


    private void DeleteAccount(Bank bank){
        displayHeader("Deleting Account.. This will automically delete the account and the customer associated with it");
        int account = selectAccount(bank);
        
        if (account >= 0) {
            
            int accno = bank.getCustomer(account).getAccount().getAccountNumber();
            String answer = askQuestion("Are you sure you want to delete this account?", Arrays.asList("yes", "no"));
            if (answer.equalsIgnoreCase("yes")){
                bank.getCustomers().remove(account);
                
                this.m.delete_account(accno);
                System.out.println("Contul a fost sters!");
            }
            else { return;}
            // iesire din functie** daca nu se raspunde cu da la intrebarea "vrei sa stergi sigur contul?"
        }

    }


    private void listBalances(Bank bank) {
        displayHeader("List Account Details");
        int account = selectAccount(bank);
        if (account >= 0) {
            displayHeader("Account Details");
            System.out.println(bank.getCustomer(account).getAccount());
        }
    }
    
    private void displayHeader(String message){
        System.out.println();
        int width = message.length() + 6;
        StringBuilder sb = new StringBuilder();
        sb.append("+");
        for(int i = 0; i < width; ++i){
            sb.append("-");
        }
        sb.append("+");
        System.out.println(sb.toString());
        System.out.println("|   " + message + "   |");
        System.out.println(sb.toString());
    }

    private int selectAccount(Bank bank) {
        Scanner keyboard = new Scanner(System.in);
        ArrayList<Customer> customers = bank.getCustomers();
        if (customers.size() <= 0) {
            System.out.println("No customers at your bank.");
            return -1;
        }
        System.out.println("Select an account:");
        for (int i = 0; i < customers.size(); i++) {
            System.out.println("\t" + (i + 1) + ") " + customers.get(i).basicInfo());
        }
        int account;
        System.out.print("Please enter your selection: ");
        try {
            account = Integer.parseInt(keyboard.nextLine()) - 1;
        } catch (NumberFormatException e) {
            account = -1;
        }
        if (account < 0 || account > customers.size()) {
            System.out.println("Invalid account selected.");
            account = -1;
        }
        return account;


    }

 
    
    private int switchBanks(ArrayList<Bank> banks){
        exit2 = false;
        Scanner keyboard = new Scanner(System.in);
        
        if (banks.size() <= 0) {
            System.out.println("No banks in your bank app.");
            return -1;
        }
        System.out.println("Select a bank:");
        for (int i = 0; i < banci.size(); i++) {
            System.out.println("\t" + (i + 1) + ") " + banci.get(i).basicInfo());
        }
        int account;
        System.out.print("Please enter your selection: ");
        try {
            account = Integer.parseInt(keyboard.nextLine()) - 1;
        } catch (NumberFormatException e) {
            account = -1;
        }
        if (account < 0 || account > banci.size()) {
            System.out.println("Invalid bank selected.");
            account = -1;
        }
        return account;

    }

    private void addBank(){
        String name = askQuestion("Please enter bank name: ", null);
        Bank bank = new Bank(name);
        banci.add(bank);
        this.m.insert_bank(name);

        try {
            WriteFile("A fost adaugata banca: " +bank.basicInfo());
        } catch (IOException e) {
           
            System.out.println("se pare ca nu s-a putut deschide fisierul!");
           
        }
       
    }

    
 /*   private void openFile(String fis, BufferedReader reader) throws InvalidFileException{
        try {
            reader = new BufferedReader(new FileReader(fis));
            
        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            throw new InvalidFileException();
        }
        
    }*/

    private void citireBanci(){
        String fis = askQuestion("Please enter file path for bank file: (data/banks.csv) ", null);
        
        try {
        
            BufferedReader csvReader = new BufferedReader(new FileReader(fis));
           
            
             String row = csvReader.readLine();
    
    
             while ( row != null) {
              row = csvReader.readLine();
              if(row == null) { break;}
              String[] data = row.split(",");
              Bank b = new Bank(data[1]);
              
              banci.add(b);
              
    
            }
    
        }catch(IOException e ){
            System.out.println("File for banks not found, try again.");
        }

        for(Bank b : banci) {
            System.out.println(b);
        }

    }

    private void citireConturi(String type) {
    String fis = askQuestion("Please enter file path for " + type + " file: (data/checking.csv sau data/savings.csv) ", null);

        try {
        
        BufferedReader csvReader = new BufferedReader(new FileReader(fis));
       
        
         String row = csvReader.readLine();


         while ( row != null) {
          row = csvReader.readLine();
          if(row == null) { break;}
          String[] data = row.split(",");
          Savings p = new Savings(Integer.parseInt(data[0]), Integer.parseInt(data[1]));
          saves.add(p);
          System.out.println("Ajunge aici");

        }
        for (Savings p : saves) {
            System.out.println(p);
        }
        
        

    }catch(IOException e ){
        System.out.println("File for " + type + " not found, try again.");
    }




}

    private void CitireCustomers(){
        String fis = askQuestion("Please enter file path for customers file: (data/Customers.csv) ", null);

        try {
        
        BufferedReader csvReader = new BufferedReader(new FileReader(fis));
       
        
         String row = csvReader.readLine();


         while ( row != null) {
            // System.out.println("asta merge sigur!");
             row = csvReader.readLine();
             if(row == null) { break;}
             String[] data = row.split(",");
           
             List<Savings> result = saves.stream()
               .filter(item -> item.getAccountNumber() == Integer.parseInt(data[3]))
               .collect(Collectors.toList());
           
             if(result.size() > 0){
                 
                 Savings p = result.get(0);
                 Customer c = new Customer(data[0], data[1], data[2], p);
                 customers.add(c);
                 for(int i=0; i<banci.size(); i++){
                    
                    
                     if(banci.get(i).basicInfo().equals(data[4])) {
                         (banci.get(i)).addCustomer(c);
                         System.out.println("ce pula mea?");
                     }
                 }
               
             }

        }
        for(Customer c : customers) {
            System.out.println("Customer: " + c);
        }
        
      
        
        

    }catch(IOException e ){
        System.out.println("File for customers not found, try again.");
    }
    }

    private void InitFile(String ff) throws IOException{

    FileWriter csvWriter = new FileWriter(ff);
    System.out.println("SMR DE STIU CE ARE VERE + " + ff + "??");
        csvWriter.append("Operatie efectuata");
        csvWriter.append(",");
        csvWriter.append("TimeStamp");
        csvWriter.append("\n");
        x = csvWriter; 
        System.out.println(x);
    }



    private void WriteFile(String message) throws IOException{
        x.append(message);
        x.append(",");
        SimpleDateFormat formatter = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");  
        Date date = new Date();  
       
        x.append(formatter.format(date));
       x.append("\n");
        x.flush();
        
    }

}

